"""
Stage 3 of 4: REPORT

Reads oscar_filtered.tsv and produces the final human-readable output:
grouped by film + ceremony year, with a count of how many awards that
film won and its director's birth year.

Output: oscar_report.tsv (+ printed summary table)
"""

import csv, glob
from collections import defaultdict
from datetime import datetime, timezone


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

groups = defaultdict(lambda: {"director": "", "birth_year": "", "awards": set()})
for r in rows:
    key = (r["Ceremony Year"], r["Film"])
    g = groups[key]
    g["director"] = r["Director"]
    g["birth_year"] = r["Director Birth Year"]
    g["awards"].add(r["Award"])

summary = []
for (year, film), g in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    summary.append((year, film, g["director"], g["birth_year"], len(g["awards"])))

run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
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
