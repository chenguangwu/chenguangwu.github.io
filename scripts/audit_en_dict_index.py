#!/usr/bin/env python3
"""Audit i18n/tools/en/<industry>/_index.json consistency.

The English runtime only requests per-tool dictionaries when the slug is listed
in `_index.json` ("只对已有字典的工具发请求，零 404"). A stale entry therefore
creates a guaranteed 404 request, and a dictionary missing from the index is
never loaded. This gate keeps both directions in sync.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "i18n" / "tools" / "en"
IGNORED = {"_common.json", "_prefix.json"}


def main() -> int:
    errors: list[str] = []
    index_count = 0

    for index_path in sorted(EN_ROOT.glob("*/_index.json")):
        index_count += 1
        industry = index_path.parent.name
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{index_path}: invalid JSON: {exc}")
            continue

        if data.get("industry") != industry:
            errors.append(
                f"{index_path}: industry={data.get('industry')!r} != directory {industry!r}"
            )

        tools = data.get("tools")
        if not isinstance(tools, list):
            errors.append(f"{index_path}: missing tools list")
            continue

        slugs = [str(t) for t in tools]
        if len(slugs) != len(set(slugs)):
            dupes = sorted({s for s in slugs if slugs.count(s) > 1})
            errors.append(f"{index_path}: duplicate slugs {dupes}")

        for slug in slugs:
            target = index_path.parent / f"{slug}.json"
            if not target.exists():
                errors.append(f"{index_path}: listed {slug!r} but {target.name} is missing")

    for industry_dir in sorted(p for p in EN_ROOT.iterdir() if p.is_dir()):
        index_path = industry_dir / "_index.json"
        if not index_path.exists():
            errors.append(f"{industry_dir}: missing _index.json")
            continue
        data = json.loads(index_path.read_text(encoding="utf-8"))
        listed = {str(t) for t in data.get("tools", [])}
        for json_path in sorted(industry_dir.glob("*.json")):
            if json_path.name == "_index.json" or json_path.name in IGNORED:
                continue
            if json_path.stem not in listed:
                errors.append(f"{json_path}: dictionary not listed in {index_path.name}")

    if errors:
        print(f"EN dictionary index audit FAILED: {len(errors)} issue(s)")
        for line in errors:
            print(f"  - {line}")
        return 1

    print(f"EN dictionary index audit PASS: {index_count} industry indexes consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
