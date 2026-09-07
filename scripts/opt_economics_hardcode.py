#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 economics 分类中 B 类 opt 套话「工作与生活中的相关计算与查询」。

economics 仅 inflation-rate 1 页含该占位（出现 3 处：JSON-LD FAQ 的 acceptedAnswer.text、
适用场景段的 <p>、opt-faq 的 <dd>）。替换为真实经济学场景描述。
A 类 formula-desc 经核验全为真实领域描述（如「输入消费 C 与收入 Y，求平均消费倾向」），
C 类 tool-intro-body 套话 0 命中，均无需处理。
"""
import sys, os

TARGET = "tools/economics/inflation-rate.html"
PLACEHOLDER = "工作与生活中的相关计算与查询。"
REAL = ("用于根据基期与报告期 CPI 测算通货膨胀率，评估物价水平变化与货币购买力变动，"
        "辅助个人理财规划、薪资调整研判与宏观经济观察。")

dry = "--dry" in sys.argv

if not os.path.exists(TARGET):
    print("目标页不存在:", TARGET)
    sys.exit(1)

t = open(TARGET, encoding="utf-8").read()
cnt = t.count(PLACEHOLDER)
print(f"{os.path.basename(TARGET)} 占位次数: {cnt}")

if dry:
    print("残留:", cnt > 0)
else:
    if cnt > 0:
        t2 = t.replace(PLACEHOLDER, REAL)
        open(TARGET, "w", encoding="utf-8").write(t2)
        t3 = open(TARGET, encoding="utf-8").read()
        print("写回后残留:", t3.count(PLACEHOLDER))
        # JSON-LD 合法性快速校验：提取第一个含 "@context" 的 script 块解析
        import json
        m = re.search(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', t3, re.S) if (re:=__import__("re")) else None
        if m:
            try:
                json.loads(m.group(1))
                print("JSON-LD 合法: True")
            except Exception as e:
                print("JSON-LD 解析失败:", e)
                sys.exit(2)
    else:
        print("无需替换")
