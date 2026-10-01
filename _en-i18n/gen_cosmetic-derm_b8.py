#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 第8批：temp-time-4 / thread-lift / time-23 / visia-spots / wrinkle-dynamic-static"""
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


# ---------------- temp-time-4 (41) ----------------
write('temp-time-4', build('temp-time-4', [
    "\u2728 RF Skin-Tightening Effect Assessment",
    "Enter the target dermal temperature and hold time to assess collagen contraction and skin-tightening effect.",
    "RF Skin-Tightening Effect",
    "/ RF Skin-Tightening Effect",
    '\U0001F4D6 View the "RF Skin-Tightening Effect Assessment User Guide"',
    "Collagen contraction rate is segmented by dermal temperature; contraction rate = min(segment value × time factor, 55%); time factor = min(1 + 0.3 × ln(time), 1.8)",
    "Contraction segments: <45 °C = 0; 45\u201355 °C = (T \u2212 45)/10 × 10; 55\u201360 °C = 10 + (T \u2212 55)/5 × 10; 60\u201370 °C = 20 + (T \u2212 60)/10 × 25; 70\u201375 °C = 45 + (T \u2212 70)/5 × 5; \u226575 °C capped at 50%. Effect grading: <45 none, <55 slight, <65 good, <75 marked, \u226575 risk zone. Used to quantify RF / thermal collagen contraction and skin-tightening effect.",
    "Dermal temperature (\u00b0C)",
    "Hold time (min)",
    "RF type",
    "Monopolar RF",
    "Bipolar RF",
    "Fractional RF (microneedle)",
    "\U0001F4A1 Collagen contraction starts around 55\u201360 \u00b0C; 60\u201370 \u00b0C can reach 30\u201350% contraction; above 75 \u00b0C carries thermal-injury risk.",
    "Tap",
    "for a quick assessment,",
    "Copy result",
    "RF treatment is a medical procedure; parameters must be set by a licensed physician per device.",
    "\U0001F4DA Deep Dive: RF Skin-Tightening Effect Assessment",
    "Home RF education: understand why low-frequency, low-energy home devices need long-term use and why clinics are faster.",
    "Risk awareness: burn risk from staying too long at one spot.",
    "Efficacy review: use temperature-time logs to judge whether the stimulation window was reached.",
    "Home RF use",
    "Input: epidermis 38\u201340 \u00b0C, 3 min per zone, 3× weekly → gentle maintenance level, needs long-term use; marked laxity still warrants clinic assessment.",
    "Can home use replace the clinic?",
    "Hard. Energy and depth are limited; severe laxity needs professional devices.",
    "Is longer always better?",
    "No. Lingering at one spot risks burns; keep it moving per instructions.",
    "Can the result be used as a basis?",
    "No. Follow your physician for the specific plan.",
    'About "RF Skin-Tightening Effect"',
    "RF skin-tightening effect assessment tool: estimate collagen contraction rate and grade the tightening effect from dermal temperature, hold time and RF type.",
    "Collagen contraction estimate",
    "Time-factor correction",
    "Effect-level grading",
    "Safe-temperature warning",
    "RF parameter planning",
    "Tightening effect estimate",
    "Device parameter reference",
    "Dermal temperature",
    "Hold time",
]))

