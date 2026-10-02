#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'welding')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'welding')
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
    out = {'slug': slug, 'industry': 'welding', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
def main():
    write('hancaixuanyongtuijian', build('hancaixuanyongtuijian', [
"🛡️ Welding Consumable Selection Recommendation",
"Enter the base material, plate thickness and welding position to get recommended electrode and wire models plus diameters",
"Base material",
"Q235 carbon steel",
"Q345 low-alloy steel",
"20 steel",
"💡 Consumable selection follows the equal-strength matching principle; for stainless steel pick the matching grade by base composition; electrodes for vertical and overhead positions should be 4 mm or smaller.",
"The consumable grades are for reference only; the official choice should follow the qualified welding procedure",
"Critical structures should use low-hydrogen electrodes and bake them as specified",
"📚 In-depth analysis: welding consumable selection recommendation",
"Look up the recommended electrode and wire grades by base material grade, selecting consumables by the equal-strength matching principle.",
"Choose the electrode diameter by plate thickness and correct it for the welding position (thick electrodes are unsuitable for vertical and overhead welding).",
"Give a reference current range as the starting point for test-welding parameter tuning.",
"Consumable selection rules",
"Common matches: Q235 → E4303(J422)/E4315(J427), wire ER50-6; Q345 → E5015(J507)/E5016(J506), wire ER50-6; 20 steel → same as Q235; 304 stainless → E308-16(A102)/E308-15(A107), wire ER308; 316 → E316-16(A202)/E316-15(A207), wire ER316. Electrode diameter by plate thickness: under 4 mm use 2.5, 4~12 mm use 3.2, 12~25 mm use 4.0, 25 mm or more use 5.0 mm; for vertical (PF) and overhead (PE) positions keep the diameter at or below 4 mm. Reference current = 40 × diameter (mm), with ±15% tolerance.",
"Q345 steel, 16 mm plate thickness, horizontal welding position: recommended electrode E5015(J507), 4.0 mm diameter (16 mm falls in the 12~25 mm range), reference current = 40×4 = 160 A, roughly 136~184 A. At the same thickness in the vertical position the diameter stays 4.0 mm (still under the limit), but in operation you should use the lower end of the current range for better weld pool control.",
"What does equal-strength matching mean?",
"The strength of the weld metal (especially yield and tensile strength) should be comparable to the base material. Choosing too low leaves the joint under-strength; choosing too high gives a weld with poor ductility and high residual stress, and may initiate cracks.",
"Why are stainless steel consumables selected by composition?",
"Stainless steel consumables must match the chromium-nickel system of the base material (for example 304 with the 308 series, 316 with the 316 series), so that the weld keeps its corrosion resistance and metallurgical structure (avoiding carbide precipitation or an unfavorable amount of ferrite).",
"About the Welding Consumable Selection Recommendation",
"The welding consumable selection tool takes the base material (Q235/Q345/304/316/20 steel), plate thickness and welding position, then recommends matching electrode grades, wire grades, electrode diameter and reference current to support consumable selection.",
"Matching for five common base materials",
"Both electrode and wire recommended",
"Electrode diameter and current reference",
"Welding position correction",
"Consumable purchasing and selection",
"Welding process design",
"Shop-floor consumable issue reference",
"Welding teaching and training",
"Plate thickness",
    ]))

    write('speed-voltage-current', build('speed-voltage-current', [
"🧮 Welding Parameter Calculation",
"Enter plate thickness, material and welding position to get recommended current, voltage, travel speed and heat input",
"Flat welding PA",
"Horizontal welding PC",
"Vertical welding PF",
"Overhead welding PE",
"💡 Current is estimated empirically from plate thickness and position; for GMAW voltage U = 14+0.05×I; heat input HI = U×I/v ÷1000 (kJ/mm).",
"The recommended values are empirical estimates; in practice they should be fixed by a procedure qualification (PQR)",
"Vertical and overhead positions need lower current; on thin plate watch the heat input carefully",
"📚 In-depth analysis: welding parameter calculation",
"Derive process parameters such as current, voltage and travel speed from plate thickness, material and welding position as a starting point for test welding.",
"Estimate the heat input and judge whether the parameter combination would cause burn-through or degrade the heat-affected zone properties.",
"Correct the current by position (decreasing from horizontal to vertical to overhead) to give operable parameters for each position.",
"Parameter model",
"Base current = material coefficient × plate thickness (mm) × position coefficient, where the material coefficient is 40 for carbon steel, 35 for stainless steel and 30 for aluminium; the position coefficient is 1.0 for flat welding PA, 0.85 for horizontal PC, 0.75 for vertical PF and 0.8 for overhead PE; the recommended current is the base value ±15%. Voltage: for manual arc welding U = 22 + 0.2×thickness, for other methods U = 14 + 0.05×base current. Travel speed: 2~4 mm/s for manual arc welding, 4~8 mm/s otherwise. Heat input HI (kJ/mm) = voltage × current ÷ travel speed (mm/s) ÷ 1000.",
"6 mm carbon steel plate, flat welding: base current = 40×6×1.0 = 240 A, range about 204~276 A; manual arc welding voltage = 22+0.2×6 = 23.2 V; taking a speed of 3 mm/s, heat input = 23.2×240/3/1000 ≈ 1.86 kJ/mm (moderate). At the same thickness in the vertical position: current = 240×0.75 = 180 A, and you should work at the lower end for weld pool control.",
"Why reduce current for vertical and overhead welding?",
"In positions other than flat welding the weld pool tends to run downward under gravity; reducing current shrinks the pool volume and its fluidity and makes the bead easier to form. A common rule is 75%~85% of the flat-welding current.",
"How much heat input is appropriate?",
"It depends on material and thickness: for carbon steel, keep it within 1~2.5 kJ/mm; thin plate takes the lower value to prevent burn-through, while thick plate and hardenable steels need enough heat input to lower the cooling rate. The procedure qualification remains the authority.",
"About the Welding Parameter Calculation",
"The welding parameter calculation tool takes plate thickness, material (carbon steel, stainless steel, aluminium alloy), welding position and method, then recommends a welding current range, arc voltage, travel speed, heat input and consumable diameter to support initial process parameter selection.",
"Correction for material and welding position",
"Outputs current, voltage and speed together",
"Heat input range calculation",
"Consumable diameter recommendation",
"Initial welding process parameter selection",
"Parameter estimation before procedure qualification",
"Exploring parameters for new materials",
"Welding teaching and training reference",
"Plate thickness",
    ]))

    write('temp-10', build('temp-10', [
"🌡️ Interpass Temperature Control Calculation",
"Enter the material type, plate thickness and preheat temperature to calculate the recommended interpass temperature range",
"Performs a professional calculation based on the entered material type, plate thickness and preheat temperature, and outputs the result.",
"Low-alloy steel",
"Martensitic stainless steel",
"💡 The interpass temperature is generally not below the preheat temperature; different materials have maximum interpass temperature limits, which matters especially for stainless steel.",
"The minimum interpass temperature usually equals the preheat temperature",
"Austenitic stainless steel interpass temperature must be tightly controlled to prevent intergranular corrosion",
"📚 In-depth analysis: interpass temperature control calculation",
"Set the minimum interpass temperature from the preheat temperature and give the maximum limit by material.",
"In multi-pass welding keep the interpass temperature inside a sensible window to prevent heat-affected zone embrittlement or loss of corrosion resistance.",
"Check whether the preheat temperature exceeds the maximum interpass temperature allowed for that material, catching process conflicts early.",
"Temperature window",
"Take the minimum interpass temperature as the preheat temperature. Maximum interpass temperature by material: low-carbon steel 300°C, low-alloy steel 250°C, austenitic stainless steel 150°C, martensitic stainless steel 350°C. Control points: keep low-carbon steel at or below 300°C to avoid grain coarsening and lost toughness; low-alloy steel at ≤250°C to prevent heat-affected zone embrittlement; austenitic stainless steel below 150°C to avoid carbide precipitation that reduces corrosion resistance; martensitic stainless steel needs a higher interpass temperature plus post-weld heat treatment. If the preheat temperature exceeds the maximum interpass temperature, the tool flags the conflict.",
"Low-alloy steel Q345 preheated to 150°C: recommended interpass temperature 150~250°C. If the measured interpass temperature climbs to 280°C, above the 250°C limit, welding should pause to cool or the welding rhythm should be adjusted, to avoid a loss of heat-affected zone toughness. For austenitic stainless steel 304 with a preheat setting of 180°C, above its 150°C limit, the tool reports a conflict.",
"What problems does too low an interpass temperature cause?",
"Staying below the preheat temperature speeds up cooling of the subsequent passes and raises the risk of hardening and cold cracking, especially for thick plate and high-carbon-equivalent steels. That is why the minimum interpass temperature is normally not below the preheat temperature.",
"Why does austenitic stainless steel have to be kept so low?",
"Austenitic stainless steel that lingers in the 500~800°C range precipitates chromium carbide, causing intergranular chromium depletion (sensitization) and lowering corrosion resistance. Controlling the interpass temperature shortens the time spent in that range.",
"About the Interpass Temperature Control Calculation",
"The interpass temperature control tool takes the material type (low-carbon steel, low-alloy steel, austenitic stainless steel, martensitic stainless steel), plate thickness and preheat temperature, then calculates the recommended interpass temperature range to support temperature control in multi-pass and multi-layer welding.",
"Handles four material types",
"Minimum and maximum interpass temperature calculation",
"Material characteristic notes",
"Preheat temperature sanity check",
"Temperature control in multi-pass and multi-layer welding",
"Stainless steel welding process design",
"Setting welding parameters for low-temperature steels",
"Plate thickness",
"Preheat temperature",
    ]))

    write('temp-time-6', build('temp-time-6', [
"🌡️ Preheat Temperature and Hold Time Calculation",
"Enter plate thickness and carbon equivalent to calculate the preheat temperature and hold time",
"Core formulas (by input variable): cV+mnV÷6+(crV+moV)÷5; 100+(ce-0.5)×500; 150+(ce-0.6)×500",
"Carbon equivalent CEV",
"💡 CEV<0.4 means excellent weldability and generally no preheat; 0.4~0.6 calls for preheat; above 0.6 weldability is poor and a higher preheat temperature is needed.",
"The carbon equivalent can be entered manually or estimated from element contents using the IIW formula",
"Hold time is estimated at 2~3 min/mm, taking the upper end for thick plate",
"📚 In-depth analysis: preheat temperature and hold time calculation",
"Calculate the carbon equivalent CEV from the base metal chemistry, judge the weldability of the steel and decide whether preheat is needed.",
"For thick plate or high-carbon-equivalent steels prone to cold cracking, give a recommended preheat temperature and hold time.",
"Provide quantified evidence for preheat parameters when writing a welding procedure, instead of relying on rule of thumb.",
"Carbon equivalent and preheat",
"IIW carbon equivalent formula: CEV = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15 (all element contents as mass percentages). Preheat conditions: CEV ≥ 0.4 or plate thickness ≥ 25 mm. Preheat temperature T (°C): 0 when CEV<0.4; 80+(CEV−0.4)×200 when 0.4~0.5; 100+(CEV−0.5)×500 when 0.5~0.6; 150+(CEV−0.6)×500 when ≥0.6; then add the thickness term max(0, thickness−10)×2, and if the result falls between 0 and 80°C take 80°C. Hold time (min) = 2.5 × thickness (mm). Weldability: below 0.4 excellent, 0.4~0.5 good, 0.5~0.6 fairly poor, 0.6 or more poor.",
"C=0.20, Mn=1.20, Cr=0.30, Mo=0.10: CEV = 0.20 + 1.20/6 + 0.40/5 = 0.20+0.20+0.08 = 0.48 (good weldability). For 30 mm plate: T = 80+(0.48−0.4)×200 = 96°C, plus the thickness term (30−10)×2 = 40 → 136°C; hold = 2.5×30 = 75 min. If the plate is only 8 mm thick with CEV=0.35, no preheat is needed.",
"Why can the carbon equivalent indicate weldability?",
"Different alloy elements contribute differently to the hardening tendency; once converted into an equivalent carbon content they can be assessed together for sensitivity to cold cracking. The higher the CEV, the more readily the heat-affected zone forms hard brittle martensite, and the more preheat and postheat are needed.",
"Why does the hold time grow with plate thickness?",
"Heavy sections have a large thermal capacity and lose heat quickly, so it takes longer for the whole cross-section to reach a uniform preheat temperature. Estimating at 2~3 min/mm is standard engineering practice, but actual temperature measurement governs.",
"About the Preheat Temperature and Hold Time Calculation",
"The preheat temperature and hold time tool takes plate thickness and carbon equivalent (which can be estimated from C, Mn, Cr, Mo and other element contents using the IIW formula), decides whether preheat is needed, computes the recommended preheat temperature and hold time, and rates the weldability of the material.",
"IIW carbon equivalent formula",
"Preheat necessity decision",
"Preheat temperature and hold time",
"Weldability rating",
"Setting the pre-welding preheat process",
"Assessing weldability of low-alloy steel",
"Preventing cold cracking risk",
"Plate thickness",
"Carbon equivalent CEV",
    ]))

    write('energy-cost-1', build('energy-cost-1', [
"⚡ Welding Energy Cost Accounting",
"Enter current, voltage, welding time and electricity price to calculate arc power, energy consumption and electricity cost",
"Core formulas (by input variable): idleP×(t×(100-duty)÷100)÷60; Parc÷(eff÷100); Pin×duty÷100",
"Welding time (min)",
"Duty cycle (%)",
"Welding machine efficiency (%)",
"💡 Arc power P = U × I ÷ 1000 (kW); actual energy consumption and electricity cost are computed after accounting for machine efficiency and duty cycle.",
"The duty cycle (formerly called intermittent duty factor) is the fraction of total time spent arcing; 60% is a common value",
"The results are for reference only; actual consumption depends on the machine model and working conditions",
"📚 In-depth analysis: welding energy cost accounting",
"Calculate arc power and real power consumption from current, voltage, duty cycle and machine efficiency to account for electricity cost per shift or per part.",
"Include the no-load loss of the welding machine and evaluate the savings available from cutting idle time.",
"Compare the energy level of different welding methods or equipment to judge the economics of an energy-saving retrofit.",
"Energy formulas",
"Arc power Parc (kW) = voltage × current ÷ 1000; machine input power Pin = Parc ÷ efficiency (%)×100; average power Pavg = Pin × duty cycle ÷ 100; arcing time (min) = total time × duty cycle ÷ 100; arcing energy E (kWh) = Pavg × total time (min) ÷ 60; electricity cost = E × unit price. No-load power is estimated at 10% of the arc power; adding it gives total energy and total cost.",
"Current 200 A, voltage 25 V, efficiency 85%, duty cycle 60%, 60 min of work, electricity price CNY 0.8/kWh: Parc = 5.0 kW; Pin = 5.0/0.85 ≈ 5.88 kW; Pavg = 3.53 kW; arcing time 36 min; arcing energy = 3.53×60/60 = 3.53 kWh, electricity cost about CNY 2.82. The 24 min of idling at 0.5 kW adds about 0.20 kWh, giving total energy about 3.73 kWh and total cost about CNY 2.98.",
"Why does the duty cycle affect energy consumption?",
"The machine does not arc the whole time, and the duty cycle reflects the arcing fraction. With intermittent welding the input power is high but average consumption is low, while idling still draws power (about 10% of the arc power), so cutting idle waiting is an effective energy-saving measure.",
"How much can a more efficient machine save?",
"Raising efficiency from 70% to 85% lowers input power by about 18%, which is a clear long-run saving. Inverter welders are usually more efficient than conventional arc welding transformers, which is why they are the main direction for energy-saving retrofits.",
"About the Welding Energy Cost Accounting",
"The welding energy cost tool takes current, voltage, welding time, electricity price, duty cycle and machine efficiency, then computes arc power, arcing energy, average power and electricity cost, and estimates total energy including no-load loss to support welding cost management.",
"Accounts for duty cycle and machine efficiency",
"Outputs arcing energy and total energy",
"Fast electricity cost accounting",
"History can be replayed for comparison",
"Workshop cost accounting",
"Quotation and labour hour assessment",
"Comparing energy-saving retrofits",
"Estimating energy use per production run",
"Welding current",
"Arc voltage",
"Welding time",
"Duty cycle",
"Welding machine efficiency",
    ]))

    write('calc-1', build('calc-1', [
"⚡ Welding Current Selection",
"From the electrode diameter, plate thickness, welding position and electrode type, recommend a manual arc welding current range and estimate the heat input.",
"Manual arc welding current rule of thumb: I = k × d (k is an empirical coefficient, usually 30 to 50, and d is the electrode diameter in mm); welding line energy E = 60 × U × I ÷ v, where U is the arc voltage (V), I the current (A) and v the travel speed (mm/min); the current range is recommended from the electrode diameter and material.",
"Electrode diameter d (mm)",
"Plate thickness t (mm)",
"Horizontal welding",
"Electrode type",
"Cellulosic",
"Titanium type",
"Low-hydrogen",
"Iron powder type",
"Arc voltage U (V)",
"Travel speed v (mm/s)",
"Recommended current",
"Rule of thumb: I = (35 ~ 55) × d, using the lower end for low-hydrogen and the upper end for iron powder",
"Vertical and overhead current is 10% ~ 15% lower than flat welding",
"Heat input E = 60 × U × I / v (J/mm); for low-hydrogen electrodes keep it at ≤ 1.0 ~ 1.5 kJ/mm (depending on the steel grade)",
"Results are reference only and should be adjusted per the electrode data sheet and the procedure qualification",
"📚 In-depth analysis: welding current selection",
"Fix the usable welding current range from the electrode type and diameter, avoiding burn-through from excessive current or slag inclusion from insufficient current.",
"Correct the current by welding position (decreasing from horizontal to vertical to overhead) to obtain operable parameters.",
"Estimate the heat input from voltage and travel speed, and check whether the parameter combination is reasonable.",
"Current model",
"Lower current limit = electrode-type lower coefficient × diameter (mm), upper limit = type upper coefficient × diameter; type coefficients (lower/upper): cellulosic 40/50, titanium-calcium 35/50, basic low-hydrogen 30/45, iron oxide 40/55. Position coefficients: flat 1.0, horizontal 0.95, vertical 0.85, overhead 0.8. Thickness correction: thin plate (<4 mm) uses 0.9/0.95 times, thick plate (>20 mm) uses 1.05/1.10 times. Recommended current = mean of the two limits. Heat input (kJ/mm) = 60 × voltage × current ÷ travel speed (mm/min) ÷ 1000.",
"Basic low-hydrogen electrode of 4.0 mm diameter, flat welding, 12 mm plate: lower limit = 30×4 = 120 A, upper limit = 45×4 = 180 A, recommended about 150 A. Switching to overhead welding, both limits are multiplied by 0.8 → 96~144 A, recommended about 120 A. Taking 24 V and 150 mm/min: heat input = 60×24×150/150/1000 = 1.44 kJ/mm.",
"Why do basic electrodes need less current than titanium-calcium ones?",
"Basic low-hydrogen electrode coatings have poor conductivity and high resistive heating, so excessive current makes the coating glow red and spall off, losing its shielding action, while spatter also increases. Their permissible current ceiling is therefore below that of a titanium-calcium electrode of the same diameter.",
"What defects does too small a current cause?",
"Too small a current makes the arc unstable and the penetration shallow, readily producing lack of fusion, slag inclusions and excess weld metal; too large a current causes undercut, burn-through, heavy spatter and a coarser heat-affected zone. Stay inside the recommended range and fine-tune during test welding.",
    ]))


if __name__ == '__main__':
    main()