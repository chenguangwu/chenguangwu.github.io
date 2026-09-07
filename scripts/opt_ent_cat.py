#!/usr/bin/env python3
# 修正 ent 批 cat 错标：engineer/calculator 改 health/reference/validator
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'ent')

FIX = {
    'analysis-13.html': 'reference',
    'eustachian-tube.html': 'validator',
    'grbas-scale.html': 'reference',
    'laryngeal-nerve.html': 'reference',
    'caloric-test.html': 'reference',
    'hearing-loss-classification.html': 'health',
    'nasal-resistance.html': 'validator',
    'tympanic-perforation.html': 'reference',
}

n = 0
for fn, newcat in FIX.items():
    p = os.path.join(TOOLS, fn)
    html = open(p, encoding='utf-8').read()
    new_html, cnt = re.subn(r'cat=(calculator|engineer)', 'cat=' + newcat, html)
    if cnt:
        open(p, 'w', encoding='utf-8').write(new_html)
        n += 1
        print('FIX', fn, '-> cat=' + newcat, '(%d处)' % cnt)
    else:
        print('NOCHANGE', fn)
print('total fixed:', n)
