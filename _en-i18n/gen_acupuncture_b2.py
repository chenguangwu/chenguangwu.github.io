#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'acupuncture')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'acupuncture')
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
    out = {'slug': slug, 'industry': 'acupuncture', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('cupping-pressure', build('cupping-pressure', [
        "📍 Cupping Negative Pressure (mmHg) Safety Threshold Lookup",
        "Look up the safe negative pressure range for different cupping methods and body regions, to prevent cupping injury",
        "/ Cupping Negative Pressure Safety Threshold Lookup",
        "📖 View the usage guide for the Cupping Negative Pressure (mmHg) Safety Threshold Lookup",
        "(1) Type of cupping method",
        "Back and lumbar region (thick muscle)",
        "Limbs",
        "Young and middle-aged adults",
        "🔍 Look up the threshold",
        "📋 Cupping negative pressure and time reference",
        "⚠️ Excessive negative pressure or too long a retention time easily causes blisters, subcutaneous bleeding and even skin necrosis; cupping is prohibited over skin ulcers, edema and allergic areas, and on the abdomen and lumbosacral region of pregnant women.",
        "📚 Deep dive: Cupping Negative Pressure (mmHg) Safety Threshold Lookup",
        "For retaining cups on the Bladder meridian of the back, take a low to moderate negative pressure according to tolerance.",
        "For flash cupping on the face and neck, use low negative pressure and a short time.",
        "For moving cupping on the back and waist, use moderate negative pressure together with a lubricating medium.",
        "Look up the safe negative pressure range",
        "For retaining cups on the back of an adult (thick muscle) the negative pressure is about -100 to -200 mmHg (relative to atmospheric pressure; a general reference for both fire cups and suction cups); for flash cupping on the face take -40 to -80 mmHg with each application under 30 seconds, to avoid facial bruising or blisters.",
        "Why is the negative pressure value negative?",
        "A negative pressure forms inside the cup (below atmospheric pressure) to draw in the skin, and the relative value is commonly used to express the suction strength; refer to the cup manufacturer's instructions for specifics.",
        "How long should the cup be retained?",
        "Generally 5-15 minutes, shortened for the elderly, the frail and children; it is contraindicated where the skin is broken or there is allergy.",
        "About the Cupping Negative Pressure (mmHg) Safety Threshold Lookup",
        "Cupping Negative Pressure (mmHg) Safety Threshold Lookup - look up the safe negative pressure range for different cupping methods (retaining, flash, moving) and body regions, to prevent blisters and subcutaneous injury. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('deqi-sensation', build('deqi-sensation', [
        "📋 Deqi Sensation (Soreness, Numbness, Distension, Heaviness) Intensity Grader",
        "Combines the patient's subjective needle sensation with the practitioner's sense under the needle to grade the degree of deqi and advise on technique",
        "/ Deqi Sensation Intensity Grader",
        "📖 View the usage guide for the Deqi Sensation Intensity Grader",
        "(1) Patient's subjective needle sensation (multiple choice)",
        "Sensation intensity (patient self-rating 0-10)",
        "Patient intensity:",
        "(2) Practitioner's sense under the needle",
        "Sense of tightness under the needle (0 = empty and slippery, 10 = deep and tight)",
        "Practitioner's feel:",
        "Propagation along the meridian",
        "No propagation",
        "Local propagation (short distance)",
        "Propagation along the meridian (reaching one joint)",
        "Propagation along the meridian (the whole course or beyond)",
        "📊 Assess and grade",
        "📋 Deqi grading standard reference",
        "⚠️ Deqi is the key to acupuncture efficacy, but the intensity of propagation varies greatly between individuals, and pursuing strong stimulation to excess does not guarantee efficacy. This tool is a clinical assessment reference.",
        "📚 Deep dive: Deqi Sensation (soreness, numbness, distension, heaviness) Intensity Grader",
        "When Hegu is needled and deqi is obtained, the patient feels soreness and distension radiating to the index finger.",
        "With lifting-thrusting and rotation, the practitioner feels a deep tightness under the needle, like 'a fish swallowing the bait'.",
        "If deqi is not obtained, one should wait for the qi, prompt the qi or change the point.",
        "Assessing deqi intensity",
        "The needle feels deep and tight and the patient reports local soreness and distension (grade 2, 'deqi clearly obtained'); gentle lifting-thrusting and rotation (about 120-180 times per minute) can be applied to hold the qi. If there is only pricking pain without soreness or distension (grade 0, 'deqi not obtained'), it is appropriate to retain the needle and wait for the qi, or to flick the needle handle to prompt it.",
        "What does deqi feel like?",
        "The patient feels soreness, numbness, distension, heaviness or an electric-shock-like radiation, and the practitioner feels a deep tightness under the needle; it signals that the meridian qi has arrived and that the effect is likely to be good.",
        "Does absence of deqi mean there is no effect?",
        "Not necessarily. In the elderly, in deficiency patterns and in those with diminished sensation, deqi comes slowly; one can wait for the qi or add warm needling. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Deqi Sensation Intensity Grader",
        "Deqi Sensation Intensity Grader - grades the degree of deqi from the patient's subjective sensations (soreness, numbness, distension, heaviness, propagation) and the practitioner's sense under the needle, to guide reinforcing and reducing technique. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('ear-acupressure', build('ear-acupressure', [
        "📚 Auricular Acupressure (Corresponding Regions) Illustrated Lookup",
        "Look up the body regions and indications corresponding to auricular points, with guidance on the acupressure procedure",
        "/ Auricular Acupressure Illustrated Lookup",
        "📖 View the usage guide for the Auricular Acupressure (Corresponding Regions) Illustrated Lookup",
        "Search by region",
        "Auricular zone",
        "📋 Copy the search result",
        "📋 Auricular acupressure operating standards",
        "⚠️ Acupressure is prohibited where the auricle has inflammation, chilblains or skin lesions; use with caution in pregnancy; those allergic to adhesive tape should use paper tape instead. This tool is for study reference.",
        "📚 Deep dive: Auricular Acupressure (Corresponding Regions) Illustrated Lookup",
        "For insomnia use the auricular points Shenmen, Heart and Subcortex.",
        "For stomach pain use the auricular points Stomach, Sympathetic and Spleen.",
        "For myopia use the auricular points Eye, Liver and Kidney.",
        "Look up auricular points by symptom",
        "The patient reports difficulty falling asleep and easy waking; select the auricular points Shenmen (calming), Heart (quieting the spirit) and Subcortex (regulating the central nervous system), apply vaccaria seeds, and press each point 3-5 times a day for 1-2 minutes each time.",
        "What materials are used for auricular acupressure?",
        "Vaccaria seeds and magnetic bead patches are commonly used; the physician selects the points and the patient presses them, and in summer the wearing time should be shorter to prevent detachment from sweat.",
        "Can acupressure replace treatment?",
        "No. It is a supplementary health measure; seek medical care for serious conditions. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Auricular Acupressure (Corresponding Regions) Illustrated Lookup",
        "Auricular Acupressure (Corresponding Regions) Illustrated Lookup - look up the corresponding body regions and indications of auricular points, with guidance on the pressing frequency and retention days for auricular acupressure (vaccaria seeds). A medical professional tool based on authoritative medical standards, for reference only.",
        "e.g. insomnia, stomach pain",
    ]))

    write('electroacupuncture', build('electroacupuncture', [
        "📡 Electroacupuncture Parameter (Frequency/Waveform) Selector",
        "Selects the electroacupuncture waveform, frequency and current intensity according to the treatment goal, to standardize practice",
        "📖 View the usage guide for the Electroacupuncture Parameter (Frequency/Waveform) Selector",
        "(1) Treatment goal",
        "Main goal",
        "Analgesia/pain relief",
        "Relieving spasm/muscle spasm",
        "Promoting neuromuscular function (flaccidity pattern/hemiplegia)",
        "Promoting qi and blood circulation/reducing inflammation",
        "Regulating deficiency/strengthening function",
        "Sensitive sensation",
        "Treatment region",
        "Limbs/trunk",
        "Both sides of the spine",
        "Treatment duration (minutes)",
        "(2) Recommended waveform",
        "⚙️ Generate parameters",
        "📋 Comparison table of electroacupuncture waveform characteristics",
        "⚠️ Electroacupuncture is contraindicated in pacemaker carriers and severe heart disease, on the abdomen and lumbar region of pregnant women, and near the medulla and the carotid sinus; the current intensity must stay within the patient's tolerance and must not be increased abruptly.",
        "📚 Deep dive: Electroacupuncture Parameter (Frequency/Waveform) Selector",
        "For flaccidity patterns and facial paralysis, choose the intermittent wave to promote nerve excitation.",
        "For pain and soft tissue injury, choose the dense-sparse wave.",
        "For regulating the zang-fu organs, choose the continuous wave at low frequency.",
        "Selecting electroacupuncture parameters",
        "After the acute phase of peripheral facial paralysis, connect electroacupuncture to the points on the affected side of the face, choose the dense-sparse wave at 2/15 Hz, and set the current intensity to produce slight muscle twitching within the patient's tolerance (usually 1-5 mA), for 15-20 minutes per session.",
        "What is the difference between the dense-sparse wave and the continuous wave?",
        "The dense-sparse wave alternates between sparse and dense frequencies and is better for analgesia and improving circulation; the continuous wave is constant, with low frequency sedating and high frequency analgesic, chosen according to the goal.",
        "Who cannot use electroacupuncture?",
        "It is contraindicated in pacemaker carriers and severe heart or brain disease, and on the abdomen and lumbosacral region during pregnancy; it must be operated by a physician. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Electroacupuncture Parameter (Frequency/Waveform) Selector",
        "Electroacupuncture Parameter (Frequency/Waveform) Selector - selects the electroacupuncture frequency (dense wave, sparse wave, dense-sparse wave, intermittent wave) and current intensity according to the treatment goal, to standardize electroacupuncture practice. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('flash-cupping', build('flash-cupping', [
        "🎨 Flash Cupping vs Retained Cupping (Skin Color) Comparator",
        "Compare the skin color reactions of flash cupping and retained cupping to judge the intensity of the operation and the constitution",
        "/ Flash Cupping vs Retained Cupping Skin Color Comparator",
        "📖 View the usage guide for the Flash Cupping vs Retained Cupping (Skin Color) Comparator",
        "Back and waist",
        "Shoulder and neck",
        "Observed cupping mark color",
        "Pink/flushed red",
        "Bright red",
        "Purple-red",
        "Dark purple/blue-purple",
        "Pale and whitish",
        "Blisters",
        "🔍 Compare and analyze",
        "📋 Flash cupping vs retained cupping comparison table",
        "⚠️ The cupping mark color is only a reference for constitution and the operation, not a basis for diagnosis; cupping is prohibited over skin ulcers, edema and hairy areas, and on the abdomen and lumbosacral region of pregnant women.",
        "📚 Deep dive: Flash Cupping vs Retained Cupping (Skin Color) Comparator",
        "For facial numbness, apply flash cupping until the skin flushes and then stop.",
        "For wind-cold back pain, retain the cup until the mark turns purple-red.",
        "For children and the frail, use gentle flash cupping with only slight reddening of the skin.",
        "Comparing skin reactions",
        "Taking the Bladder meridian of the back for both: after more than ten flash cupping applications the skin is evenly flushed ('flushed is the limit'), while 10 minutes of retained cupping produces a purple-red mark. The two differ in intensity: flash cupping is light and retained cupping is heavy, chosen according to constitution and purpose.",
        "Which situations is flash cupping suitable for?",
        "It is mostly used on the face, for delicate skin, or for those too frail to tolerate retained cupping; flushing is the limit and bruising is less likely.",
        "What does blistering of the skin mean?",
        "It is mostly due to retaining the cup too long, excessive negative pressure or damp predominance; reduce the intensity and manage the blisters according to protocol. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Flash Cupping vs Retained Cupping (Skin Color) Comparator",
        "Flash Cupping vs Retained Cupping (Skin Color) Comparator - compares the skin color reactions of flash cupping and retained cupping (flushed, purple-red, dark purple, blisters) to judge the intensity of the operation and the constitutional reaction. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()
