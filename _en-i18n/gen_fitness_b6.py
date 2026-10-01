#!/usr/bin/env python3
# fitness batch6 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'rater-time': [
"📋 Foam Rolling Duration and Tenderness Rating",
"Enter the target muscle group, tenderness level (VAS 0–10) and session length to get pressure, hold time, sets and frequency advice following myofascial release principles.",
'📖 View the "Myofascial Release Pressure Scoring (Tenderness Grading + Duration Assessment) Guide"',
"Recommended duration = 60 s (tenderness 0–2) / 90 s (3–5) / 120 s (6–7) / 60 s (≥8); assessment: actual < 0.6×recommended too short, 0.6–1.5×recommended appropriate, > 1.5×recommended too long",
"The tenderness VAS band gives the recommended duration for a single foam-rolling session, and the ratio of the actual duration to the recommended range then judges whether it is sufficient. Tenderness ≥6 prompts reducing pressure and prioritising around the painful point; ≥8 prompts stopping deep pressure and seeking medical advice as appropriate.",
"Target muscle group",
"Triceps surae (gastrocnemius/soleus)",
"Latissimus dorsi",
"Upper back (paraspinal muscles)",
"Iliotibial band (IT band)",
"Shoulder muscles",
"Tenderness level (VAS 0–10, 0 no pain / 10 severe pain)",
"Session length (seconds per site)",
"Generate release plan",
"📚 In-Depth Analysis: Myofascial Release Pressure Scoring (Tenderness Grading + Duration Assessment)",
"Before and after foam rolling / using a massage gun, self-rate the target area's tenderness on 0–10 to get a tightness grade and a release plan.",
"Gives advice on pressure, rolling / single-point hold time, sets and frequency based on the tenderness level.",
"Assesses whether this session's duration falls in the recommended range, flagging both too long and too short.",
"Reproducible example: quadriceps, tenderness 5/10, 60 seconds of release",
"Input: site=quadriceps, tenderness 5, session length 60 seconds.\npainInfo(5)=moderate tightness (warning); plan(5)=medium pressure, roll 60–90 seconds, single-point hold 30–45 seconds, 2 sets, 1–2 times a day.\nRecommended single-point duration recSec: p=5 falls in the p≤5 band → 90 seconds; assessment range=90×0.6~90×1.5=54~135 seconds.\nThis 60 seconds falls in [54,135] → appropriate, within the recommended range (success).\nConclusion: quadriceps moderately tight — medium-pressure rolling with a 30–45 second single-point hold is suggested; this 60-second session is appropriate. Tenderness ≥6 prompts reducing pressure, and ≥8 prompts a possible acute injury requiring medical advice.",
"Does higher tenderness mean pressing harder?",
"The opposite. Tenderness ≥6 means reducing pressure, shortening the single-point hold and pressing lightly around the painful point; ≥8 indicates severe tenderness and suggests stopping, icing, and checking for strain or inflammation. Release is about loosening, not toughing out pain.",
"How long should a release session be?",
"The recommended single-point duration varies with the tenderness level: about 60 seconds at ≤2, about 90 seconds at ≤5, about 120 seconds at ≤7. Keeping the total release duration at 0.6–1.5× the recommended value is best; too short under-releases, too long easily over-stimulates and worsens soreness.",
"The tenderness level uses the VAS visual analogue scale (0 no pain, 10 severe pain) to judge myofascial tightness",
"Foam rolling should be mildly painful but tolerable; the higher the tenderness, the more you should reduce pressure and lengthen the single-point hold",
"Do not roll over acute injuries, red/swollen/hot areas, osteoporotic bone or broken skin; consult a professional physician",
"This tool runs entirely in the front end and uploads no data to a server; the advice is for training-support reference only",
'About "Foam Rolling Duration and Tenderness Rating"',
"The foam rolling duration and tenderness rating tool gives a personalised myofascial release plan — pressure, single-point hold, rolling duration, sets and frequency — based on the VAS tenderness level and the target muscle group's characteristics. It runs entirely in the front end and uploads no data.",
"VAS tenderness rating",
"Separate advice for 8 major muscle groups",
"Personalised release plan",
"Duration-sufficiency assessment",
"Post-training myofascial release",
"Self-treatment of trigger points",
"Active release on recovery days",
"Support for sports rehabilitation",
],
'ratio-19': [
"🏋️ Muscle Symmetry Measurement",
"Enter the left and right upper arm, thigh and calf girth to compute each site's symmetry difference and an overall score, assessing how balanced your muscle development is.",
'📖 View the "Limb Girth Symmetry Score (Left/Right Difference Analysis) Guide"',
"Average girth = (left + right) / 2; difference = |left − right|; difference% = difference / average × 100; symmetry score = max(0, 100 − difference%); overall score = mean symmetry score across sites",
"For the upper arm, thigh and calf, compute the left-right difference percentage site by site and convert it into a symmetry score (the larger the difference, the lower the score). A difference > 5% is flagged and > 10% is warned; overall score ≥98 excellent, ≥95 good, ≥90 fair, otherwise needs improvement.",
"Left upper arm (cm)",
"Right upper arm (cm)",
"Left thigh (cm)",
"Right thigh (cm)",
"Left calf (cm)",
"Right calf (cm)",
"💡 difference% = |left−right| ÷ average × 100; symmetry score = 100 − difference%. A difference >10% indicates marked asymmetry.",
"Measure with muscles relaxed, at the same anatomical point and with the same tape tension",
"The dominant arm is usually 1-2 cm thicker, which is normal",
"A difference >10% may indicate training imbalance or injury history; strengthening the weaker side is recommended",
"Girth symmetry does not equal strength symmetry; combine it with single-side strength tests",
"📚 In-Depth Analysis: Limb Girth Symmetry Score (Left/Right Difference Analysis)",
"In rehabilitation/posture assessment, compare left and right limb girth (upper arm/thigh/calf) to quantify the degree of asymmetry.",
"After strength training or injury follow-up, monitor whether the girth difference between the two sides shrinks.",
"A difference >10% suggests possible compensation, atrophy or one-sided weakness and needs attention.",
"Reproducible example: upper arm 33/33.5, thigh 55/55.5, calf 37/37 cm",
"Input: upper arm left 33, right 33.5; thigh left 55, right 55.5; calf left 37, right 37 (units cm).\nUpper arm: mean 33.25, difference 0.5, difference%=0.5/33.25×100=1.50%, symmetry score=100−1.50=98.5.\nThigh: mean 55.25, difference 0.5, difference%=0.91%, symmetry score=99.1.\nCalf: difference 0, symmetry score=100.\nOverall=(98.5+99.1+100)/3=99.2 → grade excellent (≥98); sites with difference >10%: 0.\nConclusion: all three girths differ by less than 2% left to right, overall symmetry score 99.2 (excellent), with no significant asymmetry.",
"What symmetry score counts as normal?",
"Overall symmetry score ≥98 excellent, ≥95 good, ≥90 fair, <90 needs improvement. A single-site difference% >5% is flagged yellow and >10% is warned red. In ordinary people the left-right difference is usually 1–3%, and >10% often suggests one-sided atrophy or compensation, so it is best judged together with a strength test.",
"What should I watch out for when measuring?",
"Take the same anatomical point for each site (e.g. the thigh 10 cm above the patella) and measure the same limb standing relaxed; congestion after meals/training temporarily enlarges girth, so measuring at a fixed time (e.g. on waking) is recommended for comparability.",
'About "Muscle Symmetry Measurement"',
"By comparing left and right upper arm, thigh and calf girth, it computes each site's symmetry difference and an overall score, helping you spot imbalances in muscle development.",
"Left-right girth comparison for three sites",
"Quantified difference percentage",
"Overall symmetry score",
"Automatic flagging of abnormal differences",
"Bodybuilding physique assessment",
"Tracking symmetry in rehabilitation training",
"Prioritising training for the weaker side",
"Recording physical-test data",
"Left upper arm",
"Right upper arm",
"Left thigh",
"Right thigh",
"Left calf",
"Right calf",
],
'reminder': [
"⏰ Water Intake Reminder Timer",
"Set a daily hydration goal, get periodic reminders to drink, and log each drink, with data stored locally.",
"Water Intake Reminder Timer (with local storage)",
'📖 View the "Water Reminder Schedule (Generated from Goal and Interval) Guide"',
"ml half cup",
"ml cup",
"ml large cup",
"ml bottle",
"Custom drink amount (ml)",
"Undo last",
"Clear today",
"⚙️ Goal and reminder settings",
"Daily goal (ml)",
"Reminder interval (minutes)",
"Enable reminders",
"Reminders off",
"Completion % = min(100, round(daily cumulative intake / daily goal × 100)); remaining = goal − cumulative",
"The daily goal is adjustable (default 2000 ml); each logged drink accumulates and updates the progress, the ring progress bar is coloured by the completion rate, and reminders come at the set interval (default 60 minutes). All records are stored locally in the browser.",
"📋 Today's water log",
"📅 Last 7 days stats",
"Browser notifications require permission, and the page must stay open for reminders to trigger",
"Daily records are stored by local date, and a new day starts automatically after midnight",
"A daily intake of 1500-2000 ml is recommended; adjust it to your body weight and activity level",
"📚 In-Depth Analysis: Water Reminder Schedule (Generated from Goal and Interval)",
"From the daily goal and the single-drink amount, generate",
"evenly spaced",
" multi-cup drinking reminder schedule.",
"Desk workers and gym-goers can use fixed-interval reminders to avoid gulping it all at once or being dehydrated all day.",
"Adjust the total goal and reminder frequency for the extra hydration needs on training days.",
"Reproducible example: goal 2000 ml, 250 ml each time, 60-minute interval",
"Input: 250 ml per drink, daily goal 2000 ml, interval 60 minutes.\nCups per day=goal/per-drink=2000/250=8 cups; starting from the first cup, one every 60 minutes, the coverage=(8−1)×60=420 minutes≈7 hours.\nIf the first cup is at 08:00, the reminders are 08:00/09:00/…/14:00, 8 in total.\nConclusion: a 2000 ml daily goal needs 8 drinks of 250 ml, about one per hour, completed within 7 hours.",
"Must I drink 2000 ml every day?",
"2000 ml is a general reference; actual needs vary with body weight, temperature and activity level (often 30–35 ml/kg). With heavy exercise or hot weather it can reach 3000 ml+; people who restrict fluids (kidney disease, heart failure, etc.) should follow medical advice and not apply this table.",
"Is drinking a lot at once different from drinking in portions?",
"Smaller, more frequent drinks are better for absorption and kidney regulation, avoiding a sudden dilution of the blood and frequent urination; during exercise it is also advisable to drink 150–200 ml every 15–20 minutes rather than gulping when thirsty.",
'About "Water Intake Reminder Timer"',
"Set a daily hydration goal and reminder interval, log each drink with one tap, see the achievement rate in a ring progress display, get periodic reminders via browser notifications, and view the last 7 days' stats at a glance.",
"Ring progress showing the achievement rate",
"One-tap logging of common amounts",
"Timed reminders via browser notification",
"Daily records stored locally",
"Last 7 days hydration stats",
],
'resistance': [
"⚡ Bioelectrical Impedance Body Fat Estimator (BIA)",
"Based on bioelectrical impedance analysis (BIA), estimate total body water and fat-free mass from the impedance index, then derive body-fat percentage.",
"Body Fat Resistance Estimate",
"/ Body Fat Resistance Estimate",
'📖 View the "Body Fat Bioimpedance Estimate (BIA Formula) Guide"',
"Impedance index = height² / impedance Z; total body water TBW = 1.20 + 0.45×index + 0.18×weight; fat-free mass FFM = TBW / 0.732 (capped at 0.95×weight); body fat % = (weight − FFM) / weight × 100",
"Bioelectrical impedance analysis (BIA): compute the impedance index from height squared and impedance, then estimate total body water from the regression, back out fat-free mass (FFM) using the ~73.2% water fraction of lean tissue, and finally obtain body-fat percentage and fat mass. Results are rated by sex; before measuring, avoid strenuous exercise and heavy water intake to reduce error.",
"Bioelectrical impedance Z (Ω)",
"💡 Sun et al. (2003) BIA: total body water TBW = 1.20 + 0.45×(H²/Z) + 0.18×W; fat-free mass FFM = TBW ÷ 0.732.",
"BIA is strongly affected by hydration status: alcohol, exercise, menstruation and dehydration all change the reading",
"Measure on waking after emptying your bladder, fasted; comparing trends at a fixed time is more reliable",
"Higher impedance usually means higher body fat (water conducts, fat has high impedance)",
"This formula is an estimate for the adult population and does not apply to pregnant women or patients with oedema",
"📚 In-Depth Analysis: Body Fat Bioimpedance Estimate (BIA Formula)",
"Use the impedance value from a body-fat scale / impedance meter, combined with height and weight, to estimate",
"body-fat percentage",
", fat-free mass and total body water.",
"When monitoring body-composition changes at home, track the trend on the same device at the same time of day.",
"Outputs a body-fat rating (essential fat / athlete / healthy / acceptable / obese) to aid judgement.",
"Reproducible example: man, 30 years, 175 cm, 70 kg, impedance 450 Ω",
"Input: male, 30 years, height 175 cm, weight 70 kg, impedance 450 Ω.\nImpedance index H²/Z=175²/450=30625/450=68.1 cm²/Ω.\nTotal body water TBW=1.20+0.45×68.1+0.18×70=1.20+30.6+12.6=44.4 L.\nFat-free mass FFM=TBW/0.732=44.4/0.732=60.7 kg (≤ weight, valid).\nBody fat %=(70−60.7)/70×100=13.3%; men <14 → grade athlete.\nFat mass=9.3 kg; water share of body weight=44.4/70×100=63.5%.\nConclusion: this man's body-fat percentage is about 13.3% (athlete level), with FFM 60.7 kg and TBW 44.4 L.",
"Is the BIA estimate accurate?",
"BIA is affected by hydration (drinking/sweating), meals and the time of measurement, with an error usually of ±3–5%. Measuring barefoot at a fixed time on waking after emptying the bladder is recommended; this formula is an empirical regression for trend reference only, and medical-grade body fat should be measured by DEXA/underwater weighing.",
"What does the impedance index H²/Z represent?",
"Height squared divided by impedance reflects how much conductive tissue (lean body water) the body has: a higher index usually means more lean mass and lower body fat. It is the core intermediate quantity for converting BIA into TBW and FFM, and the body-fat grading thresholds differ by sex/age.",
'About "Body Fat Resistance Estimate"',
"Bioelectrical impedance analysis (BIA) uses the difference in conductivity between fat and water to estimate body composition. This tool is based on the Sun et al. (2003) formula, estimating total body water and fat-free mass from the impedance index.",
"Sun (2003) BIA formula",
"Automatic impedance-index calculation",
"Body-fat percentage and composition breakdown",
"Body-fat rating",
"Interpreting body-fat scale data",
"Converting data from BIA devices",
"Tracking body composition during fat loss",
"Reference for body-composition research",
"Height",
"Bioelectrical impedance",
],
}

EXTRA = {
}

def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(en)); sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'fitness', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, slug + '.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
