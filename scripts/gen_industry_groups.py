#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B1: 生成 json/industry-groups.json —— 266 个子行业 → ~10 个一级分类。

布局参考 chinaz tools/nav：顶部一级横向菜单，下拉面板左侧=子行业列表，
右侧=选中子行业的常用工具（名称 + 描述）。

用法：python3 scripts/gen_industry_groups.py
      _build.py 后续会自动调用（幂等）。
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 人工补齐的工具描述（源数据确实没写的那批）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from tool_desc_override import DESC_OVERRIDE
except ImportError:      # pragma: no cover - 数据文件缺失时降级为空表
    DESC_OVERRIDE = {}

# ---- 中英文名/描述选取 ----------------------------------------------------
# 背景：_build.py 会对部分页面做「英文 title 预渲染」，导致 tools.json 里
#   name（来自 <title>）与 desc 的中英属性是互换的：
#     · 4905 条：name=中文名，desc=英文描述
#     · 109  条：name=英文名，desc=中文描述
# 因此统一规则：**谁含中日韩字符，谁就是中文那一侧**，另一侧即为英文。
CJK = re.compile(r'[\u4e00-\u9fff]')

# 质量优先序：下拉面板/首页展示优先挑 A 级工具，避免只按文件名取到低质页
QUALITY_ORDER = {'A': 0, 'B': 1, 'C': 2}

_desc_cache = {}


def zh_name(t):
    """中文名：name 与 desc 中含中文的那个。"""
    n = t.get('name') or ''
    d = t.get('desc') or ''
    return n if CJK.search(n) else (d if CJK.search(d) else n)


def en_name(t):
    """英文名：优先用 _en_override 产出的 en 字段，否则取 name/desc 中不含中文的一侧。"""
    e = (t.get('en') or '').strip()
    if e and not CJK.search(e):
        return e
    n = t.get('name') or ''
    d = t.get('desc') or ''
    v = n if not CJK.search(n) else (d if not CJK.search(d) else n)
    return re.sub(r'^[\s.]+', '', v) or n


# ed 字段里大量「Free online tool on ToolBox — 100% client-side」这类模板签名，
# 直接展示会满屏套话（实测 1648 条中 1519 条、92% 是模板腔），先剥掉再判断有无实质内容
ED_BOILERPLATE = [
    r'\s*[.\-–—,]?\s*Free online tool on ToolBox.*$',
    r'\s*[.\-–—,]?\s*\d+%\s*client[-\s]side.*$',
    r'\s*[.\-–—,]?\s*Free online tool\b.*$',
    r'\s*[.\-–—,]?\s*Free and (secure|instant)\.?\s*$',
    r'\s*[.\-–—,]?\s*Browser[-\s]only\.?\s*$',
    r'\s*[.\-–—,]?\s*No sign[- ]up\.?\s*$',
    # 「encode and decode online / calculate online, free and accurate」这类
    # 只说动作不说内容的空话，同样没有信息量
    r'\s*[.\-–—,]?\s*\w+\s+(and\s+\w+\s+)?online\b.*$',
    r'\s*,\s*free and \w+[\w\s]*$',
    r'\s*[.\-–—,]?\s*Free\s*$',
]


def strip_ed_boilerplate(s):
    for pat in ED_BOILERPLATE:
        s = re.sub(pat, '', s, flags=re.I)
    return s.strip().rstrip(' .,-–—:·|')


def en_desc(t):
    """英文描述：取 tools.json 的 ed 字段，去掉「英文名 - 」前缀后截断。

    ed 形如 ".gitignore Generator - Pick stacks ... Free, browser-only."，
    直接显示会和卡片标题重复，故先剥掉名字前缀。
    """
    raw = (t.get('ed') or '').strip()
    if not raw:
        return ''
    name = en_name(t)
    if name and raw.startswith(name):
        stripped = raw[len(name):].lstrip(' -–—:·|')
        if stripped:
            raw = stripped
    clean = strip_ed_boilerplate(raw)
    # 洗掉模板腔后没剩多少实质内容，就不显示描述（宁缺毋滥，避免满屏套话）
    return clip(clean, 60) if len(clean) >= 20 else ''


