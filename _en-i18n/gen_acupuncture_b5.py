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
    write('tuina-frequency', build('tuina-frequency', [
        "📡 Tuina Technique Frequency (Times per Minute) Standardizer",
        "Look up the standard frequency range of common tuina techniques and convert the technique rhythm according to the treatment goal",
        "/ Tuina Technique Frequency Standardizer",
        "📖 View the usage guide for the Tuina Technique Frequency (Times per Minute) Standardizer",
        "(1) Select the technique",
        "Relaxation and relieving spasm",
        "Excitation and activation",
        "Warming and unblocking qi and blood",
        "Patient tolerance",
        "Sensitive/frail",
        "Good tolerance/sturdy",
        "Planned operating time (minutes)",
        "📊 Calculate the frequency",
        "📋 Tuina technique frequency standard table",
        "⚠️ The frequency is a reference range; in actual operation it must be 'within the patient's comfort', and the technique requires being 'sustained, forceful, even, gentle and penetrating'.",
        "📚 Deep dive: Tuina Technique Frequency (Times per Minute) Standardizer",
        "Palm-root pressing and kneading on the back and waist, about 120-160 times/min.",
        "One-finger meditation pushing, about 120-140 times/min.",
        "The vibration technique is high frequency, about 600-800 times/min.",
        "Look up the standard frequency",
        "For adult shoulder and neck soreness using the grasping and kneading techniques, the kneading frequency is about 120-160 times/min for 3-5 minutes per area; for a child with spleen deficiency using Spleen meridian reinforcement, the frequency is steady and the pressure light, about 100-120 times/min, with an even rhythm as the key point.",
        "Is a higher frequency always better?",
        "No. It depends on the technique and the goal: relaxation suits a medium speed, the vibration technique needs high frequency, and reinforcement suits a slow speed; too fast causes fatigue while too slow is ineffective.",
        "Can tuina be done at home?",
        "Light techniques for health maintenance are feasible, while heavy techniques and joint manipulation require a professional; seek medical care if pain persists. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Tuina Technique Frequency (Times per Minute) Standardizer",
        "Tuina Technique Frequency (Times per Minute) Standardizer - look up the standard frequency range of common tuina techniques (pushing, grasping, kneading, rolling, pressing, rubbing) and convert the rhythm according to the treatment goal. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('tuina-medium', build('tuina-medium', [
        "📍 Tuina Medium (Oil/Ointment) Selection Guide",
        "Recommends tuina media according to the technique, disorder, season and skin type, providing lubrication and a synergistic medicinal effect",
        "/ Tuina Medium Selection Guide",
        "📖 View the usage guide for the Tuina Medium (Oil/Ointment) Selection Guide",
        "Main technique",
        "Kneading/rubbing",
        "Scrubbing/pushing",
        "Rolling",
        "Pressing/point pressing",
        "Plucking/flicking",
        "Patting/striking",
        "Relaxation and soothing the sinews",
        "Dispelling cold and warming the channels",
        "Activating blood and resolving stasis",
        "Releasing the exterior and inducing sweating",
        "Pediatric tuina",
        "Skin type/region",
        "Oily",
        "📍 Recommend a medium",
        "📋 Overview of common tuina media",
        "⚠️ A skin allergy test should be done before using a medium; media containing irritant ingredients should not be used on broken or infected skin; mild media should be used for children's delicate skin.",
        "📚 Deep dive: Tuina Medium (Oil/Ointment) Selection Guide",
        "For dry skin and the scrubbing technique, massage oil is often used.",
        "For children and in summer, body powder is used to reduce stickiness.",
        "For soft tissue injury, a blood-activating and stasis-resolving ointment is used.",
        "Choose the medium according to the situation",
        "For the scrubbing technique on an adult's back in winter (to prevent skin injury), choose petrolatum or massage oil for lubrication; for pediatric spine pinching use body powder to keep the skin dry; in the early stage of a traumatic injury use a blood-activating medium such as safflower oil, but it is contraindicated on broken skin.",
        "What is the role of the medium?",
        "It lubricates to prevent injury and also supports the medicinal action (such as dispersing cold or activating blood), chosen according to the technique and the pattern.",
        "What should be done about allergy?",
        "Try it first on a small area, and stop and wash it off if redness or itching appears. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Tuina Medium (Oil/Ointment) Selection Guide",
        "Tuina Medium (Oil/Ointment) Selection Guide - recommends tuina media (oil, ointment, powder, wine) according to the technique, disorder, season and skin type, providing lubrication and a synergistic medicinal effect. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('warm-needle-moxibustion', build('warm-needle-moxibustion', [
        "🌡️ Warm Needling (Temperature Regulation) Simulator",
        "Simulates the temperature change of the burning moxa segment in warm needling and estimates the heat received at the point and the safety parameters",
        "/ Warm Needling Temperature Regulation Simulator",
        "📖 View the usage guide for the Warm Needling (Temperature Regulation) Simulator",
        "(1) Moxa segment specification",
        "Number of moxa segments burned per needle",
        "1 segment",
        "2 segments",
        "3 segments",
        "Needle body length (cun)",
        "1 cun",
        "1.5 cun",
        "2 cun",
        "Patient tolerance (adjustment)",
        "🌡️ Simulate the temperature",
        "📋 Warm needling operating standards",
        "⚠️ The moxa ash in warm needling falls off easily and can burn the skin, so a piece of stiff cardboard should be placed to protect the skin. Use caution where the needle hole is infected or the skin is ulcerated, and in those unable to cooperate. This tool is a simulation reference.",
        "📚 Deep dive: Warm Needling (Temperature Regulation) Simulator",
        "Simulate the burning temperature curve of the moxa segment to estimate the heat received.",
        "Calculate the safe upper limit of the skin surface temperature at the point.",
        "Adjust the number of moxa segments and the spacing to control the temperature and prevent burns.",
        "Simulate the heat received in warm needling",
        "In warm needling, 1-2 moxa cones are placed on the needle handle (about 2 cm each) and burn out in about 5-8 minutes; conduction along the needle body raises the skin temperature at the point to about 40-45 C. If the skin temperature exceeds 48 C or there is burning pain, reduce the number of segments or add an insulating barrier to prevent burns.",
        "How is the temperature of warm needling controlled?",
        "The guide is that the patient feels comfortably warm without burning pain, with 1-2 moxa segments at an appropriate distance from the skin and with dedicated supervision. This tool is a simulation reference.",
        "Who should use it with caution?",
        "Use with caution in those with diminished sensation (such as diabetic peripheral neuropathy), thin delicate skin, or a bleeding tendency; the procedure must be performed by a professional to prevent burns.",
        "About the Warm Needling (Temperature Regulation) Simulator",
        "Warm Needling (Temperature Regulation) Simulator - simulates the temperature curve of the burning moxa segment in warm needling and, together with the retention time and moxa segment specification, estimates the heat received at the point and the safety distance. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()
