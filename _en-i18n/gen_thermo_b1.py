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
# body_t_b1.py
def main():
    write('adiabatic-tv', build('adiabatic-tv', [
        'Reversible adiabatic T-V relation for ideal gas',
        'Enter the initial temperature/volume, final volume and specific-heat ratio gamma to find the final temperature.',
        'T V^(gamma-1) = constant',
        '/ Adiabatic process temperature calculator',
        'Adiabatic Process Temperature Calculator',
        'View "Reversible adiabatic T-V relation for ideal gas" guide',
        'Initial temperature T1 (K)',
        'Initial volume V1 (L)',
        'Final volume V2 (L)',
        '300K with doubled volume (gamma=1.4) -> T2~227.4 K.',
        'Deep dive: Adiabatic T-V relation',
        'For a reversible adiabatic expansion/compression of an ideal gas, temperature changes with volume.',
        'Estimate near-adiabatic processes in compressors and internal-combustion cylinders.',
        'Compare temperature drop magnitude with the isothermal process.',
        'Air adiabatic expansion 1->2 m3',
        'Compression heating',
        'V1/V2=2: T2=300x2^0.4~396 K; adiabatic compression heats up markedly.',
        'Why is the adiabatic temperature drop larger than the isothermal one?',
        'Adiabatic has no heat exchange, so cooling comes entirely from work done by the gas; isothermal keeps temperature by heat absorption, giving a smaller drop.',
        'What is the value of gamma?',
        'Diatomic gas (air) gamma~1.4, monatomic~1.67, polyatomic~1.3.',
        'How to use the reversible adiabatic T-V relation for ideal gas',
        'What does the reversible adiabatic T-V relation for ideal gas do?',
        'Enter the ideal-gas initial temperature and volume, the final volume and the specific-heat ratio gamma, then solve for the final temperature from the adiabatic equation T V^(gamma-1) = constant; used for reversible adiabatic estimation in compressors and expanders.',
        'How to use the reversible adiabatic T-V relation for ideal gas?',
        'Which scenarios suit the reversible adiabatic T-V relation for ideal gas?',
    ]))
    write('biot-number', build('biot-number', [
        'Check applicability of lumped-parameter method',
        'Enter the heat-transfer coefficient, characteristic length and thermal conductivity to find the Biot number Bi.',
        'Biot Number Calculator',
        '/ Biot Number Calculator',
        'View "Check applicability of lumped-parameter method" guide',
        'Bi = hL/k. Metallic small parts often satisfy Bi',
        'Bi = hL/k. The lumped-parameter method applies when Bi<0.1.',
        'Small metal parts often satisfy Bi<<1.',
        'Deep dive: Biot number',
        'Determine whether transient conduction can use the lumped-parameter method (Bi<0.1).',
        'Whether the interior temperature of a solid is uniform during heating/cooling.',
        'A large Bi requires considering the internal temperature gradient.',
        'Small steel ball h=50',
        'h=50 W/m2K, Lc=0.05 m, k=400: Bi=hLc/k=50x0.05/400=0.00625<0.1, lumped-parameter method applies.',
        'Large block, low conductivity',
        'k 400->4 (e.g. plastic), Bi=0.625>0.1, internal temperature gradient cannot be ignored.',
        'What is Lc?',
        'Characteristic length Lc=V/A (volume/surface area); for a sphere it is r/3.',
        'What does a small Bi mean?',
        'The conduction resistance is far smaller than the convection resistance, so the object interior is approximately isothermal.',
    ]))
    write('boyles-law', build('boyles-law', [
        'Boyle Law Calculator',
        'At constant temperature, ideal-gas pressure is inversely proportional to volume.',
        '/ Boyle Law',
        'Boyle Law',
        'View "Boyle Law Calculator" guide',
        'Isothermal pressure-volume (P1 V1 = P2 V2)',
        'Final pressure (kPa)',
        'P1 V1 = P2 V2 (isothermal).',
        'Halve the pressure and the volume doubles.',
        'Deep dive: Boyle law',
        'At constant temperature',
        'ideal-gas pressure',
        'is inversely proportional to volume.',
        'Estimate isothermal processes for balloons and pistons.',
        'With Charles/',
        'Gay-Lussac law',
        'used together.',
        'P2=200 kPa: V2=1 L, volume halved and pressure doubled.',
        'What are the applicable conditions?',
        'Ideal gas with constant temperature and mass; approximately valid at moderate pressure and room temperature.',
        'What about the Celsius scale?',
        'Absolute temperature must be used; the law is P1V1=P2V2 (same temperature).',
    ]))
    write('charles-law', build('charles-law', [
        'Charles Law Calculator',
        'At constant pressure, ideal-gas volume is proportional to thermodynamic temperature.',
        '/ Charles Law',
        'Charles Law',
        'View "Charles Law Calculator" guide',
        'Isobaric volume-temperature (V2 = V1 T2 / T1)',
        'V1/T1 = V2/T2; temperature must be in kelvin.',
        '0C->100C (isobaric) volume increases about 36.6%.',
        'Deep dive: Charles law',
        'At constant pressure, ideal-gas volume is proportional to absolute temperature.',
        'Estimate hot-air balloons and gas volume change with temperature.',
        'Boyle law',
        'combined yields',
        'cooling contraction',
        'T2=223 K: V2=0.816 L; volume decreases linearly with absolute temperature.',
        'Why use K?',
        'The proportion holds only for absolute temperature; at zero Celsius the gas still has volume.',
        'What about constant pressure?',
        'Pressure must be constant; otherwise combine with Boyle law.',
    ]))
    write('compressor-isentropic-work', build('compressor-isentropic-work', [
        'Ideal-gas isentropic specific compression work',
        'Enter the inlet temperature, pressure ratio, specific-heat ratio and gas constant to find the specific compression work.',
        'Isentropic Compression Work Calculator',
        '/ Isentropic Compression Work Calculator',
        'View "Ideal-gas isentropic specific compression work" guide',
        'Inlet temperature T1 (K)',
        'Pressure ratio P2/P1',
        'Air at 300K, pressure ratio 8 -> about 234 kJ/kg.',
        'Deep dive: Compressor isentropic specific work',
        'Isentropic specific technical work per unit mass for ideal-gas compression.',
        'Compressor energy estimation and pressure-ratio selection.',
        'Compare with polytropic/actual efficiency.',
        'Air pressure ratio 8',
        'Effect of pressure ratio',
        'PR 8->12: the exponential term grows and specific work rises to about 320 kJ/kg.',
        'What about actual power consumption?',
        'Actual w_actual = w_isentropic/eta_c, the',
        'Thermal efficiency',
        'Typically 0.7 to 0.85.',
        'Why does it grow with pressure ratio?',
        'A higher pressure ratio raises the pressure of a given mass more, and the work grows roughly logarithmically.',
        'How to use ideal-gas isentropic specific compression work',
        'What does ideal-gas isentropic specific compression work do?',
        'Enter inlet temperature T1, pressure ratio P2/P1, specific-heat ratio gamma and gas constant R to compute the ideal-gas isentropic specific compression work w; used for power estimation of compressors, refrigeration and gas-boosting equipment.',
        'How to use ideal-gas isentropic specific compression work?',
        'Which scenarios suit ideal-gas isentropic specific compression work?',
    ]))
if __name__ == '__main__':
    main()
