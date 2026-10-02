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
    write('semen-stain-confirmation', build('semen-stain-confirmation', [
        "\U0001F3CB\ufe0f Semen Stain (PSA/p30) Confirmation Test Tool",
        "Semen stain examination workflow: screening test \u2192 confirmatory test \u2192 sperm microscopy, with step selection and result interpretation",
        "/ Semen Stain Confirmation Test Tool",
        "\U0001F4D6 Read the \"Guide to Using the Semen Stain (PSA/p30) Confirmatory Test\"",
        "Step 1: Screening Test",
        "Acid Phosphatase Test (disodium phenyl phosphate method)",
        "Ultraviolet Irradiation Test",
        "Potassium Iodide Iodine Crystal Test",
        "Step 2: Confirmatory Test",
        "PSA (Prostate-Specific Antigen) Detection",
        "p30 Protein Colloidal Gold Strip",
        "Semen Vesicle Protein Detection",
        "Direct Microscopic Search for Sperm",
        "Sperm Microscopy Parameters (optional)",
        "Sperm Detection",
        "No sperm detected",
        "Few sperm (1 to 5 per slide)",
        "Moderate amount of sperm",
        "Only sperm heads seen",
        "Sperm Motility",
        "No motility (dead)",
        "Motile sperm present",
        "Semen Stain Examination Method Reference",
        "Screening Tests",
        "Acid phosphatase test",
        ": ACP activity is extremely high in semen, turning purple or red when positive. Sensitivity is high, but prostatic fluid and vaginal secretions can also be weakly positive.",
        "Ultraviolet irradiation",
        ": the stain fluoresces silvery white under a UV lamp; used for locating, not specific.",
        "Potassium iodide iodine crystals",
        ": choline in the stain reacts with iodine to form brown crystals, with poor specificity.",
        "Confirmatory Tests",
        "PSA detection",
        ": prostate-specific antigen, specifically expressed in human semen. ELISA or colloidal gold methods give high sensitivity and good specificity.",
        "p30 colloidal gold strip",
        ": fast, simple and operable at the scene, with high sensitivity and specificity. p30 is PSA.",
        "Semen vesicle protein",
        ": a semen-specific protein detected by ELISA.",
        "Sperm Microscopy",
        "Direct evidence",
        "Smear staining microscopy",
        ": HE staining or Papanicolaou staining shows sperm with a darkly stained head and a lightly stained tail. Detecting sperm is the most direct evidence of a semen stain.",
        "Note on azoospermia",
        ": vasectomy or azoospermia means no sperm in the stain, so confirmation relies on PSA/p30.",
        "Motile sperm indicate a short interval since ejaculation (within hours), which is valuable for forensic timing.",
        "Forensic Meaning of Semen Stain Examination",
        "Semen stain examination is key physical evidence in sexual assault cases",
        "After confirming a semen stain, DNA should be extracted for individual identification (STR profiling)",
        "Mixed stains (semen mixed with vaginal secretions) require separation and extraction",
        "Both sperm DNA and seminal plasma DNA in the stain can be used for profiling",
        "\U0001F4DA In-Depth Analysis: Semen Stain (PSA/p30) Confirmatory Testing",
        "Identification of Semen Stains in Sexual Assault Cases",
        "Stepwise Interpretation of Screening and Confirmatory Tests",
        "Reliability of Sperm-free Specimens",
        "Confirm stepwise with the screening test (acid phosphatase, high sensitivity) \u2192 the confirmatory test (PSA/p30, a human semen specific protein) \u2192 sperm microscopy (HE or differential staining to find sperm). A positive PSA supports human semen, and the sperm-free type (after vasectomy or with infertility) still holds.",
        "A strongly acid-phosphatase-positive stain \u2192 PSA/p30 immunochromatography positive \u2192 sperm found by differential staining \u2192 identified as a semen stain. If PSA is positive but microscopy finds no sperm (as in a vasectomised person), PSA-specific protein still supports human semen, so the conclusion is reliable.",
        "Does a positive acid phosphatase mean it is a semen stain?",
        "No. Prostatic fluid, vaginal secretions and plant peroxidases can also be positive, so PSA/p30 specific confirmation is required to avoid false positive misjudgements.",
        "If no sperm is found, does that mean it is not a semen stain?",
        "No. Vasectomy, infertility and low ejaculate volume often mean no sperm is present. A positive PSA/p30 specific protein is enough to identify human semen, and a negative microscopy does not invalidate the conclusion.",
        "About \"Semen Stain Confirmation Test Tool\"",
        "A forensic evidence aid covering the whole semen stain examination workflow, including step selection and result interpretation for screening, confirmatory (PSA/p30) and sperm microscopy steps.",
        "Three-step examination workflow guidance",
        "Supports PSA/p30 confirmatory testing",
        "Sperm detection and motility analysis",
        "Automatic combined conclusion interpretation",
        "Reference for physical evidence examination in sexual assault cases",
        "Aid to writing semen stain examination reports",
        "About \"Semen Stain (PSA/p30) Confirmation Test Tool\"",
        "Semen Stain (PSA/p30) Confirmation Test Tool - a forensic evidence tool supporting the steps and interpretation of semen stain screening tests, confirmatory tests (acid phosphatase / PSA/p30) and sperm detection. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()