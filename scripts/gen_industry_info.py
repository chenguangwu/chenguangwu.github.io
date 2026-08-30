#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B0: 生成 js/industry-info.js —— 全量行业（中文名 + emoji 图标）字典。

背景：js/app.js 里 INDUSTRY_INFO 只有 77 个行业有中文名，其余 192 个缺失，
导致首页分类导航只能显示英文 slug（accounting/acoustics…）。
本脚本从 tools/<key>/index.html 的 <title> 提取中文名（行业页 title 由
_build.py 生成，是权威来源），配上语义 emoji，输出 window.INDUSTRY_INFO。

用法：python3 scripts/gen_industry_info.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 导航显示别名：解决不同 slug 提取出相同中文名的问题（行业页 title 不动，仅导航显示用）
NAME_OVERRIDE = {
    'pets': '宠物饲养',          # pet 已占「宠物养护」
    'service': '生活服务',        # customer-service 已占「客户服务」
    'water': '水务管理',          # hydraulic 已占「水利工程」
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
    """从行业页提取 (中文名, h1 自带 emoji)。
    title: '会计审计工具集合 - ToolBox' -> '会计审计'
    h1   : '🔊 声学工具'                 -> '🔊'（若为默认 🔧 则忽略）"""
    p = os.path.join(ROOT, 'tools', key, 'index.html')
    if not os.path.exists(p):
        return None, None
    src = open(p, encoding='utf-8').read()
    m = re.search(r'<title>([^<]*)</title>', src)
    if not m:
        return None, None
    name = m.group(1).replace('工具集合 - ToolBox', '').strip()
    # 清掉 title 里可能带的英文 slug 后缀，如 '宠物养护（pet）'
    name = re.sub(r'[（(]\s*[a-z0-9\-]+\s*[)）]', '', name).strip()
    name = re.sub(r'工具$', '', name).strip()

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
        # 1) 导航别名优先（解决同名冲突）
        h1_icon = None
        name = NAME_OVERRIDE.get(k)
        if not name:
            name, h1_icon = extract_info(k)
        if not name:
            missing.append(k)
            name = k
        # 图标优先级：手工 ICON_MAP > 行业页 h1 自带专属图标 > 默认 🔧
        icon = ICON_MAP.get(k) or h1_icon or DEFAULT_ICON
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
        '/* 数据来源：tools/<key>/index.html 的 <title>（_build.py 生成，权威） + 语义 emoji 映射 */',
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
