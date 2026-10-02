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
    write('makeup-shade', build('makeup-shade', [
        "\U0001F3A8 Smart lipstick shade recommendation",
        "Recommend the most flattering lipstick shade for your skin tone and the occasion",
        "Lipstick shade selector",
        " / Lipstick shade selector",
        "Step one: choose your skin tone",
        "Cool skin",
        "Veins lean blue-purple",
        "Neutral skin",
        "Veins show both blue and green",
        "Warm skin",
        "Veins lean green",
        "Step two: choose the occasion",
        "\u2600\uFE0F Daily commute",
        "\U0001F4BC Office work",
        "\U0001F495 Date night",
        "\U0001F389 Party and gala",
        "\U0001F48B Bold makeup look",
        "Filter by colour family",
        "\u2728 Start recommendation",
        "\U0001F4BE Save selection",
        "\U0001F3AF Recommended for you",
        "Choose a skin tone and an occasion first, then click \"Start recommendation\"",
        "\U0001F4A1 Swatch tips",
        "\U0001F4CA Colour family chart",
        "\U0001F3A8 How do I determine my skin tone?",
        "Vein check:",
        "Look at the veins on the inside of your wrist in natural light: blue-purple means cool skin, green means warm skin, and both means neutral skin.",
        "Jewellery test:",
        "If silver suits you, you have cool skin; if gold suits you, you have warm skin; if both suit you, you have neutral skin.",
        "Tanning reaction:",
        "Burning easily means cool skin, tanning easily means warm skin",
        "White paper comparison:",
        "Compare bare skin against white paper: pink-leaning skin is cool, yellow-leaning skin is warm",
        "\U0001F48B In-store swatch tips",
        "Skip makeup before swatching so the lips stay in their natural state",
        "Swatch on the lip-to-skin junction rather than the back of the hand",
        "Judge the colour in natural light, since shop lighting shifts it",
        "Try no more than three colours at a time to avoid visual fatigue",
        "After trying, walk around for 15 minutes to see the shade after it oxidises",
        "\U0001F4F1 Online swatch notes",
        "Watch for screen colour differences, since every phone displays differently",
        "Look at customer photos and real swatch images",
        "Check swatches from creators with a similar skin tone",
        "Remember that lip base products affect the final result",
        "\u26A0\uFE0F This tool is for reference only. Everyone's natural lip colour and lip condition differ, so the result on your lips may vary. Try before you buy.",
        "\U0001F308 Lipstick colour family chart",
        "Colour family",
        "Suitable skin tones",
        "Representative shades",
        "True red",
        "Commanding presence, classic and versatile",
        "All skin tones",
        "Dior 999, MAC Ruby Woo",
        "Rose red",
        "Cool and bright, very feminine",
        "Cool and neutral skin",
        "YSL Rouge Pur Couture No.1, MAC Girl About Town",
        "Mulberry",
        "Mature and regal, full presence",
        "Cool skin, fair skin",
        "MAC Diva, Chanel 58",
        "Orange red",
        "Energetic and lively, youthful and playful",
        "Warm skin, yellow skin",
        "MAC Lady Danger, Armani 405",
        "Pumpkin",
        "Soft and vintage, an autumn and winter essential",
        "Warm and neutral skin",
        "MAC Chili, Estee Lauder 333",
        "Earthy nude",
        "Sophisticated, Western editorial look",
        "Warm skin, healthy skin tone",
        "MAC Mocha, Armani 200",
        "Bean paste",
        "Gentle and everyday, never goes wrong",
        "Estee Lauder 420, MAC Brick-o-la",
        "Coral",
        "Youthful and fresh, natural",
        "Fair and neutral skin",
        "YSL Rouge Pur Couture 12, MAC See Sheer",
        "Strawberry red",
        "Sweet and cute, brightening and lifting",
        "Cool and fair skin",
        "MAC Cockney, Givenchy 333",
        "Berry",
        "Mysterious and cool, rich for autumn and winter",
        "MAC Rebel, YSL Black Rouge 409",
        "\U0001F4DA In-depth analysis: smart lipstick shade recommendation",
        "Unsure which red suits a cool or warm skin tone.",
        "You want different brightening shades for daily commuting versus an evening gala.",
        "A beauty counter associate quickly narrows candidate shades from the client's skin and lip colour.",
        "Cool/warm shade selection example",
        "With a cool skin tone and light natural lip colour, a cool blue-red (such as true red or berry) brightens the complexion. A warm yellow skin tone looks more harmonious in orange or brick red. On the occasion dimension, commuting takes low-saturation bean paste while a gala takes high-saturation true red.",
        "Can yellow skin never wear pink?",
        "Not necessarily. Cool yellow skin (olive skin) can carry cool rose tones, while warm yellow skin in neon pink can make teeth look yellow. The key is cool versus warm tone, not simply \"yellow\".",
        "What is the most accurate way to swatch?",
        "Apply to the fingertips or the lower lip and avoid the wrist, then judge in natural light by how the shade blends with your skin, so counter warm lighting does not mislead you.",
        "About the Lipstick shade selector",
        "Lipstick shade selector. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))

    write('nail-color-harmony', build('nail-color-harmony', [
        "\U0001F3A8 Nail colour pairing score",
        "Pick two nail polish colours and rate how well they pair using colour theory",
        "Compute the angular difference between the two hues on the colour wheel: within 30 degrees is analogous (harmonious), a complementary 180 degrees is high contrast, and a triadic 120 degrees is balanced. The score also factors in lightness difference, so it reflects coordination rather than absolute good or bad.",
        "Colour A",
        "Colour B",
        "\U0001F3A8 Score",
        "\U0001F3B2 Random pairing",
        "\U0001F4CA Pairing score",
        "\U0001F4DA In-depth analysis: nail colour pairing score",
        "Pick two polish colours and wonder whether they go together.",
        "Preview the harmony before doing a gradient or a bold contrast look.",
        "A nail artist explains colour theory to clients to make the recommendation more convincing.",
        "Hue difference harmony example",
        "Take the hue wheel angle difference between the two colours: within 30 degrees (analogous) scores 90, a complementary 180 degrees (such as red with green) scores 60, and a triadic 120 degrees scores 75. Here blue (220 degrees) with light purple (280 degrees) gives \u0394h = 60 degrees, an analogous coordination scoring 85.",
        "Are complementary colours always bad looking?",
        "Not necessarily. Complementary pairs are high contrast and eye-catching, which suits a bold colour-block look. The harmony score is low but the design impact is strong, and reducing the lightness difference or adding a transition colour makes it easier to wear.",
        "How do I quickly judge whether two colours pair?",
        "Use the colour wheel: adjacent hues (analogous) are the steadiest, same-family colours are the safest and complements are the boldest. Then consider lightness \u2014 a very wide light-to-dark gap can look jarring.",
        "About the Nail colour pairing score",
        "Nail colour pairing score is an online tool for everyday life. An everyday-life utility, close to daily needs, practical and convenient.",
    ]))

    write('perming-rod', build('perming-rod', [
        "\U0001F3CB\uFE0F Perm rod size chart",
        "Rod diameter versus curl result, so you can pick the right rod for the curl you want",
        "Perm rod size chart",
        " / Perm rod size chart",
        "Curl size correlates positively with rod diameter: a 14 mm rod gives tight curls, a 22 mm rod gives natural waves, and a 30 mm rod gives lazy large curls. The hair must be long enough to wrap the rod (at least 1.5 turns) to hold a curl, which limits short hair from achieving large curls.",
        "Choose your target curl",
        "Show all",
        "Tight small curls",
        "Medium curl",
        "Natural large curl",
        "Soft curl / wave",
        "\U0001F4CB Rod chart",
        "\U0001F4DA In-depth analysis: perm rod size chart",
        "Wondering whether to go for large curls or small curls? Check what each rod diameter delivers.",
        "Short hair is afraid of curls that are too tight, so choose a larger rod to control the arc.",
        "A stylist picks the rod from the client's hair length and desired curl.",
        "Rod diameter and curl example",
        "Curl size correlates positively with rod diameter: a 14 mm rod gives tight small curls, a 22 mm rod gives natural waves, and a 30 mm rod gives lazy large curls. For 15 cm of hair, a 19 mm rod gives medium curls; hair shorter than 8 cm struggles with a large rod and loosens easily.",
        "Why can't short hair be permed into large curls?",
        "The strand does not wrap the rod enough (fewer than 1.5 turns), so elasticity is poor after setting and the hair springs straight. Short hair is limited by length, and a large rod needs enough length to wind around it.",
        "Does rod diameter affect how long the perm lasts?",
        "Yes. Small curls hold a stronger shape, look more defined and tend to last longer. Large curls loosen with washing and care, so pair them with styling products.",
        "About the Perm rod size chart",
        "Perm rod size chart is an online tool for everyday life. An everyday-life utility, close to daily needs, practical and convenient.",
    ]))


if __name__ == '__main__':
    main()
