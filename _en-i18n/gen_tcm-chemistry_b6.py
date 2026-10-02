#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tcm-chemistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tcm-chemistry')
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
    out = {'slug': slug, 'industry': 'tcm-chemistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('capsule-filling', build('capsule-filling', [
        "\U0001F9EE Capsule Filling (Powder / Flowability) Angle of Repose Calculator",
        "Powder angle of repose calculation, flowability evaluation and capsule size selection",
        "Powder angle of repose calculation, flowability evaluation and capsule size selection.",
        "/ Capsule filling calculation",
        "Flowability evaluation",
        "Capsule filling calculation",
        "Reference data",
        "Angle of repose measurement and flowability evaluation",
        "Powder bed height h (mm)",
        "Powder bed base diameter D (mm)",
        "Bulk density rhob (g/mL)",
        "Tapped density rhot (g/mL)",
        "\U0001F9EE Compute the flowability",
        "Capsule size selection and fill volume calculation",
        "Target fill amount (mg)",
        "Powder bulk density (g/mL)",
        "Particle size (mesh)",
        "20 mesh (coarse)",
        "40 mesh",
        "60 mesh (medium)",
        "80 mesh",
        "100 mesh (fine)",
        "\U0001F9EE Compute the filling",
        "Capsule size specification table",
        "Volume (mL)",
        "Fill upper limit (mg)*",
        "*The fill upper limit is estimated from a bulk density of 0.8 g/mL; the actual fill amount depends on powder density and flowability",
        "Angle of repose and flowability grades",
        "Angle of repose (degrees)",
        "Flowability",
        "No glidant needed",
        "Can be filled directly",
        "Good",
        "Flowability is good",
        "Take care",
        "Add 1% glidant",
        "Flowability is poor",
        "Add 2-3% glidant",
        "Not suitable for direct filling",
        "Granulate or add a glidant",
        "Cannot be filled automatically",
        "Granulation is required",
        "Common glidants",
        "Colloidal silicon dioxide (white carbon black):",
        "0.1-1% level, markedly improves flowability",
        "Talc:",
        "1-5% level, acts as both glidant and anti-adherent",
        "Magnesium stearate:",
        "0.25-1% level, a lubricant that also aids flow; avoid excessive use",
        "Granulation binder, improves flowability through granulation",
        "\U0001F4DA In-depth analysis: capsule filling (powder flowability)",
        "Angle of repose evaluation",
        "Hausner ratio",
        "Capsule size selection",
        "Bed height h = 15 mm, diameter D = 6 mm so radius r = 3 mm; angle of repose = atan(15/3)x180/pi = 78.7 degrees (poor flowability); bulk 0.5 and tapped 0.65 give Hausner = 1.30 (above 1.25 indicates deviation).",
        "Capsule size selection",
        "Target fill 300 mg at a filling density of 0.7 g/mL; required volume = 300/(0.7x1000) = 0.429 mL, so size 0 (about 0.68 mL) gives a fill rate of about 63%.",
        "What angle of repose counts as good?",
        "30 degrees or less is good flowability, 30 to 40 degrees is moderate, and above 40 degrees is poor and needs a glidant.",
        "What does the Hausner ratio mean?",
        "It is tapped divided by bulk; the closer to 1 the better the flowability, and above 1.25 segregation and uneven filling become likely.",
        "About the Capsule Filling (Powder / Flowability) Angle of Repose Calculator",
        "Capsule filling powder flowability angle of repose calculator - powder flowability evaluation and capsule size selection." + DISCL_M,
        "How to use the Capsule Filling (Powder / Flowability) Angle of Repose Calculator",
        "What does the Capsule Filling (Powder / Flowability) Angle of Repose Calculator do?",
        "Enter the powder bed height and base diameter to compute the angle of repose, evaluate powder flowability and recommend a suitable empty capsule size with approximate fill volume (estimated from a bulk density of about 0.8 g/mL); used for capsule size selection in TCM powder filling.",
        "How do I use the Capsule Filling (Powder / Flowability) Angle of Repose Calculator?",
        "Which scenarios suit the Capsule Filling (Powder / Flowability) Angle of Repose Calculator?",
    ]))
    write('ointment-release', build('ointment-release', [
        "\U0001F48A Ointment (Base / Drug) Release Calculator",
        "Computes ointment drug release from the Higuchi model and evaluates how different bases affect release",
        "Computes ointment drug release from the Higuchi model and evaluates how different bases affect release.",
        "/ Ointment release",
        "Release calculation",
        "Base selection",
        "Reference data",
        "Higuchi model release calculation",
        "Base type",
        "Oily base (such as petrolatum)",
        "O/W emulsion base",
        "W/O emulsion base",
        "Water-soluble base (such as PEG)",
        "Hydrogel base (such as carbomer)",
        "Drug concentration A (mg/cm3)",
        "Drug solubility Cs (mg/cm3)",
        "Diffusion coefficient D (cm2/h)",
        "Release time t (h)",
        "Ointment thickness h (cm)",
        "\U0001F48A Compute the release",
        "Base selection recommendation",
        "Drug nature",
        "Lipophilic drug",
        "Water-soluble drug",
        "Amphiphilic drug",
        "Application site",
        "Intact skin",
        "Damaged / ulcerated skin",
        "Mucosa",
        "Release requirement",
        "Fast release",
        "Moderate release",
        "Slow release (long acting)",
        "Stability requirement",
        "High (prone to oxidation / hydrolysis)",
        "\U0001F48A Recommend a base",
        "Comparison of ointment base types",
        "Representative base",
        "Release speed",
        "Water absorption",
        "Washability",
        "Oily",
        "Petrolatum, lanolin",
        "Difficult",
        "Protective, moisturizing",
        "O/W emulsion",
        "Cetyl alcohol plus emulsifier",
        "Good",
        "Easy",
        "Penetrates and absorbs into skin",
        "W/O emulsion",
        "Lanolin plus cholesterol",
        "Relatively difficult",
        "Moisturizing and skin softening",
        "Damaged skin",
        "Hydrogel",
        "Carbomer, hyaluronic acid",
        "Cooling, transdermal",
        "Common TCM ointment formulas",
        "Zi Cao Gao (oily base)",
        "Lithospermum extract plus angelica extract in a petrolatum base",
        "Relatively slow release, suitable for repair of chronic skin lesions",
        "Huang Lian ointment (O/W emulsion)",
        "Berberine plus cetyl/stearyl alcohol with Tween/Span emulsifiers",
        "Fast release, suitable for acute infected skin",
        "Borneol gel (hydrogel base)",
        "Borneol plus menthol in a carbomer gel",
        "Fast release with a strong cooling feel, suitable for insect bites",
        "Release measurement method",
        "Method:",
        "Cell apparatus method (pharmacopoeia general chapter 1093)",
        "Medium:",
        "Phosphate buffer (pH 5.0-7.4) or artificial sweat",
        "Temperature:",
        "32 +/- 0.5 C (simulating skin temperature)",
        "Sampling time:",
        "Evaluation:",
        "Compute the cumulative release at each time point and plot the release curve",
        "Release kinetic models",
        "Higuchi model:",
        "Q = K*sqrt(t) (matrix-controlled release)",
        "Zero-order kinetics:",
        "Q = K0*t (constant-rate release)",
        "First-order kinetics:",
        "Q = K*t^n (n<=0.45 Fick diffusion, 0.45<n<0.89 mixed mechanism)",
        "\U0001F4DA In-depth analysis: ointment release (Higuchi)",
        "Higuchi equation",
        "Release rate dQ/dt",
        "Base influence",
        "Release worked example",
        "Drug loading A = 10 mg/cm3, effective diffusion D = 1e-7 cm2/h, thickness h = 0.1 cm, t = 6 h: Q = 10 x sqrt(1e-7x6/0.1) = 10 x 0.002449 = 0.0245 mg/cm2; K = Q/sqrt(t) = 0.0100, and the 6 h release rate is 0.0245 over the total drug amount.",
        "Release rate",
        "dQ/dt = K/(2*sqrt(t)) = 0.0100/(2 x sqrt(6)) = 0.00204 mg/cm2/h, decreasing over time (the sqrt(t) law).",
        "Is Higuchi applicable?",
        "It applies to planar matrix systems where the drug is in excess in the base (A is much greater than Cs).",
        "How is the base chosen?",
        "Oily bases are slowest while water-soluble and hydrogel bases are fast; choose an emulsion or water-soluble base when fast action is needed.",
        "About the Ointment (Base / Drug) Release Calculator",
        "Ointment base drug release calculator - Higuchi model release computation and ointment base selection." + DISCL_M,
    ]))
    write('response-factor', build('response-factor', [
        "\U0001F33F Multi-Component (Response Factor) Corrector",
        "Computes the relative response factor (RRF) and relative correction factor (RCF) to correct multi-component assay results",
        "Computes the relative response factor (RRF) and relative correction factor (RCF) to correct multi-component assay results.",
        "/ Response factor correction",
        "Reference substance name",
        "Reference substance concentration (mg/mL)",
        "Reference substance peak area",
        "List of components to be measured",
        "\U0001F33F Compute the correction factor",
        "Relative response factor RRF = (Ai/Ci) / (Aref/Cref)",
        "Relative correction factor RCF = 1/RRF = (Aref/Cref) / (Ai/Ci)",
        "Corrected content = content before correction x RCF",
        "\U0001F4DA In-depth analysis: multi-component relative response factor correction",
        "Single-measurement multi-evaluation RRF",
        "Relative correction factor RCF",
        "Multi-component content normalization",
        "RRF calculation",
        "Reference peak area 520000 at 1 mg/mL gives a response of 520000; component peak area 460000 at 1 mg/mL gives a response of 460000; RRF = 460000/520000 = 0.885 and RCF = 1/0.885 = 1.13.",
        "Corrected amount",
        "Component mass qty = 10 mg gives correctedQty = qty x RCF = 10 x 1.13 = 11.3 mg.",
        "What does single-measurement multi-evaluation solve?",
        "It estimates RRF for multiple components using an easily available reference standard, avoiding the need to buy every reference standard; suitable for multi-indicator component control.",
        "What is the relation between RRF and RCF?",
        "RCF = 1/RRF; it converts the component response onto the reference substance basis.",
        "About the Multi-Component (Response Factor) Corrector",
        "Multi-component response factor corrector - computes the relative response factor (RRF) and corrects multi-component quantitative analysis results." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()