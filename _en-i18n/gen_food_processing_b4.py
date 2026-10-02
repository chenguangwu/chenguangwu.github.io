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
    write('blanching-conditions', build('blanching-conditions', [
        "\U0001F321\uFE0F Blanching Time-Temperature (Enzyme Inactivation) Combiner",
        "Use thermal lethality kinetics to work out the temperature-time combination needed to inactivate the target enzyme",
        "Core formulas (by input): Tref - Z \u00D7 Math.log10(D_T \u00F7 Dref); Dref \u00D7 (10)^(Tref - T \u00F7 Z); 100 - (10)^-n",
        "Blanching Time-Temperature Combiner",
        " / Blanching Time and Temperature",
        "\U0001F4D6 See the \"Blanching Time-Temperature (Enzyme Inactivation) Combination User Guide\"",
        "Enzyme inactivation kinetics: the D value is the time needed at a given temperature for enzyme activity to fall by 90%; t = D_ref \u00D7 n \u00D7 10^((T_ref \u2212 T)/Z), where n is the log reduction (n=3 means 99.9% inactivation). Common indicator enzymes: peroxidase (heat resistant, used as the marker for adequate blanching) and polyphenol oxidase (related to browning). Blanching also inactivates enzymes, keeps colour, softens texture and removes pesticide residues.",
        "\U0001F4DA In-depth analysis: Blanching Time-Temperature (Enzyme Inactivation) Combination",
        "Blanching quick-frozen vegetables to inactivate enzymes and keep colour",
        "Peroxidase inactivation before canning",
        "Optimising the blanching intensity process window",
        "D value at that temperature D_T = D_ref \u00D7 10^((T_ref \u2212 T)/Z); the blanching time needed is t = D_T \u00D7 n (n being the log inactivation).",
        "Taking peroxidase with D_ref=0.5 min at 100\u00B0C, Z=10 and target inactivation n=3 (0.1% residual): at 95\u00B0C, D_T=0.5\u00D710^0.5\u22481.58 min, so t\u22484.74 min reaches 99.9% inactivation.",
        "What does Z represent?",
        "Z is the temperature change needed for a tenfold change in the D value (in \u00B0C); for most enzymes Z is about 8-12. The higher the temperature the smaller the D value and the faster the inactivation.",
        "How is n chosen?",
        "Routine blanching uses n=2-4 (99%-99.99% inactivation); leafy vegetables often use 3 to balance colour and texture.",
        "About \"Blanching Time-Temperature Combiner\"",
        "\uFE0F Blanching Time-Temperature (Enzyme Inactivation) Combiner. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('dough-absorption', build('dough-absorption', [
        "\U0001F9EE Dough Absorption Rate and Final Moisture Calculator",
        "Calculate dough absorption, total weight and final moisture from baker's percentages, with water-equivalent conversion for other liquids",
        " / Dough Absorption Calculation",
        "\U0001F4D6 See the \"Dough Absorption and Final Moisture User Guide\"",
        "Final dough moisture = total water in the dough \u00F7 total dough weight \u00D7 100%",
        "Flour moisture content (%)",
        "Water equivalent of other liquids (g)",
        "Weight of milk, egg and so on converted to water (milk at 87%, whole egg at 74%)",
        "Weight of other dry ingredients (g)",
        "Total weight of dry ingredients such as salt, sugar and yeast",
        "Mean moisture of other dry ingredients (%)",
        "Absorption rate (baker's percentage) = total water added \u00F7 flour weight \u00D7 100%. Final dough moisture = total water in the dough \u00F7 total dough weight \u00D7 100%. Staple bread dough is usually about 60-65% moisture, European bread 65-75% and sandwich toast 62-68%.",
        "\U0001F4DA In-depth analysis: Dough Absorption and Final Moisture",
        "Standardising absorption in baking formulas",
        "Converting water addition for steamed buns and bread",
        "Moisture compliance in finished products",
        "Absorption rate = total water added \u00F7 flour weight \u00D7 100%; total water in the dough = the flour's own water + added water + water in the dry ingredients; final moisture = total water \u00F7 total dough weight \u00D7 100%.",
        "Flour 1000g (13.5% moisture), 620g water added and 20g dry ingredients (2% moisture): absorption=620/1000\u00D7100%=62.0%; total water=135+620+0.4=755.4g, total dough weight 1640g, final moisture about 46.1%.",
        "Why does the absorption rate matter?",
        "It directly sets the water addition and the specific volume and texture of the finished product; the more protein and damaged starch in the flour, the higher the absorption, so calibrate against each flour type.",
        "How do I control the final moisture?",
        "Final moisture is set by total water over total weight, and the water carried by dry ingredients is easy to miss, so convert milk powder, sugar and other moist ingredients into the water count.",
        "About \"Dough Absorption and Final Moisture Calculator\"",
        "Dough absorption and final moisture calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('additive-limit-lookup', build('additive-limit-lookup', [
        "\U0001F4DA Food Additive Use Limits (GB 2760) Lookup",
        "Look up the maximum permitted use levels and applicable food categories of common food additives under the GB 2760 standard",
        "Additive Use Limits (GB2760) Lookup",
        " / Additive Limit Lookup",
        "\U0001F4D6 See the \"Maximum Use Levels of Food Additives (GB 2760) Lookup User Guide\"",
        "Maximum use levels of food additives are looked up in GB 2760 by food category and additive type: levels are expressed in g/kg or g/L; when several additives with the same function are used together, the sum of each one's share of its own maximum use level must not exceed 1, that is \u03A3(actual amount \u00F7 maximum amount) \u2264 1; residue limits are expressed in mg/kg and apply to processing aids and some bleaching agents; use outside the scope or above the limit is non-compliant.",
        "Search an additive / food category / function",
        "This tool includes typical limit data for some common additives and is for study reference only. In actual production follow the current text of GB 2760, and the carry-over principle and maximum use level rules.",
        "\U0001F4DA In-depth analysis: Maximum Use Levels of Food Additives (GB 2760) Lookup",
        "Checking compliant preservative levels in pastries",
        "Verifying colour fixative limits in cured meat products",
        "Assessing combined sweetener use in beverages",
        "Lookup rules",
        "GB 2760 matches on three dimensions: additive \u2192 food category \u2192 maximum use level; when several preservatives are combined, the sum of the shares of their maximum use levels must be at or below 1.",
        "Looking up sorbate potassium in pastries: the maximum use level is 1.0 g/kg; if dehydroacetic acid and its sodium salt are also used (0.5 g/kg in pastries), the sum of the two shares must stay at or below 1. For cured meat products, the sodium nitrite residue limit is 30 mg/kg or less with a maximum use level of 0.15 g/kg.",
        "What is the authoritative limit?",
        "The current GB 2760 and the National Health Commission announcements govern; this tool is an offline quick reference, and official labelling follows the standard text and the product execution standard.",
        "Can several preservatives be combined?",
        "Preservatives with the same function may be used together, but the sum of the shares of their maximum use levels must stay at or below 1 to avoid exceeding the total.",
        "About \"Additive Use Limits (GB2760) Lookup\"",
        "The Additive Use Limits (GB2760) lookup tool. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
        "e.g. preservatives, benzoic acid, beverages, antioxidants",
    ]))


if __name__ == '__main__':
    main()
