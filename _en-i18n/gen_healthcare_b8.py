#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第8批：healthcare-2 / parkland / healthcare-4 / qtc"""
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


# ---------------- healthcare-2 (18) ----------------
write('healthcare-2', build('healthcare-2', [
    "🧮 IV Drip Rate Calculator",
    "Convert a prescribed infusion volume and duration into drops per minute and millilitres per hour for a given drop factor, with a rounded practical setting suggested.",
    '📖 View the "IV Drip Rate Calculation User Guide"',
    "Total volume (mL)",
    "Time (minutes)",
    "Drop factor (drops/mL)",
    "Drip rate (drops/min) = total volume × drop factor / time (min)",
    "Clinical use requires adjustment according to the patient's condition.",
    "📚 Deep Dive: IV Drip Rate Calculation",
    "Clinical rate setting: compute the drip rate and seconds per drop from volume and time",
    "Nursing execution: set the giving set and roller clamp by the drop factor",
    "Safety check: too fast or too slow both affect efficacy and safety",
    "Algorithm: total drops = volume (mL) × drop factor (gtt/mL); drip rate = total drops ÷ time (min); seconds per drop = 60 ÷ drip rate. All values must be >0. Common drop factors are 15/20 gtt/mL.",
    "Example 1 (500 mL / 120 min / drop factor 20): total drops 500×20 = 10000, drip rate 10000/120 = 83.3 drops/min, about 0.72 s/drop. Example 2 (1000 mL / 240 min / drop factor 15): total drops 15000, drip rate 62.5 drops/min, about 0.96 s/drop.",
    "How is the drop factor determined?",
    "It is set by the giving-set specification (commonly 15 or 20 gtt/mL, different for precision sets); the drip rate is calculated with the factor of the set in use, and set according to the label or nursing standards.",
    "The drip rate is calculated but needs slowing down?",
    "Cardiac and renal patients often need a slower rate; the calculated value is the theoretical drip rate matching the prescribed time, and the actual rate must be adjusted to the patient's tolerance and the order, with regular checks.",
]))

# ---------------- parkland (18) ----------------
write('parkland', build('parkland', [
    "🩺 Parkland Burn Fluid Resuscitation Calculator",
    "Compute the Parkland formula fluid volume for the first 24 hours from body weight and burn percentage, and split it into the first 8 hours and the remaining 16.",
    '📖 View the "Parkland Burn Fluid Resuscitation User Guide"',
    "Burn area (%)",
    "Elapsed infusion time (h)",
    "24h Ringer's lactate = 4 mL × weight (kg) × burn area (%)",
    "Half in the first 8h, half in the following 16h",
    "An estimation formula; the actual amount must be adjusted by urine output and more.",
    "📚 Deep Dive: Parkland Burn Fluid Resuscitation",
    "Burn resuscitation: draft the 24h fluid plan after an adult burn",
    "First-aid reference: estimate fluid volume on scene or during transfer",
    "Monitoring adjustment: adjust the rate in real time by urine output and more",
    "Algorithm (Parkland): 24h total = 4 × weight (kg) × burn area TBSA (%) mL; infuse half in the first 8h and the other half in the following 16h; amount due at a given time = total × elapsed hours / 24. Weight and area must be >0.",
    "Example 1 (70 kg, TBSA 30%): 24h = 4×70×30 = 8400 mL, first 8h = 4200 mL, following 16h = 4200 mL; if 8 hours have passed since injury, the amount due is 8400×8/24 = 2800 mL. Example 2 (60 kg, 40%): 24h = 9600 mL.",
    "How to calculate for children / inhalation injury?",
    "Children use the modified Brooke or a more refined weight-based formula, and inhalation injury often needs more; Parkland is only a preliminary adult estimate and must be adjusted per the burns-unit protocol and urine output (adults ≥0.5 mL/kg/h).",
    "Why split into the first 8h and the following 16h?",
    "Capillary leak is greatest in the first 8h after injury, so half is given quickly to restore blood volume; in the following 16h the leak eases and the rest is given evenly to avoid pulmonary oedema.",
]))

# ---------------- healthcare-4 (18) ----------------
write('healthcare-4', build('healthcare-4', [
    "📋 NYHA Heart Function Classifier",
    "Grade cardiac function from I to IV by the degree of activity limitation and symptom pattern, following the New York Heart Association functional classification.",
    '📖 View the "NYHA Heart Function Classification User Guide"',
    "Shortness of breath on daily activity 0-3",
    "Symptoms at rest 0=none 1=yes",
    "Marked activity limitation 0=none 1=yes",
    "NYHA class I-IV graded by symptoms and degree of activity limitation",
    "For assessing the severity of heart failure.",
    "📚 Deep Dive: NYHA Heart Function Classification",
    "Heart-failure assessment: grade I-IV by exercise tolerance",
    "Exercise guidance: the higher the class, the more the intensity must be limited",
    "Follow-up records: a change in class reflects the disease course",
    "Algorithm (simplified): symptoms at rest → class IV; mild limitation of daily activity → class II; marked limitation → class III; no symptoms → class I. Judged by breathlessness after activity, whether there are symptoms at rest and the degree of limitation.",
    "Example 1 (breathlessness after activity, not at rest, no clear limitation): class II (mild limitation, slightly breathless on daily activity). Example 2 (symptoms at rest): class IV (breathless even at rest, the most severe).",
    "Is NYHA the same as heart-failure staging?",
    "No: NYHA is a symptom classification (I-IV), whereas the ACC/AHA stage is a disease course (A-D); NYHA reflects the current functional status and can change with treatment.",
    "Can I grade it myself?",
    "For understanding only; the exact class is determined by a doctor using exercise testing and ejection fraction together — do not self-diagnose.",
]))

# ---------------- qtc (17) ----------------
write('qtc', build('qtc', [
    "❤️ Corrected QT Interval Calculator",
    "Correct the QT interval for heart rate with the Bazett, Fridericia, Framingham and Hodges formulas, and flag the prolongation thresholds for each method.",
    '📖 View the "QTc Corrected Heart Rate User Guide"',
    "QT interval (ms)",
    "Heart rate (bpm)",
    "Formula 1=Bazett 2=Fridericia",
    "QTc prolongation is linked to the risk of arrhythmia.",
    "📚 Deep Dive: QTc Corrected Heart Rate",
    "Drug monitoring: antiarrhythmics / antibiotics / psychotropics can prolong QT",
    "ECG interpretation: QTc prolongation signals arrhythmia risk",
    "Follow-up: repeat the ECG to see the trend",
    "Algorithm: QTc Bazett = QT / √(RR), RR = 60 / heart rate (s); QTc Fridericia = QT / ∛(RR); normal upper limit 440 ms for men and 450 ms for women, ≥500 ms high risk. QT and heart rate must be >0.",
    "Example 1 (QT 400 ms, HR 75, male): RR = 0.8, Bazett = 400/√0.8 = 447.2 ms, Fridericia = 400/∛0.8 = 430.9 ms, above the male limit of 440 — needs attention. Example 2 (QT 360, HR 60, female): Bazett = 360 ms, normal (female limit 450).",
    "Which is better, Bazett or Fridericia?",
    "Bazett deviates more at fast or slow heart rates, while Fridericia is steadier. Clinically Bazett is used most, with Fridericia and heart-rate correction to confirm abnormal values.",
    "What to do about QTc prolongation?",
    "Check for culprit drugs (the CredibleMeds list is a useful reference), electrolyte disturbances (low potassium and magnesium) and congenital heart disease; ≥500 ms or symptomatic cases need the drug stopped and medical attention, which this tool cannot determine.",
]))
