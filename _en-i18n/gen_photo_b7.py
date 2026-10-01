#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""photo 第7批：safe-shutter（收尾剩余 slug）"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'photo')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'photo')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
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
    out = {'slug': slug, 'industry': 'photo', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- safe-shutter (19) ----------------
write('safe-shutter', build('safe-shutter', [
    "\U0001F3CE\uFE0F Safe Shutter Speed",
    "Estimate the safe handheld shutter that avoids blur.",
    '\U0001F4D6 View the "Safe Shutter Speed User Guide"',
    "Stabilization stops",
    "Safe shutter ~ 1 / (focal length x crop factor)",
    "Below this speed hand shake blurs; stabilization can relax it.",
    "\U0001F4DA Deep Dive: Safe Shutter Calculation",
    "Find the fastest shake-free handheld shutter from focal length.",
    "Relax via stabilization stops",
    "Safe shutter",
    "Low-light handheld settings.",
    "50mm: safe shutter = 1/50s (denominator ~ focal length); 200mm needs 1/200s, longer focal length shakes more easily.",
    "Stabilization relaxes",
    "5-stop stabilization: safe shutter = 1/(50 x 2^5) = 1/1600s, theoretically slower; in practice conservatively use 1/(focal length x stops) at 1/400s.",
    "What is the safe-shutter rule?",
    "Handheld fastest shutter denominator ~ focal length (full-frame equiv); stabilization relaxes 2-5 stops but not absolute, still depends on steady hands and stance.",
    "Should the crop factor be counted?",
    "Yes, use",
    ", e.g. APS-C 50mm is equivalent 75mm so safe at 1/75s is steadier.",
]))
