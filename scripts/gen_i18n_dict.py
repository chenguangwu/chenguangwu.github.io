#!/usr/bin/env python3
"""
gen_i18n_dict.py — 提取工具页源文本，生成 i18n/tools/<industry>.json 翻译字典骨架。

设计：
- 纯正则提取，无第三方依赖。
- 输出格式（与 js/i18n.js tool-i18n.js 的 loadIndustryDict 对齐）：
    { "<slug>": { "zh-CN": { "title": "...", "h1": "...", "intro": "..." , "note":["...","..."] } } }
  en-US 留空，由人工或 MT 步骤填充（见 docs/i18n-spec.md Non-goals）。
- 仅当提取到有效文本才写入，避免空键导致英文态空白。
- 幂等：已存在的 en-US 等翻译不会被覆盖（仅补充 zh-CN 源 + 新增 slug）。

用法：python3 scripts/gen_i18n_dict.py [--ind <行业>] [--dry]
"""
import os
import re
import json
import glob
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, 'tools')
OUT_DIR = os.path.join(ROOT, 'i18n', 'tools')


def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    s = s.replace('&#39;', "'").replace('&quot;', '"')
    return s.strip()


def extract_text(el):
    """从一段含标签的 HTML 中取纯文本。"""
    return strip_tags(el) if el else ''


def clean_icon(text):
    r"""去掉开头的 emoji/图标（通常是首个 \S+ 非中文片段）。"""
    if not text:
        return text
    # 若以非中文字符（emoji/字母）开头，去掉首个 token
    m = re.match(r'^(\s*\S+\s+)(.*)$', text)
    if m and not re.search(r'[\u4e00-\u9fff]', m.group(1)):
        return m.group(2).strip()
    return text.strip()


LEGACY_LANGS = ['en-US']


def _flat_to_nested(flat):
    """扁平顶层语种字典 {"json-formatter.title": ...} -> {slug: {field: ...}}。"""
    nested = {}
    for k, v in flat.items():
        parts = k.split('.')
        slug, rest = parts[0], parts[1:]
        if not rest:
            continue
        if rest[0] == 'note' and len(rest) >= 2:
            try:
                idx = int(rest[1])
            except ValueError:
                idx = None
            if idx is not None:
                arr = nested.setdefault(slug, {}).setdefault('note', [])
                while len(arr) <= idx:
                    arr.append(None)
                arr[idx] = v
                continue
        if rest[0] == 'title' and len(rest) >= 2 and rest[1] == 'h1':
            nested.setdefault(slug, {})['h1'] = v
            continue
        nested.setdefault(slug, {})[rest[0]] = v
    return nested


def _migrate_legacy(existing):
    """兼容迁移：顶层遗留扁平语种字典 -> 嵌套 per-slug 结构（幂等）。"""
    flat_langs = {lg: existing.pop(lg) for lg in LEGACY_LANGS
                  if lg in existing and isinstance(existing.get(lg), dict)}
    if not flat_langs:
        return existing
    nested = {lg: _flat_to_nested(flat) for lg, flat in flat_langs.items()}
    for lg, nst in nested.items():
        for slug, fields in nst.items():
            existing.setdefault(slug, {})
            existing[slug].setdefault(lg, fields)
    return existing


def parse_tool(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    rec = {}

    # h1（sr-only）
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    if m:
        h1 = clean_icon(extract_text(m.group(1)))
        if h1:
            rec['h1'] = h1

    # h2（工具标题，通常带图标）
    m = re.search(r'<h2[^>]*>(.*?)</h2>', html, re.S)
    if m:
        h2 = clean_icon(extract_text(m.group(1)))
        if h2:
            rec['title'] = h2

    # intro：h2 之后紧邻的 <p>
    m = re.search(r'<h2[^>]*>.*?</h2>\s*<p[^>]*>(.*?)</p>', html, re.S)
    if m:
        intro = extract_text(m.group(1))
        if intro and len(intro) > 4:
            rec['intro'] = intro

    # notes：工具说明区块的 <li>
    notes = re.findall(r'<div class="tool-notes"[^>]*>.*?<ul>(.*?)</ul>', html, re.S)
    if notes:
        items = re.findall(r'<li>(.*?)</li>', notes[0], re.S)
        items = [extract_text(i) for i in items if extract_text(i)]
        if items:
            rec['note'] = items

    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ind', help='仅生成指定行业', default=None)
    ap.add_argument('--dry', action='store_true', help='只打印统计，不写文件')
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    # 按行业聚合
    by_ind = {}
    pattern = os.path.join(TOOLS_DIR, '**', '*.html')
    for path in glob.glob(pattern, recursive=True):
        fn = os.path.basename(path)
        if fn == 'index.html' or fn.startswith('_'):
            continue
        ind = os.path.relpath(path, TOOLS_DIR).split(os.sep)[0]
        if args.ind and ind != args.ind:
            continue
        slug = fn[:-5]
        rec = parse_tool(path)
        if rec:
            by_ind.setdefault(ind, {})[slug] = rec

    total_tools = sum(len(v) for v in by_ind.values())
    print('提取行业数: %d，工具数: %d' % (len(by_ind), total_tools))

    written = 0
    for ind in sorted(by_ind.keys()):
        # 读取已有字典（保留已翻译的 en-US 等）；兼容迁移遗留扁平结构
        out_path = os.path.join(OUT_DIR, ind + '.json')
        existing = {}
        if os.path.exists(out_path):
            try:
                existing = json.load(open(out_path, 'r', encoding='utf-8'))
            except Exception:
                existing = {}
        existing = _migrate_legacy(existing)
        merged = dict(existing)
        for slug, rec in by_ind[ind].items():
            entry = merged.get(slug, {})
            # 仅补充/覆盖 zh-CN 源（不触碰已有翻译语种 en-US 等）
            entry['zh-CN'] = rec
            merged[slug] = entry
        if args.dry:
            continue
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
            f.write('\n')
        written += 1

    if not args.dry:
        print('已写入 %d 个行业字典文件到 %s' % (written, OUT_DIR))


if __name__ == '__main__':
    main()
