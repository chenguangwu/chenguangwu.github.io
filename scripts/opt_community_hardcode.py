# -*- coding: utf-8 -*-
"""
opt_community_hardcode.py — 清理 community 3 工具页硬编码套话：
1) formula-desc 1 页（财务变体：analysis-cost-9「本计算依据通用财务与货币规则…」）→ 真实成本说明
   （meta/JSON-LD 已真实无回灌）
2) tool-intro 三段块 3 页全覆盖：替换通用模板套话（「免费在线工具，纯前端处理…」「操作简单一键完成」
   「日常办公与学习/开发调试与数据处理…」）→ 真实竞品/成本/统计场景

通用套话识别（JUNK）：与临床护理/医疗专属套话不同，community 用的是「免费在线工具」类通用模板，
含隐私措辞与泛化功能/场景。本脚本整体替换三段块内容（简介 p / intro-features li / intro-scenes li）。
"""
import re, os, sys, json

TOOLS = "tools/community"
DRY = "--dry" in sys.argv
DD = json.load(open("i18n/tools/content_deepdive.json", encoding="utf-8"))

# 1) formula-desc 真实化（按页精确替换块内文本）
FD_MAP = {
    "analysis-cost-9": "本工具按固定/变动与单位/总口径拆解成本结构，输出可控项与降本优先级，结果仅供参考，正式预算以财务制度与最新法规为准。",
}

# 2) tool-intro 真实三段（3 页全覆盖，替换通用套话）
INTRO_MAP = {
    "analysis-74": {
        "intro": "用结构化维度把竞品量化对标，辅助定位差异化卖点与竞争应对优先级。",
        "feats": ["多维竞品打分", "象限定位可视化", "差异化缺口识别"],
        "scenes": ["竞品对标梳理", "差异化卖点提炼", "竞争动作优先级排序"],
    },
    "analysis-cost-9": {
        "intro": "按固定/变动与单位/总口径拆解成本结构，定位可控优化项与降本空间。",
        "feats": ["成本结构拆解", "降本优先级排序", "预算偏差归因"],
        "scenes": ["成本结构分析", "降本项筛选", "实际 vs 预算对照"],
    },
    "stats-13": {
        "intro": "聚合报名、付款与时段分布，输出转化漏斗与参与结构，辅助活动节奏与备货。",
        "feats": ["报名付款聚合", "转化漏斗分层", "时段峰值识别"],
        "scenes": ["预售报名统计", "转化流失定位", "库存与发车预备"],
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
        def r1(m): return m.group(1) + intro + m.group(2)
        def r2(m): return m.group(1) + feats + m.group(2)
        def r3(m): return m.group(1) + scenes + m.group(2)
        new = re.sub(r'(工具简介</h4>\s*<p>).*?(</p>)', r1, s, flags=re.S)
        new = re.sub(r'(<ul class="intro-features">).*?(</ul>)', r2, new, flags=re.S)
        new = re.sub(r'(<ul class="intro-scenes">).*?(</ul>)', r3, new, flags=re.S)
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
for name, d in INTRO_MAP.items():
    c = clean_intro(name, d)
    if c:
        total += c
        print((("DRY " if DRY else "") + "intro " + name))
print("total changed:", total)
