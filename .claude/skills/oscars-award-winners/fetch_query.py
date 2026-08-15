"""
Stage 1 of 4: FETCH

Pulls a wide, unfiltered set of Academy Award wins from Wikidata:
- every award category (found dynamically by label match, not hardcoded)
- full history, 1929 to present (no year floor)
- both film-level wins (e.g. Best Picture) and person-level wins
  (e.g. Best Director, Best Sound Editing) with the film they relate to

Director and director birth year are looked up OPTIONALly, so a film
missing that data on Wikidata still appears in the raw output (with
blank fields) rather than being silently dropped. Filtering (birth-year
cutoff, dropping incomplete rows) happens in filter_validate.py, not here.

Output: oscar_raw.tsv
"""

import urllib.request, urllib.parse, json, csv, time
from datetime import datetime
from zoneinfo import ZoneInfo

# Sortable, filesystem-safe timestamp (no colons) - shared by the filename
# of everything this run produces, so it's obvious at a glance which raw
# pull a given filtered/report/chart file was built from. Local London
# time (auto BST/GMT), not UTC - matches the user's wall clock.
RUN_TS = datetime.now(ZoneInfo("Europe/London")).strftime("%Y%m%dT%H%M%S")

PREFIXES = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""


def run_sparql(query, retries=3):
    # WDQS occasionally returns transient 502/504s under load even for
    # queries that run fine seconds later - a short retry is standard
    # practice against this endpoint, not a workaround for anything
    # specific to this sandbox.
    url = "https://query.wikidata.org/sparql"
    full = PREFIXES + query
    params = urllib.parse.urlencode({"query": full, "format": "json"})
    req = urllib.request.Request(
        f"{url}?{params}",
        headers={"User-Agent": "OscarAwardWinnersSkill/1.0 (educational)"}
    )
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read())["results"]["bindings"]
        except urllib.error.HTTPError as e:
            if e.code in (502, 503, 504) and attempt < retries:
                print(f"  got HTTP {e.code}, retrying ({attempt}/{retries})...")
                time.sleep(5)
                continue
            raise


# Step 1: find every Academy Award category QID
#
# NOTE: originally this scanned all Wikidata labels for
# FILTER(STRSTARTS(?name, "Academy Award")) - that full-table label scan
# reliably times out server-side (HTTP 504, WDQS enforces a ~60s query
# budget) regardless of network access. Replaced with a UNION of indexed
# property lookups instead: category items are linked to the Academy
# Awards via P1027 (conferred by -> Q212329 AMPAS), P361 (part of ->
# Q19020 Academy Awards), and/or P31 (instance of -> Q19020). No single
# one of these three is complete on its own (older/short-film categories
# are inconsistently tagged), so we UNION all three and dedupe. This
# returns ~70 categories (vs the ~34 P1027 alone gives you) in well
# under a second instead of timing out.
print("Step 1: finding all Academy Award categories...")
cat_q = """
SELECT DISTINCT ?award ?awardLabel WHERE {
  { ?award wdt:P1027 wd:Q212329 . }
  UNION
  { ?award wdt:P361 wd:Q19020 . }
  UNION
  { ?award wdt:P31 wd:Q19020 . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
"""
cats = run_sparql(cat_q)
qids = list({c["award"]["value"].split("/")[-1] for c in cats})
print(f"  Found {len(qids)} categories")

values_clause = "VALUES ?award { " + " ".join(f"wd:{q}" for q in qids) + " }"

# Step 2: film-level awards (e.g. Best Picture) - no year floor
print("\nStep 2: film-level awards (full history)...")
q_film = f"""
SELECT DISTINCT ?filmLabel ?awardLabel ?year ?directorLabel ?birthYear WHERE {{
  {values_clause}
  ?film p:P166 ?s .
  ?s ps:P166 ?award .
  ?s pq:P585 ?date .
  BIND(YEAR(?date) AS ?year)
  OPTIONAL {{
    ?film wdt:P57 ?director .
    OPTIONAL {{ ?director wdt:P569 ?b . BIND(YEAR(?b) AS ?birthYear) }}
  }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}} ORDER BY ?year ?filmLabel
"""
r_film = run_sparql(q_film)
print(f"  Got {len(r_film)} rows")

# Step 3: person-level awards (e.g. Best Director, Best Sound Editing) - no year floor
print("\nStep 3: person-level awards (full history)...")
q_person = f"""
SELECT DISTINCT ?filmLabel ?awardLabel ?year ?directorLabel ?birthYear WHERE {{
  {values_clause}
  ?person p:P166 ?s .
  ?s ps:P166 ?award .
  ?s pq:P1686 ?film .
  ?s pq:P585 ?date .
  BIND(YEAR(?date) AS ?year)
  OPTIONAL {{
    ?film wdt:P57 ?director .
    OPTIONAL {{ ?director wdt:P569 ?b . BIND(YEAR(?b) AS ?birthYear) }}
  }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}} ORDER BY ?year ?filmLabel
"""
r_person = run_sparql(q_person)
print(f"  Got {len(r_person)} rows")


def parse(bindings):
    rows = []
    for r in bindings:
        rows.append((
            r.get("year", {}).get("value", ""),
            r.get("filmLabel", {}).get("value", ""),
            r.get("awardLabel", {}).get("value", ""),
            r.get("directorLabel", {}).get("value", ""),
            r.get("birthYear", {}).get("value", ""),
        ))
    return rows


all_rows = parse(r_film) + parse(r_person)

# Drop exact duplicate rows only (not a business-logic filter - just dedup)
seen = set()
deduped = []
for row in all_rows:
    if row not in seen:
        seen.add(row)
        deduped.append(row)
deduped.sort(key=lambda r: (r[0], r[1], r[2]))

out_path = f"oscar_raw_{RUN_TS}.tsv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["Ceremony Year", "Film", "Award", "Director", "Director Birth Year"])
    w.writerows(deduped)

print(f"\nTotal raw rows (deduped): {len(deduped)}")
print(f"Written to {out_path} - no filtering applied yet, run filter_validate.py next.")
