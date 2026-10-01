#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""materials 第1批：detector-40 / detector-strength-color-diff / detector-35 / brinell-hardness / analysis-cost-profit-2"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'materials')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'materials')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or it.get('zh_src', ''))[:50]))
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
    out = {'slug': slug, 'industry': 'materials', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- detector-40 (42) ----------------
write('detector-40', build('detector-40', [
    "\u2696\uFE0F Quality (Standard/Testing/Environmental) Certification",
    "Input coating VOC, formaldehyde, heavy metals and other metrics; judge the coating eco-grade per GB 18582.",
    "Quality (Standard/Testing/Environmental) Certification",
    "/ Quality (Standard/Testing/Environmental) Certification",
    '\U0001F4D6 View the "detector-40 User Guide"',
    "Per GB 18582 and GB/T 23994: interior water-based coating VOC <= 80 g/L, free formaldehyde <= 50 mg/kg, total aromatics <= 100 mg/kg, soluble lead <= 90 mg/kg; exterior and solvent-based coatings have stricter limits (VOC often <= 120 g/L); any metric exceeding the limit fails that item and the whole product; pass rate = passed items / tested items x 100%, all items must pass for an eco-grade pass, otherwise rectify or replace.",
    "Coating type",
    "Interior coating",
    "Exterior coating",
    "Wood coating",
    "Waterproof coating",
    "Formaldehyde content (mg/kg)",
    "Total aromatics (mg/kg)",
    "Lead Pb (mg/kg)",
    "Hiding power (g/m2)",
    "\U0001F4DA Deep Dive: Coating Eco-grade Judgment",
    "Check the limit metrics on the coating test report before material selection.",
    "Check whether interior coatings can reach the Green Ten-ring level.",
    "Compare eco performance of multiple candidate coatings in batch.",
    "Interior coating reaches first-class eco-grade",
    'Coating type "Interior Coating", VOC 50 g/L, formaldehyde 30 mg/kg, aromatics 50 mg/kg, lead 20 mg/kg. Interior limits: VOC 120, formaldehyde 100, aromatics 300, lead 90, all four pass; and since VOC 50 is within 30-80, it is judged first-class eco-grade, standard GB 18582.',
    "VOC exceeding limit fails",
    'Coating type "Wood Coating", VOC 400 g/L, other metrics pass. Wood coating VOC limit is 300 g/L, 400 exceeds it, judged directly unqualified, prompting "some metrics exceed limits, not for interior use".',
    "How are eco-grades classified?",
    "First require VOC, formaldehyde, aromatics and lead all to meet their limits. All pass and VOC<=30 g/L -> premium eco-grade (Green Ten-ring); all pass and VOC<=80 g/L -> first-class; only all pass -> qualified; any over limit -> unqualified.",
    "Why do VOC limits differ by coating type?",
    "Coatings for different uses have different formulations and application needs, and national standards give different limits: interior GB 18582 VOC<=120 g/L, exterior GB/T 9755 and waterproof GB/T 19250 200 g/L, wood GB 18581 300 g/L. Choosing the right type is the premise of judgment.",
    "Interior per GB 18582, exterior per GB/T 9755, wood per GB 18581",
    "VOC is the core eco metric; Green Ten-ring certification requires VOC<=30 g/L",
    "Heavy-metal lead limit <=90 mg/kg; pay special attention in children rooms",
    "Lower hiding-power value means better coverage",
    "Ventilate 7-14 days after application before occupancy",
    "Quality (Color-difference/Strength/Standard) Inspection",
    'About "Quality (Standard/Testing/Environmental) Certification"',
    "Coating eco-quality test tool; input VOC, formaldehyde, aromatics, heavy metals and other metrics, judge the coating eco-grade per GB standards.",
    "Four coating standards selectable",
    "Five harmful-substance tests",
    "Green Ten-ring grade judgment",
    "Hiding-power performance evaluation",
    "Coating factory inspection",
    "Interior decoration material selection",
    "Coating quality spot check",
]))

# ---------------- detector-strength-color-diff (41) ----------------
write('detector-strength-color-diff', build('detector-strength-color-diff', [
    "\U0001F3A8 Quality (Color-difference/Strength/Standard) Inspection",
    "Input stone color difference (Delta E), compressive strength, flexural degree and other parameters; judge the stone quality grade per GB/T 9966.",
    "Quality (Color-difference/Strength/Standard) Inspection",
    "/ Quality (Color-difference/Strength/Standard) Inspection",
    '\U0001F4D6 View the "detector-strength-color-diff User Guide"',
    "This tool, per GB/T 9966 and GB/T 18601, automatically judges the natural-stone quality grade (premium/first-class/qualified/unqualified) from input color difference Delta E, compressive strength, flexural strength, bulk density and water absorption, and switches the corresponding standard limits by stone type (granite/marble/limestone/sandstone). Logic: four strengths and physical-chemical metrics all pass and Delta E<=1.0 -> premium; all pass and Delta E<=2.0 -> first-class; at least 3 pass and Delta E<=4.0 -> qualified; else unqualified. Judgment and calculation run locally in the browser; data is not uploaded.",
    "Stone type",
    "Granite",
    "Marble",
    "Limestone",
    "Sandstone",
    "Color difference Delta E",
    "Flexural strength (MPa)",
    "Bulk density (g/cm3)",
    "\U0001F4DA Deep Dive: Natural Stone Quality Test and Judgment",
    "Judge grade by color difference and physical-chemical metrics on stone arrival.",
    "Compare quality stability across quarries or batches.",
    "Pick slabs that meet appearance requirements (Delta E) for decoration projects.",
    "Granite judged premium",
    'Stone type "Granite", color difference Delta E=3.5, compressive 120 MPa, flexural 8.5 MPa, bulk density 2.65, water absorption 0.35%. Granite limits: compressive 100, flexural 8, density 2.56, absorption <=0.60, all four pass; but Delta E=3.5 is neither <=1.0 nor <=2.0, so check passed count: all four pass and Delta E<=4.0, thus judged qualified.',
    "Marble density insufficient",
    'Stone type "Marble", color difference Delta E=1.5, compressive 60 MPa, flexural 7.5 MPa, bulk density 2.30, water absorption 40%. Marble limit density 2.40, measured 2.30 fails, only 3 pass, still meets "passed>=3 and Delta E<=4.0", judged qualified.',
    "How are the four grades judged specifically?",
    "Four strengths and physical-chemical metrics all pass and Delta E<=1.0 -> premium; all pass and Delta E<=2.0 -> first-class; passed>=3 and Delta E<=4.0 -> qualified; else unqualified. Color difference Delta E strongly affects high grades; control Delta E first when appearance matters.",
    "Why do limits differ so much across stones?",
    "Because lithology differs. Granite is strictest (compressive 100 MPa, absorption <=0.60%), marble 50 MPa / <=0.50%, limestone 60 MPa / <=3.00%, sandstone 70 MPa / <=3.00%. After choosing stone type the tool auto-applies the matching limits.",
    "Natural stone testing follows the GB/T 9966 series (Test Methods for Natural Facing Stone)",
    "Granite compressive >=100 MPa, marble >=50 MPa; flexural >=8 and >=7 MPa respectively",
    "Color difference Delta E<=1.0 premium, <=2.0 first-class, <=4.0 qualified",
    "Water absorption reflects stone density; granite <=0.60%, marble <=0.50%",
    "Outdoor stone should also test freeze-thaw and abrasion resistance",
    "Quality (Standard/Testing/Environmental) Certification",
    'About "Quality (Color-difference/Strength/Standard) Inspection"',
    "Natural-stone quality test tool; input color difference Delta E, compressive strength, flexural strength, bulk density, water absorption and other parameters, judge the stone quality grade per GB/T 9966.",
    "Comprehensive rating of five metrics",
    "Supports granite/marble/limestone/sandstone",
    "Automatic Delta E grading",
    "Stone quality acceptance",
    "Building decoration material selection",
    "Stone import/export inspection",
    "Curtain-wall stone testing",
]))

# ---------------- detector-35 (40) ----------------
write('detector-35', build('detector-35', [
    "\u2696\uFE0F Quality (Testing/Standard/Traceability) System",
    "Input key building-material performance metrics; judge the quality grade per GB/T standards and generate a traceable test report.",
    "/ Quality (Testing/Standard/Traceability) System",
    '\U0001F4D6 View the "detector-35 User Guide"',
    "This tool, per GB/T 175 (general cement), GB/T 50081 (concrete), GB/T 5101 (fired brick), GB/T 11968 (block) and others, automatically judges the quality grade (premium/first-class/qualified/unqualified) from input compressive and flexural strengths, and generates a traceable test report with batch number. Judgment and calculation run locally in the browser; data is not uploaded.",
    "Building-material type",
    "General cement",
    "Fired brick",
    "Block",
    "Batch number",
    "Flexural strength (MPa)",
    "Copy traceable report",
    "\U0001F4DA Deep Dive: Cement and Concrete Quality-grade Judgment",
    "On arrival acceptance, for cement,",
    "do a quick grade judgment per batch.",
    "Compare whether different batches meet the relevant national-standard requirements.",
    "Generate test records with batch numbers for quality traceability.",
    "Concrete C30 judgment",
    'Material type "Concrete", batch BM-2026-001, compressive 42.5 MPa, flexural 7.5 MPa. Concrete limits: compressive 30.0, flexural 4.0, both pass; and since 42.5 >= 30.0x1.3=39.0, judged premium, standard GB/T 50081.',
    "Fired brick strength insufficient",
    'Material type "Fired brick", compressive 12.0 MPa, flexural 3.2 MPa. Fired-brick limits: compressive 15.0, flexural 3.0, flexural passes but compressive 12.0 < 15.0 fails, judged unqualified directly, prompting rectification.',
    "How is premium grade derived?",
    "First require both compressive and flexural to meet limits (qualified); on that basis, premium only if compressive reaches >=1.3x the limit; only both qualified -> first-class. Limits differ by material: general cement 32.5/5.0, concrete 30.0/4.0, fired brick 15.0/3.0, block 5.0/1.0 MPa.",
    "Why does the applied standard change with material type?",
    "Different building materials have their own national standards: general cement GB/T 175, concrete GB/T 50081, fired brick GB/T 5101, block GB/T 11968. After selecting the material type the tool auto-switches to the matching standard and limits, avoiding misjudgment from wrong-standard application.",
    "General cement per GB/T 175, concrete per GB/T 50081, fired brick per GB/T 5101",
    "Compressive strength is the core metric; test after 28 days of standard curing",
    "Traceability system should record: raw-material source, production parameters, test data, batch number",
    "Unqualified products should be isolated and labeled, not used in works",
    "Recommend an electronic traceability system for full-process quality tracking",
    'About "Quality (Testing/Standard/Traceability) System"',
    "Building-material quality test and traceability tool; input compressive and flexural strengths and other metrics, judge the quality grade per GB/T standards and generate a traceable report with batch number.",
    "Four building-material types selectable",
    "Automatic judgment per GB/T national standards",
    "Batch traceability number management",
    "Generate complete test report",
    "Building-material factory inspection",
    "Site material acceptance",
    "Quality traceability management",
    "Building-material manufacturer QC",
]))

# ---------------- brinell-hardness (28) ----------------
write('brinell-hardness', build('brinell-hardness', [
    "Brinell Hardness from Indentation Load and Diameter",
    "Input load F, indenter diameter D and indentation diameter d to find Brinell hardness.",
    "Brinell Hardness Calculator",
    "/ Brinell Hardness Calculator",
    '\U0001F4D6 View the "Brinell Hardness from Indentation Load and Diameter User Guide"',
    "F=3000N, D=10, d=4.2mm -> about 202 BHN.",
    "Load F (N)",
    "Indenter diameter D (mm)",
    "Indentation diameter d (mm)",
    "Just keep units consistent (mm/N).",
    "\U0001F4DA Deep Dive: Brinell Hardness HB",
    "Indentation method for material hardness",
    "Metal/casting quality check",
    "Rough strength conversion",
    "Hardness testing",
    "HB = 2F / (pi*D*(D - sqrt(D^2 - d^2))), F load, D indenter dia, d indentation dia. Large indentation represents volume-averaged hardness, suited to coarse-grained materials.",
    "Versus tensile",
    "Empirically HB~3*UTS (steel), a rough strength estimate only, not rigorous.",
    "Suited to soft-medium metals (e.g. annealed steel, cast iron); too-hard materials deform the indenter and give small, imprecise indentations.",
    "How does Brinell differ from Rockwell/Vickers?",
    "Brinell large indentation suits coarse homogeneous grains; Rockwell is quick for field; Vickers small indentation, universal across the whole hardness range (diamond pyramid).",
    "Can hardness stand in for strength?",
    "Same-series materials have empirical conversion (e.g. steel HB~3*UTS), but cross-material is unreliable; only a quick estimate.",
    "How to Use Brinell Hardness from Indentation Load and Diameter",
    "What does Brinell Hardness from Indentation Load and Diameter do?",
    "Input test load F, indenter diameter D and indentation diameter d; compute the Brinell hardness value as BHN = 2F / [pi*D*(D - sqrt(D^2 - d^2))], used for metal hardness testing.",
    "How do I use Brinell Hardness from Indentation Load and Diameter?",
    "Which scenarios suit Brinell Hardness from Indentation Load and Diameter?",
]))

# ---------------- analysis-cost-profit-2 (33) ----------------
write('analysis-cost-profit-2', build('analysis-cost-profit-2', [
    "\U0001F4C8 Financial (Cost/Profit/Cash-flow) Analysis",
    "Cost/profit/cash flow",
    "/ Financial (Cost/Profit/Cash-flow) Analysis",
    '\U0001F4D6 View the "analysis-cost-profit-2 User Guide"',
    "Sales revenue = unit price x volume; variable cost = unit variable cost x volume; contribution margin = revenue - variable cost; EBIT = contribution margin - fixed cost; net profit = EBIT x (1 - tax rate); break-even volume = fixed cost / (unit price - unit variable cost); break-even amount = break-even volume x unit price; safety margin rate = (volume - break-even volume) / volume.",
    "Unit selling price (CNY/unit)",
    "Sales volume (units)",
    "Unit variable cost (CNY/unit)",
    "Fixed cost (CNY)",
    "Income tax rate (%)",
    "\U0001F4DA Deep Dive: Building-material Cost-Profit and Break-even Analysis (CVP)",
    "Building-material traders estimate sales revenue, gross profit and net profit from unit price, volume, unit variable cost and fixed expense.",
    "Given the income tax rate, estimate after-tax net profit and",
    ", assisting quotation and profit-target setting.",
    "Use break-even volume/amount and safety margin rate to judge how far current volume is from",
    "break-even",
    ".",
    "Example: tile distribution",
    "Unit price 100 CNY, volume 300 units, unit variable cost 60 CNY, fixed cost 10000 CNY, tax rate 20%: revenue 30000 CNY, variable cost 18000 CNY,",
    "contribution margin",
    "12000 CNY, EBIT 2000 CNY, tax 400 CNY, net profit 1600 CNY, net margin 5.33%, break-even volume 250 units, break-even amount 25000 CNY, safety margin rate 16.67%.",
    "What is the contribution margin?",
    "Contribution margin = sales revenue - variable cost; it is the part of each unit sold that first covers variable cost and then replenishes fixed cost and forms profit; the gap of unit price over unit variable cost (unit margin) times volume is total contribution margin.",
    "Why does break-even volume use (unit price - unit variable cost) as denominator?",
    "Fixed cost can only be offset step by step by unit contribution (unit price - unit variable cost), so break-even volume = fixed cost / unit margin; when unit price <= unit variable cost it can never break even, and the tool prompts to fix parameters first.",
    "Quality (Testing/Standard/Traceability) System",
    'About "Financial (Cost/Profit/Cash-flow) Analysis"',
    "Financial (Cost/Profit/Cash-flow) Analysis. A free online tool, pure front-end processing, data not uploaded, protecting privacy and security.",
    "Free to use, no registration or login",
    "Supports Simplified / Traditional / English interfaces",
    "Material purchase-price summary: batch-input purchase prices or totals of a batch of building materials (cement/rebar/sand etc.) to quickly get average price, max-min spread (range) and dispersion, assisting supplier price comparison and bidding verification.",
    "Multi-supplier quote dispersion: statistically analyze multiple quotes for the same-spec material, use standard deviation to judge whether quotes are concentrated or scattered; larger deviation means more obvious price differences, warranting close checks of anomalous high or low quotes.",
    "Budget-execution deviation analysis: batch-input the deviation of each item actual spend vs budget, compute mean and standard deviation, judge the overall budget-execution fluctuation, and identify items with concentrated overspending.",
]))
