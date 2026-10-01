#!/usr/bin/env python3
# aerospace batch2 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'assessor-capacity': [
"🧊 Terminal Capacity and Security Check Assessment",
"Enter the terminal area, number of security lanes and other parameters to assess passenger handling capacity and security throughput.",
'📖 View the "Terminal Capacity and Security Check Assessment Guide"',
"Terminal capacity assessment uses the bottleneck-resource method: compute the upper processing capacity of each stage (security lanes, check-in counters, boarding gates) as single-resource rate × number of resources, take the minimum across stages as the theoretical peak-hour passenger ceiling, and allow for queuing buffer and staff proficiency factors. All calculations run locally in the browser and no data is uploaded.",
"Total terminal area (m²)",
"Number of security lanes",
"Number of check-in counters",
"Number of boarding gates",
"Peak-hour passengers",
"Assess capacity",
"📚 In-Depth Analysis: Terminal Capacity and Security Check Assessment",
"When building or expanding a terminal, estimate the peak-hour passenger ceiling from the total area, security lanes, check-in counters and boarding gates.",
"Identify the bottleneck resource (such as insufficient security lanes) to guide opening more lanes or adjusting rosters.",
"Given the peak-hour passenger count, back-calculate the required security/check-in resources for staffing and equipment budgets.",
"Capacity estimate for a medium terminal",
"Total area 40000 m², 12 security lanes, 40 check-in counters, 25 boarding gates and 6000 peak passengers/hour. If one lane handles 150 people/hour, the security ceiling is 12×150=1800 people/hour, well below the passenger volume, so security is the bottleneck and more lanes or staggered peaks are needed.",
"What is the difference between capacity and throughput?",
"Capacity is the theoretical ceiling (resources × per-resource handling rate), while throughput is the actual passing volume, usually below capacity because of process, staff proficiency and passenger behaviour. Assess with the minimum over bottleneck resources and leave a margin.",
"Why does the computed figure always seem insufficient?",
"Often because only the hardware (number of counters) was counted without the per-point processing time, or because the serial waiting of check-in, security and boarding was not considered. Compute the ceiling of each stage, take the minimum and add a queuing buffer.",
"Terminal capacity assessment references MH/T 5018, Code for Design of Civil Airport Terminals",
"Area standard 15 m² per person, security lane 180 people/hour, check-in counter 60 people/hour",
"The capacity bottleneck is the smallest throughput among the stages",
"Start process optimisation above 80% utilisation and consider expansion above 95%",
"Peak-hour passengers are usually 8-12% of the daily passenger volume",
'About "Terminal Capacity and Security Check Assessment"',
"A terminal capacity assessment tool: enter the area, security lanes, check-in counters and other parameters to compute the throughput of each stage and identify the bottleneck.",
"Four-stage capacity calculation",
"Bottleneck identification",
"Utilisation analysis",
"Load-level assessment",
"Airport capacity planning",
"Terminal operational assessment",
"Security lane configuration",
"Airport expansion justification",
],
'stats-weight-luggage': [
"⚖️ Baggage (Loading/Weight) Statistics",
"Loading/Weight",
'📖 View the "Baggage (Loading/Weight) Statistics Guide"',
"Enter the weight of each piece of baggage to automatically sum the total and average weight, check against the free checked allowance and free piece count to judge overweight/over-count, and estimate the excess charge from the excess rate; data is processed only locally in the browser and is not uploaded.",
"Total weight = sum of the piece weights · Overweight = Σ max(0, piece weight - free allowance/piece) · Overweight fee = overweight × excess rate",
"Baggage piece weights (kg, separated by commas or newlines, one value per piece)",
"Free checked allowance (kg/piece)",
"Free piece count (pieces)",
"Excess rate (CNY/kg)",
"Summarise baggage weight",
"📚 In-Depth Analysis: Baggage (Loading/Weight) Statistics",
"Enter a batch of baggage/cargo weights to compute the mean, extremes and distribution, supporting loading and CG estimation.",
"Compare baggage means between sectors to forecast the CG drift trend.",
"Identify abnormally overweight pieces and arrange dispersal in advance.",
"Baggage weight distribution",
"Enter 12 baggage weights (kg): 15,18,12,20,16,14,22,19,17,13,21,16. Mean ≈ 17.1 kg, maximum 22, minimum 12. Use this to estimate the total hold weight and an initial CG, and place overweight pieces in a dispersed, symmetric arrangement.",
"How does baggage weight statistics relate to CG calculation?",
"The weight of each piece × its arm = moment; dividing the sum by the total weight gives the actual CG. This tool does the weight statistics; the CG position needs the arm of each compartment (see the ",
"Center of Gravity and Weight",
" tool) to be located.",
"Is a small sample meaningful for statistics?",
"With few samples you can only read the mean/extremes, not infer the distribution. Accumulate enough samples from the same compartment and route before assessing typical values and dispersion.",
'About "Baggage (Loading/Weight) Statistics"',
"Baggage (Loading/Weight) Statistics. A free online tool that runs fully in the front end, does not upload data and protects your privacy.",
"For example: 18,22,27,19",
],
'length-temp-runway': [
"📏 Required Runway Length (Elevation/Temperature Correction)",
"Enter two parameters to automatically compute the common result.",
'📖 View the "Required Runway Length (Elevation/Temperature Correction) Guide"',
"Corrected length = baseline length × (1 + 10% · elevation/1000) × (1 + 1% · temperature difference from ISA)",
"Baseline runway length L0 (m)",
"Elevation h (m)",
"Actual temperature T (°C)",
"💡 The higher the elevation, the thinner the air, and the higher the temperature, the lower the engine thrust, so the required takeoff/landing length is greater.",
"📚 In-Depth Analysis: Required Runway Length (Elevation/Temperature Correction)",
"For high-elevation/high-temperature airports, start from the baseline ",
"runway length",
" and superimpose the elevation density-altitude correction and the temperature correction to get the actual required length.",
"Assess whether the takeoff weight must be reduced in extreme heat or at high elevation (runway too short).",
"Compare the baseline lengths and corrections of different types for airport suitability.",
"High-elevation airport length correction illustration",
"Baseline runway length 2500 m; at an elevation of 1000 m the density-altitude correction is about +8%, and a temperature 15°C above ISA adds about +5%, totalling about 2500×1.13≈2825 m. In practice follow the correction tables in the type performance manual.",
"Why do high-temperature high-elevation runways need to be longer?",
"High elevation and high temperature mean lower air density, so at the same indicated airspeed the dynamic pressure is lower and both lift and engine thrust drop, requiring a longer roll to reach lift-off speed, hence a longer runway or a reduced takeoff weight.",
"How do slope and headwind affect it?",
"An upslope increases and a downslope decreases the required length; a headwind shortens and a tailwind lengthens it. A full performance calculation superimposes all these corrections; this tool illustrates with the given elevation/temperature terms.",
'About "Required Runway Length (Elevation/Temperature Correction)"',
"Required Runway Length (Elevation/Temperature Correction). A free online tool that runs fully in the front end, does not upload data and protects your privacy.",
"Baseline runway length L0 (m)",
"Elevation h (m)",
"Actual temperature T (°C)",
],
'huoyun-uld-jizhuangqi-guige': [
"🚚 Cargo (ULD/Unit Load Device) Specifications",
"Enter two parameters to automatically compute the common result.",
'📖 View the "Cargo (ULD/Unit Load Device) Specifications Guide"',
"Weight load factor = cargo weight ÷ maximum gross weight; volume load factor = cargo volume ÷ usable volume",
"Maximum gross weight (kg)",
"Cargo weight (kg)",
"Usable volume (m³)",
"Cargo volume (m³)",
"💡 Loading a ULD requires satisfying both the weight and volume limits; exceeding either makes it unfit for loading.",
"📚 In-Depth Analysis: Cargo (ULD/Unit Load Device) Specifications",
"During air cargo loading, look up the external dimensions, internal volume and maximum gross weight of a ULD to match the cargo.",
"Compare the aircraft compatibility of different ULD types (containers/pallets/PAG/PMC/AKE).",
"From the cargo volume and weight, back-calculate the number of ULDs needed and the CG distribution.",
"AKE container suitability",
"The AKE (an air container for narrow-body/wide-body lower holds) has a typical internal volume of about 4.3 m³ and a maximum gross weight of about 1588 kg (PAG pallets are higher). When loading, check the aircraft door dimensions and floor load limits to avoid loading that fits but leaves the CG unclear.",
"Are ULD and unit load device the same?",
"ULD (Unit Load Device) is the general term, covering containers (such as AKE) and pallets (such as PMC/PAG, with a net over the pallet to secure loose cargo). Choose by the aircraft position (container position or pallet position) and size limits.",
"What happens if the maximum gross weight is exceeded?",
"Exceeding the ULD rated gross weight or the aircraft floor load/hold door limits may cause structural damage or make loading impossible. Loading must check weight, size and CG together, with the air waybill and load sheet as the authority.",
'About "Cargo (ULD/Unit Load Device) Specifications"',
"Cargo (ULD/Unit Load Device) Specifications. A free online tool that runs fully in the front end, does not upload data and protects your privacy.",
"Maximum gross weight (kg)",
"Cargo weight (kg)",
"Usable volume (m³)",
"Cargo volume (m³)",
],
'rocket-delta-v': [
"Δv from Specific Impulse Equivalent Velocity and Mass Ratio",
"Enter the effective exhaust velocity v_e, initial mass m0 and final mass mf to find the velocity increment.",
"Rocket Delta-v Calculator",
"/ Rocket Delta-v Calculator",
'📖 View the "Delta-v from Specific Impulse Equivalent Velocity and Mass Ratio Guide"',
"Exhaust velocity v_e (m/s)",
"The Tsiolkovsky rocket equation.",
"📚 In-Depth Analysis: Delta-v from Specific Impulse Equivalent Velocity and Mass Ratio",
"Rocket velocity increment Δv = v_e·ln(m0/mf), where v_e is the exhaust velocity.",
"From the ",
"specific impulse Isp",
" and the mass ratio, assess the manoeuvring capability of an upper stage or attitude control segment.",
"Compare the Δv efficiency at different exhaust velocities (electric/chemical propulsion).",
"Upper-stage velocity increment",
"Exhaust velocity v_e=2500 m/s, initial mass m0=100 t and final mass mf=20 t. Δv=2500×ln(100/20)=2500×ln(5)=2500×1.609≈4023 m/s ≈ 4.02 km/s. Enough to complete most orbital transfer segments.",
"How does this formula relate to the ",
"?",
"They are the same thing: Δv=Isp·g0·ln(m0/mf), and the exhaust velocity v_e=Isp·g0, so Δv=v_e·ln(m0/mf). One is expressed with specific impulse and the other with exhaust velocity, but they are identical in essence.",
"Electric propulsion has a high exhaust velocity but low thrust; how to choose?",
"Electric propulsion can reach v_e of several km/s or more (very high Δv efficiency), but its thrust is on the milli-newton level, so it suits only long-term on-orbit manoeuvres; high-thrust chemical propulsion is used for orbit insertion/changes. Choose by the mission time scale.",
"How to use Delta-v from Specific Impulse Equivalent Velocity and Mass Ratio",
"How does this formula relate to the Tsiolkovsky rocket equation?",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'rocket-delta-v': {'齐奥尔科夫斯基公式': 'Tsiolkovsky rocket equation'},
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
