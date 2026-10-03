#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'medical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'medical')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
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
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'medical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('dosage-calculator', build('dosage-calculator', [
        "💊 Drug Dosage Calculator",
        "\n      Calculate drug dosage by body weight or body surface area (BSA), with a built-in database of common drugs.\n    ",
        "Core formula (by input variables): √(h × w ÷ 3600)",
        "📖 Read the \"Drug Dosage Calculator Usage Guide\"",
        "By body weight (mg/kg)",
        "By body surface area (mg/m²)",
        "Dose per kg / per m²",
        "Doses per day",
        "1 time/day (QD)",
        "2 times/day (BID)",
        "3 times/day (TID)",
        "4 times/day (QID)",
        "Every 4 hours (6 times/day)",
        "By weight: dose per administration = body weight (kg) × dose per kg (mg/kg)",
        "By body surface area (Mosteller): BSA = √(height (cm) × weight (kg) / 3600)",
        "By body surface area: dose per administration = BSA (m²) × dose per m² (mg/m²)",
        "Reference: drug database",
        "Regular dose",
        "Maximum daily dose",
        "Disclaimer:",
        "This tool is for medical professionals only and the calculation results do not constitute prescription advice.\n      Actual medication must be judged holistically together with the patient's liver and kidney function, concomitant medication and allergy history.\n      Paediatric medication must strictly follow paediatric dosage specifications. Consult a clinical pharmacist or physician if in doubt.",
        "📚 In-Depth Analysis: Drug Dosage Calculator",
        "Compute single and daily doses by body weight (mg/kg), suitable for paediatric medicine and for adult drugs dosed by weight.",
        "Compute the dose by",
        "body surface area",
        "(BSA, Mosteller formula), suitable for drugs prescribed in mg/m² such as antitumour agents.",
        "Check whether the calculated daily dose exceeds the maximum daily dose in the package insert, and flag cases where paediatric dosing information is insufficient.",
        "Weight method: dose per administration = weight (kg) × dose per kg (mg/kg), daily dose = dose per administration × doses per day. Body surface area method: BSA (m²) = √(height (cm) × weight (kg) ÷ 3600) (Mosteller formula), dose per administration = BSA × dose per m² (mg/m²), daily dose = single dose × times. A warning is given when the daily dose exceeds the drug's maxDay.",
        "60 kg, 170 cm, age 30, paracetamol by weight at 10 mg/kg once daily: single dose = 60 × 10 = 600.0 mg, daily dose = 600.0 mg, below the drug's maximum daily dose of 4000 mg. The same patient switched to the body surface area method (10 mg/m²): BSA = √(170 × 60 ÷ 3600) = √2.8333 ≈ 1.68 m², single dose = 1.68 × 10 ≈ 16.8 mg, daily dose 16.8 mg. The gap in magnitude between the two methods shows the point: the dosing basis (mg/kg or mg/m²) must strictly follow the label and the two are not interchangeable — 10 mg/kg by weight for adults differs from 10 mg/m² by body surface area by about a factor of 35.",
        "When should body surface area be used instead of body weight?",
        "Cytotoxic antitumour drugs, some immunosuppressants and paediatric-specific drugs are commonly prescribed in mg/m², because body surface area correlates more strongly with basal metabolic rate, liver and kidney function and drug clearance than body weight does, which reduces dose deviation in obese or cachectic patients. Ordinary anti-infectives and antipyretic analgesics are still dosed in mg/kg or at a fixed dose. The basis of dosing is always whatever the label states.",
        "Where does the 3600 in the Mosteller formula come from?",
        "The Mosteller formula BSA (m²) = √(height (cm) × weight (kg) / 3600) is a simplified fit to the Du Bois formula (BSA = 0.007184 × height^0.725 × weight^0.425), replacing",
        "exponentiation",
        "with a",
        "square root",
        "; within normal body sizes the difference from the Du Bois result is usually below 1%-2%, which makes bedside hand calculation easy. For extreme body sizes (severe obesity, severe emaciation, extensive oedema) use a measured or more precise formula.",
        "About \"Drug Dosage Calculator\"",
        "Drug Dosage Calculator. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('calculator-calc-infusion', build('calculator-calc-infusion', [
        "🧮 Infusion Drip Rate Calculator",
        "Compute drops per minute (gtt/min) and millilitres per hour (mL/h) from the total volume, infusion time and drop factor, and check rate ceilings for special drugs.",
        "Core formula (by input variables): new Date(Date.now()+totalMin×60000); totalMin÷60; gttMin÷60",
        "📖 Read the \"Infusion Drip Rate Calculator Usage Guide\"",
        "⚠️ This tool is an auxiliary clinical calculation and the results cannot replace doctors' orders and standard prescriptions. All infusion parameters must be confirmed by a clinician/pharmacist before being carried out.",
        "Total fluid volume (mL)",
        "Infusion duration",
        "Duration unit",
        "Drop factor (gtt/mL)",
        "10 (precision blood giving set)",
        "20 (standard giving set)",
        "60 (microdrip giving set/paediatric)",
        "Drug type (rate check)",
        "Plain fluid (no special limit)",
        "Potassium chloride (KCl ≤20 mEq/h)",
        "Insulin (regular 0.1 U/kg/h)",
        "Amino acids (≤0.1 g/kg/h)",
        "3% sodium chloride (≤0.5 mEq/kg/h)",
        "Drug concentration",
        "Patient weight (kg)",
        "🧮 Calculate drip rate",
        "Drop factor and conversion formulas",
        "Drip rate (gtt/min) = total volume (mL) × drop factor (gtt/mL) ÷ infusion time (min)",
        "Flow rate (mL/h) = total volume (mL) ÷ infusion time (h)",
        "Common drop factors: standard giving set 15 or 20 gtt/mL; micro pump/paediatric 60 gtt/mL; blood giving set 10 gtt/mL",
        "Quick rule of thumb (drop factor = 20): drops per minute ÷ 3 ≈ mL/h",
        "⚠️ Infusion speed must be adjusted for the patient's cardiac function, age and the nature of the drug; slow it down in heart failure, the elderly and children.",
        "📚 In-Depth Analysis: Infusion Drip Rate Calculator",
        "After preparing the infusion, nurses convert drops per minute (gtt/min) and millilitres per hour (mL/h) from the ordered volume and duration, for setting the giving set.",
        "Recalculate the drip rate after switching drop factor (10/15/20/60 gtt/mL, where 60 corresponds to a microdrip set), so that an old rate is not carried over when the device is changed.",
        "For infusions with additives (KCl, insulin, amino acids, 3%NaCl) compute the hourly amount from the concentration and body weight and check whether it exceeds the safe infusion rate.",
        "Total minutes = duration (hours ×60 or minutes); drip rate gtt/min = volume (mL) × drop factor ÷ total minutes; flow rate mL/h = volume ÷ hours; gtt/second = drip rate ÷ 60. With a drop factor of 20 there is a quick relationship: mL/h ≈ drops/min ÷ 3. Additive safety check: hourly amount = flow rate (mL/h) × concentration (unit/mL), compared against the ceilings (KCl ≤20 mEq/h, insulin from 0.1 U/kg/h, amino acids ≤0.1 g/kg/h, 3%NaCl ≤0.5 mEq/kg/h).",
        "500 mL over 4 hours with drop factor 15: total minutes = 240; drip rate = 500 × 15 ÷ 240 = 31.25 ≈ 31 drops/min; flow rate = 125.0 mL/h; about 0.52 drops/second. Switching to a giving set with drop factor 20: drip rate = 500 × 20 ÷ 240 ≈ 42 drops/min while the flow rate stays 125.0 mL/h — at the same flow rate a larger drop factor means more drops, so changing the device requires recalculation. Additive case: if this example contains KCl at 0.4 mEq/mL, hourly potassium = 125.0 × 0.4 = 50.0 mEq/h, far above the 20 mEq/h peripheral venous safety ceiling; the tool raises an over-limit warning, so the concentration must be lowered or the infusion slowed with cardiac monitoring.",
        "Can giving sets with drop factors 15 and 20 be mixed up?",
        "The same drop count must not be carried over. The drop factor is defined as the equivalent number of drops per millilitre, so at the same flow rate a 20 gtt/mL set gives exactly 4/3 times the drops of a 15 gtt/mL set (42 drops/min vs 31 drops/min here). Mixing them up without changing the rate causes about a 25% deviation in actual flow rate, which is extremely risky for narrow therapeutic index drugs such as vasoactive drugs, insulin and potassium.",
        "Why is potassium limited per hour rather than only in total?",
        "The acute risk of intravenous potassium is a short-term rise in blood potassium triggering arrhythmia or even cardiac arrest, and the risk depends on the amount per unit time rather than the whole-day total. Peripheral veins conventionally require concentration ≤0.4 mEq/mL and rate ≤20 mEq/h (higher is possible via a central line or under cardiac monitoring); the 50 mEq/h in this example is clearly over the limit, meaning the infusion must be given over a longer time or diluted.",
        "Total fluid volume  ml",
        "Infusion duration",
    ]))

    write('calc-34', build('calc-34', [
        "⚡ Daily Calorie Needs (RER) Calculator",
        "Compute basal metabolic rate (BMR/RER) and total daily energy expenditure (TDEE) with the Mifflin-St Jeor formula, and give calorie targets for weight loss, maintenance or muscle gain.",
        "Core formula (by input variables): w÷((h÷100)×(h÷100)); tdee×0.8; tdee+400",
        "📖 Read the \"Daily Calorie Needs (RER) Calculator Usage Guide\"",
        "⚠️ This tool is only an aid to nutritional calculation and cannot replace a doctor's individualised nutrition therapy plan. For special diseases, pregnancy, children and athletes, follow a professional assessment.",
        "Sedentary (office, almost no exercise)",
        "Light (1-3 light sessions per week)",
        "Moderate (3-5 moderate sessions per week)",
        "Active (6-7 high intensity sessions per week)",
        "Very active (manual labour / professional athlete)",
        "🧮 Calculate calorie needs",
        "BMR / RER (Mifflin-St Jeor): male = 10×weight + 6.25×height − 5×age + 5; female = 10×weight + 6.25×height − 5×age − 161",
        "TDEE = BMR × activity factor (1.2 ~ 1.9)",
        "RER means resting energy expenditure, commonly used in clinical nutrition assessment, and is close to the BMR value",
        "Fat loss calories ≈ TDEE × 0.8 (about a 20% deficit); muscle gain calories ≈ TDEE + 300~500 kcal",
        "⚠️ The results are estimates; individual variation, disease state and thyroid function all affect actual energy expenditure. Weight loss is not recommended below BMR.",
        "📚 In-Depth Analysis: Daily Calorie Needs (RER) Calculator",
        "Estimate resting energy expenditure (RER/BMR) with the Mifflin-St Jeor formula, then multiply by the activity factor to get total daily expenditure (",
        "), which serves as the calorie baseline for weight management.",
        "In the fat loss phase set TDEE×0.8 to create a",
        "calorie deficit",
        ", and in the muscle gain phase set a surplus of TDEE+400 kcal, while watching",
        "grade changes at the same time.",
        "Compare the effect of different activity factors (sedentary 1.2 / light 1.375 / moderate 1.55 / active 1.725 / very active 1.9) on the target calories.",
        "Mifflin-St Jeor: male BMR = 10×weight (kg) + 6.25×height (cm) − 5×age + 5; female BMR = 10×weight + 6.25×height − 5×age − 161. TDEE = BMR × activity factor; fat loss target = TDEE × 0.8; muscle gain target = TDEE + 400; BMI = weight (kg) ÷ height (m)². The tool displays BMR directly as RER.",
        "Male 65 kg / 170 cm / age 30, sedentary (1.2): BMR = 650 + 1062.5 − 150 + 5 = 1567.5 ≈ 1568 kcal/day; TDEE = 1567.5 × 1.2 ≈ 1881 kcal; fat loss target ≈ 1505 kcal; muscle gain target ≈ 2281 kcal; BMI = 65 ÷ 1.7² ≈ 22.5, within the normal range. Compare a female 55 kg / 160 cm / age 28, moderately active (1.55): BMR = 550 + 1000 − 140 − 161 = 1249 kcal; TDEE ≈ 1936 kcal; fat loss ≈ 1549 kcal; BMI ≈ 21.5.",
        "Mifflin-St Jeor or Harris-Benedict — which should I use?",
        "Mifflin-St Jeor is based on samples closer to modern populations and is recommended as first choice by the American Nutrition and Dietetics (AND), with smaller deviation in both obese and non-obese people; the revised Harris-Benedict may overestimate by about 5% in the general population. This tool uses Mifflin-St Jeor; if you need to compare with older literature use the other formula (see the \"Resting Metabolic Rate\" tool, which gives Harris-Benedict and Katch-McArdle as well).",
        "Is a 20% calorie deficit safe?",
        "A 20% deficit (TDEE×0.8) sits in the mild fat loss range, and adequate protein plus resistance training can slow muscle loss; but staying below basal metabolic rate long term, as well as pregnancy and lactation, adolescence, or metabolic disease, calls for professional guidance rather than setting your own deficit.",
    ]))

    write('calculator-calc-2', build('calculator-calc-2', [
        "⚖️ Medication Dosage Calculator (by body weight kg)",
        "Choose a drug and enter the body weight to automatically compute the single dose in mg/kg, the daily total and the maximum daily dose check.",
        "Core formula (by input variables): (d.doseMin+d.doseMax)÷2; min(dailyDose,maxDaily); Math.round(24÷hours)",
        "📖 Read the \"Medication Dosage Calculator (by body weight kg) Usage Guide\"",
        "Age (years, optional)",
        "Dose intensity",
        "Lower bound (low dose)",
        "Median (regular)",
        "Upper bound (high dose)",
        "🧮 Calculate dose",
        "⚠️ This tool is for learning and reference only; the dose must be judged by a clinician together with the patient's liver and kidney function, allergy history and concomitant medication.",
        "Maximum daily doses differ between children and adults, and neonates/preterm infants need separate adjustment, so always check the package insert.",
        "📚 In-Depth Analysis: Medication Dosage Calculator (by body weight kg)",
        "In paediatric outpatient clinics compute the single dose and daily total by body weight (mg/kg), automatically comparing against the paediatric maximum daily dose (converted by body weight) to avoid overdosing.",
        "Switch the dosing interval (q4h/q6h/q8h/q12h/q24h) and watch how the daily total changes to judge whether a regimen would breach the daily ceiling.",
        "Switch between dose intensities (lower/median/upper) to assess the safety margin at the \"upper bound\"; when the limit is exceeded the tool gives a corrected capped regimen.",
        "Dose per administration = dose per kg (mg/kg) × weight (kg); doses per day = round(24 ÷ interval hours); daily total = dose per administration × times; paediatric maximum daily dose = per-kg daily ceiling (mg/kg) × weight, and adults (≥14 years) use the label's adult daily ceiling. If the daily total exceeds the maximum daily dose, the tool warns and gives a capped regimen: capped daily dose = maximum daily dose, capped single dose = capped daily dose ÷ times.",
        "Paracetamol, 20 kg child, median dose (12.5 mg/kg), q6h: times = 24÷6 = 4; single dose = 12.5 × 20 = 250.0 mg; daily total = 1000.0 mg; paediatric ceiling = 60 × 20 = 1200.0 mg → not over the limit, regimen 250 mg q6h. Compare amoxicillin, 20 kg, upper dose (40 mg/kg), q8h: times = 3; single dose = 800.0 mg; daily total = 2400.0 mg > ceiling 1800.0 mg → over the limit, the tool gives the corrected regimen 600.0 mg q8h (total 1800.0 mg/day). Compare ibuprofen, 20 kg, median (7.5 mg/kg), q8h: single dose 150.0 mg, daily 450.0 mg, ceiling 800.0 mg → safe.",
        "Why are children dosed by weight while adults use a fixed daily ceiling?",
        "Children's liver and kidney function and",
        "body surface area",
        "change greatly with weight, so doses are almost always converted per kg/day with a further weight-based cap; adult organ function is more stable, so the label usually gives an absolute daily ceiling directly (such as paracetamol 4000 mg/day, ibuprofen 2400 mg/day). The tool switches at age ≥14 years, but anyone whose build deviates markedly from their age group should still be dosed by actual body weight or body surface",
        "area calculation",
        "After the tool flags a limit breach, should I just adopt the capped regimen it gives?",
        "No. The capped regimen is only a mathematical even split; in practice you also need to consider dosage form (tablets cannot be split), indication, liver and kidney function and concomitant medication. A breach means the chosen dose intensity or interval is unsafe at this weight; the right move is to go back to the label or doctor's order and reselect the intensity and interval rather than mechanically dosing at the capped value.",
        "Weight  kg",
        "Age  years",
    ]))


if __name__ == '__main__':
    main()