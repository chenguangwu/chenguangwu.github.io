#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""导出全量 C 级工具治理清单（P0-2 用）。"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TOOLS_JSON = ROOT / "json" / "tools.json"
TOOLS_DIR = ROOT / "tools"

INPUT_RE = re.compile(r"<input\b", re.IGNORECASE)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="", help="导出 JSON 文件")
    ap.add_argument("--md", default="", help="导出 Markdown 清单")
    ap.add_argument("--industry", action="append", default=[], help="按行业过滤（可重复）")
    return ap.parse_args()


def read_tools():
    with open(TOOLS_JSON, encoding="utf-8") as f:
        return json.load(f)


def has_file_features(rel_url: str):
    """返回 (has_calc, has_formula, has_input, is_stub)."""
    fp = ROOT / rel_url
    if not fp.exists():
        return False, False, 0, False

    try:
        content = fp.read_text(encoding="utf-8")
    except Exception:
        return False, False, 0, False

    has_calc = "function calc" in content
    has_formula = "formula-box" in content
    input_count = len(INPUT_RE.findall(content))
    is_stub = "TOOLBOX-REDIRECT" in content
    return has_calc, has_formula, input_count, is_stub


def build_rows(tools, industries=None):
    rows = []
    for item in tools:
        if item.get("quality") != "C":
            continue
        ind = item.get("industry") or ""
        if industries and ind not in industries:
            continue

        path = item.get("path") or item.get("url") or ""
        has_calc, has_formula, input_count, is_stub = has_file_features(path)
        rows.append(
            {
                "industry": ind,
                "name": item.get("name", ""),
                "url": item.get("url", ""),
                "desc": item.get("desc", ""),
                "path": path,
                "has_calc": has_calc,
                "has_formula": has_formula,
                "inputs": input_count,
                "is_stub": is_stub,
            }
        )
    return rows


def summarize(rows):
    c = Counter(r["industry"] for r in rows)
    by_ind = defaultdict(int)
    for key, count in c.most_common():
        by_ind[key] = count

    actionable = {
        "stub": len([r for r in rows if r["is_stub"]]),
        "with_calc": len([r for r in rows if r["has_calc"]]),
        "with_formula": len([r for r in rows if r["has_formula"]]),
        "with_input": len([r for r in rows if r["inputs"] > 0]),
    }
    return {
        "total": len(rows),
        "by_industry": by_ind,
        "actionable": actionable,
    }


def write_json(path: Path, rows, summary):
    path.write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md(path: Path, rows, summary):
    lines = [
        "# ToolBox C 级工具治理清单（P0-2）",
        "",
        f"- 总数：{summary['total']}",
        f"- 纯跳转桩：{summary['actionable']['stub']}",
        f"- 包含 calc：{summary['actionable']['with_calc']}",
        f"- 已有 formula-box：{summary['actionable']['with_formula']}",
        f"- 有表单输入：{summary['actionable']['with_input']}",
        "",
        "## 分行业统计",
    ]

    for ind, count in summary["by_industry"].items():
        lines.append(f"- {ind}: {count}")

    lines.extend([
        "",
        "## 详情（前 300 条）",
        "|行业|工具名|URL|calc|formula|inputs|stub|",
        "|---|---|---|---|---|---|---|",
    ])

    for r in rows[:300]:
        lines.append(
            "|%s|%s|%s|%s|%s|%s|%s|"
            % (
                r["industry"],
                r["name"].replace("|", "｜"),
                r["url"],
                "Y" if r["has_calc"] else "N",
                "Y" if r["has_formula"] else "N",
                r["inputs"],
                "Y" if r["is_stub"] else "N",
            )
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = parse_args()
    tools = read_tools()
    rows = build_rows(tools, set(args.industry))
    summary = summarize(rows)

    if args.json:
        write_json(Path(args.json), rows, summary)
    if args.md:
        write_md(Path(args.md), rows, summary)

    print("total", summary["total"])
    print("by industry", len(summary["by_industry"]))
    print("stub", summary["actionable"]["stub"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
