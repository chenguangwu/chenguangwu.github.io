#!/usr/bin/env python3
"""One-time: build scripts/_pinyin_map.json (char -> pinyin, no tone).

ToolBox build uses this map so pinyin search works without a runtime
pypinyin dependency. Regenerate after adding many new Chinese tool names.
"""
import os, json, re
from pypinyin import pinyin, Style

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_PATH = os.path.join(ROOT, 'scripts', '_pinyin_map.json')
IDX = os.path.join(ROOT, 'json', 'tools.json')

chars = set()
if os.path.exists(IDX):
    data = json.load(open(IDX, encoding='utf-8'))
    for t in data:
        chars.update(t.get('name', ''))
        chars.update(t.get('desc', ''))

# also scan tool page titles directly for completeness
import glob
for fp in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html')):
    try:
        c = open(fp, encoding='utf-8').read()
    except Exception:
        continue
    if 'TOOLBOX-REDIRECT' in c:
        continue
    m = re.search(r'<title>(.+?)\s*-\s*ToolBox\s*</title>', c) or re.search(r'<title>([^<]+)</title>', c)
    if m:
        chars.update(m.group(1))

# keep only CJK chars
cjk = [c for c in chars if '\u4e00' <= c <= '\u9fff']
res = {}
for ch in sorted(cjk):
    py = pinyin(ch, style=Style.NORMAL, heteronym=False)
    res[ch] = (py[0][0] if py and py[0] else '')

os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
json.dump(res, open(MAP_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('pinyin map chars:', len(res), '->', MAP_PATH)
