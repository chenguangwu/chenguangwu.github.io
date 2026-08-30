#!/usr/bin/env python3
"""
ToolBox Build Script
====================
Scans tools/ directory, extracts metadata, assigns categories and industries,
generates tools.json, injects tools array into index.html, generates sitemap.xml.

Usage: python3 _build.py

Metadata priority for each tool:
1. <meta name="toolbox" content="key=val,key=val"> tags in HTML head
2. <title> - tool name
3. <h2> - description
4. Filename-based category/industry rules
"""
import os
import sys
import re
import json
import glob
import hashlib
import subprocess
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(ROOT, 'README.md')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
try:
    from zh_en_dict import translate_name, translate_text
except Exception:
    # 兜底：翻译引擎缺失时返回原文，保证构建不中断
    def translate_name(s):
        return s or ''
    def translate_text(s):
        return s or ''

# 高频可见工具英文覆盖字典（scripts/gen_en_override.py 生成，AI 批量预翻）
OVERRIDE_PATH = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
try:
    with open(OVERRIDE_PATH, encoding='utf-8') as _f:
        EN_OVERRIDE = json.load(_f)
except Exception:
    EN_OVERRIDE = {}

# 顶部“Top 工具页”英文预渲染白名单（构建期内联）
TOP_TOOL_PRE_RENDER = {
    'tools/it/json-formatter.html',
    'tools/it/qrcode.html',
    'tools/it/password-generator.html',
    'tools/design/color-picker.html',
    'tools/it/regex.html',
    'tools/life/timestamp.html',
}

HOME_PRE_RENDER_I18N_EN = {
    'hero.title': 'Free Online Tools',
    'hero.sub': '6000+ free tools, all running locally in your browser. No sign-up, your data stays private.',
    'hero.tags': 'Popular:',
    'foot.tool_json': 'JSON Formatter',
    'foot.tool_qr': 'QR Code Generator',
    'foot.tool_pwd': 'Password Generator',
    'foot.tool_color': 'Color Picker',
    'foot.tool_regex': 'Regex Tester',
    'foot.tool_timestamp': 'Timestamp Converter',
    'hero.chain': 'Tool Chains: link multiple tools; one output fills the next input',
    'hero.badge1': 'Pure Frontend',
    'hero.badge2': 'No Data Upload',
    'hero.badge3': 'No Login Required',
    'hero.badge4': 'Free Forever, No Ads',
    'tab.hot': '🔥 Hot Tools',
    'tab.recent': '🕐 Recent Use',
    'tab.fav': '❤️ Favorites',
    'section.hottools': '🔥 Hot Tools',
    'btn.allHot': 'All hot tools →',
    'section.why': 'Why ToolBox',
    'why.sub': 'Not just another skin tool site, but a true toolbox by your side',
    'why.c1_title': 'No Data Upload',
    'why.c1_desc': 'All computation happens locally. No server upload, no data collection. You can process files with confidence.',
    'why.c2_title': 'Fast Pure Frontend Start',
    'why.c2_desc': 'No backend waiting and no spinning loading animations. Open, use, and exit directly.',
    'why.c3_title': 'No Ads, No Login',
    'why.c3_desc': 'No popups, no forced registration, no usage cap. Use freely, leave immediately. Free forever.',
    'why.c4_title': '6000+ Full Coverage',
    'why.c4_desc': 'From developers to daily life, this is a one-stop toolbox with 200+ niche industries.',
    'section.hotcat': 'Popular Categories',
    'section.comtools': 'Common Tools',
    'section.about': 'About',
    'section.cat': 'Categories',
    'explore.title': '🧭 Explore Tools',
    'foot.sitemap': 'Sitemap',
    'foot.contact': 'Contact & Feedback',
    'foot.manage_data': '🗂️ Manage local data',
    'footer.privacy': '© 2026 ToolBox · Pure Frontend Tools · Data stays in your browser',
    'tabbar.home': 'Home',
    'tabbar.cat': 'Category',
    'tabbar.hot': 'Hot',
    'tabbar.fav': 'Favorites',
}

_TOP_TOOL_BODY_CACHE = {}

def _load_tool_body(i18n_dir, industry, slug):
    """按行业 + slug 读取 body 翻译：title/intro 英文稿。"""
    key = (industry, slug)
    if key in _TOP_TOOL_BODY_CACHE:
        return _TOP_TOOL_BODY_CACHE[key]

    p = os.path.join(i18n_dir, '%s-body.json' % industry)
    if not os.path.exists(p):
        _TOP_TOOL_BODY_CACHE[key] = {}
        return {}

    try:
        with open(p, encoding='utf-8') as f:
            body = json.load(f)
        entry = body.get(slug, {}) if isinstance(body, dict) else {}
        if not isinstance(entry, dict):
            entry = {}
    except Exception:
        entry = {}

    _TOP_TOOL_BODY_CACHE[key] = entry
    return entry


def _replace_data_i18n_text(html, key, text):
    """将 data-i18n=key 节点文本替换为 text（按首个内层文本，不碰属性）。"""
    if not text:
        return html
    escaped = esc_html_py(text)
    pattern = re.compile(r'(<[^>]*\bdata-i18n="%s"[^>]*>)(.*?)(</[^>]+>)' % re.escape(key), re.S)

    def _swap(m):
        return '%s%s%s' % (m.group(1), escaped, m.group(3))

    html, changed = pattern.subn(_swap, html)
    return html


def _replace_h1_text(html, text):
    if not text:
        return html
    pattern = re.compile(r'(<h1\b[^>]*>)([\s\S]*?)(</h1>)', re.S)
    return pattern.sub(lambda m: '%s%s%s' % (m.group(1), esc_html_py(text), m.group(3)), html, count=1)


def _prerender_tool_body(content, entry):
    """构建期把英文 title/intro 预渲染进工具页 h2 + 首个 p，并加 data-zh 保存中文原文。

    目的：让无 JS 的首抓（含英文 SEO 爬虫）直接拿到英文正文，不必等运行时 fetch -body.json。
    中文用户由运行时 applyToolBody 用 data-zh 还原（英文用户走 -body.json，逻辑不变）。
    仅处理含中文的节点，已是英文的页不动 —— 保证幂等且不影响纯英文工具页。
    """
    if not isinstance(entry, dict):
        return content
    en_title = (entry.get('title') or '').strip()
    en_intro = (entry.get('intro') or '').strip()
    if not en_title and not en_intro:
        return content

    _cjk = re.compile(r'[\u4e00-\u9fff]')

    if en_title:
        def _h2(m):
            open_tag, attrs, inner, close = m.group(1), m.group(2), m.group(3), m.group(4)
            if not _cjk.search(inner):
                return m.group(0)  # 已是英文，不动
            orig = inner
            mm = re.match(r'^([^\u4e00-\u9fffA-Za-z0-9]*)([\s\S]*)$', orig)
            icon = mm.group(1) if mm else ''
            new_text = icon + en_title
            if 'data-zh=' not in attrs:
                attrs = attrs.rstrip('>') + ' data-zh="%s">' % esc_html_py(orig)
            return '%s%s%s%s' % (open_tag, attrs, esc_html_py(new_text), close)
        content = re.sub(r'(<h2\b)([^>]*>)([\s\S]*?)(</h2>)', _h2, content, count=1)

    if en_intro:
        def _p(m):
            open_tag, attrs, inner, close = m.group(1), m.group(2), m.group(3), m.group(4)
            if not _cjk.search(inner):
                return m.group(0)  # 已是英文，不动
            orig = inner
            new_text = en_intro
            if 'data-zh=' not in attrs:
                attrs = attrs.rstrip('>') + ' data-zh="%s">' % esc_html_py(orig)
            return '%s%s%s%s' % (open_tag, attrs, esc_html_py(new_text), close)
        content = re.sub(r'(<p\b)([^>]*>)([\s\S]*?)(</p>)', _p, content, count=1)

    return content

def _slug_of(t):
    # 覆盖字典 key 采用「行业/basename」精确匹配，避免 calc-N 这类跨行业复用 basename 的错配。
    u = t.get('u') or t.get('url') or t.get('file') or ''
    base = u.split('/')[-1].replace('.html', '') or t.get('s') or ''
    ind = t.get('i') or t.get('industry') or ''
    if ind and base:
        return ind + '/' + base
    return base

def apply_en_override(t):
    """覆盖字典优先：slug 命中则采用人工/语义预翻的 en/ed（绝覆盖规则引擎产物）。"""
    slug = _slug_of(t)
    if slug and slug in EN_OVERRIDE:
        ov = EN_OVERRIDE[slug]
        if ov.get('en'):
            t['en'] = ov['en']
        if ov.get('ed'):
            t['ed'] = ov['ed']
    return t

TOOLS_DIR = os.path.join(ROOT, 'tools')
INDEX_FILE = os.path.join(ROOT, 'index.html')
SITEMAP_FILE = os.path.join(ROOT, 'sitemap.xml')
HTML_SITEMAP_FILE = os.path.join(ROOT, 'sitemap.html')
TOOLS_JSON_FILE = os.path.join(ROOT, 'json', 'tools.json')
TOOL_RUNTIME_MARKER = '<!-- TOOLBOX-TOOL-RUNTIME -->'
CLARITY_MARKER = '<!-- TOOLBOX-CLARITY -->'

# ============================================================
# 多语言（i18n）常量 —— 与 js/i18n.js LANG_REGISTRY 保持一致
# hreflang 采用构建期常量：每个 locale 对应一个规范 URL（语言由 ?lang 客户端切换，
# 不做 ?lang 查询态 alternate，避免爬取/索引出现 404）。
# ============================================================
I18N_LOCALES = ['zh-CN', 'en-US']
I18N_XDEFAULT = 'en-US'
I18N_HREFLANG_MARKER = '<!-- TOOLBOX-HREFLANG -->'


def _loc_under(locale):
    """hreflang/og:locale 用连字符；OpenGraph 用下划线（zh_CN / en_US）"""
    return locale.replace('-', '_')


def build_hreflang_block(abs_url, default_locale='zh-CN'):
    """生成全套 hreflang alternate 链接（含 x-default）+ og:locale。
    幂等：整体包裹在 I18N_HREFLANG_MARKER 注释内，重复构建不叠加。"""
    lines = [I18N_HREFLANG_MARKER]
    for loc in I18N_LOCALES:
        lines.append('<link rel="alternate" hreflang="%s" href="%s">'
                     % (loc, abs_url))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">'
                 % abs_url)
    lines.append('<meta property="og:locale" content="%s">'
                 % _loc_under(default_locale))
    for loc in I18N_LOCALES:
        if loc != default_locale:
            lines.append('<meta property="og:locale:alternate" content="%s">'
                         % _loc_under(loc))
    return '\n'.join(lines) + '\n'


def inject_hreflang(content, abs_url, default_locale='zh-CN'):
    """向 <head> 注入 hreflang / og:locale（幂等）。"""
    if I18N_HREFLANG_MARKER in content:
        marker_pos = content.find(I18N_HREFLANG_MARKER)
        end_pos = content.find('</head>', marker_pos)
        if end_pos != -1:
            return content[:marker_pos] + build_hreflang_block(abs_url, default_locale) + content[end_pos:]
    block = build_hreflang_block(abs_url, default_locale)
    if '</head>' in content:
        content = content.replace('</head>', block + '</head>', 1)
    return content


def _xhtml_alternates(abs_url):
    """sitemap <url> 内的 xhtml:link 多语言变体。

    中文为默认可索引版本（zh-CN / x-default 均自指本页）。
    英文态由 js/i18n.js 在 ?lang=en 时客户端切换；Google 跑 JS 后渲染为英文，
    故用 en-US -> 原URL?lang=en 声明英文变体（hreflang 语言信号优先级高于
    canonical，Google 会将其识别为英文版本）。百度/Bing 不跑/晚跑 JS 抓到中文态，
    会忽略或当作中文处理，无害。
    """
    sep = '?' if '?' not in abs_url else '&'
    en_url = abs_url + sep + 'lang=en'
    return ('    <xhtml:link rel="alternate" hreflang="zh-CN" href="%s"/>\n'
            '    <xhtml:link rel="alternate" hreflang="en-US" href="%s"/>\n'
            '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>') % (abs_url, en_url, abs_url)

# ============================================================
# Category definitions (functional)
# ============================================================
CAT_DEFS = {
    'text':      ('📝', '#e8eaf6', '文本处理'),
    'encode':    ('🔐', '#f3e5f5', '编码解码'),
    'convert':   ('🔄', '#e8eaf6', '格式转换'),
    'generate':  ('🎲', '#e3f2fd', '生成器'),
    'dev':       ('🔧', '#fff3e0', '开发工具'),
    'design':    ('🎨', '#fce4ec', '设计工具'),
    'image':     ('🖼️', '#e8f5e9', '图片处理'),
    'math':      ('🧮', '#e8eaf6', '数学计算'),
    'calculator':('🔢', '#e3f2fd', '通用计算器'),
    'validator': ('✅', '#ffebee', '验证器'),
    'reference': ('📚', '#ede7f6', '速查表'),
    'game':      ('🎮', '#fff8e1', '游戏趣味'),
    'finance':   ('💰', '#fff8e1', '金融投资'),
    'health':    ('💪', '#e8f5e9', '健康医疗'),
    'engineer':  ('⚙️', '#e3f2fd', '工程计算'),
    'life':      ('🏠', '#fce4ec', '日常生活'),
    'edu':       ('📖', '#e0f7fa', '教育学习'),
    'legal':     ('⚖️', '#fce4ec', '法律合规'),
    'music':     ('🎵', '#f3e5f5', '音乐艺术'),
    'photo':     ('📷', '#e8f5e9', '摄影影视'),
    'travel':    ('✈️', '#e1f5fe', '旅行出行'),
    'marketing': ('📢', '#fff3e0', '营销推广'),
    # 专业/公式域分类（补足中文名，避免分类标签显示原始英文 slug）
    'accounting':      ('💼', '#e8eaf6', '会计'),
    'acoustics':       ('🔊', '#e3f2fd', '声学'),
    'aerospace':       ('🚀', '#e1f5fe', '航天工程'),
    'astronomy':       ('🔭', '#ede7f6', '天文学'),
    'banking':         ('🏦', '#e8f5e9', '银行学'),
    'chemistry':       ('🧪', '#e8f5e9', '化学'),
    'dynamics':        ('⚙️', '#e3f2fd', '动力学'),
    'economics':       ('📈', '#fff8e1', '经济学'),
    'electromagnetism':('⚡', '#fff3e0', '电磁学'),
    'energy':          ('🔋', '#e0f7fa', '能源'),
    'fluid':           ('💧', '#e1f5fe', '流体力学'),
    'fun':             ('🎉', '#fff8e1', '趣味工具'),
    'geometry':        ('📐', '#e8eaf6', '几何'),
    'insurance':       ('🛡️', '#fce4ec', '保险'),
    'investment':      ('📊', '#e3f2fd', '投资'),
    'kinematics':      ('🏃', '#e3f2fd', '运动学'),
    'materials':       ('🧱', '#f3e5f5', '材料科学'),
    'metrology':       ('📏', '#ede7f6', '计量学'),
    'nuclear':         ('☢️', '#fce4ec', '核物理'),
    'optics':          ('🔬', '#e8f5e9', '光学'),
    'process':         ('⚙️', '#e0f7fa', '过程控制'),
    'quantum':         ('⚛️', '#ede7f6', '量子物理'),
    'robotics':        ('🤖', '#e3f2fd', '机器人学'),
    'securities':      ('📈', '#fff8e1', '证券'),
    'signal':          ('📡', '#e8eaf6', '信号与系统'),
    'statistics':      ('📊', '#e3f2fd', '统计学'),
    'structural':      ('🏗️', '#f3e5f5', '结构工程'),
    'surveying':       ('📐', '#e8eaf6', '测绘'),
    'tax':             ('💰', '#fff8e1', '税务'),
    'thermodynamics':  ('🌡️', '#fff3e0', '热力学'),
}

