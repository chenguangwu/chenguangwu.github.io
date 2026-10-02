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
    write('testicular-biopsy', build('testicular-biopsy', [
        "\U0001F9EC Testicular Biopsy Spermatogenic Cell Scoring Tool",
        "Johnsen score (1-10) / modified Silber grade, assessing spermatogenic function and sperm retrieval prognosis",
        "Testicular Biopsy (Spermatogenic Cell) Scoring Tool",
        "/ Testicular Biopsy Scoring Tool",
        'View "Testicular Biopsy Spermatogenic Cell Scoring Tool User Guide"',
        "Mean Johnsen score = sum(score x number of tubules at that score) / total tubules, score 1-10; >=9 normal, >=8 mild impairment, >=7 moderate impairment, <7 severe impairment; modified Silber grade 3-9 (including spermatogenic arrest / Sertoli-cell-only SCO / tubular sclerosis).",
        "Johnsen score",
        "Silber grade",
        "Score each seminiferous tubule cross-section (1-10) to obtain the mean Johnsen score",
        "Number of tubules scored 10",
        "Number of tubules scored 9",
        "Number of tubules scored 8",
        "Number of tubules scored 7",
        "Number of tubules scored 6",
        "Number of tubules scored 5",
        "Number of tubules scored 4",
        "Number of tubules scored 3",
        "Number of tubules scored 2",
        "Number of tubules scored 1",
        "Select the histologic appearance that best fits",
        "Complete spermatogenesis (all germ cell stages + sperm)",
        "Active spermatogenesis, abundant sperm",
        "Active spermatogenesis, fewer sperm",
        "Late spermatogenic arrest (secondary spermatocytes / spermatids)",
        "Early spermatogenic arrest (primary spermatocytes)",
        "Sertoli-cell-only (SCO)",
        "Seminiferous tubule sclerosis / hyalinization",
        "\U0001F4CB Johnsen Scoring Criteria",
        "Histologic appearance",
        "Normal spermatogenic function, abundant sperm",
        "Mild spermatogenic change, more sperm",
        "Few sperm, reduced late spermatids",
        "Azoospermia, many late spermatids",
        "Azoospermia, secondary spermatocytes",
        "Azoospermia, primary spermatocytes",
        "Spermatogonia only",
        "Sertoli cells only",
        "Acellular, thickened basement membrane",
        "Complete tubular hyalinization",
        "\U0001F4CA Johnsen Mean-Score Clinical Significance",
        "Spermatogenic function",
        "Sperm retrieval prognosis",
        "High sperm retrieval success rate",
        "Mild impairment",
        "Moderate sperm retrieval success rate",
        "Low sperm retrieval success rate",
        "Tip: biopsy is a focal assessment and cannot fully represent the entire testicular state. For NOA patients, multi-region sampling (mTESE) can improve sperm retrieval rate. For learning reference only.",
        "\U0001F4DA In-Depth: Testicular Biopsy Grading",
        "Johnsen / Silber grading.",
        "Qualitative spermatogenic status.",
        "Sperm retrieval method guidance.",
        "10 tubules scored, mean 7",
        "Mean 7: reduced spermatogenesis but sperm present, micro-TESE can be attempted.",
        "Mean 2",
        "Sertoli-cell-only / spermatogonia, severe spermatogenic disorder, low retrieval success, requires full informed consent.",
        "Johnsen vs Silber?",
        "Both are 1-10 systems; Silber is simpler; this tool supports both and gives grading descriptions.",
        "Sperm retrieval after biopsy?",
        "Non-obstructive azoospermia relies on micro-TESE to find focal spermatogenesis; higher score means higher success.",
        'About "Testicular Biopsy (Spermatogenic Cell) Scoring Tool"',
        "The Testicular Biopsy (Spermatogenic Cell) Scoring Tool supports the Johnsen score (1-10) and modified Silber grade, assessing seminiferous tubule spermatogenic function and sperm retrieval prognosis. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Testicular Biopsy Spermatogenic Cell Scoring Tool",
        "What does the Testicular Biopsy Spermatogenic Cell Scoring Tool do?",
        "How do I use the Testicular Biopsy Spermatogenic Cell Scoring Tool?",
        "Which scenarios suit the Testicular Biopsy Spermatogenic Cell Scoring Tool?",
    ]))
    write('testicular-volume', build('testicular-volume', [
        "\U0001F9CA Testicular Volume Measurer",
        "Ellipsoid approximation (Lambert formula), result in mL.",
        "Testicular Volume (Prader) Measurer",
        'View "Testicular Volume Measurer User Guide"',
        "Volume (mL) = length x width x height x 0.71 / 1000 (unit mm)",
        "Prader orchidometer comparison / ellipsoid formula method, adult reference 15-25 mL",
        "Prader comparison method",
        "Ellipsoid formula method",
        "Compare the testis with the Prader orchidometer (ellipsoid models) and select the closest volume",
        "Left testis (mL)",
        "Right testis (mL)",
        "Ellipsoid formula: volume (mL) = length x width x height x 0.71 / 1000 (unit mm, result mL)",
        "Left length L (mm)",
        "Left width W (mm)",
        "Left height H (mm)",
        "Right length L (mm)",
        "Right width W (mm)",
        "Right height H (mm)",
        "\U0001F4CB Testicular Volume Reference Values",
        "Unilateral volume (mL)",
        "Adult normal",
        "Suggests normal spermatogenic function",
        "Prepubertal",
        "Before pubertal development",
        "Small testis",
        "Suggests hypogonadism / dysplasia",
        "Atrophy",
        "Marked atrophy, impaired spermatogenic function",
        "Large testis",
        "Rule out tumor / hydrocele",
        "\U0001F52C Clinical Significance",
        "Testicular volume is positively correlated with spermatogenic function; total sperm count relates to testicular volume",
        "Small testis + elevated FSH suggests primary testicular failure",
        "Note to exclude hydrocele and epididymal cyst causing apparent volume increase",
        "Difference between sides >2 mL requires further examination",
        "Tip: the Prader orchidometer is a simple clinical estimate; ultrasound measurement is more accurate. Results are for reference only, requiring comprehensive clinical judgment.",
        "\U0001F4DA In-Depth: Testicular Volume Calculation",
        "Ellipsoid volume",
        "Formula estimation.",
        "Left-right asymmetry assessment.",
        "Puberty / atrophy monitoring.",
        "Left 40x30x20mm, right 38x28x19mm",
        "Left=(4x3x2x0.71)=17.0mL, right=(3.8x2.8x1.9x0.71)=14.3mL, both normal (15-25mL); difference 2.7mL slightly exceeds 2mL, follow up.",
        "Unilateral 8mL",
        "Volume <12-15 mL suggests dysplasia / atrophy, with decreased spermatogenesis.",
        "Formula?",
        "Volume=(length x width x height x 0.71)/1000 (length/width/height in mm, result mL); 0.71 is the ellipsoid coefficient.",
        "How large is normal?",
        "Adult unilateral about 15-25 mL; difference >2 mL or unilateral small requires investigation.",
        'About "Testicular Volume (Prader) Measurer"',
        "The Testicular Volume (Prader) Measurer supports the Prader orchidometer comparison method and ellipsoid formula method (L x W x H x 0.71) to calculate testicular volume, compared with the adult reference 15-25 mL. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Testicular Volume Measurer",
        "What does the Testicular Volume Measurer do?",
        "Supports two algorithms: directly enter the volume from Prader orchidometer comparison, or use length, width and height with the ellipsoid formula; outputs left and right testicular volumes separately, adult reference range about 15-25 mL, results for self-check reference only.",
        "How do I use the Testicular Volume Measurer?",
        "Which scenarios suit the Testicular Volume Measurer?",
    ]))

if __name__ == "__main__":
    main()
