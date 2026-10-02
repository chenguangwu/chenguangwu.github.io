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
    write('nine-hole-peg', build('nine-hole-peg', [
        "\U0001F9EE Hand Function (Nine-Hole Peg) Standard Time Calculator",
        "The Nine-Hole Peg Test (NHPT) assesses fine hand movements and computes standard times and percentiles",
        "Core formulas (from the input variables): (domTime - ref.dom) / ref.dom x 100; ((nonDomTime - domTime) / domTime x 100)",
        "Aged 40-49",
        "Aged 70-79",
        "Aged 80 and above",
        "Dominant hand",
        "Right hand",
        "Left hand",
        "Dominant hand test time (seconds)",
        "Non-dominant hand test time (seconds)",
        "Enter the test times",
        "\U0001F4D6 Test instructions",
        "1. The nine-hole peg board is a 3x3 array of nine holes with 3.2 cm spacing",
        "2. Prepare nine pegs (1.6 cm diameter, 3.2 cm tall) and place them in a shallow container",
        "3. The patient sits at the table with the board directly in front",
        "4. Ask the patient to insert the pegs one by one with the test hand, as fast as possible",
        "5. Time from the \"start\" command until all nine pegs are inserted",
        "6. Test the dominant hand first, then the non-dominant hand",
        "7. If a peg drops mid-test there is no need to restart the timing; just continue",
        "Normal reference values (seconds, mean +/- SD)",
        "Age group",
        "Male - dominant hand",
        "Male - non-dominant hand",
        "Female - dominant hand",
        "Female - non-dominant hand",
        "The Nine-Hole Peg Test is widely used to assess hand function in stroke, Parkinson disease, hand trauma, arthritis and similar conditions. A longer time means worse hand function. It can be used to monitor rehabilitation progress and compare changes before and after treatment.",
        "\U0001F4CC Test record",
        "\U0001F4DDA In-depth analysis: hand function (nine-hole peg) standard time assessment",
        "Post-stroke hand function",
        "Fine motor screening",
        "Rehabilitation follow-up",
        "Deviation 27%",
        "Reference for men aged 60-69 is 22s +/- 4s, measured 28s: deviation% = (28-22)/22 x 100 = 27%, Z = (28-22)/4 = 1.5, bilateral asymmetry about 12%, judged mildly abnormal and peg-board training recommended.",
        "Measured 21s, Z is about -0.25, within the reference range, hand function normal and maintaining daily activity is enough.",
        "How do I use the Z score?",
        "Z = (measured - reference mean) / SD, Z > 1.96 is abnormal; a difference greater than 20% between the hemiplegic side and the healthy side indicates significant asymmetry.",
        "Should I practice before switching hands?",
        "Yes. Test both the dominant and non-dominant hand: in healthy people the non-dominant hand is usually 5-10% slower than the dominant hand, and a gap clearly beyond that range suggests insufficient compensation on the affected side or over-compensation on the healthy side. Before testing, let the patient practice once (not counted), then run the timed test twice and take the average; if a peg drops mid-test it must be picked up and reinserted and the timer does not pause.",
        "About the Hand Function (Nine-Hole Peg) Standard Time Calculator",
        "Hand Function (Nine-Hole Peg) Standard Time Calculator." + DISCL_M,
        "e.g. 18.5",
        "e.g. 20.3",
    ]))
    write('physiotherapy-dose', build('physiotherapy-dose', [
        "\U0001F48A Physiotherapy Dose (Ultrasound / Laser) Time and Intensity Calculator",
        "Computes treatment time, intensity and total energy dose for ultrasound and laser physiotherapy",
        "Computes treatment time, intensity and total energy dose for ultrasound and laser physiotherapy from the entered parameters.",
        "Ultrasound",
        "Laser therapy",
        "TENS electrical stimulation",
        "Ultrasound treatment parameters",
        "Treatment area (cm2)",
        "Radiator head area (cm2)",
        "1 cm2 (small)",
        "5 cm2 (standard)",
        "10 cm2 (large)",
        "Intensity (W/cm2)",
        "0.1 (acute phase)",
        "0.3 (subacute)",
        "0.5 (chronic)",
        "0.8 (high dose)",
        "1.0 (maximum)",
        "1 MHz (deep tissue 4-5 cm)",
        "3 MHz (superficial tissue 1-2 cm)",
        "Continuous mode",
        "Pulsed mode (1:4)",
        "Enter parameters to calculate the ultrasound dose",
        "Laser treatment parameters",
        "GaAs (904 nm pulsed)",
        "GaAlAs (820 nm continuous)",
        "HeNe (632.8 nm continuous)",
        "Output power (mW)",
        "Target energy density (J/cm2)",
        "0.5 (acute)",
        "2 (subacute)",
        "4 (chronic)",
        "8 (high dose)",
        "Enter parameters to calculate the laser dose",
        "TENS electrical stimulation parameters",
        "TENS type",
        "Conventional (high frequency, low intensity)",
        "Acupuncture-like (low frequency, high intensity)",
        "Burst (pulse trains)",
        "Treatment time (minutes)",
        "Select parameters to see the TENS protocol",
        "Copy prescription",
        "\U0001F4D6 Physiotherapy dose reference",
        "Ultrasound dose principles",
        "Acute phase: 0.1-0.3 W/cm2, pulsed mode, 3-5 minutes",
        "Subacute phase: 0.3-0.5 W/cm2, pulsed/continuous, 5-8 minutes",
        "Chronic phase: 0.5-1.0 W/cm2, continuous mode, 5-10 minutes",
        "About 1 minute is needed per cm2 of treatment area",
        "Maximum treatment area = radiator head area x 4",
        "Laser dose principles",
        "Acute wound: 0.5-1 J/cm2",
        "Subacute injury: 1-3 J/cm2",
        "Chronic pain: 4-8 J/cm2",
        "Irradiation time per point = target dose x area / power",
        "\U0001F4CC Treatment record",
        "\U0001F4DDA In-depth analysis: physiotherapy dose (ultrasound / laser) calculation",
        "Ultrasound therapy",
        "Laser irradiation",
        "Dose setting",
        "Ultrasound 4 minutes",
        "Area 20 cm2 / radiator head 5 cm2, 0.5 W/cm2 continuous: time = 20/5 = 4 minutes, power 2.5 W, energy = 2.5 x 4 x 60 = 600 J; pulsed 1:4 gives only 120 J.",
        "Laser energy",
        "Dose 4 J/cm2 x area 10 cm2 = 40 J, power 0.5 W: time = 40/0.5 = 80 seconds; power density = 500/10 = 50 mW/cm2.",
        "How do I choose the intensity?",
        "0.3 W/cm2 or below for the acute phase, 0.3-0.5 for subacute, above 0.5 for chronic; 1 MHz reaches 4-5 cm deep while 3 MHz only reaches 1-2 cm superficially.",
        "How does the area affect treatment time?",
        "Treatment time = target total energy / power density / effective radiation area, so the larger the area the longer the total time. A practical approach is to divide the treatment region into multiples of the probe area: for ultrasound work in units of 1-2 effective radiating areas (ERA), 5-10 minutes per unit; when the area is too large",
        "the dose is diluted, so time must be extended accordingly or the region treated zone by zone. Never move the probe quickly back and forth to save time, because that lowers the dose actually delivered.",
        "About the Physiotherapy Dose (Ultrasound / Laser) Time and Intensity Calculator",
        "Physiotherapy Dose (Ultrasound / Laser) Time and Intensity Calculator." + DISCL_M,
        "e.g. 2-3x radiator head area",
        "e.g. 50",
        "e.g. 10",
        "e.g. 30",
    ]))


if __name__ == '__main__':
    main()