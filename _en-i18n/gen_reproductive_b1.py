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
    write('anti-sperm-antibody', build('anti-sperm-antibody', [
        "🧬 Anti-Sperm Antibody (MAR) Result Interpreter",
        "Interprets the mixed antiglobulin reaction (MAR) test by the percentage of sperm bound to beads, with the WHO reference threshold at 50%.",
        "Anti-Sperm Antibody (MAR) Result Interpreter",
        "/ Anti-Sperm Antibody (MAR) Result Interpreter",
        'View "Anti-Sperm Antibody (MAR) Result Interpreter User Guide"',
        "Grading of sperm-surface antibody (MAR/immunobead) positivity: <10% negative, 10\u201350% borderline positive, \u226550% positive, \u226575% strongly positive; IgA positivity (\u226550%) correlates with reduced sperm penetration of cervical mucus, and IgM positivity suggests recent infection or a local immune response.",
        "Sperm bound to beads (%)",
        "Antibody type",
        "📋 MAR Test Interpretation Threshold (WHO)",
        "Bound sperm %",
        "No clinical significance",
        "Correlate with clinical and fertility history",
        "Suggests possible immunologic infertility",
        "Significantly affects sperm function",
        "🔬 Testing notes",
        "MAR test",
        ": sperm + antiglobulin-sensitized latex/erythrocytes; observe agglutination",
        ": more closely related to reduced sperm penetration of cervical mucus",
        ": usually suggests recent infection or local immunity",
        "Positivity should be evaluated with the sperm-cervical mucus contact test (SCMCT) for fertility impact.",
        "Note: a positive anti-sperm antibody does not mean absolute infertility; it should be assessed together with antibody type, titer and sperm function. A single positive result warrants a repeat test.",
        "📚 In-Depth: Anti-Sperm Antibody (ASA) Interpretation",
        "Antibody-titer assessment in immunologic infertility.",
        "IgA/IgM subtyping and clinical significance.",
        "Association with cervical-mucus penetration.",
        "IgA 60% positive",
        "IgA\u226550% is read as positive, closely linked to reduced sperm penetration of cervical mucus; consider immunosuppressants or assisted reproduction together with the partner's situation.",
        "IgM\u226510% suggests recent infection or active local immune response; screen for genital-tract inflammation.",
        "IgG vs IgA difference?",
        "IgA directly interferes with sperm-mucus interaction and is more clinically significant; IgG is mostly serum-type and relatively secondary.",
        "Reference threshold?",
        "Commonly the mixed antiglobulin reaction (MAR) or immunobead test: IgA\u226550% and IgM\u226510% are the positive cut-offs.",
        'About "Anti-Sperm Antibody (MAR) Result Interpreter"',
        "The Anti-Sperm Antibody (MAR) Result Interpreter reads positive/negative from the mixed antiglobulin reaction (MAR) test by the percentage of sperm bound, against the WHO reference threshold of 50%. A professional medical tool based on authoritative standards, for reference only.",
        "How to use the Anti-Sperm Antibody (MAR) Result Interpreter",
        "What does the Anti-Sperm Antibody (MAR) Result Interpreter do?",
        "How do I use the Anti-Sperm Antibody (MAR) Result Interpreter?",
        "Which scenarios suit the Anti-Sperm Antibody (MAR) Result Interpreter?",
        "Interpretation criteria",
        "Mixed antiglobulin reaction (MAR) test: the proportion of motile sperm bound to coated particles",
        "Usually negative (no evident anti-sperm antibody);",
        "Read as positive, suggesting anti-sperm antibodies that may affect sperm motility and fertilization.",
        "Anti-sperm antibodies are a common factor in immunologic infertility; positivity should be assessed with semen analysis and female partner testing, and does not alone determine fertility.",
        "Applicability limits",
        "MAR is a screen for immunologic infertility; results are affected by sample motility and handling; for diagnosis and management consult a reproductive-medicine specialist.",
    ]))
    write('assessor-15', build('assessor-15', [
        "📋 Vasography (Patency) Assessment",
        "A vasography patency-assessment tool that evaluates the vas deferens/seminal vesicle/ejaculatory duct segment by segment, aiding diagnosis of obstructive azoospermia.",
        'View "Vasography (Patency) Assessment User Guide"',
        "Radiographic findings assessment",
        "Select patency segment by segment per the vasography imaging findings",
        "Left side (segment-by-segment)",
        "Right side (segment-by-segment)",
        "Assess patency",
        "Segments assessed: vas deferens \u2192 seminal vesicle \u2192 ampulla \u2192 ejaculatory duct \u2192 contrast entering urethra/bladder",
        "Patency grading: patent (contrast passes smoothly) / partial obstruction (contrast passes slowly or narrows) / complete obstruction (contrast cannot pass)",
        "This tool is for imaging-assessment reference and should be combined with semen analysis and clinical judgment.",
        "📚 In-Depth: Vasography Patency Assessment",
        "Localizing the cause of azoospermia.",
        "Obstructive vs non-obstructive differentiation.",
        "Pre-op evaluation for microsurgical reconstruction.",
        "Both sides, all segments score 2",
        "Score 0=obstruction, 1=partial, 2=patent; both sides all 2 \u2192 bilateral patent, not supporting obstructive azoospermia.",
        "One left segment scored 0",
        "A left segment scored 0 \u2192 left-side obstruction; if only unilateral with the contralateral patent, natural conception is still possible, observe first.",
        "How to use the score?",
        "Score each segment (inguinal/pelvic/ampulla, etc.) 0\u20132; any segment 0 means that side is obstructed, bilateral 0 means obstructive azoospermia.",
        "Next steps?",
        "Bilateral obstruction often chooses PESA+ICSI; unilateral may decide on surgery based on semen parameters.",
        'About "Vasography (Patency) Assessment"',
        "A vasography patency-assessment tool that evaluates the vas deferens, ampulla, seminal vesicle and ejaculatory duct segment by segment on both sides and contrast entry into the urethra, aiding localization of obstructive azoospermia.",
        "Bilateral 5-segment patency assessment",
        "Three-tier rating: patent/partial obstruction/complete obstruction",
        "Automatic localization of obstruction site",
        "Surgery / assisted-reproduction treatment advice",
        "Diagnosis of obstructive azoospermia",
        "Pre-op evaluation for vasectomy reversal",
        "Localizing the cause of male infertility",
        "Adjunct to urogenital imaging reports",
        "How to use the Vasography (Patency) Assessment",
        "What does the Vasography (Patency) Assessment do?",
        "How do I use the Vasography (Patency) Assessment?",
        "Which scenarios suit the Vasography (Patency) Assessment?",
    ]))
    write('baifenbijisuanqi', build('baifenbijisuanqi', [
        "🧬 Percentage Calculator (Reproductive Medicine)",
        "Calculates percentages, proportions and growth rates of values",
        "Progressive Motility (PR) Percentage",
        "/ Progressive Motility (PR) Percentage",
        'View "Percentage Calculator (Reproductive Medicine) User Guide"',
        "Three percentage methods: value = a \u00d7 b \u00f7 100; ratio = a \u00f7 b \u00d7 100%; change rate = (b \u2212 a) \u00f7 a \u00d7 100% and show the change amount (b \u2212 a).",
        "📚 In-Depth: Percentage Calculator",
        "Semen-parameter proportion conversion.",
        "Viability / normal morphology rate",
        "PR 40 / total 100",
        "PR proportion = 40/100\u00d7100% = 40%, above the WHO PR\u226532% reference.",
        "Normal morphology 8 / 200",
        "Normal morphology rate = 8/200\u00d7100% = 4%, at the WHO strict criterion \u22654% borderline.",
        "Difference from a dedicated calculator?",
        "This tool does general proportions; the dedicated tool auto-applies WHO thresholds and interpretation.",
        "Denominator zero?",
        "Total must be >0; otherwise proportion cannot be computed.",
        "How to use the Percentage Calculator (Reproductive Medicine)",
        "What does the Percentage Calculator (Reproductive Medicine) do?",
        "The reproductive-medicine percentage calculator finds the percentage, proportion and change rate of metrics like sperm progressive motility (PR), suited to converting key indicators in semen-analysis reports.",
        "How do I use the Percentage Calculator (Reproductive Medicine)?",
        "Which scenarios suit the Percentage Calculator (Reproductive Medicine)?",
    ]))
    write('calc-volume-concentration', build('calc-volume-concentration', [
        "🧊 Total Sperm Count (Concentration \u00d7 Volume) Calculator",
        "Enter semen concentration and volume to compute total sperm count and assess against WHO 6th-edition semen-analysis reference values.",
        'View "Total Sperm Count (Concentration \u00d7 Volume) Calculator User Guide"',
        "Total sperm count = sperm concentration \u00d7 semen volume; WHO 6th-edition reference: concentration \u226516 million/mL and volume \u22651.4 mL are normal; total \u226539 million is normal, 10\u201339 million low, <10 million markedly reduced.",
        "Sperm concentration (million/mL)",
        "Semen volume (mL)",
        "\U0001F4A1 WHO 6th-edition reference: total sperm count \u226539 million/ejaculate is the normal lower limit; concentration \u226516 million/mL, volume \u22651.4 mL.",
        "Semen analysis requires 2\u20137 days of abstinence, with the sample tested within 1 hour of collection.",
        "A single abnormal result warrants re-test after 2\u20133 weeks to confirm.",
        "This tool's results are for clinical reference only and cannot replace a laboratory report.",
        "📚 In-Depth: Total Sperm Count (Concentration \u00d7 Volume)",
        "Semen routine",
        "Total sperm count",
        "Estimation.",
        "Oligozoospermia determination.",
        "Sperm-retrieval planning for assisted reproduction.",
        "Concentration 40\u00d710\u2076/ml, volume 3.0ml",
        "Total = 40\u00d73.0 = 120\u00d710\u2076; concentration\u226516 and volume\u22651.4 are both normal, total far above WHO \u226539\u00d710\u2076.",
        "Concentration 10, volume 1.2",
        "Total=12\u00d710\u2076 <39, and both concentration and volume are below reference, suggesting oligozoospermia.",
        "WHO 6th-edition threshold?",
        "Concentration\u226516\u00d710\u2076/ml, volume\u22651.4ml, total\u226539\u00d710\u2076 are the reference lower limits.",
        "Units",
        "Concentration is \u00d710\u2076/ml (i.e. million/mL), total is \u00d710\u2076 (million).",
        'About "Total Sperm Count (Concentration \u00d7 Volume) Calculator"',
        "Based on sperm concentration and semen volume from semen analysis, compute the total sperm count per ejaculate and perform a preliminary assessment against the WHO 6th-edition semen-analysis manual.",
        "Auto-calculate total sperm count",
        "Stratify against WHO 6th-edition reference values",
        "Also indicate whether concentration and volume meet the standard",
        "Quick estimation in andrology/reproductive-medicine clinics",
        "Self-interpretation of semen reports",
        "How to use the Total Sperm Count (Concentration \u00d7 Volume) Calculator",
        "What does the Total Sperm Count (Concentration \u00d7 Volume) Calculator do?",
        "How do I use the Total Sperm Count (Concentration \u00d7 Volume) Calculator?",
        "Which scenarios suit the Total Sperm Count (Concentration \u00d7 Volume) Calculator?",
    ]))

if __name__ == "__main__":
    main()
