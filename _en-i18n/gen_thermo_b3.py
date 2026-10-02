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
# body_t_b3.py
def main():
    write('first-law', build('first-law', [
        'Internal energy change (DeltaU = Q - W)',
        'The system internal-energy change equals heat absorbed minus work done by the system.',
        'First Law of Thermodynamics Calculator',
        '/ First Law of Thermodynamics',
        'First Law of Thermodynamics',
        'View "Internal energy change (DeltaU = Q - W)" guide',
        'Heat absorbed (J)',
        'Work done by system (J)',
        'DeltaU = Q - W (heat into system positive, work by system positive).',
        'Heat 1000 J, work 400 J -> DeltaU=600 J.',
        'Deep dive: First law of thermodynamics (closed system)',
        'Energy conservation of a closed system DeltaU=Q-W.',
        'Internal-energy change under heat/work.',
        'Distinguish from the steady-flow energy equation.',
        'Heat 1000, work 400',
        'Q=1000 J, W=400 J: DeltaU=Q-W=1000-400=600 J, internal energy increases.',
        'Adiabatic compression',
        'Q=0, W=-500 (work on system): DeltaU=500 J, temperature rises.',
        'Sign of W?',
        'Conventionally work by the system is positive, so DeltaU=Q-W; some textbooks use the opposite sign.',
        'What does it apply to?',
        'Closed system (constant mass); open steady flow uses the enthalpy form.',
    ]))
    write('fourier-number', build('fourier-number', [
        'Dimensionless transient-conduction time scale',
        'Enter thermal diffusivity, time and characteristic length to find the Fourier number Fo.',
        'Fourier Number Calculator',
        '/ Fourier Number Calculator',
        'View "Dimensionless transient-conduction time scale" guide',
        'Fo = alpha t/L^2. After Fo>=0.2 the temperature profile approaches the regular regime.',
        'Thermal diffusivity alpha (m2/s)',
        'Deep dive: Fourier number',
        'Dimensionless time for transient conduction Fo=alpha t/L^2.',
        'Judge the progress of unsteady conduction.',
        'Biot number',
        'used together to read nomograms.',
        'Longer time',
        't 100->500 s: Fo=50, approaching steady state.',
        'What does a large Fo mean?',
        'The larger Fo, the more sufficient the conduction time and the closer the temperature field to steady state.',
        'What is alpha?',
        'thermal diffusivity',
        'alpha=k/(rho c), reflecting how fast a temperature change propagates.',
    ]))
    write('gay-lussac-law', build('gay-lussac-law', [
        'Gay-Lussac Law Calculator',
        'At constant volume, ideal-gas pressure is proportional to thermodynamic temperature.',
        '/ Gay-Lussac Law',
        'Gay-Lussac Law',
        'View "Gay-Lussac Law Calculator" guide',
        'Isochoric pressure-temperature (P2 = P1 T2 / T1)',
        'P1/T1 = P2/T2; temperature must be in kelvin.',
        '300 K->400 K pressure rises about 33.3%.',
        'Deep dive: Gay-Lussac law',
        'At constant volume',
        'ideal-gas pressure',
        'is proportional to absolute temperature.',
        'Estimate pressure rise in a sealed container when heated.',
        'Counterpart of Charles law (constant pressure).',
        'Cooling',
        'Difference from Charles?',
        'Gay-Lussac is constant-volume P~T, Charles is constant-pressure V~T.',
        'Container safety?',
        'A sealed container sees pressure rise linearly with heating and must be checked for pressure rating.',
    ]))
    write('grashof-number', build('grashof-number', [
        'Dimensionless number for natural-convection driving force',
        'Enter gravity, volumetric-expansion coefficient, temperature difference, characteristic length and kinematic viscosity to find Gr.',
        'Grashof Number Calculator',
        '/ Grashof Number Calculator',
        'View "Dimensionless number for natural-convection driving force" guide',
        'Gr = g beta DeltaT L^3/nu^2. Its ratio to Re^2 decides whether natural or forced convection dominates.',
        'Volumetric-expansion coefficient beta (1/K)',
        'Deep dive: Grashof number',
        'The ratio of buoyancy to viscous force in natural convection.',
        'Linked with natural-convection heat transfer (Gr Pr decides the flow regime).',
        'Works with the Rayleigh number Ra=Gr Pr.',
        'Vertical plate DeltaT=10K',
        'Larger temperature difference',
        'DeltaT 10->30: Gr increases to about 3.9x10^6.',
        'Relation with natural convection?',
        'A large Gr means strong buoyancy driving; laminar/turbulent is decided by Gr Pr (Ra).',
        'What is beta?',
        'Volumetric-expansion coefficient; for ideal gas beta=1/T, about 0.0033 for gas at room temperature.',
    ]))
    write('heat-conduction', build('heat-conduction', [
        'Heat-conduction rate (q = k A DeltaT / L)',
        'Steady 1-D conduction heat flow is proportional to temperature difference and area, and inversely proportional to thickness.',
        'Fourier Heat Conduction Calculator',
        '/ Fourier heat conduction',
        'Fourier heat conduction',
        'View "Heat-conduction rate (q = k A DeltaT / L)" guide',
        'q = k A DeltaT / L; aluminum conductivity is about 400 W/(m K). Example heat flow 4000 W.',
        'Thermal conductivity (W/(m K))',
        'Temperature difference (K)',
        'q = k A DeltaT / L; aluminum conductivity is about 400 W/(m K).',
        'Example heat flow 4000 W.',
        'Deep dive: 1-D conduction heat flow',
        'Fourier law for steady conduction through a plane wall q=kA DeltaT/L.',
        'Conduction estimation for walls and insulation layers.',
        'Linked with series thermal resistance.',
        'Copper plate k=400',
        'Switch to insulation',
        'k 400->0.04 (insulation wool): q drops to 0.4 W.',
        'Units?',
        'q is power (W), k is W/mK; mind the unit of thickness L.',
        'Multilayer wall?',
        'Use series thermal resistance R=L/(kA) summed; total q=DeltaT/sum R.',
        'How to use heat-conduction rate (q = k A DeltaT / L)',
        'What does heat-conduction rate (q = k A DeltaT / L) do?',
        'Enter thermal conductivity k, area A, temperature difference DeltaT and wall thickness L, then compute the 1-D steady conduction heat flow q by Fourier law; used for heat-transfer evaluation of walls, insulation and cladding structures.',
        'How to use heat-conduction rate (q = k A DeltaT / L)?',
        'Which scenarios suit heat-conduction rate (q = k A DeltaT / L)?',
    ]))
if __name__ == '__main__':
    main()
