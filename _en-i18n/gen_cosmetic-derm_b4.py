#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第4批：jiguangbochangbadian / laser-parameters / length-spacing / maokongcudafenji"""
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


# ---------------- jiguangbochangbadian (44) ----------------
write('jiguangbochangbadian', build('jiguangbochangbadian', [
    "\U0001F4E1 Laser Wavelength Target Finder",
    "Select a laser type to view its target chromophore, penetration depth and clinical indications.",
    "Laser Wavelength Target",
    "/ Laser Wavelength Target",
    '\U0001F4D6 View the "Laser Wavelength Target Finder User Guide"',
    "532nm KTP (frequency-doubled Nd:YAG)",
    "585nm pulsed dye laser (PDL)",
    "595nm long-pulsed dye laser (Vbeam)",
    "694nm ruby laser",
    "755nm alexandrite laser",
    "1064nm Nd:YAG laser",
    "10600nm CO2 laser",
    "2940nm Er:YAG laser",
    "1470nm diode laser",
    "1927nm thulium laser (non-ablative)",
    "\U0001F4A1 Different-wavelength lasers are selectively absorbed by different chromophores (melanin / hemoglobin / water), which determines the target and penetration depth.",
    "Laser parameters are for reference only; actual operation must be performed by a licensed physician per the device.",
    "Penetration depth is a theoretical in-tissue value, affected by skin tone and energy density.",
    "\U0001F4DA Deep Dive: Laser Wavelength Target Finder",
    "Device selection education: understand why 755nm leans toward deep melanin removal and 1064nm toward deeper heating.",
    "Risk awareness: short wavelengths are easily absorbed by epidermal melanin; deeper skin tones need caution to prevent pigmentation.",
    "Treatment communication: translate 'what light to use' into 'which target it acts on' to reduce information asymmetry.",
    "755nm target query",
    "Input: 755nm \u2192 mainly targets melanin, medium-deep penetration, commonly used for hair removal and superficial pigment; for deeper skin tones lower the parameters to prevent pigmentation.",
    "Is a longer wavelength safer?",
    "Not necessarily. Longer wavelengths penetrate deeper but with lower precision; choose by target and skin tone, not simply longer is better.",
    "Can deeper skin tones receive laser treatment?",
    "Yes, but with caution. Parameters and timing are set by a physician by skin-tone classification to avoid pigmentation.",
    "Can this finder set the parameters?",
    "No. It only explains the targeting principle; energy and pulse width are set by professionals.",
    'About "Laser Wavelength Target"',
    "Laser wavelength target finder: select a laser type to show its target chromophore, penetration depth, clinical indications and precautions.",
    "10 common lasers",
    "Chromophore / target notes",
    "Penetration depth comparison",
    "Indication query",
    "Laser device selection",
    "Laser science education",
    "How to use the Laser Wavelength Target Finder",
    "Useful for understanding the wavelength\u2013target-chromophore relationship when choosing a laser device, assessing deep-skin-tone treatment risk, and communicating the plan between doctor and patient.",
    "What does the Laser Wavelength Target Finder do?",
    "The laser wavelength target finder lets you select a laser type to view its target, penetration depth and clinical indications, assisting aesthetic device selection.",
    "How do I use the Laser Wavelength Target Finder?",
    "Which scenarios suit the Laser Wavelength Target Finder?",
]))

