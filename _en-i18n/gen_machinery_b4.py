#!/usr/bin/env python3
# machinery batch4 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'estimate-lifespan-bearing': [
"🔮 Rolling Bearing Rated Life L10 Estimation",
"Compute the basic and modified rating life of a bearing per the ISO 281 standard",
'📖 View the "Rolling Bearing Rated Life L10 Estimation Guide"',
"L10 (90% reliability)",
"L5 (95% reliability)",
"L4 (96% reliability)",
"L3 (97% reliability)",
"L2 (98% reliability)",
"L1 (99% reliability)",
"Lubrication condition a₃",
"Good lubrication (a₃=1.0)",
"Normal lubrication (a₃=0.8)",
"Poor lubrication (a₃=0.6)",
"Excellent lubrication (a₃=1.5)",
"💡 Basic rating life L₁₀=(C/P)^p (million revolutions); life in hours L₁₀h=10⁶·L₁₀/(60n). Modified life Lₙₐ=a₁·a₂·a₃·L₁₀.",
"Reliability factor a₁ (ISO 281)",
"Reliability",
"Note: a₂ is the material factor (1.0 for ordinary hardened steel, 1.5-3.0 for vacuum-degassed steel)",
"📚 In-Depth Analysis: Bearing Life and Back-Calculated Load",
"Given the target life Lh, speed n and dimensions d·B, back-calculate the required dynamic load rating C.",
"Check the mean pressure p=F/(d·B) and the pV value.",
"Compare C under different life requirements.",
"Back-calculate C",
"F=5 kN, d=40 mm, B/d=0.4→B=16 mm, n=1500 rpm, target Lh=20000 h: L10=Lh·60·n/1e6=20000×60×1500/1e6=1800 million revolutions; ball bearing C=F·L10^(1/3)=5000×1800^0.333=5000×12.16≈60800 N≈60.8 kN. Mean pressure p=5000/(40×16)=7.81 MPa.",
"Doubling the life",
"Lh 20000→40000: L10 1800→3600, C=5000×3600^0.333=5000×15.33≈76650 N, requiring a larger bearing.",
"Where does L10^(1/3) come from?",
"The ball bearing life exponent p=3, so C/P=(L10)^(1/3); for roller bearings p=10/3. This example assumes a ball bearing.",
"Mean pressure and pV?",
"p=F/(d·B) is the projected contact pressure; for plain bearings it is further multiplied by the speed to give pV, which controls heat generation.",
"Basic dynamic load rating",
"Equivalent dynamic load",
],
'frequency-17': [
"🔊 Vibration Isolation Calculator",
"Enter the mass, spring stiffness and excitation frequency to compute the system's natural frequency, frequency ratio, transmissibility and isolation efficiency",
'📖 View the "Vibration Isolation Calculator Guide"',
"Isolation frequency ratio = f/√k/m",
"Spring stiffness k (N/m)",
"Excitation frequency f (Hz)",
"Damping ratio ζ",
"💡 Formula: natural frequency fn=(1/2π)√(k/m); frequency ratio r=f/fn; transmissibility T=√(1+(2ζr)²)/√((1-r²)²+(2ζr)²); isolation efficiency η=1-T",
"Effective isolation region: when the frequency ratio r > √2 (about 1.414) the isolation efficiency is positive, and the larger r the better the isolation",
"Resonance region: when r approaches 1 the transmissibility rises sharply, so the excitation frequency should be kept away from the natural frequency",
"A larger damping ratio ζ lowers the resonance peak but reduces the high-frequency isolation",
"Typical damping ratios of isolation materials: rubber 0.05-0.15, metal spring 0.005-0.02",
"📚 In-Depth Analysis: System Natural Frequency",
"For a single degree of freedom, estimate the natural frequency by fn=(1/2π)√(k/m).",
"Back-calculate fn from the static deflection δ (δ=m·g/k).",
"Avoid the excitation frequency (isolation design).",
"Spring-mass",
"k=100 N/mm=100000 N/m, m=10 kg: fn=(1/(2π))√(100000/10)=(1/6.283)×100≈15.9 Hz. Static deflection δ=m·g/k=10×9.8/100000×1000=0.98 mm.",
"Isolation principle",
"If the excitation is 30 Hz, fn≈15.9 Hz and the frequency ratio r=30/15.9≈1.89>√2, in the isolation region with transmissibility <1, giving effective damping.",
"What is the relationship between static deflection and frequency?",
"δ=m·g/k; substituting gives fn=(1/2π)√(g/δ), so the natural frequency can be estimated from the measured static deflection alone.",
"Why must the frequency ratio be >√2?",
"When the excitation frequency / natural frequency >√2 the transmissibility is <1 and the system isolates; below √2 it amplifies the vibration instead.",
'About "Vibration Isolation Calculator"',
"A vibration isolation calculator: from the mass, spring stiffness and excitation frequency it computes the natural frequency, frequency ratio, vibration transmissibility and isolation efficiency of a single-degree-of-freedom system, identifies the current operating region, and aids isolation design.",
"Computes natural frequency and frequency ratio",
"Includes the damped transmissibility formula",
"Automatically identifies the resonance / isolation region",
"Equipment isolation design",
"Vibration-damper selection",
"Rotating-machinery vibration analysis",
"Building-structure damping assessment",
],
'gear': [
"📐 Mechanism Design Calculator",
"Select the mechanism type (four-bar/cam/gear) and enter the parameters to compute the kinematics and geometry",
'📖 View the "Mechanism Design Calculator Guide"',
"Gear design = strength / geometry calculation",
"Mechanism type",
"Hinged four-bar mechanism",
"Cam mechanism",
"Gear mechanism",
"Crank a (mm)",
"Coupler b (mm)",
"Rocker c (mm)",
"Frame d (mm)",
"Base circle radius rb (mm)",
"Stroke h (mm)",
"Rise angle Φ (°)",
"Offset e (mm)",
"Pinion tooth count z1",
"Gear tooth count z2",
"💡 Four-bar: Grashof condition (shortest + longest ≤ sum of the others); transmission angle cosγ=(b²+c²-(d±a)²)/(2bc)",
"Four-bar mechanism: a crank exists when the Grashof condition is met and the shortest link is a side link",
"The smaller the transmission angle, the worse the force transmission; the minimum transmission angle is usually required to be ≥40° (≥50° at high speed)",
"Cam mechanism: the larger the rise angle, the smaller the pressure angle, and the larger the base circle, the smaller the pressure angle",
"Gear mechanism: standard installation center distance a=m(z1+z2)/2",
"📚 In-Depth Analysis: Gear / Linkage / Cam Mechanisms",
"Gear center distance a=m(z1+z2)/2, transmission ratio i=z2/z1.",
"Existence condition of a four-bar mechanism (link-length sum theorem).",
"Base circle radius and maximum pressure angle check of a cam.",
"Gear center distance",
"Four-bar existence condition",
"The shortest + longest ≤ the sum of the other two links (Grashof theorem) is required for full rotation; otherwise it is a double rocker. For example 20+100≤40+60=100, equality holds, so it is marginal.",
"Why does the center distance equal the sum of the two pitch radii?",
"In standard installation the pitch circles are tangent and the operating pitch circle equals the reference pitch circle, so a=(d1+d2)/2=m(z1+z2)/2.",
"Is a larger pressure angle better?",
"No. A large pressure angle transmits force well but lowers efficiency and tends to self-lock; the standard is 20°, and the maximum pressure angle should be checked when the pinion is constrained.",
'About "Mechanism Design Calculator"',
"A mechanism design calculator supporting hinged four-bar, cam and gear mechanisms; it computes kinematic and geometric parameters such as the Grashof condition, transmission angle, pressure angle and center distance, aiding mechanism scheme design.",
"Switchable calculation for three mechanism types",
"Four-bar Grashof test and transmission angle",
"Cam pressure angle and base circle radius recommendation",
"Linkage scheme design",
"Cam profile parameter pre-selection",
"Gear drive center distance calculation",
"Theory of machines and mechanisms course aid",
],
'lifespan-bearing': [
"⚖️ Bearing Load and Life Selection",
"Enter the basic dynamic load rating C, equivalent dynamic load P and speed n to compute the L10 basic rating life (in million revolutions and hours)",
'📖 View the "Bearing Load and Life Selection Guide"',
"Bearing life L10 = (C/P)^p",
"Basic dynamic load rating C (N)",
"Equivalent dynamic load P (N)",
"Ball bearing (exponent 3)",
"Roller bearing (exponent 10/3)",
"💡 Formula: L10=(C/P)^ε (million revolutions), ε=3 (ball) / 10/3 (roller); L10h=10⁶/(60n)×L10 (hours)",
"The L10 life is the rating life at 90% reliability, i.e. a 10% failure probability",
"The equivalent dynamic load P is computed from the radial/axial load combination as P=XFr+YFa",
"Lives at other reliabilities require the reliability factor a1 (Lna=a1·L10)",
"General machinery bearings require a life of 10000-20000 h, and heavy machinery can reach over 50000 h",
"📚 In-Depth Analysis: Rolling Bearing Rating Life",
"L10=(C/P)^p million revolutions (ball p=3, roller p=10/3).",
"Convert to hours L10h=1e6·L10/(60·n).",
"Reliability factor a1 correction.",
"Ball bearing",
"C=60 kN, P=10 kN, n=1500 rpm: L10=(60/10)^3=216 million revolutions; L10h=1e6×216/(60×1500)=2400 h. If P=15 kN: L10=(4)^3=64 million revolutions, L10h=711 h; a 50% load increase reduces the life by about 70%.",
"Roller bearing",
"p=10/3: C=100 kN, P=20 kN: L10=(5)^(3.333)=5^3.333≈158 million revolutions.",
"What does L10 mean?",
"The life (in million revolutions) reached or exceeded by 90% of a bearing batch, i.e. 10% fail before it; it is a rating, not a guaranteed value.",
"How is the equivalent dynamic load P obtained?",
"Combine the actual radial/axial loads with the load factors as X·Fr+Y·Fa, then multiply by the impact factor; see the bearing catalogue for details.",
'About "Bearing Load and Life Selection"',
"A bearing load and life selection calculator: from the basic dynamic load rating C, equivalent dynamic load P and speed n it computes the L10 basic rating life (in million revolutions and hours), supporting ball and roller bearings, aiding bearing selection.",
"Dual mode for ball / roller bearings",
"Outputs L10 and L10h together",
"Life assessment and annual conversion",
"Rolling bearing life verification",
"Bearing model selection comparison",
"Reducer bearing design",
"Equipment maintenance-interval estimation",
],
'lifespan-bearing-1': [
"🚀 Bearing Selection (Rolling / Plain)",
"Enter the load, shaft diameter, width-to-diameter ratio, speed and required life to compute the pV value and recommend the bearing type and required dynamic load rating",
"Bearing Selection",
"/ Bearing Selection",
'📖 View the "Bearing Selection (Rolling / Plain) Guide"',
"Bearing dynamic load rating C = f(life, speed)",
"Radial load F (N)",
"Width-to-diameter ratio B/d",
"Required life Lh (h)",
"💡 Plain bearing: p=F/(d·B); v=πdn/60×10⁻³ (m/s); pV value check; rolling bearing: required C=P·(Lh·60n/10⁶)^(1/3)",
"Plain bearing allowable pV values: tin bronze 8-12, lead bronze 12-20, aluminium bronze 20-30, babbitt 6-10 (MPa·m/s)",
"Rolling bearings suit medium-to-low speed, high-precision applications; plain bearings suit high-speed, heavy-load or split constructions",
"The width-to-diameter ratio B/d is usually 0.5-1.5, commonly 0.8-1.0",
"The required dynamic load rating C for rolling bearings is computed for a ball bearing (exponent 3); roller bearings should use the exponent 10/3",
"📚 In-Depth Analysis: Plain Bearing Life and Pressure",
"Mean pressure p=F/(d·B), pV=p·v check.",
"Back-calculate the required load rating from the target life.",
"Reasonableness of the width-to-diameter ratio B/d.",
"pV check",
"F=8 kN, d=50 mm, B/d=0.8→B=40 mm, v=2 m/s: p=8000/(50×40)=4 MPa; pV=4×2=8 MPa·m/s, below the babbitt allowable (about 10-15), so it passes.",
"Width-to-diameter ratio",
"B/d is usually 0.5-1.5; too small gives high pressure, too large gives excessive end leakage. The 0.8 in the example is reasonable.",
"Why look at pV for a plain bearing?",
"pV is proportional to the frictional heat-generation power density; exceeding the limit ruptures the oil film and seizes the shaft, making it the core limit of a plain bearing.",
"What is the difference from rolling bearing life?",
"Rolling bearings use the L10 fatigue life (in revolutions); plain bearings are governed by pV and wear/temperature rise and are not termed a \"revolution life\".",
'About "Bearing Selection"',
"A bearing selection calculator: from the load, shaft diameter, speed and required life it computes the plain bearing pV value and the rolling bearing required dynamic load rating, and gives a rolling/plain bearing selection recommendation, aiding preliminary mechanical design.",
"pV value check and selection recommendation",
"Required rolling bearing dynamic load calculation",
"Supports a custom width-to-diameter ratio",
"Bearing type pre-selection",
"Plain bearing design verification",
"Rolling bearing life estimation",
"Reducer bearing selection",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'machinery', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
