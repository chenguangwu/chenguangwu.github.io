#!/usr/bin/env python3
# dump zh source strings per slug compactly for translation
import os, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'health')
for slug in sys.argv[1:]:
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    print('==== %s (%d) ====' % (slug, len(items)))
    for i, it in enumerate(items, 1):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src']
            tag = ' SD'
        else:
            z = it.get('zh', '')
            tag = ''
        print('[%d%s] %s' % (i, tag, z.replace('\n', ' \\n ')))
