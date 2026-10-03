#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'road')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'road')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
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
    out = {'slug': slug, 'industry': 'road', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- sight-distance (41) ----------------
    write('sight-distance', build('sight-distance', [
        "🧮 Sight Distance Calculator",
        "Stopping sight distance, passing sight distance and decision sight distance with code checks",
        "📖 Read the \"Sight Distance Calculator User Guide\"",
        "🛑 Stopping Sight Distance",
        "↔️ Passing Sight Distance",
        "🤔 Decision Sight Distance",
        "Perception-reaction time t (s)",
        "Longitudinal friction coefficient f",
        "Longitudinal grade G (%)",
        "Safety margin factor",
        "1.0 (no margin)",
        "1.2 (+20% wet pavement)",
        "Speed of overtaken vehicle v1 (km/h)",
        "Speed of passing vehicle v2 (km/h)",
        "Approaching vehicle speed v3 (km/h)",
        "Initial headway t1 (s)",
        "Passing occupancy time t2 (s)",
        "Decision type",
        "Stop (rural)",
        "Stop (urban)",
        "Speed/path change",
        "Complex intersection / ramp",
        "Sight distance",
        "Code minimum",
        "Reaction distance",
        "Braking distance",
        "SSD: stopping sight distance (m); V: design speed (km/h); t: perception-reaction time (s);",
        "f: longitudinal friction coefficient; G: longitudinal grade (%), positive uphill and negative downhill",
        "Tip: expressways and class-1 highways should meet stopping sight distance; two-lane class-2 to class-4 highways need passing sight distance; complex sections should meet decision sight distance.",
        "📚 Deep dive: Sight Distance Calculation",
        "Stopping sight distance SSD = reaction distance + braking distance = 0.278·V·t + V²/[254(f±G)], which guarantees a safe stop before an obstacle ahead and must be >= the code minimum (75 m at 60 km/h).",
        "Passing sight distance PSD = d1+d2+d3+d4 (initial acceleration, occupying the oncoming lane, safety gap, distance to the oncoming vehicle); two-lane highways must meet the code value (about 350 m at 60 km/h) for safe passing.",
        "Decision sight distance DSD = V·t/3.6 + V²/(2·a·3.6²), used at intersections and ramps where the driver must judge the path; the code value is higher than stopping sight distance.",
        "Reproducible example (stopping sight distance V=60, t=2.5 s, f=0.35, G=0)",
        "Reaction distance d1 = 0.278x60x2.5 = 41.7 m.\nBraking distance d2 = 60²/[254x(0.35+0)] = 3600/88.9 = 40.5 m.\nStopping sight distance SSD = (41.7+40.5)x1.0 (safety factor k=1) = 82.2 m.\nCode minimum (60 km/h) = 75 m, 82.2 >= 75 → satisfied.\nOn a downhill G=-0.03: d2 = 3600/[254x0.32] = 44.3 m, SSD ≈ 86.0 m, so downhill braking distance is longer.",
        "What value is usually taken for perception-reaction time t?",
        "Stopping sight distance typically takes t=2.5 s (covering perception plus reaction); 3 s may be used for elderly drivers or complex environments; decision sight distance needs to recognize the intersection and judge the path, so t ranges from 3 to 6 s. The larger t is, the longer the sight distance required, so conservative design takes the larger value.",
        "Why is sight distance shorter downhill?",
        "The denominator of the braking distance formula contains (f+G), and on a downhill G is negative, which shrinks the denominator and lengthens the braking distance; downhill sections therefore need longer sight distance or stronger braking assurance, so the design check should use the most adverse grade.",
        "About \"Sight Distance Calculator\"",
        "Road sight distance calculator - stopping sight distance, passing sight distance and decision sight distance calculation. Scientific tool using standard formulas, with accurate results.",
    ]))

    # ---------------- traffic-capacity (42) ----------------
    write('traffic-capacity', build('traffic-capacity', [
        "🛣️ Road Capacity",
        "Basic/possible/design capacity computation with V/C ratio and level of service (LOS) evaluation",
        "Capacity Calculation",
        "/ Capacity",
        "📖 Read the \"Road Capacity User Guide\"",
        "Road type",
        "Expressway / class 1",
        "Multi-lane highway",
        "Two-lane highway",
        "Signalized intersection",
        "Number of lanes in one direction N",
        "Heavy vehicle proportion PT (%)",
        "Heavy vehicle passenger car equivalent ET",
        "1.5 (flat terrain)",
        "2.0 (slight hills)",
        "3.0 (steep hills)",
        "Actual peak flow (pcu/h)",
        "Lateral clearance (m)",
        "0.5 (constrained)",
        "1.5 (ample)",
        "Driver correction factor fp",
        "0.85 (commuter / mixed)",
        "1.0 (experienced)",
        "Basic capacity",
        "Possible capacity",
        "Design capacity",
        "C0: basic capacity (pcu/h/ln); N: number of lanes; f_w: lane width / lateral clearance correction",
        "f_HV: heavy vehicle correction; f_p: driver correction; V/C: saturation ratio",
        "Design capacity = possible capacity x (V/C corresponding to the specified design level of service)",
        "Tip: level of service (LOS): class A is most free-flowing, class F is severe congestion. Expressway design usually takes class C (V/C <= 0.7), urban roads take class D (V/C <= 0.85).",
        "📚 Deep dive: Road Capacity",
        "Basic capacity C0 is looked up by road type and design speed (an expressway at 100 km/h with one lane is 2200 pcu/h), then multiplied by the number of lanes N to get the basic cross-section capacity.",
        "After correction for lane width f_w, heavy vehicles f_HV = 1/[1+PT(ET-1)] and drivers f_p, the possible capacity C is obtained; multiplying by the design V/C (0.7 for class C) gives the design capacity.",
        "Enter the actual flow q, compute the saturation ratio V/C = q/C, and check the LOS class (A < 0.35 free flowing ... E >= 1.0 congested) to judge the level of service; V/C > 0.85 requires capacity expansion.",
        "Reproducible example (expressway two lanes V=100, 3.5 m, cl=1.5, PT=15%, ET=2.0, q=2520)",
        "Basic capacity C0xN = 2200x2 = 4400 pcu/h.\nLane width correction f_w = 0.97 (3.5 m) x 1.0 (lateral >= 1.5 m) = 0.97.\nHeavy vehicle correction f_HV = 1/[1+0.15x(2.0-1)] = 1/1.15 = 0.870.\nPossible capacity C = 4400x0.97x0.870x1.0 = 3711 pcu/h.\nDesign capacity = 3711x0.7 = 2598 pcu/h (class C).\nSaturation ratio V/C = 2520/3711 = 0.679 → LOS C (stable flow), and 0.679 <= 0.85 meets the design requirement.",
        "What is the pcu unit?",
        "pcu is the passenger car equivalent, converting large vehicles, motorcycles and so on into an equivalent number of cars by the space they occupy. The higher the heavy vehicle proportion PT and the equivalent factor ET, the smaller f_HV and the lower the capacity, so vehicle composition must be counted for multi-lane expressways.",
        "How should LOS A~F be understood?",
        "Level of Service is graded by the saturation ratio V/C: A is free flowing, B/C is stable, D is approaching unstable, E is congested, and F is forced-flow congestion (V/C >= 1). Design generally requires no lower than class C~D, meaning V/C controlled within 0.7-0.85.",
        "About \"Capacity Calculation\"",
        "Road capacity calculator - basic capacity, possible capacity and design capacity computation with level of service evaluation. Scientific tool using standard formulas, with accurate results.",
    ]))


if __name__ == '__main__':
    main()
