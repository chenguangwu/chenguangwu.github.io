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
    write('icsi-success', build('icsi-success', [
        "\u26A1 ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator",
        "Evaluates ICSI lab efficiency and clinical pregnancy expectation combined with female factors",
        "ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator",
        "/ ICSI Success-Rate Evaluator",
        'View "ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator User Guide"',
        "ICSI lab indicators: survival rate = surviving oocytes \u00f7 injected oocytes; fertilization rate = fertilized oocytes \u00f7 injected oocytes; top-quality embryo rate = top-quality embryos \u00f7 fertilized oocytes; then compare with the expected live-birth-rate range by female age.",
        "Laboratory data",
        "ICSI injected count",
        "Post-injection surviving count",
        "Fertilized (2PN) count",
        "Female factors",
        "\U0001F4CB ICSI Efficiency Indicator Reference",
        "Oocyte survival rate",
        "Surviving / injected",
        "ICSI fertilization rate",
        "2PN / injected",
        "Top-quality / 2PN",
        "\U0001F4CA Expected Clinical Pregnancy Rate by Female Age",
        "Expected clinical pregnancy rate (per transfer cycle)",
        "Note: ICSI is suitable for severe oligoasthenoteratozoospermia, fertilization disorder and PGT cycles. The expected pregnancy rate is a population statistic with large individual variation. For learning reference only.",
        "\U0001F4DA In-Depth: ICSI Live-Birth Rate Estimation",
        "Estimate expected live birth by female age.",
        "Fertilization/survival/top-quality rate calculation.",
        "Reference for protocol communication.",
        "Age 35\u201337, MII 10/injected 8/surviving 7/fertilized 6/top-quality 4",
        "Survival rate 7/8=87.5%, fertilization rate 6/8=75%, top-quality rate 4/6=66.7%; expected live birth at this age 35\u201350%.",
        "Age >42",
        "Expected live birth drops to 5\u201315%; recommend full informed consent and consider donor oocytes.",
        "Age cut-offs?",
        "Commonly: <30:50\u201365%, 30\u201334:45\u201360%, 35\u201337:35\u201350%, 38\u201340:25\u201340%, 41\u201342:15\u201325%, >42:5\u201315%.",
        "For reference only?",
        "These are statistical ranges; actual results are affected by ovarian reserve, embryo quality and other factors.",
        'About "ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator"',
        "The ICSI Success-Rate Evaluator estimates ICSI fertilization rate and pregnancy expectation from MII oocyte count, injected count, surviving count, fertilized count, top-quality embryo count and female factors. A professional medical tool based on authoritative standards, for reference only.",
        "How to use the ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator",
        "What does the ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator do?",
        "Enter lab indicators such as retrieved oocytes, mature oocytes and normal fertilization count, combined with female age and other factors; the tool assesses ICSI fertilization efficiency and clinical pregnancy expectation, helping reproductive centers with cycle counseling and quality control.",
        "How do I use the ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator?",
        "Which scenarios suit the ICSI (Intracytoplasmic Sperm Injection) Success-Rate Evaluator?",
    ]))
    write('ivf-statistics', build('ivf-statistics', [
        "\U0001F9EC IVF Fertilization / Implantation Rate Calculator",
        "Computes key efficiency indicators of the IVF cycle and assesses lab and clinical outcomes",
        "IVF (Fertilization/Implantation Rate) Calculator",
        "/ IVF Calculator",
        'View "IVF Fertilization / Implantation Rate Calculator User Guide"',
        "Fertilization rate = fertilized / retrieved \u00d7 100%",
        "Normal fertilization rate = fertilized / MII oocytes \u00d7 100%",
        "Cleavage rate = cleaved / fertilized \u00d7 100%",
        "Top-quality embryo rate = top-quality embryos / fertilized \u00d7 100%",
        "Implantation rate = gestational sacs / transferred \u00d7 100%",
        "Laboratory phase",
        "Retrieved oocytes",
        "Fertilized (2PN)",
        "Cleaved embryos",
        "Transferable / frozen embryos",
        "Clinical outcome",
        "Implanted gestational sacs",
        "Clinical pregnancy (0/1)",
        "\U0001F4CB IVF Key Efficiency Indicator Reference",
        "Reference range",
        "Fertilization rate",
        "2PN count / retrieved",
        "Normal fertilization rate",
        "Cleavage rate",
        "Cleaved / 2PN",
        "Top-quality embryos / 2PN",
        "Usable embryo rate",
        "Transferable + frozen / 2PN",
        "Implantation rate",
        "Gestational sacs / transferred embryos",
        "Clinical pregnancy rate",
        "Clinical pregnancy cycles / transfer cycles",
        "Note: fertilization rate is affected by sperm quality, oocyte maturity and culture system; implantation rate relates to embryo quality, endometrial receptivity and transfer strategy. For reference only.",
        "\U0001F4DA In-Depth: IVF Laboratory Indicator Statistics",
        "Fertilization/cleavage/top-quality/implantation rate calculation.",
        "Cycle-quality assessment.",
        "Basis for quality control and improvement.",
        "Oocytes 12/MII 10/fertilized 8/cleaved 8/top-quality 5/usable 5/transferred 2/blastocyst 1",
        "Fertilization 8/12=66.7%, normal fertilization 8/10=80%, cleavage 100%, top-quality 5/8=62.5%, implantation 1/2=50%; lab phase meets standards.",
        "Low fertilization rate",
        "Fertilization rate <60% suggests a fertilization disorder; switch to ICSI or assess semen.",
        "Denominators of each rate?",
        "Denominators of fertilization/cleavage/top-quality rates are fertilized-oocyte count; normal fertilization rate uses MII count; implantation rate uses transferred count.",
        "Pass threshold?",
        "Fertilization rate \u226560% and implantation rate \u226530% are often used as QC references.",
        'About "IVF (Fertilization/Implantation Rate) Calculator"',
        "The IVF Fertilization/Implantation Rate Calculator computes fertilization rate, cleavage rate, top-quality embryo rate and implantation rate from retrieved oocytes, fertilized count, cleaved count, transferable embryos, transferred count and clinical pregnancies. A professional medical tool based on authoritative standards, for reference only.",
        "How to use the IVF Fertilization / Implantation Rate Calculator",
        "What does the IVF Fertilization / Implantation Rate Calculator do?",
        "Enter retrieved oocytes, fertilized count, cleaved count, transferable embryos, transferred count and clinical pregnancies; the tool computes fertilization, cleavage, top-quality embryo, implantation and pregnancy rates item by item, for IVF cycle-outcome statistics and lab QC.",
        "How do I use the IVF Fertilization / Implantation Rate Calculator?",
        "Which scenarios suit the IVF Fertilization / Implantation Rate Calculator?",
    ]))

if __name__ == "__main__":
    main()
