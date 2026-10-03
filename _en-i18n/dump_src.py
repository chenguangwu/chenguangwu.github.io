#!/usr/bin/env python3
# usage: python3 dump_src.py slug1 slug2 ...
# prints ordered effective source strings (the ones to translate) per slug.
import os, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'metalwork')
for slug in sys.argv[1:]:
    p = os.path.join(WORK, slug + '.json')
    if not os.path.exists(p):
        print('### %s : MISSING WORK FILE' % slug)
        continue
    d = json.load(open(p, encoding='utf-8'))
    items = d.get('items', [])
    print('### %s  (name=%s, count=%d)' % (slug, d.get('name',''), len(items)))
    for i, it in enumerate(items):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src']
            tag = 'SRC'
        else:
            z = it.get('zh', '')
            tag = 'zh '
        z = (z or '').strip()
        if z == '':
            z = '<EMPTY>'
        z = z.replace('\n', '\\n')
        print('%03d|%s|%s' % (i+1, tag, z))
    print()
