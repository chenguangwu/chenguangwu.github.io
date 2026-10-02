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
# body_t_b2.py
def main():
    write('convective-heat-rate', build('convective-heat-rate', [
        'Heat flux by Newton cooling law',
        'Enter the surface heat-transfer coefficient, area and temperature difference to find the convective heat-transfer power.',
        'Convective Heat Rate Calculator',
        '/ Convective Heat Rate Calculator',
        'View "Heat flux by Newton cooling law" guide',
        'Deep dive: Convective heat rate',
        'Surface convective heat flow under Newton cooling law.',
        'Estimate heat exchange at radiators and heat-exchanger surfaces.',
        'Linked with heat-transfer coefficient, area and temperature difference.',
        'Enhanced heat transfer',
        'h 10->25: q rises to 1000 W.',
        'How is h determined?',
        'Determined by flow and geometry; natural convection is about 5-25, forced convection can reach hundreds of W/m2K.',
        'Is it steady state?',
        'This is steady-state surface heat flux; transient cases must include heat capacity.',
    ]))
    write('cp-cv-ratio', build('cp-cv-ratio', [
        'Find specific-heat ratio from constant-pressure specific heat',
        'Enter constant-pressure specific heat cp and gas constant to find constant-volume specific heat and ratio gamma.',
        'Specific-Heat Ratio gamma Calculator',
        '/ Specific-Heat Ratio gamma Calculator',
        'View "Find specific-heat ratio from constant-pressure specific heat" guide',
        'gamma = cp/cv, cv = cp - R. For air cp=1005, R=287 -> gamma~1.40.',
        'Constant-pressure specific heat cp (J/(kg K))',
        'For air cp=1005, R=287 -> gamma~1.40.',
        'Deep dive: Specific-heat ratio gamma',
        'Find constant-volume specific heat cv from cp and the gas constant.',
        'Compute gamma=cp/cv for use in adiabatic processes.',
        'Convert among ideal-gas constants.',
        'Air cp=1005',
        'Diatomic gas',
        'At room temperature diatomic gamma~1.4, monatomic (helium) gamma~1.67.',
        'Where does the relation come from?',
        'For ideal gas cp-cv=R, gamma=cp/cv; knowing any two yields the third.',
        'Temperature effect?',
        'At high temperature cp increases slightly and gamma drops slightly; at room temperature it can be treated as constant.',
    ]))
    write('diesel-efficiency', build('diesel-efficiency', [
        'Ideal diesel engine (constant-pressure heat addition) thermal efficiency',
        'Enter the compression ratio r, cutoff ratio rho and specific-heat ratio gamma to find the Diesel cycle efficiency.',
        'Diesel Cycle Efficiency Calculator',
        '/ Diesel Cycle Efficiency Calculator',
        'View "Ideal diesel engine (constant-pressure heat addition) thermal efficiency" guide',
        'Cutoff ratio rho',
        'Deep dive: Ideal diesel cycle efficiency',
        'Diesel cycle (constant-pressure heat addition)',
        'thermal efficiency',
        'estimation.',
        'Effects of compression ratio and cutoff ratio on efficiency.',
        'Compare with the Otto cycle.',
        'Compression ratio 18, cutoff ratio 2',
        'Increase compression ratio',
        'r 18->22: eta rises to about 65.6%.',
        'Compare with Otto?',
        'At the same compression ratio Otto (constant-volume heat addition) is more efficient; the diesel wins via a much higher compression ratio.',
        'What about the cutoff ratio?',
        'rho = volume at end of constant-pressure heating / volume at end of compression; a larger rho lowers efficiency.',
    ]))
    write('entropy-change', build('entropy-change', [
        'Entropy change (DeltaS = Q_rev / T)',
        'For a reversible phase change or heat-transfer process, the entropy change equals the reversible heat divided by temperature.',
        'Reversible Entropy Change Calculator',
        '/ Entropy change calculation',
        'Entropy change calculation',
        'View "Entropy change (DeltaS = Q_rev / T)" guide',
        'Reversible heat (J)',
        'DeltaS = Q_rev / T; at water boiling point 373.15 K the vaporization entropy is about 11.2 J/K.',
        'Deep dive: Entropy change of a reversible process',
        'Entropy change under reversible heat transfer DeltaS=Q/T.',
        'Entropy change for phase transitions (melting, vaporization).',
        'Links with the entropy-increase principle of isolated systems.',
        'Vaporization at 100C',
        'Q=4186 J (latent heat to vaporize 1g water), T=373.15 K: DeltaS=4186/373.15=11.22 J/K.',
        'Melting at 0C',
        'Which T to use?',
        'A reversible phase change occurs at constant temperature T, so use this absolute temperature in K.',
        'Irreversible heat transfer?',
        'When irreversible, DeltaS > Q/T; the state-function difference must be computed along a reversible path.',
    ]))
    write('entropy-generation', build('entropy-generation', [
        'Find entropy generation from system and surroundings entropy change',
        'Enter the system entropy change and heat-source entropy change to find entropy generation (should be >=0).',
        'Entropy Generation Calculator',
        '/ Entropy Generation Calculator',
        'View "Find entropy generation from system and surroundings entropy change" guide',
        'S_gen = DeltaS_sys + DeltaS_surr >= 0. System +10, surroundings -9 -> S_gen=+1.',
        'System entropy change DeltaS_sys (J/K)',
        'Surroundings entropy change DeltaS_surr (J/K)',
        'System +10, surroundings -9 -> S_gen=+1.',
        'Deep dive: Entropy generation',
        'Whether the sum of system and surroundings entropy changes is non-negative.',
        'Check whether a process satisfies the second law.',
        'Quantify irreversibility (larger entropy generation means larger loss).',
        'System +10, surroundings -9',
        'DeltaS_sys=10, DeltaS_surr=-9 J/K: S_gen=10+(-9)=1 J/K>=0, satisfying the second law.',
        'Violation case',
        'If S_gen<0 the process cannot occur (e.g. heat spontaneously flowing from cold to hot).',
        'Statement of the second law?',
        'The total entropy of an isolated system does not decrease; S_gen>=0 is the criterion for process feasibility.',
        'Entropy generation and loss?',
        'Entropy generation corresponds to lost work capability (T0 S_gen); it measures exergy destruction.',
    ]))
if __name__ == '__main__':
    main()
