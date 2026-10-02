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
    write('hair-identification', build('hair-identification', [
        "\U0001F50D Hair (Human or Animal) Micromorphology Recognizer",
        "Identify human hair from animal hair by micromorphological features and judge the body region and damage",
        "/ Hair Recognizer",
        "\U0001F4D6 Read the \"Guide to Recognising Hair (Human / Animal) Micromorphology\"",
        "Hair Morphological Features",
        "Medullary Index (medulla width / shaft width)",
        "under 0.3 (narrow)",
        "0.3 to 0.5 (medium)",
        "over 0.5 (wide)",
        "Absent medulla",
        "Cuticle Pattern",
        "Imbricate (dense overlapping scale-like)",
        "Coronal (broad petal-like)",
        "Mosaic",
        "Pigment Distribution",
        "Evenly distributed in the cortex",
        "Concentrated around the medulla",
        "Concentrated in the outer cortex",
        "Sparse pigment",
        "Hair Diameter (\u03bcm)",
        "Hair Cross-section Morphology",
        "Round / oval",
        "Flattened oval",
        "Hair Tip Features",
        "Naturally tapered (untrimmed)",
        "Blunt cut (trimmed)",
        "Forked / worn",
        "Broken",
        "With root (hair follicle)",
        "Analyse Hair",
        "Key Points Distinguishing Human Hair from Animal Hair",
        "Human Hair",
        "Animal Hair",
        "Medullary Index",
        "under 0.3 (narrow or absent)",
        "Cuticle",
        "Dense scales in an imbricated pattern",
        "Broad scales, coronal or mosaic",
        "Concentrated around the medulla",
        "Shaft Diameter",
        "Thinner (hair about 70 to 100\u03bcm)",
        "Thicker, highly variable",
        "Cross-section Morphology",
        "Round or oval (head hair)",
        "Irregular shapes common",
        "Cortex to Medulla Ratio",
        "Broad cortex, narrow medulla",
        "Broad medulla, narrow cortex",
        "Determining the Body Region of the Hair",
        "Head Hair",
        "Diameter 70 to 100\u03bcm with a round or oval cross-section",
        "Narrow or absent medulla, evenly distributed pigment",
        "The longest, can exceed 100cm",
        "Pubic Hair",
        "Thicker in diameter, often S-shaped in curvature",
        "Irregular flattened oval cross-section",
        "Narrower medulla, darker pigment",
        "Axillary Hair",
        "Often curved with an oval cross-section",
        "Surface often shows wear and forking",
        "Medium diameter",
        "Beard / Body Hair",
        "Beard: thick (125\u03bcm) with a triangular cross-section and a broad medulla",
        "Body hair: short and fine with variable curvature",
        "Forensic Meaning of Hair Damage",
        "Root Condition",
        "Root with follicle (anagen hair)",
        ": DNA can be extracted for individual identification; plucked hairs often carry follicular sheath tissue at the root",
        "Root without follicle (telogen hair)",
        ": naturally shed hair with a club-shaped root (hair bulb)",
        "Distinguishing plucked from naturally shed hair: plucked hair usually has sheath tissue attached around the root, while naturally shed hair does not",
        "Type of Hair Damage",
        "Cut by a sharp instrument",
        ": a neat, sharp tip allowing the weapon to be inferred",
        "Snapped or torn by a blunt instrument",
        ": an irregular, brush-like tip",
        "Burning",
        ": the hair curls, swells and chars, indicating high temperature",
        "Chemical damage",
        ": the hair structure is destroyed, indicating the action of acids, alkalis or other chemicals",
        "\u26a0\ufe0f This tool is for forensic evidence teaching reference only. Real examination must use a microscope and other equipment in a professional laboratory.",
        "\U0001F4DA In-Depth Analysis: Recognising Hair (Human / Animal) Micromorphology",
        "Species Identification of Human Hair and Animal Hair",
        "Judging the Body Region and Damage of Hair",
        "Comparative Value of Hair as Evidence",
        "Identify by diameter, medullary index (medulla width / shaft width), medullary morphology (narrow in human hair, under one third, poor continuity) and scale arrangement (imbricated or irregular in human hair). Animal hair usually has a medulla wider than one half and smooth scales.",
        "A hair of 80 \u03bcm diameter with a narrow medulla (medullary index under 0.33) and chevron-shaped imbricate scales indicates human hair taken from the scalp; another of 120 \u03bcm diameter with a medulla wider than 0.5 and smooth scales indicates animal hair, excluding a human source and supporting contamination with animal hair.",
        "Can a single hair achieve individual identification?",
        "No. Morphology can only determine species and body region; individual identification requires mtDNA or nuclear DNA profiling. A hair shaft without a root has little nuclear DNA, so mitochondrial DNA is commonly used.",
        "Does bleaching or dyeing affect identification?",
        "It alters pigment and the surface, but medullary morphology and scale structure stay stable and remain identifiable. Damaged hair (broken ends, chemical treatment) must be judged together with cross-section features.",
        "About \"Hair Recognizer\"",
        "Identify human hair from animal hair by micromorphological features (medullary index, cuticle pattern, pigment distribution and so on), and judge the body region and damage features of the hair.",
        "Weighted scoring determination of human vs animal hair",
        "Automatic body region inference",
        "Hair damage feature analysis",
        "DNA extraction recommendations",
        "Hair Examination Teaching in Forensic Evidence",
        "Initial Screening of Hair Evidence",
        "Reference for Hair Damage Analysis",
        "About \"Hair (Human or Animal) Micromorphology Recognizer\"",
        "Hair (Human or Animal) Micromorphology Recognizer - a forensic evidence tool for hair morphology examination, distinguishing human from animal hair, judging body region and analysing damage features. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()