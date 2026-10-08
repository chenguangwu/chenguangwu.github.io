#!/usr/bin/env python3
"""扫描全站「零 verify 用例」工具页（§7.4 覆盖率缺口）
口径（2026-10-07 定，勿降）：
  - 工具页全集 = tools/**/*.html，排除各行业的 index.html 分类落地页
  - 排除 TOOLBOX-REDIRECT 存根（已下架/迁移壳，无 calc 逻辑）
  - 已覆盖 = scripts/ 下所有含用例块的文件里提取到的 slug 键（键名常不带引号）
用法: python3 scripts/_scan_zero_case.py
"""
import os, re, json, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
SCRIPTS = os.path.join(ROOT, "scripts")

# ---- 1. 工具页全集 ----
all_tools = set()
stub = set()
for ind in sorted(os.listdir(TOOLS)):
    d = os.path.join(TOOLS, ind)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.endswith(".html"):
            continue
        if fn == "index.html":
            continue
        slug = f"{ind}/{fn[:-5]}"
        all_tools.add(slug)
        try:
            head = open(os.path.join(d, fn), encoding="utf8", errors="ignore").read(4000)
        except OSError:
            continue
        if "TOOLBOX-REDIRECT" in head:
            stub.add(slug)

real_tools = sorted(all_tools - stub)

# ---- 2. 已覆盖 slug（键名可不带引号）----
KEY_RE = re.compile(r'"?slug"?\s*:\s*"([^"]+)"')
covered = {}
for fn in sorted(os.listdir(SCRIPTS)):
    if not fn.endswith((".js", ".py", ".json")):
        continue
    p = os.path.join(SCRIPTS, fn)
    if not os.path.isfile(p):
        continue
    try:
        txt = open(p, encoding="utf8", errors="ignore").read()
    except OSError:
        continue
    for m in KEY_RE.finditer(txt):
        s = m.group(1)
        if "/" in s:
            covered.setdefault(s, set()).add(fn)

# ---- 3. 差集 ----
zero = [t for t in real_tools if t not in covered]

by_ind = defaultdict(list)
for t in zero:
    by_ind[t.split("/")[0]].append(t)

print("=" * 68)
print("工具页全集            ", len(all_tools))
print("  其中 redirect 存根  ", len(stub))
print("  真实工具页          ", len(real_tools))
print("已覆盖（有用例）      ", len(set(real_tools) & set(covered)))
print("零用例                ", len(zero), f"（{len(zero)/max(1,len(real_tools))*100:.1f}%）")
print("覆盖涉及文件数        ", len(covered) and len({f for v in covered.values() for f in v}))
print("=" * 68)
print("零用例行业分布 TOP30：")
for ind, pages in sorted(by_ind.items(), key=lambda kv: -len(kv[1]))[:30]:
    print(f"  {ind:22} {len(pages)}")
print(f"\n共 {len(by_ind)} 个行业存在零用例页")

out = os.path.join("/tmp", "zero_case_all.txt")
open(out, "w").write("\n".join(zero))
print("\n全量清单 ->", out)
json.dump({"zero": zero, "by_ind": {k: v for k, v in by_ind.items()}},
          open("/tmp/zero_case_all.json", "w"), ensure_ascii=False)
