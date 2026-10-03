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
    write('index', build('index', [
"⚙️ Mechanical Engineering Tools",
"Mechanical Engineering",
"Mechanical Engineering Tools",
"Simply Supported Beam Mid-Span Concentrated Load Calculator",
"The simply supported beam mid-span concentrated load calculator uses material mechanics formulas to find the bending moment, shear force and deflection of a simply supported beam under a mid-span concentrated load, suitable for beam checks in mechanical and structural design.",
"Centrifugal Force Calculator",
"The centrifugal force calculator uses mω²r or mv²/r to find the centrifugal force of a rotating body; enter mass, radius and speed, suitable for force analysis of rotating machinery, separation equipment and amusement facilities.",
"Torque-Power-Speed Conversion",
"The torque-power-speed converter works from P=T·ω to convert between torque, power and speed, suitable for parameter matching and checking of motors, engines and transmission systems.",
"Flywheel Rotational Kinetic Energy Calculator",
"The flywheel kinetic energy calculator uses E=½Iω² to find the rotational kinetic energy stored in a flywheel; enter the moment of inertia and angular velocity, suitable for energy estimation in storage, engines and mechanical systems.",
"Enter workpiece and tool material, diameter and speed to calculate turning/milling cutting speed and feed, and recommend cutting parameters, for machining process planning and tool selection.",
"Cylindrical Helical Spring Stiffness Calculator",
"The cylindrical helical spring stiffness calculator uses spring steel parameters (wire diameter, mean diameter, number of coils) to find the rate, suitable for spring selection and buffer element checks in mechanical design.",
"Lever Mechanical Advantage Calculator",
"The lever mechanical advantage calculator derives the force saving multiplier from the arm lengths using moment equilibrium, suitable for the mechanics analysis of force-saving mechanisms, crowbars and balance tools.",
"Gear Ratio Calculator",
"The gear ratio calculator derives the ratio from the tooth counts of the driving and driven gears and supports multi-stage chains, suitable for speed and torque matching in gearboxes, reducers and mechanical transmission systems.",
"Involute standard spur cylindrical gear parameter calculation: module, tooth count, pitch circle, addendum circle, dedendum circle, base circle and centre distance.",
"The belt drive calculator finds the pulley wrap angle, belt speed and tension for mechanical transmission, including empirical wrap angle correction factors, suitable for belt drive design in reducers and conveying equipment.",
"The online chain drive calculator takes sprocket tooth count and speed to find chain speed and transmission ratio, checks centre distance and selection parameters, suitable for mechanical design, running purely front-end.",
"Enter bolt size and strength grade to compute the required preload and tightening torque, with a torque reference table of common sizes, for assembly tightening work.",
"Estimate the bearing rated life (L10) from load, speed and dynamic load rating, compare working conditions to judge the replacement cycle, used for equipment maintenance and model selection, computed purely front-end.",
"Enter driving and driven pulley parameters to compute the belt drive ratio, belt length, wrap angle and linear speed and check the centre distance, for mechanical transmission scheme design.",
"About the Mechanical Engineering Tools",
"The mechanical engineering tool collection brings together 14 free online tools covering the common calculation, conversion and lookup needs in mechanical engineering scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser, uploads no data to a server, and keeps your privacy secure.",
"The mechanical engineering tools collected on this page include (some representative tools):",
"These tools help you finish common mechanical engineering tasks quickly, with no need to memorize complex formulas or do manual conversions, just enter and get the result.",
"Do the Mechanical Engineering Tools need a download or registration?",
"No. All mechanical engineering tools on this page are pure front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
"Are the Mechanical Engineering Tools results accurate? Is my data safe?",
"The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))

    write('cutting-speed', build('cutting-speed', [
"🏎️ Cutting Speed Calculator",
"Turning and milling cutting speed and feed calculator, recommending cutting parameters from workpiece and tool material.",
"Core formulas (by input variable): (fzRange[0]+fzRange[1])÷2; (fzR[0]+fzR[1])÷2; π×D×n÷1000",
"Machining mode",
"Milling",
"Workpiece/tool material",
"Tool material",
"High speed steel (HSS)",
"Workpiece diameter D (mm)",
"Spindle speed n (rpm)",
"Number of cutter teeth Z",
"Compute cutting speed",
"Back-calculate speed",
"📋 Cutting Parameter Reference",
"Cutting speed:",
"Feed rate (milling):",
"vf = fz·Z·n, where fz is the feed per tooth",
"Empirical range:",
"Cemented carbide cutting speed is usually 3~5 times higher than high speed steel; aluminium can be cut at high speed, while stainless steel suits low speed and high feed.",
"📚 In-depth analysis: cutting speed calculation",
"Compute the cutting speed from the workpiece (or tool) diameter and spindle speed, then judge whether it falls in the recommended range for the tool and workpiece material pair.",
"Set the speed before turning or milling to avoid too low a speed (built-up edge, low efficiency) or too high a one (rapid tool wear).",
"Look up the recommended speed range for each combination of tool material (HSS/cemented carbide) and workpiece material to support process parameter selection.",
"Formulas and recommended ranges",
"Cutting speed v = π·D·n/1000 (m/min, where D is the workpiece diameter for turning or the cutter diameter for milling, in mm; n is r/min). Recommended speed ranges (m/min): carbon steel HSS 30~50 / carbide 120~200; alloy steel 20~35 / 90~150; cast iron 20~35 / 80~150; aluminium 80~150 / 300~600; stainless steel 15~25 / 70~120. The tool gives a reasonable / needs adjustment verdict for the selected combination.",
"Turning carbon steel with workpiece diameter D=50 mm, spindle speed n=800 r/min and a carbide tool: v = π×50×800/1000 ≈ 125.66 m/min, inside the 120~200 m/min range recommended for carbon steel with carbide, so it is rated reasonable. At the same 800 r/min with an HSS tool the recommended range is only 30~50 m/min, so 125.66 m/min far exceeds the upper limit and the speed must drop to about 200~320 r/min.",
"What is D for turning versus milling?",
"For turning take the diameter of the surface being machined (the main motion is the workpiece rotating, so the cutting speed is the peripheral speed of the workpiece outer surface); for milling take the cutter diameter (the main motion is the tool rotating). Both use v = πDn/1000; only the physical object behind D differs.",
"What happens if the cutting speed is too high or too low?",
"Too low easily builds up a built-up edge, gives poor surface quality and low efficiency; too high makes the cutting temperature soar, wears the tool rapidly and can even cause chipping. Choose within the recommended range, balancing tool life, surface quality and machine power.",
"About the Cutting Speed Calculator",
"The cutting speed calculator is an online tool for business and office tasks. A business and office tool that improves work efficiency, processing data locally to protect privacy.",
    ]))

    write('belt-drive', build('belt-drive', [
"📐 Belt Drive Design",
"Belt drive design calculations: ratio, belt length, wrap angle, linear speed and centre distance checks.",
"Core formulas (by input variable): 180-2×Math.asin(|(d2-d1)|÷(2×a))×180÷π; 2×a+π×(d1+d2)÷2+(d2-d1)^2÷(4×a); π×d1×n1÷60000",
"Driving pulley speed n1 (rpm)",
"Driving pulley diameter D1 (mm)",
"Driven pulley diameter D2 (mm)",
"Slip rate ε (%)",
"Back-calculate the recommended centre distance",
"📋 Design Formulas",
"Transmission ratio:",
"i = D2 / D1 (accounting for slip, the actual i = D2/(D1·(1−ε)))",
"Driven pulley speed:",
"Belt length:",
"Small pulley wrap angle:",
"α1 = 180° − 2·arcsin((D2−D1)/(2a))×180/π, and ≥ 120° is advisable",
"Linear speed:",
"v = π·D1·n1/60000 (m/s), and generally v ≤ 25~30 m/s",
"📚 In-depth analysis: belt drive design",
"Compute the ratio, belt speed, belt length and small pulley wrap angle from the pulley diameters and centre distance to complete a preliminary V-belt or timing belt selection.",
"Check the wrap angle (ideally ≥120°) and belt speed (ideally ≤25 m/s) to avoid slipping and",
"centrifugal force",
"becoming too large.",
"Compute the actual driven pulley speed after accounting for elastic slip, for speed chain calculations.",
"Theoretical ratio i = d2/d1; actual driven pulley speed n2 = n1·d1/d2·(1−ε), where ε is the slip rate; belt speed v = π·d1·n1/60000 (m/s, with d in mm); belt length L = 2a + π(d1+d2)/2 + (d2−d1)²/(4a); small pulley wrap angle α1 = 180° − 2·arcsin[(d2−d1)/(2a)]·180/π. Verdicts: α1 ≥ 120° passes, v ≤ 25 m/s passes.",
"Small pulley d1=120 mm, large pulley d2=360 mm, centre distance a=500 mm, n1=1450 r/min, slip rate 2%: i = 360/120 = 3.000; n2 = 1450×120/360×0.98 ≈ 473.7 r/min; v = π×120×1450/60000 ≈ 9.11 m/s; L = 2×500 + π×480/2 + 240²/(4×500) ≈ 1782.8 mm; α1 ≈ 152.2°. Both the wrap angle and belt speed pass.",
"Why does the slip rate matter?",
"Belt drives work by friction and unavoidable elastic slip is present (usually 1~2%), so the actual driven pulley speed is slightly below the theoretical value; ignoring it makes the output speed and power estimate optimistic, and precision drives should use timing belts instead.",
"What happens when the wrap angle is too small?",
"A small wrap angle gives a short contact arc and insufficient friction, so the belt slips and wear, heating and even burning increase. Engineering practice requires the small pulley wrap angle ≥120°; if it falls short, increase the centre distance or add a tensioner.",
"About the Belt Drive Design",
"The belt drive design tool is an online tool for business and office tasks. A business and office tool that improves work efficiency, processing data locally to protect privacy.",
    ]))

    write('bearing-life', build('bearing-life', [
"🔮 Bearing Life Estimation",
"Rolling bearing rated life L10 estimation from the basic dynamic load rating, equivalent dynamic load and speed.",
"L10 = (C/P)^ε × 10⁶ revolutions",
"Ball bearing (ε=3)",
"Roller bearing (ε=10/3)",
"Basic dynamic load rating C (kN)",
"Equivalent dynamic load P (kN)",
"Lubrication factor a3",
"Estimate life",
"📋 Life Calculation Formulas",
"Basic rated life:",
"ε = 3 (ball bearings), ε = 10/3 (roller bearings)",
"Life in hours:",
"Corrected rated life:",
"a1 reliability factor: 90%→1, 95%→0.62, 99%→0.21",
"a2 material factor (normally 1), a3 lubrication condition factor",
"Note: P/C should be below 0.5 to guarantee a reasonable fatigue life.",
"📚 In-depth analysis: bearing life estimation",
"Estimate the L10 life of a rolling bearing from the dynamic load rating C and equivalent dynamic load P (the basic rated life at 90% reliability).",
"Correct the life by working conditions (reliability 90/95/99%, service condition factor a3) to judge during selection whether the design life is met.",
"Use the P/C load ratio to judge whether the selection margin is sensible (too large wastes, too small fails early).",
"L10 = (C/P)^ε (million revolutions), with ε=3 for ball bearings and ε=10/3 for roller bearings; L10h = L10×10⁶/(60·n) (hours); corrected life Lna = a1·a2·a3·L10, where a1 is the reliability factor (90%→1, 95%→0.62, 99%→0.21), a2 the material factor (taken as 1 here) and a3 the service condition factor; the corresponding hours Lnah = Lna×10⁶/(60·n); load ratio = P/C.",
"Deep groove ball bearing C=50 kN, P=8 kN, speed 1500 r/min, reliability 90%, a3=1: L10 = (50000/8000)³ = 6.25³ ≈ 2.44×10² million revolutions; L10h = 244.1×10⁶/(60×1500) ≈ 2713 hours (about 0.3 years of continuous running); P/C = 0.160. Switching to 99% reliability gives a1=0.21 and the corrected life drops to about 570 hours, showing how strongly the reliability requirement affects life.",
"What does L10 mean?",
"L10 is the life that 90% of a batch of identical bearings can reach or exceed (i.e. 10% fail), which is the industry-standard definition of basic rated life. It is neither the",
"average life",
"nor a life guaranteed for every single bearing.",
"Why does higher reliability cut the life so much?",
"Bearing life follows the Weibull distribution with large scatter; to push the failure rate from 10% down to 1% (99% reliability) the permissible life must shorten sharply, which is why a1 drops from 1 to 0.21 and life falls to roughly one fifth.",
"About the Bearing Life Estimation",
"The bearing life estimation tool is an online tool for business and office tasks. A business and office tool that improves work efficiency, processing data locally to protect privacy.",
    ]))


if __name__ == '__main__':
    main()