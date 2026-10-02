#!/usr/bin/env python3
# gen_reproductive-medicine_head.py — shared head for reproductive-medicine batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'reproductive-medicine')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'reproductive-medicine')
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
    out = {'slug': slug, 'industry': 'reproductive-medicine', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('detector-9', build('detector-9', [
        "🔍 Retrograde Ejaculation (Urine Sperm) Detector",
        "Aids diagnosis of retrograde ejaculation by comparing sperm parameters in ejaculated semen and post-ejaculation urine.",
        'View "Retrograde Ejaculation (Urine Sperm) Detector User Guide"',
        "📐 Calculation logic",
        "Ejaculate total sperm ejTotal = ejVol × ejConc",
        "Urine total sperm urTotal = urVol × urConc",
        "Retrograde ratio retroPct = urTotal / (ejTotal + urTotal) × 100%",
        "Criteria: semen volume < 1.5ml AND retroPct \u2265 50% AND urTotal > 5\u00d710\u2076 \u2192 marked retrograde ejaculation",
        "Ejaculated semen parameters (antegrade)",
        "Semen volume (ml)",
        "Sperm concentration (million/ml)",
        "Post-ejaculation urine parameters (retrograde)",
        "Urine volume (ml)",
        "Urine sperm concentration (million/ml)",
        "Urine fructose test",
        "Assess the test result",
        "Key points for retrograde-ejaculation diagnosis: very low semen volume (often <1ml) + large numbers of sperm found in post-ejaculation urine",
        "Normal semen-volume reference: \u22651.5ml (WHO 5th-edition standard)",
        "Positive urine fructose suggests seminal-vesicle fluid refluxed into the bladder, supporting retrograde-ejaculation diagnosis.",
        "This tool is for auxiliary-diagnosis reference and should be combined with clinical judgment.",
        "📚 In-Depth: Retrograde Ejaculation Detection",
        "The proportion of sperm in post-ejaculation urine.",
        "Retrograde-ejaculation severity grading.",
        "Infertility-cause screening.",
        "Semen 1.0ml×20, urine 30ml×2",
        "ejTotal=20, urTotal=60, total 80\u00d710\u2076; urine proportion=60/80\u00d7100%=75% \u226550% and >5 million \u2192 marked retrograde ejaculation.",
        "No sperm in urine",
        "urConc=0 \u2192 urine proportion 0%, not supporting retrograde ejaculation; investigate other causes.",
        "Marked criterion?",
        "A urine sperm proportion \u226550% and total >5\u00d710\u2076 is read as marked retrograde, often with low ejaculate volume.",
        "Management?",
        "After alkalinizing urine, recover urine sperm for IUI/ICSI, or use medication (sympathomimetic) to improve.",
        'About "Retrograde Ejaculation (Urine Sperm) Detector"',
        "The retrograde-ejaculation detector compares sperm parameters (volume, concentration, total) in ejaculated semen and post-ejaculation urine, combined with urine pH and fructose testing, to aid diagnosis of retrograde ejaculation.",
        "Comparative analysis of semen and urine sperm parameters",
        "Antegrade/retrograde sperm-distribution visualization",
        "WHO-standard semen-volume reference comparison",
        "Diagnostic grading and treatment advice",
        "Retrograde-ejaculation screening in male infertility",
        "Ejaculatory-disorder assessment after diabetes/prostate surgery",
        "Differential diagnosis of reduced semen volume",
        "Pre-assessment before assisted reproduction",
        "How to use the Retrograde Ejaculation (Urine Sperm) Detector",
        "What does the Retrograde Ejaculation (Urine Sperm) Detector do?",
        "Enter the volume, sperm concentration and total of ejaculated semen and post-ejaculation urine separately, and combine with urine pH and fructose testing; the tool compares the two samples to judge whether sperm reflux into the bladder, aiding andrological diagnosis of retrograde ejaculation.",
        "How do I use the Retrograde Ejaculation (Urine Sperm) Detector?",
        "Which scenarios suit the Retrograde Ejaculation (Urine Sperm) Detector?",
    ]))
    write('embryo-grading', build('embryo-grading', [
        "📋 Embryo Gardner Blastocyst Grader",
        "Performs Gardner blastocyst grading by expansion, ICM and TE",
        "Embryo (Gardner Score) Grader",
        "/ Embryo Gardner Grader",
        'View "Embryo Gardner Blastocyst Grader User Guide"',
        "Blastocyst Gardner score = expansion (1\u20136) + inner cell mass ICM (A/B/C) + trophectoderm TE (A/B/C); ICM/TE scored as A=3, B=2, C=1; AA top-quality, sum \u22655 good, sum=4 usable, sum<4 suboptimal; expansion <3 is not fully expanded.",
        "Blastocyst expansion (1-6)",
        "1 Early blastocyst",
        "2 Blastocyst",
        "3 Full blastocyst",
        "4 Expanded blastocyst",
        "5 Hatching blastocyst",
        "6 Fully hatched",
        "Inner cell mass ICM",
        "A many cells, compact",
        "B few/loose cells",
        "C very few",
        "Trophectoderm TE",
        "A many cells, compact epithelium",
        "B few/loose epithelium",
        "📋 Gardner Scoring Standard",
        "Components",
        "Expansion",
        "Blastocoel <1/2 embryo volume",
        "Blastocoel \u22651/2 embryo volume",
        "Full blastocyst, blastocoel filled",
        "Expanded blastocyst, zona pellucida thinned",
        "Hatching in progress",
        "Fully hatched",
        "Many cells, tightly clustered",
        "Few cells, loose",
        "Very few cells",
        "Many cells forming continuous epithelium",
        "Few cells forming discontinuous epithelium",
        "Very few cells",
        "📊 Blastocyst Preference Order",
        "Priority transfer",
        ": 4AA, 5AA, 6AA (ICM/TE both grade A)",
        "Top quality",
        "Usable",
        "Suboptimal",
        ": includes grade C (3CB/3BC and below)",
        "Note: ICM determines the fetus, TE determines the placenta. TE quality strongly affects implantation rate. Blastocysts with expansion \u22653 are suitable for biopsy and freezing. For learning reference only.",
        "📚 In-Depth: Blastocyst Gardner Scoring",
        "Day 5\u20136 blastocyst grading.",
        "ICM and TE quality assessment.",
        "Transfer-priority ranking.",
        "Expansion 4, ICM A, TE A",
        "Code 4AA: ICM and TE both grade A, top-quality blastocyst, priority transfer/freezing.",
        "Expansion 3, ICM B, TE B",
        "3BB: usable embryo, moderate implantation potential, can be a secondary choice.",
        "What do the three parts mean?",
        "Expansion (1\u20136) + inner cell mass (A\u2013C) + trophectoderm (A\u2013C); higher number = more expanded, earlier letter = better.",
        "Which is highest priority?",
        "Blastocysts with expansion \u22654 and ICM/TE of A or B have the highest implantation rate.",
        'About "Embryo (Gardner Score) Grader"',
        "The Embryo (Gardner Score) Grader performs Gardner blastocyst grading by blastocyst expansion (1-6), inner cell mass (ICM A-C) and trophectoderm (TE A-C). A professional medical tool based on authoritative standards, for reference only.",
        "How to use the Embryo Gardner Blastocyst Grader",
        "What does the Embryo Gardner Blastocyst Grader do?",
        "Enter blastocyst expansion (day 1\u20136), inner cell mass ICM and trophectoderm TE grades; the tool gives the blastocyst grade by the Gardner scoring system and compares implantation potential per grade, helping reproductive labs select embryos for transfer.",
        "How do I use the Embryo Gardner Blastocyst Grader?",
        "Which scenarios suit the Embryo Gardner Blastocyst Grader?",
    ]))

if __name__ == "__main__":
    main()
