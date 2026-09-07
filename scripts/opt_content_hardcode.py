#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_content_hardcode.py — 清理 content 4 工具页硬编码套话（4 类）：

A) formula-desc 校验变体 1 页：checker-5「本校验工具依据对应数据格式与语法规范进行合法性检查…」
   → 真实内容校验描述（clean_fd 正则整体替换 <p class="formula-desc">…</p>）
B) opt 套话 2 页：generator-33 / generator-time-1「工作与生活中的相关计算与查询。」（适用场景 h2 / FAQ dd / JSON-LD 共 3 处）
   → 各自真实内容场景文本（字符串整体替换，三处一致）
C) 块内套话 3 页：generator-33 / generator-34 / generator-time-1 的 tool-intro 三段块含 6 类通用模板套话
   → 整体替换为真实内容生成场景（clean_intro）
D) 缺块 1 页：checker-5 原无 tool-intro 块 → 插入真实三段手风琴块（insert_intro）

说明：generator-33/34/time-1 的 formula-desc 为真实生成器描述（「本生成器依据指定格式规范…」），不需清。
不覆盖 title；meta/og 品牌级真实特性不动。
"""
import re, os, sys

TOOLS = "tools/content"
DRY = "--dry" in sys.argv

# A) formula-desc 真实化
FD_MAP = {
    "checker-5": "对文本或文档做结构、格式与常见问题的批量检查（标题层级、链接、重复段落），输出问题清单与定位，辅助发布前自查；结果为机器初检，最终以人工复核为准。",
}

# B) opt 套话真实化（按页不同文本）
OPT_MAP = {
    "generator-33": "按题材、人物与冲突生成小说大纲、人设与章节草稿，辅助创作起步；结果为初稿灵感，需作者打磨，非代写成品。",
    "generator-time-1": "辅助字幕时间轴调整与格式转换（偏移、拆分、双语标注），提升音画同步；结果为时间轴处理，翻译以人工为准。",
}
OPT_OLD = "工作与生活中的相关计算与查询。"

# C) 块内套话 3 页整体替换三段
INTRO_REPLACE = {
    "generator-33": {
        "intro": "按设定生成小说大纲、人设与章节草稿，辅助网文或短篇起步，打破空白页。",
        "feats": ["三幕式大纲生成", "人设卡与冲突", "续写选项扩写"],
        "scenes": ["新书大纲起步", "卡章续写选项", "配角群像生成"],
    },
    "generator-34": {
        "intro": "按主题与页数生成 PPT 大纲、版式与要点文案，辅助汇报/课件快速成稿。",
        "feats": ["大纲结构生成", "每页要点文案", "图表类型建议"],
        "scenes": ["周报立项汇报", "长文压演讲要点", "课件知识卡片"],
    },
    "generator-time-1": {
        "intro": "辅助字幕时间轴调整与格式转换（偏移/拆分/双语标注），提升音画同步与多语对照。",
        "feats": ["时间轴整体偏移", "长句拆分两行", "双语对照标注"],
        "scenes": ["音画不同步修正", "移动端字幕优化", "语言学习对照"],
    },
}

# D) 缺块 1 页插入三段（含 header 真实工具名）
INTRO_INSERT = {
    "checker-5": {
        "name": "内容校验检查器",
        "intro": "对文本或文档做结构、格式与常见问题的批量检查（标题层级、链接、重复段落），输出问题清单与定位，辅助发布前自查。",
        "feats": ["标题层级检查", "死链与 alt 扫描", "重复段落比对"],
        "scenes": ["发布前排版自查", "多版草稿差异", "批量稿件初检"],
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


def clean_opt(name, old, new):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    if old not in s:
        return 0
    new_s = s.replace(old, new)
    c = 1 if new_s != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new_s)
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


def insert_intro(name, d):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    if "功能特点</h4>" in s or "tool-intro-body" in s:
        return 0
    intro = d["intro"]
    feats = "".join("<li>" + x + "</li>" for x in d["feats"])
    scenes = "".join("<li>" + x + "</li>" for x in d["scenes"])
    _title = d["name"]
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
for name, real in FD_MAP.items():
    c = clean_fd(name, real)
    if c:
        total += c
        print((("DRY " if DRY else "") + "fd " + name))
for name, new in OPT_MAP.items():
    c = clean_opt(name, OPT_OLD, new)
    if c:
        total += c
        print((("DRY " if DRY else "") + "opt " + name))
for name, d in INTRO_REPLACE.items():
    c = clean_intro(name, d)
    if c:
        total += c
        print((("DRY " if DRY else "") + "intro(replace) " + name))
for name, d in INTRO_INSERT.items():
    c = insert_intro(name, d)
    if c:
        total += c
        print((("DRY " if DRY else "") + "intro(insert) " + name))
print("total changed:", total)
