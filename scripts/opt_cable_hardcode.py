#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cable：清理硬编码套话，分三块（幂等，仅命中才写，支持 --dry）。

A. formula-desc 占位清理（仅 analysis-cost-price-5：本计算依据通用财务…→真实描述统计说明）。
B. tool-intro「功能特点/使用场景」套话清理：精确锚定 h4（仿 opt_bonding_optguide.py，保留「工具简介」块）；
   仅当功能特点 ul 含通用套话特征词才替换（analysis-cost-price-5 命中；tester-19 已真实跳过；
   cable-tray-sizing 无标准 tool-intro 块则跳过）。使用场景取 content_deepdive 真实 scenarios 前 3 条。
C. cable-tray-sizing 的 opt-guide / opt-faq 英文套话「工作与生活中的相关计算与查询。」→真实英文场景。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv

# ---- A. formula-desc ----
PAT_FD = re.compile(r'<p class="formula-desc">.*?</p>', re.S)
FD_REAL = (
    '<p class="formula-desc">本工具基于描述统计方法，对输入的铜价、电缆报价或材料成本等数值序列'
    '计算总和、平均值、中位数、极差、方差与标准差，用于铜价跟踪、多供应商比价与成本波动分析。'
    '所有计算在浏览器本地完成，数据不上传服务器。</p>'
)

# ---- B. tool-intro ----
PH_WORDS = ["操作简单，一键完成", "日常办公与学习", "开发调试与数据处理", "实时显示结果，所见即所得"]


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


FEAT_HTML = (
    '<ul class="intro-features">\n'
    '      <li>纯前端运行，数据不上传服务器</li>\n'
    '      <li>免费使用，无需注册登录</li>\n'
    '      <li>支持简体 / 繁体 / 英文界面</li>\n'
    '    </ul>'
)
PAT_FEAT = re.compile(r'<h4>(?:(?!</h4>).)*功能特点</h4>\s*<ul class="intro-features">.*?</ul>', re.S)
PAT_SCENE = re.compile(r'<h4>(?:(?!</h4>).)*使用场景</h4>\s*<ul class="intro-scenes">.*?</ul>', re.S)
PAT_FEAT_UL = re.compile(r'<h4>(?:(?!</h4>).)*功能特点</h4>\s*<ul class="intro-features">(.*?)</ul>', re.S)


def is_placeholder(s):
    m = PAT_FEAT_UL.search(s)
    if not m:
        return False
    return any(w in m.group(1) for w in PH_WORDS)


# ---- C. cable-tray-sizing opt-guide/opt-faq ----
OPT_PHRASE = "工作与生活中的相关计算与查询。"
OPT_REAL = "用于动力配电、弱电布线、数据中心与工业厂房的电缆桥架选型，以及改造扩容时的面积与填充率校核。"

changed = 0
skipped = 0

# A
f = "tools/cable/analysis-cost-price-5.html"
if os.path.exists(f):
    s = open(f, encoding="utf-8").read()
    if "本计算依据通用财务与货币规则" in s:
        s2 = PAT_FD.sub(lambda m: FD_REAL if "本计算依据通用财务与货币规则" in m.group(0) else m.group(0), s, count=1)
        if s2 != s:
            changed += 1
            if not dry:
                open(f, "w", encoding="utf-8").write(s2)
            print(("DRY " if dry else "OK ") + "A:analysis-cost-price-5 formula-desc")
        else:
            skipped += 1
            print("A:UNMATCH analysis-cost-price-5")
    else:
        skipped += 1
        print("A:NO-PLACEHOLDER analysis-cost-price-5")
else:
    skipped += 1
    print("A:NOFILE analysis-cost-price-5")

# B
key = "cable/analysis-cost-price-5"
e = data.get(key)
if os.path.exists(f) and e:
    s = open(f, encoding="utf-8").read()
    if is_placeholder(s):
        scen = e.get("scenarios") or []
        if scen:
            scene_items = "".join("<li>%s</li>" % esc(x) for x in scen[:3])
            scene_html = '<ul class="intro-scenes">\n      %s\n    </ul>' % scene_items
            s2 = PAT_FEAT.sub('<h4><span class="h4-icon">✨</span>功能特点</h4>\n    ' + FEAT_HTML, s, count=1)
            s2 = PAT_SCENE.sub('<h4><span class="h4-icon">🎯</span>使用场景</h4>\n    ' + scene_html, s2, count=1)
            if s2 != s:
                changed += 1
                if not dry:
                    open(f, "w", encoding="utf-8").write(s2)
                print(("DRY " if dry else "OK ") + "B:analysis-cost-price-5 tool-intro")
            else:
                skipped += 1
                print("B:UNMATCH analysis-cost-price-5")
        else:
            skipped += 1
    else:
        skipped += 1
        print("B:REAL-SKIP analysis-cost-price-5")

# C
f2 = "tools/cable/cable-tray-sizing.html"
if os.path.exists(f2):
    s = open(f2, encoding="utf-8").read()
    if OPT_PHRASE in s:
        s2 = s.replace(OPT_PHRASE, OPT_REAL)
        changed += 1
        if not dry:
            open(f2, "w", encoding="utf-8").write(s2)
        print(("DRY " if dry else "OK ") + "C:cable-tray-sizing opt-guide/opt-faq")
    else:
        skipped += 1
        print("C:NO-PLACEHOLDER cable-tray-sizing")
else:
    skipped += 1
    print("C:NOFILE cable-tray-sizing")

print("changed=%d skipped=%d" % (changed, skipped))