# ---------------- thread-lift (61) ----------------
write('thread-lift', build('thread-lift', [
    "\U0001F4D0 Thread Lift (Barbed Suture) Elevation-Angle Calculator",
    "Based on the lift region, suture type and insertion angle, compute the traction-force vector distribution and optimal needle-entry angle.",
    "Thread-Lift Elevation-Angle Calculator",
    "/ Thread-Lift Elevation-Angle Calculator",
    '\U0001F4D6 View the "Thread Lift (Barbed Suture) Elevation-Angle Calculator User Guide"',
    "Single-thread traction = anchor force × suture coefficient × cos(entry-angle deviation) × cos(lift-angle deviation); total effective traction = single-thread force × count × laxity correction",
    "Suture coefficients: smooth 0, PDO 0.5, bidirectional barbed 0.6, PLA 0.7, PCLA 0.8, unidirectional barbed 0.85, 360° barbed 1.0. Angle deviation = |input angle − region optimal angle|; region optimal entry/lift angle: mid-face 50/45°, lower face 40/35°, jawline 55/50°, neck 35/30°, brow 20/15°. Laxity correction: mild 1.2, moderate 1.0, severe 0.7. Effect grading: <100 mild, <300 moderate, <600 marked, ≥600 strong lift (g). Used to assess thread-lift traction and angle quality.",
    "Lift region",
    "Mid-face (cheek-apple area)",
    "Lower face (jaw margin)",
    "Jawline contour",
    "Brow",
    "Suture type",
    "Smooth thread (no lift)",
    "Bidirectional barbed",
    "Unidirectional barbed",
    "360° barbed",
    "PDO thread",
    "PLA thread",
    "PCLA thread",
    "Needle-entry angle (°)",
    "Lift-direction angle (°)",
    "Thread length (cm)",
    "Threads inserted",
    "Skin laxity",
    "Mild (rejuvenation need)",
    "Severe (marked sagging)",
    "Anchor force per thread (g)",
    "\U0001F4CB Thread-Lift Traction Vector Reference",
    "Optimal angle",
    "Lift direction",
    "Mid-face",
    "Posterosuperior (pre-auricular)",
    "Lower face",
    "Posterosuperior",
    "Jawline",
    "Toward the earlobe",
    "Toward retroauricular / mastoid",
    "Toward the temporal region",
    "\u26A0\uFE0F Thread lifting is a medical aesthetic procedure requiring a qualified physician. Angle and force calculations are theoretical; actual operation must consider facial anatomy and individual factors.",
    "\U0001F4DA Deep Dive: Thread Lift (Barbed Suture) Elevation-Angle Calculator",
    "Plan communication: use the vector diagram to explain 'why central threads lift mid/lower face and lateral threads lift the contour'.",
    "Expectation management: understand thread lift is immediate lift + gradual collagen, not permanent.",
    "Risk awareness: too shallow shows the thread, too deep nears vessels/nerves; needs expertise.",
    "Mid/lower-face routing",
    "Input: entry 30° anchored temporally → lift vector shifts superomedial, targets nasolabial fold and buccal fat; note reassessment needed after 1\u20132 years' absorption.",
    "Is thread lift permanent?",
    "No. The thread is gradually absorbed; effect lasts 1\u20132 years varying by individual.",
    "Can I decide the angle myself?",
    "No. Routing is a medical act decided by the physician per anatomy.",
    "Can this calculation be used as a basis?",
    "No. It is only a vector illustration; follow the physician for the plan.",
    'About "Thread-Lift Elevation-Angle Calculator"',
    "Thread lift (barbed suture) elevation-angle calculator: compute thread-lift traction vector angle and force distribution online. A medical professional tool based on authoritative medical standards; for reference only.",
    "How to use the Thread Lift (Barbed Suture) Elevation-Angle Calculator",
    "Useful for clinician-patient communication on thread routing and lift region, understanding immediate lift plus gradual collagen, and knowing the depth risk boundary.",
    "What does the Thread Lift (Barbed Suture) Elevation-Angle Calculator do?",
    "Based on lift region, chosen suture type and insertion angle, it computes the barbed-thread traction vector distribution and gives optimal needle-entry angle and force-balance advice to aid planning.",
    "How do I use the Thread Lift (Barbed Suture) Elevation-Angle Calculator?",
    "Which scenarios suit the Thread Lift (Barbed Suture) Elevation-Angle Calculator?",
    "Relative to vertical",
]))

