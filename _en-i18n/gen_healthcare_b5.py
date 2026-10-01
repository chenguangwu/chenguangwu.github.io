#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第5批：nrs2002 / healthcare / apgar"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'healthcare')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'healthcare')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or '')[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'healthcare', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- nrs2002 (21) ----------------
write('nrs2002', build('nrs2002', [
    "🥗 NRS 2002 Nutritional Risk Screening",
    "Screen nutritional risk with the NRS 2002 tool by combining the impaired nutritional status score, disease severity score and the age adjustment.",
    '📖 View the "Nutrition Risk NRS2002 User Guide"',
    "Weight loss in the past 3 months",
    "Reduced food intake",
    "Disease severity 0-3",
    "Age ≥70",
    "Total = impaired nutrition (0-3) + disease severity (0-3) + age ≥70 (1)",
    "≥3 indicates nutritional risk",
    "To be combined with a clinical nutritional assessment.",
    "📚 Deep Dive: Nutrition Risk NRS2002",
    "Nutrition screening: screen inpatients for nutritional risk to decide whether nutritional support is needed",
    "Intervention decisions: a score ≥3 suggests nutritional intervention",
    "Follow-up: reassess when the condition changes",
    "Algorithm (NRS 2002): impaired-nutrition score = ",
    "item + weight-loss item + food-intake item; total = impaired nutrition + disease severity + age (add 1 for ≥70); a total ≥3 means nutritional risk. Each item is scored 0-3 per the scale.",
    "Example 1 (impaired nutrition 1+1+1, disease 2, age 1): total 6, nutritional risk present. Example 2 (all 0): 0 points, no nutritional risk.",
    "What is the difference between NRS 2002 and MUST?",
    "NRS 2002 is widely used in Europe and includes disease severity and age, suiting inpatients; MUST is British and leans toward community/screening use. In China, NRS 2002 is the more commonly recommended tool for inpatients.",
    "Does a score ≥3 always require nutritional support?",
    "It indicates that nutritional intervention is needed, but the doctor/nutrition department decides based on contraindications and goals; those with severe metabolic derangement may have it deferred.",
]))

# ---------------- healthcare (21) ----------------
write('healthcare', build('healthcare', [
    "👶 Paediatric Dose Conversion Calculator",
    "Convert an adult dose to a child dose by weight or by body surface area, with Clark's rule, Young's rule and the BSA method compared side by side.",
    '📖 View the "Paediatric Dose Conversion User Guide"',
    "Adult dose (mg)",
    "Child weight (kg)",
    "Reference adult weight (kg)",
    "Maximum multiple limit",
    "Child dose = adult dose × (child weight / adult weight)",
    "Actual medication must follow medical advice; do not decide on your own.",
    "📚 Deep Dive: Converting Child Dose by Weight",
    "Paediatric conversion: estimate the child dose from the adult dose by the weight ratio",
    "Cap protection: take the smaller of the weight-based dose and the multiple cap",
    "Medication education: stress following medical advice and not deciding on your own",
    "Algorithm: weight-based dose = adult dose × (child weight ÷ reference adult weight); capped dose = min(weight-based dose, adult dose × multiple cap); dose ratio = child weight ÷ adult weight × 100%. All values must be >0.",
    "Example 1 (adult 500 mg, child 20 kg, reference adult 70 kg, cap 2×): weight-based = 500×20/70 = 142.86 mg, capped = min(142.86, 1000) = 142.86 mg, ratio 28.57%. Example 2 (adult 300 mg, child 15 kg, adult 60 kg, cap 1.5×): weight-based = 300×15/60 = 75.00 mg, capped = min(75, 450) = 75.00 mg, ratio 25.00%.",
    "Is the weight-based method accurate?",
    "The weight-based method (such as Clark's rule) is a rough estimate that does not take into account ",
    "body surface area",
    "and organ maturity; precise paediatric dosing mostly uses the body-surface-area (BSA) method, and must be determined by a doctor per the label and guidelines.",
    "What is the multiple cap for?",
    'It prevents a single-dose overdose: the smaller of the weight-based estimate and "adult dose × multiple" is taken as the safety cap; the drug label and physician\'s prescription still govern.',
]))

# ---------------- apgar (21) ----------------
write('apgar', build('apgar', [
    "📋 Apgar Score Calculator",
    "Score appearance, pulse, grimace, activity and respiration at one and five minutes after birth, and read the summed result with its clinical interpretation band.",
    '📖 View the "Apgar Score User Guide"',
    "Skin colour 0-2",
    "Heart rate 0-2",
    "Reflex 0-2",
    "Muscle tone 0-2",
    "Respiration 0-2",
    "Apgar = skin colour + heart rate + reflex + muscle tone + respiration",
    "Each item 0-2 points",
    "A quick neonatal asphyxia assessment tool.",
    "📚 Deep Dive: Neonatal Apgar Score",
    "Delivery-room assessment: score the five items at 1 and 5 minutes after birth to quickly judge the degree of asphyxia",
    "Resuscitation decisions: a low score indicates the need to clear the airway, give oxygen or provide positive-pressure ventilation",
    "Trend observation: a rise at 5 minutes over 1 minute suggests effective resuscitation",
    "Algorithm: score heart rate, respiration, muscle tone, reflex and skin colour 0-2 each, total 0-10; total ≥7 normal, 4-6 mild asphyxia, 0-3 severe asphyxia. Each of the five items is 0-2.",
    "Example 1 (all five at 2): total 10 → normal. Example 2 (heart rate 0, skin colour 0, the rest 1 each): total = 0+1+1+1+0 = 3 → severe asphyxia, requiring immediate resuscitation.",
    "What is the difference between 1 minute and 5 minutes?",
    "The 1-minute score reflects the immediate condition after birth and guides immediate resuscitation; the 5-minute score shows the response to resuscitation and the trend, and if it is still low, assessment continues and extends to 10 minutes.",
    "Does a low score always mean a poor prognosis?",
    "Not necessarily; it is affected by labour medication, prematurity and more. It should be judged together with blood gases, fetal heart rate and neurological assessment — the score is only a quick screening tool.",
]))
