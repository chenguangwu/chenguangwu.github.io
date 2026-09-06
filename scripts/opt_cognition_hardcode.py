#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_cognition_hardcode.py — 为 cognition 8 工具页插入真实 tool-intro 块。

背景：cognition 8 工具页（stroop-test / nback-training / digit-span-test / corsi-block-test
/ schulte-table / human-benchmark / cognitive-assessment / time-perception）原**均无 tool-intro 块**
（内容层全缺，与 clinical-nursing 的 cycle-7/reminder-time-1 同性质）。formula-desc 已是真实
认知科学文本（无需清），opt 套话 0 页。本脚本为 8 页插入真实 tool-intro 三段块。

插入位置：`<div class="tool-intro open" id="toolIntro">` 手风琴插到 `</body>` 前（含 header
「关于「工具名」」+ 折叠 script + `<!-- /SEO 介绍区块 -->` 结尾注释），与 clinical-nursing 已验证
模板完全一致。该位置位于 deep-dive 注入锚点（`</body>` 前兜底）之前，_build.py 注入 deep-dive 后
两者均在 `</body>` 前、均存活（已验证）。

真实化方向：认知科学范式（Stroop/N-back/数字广度/视觉空间广度/注意力搜索/综合认知画像/
时间知觉），去伪科学、非临床诊断免责。
"""
import re, os, sys

TOOLS = "tools/cognition"
DRY = "--dry" in sys.argv

# 8 工具真实 tool-intro 三段（intro/feats/scenes）
INTRO_MAP = {
    "stroop-test": {
        "intro": "通过「读字义」与「命名字色」的反应时差量化认知干扰，用于注意力自评与 Stroop 效应课堂演示。",
        "feats": ["Stroop 干扰量计算", "一致/不一致双条件", "反应时即时反馈"],
        "scenes": ["心理学课堂效应演示", "专注度自评与训练", "注意控制实验数据采集"],
    },
    "nback-training": {
        "intro": "判断当前刺激与 N 个前刺激是否相同，渐进提升 N 训练工作记忆，并支持敏感度 d′ 测算。",
        "feats": ["可调 N 负荷", "命中/虚报统计", "敏感度 d′ 输出"],
        "scenes": ["工作记忆渐进训练", "自我追踪前后对比", "认知研究数据采集"],
    },
    "digit-span-test": {
        "intro": "顺背/倒背数字串评估听觉短时记忆与工作记忆容量，是综合智力测验的经典组成项。",
        "feats": ["顺背与倒背模式", "最大广度记录", "长度渐进呈现"],
        "scenes": ["工作记忆容量基线", "教育训练前后对比", "注意力自评练习"],
    },
    "corsi-block-test": {
        "intro": "按呈现顺序点击空间位置测量视觉空间工作记忆广度，与数字广度互补测不同记忆通道。",
        "feats": ["正向/反向敲击", "空间序列广度", "视觉空间通道"],
        "scenes": ["空间记忆训练", "言语×空间记忆对比", "认知研究演示"],
    },
    "schulte-table": {
        "intro": "在网格中按序快速点出数字，用完成耗时评估视觉搜索速度与注意力集中度。",
        "feats": ["可调网格规格", "完成耗时计时", "专注度反馈"],
        "scenes": ["注意力训练", "不同状态横向对比", "课堂专注力活动"],
    },
    "human-benchmark": {
        "intro": "集合反应时、记忆、预测等多维单人小测验，横向比较个人认知表现，属娱乐性自评。",
        "feats": ["反应时/记忆多维", "成绩趣味排名", "即时可测"],
        "scenes": ["反应速度与记忆自评", "朋友间横向对比", "多维度强弱项识别"],
    },
    "cognitive-assessment": {
        "intro": "多域小题生成注意力/记忆/速度/执行功能自评画像，用于训练基线与个人追踪。",
        "feats": ["多认知域评分", "相对强弱项画像", "复测追踪"],
        "scenes": ["训练前后对比", "自我了解认知强弱", "安排针对性练习"],
    },
    "time-perception": {
        "intro": "估计或产出指定时长，用偏差评估时间感知准确性，用于注意力与内感受研究及自评。",
        "feats": ["估计法/产出法", "相对偏差核算", "状态关联对比"],
        "scenes": ["时间知觉自评", "情绪×注意关联复测", "研究演示"],
    },
}

# header「关于「工具名」」用的真实工具名（取自页面 title 去后缀）
MISSING_NAMES = {
    "stroop-test": "Stroop 斯特鲁普效应测试",
    "nback-training": "N-Back 工作记忆训练",
    "digit-span-test": "数字广度记忆测验",
    "corsi-block-test": "Corsi 木块敲击测试",
    "schulte-table": "舒尔特方格注意力训练",
    "human-benchmark": "Human Benchmark 认知基准测评",
    "cognitive-assessment": "SCOPE 综合认知评估",
    "time-perception": "时间感知与节奏精度测试",
}

JUNK = [
    "基于权威医学标准", "医学学习与考试备考", "临床计算与评估辅助", "纯前端处理，数据不上传",
    "医疗专业领域的在线工具", "护理专业工具，基于权威标准", "工作与生活中的相关计算与查询",
    "日常生活中的计算需求", "购物消费的比价与换算",
]


def insert_intro(name, d):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    # 已存在块（理论上不会，但幂等保护）：跳过
    if "功能特点</h4>" in s or "tool-intro-body" in s:
        return 0
    # 若已含通用套话（安全校验），不静默覆盖
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