# ============================================================
# Industry definitions
# ============================================================
INDUSTRY_DEFS = {
    # Tech & Engineering
    'it':            ('💻', 'IT 开发'),
    'ai':            ('🤖', 'AI 人工智能'),
    'data':          ('📊', '数据分析'),
    'engineering':   ('🔧', '工程计算'),
    'electronics':   ('⚡', '电子电路'),
    # Finance & Business
    'finance':       ('💰', '金融财务'),
    'biz':           ('💼', '商业办公'),
    'marketing':     ('📢', '营销推广'),
    'sales':         ('📈', '销售管理'),
    'startup':       ('🚀', '创业孵化'),
    # Design & Creative
    'design':        ('🎨', '设计创意'),
    'image':         ('🖼️', '图像处理'),
    'video':         ('🎬', '视频处理'),
    'music':         ('🎵', '音乐艺术'),
    'writing':       ('✍️', '写作创作'),
    # Life Services
    'life':          ('🏠', '日常生活'),
    'health':        ('❤️', '健康医疗'),
    'travel':        ('✈️', '旅行出行'),
    'food':          ('🍳', '美食烹饪'),
    'home':          ('🏡', '家居装修'),
    # Education & Culture
    'edu':           ('📖', '教育学习'),
    'language':      ('🌍', '语言翻译'),
    'exam':          ('📝', '考试备考'),
    'history':       ('📜', '历史人文'),
    'literature':    ('📚', '文学阅读'),
    # Professional Tools
    'legal':         ('⚖️', '法律合规'),
    'science':       ('🔬', '科学研究'),
    'math':          ('🧮', '数学计算'),
    'stats':         ('📈', '统计分析'),
    'medical':       ('🏥', '医疗专业'),
    # Entertainment
    'fun':           ('🎮', '娱乐游戏'),
    'entertainment': ('🎬', '影视娱乐'),
    'sports':        ('⚽', '体育竞技'),
    # Chinese Culture
    'chinese':       ('🀄', '中华文化'),
    'yi':            ('📐', '周易八卦'),
    'fengshui':      ('🏔️', '风水命理'),
    'fortune':       ('🔮', '运势占卜'),
    # Physical Industries
    'agriculture':   ('🌾', '农业种植'),
    'construction':  ('🏗️', '建筑地产'),
    'manufacturing': ('🏭', '制造业'),
    'logistics':     ('🚚', '物流运输'),
    'energy':        ('⚡', '能源电力'),
    'environment':   ('🌱', '环保生态'),
    'automotive':    ('🚗', '汽车交通'),
    'beauty':        ('💄', '美容护肤'),
    'pet':           ('🐾', '宠物养护'),
    'parenting':     ('👶', '育儿亲子'),
    'gardening':     ('🌿', '园艺种植'),
    'mining':        ('⛏️', '矿业冶金'),
    'textile':       ('🧵', '纺织服装'),
    'chemical':      ('⚗️', '化工材料'),
    'fishery':       ('🎣', '渔业水产'),
    'forestry':      ('🌲', '林业资源'),
    'livestock':     ('🐄', '畜牧养殖'),

    'accessibility': ('🔧', '无障碍工具'),
    'accounting': ('🔧', '会计审计'),
    'acupuncture': ('🔧', '针灸推拿'),
    'admin': ('🔧', '行政管理'),
    'advertising': ('🔧', '广告设计'),
    'aerospace': ('🔧', '航空航天'),
    'antiques': ('🔧', '古董鉴定'),
    'aquaculture': ('🔧', '水产养殖'),
    'archaeology': ('🔧', '考古文博'),
    'archive': ('🔧', '档案管理'),
    'astronomy': ('🔧', '天文观测'),
    'audio': ('🔧', '音频工具'),
    'auto-beauty': ('🔧', '汽车美容'),
    'automation': ('🔧', '工业自动化'),
    'baking': ('🔧', '烘焙甜点'),
    'ballistics': ('🔧', '弹道武器'),
    'beekeeping': ('🔧', '蜜蜂养殖'),
    'beneficiation': ('🔧', '选矿冶炼'),
    'blasting': ('🔧', '爆破工程'),
    'bonding': ('🔧', '粘接密封'),
    'brand': ('🔧', '品牌管理'),
    'bridge': ('🔧', '桥梁工程'),
    'building-material': ('🔧', '建筑材料'),
    'cable': ('🔧', '电缆电线'),
    'cardiology': ('🔧', '心血管科'),
    'casting': ('🔧', '铸造工程'),
    'ceramics': ('🔧', '陶瓷工艺'),
    'chess': ('🔧', '棋类游戏'),
    'chinese-cook': ('🔧', '中式烹饪'),
    'civil': ('🔧', '土木工程'),
    'cleaning': ('🔧', '清洁保洁'),
    'clinical-lab': ('🔧', '临床检验'),
    'clinical-nursing': ('🔧', '临床护理'),
    'cnc': ('🔧', '数控加工'),
    'community': ('🔧', '社区管理'),
    'consulting': ('🔧', '咨询顾问'),
    'content': ('🔧', '内容创作'),
    'convenience': ('🔧', '便利店务'),
    'cosmetic-derm': ('🔧', '美容皮肤'),
    'cosmetics': ('🔧', '化妆品'),
    'customer-service': ('🔧', '客户服务'),
    'daily-goods': ('🔧', '日用百货'),
    'dailychem': ('🔧', '日用化工'),
    'dance': ('🔧', '舞蹈艺术'),
    'decor': ('🔧', '室内装修'),
    'defense': ('🔧', '国防军事'),
    'dentistry': ('🔧', '口腔医学'),
    'dermatology': ('🔧', '皮肤性病'),
    'discipline': ('🔧', '规章制度'),
    'domestic': ('🔧', '家政服务'),
    'dyeing': ('🔧', '印染染色'),
    'ecommerce': ('🔧', '电子商务'),
    'elderly': ('🔧', '养老护理'),
    'electrical': ('🔧', '电气工程'),
    'embedded': ('🔧', '嵌入式'),
    'endocrinology': ('🔧', '内分泌科'),
    'ent': ('🔧', '耳鼻喉科'),
    'event': ('🔧', '活动策划'),
    'exhibition': ('🔧', '会展服务'),
    'express': ('🔧', '快递物流'),
    'film': ('🔧', '电影影视'),
    'fire': ('🔧', '消防安全'),
    'fire-rescue': ('🔧', '消防救援'),
    'fitness': ('🔧', '健身运动'),
    'floral': ('🔧', '花艺设计'),
    'food-processing': ('🔧', '食品加工'),
    'food-safety': ('🔧', '食品安全'),
    'food-testing': ('🔧', '食品检测'),
    'forensic-medicine': ('🔧', '法医学'),
    'forex': ('🔧', '外汇交易'),
    'fresh': ('🔧', '生鲜冷链'),
    'funeral': ('🔧', '殡葬服务'),
    'furniture': ('🔧', '家具制造'),
    'futures': ('🔧', '期货交易'),
    'gas': ('🔧', '燃气工程'),
    'gastroenterology': ('🔧', '消化内科'),
    'general': ('🔧', '通用工程'),
    'geology': ('🔧', '地质勘探'),
    'gis': ('🔧', '地理信息'),
    'glass': ('🔧', '玻璃工艺'),
    'hardware': ('🔧', '五金建材'),
    'healthcare': ('🔧', '医疗保健'),
    'heattreat': ('🔧', '热处理'),
    'hematology': ('🔧', '血液科'),
    'hotel': ('🔧', '酒店管理'),
    'hr': ('🔧', '人力资源'),
    'hvac': ('🔧', '暖通空调'),
    'hydraulic': ('🔧', '水利工程'),
    'insurance': ('🔧', '保险计算'),
    'interior': ('🔧', '室内装饰'),
    'jewelry': ('🔧', '珠宝首饰'),
    'knowledge': ('🔧', '知识管理'),
    'labor-protection': ('🔧', '劳动保护'),
    'landscape': ('🔧', '园林绿化'),
    'leather': ('🔧', '皮革加工'),
    'livestream': ('🔧', '直播电商'),
    'machinery': ('🔧', '机械制造'),
    'martial-arts': ('🔧', '武术格斗'),
    'mechanical': ('🔧', '机械工程'),
    'media': ('🔧', '媒体传播'),
    'metallurgy': ('🔧', '冶金材料'),
    'metalwork': ('🔧', '金属加工'),
    'meteorology': ('🔧', '气象天气'),
    'mold': ('🔧', '模具工程'),
    'municipal': ('🔧', '市政工程'),
    'nephrology': ('🔧', '肾脏内科'),
    'network': ('🔧', '网络技术'),
    'neurology': ('🔧', '神经内科'),
    'niche': ('🔧', '垂直工具'),
    'nutrition': ('🔧', '营养膳食'),
    'obstetrics': ('🔧', '产科医学'),
    'office': ('🔧', '办公文档'),
    'ophthalmology': ('🔧', '眼科医学'),
    'optical': ('🔧', '视光科学'),
    'outdoor': ('🔧', '户外运动'),
    'packaging': ('🔧', '包装工程'),
    'paint': ('🔧', '油漆涂料'),
    'paper': ('🔧', '造纸印刷'),
    'pediatrics': ('🔧', '儿科医学'),
    'pharma': ('🔧', '制药工程'),
    'pharmacy': ('🔧', '药学'),
    'photography': ('🔧', '摄影摄像'),
    'pipe': ('🔧', '管道工程'),
    'plastic': ('🔧', '塑料橡胶'),
    'pneumatic': ('🔧', '气动液压'),
    'port': ('🔧', '港口工程'),
    'pr': ('🔧', '公关传播'),
    'printing': ('🔧', '印刷技术'),
    'procurement': ('🔧', '采购供应'),
    'project': ('🔧', '项目管理'),
    'property': ('🔧', '物业管理'),
    'psychiatry': ('🔧', '精神心理'),
    'psychology': ('🔧', '心理咨询'),
    'pulmonology': ('🔧', '呼吸内科'),
    'quality': ('🔧', '质量管理'),
    'railway': ('🔧', '铁路工程'),
    'realestate': ('🔧', '房地产'),
    'rehabilitation': ('🔧', '康复医学'),
    'rental': ('🔧', '租赁管理'),
    'reproductive-medicine': ('🔧', '生殖医学'),
    'research': ('🔧', '科研学术'),
    'rheumatology': ('🔧', '风湿免疫'),
    'road': ('🔧', '道路工程'),
    'rubber': ('🔧', '橡胶制品'),
    'safety': ('🔧', '安全生产'),
    'securities': ('🔧', '证券投资'),
    'security': ('🔧', '网络安全'),
    'security-guard': ('🔧', '安保服务'),
    'seismology': ('🔧', '地震学'),
    'shipping': ('🔧', '船舶海运'),
    'sports-event': ('🔧', '体育赛事'),
    'stage': ('🔧', '舞台演出'),
    'steel': ('🔧', '钢铁冶金'),
    'stone': ('🔧', '石材加工'),
    'supplychain': ('🔧', '供应链'),
    'surface': ('🔧', '表面处理'),
    'surveying': ('🔧', '测绘工程'),
    'tcm-chemistry': ('🔧', '中药化学'),
    'tcm-diagnosis': ('🔧', '中医诊断'),
    'tcm-pharmacy': ('🔧', '中药学'),
    'telecom': ('🔧', '通信技术'),
    'timber': ('🔧', '木材加工'),
    'transport': ('🔧', '交通运输'),
    'tunnel': ('🔧', '隧道工程'),
    'uiux': ('🔧', 'UI/UX设计'),
    'unitedfront': ('🔧', '统战工作'),
    'urban': ('🔧', '城市规划'),
    'urology': ('🔧', '泌尿外科'),
    'usedcar': ('🔧', '二手车'),
    'valve': ('🔧', '阀门工程'),
    'warehouse': ('🔧', '仓储管理'),
    'water': ('🔧', '水利工程'),
    'wedding': ('🔧', '婚礼策划'),
    'welding': ('🔧', '焊接工程'),
    'woodwork': ('🔧', '木工制作'),
    'yoga': ('🔧', '瑜伽冥想'),
    # P4 · 补全缺名目录中文行业名（对齐真实子目录）
    'acoustics': ('🔊', '声学'),
    'audit': ('📋', '审计合规'),
    'banking': ('🏦', '银行学'),
    'chemistry': ('🧪', '化学'),
    'dynamics': ('🌀', '动力学'),
    'eco': ('🌱', '生态环保'),
    'economics': ('📊', '经济学'),
    'edu2': ('📚', '教学辅助'),
    'electromagnetism': ('⚡', '电磁学'),
    'encode': ('🔐', '编码转换'),
    'fluid': ('💧', '流体力学'),
    'gardening2': ('🌿', '园艺养护'),
    'geometry': ('📐', '几何'),
    'investment': ('💹', '投资理财'),
    'kids': ('🧸', '儿童成长'),
    'kinematics': ('🏃', '运动学'),
    'legal2': ('⚖️', '劳动法律'),
    'library': ('📚', '图书档案'),
    'logistics2': ('📦', '仓储物流'),
    'maritime': ('⚓', '海事航运'),
    'martial': ('🥋', '武术运动'),
    'materials': ('🧱', '材料科学'),
    'medical2': ('🏥', '医疗运营'),
    'metrology': ('📏', '计量学'),
    'misc': ('🧮', '通用计算'),
    'misc2': ('🛠️', '生活杂项'),
    'museum': ('🏛️', '文博展陈'),
    'nuclear': ('☢️', '核物理'),
    'optics': ('🔭', '光学'),
    'pet-training': ('🐾', '宠物训练'),
    'petrochem': ('🛢️', '石油化工'),
    'pets': ('🐱', '宠物养护'),
    'photo': ('📷', '摄影参数'),
    'photo2': ('🎞️', '摄影后期'),
    'process': ('🏭', '过程控制'),
    'quantum': ('⚛️', '量子物理'),
    'restaurant': ('🍽️', '餐饮经营'),
    'robotics': ('🤖', '机器人学'),
    'service': ('🎧', '客户服务'),
    'signal': ('📡', '信号与系统'),
    'statistics': ('📊', '统计学'),
    'structural': ('🏗️', '结构工程'),
    'tax': ('💸', '税务'),
    'text': ('📝', '文本处理'),
    'textile2': ('🧵', '纺织印染'),
    'thermodynamics': ('🌡️', '热力学'),
    'woodworking': ('🪚', '木作工艺'),
}

