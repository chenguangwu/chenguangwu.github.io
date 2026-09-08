#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取工具页的输入默认值与计算脚本，供 tool_calc_run.js 在 Node 里跑出真实结果。

用途：
    为工具编写「深度解析」示例时，示例中的数字必须与工具实际输出一致，
    否则等于用编造的算例误导用户（DEV-PLAN 第 4/9 条）。
    本脚本把每个工具页的 input/select 默认态与 <script> 抽成 harness，
    交给 Node 用轻量 DOM mock 执行，取回默认输入下的真实输出文本。

用法：
    python3 scripts/tool_calc_probe.py <industry>      # 生成 harness
    node scripts/tool_calc_run.js                      # 跑出结果
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join("/tmp", "tool_calc_harness")

INPUT_RE = re.compile(r"<input\b([^>]*)>", re.I)
SELECT_RE = re.compile(r"<select\b([^>]*)>([\s\S]*?)</select>", re.I)
OPTION_RE = re.compile(r"<option\b([^>]*)>([\s\S]*?)</option>", re.I)
ATTR_RE = re.compile(r"([\w-]+)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))")


def attrs(tag: str) -> dict:
    d = {}
    for m in ATTR_RE.finditer(tag):
        d[m.group(1).lower()] = m.group(2) or m.group(3) or m.group(4) or ""
    # 无值属性（如 <option value="16" selected>）上面捕获不到，单独识别并置为真值
    for m in re.finditer(r"(?:^|\s)(selected|checked|disabled|multiple|required)\b(?!=)", tag, re.I):
        d[m.group(1).lower()] = m.group(1).lower()
    return d


def main() -> int:
    industry = sys.argv[1] if len(sys.argv) > 1 else "fire-rescue"
    tdir = os.path.join(ROOT, "tools", industry)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = {}

    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        slug = fn[:-5]
        src = open(os.path.join(tdir, fn), encoding="utf-8").read()
        scripts = re.findall(r"<script>([\s\S]*?)</script>", src)

        values: dict[str, str] = {}
        options: dict[str, list] = {}
        for tag in INPUT_RE.findall(src):
            a = attrs(tag)
            if a.get("id"):
                values[a["id"]] = a.get("value", "")
        for stag, body in SELECT_RE.findall(src):
            a = attrs(stag)
            sid = a.get("id")
            if not sid:
                continue
            chosen, idx, opt_vals = "", 0, []
            for i, (otag, _otext) in enumerate(OPTION_RE.findall(body)):
                oa = attrs(otag)
                opt_vals.append(oa.get("value", ""))
                if "selected" in oa:
                    chosen, idx = oa.get("value", ""), i
            if not chosen and opt_vals:
                chosen, idx = opt_vals[0], 0
            values[sid] = chosen
            options[sid] = {"values": opt_vals, "selectedIndex": idx}

        # 结果容器：取被赋 innerHTML 频次最高的 id
        ids: dict[str, int] = {}
        for m in re.finditer(r"getElementById\(['\"]([\w-]+)['\"]\)\.innerHTML", "\n".join(scripts)):
            ids[m.group(1)] = ids.get(m.group(1), 0) + 1
        res_id = max(ids, key=ids.get) if ids else "result"

        entry = "calc" if re.search(r"function\s+calc\s*\(", "\n".join(scripts)) else (
            "calculate" if re.search(r"function\s+calculate\s*\(", "\n".join(scripts)) else "")

        out[slug] = {"industry": industry, "values": values, "options": options,
                     "scripts": scripts, "res_id": res_id, "entry": entry}

    path = os.path.join(OUT_DIR, "%s.json" % industry)
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    print("已生成 harness: %s（%d 个工具）" % (path, len(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