def clip(s, n=32):
    s = (s or '').strip()
    if len(s) <= n:
        return s
    return s[:n - 1].rstrip('，,。、；;：: ') + '…'


def meta_desc(path):
    """从工具页 <meta name="description"> 取中文描述（只读前 12KB，带缓存）。"""
    if path in _desc_cache:
        return _desc_cache[path]
    d = ''
    try:
        with open(os.path.join(ROOT, 'tools', path), encoding='utf-8', errors='ignore') as f:
            head = f.read(12000)
        m = re.search(r'<meta name="description" content="([^"]*)"', head)
        if m:
            d = html.unescape(m.group(1)).strip()
    except Exception:
        d = ''
    _desc_cache[path] = d
    return d


def tool_sort_key(t):
    return (QUALITY_ORDER.get(t.get('quality', 'C'), 3), t.get('file', ''))

# 一级分类：(group_key, 中文名, icon, 英文名) —— 英文名供英文态导航使用
GROUPS = [
    ('it', 'IT开发', '💻', 'IT & Dev'),
    ('design', '设计创意', '🎨', 'Design'),
    ('finance', '金融财务', '💰', 'Finance'),
    ('health', '健康医疗', '🏥', 'Health'),
    ('engineering', '工程制造', '⚙️', 'Engineering'),
    # 以下两个由「工程制造」「商业办公」拆分而来（原工程制造 69 个、商业办公 51 个，
    # 二级分类过多导致下拉面板一屏放不下）
    ('matchem', '材料化工', '🧪', 'Materials'),
    ('translogi', '交通物流', '🚚', 'Transport'),
    ('science', '科学研究', '🔬', 'Science'),
    ('life', '生活实用', '🏠', 'Life'),
    ('edu', '教育培训', '📚', 'Edu'),
    ('business', '商业办公', '💼', 'Business'),
    # 英文名取短：12 个菜单项在 1280px 容器内排布，长名会挤出横向滚动条
    ('entertainment', '休闲娱乐', '🎮', 'Leisure'),
]


# 常见缩写：避免 it -> "It" 这类不体面的首字母大写
ACRONYMS = {
    'it': 'IT', 'ai': 'AI', 'ui': 'UI', 'ux': 'UX', 'uiux': 'UI/UX', 'api': 'API',
    'seo': 'SEO', 'hr': 'HR', 'erp': 'ERP', 'crm': 'CRM', 'oa': 'OA', 'pdf': 'PDF',
    '3d': '3D', 'ar': 'AR', 'vr': 'VR', 'id': 'ID', 'iot': 'IoT', 'sql': 'SQL',
    'b2b': 'B2B', 'b2c': 'B2C', 'cad': 'CAD', 'cpu': 'CPU', 'gpu': 'GPU', 'css': 'CSS',
    'html': 'HTML', 'js': 'JavaScript', 'qc': 'QC', 'qa': 'QA', 'sms': 'SMS', 'gps': 'GPS',
}


def key_to_en(key):
    """行业 key -> 可读英文名（auto-beauty -> Auto Beauty，it -> IT）。"""
    parts = [w for w in str(key).split('-') if w]
    if not parts:
        return str(key)
    return ' '.join(ACRONYMS.get(w, w.capitalize()) for w in parts)

