#!/usr/bin/env python3
# fire-rescue batch8 (5 tools, 最终批)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fire-rescue')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fire-rescue')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'calc-1': [
"🔥 Fire Nozzle Effective Jet Stream Calculation",
"Computed per GB 50974 Technical Code for Fire Protection Water Supply and Hydrant Systems: first convert the nozzle pressure to a pressure head Hq, then obtain the effective jet stream as Sk = Hq/(1+φ·Hq), where φ depends on the nozzle bore (13mm→0.0165, 16mm→0.0124, 19mm→0.0097, 22mm→0.0077); the outlet velocity is v=√(2gHq).",
"/ Fire Nozzle Effective Jet Stream Calculation",
"Estimate the effective jet stream length, horizontal effective reach and nozzle outlet velocity from the nozzle pressure, reduction coefficient and jet elevation angle.",
"Nozzle pressure (MPa)",
"Nozzle bore (mm)",
"Jet reduction coefficient",
"Jet elevation angle (°)",
"Bore comparison (nozzle pressure 0.30 MPa):",
"13mm → effective stream about 18.6m; 16mm → about 19.8m; 19mm → about 20.9m; 22mm → about 21.6m (all at a reduction coefficient of 0.9).",
"This tool does not account for hose friction loss, so the pressure actually reaching the nozzle is lower than the pump outlet pressure; in operations, combine equipment performance with on-scene experience.",
"📚 In-Depth Analysis: Fire Nozzle Effective Jet Stream Calculation",
"Before dispatch, estimate the building height and horizontal depth a 19mm nozzle can cover at the rated pressure of the truck-mounted pump, to decide whether a larger-bore nozzle or higher pump pressure is needed.",
"During fire design review, check whether the indoor hydrant effective jet stream meets GB 50974: ≥13m for high-rise buildings, factories and warehouses, and ≥10m for other buildings.",
"On the training ground, demonstrate to new members the ",
"square root",
" relationship behind doubling the pressure without doubling the reach, so they understand the diminishing marginal return of extra pressure on reach.",
"Reach check for a 19mm nozzle at 0.30 MPa",
"With default parameters (nozzle pressure 0.30 MPa, 19mm nozzle, jet reduction coefficient 0.9, elevation 45°): pressure head Hq = 30 m, with φ=0.0097, effective stream = 30/(1+0.0097×30) × 0.9 = 20.9 m; horizontal effective reach = 20.9 × cos45° = 14.8 m; nozzle outlet velocity = √(2×9.81×30) = 24.3 m/s. The 20.9 m effective stream meets the ≥13m requirement for high-rise buildings; switching to a 13mm nozzle reduces it to about 18.6 m.",
"What is the difference between the effective jet stream and the effective reach?",
"The effective jet stream is the length of the compact part of the jet (carrying about 90% of the water), the part that truly suppresses fire; the effective reach is its horizontal projection. Since firefighting depends on whether the effective stream can reach the fire, the code assesses the effective stream rather than the reach.",
"Why does doubling the pressure not double the reach?",
"Outlet velocity is proportional to the square root of pressure (v∝√P), and the effective jet stream is further damped by the 1/(1+φ·Hq) term, so extra pressure yields diminishing marginal returns. A more effective approach is usually to shorten the hose to reduce friction loss, or to use a smaller-bore nozzle to raise the actual pressure at the nozzle.",
],
'calc-2': [
"⚖️ Fire Load Calculation",
"This calculator uses standard math and unit conventions; inputs are parsed numerically and results output in real time; fully client-side, no upload. Tool: Fire Load Calculation - Fire and Rescue Online Tool.",
"/ Fire Load Calculation",
"Compute the fire load density and assess the fire severity level from the combustible mass, calorific value and room area.",
"Total combustible mass (kg)",
"Calorific value (MJ/kg)",
"Fire load density grading reference: low ≤ 300 MJ/m², medium 300~1200 MJ/m², high > 1200 MJ/m². Results are for reference only.",
"📚 In-Depth Analysis: Fire Load Calculation",
"In performance-based fire design, input the ",
"fire load density",
" as a boundary condition for design fire curves, flashover time and structural fire-resistance analysis.",
"Before changing the stored goods category in a warehouse, recheck whether the load density exceeds the original design allowance based on the new material mass and calorific value.",
"In fire investigation, estimate the total heat release from the burned area and residual combustibles to help judge the burning duration and whether flashover occurred.",
"Load check for 500 kg of combustibles in a 100 m² room",
"With default parameters (500 kg combustibles, average calorific value 20 MJ/kg, room 100 m²): total heat = 500 × 20 = 10000 MJ; fire load density = 10000/100 = 100 MJ/m²; converted at a wood calorific value of 18 MJ/kg, the equivalent wood load = 100/18 ≈ 5.6 kg/m², rated as a low load level. For comparison, ordinary offices are often 300~500 MJ/m², and book stacks and warehouses can exceed 1000 MJ/m².",
"How high a fire load density is dangerous?",
"Residences at about 400~600 MJ/m² and offices at about 300~500 MJ/m² are common; above about 800 MJ/m², the firefighting intensity and structural protection usually need to be considered at the high-hazard level. However, the hazard also depends on fuel distribution, ventilation and suppression systems, so density is only one input.",
"How should the calorific value be taken for mixed occupancies?",
"Use the mass-weighted average of each combustible type rather than simply applying the wood value. Common values: wood 18 MJ/kg, paper 16, polyethylene 44, gasoline 44; a high share of plastics and oils markedly raises the total heat.",
],
'calc-3': [
"🔥 Evacuation Time Calculation",
"This tool performs unit and format conversion; conversion factors follow the International System of Units (SI) and related standards, and results keep the input precision; fully client-side. Tool: Evacuation Time Calculation - Fire and Rescue Online Tool.",
"/ Evacuation Time Calculation",
"Using a crowd-flow model, estimate the walking time and passage time from the occupant count, exit width, specific flow, walking speed and travel distance.",
"Number of occupants",
"Effective exit width (m)",
"Specific flow (persons/(m·s))",
"Walking speed (m/s)",
"Travel distance (m)",
"Pre-movement time (s, optional)",
"Specific flow reference: ordinary exit doors 1.3~1.5 persons/(m·s); stairs 0.9~1.1 persons/(m·s). Pre-movement time covers detection, alarm and occupant response.",
"📚 In-Depth Analysis: Evacuation Time Calculation",
"During mall opening hours, verify the safe evacuation time using the occupant count of the worst-off floor to see whether the exit width becomes a bottleneck.",
"After a cinema, theater or stadium egress drill, back-calculate the passage time from the measured occupants and exit width to evaluate evacuation management efficiency.",
"Before changing the use of an existing building (such as office to training), quickly screen whether the original egress width can handle the new occupant load.",
"RSET check for 200 occupants evacuating through a 1.4m-wide exit",
"With default parameters (200 occupants, effective exit width 1.4 m, specific flow 1.3 persons/(m·s), travel distance 50 m, speed 1.2 m/s, pre-movement 60 s): walking time = 50/1.2 = 41.7 s; exit passage time = 200/(1.4×1.3) = 109.9 s; this tool conservatively sums the two, giving a movement time of 151.6 s and RSET = 151.6 + 60 = 211.6 s (about 3.5 min). Under a continuous-flow model taking the larger of the two, the movement time would be 109.9 s and RSET 169.9 s.",
"Why are walking time and exit passage time combined?",
"Walking time is how long an individual takes to reach the exit from the farthest point, while exit passage time is how long the whole crowd takes to pass through the exit. This tool sums them conservatively; under a continuous-flow model (the crowd passes through as it arrives) taking the larger value, the result is smaller. For formal assessments, report both and state the basis.",
"How should pre-movement time be set?",
"It depends on the alarm type and occupant state: about 30~60 s in a familiar building with voice notification; often 120 s or more for unfamiliar occupants or sleeping occupancies at night; increase it further for places with the elderly, children or people with disabilities. It is the most uncertain term in RSET, so a separate sensitivity analysis is advisable.",
"Detection + reaction time",
],
'calc-4': [
"🔥 Fire Extinguisher Configuration Calculation (Emergency Rescue)",
"This calculator uses standard math and unit conventions; inputs are parsed numerically and results output in real time; fully client-side, no upload. Tool: Fire Extinguisher Configuration Calculation (Emergency Rescue).",
"Estimate the number of fire extinguishers required from the protection area, fire class and hazard level using common design parameters.",
"Fire class",
"Class A (solid combustibles)",
"Class B (liquids / meltable solids)",
"Class C (gases / energized electrical equipment)",
"Reference values are based on common design practice: for Class A, light/ordinary/high hazard use 100/75/50 m² per extinguisher; for Class B, 1.5/1.0/0.5 m² per extinguisher. Each setting point should have no fewer than 2 extinguishers.",
"📚 In-Depth Analysis: Fire Extinguisher Configuration Calculation (Emergency Rescue)",
"For a new workshop, estimate the required extinguishing rating and number of units per GB 50140 as the basis for the purchase and layout list.",
"After a premises changes fire hazard level (such as office to storage), recheck whether the existing configuration still complies.",
"During a fire safety inspection, quickly verify from the actual protection area whether the number of units and setting points meets the minimum requirements.",
"Configuration check for a 300 m² Class A light-hazard premises",
"With default parameters (Class A fire, light hazard, protection area 300 m²): the light-hazard coverage per extinguisher is taken as 100 m², so 300/100 = 3 and about 3 units are estimated; laid out at 2 units per setting point, about 2 setting points are needed. Note that each setting point should have no fewer than 2 and no more than 5 units, and the spacing should keep the walking distance from any point to the nearest setting point within the protection radius.",
"Why at least 2 units, and why spread over 2 points?",
"GB 50140 requires no fewer than 2 units per setting point so that a backup remains if one fails, loses pressure or is cut off by fire; spreading them out ensures usable equipment near the fire origin and avoids long retrieval distances.",
"How are hazard levels classified?",
"They are divided into light, ordinary and high hazard by the amount of combustibles, fire spread rate and difficulty of suppression. Different areas of the same building may be graded separately (for example ordinary hazard for offices, high hazard for storage), and each should be calculated at its own worst case and then summed.",
],
'detector-20': [
"🔥 Fire Facility Compliance Self-Check",
"Run an item-by-item self-check across three modules: facility configuration / maintenance / inspection and acceptance, automatically computing the pass rate of each module and the overall compliance rate, and outputting a hidden-hazard rectification list.",
"Fire Facility (Equipment / Maintenance / Inspection) Standard",
"/ Fire Facility (Equipment / Maintenance / Inspection) Standard",
"Overall compliance = sum of item scores ÷ full marks ×100%",
"Each item is scored by degree of compliance: non-compliant 0 / basically compliant 1 / compliant 2",
"≥90% compliant, 75-89% basically compliant, 60-74% needs rectification, <60% non-compliant",
"This tool is designed with reference to the Fire Protection Law and GB 50016 and other standards, and does not replace inspection by the fire department",
"📚 In-Depth Analysis: Fire Facility Compliance Self-Check",
"Monthly fire safety self-check at an organization, scoring each item under configuration, maintenance and inspection/acceptance and keeping a record.",
"Run an internal pre-check before a fire supervision inspection to spot deficiencies in extinguishers, hydrants and alarm systems in advance.",
"A newly appointed fire manager can use this form to quickly establish a baseline of facility status and set rectification priorities and funding order.",
"Scoring basis for the 16 self-check items",
"Each item scores 0 for non-compliant, 1 for basically compliant and 2 for compliant, giving a full mark of 32 for 16 items. For example, ",
"fire extinguisher configuration",
" and annual inspection maintenance are rated basically compliant while the other 14 items are compliant, giving 30 points: the system still judges it compliant, but lists the maintenance items as a priority in the rectification advice. Below 24 points usually indicates a systemic deficiency that requires immediate rectification and reporting.",
"How should the scoring result be graded and used?",
"Convert the 32-point full mark to a 100-point scale and grade it: ≥90% is good, 70%~90% needs partial rectification, and below 70% (24 points) is a systemic deficiency that should be listed as a major hazard for rectification within a deadline.",
"Can self-check replace the annual inspection?",
"No. Self-check is an internal daily management tool for promptly spotting problems, while third-party annual fire facility inspection and fire acceptance have legal effect; the depth and responsible party differ, so they cannot substitute for each other.",
"About: Fire Facility Compliance Self-Check",
"A fire facility compliance self-check tool for enterprises and institutions, covering 17 key points across the three modules of facility configuration, maintenance and inspection/acceptance, quantifying compliance and generating a hidden-hazard rectification list.",
"Checklist self-check across the facility / maintenance / inspection modules",
"Module pass rates and overall compliance",
"Automatically generates a hidden-hazard rectification list",
"Self-check for key fire safety units",
"Preparation for fire inspections",
"Assistance for the annual fire assessment",
"Property fire safety management",
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
    out = {'slug': slug, 'industry': 'fire-rescue', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
