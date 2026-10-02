#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'nephrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'nephrology')
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
    out = {'slug': slug, 'industry': 'nephrology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('dialysis-ktv', build('dialysis-ktv', [
        "\U0001F4CB Dialysis (Kt/V) Adequacy Assessor",
        "Compute single-pool Kt/V (spKt/V) and urea reduction ratio (URR) to assess hemodialysis adequacy",
        "Core calculation formula (by input variables): -Math.log(R-0.008\u00d7tHours)+(4-3.5\u00d7R)\u00d7ufL\u00f7postWeight; spKt\u00f7V - (0.6 \u00d7 spKt\u00f7V \u00f7 t) + 0.03; -ln(R - 0.008\u00d7t) + (4-3.5\u00d7R)\u00d7UF\u00f7W",
        "Dialysis (Kt/V) Adequacy Assessor",
        "/ Kt/V Assessor",
        "Pre-dialysis BUN (mmol/L)",
        "Post-dialysis BUN (mmol/L)",
        "Dialysis time (minutes)",
        "Dialysis frequency",
        "3 times per week",
        "2 times per week",
        "1 time per week",
        "Weight loss (kg)",
        "Post-dialysis weight (kg)",
        "\U0001F4CB Dialysis adequacy standard (KDOQI)",
        "\u22651.2 (3 times per week)",
        "Equilibrated Kt/V",
        "Standard Kt/V (including residual renal function)",
        "For patients dialyzed 3 times a week the single-session spKt/V target is \u22651.2; for 2 times a week a higher single-session Kt/V is needed; short daily dialysis (4-6 times per week) allows a lower single-session target.",
        "Note: Kt/V is the core indicator of dialysis adequacy and is affected by blood flow, dialyzer surface area, vascular access recirculation and ultrafiltration volume. Post-dialysis BUN sampling should follow the slow-flow or stop-pump method to avoid the effect of recirculation. This tool is for learning reference only.",
        "\U0001F4DA In-depth analysis: dialysis adequacy Kt/V",
        "Hemodialysis single-pool Kt/V",
        "Target value assessment",
        "Effect of dialysis frequency",
        "R=0.4, 4h, UF 2L, post-dialysis 70 kg: spKt/V\u22481.07; against the target of 1.2 for 3 sessions per week it is slightly insufficient, so increase the dose or extend the time.",
        "spKt/V\u22651.2 (3 times per week) or eKt/V\u22651.2 is considered adequate; a lower value indicates an insufficient dose.",
        "spKt/V versus eKt/V?",
        "spKt/V is single-pool while eKt/V is equilibrated, correcting for rebound; the latter is more accurate.",
        "Does frequency affect the target?",
        "Standard minimum targets are 1.2 for 3 sessions per week, 1.8 for 2 sessions and 3.0 for 1 session.",
        "About \"Dialysis (Kt/V) Adequacy Assessor\"",
        "Dialysis Kt/V adequacy assessor: computes single-pool Kt/V and urea reduction ratio (URR) from pre- and post-dialysis BUN to assess hemodialysis adequacy. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('diuretic-conversion', build('diuretic-conversion', [
        "\U0001F504 Diuretic (Loop/Thiazide) Converter",
        "Equivalent dose conversion among loop diuretics and between loop diuretics and thiazides",
        "Diuretic (Furosemide-Hydrochlorothiazide) Converter",
        "/ Diuretic Converter",
        "Loop diuretic equivalence: first convert to a furosemide-equivalent dose = original drug dose \u00d7 furosemide reference dose \u00f7 original drug reference dose; then convert to the target drug = furosemide-equivalent \u00d7 target drug reference dose \u00f7 furosemide reference dose.",
        "Loop diuretic equivalent conversion",
        "Original drug",
        "Furosemide (Lasix)",
        "Torasemide",
        "Bumetanide",
        "Ethacrynic acid",
        "Original dose (mg)",
        "Target drug",
        "\U0001F4CB Loop diuretic equivalent dose table",
        "Equivalent dose (mg)",
        "Bioavailability",
        "Duration of action",
        "Furosemide",
        "50-70% (high variability)",
        "Most commonly used, oral absorption varies widely",
        "80-90% (stable)",
        "Stable absorption, long duration",
        "High bioavailability",
        "Close to 100%",
        "Can be used in patients allergic to sulfonamides",
        "\U0001F4CB Equivalence reference between loop diuretics and thiazides",
        "Loop diuretic",
        "Equivalent thiazide",
        "Furosemide 20 mg",
        "Hydrochlorothiazide 25 mg",
        "Approximate equivalence reference",
        "Furosemide 40 mg",
        "Hydrochlorothiazide 50 mg",
        "Furosemide 80 mg",
        "Hydrochlorothiazide 100 mg (above the maximum dose)",
        "High doses require loop diuretics",
        "Note: loop diuretics and thiazides differ in mechanism and site of action; the equivalent conversion is a clinical reference only and they cannot be substituted one-for-one.",
        "Note: oral furosemide bioavailability varies greatly between individuals (10-100%), and the intravenous potency is about twice the oral potency (oral 40 mg \u2248 IV 20 mg). Torasemide and bumetanide have stable bioavailability. CKD patients often need high doses of loop diuretics. This tool is for learning reference only; follow medical advice for actual medication.",
        "\U0001F4DA In-depth analysis: diuretic equivalent conversion",
        "Switching among loop diuretics",
        "Switching to thiazides",
        "Switching from IV to oral",
        "Equivalent to torasemide 20 mg or bumetanide 1 mg (furosemide:torasemide = 2:1, furosemide:bumetanide = 40:1).",
        "Switching torasemide to furosemide",
        "Torasemide 20 mg \u2192 furosemide 40 mg; watch for the difference in oral bioavailability.",
        "Why convert?",
        "Different loop diuretics have different potencies; switch by equivalent dose to avoid overdose or underdose.",
        "Effect of renal function?",
        "Furosemide remains usable in renal failure, while torasemide is metabolized by the liver and affected by liver function.",
        "About \"Diuretic (Furosemide-Hydrochlorothiazide) Converter\"",
        "Diuretic converter: equivalent dose conversion for loop diuretics such as furosemide, torasemide and bumetanide, and thiazides such as hydrochlorothiazide. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()
