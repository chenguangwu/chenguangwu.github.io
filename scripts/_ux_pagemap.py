#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全站逐页 UX 评分地图（一次性诊断，_ 前缀不入 git）。

复用 _ux_baseline.scan_one 的口径，导出每页 {score, feats, inputs, cross, bytes}，
供中分段 uplift 专项选页。输出到 .workbuddy/ux/pagemap.json（gitignore）。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from _ux_baseline import scan_one, TOOLS  # noqa: E402

OUT_DIR = os.path.join(ROOT, ".workbuddy", "ux")
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    rows = []
    for ind in sorted(os.listdir(TOOLS)):
        d = os.path.join(TOOLS, ind)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            with open(p, encoding="utf-8", errors="ignore") as _f:
                if "TOOLBOX-REDIRECT" in _f.read(4096):
                    continue
            try:
                r = scan_one(p)
            except Exception as e:
                print("ERR", p, e)
                continue
            r["ind"] = ind
            r["slug"] = fn[:-5]
            r["path"] = f"tools/{ind}/{fn}"
            rows.append(r)
    rows.sort(key=lambda r: (r["score"], r["ind"], r["slug"]))
    out = os.path.join(OUT_DIR, "pagemap.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)
    # 控制台概要
    from collections import Counter
    c = Counter(r["score"] for r in rows)
    print(f"总页 {len(rows)}")
    for s in range(0, 10):
        print(f"  score={s}: {c.get(s,0)} 页")
    print("写出", out)


if __name__ == "__main__":
    main()
