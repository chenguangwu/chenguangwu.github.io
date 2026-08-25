#!/usr/bin/env python3
"""B5-04: disambiguate the 10 duplicate tool titles found by qa_gates.py.

Appends a trailing parenthetical qualifier to the <title> (and matching
og:title / twitter:title) of one member of each duplicate group. calc()
reads input IDs, not the title, so this is safe for tool logic.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# file -> qualifier to append
FIX = {
    'tools/statistics/statistics-14.html': '统计',
    'tools/marketing/sample-size.html': '统计',
    'tools/eco/rainwater-harvest.html': '环保',
    'tools/eco/eco-12.html': '通用',
    'tools/energy/calc-area.html': '能源',
    'tools/healthcare/bsa.html': '标准',
    'tools/healthcare/bmi.html': '基础',
    'tools/eco/eco-2.html': '通用',
    'tools/eco/eco-13.html': '通用',
    'tools/pr/sentiment-analysis.html': '舆情',
    'tools/ai/ai-2.html': '通用',
    'tools/ai/ai-3.html': '通用',
}

def fix(fp, q):
    p = os.path.join(ROOT, fp)
    c = open(p, encoding='utf-8').read()
    orig = c
    # <title>base - ToolBox</title>
    def add_paren(m):
        return f'<title>{m.group(1)}（{q}） - ToolBox</title>'
    c = re.sub(r'<title>(.+?)\s*-\s*ToolBox\s*</title>', add_paren, c, count=1)
    # og:title / twitter:title content="base"
    def add_prop(m):
        return f'{m.group(1)}content="{m.group(2)}（{q}）"'
    c = re.sub(r'(property="og:title"\s+content=")([^"]+)(")', add_prop, c, count=1)
    c = re.sub(r'(name="twitter:title"\s+content=")([^"]+)(")', add_prop, c, count=1)
    if c != orig:
        open(p, 'w', encoding='utf-8').write(c)
        print('fixed', fp)
    else:
        print('NO CHANGE', fp)

for fp, q in FIX.items():
    fix(fp, q)
