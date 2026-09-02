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


def main():
    guide_path = os.path.join(ROOT, 'json', 'guides.json')
    with io.open(guide_path, encoding='utf-8') as f:
        guides = json.load(f)

    GUIDE_MAP = {}
    for _g in guides:
        _gt = _g.get('tool')
        if not _gt:
            continue
        _title = _g.get('title', '') or ''
        if _title and '使用指南' not in _title:
            _title = _title + '使用指南'
        GUIDE_MAP[_gt] = (_g.get('guide', ''), _title)

    tool_html = {}
    for fn in glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True):
        tool_html[os.path.basename(fn)] = fn

    injected = skipped = no_anchor = 0
    for _tb, (_g_url, _g_title) in GUIDE_MAP.items():
        html_path = tool_html.get(_tb)
        if not html_path:
            continue
        with io.open(html_path, encoding='utf-8') as f:
            content = f.read()
        if 'data-guide-link' in content:
            skipped += 1
            continue
        if not _g_url:
            skipped += 1
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
            print('  ! 无插入锚点，跳过:', _tb)
            continue
        with io.open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        injected += 1
        print('  + 注入回链:', _tb)

    print('完成：注入 %d，已存在跳过 %d，无锚点跳过 %d' % (injected, skipped, no_anchor))


if __name__ == '__main__':
    main()
