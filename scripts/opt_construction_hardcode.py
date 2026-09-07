#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_construction_hardcode.py — 清理 construction 26 工具页硬编码套话（4 类）：

A) formula-desc 工程变体 1 页：soundproof-material「本工程计算基于标准物理…商业办公领域的在线工具」
   → 真实隔音用量描述（clean_fd 正则整体替换 <p class="formula-desc">…</p>）
B) opt 套话 1 页：estimate-area-dosage「工作与生活中的相关计算与查询。」（适用场景 h2 / FAQ dd / JSON-LD 共 3 处）
   → 真实墙面粉刷场景文本（字符串整体替换，三处一致）
C) 块内套话 7 页：ac-size-guide / pipe-flow / radiator-calculator / rebar-weight /
   soundproof-material / timber-volume / window-shading 的 tool-intro 三段块含「操作简单，一键完成」
   → 整体替换为真实三段（clean_intro，与 community 同）
D) 缺块 3 页：calc-1 / cement-mortar-ratio / renovation-labor-cost 原无 tool-intro 块
   → 插入真实三段手风琴块（insert_intro，与 cognition 同）

不覆盖 title；meta/og/JSON-LD 的品牌级真实特性（免费在线工具/纯前端处理）不动。
"""
import re, os, sys

TOOLS = "tools/construction"
DRY = "--dry" in sys.argv

# A) formula-desc 真实化
FD_MAP = {
    "soundproof-material": "按墙面净面积与隔音材料幅宽估算用量，结果供下料参考；实际隔声效果取决于系统构造与缝隙密封，非单一材料决定。",
}

# B) opt 套话真实化（estimate-area-dosage 三处一致替换）
OPT_OLD = "工作与生活中的相关计算与查询。"
OPT_NEW = "墙面翻新、旧房刷漆前按面积与遍数估算腻子与涂料用量，快速得出采购量与预算区间。"

# C) 块内套话 7 页整体替换三段（含 soundproof-material，其 FD 另由 A 处理）
INTRO_REPLACE = {
    "ac-size-guide": {
        "intro": "按房间面积、层高、朝向与气候估算空调制冷/制热匹数，帮助选购前快速定位机型区间。",
        "feats": ["面积负荷法速算", "朝向层高余量修正", "匹数与制冷量换算"],
        "scenes": ["新房选购前粗估", "西晒顶层加余量", "多房间批量配机"],
    },
    "pipe-flow": {
        "intro": "按管径与流速估算给水管流量，辅助选入户管径与判断水压是否够用。",
        "feats": ["管径截面积换算", "经济流速取值", "流量单位换算"],
        "scenes": ["入户管径选型", "高峰用水核对", "管径流量对比"],
    },
    "radiator-calculator": {
        "intro": "按房间面积与热指标估算散热器片数，辅助采暖选型与预算。",
        "feats": ["面积热负荷法", "单柱散热量折算", "边户顶层余量"],
        "scenes": ["装修定暖气片", "客餐厅连通核算", "旧房加片对比"],
    },
    "rebar-weight": {
        "intro": "按钢筋直径与长度求理论重量，用于下料算量与进料计划。",
        "feats": ["米重经验公式", "根数批量求和", "规格汇总"],
        "scenes": ["预算钢筋量", "余料清点", "下料优化"],
    },
    "soundproof-material": {
        "intro": "按需隔音的墙面/顶面面积与材料幅宽估算隔音毡、吸音棉用量，辅助下料。",
        "feats": ["面积净量核算", "幅宽卷数换算", "损耗预留"],
        "scenes": ["临街卧室隔音", "吊顶吸音棉铺设", "构造性价比对比"],
    },
    "timber-volume": {
        "intro": "按板材/方材截面与长度求材积，用于下料、贸易与库存盘点。",
        "feats": ["长×宽×厚求积", "原木检尺对照", "规格汇总"],
        "scenes": ["木工下料估算", "库存材积盘点", "树种重量换算"],
    },
    "window-shading": {
        "intro": "估算外遮阳构造后的窗户综合遮阳系数，辅助隔热选型与节能判断。",
        "feats": ["几何遮挡建模", "综合 SC 相乘", "活动固定对比"],
        "scenes": ["西晒窗遮阳", "南向兼顾冬阳", "节能审查粗核"],
    },
}

# D) 缺块 3 页插入三段（含 header 真实工具名）
INTRO_INSERT = {
    "calc-1": {
        "name": "脚手架承载力计算",
        "intro": "按立杆间距与步距粗算单杆容许荷载，辅助搭设前初核；正式方案须由持证人员按规范设计。",
        "feats": ["立杆荷载初估", "步距影响对照", "堆载平台校核"],
        "scenes": ["外墙架初核", "堆料平台验算", "稳定性余量评估"],
    },
    "cement-mortar-ratio": {
        "name": "水泥砂浆配比",
        "intro": "按用途给出水泥砂浆质量比与每方用量，辅助砌筑/抹灰/找平配料。",
        "feats": ["强度等级选比", "每方材料估算", "砂率控制"],
        "scenes": ["砌筑砂浆配料", "墙面抹灰估算", "地面找平算量"],
    },
    "renovation-labor-cost": {
        "name": "装修人工费估算",
        "intro": "按工种与计费方式粗算装修人工总价，辅助半包比价与合同核算。",
        "feats": ["项目单价核算", "点工包工对比", "人工材料分离"],
        "scenes": ["半包人工列项", "工种工价比对", "增项防漏核算"],
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
    if "工作与生活中的相关计算与查询" in s or "纯前端处理，数据不上传" in s:
        print("WARN 套话残留（检查）:", name)
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
c = clean_opt("estimate-area-dosage", OPT_OLD, OPT_NEW)
if c:
    total += c
    print((("DRY " if DRY else "") + "opt estimate-area-dosage"))
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
