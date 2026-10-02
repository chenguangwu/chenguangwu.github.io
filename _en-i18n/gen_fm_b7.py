#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'forensic-medicine')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'forensic-medicine')
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
    out = {'slug': slug, 'industry': 'forensic-medicine', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('bone-age-estimation', build('bone-age-estimation', [
        "\u2696\ufe0f Age (Bone Age) Estimator",
        "Infer biological age from the timing of ossification centres, epiphyseal fusion and pubic symphysis morphology",
        "Core formula (over the input variables): (sb.mean \u00d7 0.45 + ribAge \u00d7 0.35 + sutureAge \u00d7 0.20); (ageByRadius + ageByMeta + ageByPhal) \u00f7 3; (ageByCarpal \u00d7 0.6 + ageByMeta \u00d7 0.4)",
        "/ Bone Age Estimator",
        "\U0001F4D6 Read the \"Guide to Using the Bone Age (Biological Age) Estimator\"",
        "Fetal Period (before birth)",
        "Infancy and Toddlerhood (0 to 6 years)",
        "Childhood (6 to 15 years)",
        "Adolescence (15 to 25 years)",
        "Adulthood (over 25)",
        "Estimate Age",
        "\u26a0\ufe0f Bone age estimation has considerable individual variation (\u00b11 to 5 years) and is affected by nutrition, disease, ethnicity and socioeconomic factors, so results are for forensic teaching and preliminary reference only.",
        "Reference Methods for Bone Age Estimation",
        "Infancy and Toddlerhood: Order of Appearance of Ossification Centres",
        "Observe on X-ray when major ossification centres first appear to infer age.",
        "Ossification Centre",
        "Male (months)",
        "Female (months)",
        "Head of the humerus",
        "birth to 3",
        "birth to 2",
        "Head of the femur",
        "birth to 4",
        "Carpal - capitate",
        "Carpal - hamate",
        "Carpal - triquetrum",
        "Carpal - lunate",
        "Carpal - trapezium",
        "Carpal - trapezoid",
        "Carpal - scaphoid",
        "Carpal - pisiform",
        "Rough estimate: carpal count \u00d7 1 year + 1 \u2248 bone age (applicable to ages 1 to 8)",
        "Adolescence: Ages of Major Epiphyseal Fusion",
        "Epiphyseal Site",
        "Male (years)",
        "Female (years)",
        "Fusion Order",
        "Sternal end of the clavicle",
        "One of the last to fuse",
        "Proximal end of the humerus",
        "Distal end of the humerus (medial epicondyle)",
        "Earlier",
        "Distal end of the radius",
        "Distal end of the ulna (olecranon)",
        "Distal end of the femur",
        "Proximal end of the tibia",
        "Distal end of the fibula",
        "Iliac crest",
        "Later",
        "Ring apophysis of the vertebral body",
        "Adulthood: Suchey-Brooks Method for the Pubic Symphysis",
        "Morphological Feature",
        "Male Age (years)",
        "Female Age (years)",
        "Stage I",
        "The symphyseal face has high relief ridges with deep grooves between them",
        "Stage II",
        "The ridges lower, the grooves shallow, and the dorsal border begins to form",
        "Stage III",
        "The ventral border forms, the symphyseal face becomes smoother and the dorsal border is complete",
        "Stage IV",
        "The symphyseal face is granular, the ventral border is complete and the dorsal border is rounded and lipped",
        "Stage V",
        "The symphyseal face is smooth, the ventral border begins to break down and the dorsal border is everted like a lip",
        "Stage VI",
        "The symphyseal face is porous, the margins are broken down and the ventral border is disrupted",
        "The Suchey-Brooks method is the most commonly used for adult age estimation, but its standard deviation is large (\u00b17 to 12 years).",
        "Other Age Estimation Methods",
        "Dental Development Method",
        "(fetus to 25 years): tooth bud calcification, root formation and third molar mineralisation.",
        "Cranial Suture Closure",
        "(25 to 60 years): the sagittal, coronal and lambdoid sutures close from the inside out.",
        "Sternal End of the Rib",
        "(20 to 60 years): ossification changes at the fourth rib end (Iscan method).",
        "Joint Surface Degeneration",
        "(over 40 years): articular cartilage degeneration and osteophyte formation.",
        "Bone Histology",
        ": the number of osteons in the cortex increases with age (Kerley method).",
        "\U0001F4DA In-Depth Analysis: Bone Age (Biological Age) Estimation",
        "Age Assessment of Minors (Criminal Responsibility Age)",
        "Ossification Centre Assessment in Fetuses and Infants",
        "Inferring the Adult Age Range from Epiphyseal Fusion",
        "Choose the method by developmental stage: use femoral length or crown-rump length to estimate gestational age in fetuses; combine the carpal appearance count (about carpal count + 1 year) with the number of metacarpal and phalangeal epiphyses in infants; use epiphyseal fusion grades and pubic symphysis morphology against standards to infer the age range in adolescents and adults.",
        "With 3 carpal bones appeared and 5 metacarpal and phalangeal epiphyses in a young child: the carpal method gives about 3 + 1 = 4 years and the epiphysis method about 5 \u00d7 0.4 + 0.5 = 2.5 years, for a weighted estimate of about 3.4 years (range about 2.4 to 4.9 years), indicating a preschool child consistent with the stage of deciduous and permanent tooth eruption.",
        "Can bone age be pinpointed to an exact birthday?",
        "No. Bone age reflects a biological development range (\u00b11 to 2 years) and is affected by nutrition, disease and region, so it only yields an age range and cannot replace household registration or a birth certificate.",
        "Do standards differ much (Greulich-Pyle vs Chinese standards)?",
        "Yes, they differ, and the standard for the population in question should be preferred (such as CHN or the Chinese 05 standard); mixing in European or American standards over- or under-estimates age.",
        "About \"Bone Age Estimator\"",
        "A forensic aid that selects a suitable bone age estimation method for each age stage (ossification centre counting, TW3 scoring, epiphyseal fusion, the Suchey-Brooks pubic symphysis method and so on) and combines them to estimate biological age.",
        "Supports estimation from the fetal period through adulthood",
        "Infants: carpal counting plus ossification centre assessment",
        "Adolescents: combined judgement of multi-site epiphyseal fusion",
        "Adults: Suchey-Brooks plus the Iscan rib method plus cranial sutures",
        "Separates male and female differences",
        "Age Assessment of Unidentified Bodies in Forensic Practice",
        "Individual Identification of Skeletal Remains",
        "Aid to Forensic Anthropology Teaching",
        "Judicial Appraisal Age Confirmation Reference",
        "About \"Age (Bone Age) Estimator\"",
        "Age (Bone Age) Estimator - infers biological age from the order of ossification centre appearance, epiphyseal fusion and pubic symphysis morphology; a forensic aid for age assessment. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()