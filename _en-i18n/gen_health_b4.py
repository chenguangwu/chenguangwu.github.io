#!/usr/bin/env python3
# health batch4 (3 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'health')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'health')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'pregnancy-due-date': [
"📅 Due Date Calculator (Health)",
"Supports multiple methods and details the week-by-week changes of pregnancy",
"Due Date Calculator",
'📖 View the "Due Date Calculator User Guide"',
"Naegele's rule: due date = last menstrual period + 280 days",
"or ovulation day + 266 days; the ultrasound method back-calculates and corrects from the gestational age at the scan date",
"Last menstrual period",
"Ovulation / conception date",
"Ultrasound gestational age",
"IVF transfer date",
"For regular menstrual cycles (about 28 days)",
"Ovulation day determined by basal body temperature, ovulation test strips or ultrasound monitoring",
"Ultrasound scan date",
"Ultrasound gestational weeks (weeks)",
"Ultrasound extra days (days)",
"A first-trimester ultrasound (before 12 weeks) estimates the due date most accurately",
"Transfer date",
"Day-3 embryo (D3)",
"Day-5 blastocyst (D5)",
"Day-6 blastocyst (D6)",
"Estimate the due date from the IVF transfer date",
"📅 Gestational week calendar",
"First trimester (weeks 1-13)",
"Second trimester (weeks 14-27)",
"Third trimester (weeks 28-40)",
"🏥 Key prenatal checkup schedule",
"⚖️ Estimated fetal weight",
"BPD biparietal diameter (cm)",
"FL femur length (cm)",
"📊 Pregnancy month and gestational week chart",
"Disclaimer:",
"This calculator's results are for reference only and cannot replace a professional doctor's diagnosis and advice. The actual due date may differ from the result by 1-2 weeks; please follow your doctor's assessment. If you feel unwell at any time during pregnancy, seek medical attention promptly.",
"📚 In-depth: Due Date Calculator (Health)",
"Last menstrual period (LMP) method: if you remember the first day of your last period, use Naegele's rule directly: due date = LMP + 280 days (40 weeks). This is the most common method.",
"Ovulation / early ultrasound method: if the ovulation day is confirmed by test strips or ultrasound, due date = ovulation day + 266 days; a first-trimester ultrasound (before 12 weeks) back-calculates the LMP from the gestational age and then adds 280 days, giving a smaller error.",
"IVF method: calculated from the embryo transfer date: a day-5 blastocyst (D5) gives due date = transfer date + (266 − 5) = transfer date + 261 days; a day-3 embryo (D3) gives +263 days.",
"Example: LMP 2026-01-01",
"LMP = 2026-01-01, due date = 2026-01-01 + 280 days = 2026-10-08 (2026 is a common year; the 280th day from 1/1 is 10/8). The current gestational age is calculated in real time as (today − LMP)/7,",
"progress bar",
"showing the proportion of the 40 weeks at the same time.",
"Why can the due date be off by 1-2 weeks?",
"Naegele's rule assumes a 28-day cycle with ovulation on day 14; real ovulation-day variation makes the due date vary by ±1 week. Ultrasound (especially early) can narrow the error to ±3-5 days. The due date is an \"estimated range\", not an exact date.",
"How do I calculate with an irregular cycle?",
"When the cycle is longer or shorter or irregular, LMP alone has a large error; it is better to recalculate using an early ultrasound (CRL crown-rump length) or a confirmed ovulation day (ultrasound/test strips).",
'About the "Due Date Calculator"',
"Due Date Calculator. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
"Optional",
],
'pregnancy-weight-gain': [
"⚖️ Pregnancy Weight Gain Recommendation Calculator",
"/ Pregnancy Weight Gain Recommendation Calculator",
"📖 View the User Guide",
"Pre-pregnancy BMI = weight (kg) ÷ height (m)²",
"Per IOM 2009: underweight 12.5-18 kg, normal 11.5-16 kg, overweight 7-11.5 kg, obese 5-9 kg (with weekly gain ranges for the second and third trimesters)",
"📚 In-depth: Pregnancy Weight Gain Recommendation Calculator",
"By pre-pregnancy",
"gain range: using the US Institute of Medicine IOM 2009 standard: underweight (BMI<18.5) total gain 12.5-18 kg; normal (18.5-24.9) 11.5-16 kg; overweight (25-29.9) 7-11.5 kg; obese (≥30) 5-9 kg.",
"Check the weekly gain rate in the second and third trimesters: total gain in the first trimester (first 3 months) is about 0.5-2 kg; afterwards control the weekly gain: about 0.35-0.50 kg/week for normal BMI, 0.44-0.58 for underweight, 0.23-0.33 for overweight and 0.17-0.27 for obese.",
"Estimate cumulative gain by current week: entering the current gestational week back-calculates roughly how much should have been gained: cumulative ≈ first-trimester base + weekly gain × (current week − 13), helping judge whether the rate is too fast or too slow.",
"Example: height 165 cm, weight 55 kg, currently 20 weeks",
"BMI = 55 / 1.65² = 20.2 (normal) → recommended total gain 11.5-16 kg, weekly gain 0.35-0.50 kg in the second and third trimesters. Estimated cumulative gain at 20 weeks ≈ 2 (first trimester) + 7 × (0.35~0.50) = 4.45~5.5 kg, within the reasonable range.",
"Are the gain standards the same for twins/multiples?",
"No. The IOM recommends higher gains for twins: normal BMI 16.8-24.5 kg, overweight 14.1-22.7 kg, obese 11.3-19.1 kg. This tool uses singleton standards; for multiples follow your doctor's advice.",
"Is gaining weight fast bad?",
"Gaining too fast (e.g. far above the weekly upper limit) warrants caution about gestational hypertension/diabetes risk; gaining too slowly may indicate nutritional or fetal growth problems. The figures are for reference only; rely on prenatal fundal height and ultrasound assessment.",
"BMI = pre-pregnancy weight (kg) ÷ height² (m²)",
"Based on the IOM 2009 \"Weight Gain During Pregnancy\" guideline: underweight 12.5-18 kg, normal 11.5-16 kg, overweight 7-11.5 kg, obese 5-9 kg",
"This tool is a general reference; twins, advanced maternal age and comorbidities require individualized assessment",
"The results do not constitute medical advice; please follow your prenatal doctor's guidance",
],
'premature-age-calculator': [
"👶 Corrected Age Calculator for Preterm Infants",
"Calculate corrected age from birth date and due date, and view development reference ranges",
"📖 View the User Guide",
"Preterm days = (40 − gestational weeks at birth) × 7 − gestational days; due date = birth date + preterm days",
"Corrected age (months) = (today − due date in days) ÷ 30.44; corrected age (weeks) = corrected days ÷ 7",
"📌 Corrected age = actual age − premature weeks, used to assess whether a preterm infant's growth and development meet expectations.",
"Enter due date",
"Enter gestational weeks",
"Due date (EDD)",
"Gestational weeks at birth",
"Extra days",
"Calculate corrected age",
"📏 Corrected-age growth reference",
"Height, weight and head-circumference reference ranges based on corrected age (simplified WHO standard)",
"📖 Preterm development catch-up guide",
"What is corrected age?",
"Corrected age (also called adjusted age) is the age calculated from the due date rather than the actual birth date. For preterm infants, corrected age is usually used to assess development during the first 2 years.",
"Development catch-up timeline",
"Weight: most preterm infants catch up with peers within 6-12 months",
"Height: usually caught up within 12-24 months",
"Head circumference: generally caught up within 12-18 months",
"Motor development: assessed by corrected age, usually caught up by age 2",
"Language and cognition: assessed by corrected age, most catch up before age 3",
"Situations that need attention",
"Still more than 2 standard deviations behind for corrected age",
"No catch-up trend after more than 3 months",
"Markedly delayed motor-development milestones",
"Feeding difficulties and slow weight gain",
"About the Corrected Age Calculator for Preterm Infants",
"The corrected-age calculator for preterm infants helps parents quickly compute their baby's corrected age and compare it with growth references for full-term babies of the same age, so they can track catch-up progress.",
"Supports both due-date and gestational-week inputs",
"Automatically calculates corrected age and preterm days",
"Visualizes development catch-up progress",
"0-36 month growth reference table",
"Catch-up timeline guide",
"Assess the baby's development regularly",
"Prepare before a pediatric visit",
"Record the development catch-up process",
"📚 In-depth: Corrected Age Calculator for Preterm Infants",
"Given the",
"due date",
" (EDD): enter the baby's actual birth date and due date; corrected age = (today − due date)/30.44 months, used to compare development with full-term babies on the same standard.",
"Given gestational weeks/days at birth: without a due date, use the gestational weeks + days at birth: preterm days = (40 − weeks) × 7 − days, EDD = birth date + preterm days, then compute the corrected age.",
"Assess catch-up progress: compare the corrected age against the WHO growth curves (0-36 months) and compute the catch-up",
" = corrected age / actual age, to judge whether the child catches up within 2 years.",
"Example: born 1 January, due date 1 April, today 8 September",
"Preterm days = 4/1 − 1/1 ≈ 90 days (about 12.9 weeks, i.e. born around 29 weeks). Actual age = (9/8 − 1/1)/30.44 ≈ 8.3 months; corrected age = (9/8 − 4/1)/30.44 ≈ 5.2 months; catch-up progress = 5.2/8.3 ≈ 63%.",
"Why use corrected age for preterm infants?",
"Preterm infants are born early, so their organs and physique have not finished developing in the womb. Using corrected age (counted from the due date) allows a fair comparison with full-term growth milestones and avoids misjudging \"developmental delay\".",
"Until what age is corrected age used?",
"Usually until age 2-3. Most preterm infants catch up in physique (weight/height/head circumference) within 2 years; motor, language and cognition also mostly approach peers before age 3. Afterwards, actual age can be used directly.",
'About "Corrected Age Calculator for Preterm Infants"',
"The corrected-age calculator for preterm infants is an online health/medical tool. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
],
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
        if it.get('src_diff') and it.get('zh_src'):
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
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'health', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_health_b4 done')
