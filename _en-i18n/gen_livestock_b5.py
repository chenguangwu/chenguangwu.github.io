#!/usr/bin/env python3
# gen_livestock_head.py — shared head for livestock batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'livestock')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'livestock')
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
    out = {'slug': slug, 'industry': 'livestock', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('silage-density-ph', build('silage-density-ph', [
        "Silage compaction density and pH analyzer",
        "Assess silage compaction density, dry matter and pH to judge silage quality",
        "Assess silage compaction density, dry matter and pH to judge silage quality, and output results from inputs.",
        'View "Silage compaction density and pH analyzer" guide',
        "Compaction density analysis",
        "pH quality evaluation",
        "Silo length (m)",
        "Silo width (m)",
        "Silo height (m)",
        "Total fresh weight (t)",
        "Dry matter (%)",
        "Silage type",
        "Corn silage",
        "Forage silage",
        "Legume silage",
        "Sorghum silage",
        "Straw silage",
        "Measured pH",
        "Odor score (1\u20135)",
        "Silage quality reference standard",
        "Compaction density reference",
        "\u2022 Excellent: \u2265240 kg dry matter/m\u00b3 (fresh ~700 kg/m\u00b3)",
        "\u2022 Good: 200\u2013240 kg dry matter/m\u00b3",
        "\u2022 Fair: 160\u2013200 kg dry matter/m\u00b3",
        "\u2022 Low: <160 kg dry matter/m\u00b3 (poor fermentation)",
        "pH quality grading",
        "\u2022 Excellent: pH \u2264 4.0 (corn/sorghum), \u2264 4.5 (forage)",
        "\u2022 Good: 4.0\u20134.3 (corn), 4.5\u20134.8 (forage)",
        "\u2022 Fair: 4.3\u20134.8 (corn), 4.8\u20135.2 (forage)",
        "\u2022 Poor: pH > 4.8 (corn), > 5.2 (forage)",
        "Insufficient density leaves too much air, causing aerobic spoilage and mold. pH is the core fermentation metric; too low aids preservation, too high invites decay.",
        "Deep dive: Silage density and quality scoring",
        "From silo size and weight compute fresh / dry-matter density.",
        "Weighted score of pH, dry matter and odor.",
        "Silage fermentation quality judgment.",
        "Silo 10\u00d74\u00d73, weight 80 t, DM 30%",
        "Volume 120 m\u00b3, fresh density=80\u00d71000/120=667 kg/m\u00b3, dry-matter density=667\u00d730%=200 kg/m\u00b3.",
        "pH score",
        "Corn silage excellent pH<3.8; score drops as pH rises (weight 0.6).",
        "How high a density?",
        "Higher density excludes oxygen and ferments better; corn silage fresh density should be \u2265700 kg/m\u00b3.",
        "What is the score made of?",
        "pH 0.6 + dry matter 0.2 + odor 0.2 weighted; excellent \u226585.",
        'About "Silage compaction density and pH analyzer"',
        "Silage compaction density and pH analyzer. " + DISCL,
    ]))
    write('stats-7', build('stats-7', [
        "Calving (dystocia rate) statistics",
        "Dystocia rate",
        "Summarize the numbers of normal, lightly-assisted and difficult (heavily-assisted/C-section) calvings to compute dystocia and assistance rates, and grade the herd by experience ranges. Data is processed only locally in your browser, never uploaded.",
        'View "Calving (dystocia rate) statistics" guide',
        "Dystocia rate = difficult calvings \u00f7 total calvings \u00d7 100%",
        "Assistance rate = (lightly-assisted + difficult) \u00f7 total calvings \u00d7 100%",
        "Summarize normal, lightly-assisted and difficult (heavily-assisted or C-section) calvings to compute dystocia and assistance rates, grading by experience ranges. All data is processed only locally, not uploaded.",
        "Total calvings (head)",
        "Lightly-assisted (head)",
        "Difficult calvings (head)",
        "Deep dive: Calving dystocia-rate statistics",
        "Summarize a lactation or year's normal, lightly-assisted and difficult counts to compute dystocia and assistance rates.",
        "Compare heifers vs cows, different houses or sire offspring assistance ratios.",
        "When dystocia exceeds the range, trace calf birth weight, sire choice and calving procedure.",
        "Annual calving summary",
        "A farm calves 240/year: 200 normal, 26 light-assisted, 14 difficult \u2192 dystocia 14\u00f7240=5.83%, assistance (26+14)\u00f7240=16.67%, normal 83.33%, rated 'watch'.",
        "Investigating a high heifer rate",
        "Heifers 120 with 18 difficult = 15.00%, rated 'high'. Common causes are large birth weight and under-developed pelvis; first check the sire's calving-ease index, then whether assistance was too early.",
        "Does light assistance count in the dystocia rate?",
        "No. This tool separates the three: dystocia rate counts only heavily-assisted or C-section; assistance rate also includes light-assisted, for cross-farm comparison.",
        "What is the rating-range basis?",
        "Common cattle experience ranges: dystocia <3% good, 3%\u20138% watch, >8% high. Adjust by breed, parity and season; long-run <1% may mean a loose definition.",
        "What if the counts are inconsistent?",
        "When light-assisted + difficult exceeds total calvings, the tool prompts to re-check entry and gives no ratio, avoiding an over-100% error.",
        'About "Calving (dystocia rate) statistics"',
        "Calving (dystocia rate) statistics. " + DISCL,
    ]))
    write('vaccine-schedule', build('vaccine-schedule', [
        "Vaccine immunization-schedule generator",
        "Pick animal type to generate a standard vaccine program with age, vaccine name, route and dose",
        'View "Vaccine immunization-schedule generator" guide',
        "Show planned vaccination dates",
        "Vaccination precautions",
        "Before vaccination",
        "\u2022 Confirm animal health; delay if sick or stressed",
        "\u2022 Check vaccine lot, expiry and storage",
        "\u2022 Avoid antibiotics 2 days prior (live vaccines)",
        "After vaccination",
        "\u2022 Watch for anaphylaxis; keep epinephrine ready",
        "\u2022 Record name, lot, date and dose",
        "\u2022 Test antibody 7\u201314 days later to assess effect",
        "This is a general reference; the real program should follow local disease, maternal-antibody levels and veterinary guidance. Regions and farms may need adjustment.",
        "Deep dive: Immunization-schedule derivation",
        "By animal and birth date derive each vaccine's age and date.",
        "Standard pig/poultry/cattle/sheep programs.",
        "Mark routes (IM / drinking water / eye-drop).",
        "Piglet",
        "Born 2026-01-01: day-7 mycoplasma (1/8 IM), day-21 classical swine fever (1/22 IM) dated by age.",
        "Day-1 Marek's, day-14 Newcastle dated forward from birth.",
        "Can the program change?",
        "Must adjust to farm disease and regulations; this tool gives the standard reference.",
        "Route differences?",
        "Live vaccines often drinking/eye-drop, inactivated mostly IM; follow instructions.",
        'About "Vaccine immunization-schedule generator"',
        "The Vaccine immunization-schedule generator is a general-purpose online tool. " + DISCL,
    ]))
    write('water-feed-ratio', build('water-feed-ratio', [
        "Water-intake and feed-intake ratio monitor",
        "Monitor the water-to-feed ratio to assess normal drinking and warn of health or environment anomalies",
        "Core formula (by inputs): (|(tempCorrection)| \u00d7 |(tempDelta)| \u00d7 100); temp - 20",
        'View "Water-intake and feed-intake ratio monitor" guide',
        "Duck",
        "Daily water intake (L/head\u00b7day)",
        "Daily feed intake (kg/head\u00b7day)",
        "Normal water-feed ratio reference by animal",
        "Normal water-feed ratio",
        "Each 1\u00b0C rise adds about 6%",
        "Pig (lactating sow)",
        "Insufficient water hurts lactation",
        "Chicken (laying)",
        "Can reach 4:1 in heat",
        "Chicken (broiler)",
        "Varies with age",
        "Cattle (dairy)",
        "High-yield cows drink more",
        "Stronger drought tolerance",
        "Playing in water needs extra",
        "A sudden rise may signal heat stress, excess salt or disease (fever, diarrhea); a sudden drop may signal water-system failure, water quality or appetite loss. Record daily.",
        "Deep dive: Water-feed ratio",
        "From water and feed intake compute the ratio.",
        "Temperature-corrected recommended ratio range.",
        "Shortage/stress warning.",
        "Pig water 4 L, feed 2 kg, temp 25\u00b0C",
        "Ratio=2:1; 5\u00b0C rise correction 1+0.03\u00d75=1.15, recommended lower bound up ~15%.",
        "At 35\u00b0C the factor 1.45; ratio demand rises sharply.",
        "What is the normal range?",
        "Pig ~2\u20133:1, poultry ~1.8\u20132.5:1 (by dry feed), varying with temperature.",
        "Temperature effect?",
        "Each 1\u00b0C rise adds about 3%\u20136% water demand; ensure supply in heat.",
        'About "Water-intake and feed-intake ratio monitor"',
        "Water-intake and feed-intake ratio monitor. " + DISCL,
    ]))
    write('weaning-weight-survival', build('weaning-weight-survival', [
        "Piglet weaning weight and survival analyzer",
        "Analyze piglet weaning weight, survival, litter weight and pass rate to assess lactation management",
        "Core formula (by inputs): (avgW - 1.4) \u00f7 day \u00d7 1000; qualified \u00f7 weaned \u00d7 100; below \u00f7 weaned \u00d7 100",
        'View "Piglet weaning weight and survival analyzer" guide',
        "Born alive (head)",
        "Weaned alive (head)",
        "Weaning age (days)",
        "Average weaning weight (kg/head)",
        "Qualified weaning-weight standard (kg)",
        "Below-standard count (head)",
        "Weaning-weight reference (28 days)",
        "\u2022 Excellent: \u2265 8.0 kg/head",
        "\u2022 Good: 7.0\u20138.0 kg/head",
        "\u2022 Fair: 6.0\u20137.0 kg/head",
        "\u2022 Low: < 6.0 kg/head (strengthen lactation management)",
        "Nursing piglet survival reference",
        "\u2022 Excellent: \u2265 92%",
        "\u2022 Good: 88%\u201392%",
        "\u2022 Fair: 82%\u201388%",
        "\u2022 Low: < 82% (check crushing, diarrhea, etc.)",
        "Weaning weight directly affects finishing performance. Studies show each 1 kg higher weaning weight advances market by 5\u20137 days. Focus on colostrum, sow milking and warmth.",
        "Deep dive: Weaning weight and survival",
        "From born-alive/weaned-alive compute survival and litter weight.",
        "Daily gain and pass-rate assessment.",
        "Locate lactation-management problems.",
        "12 born, 11 weaned, 28 days",
        "Survival=11/12\u00d7100=91.7%; litter weight=11\u00d77.5=82.5 kg; daily gain=(7.5\u22121.4)/28\u00d71000=218 g/d; qualified 10 head (90.9%).",
        "Survival low",
        "Survival <85% hints nursing death or crushing; check management.",
        "What is normal survival?",
        "Good groups \u226590% at weaning; below hurts annual output.",
        "Daily gain?",
        "Born ~1.4 kg, reaching 7\u20138 kg at 28 days is normal; low means check milk.",
        'About "Piglet weaning weight and survival analyzer"',
        "Piglet weaning weight and survival analyzer. " + DISCL,
    ]))

if __name__ == "__main__":
    main()
