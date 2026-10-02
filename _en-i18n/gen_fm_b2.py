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
    write('death-time-estimation', build('death-time-estimation', [
        "\U0001F441\ufe0f Death Time Estimator (Body Cooling and Corneal Clouding)",
        "Estimate the post-mortem interval from body cooling formulas (Glaister/Henssge) combined with the degree of corneal clouding",
        "Core formula (over the input variables): glaisterHours \u00d7 0.35 + henssgeHours \u00d7 0.65; max(0, henssgeHours - 2.8); Math.round((h - hh) \u00d7 60)",
        "/ Death Time Estimator",
        "\U0001F4D6 Read the \"Guide to Using the Death Time (Body Cooling + Corneal Clouding) Estimator\"",
        "Rectal Temperature Tr (\u00b0C)",
        "Degree of Corneal Clouding",
        "Clear (transparent)",
        "Mild clouding (hazy)",
        "Moderate clouding (pupil blurred)",
        "Severe clouding (fully opaque)",
        "Clothing Condition",
        "Naked / thin clothing",
        "Normal clothing",
        "Thick clothing / covered with bedding",
        "Environmental Condition",
        "Indoor still air",
        "Ventilated / windy",
        "In water / in rain",
        "Estimate Death Time",
        "\u26a0\ufe0f This tool estimates from empirical formulas and is strongly affected by individual variation and environmental factors. Results are for forensic teaching and preliminary reference only and cannot replace a professional forensic examination.",
        "Reference Basis",
        "Glaister Formula (simple estimation)",
        "Post-mortem interval (hours) = (37 - Tr) / 0.83",
        "Applicable to the early post-mortem period (within a few hours) as a rough estimate at an ambient temperature of about 18 to 20\u00b0C. Here 0.83 is the empirical cooling rate (\u00b0C/h).",
        "Henssge Nomogram Method (corrected formula)",
        "Post-mortem interval (hours) = (37.2 - Tr) / [K \u00d7 correction factor]",
        "Here K is the cooling constant, affected by body weight: K \u2248 0.4 \u00d7 (70/W)^0.5 (approximate), and the correction factor accounts for clothing and environment.",
        "The Henssge method gives a 95% confidence interval and applies to rectal temperatures of 10 to 37.2\u00b0C and ambient temperatures of \u221210 to +23\u00b0C.",
        "Relationship Between Corneal Clouding and Post-mortem Time",
        "About 1 to 2 hours after death",
        "Mild clouding",
        "About 3 to 6 hours after death, the cornea takes on a hazy appearance",
        "Moderate clouding",
        "About 7 to 12 hours after death, the pupil becomes visibly blurred",
        "Severe clouding",
        "More than about 15 to 24 hours after death, the cornea is completely opaque and greyish-white",
        "Note: corneal clouding is affected by ambient humidity and whether the eyelids are closed; clouding develops more slowly with closed eyelids.",
        "Body Cooling Trend",
        "The dashed line is the theoretical body cooling curve (ambient temperature",
        "\U0001F4DA In-Depth Analysis: Death Time Estimation by Body Cooling and Corneal Clouding",
        "Time of Death Inference in Early Cases",
        "Field Application of the Body Cooling Method",
        "Cross-validation by Corneal Clouding Grade",
        "By the simple Glaister formula, hours = (37 - rectal temperature)/0.83; by the Henssge correction, hours = (37.2 - rectal temperature)/(K \u00d7 correction), with K \u2248 0.4 \u00d7 sqrt(70/weight) and correction = clothing \u00d7 environment. A weighted combination of the two is used, cross-checked against the corneal clouding grade (0 to 4).",
        "With rectal temperature 32\u00b0C, ambient 20\u00b0C, weight 70 kg and clothing/environment factors of 1: Glaister = (37-32)/0.83 = 6.0 h and Henssge = (37.2-32)/(0.4\u00d71) = 13.0 h (95% interval about 10.2 to 15.8 h), giving a weighted combined estimate of about 10.6 h, that is more than 10 hours after death.",
        "Is the body cooling method reliable in low temperatures or in water?",
        "Not really. Low temperatures, immersion, febrile disease and heavy clothing all change the cooling curve significantly. The Henssge method applies corrections but remains approximate, so it should be combined with livor mortis, rigor mortis, stomach contents and other findings.",
        "Why cross-validate with multiple indicators?",
        "A single indicator carries large error (body temperature fluctuates with the environment, the cornea varies between individuals). Convergence of multiple indicators (body cooling, lividity, rigor, stomach contents and entomology) is what raises the reliability of the inference.",
        "About \"Death Time Estimator\"",
        "A forensic aid that estimates the post-mortem interval from body cooling formulas (the Glaister method and the Henssge nomogram method) together with the degree of corneal clouding.",
        "Supports the simple Glaister formula",
        "Supports the Henssge correction formula (including weight, clothing and environment corrections)",
        "Four-stage corneal clouding reference",
        "Visualization of the body cooling trend curve",
        "Provides a 95% confidence interval estimate",
        "Forensic Teaching and Study",
        "Preliminary time inference at the scene",
        "Forensic Pathology Case Discussion",
        "Judicial Appraisal Reference",
        "About \"Death Time Estimator (Body Cooling and Corneal Clouding)\"",
        "Death Time Estimator (Body Cooling and Corneal Clouding) - estimates the post-mortem interval from body cooling formulas and the degree of corneal clouding; a forensic aid for time of death inference. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))
    write('drowning-diatom', build('drowning-diatom', [
        "\U0001F50D Drowning (Diatom) Organ Detector",
        "Assist the drowning diagnosis from diatom detection in each internal organ",
        "/ Drowning Diatom Detector",
        "\U0001F4D6 Read the \"Guide to Inferring the Distribution of Diatoms in Internal Organs in Drowning\"",
        "Diatom Detection Data per Organ",
        "Diatom Concentration in the Water Body",
        "High concentration (nutrient-rich water)",
        "Medium concentration (ordinary natural water)",
        "Low concentration (clean water / tap water)",
        "Degree of Decomposition of the Body",
        "Fresh / slightly decomposed",
        "Moderately decomposed",
        "Highly decomposed / skeletonized",
        "Principles of the Diatom Test for Diagnosing Drowning",
        "Basic Principle",
        "During antemortem drowning the victim inhales a large amount of water, and the diatoms in it travel through the pulmonary circulation via the lungs into the left heart and then reach all internal organs (liver, kidney, spleen, bone marrow and so on) through the systemic circulation. Diatoms can therefore be detected in the organs of a drowned person.",
        "In post-mortem immersion (a body thrown into the water) there is no respiratory movement, so diatoms cannot enter the circulation and are not detected in the organs (or only a few in the lungs).",
        "Disruption Method",
        ": take organ tissue, destroy the organic matter with concentrated nitric acid or hydrogen peroxide, centrifuge to sediment, then examine for diatoms under the microscope",
        "Main Organs Tested",
        ": lung, liver, kidney, spleen and bone marrow (sampling closed organs rules out contamination)",
        "Control Water Sample",
        ": a water sample from the drowning point is needed as a reference for diatom species and counts",
        "Evaluation Standards for Diatom Test Results",
        "Test Result",
        "Diagnostic Meaning",
        "Diatoms detected in lung plus liver/kidney/spleen/bone marrow",
        "Supports a drowning diagnosis",
        "Diatoms detected only in the lungs",
        "Inconclusive (post-mortem immersion may yield a few diatoms in the lungs)",
        "Diatoms in lung plus liver/kidney with species matching the water sample",
        "Strongly supports drowning",
        "Diatoms detected in bone marrow",
        "Supports drowning (bone marrow is a closed organ, resistant to contamination)",
        "No diatoms detected in any organ",
        "Does not support drowning, or too few diatoms in the water",
        "Precautions for the Diatom Test",
        "The test must exclude laboratory contamination (prevent contamination throughout the procedure)",
        "Bone marrow and kidney are good samples (closed organs, less exposed to outside contamination)",
        "Diatom species must match the water sample from the drowning point to have diagnostic value",
        "The test still has some value on decomposed bodies (diatoms resist acid and decay)",
        "Organs of people who did not drown generally contain no diatoms (tap water has very few)",
        "Other Supporting Findings for Drowning",
        "External Findings",
        ": foam at the mouth and nose (mushroom-like foam), water plants or silt grasped in the hands, whitened sodden skin on the hands and feet (washerwoman's hand)",
        "Internal Findings",
        ": watery pulmonary oedema, Paltauf spots (subpleural haemorrhages), drowning fluid in the stomach",
        "Laboratory Tests",
        ": electrolyte differences between left and right cardiac blood (in freshwater drowning the left cardiac blood is diluted with lower sodium and chloride), haemoglobin dilution and so on",
        "\u26a0\ufe0f This tool is for forensic pathology teaching reference only. Diatom testing must be carried out in a professional laboratory under strict operating procedures.",
        "\U0001F4DA In-Depth Analysis: Inferring Diatom Distribution in Organs in Drowning",
        "Inferring the Route of Diatoms Through the Circulation",
        "Judging Immersion Mode and the Nature of the Water",
        "The Multi-organ Evidence Chain for Antemortem Drowning",
        "Following the lungs \u2192 left heart \u2192 systemic circulation route, compare where diatoms are found and in what quantity across the organs (lung, liver, kidney, spleen, bone marrow). Antemortem drowning shows whole-body distribution with species matching the scene water, whereas post-mortem immersion is limited to the respiratory tract.",
        "With diatoms in lung, liver, kidney and bone marrow and 3 species matching the water sample, counts decreasing along the circulation (lung > liver > kidney > bone marrow), this supports antemortem aspiration of water. If only the lungs are positive and downstream organs negative, this leans toward post-mortem immersion.",
        "Why does species consistency matter?",
        "If the diatom species in the organs differ from the scene water sample, this suggests drowning happened elsewhere or the specimen is contaminated; only consistent species supports reconstructing the scene as drowning in that water body.",
        "How does this differ from detector-10?",
        "Both belong to the diatom method. detector-10 focuses on organ positivity determination and scoring, while this tool focuses on mechanistic inference of the circulation route and distribution order; the conclusions should corroborate each other.",
        "About \"Drowning Diatom Detector\"",
        "Uses diatom counts in each internal organ (lung, liver, kidney, spleen, bone marrow) to assist the drowning diagnosis and evaluate the reliability of the test.",
        "Diatom Entry for Five Organs",
        "Automatic Drowning / Non-drowning Determination",
        "Water Concentration and Decomposition Corrections",
        "Bone Marrow Detection Highlighted",
        "Forensic Pathology Drowning Diagnosis Teaching",
        "Evaluating Diatom Test Results",
        "Reference for Cause of Death in Body Recovery Cases",
        "About \"Drowning (Diatom) Organ Detector\"",
        "Drowning (Diatom) Organ Detector - a forensic pathology tool for diagnosing drowning via diatom testing, evaluating diatom detection in each internal organ and assisting the drowning diagnosis. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()