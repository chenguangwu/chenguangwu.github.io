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
    write('assessor-35', build('assessor-35', [
        "Nursing Care (Level/Assessment/Plan) Formulation",
        "Level/assessment/plan",
        "View the Nursing Care (Level/Assessment/Plan) Formulation User Guide",
        "Barthel index = feeding + bathing + grooming + dressing + bowel control + bladder control + toileting + bed-chair transfer + walking on level ground + stairs, 10 items totalling 0 to 100 points; 80 points or above with normal cognition is level 4 self-care, 60 to 79 is level 3 mild dependence, 40 to 59 is level 2 moderate dependence, below 40 is level 1 severe dependence.",
        "Nursing level assessment for older adults (based on the Barthel index ADL plus cognition and age)",
        "Barthel index (activities of daily living, 0-100 points)",
        "Feeding",
        "Independent (10 points)",
        "Needs partial help (5 points)",
        "Fully dependent (0 points)",
        "Bathing",
        "Independent (5 points)",
        "Needs help (0 points)",
        "Grooming",
        "Dressing",
        "Bowel control",
        "Controllable (10 points)",
        "Occasional loss of control (5 points)",
        "Incontinence (0 points)",
        "Bladder control",
        "Toileting",
        "Bed-chair transfer",
        "Independent (15 points)",
        "Needs a small amount of help (10 points)",
        "Needs a great deal of help (5 points)",
        "Walking on level ground",
        "Walks independently (15 points)",
        "Needs assistance (10 points)",
        "Wheelchair independent (5 points)",
        "Unable (0 points)",
        "Stairs",
        "Needs help (5 points)",
        "Cognitive status",
        "Cognition normal",
        "Mild cognitive decline",
        "Moderate dementia",
        "Severe dementia",
        "Rate the nursing level",
        "In-Depth Analysis: Nursing Care (Level/Assessment/Plan) Formulation",
        "In long-term care level rating, the Barthel index (10 ADL items) combined with cognitive status classifies the person from self-care to severe dependence.",
        "Communities and institutions use this to match visit frequency, care intensity and rehabilitation plans.",
        "The higher the score the more self-sufficient life is; cognitive decline adds to the dependence level, so a combined judgement is needed.",
        "Worked example: Barthel=85, cognition normal(cog=0)",
        "Barthel>=80 and cognition normal -> 'Level 4 (self-care)', recommended 1 visit per week plus health guidance and social activities.",
        "Worked example: Barthel=50, mild cognitive decline(cog=1)",
        "Barthel>=40 and <60 -> 'Level 2 (moderate dependence)', needs daily visits, help with daily life and rehabilitation training; if cognition>=2, add the cognitive impairment note.",
        "How is the Barthel index scored 0-100?",
        "The 10 ADL items (feeding, bathing, grooming, dressing, bowel and bladder control, toileting, bed-chair transfer, walking, stairs, etc.) are scored by degree of independence and summed, for a full score of about 100. The higher the score the more self-sufficient, and it is a dependence scale commonly used at home and abroad.",
        "How does cognitive status affect the level?",
        "This tool overlays cognition (cog) on top of the Barthel: a high score with normal cognition is rated self-care; cognitive decline raises the dependence level and adjusts the care plan (such as stronger anti-wandering measures and medication reminders).",
        "About Nursing Care (Level/Assessment/Plan) Formulation",
        "Nursing Care (Level/Assessment/Plan) Formulation.",
    ]))

    write('assessor-36', build('assessor-36', [
        "Social Work (Intervention/Assessment/Resource) Linkage",
        "Intervention/assessment/resource",
        "View the Social Work (Intervention/Assessment/Resource) Linkage User Guide",
        "Total social work intervention need = economic security + health care + psychological support + social support (0 to 3 points each, 12 in total); 3 points or below is low need, 4 to 7 is medium need, 8 and above is high need; the dimension with the lowest score is prioritised for linking community resources such as the subsistence allowance application, family doctor contracting or psychological counselling.",
        "Social work intervention need assessment and resource linkage for older adults (4 dimensions, 0-3 points each)",
        "1. Economic security need",
        "Financially comfortable (0 points)",
        "Basically sufficient (1 point)",
        "Rather difficult (2 points)",
        "Severely difficult (3 points)",
        "2. Health care need",
        "Healthy and self-sufficient (0 points)",
        "Needs occasional medical visits (1 point)",
        "Needs regular care (2 points)",
        "Needs continuous medical care (3 points)",
        "3. Psychological support need",
        "Psychologically well (0 points)",
        "Occasionally lonely (1 point)",
        "Clearly depressed or anxious (2 points)",
        "Severe psychological problem (3 points)",
        "4. Social support need",
        "Support network complete (0 points)",
        "Support average (1 point)",
        "Support weak (2 points)",
        "Completely isolated (3 points)",
        "Assess the intervention plan",
        "In-Depth Analysis: Social Work (Intervention/Assessment/Resource) Linkage",
        "In home-based eldercare, the intervention need is assessed on four dimensions: economic security, health care, psychological support and social support.",
        "A result of low/medium/high need maps to different follow-up frequencies and resource linkage strategies.",
        "Key dimensions (score>=2) automatically generate a resource linkage list (such as long-term care insurance and day care).",
        "Worked example: all four items scored 0 (good condition)",
        "Total intervention need = 0 / 12 -> 'low need'; regular follow-up and keeping community contact is enough.",
        "Worked example: all four items scored 2 (key intervention)",
        "Total = 8 > 7 -> 'high need'; immediately start case management, multi-disciplinary collaboration and weekly follow-up, and link the four corresponding resources (subsistence allowance / family doctor / psychological hotline / day care, etc.).",
        "How many levels of intervention need are there?",
        "This tool sums the four dimensions (12 in total): <=3 low need, <=7 medium need, >7 high need. High need requires immediate case management and linkage to multiple resources.",
        "What is a key intervention dimension?",
        "A single dimension score>=2 counts as a key intervention, and the tool pushes the matching resource for that dimension (such as health care -> long-term care insurance application, social support -> volunteer pairing), for precise assistance.",
        "About Social Work (Intervention/Assessment/Resource) Linkage",
        "Social Work (Intervention/Assessment/Resource) Linkage.",
    ]))


if __name__ == '__main__':
    main()
