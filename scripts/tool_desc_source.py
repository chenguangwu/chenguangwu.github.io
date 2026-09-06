#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站「工具描述」的唯一权威源（single source of truth）。

历史问题：三处各自解析描述，结果互相打架——
  · json/tools.json 的 d（供搜索、首页、industry-*.json 消费）：
    只判「含中文」就返回，而 i18n 的 zh-CN.desc 常常就是标题本身
    （如「矩阵转置」「KSUID 生成器」）→ 描述退化成名称。
  · tools/<ind>/index.html 的 .t-zh-desc（分类落地页）：
    额外做 is_weak_desc 判定，能落到 zh-CN.intro 的真实描述 → 有内容。
  · json/industry-groups.json（顶部导航下拉面板）：
    用 tools.json 的 d + 页面 meta → 实测 92% 卡片无描述。

现在 _build.py（分类页 + compute_zh_desc）与 scripts/gen_industry_groups.py
统一调用本模块，保证「分类页 / 搜索 / 首页 / 顶部导航」看到的描述完全一致。

中文描述优先级：
  1. i18n/tools/<ind>.json 的 <slug>.zh-CN.desc（须通过 is_weak_desc 判定）
  2. 同上 .zh-CN.intro（真实描述，按需截断）
  3. 工具页 <meta name="description">（须含中文且非弱）
  4. tools.json 的 desc / name 中含中文的一侧
  5. 最后回退 name

英文描述优先级：
  1. i18n 的 <slug>.en-US.intro（剥掉模板套话后须仍有 ≥20 字符实质内容）
  2. DESC_OVERRIDE[1]（人工精翻英文，scripts/tool_desc_override.py，按中文名索引）
  3. tools.json 的 ed（同样剥套话）
  4. 翻译中文 zh_desc / 中文兜底（保证英文态也有内容、与中文态一致）
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CJK = re.compile(r'[一-鿿]')

# ed / en-US.intro 里大量「Free online tool on ToolBox — 100% client-side」这类模板签名，
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
    # i18n en-US.intro 的机器腔（"X is a free online tool." / "Generate results online..."）
    r'\s*[.\-–—,]?\s*is a (free|handy|simple).*$',
    r'\s*[.\-–—,]?\s*(Generate|Calculate|Convert|Create)\s+\w+\s+online.*$',
]

# i18n 文件按行业缓存（构建期会被调用上万次，必须缓存）
_I18N_CACHE = {}
_META_CACHE = {}

# 人工补齐的中英文描述表：scripts/tool_desc_override.py -> DESC_OVERRIDE
# key 为工具中文名 -> (中文描述, 英文描述)。属于「人工精翻」，优先级高于
# tools.json 的脏 ed / 空 meta 回退。_build.py 与 gen_industry_groups.py
# 统一通过本模块消费，保证分类页 / 导航 / 搜索三端描述完全一致。
try:
    from tool_desc_override import DESC_OVERRIDE as _DESC_OVERRIDE
except Exception:
    _DESC_OVERRIDE = {}


# 少数 i18n 条目尚未真实化，intro 是生成器批量吐的模板腔
# （例："本开发工具在前端本地完成解析、转换与处理… 工具名称：API 签名生成器。"）
# 这类句子虽长于标题但零信息量，命中即视为弱描述继续回退，避免污染全站卡片
ZH_BOILERPLATE = [
    r'工具名称[：:]',
    r'本(?:开发|计算|在线)?工具在前端本地完成',
    r'依据指定格式规范在前端按规则',
    r'遵循对应语法与格式规范',
    r'本工具(?:为|是)?(?:纯前端|本地)(?:运行|处理)的?在线工具',
]


def is_boilerplate(desc):
    """中文描述是否为生成器模板套话。"""
    s = desc or ''
    return any(re.search(p, s) for p in ZH_BOILERPLATE)


def has_cjk(s):
    """字符串是否含中日韩（中文）字符。"""
    return bool(CJK.search(s or ''))


