#!/usr/bin/env python3
# gen_clinical_lab_head.py — shared head for clinical-lab batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'clinical-lab')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'clinical-lab')
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
    out = {'slug': slug, 'industry': 'clinical-lab', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('urine-sediment-atlas', build('urine-sediment-atlas', [
        "Urine Sediment Atlas",
        "Look up the morphology and clinical significance of formed elements in urine sediment: casts, crystals and cells.",
        "Urine Sediment Atlas",
        "/ Urine Sediment Atlas",
        'View "Urine Sediment (Casts/Crystals) Atlas User Guide"',
        "Provides an atlas-style comparison of the morphology and cues of urine-sediment formed elements (RBC/WBC/casts/crystals) to aid microscopy review.",
        "Urine Sediment Exam Essentials:",
        "Take 10 mL fresh urine, centrifuge (1500 rpm/5 min), keep 0.2 mL sediment for microscopy. Count casts under low power (x10) across 20 fields; count cells under high power (x40) across 10 fields. Casts are based on hyaline matrix; those containing cells/granules differ in meaning.",
        "📚 In-Depth: Urine Sediment (Casts/Crystals) Atlas",
        "Review RBC (uniform/dysmorphic) and WBC differentiation under sediment microscopy.",
        "Cast types (hyaline/granular/cellular/waxy) correspond to renal-parenchyma cues.",
        "Demonstrate crystal morphology differences (calcium oxalate/uric acid).",
        "Dysmorphic RBC Example",
        "Predominantly polymorphic/dysmorphic RBC suggests glomerular hematuria; uniform RBC tends toward non-glomerular origin. The tool lists key points side by side to aid judgment.",
        "Does seeing casts mean kidney disease?",
        "A few hyaline casts can appear physiologically; granular/cellular/waxy casts mostly suggest renal parenchymal lesions and need clinical correlation.",
        "Are all crystals harmful?",
        "Calcium oxalate etc. can appear physiologically; uric acid/cystine crystals relate to metabolism; persistent large amounts need evaluation.",
        "Can it replace the microscopy report?",
        "No; this tool is for morphology review, and the result should follow the laboratorian's microscopy.",
        "About the Urine Sediment Atlas",
        "A urine-sediment formed-element atlas. Compares RBC/WBC/cast/crystal morphology and cues to aid microscopy review; interpretation is confirmed by the laboratorian.",
        "Formed-Element Comparison",
        "Renal-Parenchyma Cue",
        "Crystal-Type Notes",
        "Sediment Microscopy Review",
        "Cast-Type Cue",
        "Crystal Demo Teaching",
        "e.g. cast, crystal, RBC",
    ]))
    write('vaginal-discharge-grading', build('vaginal-discharge-grading', [
        "Vaginal Discharge Grading",
        "Automatically grades vaginal cleanliness from microscopic epithelial cells/WBC/bacilli/cocci ratios.",
        "Vaginal Discharge Grading",
        "/ Vaginal Discharge Grading",
        'View "Vaginal Discharge (Microscopy) Grading User Guide"',
        "Grades vaginal discharge by Nugent or AV score to aid report understanding; diagnosis and medication are decided by the gynecologist.",
        "Bacilli (Lactobacillus)",
        "++++ (many)",
        "++ (moderate)",
        "+ (few)",
        "- (none)",
        "Cocci",
        "Epithelial Cells (HPF/HP)",
        "++++ (full field)",
        "++ (more)",
        "+ (few)",
        "WBC/Pus Cells (count/HP)",
        "Cleanliness Grading Standard",
        "Bacilli",
        "Epithelial Cells",
        "WBC (count/HP)",
        "Grade I",
        "Grade II",
        "Grade III",
        "suggests inflammation",
        "Grade IV",
        "severe inflammation",
        "Interpretation Principle:",
        "Grades I-II are normal (dominated by lactobacilli and epithelial cells); Grades III-IV suggest vaginitis (increased cocci and WBC, reduced lactobacilli). Combine with pH, amine test and clue cells to judge bacterial vaginosis (BV), trichomonas or fungal infection.",
        "📚 In-Depth: Vaginal Discharge (Microscopy) Grading",
        "Routine discharge is graded for bacterial vaginosis (BV) severity by clue cells/Nugent score.",
        "AV score helps understand aerobic vaginitis.",
        "Demonstrate the smear scoring standard.",
        "Nugent Score Example",
        "Few lactobacilli and many clue cells, Nugent 7-10 is BV-positive; 0-3 normal, 4-6 intermediate. The tool gives the grade and advises follow-up.",
        "Does a high score require medication?",
        "Treat if symptomatic or pregnant; asymptomatic intermediate types can be observed; specifics are decided by the gynecologist.",
        "Can douching cure it?",
        "Excessive douching may disrupt flora and worsen it; standard diagnosis and treatment are advised.",
        "Can it replace the gynecologic exam?",
        "No; the score is auxiliary; diagnosis combines symptoms, pH and microscopy and is judged by the physician.",
        "About the Vaginal Discharge Grading",
        "A vaginal-discharge grading tool. Computes the grade by Nugent/AV score to aid report understanding; diagnosis and medication are decided by the gynecologist.",
        "Nugent/AV Score",
        "Grade Calculation",
        "Routine Discharge Reading",
        "AV Score Understanding",
        "Scoring Demo Teaching",
    ]))

if __name__ == "__main__":
    main()
