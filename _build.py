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
from concurrent.futures import ThreadPoolExecutor

# 全站工具描述的唯一权威源：scripts/tool_desc_source.py
# 分类页 .t-zh-desc 与 compute_zh_desc（→ tools.json 的 d，供搜索/首页/导航消费）
# 必须共用同一套解析逻辑，否则又会出现「分类页有描述、搜索与导航没有」的不一致。
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import tool_desc_source as TDS
# 分类聚合页差异化 SEO 正文（修复 GSC「Thin Content」：全站共用套话导致页面互为重复）
import category_auto_content as CAUTO


def _clean_en_desc(s):
    """Strip the identical boilerplate suffix from English meta descriptions.

    Source data (industry-*.json `ed` / EN_OVERRIDE `ed`) may carry the identical
    template "Free online tool on ToolBox — 100% client-side..." which hurts SEO
    uniqueness; keep only each tool's unique English prefix. Also guards against
    re-injecting the template on every build (it otherwise overwrites hand-trimmed
    desc-en edits in tools/*.html).
    """
    if not s:
        return s
    s = str(s)
    for marker in ('Free online tool on ToolBox', 'Free online tool on toolbox'):
        idx = s.find(marker)
        if idx != -1:
            return s[:idx].strip().rstrip('.').strip()
    return s

ROOT = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(ROOT, 'README.md')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))


def _configured_build_workers(item_count=None):
    """Return a conservative worker count for independent per-file work.

    CI and sandbox hosts can expose a very large CPU count while providing much
    less real I/O capacity. Cap the default to avoid making cold builds slower
    through disk contention; TOOLBOX_BUILD_WORKERS=1 remains the deterministic
    troubleshooting escape hatch.
    """
    raw = os.environ.get('TOOLBOX_BUILD_WORKERS', '').strip()
    try:
        requested = int(raw) if raw else min(8, max(1, os.cpu_count() or 1))
    except ValueError:
        requested = min(8, max(1, os.cpu_count() or 1))
    workers = max(1, requested)
    if item_count is not None:
        workers = min(workers, max(1, item_count))
    return workers


def _round_robin_chunks(items, chunk_count):
    chunks = [[] for _ in range(max(1, chunk_count))]
    for index, item in enumerate(items):
        chunks[index % len(chunks)].append(item)
    return [chunk for chunk in chunks if chunk]


# 工具页 / 落地页 critical CSS 内联（弱网首屏防白屏/FOUC）。单一来源 scripts/critical_tool_css.txt。
CRITICAL_TOOL_CSS = ''
_crit_path = os.path.join(ROOT, 'scripts', 'critical_tool_css.txt')
if os.path.isfile(_crit_path):
    try:
        CRITICAL_TOOL_CSS = open(_crit_path, encoding='utf-8').read().strip()
    except Exception:
        CRITICAL_TOOL_CSS = ''
try:
    from zh_en_dict import translate_name, translate_text
except Exception:
    # 兜底：翻译引擎缺失时返回原文，保证构建不中断
    def translate_name(s):
        return s or ''
    def translate_text(s):
        return s or ''

try:
    from gen_hot_tools import HOT_TOOL_URLS
except Exception:
    HOT_TOOL_URLS = ()

HOT_TOOL_URL_SET = set(HOT_TOOL_URLS)

# ============================================================
# 热度排序模型（2026-09-12）
# ------------------------------------------------------------
# 全站「分类内工具」与「分类本身」的排序统一改用热度分 hot（整数，越大越热）。
# 数据现状：51.la 仅站点级概览、URL 级接口被限流(5005)；GSC 无逐页表现导出，
# 故无逐工具真实访问量。口径（老板定）：
#   1) hot-tools.json 的 80 个「编辑精选热门工具」（老板用多 AI 整合的排名）作为热度金字塔
#      顶端，严格保持原顺序不动（HOT_TIER_BASE - 排名）。
#   2) 其余工具：由确定性评分模型 compute_hot() 根据工具名/语义分析初始化热度分，
#      权重参考热门工具的类型分布（转换器/计算器/生成器/编解码/哈希/二维码/密码/时间戳…
#      这类通用工具天然高流量），叠加质量等级与可发现性。模型可复现、可构建幂等、不抖动。
#   3) hot 持久化进 tools.json，所有入口（分类页/导航/站点地图/首页）按 hot 降序；
#      分类本身按聚合 hot 降序。新增工具在 main() 统一计算 hot，自动按热度排。
# 真正流量到位后，只需用真实 PV/CTR 重算 hot 字段即可，排序逻辑无需改动。
# ⚠️ 后续新增工具页：务必在 main() 计算 hot（已统一处理），不要改回按 name 排序。
# ============================================================
HOT_RANK = {url: i for i, url in enumerate(HOT_TOOL_URLS)}  # 0..79，越小越热
HOT_TIER_BASE = 1000000   # 热门工具热度起点，确保整体高于非热门（非热门上限约 <20000）

QUALITY_RANK = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

# 通用高流量工具类型权重（参考热门工具类型分布 + 通用工具站经验）。
# 英文键按「词 token」匹配（slug/en 切分后成员判定，避免 age∈package 类误命中）；
# 中文键按工具名子串匹配（中文关键词区分度高，误命中极低）。
UTILITY_WEIGHTS = {
    # 转换器/换算/计算（最高流量）
    'converter': 3000, 'convert': 3000, '换算': 3000, '转换': 3000,
    'calculator': 3000, 'calc': 3000, '计算': 3000, '计算器': 3000,
    # 生成器
    'generator': 2500, 'generate': 2500, '生成': 2500, '生成器': 2500,
    # 格式化
    'formatter': 2200, 'format': 2200, '格式化': 2200,
    # 编解码/加密
    'encoder': 2200, 'encode': 2200, '编解码': 2200, '编码': 2200, '解码': 2200,
    'encrypt': 1500, '加密': 1500, 'decrypt': 1500, '解密': 1500,
    # 二维码/密码/哈希/时间戳
    'qr': 2000, '二维码': 2000,
    'password': 2000, '密码': 2000,
    'hash': 1800, '哈希': 1800, 'md5': 1800, 'sha': 1800,
    'timestamp': 1800, '时间戳': 1800,
    # 校验/验证
    'validator': 1800, 'validate': 1800, '校验': 1800, '验证': 1800,
    # 压缩/混淆
    'compress': 1500, '压缩': 1500, 'minify': 1500, 'minifier': 1500,
    # 取色/调色/颜色
    'picker': 1500, '取色': 1500, '调色': 1500, 'color': 1000, '颜色': 1000, '色彩': 1000,
    # 对比/差异
    'diff': 1200, '对比': 1200, '比较': 1200, '差异': 1200,
    # 合并/分割
    'merge': 1200, 'split': 1200, '合并': 1200, '分割': 1200, '拆分': 1200,
    # 计数/统计
    'count': 1200, '计数': 1200, '字数': 1200, '统计': 1200,
    # 随机
    'random': 1200, '随机': 1200,
    # 时间/日期/时区
    'clock': 1200, '时间': 1200, '时钟': 1200, 'date': 1200, '日期': 1200,
    'timezone': 1000, '时区': 1000, 'zone': 1000, '世界': 1000,
    # 图片/图像
    'image': 1000, '图片': 1000, '图像': 1000,
    'resizer': 1000, 'resize': 1000, '缩放': 1000, 'crop': 1000, '裁剪': 1000,
    'watermark': 800, '水印': 800, 'favicon': 800, 'gradient': 1000, '渐变': 1000,
    # PDF / 文档
    'pdf': 1000,
    # 数据格式
    'json': 800, 'csv': 800, 'yaml': 800, 'xml': 800, 'sql': 800, 'html': 800,
    'css': 800, 'markdown': 800, '正则': 1000, 'regex': 1000, 'cron': 1000, 'jwt': 1000,
    # 网络/URL
    'url': 1000, '网址': 1000, '域名': 1000,
    # 翻译/简繁
    'translate': 1200, '翻译': 1200, '简繁': 1200, '繁体': 1200,
    # 生活/财务通用
    'interest': 800, '利率': 800, '利息': 800, 'loan': 800, '贷款': 800, '房贷': 800,
    'mortgage': 800, '复利': 800, '税务': 800, '税': 800, 'tax': 800,
    'age': 800, '年龄': 800, 'bmi': 800, '体重': 800, '卡路里': 800, 'calorie': 800,
    '孕期': 800, '预算': 800, 'budget': 800, '小费': 800, 'tip': 800, '折扣': 800,
    'discount': 800, '百分比': 800, 'percentage': 800, 'roi': 800, 'gpa': 800, '成绩': 800,
    'uuid': 800,
}
# 分类加成：核心通用工具分类整体更可能被使用
_HOT_CAT_BOOST = 500
_HOT_CATS = {'convert', 'calculator', 'finance', 'encode', 'generate', 'dev', 'text', 'design', 'life'}


def _tool_hot_text_tokens(tool):
    """返回 (中文名文本, 英文小写 token 集合) 用于热度匹配。"""
    name = (tool.get('name') or '')
    en = (tool.get('en') or '')
    slug = (tool.get('file') or '').replace('.html', '')
    al = tool.get('al') or []
    toks = set()
    for s in (en, slug):
        for tok in str(s).lower().replace('.html', '').replace('_', '-').split('-'):
            if tok:
                toks.add(tok)
    for a in al:
        for tok in str(a).lower().split():
            if tok:
                toks.add(tok)
    return name, toks


def compute_hot(tool):
    """返回工具热度分（整数，越大越热）。确定性、可复现。

    - 编辑精选热门工具：HOT_TIER_BASE - 其排名（严格保持 hot-tools.json 原序）。
    - 其余工具：质量等级 + 通用工具类型权重(参考热门类型分布) + 可发现性 + 分类加成。
    """
    url = tool.get('url')
    if url in HOT_RANK:
        return HOT_TIER_BASE - HOT_RANK[url]   # 0 名最高=1,000,000 … 79 名=921,000
    score = 0
    q = tool.get('quality', 'C')
    score += {'A': 5000, 'B': 2500, 'C': 800, 'D': 200}.get(q, 800)
    name_zh, toks = _tool_hot_text_tokens(tool)
    for tok, w in UTILITY_WEIGHTS.items():
        if tok.isascii():
            if tok in toks:
                score += w
        else:
            if tok in name_zh:
                score += w
    # 可发现性：别名/关键词越多越易被搜到 → 间接反映潜在使用
    al = tool.get('al') or []
    score += min(len(al) * 6, 500)
    d = tool.get('d') or tool.get('desc') or ''
    score += min(len(d) // 8, 300)
    if tool.get('cat') in _HOT_CATS:
        score += _HOT_CAT_BOOST
    return score


def hot_sort_key(tool):
    """统一排序键：热度降序 → 质量升序(同热度时 A 在前) → 名称(稳定)。"""
    return (-tool.get('hot', 0), QUALITY_RANK.get(tool.get('quality', 'C'), 3), tool.get('name', ''))


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
    'hero.sub': '5000+ free tools, all running locally in your browser. No sign-up, your data stays private.',
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
    'hero.badge4': 'Free Forever',
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
    'why.c3_title': 'No Login, Free Forever',
    'why.c3_desc': 'No popups, no forced registration, no usage cap. Use freely, leave immediately. Free forever.',
    'why.c4_title': '5000+ Full Coverage',
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
_TOOL_BODY_FILE_CACHE = {}


def _load_tool_body_file(i18n_dir, industry):
    """Load one industry's body dictionary once for the whole build."""
    file_key = (i18n_dir, industry)
    if file_key in _TOOL_BODY_FILE_CACHE:
        return _TOOL_BODY_FILE_CACHE[file_key]

    path = os.path.join(i18n_dir, '%s-body.json' % industry)
    try:
        with open(path, encoding='utf-8') as f:
            body = json.load(f)
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}
    _TOOL_BODY_FILE_CACHE[file_key] = body
    return body

def _load_tool_body(i18n_dir, industry, slug):
    """按行业 + slug 读取 body 翻译：title/intro 英文稿。"""
    key = (industry, slug)
    if key in _TOP_TOOL_BODY_CACHE:
        return _TOP_TOOL_BODY_CACHE[key]

    body = _load_tool_body_file(i18n_dir, industry)
    entry = body.get(slug, {})
    if not isinstance(entry, dict):
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
    """覆盖字典优先：slug 命中则采用人工/语义预翻的 en（英文名称）。

    注意：ed（英文描述）不再由此函数覆写。EN_OVERRIDE[slug].ed 实为 gen_en_override.py
    批量吐出的「Free online tool…」模板套话，若在此覆盖会抵消 TDS.en_desc 的清洗，
    导致分类页(industry-*.json)的 ed 被重新污染、与导航(industry-groups.json)出现不一致。
    ed 现统一由 TDS.en_desc 产出（已内含 DESC_OVERRIDE 人工精翻与套话剥离），三端同源。
    """
    slug = _slug_of(t)
    if slug and slug in EN_OVERRIDE:
        ov = EN_OVERRIDE[slug]
        if ov.get('en'):
            t['en'] = ov['en']
    return t

TOOLS_DIR = os.path.join(ROOT, 'tools')
INDEX_FILE = os.path.join(ROOT, 'index.html')
SITEMAP_FILE = os.path.join(ROOT, 'sitemap.xml')
HTML_SITEMAP_FILE = os.path.join(ROOT, 'sitemap.html')
TOOLS_JSON_FILE = os.path.join(ROOT, 'json', 'tools.json')
TOOL_RUNTIME_MARKER = '<!-- TOOLBOX-TOOL-RUNTIME -->'
CLARITY_MARKER = '<!-- TOOLBOX-CLARITY -->'

# ============================================================
# common.js 异步化（defer）+ API 兼容桩
# ------------------------------------------------------------
# 背景：国内访问 github.io 较慢，common.js（约 170KB / gzip 42KB）若在 <head>
#       同步加载会阻塞 HTML 解析，弱网下表现为长时间白屏。改为 defer 后
#       HTML/CSS 立即渲染，脚本在 DOM 解析完成后、DOMContentLoaded 之前执行。
# 风险：改 defer 后页面内联脚本会先于 common.js 执行，其顶层 ToolBox.xxx()
#       调用会抛 TypeError。故注入本桩：先把调用收进 window.__tbq 队列，
#       common.js 就绪后回放（见 js/common.js 的 replayToolBoxQueue）。
# 幂等：注入内容带 TOOLBOX_API_STUB_MARKER，重复构建不会重复插入。
#
# 2026-09-05 补充：桩原先只覆盖 13 个「无返回值」方法。页面内联脚本顶层若调用
# escHtml / formatNumber / createTable / debounce（有返回值）或
# setResult / markInvalid（DOM 写入）等方法，会因方法不存在直接抛 TypeError，
# 表现为整页功能不可用（实测：braille-translator、grave-design、arbitration-fee、
# paper/basis-weight、compound-interest 等）。故按返回值特性分两类补齐：
#   A. 有返回值 → <head> 阶段即可运行的等价实现；
#   B. 无返回值的 DOM 写入 → 入 __tbq 队列，等 common.js 就绪后回放（此时元素才存在）。
# common.js 加载完成后其整体赋值 global.ToolBox = {...} 覆盖为完整版，行为一致。
# 版本：升级逻辑见 _upgrade_toolbox_api_stub，指纹为 __stubV。
# ============================================================
# 桩版本号：新增早期 API 时必须 +1，否则历史页面不会被升级。
# 指纹判定见 _upgrade_toolbox_api_stub（解析 __stubV=N 后做数值比较）。
TOOLBOX_STUB_VERSION = 3
TOOLBOX_API_STUB_MARKER = '<!-- TOOLBOX-API-STUB -->'

