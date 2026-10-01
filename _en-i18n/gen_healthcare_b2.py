#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第2批：checker-manager / heart-rate-zones"""
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


# ---------------- checker-manager (44) ----------------
write('checker-manager', build('checker-manager', [
    "⚖️ Management System Compliance Self-Check",
    "Score eight management system check items together with the recorded temperature and humidity, then read the total out of 80 as a percentage readiness grade.",
    "Quality (Management / System / Check) Mechanism",
    "/ Quality (Management / System / Check) Mechanism",
    '📖 View the "checker-manager User Guide"',
    "Total score = sum of the eight check scores (each 0-10, out of 80)",
    "Compliance rate (%) = total score ÷ 80 × 100, combined with the recorded temperature and humidity for an overall grade",
    "1. Quality management system and documents (1-10 points)",
    "2. Personnel and training management (1-10 points)",
    "3. Facilities and equipment management (1-10 points)",
    "4. Purchasing and acceptance management (1-10 points)",
    "5. Storage and maintenance management (1-10 points)",
    "6. Sales and after-sales service (1-10 points)",
    "7. Transport and distribution management (1-10 points)",
    "8. Computer information management (1-10 points)",
    "Cool storage room measured temperature (°C)",
    "Cool storage room measured humidity (%)",
    "Run GSP Check",
    "Finance (Cost / Profit / Statement) Analysis",
    'About the "Quality (Management / System / Check) Mechanism"',
    "A GSP pharmaceutical quality management compliance check tool that scores eight dimensions: quality system, personnel training, facilities and equipment, purchasing and acceptance, storage and maintenance, sales and after-sales, transport and distribution, and information management.",
    "Eight-dimension GSP compliance check",
    "Automatic temperature and humidity assessment",
    "GSP certification grade evaluation",
    "Inspection report generation",
    "GSP self-check for pharmaceutical retail enterprises",
    "Quality audit for pharmaceutical wholesale enterprises",
    "GSP inspection by drug regulatory authorities",
    "Quality management system review",
    "📚 Deep Dive: Management System Compliance Self-Check",
    "Internal audit prep: score each of the eight clauses to identify weak points in advance",
    "Pre-inspection self-check: enter the on-site temperature and humidity records together to output a rectification priority",
    "Monthly review: repeat the scoring with a fixed rubric and watch the compliance-rate trend",
    "Algorithm: enter each of the eight checks as 0-10 points, out of 80; compliance rate = total ÷ 80 × 100; then combine with the recorded temperature and humidity for an overall grade. Each value must be 0-10.",
    "Example 1 (all eight at 10 points): total 80, compliance rate 100.0%, meaning every clause is in place. Example 2 (all eight at 5 points): total 40, compliance rate 50.0%; the lowest-scoring clauses should be rectified first.",
    "How should the scoring criteria be set?",
    "Score by the sufficiency of evidence: 8-10 points when there is both a system and execution records, 4-7 with the system only, and 0-3 when both are missing; avoid giving every item the same score, which would remove any discrimination.",
    "Why are temperature and humidity included too?",
    "Storage and production environments have explicit temperature and humidity requirements, which are a fixed item in on-site inspections; listing it alongside the clause scores reminds you that an out-of-range environment is equally a non-conformity.",
    "GSP (Good Supply Practice for Pharmaceutical Products) is the statutory standard for pharmaceutical distribution",
    "Temperature and humidity must be recorded at least twice a day, with data retained for at least 5 years",
    "Prescription and non-prescription drugs must be displayed in separate zones, and specially controlled drugs kept under double lock with two people",
    "Near-expiry warning for drugs (6 months) with promotion or return/exchange",
    "The GSP certificate is valid for 5 years; apply for recertification 6 months before expiry",
]))

# ---------------- heart-rate-zones (38) ----------------
write('heart-rate-zones', build('heart-rate-zones', [
    "❤️ Heart Rate Training Zone Calculator",
    "Derive the five training zones from resting and maximum heart rate using the Karvonen method, and see the warm-up, aerobic, threshold and VO2 max bands.",
    "Heart Rate Zone Calculator",
    "/ Heart Rate Zone Calculator",
    "Max heart rate = 220 − age; heart rate reserve HRR = max heart rate − resting heart rate",
    "Max-HR zones Z1-Z5 start at max heart rate × 50%/60%/70%/80%/90%; Karvonen zones = resting heart rate + HRR × factor",
    "Heart Rate Reserve (HRR)",
    "Max Heart Rate Method",
    "Lactate Threshold Method",
    "Lactate threshold heart rate (bpm)",
    "Max heart rate (bpm)",
    "Max heart rate",
    "Heart rate reserve",
    "📊 Heart Rate Zone Visualization",
    "🎯 Five Zones in Detail",
    "🏃 Common Exercise Heart Rate Reference",
    "The ranges below are for a general adult; actual values vary from person to person",
    "Important:",
    "This calculator is for reference only and cannot replace the advice of a doctor or coach.",
    "• A medical check-up is advised before starting to exercise, especially for those with a history of cardiovascular disease",
    "• Stop immediately if chest pain, dizziness or breathing difficulty occurs during exercise",
    "• Training plans are best made under the guidance of a professional coach",
    "• If resting heart rate is persistently abnormal (above 100 or below 40), seek medical examination",
    "• Optimal fat-burning results require combining diet and regular exercise",
    "📚 Deep Dive: Heart Rate Training Zones (Karvonen Method)",
    "Exercise zones: estimate fat-burn / aerobic / target zones from heart rate reserve",
    "Intensity control: compute the target heart rate from the target intensity",
    "Individual variation: the formula is an estimate, affected by medication and fitness",
    "Algorithm (Karvonen):",
    "= 220 − age; fat-burn zone (60%) = (max − resting) × 0.6 + resting; target heart rate = (max − resting) × intensity + resting. Intensity 0-1.",
    "Example 1 (age 30, resting 70, intensity 0.7): max 190 bpm, fat-burn (190−70)×0.6+70 = 142 bpm, target (190−70)×0.7+70 = 154 bpm. Example 2 (age 40, resting 60, intensity 0.8): max 180, fat-burn 132, target 156 bpm.",
    "Is 220 − age accurate?",
    'It is a common estimate but individual variation is large (±10-12 bpm); for greater accuracy use "208 − 0.7 × age" or measure max heart rate directly with an exercise test.',
    "Why subtract the resting heart rate?",
    'The Karvonen method uses the "heart rate reserve" (max − resting) and adds it back to resting proportionally, which, compared with using max heart rate directly, ',
    "fits the individual better and avoids counting resting heart rate as part of the intensity.",
    'About the "Heart Rate Zone Calculator"',
    "Heart Rate Zone Calculator. A health-metric calculation tool based on authoritative medical standards; data is processed locally to protect privacy.",
]))
