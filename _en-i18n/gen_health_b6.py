#!/usr/bin/env python3
# health batch6 (3 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'health')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'health')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'symptom-checker': [
"✅ Symptom Self-Check Decision Tree",
"Narrow down possible conditions step by step through symptom choices and get visit advice",
"📖 View the User Guide",
"⚠️ Important notice: this tool is for reference only and does not constitute medical advice. If you feel unwell, seek medical attention promptly!",
"Select a symptom area",
"Respiratory symptoms (cough/fever/sore throat)",
"Digestive symptoms (abdominal pain/diarrhea/nausea)",
"Head symptoms (headache/dizziness)",
"Cardiovascular symptoms (chest tightness/palpitations)",
"Metabolic symptoms (excessive thirst/urination)",
"Environment-related (heatstroke/allergy)",
"Start self-check",
"📋 Self-check instructions",
"Select the area of the main symptom",
"Answer the questions step by step as prompted (2-4 options per step)",
"The system narrows the range of possible conditions based on your answers",
"Finally gives possible conditions, recommended departments and precautions",
"Conditions covered",
"Respiratory: common cold, flu, bronchitis, pneumonia",
"Digestive: acute gastroenteritis, food poisoning, gastritis",
"Head: migraine, tension headache, hypertension warning",
"Cardiovascular: angina, arrhythmia warning",
"Metabolic: diabetes warning",
"Environment: heatstroke, allergic rhinitis",
"Emergency care signals",
"Persistent high fever above 39°C that does not respond to fever reducers",
"Difficulty breathing, bluish lips",
"Severe chest pain lasting more than 15 minutes",
"Confusion, fainting",
"Severe abdominal pain with vomiting",
"Sudden severe headache (\"thunderclap\")",
"About the Symptom Self-Check Decision Tree",
"The Symptom Self-Check Decision Tree uses interactive questions to help users get a preliminary idea of which conditions a symptom may point to, and provides suggested departments and precautions for reference.",
"6 major symptom area categories",
"10+ common-condition decision trees",
"Narrow the diagnostic range step by step",
"Recommended visit departments",
"Emergency care reminders",
"Get a preliminary idea of possible causes",
"Judge whether immediate care is needed",
"Choose the right department to visit",
"📚 In-depth: Symptom Self-Check Decision Tree",
"Self-check step by step by symptom category: first pick a broad category (e.g. fever, headache, abdominal pain, cough), and the tool asks one question at a time along the decision tree, branching to the next node based on your answers until it gives the possible conditions.",
"Output possible conditions and departments: at a leaf node it shows \"possible conditions, recommended departments, precautions\", and you can one-click copy the key points on the result page for easy description at a visit.",
"Recognize emergency signals: when the path hits high-risk features (e.g. severe headache with vomiting, chest pain, breathing difficulty, impaired consciousness), the result shows a red \"🚨 Possibly urgent\" warning and advises seeking care immediately or calling 120.",
"Example: self-check starting from \"headache\"",
"Choose \"headache\" → Q&A: sudden and severe? with fever? blurred vision? Branch by answer: with fever usually points to a cold/flu; a sudden thunderclap pain needs to rule out a cerebrovascular event (flagged urgent); an ordinary migraine suggests neurology or symptomatic rest. The result page gives possible conditions + department + precautions.",
"Can a symptom self-check replace a doctor's diagnosis?",
"No. It is a preliminary triage reference based on common patterns that helps judge \"roughly which department and whether to seek care soon\", and cannot replace an in-person consultation, physical exam or tests. If symptoms worsen or persist, seek care promptly.",
"What if the result flags an emergency?",
"Seek care immediately or call 120; do not delay by observing on your own. High-risk signals (severe chest pain, breathing difficulty, impaired consciousness, sudden severe headache, etc.) may involve a life-threatening situation.",
'About the "Symptom Self-Check Decision Tree"',
"The Symptom Self-Check Decision Tree is an online health/medical tool. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
],
'vo2-max-calculator': [
"🧮 VO2 Max Calculator",
"Estimate VO2 max with several test methods to assess cardiorespiratory endurance",
"VO2 Max Calculator",
"/ VO2 Max Calculator",
"📖 View the User Guide",
"Cooper 12-minute run: VO₂max = (distance m − 504.9) ÷ 44.73",
"1.5-mile walk/run: 3.5 + 483 ÷ time (min); the Bruce protocol plugs total exercise time into a graded equation",
"Cooper 12-minute run",
"1.5-mile run",
"Bruce treadmill",
"Walking test",
"Resting heart rate method",
"👨 Male",
"👩 Female",
"1.5-mile run time (min:sec)",
"Bruce protocol total time (min:sec)",
"1-mile walk time (min:sec)",
"Post-exercise heart rate (bpm)",
"📊 Age and sex rating chart",
"Your position within your age and sex group",
"🏃 Comparison with athlete levels",
"💪 How to improve VO2 Max",
"❤️ Health benefits",
"The many health benefits of raising VO2 max",
"Cardiovascular health",
"Lowers heart disease risk",
"Cognitive function",
"Boosts brain vitality",
"Weight management",
"Efficient fat burning and weight control",
"Improves sleep depth",
"Bone health",
"Increases bone density",
"Mental health",
"Relieves anxiety and depression",
"Delays aging",
"Keeps you feeling young",
"Strengthens resistance to illness",
"Important:",
"This calculator is for reference only and cannot replace the advice of a professional doctor or coach.",
"• VO2 Max testing should be done under professional guidance",
"• VO2 max testing is high-intensity exercise and carries some risk",
"• Ensure a thorough warm-up and good physical condition before testing",
"• If you have cardiovascular disease, hypertension, etc., consult a doctor first",
"• Improving VO2 Max requires long-term systematic training, progressing gradually",
"📚 In-depth: VO2 Max Calculator",
"Cooper 12-minute run method: run as far as you can in 12 minutes, record the distance (m); VO2max = (distance − 504.9) / 44.73 (ml/kg/min). Simple and easy, often used for fitness screening.",
"1.5-mile / Bruce treadmill method: time the 1.5-mile run t (min): VO2max = 3.5 + 483/t; the Bruce treadmill uses a polynomial for the completion time t (min) (men 14.8−1.379t+0.451t²−0.012t³).",
"Resting heart rate / walking method (no running): when you cannot exercise, use the resting method: men 65.81−0.262×age−0.196×resting HR−0.483×",
"+9.05; or the walking method (with weight/heart rate/time), suitable for self-testing by the general public.",
"Example: 30-year-old man runs 2800 m in 12 minutes (Cooper)",
"VO2max = (2800 − 504.9) / 44.73 = 51.3 ml/kg/min, in the \"good-excellent\" range for adult men. The higher the value, the stronger the aerobic capacity; it is a core reference for endurance sports and cardiorespiratory health.",
"What does the VO2max value represent?",
"The maximum oxygen uptake per kilogram of body weight per minute (ml/kg/min), the gold standard of cardiorespiratory endurance. Ordinary adult men are about 35-45 and women about 30-40; high-level endurance athletes can exceed 60. It declines naturally with age.",
"How do I improve VO2 max?",
"Focus on sustained moderate-to-high-intensity aerobic exercise (running, cycling, swimming) and add interval training (e.g. 4×4 minutes of high intensity) to improve faster; regular training shows clear gains in 8-12 weeks, aided by sleep and recovery.",
'About the "VO2 Max Calculator"',
"VO2 Max Calculator. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
],
'wound-healing-time': [
"🔮 Wound Healing Time Estimator",
"Estimate the healing period by body part and wound type and get care advice",
"📖 View the User Guide",
"⚠️ This tool is for estimation reference only; actual healing time varies between individuals. Seek care promptly if a wound is abnormal.",
"Body part",
"Scalp",
"Torso (chest/abdomen/back)",
"Upper arm",
"Thigh",
"Lower leg",
"Joint area",
"Deep tissue",
"Diabetic foot",
"Wound type",
"Abrasion",
"Cut",
"Laceration",
"Burn",
"Surgical incision",
"Wound size",
"Small (< 3 cm)",
"Medium (3-10 cm)",
"Large (> 10 cm)",
"Child (0-14 years)",
"Young adult (15-35 years)",
"Middle-aged (36-55 years)",
"Older adult (56+ years)",
"Estimate healing time",
"📖 Baseline healing time by body part",
"Healing period for a medium cut in a healthy adult",
"🏥 Wound care essentials",
"Cleaning and disinfection",
"First rinse the wound with saline or clean water",
"Disinfect the skin around the wound with iodophor",
"Avoid using alcohol directly to disinfect an open wound",
"Change the dressing at least once a day",
"Factors that speed healing",
"Adequate protein and vitamin C intake",
"Keep the wound clean and moist (avoid scabbing)",
"Avoid overusing the injured area",
"Quitting smoking and drinking aids healing",
"Signals that you need medical care",
"Continuous bleeding that does not stop (> 15 minutes)",
"Worsening redness, swelling, heat and pain, or purulent discharge",
"Fever above 38°C",
"Blackened wound edges or a foul odor",
"Special groups such as diabetics and the immunocompromised",
"About the Wound Healing Time Estimator",
"The Wound Healing Time Estimator comprehensively estimates the time needed for a wound to heal based on body part, wound type, size and age, and provides targeted care advice.",
"12 body-part database",
"5 wound type analyses",
"Age correction factor",
"Personalized care advice",
"Healing-time visualization",
"Understand the approximate recovery time",
"Wound care reference for different body parts",
"Judge whether prompt medical care is needed",
"📚 In-depth: Wound Healing Time Estimator",
"Set the baseline duration by body part: the richer the blood supply, the faster the healing: face 5-10 days, scalp 7-14, torso/limbs 10-25, lower leg/foot 14-30, joints 14-28; diabetic foot 30-90 days and deep tissue 21-42 days (each multiplied by a body-part factor).",
"Adjust by wound type and size: type factors: abrasion 0.7, surgical incision 0.85, cut 1.0, laceration 1.2, burn 1.3; size: small 0.75, medium 1.0, large 1.4 (multiplied).",
"Adjust by age and split into phases: age factors: child 0.8, young adult 1.0, middle-aged 1.15, older adult 1.35. Healing is shown in four phases: inflammation (20%), proliferation (50%), epithelialization (lower bound) and remodeling (upper bound).",
"Example A: forearm cut (medium, young adult)",
"Forearm baseDays[10,18] × factor 0.95, cut 1.0 × medium 1.0 × young adult 1.0 → lower bound 10×0.95≈9.5→10 days, upper bound 18×0.95≈17.1→18 days, estimated healing in 10-18 days.",
"Example B: diabetic foot large wound (older adult, cut)",
"Diabetic foot baseDays[30,90] × factor 1.5, cut 1.0 × large 1.4 × older adult 1.35 → lower bound 30×1.5×1.0×1.4×1.35≈85→86 days, upper bound 90×1.5×1.0×1.4×1.35≈255→256 days, estimated about 86-256 days (3-8.5 months); strict glucose control and medical care are needed.",
"Why do diabetic foot wounds heal so slowly?",
"High blood sugar damages blood vessels and nerves, reduces local blood supply and immunity, markedly lowers tissue repair capacity and increases infection risk. Strict glucose control, daily foot checks and a clean wound are essential, and any wound should be seen by a doctor early.",
"How can I promote wound healing?",
"Debride and stop bleeding, keep the wound moderately moist and clean, take balanced protein and vitamin C/zinc, quit smoking and control underlying conditions (glucose/blood supply). If signs of infection appear (redness, swelling, heat, pain, discharge, fever), seek care promptly.",
'About the "Wound Healing Time Estimator"',
"The Wound Healing Time Estimator is an online health/medical tool. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
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
    print('gen_health_b6 done')