# ============================================================
# Manual category mappings for existing tools
# ============================================================
CAT_MAP = {}
def _init_cat_map():
    m = {}
    # Image
    for k in ['image-compress','image-to-ascii','pixel-art','image-resizer','image-rotator',
              'image-flipper','image-cropper','image-filters','image-watermark','image-color-picker',
              'image-to-base64','base64-to-image','svg-viewer','svg-minifier','svg-to-png','png-to-svg',
              'favicon-from-text','favicon-from-emoji','qr-code-styled']:
        m[k] = 'image'
    # Design
    for k in ['color-converter','color-picker','gradient','shadow-generator','color-palette',
              'material-color','tailwind-colors','aztec-code','data-matrix','color-scheme-generator',
              'mesh-gradient','pattern-generator','stripe-pattern','dot-pattern','grid-pattern',
              'checkerboard-generator','isometric-grid','blueprint-grid','shadow-generator-advanced',
              'neumorphism-generator','glassmorphism-generator','button-generator','card-generator',
              'toast-generator','skeleton-loader','spinner-generator','progress-bar-generator',
              'badge-generator','avatar-generator','initials-avatar','identicon-generator',
              'loading-dots','waveform-visualizer','spectrum-visualizer','ripple-effect',
              'gradient-from-color','typography-scale','spacing-scale','border-radius-generator',
              'text-shadow-generator','favicon-generator','signature-pad']:
        m[k] = 'design'
    # Generators
    for k in ['qrcode','password','uuid','random','lorem','pomodoro','stopwatch','typing-test',
              'ascii-art','fake-data','nanoid-generator','password-generator-advanced',
              'passphrase-generator','pin-generator','otp-generator','recovery-code-generator',
              'coupon-code-generator','serial-key-generator','invite-code-generator',
              'wifi-qr','vcard-qr','email-qr','sms-qr','location-qr','calendar-qr','url-qr',
              'phone-qr','text-qr','wifi-password-show','qr-decoder','barcode-upc','barcode-ean',
              'barcode-code128','barcode-code39','barcode-itf','barcode-codabar','barcode-msi',
              'barcode-pharmacode','barcode-generator','sn-generator','uuid-v4-generator',
              'uuid-v5-generator','uuid-v7-generator','ulid-generator','cuid-generator',
              'ksuid-generator','hash-id-generator','short-link-generator','tiny-url',
              'slug-generator-advanced','hashtag-generator','username-generator','nickname-generator',
              'gamertag-generator','team-name-generator','domain-name-generator','app-name-generator',
              'business-name-generator','product-name-generator','brand-name-generator',
              'tagline-generator','slogan-generator','motto-generator']:
        m[k] = 'generate'
    # Encode/Cipher
    for k in ['base64','url-encode','hash','morse','html-escape','base32-encode','base58-encode',
              'base85-encode','hex-encode','binary-encode','octal-encode','decimal-encode',
              'uuencode','xxencode','quoted-printable','punycode','url-encoder-advanced',
              'html-entities-encode','js-escape','css-escape','sql-escape','regex-escape',
              'c-string-escape','java-escape','python-escape','php-escape','go-escape',
              'rust-escape','char-encoder','text-to-binary','binary-to-text','text-to-hex',
              'hex-to-text','text-to-octal','text-to-decimal','morse-decode-advanced',
              'baudot-code','bacon-cipher','polybius-cipher','adfgvx-cipher','playfair-cipher',
              'hill-cipher','affine-cipher','rail-fence-cipher','rot-cipher','atbash-cipher',
              'a1z26-cipher','vigenere-visualizer','xor-cipher','aes-encryptor','hmac-generator',
              'crc-calculator','caesar-cipher']:
        m[k] = 'encode'
    # Validators
    for k in ['credit-card-validator','iban-validator','isbn-validator','vin-validator',
              'password-strength','credit-card-bin','credit-card-type','credit-card-luhn',
              'routing-number-validator','swift-bic-validator','bic-validator',
              'sort-code-validator-validator','aba-validator','bic-lookup','ifsc-validator',
              'pan-validator','gst-validator','ein-validator','tin-validator','npi-validator',
              'dea-validator','nric-validator','sin-validator','tfn-validator','ird-validator',
              'cnpj-validator','cpf-validator','curp-validator','rfc-validator','dni-validator',
              'nie-validator','abn-validator','gstin-validator','uan-validator','aadhaar-validator',
              'voter-id-validator','passport-validator','driver-license-validator',
              'license-key-validator','imei-validator','meid-validator','esn-validator',
              'iccid-validator','imsi-validator','msisdn-validator','zip-code-validator',
              'postal-code-validator']:
        m[k] = 'validator'
    # Dev
    for k in ['json-formatter','regex','cron','jwt','slugify','device-info','ip-calculator',
              'sql-formatter','url-parser','json-to-code','user-agent-parser','html-minifier',
              'css-minifier','js-minifier','http-headers','http-response-headers','http-methods',
              'http-cache','http-cookies','rest-api-cheatsheet','json-schema-generator',
              'json-path','json-diff','json-to-tsv','json-to-xml','json-to-yaml','json-to-toml',
              'xml-formatter','xml-to-json','yaml-formatter','toml-formatter','ini-parser',
              'properties-parser','plist-parser','graphql-formatter','protobuf-parser',
              'shell-script-formatter','python-formatter','html-formatter','css-formatter',
              'js-formatter']:
        m[k] = 'dev'
    # Reference
    for k in ['http-status','emoji-cheatsheet','nato-phonetic','mime-type','ascii-table',
              'country-flag','unicode-lookup','mac-lookup','ssl-info','dns-record-info',
              'html-tags','css-properties','js-methods','emoji-meaning','git-commands',
              'sql-cheatsheet','mysql-cheatsheet','postgresql-cheatsheet','sqlite-cheatsheet',
              'mongodb-cheatsheet','redis-cheatsheet','vim-cheatsheet','emacs-cheatsheet',
              'tmux-cheatsheet','docker-cheatsheet','kubernetes-cheatsheet','nginx-cheatsheet',
              'regex-cheatsheet','typescript-cheatsheet','python-cheatsheet','java-cheatsheet',
              'linux-cheatsheet','go-cheatsheet','rust-cheatsheet','cpp-cheatsheet','csharp-cheatsheet',
              'php-cheatsheet','ruby-cheatsheet','msisdn-lookup','phone-lookup','area-code-lookup',
              'country-code-lookup','currency-lookup','language-code-lookup','locale-lookup',
              'timezone-lookup','currency-symbol','html-entities']:
        m[k] = 'reference'
    # Convert
    for k in ['converter','timestamp','color-converter','base-convert','csv-json','date-diff',
              'number-to-chinese','yaml-json','timezone-converter','roman-numeral',
              'data-unit-converter','csv-to-markdown','markdown-to-html','calendar',
              'length-converter','weight-converter','temperature-converter','volume-converter',
              'area-converter','speed-converter','pressure-converter','energy-converter',
              'power-converter','angle-converter','time-converter','frequency-converter',
              'data-rate-converter','fuel-converter','density-converter','flow-rate-converter',
              'torque-converter','magnet-converter','radiation-converter','concentration-converter',
              'shoe-size-converter','ring-size-converter','clothing-size-converter',
              'bra-size-converter','cooking-converter','roman-to-number','chinese-number',
              'number-to-words','number-to-words-chinese','timezone-converter-advanced',
              'world-clock','countdown-timer','event-countdown','workday-calculator',
              'age-in-days','date-add-subtract','leap-year-checker','zodiac-calculator',
              'birthday-paradox']:
        m[k] = 'convert'
    # Math (general)
    for k in ['calculator','bmi-calculator','mortgage-calculator','tax-calculator',
              'percentage-calculator','fraction-calculator','quadratic-equation','prime-number',
              'fibonacci','pi-digits','age-calculator','discount-calculator','tip-calculator',
              'compound-interest','simple-interest','investment-calculator','retirement-calculator',
              'car-loan-calculator','provident-fund','salary-calculator','tax-bracket',
              'depreciation-calculator','roi-calculator']:
        m[k] = 'math'
    # Text
    for k in ['word-counter','markdown','text-diff','text-case','text-reverse','text-dedup',
              'text-extract','text-sort','text-wrap','text-to-speech','speech-to-text',
              'text-stats','char-frequency','word-frequency','text-compare','text-merge',
              'text-split','text-trim','text-pad','text-truncate','text-repeat','text-shuffle',
              'text-reverse-words','text-reverse-lines','text-prefix-suffix','text-line-numbers',
              'text-remove-numbers','text-keep-only','text-replace-advanced',
              'text-remove-duplicates-lines','text-sort-advanced','text-filter-lines',
              'text-extract-emails','text-extract-urls','text-extract-phones','text-extract-ips',
              'text-extract-numbers','text-extract-dates','text-extract-html-tags',
              'text-extract-chinese','text-extract-english','text-case-advanced',
              'fullwidth-halfwidth','simplified-traditional','unicode-normalize','fancy-text',
              'small-caps','superscript-text','zalgo-text','upside-down-text','mirror-text',
              'strawberry-text','text-to-banner','text-box-drawing','word-wrap','justify-text',
              'text-indent','comment-generator','markdown-quote','text-to-slug',
              'lorem-ipsum-advanced']:
        m[k] = 'text'
    # Games
    for k in ['tic-tac-toe','memory-game','number-guess','color-guess','dice-roller','coin-flipper',
              'spinner-wheel','magic-8-ball','rock-paper-scissors','hangman','word-scramble',
              'anagram-game','typing-game','math-quiz','trivia-quiz','country-quiz','capital-quiz',
              'flag-quiz','emoji-memory','reaction-tester','color-memory','pattern-memory',
              'sequence-memory','number-memory','word-memory','cps-test','aim-trainer',
              'click-speed','whack-a-mole','slot-machine','roulette-simulator',
              'blackjack-simulator','poker-hand-evaluator','chess-fen-viewer','sudoku-generator',
              'word-search','bingo-generator','lottery-picker','raffle-picker','random-picker',
              'coin-toss-streak','dice-statistics','fortune-cookie','daily-quote','dad-joke',
              'riddle-generator','tongue-twister','color-quiz','shape-memory','sequence-puzzle']:
        m[k] = 'game'
    return m

CAT_MAP.update(_init_cat_map())

# Industry mapping (filename -> industry) - overrides heuristic
INDUSTRY_MAP = {}

def assign_industry(name, cat):
    """Heuristic industry assignment."""
    n = name
    # Finance-specific categories
    if cat == 'finance': return 'finance'
    # Health-specific categories
    if cat == 'health': return 'health'
    # Engineering
    if cat == 'engineer': return 'science'
    # Education
    if cat == 'edu': return 'edu'
    # Legal
    if cat == 'legal': return 'legal'
    # Music
    if cat == 'music': return 'music'
    # Photo
    if cat == 'photo': return 'photo'
    # Travel
    if cat == 'travel': return 'travel'
    # Marketing
    if cat == 'marketing': return 'marketing'
    # Life
    if cat == 'life': return 'life'
    # IT/Dev
    if cat in ('dev', 'encode'): return 'it'
    # Cheatsheets -> it
    if 'cheatsheet' in n and any(x in n for x in ('sql','git','docker','kubernetes','nginx',
        'linux','vim','emacs','tmux','redis','mongodb','postgres','mysql','sqlite','java',
        'python','go','rust','cpp','csharp','php','ruby','typescript','regex','rest-api')):
        return 'it'
    # Design
    if cat == 'design' or cat == 'image': return 'design'
    # Finance keywords
    fin_kws = ['mortgage','tax','loan','interest','investment','retirement','salary','roi',
               'depreciation','discount','tip','compound','credit-card','iban','bic','currency',
               'percentage','invoice','vat','gst','accounting','budget','expense','stock','bond',
               'option','future','forex','crypto','bitcoin','insurance','pension','annuity',
               'npv','irr','amortization','apr','apy','dividend','yield','401k','roth','ira',
               'mortgage','loan','emi','ppf','fd','rd','sip','mf','nav']
    if any(x in n for x in fin_kws): return 'finance'
    # Health keywords
    health_kws = ['bmi','calorie','body-fat','pregnancy','due-date','ovulation','heart-rate',
                  'blood-pressure','sleep','water','bmr','tdee','macro','protein','carbs','fat',
                  'cholesterol','glucose','diabetes','bmi','whr','waist','hip','ideal-weight',
                  'bmr','tdee','fitness','workout','exercise','run','pace','vo2','hrv',
                  'smoking','alcohol','pregnancy','fertility','due-date','contraction','fetal',
                  'vaccine','dosage','medical','health','bp','ecg','blood-sugar','insulin']
    if any(x in n for x in health_kws): return 'health'
    # Engineering/Science keywords
    eng_kws = ['resistor','ohm','voltage','circuit','physics','chemistry','element','periodic',
               'ohms-law','force','newton','joule','watt','henry','farad','coulomb','ampere',
               'volt','hertz','pascal','weber','tesla','inductance','capacitance','impedance',
               'rf','antenna','gear','bearing','shaft','beam','column','stress','strain',
               'moment','inertia','torque','friction','velocity','acceleration','projectile',
               'kinematic','thermo','entropy','enthalpy','molar','avogadro','ideal-gas',
               'ph','molarity','molality','titration','half-life','decay','isotope']
    if any(x in n for x in eng_kws): return 'science'
    # Education
    edu_kws = ['quiz','flashcard','spelling','grammar','vocab','multiplication','division',
               'fraction','percent','algebra','geometry','chem','bio','physics','history',
               'geography','language','learn','study','exam','test-prep','homework']
    if cat == 'game' and any(x in n for x in ('quiz','math-quiz','typing-game','flag-quiz',
        'capital-quiz','country-quiz','trivia')): return 'edu'
    # Music/Art
    music_kws = ['chord','scale','bpm','metronome','tuner','music','note','rhythm','tempo',
                 'piano','guitar','chord-progression','circle-of-fifths','interval','transpose']
    if any(x in n for x in music_kws): return 'music'
    # Photo
    photo_kws = ['photo','camera','aperture','shutter','iso','exposure','depth-of-field',
                 'focal-length','bokeh','histogram','white-balance','resolution','megapixel',
                 'aspect-ratio','print-size']
    if any(x in n for x in photo_kws): return 'photo'
    # Legal
    legal_kws = ['nda','contract','nda','privacy-policy','terms-of-service','eula','copyright',
                 'trademark','patent','nda','liability','indemnification','governing-law',
                 'arbitration','jurisdiction','force-majeure','severability','waiver']
    if any(x in n for x in legal_kws): return 'legal'
    # Travel
    travel_kws = ['flight','hotel','baggage','visa','passport','customs','timezone','jet-lag',
                  'packing','itinerary','distance','fuel-cost','toll','currency-exchange',
                  'tip-calculator','luggage','airport','train','bus','transit','mileage']
    if any(x in n for x in travel_kws): return 'travel'
    # Marketing
    mkt_kws = ['seo','keyword','adwords','meta-tag','headline','cta','landing-page',
               'conversion-rate','roi','cpc','cpa','ctr','impression','reach','engagement',
               'hashtag','slogan','tagline']
    if any(x in n for x in mkt_kws): return 'marketing'
    # Business/Office
    biz_kws = ['invoice','business','resume','meeting','pdf','ppt','excel','roi',
               'business-name','tagline','slogan','motto','product-name','brand-name',
               'app-name','letterhead','proposal','contract','invoice','receipt']
    if any(x in n for x in biz_kws): return 'biz'
    # Life/daily
    life_kws = ['cooking','shoe-size','ring-size','clothing-size','bra-size','age-calculator',
                'zodiac','birthday','countdown','countdown-timer','event-countdown','workday',
                'date-','calendar','world-clock','timezone','cooking-converter','horoscope',
                'astrology','chinese-zodiac','bazi','fengshui','lucky','wedding','anniversary']
    if any(x in n for x in life_kws): return 'life'
    # Games -> fun
    if cat == 'game': return 'fun'
    # Math stats -> science
    sci_math = ['calculator','fraction','quadratic','prime','fibonacci','pi','gcd','lcm',
                'matrix','vector','trigono','log-','exp-','power-calc','root-calc','nth-root',
                'factorial','permutation','combination','probability','statistics',
                'standard-deviation','variance','mean','median','mode','range','quartile',
                'percentile','z-score','t-score','correlation','regression','binomial',
                'normal-distribution','poisson','exponential','uniform','hypergeometric',
                'chi-square','anova','confidence-interval','sample-size','margin-of-error',
                'p-value','hypothesis-test','effect-size','statistical-power','bayes-theorem']
    if cat == 'math' and any(x in n for x in sci_math): return 'science'
    # Text/writing -> biz
    if cat == 'text' and any(x in n for x in ('markdown','word-counter','text-case','fancy-text',
        'lorem','comment-generator','lorem-ipsum')): return 'biz'
    # Default by cat
    cat_to_ind = {
        'convert': 'life', 'generate': 'it', 'reference': 'it', 'validator': 'finance',
        'math': 'science', 'text': 'biz',
    }
    return cat_to_ind.get(cat, 'it')