# ToolBox 早期 API（逐个与 js/common.js 对齐，勿单边修改）
#
# 分两类处理：
#   A. 有返回值（纯函数 / DOM 查询）→ 直接提供等价实现。调用方需要立刻拿到返回值，
#      入队无意义，且这些实现在 <head> 阶段即可安全工作（查不到元素返回 null，不抛错）。
#   B. 无返回值的 DOM 写入类（setResult / markInvalid / clearInvalid / addToolStyles）
#      → 入 window.__tbq 队列。common.js 就绪后由 replayToolBoxQueue 回放，此时 DOM
#      已解析完成，写入才真正生效（若在 <head> 阶段直接执行，元素尚不存在会静默丢失）。
_TOOLBOX_EARLY_API = (
    "(function(){var T=window.ToolBox;"
    # --- 版本号：_upgrade_toolbox_api_stub 解析 __stubV=N 做数值比较，判断是否需升级 ---
    "T.__stubV=" + str(TOOLBOX_STUB_VERSION) + ";"
    # --- A. 有返回值：等价实现 ---
    "if(typeof T.escHtml!=='function')T.escHtml=function(s){"
    "var d=document.createElement('div');d.textContent=s;return d.innerHTML;};"
    "if(typeof T.formatNumber!=='function')T.formatNumber=function(n,dec){"
    "if(typeof n!=='number'||isNaN(n))return String(n);"
    "dec=dec!=null?dec:0;"
    "return n.toLocaleString('zh-CN',{minimumFractionDigits:dec,maximumFractionDigits:dec});};"
    "if(typeof T.createTable!=='function')T.createTable=function(h,r){"
    "var x='<table><thead><tr>';"
    "h.forEach(function(t){x+='<th>'+T.escHtml(t)+'</th>';});"
    "x+='</tr></thead><tbody>';"
    "r.forEach(function(row){x+='<tr>';"
    "row.forEach(function(c){x+='<td>'+(c!=null?T.escHtml(String(c)):'')+'</td>';});"
    "x+='</tr>';});"
    "return x+'</tbody></table>';};"
    "if(typeof T.debounce!=='function')T.debounce=function(fn,ms){"
    "var t;return function(){var a=arguments,s=this;clearTimeout(t);"
    "t=setTimeout(function(){fn.apply(s,a);},ms);};};"
    "if(typeof T.$!=='function')T.$=function(id){return document.getElementById(id);};"
    "if(typeof T.qs!=='function')T.qs=function(s,c){return (c||document).querySelector(s);};"
    "if(typeof T.qsa!=='function')T.qsa=function(s,c){"
    "return Array.prototype.slice.call((c||document).querySelectorAll(s));};"
    "if(typeof T.validateNumberInput!=='function')T.validateNumberInput=function(el){"
    "if(!el||el.type!=='number')return true;"
    "return el.value===''||!isNaN(parseFloat(el.value));};"
    # --- B. 无返回值的 DOM 写入类：入队，等 common.js 回放 ---
    "['setResult','markInvalid','clearInvalid','addToolStyles'].forEach(function(k){"
    "if(typeof T[k]!=='function')T[k]=function(){"
    "window.__tbq.push([k,[].slice.call(arguments)]);};});"
    # --- C. common.js 末尾挂载的全局函数（非 ToolBox 命名空间）---
    # 这些函数在 common.js 文件尾部才挂到 window，同样受 defer 时序影响：
    # 页面若在顶层绘制 canvas（如 compound-interest 的 drawChart）或取文案，会 ReferenceError。
    "if(typeof window.resolveCanvasColor!=='function')window.resolveCanvasColor=function(v,f){"
    "var c=String(v||'').trim(),m=c.match(/^var\\((--[\\w-]+)\\)$/);"
    "if(m)c=getComputedStyle(document.documentElement).getPropertyValue(m[1]).trim();"
    "return c||f;};"
    "if(typeof window.canvasColorWithAlpha!=='function')window.canvasColorWithAlpha=function(v,f,a){"
    "var c=window.resolveCanvasColor(v,f),h=c.match(/^#([0-9a-f]{6})$/i);"
    "if(h){var n=parseInt(h[1],16);"
    "return 'rgba('+(n>>16)+','+((n>>8)&255)+','+(n&255)+','+a+')';}"
    "var s=c.match(/^#([0-9a-f]{3})$/i);"
    "if(s)return window.canvasColorWithAlpha('#'+s[1].split('').map(function(x){return x+x;}).join(''),f,a);"
    "var r=c.match(/^rgb\\(([^)]+)\\)$/i);if(r)return 'rgba('+r[1]+','+a+')';return c;};"
    # i18nText 依赖 common.js 的 I18N_MSG 词典，早期阶段只能降级为返回 fallback（与词典缺失时行为一致）
    "if(typeof window.i18nText!=='function')window.i18nText=function(k,f){return f!=null?f:k;};"
    "})();"
)

TOOLBOX_API_STUB = (
    '<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};'
    "['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard',"
    "'copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool',"
    "'toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')"
    "window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});"
    + _TOOLBOX_EARLY_API +
    '</script>'
    + TOOLBOX_API_STUB_MARKER + '\n'
)

# ============================================================
# 多语言（i18n）常量 —— 与 js/i18n.js LANG_REGISTRY 保持一致
# hreflang 采用构建期常量：每个 locale 对应一个规范 URL（语言由 ?lang 客户端切换，
# 不做 ?lang 查询态 alternate，避免爬取/索引出现 404）。
# ============================================================
I18N_LOCALES = ['zh-CN', 'zh-TW', 'en-US']
I18N_STATIC_LOCALES = ['zh-CN', 'zh-TW']
I18N_STATIC_DIRS = {'zh-TW': 'zh-tw'}
I18N_XDEFAULT = 'zh-CN'
I18N_HREFLANG_MARKER = '<!-- TOOLBOX-HREFLANG -->'
I18N_HREFLANG_BLOCK_RE = re.compile(
    r'<!-- TOOLBOX-HREFLANG -->\s*'
    r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]*">\s*)+'
    r'(?:<meta property="og:locale(?::alternate)?" content="[^"]+">\s*)+',
    re.I,
)


def _loc_under(locale):
    """hreflang/og:locale 用连字符；OpenGraph 用下划线（zh_CN / en_US）"""
    return locale.replace('-', '_')


def localized_i18n_url(abs_url, locale):
    """Return the physical static URL for a locale; English remains runtime query mode."""
    if locale == 'zh-CN':
        return abs_url
    if locale == 'en-US':
        return abs_url + ('&' if '?' in abs_url else '?') + 'lang=en-US'
    prefix = I18N_STATIC_DIRS[locale]
    base = 'https://chenguangwu.github.io'
    suffix = abs_url[len(base):] if abs_url.startswith(base) else abs_url
    if suffix in ('', '/'):
        return base + '/' + prefix + '/'
    return base + '/' + prefix + suffix


def build_hreflang_block(abs_url, default_locale='zh-CN'):
    """生成全套 hreflang alternate 链接（含 x-default）+ og:locale。
    幂等：整体包裹在 I18N_HREFLANG_MARKER 注释内，重复构建不叠加。"""
    lines = [I18N_HREFLANG_MARKER]
    for loc in I18N_LOCALES:
        lines.append('<link rel="alternate" hreflang="%s" href="%s">'
                     % (loc, localized_i18n_url(abs_url, loc)))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">'
                 % localized_i18n_url(abs_url, I18N_XDEFAULT))
    lines.append('<meta property="og:locale" content="%s">'
                 % _loc_under(default_locale))
    for loc in I18N_LOCALES:
        if loc != default_locale:
            lines.append('<meta property="og:locale:alternate" content="%s">'
                         % _loc_under(loc))
    return '\n'.join(lines) + '\n'


def inject_hreflang(content, abs_url, default_locale='zh-CN'):
    """向 <head> 注入 hreflang / og:locale（幂等）。"""
    block = build_hreflang_block(abs_url, default_locale)
    if I18N_HREFLANG_MARKER in content:
        updated, count = I18N_HREFLANG_BLOCK_RE.subn(block, content, count=1)
        if count:
            return updated
        marker_pos = content.find(I18N_HREFLANG_MARKER)
        end_pos = content.find('</head>', marker_pos)
        if end_pos != -1:
            return content[:marker_pos] + block + content[end_pos:]
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
    base = re.sub(r'^https://chenguangwu\.github\.io/zh-(?:tw|hk)(?=/|$)',
                  'https://chenguangwu.github.io', abs_url)
    return '\n'.join(
        '    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
        % (loc, localized_i18n_url(base, loc))
        for loc in I18N_LOCALES
    ) + '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % localized_i18n_url(base, I18N_XDEFAULT)


def _localized_url_blocks(abs_url, today, freq, prio):
    """One compact <url> per crawlable Chinese static locale.

    Locale relationships already live in every page's hreflang head. Repeating
    the same alternate chain for every sitemap URL inflated sitemap.xml by more
    than ten megabytes without adding another crawlable page.
    """
    return [_url_block(localized_i18n_url(abs_url, loc), today, freq, prio)
            for loc in I18N_STATIC_LOCALES]