# ---------------- time-23 (35) ----------------
write('time-23', build('time-23', [
    "\U0001FA79 Post-Procedure Recovery Timeline",
    "Select a medical-aesthetic procedure type to generate a recovery timeline for erythema, swelling and scabbing with care advice.",
    '\U0001F4D6 View the "Post-Procedure Recovery Timeline User Guide"',
    "Procedure type",
    "Photofacial (IPL/DPL)",
    "Non-ablative fractional laser",
    "Ablative fractional laser (CO2/Er)",
    "Superficial chemical peel",
    "Medium chemical peel",
    "Laser hair removal",
    "Thread-lift lift",
    "\U0001F4A1 Recovery time varies by individual constitution and procedure intensity; the following are general reference ranges.",
    "Recovery times are general references; actual recovery varies by person, follow your physician.",
    "Seek care promptly for abnormal redness, swelling or infection.",
    "\U0001F4DA Deep Dive: Post-Procedure Recovery Timeline",
    "Companion planning: family learns from the timeline when accompaniment is needed and when self-care is fine.",
    "Skincare restart: indicates when to switch from repair phase back to routine care.",
    "Risk identification: abnormal prolongation of any stage is a warning.",
    "Post-meso recovery",
    "Input: meso injection → needle marks close in 6\u201312 h, redness 1\u20132 days, normal skincare 2\u20133 days, stable in 1 week; note no makeup within 24 h.",
    "Does everyone recover the same?",
    "No. Metabolism, care and energy differ; ranges are only reference.",
    "Can I resume skincare early?",
    "Not advised. Open wounds risk infection; follow the physician's timing.",
    "Is this table a medical basis?",
    "No. Post-procedure, the physician's guidance is final.",
    'About "Post-Procedure Recovery Timeline"',
    "Post-procedure recovery timeline tool: generate erythema, swelling and scabbing timelines with stage-by-stage care points by procedure type.",
    "11 common procedures",
    "Staged recovery times",
    "Timeline visualization",
    "Post-procedure care advice",
    "Pre-procedure recovery planning",
    "Post-procedure care reference",
    "Leave-time arrangement",
]))

# ---------------- visia-spots (47) ----------------
write('visia-spots', build('visia-spots', [
    "\U0001F4CF Pigmentation (VISIA) Area-Depth Assessor",
    "Based on VISIA skin-analysis logic, assess facial pigmentation area proportion and pigment depth, and output a severity grade.",
    "Pigmentation Area-Depth Assessor",
    "/ Pigmentation Area-Depth Assessor",
    '\U0001F4D6 View the "Pigmentation (VISIA) Area-Depth Assessor User Guide"',
    "VISIA pigmentation score = (area×3 + depth×5 + count÷5 + percentile÷10) × region weight; region weight 1.0\u20131.5 by site, graded by score.",
    "Pigment count (spots)",
    "Total pigmentation area (%)",
    "Pigment depth / color intensity (0\u201310)",
    "Distribution region",
    "Cheekbone / cheek (sun-exposed)",
    "Diffuse whole face",
    "Jawline (hormonal patch)",
    "Pigment type",
    "Freckle (Ephelis)",
    "Solar lentigo",
    "Melasma",
    "Post-inflammatory hyperpigmentation (PIH)",
    "Seborrheic keratosis / age spot",
    "VISIA relative percentile",
    "\U0001F4CB Pigmentation Severity Grading",
    "Superficial, few scattered",
    "More visible, clear borders",
    "Dark, dense distribution",
    "Deep, diffuse confluence",
    "\u26A0\uFE0F This tool references VISIA analysis principles for assessment only. Pigment diagnosis needs dermoscopy and other professional exams; consult a dermatologist for treatment.",
    "\U0001F4DA Deep Dive: Pigmentation (VISIA) Area-Depth Assessor",
    "Pre-treatment assessment: epidermal patches lean on energy devices, dermal patches on oral / maintenance; understand why some clear fast and some slow.",
    "Efficacy quantification: measure area difference before and after treatment on the same device, using",
    "to present.",
    "Expectation management: dermal patches are hard to fully clear; aim for fading, not eradication.",
    "Mixed-patch grading",
    "Input: epidermal patches 12% of face with few dermal patches → judged mainly epidermal; energy devices primary + sun protection, dermal part as fading target.",
    "Can VISIA confirm the patch type?",
    "It helps layer classification, but the physician decides clinically.",
    "Can dermal patches be eradicated?",
    "Hard. Mostly fading improvement; don't trust 'one-time eradication'.",
    "Is this assessment a diagnosis?",
    "No. Imaging reference only; follow the physician for treatment.",
    'About "Pigmentation Area-Depth Assessor"',
    "Pigmentation (VISIA) area-depth assessor: assess facial pigmentation area and depth online and compute severity grade. A medical professional tool based on authoritative medical standards; for reference only.",
    "How to use the Pigmentation (VISIA) Area-Depth Assessor",
    "Useful for distinguishing epidermal vs dermal patches before treatment, quantifying area before/after, and setting realistic expectations of fading rather than eradication.",
    "What does the Pigmentation (VISIA) Area-Depth Assessor do?",
    "How do I use the Pigmentation (VISIA) Area-Depth Assessor?",
    "Which scenarios suit the Pigmentation (VISIA) Area-Depth Assessor?",
    "Peer comparison percentile",
]))

