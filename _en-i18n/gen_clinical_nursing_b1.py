#!/usr/bin/env python3
# gen_clinical_nursing_head.py — shared head for clinical-nursing batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'clinical-nursing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'clinical-nursing')
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
    out = {'slug': slug, 'industry': 'clinical-nursing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('assessor-pressure-risk', build('assessor-pressure-risk', [
        "Surgical Position (Pressure Point) Risk Assessment",
        "Pressure Points",
        'View "Surgical Position (Pressure Point) Risk Assessment User Guide"',
        "This tool scores surgical-position pressure-point risk item by item per a clinical nursing assessment scale; for reference only, not a substitute for bedside professional assessment.",
        "Surgical Position",
        "Trendelenburg (head-down) position",
        "Estimated surgery duration (hours)",
        "Patient BMI",
        "Diabetes",
        "Edema",
        "Fecal/urinary incontinence",
        "General anesthesia",
        "Hypotension",
        "Assess pressure-point risk",
        "📚 In-Depth: Surgical Position (Pressure Point) Risk Assessment",
        "Before prone or lateral-position surgery under general anesthesia, preliminarily assess pressure-redness and ischemia risk from pressure-point distribution to decide silicone-pad and heel-offloading plans.",
        "For prolonged fixed-position surgeries (spine, anorectal, etc.), flag high-risk bony prominences by duration segments and remind intraoperative timed pressure relief.",
        "For obese or hypoproteinemic patients, combine",
        "with nutritional status to raise the risk level and shorten relief intervals.",
        "Review a laparoscopic lateral-position risk case",
        "Input BMI 28, estimated 120 min, lateral pressure points at the greater trochanter and auricle; the tool flags high risk and suggests relief every 30 min, consistent with the actual nursing record.",
        "Can this tool replace the OR pressure-injury",
        "chart?",
        "No; it only gives a preliminary pressure-point cue. Formal records still follow the hospital pressure-injury scale (e.g. Braden) and the intraoperative nursing sheet.",
        "What if results differ from actual redness?",
        "Defer to bedside observation; tool results are reference thresholds. On obvious pallor or flushing, relieve pressure immediately and extend observation.",
        "How to score pediatric or very thin patients?",
        "Adjust children by age- and weight-based percentiles; very thin patients show more prominent bony points and should be up-graded one level, with specialist-nurse consultation if needed.",
        "About the Surgical Position (Pressure Point) Risk Assessment",
        "Assesses sacral/heel bony-prominence pressure risk after positioning, aiding the circulating nurse in planning relief and padding.",
        "Pressure-Point Risk Grading",
        "Duration-Segment Flagging",
        "BMI/Nutrition-Linked Rating",
        "Pre-op Prone/Lateral Preliminary",
        "Intra-op Relief Reminder",
        "Obese/Hypoproteinemic Up-Risk",
    ]))
    write('assessor-rater-risk', build('assessor-rater-risk', [
        "Fall Risk (Morse Score) Assessment",
        "Morse Score",
        'View "Fall Risk (Morse Score) Assessment User Guide"',
        "This tool scores fall risk item by item per the Morse Fall Scale; for reference only, subject to the nurse's bedside assessment and signature.",
        "Morse Fall Risk Scale (6 items, total 125)",
        "1. Fall history (last 3 months)",
        "Yes (15 pts)",
        "2. Medical diagnoses (>=2)",
        "3. Ambulatory aid",
        "None/wheelchair/nurse assist (0 pts)",
        "Cane/walker/prosthesis (15 pts)",
        "Furniture-hopping gait (30 pts)",
        "4. IV infusion/heparin lock",
        "Yes (20 pts)",
        "5. Gait/mobility",
        "Normal/bedridden/immobile (0 pts)",
        "Weak (10 pts)",
        "Impaired (20 pts)",
        "6. Mental status",
        "Aware of own limits (0 pts)",
        "Overestimates/forgets limits (15 pts)",
        "📚 In-Depth: Fall Risk (Morse Score) Assessment",
        "Complete the Morse score within 24 h for new admissions or transfers; >=45 is high-risk and warrants a",
        "fall-prevention",
        "label.",
        "Reassess before postoperative ambulation; those with IV infusion or analgesia pump still in place auto-count for the IV-therapy item.",
        "Reassess after sedatives/hypnotics or antihypertensives; raise risk promptly when gait or cognition changes.",
        "Review a post-orthopedic Morse score case",
        "A patient with 1 prior fall, walker use, indwelling-needle infusion and assisted gait totals 55 across six items, rated high-risk, matching the ward assessment sheet.",
        "Can this tool replace the hospital Morse sheet?",
        "No; it only checks dimensions and demonstrates training. Formal scoring follows the nurse's bedside sheet and signature.",
        "How to handle a score near the cutoff (e.g. 44/45)?",
        "Manage as high-risk (round up), and defer to actual gait and cognition observation.",
        "Does it apply to children or ICU patients?",
        "Morse mainly fits adult inpatients; for children and ICU use dedicated scales such as Schmid or Humphreys.",
        "About the Fall Risk (Morse Score) Assessment",
        "Quantifies inpatient fall risk across six Morse dimensions to aid tiered supervision and fall-prevention management.",
        "Six-Dimension Scoring",
        "Auto Risk Stratification (low/mid/high)",
        "High-Risk Flag Hint",
        "Assess Within 24h of Admission",
        "Reassess Before Post-op Ambulation",
        "Reassess After Sedative/Antihypertensive",
    ]))
    write('bag-valve-mask', build('bag-valve-mask', [
        "Bag Valve Mask (Ventilation Rate) Setter",
        "Computes bag-valve-mask (BVM) ventilation rate, tidal volume and squeeze rhythm by scenario and patient age, with a metronome guide.",
        "Bag-Valve-Mask Ventilation Rate Setter",
        "/ BVM Setting",
        'View "Bag-Valve-Mask (Ventilation Rate) Setter User Guide"',
        "Rates by scenario and age: adult 10-12/min (fixed 10/min during CPR), child 12-20/min, infant 20-30/min; tidal volume about 6-7 mL/kg or 1/2-1/3 bag squeeze; squeeze:relax 1:1 to 1:2, each squeeze about 1 s.",
        "CPR",
        "Emergency ventilation",
        "Transport ventilation",
        "Apnea",
        "Child (1-8 yr)",
        "Infant (<1 yr)",
        "Adult (1500 mL)",
        "Child (800 mL)",
        "Infant (240 mL)",
        "/min",
        "CPR adult rate: 8-10/min",
        "Tidal volume (mL)",
        "Squeeze per press (s)",
        "Interval (s)",
        "Compression:ventilation ratio",
        "Compression metronome (click the button below to start/stop)",
        "▶ Start metronome",
        "Copy ventilation params",
        "BVM ventilation reference:",
        "CPR (after advanced airway):",
        "Adult 8-10/min, child 12-20/min",
        "Emergency ventilation:",
        "Adult 10-12/min (1 breath every 5-6 s)",
        "Transport ventilation:",
        "Adult 10-12/min, child 15-30/min",
        "Tidal volume:",
        "Adult 400-600 mL (1/2-2/3 bag), child 6-8 mL/kg",
        "Key steps:",
        "EC-clamp the mask, head-tilt/chin-lift to open the airway, squeeze about 1 s each time, watch chest rise to confirm effective ventilation.",
        "Note: avoid hyperventilation! It raises intrathoracic pressure, reduces venous return and lowers cardiac output. During CPR, compressions and ventilation must not run together.",
        "📚 In-Depth: Bag-Valve-Mask (Ventilation Rate) Setter",
        "For adult cardiac-arrest CPR, set BVM ventilation 10-12/min at a 30:2 ratio, avoiding hyperventilation.",
        "For infant respiratory arrest, 12-20/min with small tidal volume (chest just rising), gentle squeeze to prevent gastric distension.",
        "For those with spontaneous rhythm but hypoventilation, adjust assisted",
        "rate by SpO2 and",
        "respiratory rate.",
        "Review adult CPR BVM rate",
        "Input patient=adult, cycle 30:2; the tool gives 10-12/min and 1/3 bag per squeeze, consistent with AHA guidance.",
        "Can this tool replace the physician's rescue orders?",
        "No; it only checks parameters. Actual ventilation follows the rescue team lead and chest-rise observation.",
        "What if gastric distension is obvious after squeezing?",
        "Lower tidal volume to just chest rise, lift the jaw to open the airway, and place an oropharyngeal airway if needed.",
        "How to adjust with an oxygen source?",
        "Connect a reservoir bag to raise FiO2 near 100%; rate unchanged, still avoid hyperventilation.",
        "About the Bag-Valve-Mask Ventilation Rate Setter",
        "Sets BVM artificial-ventilation rate and tidal-volume reference by age to aid CPR parameter checks.",
        "Age-Based Rate Range",
        "Gentle Tidal-Volume Hint",
        "30:2 Ratio Fit",
        "Adult CPR 10-12/min",
        "Infant Small Tidal to Avoid Distension",
        "Spontaneous-Rhythm Assist",
    ]))
    write('barthel-index', build('barthel-index', [
        "Barthel Index (ADL) Grader",
        "The Barthel Index assesses activities of daily living (ADL) across 10 items (0-100); higher scores mean greater independence. Click options to auto-score.",
        "Barthel Index (ADL) Grader",
        "/ Barthel ADL Index",
        'View "Barthel Index (ADL) Grader User Guide"',
        "This health tool estimates from common physiological constants and empirical formulas; for reference only, not a substitute for professional medical diagnosis. Tool: Barthel Index (ADL) Grader.",
        "Fully independent",
        "Patient is fully independent in daily life, needing no help",
        "Barthel Index grading:",
        "100: fully independent -> completes all ADL independently",
        "75-95: mild deficit -> mostly independent, little help",
        "50-70: moderate deficit -> needs substantial help for ADL",
        "25-45: severe deficit -> most ADL need assistance",
        "0-20: fully dependent -> all ADL rely on others",
        "📚 In-Depth: Barthel Index (ADL) Grader",
        "Reassess every two weeks in stroke rehab; compare index changes to judge recovery and discharge readiness.",
        "Orthopedic post-op patients score low on transfer and walking; arrange walkers and supervision accordingly.",
        "For long-term care insurance or care-level applications, grade by total 0-100 (<=40 is severe dependency).",
        "Review a stroke patient Barthel score",
        "Patient: feeding 5, bathing 0, transfer 10, walking 10; ten items total 45, moderate dependency, matching rehab assessment.",
        "Can this tool replace the rehab assessment report?",
        "No; it only checks items. Formal assessment is by the therapist with overall clinical judgment.",
        "How to score cognitively impaired patients?",
        "Score by actual completion; items needing full assistance count 0, avoid overestimation.",
        "What does large score fluctuation mean?",
        "It suggests unstable function or varying timing; reassess at fixed times by the same rater for comparison.",
        "About the Barthel Index (ADL) Grader",
        "Quantifies self-care by ten Barthel ADL items to aid rehab progress and care-level decisions.",
        "Ten-Item Scoring",
        "Total 0-100",
        "Dependency Grading",
        "Stroke Rehab Biweekly Reassess",
        "Orthopedic Post-op Transfer/Walk",
        "Long-Term Care Application",
        "Is this tool free?",
        "Completely free, no registration; use directly in the browser.",
    ]))
    write('braden-score', build('braden-score', [
        "Braden Score (Pressure-Injury Risk) Calculator",
        "The Braden Scale assesses pressure-injury risk across 6 dimensions (6-23); lower scores mean higher risk. Click dimension options to auto-score.",
        "Braden Score (Pressure-Injury Risk) Calculator",
        "/ Braden Pressure-Injury Score",
        'View "Braden Score (Pressure-Injury Risk) Calculator User Guide"',
        "This tool scores and stratifies per the Braden nursing scale item by item; for reference only, subject to the nurse's bedside assessment and signature.",
        "Patient low pressure-injury risk; maintain routine care",
        "Braden score reference:",
        "15-18: mild risk -> turn q4h, protect skin",
        "13-14: moderate risk -> turn q2h, use pressure-reduction mattress",
        "10-12: high risk -> turn q2h, air mattress, local relief",
        "<=9: very high risk -> turn q1h, air mattress, nutritional support",
        "📚 In-Depth: Braden Score (Pressure-Injury Risk) Calculator",
        "Score bedridden or ICU patients within 24 h; <=18 triggers turning q2h and a pressure-reduction mattress.",
        "Post-op immobilized or incontinent patients drop on moisture and activity; reassess dynamically to adjust care level.",
        "Those with abnormal nutrition screening: raise risk by serum albumin and intake, consult nutrition.",
        "Review a bedridden elder Braden score",
        "Sensation 3, moisture 2, activity 1, mobility 2, nutrition 2, friction 2, total 12, very high risk, matching ward assessment.",
        "Can this tool replace the pressure-injury sheet?",
        "No; it only checks dimensions. Formal scoring follows the nurse's bedside Braden scale and signature.",
        "How to handle a borderline 18?",
        "18 is the high-risk cutoff; manage as high-risk with closer observation, per clinical reality.",
        "Continue scoring after a stage-1 redness?",
        "Yes; after injury keep scoring to monitor progression and report, while starting local relief and skin care.",
        "About the Braden Score (Pressure-Injury Risk) Calculator",
        "Identifies pressure-injury risk by six Braden dimensions to guide turning frequency and mattress use.",
        "Six-Dimension Scoring",
        "Risk Stratification (<=18 high)",
        "Dynamic Reassess Reminder",
        "Bedridden/ICU Assess Within 24h",
        "Incontinent/Immobile Reassess",
        "Nutrition-Abnormal Up-Risk",
    ]))

if __name__ == "__main__":
    main()
