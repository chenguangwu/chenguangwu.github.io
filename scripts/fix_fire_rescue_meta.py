#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 fire-rescue 分类下工具页的行业与分类字段错标。

问题背景：
    tools/fire-rescue/ 下的 calc-1~calc-4 由早期 fire 分类迁移而来，
    <meta name="toolbox"> 仍标 industry=fire，导致：
      · 面包屑与 BreadcrumbList 指向 tools/fire/index.html（与所在目录不一致）
      · 被统计进 fire 行业，fire-rescue 少计 4 个工具
      · deep-dive / _en_override 等按「行业/slug」匹配的字典全部落空
    另有若干工具 cat 被标成 convert / finance / health / math / engineer，
    与工具实际形态（计算 / 速查）不符，影响分类页归类与导航。

    按 DEV-PLAN §4.1 第 6 条「发现错标必须在源 HTML 修正，不能只手改构建产物」。

用法：
    python3 scripts/fix_fire_rescue_meta.py            # 预览
    python3 scripts/fix_fire_rescue_meta.py --apply    # 落盘
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDIR = os.path.join(ROOT, "tools", "fire-rescue")

# 文件名 -> 修正后的 cat（industry 一律统一为 fire-rescue）
CAT_FIX = {
    "calc-1": "calculator",
    "calc-2": "calculator",
    "calc-3": "calculator",       # 原 convert：疏散时间是计算，不是单位换算
    "calc-4": "calculator",
    "calc-pressure-1": "calculator",   # 原 engineer
    "calc-time-response": "calculator",  # 原 convert
    "evacuation-time": "calculator",     # 原 convert
    "fire-load": "calculator",           # 原 engineer
    "fire-risk-assessment": "calculator",  # 原 finance
    "length-distance": "calculator",     # 原 math
    "pressure-flow": "calculator",       # 原 engineer
    "speed-3": "calculator",             # 原 engineer
    "time-41": "calculator",             # 原 convert
    "time-air": "calculator",            # 原 health
    "time-evacuation": "calculator",     # 原 convert
    "time-lux": "calculator",            # 原 convert
    "zuranyangzhishupanding": "reference",  # 原 health：氧指数判定属速查
    # 保留 engineer：post-fire-assessment（结构评估）、smoke-management（防排烟设计）
    # 保留 reference：chemical-spill / fire-extinguisher-selection / fire-fighting-tactics
    #                 fire-investigation / fire-resistance-rating / high-rise-fire
    #                 rescue-route / ventilation-tactics / water-rescue
    # 保留 validator：detector-11 / detector-20
}

OLD_IND = "fire"
NEW_IND = "fire-rescue"
NEW_IND_NAME = "消防救援"
OLD_IND_NAME = "消防安全"


def main() -> int:
    apply = "--apply" in sys.argv
    changed = 0
    report = []

    for fn in sorted(os.listdir(TDIR)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        slug = fn[:-5]
        path = os.path.join(TDIR, fn)
        src = open(path, encoding="utf-8").read()
        new = src
        touched = []

        # 1) industry 字段
        def _ind_rep(m: re.Match) -> str:
            body = m.group(2)
            # 负向前瞻：避免误伤已经是 industry=fire-rescue 的页面（'-' 也是单词边界）
            if re.search(r"industry=%s(?![\w-])" % OLD_IND, body):
                body = re.sub(r"industry=%s(?![\w-])" % OLD_IND, "industry=" + NEW_IND, body)
                touched.append("industry")
            return m.group(1) + body + m.group(3)

        new = re.sub(r'(name=["\']toolbox["\']\s+content=["\'])([^"\']*)(["\'])' , _ind_rep, new)

        # 2) cat 字段
        if slug in CAT_FIX:
            def _cat_rep(m: re.Match, _c=CAT_FIX[slug]) -> str:
                body = m.group(2)
                nb = re.sub(r"cat=[\w-]+", "cat=" + _c, body)
                if nb != body:
                    touched.append("cat->" + _c)
                return m.group(1) + nb + m.group(3)
            new = re.sub(r'(name=["\']toolbox["\']\s+content=["\'])([^"\']*)(["\'])' , _cat_rep, new)

        # 3) 面包屑链接与名称（仅 industry 被修正的页面需要）
        if "industry" in touched:
            nb = new.replace('href="../fire/index.html"', 'href="index.html"')
            nb = nb.replace(OLD_IND_NAME, NEW_IND_NAME)
            if nb != new:
                touched.append("breadcrumb")
                new = nb

        # 4) BreadcrumbList 结构化数据
        if "industry" in touched:
            nb = new.replace("https://chenguangwu.github.io/tools/fire/index.html",
                             "https://chenguangwu.github.io/tools/fire-rescue/index.html")
            if nb != new:
                touched.append("breadcrumb-ld")
                new = nb

        if new != src:
            changed += 1
            report.append((slug, touched))
            if apply:
                open(path, "w", encoding="utf-8").write(new)

    print("待修正页面: %d" % changed)
    for slug, t in report:
        print("  %-32s %s" % (slug, ", ".join(t)))
    print("模式: %s" % ("已落盘" if apply else "预览（加 --apply 落盘）"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
