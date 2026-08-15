"""
Stage 3 of 4: REPORT

Reads oscar_filtered.tsv and produces the final human-readable output:
grouped by film + ceremony year, with a count of how many awards that
film won and its director(s)' birth year(s).

Co-directors are aggregated (not overwritten) when a film has more than
one qualifying director row. Films split across two adjacent ceremony
years with an overlapping director are merged into one row under the
later year - a known Wikidata quirk (nomination date vs. ceremony date
sometimes land in different years for the same award). Merge never
happens without a shared director, so two different films that happen
to share a title are never collapsed into each other.

Output: oscar_report.tsv (+ printed summary table)
"""

import csv, glob
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo


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

groups = defaultdict(lambda: {"directors": {}, "awards": set()})
for r in rows:
    key = (r["Ceremony Year"], r["Film"])
    g = groups[key]
    if r["Director"]:
        g["directors"][r["Director"]] = r["Director Birth Year"]
    g["awards"].add(r["Award"])

# Merge same-film entries split across adjacent ceremony years, but only
# when they share a director - see module docstring.
by_film = defaultdict(list)
for (year, film), g in groups.items():
    by_film[film].append((year, g))

merged = {}
for film, entries in by_film.items():
    entries.sort(key=lambda e: e[0])
    kept = []
    for year, g in entries:
        prev = kept[-1] if kept else None
        if prev and int(year) - int(prev[0]) == 1 and set(prev[1]["directors"]) & set(g["directors"]):
            prev_year, prev_g = kept.pop()
            prev_g["directors"].update(g["directors"])
            prev_g["awards"].update(g["awards"])
            kept.append((year, prev_g))  # keep the later of the two years
        else:
            kept.append((year, g))
    for year, g in kept:
        merged[(year, film)] = g

summary = []
for (year, film), g in sorted(merged.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    directors = sorted(g["directors"])
    summary.append((
        year, film,
        "; ".join(directors),
        "; ".join(g["directors"][d] for d in directors),
        len(g["awards"]),
    ))

run_ts = datetime.now(ZoneInfo("Europe/London")).strftime("%Y%m%dT%H%M%S")
out_path = f"oscar_report_{run_ts}.tsv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["Ceremony Year", "Film", "Director", "Director Birth Year", "Awards Won"])
    w.writerows(summary)

print(f"{'Year':<6} {'Film':<45} {'Director':<25} {'Born':<6} Awards")
print("-" * 95)
for row in summary:
    print(f"{row[0]:<6} {row[1]:<45} {row[2]:<25} {row[3]:<6} {row[4]}")

print(f"\nTotal films: {len(summary)}")
print(f"Total award wins: {sum(r[4] for r in summary)}")
print(f"Full detail in {out_path}")
