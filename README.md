# NYC 2025 mayoral election map

An interactive, election-district map of New York City's **November 4, 2025 mayoral general election**. The map keeps the visual design and interaction model of [NYC 2026 election map](https://github.com/ssupakane/nyc-2026-election-map), with the 2025 mayoral contest and the 2025 election-district boundaries.

## Map

Open [index.html](https://ssupakane.github.io/nyc-2025-mayoral-election-map/) after enabling GitHub Pages for the `main` branch (root).

Run locally with a static server:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000/.

Each district is ranked across all seven named candidates. Districts led by Mamdani or Cuomo use the original continuous blue–neutral–red gradient, based on their two-candidate share. Districts led by Sliwa, Adams, Estrada, Walden, or Hernandez use distinct colors. The detail panel shows all seven candidates and the actual first- and second-place finishers; exact ties use a neutral map color.

## Citywide certified results

The citywide figures below are from the NYC Board of Elections' certified 2025 general-election recap (certified December 2, 2025).

| Candidate | Certified citywide votes |
| --- | ---: |
| Zohran Kwame Mamdani | 1,114,184 |
| Andrew M. Cuomo | 906,614 |
| Curtis A. Sliwa | 153,749 |
| Eric L. Adams | 6,897 |
| Irene Estrada | 2,856 |
| Jim Walden | 2,319 |
| Joseph Hernandez | 1,379 |

## District-level data caveat

The checked-in map CSV is an archived, normalized version of the public election-district returns. It covers 4,117 election districts and agrees with the certified citywide totals for the six named candidates other than Cuomo. The district CSV sums to **901,253 Cuomo votes**, which is **5,361 fewer** than the certified citywide total of 906,614.

The app deliberately keeps the two reporting levels separate: citywide scorecards show the certified recap; district shading and district detail cards use the archived ED-level file without scaling or allocating the difference. District results should therefore not be described as certified precinct-level totals. The map color and district lead line compare all seven named candidates. The detail panel lists named-candidate returns; write-in votes are not included in its candidate total.

The checked-in ED CSV was normalized from the public file in [joshgreenman1973/nyc-election-archive](https://github.com/joshgreenman1973/nyc-election-archive/blob/main/data/normalized/2025_general_mayor_ed_results.csv), whose project documents BOE ED-level results as its source. The [official BOE results page](https://vote.nyc/page/election-results-summary-2025) also publishes the certified Citywide Mayor ED-Level CSV.

## Geography

The map uses NYC Department of City Planning election-district boundaries, **release 25C** (published August 18, 2025), the boundary vintage for the 2025 election. The browser loads the archived 25C shapefile from [ry-li/map-nyc-election](https://github.com/ry-li/map-nyc-election/tree/main/general-mayoral-enr/shapefile) and converts it to GeoJSON with [shpjs 6.2.0](https://www.npmjs.com/package/shpjs). The shapefile metadata identifies NYC DCP as the source.

## Rebuild the district CSV

The build script downloads the BOE's Citywide Mayor ED-Level CSV from the [2025 Election Results Summary](https://vote.nyc/page/election-results-summary-2025), combines party lines for each candidate within each election district, and writes `data/results_2025_mayor.csv`.

Install the dependency and run:

```sh
python3 -m pip install pandas
python3 scripts/build_2025_results.py
```

**Safety check:** the script compares all seven candidate totals with the certified citywide recap and refuses to overwrite the checked-in CSV if any candidate total differs. A successful rebuild is therefore required before the district file can be treated as reconciled to the certified totals.

## Sources

- **Certified citywide results and certified ED-Level CSV:** [NYC Board of Elections — Election Results Summary 2025](https://vote.nyc/page/election-results-summary-2025)
- **District CSV currently checked in:** [NYC election archive — 2025 general mayor ED results](https://github.com/joshgreenman1973/nyc-election-archive/blob/main/data/normalized/2025_general_mayor_ed_results.csv)
- **Election-district boundaries:** NYC Department of City Planning, BYTES of the BIG APPLE, release 25C (August 18, 2025); shapefile metadata is included in the boundary archive.
- **Boundary archive:** [ry-li/map-nyc-election — nyed_25c.zip](https://github.com/ry-li/map-nyc-election/tree/main/general-mayoral-enr/shapefile)

## Credits

The map layout and interaction design are adapted from [ssupakane/nyc-2026-election-map](https://github.com/ssupakane/nyc-2026-election-map). The original repository is unchanged.
