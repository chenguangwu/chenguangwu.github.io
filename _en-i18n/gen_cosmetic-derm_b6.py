#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第6批：pore-grading / post-procedure-recovery / ratio-composition-injection / rf-tightening"""
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


# ---------------- pore-grading (47) ----------------
write('pore-grading', build('pore-grading', [
    "\U0001F9B4 Pore (Magnified) Enlargement Grader",
    "Based on pore visibility and density under magnified imaging, grade the pore-enlargement degree of each facial region.",
    "Pore Enlargement Grader",
    "/ Pore Enlargement Grader",
    '\U0001F4D6 View the "Pore (Magnified) Enlargement Grader User Guide"',
    "Pore score = (nose tip\u00d73 + nasal ala\u00d73 + cheek\u00d72 + forehead\u00d72) \u00f7 10 \u00d7 25 (max 100); the T-zone carries higher weight than the U-zone, graded together with sebum level and pore type.",
    "Regional pore assessment",
    "Nose-tip pore visibility (0\u20134)",
    "Grade 0 \u2014 barely visible",
    "Grade 1 \u2014 slightly visible",
    "Grade 2 \u2014 clearly visible",
    "Grade 3 \u2014 enlarged with blackheads",
    "Grade 4 \u2014 markedly enlarged and depressed",
    "Nasal-alar pore visibility (0\u20134)",
    "Cheek pore visibility (0\u20134)",
    "Grade 3 \u2014 markedly enlarged",
    "Grade 4 \u2014 markedly enlarged",
    "Forehead pore visibility (0\u20134)",
    "Sebaceous pores (mostly T-zone)",
    "Aging pores (teardrop / vertical)",
    "Scar pores (depressed)",
    "Sebum secretion level",
    "Low (dry)",
    "Normal (neutral)",
    "High (oily-leaning)",
    "Very high (oily)",
    "\U0001F4CB Pore Enlargement 5-level Scoring Standard",
    "Barely visible",
    "Visible up close",
    "Clearly visible",
    "Enlarged with blackheads",
    "Markedly enlarged and depressed",
    "\u26A0\uFE0F Pore enlargement is affected by multiple factors such as genetics, sebum and photo-aging. The assessment result is for reference; the treatment plan must be determined by a licensed physician after consultation.",
    "\U0001F4DA Deep Dive: Pore (Magnified) Enlargement Grader",
    "Before-after comparison: grade at the same magnification before and after treatment, using level change instead of subjective feeling.",
    "Product test: use grading to see whether acid / oil-control products drop one level over 4\u20138 weeks.",
    "Education: explain that pore enlargement is multi-factorial (oil / aging / acne), not single-factor.",
    "8-week post-acid re-assessment",
    "Input: moderate before treatment, mild after 8 weeks \u2192 suggests oil control + salicylic acid works; continue maintenance and sun protection.",
    "Is magnifier self-test accurate?",
    "Rough. Magnification and lighting vary a lot; only watch the trend.",
    "Will grading improve on its own?",
    "Good oil control and anti-aging can improve it, but laxity rises with age.",
    "Can it replace seeing a doctor?",
    "No. With severe acne see a dermatologist.",
    'About "Pore Enlargement Grader"',
    "Pore enlargement grader: assess facial pore-enlargement degree online and give pore grading and improvement advice. A medical professional tool based on authoritative medical standards; for reference only.",
]))

