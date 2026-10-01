#!/usr/bin/env python3
# gen_materials_b7.py — materials b7 (1 slug, closing)
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'materials')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'materials')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}

def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'materials', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

PRC = [
 "Poisson's Ratio from Lateral and Axial Strain",
 "Enter lateral strain ε_lat and axial strain ε_ax to find Poisson's ratio.",
 "Poisson's Ratio Calculator",
 "/ Poisson's Ratio Calculator",
 "📖 View Guide: Poisson's Ratio from Lateral and Axial Strain",
 "Lateral strain ε_lat",
 "Axial strain ε_ax",
 "📚 In Depth: Poisson's Ratio Calculation",
 "Lateral contraction characteristics",
 "Finite element parameter",
 "nu = - epsilon_lat / epsilon_ax. Under tension the axial direction elongates while the lateral direction thins; Poisson's ratio describes this ratio. Metals ≈ 0.3, rubber ≈ 0.5, cork ≈ 0.",
 "For isotropic linear-elastic materials nu ranges from -1 to 0.5; 0.5 is incompressible (e.g. rubber), negative values indicate auxetic materials (rare).",
 "Can Poisson's ratio exceed 0.5?",
 "Ordinary materials cannot (it would violate volumetric positive definiteness); 0.5 is the upper bound for isotropic incompressibility. Special auxetic materials have nu < 0 (lateral expansion under tension).",
 "Why is rubber close to 0.5?",
 "Rubber is nearly incompressible, its volume barely changes, so axial elongation must be compensated by lateral contraction, hence nu → 0.5.",
]

write('poisson-ratio-calc', build('poisson-ratio-calc', PRC))
