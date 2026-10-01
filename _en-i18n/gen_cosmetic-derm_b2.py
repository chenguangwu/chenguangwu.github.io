#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第2批：concentration / corneometer / cosmetic-injection / eyebag-assessment"""
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


# ---------------- concentration (39) ----------------
write('concentration', build('concentration', [
    "\U0001F4CF AHA Peel Depth Estimator",
    "Enter the AHA concentration and pH to estimate the chemical exfoliation depth and the skin layer affected.",
    "AHA Peel Depth",
    "/ AHA Peel Depth",
    '\U0001F4D6 View the "AHA Peel Depth Estimator User Guide"',
    "Free-acid ratio = 10^(pH \u2212 pKa) / (1 + 10^(pH \u2212 pKa)); free-acid concentration = input concentration \u00d7 free-acid ratio",
    "pKa constants: AHA (glycolic) 3.83, BHA (salicylic) 2.97, TCA 0.66. The lower the pH, the higher the free-acid ratio and the stronger the exfoliation; pH guide: <2.0 highly irritating, <3.0 strong exfoliation, <3.5 moderate, \u2265\u20093.5 gentle. Depth grading: AHA is graded by the concentration\u2013pH combination into very superficial (\u226420% and pH\u2265\u20093.5) / superficial / medium / deep; BHA into superficial / medium / deep by \u226410% / \u226420% / >20%; TCA into superficial / medium / deep by \u226415% / \u226435% / >35%. Used for the quantitative assessment of peel concentration and pH in acid-treatment planning.",
    "Acid type",
    "Alpha-hydroxy acid AHA (glycolic / lactic)",
    "Beta-hydroxy acid BHA (salicylic)",
    "Trichloroacetic acid TCA",
    "\U0001F4A1 Peel depth is determined together by acid type, concentration and pH. The lower the pH and the higher the concentration, the deeper the exfoliation. Free-acid amount = concentration \u00d7 10^(pH-pKa) / (1 + 10^(pH-pKa)).",
    "Press",
    "quick estimate,",
    "Copy result",
    "Chemical peeling is a medical procedure and must be performed by a qualified physician; do not do it yourself.",
    "No estimate records yet",
    "\U0001F4DA Deep Dive: AHA Peel Depth Estimator",
    "Ingredient comparison: the penetration difference between the same concentration at different pH, to understand why 'same concentration does not always mean same effect'.",
    "Post-procedure care: estimate the days needed for barrier recovery after peeling and plan the moisturizing and repair rhythm.",
    "Pitfall alert: tell whether the marketing claim of 'high concentration yet gentle' is self-contradictory.",
    "Salicylic acid 2% vs glycolic acid 10%",
    "Input both parameters \u2192 salicylic acid is lipid-soluble and targets pores, glycolic acid is water-soluble and targets the epidermis; the layers are similar but the targets differ, so choose by need rather than concentration alone.",
    "How to choose between salicylic and fruit acids?",
    "Oily acne-prone skin with clogged pores usually uses salicylic acid (lipid-soluble, enters follicles); dry skin wanting brightening usually uses glycolic acid; decide by skin type.",
    "Why does pH matter?",
    "The free-acid concentration is determined by pH; a higher pH means less active acid, lower irritation but weaker effect, so a balance is needed.",
    "Can this tool determine the treatment plan?",
    "No. It only illustrates the principle; for actual operation and post-procedure care, please follow your physician's advice.",
    'About "AHA Peel Depth"',
    "AHA peel depth estimator: based on acid type (AHA/BHA/TCA), concentration and pH, it calculates the free-acid amount and estimates the chemical exfoliation depth.",
    "Free-acid concentration calculation",
    "Peel depth grading",
    "Multiple acid support",
    "Recovery-period advice",
    "Chemical peel planning",
    "Peel concentration reference",
    "Skincare education",
    "Acid concentration",
]))

