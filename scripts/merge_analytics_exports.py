#!/usr/bin/env python3
"""Merge analytics exports into one source-labelled CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = ["query", "page", "impressions", "clicks", "ctr", "position"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return [{field: (row.get(field) or "").strip() for field in FIELDS} for row in reader]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clarity", type=Path, default=Path("clarity_traffic_export.csv"))
    parser.add_argument("--bing", type=Path, default=Path("bing_traffic_export.csv"))
    parser.add_argument("--51la", dest="la", type=Path)
    parser.add_argument("--output", type=Path, default=Path("analytics_traffic_merged.csv"))
    args = parser.parse_args()

    inputs = [("clarity", args.clarity), ("bing", args.bing)]
    if args.la:
        inputs.append(("51la", args.la))

    total = 0
    counts: dict[str, int] = {}
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["source", "source_row", *FIELDS])
        writer.writeheader()
        for source, path in inputs:
            if not path.exists():
                continue
            rows = read_rows(path)
            counts[source] = len(rows)
            for index, row in enumerate(rows, start=2):
                writer.writerow({"source": source, "source_row": index, **row})
                total += 1

    print(f"已写入 {args.output}: total={total}, " + ", ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
