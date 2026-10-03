#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gas')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gas')
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
    out = {'slug': slug, 'industry': 'gas', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('load-1', build('load-1', [
        "🧮 Household Gas Load Calculation",
        "Enter the number and power of cookers and water heaters to compute the total heat load and design flow",
        "The professional calculation for \"enter the number and power of cookers and water heaters to compute the total heat load and design flow\" runs on the input parameters and outputs the result.",
        "📖 View the \"Household Gas Heat Load and Pipe Diameter User Guide\"",
        "Number of cookers (units)",
        "Power per cooker (kW)",
        "Number of water heaters (units)",
        "Power per water heater (kW)",
        "Simultaneity coefficient",
        "💡 The calorific value of natural gas is about 10 kWh/m³; design flow = heat load ÷ calorific value; the residential simultaneity coefficient is 0.7~0.8.",
        "The recommended pipe diameter is an estimate; actual hydraulic calculation must follow the code",
        "Gas appliances must meet national standards and be fitted with a flame-failure protection device",
        "📚 In-Depth Analysis: Household Gas Heat Load and Pipe Diameter",
        "Gas pipeline design matching residential cookers and water heaters",
        "Choice of simultaneity coefficient and verification of the design flow",
        "Recommended diameter of household branch pipes",
        "Total cooker power = number × power per unit, and likewise for water heaters; total rated = the sum of the two; design load = total rated × simultaneity coefficient (0.7~0.8 for residences); design flow = design load ÷ calorific value (natural gas ≈ 10 kWh/m³); look up DN15~DN40 from the flow.",
        "2 cookers × 3.5kW, 1 water heater × 20kW, coefficient 0.8: total rated 27.0kW, design load 21.6kW, flow 21.6÷10=2.16 m³/h, which lands on DN20 (<4 take DN20).",
        "What value should the simultaneity coefficient take?",
        "For residences it is generally 0.7~0.8, since many appliances never reach full load at the same time; public buildings take the simultaneous usage rate of the equipment, and using 1 would badly oversize the result.",
        "Should the calorific value be 10 or 36?",
        "The lower calorific value of natural gas is about 36 MJ/m³≈10 kWh/m³; the flow uses the kWh value (10) and divides directly to get m³/h; if MJ is used you must divide by 36 — do not mix the units.",
        "About Household Gas Load Calculation",
        "Household gas load calculation tool; enter the number and unit power of cookers and water heaters plus the simultaneity coefficient, compute the total heat load, design heat load and gas flow, and recommend a pipe diameter, assisting household gas system design.",
        "Aggregate load of cookers and water heaters",
        "Simultaneity coefficient correction",
        "Gas flow calculation",
        "Pipe diameter recommendation",
        "Household gas pipeline design",
        "Gas meter and pipe diameter selection",
        "Residential gas load verification",
        "Gas engineering quantity calculation",
        "Number of cookers",
        "Power per cooker",
        "Number of water heaters",
        "Power per water heater",
        "Simultaneity coefficient",
    ]))

    write('load-2', build('load-2', [
        "🧮 Heating Heat Load Calculation",
        "Enter the floor area and heating temperatures to compute the wall-hung boiler heat load and gas consumption",
        "Core formula (by input variable): A×idx×(dt÷dtStd)×(h÷3); gasFlow×24; Q÷1000",
        "Heating heat index (W/m²)",
        "Indoor design temperature (℃)",
        "Outdoor design temperature (℃)",
        "Floor height (m)",
        "💡 The heat index of an energy-efficient residence is about 50 W/m², and 60~80 W/m² for older buildings; select the wall-hung boiler at 1.2 times the heat load.",
        "The heat index relates to the insulation performance of the building and should be taken from actual values",
        "The wall-hung boiler should provide both space heating and domestic hot water",
        "📚 In-Depth Analysis: Heating Heat Load and Wall-Hung Boiler Selection",
        "Selection of gas wall-hung boilers for residential heating",
        "Estimating heating gas consumption from area and heat index",
        "Correction by indoor-outdoor temperature difference and floor height",
        "Heat load Q = area × heat index × (indoor-outdoor difference/20) × (floor height/3); boiler power = QkW×1.2; hourly gas consumption = QkW÷10; daily consumption = hourly×24; the heating season is estimated at 120 days. The heat index of an energy-efficient residence is about 50 W/m².",
        "Area 100m², heat index 50, indoor 20℃ / outdoor -5℃, floor height 3m: Q=100×50×(25/20)×1=6250W=6.25kW, boiler 7.5kW, gas consumption 0.625 m³/h, 15.0 m³ per day, about 1800 m³ for the heating season.",
        "Does a heat index of 50 apply to every residence?",
        "It applies only to newly built energy-efficient residences; take 60~80 W/m² for older buildings, and raise it further for single-storey or high window-to-wall ratios, otherwise the heating will be insufficient.",
        "Why is the heating season taken as 120 days?",
        "The central heating season in northern China is on the order of 120 days; correct it with the local heating days and load curve — it is only for energy estimation.",
        "About Heating Heat Load Calculation",
        "Heating heat load calculation tool; enter the floor area, heating heat index, indoor and outdoor design temperatures and floor height, compute the heat load, wall-hung boiler power, and hourly, daily and heating-season gas consumption, assisting boiler selection and energy estimation.",
        "Correction by temperature difference and floor height",
        "Wall-hung boiler power selection",
        "Gas consumption estimation",
        "Heating season energy accounting",
        "Wall-hung boiler selection",
        "Residential heating energy estimation",
        "Gas heating load accounting",
        "Energy-saving retrofit effect assessment",
        "Heating heat index",
        "Indoor design temperature",
        "Outdoor design temperature",
    ]))

    write('pressure-6', build('pressure-6', [
        "🚀 Regulator Selection Calculation",
        "Enter the inlet and outlet pressures, flow and outlet pressure to compute the regulator size",
        "Core formula (by input variable): Q÷√(dP÷SG); rho÷1.29; Cv×1.3",
        "Inlet pressure (kPa)",
        "Outlet pressure (kPa)",
        "💡 Simplified gas Cv: Cv = Q/√(ΔP/SG); take 1.3× margin for selection; a pressure ratio ≤0.528 means critical flow.",
        "The Cv formula is a simplified estimate; formal selection should follow the manufacturer data and the standards",
        "The regulator should be fitted with a safety shut-off and a relief device",
        "📚 In-Depth Analysis: Regulator Pressure Differential and Cv Selection",
        "Gas regulating station / box-type regulator size selection",
        "Determination of Cv from the inlet and outlet pressures and flow",
        "Critical / subcritical flow check",
        "Pressure differential ΔP = inlet - outlet; relative density SG = density÷1.29; Cv = flow÷√(ΔP/SG); the selection Cv is 1.3 times the calculated value; a pressure ratio P2/P1 ≤0.528 is critical flow and must be checked with the gas expansion formula. Look up DN15~DN80 from the selection Cv.",
        "P1=300kPa, P2=3kPa, flow 100 m³/h, ρ=0.7: ΔP=297kPa, SG=0.543, Cv=100/√(297/0.543)=4.27, selection Cv=5.56; the pressure ratio 0.01≤0.528 is critical flow, and the table lands on a DN25 regulator.",
        "Why is the selection Cv multiplied by 1.3?",
        "To leave margin for flow fluctuation and valve trim wear, avoiding long-term operation at full opening that would make control unstable and shorten service life.",
        "What does critical flow mean?",
        "When the pressure ratio is very low the downstream velocity reaches the speed of sound, the simple Cv formula fails, and the actual flow capacity must be checked with a gas expansion formula such as Fliegner's.",
        "About Regulator Selection Calculation",
        "Regulator selection calculation tool; enter the inlet and outlet pressures, flow and gas density, compute the pressure differential, flow coefficient Cv and selection Cv, and recommend a regulator size, assisting gas regulator selection design.",
        "Pressure differential and relative density calculation",
        "Flow coefficient Cv calculation",
        "Selection margin and size recommendation",
        "Flow state judgement",
        "Gas regulator selection",
        "Regulating station design",
        "Regulator capacity check",
        "Gas transmission and distribution system design",
        "Inlet pressure",
        "Outlet pressure",
        "Gas density",
    ]))

    write('pressure-7', build('pressure-7', [
        "🎚️ Pipeline Pressure Drop Calculation",
        "Enter the pipe diameter, flow and pipe length to compute the friction and local pressure drops",
        "Core formula (by input variable): dpTotal÷101325×100; 0.11×(term)^0.25; k÷1000÷Dm+68÷Re",
        "📖 View the \"Gas Pipeline Hydraulic Pressure Drop User Guide\"",
        "Absolute roughness (mm)",
        "Sum of local resistance coefficients",
        "💡 Darcy formula ΔP=λ·(L/D)·(ρv²/2); use the Haaland formula for λ; the total pressure drop of a low-pressure pipe should be <5%.",
        "The kinematic viscosity of gas is approximated as 1.5×10⁻⁵ m²/s",
        "High-pressure pipelines must account for gas compressibility",
        "📚 In-Depth Analysis: Gas Pipeline Hydraulic Pressure Drop",
        "Hydraulic calculation and diameter verification of medium- and low-pressure gas networks",
        "Flow velocity",
        "and friction and local resistance assessment",
        "Whether the pressure drop share meets the terminal pressure requirement",
        "Velocity v = flow÷3600÷cross-section; Reynolds number Re = v·D/ν (ν≈1.5e-5); laminar λ=64/Re, turbulent λ=0.11·(k/(1000D)+68/Re)^0.25; friction drop = λ·(L/D)·(ρv²/2), local drop = Σk·(ρv²/2), total drop = the sum of the two.",
        "D=100mm, Q=100m³/h, L=200m, roughness 0.02, Σk=5, ρ=0.7: v=3.54m/s, Re=23579 (turbulent), λ=0.026, friction drop 0.227kPa, local 0.022kPa, total 0.249kPa, only 0.25% of atmospheric pressure — the drop is very small.",
        "What share of atmospheric pressure is a normal pressure drop?",
        "The terminal drop of a medium-pressure network is generally required to be <3%~5%; this example at 0.25% has plenty of margin; if it exceeds 5% the diameter must be enlarged or the pressure losses reduced.",
        "How is local resistance estimated?",
        "Accumulate the equivalent local resistance coefficients Σk for elbows, valves and tees; the equivalent length method is more accurate for complex networks.",
        "About Pipeline Pressure Drop Calculation",
        "Pipeline pressure drop calculation tool; enter the pipe inner diameter, flow, length, roughness, local resistance coefficients and gas density, compute the velocity, Reynolds number, friction factor, friction drop, local drop and total drop, assisting gas pipeline hydraulic calculation.",
        "Friction factor Haaland formula",
        "Splitting friction and local pressure drops",
        "Pressure drop grade assessment",
        "Gas pipeline hydraulic calculation",
        "Diameter verification and optimisation",
        "Inlet and outlet pressure check of the regulating station",
        "Gas network design",
        "Pipe inner diameter",
        "Pipe length",
        "Absolute roughness",
        "Sum of local resistance coefficients",
        "Gas density",
    ]))

    write('index', build('index', [
        "🔥 Gas Engineering Tools",
        "Gas Engineering",
        "Gas Engineering Tools",
        "Enter the number of cookers and water heaters, the power per unit and the simultaneity coefficient to compute the total household heat load and design flow and recommend a pipe diameter, for matching design of residential gas piping and appliances.",
        "Enter the inlet and outlet pressures of the regulator, the flow and the gas density to compute the pressure differential and flow coefficient Cv and recommend a regulator model, for selection design of gas regulating stations and regulating equipment.",
        "Enter the gas consumption of each time period (at least 2 values) to compute the monthly or daily non-uniformity coefficient (hourly, daily, monthly peak-to-valley ratio) and estimate the peak-shaving demand, for gas storage, distribution and dispatch planning.",
        "Enter the crossing distance, pipe diameter, entry and exit angles and burial depth of the directional drilling to compute the entry and exit section lengths, total construction length and reaming diameter, assess the crossing difficulty and assist the trenchless pipeline crossing design.",
        "Select the liquefied gas type (LPG/LNG/liquid ammonia/liquid chlorine), enter the mass and vaporisation time to compute the vaporisation heat coefficient, total vaporisation heat, average heating power and post-vaporisation volume, assisting vaporiser selection and energy accounting.",
        "Enter the pipe material, soil resistivity, protection area and measured potential to compute the current density and total protection current required by cathodic protection, judge the protection state and recommend an anode scheme, assisting buried pipeline anti-corrosion design.",
        "Enter the floor area, heating heat index, indoor and outdoor design temperatures and floor height to compute the heating heat load, wall-hung boiler power and hourly and heating-season gas consumption, assisting boiler selection and operating energy estimation.",
        "Gas odorant concentration calculation",
        "Enter the gas flow and the target odorant concentration to compute the dosing rate and operating consumption of odorants such as tetrahydrothiophene (THT), and recommend an odorant pump range, for gas odorisation process design.",
        "Select the orifice plate or turbine metering method, enter parameters such as bore diameter / pressure differential or instrument factor / frequency, to compute the volumetric flow, mass flow and velocity of the gas, for gas metering device design and verification.",
        "Enter the pipe inner diameter, flow, length, roughness and local resistance coefficients to compute the velocity, Reynolds number, friction and local pressure drops and the total pressure drop, for gas pipeline hydraulic calculation and diameter verification.",
        "Select the gas type (natural gas/LPG/manufactured gas/hydrogen) and enter the leak volume concentration, then check against the explosion limits to judge the explosion risk level (safe/dangerous), for leak emergency response assessment.",
        "About \"Gas Engineering Tools\"",
        "The Gas Engineering Tools collection gathers 11 free online tools covering the common calculation, conversion and lookup needs of gas engineering scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run purely on the front end, data is not uploaded to a server, and your privacy and security are protected.",
        "The gas engineering tools collected on this page include (representative tools):",
        "These tools help you quickly finish common gas engineering tasks without memorising complex formulas or doing manual conversions — just enter the values and get the result.",
        "Do the Gas Engineering Tools require a download or registration?",
        "No. All gas engineering tools on this page are purely front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the calculation results of the Gas Engineering Tools accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available immediately. All operations run locally on your device, data is never uploaded to a server, and your privacy and security are guaranteed.",
    ]))

    write('yongqibujunyunxishujisuan', build('yongqibujunyunxishujisuan', [
        "🧮 Gas Consumption Non-Uniformity Coefficient Calculation",
        "Enter the gas consumption of each time period to compute the non-uniformity coefficient and peak-shaving demand",
        "Gas consumption of each time period (comma separated)",
        "Time period type",
        "Monthly non-uniformity coefficient",
        "Daily non-uniformity coefficient",
        "Hourly non-uniformity coefficient",
        "💡 Non-uniformity coefficient = consumption of each period ÷ average consumption; Kmax reflects the peak-shaving pressure, so gas storage or source regulation is required.",
        "Data may be separated by commas, spaces or newlines",
        "Peak shaving methods include gas holders, underground storage and gas source dispatch",
        "📚 In-Depth Analysis: Gas Consumption Non-Uniformity Coefficient and Peak Shaving",
        "Planning of city gas storage and distribution stations and peak-shaving facilities",
        "Monthly/daily/hourly consumption fluctuation analysis",
        "Gas holder capacity and gas source dispatch",
        "Enter the gas consumption of each period (≥ 2 values): average = total ÷ count; peak factor Kmax = peak ÷ average, valley factor Kmin = valley ÷ average, peak-shaving demand = peak - average. Kmax<1.2 is very uniform, <1.5 fairly uniform, <2.0 fluctuates considerably, otherwise it is severe.",
        "Monthly consumption 120/150/90/180/110/200 (in 10k m³): average 141.7, peak 200, valley 90, Kmax=1.41, Kmin=0.64, peak-shaving demand 58.3 — fairly uniform (Kmax<1.5); the gas holder should be sized from the peak-shaving volume plus a safety margin.",
        "What is the non-uniformity coefficient used for?",
        "It directly determines the scale of storage facilities and the flexibility of gas source dispatch: the larger Kmax, the stronger the required peak-shaving capability, making it a core input for storage and distribution station design.",
        "Is the hourly coefficient usually larger than the monthly coefficient?",
        "Yes. Morning and evening peaks within a day make the hourly non-uniformity coefficient clearly larger than the monthly one, so dispatch should be checked against the worst-case period (hourly).",
        "About Gas Consumption Non-Uniformity Coefficient Calculation",
        "Gas consumption non-uniformity coefficient calculation tool; enter the gas consumption of each period (monthly/daily/hourly), compute the average consumption, peak and valley values, peak and valley non-uniformity coefficients and peak-shaving demand, and visualise the fluctuation as a bar chart, assisting gas peak-shaving design.",
        "Monthly/daily/hourly non-uniformity coefficients",
        "Peak, valley and peak-shaving demand",
        "Fluctuation grade assessment",
        "Bar chart visualisation",
        "Gas peak-shaving and storage design",
        "Gas load analysis",
        "Gas source dispatch planning",
        "Gas network operation optimisation",
        "Gas consumption of each time period (comma separated)",
    ]))


if __name__ == '__main__':
    main()