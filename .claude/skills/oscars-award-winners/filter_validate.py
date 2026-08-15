"""
Stage 2 of 4: FILTER + VALIDATE

Reads oscar_raw.tsv (wide, unfiltered) and:
  1. applies the ceremony year floor: Ceremony Year >= YEAR_FLOOR
  2. reports data-quality counts (missing director, missing birth year)
     scoped to that post-YEAR_FLOOR set
  3. drops rows that can't be checked against the cutoff (no birth year)
  4. applies the age cutoff: director_birth_year < CUTOFF_YEAR

Change CUTOFF_YEAR or YEAR_FLOOR below to re-run with different
thresholds without re-fetching from Wikidata.

Output: oscar_filtered.tsv
"""

import csv, glob
from datetime import datetime
from zoneinfo import ZoneInfo

CUTOFF_YEAR = 1960  # keep films where the director was born before this year
YEAR_FLOOR = 1996  # keep films whose Oscar ceremony was in this year or later


def latest(pattern):
    # Filenames carry a sortable UTC timestamp (YYYYMMDDTHHMMSSZ), so the
    # lexicographically last match is always the most recent run - no need
    # to trust file mtimes, which don't survive being copied elsewhere.
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matching {pattern} - run the previous stage first.")
    return files[-1]


in_path = latest("oscar_raw_*.tsv")
print(f"Reading {in_path}")

with open(in_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    all_rows = list(reader)

# Apply ceremony year floor first - everything below scopes to this set
rows = [r for r in all_rows if int(r["Ceremony Year"]) >= YEAR_FLOOR]
dropped_before_floor = len(all_rows) - len(rows)

total = len(rows)
missing_director = sum(1 for r in rows if not r["Director"])
missing_birth_year = sum(1 for r in rows if not r["Director Birth Year"])

print(f"Raw rows read: {len(all_rows)}")
print(f"Dropped (ceremony year before {YEAR_FLOOR}): {dropped_before_floor}")
print(f"Rows from {YEAR_FLOOR} onward: {total}")
print(f"  Missing director: {missing_director}")
print(f"  Missing director birth year: {missing_birth_year}")

# Can't apply the cutoff without a birth year - drop those, but report the count
usable = [r for r in rows if r["Director Birth Year"]]
dropped_no_birth_year = total - len(usable)

# Apply cutoff
kept = [r for r in usable if int(r["Director Birth Year"]) < CUTOFF_YEAR]

print(f"\nDropped (no birth year, can't check cutoff): {dropped_no_birth_year}")
print(f"Cutoff applied: director born before {CUTOFF_YEAR}")
print(f"Rows kept: {len(kept)} of {total}")

run_ts = datetime.now(ZoneInfo("Europe/London")).strftime("%Y%m%dT%H%M%S")
out_path = f"oscar_filtered_{run_ts}.tsv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Ceremony Year", "Film", "Award", "Director", "Director Birth Year"]
    w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    w.writeheader()
    w.writerows(kept)

print(f"\nWritten to {out_path} - run report.py next.")
