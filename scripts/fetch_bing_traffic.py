#!/usr/bin/env python3
"""Export Bing Webmaster query and page traffic stats as a candidate CSV."""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://ssl.bing.com/webmaster/api.svc/json"
DEFAULT_SITE = "https://chenguangwu.github.io/"


def get_json(endpoint: str, api_key: str, site_url: str) -> list[dict]:
    params = urllib.parse.urlencode({"apikey": api_key, "siteUrl": site_url})
    url = f"{API_BASE}/{endpoint}?{params}"
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
            return payload.get("d", []) or []
        except (urllib.error.HTTPError, urllib.error.URLError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    return []


def number(value: object) -> str:
    return "" if value is None else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", default=DEFAULT_SITE)
    parser.add_argument("--output", type=Path, default=Path("bing_traffic_export.csv"))
    args = parser.parse_args()

    api_key = os.environ.get("BING_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("请先设置 BING_API_KEY")

    query_rows = get_json("GetQueryStats", api_key, args.site_url)
    page_rows = get_json("GetPageStats", api_key, args.site_url)
    with args.output.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["query", "page", "impressions", "clicks", "ctr", "position"])
        for row in query_rows:
            impressions = row.get("Impressions", 0)
            clicks = row.get("Clicks", 0)
            ctr = float(clicks) / float(impressions) if impressions else 0
            writer.writerow([
                row.get("Query", ""), "", number(impressions), number(clicks), ctr,
                number(row.get("AvgImpressionPosition")),
            ])
        for row in page_rows:
            impressions = row.get("Impressions", 0)
            clicks = row.get("Clicks", 0)
            ctr = float(clicks) / float(impressions) if impressions else 0
            writer.writerow([
                "", row.get("Query", ""), number(impressions), number(clicks), ctr,
                number(row.get("AvgImpressionPosition")),
            ])
    print(f"已写入 {args.output}: queries={len(query_rows)}, pages={len(page_rows)}")


if __name__ == "__main__":
    main()