# ---------------- post-procedure-recovery (57) ----------------
write('post-procedure-recovery', build('post-procedure-recovery', [
    "\U0001FA7A Post-procedure Recovery (Redness / Scabbing) Timeline",
    "Select an aesthetic procedure and treatment parameters to generate a detailed post-procedure recovery timeline and staged care guidance.",
    "Post-procedure Recovery Timeline",
    "/ Post-procedure Recovery Timeline",
    '\U0001F4D6 View the "Post-procedure Recovery (Redness / Scabbing) Timeline User Guide"',
    "Aesthetic procedure",
    "Q-switched / picosecond laser",
    "CO2 fractional laser",
    "Erbium laser resurfacing",
    "Photofacial (IPL)",
    "Glycolic peel",
    "TCA chemical peel",
    "Thread lift",
    "Hydration injection / mesotherapy",
    "Treatment intensity",
    "Moderate (standard)",
    "Severe (intensive)",
    "Treatment date",
    "Type I\u2013II (fair, high PIH risk)",
    "Type V\u2013VI (dark, high PIH risk)",
    "Generate timeline",
    "Copy timeline",
    "\U0001F4CB Common Recovery Reactions",
    "Needs medical care",
    "Redness / swelling",
    "Gradually subsides in 1\u20137 days",
    "Persists >2 weeks or worsens",
    "Scabbing",
    "Naturally sheds in 3\u201310 days",
    "Forceful picking / pus",
    "Dry desquamation",
    "3\u201314 days",
    "Crack infection",
    "Pigmentation",
    "Gradually fades in 1\u20133 months",
    "Persists and deepens after 3 months",
    "Mild pain",
    "Severe persistent pain",
    "\u26A0\uFE0F Individual recovery speed varies greatly. If persistent redness, pus, severe pain or abnormal pigmentation appears, contact the treating physician immediately. This timeline is for reference only.",
    "\U0001F4DA Deep Dive: Post-procedure Recovery (Redness / Scabbing) Timeline",
    "Schedule planning: stagger recovery with meetings / travel to avoid 'having a date tomorrow but scabbing'.",
    "Expectation management: understand why fractional laser needs a 5\u20137 day scabbing period.",
    "Abnormal handling: redness and oozing beyond the normal window means seeking care promptly.",
    "Post-photofacial arrangement",
    "Input: Photofacial \u2192 redness for a few hours, micro-scabs 1\u20133 days, light makeup about 2\u20133 days, with strict sun protection advised.",
    "Are the time windows accurate?",
    "They are typical ranges only; individuals and energy levels differ greatly\u2014follow the operator's instructions.",
    "What if it stays red beyond the window?",
    "Return to the clinic or see a doctor promptly; do not self-treat.",
    "Can this table replace medical advice?",
    "No. It is only a schedule reference; follow the operating physician for post-procedure care.",
    'About "Post-procedure Recovery Timeline"',
    "Post-procedure recovery (redness / scabbing) timeline: online generates an aesthetic post-procedure recovery schedule and care guidance. A medical professional tool based on authoritative medical standards; for reference only.",
    "How to use the Post-procedure Recovery (Redness / Scabbing) Timeline",
    "Useful for arranging rest and appointments after an aesthetic procedure, learning each procedure's redness / scabbing window, and recognizing abnormal recovery that needs prompt care.",
    "What does the Post-procedure Recovery (Redness / Scabbing) Timeline do?",
    "Select a specific aesthetic procedure and enter treatment parameters to auto-generate a post-procedure recovery timeline for redness, scabbing and more, with staged home care and sun-protection repair guidance.",
]))

# ---------------- ratio-composition-injection (35) ----------------
write('ratio-composition-injection', build('ratio-composition-injection', [
    "\U0001F9B4 Hydration Injection Ratio Calculator",
    "Enter the total formula volume and each component's concentration ratio to calculate each component's volume in the hydration injection formula.",
    "Hydration Injection Ratio",
    "/ Hydration Injection Ratio",
    '\U0001F4D6 View the "Hydration Injection Ratio Calculator User Guide"',
    "Adjusted ratio = each component ratio / total ratio; volume = total \u00d7 adjusted ratio; content = volume \u00d7 reference concentration",
    "When the total ratio deviates from 100% (\u00b10.5%), it is proportionally adjusted with a warning. Component content: hyaluronic acid = volume \u00d7 input concentration (mg/ml); vitamin C, glutathione and other / PRP are converted at reference concentrations 50 / 30 / 5 mg/ml respectively. Outputs each component's adjusted ratio, volume, content and total, and shows the ratio structure with a bar chart, for compound injection (HA+VC+glutathione) formula accounting.",
    "Hyaluronic acid concentration (mg/ml)",
    "Glutathione ratio (%)",
    "Other / PRP ratio (%)",
    "\U0001F4A1 Hydration injection uses non-cross-linked HA as a base, optionally with vitamin C (brightening) and glutathione (antioxidant). The total ratio is auto-adjusted to 100%.",
    "Hydration injection is a medical procedure; the formula must be designed and performed by a licensed physician.",
    "\U0001F4DA Deep Dive: Hydration Injection Ratio Calculator",
    "Compound check: when scaling up by total volume for multiple patients, keep ratios consistent.",
    "Error control: warn of accumulated rounding deviation; suggest computing the total first then allocating.",
    "Teaching demo: explain the basic relation 'concentration \u00d7 volume = active amount' to beginners.",
    "Dual-component ratio",
    "Input: stock A 3%, stock B 1%, target 5 mL, A:B=2:1 \u2192 outputs A 3.33 mL, B 1.67 mL, with a note to shake well and use fresh.",
    "Can ratios be adjusted freely?",
    "No. Each ingredient has a safe concentration; excess easily irritates, so follow instructions.",
    "Does the result need to be sterile?",
    "The operation itself is done aseptically in a clinic; this tool only computes ratios.",
    "Can it replace a prescription?",
    "No. The ratio is only arithmetic; defer ingredient choice to a physician.",
    'About "Hydration Injection Ratio"',
    "Hydration injection ratio calculator: based on the total formula volume and each component's (HA, vitamin C, glutathione etc.) concentration ratio, it calculates each component's volume and content detail.",
    "Four-component ratio calculation",
    "Hydration injection formula design",
    "Brightening / antioxidant ratio",
    "Total formula volume",
    "Hyaluronic acid concentration",
    "Hyaluronic acid ratio",
    "Vitamin C ratio",
    "Glutathione ratio",
    "Other ratio",
]))

