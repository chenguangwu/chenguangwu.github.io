#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'mechanical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'mechanical')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
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
    out = {'slug': slug, 'industry': 'mechanical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
def main():
    write('bolt-torque', build('bolt-torque', [
"🔩 Bolt Torque Reference",
"Bolt preload and tightening torque calculation, with a torque reference table of common sizes.",
"Core formulas (by input variable): K×F×d÷1000",
"Grade 4.8",
"Grade 5.8",
"Grade 8.8",
"Grade 10.9",
"Grade 12.9",
"📋 Common Bolt Torque Reference Table (μ=0.14)",
"Torque formula:",
"T = K·F·d, where K is the torque coefficient (related to μ, generally K≈0.2) and F is the preload taken as 70%~75% of the yield strength.",
"Preload:",
"F ≈ 0.75·σs·As, where As is the thread stress cross-sectional area.",
"Note: actual tightening should follow the drawing or code requirements; this table is for reference and applies to ordinary mechanical connections.",
"📚 In-depth analysis: bolt torque reference",
"Estimate the recommended tightening torque from the bolt strength grade and nominal diameter to guide assembly torque settings and avoid snapping the bolt or under-preloading.",
"Back-calculate the allowable preload from the stress cross-sectional area and yield strength to assess whether the joint clamping force is sufficient.",
"Compare how different friction coefficients (lubricated or not) affect the torque-preload relationship.",
"Stress cross-sectional area As = 0.7854·(d − 0.9382·p)², where p is the pitch (d≤6→1, ≤10→1.5, ≤14→2, ≤20→2.5, ≤30→3.5, >30→4); preload F = 0.75·σs·As (75% of yield); torque coefficient K = 0.161 + 0.585·μ; tightening torque T = K·F·d/1000 (N·m, with d in mm). Yield strength σs (MPa): 4.8→320, 5.8→400, 8.8→640, 10.9→900, 12.9→1080.",
"Grade 8.8 M12 bolt (p=2) with friction coefficient μ=0.14: As = 0.7854×(12−0.9382×2)² ≈ 80.5 mm²; F = 0.75×640×80.5 ≈ 38.6 kN; K = 0.161+0.585×0.14 ≈ 0.243; T = 0.243×38600×12/1000 ≈ 112.6 N·m. Switching the same bolt to dry friction (μ≈0.2) raises K to about 0.278, and at the same 112.6 N·m torque the preload actually comes out lower, showing how strongly lubrication affects torque control.",
"Why is the preload taken at 75% of yield?",
"It leaves about 25% safety margin so the bolt does not enter plastic range or get snapped during tightening; for critical joints, also check fatigue, relaxation and crushing of the connected parts against the working conditions and then re-determine the utilisation.",
"Is the torque method accurate for controlling preload?",
"The torque method is strongly affected by friction coefficient variation (K is very sensitive to μ), and the preload scatter can reach ±25% or more; critical locations should use the torque-angle method, the yield point method, or direct measurement such as hydraulic tensioning and ultrasonic length measurement.",
"About the Bolt Torque Reference",
"The bolt torque reference tool is an online tool for business and office tasks. A business and office tool that improves work efficiency, processing data locally to protect privacy.",
    ]))

    write('gear-parameters', build('gear-parameters', [
"⚙️ Gear Parameter Calculator",
"Involute standard spur cylindrical gear parameter calculation: module, tooth count, pitch circle, addendum circle, dedendum circle, base circle and centre distance.",
"Core formulas (by input variable): d1-2×(ha+c)×m+2×x1×m; d2-2×(ha+c)×m+2×x2×m; d1+2×ha×m+2×x1×m",
"Tooth count z1",
"Tooth count z2 (meshing gear)",
"Profile shift coefficient x1",
"Profile shift coefficient x2",
"📋 Gear Parameter Formulas",
"Standard spur cylindrical gear:",
"pitch circle d = m·z　|　addendum circle da = d + 2·ha*·m　|　dedendum circle df = d − 2·(ha*+c*)·m",
"base circle db = d·cosα　|　centre distance a = (d1+d2)/2 = m·(z1+z2)/2",
"circular pitch p = π·m　|　tooth thickness on pitch circle s = π·m/2",
"ratio i = z2/z1",
"📚 In-depth analysis: gear parameter calculation",
"Compute the geometric dimensions of standard and profile-shifted spur gears (pitch circle, addendum circle, dedendum circle, base circle, centre distance and more) from module, tooth count and pressure angle.",
"When designing profile-shifted gears, recompute the shifted addendum circle, dedendum circle and actual centre distance to avoid interference and undercutting.",
"Check whether the ratio and centre distance satisfy the structural design constraints.",
"pitch circle d = m·z; addendum circle da = d + 2·ha*·m + 2·x·m; dedendum circle df = d − 2(ha*+c*)·m + 2·x·m; base circle db = d·cosα; standard centre distance a = (d1+d2)/2; shifted centre distance a′ = a + (x1+x2)·m; circular pitch p = π·m; ratio i = z2/z1. Defaults: addendum coefficient ha*=1, clearance coefficient c*=0.25, pressure angle α=20°.",
"Module m=2, z1=24, z2=36, α=20°, no shift (x1=x2=0): d1=48, da1=52, df1=43, db1≈45.105 mm; d2=72, da2=76, df2=67, db2≈67.658 mm; centre distance a=60.000 mm; circular pitch p≈6.283 mm; ratio i=1.500. Shifting each gear by +0.5 (x1+x2=1) enlarges the addendum circles and the actual centre distance becomes 60+1×2 = 62 mm.",
"What is the significance of the base circle?",
"The base circle is the generating circle of the involute tooth profile, where the pressure angle is zero; it determines the involute shape and is also the geometric basis for judging undercutting (when the cutter cuts into the tooth root at too few teeth) and for computing the contact ratio.",
"Why profile shift?",
"Profile shift avoids undercutting low tooth-count gears, lets you match centre distance, and improves flank contact strength and wear uniformity; positive shift increases tooth thickness and bending strength but sharpens the tooth tip, so the shift coefficient upper limit must be controlled and tip thickness checked.",
"About the Gear Parameter Calculator",
"The gear parameter calculator is an online tool for business and office tasks. A business and office tool that improves work efficiency, processing data locally to protect privacy.",
    ]))

    write('spring-rate', build('spring-rate', [
"🧮 Cylindrical Helical Spring Rate Calculator (Mechanical)",
"Compute the axial rate of a cylindrical helical compression spring from wire diameter, mean diameter and active coils using material mechanics formulas.",
"Cylindrical Helical Spring Rate Calculator",
"Cylindrical helical spring rate k = G·d⁴ ÷ (8·D³·n), where d is the wire diameter, D the mean diameter, n the number of active coils and G the shear modulus.",
"Spring wire diameter d (mm)",
"k = G·d⁴ / (8·D³·n) (axial rate of a cylindrical helical spring)",
"Take G as the material shear modulus: steel ≈79 GPa, stainless steel ≈73 GPa",
"d is the wire diameter, D the mean diameter and n the number of active coils",
"📚 In-depth analysis: cylindrical helical spring rate calculation (mechanical)",
"Compute the cylindrical helical",
"shear modulus",
"to derive the rate of a cylindrical helical compression/tension spring, for",
"spring design",
"and selection.",
"Evaluate the spring load under a given deflection (F = k·Δ) and check whether the working force and travel requirements are met.",
"Compare how different parameters affect the rate (wire diameter is the most sensitive, as a fourth-power relation).",
"Rate k = G·d⁴/(8·D³·n) (N/mm), where G is the shear modulus (N/mm², so input GPa in the tool and multiply by 1000), d the wire diameter, D the mean diameter and n the number of active coils. Load F = k·Δ (Δ being the deflection in mm).",
"Wire d=5 mm, mean diameter D=30 mm, active coils n=6, shear modulus G=79 GPa (spring steel): k = 79000×5⁴/(8×30³×6) = 79000×625/(8×27000×6) ≈ 38.10 N/mm (about 38098 N/m). Compressed by 10 mm the load is about 381 N. Rate is proportional to d⁴: raising the wire diameter from 5 to 6 mm raises the rate to about (6/5)⁴ ≈ 2.07 times.",
"Why does the wire diameter matter so much?",
"Because the rate is proportional to the fourth power of d, making it the most sensitive parameter; the mean diameter D enters as an inverse cube and the coil count n as an inverse first power. In design, fine-tune d first, then D, and use n for final trimming to avoid large changes that throw the structure out of proportion.",
"Which springs does this formula apply to?",
"It applies to cylindrical helical compression/tension springs with round wire and equal pitch (small helix angle, static or quasi-static loads); large deflection, high-speed cyclic loading, variable-pitch or conical springs need separate checks of shear stress, fatigue and stability per standards such as GB/T 23935.",
    ]))

    write('calc-1', build('calc-1', [
"🧮 Belt Drive Calculator (Mechanical)",
"Compute the ratio, belt speed, wrap angle, reference length and large pulley speed of a V-belt or flat belt drive.",
"Belt drive: small pulley linear speed v = π·d₁·n₁ ÷ 60000 (m/s); ratio i = d₂ ÷ [d₁·(1 − ε)], where d is the pulley diameter, n the speed and ε the slip rate.",
"Small pulley diameter d₁ (mm)",
"Large pulley diameter d₂ (mm)",
"Centre distance a (mm)",
"Slip rate ε (%)",
"Ratio i = d₂ / d₁ (accounting for the slip rate, i_actual = d₂ / [d₁(1−ε)])",
"Belt speed v = π·d₁·n₁ / 60000 (m/s), with 5~25 m/s recommended for V-belts",
"Wrap angle α₁ ≈ 180° − 57.3°×(d₂−d₁)/a",
"Belt length Ld ≈ 2a + π(d₁+d₂)/2 + (d₂−d₁)²/(4a)",
"📚 In-depth analysis: belt drive calculation (mechanical)",
"Compute the theoretical and actual ratio, belt speed, wrap angle and reference belt length from pulley diameters, centre distance, speed and slip rate to complete the belt drive geometry design.",
"Back-calculate the effective tension from the transmitted power and belt speed to support belt type (number of strands) and initial tension selection.",
"Check whether the small pulley wrap angle and belt speed fall in the recommended range and judge whether the scheme needs adjustment.",
"Theoretical ratio i = d2/d1; actual ratio i′ = d2/[d1·(1−ε)] where ε is the slip rate; belt speed v = π·d1·n1/60000 (m/s); driven pulley speed n2 = n1/i′; small pulley wrap angle α1 ≈ 180° − 57.3·(d2−d1)/a; reference belt length Ld = 2a + π(d1+d2)/2 + (d2−d1)²/(4a); effective tension F = P×1000/v (N, with P in kW). Recommended belt speed 5~25 m/s; the wrap angle correction factor has an empirical value ≈ 0.9 + max[0,(α1−120)/60×0.1].",
"d1=125 mm, d2=315 mm, a=800 mm, n1=1450 r/min, slip rate 1.5%, power 5.5 kW: i = 2.52, i′ = 315/(125×0.985) ≈ 2.56; v ≈ 9.49 m/s; n2 ≈ 566.8 r/min; α1 ≈ 166.4°; Ld ≈ 2302.4 mm; effective tension F = 5500/9.49 ≈ 579.5 N; wrap angle correction factor about 0.98. The belt speed falls in the recommended 5~25 m/s range, so the scheme is workable.",
"Why do the theoretical and actual ratios differ?",
"The theoretical value depends only on the pulley diameters; the actual value accounts for the speed loss from elastic slip (1~2%) and is the true basis for estimating output speed and the downstream speed chain.",
"What is the effective tension used for?",
"Effective tension F = P/v is the circumferential force the belt transmits, used to determine the number of strands (z ≥ F/[F]), the initial tension and the shaft load. It is the starting point of belt drive strength design and also determines the shaft and bearing loads.",
    ]))

    write('torque-power', build('torque-power', [
"⚡ Torque-Power-Speed Conversion (Mechanical)",
"Convert speed and power into the output torque of a rotating shaft (and angular velocity).",
"Torque-Power-Speed Conversion",
"P = T·ω/1000 should convert back to the input power",
"You can also use T = P/ω (P in W, ω in rad/s)",
"The check row P=T·ω/1000 should convert back to the input power",
"📚 In-depth analysis: torque-power-speed conversion (mechanical)",
"Convert quickly between power, torque and speed for",
"transmission system design.",
"Derive the output torque from power",
"and speed, and judge whether the load torque requirement is met.",
"Check the torque and power matching at the reducer output.",
"Torque T = 9550·P/n (N·m, with P in kW and n in r/min);",
"angular velocity",
"ω = 2π·n/60 (rad/s); check power P = T·ω/1000 (kW). The coefficient 9550 comes from the engineering rounding of 60×1000/(2π) ≈ 9549.3.",
"With power P=7.5 kW and speed n=1450 r/min: T = 9550×7.5/1450 ≈ 49.4 N·m; ω = 2π×1450/60 ≈ 151.84 rad/s; the back-calculated power = 49.4×151.84/1000 ≈ 7.5 kW, matching the input (cross-checking). This is exactly the rated operating point of a common 4-pole asynchronous motor at 50 Hz.",
"Where does the coefficient 9550 come from?",
"From T(N·m) = P(W)/ω(rad/s) together with ω = 2πn/60, giving T = 60×P(kW)×1000/(2π×n) ≈ 9549.3·P/n; engineering practice rounds this to 9550 for easier memorisation and hand calculation, and the error is negligible.",
"Why is torque larger at lower speed for the same power?",
"Because power is the product of torque and angular velocity (P = T·ω), so at fixed power torque is inversely proportional to speed. A reducer therefore amplifies torque in proportion as it lowers speed (minus efficiency losses), which is the principle behind fitting a reducer to heavy-load low-speed equipment.",
    ]))


if __name__ == '__main__':
    main()