# ---------------- corneometer (37) ----------------
write('corneometer', build('corneometer', [
    "\U0001F9B4 Skin Hydration (Corneometer) Assessor",
    "Based on Corneometer CM825 stratum corneum hydration measurements (AU), assess skin hydration status and barrier function.",
    "Skin Hydration Assessor",
    "/ Skin Hydration Assessor",
    '\U0001F4D6 View the "Skin Hydration (Corneometer) Assessor User Guide"',
    "Corneometer measurement of skin moisture: ambient-humidity correction = (humidity \u2212 50) \u00f7 10 \u00d7 3 AU; the corrected moisture value is the measured value per site plus the correction, graded by AU (<30 dry, 30\u201345 normal, >45 moist).",
    "Measured hydration per region (AU)",
    "Applied skincare before measurement?",
    "Not applied (accurate measurement)",
    "Applied (for reference only)",
    "\U0001F4CB Corneometer Hydration Grading (AU)",
    "Measured value (AU)",
    "Hydration status",
    "Severe dehydration",
    "Rough, flaky, tight",
    "Tightness, fine lines",
    "Well hydrated",
    "Smooth, elastic",
    "Moist",
    "Plump, radiant",
    "Over-hydrated",
    "Possible barrier damage",
    "\u26A0\uFE0F Before measurement, cleanse and rest the skin for 15\u201330 minutes; avoid measuring right after applying skincare (affects accuracy). Ambient humidity affects the result, and this tool has already applied a correction.",
    "\U0001F4DA Deep Dive: Skin Hydration (Corneometer) Assessor",
    "Skincare evaluation: compare the capacitance at the same site before and after using a moisturizer to judge whether the product works.",
    "Seasonal management: low winter values suggest reinforcing occlusives (ceramides / petrolatum); high summer values allow lighter care.",
    "Barrier monitoring: combined with transepidermal water loss, distinguish 'lacking water' from 'leaky barrier'.",
    "Cheek capacitance comparison",
    "Input: Before use 38 AU, after 2 weeks of ceramide cream 62 AU \u2192 rose from dry to normal-moist, suggesting the formula fits.",
    "Is a higher capacitance always better?",
    "Moderation is enough. Too high may only mean surface moisture; judge together with barrier indicators.",
    "Can I measure at home?",
    "You can use a consumer Corneometer-style probe, but technique, site and ambient temperature all affect the reading.",
    "Does lacking water mean a damaged barrier?",
    "Not necessarily. Water loss can be replenished short-term; barrier damage shows in transepidermal water loss \u2014 don't confuse the two.",
    'About "Skin Hydration Assessor"',
    "Skin hydration (Corneometer) assessor: assess stratum corneum hydration online and judge skin hydration status. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- cosmetic-injection (64) ----------------
write('cosmetic-injection', build('cosmetic-injection', [
    "\U0001F504 Aesthetic Injection (Botox / HA) Unit Calculator",
    "Based on treatment area and muscle strength, calculate the reference dosage of botulinum toxin (Botox) and hyaluronic acid (HA) filler.",
    "Aesthetic Injection Unit Calculator",
    "/ Aesthetic Injection Unit Calculator",
    '\U0001F4D6 View the "Aesthetic Injection (Botox / HA) Unit Calculator User Guide"',
    "\U0001F489 Botulinum toxin",
    "\U0001F489 HA filler",
    "Botulinum toxin dosage",
    "Glabellar lines (corrugator / depressor supercilii)",
    "Forehead lines (frontalis)",
    "Crow's feet (orbicularis oculi)",
    "Chin wrinkles (mentalis)",
    "Masseter (jaw slimming)",
    "Bunny lines (nasalis)",
    "Perioral lines (orbicularis oris)",
    "Marionette lines (depressor anguli oris)",
    "Neck cords (platysma)",
    "Muscle strength",
    "Weaker (female / first time)",
    "Stronger (male / well-developed)",
    "Brand",
    "Botox (OnabotulinumtoxinA)",
    "Xeomin (IncobotulinumtoxinA)",
    "Dysport (AbobotulinumtoxinA) (1:2.5)",
    "Hengli (domestic BTXA)",
    "HA filler volume",
    "Nasolabial folds",
    "Tear trough",
    "Lips (lip augmentation)",
    "Chin",
    "Nose",
    "Cheeks / apple of the cheek",
    "Temples",
    "Marionette lines",
    "Depression degree",
    "Single-syringe specification",
    "\U0001F4CB Common Reference Dosage Table",
    "Botulinum toxin (U)",
    "HA filler (ml)",
    "Glabellar lines",
    "Forehead lines",
    "Crow's feet (both sides)",
    "Masseter (both sides)",
    "25\u201350 / side",
    "Nasolabial folds (both sides)",
    "0.5\u20131.5 / side",
    "Tear trough (both sides)",
    "0.3\u20130.5 / side",
    "Lip augmentation",
    "\u26A0\uFE0F Injectable aesthetics are medical procedures; dosage varies with individual differences, product brand and injection technique. This tool only provides a reference range and must be performed by a licensed physician after consultation.",
    "\U0001F4DA Deep Dive: Aesthetic Injection (Botox / HA) Unit Calculator",
    "Pre-consultation prep: learn the approximate unit ranges for common areas so you are not misled by 'sky-high unit' quotes.",
    "Rough budget estimate: convert the single-treatment cost range by unit / ml unit price.",
    "Risk awareness: recognize the potential stiffness and diffusion risk of over-injection sites (e.g. full-face layering).",
    "Glabellar Botox estimate",
    "Input: Moderate glabellar lines in a female \u2192 common range about 15\u201325 U; when consulting, verify the brand's unit definition (Botox and Hengli units are not fully equivalent).",
    "Can I inject directly based on the calculation?",
    "Absolutely not. The dosage must be set on-site by a licensed physician based on muscle distribution and expression habits; this tool is for education only.",
    "Are units the same across brands?",
    "No. Each brand has different unit definitions and potencies; conversion requires a professional.",
    "Can HA and botulinum toxin units be mixed in one calculation?",
    "No. The former is by ml / syringe, the latter by units; the dimensions differ, so do not add them directly.",
    'About "Aesthetic Injection Unit Calculator"',
    "Aesthetic injection (botulinum toxin / HA) unit calculator: compute the reference injection dosage of botulinum toxin and HA for each area online. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- eyebag-assessment (63) ----------------
write('eyebag-assessment', build('eyebag-assessment', [
    "\u2728 Eye Bag (Fat / Edema) Assessor",
    "Assess the severity of lower-eyelid fat herniation (eye bags), distinguish eye bag / under-eye roll (Weicang) / edema type, and provide treatment-direction reference.",
    "Eye Bag Assessor",
    "/ Eye Bag Assessor",
    '\U0001F4D6 View the "Eye Bag (Fat / Edema) Assessor User Guide"',
    "Eye-bag assessment = fat protrusion + skin laxity + tear trough + edema (each 0 to 3) combined; integrated with type (under-eye roll / eye bag / tear trough) and age classification; the under-eye roll is a normal structure and needs no treatment.",
    "Lower-eyelid assessment",
    "Fat protrusion degree (0\u20134)",
    "0 \u2014 no protrusion",
    "1 \u2014 slight, visible when smiling",
    "2 \u2014 obvious protrusion, visible at rest",
    "3 \u2014 marked protrusion beyond the orbital rim",
    "4 \u2014 severe, with laxity and ptosis",
    "Skin laxity (0\u20134)",
    "0 \u2014 no laxity",
    "1 \u2014 slight fine lines",
    "2 \u2014 moderate laxity",
    "3 \u2014 obvious laxity and wrinkles",
    "4 \u2014 severe redundant laxity",
    "Tear-trough depression (0\u20134)",
    "1 \u2014 slight shadow",
    "2 \u2014 obvious depression",
    "3 \u2014 deep depression with pigmentation",
    "4 \u2014 severe deep groove extension",
    "Edema degree",
    "No edema",
    "Mild morning swelling",
    "Visible puffiness all day",
    "Obvious edema, pitting on pressure",
    "Type judgment",
    "Fat-type eye bag",
    "Edema-type eye bag",
    "Laxity-type eye bag",
    "Uncertain (may be under-eye roll)",
    "Under 20",
    "\u2728 Eye Bag vs Under-eye Roll",
    "Under-eye roll",
    "Eye bag",
    "Adjacent to lower lashes, 4\u20137 mm wide",
    "Farther from lower lashes, below the orbital septum",
    "Strip-like ridge, obvious when smiling",
    "Triangular protrusion, visible at rest",
    "Cause",
    "Orbicularis contraction (aesthetic)",
    "Fat herniation / laxity / edema",
    "Appearance",
    "Youthful, approachable",
    "Tired, aged",
    "\u26A0\uFE0F Eye-bag causes are complex and may involve orbital-septum fat, skin laxity and edema. The assessment result is for reference only; the surgical plan must be determined by a plastic surgeon after consultation.",
    "\U0001F4DA Deep Dive: Eye Bag (Fat / Edema) Assessor",
    "Morning-edema identification: if light pressure temporarily reduces it, it is mostly edema type, suggesting sleep / salt / circulation issues.",
    "Age-related protrusion: if it does not disappear when smiling or lying down and shows a shadow under light, it is mostly fat type, calling for surgery or filler approaches.",
    "Skincare pitfall: recognize that 'eye cream removes eye bags' claims are usually ineffective for true fat type.",
    "Under-eye roll vs lower protrusion",
    "Input: Obvious in the morning, relieved after a nap, pitting on finger pressure \u2192 judged as edema type; advise salt control and sleep; if it persists, switch to fat-type assessment.",
    "Can eye cream remove true eye bags?",
    "Very hard. Fat protrusion or ligament laxity sees limited improvement from skincare and belongs to medical aesthetics / ophthalmology.",
    "How to tell edema type from fat type?",
    "Look at reversibility and timing: heavy in the morning and lighter at night is mostly edema; persistent protrusion is mostly fat; still needs physician confirmation.",
    "Can this tool determine the surgical plan?",
    "No. It only gives an initial type judgment; the surgical method is evaluated by a specialist.",
    'About "Eye Bag Assessor"',
    "Eye bag (fat / edema) assessor: assess eye-bag severity online, distinguish eye bag from under-eye roll, and provide treatment reference. A medical professional tool based on authoritative medical standards; for reference only.",
]))
