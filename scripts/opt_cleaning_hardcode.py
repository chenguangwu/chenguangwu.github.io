#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 cleaning 分类工具页硬编码套话。

范围（基于扫描结果）：
- formula-desc 占位仅 1 页：appliance-cycle，变体「本速查内容依据权威标准与公开资料整理…」
  （本批 cleaning 工具页的 <head> meta/JSON-LD 描述已真实，不含回灌占位，仅 formula-desc 块需清）
- tool-intro 三段块（简介/功能/场景）：8 页全部已真实化，无套话，不需清
- opt-guide/opt-faq 套话（工作与生活中的相关计算与查询）：0 页，不需清

用法：
  python3 scripts/opt_cleaning_hardcode.py --dry    # 预览
  python3 scripts/opt_cleaning_hardcode.py          # 正式
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "cleaning")

PLACEHOLDER = "本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。"
REAL_FD = "家电清洁周期表依据厂商保养手册与家政实操经验，整理常见家电的建议清洁频率（油烟机每月表面、每季度拆洗；冰箱每周整理、每季除味；空调滤网每两周、蒸发器每季；洗衣机每月筒自洁），可按使用强度与水油环境微调。"

DRY = "--dry" in sys.argv


def clean_file(name):
    path = os.path.join(TOOLS, name + ".html")
    if not os.path.exists(path):
        return 0
    s = open(path, encoding="utf-8").read()
    cnt = s.count(PLACEHOLDER)
    if cnt == 0:
        return 0
    new = s.replace(PLACEHOLDER, REAL_FD)
    if not DRY:
        open(path, "w", encoding="utf-8").write(new)
    return cnt


def main():
    targets = ["appliance-cycle"]
    total = 0
    for name in targets:
        c = clean_file(name)
        if c:
            total += c
            print(("DRY " if DRY else "") + "cleaned", name, "替换", c, "处")
    print(("DRY 预览 " if DRY else "正式 ") + "完成，总替换:", total)


if __name__ == "__main__":
    main()
