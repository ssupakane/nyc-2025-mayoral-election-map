# NYC 2025 mayoral election map

An interactive, election-district map of New York City's **November 4, 2025 mayoral general election**. The map keeps the visual design and interaction model of [NYC 2026 election map](https://github.com/ssupakane/nyc-2026-election-map), with 2025 mayoral results and the 2025 election-district boundaries.

## Map

Open [index.html](https://ssupakane.github.io/nyc-2025-mayoral-election-map/) after enabling GitHub Pages for the `main` branch (root).

Run locally with a static server:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000/.

The map is shaded by **Cuomo's share of the Mamdani + Cuomo vote** in each election district: blue indicates Mamdani-heavy districts, cream is even, and red indicates Cuomo-heavy districts. Select an election district or assembly district to inspect candidate-level totals.

## Results

Citywide figures use the NYC Board of Elections' certified 2025 general-election recap. District results use the Board of Elections' published election-district-level CSV for the Citywide Mayor contest.

| Candidate | Certified citywide votes |
| --- | ---: |
| Zohran Kwame Mamdani | 1,114,184 |
| Andrew M. Cuomo | 906,614 |
| Curtis A. Sliwa | 153,749 |
| Eric L. Adams | 6,897 |

The district file reports results by election district. Its sums should not be substituted for the certified citywide recap; the map keeps those two reporting levels distinct. The district detail panel shows the district-level candidate counts available in the ED-level dataset.

## Geography

The map uses NYC Department of City Planning election-district boundaries, **release 25C** (published August 18, 2025), which is the appropriate boundary vintage for the 2025 election. The shapefile is read in the browser using [shpjs 6.2.0](https://www.npmjs.com/package/shpjs) from the archived 25C shapefile in [ry-li/map-nyc-election](https://github.com/ry-li/map-nyc-election). The shapefile metadata identifies NYC DCP as the source.

## Rebuild the district CSV

The source file is the BOE's published Citywide Mayor ED-Level CSV, linked from the [2025 Election Results Summary](https://vote.nyc/page/election-results-summary-2025).

Install the dependency and run:

```sh
python3 -m pip install pandas
python3 scripts/build_2025_results.py
```

The script downloads the BOE CSV, combines party lines for each candidate within each election district, and writes `data/results_2025_mayor.csv`.

## Sources

- **Official certified citywide results and ED-Level CSV:** [NYC Board of Elections — Election Results Summary 2025](https://vote.nyc/page/election-results-summary-2025)
- **Election-district boundaries:** NYC Department of City Planning, BYTES of the BIG APPLE, release 25C (August 18, 2025); metadata is included with the archived shapefile.
- **Boundary archive used by the browser:** [ry-li/map-nyc-election — nyed_25c.zip](https://github.com/ry-li/map-nyc-election/tree/main/general-mayoral-enr/shapefile)

## Credits

The map layout and interaction design are adapted from [ssupakane/nyc-2026-election-map](https://github.com/ssupakane/nyc-2026-election-map). The original repository is unchanged.
