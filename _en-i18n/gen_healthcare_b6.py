#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第6批：wells / map / healthcare-3"""
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


# ---------------- wells (20) ----------------
write('wells', build('wells', [
    "🫁 Wells Pulmonary Embolism Score",
    "Total the Wells criteria items for suspected pulmonary embolism and read the two-tier or three-tier probability band together with the suggested next diagnostic step.",
    '📖 View the "Wells Pulmonary Embolism Score User Guide"',
    "DVT signs and symptoms",
    "PE most likely diagnosis",
    "Heart rate >100",
    "Immobilisation or recent surgery",
    "Previous DVT/PE",
    "Total = sum of all item scores; ≤4 low probability, >4 high probability",
    "To be combined with D-dimer or imaging.",
    "📚 Deep Dive: Wells Pulmonary Embolism Score",
    "Emergency triage: use Wells to stratify the probability when PE is suspected",
    "Test decisions: combine with D-dimer to decide on imaging",
    "Follow-up: reassess as the course changes during treatment",
    "Algorithm (Wells PE): score = lower-limb DVT signs + previous DVT/PE + heart rate >100 + recent immobilisation/surgery + alternative diagnosis less likely + haemoptysis + malignancy, the sum of seven items; ≤1 low, 2-6 moderate, >6 high. Each item is 0/1 or 0/1.5/3 (this tool simplifies to 0/1).",
    "Example 1 (DVT signs, fast heart rate, immobilisation, alternative less likely, haemoptysis, malignancy — 1 each, 5 items): score 5, moderate probability. Example 2 (all 1): 7, high probability. Example 3 (all 0): 0, low.",
    "Does a high Wells score definitely mean PE?",
    "No, it is a probability stratification; even low probability can be PE, so combine with D-dimer (a negative result largely rules it out) and CT pulmonary angiography for confirmation.",
    "What is the difference between Wells and Geneva?",
    "Wells includes clinical judgement (alternative diagnosis), while Geneva uses purely clinical variables and is more objective; both are used for stratification, and the result must be combined with D-dimer and imaging.",
]))

# ---------------- map (20) ----------------
write('map', build('map', [
    "🩺 Mean Arterial Pressure Calculator",
    "Compute mean arterial pressure as diastolic plus one third of the pulse pressure, the value used to judge organ perfusion in shock and critical care monitoring.",
    '📖 View the "MAP Mean Arterial Pressure User Guide"',
    "MAP ≈ diastolic + (systolic − diastolic) / 3",
    "An important indicator of organ perfusion pressure.",
    "📚 Deep Dive: MAP Mean Arterial Pressure",
    "Organ perfusion: MAP reflects the average perfusion pressure of the heart, brain, kidneys and more",
    "Shock monitoring: MAP<65 often needs vasopressors to maintain perfusion",
    "Blood pressure management: read systolic/diastolic together for the whole picture",
    "Algorithm: MAP ≈ diastolic + (systolic−diastolic)/3; pulse pressure = systolic−diastolic; grading: MAP≥70 normal, 65-69 borderline, <65 low. Blood pressure must be >0.",
    "Example 1 (120/80): MAP = 80+(120−80)/3 = 93.3 mmHg, pulse pressure 40 mmHg, normal. Example 2 (100/60): MAP = 73.3 mmHg, normal. Example 3 (90/55): MAP = 66.7 mmHg, borderline.",
    "Is MAP more important than systolic pressure?",
    "MAP better represents average organ perfusion; anaesthesia and the ICU in particular watch whether MAP is ≥65. But very low systolic pressure also affects coronary perfusion, so judge the two together.",
    "Why divide by 3 and not 2?",
    "Diastole takes about 2/3 of the cardiac cycle, so 2/3 of the weight goes to diastolic pressure and 1/3 to pulse pressure, i.e. DBP+PP/3 — an empirical approximation.",
    "How to Use the MAP Mean Arterial Pressure Calculator",
    "What does the MAP Mean Arterial Pressure calculator do?",
    "MAP Mean Arterial Pressure calculator. Enter systolic and diastolic pressure to estimate MAP as MAP ≈ diastolic + (systolic−diastolic)/3, reflecting organ perfusion pressure, for circulatory monitoring reference.",
    "How do I use the MAP Mean Arterial Pressure calculator?",
    "What scenarios is the MAP Mean Arterial Pressure calculator best for?",
]))

# ---------------- healthcare-3 (19) ----------------
write('healthcare-3', build('healthcare-3', [
    "🏎️ Hyponatraemia Correction Rate Calculator",
    "Work out the safe sodium correction rate and the infusion rate needed to raise serum sodium without exceeding the daily limit that risks osmotic demyelination.",
    '📖 View the "Hyponatraemia Correction Rate User Guide"',
    "Infusate sodium concentration (mmol/L)",
    "Total body water (L)",
    "Target serum sodium (mmol/L)",
    "Current serum sodium (mmol/L)",
    "Change in serum sodium ≈ (infusate sodium − current serum sodium) / (total body water + 1)",
    "A teaching estimate only; clinical treatment must be individualised.",
    "📚 Deep Dive: Hyponatraemia Correction Rate Estimation",
    "Teaching demo: estimate the expected rise in serum sodium after sodium replacement",
    "Safety boundary: a reminder that the 24h rise in serum sodium should not exceed 8-10 mmol/L",
    "Risk awareness: correcting too fast can cause osmotic demyelination",
    "Algorithm (simplified teaching): expected rise = (infusate sodium − current serum sodium) ÷ (total body water + 1); target gap = target serum sodium − current serum sodium; with a 24h cap reminder (8-10 mmol/L). Teaching only; clinical use must be individualised.",
    "Example 1 (infusate sodium 154, total body water 42 L, target 130, current 118): expected rise (154−118)/(42+1) = 0.84 mmol/L, target gap 12.0 mmol/L. Example 2 (total body water 35 L, target 135, current 120): rise (154−120)/36 = 0.94 mmol/L, gap 15.0 mmol/L (a large gap calls for even slower correction).",
    "Why can't sodium be replaced too fast?",
    "Correcting serum sodium too fast (>8-10 mmol/L/24h) can trigger osmotic demyelination syndrome with severe disability; chronic hyponatraemia especially requires slow correction, often limited to 4-6 mmol/L/24h.",
    "Can this be used as a medical order?",
    "No, it is a teaching estimate; real sodium replacement must consider volume status (hypovolaemic/euvolemic/hypervolaemic), urine electrolytes and endocrine assessment, and be set by a doctor.",
]))
