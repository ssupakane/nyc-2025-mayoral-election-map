#!/usr/bin/env python3
"""Build a map-ready 2025 NYC mayoral result CSV from the BOE ED-Level CSV.

The BOE publishes the certified Citywide Mayor ED-Level CSV on its 2025
Election Results Summary page. The CSV has appeared both as an ordinary
11-column file and as a 22-column export with its header repeated in the
first half of every row; read_edlevel_csv handles both formats.
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

BOE_CSV_URL = (
    "https://vote.nyc/sites/default/files/pdf/election_results/2025/"
    "20251104General%20Election/"
    "00000100000Citywide%20Mayor%20Citywide%20EDLevel.csv"
)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results_2025_mayor.csv"

EXPECTED_COLS = [
    "AD", "ED", "County", "EDAD Status", "Event", "Party/Independent Body",
    "Office/Position Title", "District Key", "VoteFor", "Unit Name", "Tally",
]
NAME_PARTY_RE = re.compile(r"^(.+?)\\s*\\(([^()]+)\\)\\s*$")

CANDIDATE_FIELDS = {
    "Zohran Kwame Mamdani": "mamdani",
    "Andrew M. Cuomo": "cuomo",
    "Curtis A. Sliwa": "sliwa",
    "Eric L. Adams": "adams",
    "Irene Estrada": "estrada",
    "Jim Walden": "walden",
    "Joseph Hernandez": "hernandez",
}
FIELDS = list(CANDIDATE_FIELDS.values())
OUTPUT_COLS = ["elect_dist", "ad", "ed", *FIELDS, "total", "cuomo_share"]


def read_edlevel_csv(source: str = BOE_CSV_URL) -> pd.DataFrame:
    """Read either normal 11-column or duplicated-header 22-column BOE CSV."""
    raw = pd.read_csv(source, header=None, dtype=str, keep_default_na=False)
    if raw.shape[1] == len(EXPECTED_COLS):
        df = raw.iloc[1:].copy()
        df.columns = raw.iloc[0].tolist()
    elif raw.shape[1] == 2 * len(EXPECTED_COLS):
        df = raw.iloc[:, len(EXPECTED_COLS):].copy()
        df.columns = EXPECTED_COLS
    else:
        raise ValueError(f"Unexpected ED-Level CSV shape: {raw.shape}")
    return df.reset_index(drop=True)


def candidate_name(unit_name: str) -> str:
    """Remove a party suffix, leaving the canonical candidate name."""
    if not isinstance(unit_name, str):
        return ""
    match = NAME_PARTY_RE.match(unit_name.strip())
    return match.group(1).strip() if match else ""


def main() -> None:
    df = read_edlevel_csv()
    df = df[df["Office/Position Title"].astype(str).str.strip() == "Mayor"].copy()
    df["AD"] = pd.to_numeric(df["AD"], errors="coerce")
    df["ED"] = pd.to_numeric(df["ED"], errors="coerce")
    df["Tally"] = pd.to_numeric(df["Tally"], errors="coerce").fillna(0).astype(int)
    df = df.dropna(subset=["AD", "ED"])
    df["ad"] = df["AD"].astype(int)
    df["ed_number"] = df["ED"].astype(int)
    df["elect_dist"] = df["ad"] * 1000 + df["ed_number"]
    df["candidate"] = df["Unit Name"].map(candidate_name)
    df["field"] = df["candidate"].map(CANDIDATE_FIELDS)
    df = df[df["field"].notna()]

    totals: dict[int, dict[str, int]] = defaultdict(lambda: {field: 0 for field in FIELDS})
    for row in df.itertuples(index=False):
        ed_id = int(row.elect_dist)
        totals[ed_id][row.field] += int(row.Tally)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLS)
        writer.writeheader()
        for ed_id in sorted(totals):
            votes = totals[ed_id]
            mamdani_cuomo = votes["mamdani"] + votes["cuomo"]
            record = {
                "elect_dist": ed_id,
                "ad": ed_id // 1000,
                "ed": ed_id % 1000,
                **votes,
                "total": sum(votes.values()),
                "cuomo_share": (
                    votes["cuomo"] / mamdani_cuomo if mamdani_cuomo else 0.5
                ),
            }
            writer.writerow(record)
            written += 1

    print(f"Wrote {written:,} election districts to {OUT}")
    for field in FIELDS:
        print(f"{field:12s} {sum(row[field] for row in totals.values()):,}")


if __name__ == "__main__":
    main()
