#!/usr/bin/env python3
# fire-rescue batch7 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fire-rescue')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fire-rescue')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'temp-6': [
"🌡️ Fire Temperature Curve Calculator",
"Select a fire type and enter the exposure time to compute the fire temperature and heating rate, with a standard time-temperature reference table.",
"Fire type",
"Standard fire (ISO 834)",
"Hydrocarbon fire",
"External fire",
"Localized fire",
"Exposure time t (min)",
"💡 ISO 834: T=345·lg(8t+1)+20; hydrocarbon: T=1100·(1−0.325·e",
"); external: T=660·(1−0.687·e",
"The standard fire curve ISO 834 is used for evaluating the fire-resistance performance of building members and heats up relatively slowly.",
"Hydrocarbon fires heat up extremely fast initially, approaching 1100℃ within minutes, common in oil and chemical fires.",
"A localized fire is cooler than a fully developed fire and is suitable for estimating localized ignition-source scenarios.",
"The curve is a standard temperature-time relationship; actual fire-scene temperature is strongly affected by fuel, ventilation and heat loss.",
"📚 In-Depth Analysis: Standard Fire Heating Curve",
"In structural fire design, evaluate the member temperature at different fire-exposure times using the ISO 834 standard heating curve.",
"Compare the effect of different heating stages (early/growth/high-temperature) on material strength degradation.",
"Instructional demonstration of the heating-rate difference between a standard fire and a real fire (such as a hydrocarbon fire).",
"Standard fire temperature at t=10 min",
"With the default parameters (standard fire ISO 834, exposure time t=10 min): T = 20 + 345·lg(8t+1) = 20 + 345·lg(81) = 20 + 345×1.908 = 678.4 ℃; net temperature rise 658.4 ℃, heating rate about 15.58 ℃/min, in the high-temperature stage. This curve is used for member fire-resistance testing and fire-resistance load-bearing calculation.",
"Does the ISO 834 curve apply to all fires?",
"It represents the average heating of a cellulosic fire and is used for standard member fire-resistance testing; hydrocarbon fires (such as a pool fire) heat up faster and require the RABT/hydrocarbon curve, so ISO 834 must not be applied.",
"What does 678℃ at 10 minutes mean?",
"This is the ambient temperature inside the standard test furnace, reflecting the rapid rise in the initial exposure stage; the actual member temperature also depends on the section, protective layer and heat conduction, but the heating curve is the unified basis for fire-resistance-limit determination.",
'About "Fire Temperature Curve Calculator"',
"Based on international standard temperature-time curves (ISO 834, hydrocarbon, external, localized fire), compute the fire temperature and heating rate at a given exposure time, for structural fire-resistance analysis and fire-scene assessment.",
"Supports 4 standard fire temperature curves",
"Outputs the temperature, heating rate and net temperature rise",
"Automatically generates a multi-interval temperature reference table",
"Distinguishes fire-temperature stages",
"Building-member fire-resistance performance analysis",
"Fire-scene temperature development assessment",
"Structural fire-resistance design evaluation",
"Fire research and instruction",
"Exposure time",
],
'time-evacuation': [
"🔥 Evacuation Time Comparison (ASET/RSET)",
"Enter the components of the available safe egress time (ASET) and required safe egress time (RSET) to compare and judge evacuation safety.",
"Required safe egress time RSET = detection/alarm t_det + pre-movement t_pre + travel t_move; safety margin = ASET − RSET; safety factor K = ASET/RSET (K≥1.5 safe, K<1.0 unsafe).",
"ASET available safe egress time (min)",
"Detection/alarm time (min)",
"Pre-movement time (min)",
"Travel time (min)",
"💡 RSET = detection/alarm + pre-movement + travel time; safety criterion: ASET ≥ RSET and safety factor ASET/RSET ≥ 1.2 is acceptable.",
"ASET is the time available before a dangerous critical state arrives, determined by smoke descent, temperature and toxicity.",
"RSET consists of three parts: detection/alarm, pre-movement behavior (recognition and reaction) and travel time.",
"In engineering, ASET/RSET ≥ 1.2 is usually required, and 1.5 or above for important premises.",
"The result is for reference in performance-based fire design and evacuation-safety assessment.",
"📚 In-Depth Analysis: Available/Required Egress Time Comparison",
"In performance-based fire design, compare ASET and RSET to judge whether evacuation is safe.",
"For large-event security plans, back-calculate the required ",
"evacuation time",
"For renovation projects, re-check whether the ASET/RSET safety factor still meets the standard after a layout change.",
"Determination for RSET 7 min and ASET 10 min",
"With the default parameters (detection/alarm 1 min + pre-movement 2 min + travel 4 min = RSET 7.0 min, ASET 10.0 min): safety margin = 10 − 7 = 3.0 min, safety factor ASET/RSET = 1.43, rated 'safe (compliant)', recommending keeping the current evacuation conditions. If RSET rises to 9 min, the margin is only 1 min and the factor 1.11, approaching the acceptable lower limit.",
"Which of ASET and RSET is more important?",
"Neither can be dispensed with; the key is ASET > RSET with an adequate margin; the engineering acceptability criterion usually requires ASET/RSET ≥ 1.5 (some codes take 1.2-1.3), and the larger the safer.",
"Which part of RSET is easiest to shorten?",
"Travel time depends on distance and exit width, and pre-movement time depends on the alarm and occupants' state; optimizing evacuation signage, reducing pre-movement delay and widening exits most effectively reduce RSET.",
'About "Evacuation Time Comparison (ASET/RSET)"',
"Evaluate building evacuation safety by comparing the available safe egress time (ASET) with the required safe egress time (RSET), the core method of performance-based fire design and evacuation assessment.",
"Automatic summing of the three RSET stages",
"Computes the safety margin and safety factor",
"Graded determination of evacuation safety",
"Gives optimization recommendations",
"Building evacuation-safety analysis",
"Fire acceptance and justification",
"Detection/alarm time",
"Pre-movement time",
"Travel time",
],
'pressure-flow': [
"🎚️ Fire Hose Flow-Pressure Calculator",
"Enter the hose inlet pressure, outlet pressure, diameter and length to back-calculate the hose's actual flow and velocity from the pressure difference.",
"Flow from pressure drop (inverted Hazen-Williams): Q = [ΔP÷0.00980665 · C^1.852·D^4.87 ÷ (10.67·L)]^(1/1.852); velocity v = Q÷A (Q in m³/s, D in m).",
"Inlet pressure P₁ (MPa)",
"Outlet pressure P₂ (MPa)",
" (inverted Hazen-Williams).",
"The inlet pressure must be greater than the outlet pressure, otherwise no flow is produced.",
"The pressure difference is the head loss to overcome friction along the hose and does not include local losses.",
"The velocity is recommended to be kept within 2-3 m/s; too high a value easily damages the hose.",
"The result is for on-site flow estimation; in practice the flow meter or pressure gauge reading prevails.",
"📚 In-Depth Analysis: Pipe Pressure-Flow Conversion",
"In water-supply and fire-pipe network design, estimate the flow, velocity and head loss from the pressure difference and pipe diameter.",
"Verify whether the pipe-section velocity exceeds the economic/safety upper limit and judge whether the diameter needs enlarging.",
"During pump-room or sprinkler system commissioning, back-calculate whether the diameter and flow match the design condition.",
"Pipe-section verification at a 0.2 MPa pressure difference",
"With the default parameters (pressure difference 0.2000 MPa, velocity about 8.98 m/s for the diameter): flow 29.78 L/s (107.2 m³/h), velocity 8.98 m/s, friction head loss about 20.39 m. The tool rates it 'velocity too high' — the economic velocity of a water-supply pipe is usually 1-3 m/s, and even a fire main should not exceed 5 m/s for long; it is recommended to enlarge the diameter or shorten the pipe section to reduce the velocity and head loss.",
"What velocity counts as too high?",
"The economic velocity of a domestic water-supply pipe is about 1-3 m/s, and a fire pipe may be higher briefly but should not exceed 5 m/s for long; too high a velocity significantly increases head loss, causes water hammer and noise, and accelerates pipe-wall wear.",
"What mainly reduces the velocity?",
"At the same flow, enlarging the diameter lowers the velocity roughly by the square of the area (doubling the diameter cuts the velocity to about 1/4), the most direct way to control velocity and head loss.",
'About "Fire Hose Flow-Pressure Calculator"',
"Using the pressure difference between the hose inlet and outlet and the Hazen-Williams formula to back-calculate the hose's actual flow and velocity, for on-site supply-status assessment and hydraulic verification.",
"Back-calculates the flow and velocity from the pressure difference",
"Automatically assesses whether the velocity is reasonable",
"Outputs both L/s and m³/h",
"Supports multiple diameters and hose types",
"On-scene actual supply-flow assessment",
"Hose hydraulic-condition verification",
"Pressure-flow relationship instruction",
"Supply-plan optimization",
"Inlet pressure",
"Outlet pressure",
"Hose length",
"💡 Formula: hf = (P₁−P₂)/0.00981; Q = [hf × C",
],
'calc-pressure-1': [
"🎚️ Hose Pressure Loss Calculator",
"Enter the hose diameter, length, flow and type to compute the friction pressure loss using the Hazen-Williams formula.",
"Hose friction head loss by Hazen-Williams: h_f = 10.67·Q^1.852·L ÷ (C^1.852·D^4.87) (mH₂O, Q in m³/s, D in m); pressure drop ΔP = h_f×0.00980665 (MPa); velocity v = Q÷A.",
"Lined hose (C=140)",
"New polyurethane (C=150)",
"Unlined canvas (C=100)",
"Old lined hose (C=120)",
"); pressure loss ΔP = hf × 0.00980665 MPa.",
"The Hazen-Williams formula is suitable for estimating the friction head loss of fire hose in normal-temperature clear water under turbulent flow.",
"The C value is the Hazen-Williams roughness coefficient: 140 for lined hose, up to 150 for new hose, and it should be reduced appropriately for old hose.",
"The result does not include local losses at couplings and elbows (local losses are generally estimated at 10%-20% of the friction loss).",
"The result is for reference in firefighting water-supply calculation only; in practice the on-site pressure-gauge reading prevails.",
"📚 In-Depth Analysis: Hose Pressure Loss Calculation",
"In fire water supply, estimate the friction loss of a main from the hose diameter, length and flow and back-calculate how high the pump outlet pressure must be to ensure the nozzle pressure.",
"For long-distance relay supply, compare the loss of a single DN65 main versus two mains in parallel to decide the laying method.",
"Equipment selection and training: verify how much friction loss is reduced by replacing an old lined hose with a new polyurethane-lined hose (C≈150).",
"Friction loss of a DN65 hose, 20 m, 6.5 L/s",
"With the default parameters (DN65, lined hose C=140, length 20 m, flow 6.5 L/s): pipe velocity about 1.96 m/s, friction head loss 1.22 mH₂O (0.0119 MPa), about 0.014 MPa including estimated local losses, equivalent to about 0.06 MPa per 100 m. This means a 200 m main loses about 0.12 MPa along the way, so the pump outlet pressure must be raised accordingly to ensure the nozzle-end pressure.",
"Why does the loss increase so much when the flow doubles?",
"The friction loss is approximately proportional to the 1.85 power of the flow: raising the flow from 6.5 to 13 L/s increases the loss about 3.6×. So the first measure to increase supply is to enlarge the hose diameter or lay mains in parallel, not simply to raise the pump pressure.",
"How much loss do two mains in parallel reduce?",
"When two mains of the same specification are laid in parallel, each carries only half the flow and the loss drops to about 30% of a single main; this is standard practice for long-distance, high-flow supply, at the cost of doubling the laying work and hose consumption.",
'About "Hose Pressure Loss Calculator"',
"The hose pressure loss calculator estimates the friction pressure loss of a fire hose at a given diameter, length and flow, providing data support for fire-scene water supply, pump-pressure estimation and series hose laying.",
"Based on the internationally accepted Hazen-Williams formula",
"Supports 4 diameters and 4 hose types",
"Outputs multiple units (mH₂O / MPa / bar) simultaneously",
"Automatically computes the velocity and an estimate including local losses",
"Fire-scene supply-pressure estimation",
"Series hose laying planning",
"Fire-pump outlet pressure verification",
"Water-supply training and instruction demonstration",
"Hose length",
],
'detector-11': [
"⚡ Leakage Detection and Detector Status Assessment",
"Enter the measured and rated leakage current to judge whether leakage exceeds the limit, and self-check the state of the leakage detector to ensure the test equipment is reliable.",
"Leakage (detector) testing",
"/ Leakage (detector) testing",
"Leakage ratio = measured leakage current ÷ rated operating current; a ratio of not less than 1 is judged over-limit (the protective device should trip), 0.5 to 1 is critical and needs attention, and below 0.5 is normal; the rated operating current of a residential leakage protector is usually 30 mA (operating time not more than 0.1 s), and 100 to 300 mA may be used in industrial settings; the detector self-check includes battery level, zero calibration and comparison with a standard source, and an error exceeding ±10% requires sending for inspection.",
"I. Leakage-current determination",
"Rated leakage operating current IΔn (mA)",
"Measured leakage current IΔ (mA)",
"II. Detector status self-check",
"The leakage-current determination follows GB 13955 Residual Current Operated Protective Devices: a measured value ≥ IΔn should trip, and 0.5×IΔn to IΔn is the warning zone",
"In general locations IΔn ≤30 mA, in damp locations ≤15 mA, and in special locations such as swimming pools ≤10 mA",
"The detector should be calibrated regularly and a self-test function check performed before use",
"During testing, keep a safe distance and wear insulating protective equipment",
"📚 In-Depth Analysis: Leakage Detection and Detector Status Assessment",
"Before an electrical fire-safety inspection, self-check the leakage detector, confirming the battery, power-on self-test, range selection and calibration validity.",
"After on-site measurement, compare the measured leakage current with the rated operating current to judge whether the protective device will operate within the expected range.",
"When a maintenance unit sets up an instrument ledger, use this table as the checklist before each inspection and keep it on file.",
"Interpretation of a measured 15 mA on a 30 mA rated circuit",
"With the default parameters (rated leakage operating current 30 mA, measured leakage current 15 mA): the measured value is 50% of the rated value, in the non-operating zone of the protector, meaning the circuit's leakage has not reached the operating threshold. But it has reached the empirical warning line of 'over 50% of rated value, investigate the cause', so recording the trend and investigating the insulation-aging point later is recommended; if the measured value exceeds 30 mA while the protector does not trip, the protector is judged failed and must be replaced immediately.",
"At what measured leakage must action be taken?",
"The empirical practice is to use 50% of the rated operating current as the warning line, beyond which the cause is investigated; if the rated value is reached or exceeded while the protector does not operate, the leakage protector has failed, an electrical fire hazard that must be rectified immediately.",
"Why must the calibration validity be checked?",
"Once a clamp leakage meter is past its calibration period, the reading deviation may reach the order of tens of milliamps. Judging 'pass/fail' on this basis would directly mislead rectification decisions and even miss real leakage hazards.",
'About "Leakage Detection and Detector Status Assessment"',
"An electrical leakage-detection aid: enter the measured leakage current and rated operating current to automatically determine the leakage state (normal/warning/over-limit), and perform a pre-use status self-check of the leakage detector.",
"Leakage-current ratio determination (GB 13955 standard)",
"5-item detector status self-check list",
"Automatically identifies warning and over-limit states",
"Fire electrical-safety inspection",
"Leakage detection at construction sites",
"Residual-current protective device commissioning",
"Electrical fire-hazard screening",
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
