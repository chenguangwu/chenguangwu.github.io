#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hvac')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hvac')
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
    out = {'slug': slug, 'industry': 'hvac', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "❄️ HVAC Tools",
        "HVAC",
        "HVAC Tools",
        "Compute the fresh-air total / sensible / latent heat load from psychrometric formulas, suitable for HVAC design selection",
        "Compute the HVAC system supply airflow, air changes, supply outlet count and duct velocity recommendation from the indoor cooling load and supply temperature difference, suitable for preliminary comfort-AC design selection.",
        "Enter airflow, system resistance, fan efficiency and other parameters to compute the fan shaft power, motor power and recommend a standard motor power grade.",
        "Chiller Energy Efficiency Calculator",
        "&#127981; Chiller COP/EER Energy Efficiency Calculator",
        "Pump Head and Flow Calculator",
        "Enter the system flow and piping parameters to auto-compute the pipe velocity, piping resistance loss, pump head and pump shaft power. Suitable for HVAC, water supply/drainage and circulating-water system selection estimation.",
        "Dehumidifier Sizing Calculator",
        "Enter room dimensions, envelope, occupant/equipment heat and orientation to compute envelope, fresh-air and internal heat loads item by item by a simplified cooling-load coefficient method; sum them, multiply by a 1.1 safety factor to give the total cooling load (W), and recommend an AC model and tonnage.",
        "Cooling Tower Calculator",
        "Enter the circulating water flow, inlet/outlet water temperatures and wet-bulb temperature to compute the heat rejected and each water loss, and chart how the concentration ratio affects the makeup water.",
        "Per HVAC design codes, enter the airflow, velocity and duct parameters to compute the cross-sectional area, equivalent diameter, friction resistance, local resistance and total resistance.",
        "Air Filter Efficiency Grade Query Tool",
        "Select a standard and grade to view detailed parameters such as gravimetric efficiency, counting efficiency, face velocity, initial resistance and final resistance.",
        "About HVAC Tools",
        "The HVAC Tools collection gathers 10 free online tools covering common calculation, conversion and lookup needs in HVAC scenarios. Whether you are a professional, student or ordinary user in the field, you can find ready-to-use handy tools here. All tools run entirely in the browser with no data uploaded to the server, protecting privacy and security.",
        "The HVAC tools collected on this page include (representative samples):",
        "These tools help you quickly complete common HVAC-related tasks without memorizing complex formulas or manual conversions; just enter to get results.",
        "Do HVAC Tools need download or registration?",
        "No. All HVAC tools on this page are pure front-end online tools; open the web page and use them directly, with no software installation, no account registration and no data upload.",
        "Are the HVAC Tools calculations accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and common industry standards, with results available instantly. All operations are performed locally on your device, data is never uploaded to a server, and privacy and security are guaranteed.",
    ]))

    write('pump-calculator', build('pump-calculator', [
        "💧 Pump Head and Flow Calculator",
        "Enter the system flow and piping parameters to auto-compute the pipe velocity, piping resistance loss, pump head and pump shaft power. Suitable for HVAC, water supply/drainage and circulating-water system selection estimation.",
        "Pump Head and Flow Calculator",
        "/ Pump Head and Flow Calculator",
        "📖 View the \"Pump Head and Flow Calculator User Guide\"",
        "System flow Q (m³/h)",
        "Total piping length L (m)",
        "Pipe diameter d (mm)",
        "Sum of local resistance coefficients Σξ",
        "Elevation difference Δz (m)",
        "Pump efficiency η (0~1)",
        "Head safety margin (%)",
        "💡 Formula: velocity v = Q/(3600·π·d²/4); friction loss hf = λ·(L/d)·(v²/2g); local loss hj = Σξ·(v²/2g); head H = (hf+hj+Δz)×(1+margin); shaft power N = ρgQH/(3600×1000×η), ρ=1000kg/m³, g=9.81m/s².",
        "Pipe diameter d is entered in millimeters (mm) and auto-converted to meters internally",
        "The friction coefficient λ can be read from the Moody chart; common galvanized steel pipe about 0.025–0.040, plastic pipe about 0.020–0.030",
        "The sum of local resistance coefficients Σξ includes elbows, valves, tees and other fittings; with no data, use references: each elbow ≈0.7–1.5, gate valve ≈0.2, check valve ≈2.0–2.5",
        "Elevation difference Δz is the level difference between the outlet and inlet surfaces; positive for supply (up) direction, negative for return / down",
        "Results are estimates; for actual selection follow the manufacturer's pump performance curve and verify the net positive suction head",
        "📚 In-Depth Analysis: Verifying Pump Head and Shaft Power",
        "Compute total head from pipe friction, local resistance and elevation, add margin and select the pump.",
        "From flow, head and efficiency, compute shaft power to size the motor.",
        "For VFD operation, recompute power at the actual flow point for energy savings.",
        "Flow 50 m³/h, head 120 m, efficiency 70%",
        "Shaft power N = 1000×9.81×(50/3600)×120 ÷ (1000×0.70) ≈ 2.33 kW, select a 3 kW motor; add head margin of 5%–10%.",
        "Efficiency impact",
        "Efficiency 70%→80%, same parameters power drops from 2.33 to 2.04 kW, saving considerable electricity over long runs.",
        "How to estimate head?",
        "Total head = friction loss + local loss + geometric elevation, then multiply by 1.05–1.10 margin to avoid sizing too close to the limit.",
        "Which is fixed first, flow or head?",
        "First fix flow by process, then head by piping resistance; together they determine power and pump type.",
        "About the Pump Head and Flow Calculator",
        "The Pump Head and Flow Calculator is for pump selection estimation in HVAC, water supply/drainage and circulating cooling-water systems. Enter the system flow, piping length, diameter, friction coefficient, sum of local resistance coefficients, elevation and pump efficiency to compute in one click the pipe velocity, friction and local resistance losses, pump head and pump shaft power, with recommended motor power and velocity evaluation.",
        "Pure front-end calculation with no data uploaded to the server",
        "Real-time calculation, results update on input",
        "Data cards clearly show head, power and velocity",
        "Auto-recommends standard motor power",
        "Smart pipe-velocity evaluation with reference ranges",
        "HVAC chilled / cooling water pump selection",
        "Building water-supply booster pump estimation",
        "Circulating-water system piping resistance check",
        "Agricultural irrigation and garden water-supply design",
        "Industrial circulating pump power verification",
        "How to use the Pump Head and Flow Calculator",
        "What does the Pump Head and Flow Calculator do?",
        "How to use the Pump Head and Flow Calculator?",
        "What scenarios is the Pump Head and Flow Calculator for?",
        "System flow, cubic meters per hour",
        "Total piping length, meters",
        "Pipe diameter, millimeters",
        "Friction coefficient",
        "Sum of local resistance coefficients",
        "Elevation difference, meters (can be negative)",
        "Pump efficiency",
        "Head safety margin, percent",
    ]))

    write('supply-air', build('supply-air', [
        "🏎️ Supply Air Volume and Velocity Design Calculator",
        "Compute the HVAC system supply airflow, air changes, supply outlet count and duct velocity recommendation from the indoor cooling load and supply temperature difference, suitable for preliminary comfort-AC design selection.",
        "📖 View the \"Supply Air Volume and Velocity Design Calculator User Guide\"",
        "Supply air volume L = Q / ( ρ × c",
        "Q — indoor cooling load (W) | ρ — air density",
        "— air constant-pressure specific heat",
        "| Δt — supply air temperature difference (°C)",
        "Air changes n = L / V | supply outlets = ⌈ L(m³/h) / 500 ⌉",
        "Indoor cooling load Q (W)",
        "1 W = 0.86 kcal/h, common rooms 80–150 W/m²",
        "Supply air temperature difference Δt (°C)",
        "Comfort AC recommended 8–10°C",
        "Area × floor height, e.g. 40 m²×3 m",
        "Supply temperature-difference presets:",
        "📊 Calculation result",
        "🌬️ Duct velocity design recommendation",
        "Recommend duct area and equivalent diameter at main-duct velocity 6–10 m/s and branch-duct velocity 4–6 m/s.",
        "Duct area A = L(m³/s) / v; equivalent circular diameter d = √(4A/π). Actual engineering must combine noise control, resistance and rectangular aspect ratio comprehensively.",
        "📋 Airflow comparison at different supply temperature differences",
        "At the same cooling load, a larger supply temperature difference needs less airflow (energy-saving but watch temperature gradient and draft sensation).",
        "📚 Design reference",
        "Air-changes evaluation (comfort AC)",
        "n < 5 ACH/h: low, possible insufficient ventilation and uneven temperature distribution",
        "5 ≤ n ≤ 10 ACH/h: suitable, the recommended range for conventional comfort AC",
        "10 < n ≤ 15 ACH/h: high, watch air distribution and noise control",
        "n > 15 ACH/h: too high, recommend increasing the supply temperature difference to reduce airflow",
        "Duct velocity recommendation (GB 50736 reference)",
        "Main duct: 6–10 m/s, recommended 8 m/s",
        "Branch duct: 4–6 m/s, recommended 5 m/s",
        "Supply outlet neck velocity: 2–5 m/s (depends on outlet type)",
        "Too high velocity increases noise and resistance; too low makes the duct section large and space-consuming",
        "Supply temperature-difference selection",
        "Comfort AC (constant volume): 8–10°C",
        "Variable-air-volume (VAV) system: 8–12°C",
        "Large space / stratified AC: 10–14°C",
        "Too large a difference causes a large working-zone temperature gradient and draft sensation",
        "📚 In-Depth Analysis: Supply Air Volume and Air-Changes Design",
        "Back-calculate the required supply airflow from room volume and air changes.",
        "From the supply temperature difference compute the sensible supply airflow, and check outlet count and per-outlet airflow.",
        "Compare energy and comfort at different air-changes.",
        "Room 2500 m³, 8 ACH/h",
        "Supply airflow L = 2500×8 = 20000 m³/h; if the supply temperature difference is 8°C the sensible airflow is computed separately, with outlets sized at 1000 m³/h each for about 20 outlets.",
        "Outlet count",
        "Total airflow 20000 ÷ 1000 per outlet = 20 supply outlets, arranged evenly to avoid short-circuiting and dead zones.",
        "How many air changes to take?",
        "By room use: office 6–10, lab/pharmacy higher; refer to cleanliness and occupancy density.",
        "Is a larger or smaller supply temperature difference better?",
        "Larger difference saves airflow but risks draft; smaller is comfortable but larger airflow and footprint; trade off by comfort and space.",
        "About the Supply Air Volume and Velocity Design Calculator",
        "The Supply Air Volume and Velocity Design Calculator is an online HVAC design tool that, from the indoor cooling load, supply temperature difference and room volume, quickly computes the AC supply airflow, air changes, recommended supply outlet count and the main/branch duct velocity, area and equivalent diameter, and auto-generates an airflow comparison table across supply temperature differences, aiding preliminary HVAC system design and equipment selection.",
        "Uses the standard supply-air formula L=Q/(ρ·cp·Δt)",
        "Auto-converts between m³/s and m³/h dual units",
        "Air-changes evaluation and design advice",
        "Main/branch duct velocity and equivalent-diameter recommendation",
        "Multi-temperature-difference airflow comparison table",
        "Automatic supply-outlet count estimation",
        "Preliminary design of comfort AC systems",
        "AC supply airflow and duct-size estimation",
        "Supply-outlet count and air-distribution planning",
        "HVAC course study and design assignments",
        "Quick on-site airflow verification",
        "VAV system temperature-difference comparison",
        "Toggle dark mode",
        "e.g. 2500",
        "Comfort AC 8–10°C",
        "Used for air-changes calculation",
    ]))


if __name__ == '__main__':
    main()
