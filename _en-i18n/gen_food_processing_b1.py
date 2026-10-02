#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food-processing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food-processing')
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
    out = {'slug': slug, 'industry': 'food-processing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('ph-adjustment', build('ph-adjustment', [
        "\U0001F4D0 pH Adjustment (Acidulant) Dosage Calculator",
        "Calculate the amount of acidulant needed to bring a solution from its current pH to the target pH",
        "Core formulas (by input): (10)^ph1 - ag.pKa \u00F7 (1 + (10)^ph1 - ag.pKa); (10)^ph0 - ag.pKa \u00F7 (1 + (10)^ph0 - ag.pKa); molesNeeded \u00F7 conc \u00D7 1000",
        "pH Adjuster Dosage Calculator",
        " / pH Adjuster Dosage",
        "\U0001F4D6 See the \"pH Adjustment Dosage User Guide\"",
        "Adjuster type",
        "Citric acid (monoprotic weak acid, pKa1=3.13)",
        "Lactic acid (monoprotic weak acid, pKa=3.86)",
        "Acetic acid (monoprotic weak acid, pKa=4.76)",
        "Phosphoric acid (polyprotic acid, using pKa1=2.16)",
        "Hydrochloric acid (strong acid)",
        "Sodium hydroxide (strong base)",
        "Sodium carbonate (strong base salt, 2 equivalents)",
        "Adjuster concentration (mol/L)",
        "Common values: citric acid 1mol/L is about 192g/L, lactic acid 1mol/L about 90g/L, acetic acid 1mol/L about 60g/L",
        "The calculation approximates an unbuffered system: when acidifying, H\u207A to add = (10^\u2212pH target \u2212 10^\u2212pH current)\u00D7V; when alkalising, OH\u207B equivalents = (10^\u2212(14\u2212pH target) \u2212 10^\u2212(14\u2212pH current))\u00D7V. For weak acids the effective dissociation is estimated from pKa and the target pH with Henderson-Hasselbalch. Buffered systems need a titration to determine the true dosage.",
        "\U0001F4DA In-depth analysis: pH Adjustment (Acidulant) Dosage",
        "Acidulation blending of beverages",
        "Canning acidity working together with preservation",
        "Standardising sauce acidity",
        "H\u207A to add = (10^(minus pH target) \u2212 10^(minus pH initial)) \u00D7 volume; for weak acids the added amount is scaled by the dissociation \u03B1=10^(pH\u2212pKa)/(1+10^(pH\u2212pKa)) at the target pH.",
        "Bringing 10 L of water from pH 7.0 to pH 4.5 with citric acid (pKa1 about 3.13): dissociation at the target pH is about 96%, so H\u207A to add is about 3.15\u00D710\u207B\u2074 mol, needing about 3.3\u00D710\u207B\u2074 mol of citric acid, or roughly 0.063 g (approximate, correct for buffering).",
        "What if the system is buffered?",
        "Foods containing protein or organic acids buffer, so the real dosage is higher than a plain-water estimate; rely on the measured titration curve with a pH meter.",
        "Strong acid versus weak acid?",
        "A strong acid dissociates completely and is dosed on the H\u207A actually needed; a weak acid only partly dissociates, so the added amount must be scaled up by its dissociation at the target pH.",
        "About \"pH Adjuster Dosage Calculator\"",
        "pH adjustment (acidulant) dosage calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('sterilization-f-value', build('sterilization-f-value', [
        "\U0001F9EE Sterilisation F Value (D Value / Z Value) Calculator",
        "Compute the thermal lethality and F value, with D value / Z value conversion and the required sterilisation time",
        "Sterilisation F Value (D/Z Value) Calculator",
        " / Sterilisation F Value",
        "\U0001F4D6 See the \"Thermal Sterilisation F Value (D/Z Value) User Guide\"",
        "The sterilisation value is based on thermal lethality kinetics:",
        "D value",
        "is the time needed at a given temperature to destroy 90% of the microorganisms;",
        "Z value",
        "is the temperature rise needed for the D value to change tenfold (commonly 10\u00B0C for bacteria);",
        "F value",
        "is the equivalent sterilisation time (reference 121.1\u00B0C). Integral form",
        "The commercial sterility target F\u2080 is usually 3-12 min (depending on product and flora).",
        "Take Z as 10\u00B0C and D from the 121\u00B0C reference; acidic foods (low pH) need less.",
        "Results are for process estimation; the official sterilisation schedule follows experiments and regulations.",
        "\U0001F446 Choose a mode and enter the parameters",
        "F value: the lethality of thermal sterilisation at a given temperature, in min. Lethality L = 10^((T \u2212 Tref)/Z), F = L \u00D7 t. D value: the time to destroy 90% (one log) of the microorganisms. Z value: the temperature difference for a tenfold change in D value. Low-acid canned food usually uses F\u2080\u22653 min at 121.1\u00B0C as the safety reference.",
        "\U0001F4DA In-depth analysis: Thermal Sterilisation F Value (D/Z Value)",
        "Designing sterilisation schedules for low-acid canned food",
        "Equivalent conversion between sterilisation temperature and time",
        "Judging commercial sterility safety",
        "Lethality L = 10^((T \u2212 T_ref)/Z); F value = L \u00D7 t (equivalent sterilisation time at T_ref); working backwards, t = F_target \u00F7 L.",
        "At 121.1\u00B0C for 15 min (Z=10): L=1 and F\u2080=15 min, far above the 3 min safety reference; at only 110\u00B0C, L=10^((110\u2212121.1)/10)\u22480.0776, so reaching F\u2080=3 needs about 38.7 min.",
        "What does F\u2080\u22653 mean?",
        "It is equivalent to 3 min of lethality at 121.1\u00B0C, the routine commercial sterility reference for low-acid canned food (adjustable for the target flora).",
        "What Z value should I use?",
        "Common spoilage organisms give Z around 10\u00B0C; acidic foods need less, and the D/Z of the target organism should come from experiment.",
        "About \"Sterilisation F Value (D/Z Value) Calculator\"",
        "Sterilisation F value (D value / Z value) calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('water-activity', build('water-activity', [
        "\u2622\uFE0F Water Activity (Aw) and Microbial Growth Assessor",
        "Enter the water activity Aw to assess microbial growth risk and product stability",
        "Water Activity and Microbial Growth Assessor",
        " / Water Activity Assessment",
        "\U0001F4D6 See the \"Water Activity (Aw) and Microbial Risk User Guide\"",
        "Aw = water vapour pressure in the food / pure water vapour pressure",
        "Water activity Aw (0 - 1.0)",
        "Water activity Aw = water vapour pressure in the food divided by pure water vapour pressure, reflecting the water available to microorganisms. The lower the Aw the more stable the product. Most bacteria need Aw above 0.9, yeast above 0.85 and moulds above 0.7; halophiles above 0.75 and osmotolerant yeast above 0.62. Lowering Aw (drying, salting, sugaring) is a classic preservation method.",
        "\U0001F4DA In-depth analysis: Water Activity (Aw) and Microbial Risk",
        "Preservative and shelf-life design",
        "Microbial control in low-moisture products",
        "Rewetting and humectant formulation assessment",
        "Aw = water vapour pressure of the food divided by that of pure water (0-1); growth thresholds: most organisms do not grow below Aw 0.60, yeasts and moulds grow between 0.60 and 0.85, and bacteria above 0.85.",
        "Aw=0.85 sits at the lower limit for bacteria and in the easy range for yeasts and moulds, so it needs a lower Aw (dehydration, sugar or salt), preservatives or refrigeration; going below 0.85 noticeably inhibits bacteria.",
        "Is Aw the same as water content?",
        "No. Water content is absolute water, while Aw is the free water available to microorganisms and is affected by binding from sugars and salts.",
        "How do I lower Aw?",
        "Dehydrate, add sugar or salt to bind free water, use humectants (glycerol or sorbitol) and combine with preservatives and packaging.",
        "About \"Water Activity and Microbial Growth Assessor\"",
        "Water activity (Aw) and microbial growth assessor. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))


if __name__ == '__main__':
    main()