def extract_meta(content, key):
    m = re.search(r'<meta\s+name=["\']' + re.escape(key) + r'["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    return m.group(1).strip() if m else None

def parse_toolbox_meta(content):
    meta = extract_meta(content, 'toolbox')
    if not meta:
        return {}
    result = {}
    for part in meta.split(','):
        if '=' in part:
            k, v = part.split('=', 1)
            result[k.strip()] = v.strip()
    return result


_SHARED_SCRIPTS = None
SHARED_SCRIPT_MIN_FILES = 20   # 出现在 >=20 个页面的脚本块视为公共样板，不计入工具自身逻辑

def build_shared_script_index():
    """扫描全部工具页，统计脚本块出现频次，识别公共样板代码。

    站内存在若干注入型公共脚本（主题引导、SW 注册、tool-intro 折叠、
    通用双输入模板引擎等）。若把它们计入代码量，几乎所有工具都会被判为
    高质量，分级就失去意义。这里按内容哈希统计频次自动识别，
    未来新增样板脚本也无需改代码。
    """
    global _SHARED_SCRIPTS
    if _SHARED_SCRIPTS is not None:
        return _SHARED_SCRIPTS
    freq = {}
    for root, dirs, files in os.walk(TOOLS_DIR):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            try:
                with open(os.path.join(root, fn), 'r', encoding='utf-8') as f:
                    c = f.read()
            except Exception:
                continue
            if 'TOOLBOX-REDIRECT' in c:
                continue
            seen = set()
            for b in re.findall(r'<script>(.*?)</script>', c, re.S):
                h = hashlib.md5(b.encode('utf-8')).hexdigest()
                seen.add(h)
            for h in seen:
                freq[h] = freq.get(h, 0) + 1
    _SHARED_SCRIPTS = {h for h, n in freq.items() if n >= SHARED_SCRIPT_MIN_FILES}
    return _SHARED_SCRIPTS


def classify_quality(content):
    """工具质量分级。

    A 专业级：有公式说明面板 / 图表可视化 / 大量自研计算逻辑
    B 标准级：具备完整可用的交互与计算能力（含通用模板计算器）
    C 轻量级：交互极简、以速查展示为主，属于待升级清单
    """
    shared = build_shared_script_index()
    inputs = len(re.findall(r'<(?:input|select|textarea)', content))
    own_len = 0
    for b in re.findall(r'<script>(.*?)</script>', content, re.S):
        if hashlib.md5(b.encode('utf-8')).hexdigest() not in shared:
            own_len += len(b)
    rich = ('formula-box' in content) or ('<canvas' in content) or ('data-viz' in content)
    uses_template_engine = 'function getV0()' in content
    has_calc = 'function calc' in content
    has_intro = bool(re.search(r'<p style="font-size:13px;color:var\(--text-muted\);margin-bottom:\d+px;">', content))

    if rich or own_len >= 6000 or (own_len >= 3000 and inputs >= 3):
        return 'A'
    if own_len >= 800 or inputs >= 3 or (uses_template_engine and inputs >= 2):
        return 'B'
    # 功能性计算器（有计算逻辑且有标准说明）即视为标准级，不应归为轻量级待升级
    if has_calc and has_intro:
        return 'B'
    return 'C'

def get_tool_info(filepath):
    """Get tool info from HTML file. Returns dict or None."""
    # Get relative path from tools/ directory
    rel_path = os.path.relpath(filepath, TOOLS_DIR)
    fname = os.path.basename(filepath)
    name_base = fname.replace('.html', '')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    # Skip redirect stubs (generated by rename script to preserve old URLs)
    if 'TOOLBOX-REDIRECT' in content:
        return None

    tb_meta = parse_toolbox_meta(content)

    # Title
    title_m = re.search(r'<title>(.+?)\s*-\s*ToolBox\s*</title>', content)
    if not title_m:
        title_m = re.search(r'<title>([^<]+)</title>', content)
    title = tb_meta.get('name') or (title_m.group(1).strip() if title_m else name_base)

    # Description from h2 or meta
    desc_m = re.search(r'<h2[^>]*>(.+?)</h2>', content, re.S)
    raw_desc = desc_m.group(1).strip() if desc_m else title
    raw_desc = re.sub(r'<[^>]+>', '', raw_desc)
    raw_desc = re.sub(r'^[\U0001F000-\U0001FAFF\u2600-\u27BF💰💪⚙️🏠📊🧪🎯📋📐🌈🎵📷🔬⚖️❤️📖💼💻✈️📢]+\s*', '', raw_desc).strip()
    desc = tb_meta.get('desc', raw_desc)
    if len(desc) > 60:
        desc = desc[:60] + '...'

    # Category
    cat = tb_meta.get('cat') or CAT_MAP.get(name_base)
    if not cat:
        if 'cipher' in name_base or 'encode' in name_base or 'escape' in name_base:
            cat = 'encode'
        elif '-calculator' in name_base or name_base.endswith('-calculator'):
            cat = 'math'
        elif 'validator' in name_base or 'luhn' in name_base:
            cat = 'validator'
        elif 'cheatsheet' in name_base or 'lookup' in name_base:
            cat = 'reference'
        elif 'qr' in name_base or 'barcode' in name_base or 'generator' in name_base:
            cat = 'generate'
        elif 'converter' in name_base:
            cat = 'convert'
        else:
            cat = 'dev'

    # Industry
    industry = tb_meta.get('industry') or INDUSTRY_MAP.get(name_base) or assign_industry(name_base, cat)

    # Icon and color from category
    cat_def = CAT_DEFS.get(cat, ('🔧', '#f5f5f5', cat))
    icon, bg, _ = cat_def

    # Override icon/color from meta
    if 'icon' in tb_meta: icon = tb_meta['icon']
    if 'bg' in tb_meta: bg = tb_meta['bg']

    # URL: relative from root (tools/industry/file.html)
    url = 'tools/' + rel_path.replace(os.sep, '/')

    return {
        'name': title,
        'cat': cat,
        'industry': industry,
        'icon': icon,
        'bg': bg,
        'url': url,
        'desc': desc,
        'file': fname,
        'path': rel_path,
        'quality': classify_quality(content),
    }

def generate_tools_js(tools):
    lines = ['const tools = [']
    for i, t in enumerate(tools):
        name = t['name'].replace("'", "\\'").replace('\n', ' ').strip()
        desc = t['desc'].replace("'", "\\'").replace('\n', ' ').strip()
        icon = t['icon']
        bg = t['bg']
        line = "  {name:'%s',cat:'%s',industry:'%s',icon:'%s',bg:'%s',url:'%s',desc:'%s'}" % (
            name, t['cat'], t['industry'], icon, bg, t['url'], desc
        )
        if i < len(tools) - 1:
            line += ','
        lines.append(line)
    lines.append('];');
    return '\n'.join(lines)

# ============================================================
# B5-01 Search alias / pinyin / synonym dictionary
# ============================================================
# Chinese tool-term -> English synonyms. Used to enrich the search index so
# that "二维码" also matches "qrcode", "计算器" matches "calculator", etc.
# Pinyin search is covered by the filename slug (B1-05 renamed tools to
# pinyin/English slugs), which we also add as an alias.
ZH_EN_SYNONYMS = {
    '计算器': 'calculator', '计算': 'calculate calc', '换算': 'convert conversion',
    '转换': 'convert converter', '生成': 'generate generator', '生成器': 'generator',
    '校验': 'validate validator check', '验证': 'verify validator', '检查': 'check checker',
    '加密': 'encrypt encryption', '解密': 'decrypt decryption', '编码': 'encode encoder',
    '解码': 'decode decoder', '二维码': 'qrcode qr', '条形码': 'barcode',
    '时间戳': 'timestamp', '哈希': 'hash hashing', '随机': 'random', '密码': 'password',
    '颜色': 'color colour', '单位': 'unit', '日期': 'date', '时间': 'time',
    '图片': 'image', '图像': 'image', '文本': 'text', '字符串': 'string',
    '字数': 'word count', '大小写': 'case', '正则': 'regex regular expression',
    '域名': 'domain', '网址': 'url', '邮件': 'email', '邮箱': 'email',
    '金额': 'money amount', '利率': 'interest rate', '利息': 'interest',
    '贷款': 'loan', '房贷': 'mortgage', '复利': 'compound interest',
    '税率': 'tax rate', '发票': 'invoice', '汇率': 'exchange rate',
    '货币': 'currency', '进制': 'base radix', '字节': 'byte', '文件': 'file',
    '压缩': 'compress compression', '格式化': 'format formatter', '解析': 'parse parser',
    '端口': 'port', '密钥': 'key', '签名': 'signature', '证书': 'certificate',
    '字体': 'font', '音频': 'audio', '视频': 'video', '长度': 'length',
    '重量': 'weight', '面积': 'area', '体积': 'volume', '温度': 'temperature',
    '速度': 'speed', '距离': 'distance', '角度': 'angle', '百分比': 'percentage percent',
    '比例': 'ratio', '分数': 'fraction', '指数': 'exponent', '对数': 'logarithm log',
    '矩阵': 'matrix', '向量': 'vector', '统计': 'statistics stat', '概率': 'probability',
    '平均值': 'average mean', '中位数': 'median', '标准差': 'standard deviation',
    '方差': 'variance', '积分': 'integral', '微分': 'derivative', '方程': 'equation',
    '营养': 'nutrition', '卡路里': 'calorie', '密码强度': 'password strength',
    'Markdown': 'markdown', '取色': 'color picker', '调色': 'color palette',
    'Base64': 'base64', '体脂': 'body fat', '健康': 'health',
}

CAT_EN = {
    'text': 'text', 'encode': 'encode', 'convert': 'convert', 'generate': 'generator',
    'dev': 'developer dev', 'design': 'design', 'image': 'image', 'math': 'math',
    'calculator': 'calculator', 'validator': 'validator', 'reference': 'reference',
    'game': 'game', 'finance': 'finance', 'health': 'health', 'engineer': 'engineering',
    'life': 'life', 'edu': 'education', 'legal': 'legal', 'music': 'music',
    'photo': 'photo', 'travel': 'travel', 'marketing': 'marketing',
}

def build_search_aliases(tool):
    """Build the search alias list for a tool (pinyin slug + English synonyms)."""
    al = set()
    slug = (tool.get('file') or '').replace('.html', '')
    if slug:
        al.add(slug)
        for tok in slug.split('-'):
            if len(tok) >= 2:
                al.add(tok)
    title = tool.get('name') or ''
    for zh, en in ZH_EN_SYNONYMS.items():
        if zh and zh in title:
            for w in en.split():
                if w:
                    al.add(w)
    cat_en = CAT_EN.get(tool.get('cat', ''))
    if cat_en:
        al.add(cat_en)
    ind = tool.get('industry', '')
    if ind:
        al.add(ind)
    al.discard('')
    return sorted(al)


# Self-contained pinyin map (no runtime pypinyin dependency). Generated by
# scripts/_extract_pinyin.py from all tool titles.
PINYIN_MAP = {}
_MAP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', '_pinyin_map.json')
try:
    with open(_MAP_PATH, 'r', encoding='utf-8') as _f:
        PINYIN_MAP = json.load(_f)
except Exception:
    PINYIN_MAP = {}

def title_pinyin(name):
    """Continuous pinyin (no tone) of a Chinese title, e.g. 二维码->erweima."""
    if not name:
        return ''
    return ''.join(PINYIN_MAP.get(ch, '') for ch in name).lower()


def title_pinyin_initials(name):
    """Pinyin initials of a Chinese title, e.g. 计算器->jsq (non-CJK kept as-is)."""
    if not name:
        return ''
    out = []
    for ch in name:
        py = PINYIN_MAP.get(ch, '')
        if py:
            out.append(py[0])
        else:
            out.append(ch.lower())
    return ''.join(out)


def generate_split_jsons(tools):
    """Generate per-industry JSON files and lightweight search index."""
    json_dir = os.path.dirname(TOOLS_JSON_FILE)
    os.makedirs(json_dir, exist_ok=True)

    # Per-industry JSON files
    industries = {}
    for t in tools:
        ind = t.get('industry', 'it')
        if ind not in industries:
            industries[ind] = []
        industries[ind].append(t)
    
    for ind, items in industries.items():
        for t in items:
            t['en'] = translate_name(t.get('name', ''))
            t['ed'] = translate_text(t.get('desc', ''))
            apply_en_override(t)
        path = os.path.join(json_dir, 'industry-%s.json' % ind)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        size_kb = os.path.getsize(path) / 1024
        print('  %-12s %3d tools  %5.1fKB' % (ind, len(items), size_kb))

    # Clear orphan industry files without deleting them. This keeps rebuilds safe
    # on environments that reject bulk file removal while preventing deleted
    # tools from remaining in the lazy-loaded industry indexes.
    active_files = {'industry-%s.json' % ind for ind in industries}
    for filename in glob.glob(os.path.join(json_dir, 'industry-*.json')):
        if os.path.basename(filename) in active_files:
            continue
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print('  cleared orphan %s' % os.path.basename(filename))
    
    # Lightweight search index (name, desc, industry, cat, url only)
    light_index = []
    for t in tools:
        aliases = build_search_aliases(t)
        apply_en_override(t)
        light_index.append({
            'n': t['name'],
            'en': t.get('en') or translate_name(t['name']),
            'd': t.get('desc', ''),
            'ed': t.get('ed') or translate_text(t.get('desc', '')),
            'al': aliases,
            'i': t['industry'],
            'c': t['cat'],
            'u': t['url'],
            'ic': t.get('icon', '🔧'),
            'b': t.get('bg', '#f5f5f5'),
            'q': t.get('quality', 'B'),
            's': (t.get('file') or '').replace('.html', ''),
            'py': title_pinyin(t['name']),
            'pyi': title_pinyin_initials(t['name']),
        })
    idx_path = os.path.join(json_dir, 'search-index.json')
    with open(idx_path, 'w', encoding='utf-8') as f:
        json.dump(light_index, f, ensure_ascii=False)
    print('  search-index  %3d tools  %5.1fKB' % (len(light_index), os.path.getsize(idx_path) / 1024))

# 全站 lastmod 映射（{url: 'YYYY-MM-DD'}），由 main() 在构建时填充为模块全局，
# _lastmod_for() 直接读取，避免逐处传参。数据持久化于仓库根 sitemap_lastmod.json。
_LASTMOD_MAP = {}


def _lastmod_map_path():
    return os.path.join(ROOT, 'sitemap_lastmod.json')


def load_lastmod_map():
    """读取持久化的 lastmod 映射；文件不存在/损坏返回 {}。"""
    p = _lastmod_map_path()
    if os.path.isfile(p):
        try:
            import json
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_lastmod_map(m):
    """原子写回 lastmod 映射（先写 .tmp 再 os.replace）。"""
    import json
    p = _lastmod_map_path()
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=0, sort_keys=True)
    os.replace(tmp, p)


def _assign_dates_sequential(urls, start, end, seed=20260601):
    """一次性把 urls（按传入顺序）铺到 [start, end] 时间轴。
    每天配额前期偏多（权重线性递减后取 1.5 次幂强化），再加 0.5~1.5 倍随机扰动，
    使每天数量随机、整体前期偏多。按 urls 顺序对应日期，故 sitemap 前文偏早期。
    返回 {url: date_str}。"""
    import random
    from datetime import timedelta
    if not urls:
        return {}
    rnd = random.Random(seed)
    total_days = (end - start).days + 1
    M = len(urls)
    weights = [(1 - d / total_days) ** 1.5 for d in range(total_days)]
    total_w = sum(weights) or 1
    daily = [w / total_w * M for w in weights]
    daily = [max(0.0, q * rnd.uniform(0.5, 1.5)) for q in daily]
    s = sum(daily) or 1
    daily = [int(round(q / s * M)) for q in daily]
    # 修正四舍五入差额，优先补到前期以保持前期偏多
    diff = M - sum(daily)
    d = 0
    while diff != 0:
        idx = d % total_days
        if diff > 0:
            daily[idx] += 1
            diff -= 1
        elif daily[idx] > 0:
            daily[idx] -= 1
            diff += 1
        d += 1
        if d > total_days * 3:
            break
    date_pool = []
    for day in range(total_days):
        ds = (start + timedelta(days=day)).strftime('%Y-%m-%d')
        date_pool.extend([ds] * daily[day])
    date_pool = date_pool[:M]
    while len(date_pool) < M:
        date_pool.append((start + timedelta(days=total_days - 1)).strftime('%Y-%m-%d'))
    return {urls[i]: date_pool[i] for i in range(M)}


def ensure_lastmod_map(all_urls, today):
    """构建/补全全站 lastmod 映射（持久化 sitemap_lastmod.json）。
    - 映射文件不存在：按 all_urls 顺序一次性分配历史日期（项目起于 2026-06），写文件。
    - 映射已存在：仅缺失的（新增）URL 用当天日期追加；已有 URL 保持原值不更新。
    即「只干一次」历史分配，后续每次 build 不刷新已有日期，仅新增内容带当前日期。"""
    lm = load_lastmod_map()
    changed = False
    if not lm:
        from datetime import date
        start = date(2026, 6, 1)
        end = date.today()
        lm = _assign_dates_sequential(all_urls, start, end)
        changed = True
    else:
        for u in all_urls:
            if u not in lm:
                lm[u] = today
                changed = True
    if changed:
        save_lastmod_map(lm)
    return lm


