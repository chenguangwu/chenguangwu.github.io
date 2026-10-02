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
def main():
    write('tester-rater', build('tester-rater', [
        "\U0001FABF Balance Function (Berg Score) Test",
        "Berg Balance Scale (14 test items, 0-4 points each, 0-56 total; a lower score means higher fall risk)",
        "The Berg Balance Scale has 14 items each scored 0 to 4 with a maximum of 56 points: 45 points or above means low fall risk, 40 to 44 means moderate risk, and below 40 means high fall risk (wheelchair or walker needed with 24-hour supervision). The minimal clinically important difference is about 4 to 8 points; any item scoring below 2 points is a functional weak point and should be targeted with specific training such as single-leg standing and turning.",
        "1. Sitting up",
        "0 - needs help",
        "1 - help with both arms",
        "2 - light support",
        "3 - on own but unsteady",
        "2. Standing independently",
        "1 - under 10 s",
        "2 - 10-30 s",
        "3 - 30 s to 2 min",
        "4 - over 2 minutes",
        "3. Sitting independently (unsupported)",
        "1 - needs support",
        "2 - possible but unsteady",
        "3 - fairly steady",
        "4 - steady for 2 min",
        "4. Sitting down",
        "0 - unsafe",
        "1 - needs arm help",
        "2 - not smooth",
        "3 - mostly smooth",
        "4 - safe and smooth",
        "5. Transfer",
        "0 - needs two people",
        "1 - a lot of help",
        "2 - a little help",
        "3 - verbal cueing",
        "4 - independent",
        "6. Standing with eyes closed",
        "1 - under 3 s",
        "2 - 3-5 s",
        "3 - 6-10 s",
        "4 - over 10 s",
        "7. Standing with feet together",
        "1 - needs help",
        "2 - together but unsteady",
        "3 - stands steadily on own",
        "4 - stable and independent",
        "8. Reaching forward with the upper limb",
        "1 - needs to step forward",
        "2 - reach over 5 cm",
        "3 - reach over 12 cm",
        "4 - reach over 25 cm",
        "9. Picking an object off the floor",
        "2 - barely manages",
        "3 - fairly easy",
        "10. Turning to look behind",
        "2 - one side",
        "3 - both sides but unsteady",
        "4 - both sides steady",
        "11. Turning 360 degrees in place",
        "2 - over 4 s per side",
        "3 - 3-4 s per side",
        "4 - under 3 s per side",
        "12. Stepping onto a stool (alternating steps)",
        "2 - 2 steps independently",
        "3 - 4 steps independently",
        "4 - 8 steps independently",
        "13. Standing with one foot in front of the other",
        "1 - parallel position",
        "2 - brief anterior-posterior stance",
        "3 - hold 30 s",
        "4 - hold 60 s",
        "14. Single-leg standing",
        "1 - brief",
        "2 - 2-5 s",
        "3 - over 5 s",
        "Compute the Berg score",
        "\U0001F4DDA In-depth analysis: balance function (Berg) score test",
        "Community walking",
        "Transfer ability",
        "Fall prevention",
        "Total 52",
        "The 14 items such as sitting up, standing, transfer and single-leg stance total 52/56, which is normal but low, so advanced balance and out-of-body activity training is recommended.",
        "Total 38",
        "Total 38 (medium risk), balance is limited, training with a walking aid is needed and the turning and single-leg standing items should be improved.",
        "How does it compare with the Berg scale?",
        "This tool sums the 14 items (0-56), consistent with the Berg Balance Scale; below 45 indicates increased fall risk.",
        "How long does one test take?",
        "The full 14 items usually take 15-20 minutes, and a stopwatch, ruler, chair, step stool, small ball and other props must be prepared. Items such as standing with eyes closed, single-leg standing and turning 360 degrees need guarded standing to avoid falls. For the same patient it is best to keep the same time slot and the same assessor, because fatigue and differences in interpretation can both produce 2-4 point swings.",
        "About the Balance Function (Berg Score) Test",
        "Balance Function (Berg Score) Test." + DISCL,
    ]))
    write('index', build('index', [
        "\U0001F4BE Rehabilitation Medicine Tools",
        "Rehabilitation medicine",
        "Rehabilitation medicine tools",
        "Enter the Nine-Hole Peg Test (NHPT) completion time to convert it into a standard time and a percentile for the same age group, quantifying fine hand movement and coordination for neurological rehabilitation and motor function follow-up assessment.",
        "Enter the stretch site, hold duration and number of daily sets; the tool accumulates the total stretch time and gives a recommended frequency, preventing joint contracture based on soft tissue extensibility, used for planning stretch programs for hemiplegic or long-term immobilized patients.",
        "Enter the stance and swing durations of the gait cycle; the tool computes the ratio between them and evaluates left-right symmetry, supporting quantification of gait abnormality and rehabilitation follow-up for stroke or post-orthopedic surgery patients.",
        "Enter the treatment area and ultrasound or laser output intensity; the tool computes the single-session treatment time, total energy dose and recommended frequency, avoiding under-dosing or excessive burns, used to plan ultrasound and low-level laser therapy programs.",
        "Enter patient height, weight and limb measurements; the tool computes fitting dimensions and load recommendations for assistive devices such as wheelchair seat width and depth, crutch and walker height, helping therapists select a safe, well-fitting device.",
        "Enter the amputee's residual limb parameters and prosthetic geometry; the tool computes the load line position and the alignment offset, flags inversion and eversion risk, and helps prosthetists assemble and dynamically adjust the prosthesis for better stability while walking.",
        "Enter age and measured pulmonary function; the tool computes target training values for maximal inspiratory pressure (MIP) and maximal expiratory pressure (MEP) and gives a respiratory muscle training load plan, used as a reference for respiratory rehabilitation and weaning assessment.",
        "FIM functional independence rating of 18 items (13 motor + 5 cognitive), 1-7 points each, 18-126 total",
        "After passively moving the patient's joint to the target angle and having the patient reproduce it actively, enter the reproduced angle; the tool computes the position sense error (in degrees) against the target angle, quantifying proprioceptive function for post-joint-injury rehabilitation assessment and training tracking.",
        "Berg Balance Scale (14 test items, 0-4 points each, 0-56 total; a lower score means higher fall risk)",
        "Enter the user's height (or use the greater trochanter as reference); the tool computes the correct handle height for walkers, axillary crutches and canes so the elbow is slightly flexed when standing and weight bearing is safe, preventing strain on the low back and joints from an incorrect height.",
        "Select a joint such as shoulder, knee or hip and enter the measured range angle; the tool compares it against the normal range of motion for that joint and automatically assesses the degree of limitation and the missing percentage, used for rehabilitation assessment records and joint dysfunction screening.",
        "The Kubota Water Drinking Test lets the patient drink 30 mL of warm water and grades swallowing function by time and performance",
        "Berg Balance Scale (BBS) 14 test items, 0-4 points each, 56 points total, assessing static and dynamic balance ability",
        "ASIA (American Spinal Injury Association) impairment grading, determining the neurological level and severity of injury (AIS grade)",
        "Breaks activities of daily living into step-by-step training steps to help patients with cognitive and motor dysfunction learn gradually",
        "Enter the occupant's height and weight and cushion parameters; the tool computes the seated pressure distribution, ischial tuberosity load share and backrest angle, indicates the pressure relief interval to prevent pressure ulcers and optimizes the center of mass to lift seated balance, for long-term wheelchair users.",
        "Enter the 30 MMSE item scores to auto-sum the total (30 points maximum) and indicate the cognitive impairment grade, used as a reference for elderly cognitive screening and initial assessment of memory decline.",
        "The FLACC scale is used for patients who cannot report pain themselves (infants, cognitive impairment, impaired consciousness), 5 items at 0-2 points each, 0-10 total",
        "Boston Diagnostic Aphasia Examination (BDAE) severity grading (0-5) for evaluating language function in aphasia patients",
        "Manual muscle testing (MMT) grade 0-5 reference, determines the muscle strength grade from the test condition",
        "About the Rehabilitation Medicine Tools",
        "This Rehabilitation Medicine tool collection includes 21 free online tools covering the common calculation, conversion and lookup needs in rehabilitation medicine. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run entirely in the front end and no data is uploaded to the server, so privacy and security are protected.",
        "The rehabilitation medicine tools included on this page are (some representative tools):",
        "These tools help you quickly finish common rehabilitation medicine tasks without memorizing complex formulas or doing manual conversions, so you just enter the values and get the result.",
        "Do the rehabilitation medicine tools need a download or registration?",
        "No. All rehabilitation medicine tools on this page are pure front-end online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the rehabilitation medicine tool results accurate, and is the data secure?",
        "The tools compute locally in your browser using public mathematical formulas and common industry standards, so results are immediate. All computation happens locally on your device and no data is uploaded to the server, so privacy and security are assured.",
    ]))


if __name__ == '__main__':
    main()