#!/usr/bin/env python3
# health batch5 (4 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'health')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'health')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'safe-period-calculator': [
"🧮 Safe Period Calculator",
"/ Safe Period Calculator",
"📖 View the User Guide",
"Ovulation day = last menstrual period + cycle length − 14",
"Fertile window = ovulation day −5 to +4; safe period = the remaining days of the cycle (calendar method, only for regular cycles)",
"Last menstrual period date",
"Cycle length (days)",
"Period length (days)",
"📚 In-depth: Safe Period Calculator",
"Estimate the ovulation day and fertile window: enter the LMP, cycle length and period length; ovulation day ≈ LMP + (cycle − 14); fertile window = ovulation day ±5 days (sperm can survive several days).",
"Estimate the next period: next period ≈ LMP + cycle; the period is marked by the period length. The cycle calendar labels each day as period / fertile / safe.",
"Understand the limits of the safe period: ovulation can shift earlier or later due to emotions, illness and stress, so the calendar method is only a health-management reference and never a reliable contraceptive.",
"Example: LMP 2026-08-01, cycle 28 days, period 5 days",
"Ovulation day = 8/1 + (28−14) = 8/15; fertile window = 8/10 to 8/19; next period = 8/29 (period 5 days from 8/29). ⚠️ The annual failure rate of safe-period contraception is about 24%, so it is not recommended as a contraceptive method.",
"Why is the safe period unreliable?",
"Women's ovulation can shift by ±several days due to stress, illness, travel and so on, and sperm can survive about 5 days in the uterus while the egg about 1 day, so the fertile window is wide and calendar estimation easily misses.",
"What should I use for contraception?",
"Reliable methods include condoms, combined oral contraceptives and intrauterine devices; the safe period and withdrawal have high failure rates and are not recommended on their own. Consult a doctor as needed.",
"The calendar method assumes ovulation day = 14 days before the next period, with sperm surviving about 3-5 days and the egg 1 day",
"Fertile window = 5 days before to 4 days after ovulation; the rest is the relatively safe period",
"Irregular cycles and stress/illness/travel affect ovulation, giving the calendar method a large error",
"The results are not medical or contraceptive advice; consult a professional doctor for important decisions",
],
'stretch-generator': [
"✨ Random Stretch Routine Generator",
"Choose body parts and session length, then generate a random stretch routine in one click to keep every session fresh",
"/ Stretch Routine Generator",
"📖 View the User Guide",
"Select body parts",
"(multiple allowed)",
"Neck",
"Shoulders",
"Back",
"Lower back",
"Hips",
"Legs",
"Arms",
"Deselect all",
"Session length",
"5 minutes",
"10 minutes",
"15 minutes",
"20 minutes",
"✨ Generate routine",
"After choosing body parts and a length, click \"Generate routine\" to start",
"Tool description and user guide",
"The Random Stretch Routine Generator is a pure front-end online tool that intelligently generates a complete stretch routine based on the body parts and session length you choose. Each generation differs, helping enrich your stretching workouts.",
"Pure front-end processing, no registration, no data upload",
"7 major body parts, 24+ selected stretches",
"4 length options, flexible from 5 to 20 minutes",
"Randomly generated each time, no more repetitive training",
"One-click copy of the routine text for easy recording and sharing",
"Warm-up stretching before exercise",
"Cool-down and recovery after exercise",
"Relaxation during breaks from prolonged sitting",
"Bedtime body stretch and relaxation",
"📚 In-depth: Random Stretch Routine Generator",
"Generate a plan by body part: tick the body parts you want to stretch (shoulders/neck, lower back, legs, full body, etc.) and the tool filters matching movements from its library.",
"Fill the session by length: set a total length (e.g. 10 minutes); the tool schedules at least 1 movement for each selected body part and then randomly cycles to fill until the target length is reached.",
"Random variety and reproducibility: each generation combines randomly within the selected parts to avoid monotony; you can \"regenerate\" for a different set or copy the plan text for reference on the go.",
"Example: select \"shoulders/neck + lower back\", length 10 minutes",
"Target length = 10 × 60 = 600 seconds. The first round takes 1 movement per body part (e.g. shoulders/neck 45s, lower back 50s), then cycles through the selected parts' libraries (each movement about 30-60s) until the total approaches 600s, allowing a ±30s deviation.",
"Are the movements reliable?",
"The movements come from a built-in stretch library (name, body part, suggested duration, key points). They remain general fitness references; people with injuries or illnesses should follow medical advice and avoid forcing a stretch.",
"Can the same movement repeat?",
"The first round guarantees at least 1 movement per selected body part; later cycles fill randomly and may repeat. Click \"regenerate\" for a different combination, or trim it yourself.",
],
'rehab-timer': [
"🦿 Rehab Training Timer",
"Create training items, time and check in, and record your consecutive-day streak",
"📖 View the User Guide",
"Per-set duration = movement duration (s); total duration = sets × movement duration + (sets − 1) × rest between sets",
"Timed training",
"Manage items",
"Check-in calendar",
"Select a training item",
"Please select a training item",
"Check in",
"Add training item",
"Hot compress",
"Cold compress",
"Joint range-of-motion training",
"Strength training",
"Balance training",
"Stretching",
"Aerobic exercise",
"Duration per set (seconds)",
"Rest between sets (seconds)",
"Add item",
"Training item list",
"Select month",
"Check-in records",
"About the Rehab Training Timer",
"The Rehab Training Timer helps patients keep up daily rehab training, supports custom training items, sets and rest times, and automatically records check-ins to encourage sustained recovery.",
"Custom training items",
"Multi-set timing with between-set rest reminders",
"Daily check-in records",
"Consecutive-day statistics",
"Monthly calendar visualization",
"Post-surgery rehab training check-ins",
"Daily exercise for chronic conditions",
"Sports injury recovery",
"📚 In-depth: Rehab Training Timer",
"Training item timing: add rehab movements in \"Manage items\" (icon + name + sets × per-set duration); the timer counts down in a train-rest cycle and prompts when all sets are done.",
"Between-set rest and multi-set cycles: each movement has \"X sets × Y seconds\" and automatically enters rest between sets; the rest duration is configurable to control training density and protect movement quality.",
"Check-in and streak statistics: each completed session counts as a check-in; the tool tracks \"consecutive check-in days / today's check-in / cumulative days / total count\" and visualizes them to encourage persistence. Data is saved in your local browser and not uploaded to a server.",
"Example: shoulder/neck relaxation 3 sets × 30 seconds, rest 10 seconds between sets",
"The timer runs in sequence: train 30s → rest 10s → train 30s → rest 10s → train 30s (3 sets total), for 90s of training and 20s of rest. After check-in the \"consecutive check-in days\" increases by 1 and the stat cards refresh.",
"How do I add or delete training items?",
"Open the \"Manage items\" page to add or remove movements and set the sets and durations; deleting does not affect historical check-in records. Items are stored only in your local browser's localStorage.",
"Is the check-in data safe?",
"All data is saved in your local browser with pure front-end processing and is not uploaded to any server; it is lost when you change devices or clear the cache, so record important content yourself.",
'About the "Rehab Training Timer"',
"The Rehab Training Timer is an online health/medical tool. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
"e.g. Hot compress on shoulders",
],
'running-calories': [
"⚡ Running Calorie Burn Calculator",
"Multiple input methods to accurately estimate the calories burned while running",
"Running Calorie Calculator",
"/ Running Calorie Calculator",
"📖 View the User Guide",
"Calories (kcal) = MET × weight (kg) × time (h)",
"MET is obtained from the pace table; the heart-rate method estimates separately from average heart rate, resting heart rate and age",
"Pace + distance",
"Time + distance",
"Pace + time",
"👨 Male",
"👩 Female",
"Pace (min:sec/km)",
"Time (min:sec)",
"Time (hours:min)",
"Use heart rate (more precise)",
"Average heart rate (bpm)",
"Calories burned",
"Running distance",
"MET value",
"🔥 Estimated fat burn (about 1g fat = 9 kcal)",
"🏅 Reference burn for common running distances",
"Estimated from your current weight and pace",
"💪 Training effect assessment",
"📝 Pace calculator",
"Convert among time, distance and pace",
"Important:",
"This calculator is for reference only and cannot replace the advice of a professional coach or doctor.",
"• The calorie burn is an estimate; actual burn varies between individuals",
"• Warm up thoroughly before running to avoid sports injuries",
"• Running 3-5 times a week for 30-60 minutes each is recommended",
"• Fat loss requires dietary control to create a calorie deficit",
"• If you have cardiovascular disease or other chronic conditions, exercise as advised by your doctor",
"📚 In-depth: Running Calorie Burn Calculator",
"Estimate a single run's burn: estimate calories from weight, distance and pace, useful for quick reference when planning fat-loss/aerobic programs.",
"Compare distances: view the estimated burn for 1/3/5/10 km plus half and full marathons at once to feel the distance-to-calorie relationship.",
"See efficiency with pace: at the same distance a slower pace burns less per unit time but lasts longer; the tool gives baseline figures using a default weight (about 60 kg, 6 min/km).",
"Example: default parameters (about 60 kg, 6 min/km)",
"1 km ≈ 72 kcal (6 min); 5 km ≈ 358 kcal (30 min); 10 km ≈ 715 kcal; half marathon ≈ 1508 kcal; full marathon ≈ 3017 kcal. Actual burn varies with weight, gradient and pace.",
"Why does it differ from my watch/app?",
"Different device algorithms,",
"heart-rate zones",
", terrain and individual metabolic rate cause differences, usually ±10-20%. This tool is an empirical estimate based on weight and distance, suited to trend comparison rather than precise measurement.",
"What should I note for fat-burning runs?",
"Sustained low-to-moderate intensity for over 30 minutes favors fat as fuel; combining with heart-rate zones (if available) is more accurate. Warm up before and stretch after running, and progress gradually to avoid injury.",
'About the "Running Calorie Calculator"',
"Running Calorie Calculator. A health-metric calculation tool based on authoritative medical standards, with all data processed locally to protect privacy.",
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
    print('gen_health_b5 done')
