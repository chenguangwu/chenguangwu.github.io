#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B0: 生成 js/industry-info.js —— 全量行业（中文名 + emoji 图标）字典。

背景：js/app.js 里 INDUSTRY_INFO 只有 77 个行业有中文名，其余 192 个缺失，
导致首页分类导航只能显示英文 slug（accounting/acoustics…）。
本脚本从 _build.py 的 INDUSTRY_DEFS 取权威中文短名（覆盖 268/268 全量行业），
配上语义 emoji，输出 window.INDUSTRY_INFO。

⚠️ 重要规则（2026-09-07 老板明确）：
  - name（行业显示名）只取**短名**（如 "设计创意"），不要再写成描述长串
    （如 "设计创意在线工具集合 - 免费实用的设计创意工具箱"）。
  - 真正的描述走 tools/<key>/index.html 的 <meta description> 与 og:description,
    不再被抽进 name。
  - 解析顺序：NAME_OVERRIDE（导航别名） > INDUSTRY_DEFS 短名（权威） > title 截断（兜底）。

用法：python3 scripts/gen_industry_info.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 加载 _build.py 中的 INDUSTRY_DEFS 作为权威短名源（268/268 覆盖）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 关键：脚本在 scripts/ 下运行时 sys.path[0] 是 scripts/ 而非项目根，必须把 ROOT 也加入，
# 否则 from _build import 会失败掉进 except 退路（退路正则与 (emoji,name) 顺序不匹配 → icon 错成首字）
sys.path.insert(0, ROOT)
try:
    from _build import INDUSTRY_DEFS as _INDUSTRY_DEFS
except Exception:
    # 退路：直接正则抽
    _src = open(os.path.join(ROOT, '_build.py'), encoding='utf-8').read()
    _INDUSTRY_DEFS = {}
    _m = re.search(r'INDUSTRY_DEFS\s*=\s*\{', _src)
    if _m:
        _end = _src.index('\n}\n', _m.end()) + 3
        _seg = _src[_m.start():_end]
        for _mm in re.finditer(r"'([^']+)'\s*:\s*\(\s*'([^']+)'\s*,\s*'([^']+)'", _seg):
            # 元组顺序与 _build.py 一致：(emoji, 中文短名)；存元组而非字符串，避免 [0] 取到 name[0]
            _INDUSTRY_DEFS[_mm.group(1)] = (_mm.group(2), _mm.group(3))

# 导航显示别名：解决不同 slug 提取出相同中文名的问题（行业页 title 不动，仅导航显示用）
NAME_OVERRIDE = {
    'pets': '宠物饲养',          # pet 已占「宠物养护」
    'service': '生活服务',        # customer-service 已占「客户服务」
    'water': '水务管理',          # hydraulic 已占「水利工程」
    # 二级分类名统一压到 4 字以内：下拉面板列宽约 161px，5 字以上会被截断
    'uiux': 'UI设计',            # 原「UI/UX设计」7 字
    'ai': '人工智能',             # 原「AI 人工智能」6 字
    'signal': '信号系统',          # 原「信号与系统」5 字
}

