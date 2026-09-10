#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 pharmacy/analysis-report-cost.html 的 tool-intro-body intro-scenes 第四处通用默认占位。
checker-manager.html 的 intro-scenes 已是真实 GSP 场景，不动。"""
import re, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "tools", "pharmacy", "analysis-report-cost.html")

REAL = [
    "门店月度毛利结构分析",
    "多门店/多品规成本对比",
    "进销存报表数据核对",
    "经营管理例会数据支撑",
]

s = open(P, encoding="utf-8").read()
# 匹配 <ul class="intro-scenes"> ... </ul>
pat = re.compile(r'(<ul class="intro-scenes">)(.*?)(</ul>)', re.DOTALL)
m = pat.search(s)
if not m:
    print("未找到 intro-scenes，跳过")
else:
    old = m.group(2)
    if "日常办公与学习" in old or "开发调试与数据处理" in old:
        new_list = "".join(f"      <li>{x}</li>\n" for x in REAL)
        s = s[:m.start(2)] + new_list + s[m.end(2):]
        open(P, "w", encoding="utf-8").write(s)
        print("analysis-report-cost intro-scenes 已替换为真实药店财务场景")
    else:
        print("analysis-report-cost intro-scenes 已非通用占位，无需处理")
