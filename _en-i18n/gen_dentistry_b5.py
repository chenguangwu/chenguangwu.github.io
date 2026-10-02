#!/usr/bin/env python3
# gen_dentistry_head.py — shared head for dentistry batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dentistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dentistry')
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
    out = {'slug': slug, 'industry': 'dentistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('tooth-preparation', build('tooth-preparation', [
        "Tooth Preparation Taper and Retention Assessor",
        "Assesses the retention and resistance form of full crowns/inlays from total axial-wall taper, preparation height and base diameter.",
        'View "Tooth Preparation Taper and Retention Assessor User Guide"',
        "Total axial-wall taper (deg)",
        "Preparation height (mm)",
        "Base diameter / width (mm)",
        "Restoration type",
        "Full crown",
        "Onlay",
        "Inlay",
        "Veneer",
        "This tool estimates from classic retention principles; actual retention is also affected by cement, path of insertion and auxiliary retention (axial groove / box).",
        "Retention Principle and Reference",
        "Jorgensen relation: the larger the taper, the sharper the drop in frictional retention.\nIdeal total taper: 3-10 deg (1.5-5 deg per wall)\nClinically acceptable: <=20 deg\nRetention index is proportional to height/diameter x cos(taper)\n\nHeight/diameter ratio (H/D) >= 0.4 aids retention and resistance.",
        "Taper",
        "Relative retention value",
        "Insufficient retention",
        "In-Depth: Tooth Preparation Taper and Retention Assessor",
        "For a full crown with large taper, after entering parameters the tool warns of reduced retention and suggests decreasing the taper.",
        "For insufficient preparation height, quantify the gap to minimum retention height, suggesting crown lengthening or post-core.",
        "For inlay cavity, assess resistance form, suggesting wall thickness and rounded line angles. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Retention Estimation",
        "Input: axial-wall taper 6 deg/side (total 12 deg), prep height 4mm, base diameter 5mm\nDetermination: taper and height are in the acceptable range for routine full-crown retention; if taper >20 deg retention drops markedly.",
        "Why does taper affect retention?",
        "Larger taper makes the axial wall more flared, reducing frictional retention area and the crown easily comes off; clinically keep total taper 10-20 deg balancing retention and seating.",
        "What if preparation height is insufficient?",
        "Use crown lengthening or post-core rebuild to increase clinical crown height; too short raises dislodgement risk, designed by a prosthodontist.",
        "What does resistance form mean?",
        "It means the restoration and abutment can bear occlusal force without fracture, requiring thick walls, rounded line angles and no weak cusps; specific to the dentist's preparation.",
        "About the Tooth Preparation Taper and Retention Assessor",
        "Tooth Preparation Taper and Retention Assessor - Assesses full-crown retention and resistance form from axial-wall taper, preparation height and base width. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('wisdom-tooth', build('wisdom-tooth', [
        "Impacted Wisdom Tooth Pell-Gregory Classifier",
        "Classifies by the relation of the mandibular third molar to the anterior ramus border and occlusal plane, combined with Winter classification angle to assess extraction difficulty.",
        "Impacted Wisdom Tooth Pell-Gregory Classifier",
        "/ Impacted Wisdom Tooth Pell-Gregory Classifier",
        'View "Impacted Wisdom Tooth Pell-Gregory Classifier User Guide"',
        "1. Relation to anterior ramus border (horizontal class)",
        "Anterior ramus border to second molar distal",
        "Class I: space >= mesiodistal crown diameter",
        "Class II: space < mesiodistal crown diameter",
        "Class III: wisdom tooth entirely within the ramus",
        "2. Relation to occlusal plane (depth class)",
        "Wisdom-tooth occlusal-surface position",
        "Class A: level with second-molar occlusal plane",
        "Class B: between occlusal plane and cervix",
        "Class C: below second-molar cervix",
        "3. Winter classification (impaction direction)",
        "Long-axis angle",
        "Vertical impaction",
        "Mesial impaction (most common)",
        "Horizontal impaction",
        "Distal impaction (most difficult)",
        "Buccolingual impaction",
        "Inverted impaction (rare)",
        "Completely bone-impacted?",
        "No (partially erupted / soft-tissue impacted)",
        "Yes (completely bone-impacted)",
        "Root morphology",
        "Normal / fused root",
        "Curved root",
        "Bifurcated root",
        "Root-bone ankylosis",
        "Extraction difficulty is also affected by surgeon experience, mouth opening, neighboring teeth and distance to the inferior alveolar nerve. This assessment is for pre-op reference.",
        "Pell-Gregory Classification Notes",
        "Horizontal class (relation to ramus)",
        "Class I: enough space between anterior ramus border and second-molar distal to fit the wisdom-tooth mesiodistal diameter",
        "Class II: space smaller than the wisdom-tooth mesiodistal diameter",
        "Class III: wisdom tooth entirely inside the anterior ramus border",
        "Depth class (relation to occlusal plane)",
        "Class A: wisdom-tooth occlusal surface level with second-molar occlusal plane (highest)",
        "Class B: between occlusal plane and second-molar CEJ",
        "Class C: below second-molar CEJ (deepest)",
        "Difficulty-score reference (Pederson difficulty index)",
        "Horizontal: Class I=1, II=2, III=3",
        "Depth: A=1, B=2, C=3",
        "Direction: vertical=1, mesial=2, horizontal=3, distal=4",
        "In-Depth: Impacted Wisdom Tooth Pell-Gregory Classifier",
        "For mesially impacted wisdom tooth, enter relation to ramus border / occlusal plane; the tool gives the Pell-Gregory class and difficulty.",
        "Horizontal impaction overlapping the inferior alveolar nerve suggests high extraction risk needing CBCT.",
        "Vertical impaction with adequate space suggests relatively low difficulty but still needs pericoronal assessment. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Pell-Gregory Classification",
        "Input: wisdom-tooth crown entirely in front of the anterior ramus border (Class I), above occlusal plane (Class A), mesial tilt 45 deg\nDetermination: I-A class, relatively adequate space, lower difficulty; if Class II/III or B/C position, difficulty rises.",
        "How many Pell-Gregory classes are there?",
        "By relation to ramus border: Class I/II/III (decreasing space); by relation to occlusal plane: Class A/B/C (descending position); combined to assess difficulty.",
        "What is the Winter classification?",
        "By impaction direction: vertical, mesial, distal, horizontal, buccolingual, etc.; horizontal/mesial impaction is often harder, needs imaging.",
        "When should wisdom teeth be extracted?",
        "Recurrent pericoronitis, caries, proximal pressure resorption, cyst or orthodontic need; those near the inferior alveolar nerve need CBCT, assessed by oral-maxillofacial surgery.",
        "About the Impacted Wisdom Tooth Pell-Gregory Classifier",
        "Impacted Wisdom Tooth Pell-Gregory Classifier - Performs Pell-Gregory classification from the mandibular impacted wisdom tooth relation to the ramus and occlusal plane, assessing extraction difficulty. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('zirconia-aesthetics', build('zirconia-aesthetics', [
        "Zirconia (Translucency) Aesthetics Assessor",
        "Recommends a suitable zirconia generation (3Y-5Y) and translucency by restoration site, aesthetic need and shade, balancing strength and aesthetics.",
        "Zirconia Translucency Aesthetics Assessor",
        "/ Zirconia Translucency Aesthetics Assessor",
        'View "Zirconia (Translucency) Aesthetics Assessor User Guide"',
        "Restoration site",
        "Anterior (aesthetic zone)",
        "Posterior (molar zone)",
        "Three-unit fixed bridge",
        "Long-span bridge (>=4 units)",
        "Aesthetic need",
        "High (anterior aesthetics / high smile line)",
        "Low (function first)",
        "Abutment color",
        "Normal (vital / light)",
        "Discolored tooth (non-vital / metal post)",
        "Metal abutment / implant",
        "Target shade",
        "A1-A2 (brighter)",
        "A3 (medium)",
        "A3.5-A4 (darker)",
        "Occlusal-force condition",
        "Bruxism / clenching",
        "Low occlusal force",
        "Restoration form",
        "Single crown",
        "Fixed bridge",
        "Veneer / inlay",
        "Recommended material",
        "Zirconia translucency and strength are inversely related. High-translucency materials look better but lower strength; weigh by site and occlusal force.",
        "Zirconia Generation Comparison",
        "Generation",
        "Y2O3 content",
        "Translucency",
        "Flexural strength",
        "3Y-TZP (first gen)",
        "Low (opaque)",
        "Posterior crown / long bridge, strong masking",
        "4Y-PSZ (second gen)",
        "Premolar / anterior backing crown",
        "5Y-PSZ (third gen)",
        "High (translucent)",
        "Anterior aesthetic single crown",
        "6Y (experimental)",
        "Veneer (low occlusion)",
        "Selection principle",
        "Aesthetic zone + normal abutment -> 5Y high-translucent, mimics natural tooth",
        "Discolored abutment / implant -> 3Y masking layer + 5Y veneering porcelain (layered)",
        "Posterior / bruxism -> 3Y high-strength, avoid 5Y",
        "Long-span bridge -> 3Y ensures connector strength",
        "Reference: Prosthodontics zirconia ceramic materials chapter; ISO 6872 dental ceramic standard.",
        "In-Depth: Zirconia (Translucency) Aesthetics Assessor",
        "For anterior all-ceramic restoration, enter site and shade; the tool recommends a high-translucent generation and suggests labial veneering.",
        "For posterior high-occlusal-force zones, favor strength and choose conventional-translucent generation.",
        "Obvious shade difference suggests matching translucency to neighboring teeth to avoid dead white. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Recommendation by Site and Shade",
        "Input: maxillary lateral incisor, high aesthetic need, shade 1M1\nOutput: recommend 5Y high-translucent zirconia, translucency close to natural enamel; posterior zone 3Y to balance strength, veneering if needed.",
        "How to choose 3Y/4Y/5Y?",
        "Anterior aesthetic zone leans 4Y/5Y (high-translucent), posterior occlusal zone leans 3Y (high-strength); specifically set by the prosthodontist combining occlusal force and opposing teeth.",
        "What does translucency affect?",
        "Translucency decides whether the restoration looks dead white and has depth; too high translucency over a dark substrate may show the base color, needing veneering or a moderate generation.",
        "Is shade important?",
        "Yes. Shade error makes the restoration stand out under natural light; this tool is only a generation pre-screening; formal shade-taking and bonding are done by the dentist.",
        "About the Zirconia Translucency Aesthetics Assessor",
        "Zirconia Translucency Aesthetics Assessor - Recommends zirconia generation and translucency choice by restoration site, aesthetic need and shade. A professional medical tool based on authoritative standards, for reference only.",
        "How to use the Zirconia (Translucency) Aesthetics Assessor",
        "Suitable as pre-screening reference when planning restoration: choosing zirconia generation (3Y-5Y) by site and aesthetic need, assessing shade-translucency match, and weighing material between anterior aesthetic and posterior functional zones.",
        "What does the Zirconia (Translucency) Aesthetics Assessor do?",
        "How to use the Zirconia (Translucency) Aesthetics Assessor?",
        "Which scenarios suit the Zirconia (Translucency) Aesthetics Assessor?",
    ]))

if __name__ == "__main__":
    main()
