#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'cleaning')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'cleaning')
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
    out = {'slug': slug, 'industry': 'cleaning', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('checker-9', build('checker-9', [
        "\u2705 Cleaning Process Standardization Assessment",
        "Self-check item by item across three modules - SOP standardisation, operation-spec execution, inspection-standard implementation - and auto-compute each module's completion rate and process standardization level.",
        "Process (Standardization / Operation / Inspection) Formulation",
        "/ Process (Standardization / Operation / Inspection) Formulation",
        "\U0001F4D6 View the User Guide for Cleaning Process Standardization Assessment",
        "Standardization level = total actual score / full marks x 100%",
        "Assess Standardization Level",
        "Score each item by completion: not formulated 0 / formulated but pending improvement 1 / formulated and executed 2",
        ">=90% complete, 75-89% basically complete, 60-74% needs improvement, <60% needs rebuilding",
        "This tool suits cleaning-service companies such as property cleaning, sanitation cleaning and industrial washing",
        "\U0001F4DA In-depth: Cleaning Process Standardization Assessment",
        "When introducing a standard operating procedure (SOP) to a new project, use this tool to check step by step whether the team operates per the spec.",
        "For quality audits or spot checks, sample on-duty staff's process compliance to find habitual violations.",
        "For new-employee onboarding training, use the 9-step checklist result to judge whether standard actions are mastered.",
        "Example: 9-Step Compliance Rate",
        "Prepare check, zone check, top-to-bottom check, dry-wet separation check, tool reset cross, process acceptance check, record cross, handover check, safety check - 7/9 hit, compliance about 78%, weak points are tool reset and record.",
        "What is the difference from checker-10?",
        "checker-10 checks the final cleaning quality result, this tool checks whether the work process is compliant; only together do you see both result and process.",
        "Can the 9 steps be added or removed?",
        "Yes. Different business types (e.g. hospital, food factory) can add/remove steps or add mandatory items via template config; you need not stick to a fixed 9 steps.",
        "Below what compliance rate should retraining occur?",
        "Suggest arranging retraining and follow-up below 85%; two consecutive failures should trigger re-assessment of job competency.",
        "About Cleaning Process Standardization Assessment",
        "A process-standardization assessment tool for cleaning-service companies, covering three modules - SOP standardisation, operation-spec execution, inspection-standard implementation - with 15 key points, quantifying process completeness.",
        "Checklist assessment across SOP / operation / inspection modules",
        "Per-module completion rate and overall standardization level",
        "Auto-identifies items pending improvement",
        "Cleaning-service company standardization build-out",
        "Property cleaning project process mapping",
        "Quality-management-system document preparation",
        "Cleaning team training and assessment",
    ]))
    write('cycle-20', build('cycle-20', [
        "\u23F1\uFE0F Carpet (Vacuum / Wash / Dry) Cycle",
        "Manage carpet vacuuming, deep washing and drying cycles. Recommend care frequency by carpet type and usage intensity, track each maintenance due date, with a common-stain treatment guide.",
        "\U0001F4D6 View the User Guide for Carpet (Vacuum / Wash / Dry) Cycle",
        "\u2795 Add Carpet",
        "Carpet Name / Location",
        "Carpet Type",
        "Wool Carpet",
        "Synthetic Carpet",
        "Cotton-Linen Carpet",
        "Silk / Blended",
        "Usage Intensity",
        "High (entry / living room / pets)",
        "Medium (bedroom / study)",
        "Low (guest room / decorative)",
        "\U0001F4CB Carpet Care Schedule",
        "No carpets yet, please add first",
        "Select Carpet",
        "Vacuum",
        "Deep Wash",
        "Dry / Ventilate",
        "Area (m2)",
        "\U0001F9EF Common Stain Treatment Guide",
        "Care frequency is auto-computed by carpet type and usage intensity; adjust by ambient dust in practice",
        "Wool and silk carpets avoid high-temperature washing and sun exposure; prefer professional dry cleaning or low-temperature spot cleaning",
        "After deep washing, dry thoroughly; damp carpets easily breed mould and odour",
        "When treating a stain, first blot liquid with a dry cloth, then wipe from the stain edge toward the centre to avoid spreading",
        "Tap \u2705 to quickly log today's maintenance and auto-update the next due date",
        "\U0001F4DA In-depth: Carpet (Vacuum / Wash / Dry) Cycle",
        "For home carpet daily care, set vacuum frequency by foot traffic to prevent sand from wearing the pile.",
        "Planned washing of hotel-room carpets balances guest experience with the cost of vacant rooms during drying.",
        "Pet-owning households set a higher-frequency local-cleaning rhythm for fur and urine stains.",
        "Example: Living-Room Carpet Care Cycle",
        "Daily vacuum twice a week, treat local stains like spills immediately, deep wash every 3-6 months; after washing, ventilate and dry about 24 hours before walking on it.",
        "How long to fully dry after deep washing?",
        "Well-ventilated about 24-48 hours, longer in humid seasons or thick-pile carpets; walking before fully dry leaves water marks and risks mould.",
        "Can a whole carpet be machine-washed?",
        "Small washable mats can go in a machine; large wall-to-wall carpets should be professionally extracted - machine washing easily shrinks, deforms and fails to fully dewater.",
        "How to treat pet urine stains?",
        "First blot with paper, then use an enzyme cleaner to break down protein and remove odour; avoid ammonia (smells like urine and may trigger re-marking), then dry thoroughly.",
        "About Carpet (Vacuum / Wash / Dry) Cycle",
        "A carpet care-cycle management tool. Supports adding multiple carpets and auto-recommending three care frequencies - vacuum, deep wash, dry/ventilate - by type (wool / synthetic / cotton-linen / silk) and usage intensity (high / medium / low), tracking each maintenance due date, logging details, with a guide to 8 common stains, helping homes and properties manage carpet care scientifically.",
        "Care plans for four carpet types",
        "Usage-intensity-adaptive frequency",
        "Tracking of three care due dates",
        "Stain treatment guide",
        "Multi-carpet management",
        "Home carpet daily care",
        "Hotel carpet maintenance scheduling",
        "Office carpet cleaning management",
        "Emergency stain handling",
        "e.g. living-room large carpet",
        "e.g. 8",
        "e.g. treated coffee stain, vacuumed 3 times",
    ]))
    write('dilution-ratio', build('dilution-ratio', [
        "\U0001F9EE Cleaner Dilution-Ratio Calculator",
        "Calculate the dilution ratio, concentrate volume and water volume for various cleaners",
        "Core formula (by input variables): (originalVol / totalVol x 100); originalVol x 1000; waterVol x 1000",
        "\U0001F4D6 View the User Guide for Cleaner Dilution-Ratio Calculator",
        "\U0001F4CB By Preset Use",
        "\u2699\uFE0F Custom Ratio",
        "Select Cleaning Use",
        "Dilution Ratio (1 : N)",
        "Total Diluted Volume Needed (L)",
        "Concentrate Concentration (%, optional)",
        "\U0001F4D6 Dilution-Ratio Reference",
        "Daily Floor Cleaning",
        ": 1:80-1:100, light-soil daily mopping",
        "Heavy-Soil Floor",
        ": 1:30-1:50, kitchen floor with heavier grease",
        "Carpet Washing",
        ": 1:20-1:40, with an extraction machine",
        "Glass Cleaning",
        ": 1:50-1:100, spray and wipe",
        "Restroom Disinfection",
        ": 1:100-1:200, 84-disinfectant type",
        "Tableware Soaking",
        ": 1:200-1:500, disinfectant soak",
        "\u2022 Dilution ratio means concentrate : water by volume; follow the product label",
        "\U0001F4DA In-depth: Cleaner Dilution-Ratio Calculator",
        "When a property team batches liquid, pick the ratio by zone soiling and compute each bucket's concentrate and water to keep concentration consistent.",
        "Housekeeping picks concentration by stain type: heavy grease uses a low ratio (e.g. 1:10), daily floor uses a high ratio (e.g. 1:100).",
        "Follow the disinfectant label ratio (e.g. 84 disinfectant 1:100) to ensure effective disinfection concentration without excessive irritation.",
        "Example: 84 Disinfectant 1:100 for 1 Litre",
        "Target 1 L, ratio 1:100, then concentrate about 10 mL, water about 990 mL; mix fresh and use within 24 hours, discard any leftover.",
        "Are dilution ratios the same across cleaners?",
        "No, you must follow the product label or MSDS; strong acids, strong alkalis and chlorine disinfectants each have safe concentrations - check the ingredients before mixing.",
        "Can acidic cleaner and chlorine cleaner be mixed?",
        "Never mix. Acid mixed with chlorine type (e.g. 84) releases chlorine gas, causing poisoning; use separately with a rinse interval.",
        "Does higher concentration mean stronger cleaning?",
        "No. Too high a concentration corrodes surfaces, leaves skin-irritating residue and wastes product; use the label-recommended ratio; for stubborn stains increase contact time rather than blindly concentrating.",
        "About Cleaner Dilution-Ratio Calculator",
        "Cleaner Dilution-Ratio Calculator supports preset-by-use or custom ratios, precisely computing concentrate and water volumes, with concentrate-concentration conversion.",
        "8 preset cleaning uses",
        "Supports custom dilution ratio",
        "Auto concentration conversion",
        "Cleaning-company cleaner mixing",
        "Home daily cleaning ratios",
        "Disinfectant dilution calculation",
        "Carpet / floor wash mixing",
    ]))

if __name__ == '__main__':
    main()
