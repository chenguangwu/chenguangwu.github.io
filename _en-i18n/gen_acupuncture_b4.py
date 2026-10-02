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
    write('needle-retention', build('needle-retention', [
        "📍 Needle Retention Time (by Disorder) Recommender",
        "Recommends the needle retention time according to the nature of the disorder and the patient's condition; retention serves to hold the qi, wait for the qi and regulate the qi",
        "/ Needle Retention Time Recommender",
        "📖 View the usage guide for the Needle Retention Time (by Disorder) Recommender",
        "(1) Category of the disease pattern",
        "Child (<= 10)",
        "Elderly (>= 65)",
        "Mixed deficiency and excess",
        "Cold pattern or winter",
        "Yes (cold pattern/winter)",
        "General regulation",
        "Analgesia",
        "Calming the spirit and sedating",
        "⏲️ Recommend retention",
        "📋 Needle retention time reference",
        "⚠️ Retention time must be adapted to the individual and the pattern; for children, the frail and those prone to fainting during acupuncture, retain briefly or not at all. This tool is for reference.",
        "📚 Deep dive: Needle Retention Time (by Disorder) Recommender",
        "For deficiency and cold patterns, retain the needles longer to wait for the qi (30-40 min).",
        "For excess and heat patterns, retain briefly (10-20 min).",
        "For acute pain patterns, manipulate the needle intermittently during retention.",
        "Recommend the retention time",
        "For stomach pain from spleen-stomach deficiency cold (deficiency, cold), retain for 30 minutes and rotate the needle once every 10 minutes to warm and move the qi; for wind-heat common cold with high fever (excess, heat), retain for 10-15 minutes with shallow insertion and quick withdrawal, and do not retain for long.",
        "Is a longer retention always better?",
        "No. It depends on the deficiency, excess, cold or heat of the pattern; the purpose of a long retention is to hold and wait for the qi. An excessive duration brings no benefit and increases tension. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "Can the patient move during retention?",
        "Points on the distal limbs allow moderate movement to help the qi arrive, while points near joints or deeply needled sites require lying still to prevent needle bending; follow medical advice.",
        "About the Needle Retention Time (by Disorder) Recommender",
        "Needle Retention Time (by Disorder) Recommender - recommends the acupuncture retention time from the nature of the disorder (acute, chronic, deficiency or excess, pain pattern) and the patient's condition, adjusted for season and age. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('needling-depth', build('needling-depth', [
        "📏 Needling Depth (by Build/Region) Standard Lookup",
        "Look up the standard needling depth of commonly used points, with individual adjustment of the depth and angle according to build, age and region",
        "/ Needling Depth Standard Lookup",
        "📖 View the usage guide for the Needling Depth (by Build/Region) Standard Lookup",
        "Select the point",
        "Age group",
        "Child (<= 10 years)",
        "Youth/middle age",
        "Constitution (optional)",
        "Frail",
        "Strong",
        "🔍 Look up the depth",
        "Please select a point and search",
        "📌 Principles of insertion angle and depth",
        "⚠️ Deep needling of the chest and back points carries a risk of organ injury, so the depth and direction must be strictly controlled. This tool is for reference; actual needling must be performed by a licensed physician.",
        "📚 Deep dive: Needling Depth (by Build/Region) Standard Lookup",
        "Chest and back points are needled shallowly to prevent pneumothorax.",
        "Zusanli is needled deeply into the muscle layer according to build.",
        "For children and the elderly, reduce both the amount and the depth.",
        "Look up and individualize the depth",
        "For Zusanli (3 cun below Dubi), standard insertion is about 30-40 mm; in thin patients reduce it to 20-25 mm, and in obese patients it may reach 40-50 mm but must not be forced deeply. Chest and back points (such as Feishu) are only 5-10 mm with oblique insertion, strictly avoiding deep perpendicular insertion that injures the lung.",
        "Why needle the chest and back shallowly?",
        "The thoracic cavity contains the lungs, so deep perpendicular insertion risks pneumothorax; these points are usually needled obliquely toward the spine with the depth controlled.",
        "How is the depth individualized for build?",
        "Use the arrival of deqi together with the anatomical layer: shallower for the thin and deeper for the sturdy, with a reduced amount for the elderly and children. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Needling Depth (by Build/Region) Standard Lookup",
        "Needling Depth (by Build/Region) Standard Lookup - look up the needling depth of commonly used points and individualize it according to the patient's build (thin, medium, obese), age and region. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('pediatric-tuina', build('pediatric-tuina', [
        "💊 Pediatric Tuina (Age/Point) Dose Converter",
        "Converts the number of tuina strokes, the time and the pressure according to the child's age, with dosage guidance for commonly used points",
        "/ Pediatric Tuina Dose Converter",
        "📖 View the usage guide for the Pediatric Tuina (Age/Point) Dose Converter",
        "(1) Child's age",
        "Exact age in months (optional, overrides the group above)",
        "Condition",
        "Acute",
        "🔢 Convert the dose",
        "📋 Dosage for commonly used pediatric tuina points",
        "⚠️ Pediatric tuina should be 'light, quick, gentle, steady and substantial'; tuina is contraindicated with broken skin, fractures, acute infectious disease and bleeding disorders. This tool is for reference.",
        "📚 Deep dive: Pediatric Tuina (Age/Point) Dose Converter",
        "For infants, reinforcing the Spleen meridian uses more strokes than for older children.",
        "For fever, clearing the Tianhe water sets the operating time by age.",
        "For diarrhea, abdominal rubbing uses light pressure and a steady rhythm.",
        "Convert the dose by age",
        "For a 2-year-old with spleen deficiency, reinforce the Spleen meridian (radial side of the thumb) about 300 times and rub the abdomen for 5 minutes with gentle, caressing pressure; for a 6-year-old, about 500 strokes over 8-10 minutes, increasing with age, with slight reddening of the skin as the limit.",
        "Why is the number of strokes based on age?",
        "Children have 'delicate yin and delicate yang', so the dose increases with age and constitution; too little is ineffective and too much damages the upright qi. This tool gives a reference range.",
        "Can a medium be used?",
        "Body powder and massage oil are commonly used for lubrication to prevent abrasion; warm the hands in winter and avoid wind and cold. Seek medical care for serious conditions.",
        "About the Pediatric Tuina (Age/Point) Dose Converter",
        "Pediatric Tuina (Age/Point) Dose Converter - converts the number of strokes, time and pressure according to the child's age, and provides dosage guidance for common pediatric tuina points and techniques. A medical professional tool based on authoritative medical standards, for reference only.",
        "e.g. 18",
    ]))

    write('recommender-acupoint', build('recommender-acupoint', [
        "💊 Acupoint Combination (Four Gates) Recommendation",
        "Four Gates",
        "📖 View the usage guide for the Acupoint Combination (Four Gates) Recommendation",
        "The Four Gates centers on Hegu paired with Taichong: Hegu lies at the midpoint of the radial side between the first and second metacarpal bones (governing disorders of the head, face and upper limbs), and Taichong lies on the dorsum of the foot between the first and second metatarsal bones (governing soothing the liver and regulating qi). Together they mainly treat qi stagnation and depression, headache and insomnia. Other common pairings are Neiguan with Gongsun (heart, chest and stomach), Zusanli with Zhongwan (strengthening the spleen and harmonizing the stomach), and Sanyinjiao with Guanyuan (nourishing the source and gynecology); 2 to 4 points are taken each time and the needles are retained for 20 to 30 minutes.",
        "📚 Deep dive: Acupoint Combination (Four Gates) Recommendation",
        "To regulate liver depression, take Hegu and Taichong.",
        "To calm the spirit and settle the mind, add Shenmen and Sanyinjiao.",
        "For disorders of the head and face, take Hegu with Fengchi.",
        "Recommend combinations by regulation goal",
        "For the goal 'soothing the liver and regulating qi', bilateral Hegu plus bilateral Taichong (the Four Gates) are recommended, with Xingjian added on the same meridian as Taichong to clear the liver. Hegu lies on the back of the hand between the 1st and 2nd metacarpal bones and Taichong on the dorsum of the foot between the 1st and 2nd metatarsal bones, for reference when locating the points.",
        "Is the Four Gates suitable for everyone?",
        "It is mostly used for qi stagnation, pain patterns and mental disorders; Hegu and Sanyinjiao are contraindicated in pregnancy, and it should be used with caution in those with a bleeding tendency. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "Are more paired points better?",
        "No. The main and adjunct points should be clear and few but well chosen, avoiding a jumble of many points; needling should be performed by a physician according to pattern differentiation.",
        "About the Acupoint Combination (Four Gates) Recommendation",
        "Acupoint Combination (Four Gates) Recommendation. A free online tool with pure front-end processing; data is not uploaded, protecting your privacy and security.",
        "How to use the Acupoint Combination (Four Gates) Recommendation",
        "Number generated",
    ]))

    write('recommender-time', build('recommender-time', [
        "📍 Needle Retention Time (by Disorder) Recommendation",
        "By disorder",
        "📖 View the usage guide for the Needle Retention Time (by Disorder) Recommendation",
        "Retention time depends on the disorder and the constitution: 20 to 30 minutes for general disorders, 10 to 20 minutes for acute pain, and 30 to 45 minutes for chronic deficiency patterns. The frail, the elderly, children and those undergoing acupuncture for the first time should have a short retention (10 to 20 minutes), while the sturdy with excess heat may have it extended appropriately. Usually the treatment is given once daily or every other day, with 10 to 12 sessions per course and a rest of 3 to 5 days between courses. Fainting during acupuncture, hunger, fatigue, and the lumbar and abdominal points in pregnancy call for shortening or avoidance.",
        "📚 Deep dive: Needle Retention Time (by Disorder) Recommendation",
        "For cold and deficiency patterns the retention is relatively long.",
        "For acute pain patterns, retain and manipulate the needle at the same time.",
        "For the elderly, the frail and children the retention is relatively short.",
        "Recommend retention by disorder",
        "For deficiency-cold joint pain, retain for 25-30 minutes and manipulate the needle every 10 minutes; for wind-heat sore throat, use shallow insertion and retain for 10-15 minutes, shortened by another third for the elderly and children. Contraindications such as fainting during acupuncture and stuck needles are also flagged.",
        "What should be watched during retention?",
        "Watch for fainting during acupuncture (palpitations, sweating) and stuck needles; press on withdrawal to prevent bleeding. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "Why is 'not a prescription' emphasized?",
        "Retention time must be combined with pattern differentiation and varies greatly between individuals, so it cannot replace a physician's prescription.",
        "About the Needle Retention Time (by Disorder) Recommendation",
        "Needle Retention Time (by Disorder) Recommendation. A free online tool with pure front-end processing; data is not uploaded, protecting your privacy and security.",
    ]))


if __name__ == '__main__':
    main()