# 分类规则：行业 key -> 一级 group_key。列出的 key 优先按此表映射。
KEY_RULES = {
    # IT 开发
    'it': 'it', 'ai': 'it', 'data': 'it', 'encode': 'it', 'text': 'it', 'office': 'it',
    'network': 'it', 'security': 'it', 'electronics': 'it', 'telecom': 'it', 'embedded': 'it',
    # 设计创意
    'design': 'design', 'image': 'design', 'photo': 'design', 'photo2': 'design',
    'video': 'design', 'music': 'design', 'uiux': 'design', 'media': 'design',
    'advertising': 'design', 'film': 'design', 'beauty': 'design',
    'cosmetics': 'design', 'cosmetic-derm': 'design', 'photography': 'design',
    'floral': 'design', 'content': 'design',
    # 金融财务
    'finance': 'finance', 'accounting': 'finance', 'banking': 'finance', 'insurance': 'finance',
    'investment': 'finance', 'tax': 'finance', 'securities': 'finance', 'forex': 'finance',
    'futures': 'finance', 'economics': 'finance', 'audit': 'finance',
    # 健康医疗（含医疗科室、中医、护理、药学、康复）
    'health': 'health', 'medical': 'health', 'medical2': 'health', 'healthcare': 'health',
    'fitness': 'health', 'nutrition': 'health', 'elderly': 'health', 'parenting': 'health',
    'cardiology': 'health', 'dentistry': 'health', 'dermatology': 'health',
    'endocrinology': 'health', 'ent': 'health', 'gastroenterology': 'health',
    'hematology': 'health', 'nephrology': 'health', 'neurology': 'health',
    'obstetrics': 'health', 'ophthalmology': 'health', 'pediatrics': 'health',
    'psychiatry': 'health', 'pulmonology': 'health', 'rheumatology': 'health',
    'urology': 'health', 'acupuncture': 'health', 'tcm-pharmacy': 'health',
    'tcm-diagnosis': 'health', 'tcm-chemistry': 'health', 'clinical-lab': 'health',
    'clinical-nursing': 'health', 'forensic-medicine': 'health',
    'reproductive-medicine': 'health', 'rehabilitation': 'health', 'pharmacy': 'health',
    # 工程制造（含土木、机械、材料、化工、交通、能源、矿业、建筑）
    'engineering': 'engineering', 'mechanical': 'engineering', 'machinery': 'engineering',
    'manufacturing': 'engineering', 'electrical': 'engineering', 'civil': 'engineering',
    'construction': 'engineering', 'structural': 'engineering', 'hydraulic': 'engineering',
    'fire-rescue': 'engineering', 'mining': 'engineering', 'metallurgy': 'engineering',
    'metalwork': 'engineering', 'materials': 'engineering', 'aerospace': 'engineering',
    'automotive': 'engineering', 'energy': 'engineering', 'transport': 'engineering',
    'road': 'engineering', 'railway': 'engineering', 'tunnel': 'engineering',
    'bridge': 'engineering', 'surveying': 'engineering', 'geology': 'engineering',
    'gis': 'engineering', 'glass': 'engineering', 'ceramics': 'engineering',
    'paper': 'engineering', 'printing': 'engineering', 'packaging': 'engineering',
    'plastic': 'engineering', 'rubber': 'engineering', 'leather': 'engineering',
    'textile': 'engineering', 'textile2': 'engineering', 'dyeing': 'engineering',
    'chemical': 'engineering', 'chemistry': 'engineering', 'petrochem': 'engineering',
    'gas': 'engineering', 'fire': 'engineering', 'safety': 'engineering',
    'welding': 'engineering', 'casting': 'engineering', 'cnc': 'engineering',
    'woodworking': 'engineering', 'woodwork': 'engineering', 'timber': 'engineering',
    'stone': 'engineering', 'building-material': 'engineering', 'beneficiation': 'engineering',
    'blasting': 'engineering', 'bonding': 'engineering', 'surface': 'engineering',
    'heattreat': 'engineering', 'hvac': 'engineering', 'pneumatic': 'engineering',
    'process': 'engineering', 'quality': 'engineering', 'mold': 'engineering',
    'municipal': 'engineering', 'water': 'engineering', 'defense': 'engineering',
    'general': 'engineering', 'auto-beauty': 'engineering', 'steel': 'engineering',
    'supplychain': 'engineering',
    # 科学研究（数理、物理、天文、地球科学）
    'science': 'science', 'math': 'science', 'stats': 'science', 'statistics': 'science',
    'astronomy': 'science', 'acoustics': 'science', 'metrology': 'science',
    'geometry': 'science', 'quantum': 'science', 'optics': 'science',
    'thermodynamics': 'science', 'nuclear': 'science', 'seismology': 'science',
    'dynamics': 'science', 'electromagnetism': 'science', 'fluid': 'science',
    'kinematics': 'science', 'signal': 'science', 'research': 'science',
    # 生活实用
    'life': 'life', 'food': 'life', 'food-testing': 'life', 'food-safety': 'life',
    'food-processing': 'life', 'chinese-cook': 'life', 'baking': 'life',
    'home': 'life', 'gardening': 'life', 'gardening2': 'life', 'travel': 'life',
    'hotel': 'life', 'restaurant': 'life', 'wedding': 'life', 'funeral': 'life',
    'daily-goods': 'life', 'cleaning': 'life', 'domestic': 'life', 'convenience': 'life',
    'pets': 'life', 'pet': 'life', 'pet-training': 'life', 'livestock': 'life',
    'fishery': 'life', 'aquaculture': 'life', 'agriculture': 'life', 'beekeeping': 'life',
    'forestry': 'life', 'outdoor': 'life', 'accessibility': 'life',
    # 教育培训
    'edu': 'edu', 'edu2': 'edu', 'language': 'edu', 'exam': 'edu', 'history': 'edu',
    'literature': 'edu', 'writing': 'edu', 'knowledge': 'edu', 'library': 'edu',
    'archive': 'edu', 'museum': 'edu', 'chinese': 'edu', 'yi': 'edu', 'fengshui': 'edu',
    'fortune': 'edu', 'archaeology': 'edu',
    # 商业办公
    'biz': 'business', 'marketing': 'business', 'sales': 'business', 'hr': 'business',
    'startup': 'business', 'pr': 'business', 'consulting': 'business', 'procurement': 'business',
    'logistics': 'business', 'logistics2': 'business', 'warehouse': 'business',
    'express': 'business', 'shipping': 'business', 'ecommerce': 'business',
    'project': 'business', 'property': 'business', 'admin': 'business',
    'unitedfront': 'business', 'event': 'business', 'exhibition': 'business',
    'customer-service': 'business', 'service': 'business', 'brand': 'business',
    'usedcar': 'business', 'rental': 'business', 'niche': 'business',
    'community': 'business', 'discipline': 'business', 'legal': 'business', 'legal2': 'business',
    # 休闲娱乐
    'fun': 'entertainment', 'sports': 'entertainment', 'sports-event': 'entertainment',
    'chess': 'entertainment', 'dance': 'entertainment', 'yoga': 'entertainment',
    'martial': 'entertainment', 'martial-arts': 'entertainment', 'antiques': 'entertainment',
}

