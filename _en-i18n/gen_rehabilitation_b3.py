#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'rehabilitation')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'rehabilitation')
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
    out = {'slug': slug, 'industry': 'rehabilitation', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('flacc-scale', build('flacc-scale', [
        "\U0001FABF Pain Behavior Observation (FLACC) Assessor",
        "The FLACC scale is used for patients who cannot report pain themselves (infants, cognitive impairment, impaired consciousness), 5 items at 0-2 points each, 0-10 total",
        "Select the performance of each item to see the score",
        "\U0001F4CCA FLACC score interpretation",
        "No analgesic needed, recheck periodically",
        "Mild pain",
        "Non-pharmacologic measures first, oral analgesia if needed",
        "Moderate pain",
        "Oral analgesics plus non-pharmacologic measures, assess the effect",
        "Severe pain",
        "Potent analgesia, intravenous dosing if necessary, close monitoring",
        "Applicable population:",
        "FLACC applies to children aged 2 months to 7 years, adults with cognitive impairment, delirious patients, sedated ICU patients and others who cannot self-report pain. For adult ICU patients the revised FLACC (r-FLACC) can be used.",
        "\U0001F4CC Assessment record",
        "\U0001F4DDA In-depth analysis: pain behavior observation (FLACC) scoring",
        "Postoperative analgesia",
        "Infant pain",
        "Cognitive impairment",
        "Total 4",
        "Face/legs/activity/cry/consolability each 0-2 gives 4/10, moderate pain, analgesia should be given and reassessed; 0 means no pain.",
        "Total 8",
        "Total 8 (<=6 orange zone, <=10 red zone), severe pain, intervene immediately and look for the cause, then retest after 30 minutes.",
        "Which population is it for?",
        "People who cannot self-report pain (infants, dementia, intubated patients); five dimensions at 0-2 each, 0-10 total, >=4 needs action.",
        "Does scoring during sleep count?",
        "It counts and is highly valuable: a FLACC baseline during sleep or quiet reflects persistent pain, while a score during activity reflects movement-provoked pain. Score at three fixed time points (rest, activity or post-care, and 30 minutes after medication) and read the trend rather than a single value. Note that irritability may also come from hypoxia, urinary retention or fear, so before giving analgesia at a score of 4 or above, rule out these non-pain causes.",
        "About the Pain Behavior Observation (FLACC) Assessor",
        "Pain Behavior Observation (FLACC) Assessor." + DISCL_M,
    ]))
    write('gait-analysis', build('gait-analysis', [
        "\U0001FABF Gait Analysis (Stance/Swing) Time Ratio Calculator",
        "Enter the phase times of a gait cycle to compute the stance/swing ratio and assess gait symmetry",
        "Core formulas (from the input variables): |stance - stance2| / max(stance, stance2) x 100; (cadence x stepLen / 100) / 60; (doubleStance / cycle x 100)",
        "Gait parameter input",
        "Total gait cycle time (seconds)",
        "Single-support stance time (seconds)",
        "Double-support time (seconds)",
        "Step length (cm)",
        "Opposite-side stance time (seconds, optional)",
        "Enter the gait cycle parameters",
        "Analyze gait",
        "\U0001F4CCA Normal gait parameter reference",
        "Normal value",
        "Gait cycle",
        "1.0-1.2 seconds",
        "From one heel strike to the next heel strike on the same side",
        "Stance phase share",
        "Time the foot is in contact with the ground",
        "Swing phase share",
        "Time the foot is swinging in the air",
        "Double support",
        "Time both feet are on the ground together",
        "Single support",
        "Time a single foot is on the ground bearing weight",
        "Cadence",
        "100-120 steps/min",
        "Steps per minute",
        "Distance from the same-side heel to the opposite heel",
        "Walking speed",
        "Distance walked per second",
        "\U0001F4CC Analysis record",
        "\U0001F4DDA In-depth analysis: gait analysis (stance/swing) time ratio",
        "Speed assessment",
        "Hemiplegic gait",
        "Orthosis effectiveness",
        "Stance/swing 1.75",
        "Gait cycle 1.1 s, stance 0.70 s, swing 0.40 s: stance% = 63.6, swing% = 36.4, ratio 1.75; double support 0.12/1.1 = 10.9% (normal 8-12%).",
        "Speed 1.1 m/s",
        "Cadence 110, step length 60 cm: speed = 110x60/100/60 = 1.1 m/s, within the normal range; below 0.8 indicates clear slowing.",
        "What does a longer double-support phase mean?",
        "Double support above 12% indicates slowed or unstable walking (as in Parkinson disease or hemiplegia), below 8% indicates faster walking; normal is about 10%.",
        "Does walking speed affect the ratio?",
        "Yes. At normal speed the stance phase is about 60% and the swing phase about 40%; when speed drops the stance share rises (the slower the walk, the longer the stance), and when walking fast the swing share rises. So comparing two measurements requires fixing the speed (choose a comfortable speed and record the speed value at the same time), otherwise a difference in the ratio may only reflect a difference in speed rather than a functional change.",
        "About the Gait Analysis (Stance/Swing) Time Ratio Calculator",
        "Gait Analysis (Stance/Swing) Time Ratio Calculator." + DISCL_M,
        "e.g. 1.2",
        "e.g. 0.72",
        "e.g. 0.12",
        "e.g. 110",
        "e.g. 70",
        "Used for symmetry analysis",
    ]))
    write('mmse-scoring', build('mmse-scoring', [
        "\U0001F4CC Cognitive Impairment (MMSE) Scale Auto-Scorer",
        "30-item Mini-Mental State Examination (MMSE) scale, 30 points total, used for cognitive impairment screening",
        "Score each item to see the result",
        "\U0001F4CCA MMSE score interpretation",
        "Cognitive level",
        "Needs further assessment, may be MCI",
        "Needs partial help with daily life",
        "Needs full care for daily life",
        "Education correction:",
        "Illiterate <=17 points, primary school <=20 points, junior high or above <=24 points suggests cognitive impairment. This scale is widely used for dementia screening, with about 80% sensitivity and about 90% specificity.",
        "\U0001F4CC Assessment record",
        "\U0001F4DDA In-depth analysis: cognitive impairment (MMSE) scale scoring",
        "Dementia screening",
        "Follow-up comparison",
        "Preoperative assessment",
        "Total 24",
        "Orientation 9 + memory 3 + attention 4 + recall 2 + language 6 = 24/30, mild cognitive impairment (21-26); below 27 further cognitive assessment is recommended.",
        "Total 18",
        "Total 18 (11-20 orange zone), moderate impairment, a caregiver should join in and reversible factors (nutrition / medication / depression) should be excluded.",
        "What do the grades mean?",
        ">=27 normal, 21-26 mild, 11-20 moderate, <=10 severe (full score 30, covering orientation / memory / attention / recall / language).",
        "How should low scores in illiterate elderly people be judged?",
        "The MMSE is strongly affected by education level: cognitive impairment is only judged at no more than 17 for illiterate, no more than 20 for primary school, and no more than 24 for junior high or above; using a uniform 24-point cutoff would massively misjudge elderly people with low education. Also the serial 7s subtractions and backwards word recall depend heavily on hearing and attention, so people with hearing impairment should wear a hearing aid before testing. The MMSE is insensitive to early mild cognitive impairment (MCI), so MoCA can be added when necessary.",
        "About the Cognitive Impairment (MMSE) Scale Auto-Scorer",
        "Cognitive Impairment (MMSE) Scale Auto-Scorer." + DISCL_M,
    ]))
    write('mmt-grading', build('mmt-grading', [
        "\U0001F4CC Manual Muscle Testing (MMT) Grading and Function Descriptor",
        "Manual muscle testing (MMT) grade 0-5 reference, determines the muscle strength grade from the test condition",
        "Test condition selection",
        "Grade 0: no observable muscle contraction",
        "Grade 1: trace contraction but no joint movement",
        "Grade 2: full range of motion achievable in a gravity-eliminated position",
        "Grade 3: full range of motion achievable against gravity",
        "Grade 4: full range of motion against gravity plus moderate resistance",
        "Grade 5: full range of motion against gravity plus maximum resistance",
        "Select a muscle strength grade to see the detailed description",
        "\U0001F4CC MMT grading reference table",
        "\U0001F4CC Assessment record",
        "\U0001F4DDA In-depth analysis: manual muscle testing (MMT) grading and function",
        "Peripheral paralysis",
        "Muscle strength assessment",
        "MMT grade 3 means full range of motion against gravity with no added resistance, so the limb can be lifted off the bed; train toward grade 4 (against some resistance) and then grade 5 normal.",
        "Grade 0",
        "Grade 0 has no visible contraction and needs electrical stimulation plus passive ROM to prevent atrophy and contracture, combined with neurofacilitation techniques.",
        "What do grades 0-5 mean?",
        "0 no contraction, 1 trace movement, 2 full range in a gravity-eliminated position, 3 against gravity, 4 against partial resistance, 5 normal; each grade corresponds to roughly",
        "0 / 10 / 25 / 50 / 75 / 100% of muscle strength.",
        "How to distinguish grade 3 from grade 4 more accurately?",
        "The key lies in how resistance is applied: grade 3 achieves the full range against gravity but cannot resist any added resistance; grade 4 resists some resistance but less than normal. In practice, give resistance compared with the examiner's same-named muscle group, and apply it in the middle portion of the joint range (not the start or end), because leverage and muscle tone at the ends mislead interpretation. Values between two grades are marked with + or -, but before-and-after assessments of the same patient must be performed by the same examiner to reduce bias.",
        "About the Manual Muscle Testing (MMT) Grading and Function Descriptor",
        "Manual Muscle Testing (MMT) Grading and Function Descriptor." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()