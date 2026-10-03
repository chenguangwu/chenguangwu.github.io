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
    write('calculator-calc-due-date', build('calculator-calc-due-date', [
        "📅 Due Date Calculator (Medical)",
        "Compute the due date, current gestational age and key prenatal check milestones from the last menstrual period (LMP), the conception date or the IVF embryo transfer date, using Naegele's rule.",
        "Due Date Calculator (Last Menstrual Period)",
        "📖 Read the \"Due Date Calculator (Medical) Usage Guide\"",
        "Last menstrual period",
        "Conception date",
        "IVF transfer date",
        "Conception is about 14 days after the LMP (ovulation day). Due date = conception date + 266 days.",
        "Embryo transfer date",
        "Day 3 cleavage-stage embryo",
        "Day 5 blastocyst",
        "Day 6 blastocyst",
        "IVF due date = transfer date + 266 − embryo age. That is, LMP = transfer date − (14 + embryo age).",
        "🧮 Calculate the due date",
        "⚠️ The due date is only an estimate and the actual delivery date can differ by 1-2 weeks either way. Those with irregular cycles should correct the gestational age by early ultrasound.",
        "📚 In-Depth Analysis: Due Date Calculator (Medical)",
        "Derive the",
        "due date",
        "(EDD) from the last menstrual period (LMP) with Naegele's rule, corrected by the actual cycle length.",
        "Derive the current gestational age and trimester, and judge whether it has entered the term window (37-42 weeks).",
        "Back-calculate the estimated conception date (ovulation day) to check whether the gestational age matches ultrasound findings.",
        "EDD = LMP + 280 days (Naegele's rule, assuming a 28-day cycle with ovulation 14 days after the LMP); cycle correction: EDD = LMP + (280 + (actual cycle − 28)) days; estimated conception date = LMP + 14 days. Trimester: <14 weeks first trimester, <28 weeks second trimester, ≤42 weeks third trimester, >42 weeks post-term pregnancy; 37-42 weeks is term.",
        "LMP 2026-01-01 with a 28-day cycle: EDD = 2026-01-01 + 280 days = 2026-10-08, estimated conception date = 2026-01-15. With a 35-day cycle (later ovulation), EDD = 2026-01-01 + 287 days = 2026-10-15, 7 days later than the standard algorithm. For LMP 2026-03-01 with a 28-day cycle: EDD = 2026-12-06. Pregnancy progress is computed as \"days since LMP ÷ 280\", and past 280 days the",
        "progress bar",
        "is capped at 100%.",
        "Why is the due date often inconsistent with the actual delivery date?",
        "Naegele's rule assumes a 28-day cycle, ovulation on day 14, and a pregnancy lasting exactly 280 days. In real populations only about 5% of babies are born on the due date and about 80% fall within two weeks either side. Irregular cycles, delayed ovulation and menstruation not yet resumed after breastfeeding introduce larger error, and then early pregnancy ultrasound (CRL) should be used to verify the gestational age.",
        "How do I correct it when the cycle is not 28 days?",
        "Correct with \"EDD = LMP + 280 + (actual cycle − 28)\": a cycle shorter than 28 days moves the date earlier, a longer one pushes it later, and the difference equals the offset of ovulation relative to day 14. Note that this only corrects for ovulation timing, not for an abnormal luteal phase or a misrecorded LMP; if the ultrasound gestational age differs from the corrected one by ≥7 days (≥5 days in the first trimester), the ultrasound normally takes precedence.",
    ]))

    write('estimate-metabolism', build('estimate-metabolism', [
        "⚡ Calorie Expenditure Estimate (Resting Metabolic Rate)",
        "Compare three mainstream formulas for resting metabolic rate (RMR) and, combined with activity level, give a daily calorie target range for fat loss, maintenance or muscle gain.",
        "Core formula (by input variables): 370+21.6×lbm; w×(1-bf÷100)",
        "📖 Read the \"Calorie Expenditure Estimate (Resting Metabolic Rate) Usage Guide\"",
        "Body fat % (optional, for Katch-McArdle)",
        "🧮 Calculate metabolic rate",
        "Comparison of the three formulas",
        "Mifflin-St Jeor: the most widely used today, suitable for ordinary people. Male = 10W+6.25H−5A+5; female = …−161",
        "Harris-Benedict (revised 1984): an earlier classic formula, tends to overestimate.",
        "Katch-McArdle: RMR = 370 + 21.6×lean body mass (LBM), needs body fat %, suitable for athletes and fitness users.",
        "Targets: fat loss ≈ TDEE×0.8; maintenance ≈ TDEE; muscle gain ≈ TDEE+400; going below RMR is not recommended.",
        "⚠️ The estimates are for reference only; thyroid function, muscle mass and disease state all affect actual metabolism.",
        "📚 In-Depth Analysis: Calorie Expenditure Estimate (Resting Metabolic Rate)",
        "Estimate resting metabolic rate with both the Mifflin-St Jeor and Harris-Benedict formulas, look at the difference between methods and take the mean.",
        "When",
        "body fat %",
        "is known, add the Katch-McArdle formula (based on lean body mass) to improve accuracy for fitness users.",
        "Use the estimate as the calorie intake baseline and combine it with the activity factor to set fat loss or muscle gain targets.",
        "The three formulas",
        "Mifflin-St Jeor: male 10×weight + 6.25×height − 5×age + 5; female −161. Harris-Benedict (revised): male 88.362 + 13.397×weight + 4.799×height − 5.677×age; female 447.593 + 9.247×weight + 3.098×height − 4.330×age. Katch-McArdle (needs body fat %): lean body mass LBM = weight × (1 − body fat %), BMR = 370 + 21.6 × LBM. When body fat % is blank the mean of the first two formulas is used; once filled in the mean of the three is used.",
        "Male 65 kg / 170 cm / age 30, body fat % left blank: Mifflin = 1567.5 ≈ 1568 kcal, Harris-Benedict = 88.362 + 870.805 + 815.83 − 170.31 ≈ 1605 kcal, mean ≈ 1586.1 kcal, the two formulas differing by about 37 kcal (2.4%). Adding body fat 20%: LBM = 65 × 0.8 = 52 kg, Katch-McArdle = 370 + 21.6 × 52 = 1493 kcal, mean of the three ≈ 1555.1 kcal. Compare a female 55 kg / 160 cm / age 28, body fat 28%: Mifflin ≈ 1249, Harris-Benedict ≈ 1331, Katch-McArdle (LBM 39.6 kg) ≈ 1225, mean of the three ≈ 1268.3 kcal.",
        "Why is Katch-McArdle more trustworthy when body fat % is known?",
        "Resting metabolism comes mainly from lean body mass (muscle, organs, brain), while fatty tissue has very low metabolic activity. Katch-McArdle models lean body mass directly, so people with high body fat are overestimated by weight-based formulas and those with low body fat (more muscle) are underestimated. The premise is that the body fat figure is reliable — the bioimpedance method on body fat scales often errs by ±3-5 percentage points, and the error is amplified into the BMR, so if the body fat source is unreliable it is better to use Mifflin-St Jeor directly.",
        "Does a difference of tens of kilocalories between the three formulas matter?",
        "For planning a diet, a difference of tens of kilocalories (about 2%-3%) is smaller than the errors from weighing food, estimating the activity factor and day-to-day fluctuation (often over 10%), so there is no need to agonise over which one to use. The genuinely useful approach is to fix one formula and track the trend over time, then back-correct your real expenditure from the actual 2-4 week weight change.",
        "e.g. 20",
    ]))

    write('convert-glucose', build('convert-glucose', [
        "⚗️ Blood Glucose Unit Conversion (mmol/L ↔ mg/dL)",
        "Blood glucose mmol/L ↔ mg/dL (×18)",
        "Blood Glucose Unit Conversion (mmol/L  mg/dL)",
        "📖 Read the \"Blood Glucose Unit Conversion (mmol/L ↔ mg/dL) Usage Guide\"",
        "Blood glucose unit conversion: mg/dL and mmol/L convert according to the glucose molecular weight ratio, with a factor of about 18.0182, that is mmol/L = mg/dL ÷ 18.0182 and mg/dL = mmol/L × 18.0182.",
        "📚 In-Depth Analysis: Blood Glucose Unit Conversion (mmol/L ↔ mg/dL)",
        "Domestic lab reports commonly use mmol/L while imported glucometers and Western literature use mg/dL, so values often need to be read interchangeably.",
        "Check whether the glucometer (mostly mg/dL) agrees with the hospital biochemistry report (mostly mmol/L), avoiding unit confusion that leads to dosing errors.",
        "Learn the interpretation bands for immediate blood glucose outside glycated haemoglobin (fasting, 2-hour postprandial, hypoglycaemia threshold).",
        "Glucose",
        "Molecular weight",
        "about 180.159, so 1 mmol/L = 18.0159 mg/dL (engineering practice commonly takes 18). mmol/L → mg/dL: mg/dL = mmol/L × 18.0159; mg/dL → mmol/L: mmol/L = mg/dL ÷ 18.0159. Common equivalents: 3.9 mmol/L ≈ 70 mg/dL (lower limit of normal and the hypoglycaemia alert), 5.6 ≈ 100.9, 6.1 ≈ 110 (upper limit of normal fasting), 7.0 ≈ 126.1 (fasting threshold for diabetes diagnosis), 7.8 ≈ 140 (upper limit of normal at 2h postprandial), 11.1 ≈ 200.0 (symptomatic plus random threshold for diabetes diagnosis).",
        "Fasting glucose 5.6 mmol/L → 5.6 × 18.0159 ≈ 100.9 mg/dL, within the normal range (3.9-6.1 mmol/L / 70-110 mg/dL). Random glucose 11.1 mmol/L → × 18.0159 ≈ 200.0 mg/dL, reaching the random threshold for diabetes diagnosis. In reverse, a glucometer reading of 100.9 mg/dL → ÷ 18.0159 ≈ 5.60 mmol/L. Note that this tool is implemented as \"output = input × source unit factor ÷ target unit factor\", and the option factors are mmol/L = 1 and mg/dL = 18, so to get the mmol/L → mg/dL result you must set \"from\" to mg/dL(18) and \"to\" to mmol/L(1) (5.6 × 18 ÷ 1 = 100.8). The semantics of the select boxes are the opposite of intuition, so verify the unit by the magnitude of the output (mmol/L in single digits, mg/dL in the hundreds). The blood glucose conversion embedded in the site's \"",
        "\" uses the exact 18.0159 (5.6 → 100.9) and can be preferred.",
        "Why does the same 5.6 give 100.8 and 100.9 in different tools?",
        "The difference is factor precision: taking 18 gives 100.8, taking 18.0159 gives 100.9. Clinical interpretation is unaffected (1 mg/dL is far below the allowed glucometer error, and ISO 15197 requires ±15% or ±15 mg/dL), but when checking digit by digit against a lab report it is better to use the exact factor of 18.0159.",
        "Does it affect the diabetes diagnostic cutoffs?",
        "The cutoffs themselves do not change, but values in different units must be used as a matched set: fasting ≥7.0 mmol/L is equivalent to ≥126 mg/dL, and 2-hour postprandial ≥11.1 mmol/L is equivalent to ≥200 mg/dL. Never treat 7.0 mmol/L as 70 mg/dL (that is actually 3.9 mmol/L, already hypoglycaemic); such unit slips are among the most dangerous misreadings in home monitoring.",
        "About \"Blood Glucose Unit Conversion (mmol/L ↔ mg/dL)\"",
        "Blood Glucose Unit Conversion (mmol/L ↔ mg/dL). A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('convert-time-infusion', build('convert-time-infusion', [
        "🔄 Intravenous Infusion Drip Rate and Time Conversion (existing but enhanced)",
        "existing but enhanced",
        "📖 Read the \"Intravenous Infusion Drip Rate and Time Conversion (existing but enhanced) Usage Guide\"",
        "Intravenous infusion drip rate",
        "Milli intravenous infusion drip rate",
        "Kilo intravenous infusion drip rate",
        "Milli time conversion",
        "Kilo time conversion",
        "📚 In-Depth Analysis: Intravenous Infusion Drip Rate and Time Conversion (existing but enhanced)",
        "Given the total infusion volume and drop factor, compute the total drop count first, then convert to drops per minute over the planned duration.",
        "Convert mL/h and drops per minute to each other, to check whether the pump setting matches the actual flow rate of gravity drip.",
        "Apply decimal magnitude conversion (×1 / ×0.001 / ×1000) to the same value when switching unit magnitudes.",
        "Core infusion formulas",
        "Total drops = total volume (mL) × drop factor (gtt/mL); drops/min = total drops ÷ total infusion minutes; mL/h = volume ÷ infusion hours = drops/min × 60 ÷ drop factor. Common drop factors: standard giving set 10, 15, 20 gtt/mL, microdrip set 60 gtt/mL. With a drop factor of 15, 1 mL ≈ 15 drops, so 125 mL/h is about 31 drops/min.",
        "500 mL with drop factor 15 planned over 4 hours: total drops = 500 × 15 = 7500 drops; drops/min = 7500 ÷ 240 = 31.25 ≈ 31 drops/min; mL/h = 500 ÷ 4 = 125.0 mL/h. With drop factor 20 instead: total drops = 10000 drops, drops/min = 41.7 ≈ 42, while mL/h is still 125.0. The magnitude conversion part uses \"output = input × factor × source magnitude ÷ target magnitude\", with magnitude steps of 1 / 0.001 / 1000; for example entering 500 with factor 15, source magnitude 1 and target magnitude 0.001 outputs 7500000.000000, i.e. the total expressed in drops (7500) scaled up by 0.001 — confirm the target magnitude is what you need before using it.",
        "Once the infusion pump is set to mL/h, do you still need to count drops?",
        "With a pump, mL/h is authoritative and the drop count serves only as a back-up check during power loss or gravity drip. But when switching to a standard giving set, when the pump fails, or when gravity drip is used during transport, drops per minute must be recalculated from the drop factor. Also remember that patient position, line kinking and fluid level all make the actual flow rate of gravity drip deviate from the calculated value, so review it regularly.",
        "Where is the drop factor printed?",
        "On the outer packaging of the giving set and on the drip chamber (Chamber set), commonly marked \"20 drops ≈ 1 mL\" or \"15 gtt/mL\". Microdrip sets are 60 gtt/mL, often used in paediatrics and for vasoactive drugs. Makers and batches vary, so reconfirm every time you change the device instead of carrying over an old figure from experience.",
        "About \"Intravenous Infusion Drip Rate and Time Conversion (existing but enhanced)\"",
        "Intravenous Infusion Drip Rate and Time Conversion (existing but enhanced). A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('drug-info', build('drug-info', [
        "💊 Common Drug Quick Reference",
        "\n      Built-in information on 30+ common drugs, supporting category filtering, keyword search and favourites (stored locally).\n    ",
        "📖 Read the \"Common Drug Quick Reference Usage Guide\"",
        "Search drugs (generic name / brand name / indication)",
        "Disclaimer:",
        "The drug information in this tool is for learning and reference only and does not constitute medication advice or a basis for prescribing.\n      Indications, dosages and adverse reactions may change as guidelines are updated, so follow the latest package insert and the guidance of your physician/pharmacist for clinical use.\n      Favourite data is stored only in your local browser and nothing is uploaded.",
        "📚 In-Depth Analysis: Common Drug Quick Reference",
        "Search common drugs by category or keyword and quickly review indications, usual dosage, main adverse reactions and contraindications.",
        "Cross-check the common brand names under one generic name to avoid duplicate therapy (especially compound cold medicines containing paracetamol).",
        "Quickly confirm key contraindications before use (such as aspirin being prohibited in children, amoxicillin being prohibited in penicillin allergy).",
        "Coverage",
        "34 common drugs in 6 categories: 5 antipyretic analgesics (paracetamol, ibuprofen, aspirin, celecoxib, diclofenac), 8 antibiotics, 5 digestive system drugs, 7 cardiovascular drugs, 4 respiratory drugs, 5 nervous system drugs. Each record has nine fields — generic name, English name, category, common brand names, indications, dosage, adverse reactions, contraindications and medication notes — and can be filtered by category, searched by name or pinyin keyword, and added to favourites.",
        "Representative parameters for antipyretic analgesics: paracetamol adults 0.5-1 g per dose, every 4-6 hours, maximum 4 g per day; children 10-15 mg/kg, the main risk being hepatotoxicity, contraindicated in severe hepatic impairment and not to be combined with compound medicines containing the same ingredient. Ibuprofen adults 0.3-0.6 g per dose, every 6-8 hours, maximum 2.4 g per day, take after meals, contraindicated with gastrointestinal ulcer and in late pregnancy. Aspirin for antiplatelet use 75-100 mg per day, prohibited in children (risk of Reye's syndrome). These figures also match the dose tables built into the site's \"Medication Dosage Calculator\" \"",
        "\" and can be cross-checked.",
        "Why can't I just follow the doses in the quick reference table?",
        "The quick reference gives the usual adult dose range and does not cover individual factors such as age, weight, liver and kidney function, pregnancy and breastfeeding, concomitant medication and allergy history. For example, patients with impaired renal function need antibiotic doses adjusted by creatinine clearance, and the paracetamol ceiling must be markedly lowered in hepatic impairment. Actual medication follows the prescription, the insert and the pharmacist's check; this table is for quickly understanding a drug's position and key contraindications.",
        "How do I avoid taking the same ingredient twice?",
        "Focus on generic names rather than brand names: many compound cold and pain medicines contain paracetamol with different brand names but overlapping ingredients, so taking them together can unknowingly exceed the 4 g/day ceiling and damage the liver. Read the ingredient list before dosing, or search by generic name here and compare the brand lists; when using two or more drugs at once, have a pharmacist do a medication review first.",
        "About \"Common Drug Quick Reference\"",
        "Common Drug Quick Reference. A professional medical tool based on authoritative medical standards, for reference only.",
        "e.g.: amoxicillin / antihypertensive / headache",
    ]))

    write('stats-4', build('stats-4', [
        "🩺 Expected Surgical Duration (by Procedure)",
        "By procedure type",
        "Enter surgical durations case by case for each procedure to obtain the case count, mean duration, median, minimum and maximum; when there are at least 2 cases it also gives the standard deviation and an upper duration bound for scheduling reference. Results are for reference only when the sample is small. Data is processed locally in the browser and never uploaded.",
        "📖 Read the \"Expected Surgical Duration (by Procedure) Usage Guide\"",
        "Mean duration x̄ = Σduration ÷ case count",
        "Upper duration bound P95 ≈ x̄ + 1.645 × standard deviation",
        "Enter surgical durations case by case for each procedure to obtain the case count, mean duration, median, minimum and maximum, and when there are at least 2 cases it also gives the standard deviation and an upper duration bound for scheduling. Results are for reference only when the sample is small. All data is processed locally in the browser and not uploaded.",
        "Surgical duration records (one case per line: procedure,duration in minutes)",
        "Laparoscopic cholecystectomy,75\nLaparoscopic cholecystectomy,92\nLaparoscopic cholecystectomy,68\nLaparoscopic cholecystectomy,110\nLaparoscopic cholecystectomy,85\nLaparoscopic cholecystectomy,79",
        "Compute statistics",
        "📚 In-Depth Analysis: Expected Surgical Duration (by Procedure)",
        "Paste the historical surgical durations (minutes) for the same procedure to get the number of cases, the mean,",
        "and the dispersion, for scheduling and turnover estimation.",
        "Compare the mean with the median to judge whether a few unusually long operations are inflating the mean and disrupting turnover scheduling.",
        "Use",
        "and the range to assess the fluctuation range of durations, reserving reasonable buffer for operating room scheduling.",
        "Definitions of the statistics",
        "n; sum; arithmetic mean = sum ÷ n; median (middle value when n is odd, mean of the two middle values when even); minimum, maximum and range; population variance = Σ(x − mean)² ÷ n (note: not ÷(n−1)); standard deviation = √variance. Input accepts commas, spaces or newlines as separators.",
        "Eight operations of the same type with durations 10, 20, 30, 40, 50, 60, 70, 80 minutes: n = 8, sum 360.00, mean 45.00 minutes, median 45.00 minutes, minimum 10, maximum 80, range 70.00, variance 525.00, standard deviation 22.91 minutes. The mean equalling the median shows the distribution is symmetric, but a standard deviation of 22.91 is",
        "about 51% of the mean of 45, meaning durations for this procedure vary widely — if turnover is scheduled at the mean of 45 minutes, about half of cases will overrun, so it is better to reserve buffer at \"mean + 1 standard deviation\" or to use the upper",
        "quartile",
        "directly.",
        "Should scheduling use the mean or the median?",
        "If the distribution is roughly symmetric the two are close and either will do; if there are a few unusually long operations (right-skewed distribution) the median is more robust, but what scheduling really cares about is \"how long do most cases take to finish\" and \"how large is the overrun risk\". So the more practical approach is to schedule with the median and use the upper quartile or the mean plus 0.5-1 standard deviations as buffer, and separately identify the cause of unusually long cases (such as adhesions, complications, surgeon experience).",
        "Why is the variance here divided by n rather than n−1?",
        "Dividing by n gives the",
        "population variance",
        ", appropriate for \"treat these 8 cases as the entire population and merely describe the dispersion of this dataset\"; dividing by n−1 gives the sample variance used to infer from sample to population. This tool uses the population convention; to treat these 8 cases as a sample estimating the overall variation for this procedure, convert by n/(n−1) yourself (525.00 × 8/7 = 600.00, standard deviation about 24.49).",
        "About \"Expected Surgical Duration (by Procedure)\"",
        "Expected Surgical Duration (by Procedure). A professional medical tool based on authoritative medical standards, for reference only.",
        "Laparoscopic cholecystectomy,75",
    ]))

    write('index', build('index', [
        "🏥 Professional Medical Tools",
        "Professional medical",
        "Professional Medical Tools",
        "Due Date Calculator (Last Menstrual Period)",
        "Compute the due date, current gestational age and key prenatal check milestones from the last menstrual period (LMP), the conception date or the IVF embryo transfer date, using Naegele's rule.",
        "Choose a drug and enter the body weight to automatically compute the single dose in mg/kg, the daily total and the maximum daily dose check.",
        "Compute drops per minute (gtt/min) and millilitres per hour (mL/h) from the total volume, infusion time and drop factor, and check rate ceilings for special drugs.",
        "Enter the patient's body weight or body surface area (BSA) and choose a drug to compute single and daily doses from the built-in common drug database, assisting clinical administration (for reference only).",
        "Medical Calculator",
        "&#127973; Medical Health Calculator",
        "Blood Glucose Unit Conversion (mmol/L  mg/dL)",
        "Compute basal metabolic rate (BMR/RER) and total daily energy expenditure (TDEE) with the Mifflin-St Jeor formula, and give calorie targets for weight loss, maintenance or muscle gain.",
        "Compute the infusion drip rate (drops/min) or expected finish time from the volume, drop factor and duration, for nursing infusion checks; purely front-end calculation, not a doctor's order.",
        "Enter historical durations by procedure to get the mean and range, estimate the expected duration of this operation, for scheduling and resource preparation; purely front-end statistics for reference.",
        "Enter urine pH and dietary factors to assess urinary stone formation risk and get advice on water intake and dietary restriction, for urinary stone prevention and health management.",
        "Compare three mainstream formulas for resting metabolic rate (RMR) and, combined with activity level, give a daily calorie target range for fat loss, maintenance or muscle gain.",
        "Clinical Scoring Tools",
        "Integrates common clinical scoring scales (such as GCS); selecting parameters automatically computes the score and gives the grade and clinical advice, assisting bedside assessment and record keeping.",
        "Built-in information on 30+ common drugs, supporting category filtering, keyword search and favourites (stored locally).",
        "Record medicine names, batch numbers and expiry dates, automatically compute remaining days and sort by expiry, with green, yellow, orange and red colour-graded alerts to avoid using expired medicines.",
        "About \"Professional Medical Tools\"",
        "Professional Medical Tools collects 14 free online tools covering the common calculation, conversion and lookup needs of professional medical scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find practical small tools here that are ready to use the moment you open them. All tools run purely on the front end and data is not uploaded to the server, protecting privacy.",
        "The professional medical tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common professional medical tasks without memorising complex formulas or doing manual conversions — just enter and the result appears.",
        "Do the Professional Medical Tools need a download or registration?",
        "No. All professional medical tools on this page are purely front-end online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the Professional Medical Tools results accurate, and is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available immediately. All computation runs locally on your device, the data is never uploaded to the server, and privacy is well protected.",
    ]))


if __name__ == '__main__':
    main()