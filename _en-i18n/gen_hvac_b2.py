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
    write('cooling-load', build('cooling-load', [
        "❄️ Air Conditioning Load Calculator",
        "Based on a simplified cooling-load coefficient method, calculate each cooling-load component of a room and provide AC selection advice",
        "Core formula (by input variable): Math.ceil(total ÷ HP_WATT); freshVol × RHO × dh ÷ 3.6; V × ρ × Δh ÷ 3.6 (W)",
        "📖 View the \"Air Conditioning Load Calculator User Guide\"",
        "🏗️ Envelope structure parameters",
        "Exterior wall area (m²)",
        "Exterior wall heat-transfer coefficient K (W/m²·K)",
        "Window area (m²)",
        "Double glazing",
        "Low-E double glazing",
        "Window heat-transfer coefficient K_win (W/m²·K)",
        "Indoor design temperature tn (°C)",
        "Outdoor design temperature tw (°C)",
        "👥 Internal heat sources",
        "Number of occupants (persons)",
        "Activity level",
        "Sedentary (residential / still)",
        "Very light work (office)",
        "Light work",
        "Moderate work",
        "Heavy work",
        "Equipment simultaneous-use factor",
        "🌬️ Fresh-air parameters",
        "Fresh-air rate standard (m³/h·person)",
        "Outdoor enthalpy hw (kJ/kg)",
        "Indoor enthalpy hn (kJ/kg)",
        "❄️ Calculate cooling load",
        "Calculation basis: Q1=K·F·(tw-tn) exterior-wall conduction; Q2=K_win·F_win·(tw-tn)+solar radiation; Q3=occupants×(sensible+latent); Q4=equipment power×simultaneous-use factor; Q5=lighting power×0.8; Q6=fresh-air×ρ×(hw-hn); total load Q=ΣQi×1.1 (safety factor). Air density ρ=1.2 kg/m³.",
        "This tool adopts the",
        "simplified cooling-load coefficient method",
        ", suitable for preliminary HVAC design and selection estimation of general civil buildings",
        "The solar-radiation addition is auto-computed from the vertical-surface solar irradiance by orientation (summer typical value) × window area × shading coefficient SC",
        "Switching window type or activity level auto-fills the corresponding heat-transfer coefficient, SC and fresh-air standard; values can be edited manually",
        "Enthalpy is an air-state parameter; in summer the outdoor is about 85 kJ/kg and the indoor at 26°C/50% about 53 kJ/kg, adjustable per the actual psychrometric chart",
        "Results are for reference only; for actual engineering, perform detailed calculations per 'Design Code for Heating, Ventilation and Air Conditioning of Civil Buildings' GB 50736",
        "📚 In-Depth Analysis: Superposing Air-Conditioning Cooling-Load Components",
        "For an office, sum the five components of envelope, occupants, equipment, lighting and fresh-air to get the total cooling load.",
        "For rooms with different functions (server room / meeting room / shop) reweight and recompute each component.",
        "After estimating the total cooling load, back-calculate the chiller capacity and power distribution.",
        "100 m² office",
        "Envelope q1≈30 W/m²×100=3000 W, occupants 10×120 W=1200 W, equipment 2 kW×0.8=1600 W, lighting 1 kW×0.8=800 W, fresh-air about 1500 W; total ≈ 8100 W ≈ 8.1 kW.",
        "Indicator method (rough estimate)",
        "Take the composite indicator 150 W/m² × 100 m² = 15 kW as an upper-bound reference, and compare with the component method to pick a safe value.",
        "Which to use, component method or indicator method?",
        "Use the indicator method for a quick estimate at the scheme stage, and the component method for item-by-item check at detailed design; if the two deviate greatly, review each input.",
        "Fresh-air load",
        "Why is its share so high?",
        "In summer the outdoor enthalpy is far above indoor, so fresh air often accounts for 20%–40% of the total load and is a key energy-saving focus.",
        "About the Air Conditioning Load Calculator",
        "The Air Conditioning Load Calculator is an HVAC design aid based on the simplified cooling-load coefficient method. After entering room envelope, internal heat sources and fresh-air parameters, it auto-computes the six cooling-load components of exterior wall, windows (including solar-radiation addition), occupants, equipment, lighting and fresh-air, and summarizes the total cooling load, area load indicator and AC tonnage selection advice. It runs entirely in the browser with no data uploaded, suitable for preliminary HVAC design and selection estimation.",
        "Simplified cooling-load coefficient method covering six major heat sources",
        "Window type auto-matches heat-transfer coefficient and shading coefficient SC",
        "Solar-radiation addition load auto-computed by orientation",
        "Activity level auto-matches per-person sensible/latent heat and fresh-air standard",
        "Data cards + proportion bar chart clearly show each load",
        "Automatic area indicator and AC tonnage selection advice",
        "Residential / office AC selection estimation",
        "HVAC course design and load-calculation exercises",
        "Quick cooling-capacity demand assessment before renovation",
        "Server room / commercial space cooling-capacity check",
        "Fresh-air system airflow and load check",
        "Building energy-efficiency and insulation-retrofit assessment",
        "Window orientation",
        "Exterior wall area",
        "Exterior wall heat-transfer coefficient",
        "Window area",
        "Window type",
        "Window heat-transfer coefficient",
        "Indoor design temperature",
        "Outdoor design temperature",
        "Number of occupants",
        "Occupant activity level",
        "Equipment simultaneous-use factor",
        "Lighting power",
        "Fresh-air rate standard",
        "Outdoor enthalpy",
        "Indoor enthalpy",
    ]))

    write('cooling-tower', build('cooling-tower', [
        "❄️ Cooling Tower Heat Rejection and Makeup Water Calculator",
        "Enter the circulating water flow, inlet/outlet water temperatures and wet-bulb temperature to compute the heat rejected and each water loss, and chart how the concentration ratio affects the makeup water.",
        "Core formula (by input variable): 4.187 × G × 1000 × dT ÷ 3600; G × dT × 0.0015; E ÷ (N - 1)",
        "Cooling Tower Calculator",
        "📖 View the \"Cooling Tower Heat Rejection and Makeup Water Calculator User Guide\"",
        "Circulating water flow G (m³/h)",
        "Inlet water temperature t",
        "Outlet water temperature t",
        "Wet-bulb temperature t",
        "Concentration ratio N",
        "Drift loss rate (share of circulating water)",
        "📊 Effect of concentration ratio on makeup water",
        "As the concentration ratio N increases, the blowdown loss B drops and the total makeup M approaches the sum of evaporation and drift (E+D), with diminishing water-saving returns.",
        "📖 Formulas and notes",
        "Heat rejected:",
        "Cooling range:",
        "Approach:",
        "Evaporation loss:",
        "Drift loss:",
        "D = G × drift rate",
        "(default 0.001, i.e. 0.1%)",
        "Blowdown loss:",
        "Total makeup water:",
        "c is the specific heat of water 4.187 kJ/(kg·°C); water density is taken as 1000 kg/m³; the evaporation coefficient 0.0015 /°C is a common empirical value. Raising the concentration ratio markedly reduces blowdown and makeup, but too high accelerates scaling and corrosion risk; in practice N = 3–8 is typical.",
        "📚 In-Depth Analysis: Estimating Cooling Tower Heat Rejection and Evaporative Makeup",
        "Use the circulating water flow and inlet/outlet temperature difference to verify heat-rejection capacity and check the cooling-tower selection.",
        "Estimate the makeup water from evaporation + drift + blowdown to support water-treatment and makeup design.",
        "Use the wet-bulb temperature approach to evaluate cooling-tower performance in humid weather.",
        "Water flow 600 m³/h, inlet/outlet 37/32°C",
        "Heat rejected Q = 600×4.18×5 ÷ 3.6 ≈ 3483 kW; evaporative water ≈ 600×5 ÷ 580 ≈ 5.17 m³/h, and makeup is roughly estimated as evaporation + blowdown.",
        "Approach check",
        "The approach of outlet 32°C vs wet-bulb 27°C is 5°C; a smaller value means a larger, costlier tower, so balance investment against condensing temperature.",
        "How to estimate evaporative water?",
        "Engineering approximation: about 1% of circulating water evaporates per 5.8°C temperature difference, i.e. G×ΔT/580, for quick makeup estimation.",
        "Is a smaller approach always better?",
        "Smaller means outlet closer to wet-bulb and higher unit efficiency, but tower size and cost rise, so weigh against payback.",
        "The evaporation coefficient 0.0015/°C is a common empirical value; in practice it should be adjusted for climate and water quality",
        "The drift loss rate defaults to 0.1%; new drift-eliminator cooling towers can be as low as 0.001%–0.005%",
        "Results are for reference only; for engineering design, determine them comprehensively with water-quality tests and equipment-manufacturer parameters",
        "About the Cooling Tower Heat Rejection and Makeup Water Calculator",
        "The Cooling Tower Heat Rejection and Makeup Water Calculator quickly estimates a cooling tower's heat rejection, cooling range and approach, as well as the evaporative, drift and blowdown water losses and total makeup, and clearly charts how the concentration ratio affects makeup. It is a practical tool for HVAC and circulating cooling-water system operation.",
        "Heat rejection precisely computed as Q=c·m·Δt",
        "Evaporation / drift / blowdown losses shown by category",
        "Concentration-ratio influence curve chart",
        "Supports custom drift loss rate",
        "Cooling-tower selection and makeup design",
        "Circulating cooling-water system operation",
        "Water-saving and water-treatment scheme evaluation",
        "HVAC engineering teaching demonstration",
    ]))

    write('dehumidifier', build('dehumidifier', [
        "🧮 Dehumidifier Sizing Calculator",
        "Calculate the dehumidification load and recommend a dehumidifier capacity from the room volume, temperature, humidity and air changes. Based on standard atmospheric pressure (101.325 kPa) and the Magnus saturation-vapor-pressure formula.",
        "Core formula (by input variable): max(6, Wday × 1.3); massFlow × dD ÷ 1000; W × 24",
        "Dehumidifier Sizing Calculator",
        "/ Dehumidifier Sizing Calculator",
        "📖 View the \"Dehumidifier Sizing Calculator User Guide\"",
        "Current temperature",
        "Air changes",
        "(ACH/h)",
        "Current relative humidity",
        "Target relative humidity",
        "Relative-humidity band",
        "Target 55%",
        "Comfort 40–60%",
        "Slightly humid 60–70%",
        "Over-humid >70%",
        "Basement",
        "Warehouse",
        "Bedroom",
        "Bathroom",
        "Southern rainy season",
        "📊 Start calculation",
        "📈 Calculation result",
        "🔢 Calculation process",
        "🎯 Recommended dehumidifier capacity",
        "📚 Saturated humidity-ratio reference table",
        "At standard atmospheric pressure (101.325 kPa), the saturated humidity ratio d at 100% relative humidity for each temperature",
        "(g/kg dry air).",
        "How to read the table",
        ": at the same temperature, the actual humidity ratio = saturated humidity ratio × relative humidity (%). The higher the temperature, the more moisture air can hold and the larger the saturated humidity ratio.",
        "About the Dehumidifier Sizing Calculator",
        "The Dehumidifier Sizing Calculator is an online tool for HVAC and everyday moisture-proofing. Enter the room volume, current temperature, current relative humidity, target relative humidity and air changes, and it computes the current and target humidity ratio, the humidity-ratio difference, dew-point temperature and moist-air density, and derives the hourly (kg/h) and daily (kg/day) dehumidification load, finally recommending a dehumidifier capacity (L/day). The calculation is based on the Magnus saturated water-vapor partial-pressure formula and standard atmospheric pressure (101.325 kPa); all operations run locally in the browser with no data uploaded.",
        "Humidity ratio d calculation",
        "Dew-point temperature calculation",
        "Moist-air density ρ calculation",
        "Hourly / daily dehumidification",
        "Dehumidifier capacity recommendation",
        "Saturated humidity-ratio reference table",
        "Relative-humidity band visualization",
        "Basement / warehouse / rainy-season presets",
        "Basement moisture-proofing selection",
        "Warehouse / archive humidity control",
        "Southern rainy-season dehumidification setup",
        "Home bedroom / living-room dehumidification",
        "Bathroom / pool-area dehumidification",
        "HVAC dehumidification load estimation",
        "📚 In-Depth Analysis: Estimating Dehumidification by Airflow and Humidity-Ratio Difference",
        "For underground garages, warehouses and pools, compute the dehumidification load from the ventilation rate and the humidity-ratio difference before and after treatment.",
        "When selecting a dehumidifier capacity, add a safety margin and verify the treated temperature and humidity.",
        "Compare the economics of rotary-wheel vs refrigerated dehumidification under different inlet conditions.",
        "Airflow 120 m³/h, inlet 26°C/80% RH",
        "Inlet humidity ratio d1≈18.5 g/kg, treated to 15°C/90% RH outlet d2≈9.5 g/kg; hourly dehumidification W = 120×1.2×(18.5−9.5)/1000 ≈ 1.30 kg/h, about 31 L/day.",
        "Capacity margin",
        "Daily load ×1.3 safety factor with a 6 L/day floor, to avoid under-capacity in humid weather.",
        "Where does the humidity-ratio difference come from?",
        "Obtain d (g/kg) from the inlet/outlet temperature and humidity via the psychrometric chart; the difference times airflow × air density gives the mass-flow dehumidification rate.",
        "Refrigerated or rotary-wheel?",
        "At normal temperature and high humidity, refrigerated dehumidification is economical; at low temperature/low humidity or for deep dehumidification use a rotary wheel, chosen by inlet condition.",
        "This tool computes at standard atmospheric pressure (101.325 kPa); at high altitude the air density and saturated vapor pressure differ slightly",
        "The result is a theoretical dehumidification-load estimate; actual selection must consider room air-tightness, occupancy, moisture sources, etc. comprehensively",
        "Target relative humidity is recommended between 45% and 60%; too low causes dry discomfort, too high fails to prevent mold",
        "Runs entirely in the browser; input data are never uploaded to a server, privacy secured",
        "e.g. area × floor height",
    ]))


if __name__ == '__main__':
    main()
