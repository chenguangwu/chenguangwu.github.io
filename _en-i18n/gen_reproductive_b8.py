#!/usr/bin/env python3
# gen_reproductive-medicine_head.py — shared head for reproductive-medicine batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'reproductive-medicine')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'reproductive-medicine')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {
    'sperm-concentration': {"稀释倍数 D（1:X）": "Dilution factor D (1:X)"},
}
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
    write('sperm-cryopreservation', build('sperm-cryopreservation', [
        "\U0001F9EC Sperm Cryopreservation Recovery-Rate Estimator",
        "Calculates freeze-thaw recovery rate and motile sperm recovery rate, assessing sperm cryopreservation effect",
        "Frozen Sperm (Recovery Rate) Estimator",
        'View "Sperm Cryopreservation Recovery-Rate Estimator User Guide"',
        "Recovery rate = post-thaw sperm count / pre-freeze sperm count x 100",
        "Recovery rate = post-thaw sperm count / pre-freeze sperm count x 100; motile sperm recovery rate = post-thaw motile sperm / pre-freeze motile sperm",
        "Pre-freeze concentration (x10^6/mL)",
        "Pre-freeze volume (mL)",
        "Pre-freeze motility (%)",
        "Post-thaw concentration (x10^6/mL)",
        "Post-thaw volume (mL)",
        "Post-thaw motility (%)",
        "\U0001F4CB Freeze-Thaw Quality Interpretation",
        "Recovery rate",
        "Cryopreservation protocol effective",
        "Can meet ART needs, protocol may be optimized",
        "Adjust cryoprotectant / cooling program recommended",
        "\U0001F52C Cryopreservation Key Points",
        "Cryoprotectant",
        ": glycerol-egg yolk-citrate buffer (G-Y-C) or commercial sperm cryoprotectant",
        ": programmed cooling or vitrification, liquid nitrogen (-196\u2103) storage",
        "Thawing",
        ": 37\u2103 water bath rapid rewarming, centrifuge to remove cryoprotectant",
        "During storage, about 30-50% of motile sperm are lost; for severe oligoasthenozoospermia, aliquot into multiple straws",
        "Tip: motile sperm recovery rate reflects cryopreservation quality better than survival rate alone. Sample volume, cryoprotectant ratio and cooling rate all affect recovery rate. For learning reference only.",
        "\U0001F4DA In-Depth: Sperm Cryopreservation Recovery Rate",
        "Total count comparison before and after freeze-thaw.",
        "Motile sperm recovery rate.",
        "Fertility preservation assessment.",
        "Pre-freeze 60x3mL/50%, post-thaw 45x3mL/40%",
        "Pre-freeze total 180, motile 90x10^6; post-thaw total 135, motile 54x10^6; recovery rate 75%, motile recovery 60%, good.",
        "Motile recovery low",
        "Motile recovery <50% suggests large cryodamage; optimize program or aliquot.",
        "How to calculate recovery rate?",
        "Recovery rate = post-thaw total / pre-freeze total; motile recovery = post-thaw motile / pre-freeze motile x 100%.",
        "Normal level?",
        "Motile recovery is often 40-70%, affected by method and cryoprotectant.",
        'About "Frozen Sperm (Recovery Rate) Estimator"',
        "The Frozen Sperm (Recovery Rate) Estimator calculates recovery rate and survival rate from pre-freeze and post-thaw motile sperm counts, assessing cryopreservation effect. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('sperm-dfi', build('sperm-dfi', [
        "\U0001F9EC Sperm DNA Fragmentation (DFI) Index Assessor",
        "Assesses sperm DNA integrity, commonly by SCSA / SCD, thresholds DFI 15% / 25%",
        "Sperm DNA Fragmentation (DFI) Index Assessor",
        "/ Sperm DFI Assessor",
        'View "Sperm DNA Fragmentation (DFI) Index Assessor User Guide"',
        "Sperm DNA Fragmentation Index (DFI) grading: <15% excellent, 15-25% good / borderline, 25-50% abnormal, >50% markedly abnormal; HDS >15% suggests increased immature sperm, spermatogenic abnormality or oxidative stress.",
        "HDS high stainability (%)",
        "\U0001F4CB DFI Evaluation Grading (SCSA method)",
        "Good DNA integrity, normal fertility",
        "Good / borderline",
        "May have impact, recheck recommended",
        "Natural conception rate declines, ART affected",
        "Markedly abnormal",
        "ICSI or sperm selection recommended",
        "\U0001F52C Testing Method and Significance",
        ": flow cytometry acridine orange staining, distinguishing double-strand / single-strand DNA",
        ": high-stainability sperm %, >15% suggests increased immature sperm",
        "Etiology",
        ": varicocele, infection, oxidative stress, smoking, high temperature",
        "Improvement",
        ": antioxidant (vitamin C/E, coenzyme Q10), lifestyle intervention, recheck after 2-3 months",
        "Tip: elevated DFI is associated with recurrent miscarriage, decreased IVF fertilization rate and poor embryo quality. Results need comprehensive judgment with routine semen analysis and clinical findings.",
        "\U0001F4DA In-Depth: Sperm DNA Fragmentation (DFI)",
        "Single-indicator DFI interpretation.",
        "Infertility / miscarriage risk stratification.",
        "Treatment follow-up monitoring.",
        "DFI<30% (stricter labs <15% optimal) is normal, DNA integrity acceptable.",
        "DFI>=30-40% elevated, associated with fertilization failure and recurrent miscarriage; antioxidant + recheck recommended.",
        "DFI vs motility?",
        "The two are not completely correlated; high DNA damage may coexist with normal motility, requiring specific testing.",
        "Can it improve?",
        "Quit smoking and alcohol, antioxidant (vitamin C/E, coenzyme Q10), control heat and infection can lower DFI.",
        'About "Sperm DNA Fragmentation (DFI) Index Assessor"',
        "The Sperm DNA Fragmentation (DFI) Index Assessor evaluates sperm DNA integrity by DFI%, interprets fertility impact against thresholds 15% / 25%, and indicates high HDS stainability. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Sperm DNA Fragmentation (DFI) Index Assessor",
        "What does the Sperm DNA Fragmentation (DFI) Index Assessor do?",
        "How do I use the Sperm DNA Fragmentation (DFI) Index Assessor?",
        "Which scenarios suit the Sperm DNA Fragmentation (DFI) Index Assessor?",
        "Grading reference",
        "Sperm DNA Fragmentation Index (DFI):",
        "usually considered normal;",
        "borderline / elevated;",
        "high fragmentation, associated with decreased natural pregnancy rate and increased miscarriage risk.",
        "DFI reflects the integrity of sperm genetic material and is more meaningful for those with recurrent miscarriage and assisted-reproduction failure; lifestyle (smoking, high temperature, oxidative stress) can elevate DFI.",
        "Applicability limits",
        "DFI is a specialized test; thresholds vary slightly between kits; interpretation requires combining routine semen analysis, with comprehensive assessment by reproductive medicine.",
    ]))
    write('sperm-morphology', build('sperm-morphology', [
        "\U0001F3CB\uFE0F Sperm Morphology Classifier (Strict Criteria)",
        "WHO strict morphology criteria, lower reference limit 4%.",
        "Sperm Morphology (Normal / Abnormal) Classifier",
        "/ Sperm Morphology Classifier",
        'View "Sperm Morphology Classifier (Strict Criteria) User Guide"',
        "Normal morphology (%) = normal morphology count / total counted x 100",
        "Calculates the percentage of normal morphology sperm, compared with the WHO 5th edition strict criteria lower reference limit 4%",
        "Formula: normal morphology % = normal morphology count / total counted x 100",
        "Normal morphology sperm (count)",
        "Total counted sperm (count)",
        "\U0001F4CB WHO 5th Edition Normal Morphology Lower Reference Limit",
        "Normal morphology %",
        "Recheck recommended and combine with other indicators",
        "Teratozoospermia",
        "IVF fertilization rate may decline",
        "Severe teratozoospermia",
        "ICSI assessment recommended",
        "\U0001F52C Strict Criteria Morphology Determination (head / neck / tail)",
        "Head",
        ": oval, acrosome covers 40-70% of head, vacuoles <20%, length 4.0-5.0 um, width 2.5-3.5 um",
        "Neck / midpiece",
        ": regular without angulation, residual cytoplasm not exceeding 1/3 of head",
        "Tail",
        ": single, uncoiled, length about 45 um",
        "Any defect in any region is judged abnormal; count >=200 sperm recommended",
        "Tip: modified Papanicolaou or Shorr staining is recommended for morphology assessment. Standards vary greatly between laboratories; a fixed protocol and local reference range are recommended.",
        "\U0001F4DA In-Depth: Sperm Normal Morphology Rate",
        "Strict-criteria morphology counting.",
        "Teratozoospermia determination.",
        "IVF / ICSI decision reference.",
        "Normal 8 / total 200",
        "Normal rate = 8/200 x 100% = 4%, meets WHO strict criteria >=4% borderline normal.",
        "Normal 2 / 200",
        "Normal rate = 1% < 4%: teratozoospermia, natural pregnancy declines, ICSI can bypass morphology issues.",
        "Strict criteria?",
        "WHO 5th / 6th edition strict criteria normal morphology >=4% as lower reference limit (Tygerberg method).",
        "Must ICSI for poor morphology?",
        "Not mandatory; ICSI is favored only when combined with oligoasthenozoospermia or repeated failure.",
        'About "Sperm Morphology (Normal / Abnormal) Classifier"',
        "The Sperm Morphology (Normal / Abnormal) Classifier calculates the normal morphology percentage from normal morphology count and total counted sperm, interpreted against the WHO 5th edition strict criteria lower reference limit 4%. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Sperm Morphology Classifier (Strict Criteria)",
        "What does the Sperm Morphology Classifier (Strict Criteria) do?",
        "Sperm Morphology Classifier (Strict Criteria): compared with the WHO 5th edition strict morphology criteria, enter the normal morphology and total counted sperm to calculate the normal morphology percentage and interpret fertility risk against the 4% lower reference limit.",
        "How do I use the Sperm Morphology Classifier (Strict Criteria)?",
        "Which scenarios suit the Sperm Morphology Classifier (Strict Criteria)?",
        "Strict criteria",
        "By Tygerberg strict criteria, the normal morphology sperm lower reference limit is",
        "; below 4% is teratozoospermia (high abnormality rate), which may affect fertilization capacity.",
        "Strict criteria are much stricter than older versions (e.g. WHO 4th edition 15%); standards between laboratories are not directly comparable; mild morphological abnormality is common in the population.",
        "Applicability limits",
        "Morphology is one item of semen analysis, requiring combination with concentration and motility; a single abnormal result need not be over-worried; recheck and specialist consultation are recommended.",
    ]))

if __name__ == "__main__":
    main()
