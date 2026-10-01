#!/usr/bin/env python3
# aerospace batch1 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'lift-coefficient': [
"✈️ Lift Coefficient Chart",
"Lift coefficient Cl versus angle of attack alpha for an airfoil, plotting stall behaviour with a thin-airfoil model, and computing lift.",
'📖 View the "Lift Coefficient Chart Guide"',
"Linear region CL = CLalpha · (alpha - alpha0), capped at CLmax; after alpha > alpha_stall a stall drop-off correction is applied",
"Lift coefficient grows linearly with angle of attack, the slope being the lift-curve slope CLalpha; beyond the maximum lift coefficient CLmax stall begins, and this tool applies a smooth drop-off after stall.",
"Airfoil type",
"NACA 0012 (symmetric)",
"NACA 2412 (positive camber)",
"NACA 4412 (high camber)",
"Flat plate",
"Zero-lift angle alpha0 (°)",
"Lift-curve slope (1/rad)",
"Stall angle of attack (°)",
"Maximum lift coefficient Clmax",
"Angle of attack to inspect (°)",
"Lift calculation (at the inspected angle of attack)",
"Flight speed V (m/s)",
"Plot curve",
"📖 Lift Coefficient Principles",
"Lift equation",
"Lift L",
": air density (1.225 kg/m³ at sea level)",
": flight speed (m/s)",
": wing reference area (m²)",
": lift coefficient, varying with angle of attack",
"Cl-alpha curve characteristics",
"Linear region",
": Cl = Clalpha × (alpha - alpha0), alpha in radians",
"Zero-lift angle alpha0",
": 0° for a symmetric airfoil, negative for a positively cambered one",
"Stall",
": Cl drops sharply beyond the stall angle of attack (flow separation)",
"Lift-curve slope",
": about 2pi/rad ≈ 0.11/° in thin-airfoil theory",
"Typical airfoil parameters",
"NACA 0012: alpha0=0°, Clmax≈1.3, stall≈15°",
"NACA 2412: alpha0=-2°, Clmax≈1.5, stall≈16°",
"NACA 4412: alpha0=-4°, Clmax≈1.6, stall≈14°",
"Flat plate: alpha0=0°, Clmax≈0.9, stall≈11°",
"📚 In-Depth Analysis: Lift Coefficient Chart",
"Airfoil aerodynamic assessment: plot the Cl-alpha curve from the zero-lift angle alpha0, lift-curve slope, stall angle of attack and Clmax.",
"When selecting, compare the lift characteristics of a symmetric airfoil (NACA 0012) with a positively cambered one (NACA 2412).",
"Given a target Cl (such as needed for takeoff), back-calculate the required angle of attack while avoiding the stall region.",
"Lift coefficient of NACA 2412 at a given angle of attack",
"NACA 2412 has a zero-lift angle alpha0≈-2° and a lift-curve slope of about 0.1/° (≈5.7 /rad). At alpha=4°, Cl≈0.1×(4-(-2))=0.6; near the stall angle (about 16°) Cl reaches Clmax≈1.5 and then drops sharply.",
"Does the lift coefficient keep rising with angle of attack?",
"No. After the linear region (about 10-16° depending on the airfoil) the flow separates and Cl drops sharply after peaking at Clmax, which is stall. In flight the angle of attack must stay below the stall angle.",
"Are the stall angle and Clmax fixed?",
"They vary with ",
", surface contamination (ice/bugs) and trailing-edge flap deflection. Icing greatly reduces Clmax and causes earlier stall, so speed is strictly limited in icing conditions. This tool computes from the airfoil parameters you give.",
'About "Lift Coefficient Chart"',
"Lift Coefficient Chart is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
"How to use the Lift Coefficient Chart",
"They vary with Reynolds number, surface contamination (ice/bugs) and trailing-edge flap deflection. Icing greatly reduces Clmax and causes earlier stall, so speed is strictly limited in icing conditions. This tool computes from the airfoil parameters you give.",
],
'fuel-consumption': [
"🔮 Fuel Consumption Estimator",
"Estimate sector fuel burn from the cruise fuel flow of the type and the flight distance/time, including taxi and reserve fuel.",
'📖 View the "Fuel Consumption Estimation Guide"',
"A320 (narrow-body)",
"B737-800 (narrow-body)",
"A330-300 (wide-body)",
"B777-300ER (wide-body)",
"A350-900 (wide-body)",
"B787-9 (wide-body)",
"A380 (very large)",
"Custom type",
"By flight distance",
"By flight time",
"Flight distance (km)",
"Cruise speed (km/h)",
"Flight time (hours)",
"Cruise fuel flow (kg/h)",
"Taxi fuel (kg)",
"Reserve fuel time (min)",
"Sector fuel factor (0.9-1.2)",
"Estimate fuel",
"📖 Fuel Calculation Notes",
"Fuel composition",
"Sector fuel",
"= cruise fuel flow × flight time × sector factor",
"Taxi fuel",
": ground taxi burn, usually 150-300 kg",
"Reserve fuel",
"= cruise fuel flow × (reserve time/60), by regulation no less than 30-45 minutes",
"Total fuel uplift",
"= taxi fuel + sector fuel + reserve fuel",
"Reference fuel flow by type (cruise)",
"A320 / B737-800: about 2400-2600 kg/h",
"A330-300: about 5800-6000 kg/h",
"B777-300ER: about 6800-7200 kg/h",
"A350-900: about 5800 kg/h",
"B787-9: about 5300 kg/h",
"A380: about 11000-12000 kg/h",
"Flight time t = distance / cruise speed; sector fuel = fuel flow × t × sector factor; reserve fuel = fuel flow × reserve minutes / 60; total fuel = taxi fuel + sector fuel + reserve fuel; volume = total fuel / 0.8 (kg/L)",
"Estimate sector fuel from the cruise fuel flow and flight time, then add taxi and reserve fuel for the block total; jet fuel density is about 0.8 kg/L, used for the volume conversion.",
"Note: actual fuel burn is affected by payload, en-route wind, cruise altitude and temperature; this tool is an estimation reference and must not be used directly for flight planning.",
"📚 In-Depth Analysis: Fuel Consumption Estimation",
"Estimate sector fuel burn from typical type-specific fuel flow and the flight distance/time.",
"Compare the fuel burn per unit of traffic between types (narrow-body/wide-body) for fleet selection or scheduling.",
"Given tank capacity and fuel flow, back-calculate the maximum range or diversion margin.",
"A320 sector fuel burn",
"The A320 cruises at about 2.5 t/h and about 830 km/h. For a flight distance of 1200 km: time≈1.45 h then fuel≈2.5×1.45≈3.6 t (excluding taxi/diversion/reserve fuel).",
"Why is the actual uplift much more than the estimate?",
"The estimate is only cruise fuel; in reality you also need takeoff/climb increment fuel, en-route diversion fuel, holding fuel, company reserve fuel and taxi fuel, which together are often 1.3-1.6 times the cruise value. This tool gives the sector base fuel burn.",
"Where does the type fuel flow come from?",
"From aircraft manufacturer performance manuals or airline operational data, varying significantly with payload, altitude, temperature and wind. This tool uses typical values for illustration; for precise loading rely on the flight planning system.",
'About "Fuel Consumption Estimator"',
"Fuel Consumption Estimator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
],
'flight-time': [
"✈️ Flight Time Calculator",
"Cross-time-zone flight time conversion: enter the departure and arrival local times to automatically compute the actual flight duration and the time difference.",
'📖 View the "Flight Time Calculation Guide"',
"Known departure + arrival to flight duration",
"Known departure + duration to arrival time",
"Departure airport time zone",
"Beijing/Shanghai (UTC+8)",
"Tokyo/Seoul (UTC+9)",
"Paris/Berlin (UTC+1)",
"New York (UTC-5)",
"Los Angeles (UTC-8)",
"Sydney (UTC+10)",
"Buenos Aires (UTC-3)",
"New Delhi (UTC+5:30)",
"Denver (UTC-7)",
"Arrival airport time zone",
"Departure local time",
"Arrival date",
"Arrival local time",
"Flight duration (hours)",
"Flight duration (minutes)",
"📖 Time Zones and Flight Time Notes",
"Convert departure and arrival times to a common UTC (Coordinated Universal Time) basis",
"Flight duration = arrival UTC time - departure UTC time",
"Time difference = arrival zone - departure zone (positive eastward, negative westward)",
"Date-line crossing: adjust the date when the time difference exceeds ±12 hours",
"Reference durations for common routes",
"Beijing to New York: about 13-15 hours (eastbound, time difference -13h)",
"Beijing to London: about 11-12 hours (time difference -8h)",
"Beijing to Tokyo: about 3-3.5 hours (time difference +1h)",
"Beijing to Sydney: about 11-12 hours (time difference +2h)",
"London to New York: about 7-8 hours (westbound, time difference -5h)",
"Actual flight duration = (arrival local time - departure local time) + (arrival zone - departure zone)",
"First convert each time to a common basis (UTC) by its own zone and then subtract, avoiding date and time-difference errors; the result is the actual airborne time, excluding ground time.",
"Note: standard time-zone offsets are used here, without daylight saving time (DST). During DST some zones shift by +1 hour.",
"📚 In-Depth Analysis: Flight Time Calculation",
"For cross-time-zone flights, compute the arrival local time from the departure/arrival airport time zones and the flight duration.",
"Given the departure local time and planned duration, back-calculate the arrival time for connection planning.",
"Check how the DST/standard-time difference affects the arrival time.",
"Flight duration estimate for Beijing to London",
"Departure from Beijing at 10:00 (UTC+8) = 02:00 UTC; flying 11 hours gives arrival at 13:00 UTC. London is UTC+0, so local arrival is 13:00. Ignoring the time difference would wrongly give the next day, so always convert to UTC first and then to local time.",
"Why use UTC as an intermediate step?",
"Computing directly across several time zones is error-prone. The correct method: convert the departure time to UTC, add the flight duration to get the arrival UTC, then convert to the arrival local zone. This tool follows that process to avoid off-by-a-day errors.",
"Does the flight duration include taxi time and the time difference?",
"Flight duration refers to airborne time (block time often includes taxi), not the time difference; the time difference is only a display conversion. The actual itinerary also adds check-in, immigration and ground transfer time.",
'About "Flight Time Calculator"',
"Flight Time Calculator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
],
'runway-length': [
"📏 Runway Length Calculator",
"Takeoff runway length correction: adjust the baseline length for airport elevation, air temperature and runway slope.",
'📖 View the "Runway Length Calculation Guide"',
"Baseline runway length for the type (m)",
"Airport elevation (m)",
"Airport temperature (°C)",
"Runway effective slope (%)",
"Headwind component (m/s)",
"Aircraft takeoff weight class",
"Light (smaller correction)",
"Heavy (larger correction)",
"Compute correction",
"📖 Runway Correction Notes",
"Correction method (ICAO empirical formula)",
"ISA standard temperature",
"= 15 - 0.0065 × elevation",
"Elevation correction",
": for every 300 m (1000 ft) above sea level, runway length increases by about 7%",
"Temperature correction",
": for every 1°C above ISA, runway length increases by about 1%",
"Slope correction",
": for every 1% upslope, runway length increases by about 10%",
"Headwind correction",
": for every 5 m/s (10 kt) of headwind, runway length decreases by about 7%",
"Runway length types",
" (TORA): runway length + clearway",
" (ASDA): runway length + stopway",
" (LDA): the length of runway available for landing",
"ISA temperature = 15 - 0.0065 × elevation (m); corrected length = baseline × weight factor × (1 + elevation/300 × 0.07) × (1 + max(0, dT) × 0.01) × (1 + slope × 0.10) × (1 - headwind/5 × 0.07); recommended length = corrected length × 1.15",
"Every 300 m of elevation adds 7%, every 1°C above ISA adds 1%, every 1% upslope adds 10%, and every 5 m/s of headwind shortens it by 7% (up to 30%); then add a 15% safety margin.",
"This tool uses empirical correction factors for teaching estimation only. Actual flight planning must use the aircraft flight manual (AFM) performance charts.",
"📚 In-Depth Analysis: Runway Length Calculation",
"Starting from the type baseline runway length, add elevation, temperature, slope and headwind corrections to get the actual required length.",
"Assess takeoff weight limits at high-elevation/high-temperature airports (reduce payload if the runway is too short).",
"Compare the extra length needed for a wet runway (lower friction).",
"High-elevation high-temperature runway correction illustration",
"For a type with a 2500 m baseline runway at sea-level ISA: at an airport elevation of 1500 m the density-altitude correction is about +12%, a temperature 10°C above standard adds +6%, and a 1% slope adds +3%, totalling 2500×1.21≈3025 m. In practice follow the type performance manual correction tables.",
"Why can a headwind shorten the runway?",
"A headwind improves the ground-roll efficiency of reaching lift-off airspeed, effectively shortening the ground roll needed; a tailwind does the opposite. Performance calculations treat the headwind component as a negative correction.",
"Why does a wet runway require more length?",
"On a slippery surface braking and acceleration performance degrade and the rejected-takeoff distance grows, requiring a longer runway or stricter weight limits. Regulations apply specific performance discounts for wet/contaminated runways.",
'About "Runway Length Calculator"',
"Runway Length Calculator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
],
'weight-balance': [
"🧮 Center of Gravity and Weight Calculator",
"Aircraft weight and balance: compute the center of gravity from the station loads and arms and check whether it is within the allowed range.",
'📖 View the "Center of Gravity and Weight Calculation Guide"',
"Basic empty weight (kg)",
"Empty-weight CG arm (m or in)",
"Forward CG limit (m)",
"Aft CG limit (m)",
"Station loads",
"The arm is the distance from the center of gravity of each load to the reference datum.",
"Compute CG",
"+ Add load item",
"📖 Center of Gravity and Balance Principles",
"= empty weight + the load weights summed",
"Total moment",
"= the sum of each weight × its arm",
"Center of gravity position (CG)",
"= total moment ÷ total weight",
"Balance condition",
": forward limit ≤ CG ≤ aft limit",
"Load references",
"Pilot/passenger: about 77 kg each (including baggage)",
"Fuel: jet fuel density about 0.8 kg/L",
"Cargo hold goods: by actual weighing",
"Arms must follow the loading diagram of each type (compartment positions differ)",
"CG = the weight-arm products summed / the weights summed; check cgFwd ≤ CG ≤ cgAft",
"The total moment is the sum of the weight of each item times its arm; dividing by the total weight gives the CG position, which must fall between the forward limit cgFwd and the aft limit cgAft, or the load cannot be released.",
"A CG forward of the limit makes rotation difficult and raises the stall speed; a CG aft of the limit causes longitudinal instability. This tool is a teaching estimate; actual flight must follow the type manual.",
"📚 In-Depth Analysis: Center of Gravity and Weight Calculation",
"From the basic empty weight and CG and the weight and arm of each load (passengers/fuel/cargo), compute the CG position of the whole aircraft.",
"Check whether the CG falls within the allowed envelope (forward limit to aft limit); otherwise the load must be rearranged.",
"Assess the forward/aft CG drift as fuel is burned.",
"Loading CG check",
"Basic empty weight 40000 kg at arm 12.0 m (moment 480000 kg·m); add cargo 5000 kg at arm 8 m (40000 kg·m). Total weight 45000 kg and total moment 520000 kg·m, so CG = 520000/45000 ≈ 11.56 m, which must lie between the forward limit (11.0) and the aft limit (12.5) to be valid.",
"What are the dangers of an out-of-limit CG?",
"A too-forward CG makes pitch control heavy and rotation on takeoff difficult; a too-aft CG causes longitudinal static instability, hard trim and even loss of control. The load sheet must therefore verify the CG envelope, and takeoff is not allowed if it is out of limits.",
"How does fuel burn change the CG?",
"It depends on tank location: burning the center tank moves the CG forward while burning the wing tanks moves it aft; the CG drifts within the envelope in flight, and the design envelope already allows margin. This tool computes the static loading CG.",
'About "Center of Gravity and Weight Calculator"',
"Center of Gravity and Weight Calculator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'lift-coefficient': {'雷诺数': 'Reynolds number'},
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
    out = {'slug': slug, 'industry': 'aerospace', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
