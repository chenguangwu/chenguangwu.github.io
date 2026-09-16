#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复「工具 ↔ 使用指南」双向配对链路（三类缺陷）。

背景
----
`_build.py`（行 ~3040）按 `json/guides.json` 给工具页注入「📖 查看 xxx 使用指南」入口，
映射靠两本字典：`GUIDE_MAP[tool basename]` 与 `GUIDE_MAP_IND['<industry>/<basename>']`
（后者由指南页正文里的 `/tools/<industry>/<base>.html` 引用反查）。
只要 `guides.json` 缺条目或 `tool` 字段写错，这篇指南就永不出现在工具页上。

三类缺陷：
1) `--register` 补登记：磁盘有指南页但 json 无条目。
2) `--fix-tool-field` 修错位登记：条目在但 `tool` basename 全站不存在（工具改名遗留）。
3) `--prune` 下架孤儿指南：工具页已不存在（多为合规下架工具残留），主 CTA 指向 404。
   删除：HTML 本体 + zh-tw 副本 + 中英索引条目 + json 条目；sitemap/sw 由构建重建。

配对判据（唯一才认，歧义跳过）：
  a. 同名 basename  b. 行业前缀消歧 `<ind>-<base>`  c. 指南页 back 主链接  d. 正文唯一工具引用

用法
----
    python3 scripts/fix_guides_pairing.py
    python3 scripts/fix_guides_pairing.py --register --fix-tool-field --prune
    python3 scripts/fix_guides_pairing.py --register --fix-tool-field --prune --apply
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
ZH_GUIDES_DIR = os.path.join(ROOT, 'zh-tw', 'guides')
GUIDES_JSON = os.path.join(ROOT, 'json', 'guides.json')
TOOLS_JSON = os.path.join(ROOT, 'json', 'tools.json')
INDEX = os.path.join(ROOT, 'guides', 'index.html')
ZH_INDEX = os.path.join(ROOT, 'zh-tw', 'guides', 'index.html')

# 人工逐篇核实的「旧 slug -> 现工具」对照（正文引用不足以唯一定位时用）
MANUAL_TOOL_FIX = {
    'base64-guide.html': 'tools/it/base64-converter.html',
    'calorie-calculator-guide.html': 'tools/food/food-calorie-counter.html',
    'gradient-generator-guide.html': 'tools/design/gradient.html',
    'color-blindness-sim-guide.html': 'tools/design/colorblind-simulator.html',
    'budget-planner-guide.html': 'tools/funeral/funeral-budget-planner.html',
    'roi-calculator-guide.html': 'tools/finance/investment-roi.html',
    'tnss-guide.html': 'tools/ent/calc-1.html',
}

TOOLREF_RE = re.compile(
    r'(?:https://chenguangwu\.github\.io)?/?(?:tools/)?([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+\.html)')
BACK_DIV_RE = re.compile(r'<div class="back">([\s\S]{0,400}?)</div>')
TREF_RE = re.compile(
    r'href="(?:https://chenguangwu\.github\.io)?/?(tools/[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+\.html)"')
H1_RE = re.compile(r'<h1[^>]*>([\s\S]{0,200}?)</h1>')
FB_RE = re.compile(r'data-i18n-fb="([^"]{1,200})"')


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def guide_title(path):
    c = read(path)
    m = H1_RE.search(c)
    name = ''
    if m:
        fb = FB_RE.search(m.group(0))
        name = (fb.group(1) if fb else re.sub(r'<[^>]+>', '', m.group(1))).strip()
    for suf in (' 使用指南', '使用指南', ' 指南', '指南'):
        if name.endswith(suf):
            name = name[: -len(suf)].strip()
    return name.strip()


def tool_refs(content):
    """(back 区工具链接, 全文工具链接)"""
    m = BACK_DIV_RE.search(content)
    back = [x.lstrip('/') for x in TREF_RE.findall(m.group(1))] if m else []
    allrefs = [x.lstrip('/') for x in TREF_RE.findall(content)]
    return back, allrefs


