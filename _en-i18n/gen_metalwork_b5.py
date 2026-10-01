#!/usr/bin/env python3
# metalwork batch5 (7 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'metalwork')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'metalwork')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'thread': [
"📐 Thread-Machining Scheme",
"Input thread specification, material and machining type to recommend a suitable thread-machining method and cutting parameters",
'📖 View the "Thread-Machining Scheme User Guide"',
"Thread machining = scheme selection",
"Thread type",
"Metric thread M",
"Inch thread UNC/UNF",
"Pipe thread G/NPT",
"Trapezoidal thread Tr",
"Nominal diameter d (mm)",
"External thread",
"Internal thread",
"💡 External threads: prefer turning / rolling; internal threads: prefer tapping; high volume: prefer rolling / thread-rolling (high efficiency, chipless).",
"Thread machining needs attention to chip evacuation, cooling and thread precision grade",
"📚 In-depth: Thread-Machining Spindle Speed and Dimension Calculation",
"Set spindle speed n and feed match for thread turning.",
"Find pitch diameter, minor diameter and tapping drill size.",
"Verify pitch to avoid mismatched threads.",
"Thread-turning parameters",
"d=10mm, P=1.5mm, vc=20m/min: n = 1000×20÷(π×10) ≈ 637 rpm; pitch diameter d2 = 10−0.6495×1.5 ≈ 9.03mm, drill D = 10−1.5 = 8.5mm.",
"Mismatched-thread prevention",
"Each pass needs a consistent tool-reference; pitch 1.5mm means the toolpost advances 1.5mm per spindle revolution; mismatch is usually from not lifting the half-nut on retract or encoder step loss.",
"How to set the thread-turning speed?",
"Compute from vc and diameter; small diameters can run at high rpm; but ensure feed-to-pitch synchronization, with system response keeping up at high speed.",
"Is the pitch-diameter formula universal?",
"The metric triangular-thread d2 = d−0.6495P is the standard 60° profile approximation; inch / trapezoidal threads use different coefficients and need their respective standards.",
'About "Thread-Machining Scheme"',
"The thread-machining scheme tool recommends a suitable thread-machining method (turning / tapping / milling / rolling) from thread specification, material, machining direction and batch, and computes spindle speed, pitch diameter, minor diameter and other parameters.",
"Recommendation of multiple machining methods",
"Thread geometric-parameter calculation",
"Tapping drill recommendation",
"Thread-process design",
"Machining-method selection",
"Tapping drill determination",
"Cutting-parameter calculation",
"Nominal diameter",
"Pitch",
],
'thread-spec': [
"📚 Thread-Specification Lookup",
"Look up the pitch, pitch diameter, minor diameter and recommended drill size for metric (coarse / fine) and inch (UNC / UNF) threads.",
'📖 View the "Thread-Specification Lookup User Guide"',
"Metric thread: pitch P from coarse/fine series tables, pitch diameter d₂ = d − 0.6495P, minor diameter d₁ = d − 1.0825P, tapping drill ≈ d − P; inch UNC/UNF uses threads per inch n, pitch = 25.4 ÷ n (mm), drill ≈ nominal diameter − 25.4 ÷ n.",
"Search specification (e.g. M8, 1/4)",
"Metric coarse",
"Metric fine",
"Inch UNC",
"Inch UNF",
"📋 Thread basics",
"Metric thread:",
"Thread angle 60°, specification M×pitch (mm). Coarse is the common series; fine is for thin-wall / precision / fine adjustment.",
"Drill diameter (metric):",
"Drill ≈ nominal diameter − pitch (ductile material) or − 1.1×pitch (brittle material such as cast iron).",
"Inch thread:",
"Thread angle 60° (UN series), specification is fractional diameter - threads per inch (TPI), e.g. 1/4-20.",
"Coarse,",
"fine. Drill diameter (inch) ≈ nominal diameter − 1/TPI.",
"The tapping drill should be slightly larger than the minor diameter, leaving cutting allowance to avoid tap breakage.",
"📚 In-depth: Quick Thread-Specification Size Lookup",
"Look up standard thread pitch diameter, minor diameter and drill size.",
"Metric / inch conversion for selection.",
"Match drills to prevent thread stripping.",
"M10 specification",
"M10×1.5: pitch diameter d2 = 10−0.6495×1.5 ≈ 9.026mm, minor diameter d1 ≈ 8.376mm, tapping drill D = 10−1.5 = 8.5mm.",
"Coarse vs fine",
"M10 coarse P=1.5, fine P=1.0: fine has larger pitch diameter and better self-locking, for thin wall or fine adjustment, but its drill differs and needs matching.",
"Why is the drill d−P?",
"The tapping drill ≈ outer diameter minus pitch, leaving tooth height; too small a drill breaks the tap and strips threads, too large leaves insufficient tooth height and weak joint.",
"What is the difference between pitch and minor diameter?",
"The pitch diameter is the thread-fit reference dimension; the minor diameter is the minimum root diameter; gauges control pitch diameter to ensure screwability and sealing.",
'About "Thread-Specification Lookup"',
"Thread-Specification Lookup is an online tool in the business-office domain. A business-office tool that improves work efficiency, with data processed locally to protect privacy.",
"Filter by entering a specification keyword",
],
'welding-heat': [
"🧮 Welding Heat-Input Calculator",
"From welding current, voltage, welding speed and process thermal efficiency, compute the heat input (line energy) and assess whether the welding process is reasonable.",
'📖 View the "Welding Heat-Input Calculator User Guide"',
"Heat input Q = η·U·I/v",
"Welding current I (A)",
"Arc voltage U (V)",
"Welding speed v (cm/min)",
"Welding process (thermal efficiency η)",
"SMAW manual arc welding (η≈0.85)",
"GMAW gas metal arc welding (η≈0.80)",
"GTAW tungsten inert gas welding (η≈0.70)",
"SAW submerged arc welding (η≈0.90)",
"FCAW flux-cored wire (η≈0.75)",
"Thermal efficiency η",
"Calculate heat input",
"📋 Calculation Notes",
"Heat input E = (U × I × η × 60) / v  (unit: J/cm)",
"Convert to kJ/cm: E(kJ/cm) = E(J/cm) / 1000",
"Convert to kJ/mm: E(kJ/mm) = E(kJ/cm) / 10",
"Parameter notes:",
"U is arc voltage (V), I is welding current (A), v is welding speed (cm/min), η is process thermal efficiency.",
"Reference range:",
"Thin plate low heat input 0.5-1.5 kJ/mm; general structural steel 1.5-3.0 kJ/mm; thick plate / submerged arc 3.0-6.0 kJ/mm.",
"Excessive heat input coarsens grains and lowers toughness; too little tends to cause cold cracks and lack of fusion.",
"📚 In-depth: Welding Heat-Input Calculation",
"Find heat input E from voltage, current, efficiency and speed.",
"Control heat input by material to prevent hardening / distortion.",
"Compare the heat-affected zone of different welding methods.",
"Heat input",
"U=24V, I=180A, η=0.5, v=30cm/min: E = (24×180×0.5×60)/30 = 4320 J/cm = 43.2 kJ/m (i.e. 0.432 kJ/mm), a medium-low heat input.",
"Reduce heat to prevent cracking",
"If speed rises to 45cm/min: E = (24×180×0.5×60)/45 = 2880 J/cm, heat input drops by 1/3, helping high-strength steel avoid cold cracking but must keep penetration.",
"Is more heat input better?",
"Not necessarily; too much widens the heat-affected zone, increases distortion and overheating, too little may lack fusion; high-strength steel and stainless steel should be controlled at the lower-middle range.",
"How to choose efficiency η?",
"Submerged arc η≈0.95, MIG≈0.7-0.8, manual arc≈0.7, TIG≈0.5; it reflects the share of arc power converted to workpiece heat.",
'About "Welding Heat-Input Calculator"',
"Welding Heat-Input Calculator is an online tool in the business-office domain. A business-office tool that improves work efficiency, with data processed locally to protect privacy.",
],
'wushua-zhinengyuqingliangduibijisuanqi': [
"🔨 Brushless / Smart / Lightweight Comparison Calculator",
"Compare brushless-motor and lightweight scores to give power-tool R&D route suggestions.",
"/ Innovation (Brushless / Smart / Lightweight) R&D",
'📖 View the "Brushless / Smart / Lightweight Comparison Calculator User Guide"',
"Overall gap = |brushless − lightweight|; brushless weight ratio = brushless ÷ (brushless + lightweight) × 100%",
"Power-tool upgrades focus on brushless motors and lightweighting: the brushless score reflects efficiency / life, the lightweight score reflects portability / runtime. Comparing the two gives the R&D focus; the weight ratio quantifies relative share, aiding technology-route selection.",
"Brushless score (0-100)",
"Lightweight score (0-100)",
"💡 Overall gap = |brushless − lightweight|; brushless weight ratio = brushless ÷ (brushless + lightweight).",
"📚 In-depth: Brushless / Smart / Lightweight Tool Comparison",
"Compare the energy efficiency, weight and life of brushless vs brushed tools.",
"Quantify weight reduction and runtime gains from lightweighting.",
"Value assessment of smart functions (torque memory).",
"Energy-efficiency comparison",
"At the same load brushless efficiency 85%, brushed 70%: brushless loss = 100−85 = 15% vs brushed 30%, half lower; same",
"battery runtime",
"is longer.",
"Weight reduction",
"Swapping a 1.8kg brushed drill for a 1.2kg brushless lightweight model: weight loss = 1.8−1.2 = 0.6kg, weight-loss rate = 0.6÷1.8×100 ≈ 33%, reducing fatigue in long operations.",
"Where does brushless cost more, and is it worth it?",
"Brushless motors need no carbon brush, have high efficiency, long life and strong controllability; under heavy high-frequency use the cost pays back fast; occasional use can choose brushed.",
"Does lightweighting affect torque?",
"Weight reduction mostly comes from body material and structure, not necessarily lowering torque; but too light at high torque gives poor reaction-torque feel, so look at torque spec rather than weight.",
'About "Innovation (Brushless / Smart / Lightweight) R&D"',
"Innovation (Brushless / Smart / Lightweight) R&D. A free online tool, fully client-side, no data uploaded, privacy safe.",
"Brushless",
"Smart",
],
'yuanlingongju-xifen': [
"🔨 Garden Tools (Segmented)",
"Compare mower and trimmer power to give landscaping equipment selection advice.",
'📖 View the "Garden Tools (Segmented Comparison) User Guide"',
"Power gap = |trimmer − mower|; recommend the high-power model for large-area work; power ratio = high ÷ low",
"Select garden tools by task type: mowers for lawn trimming, trimmers for hedge shaping. Comparing their power, the higher-power one suits large areas or thick branches; the power ratio reflects work-intensity span, aiding selection by garden size.",
"Mower power (W)",
"Trimmer power (W)",
"💡 Power gap = |trimmer − mower|; high power suits large-area work.",
"📚 In-depth: Garden-Tool Segmented Comparison",
"Compare mower / hedge-trimmer displacement, power and weight for selection.",
"Trade-off between fuel and lithium-ion schemes.",
"Match work efficiency to lawn area.",
"Displacement comparison",
"Gas mower displacement 140cc, power 2.5kW; lithium 40V equivalent about 1.5kW: small yards are fine with lithium, low noise; large yards choose large-displacement gas for higher efficiency.",
"Efficiency matching",
"Area 500㎡, cut width 45cm, speed 3km/h: single pass about 500÷4.5 ≈ 111m travel, time ≈ 111÷50 ≈ 2.2min (excluding turns); large areas need wider cut width for efficiency.",
"How to choose fuel vs lithium?",
"Small yard / low frequency: choose lithium, maintenance-free and low noise; large yard / continuous heavy load: choose gas for strong power and worry-free runtime, but needs fuel and maintenance care.",
"Is a wider cut width always better?",
"Wider cut is more efficient but heavier and hard to turn in narrow spaces; choose by area and terrain, 40-50cm for flexible small yards.",
'About "Garden Tools (Segmented)"',
"Garden Tools (Segmented). A free online tool, fully client-side, no data uploaded, privacy safe.",
],
'zhineng-duogongnengyunaiyongduibijisuanqi': [
"🔨 Smart / Multifunction / Durable Comparison Calculator",
"Compare smart and durable scores to give product R&D route focus advice.",
"/ Innovation (Smart / Multifunction / Durable) R&D",
'📖 View the "Smart / Multifunction / Durable Comparison Calculator User Guide"',
"Overall gap = |smart − durable|; smart weight ratio = smart ÷ (smart + durable) × 100%",
"Tool R&D often trades off smart vs durable: the smart score reflects connectivity / automation, the durable score reflects life / reliability. Comparing the two gives the focus route; the weight ratio quantifies the two's relative share, aiding resource-allocation decisions.",
"Smart score (0-100)",
"Durable score (0-100)",
"💡 Overall gap = |smart − durable|; smart weight ratio = smart ÷ (smart + durable).",
"📚 In-depth: Smart Multifunction Tool Durability Comparison",
"Compare multifunction tools' continuous working time and life.",
"Assess cost performance by task-switching efficiency.",
"Trade-off between warranty and maintenance cost.",
"Durable hours",
"Tool A rated continuous 4h, B 2.5h: A is 60% more than B, less downtime in heavy work; annualized (2h/day) A lasts about 2x the cycle.",
"Cost performance",
"A price ¥1200 at 4h/day×200days=800h/year, ¥1.5/h; B ¥800 at 2.5h×200=500h, ¥1.6/h; over a long cycle A is cheaper.",
"Does continuous working time include load?",
"Rating is mostly rated load continuous; actual intermittent is longer; overload shortens life, so convert by real conditions for accuracy.",
"Is multifunction always cost-effective?",
"One machine with many attachments saves space and money, but single-function specialist tools are often stronger and more durable; for high-frequency single tasks a dedicated tool is better.",
'About "Innovation (Smart / Multifunction / Durable) R&D"',
"Innovation (Smart / Multifunction / Durable) R&D. A free online tool, fully client-side, no data uploaded, privacy safe.",
"How to use the Smart / Multifunction / Durable Comparison Calculator",
"Multifunction",
"What does the Smart / Multifunction / Durable Comparison Calculator do?",
"The Smart / Multifunction / Durable Comparison Calculator takes various parameters for tool R&D, quantitatively comparing smart, multifunction and durable routes to aid innovation decisions.",
"How do I use the Smart / Multifunction / Durable Comparison Calculator?",
"Which scenarios suit the Smart / Multifunction / Durable Comparison Calculator?",
"Smart",
"Multifunction",
],
'zulinfeilvjisuan': [
"🧮 Lease-Rate Calculator",
"Input equipment original value, lease term, residual-value rate and annual interest rate to compute monthly rent, total rent and return on investment",
'📖 View the "Lease-Rate Calculator User Guide"',
"Lease rate = original value × rate / period",
"Equipment original value (CNY)",
"Lease term (months)",
"Annual interest rate (%)",
"Payment method",
"Monthly (end of period)",
"Monthly (beginning of period)",
"Quarterly (end of period)",
"Annual (end of period)",
"Management fee rate (%)",
"💡 The monthly rent is computed by the equal-principal-and-interest method, including equipment depreciation, capital interest and management fee. The residual value is recovered at lease end.",
"Actual lease rate needs to consider taxes, insurance, maintenance and other comprehensive costs",
"📚 In-depth: Equipment Lease-Rate and Return Calculation",
"Financial leasing computes each period's rent from original value, residual, interest rate and term.",
"Compare leasing vs one-time purchase cash flow.",
"Settlement",
"Rent per period",
"Equipment original value 100k, 36 months, residual rate 10%, annual rate 8%, management fee 1%: residual = 100000×10% = 10k, principal to recover = 90k, period rate = 8%÷12 ≈ 0.667%, use the annuity method to compute rent per period (including fee) and ×36 for total rent.",
"Return rate",
"Total rent 115k + residual 10k = total recovery 125k: ROI = (12.5−10)÷10×100 = 25%, annualized ≈ 25%÷3 ≈ 8.3%, judged against the interest-rate level.",
"Is leasing or buying more cost-effective?",
"Look at capital cost and usage period: short-term / tight cash flow favors leasing for flexibility; long-term high-frequency ownership often has lower total cost, but compute ROI and tax shield.",
"Does the residual-value rate matter much?",
"Higher residual means less principal to recover and lower rent; but over-estimating residual shifts risk to the lessee, so the contract must clarify buyback / residual clauses.",
'About "Lease-Rate Calculator"',
"The lease-rate calculator, from equipment original value, lease term, residual-value rate, annual interest rate and payment method, computes rent per period, total rent, total interest and return on investment by the equal-principal-and-interest method.",
"Equal-principal-and-interest monthly rent calculation",
"Support for multiple payment methods",
"Total rent / total interest / return rate",
"Management-fee calculation",
"Equipment lease pricing",
"Lease-scheme design",
"Return-on-investment evaluation",
"Financial-lease rate settlement",
"Equipment original value",
"Lease term",
"Residual-value rate",
"Annual interest rate",
"Management-fee rate",
],
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
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if it.get('src_diff') and it.get('zh') and it['zh'].strip() and it['zh'].strip() != z:
            mp[it['zh'].strip()] = en
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'metalwork', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_metalwork_b5 done')
