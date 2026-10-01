#!/usr/bin/env python3
# fitness batch4 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'fitness')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'fitness')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'circuit-timer': [
"⏱️ Circuit Training Timer",
"HIIT / circuit training timer with custom work, rest and round settings and automatic interval switching reminders",
'📖 View the "Circuit Training Timer Guide"',
"Work duration (seconds)",
"Rest duration (seconds)",
"Ready countdown (seconds)",
"Round 0 / 8",
"📋 Common training plans",
"Training",
"High-intensity fat burn",
"Classic HIIT",
"General fitness",
"Strength circuit",
"Beginner",
"Gradual adaptation",
"Round duration = work duration + rest duration; total training time = (work duration + rest duration) × rounds; total including preparation = total training time + preparation duration",
"For example, work 40 s, rest 20 s, 8 rounds, preparation 10 s: round duration 60 s, total training time 60×8 = 480 s (8 minutes), 490 s including preparation. The timer automatically switches between work and rest for each segment and tracks the cumulative training minutes.",
"Note: keep good form during work and recover actively during rest (slow walking, deep breathing). Do a 5-minute stretch at the end to aid recovery.",
"📚 In-Depth Analysis: Circuit Training Timer",
"During Tabata / circuit training (HIIT), automatically count down by work + rest rounds",
"countdown",
", freeing your hands from watching the clock.",
"Plan the total duration of a session: round duration × rounds + ready countdown, making it easy to fit into your schedule.",
"Adjust work/rest/rounds to suit different levels (longer rests for beginners, shorter rests and more rounds for advanced users).",
"Reproducible example: total duration of 40/20 × 8 rounds",
"Input: work workSec=40, rest restSec=20, rounds rounds=8, preparation readySec=10.\nRound duration=workSec+restSec=40+20=60 s.\nTotal training time=(workSec+restSec)×rounds=60×8=480 s=8 minutes.\nIncluding the ready countdown=480+10=490 s≈8 min 10 s.\nConclusion: this 8-round circuit is 8 minutes of net training, plus 10 seconds of preparation before starting, finishing in about 8 min 10 s overall.",
"How should I set rounds and duration?",
"For beginners, 20-30 s work + 20-30 s rest for 6-8 rounds; for advanced, 40 s work + 15-20 s rest for 8-12 rounds. Total training time ≈ (work+rest)×rounds, so you can work backwards from your schedule.",
"Can I skip a stage?",
"The timer supports skipping the current stage and moving straight to the next phase (ready → work → rest → done) for on-the-fly adjustments; the cumulative stats record the training sessions and minutes actually completed.",
'About "Circuit Training Timer"',
"The Circuit Training Timer is an online tool in the health and medical field. A health-metric calculator based on authoritative medical standards, processing data locally to protect privacy.",
],
'convert': [
"🏃 Running Pace (Minutes per Kilometre) Converter",
"Running pace minutes/km ↔ minutes/mile (1 mi = 1.609344 km)",
'📖 View the "Running Pace Converter Guide"',
"Fitness unit conversion: result = input value × source unit factor ÷ target unit factor; common relations: 1 kilogram = 2.20462 pounds, 1 kilometre = 0.621371 miles, 1 inch = 2.54 centimetres.",
"Minutes / km",
"Minutes / mile",
"📚 In-Depth Analysis: Running Pace Conversion (min/km ↔ min/mile)",
"When reading overseas",
"training plans",
" (which usually label pace in minutes per mile), convert it to the minutes per kilometre commonly used domestically.",
"Compare your pace over different distances such as 5 km and 10 km, using a single unit to assess progress.",
"Convert the mile pace from a track or running watch into kilometre pace to make pacing easy.",
"Reproducible example: converting 5 min/km into mile pace",
"Conversion relation: 1 mile = 1.609344 km, factor f(kilometre)=1, t(mile)=1.609344.\nFormula r=v×f/t. Input v=5 min/km: r=5×1/1.609344=3.106 min/mile.\nReverse: 3.106 min/mile → km: r=3.106×1.609344/1=5.000 min/km.\nConclusion: 5 min/km ≈ 3 min 6 s/mile; the tool processes the result with toPrecision(12), so the reverse conversion restores the value losslessly.",
"Why use 1.609344?",
"1 mile = 1609.344 m = 1.609344 km, the exact international conversion factor; the tool uses it to convert pace linearly, with error coming only from display rounding.",
"Can it convert pace into speed?",
"This tool only converts between pace units (min/km ↔ min/mile). To get km/h, use 60 ÷ minutes-per-kilometre, for example 5 min/km = 12 km/h, which is simple mental arithmetic and outside the scope of this tool.",
'About "Running Pace (Minutes per Kilometre) Converter"',
"Running pace (minutes per kilometre) converter. A free online tool that runs entirely in the front end, uploading no data and protecting your privacy.",
],
'cycle-5': [
"📖 Personal Training Cycle Planner",
"Create personal training courses, schedule weekly sessions, check in completed sessions, and report the completion rate with a monthly calendar view.",
"/ Personal Training Schedule",
"Personal Training Cycle (Week/Month) Planner",
'📖 View the "5-Day Training Cycle Plan and Check-In Guide"',
"Coach",
"Sessions per week",
"Add course",
"🗓️ This week's training schedule (click to check in)",
"‹ Last week",
"This week",
"Next week ›",
"Clear check-ins",
"📊 Completion progress",
"📅 Calendar view",
"After adding a course, click + Schedule in the corresponding day cell of this week's training schedule to set a fixed weekly time slot for the course",
"Click a scheduled slot card to check in or undo the check-in; check-in records are saved by date",
"All data is stored locally in the browser and is not uploaded to a server",
"📚 In-Depth Analysis: 5-Day Training Cycle Plan and Check-In",
"Plan a week's training schedule (e.g. strength, cardio and stretching on different days), arranged in the calendar view and colour-coded.",
"Check in on the corresponding date after each session; the tool automatically counts this week's completed/total slots and the cumulative check-ins to quantify consistency.",
"Manage multiple courses in parallel (different coaches/programmes), distinguished by colour blocks and labels to avoid conflicts.",
"Walkthrough: adding strength training and checking in",
"Steps: click Add course, enter the name Strength training, coach Coach Zhang and a weekly frequency of 2; the schedule automatically generates the corresponding colour blocks in the calendar.\nCheck-in: click Done in that course's cell on a given day → the stats card This week done +1 and cumulative check-ins +1,",
"progress bar",
" fills according to the completion rate.\nNote: this tool is a planning/recording type; data is stored locally in the browser (localStorage), it does not compute calories or scores, and it only helps you keep to and review your schedule.",
"Where is the data stored, and can it be lost?",
"Courses and check-in records are stored in your browser's localStorage and are lost when you switch devices or clear the cache; for important plans, consider a screenshot or a separate backup. This tool does not connect to the network and does not upload anything.",
"How do I read the completion rate?",
"The home stats card shows weekly slots (totalSlots), this week done (weekDone/totalSlots) and cumulative check-ins (allDone); each course's progress bar is coloured by its completion share, so you can see consistency at a glance.",
'About "Personal Training Schedule"',
"Create personal training courses, arrange weekly training slots from Monday to Sunday, check in completed sessions with one click, count this week's and cumulative completion rates, and show the training distribution in a clear calendar view.",
"Categorised management of multiple courses",
"Freely arrange weekly time slots",
"One-click check-in records",
"Completion-rate progress statistics",
"Monthly calendar distribution view",
"e.g. Strength training",
"e.g. Coach Zhang",
],
'detector-15': [
"🔍 Rounded Shoulder (Tight Pectoralis Minor) Test",
"Tight pectoralis minor",
'📖 View the "Rounded Shoulder (Slumped Posture) Risk Self-Test Guide"',
"Rounded-shoulder posture score = wall stand + shoulder forward tilt + pectoralis minor length (each 0 to 2) summed; add 1 point for sitting more than 8 hours a day; 0 normal, 1-3 mild rounded shoulders, more than 3 marked rounded shoulders.",
"Rounded shoulder test (pectoralis minor tightness assessment, 3 tests)",
"1. Wall stand test (head against the wall)",
"Back of head rests easily against the wall (0 points)",
"Barely touches the wall (2 points)",
"Cannot touch the wall (3 points)",
"2. Shoulder forward-tilt observation",
"Shoulders centred with no forward tilt (0 points)",
"Mild forward tilt (2 points)",
"Marked rounded shoulders (3 points)",
"3. Pectoralis minor length test (scapular gap when lying supine)",
"Scapulae lie flat on the table (0 points)",
"One side lifts off (2 points)",
"Both sides lift markedly (3 points)",
"Daily sitting time (hours)",
"Test rounded shoulders",
"📚 In-Depth Analysis: Rounded Shoulder (Slumped Posture) Risk Self-Test",
"Desk workers who sit for long periods can self-test for a tendency to rounded shoulders by scoring three observations: wall stand, shoulder forward tilt and pectoralis minor length.",
"Combined with daily sitting time (extra points above 8 hours) for an overall assessment, flagging the risk of rounded shoulders and thoracic stiffness.",
"Gives stretching/strengthening suggestions based on the result, guiding daily corrective moves (doorway stretch, face pull, rowing).",
"Reproducible examples: two scores, mild and marked rounded shoulders",
"Each of the three items scores 0 (normal)/2 (mild)/3 (marked), and sitting more than 8 h adds 1 to the total.\nExample A: wall stand barely touches (2), no shoulder forward tilt (0), pectoralis minor flat (0), sitting 7 h → total=2 → mild rounded shoulders (≤3).\nExample B: cannot touch the wall (3), marked rounded shoulders (3), one side lifts (2), sitting 10 h → total=8+1=9 → marked rounded shoulders (>3).\nConclusion: total 0=normal, 1-3=mild, ≥4=marked; prolonged sitting adds extra risk.",
"What does each of the three items look at?",
"1: the wall stand tests whether the head and neck protrude as compensation; 2: shoulder forward tilt observes whether the shoulders round; 3: pectoralis minor length (whether the scapulae lie flat when supine) reflects chest-muscle tightness. The three are complementary, and a score of 3 on any one flags a marked abnormality in that dimension.",
"How do I fix rounded shoulders once detected?",
"Mild: daily chest stretching (doorway stretch) + back strengthening (rowing, face pull), 3 sets × 15 reps each; marked: structured correction is needed — chest stretching 2-3 times a day, strengthening the rhomboids and lower trapezius, and adjusting sitting posture; consulting a physiotherapist is recommended.",
'About "Rounded Shoulder (Tight Pectoralis Minor) Test"',
"Rounded shoulder (tight pectoralis minor) test. A free online tool that runs entirely in the front end, uploading no data and protecting your privacy.",
],
'estimate-2': [
"⚡ Exercise Calorie Burn",
"Based on MET (metabolic equivalent) values, combine body weight and exercise duration to estimate calorie burn, covering 20+ common activities.",
"Exercise Calorie Burn Calculator",
'📖 View the "Exercise Calorie Burn Estimation (MET Method) Guide"',
"Calories burned kcal = MET × 3.5 × body weight (kg) / 200 × duration (min); kJ = kcal × 4.184; per-minute burn = kcal / duration",
"Based on the metabolic equivalent (MET) method: MET = 1 approximates resting metabolism (3.5 ml O₂/kg/min). A higher MET means greater intensity (<3 low, <6 moderate, <9 high, ≥9 very high). The rice-bowl equivalent is converted at about 230 kcal per bowl, to make the burn easier to grasp.",
"Duration (minutes)",
"💡 Formula: burn (kcal) = MET × 3.5 × body weight (kg) ÷ 200 × duration (minutes). 1 MET = resting metabolic level.",
"MET values are population averages; actual burn varies with intensity, technique and fitness level",
"For the same duration, a heavier body weight and higher intensity mean more calories burned",
"Excess post-exercise oxygen consumption (EPOC) can add a further 6-15% to the burn",
"Results are for reference only; weight management should combine diet with long-term habits",
"📚 In-Depth Analysis: Exercise Calorie Burn Estimation (MET Method)",
"Record how many kcal a session burns, and work out how long you would need to run to offset a meal (converted intuitively via rice-bowl equivalents).",
"Compare the energy cost of different activities over the same time to pick the most cost-effective training (e.g. HIIT vs jogging).",
"Customise the burn by body weight and duration — heavier and longer means a higher burn — making it easy to keep a calorie ledger.",
"Reproducible example: 30 minutes of jogging for a 70 kg person",
"Input: activity jogging (8 km/h) MET=8.3, body weight w=70 kg, duration min=30.\nFormula kcal=MET×3.5×w/200×min=8.3×3.5×70/200×30.\nStep by step: 8.3×3.5=29.05; ×70=2033.5; ÷200=10.1675; ×30=305.0 kcal.\nEquivalent to kJ=305×4.184≈1276 kJ; about 305/230≈1.3 bowls of rice (≈230 kcal each); ≈10.2 kcal per minute.\nConclusion: a 70 kg person jogging 30 minutes burns about 305 kcal, equal to 1.3 bowls of rice, which can be used to offset diet against exercise.",
"What is MET?",
"MET (metabolic equivalent) = the multiple of oxygen consumed by an activity relative to rest, with 1 MET≈3.5 ml/kg/min; the general formula is kcal=MET×3.5×weight/200×minutes. This tool has built-in MET values for 30+ activities, covering walking, running, cycling, swimming, jumping and more.",
"How accurate is the estimate?",
"The error is about ±10-15%, affected by individual metabolism, terrain and intensity fluctuations; it is good enough for a calorie ledger and trend reference but should not be treated as an exact value. The more accurate your weight and duration inputs, the closer the result is to reality.",
'About "Exercise Calorie Burn"',
"Uses the MET (metabolic equivalent) method, combining body weight and exercise duration to estimate the calorie burn of a single session, with 30 common activities built in, helping you quantify the energy cost of each workout.",
"MET data for 30 activities",
"Supports custom body weight and duration",
"Outputs in both kcal and kJ",
"Intuitive rice-bowl equivalent conversion",
"Estimating a single session's burn",
"Designing exercise for a fat-loss plan",
"Side-by-side comparison of activities",
"Validating fitness-tracker data",
"Activity type",
"Duration",
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
