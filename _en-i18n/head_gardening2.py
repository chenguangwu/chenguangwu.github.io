#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gardening2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gardening2')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
# 行业 phrases 字典（i18n/tools/gardening2-phrases.json）按「整节点 textContent」匹配
# <p>，而 per-tool 字典先译了 <p> 内的 <strong> 标签（花前修剪 等筛选按钮同串），
# 导致整串失配、剩下的「：…」碎片变残留（且随 fetch 竞态时有时无）。
# 兜底：把碎片本身也写进 per-tool 字典，两种顺序都出英文。
EXTRA = {
    'pruning-time': {
        '：在花芽分化前进行，促进花芽形成，适合夏季开花植物':
            ': done before flower bud differentiation, promoting bud formation; suited to summer-flowering plants',
        '：花谢后立即修剪，去除残花促进二次开花或来年花芽':
            ': prune right after the blooms fade, removing spent flowers to encourage a second flush or next year’s flower buds',
        '：落叶后至萌芽前（冬季）进行，修剪量可较大':
            ': carried out from leaf fall until bud break (winter), when a heavier cut is acceptable',
    },
}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'gardening2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
