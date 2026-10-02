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
# body_t_b4.py
def main():
    write('humid-air-enthalpy', build('humid-air-enthalpy', [
        'Humid-air enthalpy (h = 1.006t + w(2501 + 1.86t))',
        'The specific enthalpy of humid air is determined by dry-bulb temperature and humidity ratio.',
        'Humid Air Enthalpy Calculator',
        '/ Humid Air Enthalpy',
        'Humid Air Enthalpy',
        'View "Humid-air enthalpy (h = 1.006t + w(2501 + 1.86t))" guide',
        'Dry-bulb temperature (C)',
        'Humidity ratio (kg/kg)',
        'h = 1.006t + w(2501 + 1.86t), where w is the humidity ratio kg/kg dry air.',
        'At 25C, w=0.01, about 50.6 kJ/kg.',
        'Deep dive: Humid-air enthalpy',
        'Specific enthalpy calculation of humid air in air-conditioning and drying processes.',
        'Data linkage with the psychrometric chart (h-d diagram).',
        'Energy accounting for humidification/cooling processes.',
        '25C, humidity 0.01',
        'Higher humidity',
        'w 0.01->0.02: h~75.7 kJ/kg, latent heat dominates.',
        'Where does 2501 come from?',
        'The latent heat of vaporization of water at 0C is about 2501 kJ/kg, and 1.86 is the specific heat of water vapor.',
        'Uses?',
        'Air-conditioning processes follow constant enthalpy (adiabatic humidification) or isothermal lines; enthalpy is the core quantity.',
    ]))
    write('ideal-gas-pressure', build('ideal-gas-pressure', [
        'Ideal gas pressure (P = nRT / V)',
        'Find the gas pressure at a given volume from the ideal-gas equation of state.',
        'Ideal Gas Pressure Calculator',
        '/ Ideal Gas Pressure',
        'Ideal Gas Pressure',
        'View "Ideal gas pressure (P = nRT / V)" guide',
        '1 mol at STP (22.414 L) is about 101.3 kPa.',
        'Deep dive: Ideal gas equation of state',
        'Find ideal-gas pressure P=nRT/V from n, T, V.',
        'Estimate pressure at standard state and in gas cylinders.',
        'Used together with Boyle/Charles laws.',
        '1 mol at standard state',
        'Temperature rise',
        'T 273->373 K: P rises to 138.3 kPa.',
        'What unit for V?',
        'Use m3 (not L), R=8.314 J/molK; when using L, R=8.314 L kPa/molK.',
        'Applicability?',
        'Approximates ideal at low pressure and high temperature; real-gas equations are needed at high pressure or near liquefaction.',
    ]))
    write('isothermal-work', build('isothermal-work', [
        'Isothermal expansion work (W = nRT ln(V2/V1))',
        'Reversible isothermal expansion of an ideal gas does work on the surroundings.',
        'Isothermal Expansion Work Calculator',
        '/ Isothermal Expansion Work',
        'Isothermal Expansion Work',
        'View "Isothermal expansion work (W = nRT ln(V2/V1))" guide',
        'W = nRT ln(V2/V1); doubling volume gives work = nRT ln2. Example about 1.73 kJ.',
        'Final volume (L)',
        'W = nRT ln(V2/V1); doubling volume gives work = nRT ln2.',
        'Example about 1.73 kJ.',
        'Deep dive: Isothermal expansion work',
        'Volume work of ideal-gas isothermal reversible process W=nRT ln(V2/V1).',
        'Energy estimation for isothermal compression/expansion.',
        'Compare with adiabatic work (isothermal work is larger).',
        'V2/V1=0.5: W=-1729 J (work done on the gas).',
        'Why is isothermal work larger than adiabatic?',
        'Isothermal needs heat absorption to maintain temperature, doing more work outward.',
        'Reversible condition?',
        'The process must be infinitely slow and frictionless; actual values are slightly smaller.',
    ]))
    write('latent-heat', build('latent-heat', [
        'Latent heat (Q = m L)',
        'Heat absorbed or released during a phase change (melting/vaporization).',
        'Phase-Change Latent Heat Calculator',
        '/ Phase-Change Latent Heat',
        'Phase-Change Latent Heat',
        'View "Latent heat (Q = m L)" guide',
        'Latent heat (J/kg)',
        'Q = m L; the latent heat of fusion of ice is 3.34x10^5 J/kg.',
        'Melting 1 kg of ice needs 334 kJ.',
        'Deep dive: Phase-change latent heat',
        'Latent heat of melting, vaporization, solidification Q=mL.',
        'Load estimation for refrigeration and heat pumps.',
        'Add with sensible heat for the total heat.',
        '1 kg ice melting',
        'Water boiling',
        'L=2.26e6 (vaporization): boiling 1 kg of water absorbs 2260 kJ.',
        'Temperature during phase change?',
        'Phase change occurs at constant temperature; latent heat changes phase but not temperature.',
        'Difference from sensible heat?',
        'Sensible heat Q=mc DeltaT changes temperature; latent heat changes phase.',
    ]))
    write('linear-expansion', build('linear-expansion', [
        'Linear expansion (DeltaL = alpha L0 DeltaT)',
        'A solid elongates along its length when heated, related to the linear-expansion coefficient, original length and temperature rise.',
        'Linear Thermal Expansion Calculator',
        '/ Linear Thermal Expansion',
        'Linear Thermal Expansion',
        'View "Linear expansion (DeltaL = alpha L0 DeltaT)" guide',
        'DeltaL = alpha L0 DeltaT; for steel alpha~1.2x10^-5 /K. A 1 m steel bar at +50C elongates about 0.6 mm.',
        'Original length (mm)',
        'Temperature rise (K)',
        'DeltaL = alpha L0 DeltaT; for steel alpha~1.2x10^-5 /K.',
        'A 1 m steel bar at +50C elongates about 0.6 mm.',
        'Deep dive: Linear expansion',
        'Length change of a solid due to temperature DeltaL=alpha L0 DeltaT.',
        'Expansion-joint design for bridges and rails.',
        'Thermal strain',
        'linked (epsilon=alpha DeltaT).',
        'Steel 1000mm, +50C',
        'Longer member',
        'L0 1->10 m: DeltaL=6 mm; expansion joints must be provided.',
        'Different materials?',
        'Steel alpha~1.2e-5, aluminum~2.3e-5,',
        'When constrained?',
        'Free expansion only deforms; if constrained it turns into thermal stress sigma=E alpha DeltaT.',
    ]))
if __name__ == '__main__':
    main()