# ---------------- rf-tightening (50) ----------------
write('rf-tightening', build('rf-tightening', [
    "\U0001F9EE RF (Temperature / Time) Tightening Calculator",
    "Based on RF treatment temperature, hold time and frequency, estimate the collagen-stimulation effect and tightening grade.",
    "RF Tightening Calculator",
    "/ RF Tightening Calculator",
    '\U0001F4D6 View the "RF (Temperature / Time) Tightening Calculator User Guide"',
    "Effective-temperature zone (42\u201350 \u00b0C): effect = (temperature \u2212 42) \u00d7 time / 180; high-temperature zone (>50 \u00b0C to safe upper limit): 4 \u00d7 time / 180 \u00d7 1.2; effect cap 10",
    "Safe temperature upper limit: 52 \u00b0C with cooling, 48 \u00b0C without cooling; effective range 40 \u00b0C to the limit. Low-temperature zone (40\u201342 \u00b0C) = (temperature \u2212 40) \u00d7 time / 360 \u00d7 0.5. Frequency vs penetration depth: 1 MHz 3\u20135 mm, 2 MHz 2\u20133 mm, 3 MHz 1\u20132 mm, 6 MHz 0.5\u20131 mm, bipolar multi-layer alternating (1\u20135 mm). Multiple sessions accumulate with diminishing returns. Used for RF-tightening temperature / time parameter safety and collagen-stimulation effect assessment.",
    "Target dermal temperature (\u00b0C)",
    "Temperature hold time (seconds)",
    "RF frequency (MHz)",
    "1 MHz (deep)",
    "2 MHz (mid)",
    "3 MHz (superficial)",
    "6 MHz (epidermis\u2013superficial dermis)",
    "Dual-frequency alternating",
    "Treatment course",
    "3 sessions (standard course)",
    "5 sessions",
    "8 sessions (intensive)",
    "Interval per session (weeks)",
    "Epidermal cooling",
    "With cooling (higher safe temperature)",
    "Without cooling (conservative temperature)",
    "\U0001F4CB RF Temperature and Tissue Effect",
    "Tissue effect",
    "Mild heating",
    "Promotes circulation, no collagen denaturation",
    "Collagen triple-helix unwinding",
    "Immediate contraction + delayed neogenesis",
    "Collagen denaturation contraction",
    "Optimal tightening temperature range",
    "Tissue coagulation",
    "Needs precise temperature control to prevent burns",
    "Tissue necrosis / carbonization",
    "Dangerous! Must be avoided",
    "\u26A0\uFE0F RF treatment temperature is closely tied to tissue effect. Too high a temperature causes burns and scars. Actual parameters must be adjusted by device type and patient response, operated by a licensed physician.",
    "\U0001F4DA Deep Dive: RF (Temperature / Time) Tightening Calculator",
    "Plan communication: explain 'why one session is not enough, a course is needed' \u2014 collagen remodeling needs accumulation.",
    "Safety awareness: too low is ineffective, too high burns; rely on device temperature control, not feeling.",
    "Expectation management: tightening is gradual, noticeable only after weeks, not immediate.",
    "Monopolar RF parameter understanding",
    "Input: target dermis 40\u201343 \u00b0C, several seconds per zone \u2192 judged within the collagen-contraction safe window; needs multiple accumulations, single session only mildly tightens.",
    "Does hotter mean tighter?",
    "No. Over-temperature causes burns and fat atrophy; temperature must be controlled.",
    "Effective in one session?",
    "Most need a course; effect appears gradually over weeks.",
    "Can this calculation set the parameters?",
    "No. Energy is set by a physician per device and site.",
    'About "RF Tightening Calculator"',
    "RF (temperature / time) tightening calculator: compute the collagen-stimulation effect and safe parameters of RF tightening online. A medical professional tool based on authoritative medical standards; for reference only.",
]))
