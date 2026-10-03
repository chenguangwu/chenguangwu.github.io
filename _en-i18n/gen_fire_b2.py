#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'fire')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'fire')
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
    out = {'slug': slug, 'industry': 'fire', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('detector-178', build('detector-178', [
        "Maintenance (Detection/Repair/Upgrade) Service",
        "Detection/repair/upgrade",
        "View the Maintenance (Detection/Repair/Upgrade) Service User Guide",
        "Fire facility maintenance is evaluated item by item across 5 items (extinguishers, hydrants, alarm system, sprinkler system, emergency lighting and evacuation signage), with 1 point counted per problem; a maintenance period exceeding 3 months without inspection adds 2 points; a total of 0 means maintenance passes, 1 to 2 points is a minor defect, and 3 points or more requires rectification within a deadline; the statutory periods are extinguishers inspected once a year, hydrants inspected quarterly, and the alarm and sprinkler systems patrolled monthly with a full inspection once a year.",
        "Fire facility maintenance assessment (5-item maintenance quality detection)",
        "1. Extinguisher maintenance",
        "Passes as scheduled (0 points)",
        "Partially overdue (2 points)",
        "Large amount overdue/failed (3 points)",
        "2. Hydrant maintenance",
        "Pressure normal (0 points)",
        "Pressure insufficient (2 points)",
        "No water/damaged (3 points)",
        "3. Alarm system maintenance",
        "Operating normally (0 points)",
        "System down (3 points)",
        "4. Sprinkler system maintenance",
        "Network normal (0 points)",
        "Local leakage (2 points)",
        "Severely damaged (3 points)",
        "5. Emergency lighting/evacuation signage",
        "All normal (0 points)",
        "Partially not lit (2 points)",
        "Large area failure (3 points)",
        "Maintenance period (months)",
        "Assess the maintenance",
        "In-Depth Analysis: Maintenance (Detection/Repair/Upgrade) Service",
        "In fire facility maintenance assessment, extinguishers, hydrants, alarm, sprinklers and emergency lighting are scored item by item, combined with the maintenance period.",
        "During quarterly/annual assessment by the maintenance unit, the scoring quantifies pass, basically pass and fail.",
        "An overly long maintenance period deducts extra points, pushing the inspection interval shorter.",
        "Worked example: all pass, period 2 months",
        "Maintenance score = 0 / 17 -> 'maintenance passes'; recommended to keep the current 2-month maintenance period.",
        "Worked example: a 4-month period triggers the extra deduction",
        "If all items score 0 but the period is >3 months, the total gets +2 = 2 <= 4 -> 'basically passes', with the note 'maintenance period too long (4 months)', and shortening it to 1-2 months is recommended.",
        "Why does the maintenance period affect the score?",
        "A long period means the exposure window for hidden hazards grows; this tool deducts an extra 2 points for a period >3 months, to encourage shorter inspection intervals, in line with the maintenance principle of 'prevention first'.",
        "How are basically pass and fail defined?",
        "This tool uses a total of 0 for maintenance pass, <=4 for basically pass, and >4 for maintenance fail (17 in total, 0 = all pass). A fail requires immediate full overhaul and stronger patrolling.",
        "About Maintenance (Detection/Repair/Upgrade) Service",
        "Maintenance (Detection/Repair/Upgrade) Service. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))

    write('detector-44', build('detector-44', [
        "Detection (Annual Inspection/Repair/Refill) Service",
        "Annual inspection/repair/refill",
        "View the Detection (Annual Inspection/Repair/Refill) Service User Guide",
        "Months since the last annual inspection = (current date - last annual inspection date) / (30 x 24 x 3600 x 1000) milliseconds; a portable dry powder extinguisher must have its first hydrostatic test when 5 years old since leaving the factory and every 2 years after that, with a shell scrapping life of 10 years (12 years for carbon dioxide extinguishers); a pressure gauge pointer in the green zone is normal, the yellow zone is overpressure, and the red zone is insufficient pressure needing a refill; once the scrapping life is reached or the shell is corroded through, it is judged as fail and must be replaced.",
        "Extinguisher annual inspection and refill assessment (extinguisher condition check)",
        "Extinguisher type",
        "Carbon dioxide",
        "Dry powder",
        "Water-based",
        "Quantity (units)",
        "Last refill/annual inspection date",
        "Pressure gauge reading",
        "Green zone normal (0 points)",
        "Yellow zone high (2 points)",
        "Red zone insufficient (3 points)",
        "Shell corrosion",
        "Hose breakage",
        "Missing tamper seal",
        "Unclear label",
        "In-Depth Analysis: Detection (Annual Inspection/Repair/Refill) Service",
        "In the monthly/annual patrol of extinguishers, the annual inspection deadline and shell condition are checked by type (CO2 / dry powder / foam / water-based).",
        "Overdue, corrosion, hose breakage, missing seal and unclear label are deducted item by item, quantifying pass / needs maintenance / needs refill and replacement.",
        "Insufficient pressure is the key red line and must be sent for testing and refilling.",
        "Worked example: water-based extinguisher, 6 months since annual inspection, pressure normal, no exterior issues",
        "The maximum annual inspection period for water-based is 12 months, so 6 months is neither overdue nor near expiry (only >10 months triggers the near-expiry notice), pressure scores 0 and nothing is ticked -> score = 0 -> 'pass'; it can be used normally within its validity period.",
        "Worked example: scoring rules",
        "Overdue (12/12/24/12 months by type) adds 3 points and reports the overdue months; near expiry adds 1 point; corrosion or breakage adds +2 each; missing seal or unclear label adds +1 each; the pressure value is counted directly. 0 points pass, <=3 needs maintenance, >3 needs refilling/replacement.",
        "Is the annual inspection period the same for all extinguisher types?",
        "No. This tool uses 12 months for CO2/dry powder, 24 months for foam and 12 months for water-based (common figures, subject to the latest standard). Overdue deducts points and reports the overdue months.",
        "Why must insufficient pressure be refilled?",
        "Insufficient pressure means the internal pressure is below the working range, the spray distance and extinguishing capacity do not meet the standard, and there is a risk of failure at a critical moment; this is a hard red line and must be sent for testing and refilling or replacement, never used while faulty.",
        "About Detection (Annual Inspection/Repair/Refill) Service",
        "Detection (Annual Inspection/Repair/Refill) Service. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
    ]))

    write('smoke-spread', build('smoke-spread', [
        "Smoke Spread Estimation",
        "Estimates the smoke spread speed and visibility, assisting fire evacuation decisions",
        "Core formula (by input variable): alpha x (V_smoke / max(W x H, 0.1)) x t x 0.5; 0.071 x Q x (z)^0.667 x (Q / 1000)^-0.667; H - 0.012 x (Q)^1÷3 x (t)^2÷3 ÷ (H)^1÷3",
        "View the Smoke Spread Estimation User Guide",
        "Ceiling height H (m)",
        "Time after ignition t (seconds)",
        "Corridor width W (m)",
        "Smoke optical density coefficient α (m⁻¹, default 0.01)",
        "Plume flow rate",
        ": estimates the plume mass flow rate based on the Heskestad model",
        "Spread speed",
        ": estimates the ceiling jet velocity (about 0.5~1.2 m/s)",
        "Spread distance",
        ": the horizontal distance smoke spreads along the ceiling within time t",
        "Visibility",
        ": estimates visibility from the smoke optical density; below 10m is dangerous",
        "Smoke layer height",
        ": estimates the time for the smoke layer to descend to 1.8m (the danger height)",
        "This tool is for teaching and preliminary assessment only; actual fire protection design should be carried out by professionals.",
        "In-Depth Analysis: Smoke Spread Estimation",
        "In fire smoke assessment, the plume model is used to estimate flame height, plume mass flow rate and ceiling jet velocity.",
        "Smoke spread speed is a key input for smoke exhaust and evacuation design, and determines when the danger arrives.",
        "The Heskestad plume model applies to atrium/large space analysis with a steady fire source.",
        "Worked example: heat release rate 500 kW, ceiling height 3 m",
        "Fire source diameter D = √(4x500/(πx1000)) = 0.798 m; flame height Hf = 0.235x500^0.4 - 1.02x0.798 = 2.01 m; plume mass flow rate = about 56.6 kg/s; temperature rise ΔT = about 8.83 K; smoke",
        "= about 45.2 m3/s; ceiling jet velocity = about 0.89 m/s.",
        "Worked example: model key points",
        "Virtual origin z0 = 0.166·Q^0.4; plume height z = max(H-z0, 0.1); mass flow rate m = 0.071·Q·z^0.667·(Q/1000)^-0.667; ΔT = Q/m (take cp≈1.0). Jet velocity is clamped to 0.3-3.0 m/s.",
        "What are the applicable conditions of the Heskestad plume model?",
        "It applies to steady, roughly point-source, axisymmetric rising fire plumes, common in atrium and large space ceiling jet analysis. Unsteady, strong wind or wall-attached fires deviate from it, so another model or CFD is needed.",
        "How are the smoke volume flow rate and temperature rise used?",
        "The mass flow rate and temperature rise are used to estimate the smoke layer descent rate and hazard development; the volume flow rate and ceiling jet velocity are used for exhaust outlet layout and detection/sprinkler response judgement, and are the core inputs of performance-based design.",
        "About Smoke Spread Estimation",
        "Smoke Spread Estimation is an online tool in the business office field. Business office tools to improve work efficiency, with data processed locally to protect privacy.",
    ]))

    write('index', build('index', [
        "Fire Safety Tools",
        "Fire Safety",
        "Fire Safety Tools",
        "Hydrant Pressure at the Most Unfavourable Point Calculation",
        "Hydrant most unfavourable point pressure calculator. Enter parameters such as building height and pipe resistance to compute the required hydrant pressure and effective water jet at the most unfavourable point, for fire water system design and acceptance checks.",
        "Extinguisher Configuration Calculation (GB 50140)",
        "Personnel safe evacuation time estimator (flow method). Enter occupant density, exit width and flow coefficient, and estimate the total evacuation time by the flow method, for building fire evacuation design and safety assessment.",
        "Evacuation Time Estimation",
        "Estimates the required safe evacuation time RSET and compares it with the available safe egress time ASET, accounting for personnel evacuation by the flow method, for building fire design and safe evacuation assessment.",
        "Enter the fire heat release rate and space dimensions; the tool estimates the smoke spread speed and the visibility degradation curve, assisting preliminary fire evacuation and smoke exhaust decisions.",
        "Hydrant Pressure",
        "H = Hgeo + Hq + Hd + Hw, estimating the pressure required by the hydrant at the most unfavourable point",
        "Fire interlock system detection assessment tool. Evaluates the fire interlock service quality and hazards against 6 system interlock detection points (alarm, smoke exhaust, broadcast, etc.), and outputs rectification suggestions, for fire maintenance and annual inspection.",
        "Fire facility maintenance assessment tool. Evaluates the detection, repair and upgrade service quality against 5 maintenance quality detection points, and outputs a score and rectification items, for service quality management of fire maintenance units.",
        "Extinguisher annual inspection and refill assessment tool. Evaluates the extinguisher annual inspection, repair and refill service quality against condition check points, identifies fail items and gives handling suggestions, for periodic extinguisher management.",
        "Price (market/cost/competition) analysis tool. Enter product price, cost and competitor data, and compute gross margin and competitive positioning by general financial rules, for fire product pricing and business analysis (results for reference only).",
        "Randomly draws response procedure steps such as fire call receiving, confirmation and evacuation for question and answer, used to train or self-test the fire response proficiency of emergency personnel.",
        "About Fire Safety Tools",
        "The Fire Safety Tools collection holds 11 free online tools covering the common calculation, conversion and lookup needs of fire safety scenarios. Whether you are a practitioner, a student or an ordinary user, you can find practical ready-to-use tools here. All tools run entirely in the front end, data is not uploaded to the server, and privacy is protected.",
        "The fire safety tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common fire safety related tasks, with no need to memorise complex formulas or convert manually; enter and you get the result.",
        "Do the Fire Safety Tools need a download or registration?",
        "No. All fire safety tools on this page are pure front-end online tools; just open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the Fire Safety Tools results accurate? Is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, and results are available instantly. All computation is done locally on your device, data is never uploaded to the server, and privacy is protected.",
    ]))


if __name__ == '__main__':
    main()