def main():
    do_register = '--register' in sys.argv
    do_fix = '--fix-tool-field' in sys.argv
    do_prune = '--prune' in sys.argv
    apply = '--apply' in sys.argv

    tools = json.load(open(TOOLS_JSON, encoding='utf-8'))
    by_base = {}
    for t in tools:
        by_base.setdefault(os.path.basename(t.get('url') or ''), []).append(t)
    live_urls = {t['url'] for t in tools if os.path.exists(os.path.join(ROOT, t['url']))}
    live_base = {os.path.basename(u) for u in live_urls}
    industries = sorted({t['industry'] for t in tools})

    raw_gj = read(GUIDES_JSON)
    gj = json.loads(raw_gj)
    if json.dumps(gj, ensure_ascii=False, indent=1) != raw_gj:
        print('[FATAL] json/guides.json 非 indent=1 无尾换行格式，禁止落盘')
        return 2
    registered = {os.path.basename(e.get('guide') or ''): e for e in gj}

    files = sorted(f for f in os.listdir(GUIDES_DIR) if f.endswith('-guide.html'))

    def resolve(fn):
        slug = fn[: -len('-guide.html')]
        cands = [t for t in by_base.get(slug + '.html', []) if t['url'] in live_urls]
        if len(cands) == 1:
            return cands[0]['url']
        if not cands:
            for ind in industries:
                if slug.startswith(ind + '-'):
                    u = 'tools/%s/%s.html' % (ind, slug[len(ind) + 1:])
                    if u in live_urls:
                        return u
        content = read(os.path.join(GUIDES_DIR, fn))
        back, allrefs = tool_refs(content)
        for pool in (back, allrefs):
            hit = sorted({r for r in pool if r in live_urls})
            if len(hit) == 1:
                return hit[0]
        return None

    pairs, unresolved = {}, []
    for fn in files:
        u = resolve(fn)
        if u:
            pairs[fn] = u
        else:
            unresolved.append(fn)

    saved_by_manual = sorted(set(MANUAL_TOOL_FIX) & set(unresolved))
    for fn in saved_by_manual:
        pairs[fn] = MANUAL_TOOL_FIX[fn]
        unresolved.remove(fn)

    # ---- 待修 tool 字段 ----
    fix_field = []
    for e in gj:
        tb = e.get('tool') or ''
        gfn = os.path.basename(e.get('guide') or '')
        gp = os.path.join(GUIDES_DIR, gfn)
        if not os.path.exists(gp) or tb in live_base:
            continue
        target = MANUAL_TOOL_FIX.get(gfn)
        if not target:
            back, allrefs = tool_refs(read(gp))
            for pool in (back, allrefs):
                hit = sorted({r for r in pool if r in live_urls})
                if len(hit) == 1:
                    target = hit[0]
                    break
        if target and os.path.basename(target) != tb:
            fix_field.append((e, target))

    to_add = [(fn, u) for fn, u in sorted(pairs.items()) if fn not in registered]
    stale = [e for e in gj
             if os.path.basename(e.get('guide') or '')
             and not os.path.exists(os.path.join(GUIDES_DIR, os.path.basename(e.get('guide') or '')))]

    print('=== 全站 guides 体检 ===')
    print('指南页 %d ｜ 可唯一定位工具 %d ｜ 无法定位 %d' % (len(files), len(pairs), len(unresolved)))
    print('人工核实表救回 %d 篇: %s' % (len(saved_by_manual), saved_by_manual))
    print('仍无法定位（下架候选）%d 篇: %s' % (len(unresolved), unresolved))
    print('\n=== 1) 待补登记 %d 条 ===' % len(to_add))
    for fn, u in to_add[:8]:
        print('   %-45s -> %s' % (fn, u))
    print('\n=== 2) 待修 tool 字段 %d 条 ===' % len(fix_field))
    for e, target in fix_field:
        print('   %-32s %s -> %s' % (os.path.basename(e.get('guide') or ''),
                                     e.get('tool'), os.path.basename(target)))
    print('\n=== 3) 待清 stale 登记（指南文件已不存在）%d 条 ===' % len(stale))
    for e in stale:
        print('   tool=%-28s guide=%s' % (e.get('tool'), e.get('guide')))

    if not apply:
        print('\n[dry-run] 未写入、未删除。确认后加 --apply。')
        return 0

    if do_register and to_add:
        for fn, u in to_add:
            title = guide_title(os.path.join(GUIDES_DIR, fn)) or fn[: -len('-guide.html')]
            gj.append({'tool': os.path.basename(u),
                       'guide': '../../guides/' + fn,
                       'title': '%s使用指南' % title})
        print('[apply] 新增登记 %d 条' % len(to_add))

    if do_fix and fix_field:
        for e, target in fix_field:
            e['tool'] = os.path.basename(target)
        print('[apply] 修正 tool 字段 %d 条' % len(fix_field))

    if do_prune:
        if stale:
            before = len(gj)
            gj = [e for e in gj if e not in stale] if False else [
                e for e in gj
                if os.path.exists(os.path.join(GUIDES_DIR, os.path.basename(e.get('guide') or '')))]
            print('[apply] 清理 stale 条目 %d -> %d 条' % (before, len(gj)))
        if unresolved:
            for fn in unresolved:
                for p in (os.path.join(GUIDES_DIR, fn), os.path.join(ZH_GUIDES_DIR, fn)):
                    if os.path.exists(p):
                        os.remove(p)
            print('[apply] 删除孤儿指南页 %d 篇（含 zh-tw 副本）' % len(unresolved))
            for path in (INDEX, ZH_INDEX):
                if not os.path.exists(path):
                    continue
                c = read(path)
                cut = 0
                for fn in unresolved:
                    pat = re.compile(r'<li><a href="[^"]*%s"[\s\S]{0,800}?</li>' % re.escape(fn))
                    c2, n = pat.subn('', c, count=1)
                    if n:
                        c = c2
                        cut += 1
                    else:
                        print('   [WARN] 索引未命中: %s (%s)' % (fn, os.path.basename(path)))
                write(path, c)
                print('[apply] 索引清理 %d 条 -> %s' % (cut, path))

    # 最后统一收口：任何指向不存在文件的登记条目一律清掉（含本轮刚删除的孤儿指南）
    before = len(gj)
    gj = [e for e in gj
          if os.path.exists(os.path.join(GUIDES_DIR, os.path.basename(e.get('guide') or '')))]
    if before != len(gj):
        print('[apply] 收口清理无效登记 %d -> %d 条' % (before, len(gj)))

    write(GUIDES_JSON, json.dumps(gj, ensure_ascii=False, indent=1))
    print('[apply] guides.json 已落盘：%d 条' % len(gj))
    return 0


if __name__ == '__main__':
    sys.exit(main())
