#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 woodwork 的第四处占位残留：仅 convert-30.html 的 intro-scenes 仍是通用默认占位。
angle-1 / calculator-calc-15 的 intro-scenes 已是真实木工场景，不动。"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, "tools", "woodwork", "convert-30.html")

OLD = """    <ul class="intro-scenes">
      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>
    </ul>"""

NEW = """    <ul class="intro-scenes">
      <li>原木进厂含水率抽检与养生期判断</li>
      <li>干燥窑出窑含水率与配料余量核算</li>
      <li>不同批次木料含水率横向比对</li>
      <li>收缩率读数统一为工艺卡小数基准</li>
    </ul>"""

s = open(P, encoding="utf-8").read()
if OLD in s:
    s = s.replace(OLD, NEW)
    open(P, "w", encoding="utf-8").write(s)
    print("convert-30 intro-scenes 已替换为真实木材场景")
else:
    print("未找到 convert-30 的通用占位块，请人工核对")
