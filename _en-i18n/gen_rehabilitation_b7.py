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
    write('water-swallow-test', build('water-swallow-test', [
        "\U0001F4CC Swallowing Function (Kubota Water Drinking Test) Grader",
        "The Kubota Water Drinking Test lets the patient drink 30 mL of warm water and grades swallowing function by time and performance",
        "In the Kubota water drinking test the patient drinks 30 mL of warm water while being observed: grade 1 means finished in one go within 5 seconds with no choking (normal); grade 2 means finished in 2 or more goes with no choking (questionable); grade 3 means finished in one go with choking (abnormal); grade 4 means finished in 2 or more goes with choking (abnormal); grade 5 means repeated choking with difficulty swallowing it all (abnormal). Grade 1 is normal, grade 2 is questionable and needs re-evaluation, and grades 3 to 5 indicate dysphagia, so aspiration risk should be assessed and the feeding method and food texture adjusted.",
        "Safety note:",
        "This test carries a risk of choking and aspiration and must be performed under professional supervision. If the patient is known to have severe dysphagia, this test is not recommended.",
        "Test result input",
        "Drinking time (seconds)",
        "Drinking performance",
        "Finished in one go, no choking",
        "Finished in two goes, no choking",
        "Finished in one go, with choking",
        "Finished in two goes, with choking",
        "Frequent choking, difficulty swallowing it all",
        "Enter the test result",
        "\U0001F4CCA Kubota water drinking test grading standard",
        "Swallowing function",
        "Finished in one go, no choking (within 5 s)",
        "Normal eating",
        "Finished in one go, no choking (over 5 s)",
        "Watch closely and assess further",
        "Adjust food texture, swallowing training",
        "The diet form must change, professional swallowing therapy needed",
        "Grade V",
        "Frequent choking, difficult to swallow",
        "Tube feeding nutrition and systematic swallowing rehabilitation needed",
        "\U0001F4D6 Diet recommendation by grade",
        "Normal diet (grades I-II)",
        "A normal diet can be taken with careful chewing and slow eating. Grade II patients should avoid very dry or hard foods and stay upright while eating.",
        "Adjusted diet (grade III)",
        "Soft or semi-liquid food is recommended, avoiding dry, hard and fibrous foods. Keep the bite size moderate (about 15-20 mL), allow plenty of mealtime and maintain the correct posture.",
        "Special diet (grade IV)",
        "Puréed food or thickened liquids are recommended, avoiding thin liquids and mixed-texture foods. A professional swallowing therapist should guide direct swallowing training.",
        "Tube feeding nutrition (grade V)",
        "Nasogastric or PEG tube feeding support is needed. Try indirect swallowing training under professional assessment guidance and gradually transition to oral intake once function improves.",
        "\U0001F4CC Assessment record",
        "\U0001F4DDA In-depth analysis: swallowing function (Kubota water drinking test) grading",
        "Stroke screening",
        "Aspiration risk",
        "Oral intake",
        "Grade 1 normal",
        "Finishing 30 mL in one go within 5 s with no choking is grade 1 and oral intake is fine; over 5 s or finishing in 2 goes is grade 2 and needs observation.",
        "Grade 3 abnormal",
        "Finishing in 2 or more goes or with choking is grade 3, with aspiration risk; switch to puréed food plus swallowing training and use nasogastric feeding if necessary.",
        "How are the grades defined?",
        "1 normal, 2 questionable, 3 over 2 goes or choking, 4 choking throughout, 5 cannot swallow; grade 3 or above calls for instrumental swallowing assessment.",
        "Does a normal result mean the patient can eat normally?",
        "Not on its own. The Kubota test mainly screens for overt aspiration: drinking 30 mL of warm water smoothly in one go is grade 1. But some patients have silent aspiration (food enters the airway without choking), which the Kubota test cannot detect. So a grade 1 patient who still has recurrent fever, increased sputum or weight loss needs further FEES (fiberoptic endoscopic evaluation of swallowing) or VFSS (videofluoroscopic swallowing study). Also note that water temperature and thickness affect the result, so testing should consistently use room-temperature water.",
        "About the Swallowing Function (Kubota Water Drinking Test) Grader",
        "Swallowing Function (Kubota Water Drinking Test) Grader." + DISCL_M,
        "e.g. 8",
    ]))
    write('wheelchair-posture', build('wheelchair-posture', [
        "\U0001F39A\ufe0f Wheelchair Seated Posture (Pressure Distribution) Optimizer",
        "Computes wheelchair seated posture parameters and pressure distribution to prevent pressure ulcers and optimize sitting balance",
        "Core formulas (from the input variables): ischialPressure / 133.322; force / (2 x 5); hipW + 2",
        "Wheelchair parameters",
        "Seat width (cm)",
        "Seat depth (cm)",
        "Seat height (cm)",
        "Backrest height (cm)",
        "Cushion type",
        "No cushion / ordinary foam",
        "Gel cushion",
        "Air cushion",
        "Memory foam cushion",
        "Honeycomb silicone cushion",
        "Enter parameters to compute the seated posture recommendations",
        "\U0001F4D6 Pressure ulcer prevention reference",
        "Ischial tuberosity pressure",
        "The ischial tuberosities bear the highest pressure when seated, normally about 75-100 mmHg. Above 32 mmHg lasting more than 2 hours can cause tissue ischemia, so relieve pressure every 15-30 minutes.",
        "Wheelchair dimension standard",
        "Seat width = hip width + 2-3 cm (1-1.5 cm clearance on each side)",
        "Seat depth = distance from the popliteal fossa to the back of the buttocks - 2-5 cm (leave popliteal clearance)",
        "Seat height = distance from the sole to the popliteal fossa + footplate height (5-8 cm off the floor)",
        "Backrest height: above the inferior angle of the scapula for high-level paraplegia; 5-10 cm below the armpit for low-level paraplegia",
        "Cushion pressure relief performance",
        "Air cushion: best pressure relief, reduces ischial pressure by 60-70%",
        "Honeycomb silicone: good pressure relief, reduces 50-60%, with good stability",
        "Gel cushion: reduces 40-50%, with a cooling effect",
        "Memory foam: reduces 30-40%, with high comfort",
        "Ordinary foam: reduces 10-20%, suitable for low-risk patients",
        "\U0001F4CC Calculation record",
        "\U0001F4DDA In-depth analysis: wheelchair seated posture (pressure distribution) optimization",
        "Pressure ulcer prevention",
        "Seat width fitting",
        "Cushion selection",
        "Ideal seat width 38 cm",
        "Hip width 36 cm gives an ideal seat width of 38 cm; weight 65 kg gives an ischial pressure of 65 x 9.8/(2 x 5) = 63.7 Pa, and a foam cushion reducing pressure by 30% brings it to about 0.33 mmHg equivalent.",
        "Seat depth too long",
        "Seat depth 45 > 42, so the ideal is 40 cm; too long presses on the popliteal fossa and tips the pelvis backward, so shorten it by 5 cm and add lumbar support to maintain the lumbar curve.",
        "How do I choose a cushion?",
        "Use foam for low risk and gel, air or honeycomb cushions for medium to high risk (30-60% pressure reduction), and lift the hips every 15-30 minutes to prevent pressure ulcers.",
        "How often should pressure be relieved?",
        "Relieve pressure every 15-30 minutes (lifting the hips off the seat with both hands for 10-15 seconds, or leaning forward or sideways), because a cushion can only distribute pressure and cannot replace relief. Patients with existing pressure ulcers need the frequency raised to every 15 minutes. The effect depends on complete unloading, and merely shifting body weight is not enough; patients who can lift themselves are best, otherwise a caregiver must assist on schedule.",
        "About the Wheelchair Seated Posture (Pressure Distribution) Optimizer",
        "Wheelchair Seated Posture (Pressure Distribution) Optimizer." + DISCL_M,
        "e.g. 65",
        "e.g. 85",
        "e.g. 40",
        "e.g. 42",
        "e.g. 45",
    ]))


if __name__ == '__main__':
    main()