# ============================================================
# 工具级语义图标规则（2026-09-12）
# ------------------------------------------------------------
# 背景：早期批量生成的工具页把「行业 emoji」写进了每个工具的 meta icon，
# 造成同行业工具图标清一色（如 blasting 20 个工具全是 💣）；另有历史
# 348 个工具 meta 写死 🔧 占位。此处按工具名语义推导专属图标：
#   · 规则按「具体 → 泛化」排序，首个命中优先；
#   · 每工具取最多 5 个候选，再由 assign_tool_icons() 做行业内均衡去重，
#     从根上避免同一分类下图标千篇一律；
#   · 匹配对象 = 中文工具名 + 英文 slug（连字符转空格）。
# ★ 权威源：分类图标权威源是 INDUSTRY_DEFS[0]；工具图标权威源是本规则表，
#   例外是各工具页 meta 中已人工指定的「专属图标」（非占位时予以保留）。
# ============================================================
TOOL_ICON_RULES = [
    # ---------- 1) 唯一标识型对象（名词自证，优先级最高）----------
    (r'二维码|qrcode|qr code|^qr-|-qr-', '🔳'),
    (r'条形码|条码|barcode|codabar|code128|code39|ean-?1[238]|upc-a|tf-14|msi|pharmacode', '🏷️'),
    (r'wifi|wi-fi', '📶'),
    (r'摩斯|morse', '📻'),
    (r'凯撒|维吉尼亚|playfair|hill 密码|affine|atbash|bacon|polybius|adfgvx|a1z26|栅栏|埃特巴什|普莱费尔|仿射|培根|波利比奥斯|密文|cipher', '🕵️'),
    (r'哈希|摘要|hash|sha-?\d|md5|crc|hmac|校验和|checksum', '#️⃣'),
    (r'密码|口令|password|passphrase|pin 码|pin码|私钥|密钥|token|强密码', '🔑'),
    (r'加密|解密|aes|rsa|\bxor\b|des 加密', '🔐'),
    (r'编码|解码|encode|decode|base32|base58|base64|base85|uuencode|xxencode|punycode|quoted-printable|转义|escape|实体编解码', '🔤'),
    (r'颜色|色值|配色|调色板|色号|\brgb\b|\bhsl\b|cmyk|色差|色彩|对比度|明暗', '🎨'),
    (r'图片|图像|照片|\bpng\b|\bjpe?g\b|\bsvg\b|\bwebp\b|\bgif\b|像素画|取色|水印|裁剪|缩放|旋转|翻转|画布', '🖼️'),
    (r'字体|\bfont\b|字形|字号|字重|文字阴影', '🔤'),
    (r'头像|avatar|identicon|首字母|favicon|图标生成|徽章', '👤'),
    (r'身份证|护照|驾照|证件|税号|社保|\bsin\b|\bcpf\b|cnpj|curp|aadhaar|nric|\bird\b|\babn\b|\btfn\b|\bdni\b|\bnie\b', '🪪'),
    (r'银行卡|信用卡|借记卡|iban|\bbic\b|swift|路由号码|luhn|bin 查询|bin查询|\besn\b|iccid|imei|imsi|meid', '💳'),
    (r'邮箱|email|邮件|smtp|imap', '📧'),
    (r'手机号|电话号码|phone|msisdn|区号|短信|\bsms\b', '☎️'),
    (r'邮编|postcode|\bzip\b|收货地址', '📮'),
    (r'域名|domain|\bdns\b|\burl\b|短链接|tinyurl|slug', '🔗'),
    (r'ip 地址|ip地址|子网|掩码|cidr|网关|mac 地址|带宽|网络|wireless', '🌐'),
    (r'经纬度|坐标|度分秒|\bgis\b|geohash|缓冲区|坡度|地形', '🗺️'),
    (r'\bjson\b|\byaml\b|\btoml\b|\bxml\b|\bini\b|plist|protobuf|properties|schema', '📄'),
    (r'markdown|实时预览', '📝'),
    (r'\bcsv\b|\btsv\b|excel|电子表格', '📊'),
    (r'\bsql\b|mysql|postgres|sqlite|mongodb|redis|数据库', '🗄️'),
    (r'\bgit\b|版本控制|\bsvn\b', '🔀'),
    (r'docker|kubernetes|k8s|容器|nginx|linux|shell|bash|命令速查|tmux|\bvim\b|emacs|crontab|chmod|环境变量|\.env', '🖥️'),
    (r'正则|regex', '🔍'),
    (r'日志|log 分析', '📜'),
    (r'备份|backup', '💾'),
    (r'图表|可视化|直方图|散点|折线|饼图|仪表盘|dashboard|甘特|频数', '📈'),
    (r'代码|编程|\bsdk\b|函数|注释|语法树|\bast\b|编译|美化代码', '💻'),
    (r'时间戳|timestamp|utc|时区|iana', '⏲️'),
    (r'日期|日历|万年历|倒计时|工作日|\bdate\b', '📅'),
    (r'星期|节气|闰年|干支', '🗓️'),
    (r'随机|抽样|洗牌|打乱|抽签', '🎲'),
    (r'骰子|掷骰', '🎲'),
    (r'轮盘|转盘|抽奖|抽选|随机选择', '🎡'),
    (r'抛硬币|硬币|纪念币', '🪙'),
    (r'扑克|卡牌|21 点|扑克牌', '🃏'),
    (r'象棋|国际象棋|棋谱|围棋|将棋', '♟️'),
    (r'数独|迷宫|谜题|拼图|填字', '🧩'),
    # ---------- 2) 物理量 / 度量（按量纲给专属图标）----------
    (r'距离|长度|间距|行程|里程|厚度|深度|高度|直径|半径|周长|弦长|弧长', '📏'),
    (r'面积|截面|方量|用量|铺贴|体量', '📐'),
    (r'体积|容积|库容|容量|水箱|罐容', '🧊'),
    (r'重量|质量|克重|材积|载荷|荷载|承重|体重', '⚖️'),
    (r'温度|焓|熵|卡诺|传热|导热|比热|显热|潜热|绝热|玻意耳|查理|盖-吕萨克|饱和水汽压|露点|湿球|体感温度|风寒|湿热', '🌡️'),
    (r'压力|压强|压降|超压|气压|真空|水压|静水', '🎚️'),
    (r'速度|航速|加速度|速率|下落|沉降|终端速度|风级|风速', '🏎️'),
    (r'功率|效率|能耗|耗电|功耗|COP|发电量|转矩', '⚡'),
    (r'能量|热量|动能|焦耳|卡路里|比能量|电压|电流|电阻|电容|电感|阻抗|容抗|感抗|欧姆|三相|变压器|导线|电缆|电路|限流|分压|分流|运放|谐振|充电|电池|蓄电|熔断|断路|接地|漏电|绝缘', '⚡'),
    (r'流量|流速|水头|孔口|明渠|溢洪|堰流|水锤|渗流|水力|扬程|达西|雷诺数|伯努利|曼宁|流体|浮力|阿基米德|毛细|泊肃叶|斯托克斯', '💧'),
    (r'频率|波长|谐振|采样|滤波器|信号|增益|阻尼|阶跃|时间常数|截止', '📡'),
    (r'角度|弧度|三角|斜率|倾角|方位|斜坡', '📐'),
    (r'转速|扭矩|主轴|进给|切削|铣削|车削|刨削|镗削|磨削|钻削|锯切', '🔩'),
    (r'振动|噪声|噪音|分贝|声压|声强|混响|基频|拍频|多普勒|声学', '🔊'),
    (r'辐射|放射性|衰变|半衰期|活度|裂变|结合能|质量亏损|同位素|剂量率|碳十四', '☢️'),
    (r'量子|光子|光电效应|德布罗意|势阱|氢原子|海森堡|玻尔|康普顿|维恩|质能|里德伯|回旋频率', '⚛️'),
    (r'\bph\b|poh|酸碱|酸解离|缓冲液|摩尔|滴定|化学计量|电解质|溶解度|电镀|电解|腐蚀|氧化还原|化学反应', '🧪'),
    (r'数据存储|存储容量|字节|比特|数据速率|带宽换算', '💾'),
    (r'汇率|货币|外币|点值|点差|结汇|购汇', '💱'),
    (r'利率|利息|复利|贴现|折现|收益率|年化|内部收益率|irr|npv|久期|现值|终值', '🏦'),
    (r'贷款|按揭|月供|还款|房贷|分期|首付', '🏠'),
    (r'税|税率|个税|增值税|契税|关税|退税', '🧾'),
    (r'工资|薪酬|薪资|月薪|提成|奖金|加班费|社保公积金|经济补偿金', '💵'),
    (r'保险|保费|保额|理赔|赔付|免赔|寿险|车险', '🛡️'),
    (r'股票|证券|盈亏|波动率|布林|均线|技术指标|估值|股利|戈登|市盈率|资产负债表|现金流', '📈'),
    (r'基金|净值|持仓|组合收益|投资回报', '📊'),
    (r'成本|利润|毛利|预算|费用|报价|定价|加价率|烧钱率|盈亏平衡', '💰'),
    (r'折旧|贬值|减值|摊销', '📉'),
    (r'发票|账单|账务|凭证|账簿|报销|对账|\bAA\b 制|分摊', '🧾'),
    (r'转化率|漏斗|投递|排名|归一化', '🎯'),
    (r'广告|投放|\broi\b|\bcpm\b|\bcpc\b|曝光|落地页', '📣'),
    # ---------- 3) 医学与生命科学（器官/专科）----------
    (r'牙|口腔|义齿|颌|龋|正畸|牙槽|智齿|牙周|根管|咬合|牙弓', '🦷'),
    (r'肺|呼吸|哮喘|气胸|结核|氧合|气管|胸水|通气|戒烟|尼古丁|痰液', '🫁'),
    (r'卒中|帕金森|癫痫|偏头痛|头痛|眩晕|共济|面瘫|三叉|阿尔茨海默|不宁腿|神经|脑|moca|nihss|updrs|edss|adas|sara|twstrs|\bqmg\b|\bdhi\b|midas|ilae|brackmann', '🧠'),
    (r'心电图|心率|心脏|心梗|心血管|血压|胆固醇|冠|timi|grace|has-bled|\bmets\b', '❤️'),
    (r'视力|眼睛|瞳孔|角膜|泪膜|睑板|色觉|屈光|斜视|青光眼|眼底|视野|\biol\b|\boct\b|a 超|视功能', '👁️'),
    (r'听力|听觉|前庭|耳鸣|鼓膜|咽鼓管|声导抗|纯音', '👂'),
    (r'皮肤|皮炎|疤痕|色斑|毛孔|皱纹|皮脂|防晒|果酸|水光|微针|线雕|瘢痕|痤疮|激光美容', '🧴'),
    (r'精子|精液|睾丸|胚胎|受精|生殖|附睾|输精管|子宫|内膜|ivf|icsi|pgt|gardner', '🧬'),
    (r'风湿|狼疮|干燥综合征|血管炎|强直|痛风|尿酸|抗 ccp|anca|补体|白塞|皮肌炎|sapho|mctd', '🛡️'),
    (r'贫血|凝血|血小板|血友|淋巴瘤|骨髓|输血|血红蛋白|\bdic\b|血细胞|\bitp\b|红细胞|白细胞', '🩸'),
    (r'前列腺|排尿|残余尿|膀胱|逼尿肌|泌尿', '🚻'),
    (r'肾|肌酐|肾小球|kdigo|滤过率', '🫘'),
    (r'激素|内分泌|甲状腺|血糖|胰岛素|糖尿病|儿茶酚胺|性腺', '⚗️'),
    (r'抑郁|焦虑|强迫|恐慌|孤独症|自闭|人格|心理|精神|情绪|失眠|自杀|成瘾|物质依赖|注意力缺陷|冲动|社交恐惧|躯体化|生活事件|韧性', '💭'),
    (r'儿科|儿童|婴儿|婴幼儿|新生儿|喂养|生长发育|生长曲线|早产', '👶'),
    (r'老年|养老|高龄|失能|临终|退行', '🧓'),
    (r'康复|步态|平衡功能|辅助器具|失语|flacc|berg|疼痛行为|关节活动|肌力', '🦿'),
    (r'营养|膳食|维生素|蛋白质|膳食纤维|地中海饮食|\bdash\b|血糖生成指数|gi（', '🥗'),
    (r'药物|用药|剂量|处方|ld50|配伍|不良反应|\badr\b|抗生素|抗菌|给药', '💊'),
    (r'手术|术后|麻醉|缝合|无菌|消毒', '🩺'),
    (r'护理|照护|陪护|社工|查房|医嘱', '🧑⚕️'),
    (r'中医|中药|方剂|方歌|君臣佐使|性味归经|舌诊|中成药|辨证', '🌿'),
    (r'穴位|针刺|留针|拔罐|艾灸|针灸|骨度分寸|推拿', '📍'),
    (r'标本|检验|化验|实验室|质控|室间质评|参考区间', '🔬'),
    # ---------- 4) 行业对象 ----------
    (r'汽车|轮胎|刹车|制动|发动机|变速|汽油|柴油|车灯|车身|保养周期|驾驶|车载', '🚗'),
    (r'铁路|列车|轨道|道岔|信号联锁', '🚆'),
    (r'船舶|航运|港口|锚|航程|水尺', '🚢'),
    (r'飞机|航空|机翼|螺旋桨|升力|飞行', '✈️'),
    (r'航天|火箭|卫星|轨道速度|逃逸速度|齐奥尔科夫斯基|引力', '🚀'),
    (r'消防|火灾|灭火|着火|闪点|燃点|耐火|防火|烟气|疏散|避难', '🔥'),
    (r'救援|急救|应急|逃生|破拆|绳索|水上救援|搜救|缓降', '🚑'),
    (r'物流|运输|运价|快递|运费|配送|货运|逆向物流|托运', '🚚'),
    (r'仓储|库存|库位|盘点|货架', '🏬'),
    (r'农业|作物|种植|灌溉|土壤|肥料|化肥|农药|大棚|温室|收割|播种|农田|亩产', '🌾'),
    (r'林业|森林|采伐|造林|林分|郁闭度|蓄积量|苗木', '🌳'),
    (r'渔业|水产|鱼|养殖|盐度|投喂|虾', '🐟'),
    (r'畜牧|奶牛|饲料|育肥|产奶|生猪|肉牛|禽类', '🐄'),
    (r'宠物|犬|猫|兽医|驱虫|疫苗|宠物医院', '🐾'),
    (r'食品|烹饪|油炸|配料|保质期|food|食谱|菜谱', '🍳'),
    (r'餐饮|菜单|菜品|门店|翻台|出餐', '🍽️'),
    (r'纺织|面料|纱线|色牢度|染色|印染|服装|尺码|衣|衬布|绣花', '🧵'),
    (r'皮革|毛皮|鞣制', '🧳'),
    (r'珠宝|黄金|钻石|克拉|宝石|贵金属', '💎'),
    (r'木材|木工|榫|板材|原木|锯材', '🪵'),
    (r'陶瓷|陶艺|釉|烧制', '🏺'),
    (r'家具|沙发|桌椅|床垫|柜体', '🛋️'),
    (r'包装|纸箱|瓦楞|封箱|纸盒|缓冲材|木箱', '📦'),
    (r'印刷|色彩管理|专色|版式|折页|装订', '🖨️'),
    (r'园艺|花园|花卉|蔬菜种植|堆肥|浇水', '🌷'),
    (r'婚礼|婚纱|喜宴|婚庆', '💍'),
    (r'音乐|和弦|音阶|\bbpm\b|节拍|节奏|音准|乐理|歌曲|调式', '🎵'),
    (r'游戏|闯关|记忆游戏|猜数字|猜单词|猜颜色|打地鼠|老虎机|反应测试|点击速度|发音', '🎮'),
    (r'打字|键盘|输入法|键位', '⌨️'),
    (r'教育|学习|课程|测验|题库|单词|词汇|背诵|错题|考试|\bgpa\b|阅读速度', '📖'),
    (r'语言|翻译|语法|多语言|母语|词汇量', '🌐'),
    (r'历史|朝代|时间轴|纪年|文物|古籍', '📜'),
    (r'法律|法规|合规|合同|违约|诉讼|仲裁|继承|遗嘱|赔偿|诉讼费|文书|法务|判例', '⚖️'),
    (r'专利|知识产权|商标|著作权', '©️'),
    (r'招聘|人力|考勤|绩效|离职|员工|薪酬带宽|内推|培训体系|组织', '👥'),
    (r'客户|客服|话术|满意度|投诉|工单|响应时间|售后', '🎧'),
    (r'地产|房地产|租金|房价|物业|楼盘|按揭评估|房屋|小区', '🏠'),
    (r'装修|房间|油漆|墙面|地板|瓷砖|吊顶|预算报价', '🛠️'),
    (r'军事|国防|弹道|弹药|枪|炮|射击|瞄准|膛线|夜视|伪装|战术', '🎯'),
    (r'气象|天气|湿度|降雨|风力|干旱|云底|雾|潮汐|气压高度', '⛅'),
    (r'地震|震级|烈度|震源|余震|地震波', '🌋'),
    (r'环境|环保|碳排放|碳足迹|垃圾|回收|污水|废气|噪声治理', '♻️'),
    (r'展会|会展|展台|观众|巡展|布展', '🎪'),
    (r'舞蹈|舞伴|拉丁舞|芭蕾|街舞', '💃'),
    (r'瑜伽|冥想|体式|正念', '🧘'),
    (r'游泳|泳姿|划水|潜水', '🏊'),
    (r'足球|篮球|网球|羽毛球|乒乓|排球|棒球|高尔夫', '⚽'),
    (r'跑步|马拉松|配速|步频|步幅|长跑|越野', '🏃'),
    (r'武术|格斗|拳击|摔跤|跆拳道|柔道|击剑|散打', '🥋'),
    (r'攀岩|登山|徒步|露营|帐篷|绳降', '🧗'),
    (r'健身|力量|增肌|减脂|体脂|基础代谢|rm|肌肉', '🏋️'),
    (r'睡眠|恢复|疲劳|作息', '😴'),
    # ---------- 5) 功能操作（泛化规则，最后兜底）----------
    (r'生成器|生成|创建|批量造|造词|取名|名字|命名|口号|标语|文案|昵称|用户名|团队名|品牌名', '✨'),
    (r'校验|验证|检测有效性|合法性|合规性|资格|有效性|isvalid|checker', '✅'),
    (r'检查|检测|探查|扫描|识别|诊断|排查|审计|巡检|筛查|排查表', '🔍'),
    (r'速查|查询|查找|检索|对照表|字典|参考|指南|词典|字典表|手册', '📚'),
    (r'评分|评估|评价|量表|问卷|自评|分级|分期|分层|风险|严重度|指数|得分|打分|评级', '📋'),
    (r'对比|比较|差异|对照|pk|优劣', '⚖️'),
    (r'预测|预估|估算|趋势|外推|拟合|推算', '🔮'),
    (r'优化|调优|改进|提升|最佳|选型|择优选', '🚀'),
    (r'统计|汇总|报表|频数|占比|分布|聚类|回归|方差分析|相关|置信|显著性|检验', '📊'),
    (r'分析|解析|剖析|拆解|解构|诊断', '📊'),
    (r'设计|规划|方案|布局|排布|布置|排版设计|选型设计', '📐'),
    (r'清单|表单|清单生成|清单校验|模板|工单|目录', '📋'),
    (r'提醒|通知|到期|预警|告警|定时|周期提醒', '⏰'),
    (r'模拟|仿真|推演|沙盘', '🧪'),
    (r'测试|测验|考试|自测|题库|练习|测评', '📝'),
    (r'计时|计时器|秒表|耗时|时长|工期|周期', '⏱️'),
    (r'排序|去重|合并|拆分|拆分文本|分组|分组统计|归并|排列顺序', '🔀'),
    (r'提取|抽取|抓取|解析出|过滤|筛选|清洗', '🔎'),
    (r'格式化|美化|排版|缩进|对齐|整理|规范化', '🧹'),
    (r'压缩|精简|最小化|瘦身|minify', '🗜️'),
    (r'换算|转换|互转|互化|转换器|converter|进制转换|单位|换算器', '🔄'),
    (r'计算|计算器|求解|求值|估算值|calculator|算式', '🧮'),
    (r'矩阵|向量|行列式|转置|叉积|点积|模长', '🔢'),
    (r'方程|求根|解方程|方程组|不等式', '🧮'),
    (r'几何|圆|三角形|梯形|多边形|对角线|斜边|海伦|圆柱|圆锥|扇形|正多边形', '📐'),
    (r'概率|分布|泊松|正态|二项|超几何|贝叶斯|假设检验|抽样|显著性', '🎲'),
    (r'素数|质数|gcd|最大公约|最小公倍|阶乘|排列|组合|斐波那契|因式|约数', '🔢'),
    (r'对数|幂|平方根|立方根|指数|圆周率|π', '🧮'),
    (r'快照|截图|截屏|录屏', '📸'),
    (r'预览|编辑|编辑器|查看器|浏览器|reader', '👀'),
]

# 无规则命中时的最终兜底：行业图标 → 功能分类图标 → 中性图标
def _tool_icon_fallback(cat, industry):
    ind = INDUSTRY_DEFS.get(industry)
    if ind:
        return ind[0]
    cd = CAT_DEFS.get(cat)
    if cd:
        return cd[0]
    return '📦'

def tool_icon_candidates(name_zh, slug, cat, industry, limit=5):
    """按规则表给出该工具的候选图标（优先级从高到低，末尾为兜底）。"""
    hay = '%s %s' % (name_zh or '', (slug or '').replace('-', ' ').replace('_', ' '))
    cands = []
    for pat, emo in TOOL_ICON_RULES:
        if emo in cands:
            continue
        try:
            hit = re.search(pat, hay, re.I)
        except re.error:
            hit = None
        if hit:
            cands.append(emo)
            if len(cands) >= limit:
                break
    for tail in (_tool_icon_fallback(cat, industry), CAT_DEFS.get(cat, ('📦',))[0]):
        if tail and tail not in cands:
            cands.append(tail)
    return cands


