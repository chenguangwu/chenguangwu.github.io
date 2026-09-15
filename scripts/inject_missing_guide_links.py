#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补回工具页 -> 指南页的回链。

背景 / 根因：
- _build.py 在生成/重生成工具页时，会用 GUIDE_MAP（来自 json/guides.json）向工具页注入
  <div class="tool-guide-link" data-guide-link="1"> 区块（见 _build.py 2.5 节）。
- 但 _build.py 的插入锚点是【精确匹配】 '<div class="container">'，而 V2 模板（gen_n4b 生成）
  实际写的是 '<div class="container cb-wrap">'（类名带后缀）。精确匹配失败 -> 所有 V2 模板、
  且“先有工具页后补指南”的工具页都缺失该回链，与既有工具页不一致。
- _build.py 对未变更工具页是增量生成、不会重跑，故缺链不会自动补上。

本脚本精确复刻 _build.py 注入算法，仅把锚点放宽为【前缀匹配】 '<div class="container'，
仅对“guides.json 有映射、但工具页无 data-guide-link”的页面补链，产出与 _build.py 意图一致，
确保未来 rebuild（若 _build.py 锚点同步放宽）不产生 diff。幂等：已含 data-guide-link 的跳过。

用法：python3 scripts/inject_missing_guide_links.py
"""
import json, io, os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def esc_html_py(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def guide_backlinks(guide_url, cat, basename):
    """校验指南页正文是否反链到 tools/<cat>/<basename>。

    跨行业重名（如 calc-3.html 同时存在于 nutrition/cardiology/fitness/math/edu/health）
    无法仅凭文件名判断归属，必须用指南页自身的反链消歧。
    """
    gname = os.path.basename(guide_url or '')
    if not gname:
        return False
    gpath = os.path.join(ROOT, 'guides', gname)
    if not os.path.exists(gpath):
        return False
    try:
        with io.open(gpath, encoding='utf-8') as f:
            return ('tools/%s/%s' % (cat, basename)) in f.read()
    except Exception:
        return False


def main():
    guide_path = os.path.join(ROOT, 'json', 'guides.json')
    with io.open(guide_path, encoding='utf-8') as f:
        guides = json.load(f)

    # basename -> [(guide_url, title), ...]
    # 旧实现用 GUIDE_MAP[_gt] = ... 直接赋值，跨行业重名时后写入的分类会覆盖前面的，
    # 再配合 tool_html[basename] 仅存 glob 最后一个路径，导致「A 行业指南链注入 B 行业页面」。
    GUIDE_MAP = {}
    for _g in guides:
        _gt = _g.get('tool')
        if not _gt:
            continue
        _title = _g.get('title', '') or ''
        if _title and '使用指南' not in _title:
            _title = _title + '使用指南'
        GUIDE_MAP.setdefault(_gt, []).append((_g.get('guide', ''), _title))

    # 统计每个文件名在全站出现次数：>1 说明跨行业重名，仅靠文件名无法判断归属
    BASENAME_COUNT = {}
    for fn in glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True):
        _b = os.path.basename(fn)
        if _b == 'index.html':
            continue
        BASENAME_COUNT[_b] = BASENAME_COUNT.get(_b, 0) + 1

    injected = skipped = no_anchor = mismatch = 0
    # 遍历工具页（而非 GUIDE_MAP），每个页面按自身【分类 + 文件名】取候选，避免重名覆盖
    for fn in sorted(glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True)):
        _tb = os.path.basename(fn)
        if _tb == 'index.html':
            continue
        cat = os.path.basename(os.path.dirname(fn))
        with io.open(fn, encoding='utf-8') as f:
            content = f.read()
        if 'data-guide-link' in content:
            skipped += 1
            continue
        cands = [c for c in (GUIDE_MAP.get(_tb) or []) if c[0]]
        if not cands:
            continue
        # 始终优先用指南页反链消歧（唯一可靠判据）
        _g_url = _g_title = None
        for (gu, gt) in cands:
            if guide_backlinks(gu, cat, _tb):
                _g_url, _g_title = gu, gt
                break
        if not _g_url:
            # 无候选反链本页：仅当该文件名全站唯一（无跨行业重名）时才安全
            if len(cands) == 1 and BASENAME_COUNT.get(_tb, 0) == 1:
                _g_url, _g_title = cands[0]
            else:
                mismatch += 1
                print('  - 无法确认归属，跳过:', cat + '/' + _tb)
                continue
        _g_title_esc = esc_html_py(_g_title)
        gl_html = '\n<div class="tool-guide-link" data-guide-link="1">\n  <a href="%s">📖 查看「%s」</a>\n</div>\n' % (_g_url, _g_title_esc)
        # 锚点：优先 <div class="container...">（V2/旧模板均兼容），回退 <div class="card">
        m = re.search(r'<div class="container[^"]*">', content)
        if m:
            content = content[:m.start()] + gl_html + content[m.start():]
        elif '<div class="card">' in content:
            content = content.replace('<div class="card">', gl_html + '<div class="card">', 1)
        else:
            no_anchor += 1
            print('  ! 无插入锚点，跳过:', cat + '/' + _tb)
            continue
        with io.open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        injected += 1
        print('  + 注入回链:', cat + '/' + _tb)

    print('完成：注入 %d，已存在跳过 %d，无锚点跳过 %d，重名跳过 %d'
          % (injected, skipped, no_anchor, mismatch))


if __name__ == '__main__':
    main()
