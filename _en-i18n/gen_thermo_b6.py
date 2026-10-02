#!/usr/bin/env python3
# gen_thermo_head.py — shared head for thermodynamics batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'thermodynamics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'thermodynamics')
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
    out = {'slug': slug, 'industry': 'thermodynamics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# body_t_b6.py
def main():
    write('stefan-boltzmann', build('stefan-boltzmann', [
        'Radiant power (P = epsilon sigma A T^4)',
        'Total blackbody radiation power is proportional to the fourth power of absolute temperature.',
        'Stefan-Boltzmann Radiation Calculator',
        '/ Blackbody Radiation Power',
        'Blackbody Radiation Power',
        'View "Radiant power (P = epsilon sigma A T^4)" guide',
        'P = epsilon sigma A T^4, sigma = 5.67x10^-8 W/(m2 K^4). A 300 K blackbody is about 459 W/m2.',
        'Emissivity',
        'Surface area (m2)',
        'A 300 K blackbody is about 459 W/m2.',
        'Deep dive: Stefan-Boltzmann radiation',
        'Net radiation power of blackbody/gray body P=epsilon sigma A T^4.',
        'Radiation heat-loss estimation for high-temperature surfaces.',
        'Combine with convection and conduction for total heat loss.',
        'Blackbody 300K 1m2',
        'Marked temperature rise',
        'T 300->600: P grows 16x (T^4) reaching 7350 W.',
        'What value for epsilon?',
        'Blackbody epsilon=1, real surfaces 0.1-0.95; polished metal low, rough high.',
        'Net radiation?',
        'Net exchange with the environment must use (T^4 - T_surr^4); here it is the self-emission.',
    ]))
    write('thermal-resistance-series', build('thermal-resistance-series', [
        'Total thermal resistance and heat flow of a double-layer composite wall',
        'Enter the thickness, conductivity and area of both layers to find the total thermal resistance and heat flow under a total temperature difference.',
        'R = L / (k A) (summed in series)',
        '/ Multilayer Plane-Wall Thermal Resistance Calculator',
        'Multilayer Plane-Wall Thermal Resistance Calculator',
        'View "Total thermal resistance and heat flow of a double-layer composite wall" guide',
        'R=R1+R2, U=1/R_total. An insulation+brick wall example yields a low U value.',
        'Layer1 thickness L1 (m)',
        'Layer1 conductivity k1 (W/(m K))',
        'Layer2 thickness L2 (m)',
        'Layer2 conductivity k2 (W/(m K))',
        'In series R=R1+R2, U=1/R_total.',
        'An insulation+brick wall example yields a low U value.',
        'Deep dive: Series thermal resistance',
        'Total thermal resistance of a multilayer plane wall R=sum L/(kA).',
        'Composite wall and insulation-layer design.',
        'Find heat flow q=DeltaT/sum R from the total temperature difference.',
        'Insulation + metal layer',
        'Thicken insulation',
        'L1 0.1->0.2: R_tot=4.7 K/W, heat flow halved.',
        'Analogous to circuits?',
        'Series thermal resistance is like series resistance; the total temperature difference is divided by resistance and the heat flow is equal everywhere.',
        'Contact thermal resistance?',
        'Real multilayers have contact thermal resistance; design usually leaves a margin.',
    ]))
if __name__ == '__main__':
    main()