def assign_tool_icons(tools, verbose=False):
    """在行业内部为每个工具分配图标，并对同图标数量设上限，避免清一色。

    候选顺序即优先级；只有当首选图标在该行业已用满上限时，才退到次选，
    因此绝大多数工具仍拿到语义上最贴切的图标，同时保证分类页图标多样。
    """
    from collections import Counter, defaultdict
    n_by = Counter(t['industry'] for t in tools)
    cap = {ind: max(2, (n + 3) // 4) for ind, n in n_by.items()}
    used = defaultdict(Counter)
    changed = 0
    for t in tools:
        keep = t.get('_icon_keep')
        if keep:
            t['icon'] = keep
            continue
        cands = t.get('_icon_cands') or ['📦']
        ind = t['industry']
        pick = None
        for c in cands:
            if used[ind][c] < cap[ind]:
                pick = c
                break
        if pick is None:
            # 所有候选都已达本行业上限：选当前用量最少的候选，尽量在行业内保持多样（避免清一色）。
            # 旧实现回退到 cands[0] 会突破 cap 把同一图标堆满整页，已修正。
            pick = min(cands, key=lambda c: used[ind][c])
        used[ind][pick] += 1
        if pick != t.get('icon'):
            changed += 1
        t['icon'] = pick
    if verbose:
        print('Tool icons: %d 个工具的图标按语义重新分配' % changed)
    return changed


# 工具页「自身图标位」：meta / h2(中英) / 按钮 / JS 结果标题。
# 不含相关工具卡 rt-icon —— 后者指向别的工具，由相关工具块单独刷新，
# 避免把本工具图标误写到别家卡片（造成相关工具图标错乱）。
_TOOL_ICON_POS_SELF = (
    r'(<meta name="toolbox"[^>]*icon=)%s(?=[,"])',
    r'(<h2[^>]*data-zh=")%s(?=\s)',
    r'(<h2[^>]*>)%s(?=\s)',
    r'(<button[^>]*>)%s(?=\s)',
    r'(margin-bottom:12px;">)%s(?=\s)',
)
# 相关工具卡图标位（指向别的工具，刷新时用目标工具当前图标）。
_TOOL_ICON_POS_RT = (
    r'(<span class="rt-icon">)%s(?=</span>)',
)


def normalize_tool_icon_in_page(content, old_icon, new_icon, pos_subs=None):
    """把工具页正文（meta/h2/按钮/结果标题/相关工具卡）里的旧图标换成新图标。

    仅作用于明确的「图标位」，不触碰正文里同名的装饰性 emoji。
    pos_subs 缺省为 _TOOL_ICON_POS_SELF（工具自身图标位）；相关工具卡 rt-icon
    用 _TOOL_ICON_POS_RT 处理。
    """
    if not old_icon or not new_icon or old_icon == new_icon:
        return content, 0
    pats = [re.compile(p % re.escape(old_icon)) for p in (pos_subs or _TOOL_ICON_POS_SELF)]
    hits = 0
    out = []
    for line in content.split('\n'):
        if old_icon in line:
            for pat in pats:
                line, n = pat.subn(lambda m: m.group(1) + new_icon, line)
                hits += n
        out.append(line)
    if not hits:
        return content, 0
    return '\n'.join(out), hits


def _refresh_breadcrumb_icon(content, ind_icon):
    """刷新面包屑中行业链接的前导图标为当前行业图标（幂等；根治历史 🔧 残留）。

    面包屑因「data-breadcrumb 已存在则跳过」而保留旧图标——早期 INDUSTRY_DEFS
    未修正时注入的 🔧 行业图标不会随分类图标修复而更新，此处补刷新。
    """
    if not ind_icon:
        return content
    pat = re.compile(r'(<span class="bc-sep">‹</span>\s*<a href="[^"]*index\.html">)[^<]*(?=\s)')
    return pat.sub(lambda m: m.group(1) + ind_icon, content)


# ============================================================
# Category definitions (functional)
# ============================================================
CAT_DEFS = {
    'text':      ('📝', '#e8eaf6', '文本处理'),
    'encode':    ('🔐', '#f3e5f5', '编码解码'),
    'convert':   ('🔄', '#e8eaf6', '格式转换'),
    'generate':  ('🎲', '#e3f2fd', '生成器'),
    'dev':       ('💻', '#fff3e0', '开发工具'),
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
    'engineering':   ('⚙️', '工程计算'),
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

    'accessibility': ('♿', '无障碍工具'),
    'accounting': ('🧾', '会计审计'),
    'acupuncture': ('🪡', '针灸推拿'),
    'admin': ('🗂️', '行政管理'),
    'advertising': ('📣', '广告设计'),
    'aerospace': ('🚀', '航空航天'),
    'antiques': ('🏺', '古董鉴定'),
    'aquaculture': ('🐟', '水产养殖'),
    'archaeology': ('🏺', '考古文博'),
    'archive': ('🗄️', '档案管理'),
    'astronomy': ('🔭', '天文观测'),
    'audio': ('🎧', '音频工具'),
    'auto-beauty': ('🚘', '汽车美容'),
    'automation': ('🛠️', '工业自动化'),
    'baking': ('🧁', '烘焙甜点'),
    'ballistics': ('🎯', '弹道武器'),
    'beekeeping': ('🐝', '蜜蜂养殖'),
    'beneficiation': ('⛏️', '选矿冶炼'),
    'blasting': ('💥', '爆破工程'),
    'bonding': ('🧷', '粘接密封'),
    'brand': ('🏷️', '品牌管理'),
    'bridge': ('🌉', '桥梁工程'),
    'building-material': ('🧱', '建筑材料'),
    'cable': ('🔌', '电缆电线'),
    'cardiology': ('🫀', '心血管科'),
    'casting': ('🔥', '铸造工程'),
    'ceramics': ('🏺', '陶瓷工艺'),
    'chess': ('♟️', '棋类游戏'),
    'chinese-cook': ('🥘', '中式烹饪'),
    'civil': ('🏗️', '土木工程'),
    'cleaning': ('🧹', '清洁保洁'),
    'clinical-lab': ('🔬', '临床检验'),
    'clinical-nursing': ('💉', '临床护理'),
    'cnc': ('🔲', '数控加工'),
    'community': ('🏘️', '社区管理'),
    'consulting': ('💬', '咨询顾问'),
    'content': ('✍️', '内容创作'),
    'convenience': ('🏪', '便利店务'),
    'cosmetic-derm': ('✨', '美容皮肤'),
    'cosmetics': ('💅', '化妆品'),
    'customer-service': ('🎧', '客户服务'),
    'daily-goods': ('🛒', '日用百货'),
    'dailychem': ('🧴', '日用化工'),
    'dance': ('💃', '舞蹈艺术'),
    'decor': ('🛋️', '室内装修'),
    'defense': ('🛡️', '国防军事'),
    'dentistry': ('🦷', '口腔医学'),
    'dermatology': ('🧴', '皮肤性病'),
    'discipline': ('📋', '规章制度'),
    'domestic': ('🧺', '家政服务'),
    'dyeing': ('🎨', '印染染色'),
    'ecommerce': ('🛍️', '电子商务'),
    'elderly': ('👴', '养老护理'),
    'electrical': ('🔌', '电气工程'),
    'embedded': ('🔲', '嵌入式'),
    'endocrinology': ('🧬', '内分泌科'),
    'ent': ('👂', '耳鼻喉科'),
    'event': ('🎪', '活动策划'),
    'exhibition': ('🎫', '会展服务'),
    'express': ('📦', '快递物流'),
    'film': ('🎞️', '电影影视'),
    'fire': ('🚒', '消防安全'),
    'fire-rescue': ('🚒', '消防救援'),
    'fitness': ('🏋️', '健身运动'),
    'floral': ('💐', '花艺设计'),
    'food-processing': ('🏭', '食品加工'),
    'food-safety': ('🥗', '食品安全'),
    'food-testing': ('🧫', '食品检测'),
    'forensic-medicine': ('⚖️', '法医学'),
    'forex': ('💱', '外汇交易'),
    'fresh': ('🧊', '生鲜冷链'),
    'funeral': ('⚱️', '殡葬服务'),
    'furniture': ('🪑', '家具制造'),
    'futures': ('📉', '期货交易'),
    'gas': ('🔥', '燃气工程'),
    'gastroenterology': ('🩻', '消化内科'),
    'general': ('🛠️', '通用工程'),
    'geology': ('🪨', '地质勘探'),
    'gis': ('🗺️', '地理信息'),
    'glass': ('🪟', '玻璃工艺'),
    'hardware': ('🪛', '五金建材'),
    'healthcare': ('🩺', '医疗保健'),
    'heattreat': ('🔥', '热处理'),
    'hematology': ('🩸', '血液科'),
    'hotel': ('🏨', '酒店管理'),
    'hr': ('👥', '人力资源'),
    'hvac': ('❄️', '暖通空调'),
    'hydraulic': ('💧', '水利工程'),
    'insurance': ('🛡️', '保险计算'),
    'interior': ('🖼️', '室内装饰'),
    'jewelry': ('💎', '珠宝首饰'),
    'knowledge': ('📚', '知识管理'),
    'labor-protection': ('🦺', '劳动保护'),
    'landscape': ('🌳', '园林绿化'),
    'leather': ('👜', '皮革加工'),
    'livestream': ('📹', '直播电商'),
    'machinery': ('⚙️', '机械制造'),
    'martial-arts': ('🥋', '武术格斗'),
    'mechanical': ('⚙️', '机械工程'),
    'media': ('📰', '媒体传播'),
    'metallurgy': ('🔩', '冶金材料'),
    'metalwork': ('🔨', '金属加工'),
    'meteorology': ('🌤️', '气象天气'),
    'mold': ('🧩', '模具工程'),
    'municipal': ('🚧', '市政工程'),
    'nephrology': ('🩺', '肾脏内科'),
    'network': ('🌐', '网络技术'),
    'neurology': ('🧠', '神经内科'),
    'niche': ('🎯', '垂直工具'),
    'nutrition': ('🥗', '营养膳食'),
    'obstetrics': ('🤱', '产科医学'),
    'office': ('📄', '办公文档'),
    'ophthalmology': ('👁️', '眼科医学'),
    'optical': ('👓', '视光科学'),
    'outdoor': ('🏕️', '户外运动'),
    'packaging': ('📦', '包装工程'),
    'paint': ('🎨', '油漆涂料'),
    'paper': ('📄', '造纸印刷'),
    'pediatrics': ('🧒', '儿科医学'),
    'pharma': ('⚗️', '制药工程'),
    'pharmacy': ('💊', '药学'),
    'photography': ('📸', '摄影摄像'),
    'pipe': ('🚰', '管道工程'),
    'plastic': ('🧴', '塑料橡胶'),
    'pneumatic': ('💨', '气动液压'),
    'port': ('🛥️', '港口工程'),
    'pr': ('📢', '公关传播'),
    'printing': ('🖨️', '印刷技术'),
    'procurement': ('🛒', '采购供应'),
    'project': ('📊', '项目管理'),
    'property': ('🏢', '物业管理'),
    'psychiatry': ('🧠', '精神心理'),
    'psychology': ('💭', '心理咨询'),
    'pulmonology': ('🫁', '呼吸内科'),
    'quality': ('✅', '质量管理'),
    'railway': ('🚆', '铁路工程'),
    'realestate': ('🏘️', '房地产'),
    'rehabilitation': ('🦾', '康复医学'),
    'rental': ('🔑', '租赁管理'),
    'reproductive-medicine': ('🧬', '生殖医学'),
    'research': ('🎓', '科研学术'),
    'rheumatology': ('🦴', '风湿免疫'),
    'road': ('🛣️', '道路工程'),
    'rubber': ('🧴', '橡胶制品'),
    'safety': ('🦺', '安全生产'),
    'securities': ('📈', '证券投资'),
    'security': ('🔒', '网络安全'),
    'security-guard': ('👮', '安保服务'),
    'seismology': ('🌐', '地震学'),
    'shipping': ('🚢', '船舶海运'),
    'sports-event': ('🏆', '体育赛事'),
    'stage': ('🎭', '舞台演出'),
    'steel': ('🏗️', '钢铁冶金'),
    'stone': ('🪨', '石材加工'),
    'supplychain': ('🚛', '供应链'),
    'surface': ('✨', '表面处理'),
    'surveying': ('📐', '测绘工程'),
    'tcm-chemistry': ('🌿', '中药化学'),
    'tcm-diagnosis': ('🩺', '中医诊断'),
    'tcm-pharmacy': ('🌿', '中药学'),
    'telecom': ('📡', '通信技术'),
    'timber': ('🪵', '木材加工'),
    'transport': ('🚚', '交通运输'),
    'tunnel': ('🚇', '隧道工程'),
    'uiux': ('🎨', 'UI/UX设计'),
    'unitedfront': ('🤝', '统战工作'),
    'urban': ('🏙️', '城市规划'),
    'urology': ('🩺', '泌尿外科'),
    'usedcar': ('🚙', '二手车'),
    'valve': ('🚰', '阀门工程'),
    'warehouse': ('🏬', '仓储管理'),
    'water': ('💧', '水利工程'),
    'wedding': ('💒', '婚礼策划'),
    'welding': ('🔥', '焊接工程'),
    'woodwork': ('🪚', '木工制作'),
    'yoga': ('🧘', '瑜伽冥想'),
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
    # P5 · 认知脑力与色觉无障碍
    'cognition': ('🧠', '认知与脑力训练'),
    'colorvision': ('🎨', '色觉与色彩无障碍'),
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


def _shared_script_hashes(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return ()
    if 'TOOLBOX-REDIRECT' in content:
        return ()
    return {
        hashlib.md5(block.encode('utf-8')).hexdigest()
        for block in re.findall(r'<script>(.*?)</script>', content, re.S)
    }

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
    page_files = []
    for root, dirs, files in os.walk(TOOLS_DIR):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            page_files.append(os.path.join(root, fn))

    workers = _configured_build_workers(len(page_files))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        page_hashes = executor.map(_shared_script_hashes, page_files)

        freq = {}
        for seen in page_hashes:
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
    # 外置的页面专属脚本（由 scripts/extract_inline_scripts.py 从内联块搬移到
    # js/tools/<name>.js）仍是本页自研逻辑，须计入 own_len；否则 HTML 瘦身会让
    # 这些页的 own_len 归零、质量分级从 A 误降为 B（2026-09-05 实测踩到）。
    # 这类文件与页面一一对应，不属于跨页共享模板，无需走 shared 去重。
    for _src in re.findall(r'<script src="(/js/tools/[^"]+\.js)"', content):
        _p = os.path.join(ROOT, _src.lstrip('/'))
        try:
            with open(_p, encoding='utf-8') as _f:
                own_len += len(_f.read())
        except OSError:
            pass
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
    cat_def = CAT_DEFS.get(cat, (INDUSTRY_DEFS.get(industry, ('🛠️', industry))[0], '#f5f5f5', cat))
    icon, bg, _ = cat_def

    # 图标决策（2026-09-12）：不再把 meta icon 当作「人工专属」保留。
    # 早期生成器把行业 emoji / 🔧 写进每个工具 meta——含 Task#1 修正前的旧行业 emoji
    # （如 blasting 旧 💣 已被改为 💥），它们与「当前行业图标」不等，会被误判为人工专属而保留，
    # 导致整个行业图标清一色。此处一律视为占位，交给 assign_tool_icons() 按工具名语义推导 +
    # 行业内部均衡去重（根治「清一色」与「图标不合适」两类问题）。
    # meta 图标在 process_tool_pages 阶段被规范化写成语义图标，作为下一轮构建输入（幂等）。
    meta_icon = (tb_meta.get('icon') or '').strip()
    if 'bg' in tb_meta:
        bg = tb_meta['bg']

    # URL: relative from root (tools/industry/file.html)
    url = 'tools/' + rel_path.replace(os.sep, '/')

    return {
        'name': title,
        'cat': cat,
        'industry': industry,
        'icon': icon,   # 初始值=cat 默认；assign_tool_icons 会用语义候选覆盖（keep 已废弃）
        '_meta_icon': meta_icon,
        '_icon_keep': None,
        '_icon_cands': tool_icon_candidates(title, name_base, cat, industry),
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


# 中文描述字段 d 的统一取源（治本）：运行时渲染器按 t.d(中文) || t.desc(英文) 取描述，
# 但此前 tools.json / industry-*.json 缺 d 字段，导致 SPA 行业网格在中文模式回退英文 desc。
# 此处补上 d，优先级与 tools.json（合并后的搜索单一数据源）保持一致：
#   i18n zh-CN.desc > zh-CN.intro > 工具自带 desc > 中文名；全无中文才回退英文原名。
_zh_desc_i18n_cache = {}
def _load_zh_desc_i18n(ind):
    if ind not in _zh_desc_i18n_cache:
        fp = os.path.join(ROOT, 'i18n', 'tools', ind + '.json')
        try:
            _zh_desc_i18n_cache[ind] = json.load(open(fp, encoding='utf-8')) if os.path.isfile(fp) else {}
        except Exception:
            _zh_desc_i18n_cache[ind] = {}
    return _zh_desc_i18n_cache[ind]

def compute_zh_desc(t):
    """中文描述（写入 tools.json 的 d，供搜索/首页/导航消费）。

    注意：历史上这里只判「含中文」就返回，而 i18n 的 zh-CN.desc 往往就是标题本身
    （如「矩阵转置」），导致描述退化成名称。现统一走 TDS.zh_desc()，
    按 强desc → intro → 页面meta → 中文名 的优先级取真实描述。
    """
    return TDS.zh_desc(t, max_len=80)


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
            # 注意：t['en'] 已由主循环（main 中 for t in tools 统一赋值）设好，
            # 此处不可再无条件 translate_name 覆盖——translate_name 对未收录词会
            # 回退返回中文名，既污染「英文名称」字段，又会让下方 TDS.en_desc 误把
            # 中文名当英文前缀削掉，造成分类页与 tools.json 的 en/ed 双不一致。
            if 'en' not in t:
                t['en'] = translate_name(t.get('name', ''))
            # 先应用英文名称覆盖（与主循环顺序一致），确保 en_desc 用可靠英文名削前缀
            apply_en_override(t)
            t['ed'] = TDS.en_desc(t, max_len=60)   # 与 tools.json / 导航共用单一权威英文描述
            t['d'] = compute_zh_desc(t)   # 治本：补中文 d，消除 SPA 网格中文模式英文描述泄漏
        items = sorted(items, key=hot_sort_key)   # 行业内工具按热度降序（驱动运行时分类页/导航）
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
        base = os.path.basename(filename)
        # industry-groups.json 是 2 级分组导航产物，不在这里清理
        if base == 'industry-groups.json' or base in active_files:
            continue
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print('  cleared orphan %s' % base)
    

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
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/', today, 'daily', '1.0'))
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/sitemap.html', today, 'weekly', '0.9'))
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/search.html', today, 'weekly', '0.9'))
    # Category index pages
    if category_inds:
        for ind in sorted(category_inds):
            lines.extend(_localized_url_blocks('https://chenguangwu.github.io/tools/%s/index.html' % ind, today, 'weekly', '0.9'))
    # guides/ 指南页（自动扫描，避免重跑构建后丢失）
    # 若某指南存在同名 .en.html 英文版，则声明双向 hreflang（zh 文件 <-> en 文件）；
    # 否则沿用既有 ?lang=en 约定（与工具页一致），保持旧行为、最小 diff。
    guides_dir = os.path.join(ROOT, 'guides')
    if os.path.isdir(guides_dir):
        for fn in sorted(os.listdir(guides_dir)):
            if fn.endswith('.html') and fn != 'index.html':
                abs_url = 'https://chenguangwu.github.io/guides/%s' % fn
                if fn.endswith('.en.html'):
                    lines.append(_url_block(abs_url, today, 'monthly', '0.7'))
                else:
                    lines.extend(_localized_url_blocks(abs_url, today, 'monthly', '0.8'))
    # chains.html 工具链页（B3-05）
    if os.path.isfile(os.path.join(ROOT, 'chains.html')):
        lines.extend(_localized_url_blocks('https://chenguangwu.github.io/chains.html', today, 'weekly', '0.8'))
    # about.html 关于我们
    if os.path.isfile(os.path.join(ROOT, 'about.html')):
        lines.extend(_localized_url_blocks('https://chenguangwu.github.io/about.html', today, 'monthly', '0.7'))
    for t in tools:
        url = 'https://chenguangwu.github.io/' + t['url']
        lines.extend(_localized_url_blocks(url, today, 'monthly', '0.8'))
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


def _guide_alternates_xml(zh_url, en_url=None):
    """指南页 hreflang 变体 XML。

    en_url 给定时用「独立英文文件」互链（zh 文件 <-> en 文件，x-default 指向 zh）；
    为 None 时回退到既有 ?lang=en 约定（保持其他指南旧行为，最小 diff）。
    """
    if en_url:
        return ('    <xhtml:link rel="alternate" hreflang="zh-CN" href="%s"/>\n'
                '    <xhtml:link rel="alternate" hreflang="en-US" href="%s"/>\n'
                '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                ) % (zh_url, en_url, zh_url)
    return _xhtml_alternates(zh_url)


def _url_block_alts(url, today, freq, prio, alts_xml):
    """含指定多语言 xhtml:link 变体的 <url> 块（变体由调用方预生成）。"""
    return ('  <url>\n'
            '    <loc>%s</loc>\n'
            '    <lastmod>%s</lastmod>\n'
            '    <changefreq>%s</changefreq>\n'
            '    <priority>%s</priority>\n'
            '%s\n'
            '  </url>' % (url, _lastmod_for(url, today), freq, prio, alts_xml))


def generate_core_sitemap(today):
    """Root-level core URLs (home, html sitemap, search, guides) as a standalone sitemap."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/', today, 'daily', '1.0'))
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/sitemap.html', today, 'weekly', '0.9'))
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/search.html', today, 'weekly', '0.9'))
    if os.path.isfile(os.path.join(ROOT, 'about.html')):
        lines.extend(_localized_url_blocks('https://chenguangwu.github.io/about.html', today, 'monthly', '0.7'))
    # guides/ 目录下的指南页（自动扫描，避免重跑构建后丢失）
    guides_dir = os.path.join(ROOT, 'guides')
    if os.path.isdir(guides_dir):
        for fn in sorted(os.listdir(guides_dir)):
            if fn.endswith('.html') and fn != 'index.html':
                lines.extend(_localized_url_blocks('https://chenguangwu.github.io/guides/%s' % fn,
                                                   today, 'monthly', '0.8'))
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def generate_industry_sitemap(ind, ind_tools, today):
    """Per-industry sitemap.xml placed under tools/<ind>/. Includes the category index page + all tools."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    lines.extend(_localized_url_blocks('https://chenguangwu.github.io/tools/%s/index.html' % ind, today, 'weekly', '0.9'))
    for t in sorted(ind_tools, key=lambda x: x['name']):
        url = 'https://chenguangwu.github.io/' + t['url']
        lines.extend(_localized_url_blocks(url, today, 'monthly', '0.8'))
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
    # 分类聚合热度（分类自身按热度排序用）
    agg_hot = {ind: sum(t.get('hot', 0) for t in tl) for ind, tl in ind_tools.items()}
    
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
<link rel="stylesheet" href="/css/site-chrome.css">
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
/* 中英双语：工具链接名称各含两层，由 html[lang] 切换显隐（与 css/common.css 的 .cat-tool 规则同构） */
html[lang="en-US"] .tool-link .t-zh{display:none !important;}
html:not([lang="en-US"]) .tool-link .t-en{display:none !important;}
</style>
<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard','copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool','toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});(function(){var T=window.ToolBox;if(typeof T.escHtml!=='function')T.escHtml=function(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;};if(typeof T.formatNumber!=='function')T.formatNumber=function(n,dec){if(typeof n!=='number'||isNaN(n))return String(n);dec=dec!=null?dec:0;return n.toLocaleString('zh-CN',{minimumFractionDigits:dec,maximumFractionDigits:dec});};if(typeof T.createTable!=='function')T.createTable=function(h,r){var x='<table><thead><tr>';h.forEach(function(t){x+='<th>'+T.escHtml(t)+'</th>';});x+='</tr></thead><tbody>';r.forEach(function(row){x+='<tr>';row.forEach(function(c){x+='<td>'+(c!=null?T.escHtml(String(c)):'')+'</td>';});x+='</tr>';});return x+'</tbody></table>';};if(typeof T.debounce!=='function')T.debounce=function(fn,ms){var t;return function(){var a=arguments,s=this;clearTimeout(t);t=setTimeout(function(){fn.apply(s,a);},ms);};};})();</script><!-- TOOLBOX-API-STUB -->
<script src="/js/i18n.js" defer></script>
<script src="/js/common.js" defer></script>
</head>
<body>
<a href="/" class="back" data-i18n="sitemap.back" data-i18n-fb="← 返回首页">← 返回首页</a>
<h1><a href="/">🧰 ToolBox</a></h1>
<p class="subtitle"><span data-i18n="sitemap.subtitle_a" data-i18n-fb="站点地图 · 共 ">站点地图 · 共 </span>%d<span data-i18n="sitemap.subtitle_b" data-i18n-fb=" 个免费在线工具 · 更新于 "> 个免费在线工具 · 更新于 </span>%s</p>
''' % (len(tools), today)
    
    for ind in sorted([i for i in ind_order if i in ind_tools], key=lambda i: -agg_hot.get(i, 0)):
        if ind not in ind_tools:
            continue
        tlist = ind_tools[ind]
        ind_def = INDUSTRY_DEFS.get(ind, ('🗂️', ind, ''))
        icon = ind_def[0]
        name = ind_def[1]
        html += f'<h2>{icon} <span data-i18n="ind_{ind}" data-i18n-fb="{name}">{name}</span><span class="count">({len(tlist)}<span data-i18n="sitemap.count_suffix" data-i18n-fb="个工具">个工具</span>)</span></h2>\n'
        html += '<div class="grid">\n'
        for t in sorted(tlist, key=hot_sort_key):
            html += f'  <a class="tool-link" href="/{t["url"]}"><span class="t-zh">{t["icon"]} {t["name"]}</span><span class="t-en">{t["icon"]} {t.get("en") or t["name"]}</span></a>\n'
        html += '</div>\n'
    
    for ind in sorted(ind_tools.keys(), key=lambda i: -agg_hot.get(i, 0)):
        if ind not in ind_order:
            tlist = ind_tools[ind]
            _def = INDUSTRY_DEFS.get(ind, ('🗂️', ind))
            html += f'<h2>{_def[0]} <span data-i18n="ind_{ind}" data-i18n-fb="{_def[1]}">{_def[1]}</span><span class="count">({len(tlist)}<span data-i18n="sitemap.count_suffix" data-i18n-fb="个工具">个工具</span>)</span></h2>\n'
            html += '<div class="grid">\n'
            for t in sorted(tlist, key=hot_sort_key):
                html += f'  <a class="tool-link" href="/{t["url"]}"><span class="t-zh">{t["icon"]} {t["name"]}</span><span class="t-en">{t["icon"]} {t.get("en") or t["name"]}</span></a>\n'
            html += '</div>\n'
    
    html += '''<div class="footer">
<p><a href="/sitemap.xml">XML Sitemap</a> · <a href="/" data-i18n="sitemap.back_home" data-i18n-fb="返回首页">返回首页</a></p>
<p data-i18n="sitemap.copyright" data-i18n-fb="© 2026 ToolBox - 免费在线工具集合">© 2026 ToolBox - 免费在线工具集合</p>
</div>
</body>
</html>'''
    # 模板里的 ToolBox 桩为硬编码旧版，统一走升级函数，与 TOOLBOX_API_STUB 常量保持同步
    return _upgrade_toolbox_api_stub(html)


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
    for name in ('tools.json', 'guides.json', 'channel.json'):
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
        base = os.path.basename(fp)
        if base == 'industry-groups.json':
            continue
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            print('Build consistency failed: industry file not list -> %s' % base)
            return False
        industry_total += len(data)

    if expected_tools != industry_total:
        print('Build consistency failed: industry json total mismatch')
        print('  expected=%d actual=%d' % (expected_tools, industry_total))
        return False

    guides_dir = os.path.join(ROOT, 'guides')
    guides_count = 0
    guide_en_count = 0
    if os.path.isdir(guides_dir):
        guides_count = len([fn for fn in os.listdir(guides_dir)
                            if fn.endswith('.html') and fn != 'index.html' and not fn.endswith('.en.html')])
        guide_en_count = len([fn for fn in os.listdir(guides_dir) if fn.endswith('.en.html')])
    has_chains = 1 if os.path.isfile(os.path.join(ROOT, 'chains.html')) else 0
    has_about = 1 if os.path.isfile(os.path.join(ROOT, 'about.html')) else 0
    expected_sitemap_urls = (
        (expected_tools + 3 + len(category_inds) + guides_count + has_chains + has_about)
        * len(I18N_STATIC_LOCALES) + guide_en_count
    )
    actual_sitemap_urls = _count_xml_urls(SITEMAP_FILE)
    if expected_sitemap_urls != actual_sitemap_urls:
        print('Build consistency failed: sitemap url count mismatch')
        print('  expected=%d actual=%d' % (expected_sitemap_urls, actual_sitemap_urls))
        print('  formula: static Chinese variants + standalone English guide pages')
        return False

    return True


def generate_opencc_static_locales():
    """Generate zh-tw/ only after every source HTML/JSON artifact is final."""
    script = os.path.join(ROOT, 'scripts', 'gen_opencc_locales.mjs')
    print('\nGenerating static OpenCC locales:')
    try:
        subprocess.run(['node', script], cwd=ROOT, check=True)
        subprocess.run(['node', script, '--check'], cwd=ROOT, check=True)
    except FileNotFoundError:
        raise SystemExit('OpenCC locale build requires Node.js. Run npm ci before python3 _build.py.')
    except subprocess.CalledProcessError as exc:
        raise SystemExit('OpenCC locale build failed: %s' % exc)


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
        '<title>ToolBox - 5000+免费在线工具集合，纯前端处理数据不上传 | 工具百科</title>', html)

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
    # P0-05 统计数字统一：首页各处的营销数字统一为品牌口径 5000+，
    # 不再注入真实工具数（避免与 title/description/og:image 等处的 5000+ 不一致）。
    html = re.sub(r'等\d+\+实用工具', '等5000+实用工具', html)

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


_HEAD_OPEN_RE = re.compile(r'<head(?:\s[^>]*)?>', re.I)
_HEAD_CLOSE_RE = re.compile(r'</head\s*>', re.I)


def _document_head_bounds(content):
    """Return the real document head boundaries, ignoring HTML fragments in JS strings."""
    opening = _HEAD_OPEN_RE.search(content)
    if not opening:
        return None
    # Pattern.search(..., pos) avoids copying the complete (sometimes multi-MB)
    # body merely to find a closing tag near the beginning of the document.
    closing = _HEAD_CLOSE_RE.search(content, opening.end())
    if not closing:
        return None
    return opening.start(), opening.end(), closing.start(), closing.end()


def _head_contains(content, needle):
    bounds = _document_head_bounds(content)
    return bool(bounds and needle in content[bounds[1]:bounds[2]])


def _sub_in_document_head(pattern, repl, content, count=0, flags=0):
    """Apply a regex only to the real document head, not a multi-MB body."""
    bounds = _document_head_bounds(content)
    if not bounds:
        return content
    head = content[bounds[1]:bounds[2]]
    updated = re.sub(pattern, repl, head, count=count, flags=flags)
    if updated == head:
        return content
    return content[:bounds[1]] + updated + content[bounds[2]:]


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
        '.deep-dive{max-width:960px;margin:16px auto;padding:0 16px;}\n'
        '.deep-dive > .card{margin-bottom:0;}\n'
        '@media(max-width:600px){.deep-dive{margin:14px auto;padding:0 12px;}}\n'
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


_DEEP_DIVE_BLOCK_RE = re.compile(
    r'<!-- TOOLBOX-DEEP-DIVE -->\s*'
    r'<style>\s*\.deep-dive[\s\S]*?</style>\s*'
    r'<section class="deep-dive"[^>]*>[\s\S]*?</section>',
    re.I,
)


def _css_nonblocking(content):
    """仅把非关键 nav-menu.css 改为非阻塞加载。

    common.css 包含运行时注入的统一顶部导航样式。若将它异步加载，common.js
    可能先插入搜索框，导致首屏短暂显示浏览器默认的大输入控件。因此 common.css
    必须保持阻塞加载；只有二级菜单样式可以延后。

    幂等关键点：二次 build 时 content 已含 preload + <noscript><link rel=stylesheet>...</noscript>，
    若直接 re.sub 会再次匹配 noscript 内部的回退 stylesheet 并嵌套 <noscript>，破坏结构。
    故先 stash 所有 <noscript> 块（占位符保护），在块外安全替换阻塞 link，再还原 noscript。
    """
    nss = {}
    def _stash(m):
        k = '\x00NS%d\x00' % len(nss)
        nss[k] = m.group(0)
        return k
    # 旧构建产物把 common.css 写成 preload + noscript。先还原为普通 stylesheet，
    # 并移除对应的 noscript 回退，避免后续构建遗留重复标签。
    content = re.sub(
        r'<link rel="preload" as="style" href="([^"]*common\.css)" onload="this\.onload=null;this\.rel=\'stylesheet\'">\s*'
        r'<noscript><link rel="stylesheet" href="\1"></noscript>',
        r'<link rel="stylesheet" href="\1">',
        content,
    )
    c2 = re.sub(r'<noscript>.*?</noscript>', _stash, content, flags=re.S)

    def _repl(m):
        href = m.group(1)
        return ('<link rel="preload" as="style" href="%s" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
                '<noscript><link rel="stylesheet" href="%s"></noscript>' % (href, href))

    c2 = re.sub(r'<link rel="stylesheet" href="([^"]*nav-menu\.css)">', _repl, c2)
    for k, v in nss.items():
        c2 = c2.replace(k, v)
    return c2


# 旧桩特征：<script>window.__tbq= ... </script><!-- TOOLBOX-API-STUB -->
_TOOLBOX_STUB_OLD_RE = re.compile(
    r'<script>window\.__tbq=[\s\S]*?</script>' + re.escape(TOOLBOX_API_STUB_MARKER)
)


def _upgrade_toolbox_api_stub(content):
    """把页面里「只覆盖 13 个无返回值方法」的旧 ToolBox 桩，原地升级为含纯函数实现的新桩。

    背景：scripts/gen_*.py 生成器把旧桩硬编码进页面（存量 5270 个）。旧桩缺
    escHtml / formatNumber / createTable / debounce，页面内联脚本顶层一旦调用即抛
    TypeError，整页功能不可用（详见 TOOLBOX_API_STUB 注释）。

    幂等判定：以 stub 版本号 __stubV 为指纹。不可用方法名（如 T.escHtml）做指纹——
    一旦后续往早期 API 里新增方法，历史页面会被误判为「已升级」而跳过，新版无法下发。
    """
    if TOOLBOX_API_STUB_MARKER not in content:
        return content
    # 数值比较版本号：解析页面现有 __stubV=N，已 >= 当前版本则幂等返回。
    # 不能用方法名（如 T.escHtml）做指纹——后续往早期 API 新增方法时，历史页面
    # 会被误判为「已升级」而跳过，新版无法下发。
    _m = re.search(r'__stubV=(\d+)', content)
    if _m and int(_m.group(1)) >= TOOLBOX_STUB_VERSION:
        return content
    new_stub = TOOLBOX_API_STUB.rstrip('\n')
    # 必须用 lambda 传入替换串：stub 内含 \w、\( 等正则转义，直接作为模板会被 re 解析而报 bad escape
    new_content, n = _TOOLBOX_STUB_OLD_RE.subn(lambda _m: new_stub, content, count=1)
    return new_content if n else content


def fix_tool_pages_seo(tools, target_tools=None, report=True, existing_html_paths=None):
    """Post-process all tool pages: ensure h1, add breadcrumbs, related tools, structured data."""
    by_industry = {}
    for t in tools:
        ind = t['industry']
        by_industry.setdefault(ind, []).append(t)

    # 预加载指南映射：工具 basename -> (指南相对路径, 标题)，用于工具页注入"使用指南"链接
    # 注意：basename 在同一行业外会重名（如 calc-1.html 存在于 42 个行业目录），
    # 仅按 basename 匹配会把「增值税计算使用指南」注入到消防/医疗等无关页面。
    # 因此额外构建「行业/basename」精确映射 GUIDE_MAP_IND，注入时优先命中。
    GUIDE_MAP = {}
    GUIDE_MAP_IND = {}
    GUIDE_INDS = {}          # basename -> set(已确认归属行业)，用于识别跨行业重名
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
                    # 反查指南页正文里指向归属工具页的绝对 URL，得到精确行业归属
                    _gp = os.path.join(ROOT, (_g.get('guide', '') or '').replace('../../', ''))
                    if os.path.isfile(_gp):
                        try:
                            _gs = open(_gp, encoding='utf-8', errors='ignore').read()
                            for _m in re.finditer(
                                r'https://chenguangwu\.github\.io/tools/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+\.html)',
                                    _gs):
                                _gind, _gbase = _m.group(1), _m.group(2)
                                if _gbase == _gt:
                                    GUIDE_MAP_IND[_gind + '/' + _gt] = (_g.get('guide', ''), _title)
                                    GUIDE_INDS.setdefault(_gt, set()).add(_gind)
                                    break
                        except Exception:
                            pass
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

    # 人工策划的「相关工具」覆盖表：tools/ 相对路径 -> 同类工具路径列表。
    # 默认逻辑是按行业随机取前 6 个，会出现「样本量计算器」推荐「提取电话号码」这类无关卡片；
    # 命中本表的页面改用策划列表，按功能/输入输出类型匹配（SEO-C）。
    CURATED_RT = {}
    _crt_path = os.path.join(ROOT, 'json', 'related-tools-curated.json')
    if os.path.isfile(_crt_path):
        try:
            _crt = json.load(open(_crt_path, encoding='utf-8'))
            CURATED_RT = {k: v for k, v in _crt.items() if not k.startswith('_')}
        except Exception:
            CURATED_RT = {}
    # 跨行业引用需要按路径查工具元数据（name/desc/icon）
    _tools_by_path = {t['path']: t for t in tools}
    if existing_html_paths is None:
        existing_html_paths = {
            os.path.normpath(os.path.join(root, filename))
            for root, _, filenames in os.walk(TOOLS_DIR)
            for filename in filenames
            if filename.endswith('.html')
        }
    curated_applied = 0
    curated_missing = []

    fixed_h1 = 0
    fixed_bc = 0
    fixed_rt = 0
    fixed_rt_removed = 0
    fixed_nav = 0
    dropped_crit = 0
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

    def _zh_desc_of(rt):
        # 相关工具卡片描述：贪心取首个含中文候选（与搜索索引/hot-tools 同源修复），
        # 避免中文模式相关工具卡片显示英文 proper-noun（如 "Grace Score"）。
        # 候选优先级：i18n zh-CN.desc > zh-CN.intro > tools.json 自带 desc > 中文名；全无中文才回退英文原名。
        ind = rt.get('industry', 'it')
        base = (rt.get('file') or '').replace('.html', '')
        _zh_title_of(ind, base)            # 确保 i18n 缓存已加载
        zhe = (_ind_cache.get(ind, {}) or {}).get(base, {}) or {}
        zhe = zhe.get('zh-CN', {}) or {}
        for cand in (zhe.get('desc'), zhe.get('intro'), rt.get('desc', ''), rt.get('name', '')):
            if isinstance(cand, str) and _has_cjk(cand):
                return cand
        return rt.get('name', '')

    # 校验/错误提示串特征：这些是 JS 运行时提示，绝不能当 meta description
    # （曾导致 33 个页面 description 变成「误差范围必须 > 0」之类，搜索结果摘要不可读 → 零点击）
    _BAD_DESC_PAT = re.compile(
        r'(^\s*(请输入|请填写|请选择|请检查)|'
        r'必须\s*[>≥＞]|必须\s*[<≤＜]|必须大于|必须小于|必须等于|必须介于|'
        r'必须为正|必须为整数|不能为空|不可为空|不能为负|'
        r'格式错误|格式不正确|输入无效|参数无效|'
        r'至少需要\s*\d|至少\s*\d+\s*(个|位|项|条)|'
        r'个数必须相等|长度必须|超出范围|不在允许范围|'
        r'(值|参数|输入)\s*(有误|无效)$|^\s*(⚠️|❌)|'
        # 游戏/运行时提示文案（如「💰 余额耗尽！点击"重置"重新开始」）
        r'重新开始|点击此处|余额耗尽|游戏结束|再来一次|'
        r'抢跳|答对了|答错了|正确率是|本轮得分|'
        # JS 字符串拼接残留（如「行列式 |A| = '+fmt(d)+'」「第 '+(idx+1)+' 条」）
        r"'\s*\+\s*\(|\)\s*\+\s*'|\+\s*'\s*\+)"
    )

    def _strip_js_blocks(html):
        # 剔除 <script>/<style> 块：其中的字符串常量（错误提示、模板字面量）不是页面正文，
        # 不能被 extract_zh_desc 当作 description 来源。
        return re.sub(r'<(script|style)\b[\s\S]*?</\1\s*>', ' ', html, flags=re.I)

    def extract_zh_desc(content, t, industry, entry):
        # 中文优先 meta description 提取（2026-08-29 反转：目标用户以中文为主）。
        # 优先 per-industry 字典 zh-CN.intro/desc（零成本、有实质内容、不套话），
        # 其次页面首个含中文、非模板、非 JS 校验提示的 <p>，再次中文 h2，兜底中文标题 + 固定后缀。
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
        # 只在剔除 script/style 后的正文里找 <p>，避免抓到 JS 内的错误提示串
        body = _strip_js_blocks(content)
        paras = re.findall(r'<p[^>]*>([\s\S]*?)</p>', body)
        for p in paras:
            txt = re.sub(r'<[^>]+>', '', p).strip()
            txt = re.sub(r'\s+', ' ', txt)
            if '${' in txt or '<' in txt:
                continue
            if _BAD_DESC_PAT.search(txt):
                continue
            if re.search(r'[\u4e00-\u9fff]', txt) and len(txt) >= 8:
                return txt
        h2 = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', body)
        if h2:
            txt = re.sub(r'<[^>]+>', '', h2.group(1)).strip()
            txt = re.sub(r'\s+', ' ', txt)
            if re.search(r'[\u4e00-\u9fff]', txt) and not _BAD_DESC_PAT.search(txt):
                return txt
        zh_title = _zh_title_of(industry, base) or t.get('name') or ''
        return '%s - 免费在线工具，纯前端运行，数据不上传。' % zh_title

    for t in target_tools if target_tools is not None else tools:
        filepath = os.path.join(TOOLS_DIR, t['path'])
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # ------------------------------------------------------------------
        # ToolBox API 桩升级（2026-09-05）
        # 各生成器脚本（scripts/gen_*.py） historically 把「只覆盖 13 个无返回值方法」的旧桩
        # 硬编码进页面（存量 5000+）。页面内联脚本若在顶层调用 escHtml / formatNumber /
        # createTable 这类有返回值的纯函数，会因方法不存在抛 TypeError，整页功能直接不可用。
        # 此处在构建期把旧桩原地升级为含纯函数早期实现的新桩。
        # 注意：必须放在 `original = content` 之后——只有 content != original 才会写回磁盘。
        # 幂等：新桩自带 T.escHtml 指纹，已升级页面直接返回原内容。
        # ------------------------------------------------------------------
        original = content
        content = _upgrade_toolbox_api_stub(content)

        industry = t['industry']
        ind_def = INDUSTRY_DEFS.get(industry, ('🗂️', industry))
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
        else:
            # 已存在面包屑：刷新行业图标（根治历史 🔧 面包屑——行业图标已修正但旧面包屑因幂等跳过未更新）
            content = _refresh_breadcrumb_icon(content, ind_icon)

        # 2.3 工具页自身图标规范化：把 meta / h2 / 按钮 / JS 结果标题的旧图标写成语义推导图标。
        # （相关工具卡 rt-icon 不在此处理，由下方相关工具块刷新；图标位不含正文装饰性 emoji）
        _new_tool_icon = t.get('icon')
        _old_tool_icon = t.get('_meta_icon') or ''
        if _new_tool_icon and _old_tool_icon and _old_tool_icon != _new_tool_icon:
            content, _ni_hits = normalize_tool_icon_in_page(content, _old_tool_icon, _new_tool_icon)

        # 2.5 Add "使用指南" link (idempotent via data-guide-link)
        if 'data-guide-link' not in content:
            _tb = os.path.basename(t['path'])
            # 优先用「行业/basename」精确命中；若该 basename 已确认归属别的行业
            # （如 calc-1.html 属于 accounting），则不得回退到 basename 全局匹配，
            # 否则会把「增值税计算使用指南」注入消防 / 医疗等无关页面。
            _gitem = GUIDE_MAP_IND.get(industry + '/' + _tb)
            if not _gitem and _tb not in GUIDE_INDS:
                _gitem = GUIDE_MAP.get(_tb)
            if _gitem:
                _g_url, _g_title = _gitem
                if _g_url:
                    _g_title_esc = esc_html_py(_g_title)
                    gl_html = '\n<div class="tool-guide-link" data-guide-link="1">\n  <a href="%s">📖 查看「%s」</a>\n</div>\n' % (_g_url, _g_title_esc)
                    if '<div class="container' in content:
                        # 前缀匹配以兼容 V2 模板的 '<div class="container xxx">'（如 cb-wrap）
                        _cidx = content.find('<div class="container')
                        _cend = content.find('>', _cidx) + 1
                        content = content[:_cend] + gl_html + content[_cend:]
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

        # Ensure tool runtime script is loaded, while preserving compatibility with old inline bootstrap blocks.
        if not _head_contains(content, '/js/tool-page-runtime.js'):
            replaced = False
            if '<!-- toolbox-theme-bootstrap -->' in content and '<!-- toolbox-sw-register -->' in content:
                content, n = old_marker_pattern.subn(runtime_block, content, count=1)
                if n:
                    replaced = True
            if not replaced:
                content = _inject_into_document_head(content, runtime_block)

        # 3.5b Add generic tool UX enhancement (copy/download bar, validation hint, input persistence, a11y)
        # 注：实际注入移到下方「写回前」(2337 附近)，因为在 2079–2336 的 head 重写流程里
        # 早注入的 <script> 会被覆盖；放最后一步注入可保证落盘且幂等。

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
        # 中文优先：JSON-LD description 与 meta 描述同源取中文（extract_zh_desc），
        # 避免中文模式页面结构化数据里塞英文 t['desc']（与 meta/og 描述保持一致）
        app_desc = esc_html_py((extract_zh_desc(content, t, industry, entry) or t['name'])[:150])
        app_json_block = '\n<!-- TOOLBOX-WEBAPP-LD -->\n<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"WebApplication","name":"%s","url":"https://chenguangwu.github.io/%s","applicationCategory":"%s","operatingSystem":"Any","browserRequirements":"Requires JavaScript","inLanguage":%s,"description":"%s","image":"https://chenguangwu.github.io/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}\n</script>' % (tool_name_esc, t['url'], app_cat, json.dumps(I18N_LOCALES, ensure_ascii=False), app_desc)

        def _replace_webapp_ld(src):
            # 注意：标记注释位于 <script> 之外，必须一并纳入匹配范围，
            # 否则旧注释会被留在原地、每次构建再插一个新注释（历史累积过 14 个）。
            # 前后换行统一归一，保证多次构建结果完全一致（幂等）。
            pattern = re.compile(
                r'(?:<!--\s*TOOLBOX-WEBAPP-LD\s*-->\s*)*'
                r'<script type="application/ld\+json">.*?</script>', re.S)
            matches = [
                match for match in pattern.finditer(src)
                if '"@type":"WebApplication"' in match.group(0)
            ]
            if not matches:
                return src, False

            # Remove all historical duplicates from the end, then put exactly
            # one normalized block back at the first block's original position.
            insert_at = matches[0].start()
            updated = src
            for index, match in reversed(list(enumerate(matches))):
                start = match.start()
                if index > 0 and start > 0 and updated[start - 1] == '\n':
                    start -= 1
                updated = updated[:start] + updated[match.end():]
            head = updated[:insert_at].rstrip('\n')
            tail = updated[insert_at:].lstrip('\n')
            return head + app_json_block + '\n' + tail, True

        content, app_ld_found = _replace_webapp_ld(content)
        if not app_ld_found:
            content = content.replace('</head>', app_json_block + '\n</head>', 1)

        # 4. Add og:image / twitter:image (idempotent)
        if 'og:image' not in content:
            image_meta = '\n<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">\n<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">\n<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">\n'
            content = content.replace('</head>', image_meta + '</head>', 1)

        # 4.0 中文优先 <title>（2026-08-29 反转：目标用户以中文为主）。
        # 初始 <title> 渲染为中文（per-industry 字典 zh-CN.title 或中文名），英文标题存
        # <meta name="title-en"> 供前端 en-US 模式切回（见 js/i18n.js syncTitle）。
        # og:title / twitter:title 跟随中文。注意：title-en 注入到 I18N_HREFLANG_MARKER 之前，
        # 否则 inject_hreflang 会截断 marker→</head> 间内容导致丢失（已踩坑修复）。
        _seo_slug = _slug_of(t)
        _seo_override = EN_OVERRIDE.get(_seo_slug, {})
        _en_t = _seo_override.get('en')
        _en_desc = _clean_en_desc(_seo_override.get('ed') or '')
        _m_t = re.search(r'<title>([^<]*)</title>', content) if _en_t else None
        _obsolete_meta_names = []
        if _m_t:
            _obsolete_meta_names.extend(('title-zh', 'title-en'))
        if _en_desc:
            _obsolete_meta_names.append('desc-en')
        if _obsolete_meta_names:
            content = _sub_in_document_head(
                r'[ \t]*<meta name="(?:%s)" content="[^"]*">[ \t]*\n?'
                % '|'.join(_obsolete_meta_names), '', content)

        if _en_t:
            if _m_t:
                _base = os.path.splitext(os.path.basename(t['path']))[0]
                _zh_title = _zh_title_of(industry, _base) or t.get('name') or tool_name_esc
                # 标题只显示工具名，不再追加「 - ToolBox」品牌后缀（老板要求）；
                # 同时幂等剥离可能残留的「（免费）」「免费在线工具」「 - ToolBox / | ToolBox」。
                _zh_t = _zh_title.replace('（免费）', '').replace('免费在线工具', '').replace(' - ToolBox', '').replace(' | ToolBox', '').strip()
                _en_full = _en_t.replace('（免费）', '').replace('免费在线工具', '').replace(' - ToolBox', '').replace(' | ToolBox', '').strip() if _en_t else _zh_t
                # 初始 title 渲染中文（中文优先）
                content = content.replace(_m_t.group(0), '<title>%s</title>' % esc_once(_zh_t), 1)
                # 旧 title-zh/title-en/desc-en 已在一次 head 扫描中统一清理。
                _en_meta = '<meta name="title-en" content="%s">' % esc_once(_en_full)
                if I18N_HREFLANG_MARKER in content:
                    content = content.replace(I18N_HREFLANG_MARKER, _en_meta + '\n' + I18N_HREFLANG_MARKER, 1)
                else:
                    content = content.replace('</head>', _en_meta + '\n</head>', 1)
                # og:title / twitter:title 跟随中文（纯工具名）
                _og_t = esc_once(_zh_t)
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
        # 5a. 策划表命中：先整块移除旧的（可能是行业随机凑的无关卡片），再按策划列表重建
        _curated = CURATED_RT.get(t['path'])
        if _curated:
            _valid = []
            for _p in _curated:
                if _p == t['path']:
                    continue
                if _p not in _tools_by_path:
                    curated_missing.append('%s -> %s' % (t['path'], _p))
                    continue
                _valid.append(_tools_by_path[_p])
            if _valid:
                content = _rt_block_pat.sub('', content)
                rt_html = '<!-- 相关工具 -->\n<div class="related-tools" data-related-tools="1">\n  <h3 class="related-tools-title">🔗 相关工具</h3>\n  <div class="related-tools-grid">\n'
                rt_tool_dir = 'tools/' + os.path.dirname(t['path'])
                for rt in _valid:
                    rt_name = esc_html_py(rt['name'])
                    rt_desc = esc_html_py(_zh_desc_of(rt))[:50]
                    rt_icon = rt.get('icon', '🛠️')
                    rt_href = os.path.relpath(rt['url'], rt_tool_dir).replace(os.sep, '/')
                    rt_html += '    <a href="%s" class="related-tool-card">\n      <span class="rt-icon">%s</span>\n      <span class="rt-info"><span class="rt-name">%s</span><span class="rt-desc">%s</span></span>\n    </a>\n' % (rt_href, rt_icon, rt_name, rt_desc)
                rt_html += '  </div>\n</div>\n'
                if '<div class="tool-intro' in content:
                    content = content.replace('<div class="tool-intro', rt_html + '<div class="tool-intro', 1)
                elif '<!-- /注意事项区块 -->' in content:
                    content = content.replace('<!-- /注意事项区块 -->', '<!-- /注意事项区块 -->\n' + rt_html, 1)
                elif '</div>\n</div>\n<script>' in content:
                    content = content.replace('</div>\n</div>\n<script>', '</div>\n</div>\n' + rt_html + '<script>', 1)
                else:
                    content = content.replace('</body>', rt_html + '</body>', 1)
                curated_applied += 1

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
                if _target in existing_html_paths:
                    # 刷新 rt-icon 为当前语义图标（根治历史 🔧 / 行业图标残留；幂等）。
                    # _target 相对 ROOT（tools/<industry>/<file>.html），而 _tools_by_path 的 key
                    # 相对 TOOLS_DIR（<industry>/<file>.html），需去掉 tools/ 前缀再查。
                    _rel_target = os.path.relpath(_target, TOOLS_DIR)
                    _rt_obj = _tools_by_path.get(_rel_target)
                    if _rt_obj:
                        _cur_icon = _rt_obj.get('icon')
                        if _cur_icon:
                            _a = re.sub(r'(<span class="rt-icon">)[^<]*(?=</span>)', r'\g<1>' + _cur_icon, _a, count=1)
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
                rt_html = '<!-- 相关工具 -->\n<div class="related-tools" data-related-tools="1">\n  <h3 class="related-tools-title">🔗 相关工具</h3>\n  <div class="related-tools-grid">\n'
                rt_tool_dir = 'tools/' + os.path.dirname(t['path'])
                for rt in related:
                    rt_name = esc_html_py(rt['name'])
                    rt_desc = esc_html_py(_zh_desc_of(rt))[:50]
                    rt_icon = rt.get('icon', '🛠️')
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
            _dd_html = _build_deep_dive_html(DEEP_DIVE[_seo_slug])
            # 绝大多数构建中配置与已提交 HTML 完全一致。先做快速精确
            # 命中，避免对约 5000 个完整页面反复执行三次删除正则再原样插回。
            if _dd_html and _dd_html not in content:
                # 用 lambda 作为 repl，避免 re.sub 把 deep-dive 内容里的反斜杠
                # 当作转义模板（如 \d、\n、\$ 等合法字符会触发 bad escape）。
                content, _dd_replaced = _DEEP_DIVE_BLOCK_RE.subn(
                    lambda m: _dd_html, content, count=1)
                if not _dd_replaced:
                    # 兼容 marker 缺失或旧版残片，保留原来的清理语义。
                    content = re.sub(r'<!-- TOOLBOX-DEEP-DIVE -->\s*', '', content)
                    content = re.sub(r'<style>\s*\.deep-dive[\s\S]*?</style>\s*', '', content)
                    content = re.sub(r'<section class="deep-dive"[^>]*>[\s\S]*?</section>\s*', '', content)
                    if '<!-- 注意事项区块 -->' in content:
                        _anchor = '<!-- 注意事项区块 -->'
                    elif '<!-- 相关工具 -->' in content:
                        _anchor = '<!-- 相关工具 -->'
                    else:
                        _anchor = '</body>'
                    if _anchor in content:
                        content = content.replace(_anchor, _dd_html + '\n' + _anchor, 1)

        # 7. 注入 critical CSS + 全站 2 级分类导航资源（幂等）。
        #    - common.css 保持阻塞，确保统一顶部搜索框不会无样式闪烁；
        #    - critical CSS 内联（common.css 首屏外壳子集），弱网首访立即可见、防 FOUC；
        #    - 以上两项与 nav-menu 注入解耦：nav-menu 仅在未注入时执行，
        #      critical/common.css 每次都按幂等规则处理，避免二次 build 因已含 nav-menu.js 被跳过。
        # 仅 nav-menu.css 阻塞 link → 非阻塞 preload + noscript 兜底。
        # 必须用 _css_nonblocking（先 stash 所有 <noscript> 回退块再替换块外阻塞 link），
        # 切勿用裸 re.sub：二次 build 时裸 re.sub 会再次匹配 noscript 内部的回退 stylesheet，
        # 嵌套 <noscript> 破坏结构（build13 曾因此损坏 4993 页）。
        content = _css_nonblocking(content)
        # critical CSS 瘦身（2026-09-05）：实测 scripts/critical_tool_css.txt 的 178 条选择器
        # 100% 被 css/common.css + css/nav-menu.css 覆盖，零条独有；且 _css_nonblocking()
        # 只把 nav-menu.css 改非阻塞、common.css 保持阻塞，首次渲染前必生效，删除无 FOUC 风险。
        # 故凡引用 common.css 的页面一律移除内联副本（每页省约 23KB，全站约 132MB）；
        # 未引用 common.css 的页面（ui/ 设计稿、重定向桩等）仍注入，作为兜底。
        # 幂等：二次 build 时已无 critical-css，'common.css' 分支自然跳过，不会重复删除。
        if 'common.css' in content:
            if 'id="critical-css"' in content:
                content = re.sub(
                    r'<style id="critical-css">[\s\S]*?</style>\s*', '', content, count=1)
                dropped_crit += 1
        elif ('id="critical-css"' not in content and CRITICAL_TOOL_CSS
              and '</head>' in content):
            _crit = '<style id="critical-css">\n%s\n</style>\n' % CRITICAL_TOOL_CSS
            content = content.replace('</head>', _crit + '</head>', 1)
        if 'js/nav-menu.js' not in content:
            nav_inject = (
                '<link rel="preload" as="style" href="/css/nav-menu.css" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
                '<noscript><link rel="stylesheet" href="/css/nav-menu.css"></noscript>\n'
                '<script src="/js/industry-info.js" defer></script>\n'
                '<script src="/js/nav-menu.js" defer></script>\n'
            )
            if '</head>' in content:
                content = content.replace('</head>', nav_inject + '</head>', 1)
                fixed_nav += 1

        # 3.5b Add generic tool UX enhancement (copy/download bar, validation hint, input persistence, a11y)
        ux_block = '\n<script src="/js/tool-ux.js" defer></script>\n<!-- TOOLBOX-TOOL-UX -->\n'
        if not _head_contains(content, '/js/tool-ux.js'):
            content = _inject_into_document_head(content, ux_block)

        # The editorial popular set gets a shared productivity layer. Keeping
        # the membership in gen_hot_tools.py makes homepage cards and page UX
        # impossible to drift apart.
        hot_ux_block = '\n<script src="/js/hot-tool-enhancements.js" defer></script>\n<!-- TOOLBOX-HOT-TOOL-UX -->\n'
        hot_ux_pattern = re.compile(
            r'\s*<script src="/js/hot-tool-enhancements\.js" defer></script>\s*'
            r'<!-- TOOLBOX-HOT-TOOL-UX -->\s*'
        )
        if t['url'] in HOT_TOOL_URL_SET:
            if not _head_contains(content, '/js/hot-tool-enhancements.js'):
                content = _inject_into_document_head(content, hot_ux_block)
        elif 'TOOLBOX-HOT-TOOL-UX' in content:
            content = hot_ux_pattern.sub('\n', content, count=1)

        # Keep analytics last so hreflang normalization cannot discard it.
        if not _head_contains(content, '/js/analytics.js'):
            content = _inject_into_document_head(content, clarity_block)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    result = {
        'fixed_h1': fixed_h1,
        'fixed_bc': fixed_bc,
        'fixed_rt': fixed_rt,
        'fixed_rt_removed': fixed_rt_removed,
        'fixed_nav': fixed_nav,
        'dropped_crit': dropped_crit,
        'curated_applied': curated_applied,
        'curated_missing': curated_missing,
        'curated_config': len(CURATED_RT),
    }
    if report:
        _report_tool_seo_result(result)
    return result


def _report_tool_seo_result(result):
    print('  h1 added: %d, breadcrumbs: %d, related tools: %d (recomputed), removed stale blocks: %d, nav injected: %d' %
          (result['fixed_h1'], result['fixed_bc'], result['fixed_rt'],
           result['fixed_rt_removed'], result['fixed_nav']))
    if result.get('dropped_crit'):
        print('  critical-css removed (redundant with common.css): %d pages' %
              result['dropped_crit'])
    if result['curated_config']:
        print('  curated related-tools: %d applied (config: %d)' %
              (result['curated_applied'], result['curated_config']))
        if result['curated_missing']:
            print('  [WARN] 策划表指向了不存在的工具（已跳过）:')
            for message in result['curated_missing'][:20]:
                print('    - ' + message)


def fix_tool_pages_seo_parallel(tools):
    """Rewrite distinct tool files concurrently while preserving stage order."""
    workers = _configured_build_workers(len(tools))
    if workers == 1:
        return fix_tool_pages_seo(tools)

    i18n_dir = os.path.join(ROOT, 'i18n', 'tools')
    for industry in {tool['industry'] for tool in tools}:
        _load_tool_body_file(i18n_dir, industry)
    existing_html_paths = {
        os.path.normpath(os.path.join(root, filename))
        for root, _, filenames in os.walk(TOOLS_DIR)
        for filename in filenames
        if filename.endswith('.html')
    }
    chunks = _round_robin_chunks(tools, workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                fix_tool_pages_seo, tools, chunk, False, existing_html_paths)
            for chunk in chunks
        ]
        results = [future.result() for future in futures]

    combined = {
        'fixed_h1': sum(item['fixed_h1'] for item in results),
        'fixed_bc': sum(item['fixed_bc'] for item in results),
        'fixed_rt': sum(item['fixed_rt'] for item in results),
        'fixed_rt_removed': sum(item['fixed_rt_removed'] for item in results),
        'fixed_nav': sum(item['fixed_nav'] for item in results),
        'dropped_crit': sum(item['dropped_crit'] for item in results),
        'curated_applied': sum(item['curated_applied'] for item in results),
        'curated_missing': [message for item in results for message in item['curated_missing']],
        'curated_config': max(item['curated_config'] for item in results),
    }
    _report_tool_seo_result(combined)
    print('  parallel workers: %d' % workers)
    return combined

# 行业聚合页 meta description 覆盖（仅影响列出的行业；工具数为动态带入，避免下次 build 被模板覆盖）
CATEGORY_DESC_OVERRIDE = {
    'home': 'Home and Renovation tools: %d free online tools for room area, material estimates and renovation planning. Browse and use instantly—client-side, no upload.',
    'embedded': 'Embedded Systems tools: %d free online tool for bit, register and protocol calculations. Browse and use it instantly—client-side, no upload, no install.',
    'telecom': 'Telecommunications tools collection with %d free online tools for signal, RF and network calculations. Browse and launch instantly—client-side, no upload.',
}


def _has_cjk(s):
    """返回字符串是否含中日韩（中文）字符，用于判定工具名/描述的语言。

    实现委托 scripts/tool_desc_source.py —— 全站（分类页/搜索/首页/导航）共用一份，
    避免两份实现各自漂移导致描述又不一致。
    """
    return TDS.has_cjk(s)


def _is_weak_desc(desc, title):
    """判定中文描述是否只是标题重复或缺乏信息量，需要从 intro 取长描述。

    实现委托 scripts/tool_desc_source.py（同 _has_cjk）。
    """
    return TDS.is_weak_desc(desc, title)


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
        _nm = INDUSTRY_DEFS.get(_ind, ('🗂️', _ind))[1]
        name_to_inds.setdefault(_nm, set()).add(_ind)

    for ind, ind_tools in by_industry.items():
        ind_def = INDUSTRY_DEFS.get(ind, ('🗂️', ind))
        ind_icon, ind_name = ind_def[0], ind_def[1]
        ind_dir = os.path.join(TOOLS_DIR, ind)
        os.makedirs(ind_dir, exist_ok=True)

        ind_tools_sorted = sorted(ind_tools, key=hot_sort_key)
        count = len(ind_tools_sorted)
        en_name = _IND_EN.get(ind, ind_name)
        # 自动差异化 SEO 内容（scripts/category_auto_content.py）：基于该行业真实工具列表
        # 生成独一无二的 title / 中英文 description / 正文（栏目简介 + 核心功能 + FAQ）。
        # 全站 268 个分类页因此不再互为重复内容（修复 GSC 报的 Thin Content）。
        _names = [t['name'] for t in ind_tools_sorted]
        # 英文工具名列表：供分类页正文（.t-en 层）与英文 description 使用
        _names_en = [(t.get('en') or t['name']) for t in ind_tools_sorted]
        _seo = CAUTO.build_content(ind, ind_name, en_name, count, _names, _names_en)
        title = ('%s (%s) Tools Collection - ToolBox' % (en_name, ind)) if len(name_to_inds.get(ind_name, set())) > 1 else ('%s Tools Collection - ToolBox' % en_name)
        title_zh = _seo['title_zh']
        desc_meta = _seo['desc_en']
        desc_meta_zh = _seo['desc_zh']

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
        parts.append('<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">\n')
        parts.append('<meta name="twitter:card" content="summary_large_image">\n')
        parts.append('<meta name="twitter:title" content="%s">\n' % esc_html_py(title_zh))
        parts.append('<meta name="twitter:description" content="%s">\n' % esc_html_py(desc_meta_zh))
        parts.append('<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">\n')
        parts.append('<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">\n')
        parts.append('<title>%s</title>\n' % esc_html_py(title_zh))
        parts.append('<link rel="canonical" href="https://chenguangwu.github.io/tools/%s/index.html">\n' % ind)
        parts.append('<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n')
        # critical CSS 不再内联：其规则 100% 被下方阻塞加载的 common.css 覆盖（详见 2804 行注释）。
        parts.append('<link rel="stylesheet" href="../../css/common.css">\n')
        if '/js/analytics.js' not in ''.join(parts):
            parts.append('<script src="/js/analytics.js" defer></script>\n')
            parts.append(CLARITY_MARKER + '\n')
        parts.append(TOOLBOX_API_STUB)
        parts.append('<script src="../../js/common.js" defer></script>\n')
        parts.append('<script src="/js/tool-page-runtime.js" defer></script>\n')
        parts.append(TOOL_RUNTIME_MARKER + '\n')
        parts.append('<script src="../../js/i18n.js" defer></script>\n')
        parts.append('<script src="../../js/tool-i18n.js" defer></script>\n')
        # 全站 2 级分类导航（顶部菜单 + 下拉面板 + 移动抽屉）
        parts.append('<link rel="preload" as="style" href="/css/nav-menu.css" onload="this.onload=null;this.rel=\'stylesheet\'">\n')
        parts.append('<noscript><link rel="stylesheet" href="/css/nav-menu.css"></noscript>\n')
        parts.append('<script src="/js/industry-info.js" defer></script>\n')
        parts.append('<script src="/js/nav-menu.js" defer></script>\n')
        parts.append('<script src="/js/category-index.js" defer></script>\n')
        # 多语言 SEO：hreflang + og:locale（构建期常量，批次4）
        parts.append(build_hreflang_block('https://chenguangwu.github.io/tools/%s/index.html' % ind))
        # CollectionPage structured data
        parts.append('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"CollectionPage","name":"%s工具","url":"https://chenguangwu.github.io/tools/%s/index.html","description":"%s"}\n</script>\n' % (esc_html_py(ind_name), ind, esc_html_py(desc_meta_zh)))
        # BreadcrumbList structured data
        parts.append('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"},{"@type":"ListItem","position":2,"name":"%s","item":"https://chenguangwu.github.io/tools/%s/index.html"}]}\n</script>\n' % (esc_html_py(ind_name), ind))
        # FAQPage 结构化数据：与页面可见 FAQ 文本一致，强化索引信号（全站覆盖）
        parts.append(CAUTO.faq_ld(_seo, count))
        parts.append('</head>\n<body>\n')
        parts.append('<h1 class="sr-only tb-bi"><span class="t-zh">%s %s工具</span><span class="t-en">%s %s Tools</span></h1>\n' % (ind_icon, esc_html_py(ind_name), ind_icon, esc_html_py(en_name)))
        # Breadcrumb
        parts.append('<nav class="breadcrumb" aria-label="面包屑导航">\n  <a href="../../index.html" data-i18n="bc.home" data-i18n-fb="首页">首页</a>\n  <span class="bc-sep">‹</span>\n  <span class="bc-current tb-bi">%s <span class="t-zh">%s</span><span class="t-en">%s</span></span>\n</nav>\n' % (ind_icon, esc_html_py(ind_name), esc_html_py(en_name)))
        # Nav
        parts.append('<div class="nav">\n  <a href="../../index.html">← ToolBox</a>\n  <span class="tb-bi">/ <span class="t-zh">%s工具</span><span class="t-en">%s Tools</span></span>\n  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>\n</div>\n' % (esc_html_py(ind_name), esc_html_py(en_name)))
        # Content
        parts.append('<div class="container">\n  <div class="card">\n')
        parts.append('    <h2 class="tb-bi">%s <span class="t-zh">%s工具</span><span class="t-en">%s %s Tools</span></h2>\n' % (ind_icon, esc_html_py(ind_name), ind_icon, esc_html_py(en_name)))
        parts.append('    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;"><span data-i18n="cat.total_prefix" data-i18n-fb="共">共</span> %d<span data-i18n="cat.total_suffix" data-i18n-fb="个免费在线工具">个免费在线工具</span></p>\n' % count)
        parts.append('    <div class="category-tool-list" data-ind="%s">\n' % ind)
        index_ref_dir = 'tools/' + ind
        # 加载本行业中文 i18n 字典，供分类页卡片 .t-zh 描述使用
        i18n_path = os.path.join(ROOT, 'i18n', 'tools', '%s.json' % ind)
        ind_i18n = json.load(open(i18n_path, encoding='utf-8')) if os.path.exists(i18n_path) else {}

        for t in ind_tools_sorted:
            # 精简静态链接：仅内联 href + 中文名 + 中文描述（SEO 锚文本与可见描述，繁体页由 OpenCC 自动转繁体）；
            # 图标/英文名/英文描述由 js/category-index.js 运行时 fetch json/industry-<ind>.json 增强，
            # 避免每个行业把全部工具卡片（含英文描述长文本）内联进 HTML（原每卡 ~580B，现 ~200B，省约 65%）。
            _zh_name = TDS.slug_name(t)
            # 统一走权威描述源（与 tools.json 的 d、顶部导航卡片同源），
            # 保证分类页 / 搜索 / 首页 / 导航四处展示的描述完全一致
            _zh_desc = TDS.zh_desc(t, max_len=100)
            if _is_weak_desc(_zh_desc, _zh_name):         # 仍弱 → 回退中文名
                _zh_desc = _zh_name
            tool_href = os.path.relpath(t['url'], index_ref_dir).replace(os.sep, '/')
            parts.append('      <a href="%s" class="cat-tool"><span class="t-zh">%s</span><span class="t-zh-desc">%s</span></a>\n' % (tool_href, esc_html_py(_zh_name), esc_html_py(_zh_desc)))
        parts.append('    </div>\n  </div>\n')
        # SEO intro
        parts.append('  <div class="tool-intro open">\n    <div class="tool-intro-header"><span class="intro-icon-wrap"><span class="intro-icon">📖</span><span class="t-zh">关于「%s工具」</span><span class="t-en">About %s Tools</span></span><span class="arrow">▼</span></div>\n' % (esc_html_py(ind_name), esc_html_py(en_name)))
        parts.append('    <div class="tool-intro-body">\n')
        # 差异化正文：栏目简介 + 核心功能与适用场景 + 常见问题（全站自动生成）
        parts.append(CAUTO.render_body(_seo, count))
        parts.append('    </div>\n  </div>\n')
        parts.append('</div>\n')
        parts.append('</body>\n</html>\n')

        index_path = os.path.join(ind_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(''.join(parts))

    print('  Generated %d category index pages' % len(by_industry))
    return list(by_industry.keys())


def fix_hot_tools_desc():
    """首页热门工具 json/hot-tools.json 的 d(中文描述) 字段，在多个候选里优先取「含中文」者，
    避免中文模式热门卡片显示英文描述（与 generate_split_jsons 搜索索引的 d 字段同源修复）。
    候选优先级：i18n zh-CN.desc > zh-CN.intro > tools.json 自带 desc > 中文名(n)；
    仅当全部无中文时才回退英文原名。分析字段(imp/clk/ctr/pos)与 en/ed 保持不变。幂等。"""
    hp = os.path.join(ROOT, 'json', 'hot-tools.json')
    if not os.path.isfile(hp):
        return
    try:
        hot = json.load(open(hp, encoding='utf-8'))
    except Exception:
        return
    if not isinstance(hot, list):
        return
    # tools.json 自带 desc（按 url 索引），作为候选源之一
    tmap = {}
    try:
        for t in json.load(open(TOOLS_JSON_FILE, encoding='utf-8')):
            tmap[t.get('url', '')] = t
    except Exception:
        pass
    _i18n_cache = {}
    def _load_ind_i18n(ind):
        if ind not in _i18n_cache:
            fp = os.path.join(ROOT, 'i18n', 'tools', ind + '.json')
            try:
                _i18n_cache[ind] = json.load(open(fp, encoding='utf-8')) if os.path.isfile(fp) else {}
            except Exception:
                _i18n_cache[ind] = {}
        return _i18n_cache[ind]
    changed = 0
    for t in hot:
        if not isinstance(t, dict):
            continue
        u = t.get('u', '')
        slug = u.split('/')[-1].replace('.html', '')
        ind = t.get('i', 'it')
        zh = (_load_ind_i18n(ind).get(slug, {}) or {}).get('zh-CN', {}) or {}
        tools_desc = (tmap.get(u, {}) or {}).get('desc', '') or ''
        _d = ''
        for cand in (zh.get('desc'), zh.get('intro'), tools_desc, t.get('n', '')):
            if isinstance(cand, str) and _has_cjk(cand):
                _d = cand[:80] + ('…' if len(cand) > 80 else '')
                break
        if not _d:
            _d = t.get('n', '')
        if _d and _d != t.get('d', ''):
            t['d'] = _d
            changed += 1
    if changed:
        with open(hp, 'w', encoding='utf-8') as f:
            json.dump(hot, f, ensure_ascii=False, indent=2)
        print('Fixed %d hot-tools.json descriptions (d -> Chinese)' % changed)
    else:
        print('hot-tools.json descriptions already Chinese (%d entries)' % len(hot))


def generate_hot_tools():
    """Build the curated homepage hot-tool list from the fresh tools index."""
    script = os.path.join(ROOT, 'scripts', 'gen_hot_tools.py')
    print('\nGenerating curated hot tools:')
    try:
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit('Hot tools build failed: %s' % exc)


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

    # Quality classification needs the shared-script set. Build it once before
    # metadata workers start so no thread races the lazy global initialization.
    build_shared_script_index()
    workers = _configured_build_workers(len(files))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        tools = [info for info in executor.map(get_tool_info, files) if info]
    print('Parsed tool metadata with %d workers' % workers)

    # Sort: by category order then name
    cat_order = ['dev','encode','text','generate','convert','math','calculator','design','image',
                 'finance','health','engineer','edu','legal','music','photo','travel','marketing',
                 'validator','reference','life','game']
    tools.sort(key=lambda t: (cat_order.index(t['cat']) if t['cat'] in cat_order else 99, t['name']))

    # 工具图标语义化重分配（2026-09-12）：按工具名推导专属图标并在行业内部均衡去重，
    # 根治「同行业工具图标清一色」「工具图标不合适」两类问题。人工专属图标（_icon_keep）
    # 已在上游 get_tool_info 保留，此处只重分配历史占位（行业 emoji / 🔧）。
    assign_tool_icons(tools, verbose=True)

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
        # 先应用英文名称覆盖（EN_OVERRIDE 预翻），确保 en_desc 用「可靠的英文名」削前缀；
        # 否则未收录词回退中文名当 name_en，会漏削英文描述前缀 → 主循环与 split 两次
        # en_desc 结果不同（一个带名、一个被削名），三端 ed 不一致
        apply_en_override(t)
        # ed 统一为 TDS.en_desc（覆盖历史生成器套话，与分类页/导航单一权威源一致）
        t['ed'] = TDS.en_desc(t, max_len=60)
        t['d'] = compute_zh_desc(t)   # 治本：补中文 d，确保 tools.json 与 industry-*.json 同源一致
        # 合并 search-index.json：把搜索专用字段并入 tools.json（单一数据源，删 search-index.json）。
        # al=别名、py=拼音、pyi=拼音首字母，支撑前端 Fuse.js + 滑动窗口拼音 typo 纠错。
        if 'al' not in t:
            t['al'] = build_search_aliases(t)
        if 'py' not in t:
            t['py'] = title_pinyin(t.get('name', ''))
        if 'pyi' not in t:
            t['pyi'] = title_pinyin_initials(t.get('name', ''))
        # 热度分：统一在 main() 计算并持久化到 tools.json（见顶部热度排序模型说明）。
        # 新增工具自动获得 hot，全站按 hot 降序排序，无需在各生成函数里重复算。
        if 'hot' not in t:
            t['hot'] = compute_hot(t)

    # Save tools.json to json/ directory
    os.makedirs(os.path.dirname(TOOLS_JSON_FILE), exist_ok=True)
    with open(TOOLS_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    print('Saved json/tools.json (%d entries)' % len(tools))

    # Remove the historical root duplicate. Runtime and maintained scripts use
    # json/tools.json; keeping both added a multi-megabyte diff to every build.
    tools_json_root = os.path.join(ROOT, 'tools.json')
    if os.path.exists(tools_json_root):
        os.remove(tools_json_root)
        print('Removed legacy root tools.json duplicate')
    
    # Generate split JSON files (per industry + search index)
    print('\nGenerating split JSON files:')
    generate_split_jsons(tools)

    # 生成 phrases 索引（有数据的行业清单，供 tool-i18n 按需加载，避免对缺失行业发 404 请求）
    sync_phrases_index()

    # SEO: Fix tool pages (h1, breadcrumbs, related tools, structured data)
    print('\nFixing tool pages SEO:')
    fix_tool_pages_seo_parallel(tools)

    # SEO: Generate category index pages
    print('\nGenerating category index pages:')
    category_inds = generate_category_indexes(tools)

    # 生成 2 级分类导航数据：js/industry-info.js + json/industry-groups.json
    print('\nGenerating 2-level navigation data:')
    import subprocess as _sp
    _sp.run([sys.executable, os.path.join(ROOT, 'scripts', 'gen_industry_info.py')], check=True)
    _sp.run([sys.executable, os.path.join(ROOT, 'scripts', 'gen_industry_groups.py')], check=True)

    # Update index.html (just update counts and metadata, tools array removed)
    if update_index_html(INDEX_FILE, tools_js, len(tools), cat_counts, ind_counts):
        print('Updated index.html')

    # Inject og:image / twitter:image into index.html if missing (idempotent)
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx_html = f.read()
    if 'og:image' not in idx_html:
        image_meta = '<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">\n<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">\n<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">\n'
        idx_html = idx_html.replace('<meta property="og:type" content="website">',
                                    '<meta property="og:type" content="website">\n' + image_meta, 1)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(idx_html)
        print('Injected og:image / twitter:image into index.html')

    # 多语言 SEO：首页注入 hreflang + og:locale（构建期常量，幂等，批次4）
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx_html = f.read()
    new_idx_html = inject_hreflang(idx_html, 'https://chenguangwu.github.io/')
    if new_idx_html != idx_html:
        idx_html = new_idx_html
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(idx_html)
        print('Updated hreflang in index.html')

    # Generate one root sitemap. Per-industry sitemap files duplicated the same
    # URLs and added hundreds of generated files to every build and commit.
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
    if os.path.isfile(os.path.join(ROOT, 'about.html')):
        all_urls.append('https://chenguangwu.github.io/about.html')
    for t in tools:
        all_urls.append('https://chenguangwu.github.io/' + t['url'])
    global _LASTMOD_MAP
    _LASTMOD_MAP = ensure_lastmod_map(all_urls, today)

    removed_industry_sitemaps = 0
    for ind in os.listdir(TOOLS_DIR):
        stale_sitemap = os.path.join(TOOLS_DIR, ind, 'sitemap.xml')
        if os.path.isfile(stale_sitemap):
            os.remove(stale_sitemap)
            removed_industry_sitemaps += 1

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(generate_sitemap(tools, category_inds))
    print('Generated compact root sitemap.xml (full urlset: %d tools + %d categories + guides); removed %d industry sitemaps'
          % (len(tools), len(category_inds), removed_industry_sitemaps))
    
    # Generate HTML sitemap
    html_sitemap = generate_html_sitemap(tools)
    with open(HTML_SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(html_sitemap)
    print('Generated sitemap.html (%d tools)' % len(tools))

    # 热门清单依赖刚生成的 tools.json；描述归一化后再同步至繁体静态站。
    generate_hot_tools()
    fix_hot_tools_desc()

    # 只在源页面、JSON 与 sitemap 都已完成后生成繁体静态站，避免复制中间产物。
    generate_opencc_static_locales()

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
    # 全站生成完成后刷新顶部导航数据（读刚写好的 tools.json，保证 ed 与原 ed 同源一致，
    # 消除「导航先跑、读旧 tools.json」导致的不对称）。gen_industry_groups 本身幂等。
    _gen_nav = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', 'gen_industry_groups.py')
    _r = subprocess.run([sys.executable, _gen_nav], check=False)
    if _r.returncode != 0:
        print('[warn] gen_industry_groups 返回非零，导航数据可能未更新', file=sys.stderr)
