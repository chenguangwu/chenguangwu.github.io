#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'beauty')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'beauty')
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
    out = {'slug': slug, 'industry': 'beauty', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3


def main():
    write('skincare-routine', build('skincare-routine', [
        "\U0001F4D0 Personalized skincare routine planner",
        "Build your own skincare routine from your skin type and age",
        "Skincare step planner",
        " / Skincare step planner",
        "Step one: test your skin type",
        "20-25 years",
        "25-30 years",
        "30-40 years",
        "Over 40",
        "Dry skin",
        "Prone to dryness and tightness",
        "Oily skin",
        "Oily with frequent breakouts",
        "Combination skin",
        "Oily T-zone, dry cheeks",
        "Sensitive skin",
        "Prone to redness and sensitivity",
        "\U0001F4D0 Generate the routine",
        "\U0001F4CB Your personalized routine",
        "\u2600\uFE0F Morning routine",
        "\U0001F319 Evening routine",
        "\U0001F4C5 Weekly care",
        "\U0001F4D6 Skincare order explained",
        "\u26A0\uFE0F Ingredient clash warnings",
        "\U0001F4CF Product amount reference",
        "\U0001F4CC Basic skincare principles",
        "Cleanser:",
        "Cleanse gently and avoid over-cleansing that damages the barrier",
        "Toner:",
        "Second cleansing, hydration, opens the absorption path",
        "Serum:",
        "Efficacy product, small molecules go on first",
        "Eye cream:",
        "Eye area skin is thin and needs dedicated care",
        "Lotion / cream:",
        "Hydrate and seal in the nutrients applied before",
        "Sunscreen:",
        "The last step of the day, the key to anti-aging",
        "\U0001F504 Order mnemonic",
        "Water \u2192 serum \u2192 eye \u2192 lotion \u2192 cream \u2192 sunscreen",
        "Go from thin to thick texture, and from small to large molecules. Apply water-based products first, then oil-based.",
        "\u274C Ingredients that should not be combined",
        "Acid + acid",
        "Salicylic acid + glycolic acid, salicylic acid + retinol = over-exfoliation and barrier damage",
        "Retinol + high-strength acid",
        "Retinol + glycolic or salicylic acid = double the irritation, easy redness and peeling",
        "Vitamin C + niacinamide",
        "High-strength L-ascorbic acid (pH below 3.5) + niacinamide may convert to niacin acid and irritate the skin",
        "Copper peptide + vitamin C",
        "Blue copper peptide is oxidised and inactivated when it meets vitamin C",
        "Protease + strong acid",
        "Enzymatic exfoliating ingredients are inactivated in a strong acid environment",
        "\u2705 Safe combinations:",
        " \u2022 Vitamin C in the morning, retinol at night (but build tolerance first)",
        " \u2022 Niacinamide + retinol (a classic pairing)",
        " \u2022 Ceramides + any ingredient (repair plus efficacy)",
        " \u2022 Hyaluronic acid + any ingredient (universally mixable hydrator)",
        "\U0001F4CF Standard amounts per product",
        "Product",
        "Visual reference",
        "From a soybean to a peanut-sized blob",
        "Soak a cotton pad or a one-yuan coin",
        "Serum",
        "2-3 drops, about soybean-sized",
        "Eye cream",
        "A rice-grain amount per eye",
        "Lotion",
        "1-2 soybean-sized blobs",
        "Cream",
        "Peanut-sized",
        "Sunscreen",
        "One-yuan-coin sized for the whole face",
        "\u26A0\uFE0F Too little product means wasted product, especially sunscreen: apply too little and you get no protection at all.",
        "\U0001F4DA In-depth analysis: personalized skincare routine planner",
        "Generate the step order from cleansing to sunscreen for your skin type and age.",
        "Too many skincare steps and you want to clarify the order and the pairing principles.",
        "An advisor gives the client a copyable daily routine.",
        "Dry skin morning and evening example",
        "For a 30-year-old with dry skin: morning lukewarm water cleanse, hydrating toner, serum (hyaluronic acid), cream, sunscreen; evening makeup removal, cleanse, toner, serum, eye cream, cream as a sealing layer. Principles: water-based before oil-based, small molecules before large ones, and sunscreen as the irreplaceable last daytime step.",
        "Can serum and cream be swapped?",
        "Not recommended. Small-molecule serum penetrates first and large-molecule cream locks water in afterwards; cream before serum blocks absorption, and the cream's oils also block water-soluble ingredients.",
        "Is more always better when it comes to steps?",
        "No. More steps stack irritation and raise cost. Start from cleanse, hydrate and sunscreen, then add one or two efficacy serums to suit your needs; sensitive skin is safer going minimal.",
        "About the Skincare step planner",
        "Skincare step planner. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))


if __name__ == '__main__':
    main()
