#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 content_deepdive.json 中缺 `title` 的条目（线上渲染出「📚 深度解析：」空标题）。

背景
----
`_build.py::_build_deep_dive_html()` 只认 `title` / `scenarios` / `examples[].body` /
`faqs[].a` 四个字段。凡条目缺 `title`，页面就会渲染成 `<h2>📚 深度解析：</h2>`，
`summary` / `example` 这类旧键一概不渲染。本脚本按权威源回填中文标题，
并把写错的 example 键（`a` → `body`）归一。

标题权威源优先级（同 MEMORY.md 口径：i18n 是页面 title 的权威源）
------------------------------------------------------------
1. `i18n/tools/<industry>.json`  ->  <slug>  ->  zh-CN.title  ->  zh-CN.h1
2. 页面 HTML 首个含中日韩字符的 `<h2>` 文本（去前置图标）
3. 页面 HTML 首个含中日韩字符的 `data-zh` 属性值（去前置图标）

用法：python3 scripts/fix_deepdive_title.py            # dry-run
      python3 scripts/fix_deepdive_title.py --apply     # 落盘
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD_PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
TOOLS_JSON = os.path.join(ROOT, 'json', 'tools.json')

CJK_RE = re.compile(r'[\u4e00-\u9fff]')
# 前置图标 / 变体选择符 / 星形装饰等
LEAD_ICON_RE = re.compile(r'^[\s\u2000-\u3300\uFE0F\u2600-\u27BF\U0001F000-\U0001FAFF]+')
H2_RE = re.compile(r'<h2[^>]*>([\s\S]{0,300}?)</h2>', re.I)
DATA_ZH_RE = re.compile(r'data-zh="([^"]{1,200})"')


def clean_name(s):
    """剥标签、去前置图标与首尾空白。"""
    if not s:
        return ''
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    s = LEAD_ICON_RE.sub('', s)
    return s.strip().strip('：:').strip()


def i18n_title(industry, slug):
    p = os.path.join(ROOT, 'i18n', 'tools', '%s.json' % industry)
    if not os.path.exists(p):
        return ''
    try:
        j = json.load(open(p, encoding='utf-8'))
    except Exception:
        return ''
    e = j.get(slug) or {}
    zh = e.get('zh-CN') or {}
    for k in ('title', 'h1'):
        v = clean_name(zh.get(k) or '')
        if v and CJK_RE.search(v):
            return v
    return ''


def page_title(url):
    """从已构建页面取中文工具名（h2 文本优先，其次 data-zh）。"""
    if not url or not os.path.exists(os.path.join(ROOT, url)):
        return ''
    try:
        c = open(os.path.join(ROOT, url), encoding='utf-8').read()
    except Exception:
        return ''
    for m in H2_RE.finditer(c):
        v = clean_name(m.group(1))
        if v and CJK_RE.search(v) and '深度解析' not in v:
            return v
    for m in DATA_ZH_RE.finditer(c):
        v = clean_name(m.group(1))
        if v and CJK_RE.search(v) and '深度解析' not in v:
            return v
    return ''


def main():
    apply = '--apply' in sys.argv
    raw = open(DD_PATH, encoding='utf-8').read()
    data = json.loads(raw)

    # 格式守恒自检：本项目约定 content_deepdive.json 为 indent=1 + 尾换行
    if json.dumps(data, ensure_ascii=False, indent=1) + '\n' != raw:
        print('[FATAL] content_deepdive.json 格式与 indent=1 约定不一致，禁止落盘')
        return 2

    tools = json.load(open(TOOLS_JSON, encoding='utf-8'))
    page = {}
    for t in tools:
        url = t.get('url') or ''
        slug = os.path.splitext(os.path.basename(url))[0]
        page.setdefault((t.get('industry') or t.get('cat') or '', slug), t)

    miss = [k for k, v in data.items()
            if isinstance(v, dict) and not (v.get('title') or '').strip()]

    filled, skipped = [], []
    for k in miss:
        industry, _, slug = k.partition('/')
        t = page.get((industry, slug)) or {}
        title = ''
        src = ''
        for fn, name in ((i18n_title, 'i18n'), (page_title, 'h2'), (page_title, 'data-zh')):
            if name == 'i18n':
                v = fn(industry, slug)
            elif name == 'h2':
                v = fn(t.get('url'))
            else:
                v = ''
            if v:
                title, src = v, name
                break
        if not title:
            skipped.append(k)
            continue
        data[k]['title'] = title
        # key 顺序：与既有条目一致（title 放首位）
        if list(data[k].keys())[0] != 'title':
            items = [('title', title)] + [(kk, vv) for kk, vv in data[k].items() if kk != 'title']
            data[k] = dict(items)
        filled.append((k, src, title, bool(t)))

    # 归一化：example 缺 body 但有 a（键名写错）
    ex_fixed = []
    for k, v in data.items():
        if not isinstance(v, dict):
            continue
        for e in (v.get('examples') or []):
            if isinstance(e, dict) and not (e.get('body') or '').strip() and (e.get('a') or '').strip():
                e['body'] = e.pop('a')
                ex_fixed.append(k)

    live = [f for f in filled if f[3]]
    orphan = [f for f in filled if not f[3]]
    print('缺 title 条目: %d' % len(miss))
    print('  可回填且页面在线: %d' % len(live))
    print('  可回填但页面不存在(孤儿键，不渲染): %d' % len(orphan))
    print('  无中文名来源: %d -> %s' % (len(skipped), skipped[:10]))
    print('example 键名归一 (a->body): %d -> %s' % (len(ex_fixed), ex_fixed[:5]))
    print('--- 来源分布 ---')
    from collections import Counter
    print(Counter(f[1] for f in filled).most_common())
    print('--- 样例（在线页）---')
    for k, src, title, _ in live[:15]:
        print('  %-45s [%s] %s' % (k, src, title))

    if not apply:
        print('\n[dry-run] 未写入。加 --apply 落盘。')
        return 0

    out = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    with open(DD_PATH, 'w', encoding='utf-8') as f:
        f.write(out)
    print('\n[apply] 已写入 %s（%.1f KB）' % (DD_PATH, len(out.encode()) / 1024))
    return 0


if __name__ == '__main__':
    sys.exit(main())