def _lastmod_for(url, today):
    """取该 URL 在 lastmod 映射中的日期；缺失则回退当天（兜底，正常不应发生）。"""
    if url in _LASTMOD_MAP:
        return _LASTMOD_MAP[url]
    return today


def generate_sitemap(tools, category_inds=None):
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                 'xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/', today, 'daily', '1.0'))
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/sitemap.html', today, 'weekly', '0.9'))
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/search.html', today, 'weekly', '0.9'))
    # Category index pages
    if category_inds:
        for ind in sorted(category_inds):
            lines.append(_url_block_xhtml('https://chenguangwu.github.io/tools/%s/index.html' % ind, today, 'weekly', '0.9'))
    # guides/ 指南页（自动扫描，避免重跑构建后丢失）
    guides_dir = os.path.join(ROOT, 'guides')
    if os.path.isdir(guides_dir):
        for fn in sorted(os.listdir(guides_dir)):
            if fn.endswith('.html') and fn != 'index.html':
                lines.append(_url_block_xhtml('https://chenguangwu.github.io/guides/%s' % fn, today, 'monthly', '0.8'))
    # chains.html 工具链页（B3-05）
    if os.path.isfile(os.path.join(ROOT, 'chains.html')):
        lines.append(_url_block_xhtml('https://chenguangwu.github.io/chains.html', today, 'weekly', '0.8'))
    for t in tools:
        url = 'https://chenguangwu.github.io/' + t['url']
        lines.append(_url_block_xhtml(url, today, 'monthly', '0.8'))
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def _url_block(url, today, freq, prio):
    return ('  <url>\n'
            '    <loc>%s</loc>\n'
            '    <lastmod>%s</lastmod>\n'
            '    <changefreq>%s</changefreq>\n'
            '    <priority>%s</priority>\n'
            '  </url>' % (url, _lastmod_for(url, today), freq, prio))


def _url_block_xhtml(url, today, freq, prio):
    """含多语言 xhtml:link 变体的 <url> 块。"""
    return ('  <url>\n'
            '    <loc>%s</loc>\n'
            '    <lastmod>%s</lastmod>\n'
            '    <changefreq>%s</changefreq>\n'
            '    <priority>%s</priority>\n'
            '%s\n'
            '  </url>' % (url, _lastmod_for(url, today), freq, prio, _xhtml_alternates(url)))


