#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_colorvision_hardcode.py — 为 colorvision 4 工具页插入真实 tool-intro 块。

背景：colorvision 4 工具页（colorblind-simulator / cvd-safe-palette / farnsworth-d15-test
/ palette-cvd-checker）原**均无 tool-intro 块**（内容层全缺）。formula-desc 已是真实色觉科学
文本（Machado 矩阵/OKLCH/CIE，无需清），opt 套话 0 页。本脚本为 4 页插入真实 tool-intro 三段块。

插入位置：`<div class="tool-intro open" id="toolIntro">` 手风琴插到 `</body>` 前（含 header
「关于「工具名」」+ 折叠 script + `<!-- /SEO 介绍区块 -->` 结尾注释），与 cognition 已验证
模板完全一致。_build.py 注入 deep-dive 后两者均在 `</body>` 前、均存活。

真实化方向：色觉缺陷科学（Machado 变换/OKLCH 采样/D-15 分型/可辨识度量化），去伪科学、非临床确诊免责。
"""
import re, os, sys

TOOLS = "tools/colorvision"
DRY = "--dry" in sys.argv

INTRO_MAP = {
    "colorblind-simulator": {
        "intro": "用 Machado 线性 RGB 变换矩阵把图像模拟为各型色觉缺陷观感，帮助设计前预判配色在色觉缺陷人群中的可读性。",
        "feats": ["红/绿/蓝多型模拟", "按严重度插值", "图像实时预览"],
        "scenes": ["UI/图表配色自查", "无障碍评审复核", "色觉差异科普演示"],
    },
    "cvd-safe-palette": {
        "intro": "在 OKLCH 感知均匀空间采样并做色觉缺陷变换校验，生成在色盲视角下仍两两可分的调色板。",
        "feats": ["OKLCH 感知采样", "逐对可辨识校验", "风险对剔除补采"],
        "scenes": ["数据可视化配色", "品牌/UI 规范", "教学科研作图"],
    },
    "farnsworth-d15-test": {
        "intro": "将 15 个固定亮度色帽按色相排列，通过跨轴错误方向与数量评估色觉缺陷类型与程度。",
        "feats": ["15 色帽排列", "跨轴错误判型", "严重度计数"],
        "scenes": ["色觉快速筛查", "培训科普演示", "正式检测前分型"],
    },
    "palette-cvd-checker": {
        "intro": "对已有配色逐对做色觉缺陷变换，量化各类缺陷下的感知距离并标出可能混淆的组合。",
        "feats": ["逐对变换比对", "多型缺陷覆盖", "风险对高亮"],
        "scenes": ["现有配色复审", "图表图例验收", "无障碍合规复核"],
    },
}

MISSING_NAMES = {
    "colorblind-simulator": "色盲模拟器 Pro",
    "cvd-safe-palette": "色盲安全配色生成器",
    "farnsworth-d15-test": "Farnsworth D-15 色相排列测试",
    "palette-cvd-checker": "调色板色觉可辨识度检查器",
}

JUNK = [
    "基于权威医学标准", "医学学习与考试备考", "临床计算与评估辅助", "纯前端处理，数据不上传",
    "医疗专业领域的在线工具", "护理专业工具，基于权威标准", "工作与生活中的相关计算与查询",
    "日常生活中的计算需求", "购物消费的比价与换算",
]


def insert_intro(name, d):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    if "功能特点</h4>" in s or "tool-intro-body" in s:
        return 0
    if any(j in s for j in JUNK):
        print("WARN 套话残留未清:", name)
    intro = d["intro"]
    feats = "".join("<li>" + x + "</li>" for x in d["feats"])
    scenes = "".join("<li>" + x + "</li>" for x in d["scenes"])
    _title = MISSING_NAMES.get(name, name)
    folding = ('<script>\n'
               '// tool-intro折叠交互\n'
               'document.addEventListener(\'DOMContentLoaded\',function(){\n'
               '  var headers=document.querySelectorAll(\'.tool-intro-header\');\n'
               '  headers.forEach(function(h){\n'
               '    h.addEventListener(\'click\',function(){\n'
               '      this.parentElement.classList.toggle(\'open\');\n'
               '    });\n'
               '  });\n'
               '});\n'
               '</script>')
    block = ('<div class="tool-intro open" id="toolIntro">\n'
             '  <div class="tool-intro-header">\n'
             '    <span class="intro-icon-wrap"><span class="intro-icon">📖</span>关于「' + _title + '」</span>\n'
             '    <span class="arrow">▼</span>\n'
             '  </div>\n'
             '  <div class="tool-intro-body">\n'
             '    <h4><span class="h4-icon">📝</span>工具简介</h4>\n'
             '    <p>' + intro + '</p>\n'
             '    <h4><span class="h4-icon">✨</span>功能特点</h4>\n'
             '    <ul class="intro-features">' + feats + '</ul>\n'
             '    <h4><span class="h4-icon">🎯</span>使用场景</h4>\n'
             '    <ul class="intro-scenes">' + scenes + '</ul>\n'
             '  </div>\n'
             '</div>\n'
             '<!-- /SEO 介绍区块 -->\n\n' + folding)
    new = s.replace('</body>', block + '\n</body>', 1)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


total = 0
for name, d in INTRO_MAP.items():
    c = insert_intro(name, d)
    if c:
        total += c
        print((("DRY " if DRY else "") + "intro(insert) " + name))
print("total inserted:", total)
