#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第1批：area-12 / assessor-67 / calc-51 / chemical-peel"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'cosmetic-derm')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'cosmetic-derm')

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
    out = {'slug': slug, 'industry': 'cosmetic-derm', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- area-12 (34) ----------------
write('area-12', build('area-12', [
    "📐 Telangiectasia Area Assessment",
    "Enter the facial region and erythema area ratio to assess the severity of telangiectasia (broken capillaries).",
    '📖 View the "Telangiectasia Area Assessment User Guide"',
    "Severity is graded by erythema area ratio; vessel diameter is classified by μm.",
    "Area-ratio grading: <5% mild (telangiectasia grade I), 5-15% moderate (II), 15-30% severe (III), ≥30% very severe (IV); the ratio is capped at 100%. Vessel-diameter classification: <0.2 μm fine vessels (capillary dilation), <1 μm medium vessels (venule dilation), ≥1 μm coarse vessels (venous dilation). Used to assess facial telangiectasia severity and support treatment decisions.",
    "Facial region",
    "Full face",
    "Erythema area ratio (%)",
    "Vessel diameter (μm, optional)",
    "💡 Erythema area ratio <5% is mild, 5-15% moderate, 15-30% severe, >30% very severe telangiectasia.",
    "Press",
    "quick assess,",
    "Copy result",
    "Results are for reference only; actual diagnosis and treatment should be made by a qualified physician.",
    "📚 Deep Dive: Telangiectasia Area Assessment",
    "Rosacea follow-up: periodically estimate erythema capillary area to observe regression trends after medication or laser/light therapy.",
    "Pre-procedure communication: use the area ratio to illustrate the scope of telangiectasia intuitively, helping set treatment zones for pulsed-dye laser.",
    "Home monitoring: compare monthly photos taken from the same angle to self-assess whether telangiectasia is spreading.",
    "Nasal ala telangiectasia estimate",
    "Input: two patches of erythema on the sides of the nose cover about 8% of the cheek area → graded as mild diffuse type; avoid hot/spicy triggers and keep records; if needed, pulsed-dye laser in divided sessions.",
    "Can area replace a doctor's diagnosis of rosacea?",
    "No. Area only quantifies extent; whether papules or burning accompany it requires a physician to judge with the medical history.",
    "How should photos be taken to be comparable?",
    "Fixed distance, natural light, no makeup, same angle; preferably the same phone with the same white balance.",
    "Is the estimation error large?",
    "Manual grid method has about ±10% error; use only as a trend reference, never for precise medical conclusions.",
    'About "Telangiectasia Area Assessment"',
    "Telangiectasia area assessment tool: based on facial region, erythema area ratio and vessel diameter, it grades the severity of telangiectasia and offers grading and improvement suggestions.",
    "Vessel diameter classification",
    "Telangiectasia self-assessment",
    "Pre-laser-treatment assessment",
    "Skin barrier repair reference",
    "Erythema area ratio",
    "Vessel diameter",
]))

# ---------------- assessor-67 (42) ----------------
write('assessor-67', build('assessor-67', [
    "🔬 Registration (Filing / Testing / Safety Assessment) Process",
    "Enter the cosmetic type and test parameters to assess filing compliance per the Cosmetic Supervision and Administration Regulation.",
    "Registration (Filing / Testing / Safety Assessment) Process",
    "/ Registration (Filing / Testing / Safety Assessment) Process",
    '📖 View the "Registration (Filing / Testing / Safety Assessment) Process User Guide"',
    "This tool compares each entered test value for heavy metals (lead/mercury/arsenic/cadmium), methanol and microbes against public limits such as the Safety and Technical Standards for Cosmetics, and judges whether each item meets the standard; it runs entirely client-side with no data upload.",
    "Cosmetic category",
    "Special cosmetics",
    "Creams and lotions",
    "Face masks",
    "Lead content (mg/kg)",
    "Arsenic content (mg/kg)",
    "Mercury content (mg/kg)",
    "Methanol content (%)",
    "📚 Deep Dive: Registration (Filing / Testing / Safety Assessment) Process",
    "Pre-filing self-check: enter the lead, arsenic, mercury, methanol and total plate count from the third-party test report to see whether this batch of formula can pass filing.",
    "Formula fine-tuning: when an item sits at the limit edge, first work out the margin of each item before changing the formula and process, to avoid repeated testing.",
    "Special vs ordinary routing: switch the total plate count limit by category to see whether NMPA registration or filing applies.",
    "Reproducible example: all five items of an ordinary cosmetic meet the standard",
    "Input: category = ordinary cosmetic; lead 5, arsenic 2, mercury 0.5, methanol 0.1, total plate count 100. Built-in limits: lead ≤10, arsenic ≤4, mercury ≤1, methanol ≤0.2, total plate count (ordinary) ≤1000. Item-by-item judgment 5/5 all ✓ → conclusion 'Meets filing/registration requirements'; note that ordinary cosmetics can be marketed after filing on the NMPA platform. If the category is switched to 'special cosmetics', the total plate count limit tightens to ≤500, while the other four limits stay unchanged.",
    "Reproducible example: excess mercury is blocked",
    "Input: mercury 1.5 (limit ≤1) → this item is judged ✗, overall conclusion 'Does not meet requirements'; the page warns of an exceeding item and that the product may not be sold, and the formula or process must be adjusted and retested to pass before filing/registration.",
    "Where do the limits come from? Can they be changed?",
    "The limits are built into the page from public standards such as the Safety and Technical Standards for Cosmetics, the Cosmetic Supervision and Administration Regulation, and GB 7918, GB 7917 (lead ≤10, arsenic ≤4, mercury ≤1, methanol ≤0.2, total plate count ordinary ≤1000 / special ≤500, in mg/kg; total plate count in CFU/g). The tool runs client-side, offline, with no data upload, so the limits are a fixed reference; when regulations update, the official latest text prevails.",
    "Where is the difference between special and ordinary cosmetics?",
    "In this tool it shows mainly in two points: one is the total plate count limit (special ≤500, ordinary ≤1000); the other is the market path - special cosmetics (hair dye, perming, spot-whitening, sunscreen, anti-hair-loss, new-claim etc.) must apply for NMPA registration with an approval cycle of about 6-12 months, while ordinary cosmetics only need filing on the NMPA platform and can be marketed after filing.",
    "Can it replace third-party testing or official review?",
    "No. This tool only does an item-by-item comparison of 'entered values vs public limits' for pre-test self-check and formula pre-judgment; the legal conclusion must be based on the test report from a qualified laboratory and the review result of the drug regulator.",
    "Special cosmetics require NMPA registration (sunscreen/hair dye/perming/spot-whitening etc.); ordinary cosmetics require filing",
    "Heavy-metal limits: lead ≤10 mg/kg, arsenic ≤4 mg/kg, mercury ≤1 mg/kg",
    "Methanol limit ≤0.2% (ethanol-containing products)",
    "Total plate count: special cosmetics ≤500 CFU/g, ordinary ≤1000 CFU/g",
    "Product testing and safety assessment report must be completed before filing/registration",
    'About "Registration (Filing / Testing / Safety Assessment) Process"',
    "Cosmetic registration-filing compliance assessment tool: enter test values for heavy metals, methanol, microbes etc. and judge filing/registration compliance against regulatory standards.",
    "Ordinary / special cosmetic classification",
    "Five safety indicators testing",
    "Automatic compliance judgment",
    "Filing / registration process guidance",
    "Cosmetic filing application",
    "Cosmetic safety assessment",
    "Market supervision compliance",
]))

# ---------------- calc-51 (32) ----------------
write('calc-51', build('calc-51', [
    "🧴 Sunscreen SPF / PA Calculator",
    "Enter UVB / UVA blocking rates to compute the SPF value and PA grade.",
    '📖 View the "Sunscreen SPF / PA Calculator User Guide"',
    "SPF = 1/(1 - UVB blocking rate)",
    "UVB blocking rate (%)",
    "UVA blocking rate (%)",
    "💡 SPF = 1/(1 - UVB blocking rate); PFA = 1/(1 - UVA blocking rate), and the PA grade is determined by PFA.",
    "Theoretical values are for reference only; the actual product SPF is based on human testing.",
    "📚 Deep Dive: Sunscreen SPF / PA Calculation",
    "Daily commute: estimate whether you reach 70-80% of the labelled SPF using about 1/4 teaspoon (≈0.5-0.75 g) for the face.",
    "Outdoor sun exposure: compute the effective-protection decay after 2-hour reapplication gaps and under-application, and advise stronger physical shading.",
    "Purchase comparison: compare side by side the real gap between two SPF/PA products when 'both applied thin'.",
    "Applying half the amount of SPF50",
    "Input: labelled SPF50, measured amount about half the recommended → actual protection is roughly at the SPF15-20 level; advise applying enough or reapplying.",
    "Does higher SPF mean you can skip reapplication longer?",
    "No. SPF is an intensity, not a duration; sweat, friction and oil weaken it, so reapply about every 2 hours.",
    "What is the difference between PA and SPF?",
    "SPF mainly blocks UV-B (sunburn); PA mainly blocks UV-A (photo-aging and tanning). Both matter.",
    "What is enough to apply?",
    "The common facial recommendation is about 1/4 teaspoon, but most people actually apply only 1/4-1/2, greatly reducing protection.",
    'About "Sunscreen SPF / PA Calculator"',
    "Sunscreen factor calculator: based on UVB and UVA blocking rates, it computes the SPF and PFA values theoretically and automatically grades the PA protection level.",
    "SPF / PFA theoretical calculation",
    "Automatic PA grade determination",
    "Blocking-rate visualization",
    "Sunscreen reapplication advice",
    "Sunscreen product evaluation",
    "Formulation R&D reference",
    "Sunscreen science education",
    "Outdoor activity planning",
    "UVB blocking rate",
    "UVA blocking rate",
]))

# ---------------- chemical-peel (48) ----------------
write('chemical-peel', build('chemical-peel', [
    "📏 Chemical Peel Depth Calculator (Acid Concentration / pH)",
    "Estimate the penetration depth and safety grade of a chemical peel from the acid type, concentration, pH and dwell time.",
    "Chemical Peel Depth Calculator",
    "/ Chemical Peel Depth Calculator",
    '📖 View the "Chemical Peel Depth Calculator (Concentration / pH) User Guide"',
    "Free-acid ratio = 1 / (1 + 10^(pH - pKa)); penetration-depth index = free-acid concentration × time × (76/MW) × sensitivity × first-time factor / 100",
    "The free-acid ratio is determined by the acid's pKa and the measured pH: pKa is 3.83 for glycolic, 3.86 for lactic, 3.41 for mandelic, 2.97 for salicylic, 0.26 for TCA, 3.0 for Jessner; free-acid concentration = input concentration × free-acid ratio. The molecular-weight factor is benchmarked at 1.0 for glycolic (MW 76), and others are scaled by 76/MW (lactic 90, mandelic 152, salicylic 138, TCA 163, Jessner 100); the smaller it is, the faster the penetration. First-time peeling is multiplied by a 0.7 reduction factor. A larger depth index indicates deeper exfoliation, used to choose the acid/concentration/pH combination and estimate recovery time.",
    "Acid type",
    "Glycolic acid (AHA, MW 76)",
    "Lactic acid (AHA, MW 90)",
    "Mandelic acid (AHA, MW 152)",
    "Salicylic acid (BHA, MW 138)",
    "Trichloroacetic acid (TCA)",
    "Jessner's solution",
    "Product pH",
    "Dwell time (minutes)",
    "Skin sensitivity",
    "Sensitive (thin skin / rosacea)",
    "Tolerant (oily/thick skin)",
    "First-time peeling?",
    "Not first time (tolerance established)",
    "📋 Chemical Peel Depth Grading",
    "Common acids",
    "Recovery period",
    "Very superficial",
    "No desquamation",
    "Superficial",
    "Stratum granulosum - basal layer",
    "Medium",
    "Papillary dermis",
    "Deep",
    "Reticular dermis",
    "14-30 days",
    "⚠️ Chemical peeling is a medical procedure; AHA above 30% and TCA at any concentration should be performed by a physician. This tool is for planning reference only.",
    "📚 Deep Dive: Chemical Peel Depth Calculator (Concentration / pH)",
    "Home peeling product choice: compare the exfoliation strength of glycolic 5%/7%/10% at different pH to avoid over-strength burns.",
    "Clinic protocol design: match concentration and dwell time to the goal (exfoliation/brightening/acne marks).",
    "Risk self-check: recognize that a 'high concentration + low pH' combination has entered the medium-deep range and needs professional operation.",
    "Glycolic 8% pH 3.5 self-assessment",
    "Input: glycolic 8%, pH 3.5, dwell 5 minutes → graded as superficial peeling, home-usable; if raised to 30%+ it becomes medium-deep and requires a physician.",
    "Is higher concentration better?",
    "No. High concentration and low pH easily cause chemical burns; beginners should start with low concentration and short dwell time.",
    "Why strict sun protection after peeling?",
    "After peeling the stratum corneum thins and UV more easily causes pigmentation; post-procedure sun protection is mandatory.",
    "Can you do medium-deep peeling at home yourself?",
    "Not recommended. Medium-deep peeling is a medical act and should be performed by qualified personnel in a clinic.",
    'About "Chemical Peel Depth Calculator"',
    "Chemical peel (concentration/pH) depth calculator: computes the penetration depth and safety grade of a chemical peel online. A professional medical tool based on authoritative medical standards; for reference only.",
]))