# === 拆分规则（覆盖上面的默认归属）========================================
# 起因：工程制造 69 个、商业办公 51 个二级分类，下拉面板一屏放不下。
# 从两者各拆出一批，新组「材料化工」「交通物流」两个一级分类；
# 顺带把原本兜底进「商业办公」的错位行业归到正经分类。
KEY_RULES.update({
    # —— 材料化工（原工程制造，31 个）——
    'chemistry': 'matchem', 'materials': 'matchem', 'metallurgy': 'matchem',
    'chemical': 'matchem', 'petrochem': 'matchem', 'rubber': 'matchem',
    'plastic': 'matchem', 'ceramics': 'matchem', 'glass': 'matchem',
    'textile': 'matchem', 'textile2': 'matchem', 'dyeing': 'matchem',
    'leather': 'matchem', 'paper': 'matchem', 'printing': 'matchem',
    'woodworking': 'matchem', 'woodwork': 'matchem', 'timber': 'matchem',
    'stone': 'matchem', 'metalwork': 'matchem', 'welding': 'matchem',
    'casting': 'matchem', 'heattreat': 'matchem', 'surface': 'matchem',
    'mold': 'matchem', 'cnc': 'matchem', 'mining': 'matchem',
    'beneficiation': 'matchem', 'steel': 'matchem',
    'paint': 'matchem', 'cable': 'matchem',           # 原商业办公
    # —— 交通物流（原工程制造 + 商业办公，17 个）——
    'automotive': 'translogi', 'transport': 'translogi', 'railway': 'translogi',
    'road': 'translogi', 'bridge': 'translogi', 'tunnel': 'translogi',
    'municipal': 'translogi', 'auto-beauty': 'translogi', 'supplychain': 'translogi',
    'usedcar': 'translogi', 'logistics': 'translogi', 'logistics2': 'translogi',
    'shipping': 'translogi', 'warehouse': 'translogi', 'express': 'translogi',
    'fresh': 'translogi', 'procurement': 'translogi',
    # —— 修正兜底错位（这些本来就不属于商业办公）——
    'meteorology': 'science', 'robotics': 'science', 'ballistics': 'science',
    'misc': 'science', 'eco': 'science', 'environment': 'science',
    'psychology': 'health', 'audio': 'design', 'stage': 'design',
    'niche': 'life', 'community': 'life',
})


