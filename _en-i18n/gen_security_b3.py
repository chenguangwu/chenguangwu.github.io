#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'security')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'security')
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
    out = {'slug': slug, 'industry': 'security', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('flood-level', build('flood-level', [
        "🔒 Flood Water-Level Gauge",
        "Flood warning-level reference table, simulating the impact and response measures of different water depths. Understand flood levels and prepare for flood control.",
        "Impact is judged by water depth and flow velocity: below 0.3 m pedestrians can still wade, 0.3-0.5 m walking is difficult, above 0.5 m adults easily lose stability, above 1 m can wash away vehicles; if the product of flow velocity and water depth (m2/s) exceeds 0.5 it is dangerous to people; the warning has four escalating levels by blue (minor flood), yellow (larger flood), orange (major flood), red (extreme flood), corresponding to four response measures: prepare, alert, evacuate, withdraw.",
        "Simulated water depth",
        "Water-level warning gauge",
        "Blue 50cm",
        "Yellow 100cm",
        "Orange 150cm",
        "Red 200cm",
        "Purple 250cm",
        "Drag the slider above to simulate different water depths",
        "Flood warning-level explanation",
        "Impact and response of different water depths",
        "Water depth",
        "Personnel risk",
        "Response measures",
        "Flood prevention guide",
        "⚠️ Before the flood arrives",
        "Follow warning information released by meteorological and water-authority departments",
        "Prepare flood-control materials such as sandbags and flood boards",
        "Move valuables and appliances to higher places",
        "Clear drains and ditches to ensure smooth drainage",
        "Prepare an emergency kit (food, water, medicine, flashlight, life jacket)",
        "Know the community evacuation route and shelter location",
        "🌊 During the flood",
        "Don't wade (15cm depth can make an adult fall, 46cm depth can wash away an adult)",
        "Stay away from power lines and electrical equipment to prevent electric shock",
        "Don't drive through flooded sections (30cm depth can float a car)",
        "If trapped, move to high ground and wait for rescue, send a distress signal",
        "Turn off main power and gas valves",
        "✅ After the flood",
        "Return only after officials declare it safe",
        "Don't drink untreated water; use boiled or bottled water",
        "Clear accumulated water and silt, and do disinfection and epidemic prevention",
        "Check house structural safety, photograph and keep loss evidence",
        "Key data: 15cm depth can make an adult fall, 30cm can wash away a car, 60cm can wash away large vehicles. Never underestimate the power of standing water.",
        "Tool introduction and usage",
        "The flood water-level gauge tool shows the flood warning-level system, simulating the impact and response of different water depths.",
        "Visualized water-level gauge",
        "5-level flood warning reference",
        "Water-depth impact simulation",
        "Graded response measures",
        "Flood-control prevention guide",
        "Flood-season safety",
        "Flood-control knowledge learning",
        "Community flood-control education",
        "Emergency shelter reference",
        "📚 In-Depth Analysis: Flood Water-Level Gauge",
        "When following local warnings during flood season, use the gauge to cross-reference standing-water depth and anticipate traffic, building and personal-safety impacts.",
        "Managers of low-lying shops, garages or underground spaces deploy water-blocking and evacuation measures in advance by warning level.",
        "In community flood-control promotion, explain to residents the response actions corresponding to each blue/yellow/orange/red/purple level.",
        "Example: 'standing-water depth grading'",
        "Warning-line grading (by standing-water depth): ≥50cm blue warning (low-lying areas begin to flood, check drainage); ≥100cm yellow (partial road flooding, lower floors flooded, move valuables, reduce outings); ≥150cm orange (one-story flooding, vehicles impassable, immediately move to high ground); ≥200cm red (multi-story flooding, power outage, emergency evacuation no return); ≥250cm purple (exceeds historical extreme, extreme flood, wait for rescue). Example: a garage forecast to reach 120cm standing water is a yellow warning, so move the car to high ground in advance and prepare flood boards.",
        "Does this level look at rainfall or standing-water depth?",
        "This tool grades by 'standing-water depth', reflecting the actual inundation already formed; meteorological departments separately have rainstorm warnings (blue/yellow/orange/red) based on 'rainfall', the two caliber differ, and for prevention one should combine local real-time water conditions with emergency-management releases for a comprehensive judgement.",
        "How should garages and basements be protected?",
        "Upon reaching yellow warning (≥100cm), move vehicles to high ground, prepare flood boards and sandbags, and cut power to underground spaces; at orange and above, decisively evacuate and never return for belongings - underground spaces easily trap people in floods, and life safety takes priority over property.",
    ]))

    write('index', build('index', [
        "🔒 Network Security Tools",
        "Network Security",
        "Network Security Tools",
        "Generate high-strength passwords with custom length, character set and exclusion rules, supporting passphrase mode, pure front-end generation without storage, suitable for account security and key management.",
        "Banking-grade online password generator, with settable length, character set and confusable-character exclusion, generating high-strength random passwords, data generated locally without upload, pure front-end.",
        "Generate a professional first-aid item list by usage scenario, supporting check-off confirmation and export/print. Better prepared than sorry; it can save lives at critical moments.",
        "Test monthly whether the smoke alarm works normally. Press the test button, time 15 seconds, record the self-check result, to safeguard home fire safety.",
        "Encrypt text with a password and store it in the local browser to protect your private information. All data is saved only on this machine's localStorage, not uploaded to any server.",
        "Quality (Standard/Certification/Testing) Assurance",
        "Enter key performance parameters of security products (such as protection height, response time), judge their safety protection grade and qualified conclusion per relevant GB standards, for product testing and selection reference.",
        "Demonstrates the working principles and steps of common data-erasure algorithms, visually simulating the process of data being overwritten. For safety-education purposes only.",
        "Detailed explanations of 50+ common scam tactics; knowing the scam patterns is the key to effective prevention. Supports random card drawing for learning and category browsing.",
        "Provides the Beaufort scale and China tropical-cyclone (typhoon) grade reference table, including wind-speed (m/s, km/h) conversion, per-grade destructiveness description and prevention advice, for typhoon-warning interpretation and emergency preparation.",
        "One-tap view of common emergency numbers, supports adding custom emergency contacts. Data is saved in the local browser, accessible anytime.",
        "Generate personalized earthquake escape advice based on living environment, including shelter locations, escape routes and post-quake notes.",
        "Flood warning-level reference table, simulating the impact and response measures of different water depths. Understand flood levels and prepare for flood control.",
        "About \"Network Security Tools\"",
        "The Network Security Tools collection includes 12 free online tools covering common calculation, conversion and query needs in network-security scenarios. Whether you are a practitioner, student or general user in the field, you can find ready-to-use handy tools here. All tools run purely on the front end, with no data uploaded to the server, protecting privacy and security.",
        "The network security tools included on this page (some representative tools):",
        "These tools help you quickly complete common network-security-related tasks without memorizing complex formulas or manual conversion; just enter to get results.",
        "Do the network security tools need download or registration?",
        "No. All network security tools on this page are pure front-end online tools; just open the web page to use them directly, no software installation, no account registration, and no data upload.",
        "Are the calculation results of the network security tools accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All calculations are completed locally on your device, and data is not uploaded to the server, ensuring privacy and security.",
    ]))

    write('smoke-alarm-test', build('smoke-alarm-test', [
        "⛅ Smoke Alarm Self-Check Timer",
        "Test monthly whether the smoke alarm works normally. Press the test button, time 15 seconds, record the self-check result, to safeguard home fire safety.",
        "Smoke alarms self-check monthly: hold the test key for 15 seconds, the alarm should emit a sound no lower than 85 dB; if silent or significantly weaker, it indicates low battery or sensor failure, and the battery or whole unit must be replaced; photoelectric alarms last about 8-10 years, ionization about 5-8 years, and must be replaced as a whole upon expiry; annual-check coverage = completed checks ÷ total to-be-checked × 100%, and check records are recommended to be archived monthly.",
        "Ready - after pressing the alarm test button, click 'Start Timing'",
        "Alarm location",
        "Near kitchen",
        "Children's room",
        "Garage",
        "Attic",
        "Test passed",
        "Test failed",
        "Self-check steps",
        "📅 Recommended frequency:",
        "Test each alarm at least once a month.",
        "🔋 Battery replacement:",
        "Replace batteries once a year (recommended at spring/autumn season change).",
        "🔄 Service life:",
        "Smoke alarms generally last 8-10 years and need whole-unit replacement upon expiry.",
        "🏠 Installation location:",
        "Install on each floor, outside each bedroom, and near the kitchen (at least 3 m from the cooking area).",
        "Self-check history",
        "Smoke alarm maintenance knowledge",
        "🔥 Alarm type",
        "Photoelectric:",
        "Sensitive to smoldering smoke, suitable for bedroom and living room, low false-alarm rate",
        "Ionization:",
        "Sensitive to open-flame smoke, fast response, suitable near kitchen",
        "Dual-sensor:",
        "Has both photoelectric and ionization sensing, wide coverage",
        "CO combo:",
        "Detects both smoke and CO, suitable for areas with gas equipment",
        "⚠️ Common problem handling",
        "Frequent false alarms:",
        "Check if too close to kitchen/bathroom, clean sensor dust",
        "No alarm:",
        "Check battery level and whether the sensor is expired, replace promptly",
        "Intermittent beep:",
        "Usually a low-battery hint, replace the battery immediately",
        "No response on test:",
        "If still no response after cleaning, the alarm needs replacement",
        "Cooking oil smoke may trigger false alarms; do not remove the battery because of this. If false alarms are frequent, consider moving the alarm away from the cooking area or switching to photoelectric.",
        "Tool introduction and usage",
        "The smoke alarm self-check timer helps you periodically test the working status of home smoke alarms, record test history and safeguard home fire safety.",
        "15-second standard test timing",
        "Record self-check by location",
        "Self-check history archive",
        "Test pass/fail marking",
        "Maintenance knowledge reference",
        "Home fire safety",
        "Monthly safety check",
        "Rental safety self-check",
        "Property fire management",
        "📚 In-Depth Analysis: Smoke Alarm Self-Check Timer",
        "Household monthly fire self-check: press the test key step by step, time 15 seconds and record each alarm's status.",
        "Landlords or property managers batch-test alarms in multi-unit or multi-story buildings, marking each pass or fail.",
        "When accepting newly installed alarms, use the timer to confirm whether the ringing persistence and stop response are normal.",
        "Example: 'single-alarm monthly self-check'",
        "Eight-step process: 1) notify family the test sound will be loud; 2) walk under the alarm and find the Test button; 3) hold the button until the alarm sounds; 4) after confirming normal sound, click 'Start Timing'; 5) keep holding 15 seconds to confirm continuous sounding; 6) release the button, the alarm should stop immediately; 7) if it does not sound or keeps sounding after release, mark 'Test failed'; 8) record the result and move to the next one. The timer helps objectively judge whether 'continuous sound for 15 seconds' and the stop response meet the standard.",
        "Why test every month?",
        "Alarms are battery-powered; long idle easily fails from battery drain or dust; monthly testing catches problems before failure at critical moments, and is the most basic and effective home-fire preventive measure.",
        "What if it keeps ringing during the test and won't stop?",
        "First release the test key; if it still rings continuously, it is mostly abnormal battery level or device fault - replace the battery first, and if still abnormal replace the whole unit; if necessary, remove the battery and contact after-sales, but never use tape to seal the alarm long-term.",
    ]))


if __name__ == '__main__':
    main()
