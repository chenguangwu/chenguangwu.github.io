#!/usr/bin/env python3
# fitness batch1 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'analysis-retention': [
"📖 Data Analysis (Membership / Courses / Retention)",
"Membership / Courses / Retention",
"Data Analysis (Membership / Courses / Retention)",
"/ Data Analysis (Membership / Courses / Retention)",
'📖 View the "analysis-retention Guide"',
"📐 Calculation Principle",
"Enter the opening user (member) count, the closing retained count and the number of months in the period to automatically compute the overall retention rate, churn rate and monthly average churn rate, for membership / course stickiness analysis. The calculation is done locally in the browser.",
"Opening user count",
"Closing retained user count",
"Period (months)",
"📚 In-Depth Analysis: Data Analysis (Membership / Courses / Retention)",
"Aggregate a series of metrics such as monthly retention and attendance rates to quickly obtain the mean /",
"/range and judge the overall level and fluctuation.",
"Compare member retention data across stores or courses, using the median and",
"to identify abnormal stores and highly fluctuating courses.",
"During quarterly reviews, paste the daily new/churn/retention figures in to compute the totals and dispersion at once, as a basis for reviewing operational KPIs.",
"Reproducible example: 4-month retention-rate statistics",
"Enter \"72,75,68,80\" (in %). Count n=4; sum 295.00; mean 73.75; median (72+75)/2=73.50; min 68; max 80; range 12.00; variance 19.19; standard deviation 4.38. Reading: the mean 73.75% is close to the median 73.50%, indicating stable retention over the 4 months; a standard deviation of 4.38 percentage points is normal fluctuation and does not warrant overreacting to a single-month dip. If one month drops to 68 while the other three are 72-80, the range widens and the mean is pulled down; investigate that month's course or coach changes first.",
"Should variance/standard deviation use the population or sample basis?",
"This tool uses the population basis (divide by n), because the pasted data set is the entire set of metrics you want to analyse. The sample basis (divide by n−1) is slightly larger and is used to infer a population from a sample; when the two are close the conclusions agree.",
"Why look at both the mean and the median?",
"The mean is strongly affected by extreme values, while the median is not easily skewed by them. Their closeness indicates the",
"data distribution",
"is even; a mean clearly below the median indicates a low abnormal month that needs to be pinpointed.",
"Mass (Assessment / Optimisation / Improvement) Mechanism",
'About "Data Analysis (Membership / Courses / Retention)"',
"A data analysis (membership/courses/retention) tool. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
],
'angle-motion': [
"📐 Joint Angle Mechanics",
"Enter the joint angle, external moment arm and load to estimate the net joint torque and muscle force demand (a simplified biomechanical model).",
'📖 View the "Joint Angle Mechanics Guide"',
"Joint torque τ = F × r × sinθ (F = m·g); muscle force demand F",
"muscle",
"internal",
"; mechanical advantage = r",
"F is the load weight (m the mass, g = 9.81 m/s²), r the external moment arm (converted from cm to m) and θ the joint angle. The torque varies sinusoidally with the angle: at θ = 90° the moment arm and torque are maximal, and as θ approaches 0° or 180° the torque approaches zero. The muscle must produce a force F_muscle = τ / 0.05 on an equivalent internal moment arm of 5 cm to oppose this torque; a smaller mechanical advantage r_in / r means the angle requires more effort.",
"Joint angle θ (degrees, angle between the limb segment and the vertical)",
"External moment arm r (cm)",
"Load m (kg)",
"💡 Formula: joint torque τ = m·g·r·sin(θ); muscle force demand F = τ / r",
"(default muscle internal moment arm r",
"This tool is a simplified rigid-body model and does not account for limb self-weight, multi-joint coordination or muscle contraction velocity",
"The joint angle is defined as the angle between the limb segment and the gravity direction: at 90° the segment is horizontal and the torque is maximal",
"The muscle internal moment arm is estimated at 5 cm (a typical value for elbow flexion / knee extension); individual variation is large",
"Results are for reference in training-load and mechanics understanding only; for actual force output rely on a professional assessment",
"📚 In-Depth Analysis: Joint Angle Mechanics",
"When assessing the biomechanics of a movement in fitness or rehabilitation training, quantify the torque a limb segment bears at a given joint angle and the force the muscle must produce, to judge whether the load is reasonable and prone to compensation.",
"When designing a progressive-resistance programme, a physiotherapist compares the muscle-force demand at different angles such as 30°/60°/90° to determine a safe and effective training angle.",
"Understanding the mechanical advantage (insertion moment arm / limb-segment length): why exerting force near the joint is harder, guiding grip width, force point and protective-equipment selection.",
"Reproducible example: joint torque holding a load at 90°",
"Input: joint angle 90°, moment arm (segment length) 35 cm, load 10 kg. Calculation: rad=90°×π/180=1.5708, sinθ=1.0; load weight loadForce=10×9.81=98.1 N; joint torque torque=98.1×0.35×1.0=34.34 N·m; muscle force fMuscle=torque/0.05=686.7 N (about 70.0 kgf); mechanical advantage MA=0.05/0.35=14.3%; effective moment arm effArm=0.35×1.0=0.35 m. Conclusion: at 90° sinθ=1 gives the largest moment arm and torque, and the muscle must produce about 70 kgf to hold a 10 kg load; a smaller angle is easier but gives less training stimulus.",
"Why is 90° the hardest?",
"Torque = force × moment arm × sinθ; at 90° sinθ=1 gives the largest effective moment arm and joint torque, so the muscle must produce the greatest force; as the angle decreases sinθ falls and the torque decreases (easier but less stimulus).",
"How should the mechanical advantage MA be read?",
"MA = muscle insertion moment arm rIn / segment length r, with rIn fixed at 0.05 m in this tool. The longer the segment, the larger r and the smaller MA, hence the greater the effort: it shows that muscle leverage near a joint is inefficient and needs more force, and also suggests that a wider grip increases the moment arm and adjusts force efficiency.",
'About "Joint Angle Mechanics"',
"The joint angle mechanics calculator uses a rigid-body biomechanical model to estimate the net torque a joint bears and the force the muscle must produce from the joint angle, external moment arm and load, helping to understand the mechanics of training movements.",
"Computes joint torque and effective moment arm",
"Estimates muscle force demand and mechanical advantage",
"Supports visualisation of angle effectiveness",
"Strength-training movement mechanics analysis",
"Rehabilitation training-load assessment",
"Physical-education teaching and biomechanics demonstration",
"Reference for training-programme intensity design",
"Joint angle",
"External moment arm",
"Load",
],
'assessor-18': [
"📋 Core (Stability) Assessment",
"Stability",
'📖 View the "Core (Stability) Assessment Guide"',
"Core stability assessment = the sum of the graded scores of the plank + side plank + dead bug + bird dog, out of 12; for the plank, at least 120 s scores 3, at least 60 s scores 2 and at least 30 s scores 1, and similarly for the side plank.",
"Core stability assessment (4 tests, composite score)",
"1. Plank hold time (seconds)",
"2. Side plank hold time (seconds, take the shorter side)",
"3. Dead bug test (completion quality over 20 reps)",
"All completed to standard (3 points)",
"15-19 reps to standard (2 points)",
"10-14 reps to standard (1 point)",
"Fewer than 10 reps or unable to complete (0 points)",
"4. Bird dog test (10 reps per side)",
"All completed stably (3 points)",
"Occasional wobble (2 points)",
"Clearly unstable (1 point)",
"Unable to complete (0 points)",
"Assess core stability",
"📚 In-Depth Analysis: Core (Stability) Assessment",
"Self-test core stability before/after training: score the plank, side plank, dead bug and bird dog to get a total out of 12 and a grade.",
"Track the recovery of core function in rehabilitation clients, retesting periodically to compare changes in the total and grade and quantify the rehabilitation effect.",
"Identify weak movements (such as wobbling in the dead bug) to target core training and prevent lower-back injury.",
"Reproducible example: core stability scoring",
"Scoring rules: plank ≥120 s=3, ≥60 s=2, ≥30 s=1, otherwise 0; side plank ≥90 s=3, ≥45 s=2, ≥20 s=1, otherwise 0; dead bug / bird dog 0-3 by completion quality. Example: plank 90 s (2 points), side plank 60 s (2 points), dead bug 1 point, bird dog 2 points → total 7/12, pct=58.3% → grade \"Average core stability\" (40%≤pct<65%); systematic core training 3-4 times a week is recommended. If all four are full marks, 12/12=100% is \"Excellent\".",
"What ability does each of the four tests measure?",
"The plank measures anterior-core anti-extension; the side plank measures lateral-chain (obliques/quadratus lumborum) stability; the dead bug measures anti-rotation and limb coordination; the bird dog measures hip-shoulder stability with a neutral spine. The four are complementary, and a low score in one does not mean the whole is poor.",
"What score counts as a pass?",
"Out of 12: ≥85% (≥10 points) excellent, ≥65% (≥8) good, ≥40% (≥5) average, <40% insufficient; those falling short have a high injury risk and should progress gradually from basic core training, consulting a rehabilitation specialist if necessary.",
'About "Core (Stability) Assessment"',
"A core (stability) assessment tool. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
],
'assessor-63': [
"⚖️ Assessment (Quality / Optimisation / Improvement) Mechanism",
"Quality / Optimisation / Improvement",
'📖 View the "Assessment (Quality / Optimisation / Improvement) Mechanism Guide"',
"Assessment quality score = the average of scheme scientificity + item comprehensiveness + data accuracy + interpretation professionalism + recommendation actionability (each 0 to 5); at least 4.5 is excellent, at least 3.5 good and at least 2.5 average.",
"Fitness assessment quality optimisation mechanism (5 dimensions, each 1-5 points)",
"1. Assessment scheme scientificity",
"Highly scientific (5 points)",
"Fairly scientific (4 points)",
"Not scientific enough (2 points)",
"Not scientific (1 point)",
"2. Assessment item comprehensiveness",
"Fairly comprehensive (4 points)",
"Not comprehensive enough (2 points)",
"Not comprehensive (1 point)",
"3. Data-collection accuracy",
"Accurate (5 points)",
"Large error (2 points)",
"Inaccurate (1 point)",
"4. Result-interpretation professionalism",
"Professional and in-depth (5 points)",
"Not professional enough (2 points)",
"Unprofessional (1 point)",
"5. Improvement-recommendation actionability",
"Highly actionable (5 points)",
"Hard to execute (2 points)",
"Not executable (1 point)",
"📚 In-Depth Analysis: Assessment (Quality / Optimisation / Improvement) Mechanism",
"A fitness institution or coach self-assesses the scientificity, comprehensiveness, accuracy, professionalism and actionability of a training or physical-testing scheme across five quality dimensions.",
"Use the 5-dimension scoring to pinpoint scheme weaknesses (any dimension ≤2 is automatically flagged red as \"To improve\") and guide iterative optimisation.",
"Teams review the assessment-system quality, using the total score / mean as a KPI for training and process improvement.",
"Reproducible example: training-scheme quality assessment",
"Five dimensions each 1-5: scheme scientificity 4, item comprehensiveness 4, data accuracy 3, interpretation professionalism 5, recommendation actionability 4. Total 20/25, mean avg=4.0 → grade \"Good assessment quality\" (3.5≤avg<4.5). The weak dimension is data accuracy (3), listed as the improvement focus. If all five are 5, 25 points = excellent; if all 2, 10 points = poor.",
"How should the five dimensions be understood?",
"Scientificity = whether the basis is advanced and reasonable; comprehensiveness = whether key indicators are covered; accuracy = the size of the data/algorithm error; professionalism = the depth of interpretation; actionability = whether the user can put it into practice. The five together determine the scheme's credibility.",
"With a mean of 4.0, is there still anything to improve?",
"A mean of 4.0 is good, but any dimension ≤2 lowers credibility (here data accuracy of 3 is above 2 but still low). Focus on raising the 3-and-below dimensions to 4+, especially avoiding any ≤2 hard flaw.",
'About "Assessment (Quality / Optimisation / Improvement) Mechanism"',
"An assessment (quality/optimisation/improvement) mechanism tool. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
],
'assessor-64': [
"⚖️ Quality (Assessment / Optimisation / Enhancement) Mechanism",
"Comprehensive yoga-course quality assessment: score across the four dimensions of teaching staff, course content, teaching environment and student outcomes, and generate optimisation recommendations",
"/ Quality (Assessment / Optimisation / Enhancement) Mechanism",
'📖 View the "assessor-64 Guide"',
"I. Teaching staff",
"Composite score = staff ×0.25 + course content ×0.25 + teaching environment ×0.20 + student outcomes ×0.30",
"Teaching staff = certification coefficient ×0.6 + min(years of experience/10, 1)×4 (capped at 10); course content = the mean of the three scores; teaching environment = room temperature ×0.3 + humidity ×0.2 + class size ×0.25 + area per person ×0.25 (10 if met, 5-6 if not); student outcomes = (satisfaction ×0.3 + retention ×0.3 + renewal ×0.2 + progress ×0.2)/10. Grades: ≥8.5 excellent S, ≥7.5 good A, ≥6.0 fair B, ≥4.5 pass C, otherwise fail D; any single dimension < 7 is marked \"To improve\".",
"Coach certification level",
"Domestic certification",
"Teaching experience (years)",
"II. Course content",
"Curriculum completeness (1-10 points)",
"Asana sequencing scientificity (1-10 points)",
"Difficulty-level reasonableness (1-10 points)",
"III. Teaching environment",
"Room temperature (°C)",
"Humidity (%)",
"Class size",
"Studio area (m²)",
"IV. Student outcomes",
"Student satisfaction (%)",
"Student retention (%)",
"Progress-feedback rate (%)",
"Run quality assessment",
"📚 In-Depth Analysis: Quality (Assessment / Optimisation / Enhancement) Mechanism",
"A yoga studio or workshop conducts a quarterly course-quality check-up: score across the four dimensions of staff, course content, teaching environment and student outcomes to get a comparable composite score and grade.",
"Coaches self-assess or, during lesson evaluation, pinpoint weaknesses: any dimension below 7 is marked \"To improve\" with the improvement items listed automatically, avoiding fixating on the total while ignoring structural problems.",
"Environment compliance review: room temperature, humidity, class size and area per person are judged against thresholds with ✓/✗, serving as a hard basis for studio siting or scheduling.",
"Reproducible example: quality assessment of a group class",
"Input: certification RYT200-500 (cert=8), 3 years of experience; course content 7/6/8; environment room temperature 30°C, humidity 55%, class 20, studio 60 m²; student outcomes satisfaction 80, retention 70, renewal 60, progress 65. Teaching staff=0.6×8+min(3/10,1)×4=6.0; course content=(7+6+8)/3=7.0; teaching environment: room temperature 30°C not met (5), humidity 55% met (10), class size 20>15 not met (6), area per person 60/20=3.0 met (10) → 5×0.3+10×0.2+6×0.25+10×0.25=7.5; student outcomes=(80×0.3+70×0.3+60×0.2+65×0.2)/10=7.0; composite score=6.0×0.25+7.0×0.25+7.5×0.20+7.0×0.30=6.85 → displayed 6.8/10, grade \"Fair (B)\", weak points being teaching staff (6.0) and excessive room temperature. By contrast, an efficient class: cert=10, 6 years, content 9/8/9, room temperature 24°C, humidity 50%, 10 people, 60 m², outcomes 90/80/75/85 → composite 8.8/10, grade \"Excellent (S)\".",
"Why are the four dimension weights 25/25/20/30?",
"Student outcomes carries the highest weight (30%) because a course ultimately comes down to retention and satisfaction; teaching staff and course content at 25% each are the direct sources of quality; teaching environment at 20% is a necessary but relatively improvable condition. The weights can be replaced proportionally when the assessment criteria are adjusted.",
"Why is 6.85 displayed as 6.8?",
"The page uses toFixed(1) to keep one decimal, and 6.85 is slightly less than 6.85 in binary floating point, so it rounds to 6.8. This is a rounding-boundary artefact and does not affect the grade (6.0≤6.85<7.5 is fair grade B).",
"Yoga-course quality assessment should cover the four dimensions of staff, content, environment and outcomes",
"Yoga coaches should hold an RYT200 or higher certification (Yoga Alliance certification)",
"A course room temperature of 22-28°C and humidity of 40-60% with good ventilation is recommended",
"A class size of ≤15 is recommended so the coach can attend to every student",
"Student retention and repurchase rates are core commercial indicators of course quality",
"Data Analysis (Membership / Courses / Retention)",
'About "Quality (Assessment / Optimisation / Enhancement) Mechanism"',
"A comprehensive yoga-course quality assessment tool: it scores across the four dimensions of teaching staff, course content, teaching environment and student outcomes and generates optimisation recommendations and improvement plans.",
"Four-dimension yoga-course assessment",
"Coach qualification check",
"Course-effect quantification",
"Student retention analysis",
"Optimisation recommendation generation",
"Yoga studio course-quality assessment",
"Coach performance appraisal",
"Curriculum optimisation",
"Membership service enhancement",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'fitness', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
