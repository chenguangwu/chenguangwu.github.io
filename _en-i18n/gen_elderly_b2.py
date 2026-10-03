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
    write('assessor-37', build('assessor-37', [
        "Quality (Standard/Assessment/Improvement) System",
        "Standard/assessment/improvement",
        "View the Quality (Standard/Assessment/Improvement) System User Guide",
        "Eldercare service quality score = service response + professional competence + service standardisation + satisfaction + safety management (1 to 5 points each); average = total / 5; an average of 4.5 or above is excellent, 3.5 to 4.4 is good, 2.5 to 3.4 is average, below 2.5 is fail; the improvement plan is made for the lowest scoring dimension.",
        "Eldercare service quality assessment system (5 dimensions, 1-5 points each, 5-25 total)",
        "1. Service response",
        "Extremely fast (5 points)",
        "Rather fast (4 points)",
        "Rather slow (2 points)",
        "Very slow (1 point)",
        "2. Professional competence",
        "3. Service standardisation",
        "Very standard (5 points)",
        "Rather standard (4 points)",
        "Not standard enough (2 points)",
        "4. Satisfaction",
        "In-Depth Analysis: Quality (Standard/Assessment/Improvement) System",
        "In the quality self-assessment of an eldercare institution, scores are given on five dimensions: service response, professional competence, service standardisation, satisfaction and safety management.",
        "The mean is used to determine excellent/good/average/fail and to locate the dimensions needing improvement.",
        "Quality improvement loop: keep the dimensions that pass, and put any dimension scoring <=2 into rectification.",
        "Worked example: all five dimensions scored 5",
        "Total quality score = 25 / 25, mean = 5.00 -> 'quality excellent'; recommended to summarise and promote the experience and keep the standard.",
        "Worked example: all five dimensions scored 3",
        "Total = 15, mean = 3.00 -> 'quality average'; an improvement plan is needed, with stronger training and process optimisation (the 2.5-3.5 mean band).",
        "How are the quality levels classified?",
        "By the mean of the five dimensions: >=4.5 excellent, >=3.5 good, >=2.5 average, <2.5 fail (25 in total, 0-5 per dimension). A fail requires immediate rectification and a re-check within a set deadline.",
        "Which low-scoring dimension should be fixed first?",
        "Safety management and service standardisation are usually directly related to accident risk, and a single dimension scoring <=2 triggers rectification; recommended to complete the safety rules and standard processes first, then improve competence and satisfaction.",
        "About Quality (Standard/Assessment/Improvement) System",
        "Quality (Standard/Assessment/Improvement) System.",
    ]))

    write('assessor-risk-1', build('assessor-risk-1', [
        "Fall Prevention Risk Assessment (indoor environment questionnaire)",
        "Indoor environment questionnaire",
        "View the Fall Prevention Risk Assessment (indoor environment questionnaire) User Guide",
        "Total home fall environment risk = indoor lighting + floor anti-slip + floor obstacles + carpets and mats + bathroom safety + furniture stability + stairs and steps + bed and chair height (0 to 3 points each, 24 in total); 3 points or below is low risk, 4 to 10 is medium risk, 11 and above is high risk; items with high scores are retrofitted one by one.",
        "Indoor environment fall prevention risk assessment for older adults (8-item checklist)",
        "1. Indoor lighting",
        "Ample and bright with no dark areas (0 points)",
        "Some areas are rather dark (2 points)",
        "Dim lighting (3 points)",
        "2. Floor anti-slip",
        "Good anti-slip (0 points)",
        "Partly slippery (2 points)",
        "Wet and slippery floor (3 points)",
        "3. Floor obstacles",
        "Walkways clear (0 points)",
        "A few clutter items (2 points)",
        "Clutter piled up / cables crossing (3 points)",
        "4. Carpets and mats",
        "Fixed flat / no carpet (0 points)",
        "Edges lifted (2 points)",
        "Loose and sliding (3 points)",
        "5. Bathroom safety",
        "Has grab bars and anti-slip mat (0 points)",
        "Has grab bars or anti-slip mat (2 points)",
        "No safety facilities (3 points)",
        "6. Furniture stability",
        "Stable and reliable (0 points)",
        "Some items unstable (2 points)",
        "Many unstable / casters without locks (3 points)",
        "7. Stairs and steps",
        "Has grab bars and good lighting / no stairs (0 points)",
        "Incomplete grab bars / insufficient lighting (2 points)",
        "No grab bars / damaged (3 points)",
        "8. Bed height / seat height",
        "Suitable height (0 points)",
        "A little high or low (2 points)",
        "Too high / too low (3 points)",
        "Assess fall risk",
        "In-Depth Analysis: Fall Prevention Risk Assessment (indoor environment questionnaire)",
        "Before age-friendly home renovation, fall risk is assessed on 8 environmental elements to locate the points needing rectification.",
        "Lighting, floor anti-slip, obstacles, bathroom, furniture and stairs are scored item by item, and the total sets the risk level.",
        "Key items (>=2) automatically generate rectification suggestions (such as adding grab bars and laying anti-slip mats).",
        "Worked example: all 8 items pass (scored 0)",
        "Environment risk score = 0 / 24 -> 'low risk'; keeping the existing safety measures is enough.",
        "Worked example: several items have problems (total 16)",
        "Total = 16 > 10 -> 'high risk'; immediate renovation is needed (such as adding bathroom grab bars, floor anti-slip and clearing walkways), and professional on-site assessment is recommended.",
        "How many levels of fall risk are there?",
        "Sum the 8 environmental items (24 in total): <=3 low, <=10 medium, >10 high. High risk requires immediate age-friendly renovation and consideration of a professional assessment.",
        "Which rectifications give the best value?",
        "Bathroom grab bars and anti-slip mats, clearing walkway clutter, and night lighting are low-cost high-benefit priorities; adding grab bars and step lights at stairs and level changes significantly reduces the probability of fall injury.",
        "About Fall Prevention Risk Assessment (indoor environment questionnaire)",
        "Fall Prevention Risk Assessment (indoor environment questionnaire).",
    ]))

    write('reminder-time', build('reminder-time', [
        "Medication Time and Interval Reminder Table",
        "Add multiple medicines, automatically generating a daily medication schedule and a visual timeline",
        "View the Medication Time and Interval Reminder Table User Guide",
        "Dosage",
        "How to take",
        "Fixed time every day",
        "Every X hours",
        "Before meals",
        "After meals",
        "Medication times (multiple selection)",
        "Interval hours",
        "Meal selection",
        "Breakfast",
        "Lunch",
        "Dinner",
        "Add medicine",
        "Print medication table",
        "Schedule",
        "Timeline",
        "Medicine list",
        "The timeline shows one slot every 2 hours, and the coloured blocks represent the medicines to be taken in that period.",
        "This tool is only for assisting in generating a medication schedule; it does not replace medical advice",
        "Take medicines strictly following the doctor's prescription and the package insert",
        "Before meals generally means 30 minutes before the meal, after meals generally means 30 minutes after the meal",
        "Data is stored locally in the browser, clearing the cache will lose it, printing a backup is recommended",
        "If you have questions about drug interactions, please consult a doctor or pharmacist",
        "In-Depth Analysis: Medication Time and Interval Reminder Table",
        "Set reminders for medication, blood pressure measurement and follow-up visits for older adults with cognitive decline or living alone, reducing omissions and accidents.",
        "Reminder times are generated from the frequency (daily / every other day / weekly) and the first time.",
        "Reminders should be paired with simultaneous notification to family, and key items should keep a manual fallback.",
        "Example: setting a daily reminder",
        "Choose 'daily, first at 08:00, 2 times in total'; the tool generates 08:00 and the next dose time, and the full-day schedule can be viewed in the calendar/list view.",
        "Example: weekly follow-up reminder",
        "Choose 'follow-up every Monday at 09:30', which generates a recurring reminder; share it with the family side to avoid the older adult forgetting and missing doses or follow-ups.",
        "Can reminders fully replace human care?",
        "No. Reminders are an aid; for those with clear cognitive decline, family or a carer still has to confirm execution as a fallback, and key medication and follow-ups deserve double reminders.",
        "How to choose a reasonable frequency?",
        "Set it strictly by the prescribed frequency (e.g. qd/bid/tid corresponds to 1/2/3 times per day); any change must go through medical advice; do not merge dose times on your own for convenience.",
        "About Medication Time and Interval Reminder Table",
        "Designed for people who need to take multiple medicines, supporting the addition of multiple medicines with different dosing frequencies (fixed daily time, interval dosing, before or after meals), automatically generating a daily medication schedule and a visual timeline.",
        "Multiple dosing frequency settings",
        "Automatic daily schedule generation",
        "24-hour visual timeline",
        "Print friendly format",
        "Local storage management",
        "Multiple medication management for older adults",
        "Daily medication arrangement for chronic conditions",
        "Family care medication reminders",
        "Medication records during hospital stays",
        "e.g. Aspirin enteric-coated tablets",
        "e.g. 100mg/1 tablet",
        "e.g. half an hour after meals",
    ]))


if __name__ == '__main__':
    main()
