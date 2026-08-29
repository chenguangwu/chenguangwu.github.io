#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""挖掘工具页正文里【尚未翻译】的中文短语，按出现频率排序，供分批 AI 翻译。

流程
----
1. 扫描 tools/*/*.html，剔除 script/style/注释，提取文本节点 + placeholder/title 属性
2. 过滤：含中文、长度 2~60、非纯符号/纯数字
3. 排除已覆盖：所有 -phrases.json 的 key + tool-i18n.js 的 BODY_PHRASE_MAP key
4. 按「出现过的工具页数」降序输出 → 先翻高频短语，用最少条目覆盖最多页面

输出
----
phrases-pending.json: [{zh, freq(页面数), industries(行业->次数), sample(样例页面), len}]

用法
----
    python3 scripts/mine_pending_phrases.py                 # 全量
    python3 scripts/mine_pending_phrases.py --ind it        # 只挖某行业
    python3 scripts/mine_pending_phrases.py --min-freq 3    # 只要出现 >=3 页的
"""
import argparse
import glob
import html as html_mod
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, 'i18n', 'tools')
TOOL_I18N = os.path.join(ROOT, 'js', 'tool-i18n.js')

SCRIPT_RE = re.compile(r'<script\b.*?</script>', re.S | re.I)
STYLE_RE = re.compile(r'<style\b.*?</style>', re.S | re.I)
COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
TAG_RE = re.compile(r'<[^>]+>')

# 以下块已被其它机制覆盖，翻译它们属于无效劳动，抽取时剔除：
#  - .rt-name / .rt-desc：关联工具卡片，英文由 slug-en.json 的 en/ed 替换（translateRelatedTools）
#  - <h2> / .intro：工具正文标题与简介，英文由 -body.json 覆盖（applyToolBody）
#  - 带 data-i18n 的元素：由 I18n.apply 管理，translateBodyPhrases 会跳过
RT_RE = re.compile(r'<(span|a|div)\b[^>]*class="[^"]*\brt-(?:name|desc)\b[^"]*"[^>]*>.*?</\1>', re.S | re.I)
H2_RE = re.compile(r'<h2\b.*?</h2>', re.S | re.I)
INTRO_RE = re.compile(r'<p\b[^>]*class="[^"]*\bintro\b[^"]*"[^>]*>.*?</p>', re.S | re.I)
DI18N_RE = re.compile(r'<(\w+)\b[^>]*\bdata-i18n\b[^>]*>.*?</\1>', re.S | re.I)
ATTR_RE = re.compile(r'(?:placeholder|title|aria-label)="([^"]{0,120})"')
ZH_RE = re.compile(r'[\u4e00-\u9fff]')
NOISE_RE = re.compile(r'^[\s\d\W_]+$', re.U)

MIN_LEN, MAX_LEN = 2, 60


def load_covered():
    """已翻译的中文短语集合（phrases + BODY_PHRASE_MAP）。"""
    covered = set()

    for p in glob.glob(os.path.join(I18N_DIR, '*-phrases.json')):
        try:
            for k in json.load(open(p, encoding='utf-8')):
                covered.add(k)
                covered.add(k.lstrip('/ '))
        except (IOError, OSError, ValueError):
            pass

    # 全局短语表 BODY_PHRASE_MAP（'中文': 'English',）
    try:
        src = open(TOOL_I18N, encoding='utf-8').read()
        m = re.search(r'BODY_PHRASE_MAP\s*=\s*\{(.*?)\n  \};', src, re.S)
        if m:
            for zh, _en in re.findall(r"'((?:[^'\\]|\\.)*)'\s*:\s*'((?:[^'\\]|\\.)*)'", m.group(1)):
                covered.add(zh)
    except (IOError, OSError):
        pass

    return covered


def extract_texts(raw):
    """从单个页面提取候选中文短语（去重）。"""
    raw = SCRIPT_RE.sub(' ', raw)
    raw = STYLE_RE.sub(' ', raw)
    raw = COMMENT_RE.sub(' ', raw)
    raw = RT_RE.sub(' ', raw)
    raw = H2_RE.sub(' ', raw)
    raw = INTRO_RE.sub(' ', raw)
    raw = DI18N_RE.sub(' ', raw)

    found = set()

    for m in ATTR_RE.finditer(raw):
        found.add(html_mod.unescape(m.group(1)).strip())

    for chunk in TAG_RE.split(raw):
        t = html_mod.unescape(chunk).strip()
        if t:
            found.add(t)

    out = set()
    for t in found:
        t = re.sub(r'\s+', ' ', t).strip()
        if not t or len(t) < MIN_LEN or len(t) > MAX_LEN:
            continue
        if not ZH_RE.search(t):
            continue
        if NOISE_RE.match(t):
            continue
        out.add(t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ind', help='只挖指定行业')
    ap.add_argument('--min-freq', type=int, default=1, help='最少出现页面数')
    ap.add_argument('--out', default=os.path.join(ROOT, 'phrases-pending.json'))
    args = ap.parse_args()

    covered = load_covered()
    print('已覆盖中文短语（phrases + BODY_PHRASE_MAP）: %d 条' % len(covered))

    pattern = os.path.join(ROOT, 'tools', args.ind or '*', '*.html')
    files = sorted(glob.glob(pattern))
    print('待扫描页面: %d' % len(files))

    freq = defaultdict(int)          # zh -> 页面数
    by_ind = defaultdict(lambda: defaultdict(int))
    sample = {}

    for i, path in enumerate(files):
        if i % 500 == 0:
            print('  扫描 %d/%d ...' % (i, len(files)), file=sys.stderr)
        ind = os.path.basename(os.path.dirname(path))
        try:
            raw = open(path, encoding='utf-8', errors='ignore').read()
        except (IOError, OSError):
            continue
        page = set()
        for t in extract_texts(raw):
            if t in covered:
                continue
            page.add(t)
        for t in page:
            freq[t] += 1
            by_ind[t][ind] += 1
            sample.setdefault(t, os.path.relpath(path, ROOT))

    items = []
    for zh, n in freq.items():
        if n < args.min_freq:
            continue
        items.append({
            'zh': zh,
            'freq': n,
            'len': len(zh),
            'industries': dict(sorted(by_ind[zh].items(), key=lambda kv: -kv[1])[:6]),
            'sample': sample.get(zh, ''),
        })
    items.sort(key=lambda x: (-x['freq'], -x['len']))

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=1)

    total_pages = len(files)
    print('\n待翻译短语（去重后）: %d 条' % len(items))
    print('总出现次数: %d' % sum(i['freq'] for i in items))
    print('输出: %s' % os.path.relpath(args.out, ROOT))
    print('\nTop 20（按覆盖页面数）:')
    for it in items[:20]:
        print('  %4d页  %s' % (it['freq'], it['zh'][:52]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
