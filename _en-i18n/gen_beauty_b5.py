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
    write('hair-color', build('hair-color', [
        "\U0001F3A8 Smart hair colour recommendation",
        "Recommend hair shades that suit your skin tone and natural hair colour",
        "Hair colour selector",
        " / Hair colour selector",
        "Choose your skin tone",
        "\U0001F499 Cool fair skin",
        "\U0001F49B Warm yellow skin",
        "\U0001F49A Natural skin tone",
        "\U0001F90E Healthy deep skin",
        "Current natural hair colour",
        "Has it been bleached?",
        "Target bleach level",
        "No bleaching (natural hair)",
        "Level 6 (deep gold)",
        "Level 7 (gold)",
        "Level 8 (light gold)",
        "Level 9 (very light gold)",
        "Level 10 (platinum)",
        "Short hair (above the ear)",
        "Medium hair (below the shoulder)",
        "Long hair (below the chest)",
        "Bleach level reference",
        "\u2728 Recommended hair colours",
        "\U0001F487 Colour cream amount",
        "Extra-long hair (below the waist)",
        "Hair volume",
        "Thin hair",
        "Normal hair volume",
        "Thick hair",
        "Suggested colour cream amount",
        "\U0001F308 Recommended hair colours",
        "Click \"Recommended hair colours\" to see suggestions",
        "\u23F3 Fading process",
        "\U0001F4A1 Hair dyeing advice",
        "Reference fading process for common hair colours",
        "Click a swatch to see how that colour fades",
        "\u26A0\uFE0F Fading speed varies with hair condition and wash habits. Colour-protecting shampoo and avoiding hot water slow it down.",
        "\U0001F3AF Skin tone and hair colour pairing guide",
        "Skin tone",
        "Recommended hair colours",
        "Colours to avoid",
        "Cool fair skin",
        "Smoky grey, blue-black, purple-grey, rose gold, milky tea grey",
        "Orange, golden yellow (dull the complexion)",
        "Warm yellow skin",
        "Black tea, caramel, warm brown, dirty orange, honey tea",
        "Yellow, light gold (bring out sallowness)",
        "Natural skin tone",
        "Brown, chestnut, chocolate, deep gold",
        "Very cool tones, very warm tones",
        "Healthy deep skin",
        "Deep brown, wine red, ink green, blue-black",
        "Light yellow, neon colours (look dull)",
        "\u26A0\uFE0F Hair dyeing precautions",
        "Patch-test for skin allergy 48 hours before dyeing",
        "Do not wash your hair before dyeing \u2014 scalp oil protects it",
        "For bleaching, see a professional colourist to avoid breakage",
        "Leave at least 3 months between two dyeing sessions",
        "Wait 48 hours before washing, and use colour-protecting products",
        "Pregnancy and broken scalp are not suitable for dyeing",
        "\U0001F4DA In-depth analysis: smart hair colour recommendation",
        "You want to dye your hair but are unsure which colour suits your skin tone.",
        "You want to anticipate the final tone after fading so it does not disappoint.",
        "A stylist picks the colour cream number from the client's cool or warm tone and natural hair colour.",
        "Cool/warm tone selection example",
        "With a cool skin tone (veins leaning blue) and natural hair at level 5 (dark brown), a cool colour family suits (such as cool brown or cool tea); a target level 7 needs two levels of lifting. Warm skin tones look better in warm chestnut and honey tea, while cool grey can make you look haggard.",
        "How do I judge cool or warm before dyeing?",
        "The white paper test: hold white paper beside your face in natural light. Skin that reads pink or blue is cool; yellow or golden is warm. You can also notice whether cool grey or warm beige clothes flatter you more.",
        "Why does the colour fade toward yellow?",
        "Artificial pigment molecules are small and easily oxidised away, so the remaining base tone is usually yellow-orange. Refreshing with a colour cream of the same tone slows the shift, and the more times you bleach, the more noticeable the fade.",
        "About the Hair colour selector",
        "Hair colour selector. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))

    write('index', build('index', [
        "\U0001F484 Beauty and skincare tools",
        "Beauty and skincare",
        "Beauty and skincare tools",
        "Skin age test",
        "A skin age tester that assesses your skin's true age through a multi-dimensional questionnaire and gives care suggestions to support a personalized skincare plan.",
        "Hair dye mixing ratio",
        "A hair dye mixing ratio calculator that computes the ratio from developer strength and colour cream, so you can mix precisely and avoid a colour mismatch.",
        "Enter your face shape features to get matching hair outlines and cutting notes, helping you pick a style that makes the face look smaller and more balanced based on facial proportions.",
        "Enter your skin type and goal to generate matching skincare products, technique steps and care-cycle suggestions, ready to copy as your daily routine.",
        "A skin type tester that identifies dry, oily, combination and other types through a short questionnaire and gives basic skincare advice to help you pick products.",
        "A foundation shade matcher that recommends shades and selection tips from your skin depth and undertone, making the base look more natural.",
        "Hair colour selector",
        "Enter your skin tone and natural hair colour to get matching hair colour recommendations and a fading preview, helping you choose a shade that flatters you before dyeing.",
        "A nail colour pairing scorer that assesses how well two nail polish colours work together using colour theory, to help with manicure colour schemes.",
        "Score cosmetics across three dimensions (compliance safety, durability stability and visual appearance) with 40%/30%/30% weights, outputting a composite quality rating with improvement suggestions.",
        "Score cosmetics item by item across four dimensions (sensory, physicochemical, microbiological and packaging labelling), outputting a weighted composite score, per-dimension ratings and improvement suggestions.",
        "A cosmetic compliance risk evaluator that checks each regulatory requirement item by item, automatically computing scores and risk levels to support filing self-checks.",
        "A PDCA-based cosmetic quality check-assess-improve mechanism that outputs per-stage maturity and improvement paths",
        "Enter your base colour, main nail polish colour and optional accent, then check and score the scheme against colour theory such as complementary, analogous and triadic schemes",
        "Beauty BMI",
        "The Beauty BMI not only computes BMI but also analyses body shape and the ideal weight range and gives beauty and health advice to support body management.",
        "Enter revenue, cost and expenses to automatically compute gross profit, net profit, margins and other financial metrics for break-even analysis of a salon or an independent business.",
        "Lipstick shade selector",
        "Enter your skin tone (cool, warm or neutral) and the occasion, and the tool matches the most flattering lipstick shade with a texture suggestion to help you pick a daily lip look fast.",
        "Skincare routine planner",
        "Enter your skin type and age to generate a personalized routine order from cleansing to sunscreen (water-based before oil-based, molecules from small to large) plus matching principles.",
        "Enter skin type, age and lifestyle parameters for a preliminary assessment of skin condition based on empirical formulas, with care direction; results are for reference and do not replace a professional diagnosis.",
        "Face shape and hairstyle matching",
        "A face shape and hairstyle matcher that maps 7 face shapes to suitable styles, helping you pick a look that lifts your appearance.",
        "Perm rod size chart",
        "A perm rod reference table listing the correspondence between rod diameter and curl result, helping you choose a rod for the curl you want.",
        "Skin water loss self-assessment",
        "Skin transepidermal water loss (TEWL) self-assessment",
        "About the Beauty and skincare tools",
        "This collection brings together 21 free online tools covering the common calculation, conversion and lookup needs of beauty and skincare. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and uploads no data, so your privacy is protected.",
        "The beauty and skincare tools collected on this page include (a few representative tools):",
        "These tools help you finish common beauty and skincare tasks quickly, with no need to memorize formulas or convert by hand \u2014 enter the input and you get the result.",
        "Do the beauty and skincare tools require a download or registration?",
        "No. Every tool on this page runs entirely in the browser: open the page and start using it. No software to install, no account to create, and no data is uploaded.",
        "Are the results accurate, and is my data safe?",
        "The tools compute locally in your browser using public mathematical formulas and general industry standards, so results appear instantly. All computation happens on your own device and no data is uploaded to any server, so your privacy is protected.",
    ]))


if __name__ == '__main__':
    main()
