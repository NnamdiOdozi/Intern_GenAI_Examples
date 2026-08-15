"""
Stage 5 (additive, optional): DETERMINISTIC VALIDATE

Does NOT touch fetch_query.py / filter_validate.py / report.py / chart.py
or their outputs - this is a read-only QA pass over the existing
deliverable, run separately, that flags suspected data-quality issues
for human (or agent) review. It never modifies oscar_report.tsv itself.

Reads the latest oscar_filtered_*.tsv (the pre-report, per-award-row
data - needed because the cross-year duplicate check below relies on
the Award column, which report.py's grouping step collapses away).

Checks applied (deterministic, rule-based - added incrementally as
issues were found by manual/agent review, see oscar_review_*.md):

1. Cross-year duplicate: the same (Film, Award, Director) triple
   appearing under more than one distinct Ceremony Year. This is
   scoped tightly to all three fields matching, not just film title -
   a film legitimately winning several *different* awards is normal
   and must not be flagged.

2. Unresolved Wikidata label: a Director OR Film value that is just a
   raw Wikidata QID (e.g. "Q42101") rather than a resolved name - a
   label service gap, not necessarily a missing-data gap. Checked on
   both columns because the Film column has the same failure mode and
   it's already live in the raw data (59 rows) - it just hasn't shown
   up in a filtered/report file yet because the affected films'
   directors happen to fail the birth-year cutoff. Change CUTOFF_YEAR
   in filter_validate.py and this blind spot stops being theoretical.

3. Multi-director split across the cutoff: a (Film, Award) pair with
   more than one distinct credited director in the RAW data, where the
   birth years span the cutoff (at least one director qualifies, at
   least one doesn't). filter_validate.py evaluates each raw row
   independently, so a film survives into the deliverable as soon as
   ANY listed director qualifies - which is sometimes right (a true
   co-directing team, e.g. the Coen brothers) and sometimes misleading
   (e.g. a director credited only for a regional/dubbed version, not
   the version that actually won). This check can't tell those two
   cases apart automatically - it surfaces both for a human/agent to
   judge. Reads oscar_raw_*.tsv rather than oscar_filtered_*.tsv,
   because the whole point is to see directors that the cutoff already
   excluded from the filtered file.
   CUTOFF_YEAR/YEAR_FLOOR below must be kept in sync with
   filter_validate.py by hand if those are ever changed there.

Output: oscar_flags_<timestamp>.tsv
"""

import csv, glob, re
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

CUTOFF_YEAR = 1955  # keep in sync with filter_validate.py
YEAR_FLOOR = 1996  # keep in sync with filter_validate.py


def latest(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matching {pattern} - run the previous stage first.")
    return files[-1]


in_path = latest("oscar_filtered_*.tsv")
print(f"Reading {in_path}")

with open(in_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)

flags = []

# Check 1: cross-year duplicate (Film, Award, Director) triples
groups = defaultdict(set)
group_rows = defaultdict(list)
for r in rows:
    key = (r["Film"], r["Award"], r["Director"])
    groups[key].add(r["Ceremony Year"])
    group_rows[key].append(r)

for key, years in groups.items():
    if len(years) > 1:
        film, award, director = key
        years_str = ", ".join(sorted(years))
        for r in group_rows[key]:
            flags.append({
                "Flag Type": "cross_year_duplicate",
                "Ceremony Year": r["Ceremony Year"],
                "Film": film,
                "Award": award,
                "Director": director,
                "Detail": f"Same film+award+director also recorded under year(s): {years_str}",
            })

# Check 2: unresolved Wikidata QID standing in for a director's or film's name
qid_pattern = re.compile(r"^Q\d+$")
for r in rows:
    if qid_pattern.match(r["Director"]):
        flags.append({
            "Flag Type": "unresolved_label",
            "Ceremony Year": r["Ceremony Year"],
            "Film": r["Film"],
            "Award": r["Award"],
            "Director": r["Director"],
            "Detail": "Director shows as a raw Wikidata ID - the label service had no English label for this item",
        })
    if qid_pattern.match(r["Film"]):
        flags.append({
            "Flag Type": "unresolved_label",
            "Ceremony Year": r["Ceremony Year"],
            "Film": r["Film"],
            "Award": r["Award"],
            "Director": r["Director"],
            "Detail": "Film shows as a raw Wikidata ID - the label service had no English label for this item",
        })

# Check 3: multi-director (Film, Award) pairs whose birth years span CUTOFF_YEAR
raw_path = latest("oscar_raw_*.tsv")
print(f"Reading {raw_path} (for the multi-director check only)")
with open(raw_path, newline="", encoding="utf-8") as f:
    raw_rows = list(csv.DictReader(f, delimiter="\t"))

directors_by_film_award = defaultdict(set)
for r in raw_rows:
    if not r["Ceremony Year"] or int(r["Ceremony Year"]) < YEAR_FLOOR:
        continue
    if not r["Director"] or not r["Director Birth Year"]:
        continue
    key = (r["Film"], r["Award"])
    directors_by_film_award[key].add((r["Director"], r["Director Birth Year"]))

for (film, award), directors in directors_by_film_award.items():
    if len(directors) < 2:
        continue
    years = [int(y) for _, y in directors]
    if min(years) < CUTOFF_YEAR <= max(years):
        directors_str = "; ".join(f"{d} (b.{y})" for d, y in sorted(directors, key=lambda x: x[1]))
        # Find the ceremony year(s) this (film, award) pair actually appeared under
        ceremony_years = sorted({r["Ceremony Year"] for r in raw_rows if r["Film"] == film and r["Award"] == award})
        flags.append({
            "Flag Type": "multi_director_split_cutoff",
            "Ceremony Year": "/".join(ceremony_years),
            "Film": film,
            "Award": award,
            "Director": directors_str,
            "Detail": "Multiple credited directors, birth years span the cutoff - film is included based on whichever director happened to qualify, which may not reflect who was actually recognized for this award",
        })

run_ts = datetime.now(ZoneInfo("Europe/London")).strftime("%Y%m%dT%H%M%S")
out_path = f"oscar_flags_{run_ts}.tsv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Flag Type", "Ceremony Year", "Film", "Award", "Director", "Detail"]
    w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    w.writeheader()
    w.writerows(flags)

by_type = defaultdict(int)
for fl in flags:
    by_type[fl["Flag Type"]] += 1

print(f"\nRows checked: {len(rows)}")
for t, n in by_type.items():
    print(f"  {t}: {n} flagged rows")
print(f"\nWritten to {out_path}")
print("Note: this does NOT modify oscar_report.tsv or oscar_filtered.tsv - review only.")