# ---------------- wrinkle-dynamic-static (37) ----------------
write('wrinkle-dynamic-static', build('wrinkle-dynamic-static', [
    "\U0001F9B4 Wrinkle (Crow's-feet / Frown Lines) Dynamic-Static Assessor",
    "Assess dynamic wrinkles (appear with expression) and static wrinkles (visible at rest) per facial region to guide botulinum toxin and filler planning.",
    "Wrinkle Dynamic-Static Assessor",
    "/ Wrinkle Dynamic-Static Assessor",
    '\U0001F4D6 View the "Wrinkle (Crow\'s-feet / Frown Lines) Dynamic-Static Assessor User Guide"',
    "Per-region wrinkle score (0\u20134)",
    "0=none · 1=slight · 2=mild · 3=moderate · 4=severe",
    "Dynamic wrinkles",
    "Static wrinkles",
    "Crow's-feet (outer eye corner)",
    "Frown lines (glabella)",
    "Forehead lines",
    "Nasal dorsum lines",
    "Nasolabial folds",
    "\U0001F4CB Dynamic vs Static Wrinkles",
    "Primary treatment",
    "Appear only on muscle contraction",
    "Botulinum toxin injection (first choice)",
    "Fixed lines visible at rest",
    "Filler + botulinum combined",
    "Both dynamic and static present",
    "Control dynamic with toxin first, then fill static",
    "\u26A0\uFE0F This assessor helps judge wrinkle type and treatment direction. Botulinum toxin / fillers are medical acts requiring a licensed practitioner.",
    "\U0001F4DA Deep Dive: Wrinkle (Crow's-feet / Frown Lines) Dynamic-Static Assessor",
    "Early intervention: toxin in the dynamic phase delays becoming static; understand 'early use is not overuse'.",
    "Plan tiers: deep static lines need filler / RF combined, not toxin alone.",
    "Education: help clients understand why 'the same wrinkle gets different treatments'.",
    "Frown-line dynamic/static comparison",
    "Input: deep groove on frowning, shallow groove remains at rest → judged mixed dynamic/static; suggest toxin + local collagen stimulation; toxin alone is limited on the static part.",
    "What if dynamic wrinkles are ignored?",
    "Repeated folding can gradually become irreversible static lines; early intervention is easier.",
    "Can botulinum fill static lines?",
    "Limited effect on static parts; often needs combined methods.",
    "Does this assessment set the plan?",
    "No. It only distinguishes dynamic/static; the physician sets treatment.",
    'About "Wrinkle Dynamic-Static Assessor"',
    "Wrinkle (crow's-feet / frown lines) dynamic-static assessor: assess facial dynamic and static wrinkles online and distinguish treatment direction. A medical professional tool based on authoritative medical standards; for reference only.",
]))