def classify(key, cname):
    if key in KEY_RULES:
        return KEY_RULES[key]
    # 按中文名关键词兜底（避免 key 子串误伤，如 furniture 含 'it'）
    kw_map = [
        ('health', ['医', '药', '护理', '临床', '针灸', '中医', '康复', '口腔', '皮肤', '心血管', '内分泌', '耳鼻喉', '消化', '血液', '肾脏', '神经', '产科', '眼科', '儿科', '精神', '呼吸', '风湿', '泌尿', '生殖', '保健', '健康', '健身', '营养', '养老', '育儿', '美容皮肤']),
        ('engineering', ['工程', '机械', '制造', '电气', '土木', '建筑', '结构', '水利', '消防', '救援', '矿业', '冶金', '金属', '材料', '航空', '汽车', '能源', '交通', '铁路', '隧道', '桥梁', '测绘', '地质', '玻璃', '陶瓷', '印刷', '包装', '塑料', '橡胶', '皮革', '纺织', '印染', '化工', '化学', '石化', '燃气', '焊接', '铸造', '数控', '木材', '石材', '建材', '选矿', '爆破', '粘接', '表面', '热处理', '暖通', '气动', '模具', '市政', '水务', '钢铁', '供应链', '家居', '装修']),
        ('science', ['科学', '数学', '统计', '天文', '声学', '计量', '几何', '量子', '光学', '热力学', '核', '地震', '动力学', '电磁', '流体', '运动学', '信号', '材料学', '科研', '研究']),
        ('it', ['IT', '代码', '网络', '安全', '数据', '智能', '电子', '通信', '文本', '办公', '编码', '解码']),
        ('design', ['设计', '图像', '摄影', '视频', '音乐', '媒体', '广告', '化妆', '花艺', '内容']),
        ('finance', ['金融', '财务', '会计', '银行', '保险', '投资', '税务', '证券', '外汇', '期货', '经济', '审计']),
        ('life', ['生活', '食品', '家居', '园艺', '旅行', '酒店', '餐饮', '婚礼', '殡葬', '日用', '清洁', '家政', '宠物', '畜牧', '渔业', '水产', '农业', '养蜂', '林业', '户外', '烘焙', '烹饪']),
        ('edu', ['教育', '培训', '语言', '考试', '历史', '文学', '写作', '知识', '图书', '档案', '博物馆', '周易', '风水', '考古']),
        ('business', ['营销', '销售', '人力', '创业', '公关', '咨询', '采购', '物流', '仓储', '快递', '船运', '电商', '项目', '物业', '行政', '会展', '客服', '服务', '品牌', '二手车', '租赁', '社区', '规章', '法律', '法务']),
        ('entertainment', ['娱乐', '游戏', '体育', '棋', '舞蹈', '瑜伽', '武术', '古董']),
    ]
    for gk, kws in kw_map:
        for kw in kws:
            if kw in cname:
                return gk
    return 'business'


