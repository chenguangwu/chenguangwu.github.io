#!/usr/bin/env python3
# fire-rescue batch5 (5 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fire-rescue')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fire-rescue')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'time-air': [
"🫁 SCBA Service Time Calculator",
"Enter the cylinder volume, pressure, breathing rate and work intensity to estimate the usable service time of a positive-pressure SCBA.",
"SCBA usable air usable = V·(P−P_alarm)/P_atm (V = cylinder volume in L, P = cylinder pressure in MPa, P_atm=0.101325 MPa); consumption rate = breathing rate × tidal volume; service time t = usable/consumption rate; safe time = 0.75·t.",
"Cylinder volume (L)",
"Cylinder pressure (MPa)",
"Alarm pressure (MPa)",
"Breathing rate (breaths/min)",
"Work intensity",
"Light (tidal volume 0.8 L)",
"Moderate (tidal volume 1.5 L)",
"Heavy (tidal volume 2.5 L)",
"💡 Usable air = V×(P−P_alarm)/0.101325; consumption rate = breathing rate × tidal volume; service time = usable air / consumption rate.",
"The alarm pressure is the residual-air alarm threshold, usually 5-6 MPa; evacuate immediately when the alarm sounds.",
"The greater the work intensity and the faster the breathing, the faster the air is consumed; heavy work roughly halves the time.",
"Reserve 25% of the time for withdrawal; do not use the entire supply for work.",
"Actual consumption is affected by individual variation, mask seal and psychological state; the result is for estimation only.",
"📚 In-Depth Analysis: SCBA Service Time",
"Before entering dense smoke or oxygen-deficient areas, estimate the usable and safe working time from the cylinder capacity and consumption rate.",
"Set a withdrawal margin to prevent casualties from insufficient residual air.",
"In training, demonstrate the significant effect of the consumption rate on working time under different work intensities.",
"Calculation for a 6.8 L/30 MPa cylinder at 30 L/min consumption",
"With the default parameters (cylinder 6.8 L, fill pressure 30 MPa, consumption rate 30 L/min, 25% withdrawal margin retained): total stored air about 2013 L, usable air 1644 L, service time about 54.8 min, safe working time about 41.1 min; the tool rates it 'sufficient air'. High-intensity work can double the consumption rate, so a more conservative estimate should prevail in practice.",
"Why reserve a 25% margin?",
"The margin is for breathing on the way out and unexpected delays, preventing insufficient pressure on the return; codes usually require sufficient air to reach a safe area after the alarm, and 25% is a common conservative value.",
"How is the consumption rate chosen?",
"At rest about 20-30 L/min, while heavy work such as carrying or climbing can reach 40-60 L/min; time estimation should use the upper limit for the task intensity, better short than long.",
'About "SCBA Service Time Calculator"',
"Based on the cylinder volume and pressure of a positive-pressure SCBA and the user's work intensity, estimate the usable service time and safe working time, providing a safety reference for interior firefighting and rescue operations.",
"Accounts for residual-air deduction at the alarm pressure",
"Distinguishes light/moderate/heavy work intensity",
"Outputs the usable air volume and consumption rate",
"Automatically computes the safe working time",
"Estimating interior firefighting working time",
"Rescue cylinder allocation planning",
"SCBA training timing",
"Controlling safe withdrawal time",
"Cylinder volume",
"Cylinder pressure",
"Alarm pressure",
"Breathing rate",
],
'speed-3': [
"🏎️ Descender Speed Control Calculator",
"Based on the capstan formula, estimate the control force and theoretical descent speed of a descender at different wrap counts and friction coefficients.",
"Rope friction descent by the Euler-Eytelwein formula: T_load/T_hold = e^(μ·θ), θ=2πn (n = wraps); control tension T_ctrl = m·g/e^(μθ); acceleration a = g/e^(μθ), final speed v=√(2ah), braking share (1−1/e^(μθ))×100%.",
"Load weight (kg)",
"Rope diameter (mm)",
"Number of wraps n",
"Descent height (m)",
"💡 Capstan formula: T",
"control",
", θ=2πn; descent acceleration a = g·e",
", speed v = √(2ah).",
"The friction coefficient μ depends on the rope material and moisture: dry nylon is about 0.15-0.25 and can drop to 0.1 when wet.",
"The more wraps, the smaller the control force and the slower the descent, but too many wraps can jam the rope.",
"The theoretical speed is a uniform-acceleration estimate; in practice the operator controls it in real time and it should not exceed 2-3 m/s.",
"Rescue operations must use certified descenders and safety ropes; this result is for training reference only.",
"📚 In-Depth Analysis: Rope Descent Speed Control",
"In high-angle and cliff-descent work, estimate the descent speed and acceleration from the load, wrap count and friction coefficient.",
"Assess whether the descent speed is too fast and judge whether to add wraps or reduce the load.",
"In training, demonstrate how different friction coefficients affect the control-side force and the braking ratio.",
"Descent for an 80 kg load, 2 wraps, μ=0.2",
"With the default parameters (load 80 kg, 2 wraps, friction coefficient 0.2): theoretical descent speed 3.99 m/s, descent acceleration 0.795 m/s², descent time 5.02 s; control-side force 63.6 N, capstan braking ratio 12.35, gravity-braking share 91.9%. The tool rates it 'speed too fast', recommending more wraps or a reduced load to slow the descent.",
"Why add wraps when the speed is too fast?",
"The more wraps, the longer the rope contacts the anchor point, the stronger the friction braking and the slower the descent; 2 wraps at μ=0.2 already reach 3.99 m/s, so in practice 3-4 wraps are often used for a more controllable speed.",
"What does a high gravity-braking share indicate?",
"A high gravity-braking share means the system relies mainly on rope friction rather than mechanical braking to control speed, which wears the rope and anchor point more and is less controllable; mechanical braking should be added or the wrap pattern adjusted.",
'About "Descender Speed Control Calculator"',
"Using the capstan friction principle, estimate the control-side force and theoretical descent speed of a descender at different wrap counts and friction coefficients, providing a reference for high-angle rescue training and equipment use.",
"Based on the classic capstan friction formula",
"Outputs the control force and braking ratio",
"Estimates the descent acceleration and speed",
"Automatically gives a safety-level assessment",
"High-angle rescue descent training",
"Rescue rope equipment selection",
"Descent-plan speed verification",
"Rescue instruction demonstration",
"Load weight",
"Rope diameter",
"Number of wraps",
"Descent height",
],
'time-lux': [
"🚑 Emergency Lighting Duration Calculator",
"Enter the battery capacity, luminaire power, illuminance requirement and lit area to compute the emergency-lighting duration and the number of luminaires required.",
"Battery energy Wh = (capacity/1000)·voltage×0.8; single-lamp duration = Wh/power; lamps needed N = ⌈area×lux/(lumens×utilization)⌉; system duration = Wh/(N×power).",
"Power per lamp",
"Luminous efficacy (lm/W)",
"Illuminance requirement",
"Lit area (m²)",
"Utilization factor",
"💡 Battery energy Wh = (mAh/1000)×V; lumens per lamp = power × efficacy; lamps needed = area×illuminance/(lumens per lamp × utilization factor); system duration = Wh/total power.",
"Fire emergency lighting and exit signage must provide at least 30 min of continuous power, and at least 60 min in high-risk locations.",
"Illuminance requirements: evacuation corridors ≥1 lx, refuge floors and assembly occupancies ≥3 lx; 5 lx may be used as a general estimate.",
"The utilization factor depends on the luminaire light distribution and space height, generally 0.6-0.8.",
"The actual usable battery capacity is affected by discharge efficiency; a factor of 80% is recommended.",
"📚 In-Depth Analysis: Emergency Lighting Endurance Estimation",
"In evacuation-lighting design, estimate the system's continuous power-supply time from the battery energy and luminaire power.",
"Verify whether the duration meets the code-required emergency-lighting time.",
"In maintenance, assess whether luminaires still need replacing or adding after battery degradation.",
"Configuration of a 115.2 Wh battery and 2 × 5 W lamps",
"With the default parameters (usable battery energy 115.2 Wh, 2 × 500-lumen lamps, 5 W per lamp): system total power 10 W, single-lamp duration about 23.0 h, system duration about 11.5 h; the tool rates it 'duration somewhat short (converted at 80% discharge efficiency)', recommending increasing the ",
" or reducing the number of luminaires. If the code requires emergency lighting ≥90 min, this configuration far exceeds it, but long-duration duty requires a separate calculation.",
"Why is the system duration shorter than a single lamp's?",
"The system total power is the sum of all luminaires, and with fixed battery energy the greater the total power the shorter the duration; 11.5 h is the total duration with the whole system lit simultaneously.",
"How to understand the 80% discharge efficiency?",
"A battery cannot be fully discharged and must retain a protection margin; converting at 80% usable depth gives the actually releasable energy, avoiding over-discharge damage or a sudden power loss.",
'About "Emergency Lighting Duration Calculator"',
"Compute the duration of fire emergency lighting and the number of luminaires required from the battery capacity and luminaire parameters, for emergency-lighting system configuration and power-supply verification.",
"Compute battery usable energy and luminous flux",
"Derive the luminaire count from area and illuminance",
"Gives both the single-lamp and system durations",
"Converted at 80% discharge efficiency",
"Fire emergency lighting system configuration",
"Backup power capacity verification",
"Emergency luminaire count planning",
"Fire design and acceptance",
"Power per lamp",
"Luminous efficacy",
"Illuminance requirement",
"Lit area",
"Utilization factor",
],
'calc-time-response': [
"🎧 Sprinkler RTI Response Time Calculator",
"Enter the sprinkler RTI value, gas temperature, gas velocity and other parameters to compute the response/actuation time of a closed sprinkler head in a fire.",
"Sprinkler response time t = (RTI/√u)·ln[(Tg−Ti)/(Tg−Tact)]: RTI = Response Time Index, u = gas velocity, Tg = gas temperature, Ti = initial temperature, Tact = activation temperature; time constant τ = RTI/√u.",
"RTI value (m·s",
"Gas temperature Tg (℃)",
"Gas velocity u (m/s)",
"Initial temperature Ti (℃)",
"Activation temperature Tact (℃)",
"💡 Formula: t = (RTI / √u) × ln[(Tg − Ti) / (Tg − Tact)]; where τ = RTI/√u is the sprinkler time constant.",
"The sprinkler actuates only when Tg > Tact > Ti, otherwise it prompts that it cannot start.",
"RTI reflects the sprinkler's thermal sensitivity: quick-response sprinklers have RTI≤50 and standard-response RTI≈80-100.",
"Gas velocity u takes the average ceiling-jet velocity, usually 1-3 m/s.",
"This formula is based on the lumped-thermal-capacity model and is suitable for estimating the sprinkler heating stage; the result is for design reference.",
"📚 In-Depth Analysis: Sprinkler RTI Response Time Calculation",
"In sprinkler selection, compare the effect of different RTI values (quick response ≤50, special response 50-80, standard response 80-350) on the actuation time.",
"In tall-space projects, assess the delay of sprinkler actuation caused by ceiling gas velocity and judge whether denser layout or early-suppression sprinklers are needed.",
"In performance-based design, use the sprinkler actuation time as a time node on the fire growth curve to verify ASET.",
"Actuation time of an RTI=50 sprinkler in 300℃ smoke",
"With the default parameters (RTI=50 (m·s)^0.5, gas temperature 300 ℃, gas velocity 2.0 m/s, initial 20 ℃, actuation temperature 68 ℃): time constant τ = RTI/√u = 50/1.414 = 35.4 s; ln[(Tg−Ti)/(Tg−Tact)] = ln[280/232] = 0.1881; response/actuation time = 35.4 × 0.1881 = 6.65 s, rated quick response. If the gas velocity is reduced to 0.5 m/s, τ rises to 70.7 s and the actuation time doubles to 13.3 s.",
"What is RTI, and what value counts as quick response?",
"The Response Time Index RTI comprehensively reflects the thermal inertia and heat transfer ",
"efficiency",
", with the unit (m·s)^0.5, and the smaller the value the faster the response. Typically RTI≤50 is a quick-response sprinkler, 50-80 special response and 80-350 standard response.",
"Does a higher gas velocity always actuate the sprinkler faster?",
"At the level of the formula, yes — τ=RTI/√u, so the greater the gas velocity the faster the heat transfer. But a high-speed ceiling jet may also blow hot smoke away from the sprinkler and lower the temperature around it; in engineering, CFD simulation or physical testing should be used rather than relying on the formula alone.",
'About "Sprinkler RTI Response Time Calculator"',
"Based on the sprinkler Response Time Index (RTI) and the lumped-thermal-capacity model, compute the actuation response time of a closed sprinkler under hot fire smoke, for automatic sprinkler system design and performance-based assessment.",
"Uses the internationally accepted RTI lumped-thermal-capacity formula",
"Automatically determines whether the sprinkler can actuate",
"Outputs the time constant and response class",
"Supports a custom activation temperature",
"Automatic sprinkler system design",
"Sprinkler selection and response analysis",
"Fire-engineering instruction demonstration",
"RTI value",
"Gas temperature",
"Gas velocity",
"Initial temperature",
"Activation temperature",
],
'high-rise-fire': [
"🚒 High-Rise Fire Suppression Planner",
"Recommend suppression tactics, force deployment and a water-supply plan from the high-rise fire situation.",
"The aerial ladder must reach the fire floor: ladderReach = ladder height ≥ building height × (fireFloor/totalFloors); flagged super-high-rise when height > 100 m; the staging floor is set one below the fire floor: elevatorFloor = max(1, fireFloor−1).",
"Number of floors",
"Fire floor",
"Building use",
"Complex",
"Fire development stage",
"Decay stage",
"Maximum aerial-ladder height (m)",
"📖 High-Rise Suppression Key Points",
"Vertical water-supply methods",
"1. Fire pump adapter + indoor hydrant riser (preferred)",
"2. Lay hose vertically along the exterior wall/stairwell (≤100 m)",
"3. Relay water supply via intermediate tanks (super-high-rise)",
"4. Fire engine pumping directly to the pump adapter",
"Force-deployment principles",
"Deploy one team each on the fire floor, the floor above and the floor below",
"Park the fire elevator at the floor below the fire floor and ascend 1-2 floors on foot",
"Use refuge floors as relay staging, equipment transfer and casualty treatment bases",
"High-rise fire suppression is extremely complex; this tool provides tactical reference, and actual command must be decided by the on-scene situation and force dispatch.",
"📚 In-Depth Analysis: High-Rise Fire Suppression Simulation",
"After reconnaissance of a high-rise fire, deploy interior-attack, defensive, search-and-rescue and water-supply forces by fire floor.",
"Develop a fire-elevator parking strategy and vertical shaft sealing measures to prevent the stack effect.",
"Train company-level commanders to be familiar with the rhythm of 'decide within 5 minutes of arrival, reassess every 15 minutes'.",
"Force deployment for an 80 m high-rise with a fire on the 15th floor",
"With the default parameters (building height 80 m, fire floor 15): deploy a main-attack team of 2-3 on the fire floor (15) for interior firefighting; a defensive team of 2 on the floor above (16) to cut off upward spread; a search-and-rescue team on the floor below (14) to confirm no spread; manually control the fire elevator to park at floor 14, with personnel ascending 1-2 floors on foot to the fire floor; water supply uses fire engine → pump adapter → indoor riser as the preferred method, ensuring 6.5 L/s per nozzle.",
"Why must the fire elevator be parked manually?",
"During a fire the fire elevator must be manually controlled by firefighters and kept waiting with its doors open at the designated floor, to avoid automatically returning to the base station or being invaded by smoke and fire, ensuring attack and rescue personnel can move up and down quickly and safely.",
"Why must vertical shafts be sealed?",
"Vertically connected spaces such as pipe shafts and cable shafts form a 'stack effect' that makes smoke and flames spread rapidly upward along the shaft; sealing them normally and closely monitoring them during a fire are key measures for high-rise fire control.",
'About "High-Rise Fire Suppression Planner"',
"Based on the high-rise height, fire floor, fire stage and other parameters, recommend suppression tactics, force deployment, vertical water supply and evacuation plans.",
"Fire-stage-adaptive tactics",
"Staged force-deployment recommendations",
"Multi-mode vertical water supply",
"Special handling for super-high-rises",
"High-rise fire plan",
"Command decision support",
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
