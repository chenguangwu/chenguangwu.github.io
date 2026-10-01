#!/usr/bin/env python3
# energy batch8 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'energy')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'energy')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'battery-capacity-wh': [
"Battery Capacity Conversion",
"/ Battery Capacity Conversion",
'📖 View the "Battery Capacity Conversion (Ah ↔ Wh) User Guide"',
"Energy (Wh) = capacity (Ah) × voltage (V).",
"Capacity (Ah)",
"Voltage (V)",
"Runtime = energy / load power.",
"📚 In-Depth Analysis: Battery Capacity Conversion (Ah ↔ Wh)",
"Unify the Ah of cells at different voltages into Wh for comparison.",
"Estimate the total energy of a battery pack for an energy storage system.",
"Check the rated Wh against transport/airline limits.",
"12V 100Ah battery energy",
"Wh=12×100=1200 Wh=1.2 kWh. With an average load of 50 W, the ideal runtime ≈1200/50=24 h (excluding efficiency and depth of discharge). Tip: for lithium batteries a depth of discharge within 80% is recommended to extend life.",
"Which better represents capacity, Ah or Wh?",
"Wh is energy and comparable across voltages; Ah only represents charge and cannot be compared directly at different voltages. For selection and runtime, Wh is more accurate.",
"Why do airlines look at Wh?",
"Civil aviation limits carriage by cell Wh (usually ≤100 Wh carry-on, 100-160 Wh requires approval), because Wh directly reflects the energy and safety risk.",
],
'r-value-insulation': [
"Thermal Resistance from Thickness and Thermal Conductivity",
"Enter the material thickness d and thermal conductivity k to compute the thermal resistance R.",
"Thermal Resistance (R-value) Calculator",
"/ Thermal Resistance (R-value) Calculator",
'📖 View the "Thermal Resistance from Thickness and Thermal Conductivity User Guide"',
"The larger R is, the better the insulation.",
"📚 In-Depth Analysis: Thermal Resistance from Thickness and Thermal Conductivity",
"Compare the R-value of wall/roof insulation layers of different thicknesses.",
"Estimate the heat transfer coefficient U=1/R and the total thermal resistance.",
"Compare the heating load before and after a retrofit.",
"100mm rock wool insulation",
"Rock wool k≈0.040 W/(m·K), thickness 0.1 m: per-unit-area R=0.1/0.04=2.5 (m²·K)/W, U=0.4 W/(m²·K). If thickened to 200 mm, R=5, U=0.2, halving the heat transfer. Tip: including the inner and outer surface heat transfer resistance makes the total U slightly higher.",
"Is a larger R-value better for insulation?",
"Yes. R is the thermal resistance; the larger it is, the better the heat blocking and the smaller U; but it is limited by thickness, cost and space, and there is an economic thickness.",
"Why insulate in the south too?",
"Insulation serves both summer heat shielding and winter warmth, reducing air conditioning/heating loads, and also prevents moisture and condensation.",
],
'conductive-heat-rate': [
"Heat Rate from Thermal Conductivity, Area, Temperature Difference and Thickness",
"Enter the thermal conductivity k, area A, temperature difference ΔT and thickness d to compute the heat rate.",
"Thermal Conduction Heat Rate Calculator",
"/ Thermal Conduction Heat Rate Calculator",
'📖 View the "Heat Rate from Thermal Conductivity, Area, Temperature Difference and Thickness User Guide"',
"Fourier's law of heat conduction.",
"📚 In-Depth Analysis: Heat Rate from Thermal Conductivity, Area, Temperature Difference and Thickness",
"Estimate the steady-state heat loss of walls/pipes.",
"Thermal conduction design of radiators/heat exchangers.",
"Compare the heat transfer rate of different materials.",
"Pipe heat loss estimation",
"Steel pipe k=45, cross-sectional area 0.05 m², temperature difference 60℃, wall thickness 0.005 m: Q=45×0.05×60/0.005=27000 W=27 kW. After wrapping with 50 mm rubber-plastic (k=0.04), Q≈45×0.05×60/0.05≈270 W, a 99% reduction in heat loss. Tip: the outer surface temperature of the insulation also needs burn/condensation protection.",
"Is a smaller thermal conductivity more insulating?",
"Yes. A smaller k means less heat is transferred per unit time, the core indicator of insulation materials; but note the effects of temperature range and humidity.",
"What is the difference between steady state and transient?",
"In steady state the temperature difference is constant and the heat flow is unchanged; startup/seasonal changes are transient and require considering heat capacity and delay; engineering often uses the steady-state estimate as the upper bound.",
],
'power-factor-calc': [
"Active / Apparent",
"/ Power Factor",
'📖 View the "power-factor-calc User Guide"',
"Apparent power S (kVA)",
"A low PF requires reactive power compensation.",
"📚 In-Depth Analysis: Active / Apparent",
"Assess the reactive power compensation need to reduce the basic electricity cost.",
"Local compensation at motors raises the PF and reduces line loss.",
"Understand the power factor adjustment electricity fee rewards/penalties.",
"Reactive compensation cost-saving example",
"Load active power 80 kW, PF 0.7, target 0.95: the apparent current drops from 80/(0.38×0.7)≈300 A to 80/(0.38×0.95)≈222 A, and the line loss drops to about 55% by I²R; meeting the PF standard also avoids the power factor penalty. Tip: capacitor compensation must guard against over-compensation and resonance.",
"What are the disadvantages of a low power factor?",
"For the same active power, the current is larger, raising line loss and voltage drop; transformer/line capacity is occupied by reactive power, and the supplier often charges a power factor penalty.",
"How to improve it?",
"Connect capacitors in parallel with inductive loads (motors) or use local SVG compensation; for VFD/rectifier loads, use active filtering that also compensates.",
],
'energy-density': [
"Energy / Mass",
"/ Energy Density",
'📖 View the "Energy / Mass User Guide"',
"Lithium batteries are about 0.1-0.3 kWh/kg.",
"Gasoline is about 12 kWh/kg.",
"📚 In-Depth Analysis: Energy / Mass",
"Compare the volume footprint of a battery pack and a fuel tank.",
"Volumetric density of hydrogen storage/compressed gas.",
"Selection for volume-constrained portable devices.",
"Fuel tank vs battery volume",
"Gasoline is about 9000 Wh/L, a typical lithium battery pack about 250-400 Wh/L, so for the same energy the battery volume is dozens of times that of a fuel tank; therefore heavy long-haul vehicles tend toward fuel or hybrid. Tip: including the system (cooling/structure) makes the gap even larger.",
"Is high energy density always better?",
"It is good for space-constrained scenarios, but power density, safety and cost must also be considered; high energy density often comes with safety risks (e.g., certain lithium battery chemistries).",
"Why do volumetric and gravimetric densities differ?",
"Density = energy / volume, specific energy = energy / mass; different material densities can make the two rankings differ.",
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
    out = {'slug': slug, 'industry': 'energy', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
