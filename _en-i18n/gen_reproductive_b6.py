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
    write('pgt-indication', build('pgt-indication', [
        "\U0001F9EC PGT Genetic Screening Indication Assessor",
        "Assesses indications for PGT-A / PGT-M / PGT-SR based on clinical criteria",
        "PGT (Genetic Screening) Indication Assessor",
        "/ PGT Indication Assessor",
        'View "PGT Genetic Screening Indication Assessor User Guide"',
        "Preimplantation genetic testing (PGT) indications = advanced maternal age (>=38 years) + recurrent spontaneous abortion (>=3 times) + repeated implantation failure + male factor + monogenic disease + chromosomal translocation + previous aneuploid pregnancy + family history; any positive suggests PGT.",
        "Select the applicable conditions (multiple choices allowed)",
        "Advanced maternal age >=38 years",
        "Recurrent miscarriage (>=3 times)",
        "Repeated implantation failure (>=3 high-quality embryos without pregnancy)",
        "Severe male factor (oligoasthenoteratozoospermia)",
        "Known monogenic disease (clear pathogenic gene)",
        "Chromosomal balanced translocation / inversion",
        "Previous aneuploid pregnancy / offspring",
        "Family history of genetic disease",
        "Previous miscarriage count",
        "Assess indications",
        "\U0001F4CB PGT Classification and Indications",
        "Advanced maternal age, repeated implantation failure, recurrent miscarriage, severe male factor",
        "Known monogenic disease (clear pathogenic gene): thalassemia, hemophilia, cystic fibrosis, etc.",
        "Chromosomal structural abnormality: balanced translocation, Robertsonian translocation, inversion",
        "\U0001F52C Key Indication Thresholds",
        "Advanced maternal age",
        ": PGT-A indication threshold commonly referenced at >=38 years",
        "Recurrent spontaneous abortion (RPL)",
        ": >=3 unexplained miscarriages",
        "Repeated implantation failure (RIF)",
        ": >=3 high-quality embryo transfers without clinical pregnancy",
        "Severe male factor",
        ": severe oligoasthenoteratozoospermia, increased aneuploidy risk",
        "Structural abnormality",
        ": one partner with chromosomal balanced translocation / Robertsonian translocation / inversion",
        "Tip: PGT cannot fully replace prenatal diagnosis; chorionic villus sampling / amniocentesis is still recommended after pregnancy. PGT-M requires haplotype construction of the family first. For learning reference only.",
        "\U0001F4DA In-Depth: PGT Indication Screening",
        "PGT-A / PGT-M / PGT-SR indication judgment.",
        "Advanced age / recurrent miscarriage / chromosomal translocation.",
        "Pre-genetic-counseling assessment.",
        "Age 39 + recurrent miscarriage 3 times",
        "Advanced age (>=38) and RPL>=2 times: meets PGT-A indication; recommend embryonic aneuploidy screening.",
        "Balanced translocation carrier",
        "Chromosomal translocation: PGT-SR indication; select normal / balanced embryos to reduce miscarriage.",
        "Three types of PGT?",
        "PGT-A for aneuploidy, PGT-M for monogenic disease, PGT-SR for structural rearrangement; choose by indication.",
        "Is it mandatory?",
        "Only when clear indications exist; genetic counseling and ethics approval are required.",
        'About "PGT (Genetic Screening) Indication Assessor"',
        "The PGT (Genetic Screening) Indication Assessor evaluates indications for PGT-A / PGT-M / PGT-SR based on advanced age, repeated implantation failure, recurrent miscarriage, severe male factor and family history of genetic disease. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the PGT Genetic Screening Indication Assessor",
        "What does the PGT Genetic Screening Indication Assessor do?",
        "Evaluates item by item whether PGT-A, PGT-M or PGT-SR applies, assisting assisted-reproduction genetic screening decisions.",
        "How do I use the PGT Genetic Screening Indication Assessor?",
        "Which scenarios suit the PGT Genetic Screening Indication Assessor?",
    ]))
    write('progressive-motility', build('progressive-motility', [
        "\U0001F4CB Progressive Motility (PR) Percentage Assessor",
        "Calculates PR / NP / IM percentages and total motility (PR+NP), compared with WHO 5th edition lower reference limits PR>=32%, total motility>=40%",
        "/ Progressive Motility Assessor",
        'View "Progressive Motility (PR) Percentage Assessor User Guide"',
        "Sperm motility: progressive motility PR% = PR / (PR + NP + IM) x 100; total motility = PR% + NP%; WHO reference: PR>=32% and total motility>=40% is normal, PR met but total motility low, PR 20-32% asthenozoospermia, PR<20% severe asthenozoospermia.",
        "Progressive motility PR (count)",
        "Non-progressive NP (count)",
        "Immotile IM (count)",
        "\U0001F4CB WHO 5th Edition Motility Lower Reference Limit (5th percentile)",
        "Progressive motility PR",
        "Related to fertilization rate",
        "Total motility PR+NP",
        "Overall activity",
        "\U0001F52C Motility Grading Definitions",
        ": active movement with directionality (straight line or large circles)",
        ": movement but no directionality (in place, small circles, tail swinging)",
        ": no movement",
        "It is recommended to count at least 200 sperm and take the average across multiple high-power fields",
        "Tip: motility is significantly affected by post-ejaculation testing time (recommended within 30-60 minutes) and temperature (37\u2103). A single abnormal result suggests recheck at least twice.",
        "\U0001F4DA In-Depth: Sperm Motility Grading",
        "PR / NP / IM three-level proportion.",
        "Asthenozoospermia determination.",
        "Core indicator of routine semen analysis.",
        "Total 100; PR%=40%, total activity (PR+NP)=50%; PR>=32% normal, good progressive motility.",
        "PR=20%<32%: asthenozoospermia; recommend recheck and etiological investigation.",
        "Meaning of the three levels?",
        "PR progressive, NP non-progressive, IM immotile; WHO references PR>=32%.",
        "What if motility is low?",
        "Investigate varicocele / infection / oxidative stress; consider IUI / ICSI if needed.",
        'About "Progressive Motility (PR) Percentage Assessor"',
        "The Progressive Motility (PR) Percentage Assessor calculates the percentages of progressive (PR), non-progressive (NP) and immotile (IM) sperm and total motility (PR+NP), compared with the WHO 5th edition lower reference limit PR>=32%. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Progressive Motility (PR) Percentage Assessor",
        "What does the Progressive Motility (PR) Percentage Assessor do?",
        "How do I use the Progressive Motility (PR) Percentage Assessor?",
        "Which scenarios suit the Progressive Motility (PR) Percentage Assessor?",
    ]))
    write('reproductive-hormones', build('reproductive-hormones', [
        "\u2697\uFE0F Reproductive Hormones and Spermatogenesis Assessor",
        "Compares male reproductive hormone reference ranges, assesses the hypothalamic-pituitary-gonadal axis and spermatogenic function",
        "Hormones (FSH/LH/E2/T) and Spermatogenesis Assessor",
        "/ Reproductive Hormone Assessor",
        'View "Reproductive Hormones and Spermatogenesis Assessor User Guide"',
        "Male reproductive hormone reference intervals: FSH 1.5-12.4 IU/L, LH 1.7-8.6 IU/L, testosterone T 9.9-27.8 nmol/L, estradiol E2 0-160 pmol/L, prolactin PRL 86-390 mIU/L; compare each item with the interval and mark high / low / normal.",
        "FSH (IU/L) reference 1.5-12.4",
        "LH (IU/L) reference 1.7-8.6",
        "T (nmol/L) reference 9.9-27.8",
        "E2 (pmol/L) reference <160",
        "PRL (mIU/L) reference 86-390",
        "\U0001F4CB Male Reproductive Hormone Pattern Interpretation",
        "Primary testicular failure (hypergonadotropic hypogonadism)",
        "Hypogonadotropic hypogonadism (hypothalamic / pituitary lesion)",
        "Seminiferous tubule damage, impaired spermatogenesis",
        "Leydig cell dysfunction",
        "Gonadal axis roughly normal",
        "\U0001F52C Key Indicator Significance",
        ": a key indicator for assessing spermatogenesis; markedly elevated suggests seminiferous tubule damage and irreversible spermatogenic disorder",
        ": T decreased with LH increased suggests Leydig cell failure; T decreased with LH decreased suggests pituitary origin",
        ": hyperprolactinemia inhibits GnRH, leading to hypogonadism",
        ": increased estrogen inhibits FSH / LH, seen in obesity, liver disease and elevated aromatase activity",
        "Tip: reference ranges vary by laboratory method; please use your local laboratory reference values. Blood collection is recommended fasting in the morning, avoiding strenuous exercise.",
        "\U0001F4DA In-Depth: Reproductive Hormone Profile Interpretation",
        "Combined analysis of FSH / LH / E2 / T / PRL.",
        "Ovarian reserve and ovulation assessment.",
        "Hyperprolactinemia / hyperandrogenism differentiation.",
        "FSH elevated with E2 not low: tendency toward diminished ovarian reserve (DOR); recommend AMH and AFC recheck.",
        "PRL 80, others normal",
        "Markedly elevated prolactin (normal <25): hyperprolactinemia, inhibits ovulation; pituitary MRI is needed.",
        "Basal FSH threshold?",
        "Follicular phase FSH>10 suggests declining reserve, >20 marked decline, >25 very poor response.",
        "LH / FSH ratio?",
        "PCOS often has LH/FSH>=2 with elevated T; combine with ultrasound.",
        'About "Hormones (FSH/LH/E2/T) and Spermatogenesis Assessor"',
        "The Hormones (FSH/LH/E2/T) and Spermatogenesis Assessor evaluates spermatogenic function and gonadal axis status by comparing male reproductive hormones (FSH/LH/E2/T/PRL) against reference ranges. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Reproductive Hormones and Spermatogenesis Assessor",
        "What does the Reproductive Hormones and Spermatogenesis Assessor do?",
        "Enter male FSH, LH, E2, testosterone T, PRL and other reproductive hormone levels; the tool compares against reference ranges to assess hypothalamic-pituitary-gonadal axis function, determine the type of spermatogenic disorder (central or testicular), and assist in male infertility screening.",
        "How do I use the Reproductive Hormones and Spermatogenesis Assessor?",
        "Which scenarios suit the Reproductive Hormones and Spermatogenesis Assessor?",
    ]))

if __name__ == "__main__":
    main()
