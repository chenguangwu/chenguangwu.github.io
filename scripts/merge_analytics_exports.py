#!/usr/bin/env python3
"""Merge analytics exports into one source-labelled CSV."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse


FIELDS = ["query", "page", "impressions", "clicks", "ctr", "position"]
SITE_ORIGIN = "https://chenguangwu.github.io"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return [{field: (row.get(field) or "").strip() for field in FIELDS} for row in reader]


def page_exists(page: str) -> bool:
    """Keep only current project pages and exclude the retired evernode area."""
    if not page:
        return True
    parsed = urlparse(page)
    if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        return False
    if parsed.netloc and parsed.netloc != urlparse(SITE_ORIGIN).netloc:
        return False
    path = unquote(parsed.path or "/")
    if path == "/evernode" or path.startswith("/evernode/"):
        return False
    relative = path.lstrip("/")
    target = PROJECT_ROOT / relative
    if path.endswith("/"):
        target = target / "index.html"
    return target.is_file() or (path == "/" and (PROJECT_ROOT / "index.html").is_file())


def normalize_page(page: str) -> str:
    parsed = urlparse(page)
    path = unquote(parsed.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return f"{SITE_ORIGIN}{path}"


def aggregate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, dict[str, object]] = defaultdict(
        lambda: {"impressions": 0.0, "clicks": 0.0, "position_weight": 0.0,
                 "position_impressions": 0.0, "sources": set(), "records": 0}
    )
    for row in rows:
        page = normalize_page(row["page"])
        item = grouped[page]
        impressions = float(row["impressions"] or 0)
        clicks = float(row["clicks"] or 0)
        item["impressions"] += impressions
        item["clicks"] += clicks
        position = float(row["position"] or 0)
        if position and impressions:
            item["position_weight"] += position * impressions
            item["position_impressions"] += impressions
        item["sources"].add(row["source"])
        item["records"] += 1

    result = []
    for page, item in grouped.items():
        impressions = item["impressions"]
        clicks = item["clicks"]
        result.append({
            "page": page,
            "impressions": str(int(impressions) if impressions.is_integer() else impressions),
            "clicks": str(int(clicks) if clicks.is_integer() else clicks),
            "ctr": f"{clicks / impressions:.6f}" if impressions else "0",
            "position": f"{item['position_weight'] / item['position_impressions']:.2f}"
            if item["position_impressions"] else "",
            "sources": ",".join(sorted(item["sources"])),
            "record_count": str(item["records"]),
        })
    return sorted(result, key=lambda row: (-float(row["impressions"]), -float(row["clicks"]), row["page"]))


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

    raw_rows = []
    counts: dict[str, int] = {}
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        for source, path in inputs:
            if not path.exists():
                continue
            rows = read_rows(path)
            counts[source] = len(rows)
            for index, row in enumerate(rows, start=2):
                if not page_exists(row["page"]):
                    continue
                row["source"] = source
                raw_rows.append(row)

        merged_rows = aggregate_rows(raw_rows)
        writer = csv.DictWriter(stream, fieldnames=["page", "impressions", "clicks", "ctr", "position", "sources", "record_count"])
        writer.writeheader()
        writer.writerows(merged_rows)

    print(f"已写入 {args.output}: urls={len(merged_rows)}, " + ", ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