# ---------------- laser-parameters (50) ----------------
write('laser-parameters', build('laser-parameters', [
    "\U0001F4DA Laser (Wavelength / Pulse Width) Target Finder",
    "Query the wavelength, pulse width, target chromophore, penetration depth and clinical indications of various aesthetic lasers.",
    "Laser Target Finder",
    "/ Laser Target Finder",
    '\U0001F4D6 View the "Laser (Wavelength / Pulse Width) Target Finder User Guide"',
    "Laser targets: match the chromophore absorption peak by wavelength and pulse width \u2014 melanin 500\u20131100nm (Q-switched 532/694/755/1064nm), hemoglobin 532/585/595/1064nm, water 2940/10600nm; pulse width determines selective photothermolysis and penetration depth.",
    "Query by laser device",
    "-- select laser device --",
    "Q-switched 532nm (KTP)",
    "Q-switched 1064nm (Nd:YAG)",
    "Picosecond 532nm",
    "Picosecond 1064nm",
    "Alexandrite 755nm",
    "Diode 800\u2013810nm",
    "Intense pulsed light IPL (500\u20131200nm)",
    "CO2 laser 10600nm",
    "Erbium laser Er:YAG 2940nm",
    "Pulsed dye 585/595nm",
    "Long-pulsed 1064nm (Nd:YAG)",
    "Excimer 308nm",
    "Query by chromophore",
    "-- select chromophore --",
    "Melanin",
    "Hemoglobin",
    "Tattoo pigment",
    "\U0001F4CB Chromophore Absorption Peak Reference",
    "Chromophore",
    "Main absorption peak",
    "Corresponding laser",
    "500\u20131100nm (penetration rises with wavelength)",
    "Oxyhemoglobin",
    "Tattoo (black / blue)",
    "Q-switched / picosecond 1064",
    "Tattoo (red / orange)",
    "Q-switched / picosecond 532",
    "\u26A0\uFE0F Laser parameter selection needs comprehensive judgment by the patient's skin phototype, lesion depth and device characteristics. This finder is for learning reference; clinical operation must be performed by a trained physician.",
    "\U0001F4DA Deep Dive: Laser (Wavelength / Pulse Width) Target Finder",
    "Device comparison: how the same wavelength with different pulse widths differs in selectivity for vessels / pigment.",
    "Post-procedure expectation: understand how pulse-width length affects thermal-damage range and recovery.",
    "Education pitfall: recognize the imprecision of 'universal wavelength' claims.",
    "Long-pulsed 1064 query",
    "Input: 1064nm long-pulsed \u2192 targets hemoglobin / water, leans toward deeper vessels and heating tightening, shorter recovery but needs multiple sessions.",
    "What does pulse-width length affect?",
    "Pulse width affects how far heat spreads to surrounding tissue; shorter is more precise, longer is gentler.",
    "Can I choose the parameters myself?",
    "No. Parameter setting is a medical act, the responsibility of the operating physician.",
    "Can the query result serve as a diagnosis?",
    "No. It only illustrates the principle; defer specific indications to a physician.",
    'About "Laser Target Finder"',
    "Laser (wavelength / pulse width) target finder: query the wavelength, pulse width, target chromophore and clinical use of various lasers online. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- length-spacing (37) ----------------
write('length-spacing', build('length-spacing', [
    "\u2728 Microneedle Penetration Calculator",
    "Enter needle length and spacing to calculate needle density, penetration area and actual penetration depth.",
    "Microneedle Penetration",
    "/ Microneedle Penetration",
    '\U0001F4D6 View the "Microneedle Penetration Calculator User Guide"',
    "Needle density = 1 / (spacing_cm)\u00b2 (spacing \u03bcm \u00f7 10000 to cm); actual penetration depth = needle length \u00d7 0.8; penetration-area ratio = needle density \u00d7 \u03c0(d/2)\u00b2 \u00d7 100%",
    "Needle length is in mm; actual penetration depth is discounted by 0.8 for skin elastic recoil. Single-channel area = \u03c0 \u00d7 (diameter \u03bcm/10000 \u00f7 2)\u00b2 cm\u00b2. Layer determination: <0.3 mm stratum corneum, <0.5 mm epidermis, <1.0 mm papillary dermis, <1.5 mm reticular dermis, \u22651.5 mm deep dermis / subcutaneous. Used for layer-coverage assessment of microneedle length-and-spacing combinations.",
    "Needle length (mm)",
    "Needle spacing (\u03bcm)",
    "Needle diameter (\u03bcm, optional)",
    "\U0001F4A1 Needle density = 10\u2076 / spacing\u00b2(\u03bcm) per cm\u00b2; actual penetration depth \u2248 needle length \u00d7 0.8. Needle length determines the action layer.",
    "Microneedling is a medical procedure; depth selection must be assessed by a licensed physician.",
    "\U0001F4DA Deep Dive: Microneedle Penetration Calculator",
    "Home care: 0.25\u20130.5mm for penetration boosting, 1.0mm+ leans mesodermal; understand why longer needles need a professional.",
    "Plan design: choose length and density by goal (transdermal absorption vs collagen stimulation).",
    "Risk control: recognize the home-use contraindications of over-long / over-dense combinations (infection / pigmentation).",
    "0.5mm length, 1mm spacing estimate",
    "Input: needle length 0.5mm, spacing 1mm \u2192 moderate channel count per area, penetration-boost tier; home use for short periods only with strict disinfection.",
    "Is longer always more effective?",
    "No. Too long causes more bleeding and pain and higher infection risk; keep home use short.",
    "Is dense spacing good?",
    "Over-dense increases trauma and recovery; choose moderate density by site.",
    "Can it replace hydration injection?",
    "No. Microneedle penetration-boosting and hydration injection act at different layers and meet different needs.",
    'About "Microneedle Penetration"',
    "Microneedle penetration calculator: based on needle length, spacing and diameter, it calculates needle density, penetration-area ratio and actual penetration depth, and determines the action layer.",
    "Needle density calculation",
    "Actual penetration depth",
    "Action-layer determination",
    "Penetration-area ratio",
    "Microneedle parameter design",
    "Treatment depth selection",
    "Aesthetic project planning",
    "Device selection reference",
    "Needle length",
    "Needle spacing",
    "Needle diameter",
]))

# ---------------- maokongcudafenji (45) ----------------
write('maokongcudafenji', build('maokongcudafenji', [
    "\U0001F9B4 Pore Enlargement Grading",
    "Enter pore diameter and site to grade pore-enlargement level and give improvement advice.",
    '\U0001F4D6 View the "Pore Enlargement Grading User Guide"',
    "Pore diameter (\u03bcm)",
    "Assessment site",
    "Nose tip",
    "Sebaceous type (round)",
    "Aging type (teardrop / vertical)",
    "Scar type (depressed)",
    "\U0001F4A1 Pore diameter <200\u03bcm is fine, 200\u2013400\u03bcm mild enlargement, 400\u2013800\u03bcm moderate, >800\u03bcm severe. Nasal pores are usually larger than cheek pores.",
    "Press",
    "quick grade,",
    "Copy result",
    "Grading is for reference only; actual pore condition needs instrument testing such as VISIA.",
    "\U0001F559 Latest grading",
    "No grading records yet",
    "\U0001F4DA Deep Dive: Pore Enlargement Grading",
    "Skin-type log: photograph at the same magnification monthly to grade, and see whether oil control / acids improve things.",
    "Plan matching: oily with comedones leans cleansing + acids; aging leans firming and collagen stimulation.",
    "Pitfall education: recognize that 'pore-shrinking miracles' are often limited for true follicular hypertrophy.",
    "Nasal-alar pore grading",
    "Input: clearly round pores, medium density, with blackheads \u2192 graded moderate oily pores; suggest oil control + low-concentration salicylic acid + sun protection.",
    "Can pores disappear completely?",
    "Hard. They can be visually reduced, but true hypertrophy is hard to fully reverse; don't believe 'zero pores'.",
    "How to tell oily from aging type?",
    "The former comes with oiliness and blackheads, the latter with skin laxity; the approaches differ.",
    "Can this grading diagnose?",
    "No. It is only a self-test reference; for severe cases see a dermatologist.",
    'About "Pore Enlargement Grading"',
    "Pore enlargement grading tool: based on pore diameter, assessment site and pore type, it grades pore-enlargement level and gives improvement advice.",
    "Four-tier pore grading",
    "Three pore types",
    "Site-differentiated assessment",
    "Targeted improvement advice",
    "Pore condition self-assessment",
    "Aesthetic project selection",
    "Skincare plan design",
    "Skin-testing aid",
    "How to use Pore Enlargement Grading",
    "Useful for monthly same-magnification photo grading to track pore changes, evaluate oil-control and acid skincare effects, and distinguish oily from aging pore causes.",
    "What does Pore Enlargement Grading do?",
    "The pore enlargement grader: enter pore diameter and site to grade enlargement and give improvement advice, aiding skincare plan design.",
    "How do I use Pore Enlargement Grading?",
    "Which scenarios suit Pore Enlargement Grading?",
    "Pore diameter",
]))
