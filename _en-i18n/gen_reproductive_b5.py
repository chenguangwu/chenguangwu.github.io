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
    write('jingzidnasuipian-dfi-zhishu', build('jingzidnasuipian-dfi-zhishu', [
        "\U0001F4CB Sperm DNA Fragmentation (DFI) Index",
        "Enter DFI and HDS percentages to assess sperm DNA integrity and clinical significance.",
        'View "Sperm DNA Fragmentation (DFI) Index User Guide"',
        "Sperm DNA Fragmentation Index (DFI) and High DNA Stainability (HDS) are graded by percentage: the lower the DFI, the better the DNA integrity; elevated HDS suggests a higher proportion of immature sperm and abnormal spermatogenesis.",
        "\U0001F4A1 DFI reference: <15% excellent, 15-25% fair, 25-50% poor, >50% very poor. HDS (High DNA Stainability) reflects chromatin immaturity and is often interpreted together with DFI.",
        "DFI testing methods include SCD, TUNEL and SCSA; reference ranges vary slightly between methods.",
        "Elevated DFI is associated with risks such as recurrent miscarriage, low fertilization rate and reduced embryo quality.",
        "It is recommended to combine routine semen parameters, age, lifestyle and clinical history for a comprehensive assessment.",
        "\U0001F4DA In-Depth: Sperm DNA Fragmentation Index (DFI/HDS)",
        "Combined DFI and HDS interpretation.",
        "Recurrent miscarriage / fertilization failure assessment.",
        "Antioxidant therapy follow-up.",
        "DFI<30% (some labs prefer <15%) and HDS<15%: both normal, good DNA integrity and chromatin structure.",
        "DFI>=30% indicates elevated fragmentation and increased risk of repeated adverse pregnancy; consider antioxidant and lifestyle intervention before recheck.",
        "DFI vs HDS?",
        "DFI reflects the proportion of DNA breakage fragments; HDS reflects the proportion of immature chromatin (high stainability).",
        "Thresholds?",
        "Commonly DFI<15-30% and HDS<15% are considered normal ranges; higher values are worse.",
        'About "Sperm DNA Fragmentation (DFI) Index"',
        "The Sperm DNA Fragmentation Index (DFI) reflects the degree of sperm DNA damage, and HDS reflects chromatin maturity. Both are commonly used in male infertility, recurrent miscarriage and assisted reproduction prognosis evaluation.",
        "Quick assessment by DFI quartile method",
        "Combined with HDS to indicate chromatin maturity",
        "Provide clinical management suggestions",
        "Andrology / reproductive medicine outpatient report interpretation",
        "Male-factor screening for recurrent miscarriage",
        "Pre-assisted-reproduction evaluation",
        "How to use the Sperm DNA Fragmentation (DFI) Index",
        "What does the Sperm DNA Fragmentation (DFI) Index do?",
        "How do I use the Sperm DNA Fragmentation (DFI) Index?",
        "Which scenarios suit the Sperm DNA Fragmentation (DFI) Index?",
    ]))
    write('liquefaction-time', build('liquefaction-time', [
        "\U0001F4E6 Semen Liquefaction Time Assessor",
        "Assesses semen liquefaction status; normal liquefaction usually completes within 15-30 minutes, and failure to liquefy within 60 minutes is abnormal.",
        "/ Liquefaction Time Assessor",
        'View "Semen Liquefaction Time Assessor User Guide"',
        "Semen liquefaction grading: <=30 min normal, 30-60 min delayed, 60-120 min incomplete, >=120 min non-liquefaction; viscosity is assessed by thread length, <2 cm is normal.",
        "Liquefaction time (minutes)",
        "Appearance status",
        "Homogeneous translucent",
        "Gel-like",
        "Threading / viscous",
        "\U0001F4CB Liquefaction Time Criteria",
        "Liquefaction time",
        "<=30 min",
        "Normal liquefaction",
        "Normal prostatic secretion",
        "31 - 60 min",
        "Delayed liquefaction",
        "Suggests possible prostatic dysfunction",
        ">60 min",
        "Incomplete liquefaction",
        "Abnormal prostatic fluid, infection, etc.",
        "Non-liquefaction",
        "Significantly affects sperm motility and conception",
        "\U0001F52C Liquefaction Mechanism and Management",
        "Mechanism",
        ": Seminal vesicles secrete coagulation proteins to coagulate semen; prostate-secreted PSA liquefies it.",
        "Impact",
        ": Incomplete liquefaction limits sperm movement and affects routine semen analysis and conception.",
        "Management",
        ": Laboratories may use mechanical pipetting, 37\u2103 incubation, bromelain, etc. to assist liquefaction.",
        "Etiology",
        ": Prostatitis, infection, congenital seminal vesicle / prostate abnormalities.",
        "Tip: testing should begin as soon as possible after ejaculation, preferably in a 37\u2103 water bath. Excessive thread length suggests abnormal viscosity and may coexist with incomplete liquefaction.",
        "\U0001F4DA In-Depth: Semen Liquefaction Time",
        "Normal liquefaction determination.",
        "Delayed / non-liquefaction assessment.",
        "Abnormal viscosity indication.",
        "Complete liquefaction in 30 min",
        "WHO reference: complete liquefaction within <=60 min at room temperature; liquefaction at 30 min is normal.",
        ">60 min still gel-like",
        "Failure to liquefy after >60 min or viscous thread >2 cm suggests abnormal liquefaction, which may affect counting and conception.",
        "How long is normal?",
        "Gradual liquefaction 15-30 minutes after ejaculation; reference upper limit is 60 minutes.",
        "Causes of non-liquefaction?",
        "Often related to insufficient prostatic enzymes and inflammation; enzymatic treatment may assist testing.",
        'About "Semen Liquefaction Time Assessor"',
        "The Semen Liquefaction Time Assessor determines normal, delayed or non-liquefaction based on liquefaction time (min), and indicates the related etiology and management suggestions for abnormal liquefaction. A professional medical tool based on authoritative medical standards, for reference only.",
        "How to use the Semen Liquefaction Time Assessor",
        "What does the Semen Liquefaction Time Assessor do?",
        "How do I use the Semen Liquefaction Time Assessor?",
        "Which scenarios suit the Semen Liquefaction Time Assessor?",
        "Reference range",
        "Normal semen after ejaculation at room temperature",
        "<=60 min",
        "achieves complete liquefaction; remaining gel-like beyond 60 minutes is called incomplete (delayed) liquefaction.",
        "Delayed liquefaction limits sperm activity and penetration, and is associated with prostatitis and seminal vesicle dysfunction; long-term incomplete liquefaction may affect natural conception.",
        "Applicability limits",
        "Liquefaction time is affected by collection temperature and container; assessment should combine semen volume, motility and concentration, with comprehensive judgment by andrology / reproductive medicine.",
    ]))

if __name__ == "__main__":
    main()
