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
    write('index', build('index', [
        "\u2696\ufe0f Forensic Medicine Tools",
        "Forensic Medicine",
        "Forensic Medicine Tools",
        "Estimate the post-mortem interval from body cooling formulas (Glaister/Henssge) combined with the degree of corneal clouding",
        "Enter the major and minor axes of a single spatter stain to compute the impact angle against the surface and infer the rough source location and spatter direction, helping reconstruct the wounding action and stain morphology.",
        "Enter diatom detection results for organs such as liver, kidney and lung, and apply the diatom test to judge whether the findings support a drowning diagnosis, helping distinguish drowning from post-mortem water immersion in body-recovery cases.",
        "Observe the timing of major ossification centres, epiphyseal fusion and the morphology of the pubic symphysis on X-ray, compare against standards to infer the biological age range, for forensic anthropological age estimation.",
        "Judge from radiographic features of fractures (fracture line sharpness, callus presence, soft tissue swelling) whether a fracture is recent (under 2 weeks) or old, helping infer when the injury occurred and sequence the case timeline.",
        "Enter STR allele data for a suspected father, mother and child to compute the paternity index (PI) and paternity probability, and to help interpret mixed stains alongside parentage results, for forensic DNA evidence analysis.",
        "Follow the sequence of screening test (acid phosphatase), confirmatory test (PSA/p30) and sperm microscopy to select and interpret results, helping identify semen stains and assess test reliability in sexual assault evidence examination.",
        "Compute burn area by the Chinese nine-rule method, grade burn depth by the three-degree four-degree method, and automatically classify severity (mild/moderate/severe/extremely severe) to assist emergency triage.",
        "Bloodstain examination workflow: screening test \u2192 confirmatory test \u2192 species identification \u2192 ABO blood typing, with the steps and how to interpret results",
        "Rigor mortis assessor. Rates each joint on a 0 to 4 scale and combines the order of onset (masseter \u2192 facial muscles \u2192 trunk \u2192 limbs) to infer the post-mortem interval, as a reference for forensic time-of-death estimation.",
        "Poison (toxin spectrum) rapid screener",
        "Enter poisoning symptoms, post-mortem findings and a suspected exposure history to quickly screen for possible toxin classes (ethanol, cyanide, carbon monoxide and so on), giving an initial direction for toxicology testing.",
        "Judge livor mortis staging (congestion, diffusion or fixation phase) from morphology and the blanching-on-pressure test result, helping infer the post-mortem interval as a forensic reference.",
        "Enter morphological features of an injury (epidermal abrasion, laceration and so on) to help distinguish blunt from sharp force injury and generate standardized injury description text for forensic examination records and reports.",
        "Identify human hair versus animal hair from microscopic morphology such as shaft diameter, medulla pattern and scale arrangement, and judge which body region the hair came from and whether it is damaged, for hair trace species identification.",
        "Use skin current mark morphology (greyish-white, dendritic pattern and so on) to help identify electrical injury and analyse the entry point, exit point and current pathway, for injury assessment in electrocution deaths.",
        "Enter the position, direction, depth and bleeding features of the ligature mark on the neck to analyse the pressure points and cord characteristics, helping distinguish hanging from ligature strangulation in hanging cases.",
        "Enter the injury distribution and impact site of a fall from height to analyse the pattern of minor external and severe internal injury and the fracture types, helping infer fall height, landing posture and injury mechanism to reconstruct a high-fall death.",
        "Enter which organs show diatom detection and how many, and combine this with the circulation pathway to judge whether diatoms entered the whole body with the inhaled water, assisting the drowning diagnosis and the determination of immersion mode.",
        "Identify typical fracture and burn patterns of child or elder abuse based on forensic features, assisting injury analysis in abuse cases and providing a reference for judicial appraisal.",
        "About \"Forensic Medicine Tools\"",
        "This Forensic Medicine Tools collection gathers 19 free online tools covering the common calculation, conversion and lookup needs of forensic medicine scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use practical utilities here. All tools run entirely in the browser, never upload data to a server, and protect your privacy.",
        "The forensic medicine tools included on this page include (a few representative ones):",
        "These tools help you finish common forensic medicine tasks quickly without memorizing complex formulas or converting by hand; enter the values and get the answer.",
        "Do the forensic medicine tools require a download or registration?",
        "No. All tools on this page are pure front-end online tools: open the page and use them directly. No software to install, no account to register, and no data is uploaded.",
        "Are the calculation results accurate, and is my data safe?",
        "Tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are immediate. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))
    write('detector-10', build('detector-10', [
        "\U0001F50D Drowning (Diatom) Organ Detection",
        "Enter diatom detection results for each internal organ and apply the diatom test to judge a drowning diagnosis",
        "\U0001F4D6 Read the \"Guide to Using the Drowning (Diatom) Organ Detection Decision\"",
        "The drowning diagnosis rests on diatom examination: during drowning, diatoms can enter the lungs, liver, kidney and bone marrow through the circulation, and the species found in each organ should match the water sample at the scene. Key decision points are a diatom load in the lungs significantly higher than in other organs, detection in at least 2 organs, species matching the water at the drowning site, and the diatom count reaching the threshold (commonly more than 20 per 10 g of tissue). Meeting several criteria supports drowning; detection only in the lungs suggests post-mortem immersion, so the case circumstances and autopsy must be judged together.",
        "Organ Tested",
        "Bone Marrow (long bone)",
        "Cardiac Blood",
        "Diatom Count (per 10g)",
        "Number of Diatom Species",
        "Diatom Species in Water (control)",
        "Acid Digestion Method",
        "Enzymatic Digestion Method",
        "Solvent Method",
        "Analysis Decision",
        "Record This Organ",
        "\U0001F4DA In-Depth Analysis: Drowning (Diatom) Organ Detection Decisions",
        "Distinguishing Drowning from Post-mortem Immersion",
        "Comparing Diatom Species with the Water Sample",
        "Assessing Diatom Distribution Across Organs",
        "Digest the liver, lung, kidney and bone marrow and examine them microscopically for diatoms. In antemortem drowning the inhaled water passes through the lungs into the systemic circulation, so diatoms are found in multiple organs (especially liver, kidney and bone marrow) with species consistent with the scene water sample. In post-mortem immersion, diatoms appear only locally in the lung or trachea and other organs test negative.",
        "Liver 15, lung 12 and kidney 8 all positive, with 3 species matching the water sample and bone marrow also positive, supports an antemortem drowning diagnosis. If only the lung is positive while liver, kidney and bone marrow are negative and species do not match, this leans toward post-mortem immersion.",
        "Can a negative diatom test rule out drowning?",
        "No. Few diatoms in clear water, decomposition and insufficient test sensitivity can all cause false negatives. Combine it with pulmonary oedema and blood-stained respiratory foam; a negative result does not absolutely exclude drowning.",
        "Why look at liver, kidney and bone marrow rather than only lung?",
        "The lung directly contacts the inhaled water and is prone to false positives, whereas diatoms in liver, kidney and bone marrow must travel through the systemic circulation, so a positive result is more specific for antemortem aspiration and is key to the multi-organ consistency judgement.",
        "The diatom test is an important method for the forensic drowning diagnosis, based on the principle that after antemortem aspiration of water the diatoms enter the systemic circulation through the lungs",
        "A large diatom load in the lungs (at least 10 per 10g) with at least 2 species supports a drowning diagnosis",
        "Finding diatoms in bone marrow is strong evidence of antemortem drowning, since post-mortem contamination cannot easily reach the marrow",
        "Diatom species should be compared with the suspected drowning water body; higher consistency means a more reliable diagnosis",
        "Decomposed bodies or highly decomposed tissue can affect the test; the acid digestion method must thoroughly break down organic matter",
        "About \"Drowning (Diatom) Organ Detection\"",
        "A forensic diatom detection analysis tool. Enter the diatom counts and species found in each organ to support a drowning diagnosis based on the principles of the diatom test.",
        "Multi-organ Diatom Detection Analysis",
        "Supports lung, liver, kidney, spleen and bone marrow",
        "Diatom Species and Water Body Match Rate Calculation",
        "Multi-organ Joint Recording",
        "Forensic Drowning Diagnosis",
        "Autopsy-Assisted Analysis",
        "Forensic Medicine Teaching Demo",
        "Judicial Appraisal Reference",
    ]))
    write('dna-str-typing', build('dna-str-typing', [
        "\U0001F4CA DNA (STR) Profile Analyzer",
        "Enter STR locus allele data for parentage analysis and mixed-stain interpretation",
        "/ DNA (STR) Profiling Analyzer",
        "\U0001F4D6 Read the \"Guide to DNA (STR) Profiling and Parentage Analysis\"",
        "Parentage Testing",
        "Mixed Stain Analysis",
        "STR Reference",
        "Enter STR allele data for a suspected father, mother and child to compute the paternity index (PI) and paternity probability",
        "Compute Paternity Index",
        "Enter the STR profile of a mixed stain and known individuals to determine the number of contributors",
        "Locus Selection",
        "Alleles Detected in the Mixed Stain (comma-separated)",
        "Alleles of Known Individual 1 (comma-separated)",
        "Alleles of Known Individual 2 (comma-separated)",
        "Analyze the Mixed Stain",
        "Common STR Loci (CODIS core loci)",
        "Locus",
        "Chromosomal Location",
        "Common Allele Range",
        "Mutation Rate",
        "X (female XX) / X,Y (male XY)",
        "Key Concepts",
        "Paternity Index (PI)",
        "PI = X / Y, where X is the probability that the suspected father is the biological father and Y is the probability that a random man is the biological father.",
        "PI > 1 supports parentage, while PI < 1 does not.",
        "Cumulative Paternity Index (CPI)",
        "CPI = the product of the PI across loci. CPI > 10000 usually establishes parentage (standard: CPI > 10000).",
        "Paternity Probability (W)",
        "W = CPI / (CPI + 1), the probability that the suspected father is the biological father.",
        "When the sample contains DNA from 2 or more individuals, a single locus in the STR profile can yield more than 2 alleles.",
        "A 2-person mixed stain yields at most 4 allele peaks per locus. Once one person's profile is known, the other can be inferred.",
        "\u26a0\ufe0f This tool uses a simplified model. Real examination requires validated population genetics frequency data and dedicated software.",
        "\U0001F4DA In-Depth Analysis: DNA (STR) Profiling and Parentage Analysis",
        "Parentage in Paternity Testing",
        "Index Calculation",
        "Distinguishing Mixed Stains from Single-Source Samples",
        "Comparing STR Profiles in Evidence",
        "Compute the paternity index PI per STR locus (PI = X/Y, with X the probability the suspected father is the biological father and Y the probability for a random man), the cumulative paternity index CPI as the product of the per-locus PI, and the paternity probability W = CPI/(CPI+1). A CPI > 10000 usually establishes parentage.",
        "CPI = 15000 across 15 autosomal STR loci: W = 15000/15001 = 99.99%, supporting the suspected father as the biological father. If at a locus the child carries a mandatory allele the father does not have, that locus gives PI \u2248 0 and parentage is excluded overall.",
        "Does CPI > 10000 guarantee establishment?",
        "It is a common threshold but not absolute. Close relatives, mutations (a mutation rate of about 0.1% to 0.2% can cause a single-locus mismatch), sample contamination and maternal mismatching must be ruled out and judged together with the case.",
        "How is the number of contributors to a mixed stain determined?",
        "Estimate the contributor count from the maximum allele count per locus (heterozygous peak area ratios), requiring balanced peak heights and no stutter interference. Complex mixtures need quantitative modelling and cannot rely on peak counts alone.",
        "About \"DNA (STR) Profiling Analyzer\"",
        "Enter STR locus allele data to compute the paternity index (PI), analyse the paternity probability (W) and determine the contributors to a mixed stain.",
        "Automatic PI/CPI Calculation for Parentage Testing",
        "Mixed Stain Contributor Analysis",
        "CODIS Core Locus Reference",
        "Built-in Allele Frequency Data",
        "Forensic Genetics Teaching",
        "Interpreting Parentage Results",
        "Mixed Stain Profile Analysis Reference",
        "About \"DNA (STR) Profile Analyzer\"",
        "DNA (STR) Profile Analyzer - a tool supporting forensic DNA evidence STR profile interpretation, allele reading, parentage analysis and mixed-stain determination. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()