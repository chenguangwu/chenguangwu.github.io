#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'petrochem')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'petrochem')
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
    out = {'slug': slug, 'industry': 'petrochem', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('api-gravity', build('api-gravity', [
        '🔄 API Gravity and Density Conversion',
        'Convert between crude oil API gravity, specific gravity (SG) and density, and classify the crude automatically',
        '"Convert between crude oil API gravity, specific gravity (SG) and density, and classify the crude automatically" — the tool runs a professional calculation from the input parameters and outputs the result.',
        '/ API Gravity',
        '📖 View the API Gravity and Density Conversion user guide',
        'Enter API gravity',
        'Enter specific gravity / density',
        '= SG × water density (g/cm³)',
        '📚 In-depth analysis: API Gravity and Density Conversion',
        'Crude trading and pricing: crudes from different producing regions are quoted by API gravity and must be converted to specific gravity (SG) and density (g/cm³, kg/m³) before mass, volume and shipping stowage can be calculated; the tool converts between API and SG, so entering either one gives the other.',
        'Refinery unit design and blending: when blending crudes the mixed specific gravity is checked against density; a higher API gravity means a lighter crude and usually higher economic value. The classify step quickly identifies light / medium / heavy / extra-heavy.',
        'Laboratory work and custody transfer: custody transfer usually uses the standard density at 60 °F (15.6 °C). This tool converts density against a 60 °F water relative density of 1.0, making it easy to compare with measurement tickets.',
        'Worked example: converting API gravity to relative density and grade',
        'At API = 30, SG = 141.5/(30+131.5) = 0.8762, density (water = 1.0) = 0.8762 g/cm³ = 876.2 kg/m³; classify(30): 22.3 ≤ 30 ≤ 31.1 → medium crude.\nAt API = 35, SG = 141.5/166.5 = 0.8498, density 0.8498 g/cm³, classify(35) > 31.1 → light crude.\nBack-calculation: SG = 0.85 → API = 141.5/0.85 − 131.5 = 34.97 °API (light). Classification thresholds: >31.1 light, ≥22.3 medium, ≥10 heavy, <10 extra-heavy / bitumen.',
        'How is API gravity defined?',
        'API gravity is the American Petroleum Institute relative-density scale: °API = 141.5/SG − 131.5, where SG is the relative density at 60 °F. The larger the value, the lighter the oil; at °API = 10, SG = 1.0 (the same weight as water) — above 10 the oil is lighter than water, below 10 it is heavier.',
        'How is crude classified by weight?',
        'Common cut-offs: API > 31.1 light crude, 22.3–31.1 medium, 10–22.3 heavy, < 10 extra-heavy or bitumen. Light crudes are easier to refine into high-value fractions and usually carry a premium.',
        'About API Gravity',
    ]))

    write('catalyst-calc', build('catalyst-calc', [
        '🧮 Catalyst Loading and Reaction Time',
        'Calculate catalyst loading and reaction time from feed rate, space velocity or residence time',
        '"Calculate catalyst loading and reaction time from feed rate, space velocity or residence time" — the tool runs a professional calculation from the input parameters and outputs the result.',
        '/ Catalyst Calc',
        '📖 View the Catalyst Loading and Reaction Time user guide',
        'Loading from space velocity',
        'Loading from residence time',
        '📚 In-depth analysis: Catalyst Loading and Reaction Time',
        'Fixed-bed reactor design: derive the catalyst loading volume and mass from the feed mass flow and space velocity (LHSV); a smaller space velocity means a longer residence time and a higher ',
        'conversion',
        ', but also a larger vessel.',
        'Residence time check: given a target residence time (seconds), back-calculate the required catalyst amount and the equivalent space velocity — useful for quick loading estimates during revamps or catalyst change-outs.',
        'Catalyst procurement and loading: mass (kg) = volume × bulk density; combined with the unit price per batch you can estimate the purchase quantity and avoid over-buying or under-loading that delays start-up.',
        'Worked example: one space-velocity case and one residence-time case',
        'Space-velocity mode: feed 1000 kg/h, LHSV = 2 h⁻¹, feedstock density 800, bulk density 700. ',
        '= 1000/800 = 1.2500 m³/h; catalyst volume = 1.25/2 = 0.6250 m³; mass = 0.6250 × 700 = 437.5 kg; residence time = 3600/2 = 1800 s.\nTime mode: feed 1000 kg/h, target residence 1800 s, density 800, bulk density 700. Volumetric flow = 1.2500 m³/h; catalyst volume = (1.25/3600) × 1800 = 0.6250 m³; mass = 437.5 kg; equivalent space velocity = 3600/1800 = 2.000 h⁻¹. The two modes agree when the parameters are consistent.',
        'What is space velocity (LHSV)?',
        'Liquid hourly space velocity LHSV = feed volumetric flow / catalyst volume (unit h⁻¹); it expresses how much material passes through one catalyst volume per hour. The smaller the LHSV, the longer the residence time and generally the higher the conversion.',
        'How is catalyst loading obtained from space velocity?',
        'Catalyst volume = feed volumetric flow ÷ space velocity; multiply by bulk density to get the mass (kg). Feed volumetric flow = mass flow ÷ feedstock density. Residence time = 3600 ÷ space velocity (seconds).',
        'About Catalyst Calc',
    ]))

    write('distillation-yield', build('distillation-yield', [
        '🧮 Distillation Yield and Mass Balance',
        'Check the yield and mass balance from the feed quantity and the output of each product',
        '"Check the yield and mass balance from the feed quantity and the output of each product" — the tool runs a professional calculation from the input parameters and outputs the result.',
        '/ Distillation Yield',
        '📖 View the Distillation Yield and Mass Balance user guide',
        '📚 In-depth analysis: Distillation Yield and Mass Balance',
        'Atmospheric, vacuum and cracking unit mass balance: given the feed quantity (tonnes) and the output of each fraction, the tool computes the yield per product and totals the overall yield plus loss or residue, to judge whether the unit is running in balance.',
        'Scheme comparison: compare the product distributions under different operating conditions (for example a propylene-maximising scheme); the yield bars give a direct visual comparison of each fraction’s share to support process optimisation.',
        'Loss audit: when the total yield deviates noticeably from 100% (loss rate > 5%), a large-deviation warning is highlighted, pointing to a metering error or to by-products and loss items that were not accounted for.',
        'Worked example: two-product distribution with 1000 t of feed',
        'Feed = 1000 t, products: ethylene 480 t, propylene 290 t (the rest is by-product and loss, not listed separately).\nEthylene yield = 480/1000 × 100% = 48.0%; propylene yield = 290/1000 × 100% = 29.0%; total products = 770 t; total yield = 77.0%; loss or residue = 1000 − 770 = 230 t; loss rate = 23.0%. A loss rate above 5% is judged a large deviation, so check by-product metering or loss items.',
        'How are yield and mass balance calculated?',
        'Single-product yield = that product’s output ÷ feed × 100%; total yield = sum of all product outputs ÷ feed × 100%; loss = feed − total products, loss rate = loss ÷ feed × 100%. When the balance is good the total yield is close to 100%.',
        'Why is there loss or residue?',
        'Losses come from column bottoms residue, uncondensed light components, material clinging to equipment walls and metering errors, plus by-products that are not listed separately. A persistently high loss rate means operation and design should be reviewed, although a small loss is normal in continuous distillation.',
        'About Distillation Yield',
    ]))

    write('pipe-pressure', build('pipe-pressure', [
        '🎚️ Pipe Pressure Drop (Darcy equation)',
        'Compute the straight-pipe pressure loss with the Darcy-Weisbach equation',
        '/ Pipe Pressure',
        '📖 View the Pipe Pressure Drop (Darcy equation) user guide',
        'Volumetric flow rate (m³/h)',
        'Darcy-Weisbach equation',
        'Flow velocity',
        'Reynolds number',
        'Laminar friction factor',
        'Note: this tool computes only the straight-pipe friction pressure drop; local resistances (elbows, valves and the like) are not included and must be added separately.',
        '📚 In-depth analysis: Pipe Pressure Drop (Darcy equation)',
        'Pump and',
        'compressor selection',
        ': from the flow rate, pipe diameter, pipe length, medium density and viscosity, and pipe wall roughness, use',
        'the Darcy-Weisbach equation',
        'to compute the total pressure drop, and from it select the pump head or compressor pressure ratio.',
        'Flow regime determination: the tool first computes',
        'Re to decide whether the flow is laminar, transitional or turbulent; laminar flow uses f = 64/Re and turbulent flow uses the explicit Swamee-Jain approximation, avoiding iteration.',
        'Pipeline revamp assessment: change the pipe diameter or roughness to see how the pressure drop and the resistance per metre vary, quantify the energy saving from enlarging the diameter and support the revamp decision.',
        'Worked example: one transitional-flow case and one laminar-flow case',
        'Transitional flow: flow 100 m³/h, diameter 200 mm, length 500 m, density 900, viscosity 50 mPa·s, roughness 0.1 mm. Velocity = 0.884 m/s; Re = ρvD/μ = 900 × 0.884 × 0.2/0.05 ≈ 3183 (turbulent region); Swamee-Jain f ≈ 0.0442; total pressure drop = 0.0442 × (500/0.2) × (900 × 0.884²/2) ≈ 38.84 kPa (0.3884 bar), about 77.7 Pa/m.\nLaminar flow: flow 1 m³/h, diameter 50 mm, length 100 m, density 1000, viscosity 100 mPa·s, roughness 0.05 mm. Velocity = 0.141 m/s; Re ≈ 71 (laminar); f = 64/71 ≈ 0.9048; total pressure drop ≈ 18.11 kPa.',
        'How does the Reynolds number Re determine the flow regime?',
        'Re = ρvD/μ, where ρ is density, v velocity, D pipe diameter and μ dynamic viscosity. Re < 2300 is laminar, 2300–4000 transitional and > 4000 turbulent. The regime determines which friction factor correlation is used.',
        'How is the friction factor f obtained?',
        'For laminar flow use f = 64/Re; for turbulent flow use the explicit Swamee-Jain formula f = 0.25/[log10(ε/(3.7D) + 5.74/Re^0.9)]², where ε is the absolute roughness of the pipe wall.',
        'Darcy pressure drop',
        'About Pipe Pressure',
    ]))

    write('tank-capacity', build('tank-capacity', [
        '🧊 Tank Capacity and Level Conversion',
        'Convert between the total capacity and the volume corresponding to a liquid level for vertical and horizontal cylindrical tanks',
        '/ Tank Capacity',
        '📖 View the Tank Capacity and Level Conversion user guide',
        'Note: horizontal tanks are treated as flat-headed; spherical or dished heads must be calculated separately. This tool estimates using flat heads.',
        '📚 In-depth analysis: Tank Capacity and Level Conversion',
        'Oil inventory counting: for a vertical dome-roof tank, use the',
        'cylinder volume',
        'to get the total capacity, and the stored oil mass (tonnes) from the current level height; the tool outputs total capacity, safe capacity and current volume to support inventory checks and scheduling.',
        'Horizontal tank level metering: the liquid surface of a horizontal tank is a circular segment, so the cylinder formula cannot be applied directly; the tool multiplies the segment area by the tank length to obtain the liquid volume — the liquid level-to-',
        'volume conversion needed for road tankers and horizontal buffer tanks.',
        'Safe filling check: after setting a safe filling ratio (for example 90%), an alarm is raised when the current level exceeds the safe upper limit, preventing thermal expansion or tank overflow and meeting tank safety operating rules.',
        'Worked example: one vertical case and one horizontal case',
        'Vertical tank D = 4 m, L = 10 m, level 8 m, density 850, safe ratio 90%: total capacity = π × (2)² × 10 = 125.66 m³; safe capacity = 125.66 × 90% = 113.10 m³; liquid volume = π × (2)² × 8 = 100.53 m³; mass = 100.53 × 850/1000 = 85.45 t; filling ratio = 100.53/125.66 = 80.0%.\nHorizontal tank D = 3 m, L = 8 m, level 1.5 m (= radius, half full), density 750: total capacity = π × (1.5)² × 8 = 56.55 m³; segment area = 1.5² × acos(0) − 0 = 3.534 m²; liquid volume = 3.534 × 8 = 28.27 m³; mass = 28.27 × 750/1000 = 21.21 t; filling ratio = 50.0%.',
        'How do the vertical and horizontal tank formulas differ?',
        'A vertical tank has a rectangular liquid cross-section, so liquid volume = π × r² × level height; a horizontal tank has a circular-segment cross-section, so the segment area formula area = r²·acos((r−h)/r) − (r−h)·√(2rh−h²) must be used and then multiplied by the tank length — at half full (h = r) it is exactly half the tank.',
        'How are the safe level and safe capacity used?',
        'Safe capacity = total capacity × safe filling ratio (%); when the current liquid volume exceeds the safe capacity the tool warns that the level is above the safe limit. The setting reserves space for thermal expansion and vapour space and prevents overflow; the actual upper limit depends on the tank type and the medium.',
        'About Tank Capacity',
    ]))


if __name__ == '__main__':
    main()
