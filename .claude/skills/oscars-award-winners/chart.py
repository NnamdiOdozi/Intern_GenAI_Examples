"""
Stage 4 of 4: CHART

Reads oscar_report.tsv and plots, per ceremony year:
  - total award wins by qualifying directors (director born before CUTOFF_YEAR)
  - count of distinct qualifying directors who won that year

Output: oscar_wins_by_year.jpg
"""

import csv, glob
from collections import defaultdict
from datetime import datetime, timezone

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


def latest(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matching {pattern} - run the previous stage first.")
    return files[-1]


in_path = latest("oscar_report_*.tsv")
print(f"Reading {in_path}")

wins_by_year = defaultdict(int)
directors_by_year = defaultdict(set)

with open(in_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for r in reader:
        y = int(r["Ceremony Year"])
        wins_by_year[y] += int(r["Awards Won"])
        directors_by_year[y].add(r["Director"])

years = list(range(min(wins_by_year), max(wins_by_year) + 1))
wins = [wins_by_year.get(y, 0) for y in years]
directors = [len(directors_by_year.get(y, set())) for y in years]

run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
out_path = f"oscar_wins_by_year_{run_ts}.jpg"

if plt is not None:
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(years, wins, color="#2a78d6", linewidth=2, marker="o", markersize=4, label="Award wins")
    ax.plot(years, directors, color="#1baf7a", linewidth=2, linestyle="--", marker="o", markersize=4, label="Distinct directors")

    ax.set_ylabel("Count")
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
else:
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1650, 750
    left, top, right, bottom = 110, 70, 50, 125
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=20)
    small = ImageFont.load_default(size=16)
    plot_w = width - left - right
    plot_h = height - top - bottom
    maximum = max(max(wins), max(directors), 1)
    y_max = ((maximum + 4) // 5) * 5

    def point(index, value):
        x = left + index * plot_w / max(len(years) - 1, 1)
        y = top + plot_h - value * plot_h / y_max
        return x, y

    for value in range(0, y_max + 1, 5):
        y = point(0, value)[1]
        draw.line((left, y, width - right, y), fill="#e1e0d9", width=2)
        draw.text((left - 55, y - 10), str(value), fill="#333333", font=small)

    for color, values in (("#2a78d6", wins), ("#1baf7a", directors)):
        points = [point(i, value) for i, value in enumerate(values)]
        draw.line(points, fill=color, width=4)
        for x, y in points:
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)

    for index, year in enumerate(years):
        if index % 2 == 0 or index == len(years) - 1:
            x, _ = point(index, 0)
            draw.text((x - 20, height - bottom + 18), str(year), fill="#333333", font=small)

    draw.text((left, 20), "Oscar wins by qualifying directors", fill="#222222", font=font)
    draw.text((left, height - 35), "Ceremony year", fill="#333333", font=small)
    draw.text((15, top), "Count", fill="#333333", font=small)
    draw.line((width - 430, 28, width - 380, 28), fill="#2a78d6", width=4)
    draw.text((width - 365, 18), "Award wins", fill="#222222", font=small)
    draw.line((width - 230, 28, width - 180, 28), fill="#1baf7a", width=4)
    draw.text((width - 165, 18), "Directors", fill="#222222", font=small)
    image.save(out_path, quality=92)

print(f"Written to {out_path}")
