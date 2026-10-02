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
    write('index', build('index', [
        "\U0001F33F Chinese Medicine Chemistry Tools",
        "Chinese medicine chemistry",
        "Chinese medicine chemistry tools",
        "Enter the reference standard and internal standard peak areas, the sample and internal standard peak areas and the concentrations, then compute the correction factor and the content percentage of the active component by the internal standard method; used for data processing in chromatographic assays such as GC and HPLC.",
        "Concentration (Reduced-Pressure Evaporation) Temperature and Vacuum Calculator",
        "Enter the vacuum (or system pressure) to compute the boiling point of aqueous or ethanol solutions under reduced-pressure evaporation, helping protect heat-sensitive TCM active components during low-temperature concentration; used to choose vacuum and temperature parameters for reduced-pressure concentration of extracts.",
        "Enter the powder bed height and base diameter to compute the angle of repose, evaluate powder flowability and recommend a suitable empty capsule size and approximate fill volume (estimated from a bulk density of about 0.8 g/mL); used for capsule size selection in TCM powder filling.",
        "Extraction Count (Partition Coefficient) Calculator",
        "Enter the partition coefficient K, the phase ratio (organic to aqueous volume ratio) and the target recovery to compute the number of liquid-liquid extraction rounds needed and the recovery of each round; used to design extraction schemes that fully transfer the target component during separation and purification.",
        "Based on the Arrhenius equation with degradation rates at different temperatures, predicts the shelf life of TCM preparations at room temperature and designs light or heat accelerated test conditions; used for drug stability studies and regulatory filing preparation.",
        "Based on the Higuchi equation with time and cumulative release, computes the release rate constant of an ointment and compares how different bases affect transdermal release; used for screening and evaluating topical formulation prescriptions.",
        "Extraction count calculation (partition coefficient)",
        "Extraction count calculation (partition coefficient method)",
        "Enter the LD50 of an animal species and its body weight, convert to the equivalent dose in humans or other species by the body surface area method, and give a toxicity grade (such as highly toxic or low toxic); used for cross-species dose extrapolation and toxicity evaluation in TCM safety assessment.",
        "Enter solubility data for the target component at high and low temperatures to predict the theoretical yield of cooling crystallization or solvent evaporation crystallization; used to optimize crystallization conditions (cooling range, solvent choice) and estimate yield in TCM chemistry purification.",
        "Enter the peak data of the test TCM fingerprint and the reference fingerprint, compute the correlation coefficient or the cosine of the angle similarity to evaluate batch-to-batch consistency; used for fingerprint similarity evaluation and authenticity discrimination in TCM quality control.",
        "Enter the impurity spot concentrations and spotting volumes of the test sample and the reference, compute the impurity limit by thin-layer chromatography (TLC) and semi-quantitatively evaluate whether the impurity level exceeds the standard; used for related-substance limit tests in TCM decoction pieces and preparations.",
        "Enter the chromatographic column and mobile phase parameters to compute HPLC retention time, theoretical plate count (column efficiency) and the resolution between adjacent peaks, and evaluate and optimize the chromatographic conditions; used for developing and screening HPLC methods for TCM components.",
        "Computes the relative response factor (RRF) and relative correction factor (RCF) to correct multi-component assay results",
        "TCM compatibility taboo detector: enter two Chinese medicine names to check the eighteen antagonisms, nineteen fears and other physicochemical compatibility taboos and flag combinations that should not be used together, for reference.",
        "Chromatography (Silica Gel Column) Elution Gradient Designer",
        "Select the polarity type of the target component to generate a silica gel column chromatography gradient elution scheme (for example a stepwise transition from weak polarity to strong polarity solvent systems), optimizing the resolution and elution of the target component; used for column chromatography purification design of TCM constituents.",
        "Enter the absorption peak data of IR, UV or NMR spectra, automatically match characteristic peaks and assign functional groups (such as hydroxyl, carbonyl and aromatic ring), assisting in inferring the chemical structure of TCM constituents; used for spectral interpretation in natural product structure identification.",
        "Enter the structure and administration route of a TCM constituent to predict its phase I (oxidation, hydrolysis and similar) and phase II (conjugation) metabolic reactions and possible products; used for preliminary inference of in vivo transformation pathways in TCM pharmacokinetic studies.",
        "Enter the target component type (such as alkaloid, flavonoid or volatile oil) and its polarity to recommend a matching extraction solvent system and approximate concentration, with a note on solvent polarity matching principles; used for solvent screening in TCM active component extraction processes.",
        "Enter two or more Chinese medicines to check whether classic compatibility taboos such as the eighteen antagonisms and nineteen fears exist and flag possible physicochemical interactions (such as precipitation and decomposition); used for prescription review and safety checks of rational TCM compatibility.",
        "Look up the solubility grades of TCM active components in water, ethanol, petroleum ether and other solvents and list the solubility characteristics; used to choose extraction and purification solvents from component polarity and guide TCM extraction and separation process design.",
        "Enter the amount retained on each sieve to compute granule particle size distribution and uniformity, combine it with moisture results for an overall quality evaluation referencing Chinese Pharmacopoeia standards; used for TCM granule quality control.",
        "One-compartment open model estimation of pharmacokinetic parameters for TCM active components (Cmax, Tmax, T1/2, AUC and similar)",
        "About the Chinese Medicine Chemistry Tools",
        "This Chinese medicine chemistry tool collection includes 22 free online tools covering the common calculation, conversion and lookup needs in Chinese medicine chemistry. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run entirely in the front end and no data is uploaded to the server, so privacy and security are protected.",
        "The Chinese medicine chemistry tools included on this page are (some representative tools):",
        "These tools help you quickly finish common Chinese medicine chemistry tasks without memorizing complex formulas or doing manual conversions, so you just enter the values and get the result.",
        "Do the Chinese medicine chemistry tools need a download or registration?",
        "No. All Chinese medicine chemistry tools on this page are pure front-end online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the Chinese medicine chemistry tool results accurate, and is the data secure?",
        "The tools compute locally in your browser using public mathematical formulas and common industry standards, so results are immediate. All computation happens locally on your device and no data is uploaded to the server, so privacy and security are assured.",
    ]))
    write('metabolite-prediction', build('metabolite-prediction', [
        "\U0001F52E Metabolite (In Vivo Transformation) Predictor",
        "Predicts in vivo metabolic pathways and products of TCM active components, including phase I and phase II reactions",
        "/ Metabolite prediction",
        "Compound type",
        "Saponins",
        "Coumarins",
        "Specific compound (optional)",
        "Topical",
        "Molecular weight (optional, used to estimate metabolites)",
        "\U0001F52E Predict the metabolic pathway",
        "\U0001F4DA In-depth analysis: metabolite (in vivo transformation) prediction",
        "Oral first-pass metabolism",
        "Intravenous straight into blood",
        "Pathway inference",
        "Flavonoids taken orally undergo gastrointestinal and hepatic first-pass glycosylation and glucuronidation, so what enters the blood is mostly the aglycone or conjugates; those with low MW and good membrane permeability have higher oral bioavailability.",
        "Intravenous",
        "Intravenous injection bypasses first-pass metabolism, F is about 100%, enters the blood directly and is metabolized by hepatic CYP,",
        "determined by CL/Vd.",
        "Does first-pass metabolism matter?",
        "Oral dosing loses F through hepatic and intestinal wall metabolism, so the dose must be raised accordingly or the dosage form changed.",
        "Is the metabolite prediction reliable?",
        "It is rule-based (functional group plus pathway) and suggests possible products; the exact structure needs LC-MS measurement.",
        "About the Metabolite (In Vivo Transformation) Predictor",
        "Metabolite predictor - predicts in vivo metabolic transformation pathways of TCM active components, including phase I and phase II metabolic reactions." + DISCL_M,
    ]))
    write('pharmacokinetics', build('pharmacokinetics', [
        "\U0001F3CB\ufe0f Pharmacokinetic Parameter (Cmax/T1/2) Estimator",
        "One-compartment open model estimation of pharmacokinetic parameters for TCM active components (Cmax, Tmax, T1/2, AUC and similar)",
        "/ Pharmacokinetic parameter estimation",
        "Parameter estimation",
        "Reference data",
        "Common component presets",
        "Dose (mg)",
        "Bioavailability F (%)",
        "Apparent volume of distribution Vd (L)",
        "Clearance CL (L/h)",
        "Absorption rate constant Ka (1/h)",
        "Route of administration",
        "Oral (extravascular)",
        "Intravenous bolus",
        "Dosing interval tau (h)",
        "\U0001F3CB\ufe0f Estimate the parameters",
        "Pharmacokinetic parameter reference for TCM active components",
        "The data above come from reported literature averages and vary widely between individuals. Vd is the apparent volume of distribution and CL is the plasma clearance; practical use needs individualized data.",
        "\U0001F4DA In-depth analysis: pharmacokinetic parameter (Cmax / T1/2) estimation",
        "Oral one-compartment model Cmax",
        "Accumulation factor",
        "Steady-state trough/peak concentration",
        "Oral dosing",
        "Dose 500 mg, F = 80%, Vd = 50 L, CL = 5 L/h, ka = 1 per hour, tau = 12 h: Ke = 5/50 = 0.1 per hour, T1/2 = 0.693/0.1 = 6.93 h, AUC = 400/5 = 80 mg.h/L.",
        "Accumulation factor",
        "R = 1/(1-e^(-Ke*tau)) = 1/(1-e^(-0.1x12)) = 1/(1-0.301) = 1.43, so the steady-state peak over multiple doses is about 1.43 times the first dose.",
        "Is AUC independent of the route?",
        "Yes, AUC = F*Dose/CL holds for either intravenous or oral; oral just adds the bioavailability F.",
        "Is T1/2 affected by dose?",
        "Under linear one-compartment kinetics T1/2 = 0.693*Vd/CL and is dose-independent; only non-linear (saturating) kinetics make it vary with dose.",
        "About the Pharmacokinetic Parameter (Cmax/T1/2) Estimator",
        "Pharmacokinetic parameter Cmax/T1/2 estimator - one-compartment model estimation of pharmacokinetic parameters for TCM active components, with reference data for common components." + DISCL_M,
    ]))


if __name__ == '__main__':
    main()