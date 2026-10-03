#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'elderly')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'elderly')
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
    out = {'slug': slug, 'industry': 'elderly', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('aid-height', build('aid-height', [
        "Assistive Device Height",
        "Compute the suitable adjusted height of crutches, walkers and canes from the user's height and the device type",
        "Core formula (by input variable): Math.round(effectiveH x dev.ratio)",
        "View the Assistive Device Height User Guide",
        "User height (cm)",
        "Heel height (cm, optional)",
        "Single-sided cane (elbow crutch)",
        "Axilla crutch (crutch)",
        "Forearm support crutch",
        "Walker (four-wheel / frame type)",
        "Quad cane",
        "Measurement method",
        "The right height reduces shoulder and wrist joint injury and improves support stability. For first use, have a rehabilitation therapist adjust it on site; the result of this tool serves as a reference starting point.",
        "When using an axilla crutch, do not bear weight with the armpit pressed onto the armpit rest, as this injures the axillary nerve; bear weight by gripping the handle.",
        "In-Depth Analysis: Assistive Device Height",
        "When older adults and rehabilitation users select a cane, axilla crutch, forearm crutch or walker, the handle/top height should fit the body height to avoid stooping or shrugging.",
        "An improper height causes excessive elbow flexion (fatigue) or a forward-leaning posture (falling), and is the primary fitting parameter of assistive devices.",
        "The clinically common 'greater trochanter / wrist crease method': standing with shoes on and arms relaxed, the device handle is about level with the wrist crease and the elbow is flexed 20 degrees to 30 degrees.",
        "Worked example: height 170cm, shoe thickness 2cm, single-sided cane selected",
        "Effective height = 170 + 2 = 172.0 cm; cane handle height = round(172 x 0.46) = 79 cm (about 46% of height); axilla crutch total length = 172 x 0.77 = about 132 cm; forearm crutch handle = 172 x 0.50 = about 86 cm; walker handle = 172 x 0.49 = about 84 cm.",
        "Worked example: where the ratios come from",
        "Cane handle = greater trochanter height (about 0.46 of height), axilla crutch total length = about 0.77 of height (plus about 5cm for the 2-3 finger gap between the armpit rest and the armpit), forearm crutch and walker handle = wrist crease height (about 0.49-0.50 of height). Fine-tune using the wrist crease as the measured reference.",
        "Why is the cane handle about 46% of height?",
        "Because the handle should be level with the greater trochanter of the femur (near the wrist crease), and the greater trochanter sits at about 46% of height. Too high causes shrugging, too low causes stooping, and both add load to the shoulder, neck and lower back.",
        "Can the axilla crutch height simply be multiplied by 0.77?",
        "0.77 x height is a common approximation, but you must still ensure an armpit rest about 5cm from the armpit, the handle level with the wrist crease, and elbow flexion of 20 to 30 degrees. Compressing the axillary neurovascular bundle is a contraindication; never sacrifice the gap just to hit the height.",
        "About Assistive Device Height",
        "Assistive Device Height is an online tool in the health and medical field.",
    ]))

    write('bp-trend', build('bp-trend', [
        "Blood Pressure and Glucose Trend",
        "Record daily blood pressure and glucose readings, automatically plot a fluctuation trend chart, data is stored in the local browser",
        "Records daily blood pressure and glucose readings, automatically plots a fluctuation trend chart, data is stored in the local browser, and performs a professional calculation based on the input parameters to output the result.",
        "View the Blood Pressure and Glucose Trend User Guide",
        "Record data",
        "Trend chart",
        "On waking",
        "Morning",
        "Afternoon",
        "Evening",
        "Systolic blood pressure SBP (mmHg)",
        "Diastolic blood pressure DBP (mmHg)",
        "Heart rate (beats/min, optional)",
        "Blood glucose (mmol/L, optional)",
        "Blood glucose measurement timing",
        "2 hours after a meal",
        "Indicators to view",
        "Blood pressure (systolic/diastolic)",
        "How many recent records",
        "Most recent 14",
        "Most recent 30",
        "Clear all records",
        "This tool is for daily self-recording and trend observation, and does not replace medical diagnosis. If blood pressure stays at or above 140/90 mmHg or fasting glucose stays at or above 7.0 mmol/L, seek medical attention promptly.",
        "In-Depth Analysis: Blood Pressure and Glucose Trend",
        "In home monitoring for older adults with hypertension, record systolic/diastolic pressure and heart rate by time and observe the trend and fluctuations.",
        "Used to show the doctor the change before and after medication at follow-up, assisting plan adjustment.",
        "Recording should be at a fixed measurement period (on waking, before sleep) to avoid misjudging from a single accidental value.",
        "Example: building a monitoring record",
        "Enter 'date-time-systolic-diastolic-heart rate' one by one in the tool to generate a line trend; focus on whether several consecutive days stay persistently high or fluctuate excessively.",
        "Example: organising for follow-up",
        "Take the last 7 to 14 days of data, mark the medication periods, and explain the 'morning peak' and 'nighttime' blood pressure changes to the doctor, which is more useful than a single clinic reading.",
        "How can home blood pressure measurement be more accurate?",
        "Sit quietly for 5 minutes, keep the cuff at heart level, measure twice at 1-2 minute intervals and take the mean; record at a fixed period (such as on waking before medication, or before sleep), and avoid measuring right after alcohol, coffee or exercise.",
        "Is the trend more important than a single value?",
        "Yes. An occasional high reading may be affected by mood or activity; only a persistently high reading at the same time over several consecutive days, or sharp fluctuations, carries more clinical meaning, and the recorded trend helps the doctor judge.",
        "About Blood Pressure and Glucose Trend",
        "Blood Pressure and Glucose Trend is an online tool in the health and medical field.",
        "e.g. 130",
        "e.g. 85",
        "e.g. 72",
        "e.g. 6.1",
    ]))

    write('eldercare-level', build('eldercare-level', [
        "Eldercare Nursing Level Quick Check",
        "Self-assess daily care ability to get a recommended care level (reference only).",
        "/ Eldercare Nursing Level Quick Check",
        "View the eldercare-level User Guide",
        "Total nursing level score = sum of the values of the selected options across all assessment items; 1 to 6 points is level 1 (mild, basic self-care ability intact), 7 to 9 points is level 2 (moderate, needs prompts for washing and eating plus short-term companionship), 10 points and above is level 3 (severe, needs high-frequency care with professional care staff intervening and a rehabilitation plan assessed).",
        "In-Depth Analysis: Eldercare Nursing Level Quick Check",
        "When self-checking the care level at home, assess the degree of dependence on 7 daily living abilities (feeding, washing, transfer, toileting, dressing, going out, medication).",
        "The total maps to level 1 (mild) through level 3 (severe), corresponding to different care intensities.",
        "The result is only a reference for home self-checking and does not replace a doctor's assessment or the national formal assessment standard.",
        "Worked example: all items self-sufficient (all scored 0)",
        "Total = 0 -> 'level 1 (mild)', basic daily self-care ability is intact, daily inspection is recommended.",
        "Worked example: several items need help (total 8 points)",
        "Total 7-9 -> 'level 2 (moderate)', needing part-time daily care (washing and eating prompts, short-term companionship); >=10 points escalates to level 3 (severe) high-frequency care.",
        "How are the care levels classified?",
        "Score each of the 7 abilities and sum: <7 level 1 (mild), 7-9 level 2 (moderate), >=10 level 3 (severe). The higher the score the stronger the dependence and the denser the care.",
        "Can home self-checking be used as a formal assessment?",
        "No. This tool is only for preliminary home judgement and communication; a formal long-term care level must be determined by professionals under the unified national standard (including medical and functional assessment).",
    ]))

    write('fall-risk', build('fall-risk', [
        "Fall Prevention Assessment",
        "Assess the fall risk level of older adults through a home environment and physical status questionnaire, and give improvement suggestions",
        "View the Fall Prevention Assessment User Guide",
        "I. Home environment assessment",
        "II. Physical and behavioural status",
        "Export the improvement list",
        "This assessment is a reference for home self-testing and does not replace a professional fall risk assessment (such as the Timed Up and Go test, TUG). Those at high risk are advised to contact a community health service centre or the rehabilitation department as soon as possible.",
        "In-Depth Analysis: Fall Prevention Assessment",
        "When assessing falls in older adults,",
        "two categories of factors are examined separately: environment (lighting, flooring, obstacles, bathroom) and body (balance, gait, medication, medical history).",
        "Structured interview plus physical examination scoring gives a low/medium/high risk level and indicates the intervention focus.",
        "High risk requires prioritising environmental renovation and fall prevention training, and screening for fall-causing drugs.",
        "Example: completing the environment and body assessment",
        "Answer the environment questions (indoor lighting / floor anti-slip / obstacles / bathroom safety) and the body questions (balance and gait / recent fall history / medication / chronic disease) item by item; the system aggregates the risk level and the rectification items.",
        "Example: handling high risk",
        "If many environment items are wrong and are combined with an unsteady gait or multiple medications, rate it high risk: immediately add bathroom grab bars, clear the walkway, review the antihypertensive and sedative drugs, and arrange balance training and follow-up.",
        "What does fall risk mainly depend on?",
        "Two categories: environment (poor lighting, slippery floor, clutter, bathroom without grab bars) and individual factors (declining muscle strength, unsteady gait, reduced vision and hearing, multiple medications, previous fall history). When the two stack up the risk rises sharply.",
        "Which drugs easily cause falls?",
        "Sedative-hypnotics, antipsychotics, certain antihypertensives and diuretics (causing orthostatic hypotension), hypoglycaemic drugs (causing low blood glucose), and so on. Stand up slowly after taking medicine, monitor dizziness, and ask the doctor to adjust if necessary.",
        "About Fall Prevention Assessment",
        "Fall Prevention Assessment is an online tool in the health and medical field.",
    ]))

    write('medication-schedule', build('medication-schedule', [
        "Medication Interval Reminder Table",
        "Enter the medication plan to generate a schedule, printable and exportable, assisting long-term reminders (generated locally, not uploaded).",
        "/ Medication Interval Reminder Table",
        "View the Medication Reminder Table User Guide",
        "The dosing interval is converted from the frequency: once a day is 24 hours, twice a day is 12 hours, three times a day is 8 hours, four times a day is 6 hours; dosing time point = first dose time + interval x n (n starting from 0); total times per day = 24 / interval; multiple medicines are merged and sorted on the timeline to generate an all-day medication reminder table.",
        "Number of observation days",
        "Dosage description per dose",
        "Add medicine",
        "Generate schedule",
        "In-Depth Analysis: Medication Reminder Table",
        "Older adults with multiple conditions often need many medicines; use a plan sheet to organise the name, dose, frequency and first dose time.",
        "Dose points are laid out on a 24-hour clock, avoiding missed or duplicated doses and flagging interactions.",
        "Complex plans should be checked with a doctor or pharmacist, especially anticoagulants, hypoglycaemic drugs and antihypertensives.",
        "Example: building a medication list",
        "Add 'name - dose - interval (hours) - first time' item by item, e.g. 'antihypertensive 1 tablet, interval 24, first 08:00'; the tool computes the following dose times from the interval and generates a daily table.",
        "Example: conflicts and reminders",
        "Overlay the dose points on a one-day timeline to discover whether several medicines clash at the same moment and need separating, or whether a fasting/after-meal requirement conflicts in a given period, so it can be confirmed with the pharmacist in advance.",
        "What to watch for when taking several medicines together?",
        "Focus on interactions and dosing timing (fasting / after meals), duplicated ingredients (for example several cold remedies containing the same ingredient), and the effect of liver and kidney function on the dose. Any change to the plan must go through a doctor or pharmacist.",
        "What if a dose is missed?",
        "Never double up on your own. In most cases follow the principle of 'take it as soon as you remember, and skip it if it is close to the next dose'; follow the package insert or consult the pharmacist to avoid overdosing.",
    ]))

    write('wheelchair-width', build('wheelchair-width', [
        "Wheelchair Passage Calculation",
        "Compute the minimum clear width of door openings and corridors and the turning space diameter from accessibility design standards, assisting home renovation",
        "View the Wheelchair Passage Calculation User Guide",
        "Passage calculation",
        "Standards quick reference",
        "Scenario type",
        "Door opening (room door / bathroom door)",
        "Corridor / walkway",
        "Turning space",
        "Wheelchair type",
        "Manual wheelchair",
        "Powered wheelchair",
        "Care wheelchair (wider)",
        "Usage mode",
        "Propelled by self",
        "Pushed with assistance",
        "Reference standards: General Code for Accessibility of Buildings and Municipal Engineering GB 55019-2021, GB 50763. The clear width of a door opening should not be less than 800mm, the clear width of a one-sided ramp corridor should not be less than 1200mm, and the turning space diameter should not be less than 1500mm.",
        "Door opening clear width",
        "Minimum clear width (mm)",
        "Room door",
        "The effective passage width after the door leaf is opened",
        "Bathroom door",
        "A sliding door or an outward-opening door is recommended",
        "Balcony door",
        "The threshold should not be higher than 15mm and should transition with a slope",
        "Corridor clear width",
        "One-sided ramp (wall on one side)",
        "Two-sided ramp (walls on both sides)",
        "A door within a corridor segment",
        "Turning space",
        "Wheelchair turning space diameter",
        "(circular)",
        "or use",
        "a square turning space",
        "A turning space must be left inside the bathroom for the wheelchair to turn",
        "Common wheelchair dimension reference",
        "Width (mm)",
        "Care wheelchair",
        "In-Depth Analysis: Wheelchair Passage Calculation",
        "In age-friendly renovation of homes and public spaces, the minimum clear width of door openings, corridors and turns must be calculated by wheelchair type.",
        "Manual, powered and care wheelchairs differ in width, and assisted pushing needs extra width for walking alongside.",
        "Door openings should be measured by the 'actual clear passage width with the door leaf fully open', not by the frame dimension.",
        "Worked example: manual wheelchair through a door opening (propelled by self)",
        "A manual wheelchair is about 680 mm wide; for the door opening scenario a minimum clear width of >= 800 mm is recommended (about 60mm operating margin on one side), and a sliding or outward-opening door is recommended to maximise the passage width.",
        "Worked example: corridor passage (pushed with assistance)",
        "The minimum clear width for self-propelled corridor travel is >= 1200 mm; if a carer needs to assist alongside, then >= 1500 mm; where there is a door or a turn, raising it to 1500 mm is likewise recommended. A powered wheelchair is about 700 mm wide and a care wheelchair about 740 mm, derived the same way.",
        "What width should a wheelchair passage be?",
        "Door opening >= 800 mm, corridor self-propelled >= 1200 mm, assisted alongside >= 1500 mm, turning space >= 1500 mm (common age-friendly figures, subject to the latest standard). The wheelchair body itself is 680-740 mm wide, and extra operating margin must be left.",
        "Why should a door opening be measured by the actual clear passage width?",
        "The frame dimension includes the door leaf thickness and hardware, so the truly passable width after the door opens is smaller; sliding or outward-opening doors significantly increase the effective clear width, hence the 'clear width when fully open' is the reference.",
        "About Wheelchair Passage Calculation",
        "Wheelchair Passage Calculation is an online tool in the health and medical field.",
    ]))

    write('index', build('index', [
        "Eldercare Nursing Tools",
        "Eldercare Nursing",
        "Eldercare Nursing Tools",
        "Compute the minimum clear width of door openings and corridors and the wheelchair turning space diameter from accessibility design standards, assisting home renovation",
        "Compute the suitable adjusted height from the user's height and the device type (crutch, walker, cane), helping older adults choose the right assistive device and improving safety of use.",
        "Assess the nursing level of older adults on dimensions such as the Barthel index (ADL), cognition and age, and output the level plus care plan key points, for reference in eldercare institution assessment.",
        "Assess eldercare service quality from 5 dimensions (1-5 points each) and output the total score (5-25) and improvement direction, for institution quality appraisal and continuous improvement.",
        "An online questionnaire for fall prevention risk assessment of older adults, scoring on an 8-item indoor environment checklist to identify home fall hazards and give renovation suggestions, suitable for care assessment, pure front-end.",
        "Assess the social work intervention need of older adults from 4 dimensions (0-3 points each) and link resources, outputting the need level, for planning community eldercare social work services.",
        "Medication Time and Interval Reminder Table",
        "Medication reminder table; adding multiple medicines automatically generates a daily medication schedule and a visual timeline, assisting older adults with chronic conditions in taking medicines regularly.",
        "Medication Interval Reminder Table",
        "Enter multiple medicines and dosing frequencies to automatically generate an all-day medication schedule, indicating the interval and precautions for each dose, helping older adults take medicines regularly and safely.",
        "Record daily blood pressure and glucose readings, automatically plot a fluctuation trend chart, data is stored in the local browser, making it easy for older adults and their families to track health changes over the long term.",
        "Assess the fall risk level of older adults through a home environment and physical status questionnaire, and give improvement suggestions such as home renovation and exercise, to prevent accidental falls.",
        "Eldercare Nursing Level Quick Check",
        "About Eldercare Nursing Tools",
        "The Eldercare Nursing Tools collection holds 11 free online tools covering the common calculation, conversion and lookup needs of eldercare nursing scenarios. Whether you are a practitioner, a student or an ordinary user, you can find practical ready-to-use tools here. All tools run entirely in the front end, data is not uploaded to the server, and privacy is protected.",
        "The eldercare nursing tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common eldercare nursing related tasks, with no need to memorise complex formulas or convert manually; enter and you get the result.",
        "Do the Eldercare Nursing Tools need a download or registration?",
        "No. All eldercare nursing tools on this page are pure front-end online tools; just open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the Eldercare Nursing Tools results accurate? Is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, and results are available instantly. All computation is done locally on your device, data is never uploaded to the server, and privacy is protected.",
    ]))


if __name__ == '__main__':
    main()
