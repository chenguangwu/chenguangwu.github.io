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
    write('rom-normal-value', build('rom-normal-value', [
        "\U0001FABF Range of Motion (ROM) Normal Value Comparator",
        "Look up the normal range of motion for each joint and automatically assess limitation from a measured value",
        "Select the joint",
        "Select the movement direction",
        "Measured angle (degrees)",
        "Select a joint and enter the measured angle",
        "Save the measurement record",
        "\U0001F4CCA Normal range of motion reference table",
        "\U0001F4CC Measurement record",
        "\U0001F4DDA In-depth analysis: range of motion (ROM) normal value comparison",
        "Joint limitation",
        "Contracture assessment",
        "Shoulder flexion 150 degrees",
        "Shoulder flexion normal max is 180 degrees, measured 150 degrees: achievement rate = 150/180 x 100 = 83%, mildly limited, target restoring to above 170 degrees.",
        "Knee extension -5 degrees",
        "Knee extension normal is 0 degrees, measured -5 degrees (hyperextension within 5 degrees is a normal variant), no contracture; below -10 degrees indicates a flexion contracture.",
        "How is the achievement rate calculated?",
        "Measured angle / normal maximum for that movement x 100; below 80% is clearly limited, below 50% seriously impairs function and stretching should be prioritized.",
        "How large a left-right difference is meaningful?",
        "Usually a bilateral difference above 10 degrees, or a gap of more than 15-20 degrees from the normal value for the matching age and sex, is considered clinically meaningful; below that range it is mostly measurement error or individual variation. When measuring you must fix the position, use the same goniometer and the same bony landmarks, and record passive and active ROM separately, because a large gap between the two suggests muscle weakness or pain inhibition rather than a limitation of the joint itself.",
        "About the Range of Motion (ROM) Normal Value Comparator",
        "Range of Motion (ROM) Normal Value Comparator." + DISCL_M,
        "Enter the goniometer reading",
    ]))
    write('stretch-duration', build('stretch-duration', [
        "\u23F1\ufe0f Stretch Duration (Total Time) and Contracture Prevention Calculator",
        "Computes total stretch training time, sets and frequency to prevent joint contracture",
        "Core formulas (from the input variables): Math.ceil(restricted / target); dailyTotalTime x 7",
        "Stretch parameters",
        "Stretch site",
        "Hip joint",
        "Spine",
        "Contracture risk level",
        "Low risk (prophylactic)",
        "Moderate risk (mild tightness)",
        "High risk (contracture already present)",
        "Severe contracture",
        "Hold time per repetition (seconds)",
        "Number of repetitions",
        "Current ROM limitation (degrees)",
        "Target improvement per week (degrees)",
        "Enter parameters to compute the stretching plan",
        "\U0001F4D6 Stretching guide reference",
        "Stretch duration principles",
        "Static stretching: hold 15-60 seconds each time, which works better than very short holds",
        "Low risk: 15-30 s x 2-3 sets x 1-2 times per day",
        "Moderate risk: 30 s x 3-4 sets x 2-3 times per day",
        "High risk: 30-60 s x 4-5 sets x 3-5 times per day",
        "Severe contracture: 60 s x 5-6 sets x 5 or more times per day",
        "Contracture prevention strategies",
        "Proper limb positioning: change position every 2 hours",
        "Passive ROM training: full range of motion 2-3 times per day",
        "Active-assisted ROM: use the healthy limb or a pulley for assistance",
        "Continuous passive motion (CPM): 30-60 minutes each session",
        "Static splint: low-load long-duration stretch (30 minutes to 2 hours)",
        "Dynamic splint: provides continuous low-load stretch",
        "Site-specific advice",
        "\U0001F4CC Training record",
        "\U0001F4DDA In-depth analysis: stretch duration and contracture prevention calculation",
        "Contracture prevention",
        "ROM maintenance",
        "Home program",
        "3 minutes per day",
        "Each hold 30 s x 3 times x 2 sets per day = 180 s = 3 minutes; target improvement 15 degrees at 5 degrees per week: about 3 weeks needed; for high risk at least 3 minutes per day just meets the target.",
        "restricted 25 degrees at a weekly target of 5 degrees: about 5 weeks; severe contracture calls for at least 5 minutes of stretching per day together with bracing.",
        "How long should each hold be?",
        "For static stretching hold 15-30 s and repeat 2-4 times, 1-2 sets per day; for high risk the daily total should be at least 3 minutes to be effective.",
        "How much total daily time is needed for an effect?",
        "Research commonly uses 30-60 s per hold, 2-4 repetitions, no fewer than 5 days per week, about 5-10 minutes cumulative per week before measurable improvement in range of motion is seen; stretches shorter than 15 seconds mainly act on elastic components, rebound quickly and give limited benefit. During the spastic phase long-duration low-load stretching (more than 30 minutes of sustained stretch or bracing) is preferred over repeated short forceful pulls, which easily trigger the stretch reflex and worsen spasticity.",
        "About the Stretch Duration (Total Time) and Contracture Prevention Calculator",
        "Stretch Duration (Total Time) and Contracture Prevention Calculator." + DISCL_M,
        "e.g. 30",
        "e.g. 2",
        "e.g. 5",
    ]))
    write('walker-height', build('walker-height', [
        "\U0001F4CF Walker Height (Greater Trochanter) Adjuster",
        "Computes the correct height of walkers, crutches and canes for safe use and proper posture",
        "Core formulas (from the input variables): finalHandleHeight / height x 100; height x 0.57; wristH + 2",
        "Elbow flexion angle (degrees, measured)",
        "Wrist crease height (cm, ground to wrist crease)",
        "Sole thickness (cm)",
        "Standard (indoor and outdoor)",
        "Stair use",
        "Uneven ground",
        "Enter height and other parameters",
        "Compute the height",
        "\U0001F4D6 Assistive device height standard",
        "Standard walker",
        "Handle height = greater trochanter height (about 55-60% of standing height)",
        "or = ground-to-wrist-crease distance + 2-3 cm",
        "Elbow flexes 20-30 degrees while standing",
        "When used the body should stay behind the walker without leaning too far forward",
        "Forearm crutch",
        "Handle height is the same as for a walker (wrist crease + 2-3 cm)",
        "Cuff height = 2.5-3 cm above the olecranon",
        "The cuff should be moderately snug, letting the forearm through without slipping out",
        "Axillary crutch",
        "Axillary pad height = 5 cm below the armpit (about 77% of standing height)",
        "Handle height = wrist crease + 2-3 cm (elbow flexed 20-30 degrees)",
        "The armpit should not bear weight directly, the force goes through the hands",
        "Leave 2-3 finger widths between the axillary pad and the armpit",
        "Single crutch / cane",
        "Handle height = greater trochanter height",
        "or = ground-to-wrist-crease distance",
        "It should be used on the healthy side (not the affected side)",
        "\U0001F4CC Record",
        "\U0001F4DDA In-depth analysis: walker height (greater trochanter) adjustment",
        "Quad cane",
        "Frame walker",
        "Stair scenario",
        "Trochanter height 97 cm",
        "Height 170 cm: trochanter height is about 170 x 0.57 = 96.9 cm, axillary height about 170 x 0.77 = 130.9 cm; handle height = wrist crease + 2 cm (wrist height 100 \u2192 102 cm).",
        "Slightly lower on stairs",
        "For going up stairs lowering the handle by 2 cm (97 \u2192 95 cm) is more stable; the forearm cuff is about olecranon height = 170 x 0.74 = 125.8 cm.",
        "What handle height is right?",
        "Standing, the handle should be level with the wrist crease (at the greater trochanter level) with the elbow flexed 20-30 degrees; too high causes shoulder shrugging and too low causes bending at the waist, both increasing strain.",
        "How many degrees of elbow flexion are best?",
        "Standing with both arms relaxed, handle height is about level with the greater trochanter (or the wrist crease), at which point the elbow flexes about 20-30 degrees. Too little flexion (under 15 degrees) tires the shoulder and arm during support and makes pushing up hard; too much (over 40 degrees) shifts the center of mass forward with a trunk lean, which is actually less stable and increases low back load. After adjusting, let the patient actually walk and observe: if shrugging or a forward lean appears, fine-tune by another 1-2 cm.",
        "About the Walker Height (Greater Trochanter) Adjuster",
        "Walker Height (Greater Trochanter) Adjuster." + DISCL_M,
        "e.g. 170",
        "e.g. 70",
        "e.g. 25",
        "e.g. 105",
        "e.g. 2",
    ]))


if __name__ == '__main__':
    main()