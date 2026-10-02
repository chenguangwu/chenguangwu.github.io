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
    write('endometrial-receptivity', build('endometrial-receptivity', [
        "📏 Endometrial Receptivity Evaluator",
        "Evaluates endometrial receptivity in the embryo-transfer window by endometrial thickness and echo pattern (triple-line sign)",
        "Endometrial (Thickness Triple-Line) Receptivity Evaluator",
        'View "Endometrial Receptivity Evaluator User Guide"',
        "Endometrial receptivity is judged by thickness and echo type: type C hyperechoic has poor receptivity; thickness <6mm too thin, 6\u20137mm borderline thin, 7\u201314mm with type A triple-line is good receptivity, type B is borderline; combine with cycle day to determine the transfer window.",
        "Endometrial echo type",
        "Type A prominent triple-line",
        "Type B blurred triple-line/isoechoic",
        "Type C homogeneous hyperechoic",
        "Menstrual cycle day",
        "📋 Endometrial Receptivity Criteria",
        "Thickness + type",
        "7-14mm + Type A",
        "Good receptivity",
        "Suitable for transfer",
        "7-14mm + Type B",
        "Borderline receptivity",
        "Transferable, with individualized assessment",
        "Thin endometrium",
        "Recommend improving before transfer",
        "Thick endometrium",
        "Assess risk of being too thick",
        "Poor receptivity",
        "Not recommended for transfer in this cycle",
        "🔬 Echo Type (Gonen) Definition",
        "Type A triple-line",
        ": strong-weak-strong three layers, outer and central hyperechoic, middle hypoechoic, suggesting proliferative phase",
        "Type B",
        ": blurred triple-line, endometrium isoechoic with myometrium",
        "Type C",
        ": homogeneous hyperechoic, suggesting secretory phase/transformation",
        "Optimal transfer window: endometrium 8-12mm + Type A triple-line",
        "📊 Endometrial Thickness and Pregnancy Relation",
        "Receptivity",
        "Markedly reduced",
        "Too thick, needs assessment",
        "Note: ERA (endometrial receptivity array) can more precisely judge the transfer window. Thin endometrium may try estrogen, aspirin, G-CSF and other improvement plans. For learning reference only.",
        "📚 In-Depth: Endometrial Receptivity Assessment",
        "Determining endometrial conditions in the transfer window.",
        "Triple-line sign and thickness association.",
        "Screening before frozen/fresh embryo transfer.",
        "Thickness 9mm, Type A, cycle day 12",
        "Proliferative-phase Type A triple-line and thickness 7\u201314mm \u2192 good receptivity, suitable transfer window.",
        "Thickness 5mm, Type C",
        "Too thin and secretory-phase Type C appearing prematurely, poor receptivity, recommend adjusting the protocol or endometrial cavity assessment.",
        "Ideal thickness?",
        "Usually 7\u201314mm with Type A triple-line is best; <7mm receptivity declines.",
        "Type A/B/C?",
        "A proliferative triple-line, B transition, C secretory homogeneous hyperechoic; interpret with cycle day.",
        'About "Endometrial (Thickness Triple-Line) Receptivity Evaluator"',
        "The Endometrial (Thickness Triple-Line) Receptivity Evaluator assesses endometrial receptivity in the embryo-transfer window by endometrial thickness and the triple-line sign (echo type). A professional medical tool based on authoritative standards, for reference only.",
        "How to use the Endometrial Receptivity Evaluator",
        "What does the Endometrial Receptivity Evaluator do?",
        "Enter endometrial thickness and ultrasound echo type (whether triple-line sign is present); the tool assesses endometrial receptivity in the embryo-transfer window, flags risks of being too thin or echo abnormality, and helps reproductive physicians time the optimal transfer.",
        "How do I use the Endometrial Receptivity Evaluator?",
        "Which scenarios suit the Endometrial Receptivity Evaluator?",
    ]))
    write('epididymal-aspiration', build('epididymal-aspiration', [
        "📋 Epididymal Sperm Retrieval-Rate Evaluator",
        "Estimates total sperm obtained by epididymal puncture/aspiration; motile amount counted separately as motility%.",
        "Epididymal Puncture (Sperm) Retrieval-Rate Evaluator",
        "/ Epididymal Puncture Retrieval-Rate Evaluator",
        'View "Epididymal Sperm Retrieval-Rate Evaluator User Guide"',
        "Total retrieved sperm (\u00d710\u2076) = concentration (\u00d710\u2076/mL) \u00d7 volume (mL)",
        "PESA / MESA aspirate sperm-volume assessment, judging whether ART demand is met",
        "Total retrieved sperm (\u00d710\u2076) = concentration (\u00d710\u2076/mL) \u00d7 volume (mL); goal: ICSI needs motile sperm",
        "Puncture method",
        "PESA percutaneous epididymal puncture",
        "MESA microsurgical epididymal sperm aspiration",
        "Aspirate volume (mL)",
        "Aspirate sperm concentration (\u00d710\u2076/mL)",
        "Motile sperm rate (%)",
        "ICSI oocytes needed",
        "📋 Retrieval Result Interpretation",
        "Total motile sperm",
        "\u2265 1\u00d710\u2075 per oocyte",
        "Meets ICSI",
        "Enough \u2265 1 per oocyte",
        "ICSI can be completed",
        "Very few / immotile",
        "Switch to TESE testicular sperm extraction",
        "No sperm retrieved",
        "Contralateral puncture or switch to TESE",
        "🔬 Sperm-Retrieval Method Comparison",
        ": percutaneous blind puncture, simple but low yield and poor repeatability",
        ": micro-incision of epididymal duct, high yield and good sperm motility",
        ": used when epididymal retrieval fails or in NOA",
        "Obstructive azoospermia (OA) has high retrieval rate; non-obstructive (NOA) needs mTESE",
        "Note: epididymal sperm are usually non-motile or weakly motile, and motility may recover after in-vitro incubation. Retrieved sperm can be fresh or frozen for ICSI. For learning reference only.",
        "📚 In-Depth: Epididymal Puncture Sperm Yield",
        "PESA/MESA sperm-yield estimation.",
        "Motile sperm allocatable per oocyte.",
        "ICSI material-planning.",
        "0.5ml\u00d750\u00d710\u2076/ml, motility 40%, oocytes 8",
        "Total=0.5\u00d750=25\u00d710\u2076; motile=25\u00d740%=10\u00d710\u2076; per oocyte=10/8=1.25\u00d710\u2076, enough for ICSI.",
        "Low volume, low motility",
        "Total 5\u00d710\u2076, motile 1\u00d710\u2076, oocytes 10 \u2192 only 0.1\u00d710\u2076 per oocyte, rather tight, consider repeat puncture or TESE.",
        "PESA vs MESA?",
        "PESA percutaneous coarse needle, MESA microscopic direct vision; the latter is more precise but more invasive.",
        "How much per oocyte is enough?",
        "ICSI needs only a few motile sperm per oocyte; routine retrieval far exceeds demand.",
        'About "Epididymal Puncture (Sperm) Retrieval-Rate Evaluator"',
        "The Epididymal Puncture (PESA/MESA) sperm retrieval-rate evaluator computes total retrieved sperm from aspirate sperm count and volume, assessing ART feasibility. A professional medical tool based on authoritative standards, for reference only.",
        "How to use the Epididymal Sperm Retrieval-Rate Evaluator",
        "What does the Epididymal Sperm Retrieval-Rate Evaluator do?",
        "The Epididymal Sperm Retrieval-Rate Evaluator estimates total motile sperm from PESA/MESA aspirate concentration and volume, judging whether ICSI and other ART demands are met.",
        "How do I use the Epididymal Sperm Retrieval-Rate Evaluator?",
        "Which scenarios suit the Epididymal Sperm Retrieval-Rate Evaluator?",
    ]))

if __name__ == "__main__":
    main()