def main():
    tools = json.load(open(os.path.join(ROOT, 'json', 'tools.json'), encoding='utf-8'))
    # 工具数按行业聚合
    counts = {}
    for t in tools:
        ind = t.get('industry')
        if ind:
            counts[ind] = counts.get(ind, 0) + 1

    # 从 js/industry-info.js 提取中文名/图标（正则读 JS 对象，不 eval）
    info_src = open(os.path.join(ROOT, 'js', 'industry-info.js'), encoding='utf-8').read()
    m = re.search(r'window\.INDUSTRY_INFO = \{(.*?)\n\};', info_src, re.S)
    ind_info = {}
    if m:
        for line in m.group(1).splitlines():
            mm = re.search(r"'([a-z0-9\-]+)'\s*:\s*\{\s*name:\s*'([^']*)',\s*icon:\s*'([^']*)'", line)
            if mm:
                ind_info[mm.group(1)] = {'name': mm.group(2), 'icon': mm.group(3)}
    # 下面直接走 KEY_RULES 分类

    # 预读每个子行业的工具列表，用于下拉面板右侧展示
    industry_tools = {}
    for key in counts:
        ipath = os.path.join(ROOT, 'json', f'industry-{key}.json')
        if os.path.exists(ipath):
            industry_tools[key] = json.load(open(ipath, encoding='utf-8'))
        else:
            industry_tools[key] = []

    grouped = {gk: [] for gk, _n, _i, _e in GROUPS}
    for key, c in counts.items():
        info = ind_info.get(key, {'name': key, 'icon': '🔧'})
        gk = classify(key, info['name'])
        # A 级优先、同级按文件名，保证展示质量且每次构建结果稳定
        tools_sorted = sorted(industry_tools.get(key, []), key=tool_sort_key)
        top = []
        for t in tools_sorted[:8]:
            name_zh = zh_name(t)
            md = meta_desc(t.get('path', ''))
            # 中文描述优先级：① 页面中文 meta（含中文）→ ② 工具自带中文 d（_build.py 注入）
            # → ③ 中文名；避免页面 meta 因缺中文内容而回退英文时，卡片仍露英文描述。
            d_zh = (clip(md, 32) if CJK.search(md or '') else
                    clip(t.get('d') or '', 32) if CJK.search(t.get('d') or '') else
                    clip(name_zh, 40))
            d_en = en_desc(t)
            ov = DESC_OVERRIDE.get(name_zh)
            if ov:
                # 人工补齐表：任一侧留空表示沿用上面自动提取的结果
                if ov[0]:
                    d_zh = ov[0]
                if ov[1]:
                    d_en = ov[1]
            top.append({
                'name': name_zh,            # 中文名（导航中文态用）
                'en': en_name(t),            # 英文名（导航英文态用）
                'desc': clip(d_zh, 32),      # 中文描述
                'ed': clip(d_en, 60),        # 英文描述（导航英文态用）
                'url': '/' + t.get('url', ''),
                'icon': t.get('icon', ''),
                'bg': t.get('bg', '#f5f5f5'),
            })
        grouped.setdefault(gk, []).append({
            'key': key, 'name': info['name'], 'en': key_to_en(key), 'icon': info['icon'],
            'count': c, 'top': top,
        })

    # 每个一级分类内按工具数降序
    for gk in grouped:
        grouped[gk].sort(key=lambda x: -x['count'])

    out = []
    for gk, gname, gicon, gename in GROUPS:
        out.append({
            'key': gk,
            'name': gname,
            'en': gename,
            'icon': gicon,
            'count': sum(x['count'] for x in grouped[gk]),
            'children': grouped[gk],
        })

    out_path = os.path.join(ROOT, 'json', 'industry-groups.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f'✅ 生成 {out_path}')
    print('一级分类分布:')
    for item in out:
        print(f"  {item['icon']} {item['name']:6} {len(item['children']):3} 子行业  {item['count']:4} 工具")


if __name__ == '__main__':
    main()
