#!/usr/bin/env python3
# gen_quantum_head.py — shared head for quantum batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'quantum')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'quantum')
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
    out = {'slug': slug, 'industry': 'quantum', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('wien-displacement', build('wien-displacement', [
        "Relation between blackbody radiation peak wavelength and temperature.",
        "Wien's Displacement Law Calculator",
        "/ Wien's Displacement Law",
        "Wien's displacement law",
        "📖 View \"Wien's Displacement Law Calculator - User Guide\"",
        "Sun 5778 K -> peak approx 502 nm (green light).",
        "📚 In-depth: Wien's Displacement Law",
        "Peak wavelength of blackbody radiation.",
        "Infer stellar surface temperature.",
        "Determine thermal-radiation color.",
        "Sun 5778 K",
        "lambda_max = b/T = 2.898e-3/5778 = 5.02e-7 m = 502 nm (blue-green peak).",
        "Human body 310 K",
        "lambda_max = 9.35 um, peak in far infrared (thermal-camera working range).",
        "Constant b?",
        "Wien's displacement constant 2.898e-3 m K.",
        "Relation with Stefan's law?",
        "Both are derived from Planck's law: one fixes the peak position, the other fixes the total power.",
    ]))
    write('zeeman-splitting', build('zeeman-splitting', [
        "Find adjacent level splitting from magnetic field",
        "Enter magnetic flux density B to obtain the energy difference between adjacent Zeeman levels.",
        "Zeeman Splitting Energy Calculator",
        "/ Zeeman Splitting Energy Calculator",
        "📖 View \"Find Adjacent Level Splitting from Magnetic Field - User Guide\"",
        "B=1 T -> about 5.79 x 10^-5 eV.",
        "📚 In-depth: Zeeman Splitting",
        "Energy-level splitting in a magnetic field.",
        "Estimate magnetic-resonance frequency.",
        "Principle of atomic clocks / magnetometers.",
        "1 T magnetic field",
        "Corresponding Larmor frequency",
        "nu = Delta E/h = 9.27e-24/6.626e-34 = 14.0 GHz (electron spin resonance).",
        "Normal vs anomalous Zeeman?",
        "Normal Zeeman uses orbital magnetic moment; including spin (g=2) gives anomalous Zeeman with more complex splitting.",
        "Stronger magnetic field, more splitting?",
        "Delta E = mu_B B; the splitting grows linearly with the magnetic field.",
    ]))

if __name__ == '__main__':
    main()