def is_weak_desc(desc, title):
    """判定中文描述是否只是标题重复或缺乏信息量（弱描述需改用 intro）。

    与 _build.py 分类页历史判定规则保持一致，是全站共用的唯一实现。
    """
    if not desc or not has_cjk(desc):
        return True
    if is_boilerplate(desc):        # 模板腔：看似有内容，实则零信息量
        return True
    d = (desc or '').strip()
    t = (title or '').strip()
    if not t:
        return len(d) < 12
    if d == t:                                       # 完全等于标题
        return True
    if d.startswith(t) and len(d) <= len(t) + 8:     # 标题 + 无意义后缀
        return True
    if t.startswith(d) and len(t) <= len(d) + 8:     # 标题更长，desc 只是前缀
        return True
    if len(d) <= max(len(t), 12):                    # 比标题还短，显然不是描述
        return True
    return False


def load_tool_i18n(ind):
    """加载 i18n/tools/<ind>.json（带缓存）。"""
    if ind not in _I18N_CACHE:
        fp = os.path.join(ROOT, 'i18n', 'tools', '%s.json' % ind)
        try:
            _I18N_CACHE[ind] = json.load(open(fp, encoding='utf-8')) if os.path.isfile(fp) else {}
        except Exception:
            _I18N_CACHE[ind] = {}
    return _I18N_CACHE[ind]


def slug_of(t):
    """工具条目 -> i18n 键（文件名去掉 .html）。"""
    return (t.get('file') or '').replace('.html', '')


def i18n_entry(t):
    """取该工具在 i18n/tools/<ind>.json 中的条目（dict 或 {}）。"""
    v = load_tool_i18n(t.get('industry', 'it')).get(slug_of(t))
    return v if isinstance(v, dict) else {}


def slug_name(t):
    """中文名：name 与 desc 中含中文的那个（_build.py 会对部分页做英文 title 预渲染，
    导致 name/desc 的中英属性互换，以「谁含中文」判定语言最稳）。"""
    n = t.get('name') or ''
    d = t.get('desc') or ''
    if has_cjk(n):
        return n
    if has_cjk(d):
        return d
    return n


def meta_desc(path):
    """从工具页 <meta name="description"> 取描述（只读前 12KB，带缓存）。

    path 形如 'it/gitignore-generator.html'（相对 tools/ 目录）。
    """
    if not path:
        return ''
    if path in _META_CACHE:
        return _META_CACHE[path]
    d = ''
    try:
        with open(os.path.join(ROOT, 'tools', path), encoding='utf-8', errors='ignore') as f:
            head = f.read(12000)
        m = re.search(r'<meta name="description" content="([^"]*)"', head)
        if m:
            d = html.unescape(m.group(1)).strip()
    except Exception:
        d = ''
    _META_CACHE[path] = d
    return d


def clip(s, n):
    """截断到 n 字并在末尾加省略号（不在标点/空格处留残尾）。"""
    s = (s or '').strip()
    if len(s) <= n:
        return s
    return s[:n - 1].rstrip('，,。、；;：: ') + '…'


def strip_ed_boilerplate(s):
    for pat in ED_BOILERPLATE:
        s = re.sub(pat, '', s, flags=re.I)
    return s.strip().rstrip(' .,-–—:·|')


# 本地词典翻译（scripts/zh_en_dict.py，零成本、纯构建期），缺失时降级为原样返回
try:
    from zh_en_dict import translate_text as _translate_text
except Exception:
    def _translate_text(s):
        return s or ''


def _clean_en(raw, name_en):
    """英文描述清洗：剥名字前缀 + 去套话，留 ≥20 字实质内容则返回，否则空。

    注意：name_en 仅在「确为英文名（不含中文）」时才用于剥前缀。translate_name
    对未收录的词会回退返回中文原名，若拿中文名当英文前缀去削，会把 ed 开头的中文
    品类名（如「资本资产定价模型」）误删，导致 generate_split_jsons 与主循环两次
    调用 en_desc 拿到不同 ed（一个带名、一个被削名），三端不一致。
    """
    raw = (raw or '').strip()
    if not raw:
        return ''
    if name_en and not has_cjk(name_en) and raw.startswith(name_en):
        raw = raw[len(name_en):].lstrip(' -–—:·|')
    clean = strip_ed_boilerplate(raw)
    # 拒绝模板腔残留：主体只是「is a / helps you / allows you」等空洞短语，
    # 或仍含「free online tool / client-side」套话标记（ED_BOILERPLATE 防漏）。
    # 否则「X is a free online tool…」削前缀后变「is a…」仍 ≥20 字会被当干净英文。
    if re.search(r'\bfree online tool\b|\bclient[- ]?side\b|100%\s*client', clean, re.I):
        return ''
    if re.match(r'^(is a|are a|helps? you|allows? you|lets you|provides? (a|an) )', clean, re.I):
        return ''
    return clean if len(clean) >= 20 else ''


