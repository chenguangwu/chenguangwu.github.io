#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'bonding')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'bonding')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'bonding', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- detector-26 (20) ----------------
    write('detector-26', build('detector-26', [
        "📏 Adhesive Layer (Thickness / Uniformity / Defect) Inspection",
        "Thickness / uniformity / defect",
        "Based on the judgement thresholds for adhesive layer thickness, uniformity and defects, enter the measured thickness and tolerance band to give a pass / too thin / too thick verdict and defect risk prompts, assisting in-line quality inspection; pure front-end calculation, data never leaves the browser.",
        "📚 Deep dive: Adhesive Layer (Thickness / Uniformity / Defect) Inspection",
        "In-line quality inspection of adhesive layer thickness: enter the design thickness and multi-point measurements, compute the mean thickness, maximum deviation and uniformity (range / mean), and judge \"pass / needs rework / fail\".",
        "Batch uniformity monitoring: compare the thickness dispersion (cv uniformity index) of each measurement point in the same batch to locate uneven adhesive application.",
        "Joint defect judgement: combined with defect grades such as bubbles / debonding / inclusions, give an overall disposition recommendation (pass / rework / re-bond).",
        "Example: design 0.2mm / tolerance 20% / 8 measured points / no defects",
        "Input: design adhesive layer 0.2 mm, allowable deviation 20%, 8 measured points 0.18,0.22,0.19,0.21,0.17,0.23,0.20,0.19 mm, no defects. Mean 0.199 mm; maximum deviation = max(|0.23−0.2|,|0.17−0.2|)/0.2×100% = 15.0%; uniformity cv = range/mean×100% = 0.06/0.19875×100% = 30.2%; thickness deviation 15.0% ≤ 20% passes, but uniformity 30.2% > 15% → needs rework (uneven application). By comparison the passing example (0.20,0.21,0.19,0.20,0.20,0.19,0.21,0.20): mean 0.200, maximum deviation 5.0%, cv 10.0% → pass.",
        "Why does it still say \"needs rework\" when the mean thickness is within tolerance?",
        "Because this tool gates on two indicators, \"thickness deviation\" and \"uniformity\". A mean within range but points alternating thick and thin (cv>15%) means uneven application, which can cause local thin failure or local adhesive-rich",
        "stress concentration",
        ", so it is judged as needing rework rather than a straight pass.",
        "How does the defect grade affect the conclusion?",
        "No obvious defects + uniform thickness → pass; a few light defects such as bubbles or thickness slightly out of tolerance → needs rework; debonded areas / many bubbles / inclusions at level≥3 → fail outright and require removal and re-bonding. Defects and thickness indicators are combined with an \"or\" logic: any severe one means fail.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Compute mean thickness, maximum deviation and uniformity from in-line adhesive layer inspection to judge pass / rework",
        "Monitor thickness dispersion across measurement points in the same batch to locate uneven adhesive application",
        "Give a joint disposition recommendation from bubble / debonding / inclusion defect grades",
    ]))

    # ---------------- detector-27 (18) ----------------
    write('detector-27', build('detector-27', [
        "🔍 Bonding (Non-destructive / Inspection / Ultrasonic) Methods",
        "Non-destructive / inspection / ultrasonic",
        "Based on the ultrasonic non-destructive testing rules for sound path and defect echo, enter the sound speed, probe angle and echo position to estimate defect depth and type, assisting bonding quality assessment; pure front-end calculation, data never leaves the browser.",
        "📚 Deep dive: Bonding (Non-destructive / Inspection / Ultrasonic) Methods",
        "Ultrasonic screening of metal-to-metal / composite bonding quality: enter echo amplitude, bottom-wave attenuation and the number of suspect signals, and judge \"bonding good / basically qualified / needs recheck / fail\" against the thresholds.",
        "Spot checks on large bonded areas: for components with a large inspected area, use the \"suspect signal area ratio\" to help judge defect density and decide the sampling ratio.",
        "Recheck decision: when the signal is abnormal, recommend \"increasing the inspection ratio or supplementing with X-ray\" to avoid missing debonding.",
        "Example: echo −6dB / attenuation 3dB / area 100cm² / signals 2",
        "Input: echo amplitude −6 dB, bottom-wave attenuation 3 dB, inspected area 100 cm², suspect signals 2. Determination: echo ≥−6 dB normal, bottom-wave attenuation ≤4 dB normal, signal count ≤2 → basically qualified; suspect signal area ratio = 2/max(100/10,1)×100% = 20.0%. By comparison: 6 signals, echo −2 dB, attenuation 1 dB → fail (area ratio 60.0%); 0 signals, echo −3 dB, attenuation 2 dB → bonding good (area ratio 0%).",
        "What do the echo and the bottom wave each tell you?",
        "The echo amplitude reflects the sound energy loss caused by defects (debonding / voids); the closer to 0 dB the better (this tool judges ≥−6 dB as good). The bottom-wave attenuation reflects sound coupling and the overall bonding state, with ≤4 dB being normal. The two combined are more reliable than either alone.",
        "What to do after it says \"needs recheck\"?",
        "Do not scrap it outright. First raise the inspection ratio, scan the suspect area more densely, or cross-validate with X-ray / thermal imaging; only judge it a failure and re-bond when large-area debonding is confirmed. Ultrasonic methods are sensitive to non-contact debonding but may miss weakly bonded interfaces, which is why rechecking matters.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Ultrasonic screening of metal / composite bonding quality with the echo and bottom-wave thresholds",
        "Use the suspect signal area ratio on large bonded areas to judge defect density",
        "Recommend increasing the inspection ratio or supplementing with X-ray when the signal is abnormal",
    ]))

    # ---------------- index (18) ----------------
    write('index', build('index', [
        "🧷 Bonding and Sealing Tools",
        "Bonding and sealing",
        "Bonding and Sealing Tools",
        "Assess fatigue life grades from the performance, cycle count and ageing data of a bonded joint under alternating loads, and output a state verdict, used for structural bonding reliability checks.",
        "Judge debonding, delamination and other interface defects from ultrasonic echo and coupling data, and give a pass verdict, used for non-destructive quality inspection.",
        "Enter adhesive layer measurement data to inspect thickness deviation, uniformity and voids / debonding defects, and output the defect status and pass verdict, used for bonding quality control.",
        "Bonding (Cost / Efficiency / Substitution) Analysis",
        "Enter bonding material, labor and alternative process parameters to compare the cost, efficiency and substitutability of bonding options, assisting manufacturing process selection and cost reduction decisions.",
        "Bonding (Case Analysis / Failure / Resolution)",
        "Enter bonding failure symptoms and operating parameters, match common failure types against engineering experience and give troubleshooting and resolution ideas, assisting bonding process quality improvement.",
        "About \"Bonding and Sealing Tools\"",
        "The Bonding and Sealing Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of bonding and sealing scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The bonding and sealing tools listed on this page include (a few representative tools):",
        "These tools help you finish common bonding and sealing tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the bonding and sealing tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the bonding and sealing tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
