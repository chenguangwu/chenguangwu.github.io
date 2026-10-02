#!/usr/bin/env python3
# gen_electromagnetism_head.py — shared head for electromagnetism batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electromagnetism')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electromagnetism')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "This tool provides auxiliary calculations for electromagnetics and circuit fundamentals. Results are for educational and preliminary design reference only, and do not replace formal engineering design, EMC standards, or the judgment of a certified engineer."
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
    out = {'slug': slug, 'industry': 'electromagnetism', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('solenoid-field', build('solenoid-field', [
        "Inside a solenoid (B = \u03bc\u2080\u00b7n\u00b7I)",
        "The field inside a long solenoid is proportional to turns per unit length and current.",
        "Solenoid Field Calculator",
        "/ Solenoid Field",
        "Solenoid Field",
        'View "Inside a solenoid (B = \u03bc\u2080\u00b7n\u00b7I)" guide',
        "Turn density (turns/m)",
        "B = \u03bc\u2080\u00b7n\u00b7I; n is turns per meter.",
        "At 1000 turns/m and 1 A, about 1.26 mT.",
        "Deep dive: Solenoid field",
        "Electromagnet: current creates a strong field (amplified \u03bc\u1d63 times with an iron core).",
        "MRI superconducting magnet: high n and I sustain a strong field.",
        "Solenoid valve / relay: controls pneumatics / contacts.",
        "Maglev: superconducting solenoid fields interact with track coils.",
        "n = 1000 turns/m, I = 5 A, air core",
        "B = 4\u03c0\u00d710\u207b\u2077\u00d71000\u00d75 \u2248 6.28 mT; with \u03bc\u1d63 = 5000 core \u2192 31.4 T (actual saturation limit ~1.6 T).",
        "Why is the end field about half?",
        DISCL,
        "Why does an iron core amplify the field?",
        DISCL,
        "Magnetic flux density and",
        "magnetic field strength",
        "relationship?",
        DISCL,
    ]))

if __name__ == "__main__":
    main()
