#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P4 补丁：fire-rescue/calc-1..4.html 存在两个 toolbox meta（单引号旧值 industry=fire
被 extract_meta 优先读取，双引号重复行无关）。修正单引号 meta 的 industry=fire→fire-rescue，
并删掉重复的双引号 meta 行。"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = [os.path.join(ROOT, "tools", "fire-rescue", "calc-%d.html" % i) for i in (1, 2, 3, 4)]

for f in files:
    c = open(f, encoding="utf-8").read()
    # 1) 修第一个（单引号）toolbox meta：industry=fire -> fire-rescue
    c2 = re.sub(
        r"(<meta name='toolbox' content='cat=calculator,industry=)fire(')",
        r"\1fire-rescue\2",
        c,
        count=1,
    )
    # 2) 删掉重复的双引号 toolbox meta 整行
    c3 = re.sub(
        r'\n<meta name="toolbox" content="cat=math,industry=fire-rescue,icon=🚒,bg=#ffebee">',
        "",
        c2,
        count=1,
    )
    if c3 != c:
        open(f, "w", encoding="utf-8").write(c3)
        print("FIXED", os.path.relpath(f, ROOT))
    else:
        print("NOCHANGE", os.path.relpath(f, ROOT))