# emoji 映射：key -> emoji。优先用行业页 h1 自带的专属图标，缺失的在此补齐
ICON_MAP = {
    'accessibility': '♿', 'accounting': '🧾', 'acupuncture': '🪡', 'admin': '🗂️',
    'advertising': '📣', 'aerospace': '🚀', 'antiques': '🏺', 'aquaculture': '🐟',
    'archaeology': '🏺', 'archive': '🗄️', 'astronomy': '🔭', 'audio': '🎧',
    'auto-beauty': '🚘', 'baking': '🧁', 'ballistics': '🎯', 'beekeeping': '🐝',
    'beneficiation': '⛏️', 'blasting': '💥', 'bonding': '🧷', 'brand': '🏷️',
    'bridge': '🌉', 'building-material': '🧱', 'cable': '🔌', 'cardiology': '🫀',
    'casting': '🔥', 'ceramics': '🏺', 'chess': '♟️', 'chinese-cook': '🥘',
    'civil': '🏗️', 'cleaning': '🧹', 'clinical-lab': '🔬', 'clinical-nursing': '💉',
    'cnc': '⚙️', 'community': '🏘️', 'consulting': '💬', 'content': '✍️',
    'convenience': '🏪', 'cosmetic-derm': '✨', 'cosmetics': '💅',
    'customer-service': '🎧', 'daily-goods': '🛒', 'dance': '💃', 'decor': '🛋️',
    'defense': '🛡️', 'dentistry': '🦷', 'dermatology': '🧴', 'discipline': '📋',
    'domestic': '🧺', 'dyeing': '🎨', 'ecommerce': '🛍️', 'elderly': '👴',
    'electrical': '🔌', 'embedded': '🔲', 'endocrinology': '🧬', 'engineering': '⚙️',
    'ent': '👂', 'event': '🎪', 'exhibition': '🎫', 'express': '📦',
    'film': '🎞️', 'fire': '🚒', 'fire-rescue': '🚒', 'fitness': '🏋️',
    'floral': '💐', 'food-processing': '🏭', 'food-safety': '🥗',
    'food-testing': '🧫', 'forensic-medicine': '⚖️', 'forex': '💱', 'fresh': '🧊',
    'funeral': '⚱️', 'furniture': '🪑', 'futures': '📉', 'gas': '🔥',
    'gastroenterology': '🩻', 'general': '⚙️', 'geology': '🪨', 'gis': '🗺️',
    'glass': '🪟', 'healthcare': '🩺', 'heattreat': '🔥', 'hematology': '🩸',
    'hotel': '🏨', 'hr': '👥', 'hvac': '❄️', 'hydraulic': '💧', 'insurance': '🛡️',
    'interior': '🖼️', 'jewelry': '💎', 'knowledge': '📚', 'landscape': '🌳',
    'leather': '👜', 'livestream': '📹', 'machinery': '⚙️', 'martial-arts': '🥊',
    'mechanical': '⚙️', 'media': '📰', 'metallurgy': '🔩', 'metalwork': '🔨',
    'meteorology': '🌤️', 'mold': '🧩', 'municipal': '🚧', 'nephrology': '🩺',
    'network': '🌐', 'neurology': '🧠', 'niche': '🎯', 'nutrition': '🥗',
    'obstetrics': '🤱', 'office': '📄', 'ophthalmology': '👁️', 'optical': '👓',
    'outdoor': '🏕️', 'packaging': '📦', 'paint': '🎨', 'paper': '📄',
    'pediatrics': '🧒', 'pharmacy': '💊', 'photography': '📸', 'plastic': '🧴',
    'pets': '🐱', 'service': '🛎️',
    'pneumatic': '💨', 'pr': '📢', 'printing': '🖨️', 'process': '🎛️',
    'procurement': '🛒', 'project': '📊', 'property': '🏢', 'psychiatry': '🧠',
    'psychology': '💭', 'pulmonology': '🫁', 'quality': '✅', 'railway': '🚆',
    'realestate': '🏘️', 'rehabilitation': '🦾', 'rental': '🔑',
    'reproductive-medicine': '🧬', 'research': '🎓', 'rheumatology': '🦴',
    'road': '🛣️', 'rubber': '🧴', 'safety': '🦺', 'securities': '📈',
    'security': '🔒', 'security-guard': '👮', 'seismology': '🌐',
    'shipping': '🚢', 'sports-event': '🏆', 'stage': '🎭', 'steel': '🏗️',
    'stone': '🪨', 'supplychain': '🚛', 'surface': '✨', 'surveying': '📐',
    'tcm-chemistry': '🌿', 'tcm-diagnosis': '🩺', 'tcm-pharmacy': '🌿',
    'telecom': '📡', 'timber': '🪵', 'transport': '🚚', 'tunnel': '🚇',
    'uiux': '🎨', 'unitedfront': '🤝', 'urban': '🏙️', 'urology': '🩺',
    'usedcar': '🚙', 'warehouse': '🏬', 'water': '💧', 'wedding': '💒',
    'welding': '🔥', 'woodwork': '🪚', 'yoga': '🧘',
}

DEFAULT_ICON = '🔧'


