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
# body_t_b5.py
def main():
    write('lmtd-heat-exchanger', build('lmtd-heat-exchanger', [
        'Heat-exchanger mean temperature difference',
        'Enter the two end temperature differences DeltaT1, DeltaT2 to find the log-mean temperature difference.',
        'Log-Mean Temperature Difference Calculator',
        '/ Log-Mean Temperature Difference Calculator',
        'View "Heat-exchanger mean temperature difference" guide',
        'LMTD=(DeltaT1-DeltaT2)/ln(DeltaT1/DeltaT2). 60 and 30 -> 43.3 K.',
        'End1 temperature difference DeltaT1 (K)',
        'End2 temperature difference DeltaT2 (K)',
        '60 and 30 -> 43.3 K.',
        'Deep dive: Log-mean temperature difference',
        'Heat-exchanger mean temperature difference LMTD=(DeltaT1-DeltaT2)/ln(DeltaT1/DeltaT2).',
        'Heat-transfer area estimation for shell-and-tube and plate exchangers.',
        'Compare with the effectiveness-NTU method.',
        'End differences 60/30C',
        'More uniform end differences',
        'DeltaT1=40, DeltaT2=30: LMTD=34.7 C, close to the arithmetic mean.',
        'Why use the log-mean?',
        'The temperature difference varies nonlinearly along the path; the arithmetic mean overestimates, while LMTD is more accurate.',
        'Counterflow/parallel flow?',
        'Counterflow gives a larger LMTD and is more compact; the formula is the same but the end differences are taken differently.',
    ]))
    write('newton-cooling', build('newton-cooling', [
        'Temperature decay by the lumped-parameter method',
        'Enter initial temperature, ambient temperature, time constant k and time to find the current temperature.',
        'Newton Cooling Time Calculator',
        '/ Newton Cooling Time Calculator',
        'View "Temperature decay by the lumped-parameter method" guide',
        'k=0.05/min, 30min -> about 40C.',
        'Initial temperature T0 (C)',
        'Ambient temperature Tinf (C)',
        'Cooling constant k (1/min)',
        'Deep dive: Newton cooling (transient temperature)',
        'Exponential approach of an object cooling/heating toward ambient temperature.',
        'Cooling-time estimation for food and equipment.',
        'Paired with the lumped-parameter method (Bi<0.1).',
        '100C, k=0.05, cool 30s',
        'Slower cooling',
        'k 0.05->0.02: after 30s T~82.1 C.',
        'What is k?',
        'Cooling constant k=hA/(mc), involving convection and heat capacity; larger k means faster cooling.',
        'Applicable premise?',
        'Requires Bi<0.1 (internal isothermal); otherwise use a non-lumped model.',
    ]))
    write('otto-efficiency', build('otto-efficiency', [
        'Ideal gasoline engine (constant-volume heat addition) thermal efficiency',
        'Enter the compression ratio r and specific-heat ratio gamma to find the Otto cycle thermal efficiency.',
        'Otto Cycle Efficiency Calculator',
        '/ Otto Cycle Efficiency Calculator',
        'View "Ideal gasoline engine (constant-volume heat addition) thermal efficiency" guide',
        'Deep dive: Otto cycle efficiency',
        'Ideal constant-volume heat-addition cycle efficiency of a gasoline engine eta=1-1/r^(gamma-1).',
        'Effect of compression ratio on efficiency.',
        'Compare with the diesel cycle.',
        'Compression ratio 10',
        'Compression ratio 8',
        'Why raise the compression ratio?',
        'The larger r, the higher eta, but gasoline engines are limited by knock (typically <=12).',
        'Actual efficiency?',
        'Actual gasoline engine',
        'thermal efficiency',
        'about 30%-38%, far below the ideal value.',
    ]))
    write('polytropic-work', build('polytropic-work', [
        'Volume work of a polytropic process with index n',
        'Enter the initial/final pressure and volume and the polytropic index n to find the process work.',
        'Polytropic Process Work Calculator',
        '/ Polytropic Process Work Calculator',
        'View "Volume work of a polytropic process with index n" guide',
        'W=(P2 V2-P1 V1)/(1-n) (SI units). At n=1 it degenerates to isothermal and the ln form must be used instead.',
        'Initial pressure P1 (kPa)',
        'Initial volume V1 (m3)',
        'Final pressure P2 (kPa)',
        'Final volume V2 (m3)',
        'Polytropic index n',
        'W=(P2 V2-P1 V1)/(1-n) (SI units).',
        'At n=1 it degenerates to isothermal and the ln form must be used instead.',
        'Deep dive: Polytropic process work',
        'Volume work of an ideal-gas polytropic process (pV^n=C).',
        'Special cases: n=1 isothermal, n=gamma adiabatic, n=0 isobaric.',
        'Energy estimation for compression/expansion processes.',
        'Polytropic n=1.3 compression',
        'p1=100 kPa, v1=1, p2=60 kPa, v2=2, n=1.3: W=(p2 v2-p1 v1)/(1-n)=((60x2)-(100x1))x1000/(1-1.3)=(20000-100000)/(-0.3) ... using kPa m3: W=(120-100)/(-0.3)=-66.7 kJ (work done on the gas).',
        'Isothermal special case',
        'At n=1 and p1 v1=p2 v2, W=0 (ideal isothermal closure).',
        'Physical meaning of n?',
        'Polytropic index, describing the degree of heat exchange; during heating compression n lies between 1 and gamma.',
        'Meaning of negative work?',
        'During compression the gas volume decreases, work is done on the gas, so W is negative.',
    ]))
    write('specific-heat-q', build('specific-heat-q', [
        'Sensible heat (Q = m c DeltaT)',
        'Heat needed to raise an object temperature equals mass x specific heat x temperature rise.',
        'Specific-Heat Heat Calculator',
        '/ Specific-Heat Heat',
        'Specific-Heat Heat',
        'View "Sensible heat (Q = m c DeltaT)" guide',
        'Q = m c DeltaT; water specific heat is about 4186 J/(kg K). Raising 1 kg water by 10C needs 41.86 kJ.',
        'Specific heat (J/(kg K))',
        'Initial temperature (C)',
        'Final temperature (C)',
        'Q = m c DeltaT; water specific heat is about 4186 J/(kg K).',
        'Raising 1 kg water by 10C needs 41.86 kJ.',
        'Deep dive: Sensible-heat (specific-heat) exchange',
        'Sensible heat for heating/cooling an object Q=mc DeltaT.',
        'Heating/cooling load estimation.',
        'Add with latent heat for the total heat.',
        '1 kg water 20->30C',
        'Metal heats faster',
        'c=460 (steel): under the same conditions Q=4.6 kJ, heating much faster.',
        'c and phase?',
        'For the same substance liquid/solid/gas have different c; in the phase-change region use latent heat rather than specific heat.',
        'Variable specific heat?',
        'Over a large temperature span c varies slightly; for accurate calculation use integration or mean specific heat.',
    ]))
if __name__ == '__main__':
    main()
