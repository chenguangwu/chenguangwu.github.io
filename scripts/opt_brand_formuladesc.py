#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 brand/assessor-51.html 的 formula-desc 占位套话。

原块（第 101 行）：<p class="formula-desc">本校验工具依据对应数据格式与语法规范进行合法性检查…工具名称：品牌（资产/评估/审计）体系 - 品牌资产评估工具。</p>
替换为对齐 agriculture 范本的真实说明（Interbrand 模型原理 + 用途 + 数据不出浏览器）。
"""
import re
import sys

F = "tools/brand/assessor-51.html"
s = open(F, encoding="utf-8").read()

real = (
    "本工具基于 Interbrand 品牌评估思路：以品牌年净利润 × 品牌贡献率得到品牌净利润，"
    "再按品牌强度系数折算调整后折现率，对预测年限内的品牌净利润折现求和得到品牌资产现值；"
    "纯前端运行，输入数据不出浏览器。结果仅供管理参考与投融资沟通，正式财务披露须符合会计准则并经审计。"
)
NEW = f'<p class="formula-desc">{real}</p>'

# 匹配原 formula-desc 整段（单行）
PAT = re.compile(r'<p class="formula-desc">.*?</p>', re.S)

if "--dry" in sys.argv:
    m = PAT.search(s)
    print("DRY match:", bool(m))
    if m:
        print("OLD:", m.group(0)[:80], "...")
    sys.exit(0)

n = len(PAT.findall(s))
if n == 0:
    print("[SKIP] 未匹配到 formula-desc，可能已清理")
    sys.exit(0)
s2 = PAT.sub(NEW, s, count=1)
open(F, "w", encoding="utf-8").write(s2)
print(f"DONE: replaced {min(n,1)} formula-desc block")