def zh_desc(t, max_len=None, use_meta=True):
    """权威中文描述：i18n desc(强) → i18n intro → 页面 meta → desc/name 中文侧 → name。

    max_len: 截断长度（None 表示不截断）。分类页传 100、导航卡片传 32、tools.json 传 80。
    """
    name = slug_name(t)
    entry = i18n_entry(t) or {}
    zh = entry.get('zh-CN') or {}
    if not isinstance(zh, dict):
        zh = {}

    cand = zh.get('desc') if isinstance(zh.get('desc'), str) else ''
    if cand and not is_weak_desc(cand, name):
        return clip(cand, max_len) if max_len else cand

    intro = zh.get('intro') if isinstance(zh.get('intro'), str) else ''
    if intro and not is_weak_desc(intro, name):
        return clip(intro, max_len) if max_len else intro

    # 人工精翻表 DESC_OVERRIDE[0]：源数据无描述（meta==名称）时由人工补齐，
    # 优先级高于下方 meta / name 回退，确保导航与分类页中文描述同源一致
    _ov = _DESC_OVERRIDE.get((t.get('name') or '').strip())
    if _ov and isinstance(_ov, (list, tuple)) and len(_ov) >= 1 and isinstance(_ov[0], str) and _ov[0].strip():
        return clip(_ov[0], max_len) if max_len else _ov[0]

    if use_meta:
        md = meta_desc(t.get('path', ''))
        if md and has_cjk(md) and not is_weak_desc(md, name):
            return clip(md, max_len) if max_len else md

    # i18n 与 meta 都没给力：回退 name/desc 中含中文的一侧（可能是纯名字，前端会做去重隐藏）
    return clip(name, max_len) if max_len else name


def en_desc(t, max_len=None):
    """权威英文描述：i18n en-US.intro → DESC_OVERRIDE[1] → 翻译中文 zh_desc → 中文兜底。

    不再读取 t['ed'] 自身作为来源：t['ed'] 是历史生成器产物（92% 为套话
    「X is a free online tool…」），且构建期 t['en'] 状态不可靠（HTML 扫描时未收录
    词会回退中文名），自引用会「读脏 ed → 清洗不足 → 返回脏英文」，并且
    generate_split_jsons 与主循环两次调用拿到不同结果，造成三端不一致。
    _build.py / gen_industry_groups 仍把本结果写回 t['ed'] 字段并落盘，供搜索索引
    与导航/分类页消费，故三端最终完全同源。
    """
    entry = i18n_entry(t) or {}
    en = entry.get('en-US') or {}
    en = en if isinstance(en, dict) else {}
    name_en = (t.get('en') or '').strip()

    # 1. i18n en-US.intro（最权威的英文描述）
    c = _clean_en(en.get('intro') if isinstance(en.get('intro'), str) else '', name_en)
    if c:
        return clip(c, max_len) if max_len else c

    # 1.5. 人工精翻表 DESC_OVERRIDE[1]：优先级高于脏 ed / 翻译兜底
    _ov = _DESC_OVERRIDE.get((t.get('name') or '').strip())
    if _ov and isinstance(_ov, (list, tuple)) and len(_ov) >= 2 and isinstance(_ov[1], str):
        c = _clean_en(_ov[1], name_en)
        if c:
            return clip(c, max_len) if max_len else c

    # （不再读取 t['ed'] 自身：历史生成器套话，且会引入三端不一致，见函数 docstring）

    # 3. 翻译中文 zh_desc（本地词典，能翻出英文则用之）
    zh = zh_desc(t)
    if zh:
        tr = _translate_text(zh)
        if tr and tr != zh and not has_cjk(tr):
            c = _clean_en(tr, name_en)
            if c:
                return clip(c, max_len) if max_len else c
        # 4. 兜底中文：英文缺失时展示中文，确保英文态也有内容、与中文态一致
        return clip(zh, max_len) if max_len else zh
    return ''