def generate_core_sitemap(today):
    """Root-level core URLs (home, html sitemap, search, guides) as a standalone sitemap."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/', today, 'daily', '1.0'))
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/sitemap.html', today, 'weekly', '0.9'))
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/search.html', today, 'weekly', '0.9'))
    # guides/ 目录下的指南页（自动扫描，避免重跑构建后丢失）
    guides_dir = os.path.join(ROOT, 'guides')
    if os.path.isdir(guides_dir):
        for fn in sorted(os.listdir(guides_dir)):
            if fn.endswith('.html') and fn != 'index.html':
                lines.append(_url_block_xhtml('https://chenguangwu.github.io/guides/%s' % fn,
                                        today, 'monthly', '0.8'))
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def generate_industry_sitemap(ind, ind_tools, today):
    """Per-industry sitemap.xml placed under tools/<ind>/. Includes the category index page + all tools."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    lines.append(_url_block_xhtml('https://chenguangwu.github.io/tools/%s/index.html' % ind, today, 'weekly', '0.9'))
    for t in sorted(ind_tools, key=lambda x: x['name']):
        url = 'https://chenguangwu.github.io/' + t['url']
        lines.append(_url_block_xhtml(url, today, 'monthly', '0.8'))
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def generate_sitemap_index(sub_urls, today):
    """Root sitemap.xml as a sitemap index referencing core + per-industry sub-sitemaps."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sub_urls:
        lines.append('  <sitemap>')
        lines.append('    <loc>%s</loc>' % u)
        lines.append('    <lastmod>%s</lastmod>' % today)
        lines.append('  </sitemap>')
    lines.append('</sitemapindex>')
    return '\n'.join(lines) + '\n'


def generate_html_sitemap(tools):
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    ind_tools = {}
    for t in tools:
        ind = t['industry']
        if ind not in ind_tools:
            ind_tools[ind] = []
        ind_tools[ind].append(t)
    
    ind_order = [
        'it','ai','data','engineering','electronics',
        'finance','biz','marketing','sales','startup',
        'design','image','video','music','writing',
        'life','health','travel','food','home',
        'edu','language','exam','history','literature',
        'legal','science','math','stats','medical',
        'fun','entertainment','sports',
        'chinese','yi','fengshui','fortune',
        'agriculture','construction','manufacturing','logistics',
        'energy','environment','automotive','beauty',
        'pet','parenting','gardening','mining',
        'textile','chemical','fishery','forestry','livestock',
    ]
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index,follow">
<title>站点地图 - ToolBox 免费在线工具集合</title>
<meta name="description" content="ToolBox 在线工具站点地图，快速浏览所有工具分类和页面。">
<link rel="canonical" href="https://chenguangwu.github.io/sitemap.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #FFFAF7; color: #1E1E2E; line-height: 1.6; padding: 20px; max-width: 1200px; margin: 0 auto; }
h1 { font-size: 2rem; margin-bottom: 10px; color: #FF6B35; }
h1 a { color: inherit; text-decoration: none; }
.subtitle { color: #6B7280; margin-bottom: 30px; }
h2 { font-size: 1.3rem; margin: 25px 0 15px; padding-bottom: 8px; border-bottom: 2px solid #FF6B35; color: #7C3AED; display: flex; align-items: center; gap: 8px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px; }
.tool-link { display: block; padding: 8px 12px; background: white; border-radius: 8px; text-decoration: none; color: #1E1E2E; border: 1px solid #E5E7EB; transition: all 0.2s; font-size: 14px; }
.tool-link:hover { background: #FFF5F0; border-color: #FF6B35; color: #FF6B35; transform: translateX(4px); }
.back { display: inline-block; margin-bottom: 20px; padding: 8px 16px; background: #FF6B35; color: white; text-decoration: none; border-radius: 8px; font-size: 14px; }
.back:hover { background: #E55A25; }
.count { font-size: 12px; color: #6B7280; font-weight: normal; margin-left: 8px; }
.footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #E5E7EB; text-align: center; color: #9CA3AF; font-size: 12px; }
</style>
<script src="/js/common.js"></script>
</head>
<body>
<a href="/" class="back">← 返回首页</a>
<h1><a href="/">🧰 ToolBox</a></h1>
<p class="subtitle">站点地图 · 共 %d 个免费在线工具 · 更新于 %s</p>
''' % (len(tools), today)
    
    for ind in ind_order:
        if ind not in ind_tools:
            continue
        tlist = ind_tools[ind]
        ind_def = INDUSTRY_DEFS.get(ind, ('🔧', ind, ''))
        icon = ind_def[0]
        name = ind_def[1]
        html += f'<h2>{icon} {name}<span class="count">({len(tlist)}个工具)</span></h2>\n'
        html += '<div class="grid">\n'
        for t in sorted(tlist, key=lambda x: x['name']):
            html += f'  <a class="tool-link" href="/{t["url"]}">{t["icon"]} {t["name"]}</a>\n'
        html += '</div>\n'
    
    for ind in sorted(ind_tools.keys()):
        if ind not in ind_order:
            tlist = ind_tools[ind]
            html += f'<h2>🔧 {ind}<span class="count">({len(tlist)}个工具)</span></h2>\n'
            html += '<div class="grid">\n'
            for t in sorted(tlist, key=lambda x: x['name']):
                html += f'  <a class="tool-link" href="/{t["url"]}">{t["icon"]} {t["name"]}</a>\n'
            html += '</div>\n'
    
    html += '''<div class="footer">
<p><a href="/sitemap.xml">XML Sitemap</a> · <a href="/">返回首页</a></p>
<p>© 2026 ToolBox - 免费在线工具集合</p>
</div>
</body>
</html>'''
    return html


def run_clarity_gate():
    """Run post-build check to ensure every public HTML page has /js/analytics.js."""
    checker = os.path.join(ROOT, 'scripts', 'check_clarity_refs.py')
    if not os.path.exists(checker):
        print('  skip: clarity checker not found')
        return
    proc = subprocess.run([sys.executable, checker], cwd=ROOT)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


# ---------------------------------------------------------------------------
# Service Worker 版本戳同步
# ---------------------------------------------------------------------------
# 背景（2026-08-29）：sw.js 旧版缓存名为硬编码常量，发布后不变化，导致用户端
# CSS/JS/JSON 被永久钉死在首次安装的版本，必须无痕模式才能看到更新。
# 现改为「内容驱动版本戳」：sw.js 的 BUILD 常量由本函数按共享静态资源内容 hash
# 写入 —— 内容不变则戳不变（build 幂等），内容一变则缓存命名空间变化，
# 客户端 activate 时自动清理旧缓存，发布即生效。
SW_FILE = os.path.join(ROOT, 'sw.js')
SW_BUILD_RE = re.compile(r"^const BUILD = '[^']*';", re.M)


PHRASES_INDEX_FILE = 'phrases-index.json'


def sync_phrases_index():
    """生成 i18n/tools/phrases-index.json —— 列出真正有 phrases 数据的行业。

    背景：js/tool-i18n.js 运行时按需 fetch i18n/tools/<industry>-phrases.json，
    但全站仅部分行业生成过该数据（缺失行业会打到 404，虽被静默回退却是每页一次无谓请求）。
    前端改为先读本索引、只对清单内行业发请求 → 0 个 404；将来补生成 phrases 后，
    构建会自动把它纳入索引，无需再改前端。
    幂等：内容不变则不写盘（避免每次 build 产生无意义变更）。
    """
    i18n_dir = os.path.join(ROOT, 'i18n', 'tools')
    if not os.path.isdir(i18n_dir):
        return
    # common-phrases.json 是跨行业公共短语（全站加载一次），不是"行业"数据，须排除，
    # 否则索引里会多出一个名为 common 的伪行业。
    inds = sorted({
        fn[:-len('-phrases.json')]
        for fn in os.listdir(i18n_dir)
        if fn.endswith('-phrases.json') and fn != 'common-phrases.json'
    })
    text = json.dumps({'industries': inds, 'count': len(inds)},
                      ensure_ascii=False, indent=1) + '\n'
    out = os.path.join(i18n_dir, PHRASES_INDEX_FILE)
    try:
        with open(out, 'r', encoding='utf-8') as f:
            if f.read() == text:
                return  # 内容一致 → 不写盘，保持构建幂等
    except (IOError, OSError):
        pass
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Generated %s (%d industries with phrase data)' % (PHRASES_INDEX_FILE, len(inds)))


def compute_sw_build():
    """按共享静态资源内容计算 SW 版本戳（纯内容驱动，保证构建幂等）。"""
    h = hashlib.sha1()
    files = []
    for sub, exts in (('css', ('.css',)), ('js', ('.js',))):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(exts):
                    files.append(os.path.join(d, fn))
    jdir = os.path.join(ROOT, 'json')
    for name in ('tools.json', 'search-index.json', 'guides.json', 'channel.json'):
        p = os.path.join(jdir, name)
        if os.path.isfile(p):
            files.append(p)
    for p in files:
        try:
            with open(p, 'rb') as f:
                h.update(os.path.relpath(p, ROOT).encode('utf-8'))
                h.update(f.read())
        except OSError:
            pass
    return h.hexdigest()[:10]


def sync_service_worker_build():
    """把版本戳写回 sw.js；无变化则不落盘（避免无谓 diff）。"""
    if not os.path.isfile(SW_FILE):
        return
    build = compute_sw_build()
    with open(SW_FILE, encoding='utf-8') as f:
        src = f.read()
    new_src, n = SW_BUILD_RE.subn("const BUILD = '%s';" % build, src, count=1)
    if n == 0:
        print('[sw] WARN: 未匹配到 BUILD 常量，跳过版本戳更新')
        return
    if new_src != src:
        with open(SW_FILE, 'w', encoding='utf-8') as f:
            f.write(new_src)
        print('[sw] 版本戳更新 -> %s（客户端旧缓存将在下次激活时清理）' % build)
    else:
        print('[sw] 版本戳未变化 -> %s' % build)


def _count_xml_urls(path):
    with open(path, encoding='utf-8') as f:
        return sum(1 for line in f if '<loc>' in line)


def _build_consistency_check(tools, category_inds):
    import glob

    expected_tools = len(tools)
    with open(TOOLS_JSON_FILE, encoding='utf-8') as f:
        tools_payload = json.load(f)
    actual_tools = len(tools_payload) if isinstance(tools_payload, list) else 0
    if expected_tools != actual_tools:
        print('Build consistency failed: tools.json count mismatch')
        print('  expected=%d actual=%d' % (expected_tools, actual_tools))
        return False

    industry_total = 0
    for fp in sorted(glob.glob(os.path.join(ROOT, 'json', 'industry-*.json'))):
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            print('Build consistency failed: industry file not list -> %s' % os.path.basename(fp))
            return False
        industry_total += len(data)

    if expected_tools != industry_total:
        print('Build consistency failed: industry json total mismatch')
        print('  expected=%d actual=%d' % (expected_tools, industry_total))
        return False

    guides_dir = os.path.join(ROOT, 'guides')
    guides_count = 0
    if os.path.isdir(guides_dir):
        guides_count = len([fn for fn in os.listdir(guides_dir) if fn.endswith('.html') and fn != 'index.html'])
    has_chains = 1 if os.path.isfile(os.path.join(ROOT, 'chains.html')) else 0
    expected_sitemap_urls = expected_tools + 3 + len(category_inds) + guides_count + has_chains
    actual_sitemap_urls = _count_xml_urls(SITEMAP_FILE)
    if expected_sitemap_urls != actual_sitemap_urls:
        print('Build consistency failed: sitemap url count mismatch')
        print('  expected=%d actual=%d' % (expected_sitemap_urls, actual_sitemap_urls))
        print('  formula: tools + core pages + category index + guides + chains')
        return False

    return True


def _update_readme_metrics(qc, tool_count, ind_count):
    if not os.path.exists(README_PATH):
        return

    total = max(tool_count, 1)
    a_rate = qc.get('A', 0) / total * 100
    b_rate = qc.get('B', 0) / total * 100
    c_rate = qc.get('C', 0) / total * 100

    block = (
        '<!-- TOOLBOX_STATS_START -->\n'
        '| 指标 | 实时值 |\n'
        '|---|---:|\n'
        '| 工具总数 | %d |\n'
        '| 行业总数 | %d |\n'
        '| A 级占比 | %.1f%% |\n'
        '| B 级占比 | %.1f%% |\n'
        '| C 级占比 | %.1f%% |\n'
        '<!-- TOOLBOX_STATS_END -->'
    ) % (tool_count, ind_count, a_rate, b_rate, c_rate)

    with open(README_PATH, encoding='utf-8') as f:
        text = f.read()

    pattern = re.compile(r'<!-- TOOLBOX_STATS_START -->.*?<!-- TOOLBOX_STATS_END -->', re.S)
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        text = text.replace(
            '## 📊 工具统计（实时数据以 `json/tools.json` 为准）\n',
            '## 📊 工具统计（实时数据以 `json/tools.json` 为准）\n\n' + block + '\n'
        )

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(text)


def update_index_html(index_path, tools_js, tool_count, cat_counts, ind_counts):
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update title only if not already set correctly
    html = re.sub(r'<title>ToolBox - [^<]+</title>',
        '<title>ToolBox - 6000+免费在线工具集合，纯前端处理数据不上传 | 工具百科</title>', html)

    # Inject industry counts for sidebar (so all counts show on first load)
    ind_counts_js = json.dumps(ind_counts, ensure_ascii=False)
    if 'window.INDUSTRY_COUNTS' in html:
        # Update existing INDUSTRY_COUNTS (non-greedy match across newlines)
        html = re.sub(r'window\.INDUSTRY_COUNTS\s*=\s*\{.*?\};',
            'window.INDUSTRY_COUNTS = %s;' % ind_counts_js, html, flags=re.DOTALL)
    else:
        # Insert before app.js
        html = html.replace(
            '<script src="js/app.js" defer></script>',
            '<script>window.INDUSTRY_COUNTS = %s;</script>\n<script src="js/app.js" defer></script>' % ind_counts_js
        )

    # Update tool count in hero text (match pattern like "1010+")
    # P0-05 统计数字统一：首页各处的营销数字统一为品牌口径 6000+，
    # 不再注入真实工具数（避免与 title/description/og:image 等处的 6000+ 不一致）。
    html = re.sub(r'等\d+\+实用工具', '等6000+实用工具', html)

    # v2-02：首页构建期英文预渲染（高优先入口，首抓更友好）
    for key, text in HOME_PRE_RENDER_I18N_EN.items():
        html = _replace_data_i18n_text(html, key, text)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True

def esc_once(s):
    """幂等转义：先反转义消除历史污染，再统一转义一次。

    背景（已踩坑）：i18n/tools/_en_override.json 中的英文标题由 gen_en_override.py
    从构建产物（search-index）派生，可能已经带有一层转义（如 `&amp;#9989;`）。
    若直接对它再 esc_html_py，会累积成 `&amp;amp;#9989;`，且每跑一次 build 就多
    叠一层，页面 title / og:title 越来越烂。
    因此凡是把「可能已被转义过的文本」写入 HTML 的地方，一律走 esc_once。
    """
    if not s:
        return ''
    return esc_html_py(html.unescape(str(s)))


def esc_html_py(s):
    """Escape HTML entities in Python for building static HTML."""
    if not s:
        return ''
    s = str(s)
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    return s


def _document_head_bounds(content):
    """Return the real document head boundaries, ignoring HTML fragments in JS strings."""
    opening = re.search(r'<head(?:\s[^>]*)?>', content, re.I)
    if not opening:
        return None
    closing = re.search(r'</head\s*>', content[opening.end():], re.I)
    if not closing:
        return None
    close_start = opening.end() + closing.start()
    close_end = opening.end() + closing.end()
    return opening.start(), opening.end(), close_start, close_end


def _head_contains(content, needle):
    bounds = _document_head_bounds(content)
    return bool(bounds and needle in content[bounds[1]:bounds[2]])


def _inject_into_document_head(content, block):
    bounds = _document_head_bounds(content)
    if not bounds:
        return content
    return content[:bounds[2]] + block + content[bounds[2]:]


def _build_deep_dive_html(d):
    """构建「内容深度」区块 HTML：独有使用场景 / 实际示例 / FAQ，打掉模板化页过滤。"""
    if not isinstance(d, dict):
        return ''
    title = esc_html_py((d.get('title') or '').strip())
    parts = []
    parts.append('<!-- TOOLBOX-DEEP-DIVE -->')
    parts.append('<style>')
    parts.append(
        '.deep-dive .dd-list{margin:8px 0 16px;padding-left:20px;}\n'
        '.deep-dive .dd-list li{margin:6px 0;line-height:1.75;}\n'
        '.deep-dive .dd-example{background:var(--card-bg,#fff);border:1px solid var(--border,#eee);border-radius:10px;padding:12px 14px;margin:8px 0 16px;}\n'
        '.deep-dive .dd-ex-title{font-weight:600;color:var(--tool-accent,#FF6B35);margin-bottom:6px;}\n'
        '.deep-dive .dd-ex-body{font-size:13px;line-height:1.85;color:var(--text,#333);word-break:break-word;}\n'
        '.deep-dive .dd-faq{margin:8px 0 4px;}\n'
        '.deep-dive .dd-faq dt{font-weight:600;margin-top:10px;color:var(--text,#333);}\n'
        '.deep-dive .dd-faq dd{margin:4px 0 0;font-size:13px;line-height:1.85;color:var(--text-muted,#666);}\n'
    )
    parts.append('</style>')
    parts.append('<section class="deep-dive" data-deep-dive="1">')
    parts.append('<div class="card">')
    parts.append('<h2>📚 深度解析：%s</h2>' % title)
    _sc = d.get('scenarios') or []
    if _sc:
        parts.append('<h3>💡 常见使用场景</h3>')
        parts.append('<ul class="dd-list">')
        for s in _sc:
            parts.append('<li>%s</li>' % esc_html_py(s))
        parts.append('</ul>')
    for e in (d.get('examples') or []):
        parts.append('<div class="dd-example"><div class="dd-ex-title">%s</div><div class="dd-ex-body">%s</div></div>'
                    % (esc_html_py(e.get('title', '')), esc_html_py(e.get('body', ''))))
    _fq = d.get('faqs') or []
    if _fq:
        parts.append('<h3>❓ 常见问题（FAQ）</h3>')
        parts.append('<dl class="dd-faq">')
        for f in _fq:
            parts.append('<dt>%s</dt><dd>%s</dd>' % (esc_html_py(f.get('q', '')), esc_html_py(f.get('a', ''))))
        parts.append('</dl>')
    parts.append('</div>')
    parts.append('</section>')
    return '\n'.join(parts)


def fix_tool_pages_seo(tools):
    """Post-process all tool pages: ensure h1, add breadcrumbs, related tools, structured data."""
    by_industry = {}
    for t in tools:
        ind = t['industry']
        by_industry.setdefault(ind, []).append(t)

    # 预加载指南映射：工具 basename -> (指南相对路径, 标题)，用于工具页注入"使用指南"链接
    GUIDE_MAP = {}
    _guide_json_path = os.path.join(ROOT, 'json', 'guides.json')
    if os.path.isfile(_guide_json_path):
        try:
            for _g in json.load(open(_guide_json_path, encoding='utf-8')):
                _gt = _g.get('tool')
                if _gt:
                    _title = _g.get('title', '') or ''
                    # 兜底：老指南生成器未带"使用指南"后缀时自动补，确保工具页注入文案统一
                    if _title and '使用指南' not in _title:
                        _title = _title + '使用指南'
                    GUIDE_MAP[_gt] = (_g.get('guide', ''), _title)
        except Exception:
            pass

    # 内容深度（content-depth）试点数据：it/ 等高频工具独有使用场景 / 示例 / FAQ
    DEEP_DIVE = {}
    _dd_path = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
    if os.path.isfile(_dd_path):
        try:
            DEEP_DIVE = json.load(open(_dd_path, encoding='utf-8'))
        except Exception:
            DEEP_DIVE = {}

    fixed_h1 = 0
    fixed_bc = 0
    fixed_rt = 0
    fixed_rt_removed = 0
    i18n_dir = os.path.join(ROOT, 'i18n', 'tools')
    _ind_cache = {}

    def _zh_title_of(ind, base):
        # 取 per-industry 字典 zh-CN.title（真实中文工具名）；懒加载并缓存。
        if ind not in _ind_cache:
            fp = os.path.join(i18n_dir, ind + '.json')
            try:
                _ind_cache[ind] = json.load(open(fp, encoding='utf-8')) if os.path.isfile(fp) else {}
            except Exception:
                _ind_cache[ind] = {}
        return _ind_cache[ind].get(base, {}).get('zh-CN', {}).get('title')

    def extract_zh_desc(content, t, industry, entry):
        # 中文优先 meta description 提取（2026-08-29 反转：目标用户以中文为主）。
        # 优先 per-industry 字典 zh-CN.intro/desc（零成本、有实质内容、不套话），
        # 其次页面首个含中文且非模板的 <p>，再次中文 h2，兜底中文标题 + 固定后缀。
        base = os.path.splitext(os.path.basename(t['path']))[0]
        if industry not in _ind_cache:
            fp = os.path.join(i18n_dir, industry + '.json')
            try:
                _ind_cache[industry] = json.load(open(fp, encoding='utf-8')) if os.path.isfile(fp) else {}
            except Exception:
                _ind_cache[industry] = {}
        _ind = _ind_cache.get(industry, {})
        zh = _ind.get(base, {}).get('zh-CN', {}) if isinstance(_ind, dict) else {}
        intro = zh.get('intro') or zh.get('desc') or ''
        if re.search(r'[\u4e00-\u9fff]', intro or '') and len(intro.strip()) >= 8:
            return intro.strip()
        paras = re.findall(r'<p[^>]*>([\s\S]*?)</p>', content)
        for p in paras:
            txt = re.sub(r'<[^>]+>', '', p).strip()
            txt = re.sub(r'\s+', ' ', txt)
            if '${' in txt or '<' in txt:
                continue
            if re.search(r'[\u4e00-\u9fff]', txt) and len(txt) >= 8:
                return txt
        h2 = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', content)
        if h2:
            txt = re.sub(r'<[^>]+>', '', h2.group(1)).strip()
            txt = re.sub(r'\s+', ' ', txt)
            if re.search(r'[\u4e00-\u9fff]', txt):
                return txt
        zh_title = _zh_title_of(industry, base) or t.get('name') or ''
        return '%s - 免费在线工具，纯前端运行，数据不上传。' % zh_title

    for t in tools:
        filepath = os.path.join(TOOLS_DIR, t['path'])
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        industry = t['industry']
        ind_def = INDUSTRY_DEFS.get(industry, ('🔧', industry))
        ind_icon, ind_name = ind_def[0], ind_def[1]
        tool_name_esc = esc_html_py(t['name'])
        # 工具正文英文预渲染：把 -body.json 英文 title/intro 预渲染进静态 HTML（利于无 JS 首抓/英文 SEO）。
        # 已用 data-i18n 管理的手工页（含 6 个 Top + 其余 8 个）走原机制；其余生成页统一预渲染 +
        # 加 data-zh 保存中文原文，运行时 applyToolBody 对中文用户用 data-zh 还原，英文用户走 -body.json。
        slug = os.path.splitext(os.path.basename(t['path']))[0]
        entry = _load_tool_body(i18n_dir, industry, slug)
        key_prefix = '%s.%s' % (industry, slug)
        if ('data-i18n="%s.title"' % key_prefix) in content:
            # 已有 data-i18n 管理的手工页：走原机制（中文由 data-i18n-fb 还原）
            tool_title = (entry.get('title') or t.get('en') or tool_name_esc)
            tool_intro = (entry.get('intro') or t.get('ed') or '')
            content = _replace_data_i18n_text(content, key_prefix + '.title', tool_title)
            content = _replace_data_i18n_text(content, key_prefix + '.intro', tool_intro)
            content = _replace_h1_text(content, tool_title)
        else:
            # 生成页：预渲染英文 + data-zh 中文原文
            content = _prerender_tool_body(content, entry)

        # 1. Ensure h1 exists (idempotent)
        if '<h1' not in content:
            h1_tag = '\n<h1 class="sr-only">%s</h1>\n' % tool_name_esc
            content = content.replace('<body>', '<body>' + h1_tag, 1)
            fixed_h1 += 1

        # 2. Add breadcrumb nav (idempotent via data-breadcrumb)
        if 'data-breadcrumb' not in content:
            bc_ind_url = 'tools/' + industry + '/index.html'
            bc_tool_dir = 'tools/' + os.path.dirname(t['path'])
            bc_href = os.path.relpath(bc_ind_url, bc_tool_dir).replace(os.sep, '/')
            bc_html = '\n<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">\n  <a href="../../index.html">首页</a>\n  <span class="bc-sep">‹</span>\n  <a href="%s">%s %s</a>\n  <span class="bc-sep">‹</span>\n  <span class="bc-current">%s</span>\n</nav>\n' % (bc_href, ind_icon, ind_name, tool_name_esc)
            if '<div class="container">' in content:
                content = content.replace('<div class="container">', bc_html + '<div class="container">', 1)
            elif '<div class="card">' in content:
                content = content.replace('<div class="card">', bc_html + '<div class="card">', 1)
            else:
                content = content.replace('<body>', '<body>' + bc_html, 1)
            fixed_bc += 1

        # 2.5 Add "使用指南" link (idempotent via data-guide-link)
        if 'data-guide-link' not in content:
            _tb = os.path.basename(t['path'])
            if _tb in GUIDE_MAP:
                _g_url, _g_title = GUIDE_MAP[_tb]
                if _g_url:
                    _g_title_esc = esc_html_py(_g_title)
                    gl_html = '\n<div class="tool-guide-link" data-guide-link="1">\n  <a href="%s">📖 查看「%s」</a>\n</div>\n' % (_g_url, _g_title_esc)
                    if '<div class="container">' in content:
                        content = content.replace('<div class="container">', gl_html + '<div class="container">', 1)
                    elif '<div class="card">' in content:
                        content = content.replace('<div class="card">', gl_html + '<div class="card">', 1)

        # 3. Add BreadcrumbList structured data (idempotent)
        if 'BreadcrumbList' not in content:
            bc_json = '\n<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"},{"@type":"ListItem","position":2,"name":"%s","item":"https://chenguangwu.github.io/tools/%s/index.html"},{"@type":"ListItem","position":3,"name":"%s","item":"https://chenguangwu.github.io/%s"}]}\n</script>' % (ind_name, industry, esc_html_py(t['name']), t['url'])
            content = _inject_into_document_head(content, bc_json + '\n')

        # 3.5 Add shared tool runtime bootstrap (SW + theme + tool-intro interaction)
        clarity_block = '\n<script src="/js/analytics.js" defer></script>\n' + CLARITY_MARKER + '\n'
        runtime_block = '\n<script src="/js/tool-page-runtime.js" defer></script>\n' + TOOL_RUNTIME_MARKER + '\n'
        old_marker_pattern = re.compile(
            r'<!-- toolbox-theme-bootstrap -->\s*'
            r'<!-- toolbox-sw-register -->\s*'
            r'<script>.*?</script><script>.*?</script>\s*',
            re.S
        )

        # Keep Clarity as shared script reference (B10) to avoid inline script drift across tool pages.
        if not _head_contains(content, '/js/analytics.js'):
            content = _inject_into_document_head(content, clarity_block)

        # Ensure tool runtime script is loaded, while preserving compatibility with old inline bootstrap blocks.
        if not _head_contains(content, '/js/tool-page-runtime.js'):
            replaced = False
            if '<!-- toolbox-theme-bootstrap -->' in content and '<!-- toolbox-sw-register -->' in content:
                content, n = old_marker_pattern.subn(runtime_block, content, count=1)
                if n:
                    replaced = True
            if not replaced:
                content = _inject_into_document_head(content, runtime_block)

        # 3.5 Add WebApplication structured data（按 script 块稳态覆盖，避免老版本多语言残留）
        app_cat_map = {
            'dev': 'DeveloperApplication', 'encode': 'DeveloperApplication',
            'text': 'DeveloperApplication', 'convert': 'UtilitiesApplication',
            'validator': 'UtilitiesApplication', 'reference': 'UtilitiesApplication',
            'calculator': 'UtilitiesApplication', 'math': 'UtilitiesApplication',
            'finance': 'FinanceApplication', 'game': 'GamesApplication',
            'image': 'MultimediaApplication', 'design': 'MultimediaApplication',
        }
        app_cat = app_cat_map.get(t['cat'], 'UtilitiesApplication')
        app_desc = esc_html_py((t.get('desc') or t['name'])[:150])
        app_json_block = '\n<!-- TOOLBOX-WEBAPP-LD -->\n<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebApplication","name":"%s","url":"https://chenguangwu.github.io/%s","applicationCategory":"%s","operatingSystem":"Any","browserRequirements":"Requires JavaScript","inLanguage":%s,"description":"%s","image":"https://chenguangwu.github.io/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}\n</script>' % (tool_name_esc, t['url'], app_cat, json.dumps(I18N_LOCALES, ensure_ascii=False), app_desc)

        def _replace_webapp_ld(src):
            # 注意：标记注释位于 <script> 之外，必须一并纳入匹配范围，
            # 否则旧注释会被留在原地、每次构建再插一个新注释（历史累积过 14 个）。
            # 前后换行统一归一，保证多次构建结果完全一致（幂等）。
            pattern = re.compile(
                r'(?:<!--\s*TOOLBOX-WEBAPP-LD\s*-->\s*)*'
                r'<script type="application/ld\+json">.*?</script>', re.S)
            for m in pattern.finditer(src):
                body = m.group(0)
                if '"@type":"WebApplication"' in body:
                    head = src[:m.start()].rstrip('\n')
                    tail = src[m.end():].lstrip('\n')
                    return head + app_json_block + '\n' + tail
            return src

        before_replace = content
        content = _replace_webapp_ld(content)
        if content == before_replace:
            content = content.replace('</head>', app_json_block + '\n</head>', 1)

        # 4. Add og:image / twitter:image (idempotent)
        if 'og:image' not in content:
            image_meta = '\n<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="ToolBox - 6000+免费在线工具">\n<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">\n<meta name="twitter:image:alt" content="ToolBox - 6000+免费在线工具">\n'
            content = content.replace('</head>', image_meta + '</head>', 1)

        # 4.0 中文优先 <title>（2026-08-29 反转：目标用户以中文为主）。
        # 初始 <title> 渲染为中文（per-industry 字典 zh-CN.title 或中文名），英文标题存
        # <meta name="title-en"> 供前端 en-US 模式切回（见 js/i18n.js syncTitle）。
        # og:title / twitter:title 跟随中文。注意：title-en 注入到 I18N_HREFLANG_MARKER 之前，
        # 否则 inject_hreflang 会截断 marker→</head> 间内容导致丢失（已踩坑修复）。
        _seo_slug = _slug_of(t)
        if _seo_slug in EN_OVERRIDE and EN_OVERRIDE[_seo_slug].get('en'):
            _en_t = EN_OVERRIDE[_seo_slug]['en']
            _m_t = re.search(r'<title>([^<]*)</title>', content)
            if _m_t:
                _base = os.path.splitext(os.path.basename(t['path']))[0]
                _zh_title = _zh_title_of(industry, _base) or t.get('name') or tool_name_esc
                _zh_t = _zh_title if _zh_title.endswith('ToolBox') else (_zh_title + ' - ToolBox')
                _en_full = _en_t if _en_t.endswith('ToolBox') else (_en_t + ' - ToolBox')
                # 初始 title 渲染中文（中文优先）
                content = content.replace(_m_t.group(0), '<title>%s</title>' % esc_once(_zh_t), 1)
                # 清理旧 title-zh 残留（不再使用），避免 HTML 冗余
                content = re.sub(r'[ \t]*<meta name="title-zh" content="[^"]*">[ \t]*\n?', '', content)
                # 英文标题存 title-en：先删旧再注入，保证幂等
                content = re.sub(r'[ \t]*<meta name="title-en" content="[^"]*">[ \t]*\n?', '', content)
                _en_meta = '<meta name="title-en" content="%s">' % esc_once(_en_full)
                if I18N_HREFLANG_MARKER in content:
                    content = content.replace(I18N_HREFLANG_MARKER, _en_meta + '\n' + I18N_HREFLANG_MARKER, 1)
                else:
                    content = content.replace('</head>', _en_meta + '\n</head>', 1)
                # og:title / twitter:title 跟随中文
                _og_t = esc_once(_zh_t[:-len(' - ToolBox')] if _zh_t.endswith(' - ToolBox') else _zh_t)
                content = re.sub(r'<meta property="og:title" content="[^"]*">', lambda m: '<meta property="og:title" content="%s">' % _og_t, content, count=1)
                content = re.sub(r'<meta name="twitter:title" content="[^"]*">', lambda m: '<meta name="twitter:title" content="%s">' % _og_t, content, count=1)

        # 4.1 Add meta description / og:title / og:description / twitter:* / canonical (idempotent, 补齐老模板工具页缺失的社交与 SEO 标签)
        # 锚点优先用 I18N_HREFLANG_MARKER，避免被 inject_hreflang 的 marker→</head> 截取逻辑丢弃注入的标签
        m_title = re.search(r'<title>([^<]*)</title>', content)
        page_title = m_title.group(1).strip() if m_title else tool_name_esc
        og_title = page_title[:-len(' - ToolBox')] if page_title.endswith(' - ToolBox') else page_title
        # 4.1a 中文优先 meta description（2026-08-29 反转：目标用户以中文为主）。
        # 初始 description 渲染为中文（优先 per-industry 字典 zh-CN.intro/desc，其次页面中文正文），
        # 英文描述存 <meta name="desc-en"> 供前端 en-US 切换（见 js/i18n.js syncDesc）。
        _en_desc = ''
        if _seo_slug in EN_OVERRIDE and EN_OVERRIDE[_seo_slug].get('ed'):
            _en_desc = EN_OVERRIDE[_seo_slug]['ed']
        _zh_desc_raw = extract_zh_desc(content, t, industry, entry)
        seo_desc = esc_once(_zh_desc_raw[:120])
        anchor = I18N_HREFLANG_MARKER if I18N_HREFLANG_MARKER in content else '</head>'
        seo_tags = ''
        if 'name="description"' not in content:
            seo_tags += '\n<meta name="description" content="%s">' % seo_desc
        else:
            # 已存在 description：强制覆写为中文（中文优先，确保爬虫首抓即中文）
            content = re.sub(r'<meta name="description" content="[^"]*">',
                             lambda m: '<meta name="description" content="%s">' % seo_desc, content, count=1)
        if 'og:title' not in content:
            seo_tags += '\n<meta property="og:title" content="%s">' % esc_html_py(og_title)
        if 'og:description' not in content:
            seo_tags += '\n<meta property="og:description" content="%s">' % seo_desc
        else:
            content = re.sub(r'<meta property="og:description" content="[^"]*">',
                             lambda m: '<meta property="og:description" content="%s">' % seo_desc, content, count=1)
        # 英文描述存 desc-en（供 JS en-US 切换）：注入到 I18N_HREFLANG_MARKER 之前，
        # 否则 inject_hreflang 会截断 marker→</head> 间内容导致丢失（已踩坑修复）。
        if _en_desc:
            content = re.sub(r'[ \t]*<meta name="desc-en" content="[^"]*">[ \t]*\n?', '', content)
            _en_d = '<meta name="desc-en" content="%s">' % esc_once(_en_desc[:160])
            if I18N_HREFLANG_MARKER in content:
                content = content.replace(I18N_HREFLANG_MARKER, _en_d + '\n' + I18N_HREFLANG_MARKER, 1)
            else:
                content = content.replace('</head>', _en_d + '\n</head>', 1)
        if 'twitter:title' not in content:
            seo_tags += '\n<meta name="twitter:title" content="%s">' % esc_html_py(og_title)
        if 'twitter:description' not in content:
            seo_tags += '\n<meta name="twitter:description" content="%s">' % seo_desc
        else:
            content = re.sub(r'<meta name="twitter:description" content="[^"]*">',
                             lambda m: '<meta name="twitter:description" content="%s">' % seo_desc, content, count=1)
        if 'rel="canonical"' not in content:
            seo_tags += '\n<link rel="canonical" href="https://chenguangwu.github.io/%s">' % t['url']
        if 'og:type' not in content:
            seo_tags += '\n<meta property="og:type" content="website">'
        if 'og:url' not in content:
            seo_tags += '\n<meta property="og:url" content="https://chenguangwu.github.io/%s">' % t['url']
        if 'twitter:card' not in content:
            seo_tags += '\n<meta name="twitter:card" content="summary">'
        if seo_tags:
            content = content.replace(anchor, seo_tags + '\n' + anchor, 1)

        # 4.5 Add baseline security response meta (idempotent, B5-08)
        if 'TOOLBOX-SECURITY' not in content:
            sec_meta = '\n<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">\n<meta http-equiv="X-Content-Type-Options" content="nosniff">\n<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">\n<!-- TOOLBOX-SECURITY -->\n'
            content = content.replace('</head>', sec_meta + '</head>', 1)

        # 4.6 Load privacy data-management module (idempotent, B5-08)
        # 绝对路径 + defer：在 common.js（同步）之后执行，扩展 window.ToolBox.Privacy
        if 'TOOLBOX-PRIVACY-SCRIPT' not in content:
            priv_script = '\n<script src="/js/privacy.js" defer></script>\n<!-- TOOLBOX-PRIVACY-SCRIPT -->\n'
            content = content.replace('</head>', priv_script + '</head>', 1)

        # 4.7 Load privacy-first metrics collector (idempotent, B5-10)
        # 默认关闭（opt-in），仅记录匿名聚合事件，绝不向第三方发送数据
        if 'TOOLBOX-METRICS-SCRIPT' not in content:
            metrics_script = '\n<script src="/js/metrics.js" defer></script>\n<!-- TOOLBOX-METRICS-SCRIPT -->\n'
            content = content.replace('</head>', metrics_script + '</head>', 1)

        # 4.8 Load i18n engine + tool-page i18n runtime (idempotent, 多语言批次3)
        # i18n.js 暴露 window.I18n（自动 init：检测语言、应用 data-i18n、挂载切换器到 .nav）
        # tool-i18n.js 翻译公共框架（面包屑/相关工具/使用说明）+ 加载 per-industry 字典
        if 'TOOLBOX-I18N-SCRIPT' not in content:
            i18n_script = '\n<script src="../../js/i18n.js" defer></script>\n<script src="../../js/tool-i18n.js" defer></script>\n<!-- TOOLBOX-I18N-SCRIPT -->\n'
            content = content.replace('</head>', i18n_script + '</head>', 1)

        # 4.9 多语言 SEO：hreflang + og:locale（构建期常量，幂等，批次4）
        abs_url = 'https://chenguangwu.github.io/' + t['url']
        content = inject_hreflang(content, abs_url)

        # 5. Related tools section — 修剪模式（根治删除工具后残留死链，且不引入算法回归）
        #  - 已有块：仅删除指向「文件已不存在」的卡片（即被删工具的死链），保留历史相关工具选取；整块变空则移除整块
        #  - 无块：按行业生成（原逻辑），保持向后一致
        _rt_block_pat = re.compile(
            r'<!-- 相关工具 -->\s*<div class="related-tools"[^>]*>.*?</div>\s*</div>\s*',
            re.S
        )
        _rt_m = _rt_block_pat.search(content)
        if _rt_m:
            _block = _rt_m.group(0)
            _card_pat = re.compile(r'<a[^>]*class="related-tool-card"[^>]*>.*?</a>', re.S)
            _rtc = {'removed': 0}

            def _card_rep(cm):
                _a = cm.group(0)
                _hm = re.search(r'href="([^"]+)"', _a)
                if not _hm:
                    return _a
                _target = os.path.normpath(os.path.join(os.path.dirname(filepath), _hm.group(1)))
                if os.path.exists(_target):
                    return _a
                _rtc['removed'] += 1
                return ''

            _new_block = _card_pat.sub(_card_rep, _block)
            if 'related-tool-card' not in _new_block:
                content = content.replace(_block, '')
                fixed_rt_removed += 1
            else:
                content = content.replace(_block, _new_block)
                fixed_rt_removed += _rtc['removed']
        else:
            related = [rt for rt in by_industry.get(industry, []) if rt['url'] != t['url']][:6]
            if related:
                rt_html = '\n<!-- 相关工具 -->\n<div class="related-tools" data-related-tools="1">\n  <h3 class="related-tools-title">🔗 相关工具</h3>\n  <div class="related-tools-grid">\n'
                rt_tool_dir = 'tools/' + os.path.dirname(t['path'])
                for rt in related:
                    rt_name = esc_html_py(rt['name'])
                    rt_desc = esc_html_py(rt.get('desc', ''))[:50]
                    rt_icon = rt.get('icon', '🔧')
                    rt_href = os.path.relpath(rt['url'], rt_tool_dir).replace(os.sep, '/')
                    rt_html += '    <a href="%s" class="related-tool-card">\n      <span class="rt-icon">%s</span>\n      <span class="rt-info"><span class="rt-name">%s</span><span class="rt-desc">%s</span></span>\n    </a>\n' % (rt_href, rt_icon, rt_name, rt_desc)
                rt_html += '  </div>\n</div>\n'
                if '<div class="tool-intro' in content:
                    content = content.replace('<div class="tool-intro', rt_html + '<div class="tool-intro', 1)
                elif '<!-- /注意事项区块 -->' in content:
                    content = content.replace('<!-- /注意事项区块 -->', '<!-- /注意事项区块 -->\n' + rt_html, 1)
                elif '</div>\n</div>\n<script>' in content:
                    content = content.replace('</div>\n</div>\n<script>', '</div>\n</div>\n' + rt_html + '<script>', 1)
                fixed_rt += 1

        # 6. 内容深度块（content-depth 试点）：注入独有使用场景 / 示例 / FAQ，打掉模板化页过滤。
        #    幂等：先清除已有深度块（兼容旧构建无 marker 残留 / 重复注入），再注入，重跑构建不叠加。
        #    锚点三级回退：手工页「注意事项区块」→ 生成页「相关工具」(step5 注入) → 纯 JS 计算页兜底「</body>」(全页存在)。
        if _seo_slug in DEEP_DIVE:
            content = re.sub(r'<!-- TOOLBOX-DEEP-DIVE -->\s*', '', content)
            content = re.sub(r'<style>\s*\.deep-dive[\s\S]*?</style>\s*', '', content)
            content = re.sub(r'<section class="deep-dive"[^>]*>[\s\S]*?</section>\s*', '', content)
            if '<!-- 注意事项区块 -->' in content:
                _anchor = '<!-- 注意事项区块 -->'
            elif '<!-- 相关工具 -->' in content:
                _anchor = '<!-- 相关工具 -->'
            else:
                _anchor = '</body>'
            _dd_html = _build_deep_dive_html(DEEP_DIVE[_seo_slug])
            if _dd_html and _anchor in content:
                content = content.replace(_anchor, _dd_html + '\n' + _anchor, 1)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    print('  h1 added: %d, breadcrumbs: %d, related tools: %d (recomputed), removed stale blocks: %d' % (fixed_h1, fixed_bc, fixed_rt, fixed_rt_removed))

# 行业聚合页 meta description 覆盖（仅影响列出的行业；工具数为动态带入，避免下次 build 被模板覆盖）
CATEGORY_DESC_OVERRIDE = {
    'home': 'Home and Renovation tools: %d free online tools for room area, material estimates and renovation planning. Browse and use instantly—client-side, no upload.',
    'embedded': 'Embedded Systems tools: %d free online tool for bit, register and protocol calculations. Browse and use it instantly—client-side, no upload, no install.',
    'telecom': 'Telecommunications tools collection with %d free online tools for signal, RF and network calculations. Browse and launch instantly—client-side, no upload.',
}


def _has_cjk(s):
    """返回字符串是否含中日韩（中文）字符，用于判定工具名/描述的语言。"""
    return bool(re.search(r'[一-鿿]', s or ''))


def generate_category_indexes(tools):
    """Generate index.html for each industry directory."""
    _en_path = os.path.join(ROOT, 'i18n', 'industry-en.json')
    _IND_EN = json.load(open(_en_path, encoding='utf-8')) if os.path.exists(_en_path) else {}
    by_industry = {}
    for t in tools:
        by_industry.setdefault(t['industry'], []).append(t)

    # 同义行业（相同 ind_name 对应多个 slug）时，索引页 title 加 slug 区分以避免重复 title
    name_to_inds = {}
    for _ind in by_industry:
        _nm = INDUSTRY_DEFS.get(_ind, ('🔧', _ind))[1]
        name_to_inds.setdefault(_nm, set()).add(_ind)

    for ind, ind_tools in by_industry.items():
        ind_def = INDUSTRY_DEFS.get(ind, ('🔧', ind))
        ind_icon, ind_name = ind_def[0], ind_def[1]
        ind_dir = os.path.join(TOOLS_DIR, ind)
        os.makedirs(ind_dir, exist_ok=True)

        ind_tools_sorted = sorted(ind_tools, key=lambda x: x['name'])
        count = len(ind_tools_sorted)
        en_name = _IND_EN.get(ind, ind_name)
        title = ('%s (%s) Tools Collection - ToolBox' % (en_name, ind)) if len(name_to_inds.get(ind_name, set())) > 1 else ('%s Tools Collection - ToolBox' % en_name)
        title_zh = ('%s（%s）工具集合 - ToolBox' % (ind_name, ind)) if len(name_to_inds.get(ind_name, set())) > 1 else ('%s工具集合 - ToolBox' % ind_name)
        if ind in CATEGORY_DESC_OVERRIDE:
            desc_meta = CATEGORY_DESC_OVERRIDE[ind] % count
        else:
            desc_meta = '%s tools collection with %d free online tools. All run client-side in your browser, no data uploaded.' % (en_name, count)
        desc_meta_zh = '%s工具集合，共%d个免费在线工具，纯前端处理数据不上传。' % (ind_name, count)

        parts = []
        parts.append('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n')
        parts.append('<meta charset="UTF-8">\n')
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n')
        # 中文优先：初始 description/og:description 渲染中文（desc_meta_zh），
        # 英文描述存 desc-en 供前端 en-US 切换（见 js/i18n.js syncDesc）。
        parts.append('<meta name="description" content="%s">\n' % esc_html_py(desc_meta_zh))
        parts.append('<meta name="title-en" content="%s">\n' % esc_html_py(title))
        parts.append('<meta name="desc-en" content="%s">\n' % esc_html_py(desc_meta))
        parts.append('<meta name="robots" content="index,follow">\n')
        parts.append('<meta property="og:title" content="%s">\n' % esc_html_py(title_zh))
        parts.append('<meta property="og:description" content="%s">\n' % esc_html_py(desc_meta_zh))
        parts.append('<meta property="og:type" content="website">\n')
        parts.append('<meta property="og:url" content="https://chenguangwu.github.io/tools/%s/index.html">\n' % ind)
        parts.append('<meta property="og:site_name" content="ToolBox">\n')
        parts.append('<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">\n')
        parts.append('<meta property="og:image:width" content="1200">\n')
        parts.append('<meta property="og:image:height" content="630">\n')
        parts.append('<meta property="og:image:alt" content="ToolBox - 6000+免费在线工具">\n')
        parts.append('<meta name="twitter:card" content="summary_large_image">\n')
        parts.append('<meta name="twitter:title" content="%s">\n' % esc_html_py(title_zh))
        parts.append('<meta name="twitter:description" content="%s">\n' % esc_html_py(desc_meta_zh))
        parts.append('<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">\n')
        parts.append('<meta name="twitter:image:alt" content="ToolBox - 6000+免费在线工具">\n')
        parts.append('<title>%s</title>\n' % esc_html_py(title_zh))
        parts.append('<link rel="canonical" href="https://chenguangwu.github.io/tools/%s/index.html">\n' % ind)
        parts.append('<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n')
        parts.append('<link rel="stylesheet" href="../../css/common.css">\n')
        if '/js/analytics.js' not in ''.join(parts):
            parts.append('<script src="/js/analytics.js" defer></script>\n')
            parts.append(CLARITY_MARKER + '\n')
        parts.append('<script src="../../js/common.js"></script>\n')
        parts.append('<script src="/js/tool-page-runtime.js" defer></script>\n')
        parts.append(TOOL_RUNTIME_MARKER + '\n')
        parts.append('<script src="../../js/i18n.js" defer></script>\n')
        parts.append('<script src="../../js/tool-i18n.js" defer></script>\n')
        # 多语言 SEO：hreflang + og:locale（构建期常量，批次4）
        parts.append(build_hreflang_block('https://chenguangwu.github.io/tools/%s/index.html' % ind))
        # CollectionPage structured data
        parts.append('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"CollectionPage","name":"%s工具","url":"https://chenguangwu.github.io/tools/%s/index.html","description":"%s"}\n</script>\n' % (esc_html_py(ind_name), ind, esc_html_py(desc_meta_zh)))
        # BreadcrumbList structured data
        parts.append('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"},{"@type":"ListItem","position":2,"name":"%s","item":"https://chenguangwu.github.io/tools/%s/index.html"}]}\n</script>\n' % (esc_html_py(ind_name), ind))
        parts.append('</head>\n<body>\n')
        parts.append('<h1 class="sr-only">%s %s工具</h1>\n' % (ind_icon, esc_html_py(ind_name)))
        # Breadcrumb
        parts.append('<nav class="breadcrumb" aria-label="面包屑导航">\n  <a href="../../index.html" data-i18n="bc.home" data-i18n-fb="首页">首页</a>\n  <span class="bc-sep">‹</span>\n  <span class="bc-current">%s <span data-i18n="ind_%s" data-i18n-fb="%s">%s</span></span>\n</nav>\n' % (ind_icon, ind, esc_html_py(ind_name), esc_html_py(ind_name)))
        # Nav
        parts.append('<div class="nav">\n  <a href="../../index.html">← ToolBox</a>\n  <span>/ <span data-i18n="ind_%s" data-i18n-fb="%s">%s</span><span data-i18n="cat.suffix_tools" data-i18n-fb="工具">工具</span></span>\n  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>\n</div>\n' % (ind, esc_html_py(ind_name), esc_html_py(ind_name)))
        # Content
        parts.append('<div class="container">\n  <div class="card">\n')
        parts.append('    <h2>%s %s工具</h2>\n' % (ind_icon, esc_html_py(ind_name)))
        parts.append('    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">共 %d 个免费在线工具，纯前端处理，数据不上传</p>\n' % count)
        parts.append('    <div class="category-tool-list">\n')
        index_ref_dir = 'tools/' + ind
        for t in ind_tools_sorted:
            # 卡片双层命名：ct-name 始终为中文名、ct-desc 始终为英文名，
            # 由 CSS 按 html[lang] 切换显示（P0-08 修复：原直接取 name/desc 导致
            # 英文名为 name 的工具在中文模式只剩英文）。中文名优先取 name，
            # 否则取 desc；英文名取可靠的 en 字段。
            _zh = t['name'] if _has_cjk(t['name']) else (t.get('desc', '') if _has_cjk(t.get('desc', '')) else t['name'])
            _en = t.get('en') or t['name']
            t_name = esc_html_py(_zh)
            t_desc = esc_html_py(_en)
            t_icon = t.get('icon', '🔧')
            tool_href = os.path.relpath(t['url'], index_ref_dir).replace(os.sep, '/')
            parts.append('      <a href="%s" class="category-tool-item">\n        <span class="ct-icon">%s</span>\n        <span class="ct-info"><span class="ct-name">%s</span><span class="ct-desc">%s</span></span>\n      </a>\n' % (tool_href, t_icon, t_name, t_desc))
        parts.append('    </div>\n  </div>\n')
        # SEO intro
        parts.append('  <div class="tool-intro open">\n    <div class="tool-intro-header"><span class="intro-icon-wrap"><span class="intro-icon">📖</span>关于「%s工具」</span><span class="arrow">▼</span></div>\n' % esc_html_py(ind_name))
        parts.append('    <div class="tool-intro-body">\n      <h4><span class="h4-icon">📝</span>分类简介</h4>\n      <p>%s工具集合，涵盖%d个免费在线工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。</p>\n' % (esc_html_py(ind_name), count))
        parts.append('      <h4><span class="h4-icon">✨</span>功能特点</h4>\n      <ul class="intro-features"><li>纯前端处理，数据不上传</li><li>免费使用，无需注册</li><li>支持移动端和桌面端</li><li>实时计算，即用即走</li></ul>\n')
        parts.append('    </div>\n  </div>\n')
        parts.append('</div>\n')
        parts.append('</body>\n</html>\n')

        index_path = os.path.join(ind_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(''.join(parts))

    print('  Generated %d category index pages' % len(by_industry))
    return list(by_industry.keys())


def ensure_tool_clarity_refs(tools):
    """Final pass to make sure every tool page includes shared Clarity loader."""
    changed = 0
    clarity_block = '\n<script src="/js/analytics.js" defer></script>\n' + CLARITY_MARKER + '\n'
    for t in tools:
        filepath = os.path.join(TOOLS_DIR, t['path'])
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        if not _head_contains(content, '/js/analytics.js'):
            content = _inject_into_document_head(content, clarity_block)
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                changed += 1
    print('  Ensured clarity refs on tool pages: %d' % changed)

def main():
    print('=== ToolBox Build ===')
    # Recursively scan all HTML files in tools/ (skip index.html - generated by this script)
    files = []
    for root, dirs, filenames in os.walk(TOOLS_DIR):
        for fn in filenames:
            if fn.endswith('.html') and not fn.startswith('_') and fn != 'index.html':
                files.append(os.path.join(root, fn))
    files.sort()
    print('Found %d HTML files in tools/' % len(files))

    tools = []
    for f in files:
        info = get_tool_info(f)
        if info:
            tools.append(info)

    # Sort: by category order then name
    cat_order = ['dev','encode','text','generate','convert','math','calculator','design','image',
                 'finance','health','engineer','edu','legal','music','photo','travel','marketing',
                 'validator','reference','life','game']
    tools.sort(key=lambda t: (cat_order.index(t['cat']) if t['cat'] in cat_order else 99, t['name']))

    # Stats
    cat_counts = {}
    ind_counts = {}
    for t in tools:
        cat_counts[t['cat']] = cat_counts.get(t['cat'], 0) + 1
        ind_counts[t['industry']] = ind_counts.get(t['industry'], 0) + 1

    print('\nCategory distribution:')
    for cat in cat_order:
        if cat in cat_counts:
            icon = CAT_DEFS[cat][0]
            name = CAT_DEFS[cat][2]
            print('  %s %-12s %3d  %s' % (icon, cat, cat_counts[cat], name))
    print('\nIndustry distribution:')
    ind_order = [
        # Tech & Engineering
        'it','ai','data','engineering','electronics',
        # Finance & Business
        'finance','biz','marketing','sales','startup',
        # Design & Creative
        'design','image','video','music','writing',
        # Life Services
        'life','health','travel','food','home',
        # Education & Culture
        'edu','language','exam','history','literature',
        # Professional Tools
        'legal','science','math','stats','medical',
        # Entertainment
        'fun','entertainment','sports',
        # Chinese Culture
        'chinese','yi','fengshui','fortune',
        # Physical Industries
        'agriculture','construction','manufacturing','logistics',
        'energy','environment','automotive','beauty',
        'pet','parenting','gardening','mining',
        'textile','chemical','fishery','forestry','livestock',
    ]
    for ind in ind_order:
        if ind in ind_counts:
            icon = INDUSTRY_DEFS[ind][0]
            name = INDUSTRY_DEFS[ind][1]
            print('  %s %-12s %3d  %s' % (icon, ind, ind_counts[ind], name))
    for ind, cnt in sorted(ind_counts.items(), key=lambda x: -x[1]):
        if ind not in ind_order:
            print('  ?  %-12s %3d' % (ind, cnt))
    print('\nTotal tools: %d' % len(tools))

    # Generate tools JS (for backward compatibility if needed)
    tools_js = generate_tools_js(tools)

    # 注入英文翻译（en/ed），供英文模式首页/行业页卡片显示
    for t in tools:
        if 'en' not in t:
            t['en'] = translate_name(t.get('name', ''))
        if 'ed' not in t:
            t['ed'] = translate_text(t.get('desc', ''))
        apply_en_override(t)

    # Save tools.json to json/ directory
    os.makedirs(os.path.dirname(TOOLS_JSON_FILE), exist_ok=True)
    with open(TOOLS_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    print('Saved json/tools.json (%d entries)' % len(tools))

    # Also save to root for backward compatibility
    tools_json_root = os.path.join(ROOT, 'tools.json')
    with open(tools_json_root, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    
    # Generate split JSON files (per industry + search index)
    print('\nGenerating split JSON files:')
    generate_split_jsons(tools)

    # 生成 phrases 索引（有数据的行业清单，供 tool-i18n 按需加载，避免对缺失行业发 404 请求）
    sync_phrases_index()

    # SEO: Fix tool pages (h1, breadcrumbs, related tools, structured data)
    print('\nFixing tool pages SEO:')
    fix_tool_pages_seo(tools)
    ensure_tool_clarity_refs(tools)

    # SEO: Generate category index pages
    print('\nGenerating category index pages:')
    category_inds = generate_category_indexes(tools)

    # Update index.html (just update counts and metadata, tools array removed)
    if update_index_html(INDEX_FILE, tools_js, len(tools), cat_counts, ind_counts):
        print('Updated index.html')

    # Inject og:image / twitter:image into index.html if missing (idempotent)
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx_html = f.read()
    if 'og:image' not in idx_html:
        image_meta = '<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="ToolBox - 6000+免费在线工具">\n<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">\n<meta name="twitter:image:alt" content="ToolBox - 6000+免费在线工具">\n'
        idx_html = idx_html.replace('<meta property="og:type" content="website">',
                                    '<meta property="og:type" content="website">\n' + image_meta, 1)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(idx_html)
        print('Injected og:image / twitter:image into index.html')

    # 多语言 SEO：首页注入 hreflang + og:locale（构建期常量，幂等，批次4）
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx_html = f.read()
    if I18N_HREFLANG_MARKER not in idx_html:
        idx_html = inject_hreflang(idx_html, 'https://chenguangwu.github.io/')
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(idx_html)
        print('Injected hreflang into index.html')

    # Generate sitemaps: root full urlset + per-industry sitemap.xml (kept for optional submission)
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    by_industry = {}
    for t in tools:
        by_industry.setdefault(t['industry'], []).append(t)

    # 构建全站 URL 序列（与根 sitemap 顺序一致），一次性分配/补全 lastmod 映射
    all_urls = ['https://chenguangwu.github.io/',
                'https://chenguangwu.github.io/sitemap.html',
                'https://chenguangwu.github.io/search.html']
    if category_inds:
        for ind in sorted(category_inds):
            all_urls.append('https://chenguangwu.github.io/tools/%s/index.html' % ind)
    guides_dir = os.path.join(ROOT, 'guides')
    if os.path.isdir(guides_dir):
        for fn in sorted(os.listdir(guides_dir)):
            if fn.endswith('.html') and fn != 'index.html':
                all_urls.append('https://chenguangwu.github.io/guides/%s' % fn)
    if os.path.isfile(os.path.join(ROOT, 'chains.html')):
        all_urls.append('https://chenguangwu.github.io/chains.html')
    for t in tools:
        all_urls.append('https://chenguangwu.github.io/' + t['url'])
    global _LASTMOD_MAP
    _LASTMOD_MAP = ensure_lastmod_map(all_urls, today)

    for ind in sorted(by_industry.keys()):
        ind_dir = os.path.join(TOOLS_DIR, ind)
        os.makedirs(ind_dir, exist_ok=True)
        content = generate_industry_sitemap(ind, by_industry[ind], today)
        with open(os.path.join(ind_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
            f.write(content)

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(generate_sitemap(tools, category_inds))
    print('Generated sitemap.xml (full urlset: %d tools + %d categories + guides) + %d industry sitemaps'
          % (len(tools), len(category_inds), len(by_industry)))
    
    # Generate HTML sitemap
    html_sitemap = generate_html_sitemap(tools)
    with open(HTML_SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(html_sitemap)
    print('Generated sitemap.html (%d tools)' % len(tools))

    # Final gate: verify all public pages reference the shared Clarity module.
    # This is the build-time guard to avoid future direct inline regressions.
    run_clarity_gate()

    # 同步 Service Worker 版本戳（内容驱动，发布后客户端缓存自动失效）
    sync_service_worker_build()

    # 质量分级统计
    qc = {'A': 0, 'B': 0, 'C': 0}
    for t in tools:
        qc[t.get('quality', 'B')] = qc.get(t.get('quality', 'B'), 0) + 1
    total_q = max(len(tools), 1)
    print('\nQuality grades:')
    for k, label in (('A', '专业级'), ('B', '标准级'), ('C', '轻量级')):
        print('  %s %s  %4d  %5.1f%%' % (k, label, qc[k], qc[k] / total_q * 100))
    _update_readme_metrics(qc, len(tools), len(ind_counts))

    if not _build_consistency_check(tools, category_inds):
        raise SystemExit(1)

    print('\n=== Build complete ===')

if __name__ == '__main__':
    main()
