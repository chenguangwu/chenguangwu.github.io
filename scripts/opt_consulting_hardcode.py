#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_consulting_hardcode.py — 清理 consulting 3 工具页硬编码套话（2 类）：

A) formula-desc 校验变体 1 页：assessor-49「本校验工具依据对应数据格式与语法规范进行合法性检查…」
   → 真实胜任力评估描述（clean_fd 正则整体替换 <p class="formula-desc">…</p>）
B) tool-intro 三段块套话 2 页：analysis-47 / analysis-manager 块内含 6 类通用模板套话
   （「免费在线工具，纯前端处理…」「操作简单一键完成」「日常办公与学习」「开发调试与数据处理」
   「快速计算与格式转换」「信息查询与参考」）→ 整体替换为真实咨询场景（clean_intro）

说明：assessor-49 块内无套话（简介已真实），仅清 formula-desc；analysis-47/analysis-manager 的
formula-desc 已真实（标准数学运算描述），不需清。不覆盖 title；meta/og 品牌级真实特性不动。
"""
import re, os, sys

TOOLS = "tools/consulting"
DRY = "--dry" in sys.argv

# A) formula-desc 真实化
FD_MAP = {
    "assessor-49": "按六个维度评分并结合岗位类型加权，输出综合胜任力与短板维度，生成发展建议草稿；结果为自评/初筛参考，正式任用以组织评估流程为准。",
}

# B) tool-intro 真实三段（整体替换 2 页套话）
INTRO_REPLACE = {
    "analysis-47": {
        "intro": "围绕战略议题提供结构化分析框架（SWOT/竞争定位/实施路径），把模糊讨论拆成可执行维度。",
        "feats": ["SWOT 四象限拆解", "波特五力评估", "分析定位实施三段"],
        "scenes": ["年度战略复盘", "新业务进入评估", "战略落地里程碑"],
    },
    "analysis-manager": {
        "intro": "面向管理场景的财务分析与经营诊断框架，把收入/成本/现金/效率拆开看，辅助经营决策。",
        "feats": ["收支利现四栏诊断", "预算量差价差拆", "关键指标统一口径"],
        "scenes": ["经营例会诊断", "预算复盘超支定位", "投资降本议题准备"],
    },
}


def clean_fd(name, real):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    new = re.sub(r'<p class="formula-desc">.*?</p>',
                 '<p class="formula-desc">' + real + '</p>', s, flags=re.S)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


def clean_intro(name, d):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    intro = d["intro"]
    feats = "".join("<li>" + x + "</li>" for x in d["feats"])
    scenes = "".join("<li>" + x + "</li>" for x in d["scenes"])
    if "功能特点</h4>" in s:
        new = re.sub(r'(工具简介</h4>\s*<p>).*?(</p>)', lambda m: m.group(1) + intro + m.group(2), s, flags=re.S)
        new = re.sub(r'(<ul class="intro-features">).*?(</ul>)', lambda m: m.group(1) + feats + m.group(2), new, flags=re.S)
        new = re.sub(r'(<ul class="intro-scenes">).*?(</ul>)', lambda m: m.group(1) + scenes + m.group(2), new, flags=re.S)
        c = 1 if new != s else 0
        if not DRY and c:
            open(path, "w", encoding="utf-8").write(new)
        return c
    else:
        print("WARN 缺失 tool-intro 块(未处理):", name)
        return 0


total = 0
for name, real in FD_MAP.items():
    c = clean_fd(name, real)
    if c:
        total += c
        print((("DRY " if DRY else "") + "fd " + name))
for name, d in INTRO_REPLACE.items():
    c = clean_intro(name, d)
    if c:
        total += c
        print((("DRY " if DRY else "") + "intro(replace) " + name))
print("total changed:", total)
