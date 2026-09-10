#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 steel 分类 tool-intro-body 的 intro-scenes 第四处通用默认占位。
仅 analysis-price-1 命中（日常办公与学习/开发调试与数据处理/快速计算与格式转换/信息查询与参考），
steel-profile-weight 与 calc-1 该区块已是真实内容或不存在，不动。"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "tools", "steel", "analysis-price-1.html")

OLD = """    <ul class="intro-scenes">
      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>
    </ul>"""

NEW = """    <ul class="intro-scenes">
      <li>螺纹钢、热卷等周度报价录入，算均价与中位数判断价位高低</li>
      <li>多供应商同规格报价比价，用标准差识别异常高价批次</li>
      <li>价格序列波动跟踪，辅助锁价与套保时点决策</li>
      <li>成本波动分析，评估材料价格对预算的影响</li>
    </ul>"""

assert os.path.exists(TARGET), TARGET
s = open(TARGET, encoding="utf-8").read()
assert OLD in s, "未找到 intro-scenes 通用占位，可能已清理或非预期结构"
s = s.replace(OLD, NEW)
open(TARGET, "w", encoding="utf-8").write(s)
print("analysis-price-1 intro-scenes 第四处占位已清理")
