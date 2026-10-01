#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 第3批：analysis-report-cost / weight-dosage / chads-vasc"""
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


# ---------------- analysis-report-cost (30) ----------------
write('analysis-report-cost', build('analysis-report-cost', [
    "Descriptive Statistics Report Calculator",
    "Paste a series of numbers and derive the count, sum, mean, median, minimum, maximum, range, variance and standard deviation in one report block.",
    "Finance (Cost / Profit / Report) Analysis",
    "/ Finance (Cost / Profit / Report) Analysis",
    '📖 View the "analysis-report-cost User Guide"',
    'Enter one "department,revenue,cost" line per row. Surplus = revenue − cost; cost ratio = cost ÷ revenue × 100%; surplus rate = surplus ÷ revenue × 100%. The summary gives the hospital-wide total revenue, total cost and total surplus, and identifies the department with the highest surplus and the number of loss-making departments.',
    'Department revenue and cost data (one "department,revenue,cost" per line)',
    "Internal Medicine,800000,650000\nSurgery,1000000,920000\nPediatrics,450000,500000",
    "Analyze Revenue and Cost",
    "📚 Deep Dive: Reading Department Revenue, Cost and Surplus",
    "The hospital finance department summarises each clinical and medical-technology department's revenue and cost every quarter and outputs the surplus and cost ratio, for department ",
    "and resource allocation.",
    "When reviewing operating costs, department heads use this tool to pinpoint loss-making departments and the highest-surplus department, and to find where the cost structure is out of balance.",
    "When testing the feasibility of a new department, quickly estimate the surplus rate from projected revenue and cost to judge whether the operating target is met.",
    "Quarterly revenue and cost trial for four departments",
    'Enter "Internal Medicine,1200000,980000; Surgery,1500000,1350000; Pediatrics,600000,720000; Laboratory,900000,540000": total revenue 4200000.00, total cost 3590000.00, surplus +610000.00, cost ratio 85.48%, surplus rate 14.52%; the Laboratory has the highest surplus and 1 department is loss-making (Pediatrics).',
    "What does a negative surplus rate mean?",
    "It means the department's revenue in the period cannot cover its cost, so it is running a deficit; the cost structure should be reviewed, or service pricing and volume adjusted.",
    "How high is a cost ratio considered high?",
    "The cost ratio of medical departments typically ranges from 75% to 95%; above 95% means the surplus margin is very thin. The exact threshold depends on the department type and the hospital's management basis.",
    "What are the data input format requirements?",
    'One "department,revenue,cost" per line; Chinese or English commas, spaces or tabs all work as separators, and the currency unit just needs to be consistent.',
    "Quality (Management / System / Check) Mechanism",
    'About the "Finance (Cost / Profit / Report) Analysis"',
    "Finance (Cost / Profit / Report) Analysis. A free online tool that runs purely in the front end, uploads no data and keeps your privacy safe.",
    "Monthly gross-margin structure analysis for stores",
    "Cost comparison across multiple stores / specifications",
    "Reconciling purchase-sales-inventory report data",
    "Data support for management meetings",
    "Internal Medicine,1200000,980000",
]))

# ---------------- weight-dosage (24) ----------------
write('weight-dosage', build('weight-dosage', [
    "⚖️ Weight Based Drug Dosage Calculator",
    "Convert a milligram per kilogram prescription into a total single dose and a daily total from body weight and dosing frequency, with the maximum limit checked.",
    '📖 View the "Weight-Based Drug Dosage User Guide"',
    "Daily dose = weight × mg/kg; single dose = daily dose / number of doses",
    "Always follow your doctor's instructions for the actual medication; this tool is for calculation only.",
    "📚 Deep Dive: Weight-Based Drug Dosage",
    "Pediatrics / dosage: compute the daily dose from mg/kg",
    "Divided doses: split the single dose by the number of doses per day",
    "Medication education: stress following medical advice and that this tool only calculates",
    "Algorithm: daily dose = weight (kg) × dosing strength (mg/kg); single dose = daily dose ÷ doses per day. Weight, strength and dose count must be >0. Always follow medical advice for the actual medication.",
    "Example 1 (weight 20 kg, 10 mg/kg, twice a day): daily dose 200 mg/day, single dose 100 mg. Example 2 (15 kg, 12 mg/kg, three times a day): 180 mg/day, 60 mg per dose.",
    "Where does mg/kg come from?",
    "It is given by the drug label or the physician's prescription (for example, cephalosporins dosed by weight); this tool only computes the amount from the strength you enter and does not serve as a recommended dose.",
    "Should I use actual or ideal body weight?",
    "Most dosing uses actual body weight, while some drugs for obese patients use adjusted body weight; it depends on the specific drug and guideline, and ",
    "pediatric dose",
    "also requires age / ",
    "body surface area",
    "combined.",
    "How to Use Weight-Based Drug Dosage",
    "What does Weight-Based Drug Dosage do?",
    "Weight-Based Drug Dosage calculator. Enter body weight and the mg/kg dosing strength to compute the daily dose, with a reminder that the actual medication must follow medical advice and this tool is for calculation only, as a reference for dose estimation.",
    "How do I use Weight-Based Drug Dosage?",
    "What scenarios is Weight-Based Drug Dosage best for?",
]))

# ---------------- chads-vasc (23) ----------------
write('chads-vasc', build('chads-vasc', [
    "📋 CHADS2-VASc Stroke Risk Score",
    "Total the congestive heart failure, hypertension, age, diabetes, stroke, vascular disease and sex items to obtain the annual stroke risk and anticoagulation hint.",
    '📖 View the "Atrial Fibrillation Stroke Risk CHADS2-VASc Score User Guide"',
    "Congestive heart failure 1=Yes",
    "Hypertension 1=Yes",
    "Age ≥75 1=Yes",
    "Diabetes 1=Yes",
    "Prior stroke/TIA 1=Yes",
    "Vascular disease 1=Yes",
    "Age 65-74 1=Yes",
    "Female 1=Yes",
    "C/H/A/D 1 point each; S (prior stroke/thromboembolism) 2 points; V / age 65-74 / female 1 point each",
    "A reference for anticoagulation decisions in atrial fibrillation.",
    "📚 Deep Dive: Atrial Fibrillation Stroke Risk CHADS2-VASc Score",
    "Anticoagulation decisions: use the risk-factor score to guide whether an AF patient should be anticoagulated",
    'Risk communication: turn "risk factors" into concrete points to ease doctor-patient discussion',
    "Follow-up reference: a rising score (e.g. new hypertension) signals the need for reassessment",
    "Algorithm: congestive heart failure 1 + hypertension 1 + age ≥75 scores 2 (65-74 scores 1) + diabetes 1 + stroke/TIA history 2 + vascular disease 1 + female 1; total 0 low risk, 1 low-moderate, 2 moderate, ≥3 high risk. Each item is 0 or 1 (age by band).",
    "Example 1 (hypertension only): score = 1 → low-moderate risk (weigh anticoagulation or aspirin). Example 2 (heart failure + hypertension + age ≥65 + female): score = 1+1+1+1 = 4 → high risk, anticoagulation is advised.",
    "What is this score used for?",
    "It is used to stratify stroke risk in patients with non-valvular atrial fibrillation and to guide whether to start oral anticoagulation; the higher the score, the greater the benefit. A doctor must decide together with the bleeding risk (e.g. HAS-BLED).",
    "Can I judge it myself?",
    "It cannot replace clinical judgement; bleeding risk, liver and kidney function and drug interactions all affect the decision, so medication must be started after assessment by a cardiovascular specialist.",
]))
