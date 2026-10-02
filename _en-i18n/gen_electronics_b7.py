#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electronics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electronics')
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
    out = {'slug': slug, 'industry': 'electronics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
DISCL_E = " This is a basic electronics calculation aid; results are for circuit design and teaching reference only and do not replace formal PCB design, EMC and product reliability requirements."

def main():
    write('resistance-resistor', build('resistance-resistor', [
        "\u2699\uFE0F Resistor Colour Code Reader",
        "Choose 4 or 5 bands, then pick each band colour to get the resistance and tolerance automatically",
        "\U0001F4D6 See the \"Resistor Colour Code Reader User Guide\"",
        "Number of bands",
        "4-band",
        "5-band",
        "Band 1 (digit)",
        "Black (0)",
        "Brown (1)",
        "Red (2)",
        "Orange (3)",
        "Yellow (4)",
        "Green (5)",
        "Blue (6)",
        "Violet (7)",
        "Grey (8)",
        "White (9)",
        "Band 2 (digit)",
        "Band 3 (multiplier)",
        "Black \u00D71",
        "Brown \u00D710",
        "Red \u00D7100",
        "Orange \u00D71k",
        "Yellow \u00D710k",
        "Green \u00D7100k",
        "Blue \u00D71M",
        "Violet \u00D710M",
        "Grey \u00D7100M",
        "White \u00D71G",
        "Gold \u00D70.1",
        "Silver \u00D70.01",
        "Band 4 (tolerance)",
        "Brown \u00B11%",
        "Red \u00B12%",
        "Green \u00B10.5%",
        "Blue \u00B10.25%",
        "Violet \u00B10.1%",
        "Grey \u00B10.05%",
        "Gold \u00B15%",
        "Silver \u00B110%",
        "Band 3 (digit)",
        "Band 4 (multiplier)",
        "Band 5 (tolerance)",
        "\U0001F4A1 4-band: R=(band1\u00D710+band2)\u00D710^band3; 5-band: R=(band1\u00D7100+band2\u00D710+band3)\u00D710^band4; the last band is the tolerance",
        "Black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, grey 8, white 9",
        "Gold is \u00B15% and silver is \u00B110%",
        "Reading direction: the tolerance band is usually spaced further from the others",
        "\U0001F4DA In-depth analysis: Resistor Colour Code Reader",
        "4-band: brown black red gold = 1\u00D710\u00B2 \u00B15% = 1k\u03A9.",
        "5-band: yellow violet black brown brown = 470\u00D710\u00B9 \u00B11% = 4.7k\u03A9.",
        "1% precision resistors use 5 bands.",
        "Value to bands: 47k\u03A9 \u00B15% = yellow violet orange gold.",
        "4-band red red brown silver",
        "22\u00D710\u00B9=220\u03A9; tolerance \u00B110%.",
        "What does the 5th band on a 5-band resistor mean?",
        "A 5-band resistor is a 1%/2% precision part, with the first three bands as",
        "significant digits",
        " plus the multiplier and tolerance." + DISCL_E,
        "How are zero-ohm resistors marked?",
        "All four bands black (0\u00D710\u2070=0\u03A9); in practice they serve as jumpers or fuses." + DISCL_E,
        "Why do precision resistors use 5 bands?",
        "One extra significant digit gives a finer nominal value (for example the E96 series steps in 1% increments)." + DISCL_E,
        "About \"Resistor Colour Code Reading\"",
        "This tool supports 4-band and 5-band resistors and computes the nominal value and tolerance range from the band colours, an essential aid for engineers and hobbyists identifying resistors.",
        "4-band and 5-band switching",
        "Resistance and tolerance computed automatically",
        "Friendly value display (k\u03A9/M\u03A9)",
        "Resistor value identification",
        "Component sorting",
        "Teaching practice",
        "Troubleshooting",
        "Number of bands",
        "Band 1 (digit)",
        "Band 2 (digit)",
        "Band 3 (multiplier)",
        "Band 4 (tolerance)",
        "Band 3 (digit)",
        "Band 4 (multiplier)",
        "Band 5 (tolerance)",
    ]))


if __name__ == '__main__':
    main()