def extract_info(key):
    """兜底：从行业页 title 抽出**短名**（仅在 INDUSTRY_DEFS 没收录时用）。

    原则：name 必须保持短名，不再允许把描述（如"…在线工具集合 - 免费实用的…工具箱"）
    灌进 name。title 当前格式为「<短名>在线工具集合 - 免费实用的<短名>工具箱」，故优先
    匹配前缀 token；不匹配时再 fallback 到去后缀解析。

    例：
      '设计创意在线工具集合 - 免费实用的设计创意工具箱' -> '设计创意'
      '会计审计工具集合 - ToolBox'                       -> '会计审计'
    """
    p = os.path.join(ROOT, 'tools', key, 'index.html')
    if not os.path.exists(p):
        return None, None
    src = open(p, encoding='utf-8').read()
    m = re.search(r'<title>([^<]*)</title>', src)
    if not m:
        return None, None
    raw = m.group(1).strip()

    # 规则 1：剥历史后缀 '工具集合 - ToolBox'（旧版短 title）
    s = raw.replace('工具集合 - ToolBox', '').strip()

    # 规则 2：尝试按当前长 title 模板「X 在线工具集合 - 免费实用的X工具箱」取 X
    mt = re.match(r'^(.+?)在线工具集合\s*-\s*免费实用的.+?工具箱$', s)
    if mt:
        name = mt.group(1).strip()
    else:
        # 规则 3：通用去后缀（如「X 工具集合」/「X 工具」）
        s = re.sub(r'[（(]\s*[a-z0-9\-]+\s*[)）]', '', s).strip()
        s = re.sub(r'工具(?:集合)?\s*$', '', s).strip()
        name = s

    h1_icon = None
    h = re.search(r'<h1[^>]*>([^<]*)</h1>', src)
    if h:
        mh = re.match(r'^\s*(\S+)\s+', h.group(1))
        if mh and mh.group(1) != DEFAULT_ICON:
            h1_icon = mh.group(1)
    return (name or None), h1_icon


def main():
    tools = json.load(open(os.path.join(ROOT, 'json', 'tools.json'), encoding='utf-8'))
    inds = sorted({t.get('industry') for t in tools if t.get('industry')})

    rows = []
    missing = []
    for k in inds:
        # 1) 导航别名优先（解决同名冲突，如 pets/service/water/uiux）
        h1_icon = None
        name = NAME_OVERRIDE.get(k)
        # 2) INDUSTRY_DEFS 权威短名（覆盖 268/268，2026-09-07 老板明确禁止把
        #    description 灌进 name，所以此处作为 name 的首选来源）
        if not name:
            _def = _INDUSTRY_DEFS.get(k)
            if _def:
                name = _def[1] if isinstance(_def, (tuple, list)) else _def
        # 3) 兜底：从 tools/<key>/index.html 的 title 抽取短名
        if not name:
            name, h1_icon = extract_info(k)
        if not name:
            missing.append(k)
            name = k
        # 图标优先级：INDUSTRY_DEFS[0] 权威源 > 手工 ICON_MAP 覆盖 > 行业页 h1 图标 > 默认 🔧
        # 说明：INDUSTRY_DEFS[0] 已补全语义 emoji（无 🔧），作为分类图标的单一权威源，
        # 与行业页 H1 / sitemap / 面包屑保持一致；ICON_MAP 仅作手工微调覆盖（一般保持同步）。
        icon = _INDUSTRY_DEFS.get(k, (DEFAULT_ICON, k))[0] or ICON_MAP.get(k) or h1_icon or DEFAULT_ICON
        rows.append((k, name, icon))

    # 同名检测（导航里两个相同中文名会造成困惑，告警但不阻塞）
    from collections import Counter
    dup = [n for n, c in Counter(n for _, n, _ in rows).items() if c > 1]
    if dup:
        print(f'⚠️  重复中文名 {len(dup)} 个: {dup}')
    if missing:
        print(f'⚠️  未取到中文名 {len(missing)} 个: {missing}')

    # 生成 js/industry-info.js
    lines = [
        '/* 全站行业字典（中文名 + emoji 图标）—— 由 scripts/gen_industry_info.py 生成，勿手改 */',
        '/* 数据来源：_build.py INDUSTRY_DEFS 短名（权威，268/268）+ 语义 emoji 映射；仅显示用短名，描述走页面 meta */',
        'window.INDUSTRY_INFO = {',
    ]
    width = max(len(k) for k, _, _ in rows)
    for k, name, icon in rows:
        # key 含连字符（如 auto-beauty），必须加引号，否则 JS 语法错误
        lines.append(f"  '{k}'".ljust(width + 4) + f": {{ name: '{name}', icon: '{icon}' }},")
    lines.append('};')
    lines.append('')
    out = os.path.join(ROOT, 'js', 'industry-info.js')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'✅ 生成 {out}：{len(rows)} 个行业（原有 77 个有中文名，本次补齐全部）')


if __name__ == '__main__':
    main()
