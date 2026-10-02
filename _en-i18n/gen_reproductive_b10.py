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
    write('total-sperm-count', build('total-sperm-count', [
        "\U0001F9CA Total Sperm Count Calculator",
        "Total sperm count = sperm concentration x semen volume, compared with WHO 5th edition lower reference limit 39x10^6/ejaculate",
        "Total Sperm Count (Concentration x Volume) Calculator",
        'View "Total Sperm Count Calculator User Guide"',
        "Total sperm count = sperm concentration (million/mL) x semen volume (mL); WHO reference: >=39 million normal, 15-39 low, 5-15 oligozoospermia, <5 million severe reduction.",
        "Formula: total sperm count (x10^6) = concentration (x10^6/mL) x semen volume (mL)",
        "Sperm concentration (x10^6/mL)",
        "\U0001F4CB WHO 5th Edition Total Sperm Count Lower Reference Limit",
        "Total sperm count (x10^6/ejaculate)",
        "Requires combined assessment with concentration and motility",
        "Recheck and etiological examination recommended",
        "Severe reduction",
        "Assisted reproduction evaluation recommended",
        "\U0001F4CA Factors Affecting Total Sperm Count",
        "Abstinence time",
        ": WHO recommends 2-7 days abstinence; too long or too short affects results",
        "Semen volume",
        ": lower reference limit 1.5 mL; too low requires ruling out retrograde ejaculation / incomplete collection",
        "Sampling completeness",
        ": the first fraction has the highest sperm density; loss significantly underestimates",
        "Tip: total sperm count is an important indicator of male fertility and should be comprehensively judged with concentration, motility and morphology. A single abnormal result suggests recheck at least twice at 1-2 week intervals.",
        "\U0001F4DA In-Depth: Total Sperm Count",
        "Concentration x volume total.",
        "Oligozoospermia quantification.",
        "Fertility screening.",
        "Concentration 40x10^6/mL, volume 3.0mL",
        "Total=40x3.0=120x10^6, far above the WHO >=39x10^6 lower limit, normal.",
        "Concentration 12, volume 1.5",
        "Total=18x10^6<39: oligozoospermia; recheck and evaluation recommended.",
        "WHO lower limit?",
        "Total >=39x10^6 is the lower reference limit (concentration x volume).",
        "Relation to concentration?",
        "Total is affected by both concentration and volume; low volume also lowers the total.",
        'About "Total Sperm Count (Concentration x Volume) Calculator"',
        "The Total Sperm Count (Concentration x Volume) Calculator computes total sperm count per ejaculate from sperm concentration and semen volume, interpreted against the WHO 5th edition lower reference limit 39x10^6. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Total Sperm Count Calculator",
        "What does the Total Sperm Count Calculator do?",
        "Compute total sperm count from sperm concentration and semen volume, indicating whether it is low against the reference value, for self-check of semen analysis; pure front-end calculation, not a diagnosis.",
        "How do I use the Total Sperm Count Calculator?",
        "Which scenarios suit the Total Sperm Count Calculator?",
        "Total sperm count = semen volume x sperm concentration; WHO 5th edition lower reference limit is",
        ">=39x10^6 (39 million)",
        ". Below this (oligozoospermia) the overall fertility potential declines.",
        "Total sperm count integrates volume and concentration, more comprehensive than a single concentration; short abstinence temporarily lowers concentration and total.",
        "Applicability limits",
        "Fertility is affected by multiple factors; this value is a screening reference; for abnormalities, recheck after standard abstinence and consult andrology / reproductive medicine.",
    ]))
    write('vasography', build('vasography', [
        "\U0001F4CB Vasography Patency Assessor",
        "Assesses vas deferens patency and obstruction site based on contrast medium visualization",
        "Vasography (Patency) Assessor",
        "/ Vasography Assessor",
        'View "Vasography Patency Assessor User Guide"',
        "Vasography patency: judged by whether the vas deferens, ampulla, seminal vesicle and ejaculatory duct are visualized; all four segments visualized means patent; ejaculatory duct not visualized or seminal vesicle visualized while ejaculatory duct obstructed suggests ejaculatory duct obstruction.",
        "Contrast findings",
        "Vas deferens visualized patent",
        "Ampulla visualized",
        "Seminal vesicle visualized",
        "Ejaculatory duct visualized",
        "Obstruction site",
        "Proximal vas deferens (epididymis-vas deferens junction)",
        "Mid vas deferens",
        "Ampulla",
        "Ejaculatory duct",
        "Bilateral obstruction",
        "Seminal vesicle dilation",
        "Mild dilation",
        "Marked dilation",
        "\U0001F4CB Clinical Significance of Obstruction Site",
        "Epididymis-vas deferens junction",
        "Often congenital or infectious; microsurgical anastomosis possible",
        "Mostly iatrogenic injury; end-to-end anastomosis possible",
        "Transurethral resection of ejaculatory duct (TURED) possible",
        "Bilateral absence",
        "Congenital bilateral absence of vas deferens (CBAVD), check CFTR gene",
        "\U0001F52C Assessment Points",
        "Ejaculatory duct obstruction",
        ": seminal vesicle dilation + ejaculatory duct not visualized + low semen volume / low pH / low fructose",
        "Contrast reflux",
        ": visible reflux into bladder, suggesting partial obstruction",
        "Combine seminal plasma biochemistry",
        ": fructose (seminal vesicle), neutral alpha-glucosidase (epididymis) aid localization",
        "Vasography is an invasive examination, usually performed during sperm retrieval / recanalization surgery",
        "Tip: vasography results need comprehensive judgment with routine semen analysis, seminal plasma biochemistry and scrotal color Doppler. For learning reference only.",
        "\U0001F4DA In-Depth: Seminal Tract Angiography Obstruction Localization",
        "Vas deferens / seminal vesicle / ejaculatory duct patency determination.",
        "Obstruction site localization.",
        "Surgical indications such as TURED.",
        "Entire tract patent",
        "Vas deferens, seminal vesicle and ejaculatory duct all checked patent, site none: seminal tract patent, does not support obstructive azoospermia.",
        "Site = ejaculatory duct, seminal vesicle markedly dilated",
        "Ejaculatory duct obstruction + seminal vesicle dilation: TURED (transurethral ejaculatory duct resection) evaluation recommended.",
        "Common obstruction points?",
        "Inguinal segment, pelvic segment, ejaculatory duct; ejaculatory duct obstruction often accompanies seminal vesicle dilation and low semen volume.",
        "Next step?",
        "After clear localization, perform microsurgical / endoscopic reconstruction or direct sperm retrieval + ICSI.",
        'About "Vasography (Patency) Assessor"',
        "The Vasography (Patency) Assessor evaluates vas deferens patency and obstruction site based on contrast visualization in the vas deferens, seminal vesicle and ejaculatory duct. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Vasography Patency Assessor",
        "What does the Vasography Patency Assessor do?",
        "Based on contrast visualization in the vas deferens, seminal vesicle and ejaculatory duct in vasography, the tool assesses duct patency and indicates possible obstruction sites (testicular end / inguinal / pelvic), assisting in the diagnosis of male obstructive azoospermia.",
        "How do I use the Vasography Patency Assessor?",
        "Which scenarios suit the Vasography Patency Assessor?",
    ]))

if __name__ == "__main__":
    main()
