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
    write('rater-nail', build('rater-nail', [
        "\U0001F4CB Nail colour family harmony score",
        "Enter a base colour, a main polish colour and an optional accent, then check and score the scheme against colour theory such as complementary, analogous and triadic schemes",
        "Base colour (base coat or nude)",
        "Main polish colour",
        "Accent colour (optional)",
        "Include the accent colour in the triadic scheme check",
        "Score the pairing",
        "\U0001F4DA In-depth analysis: nail colour family harmony score",
        "Design a three-colour scheme of base, main and accent and preview the overall coordination.",
        "Avoid clashing triads by using colour theory scores to filter out bad combinations.",
        "A nail artist shows the client the scheme score to build trust.",
        "Three-colour harmony example",
        "Base nude pink (350 degrees), main wine red (350 degrees), accent gold (50 degrees): the base and main colour share a hue and score high, and the small gold accent (under 10% of the area) brightens without clashing, giving a composite harmony of 82. Switching the main colour to neon green (120 degrees) creates a clash and drops the score to 55.",
        "What is the safest way to combine three colours?",
        "\"Main colour + same-family base colour + small-area accent\" works best. Keep the accent to 5%-10% of the design so it pops without breaking the whole look.",
        "Must I change something when the harmony score is low?",
        "Not necessarily. A low score means strong contrast and a bold style, which is acceptable if the client wants a statement look. The score is a reference, not a hard rule.",
        "Hue difference is computed as the smallest angle within 0-180 degrees, identifying six two-colour relations: same family, analogous, medium contrast, split, contrast and complementary",
        "With the accent colour enabled, the three colours are additionally checked against triadic schemes (about 120 degrees apart) and split-complementary schemes",
        "Nail colour schemes can be reasonably bold, since complementary and triadic schemes carry more visual tension in fashion looks",
        "About the Nail colour family harmony score",
        "The nail colour family harmony score tool uses the HSL colour model to identify same-family, analogous, complementary and triadic schemes among the base colour, main polish colour and accent colour, then returns a harmony score with pairing suggestions. It runs entirely in the browser and uploads no data.",
        "Supports triadic three-colour checks",
        "Recognises six types of colour scheme",
        "Professional nail pairing advice",
        "Colour design for nail styles",
        "Pre-review for accent and gradient schemes",
        "Gel polish colour pairing",
    ]))

    write('recommender-cycle', build('recommender-cycle', [
        "\U0001F9D1\uFE0F\u2695\uFE0F Care (product / technique / cycle) recommendation",
        "Product / technique / cycle",
        "Generate the steps cleanser, toner, serum, lotion, cream, sunscreen from your skin type and goal, following the absorption order of water-based before oil-based and small molecules before large ones. For the cycle dimension it gives weekly frequency caps for cleansing, masks and acids, always within what your skin tolerates.",
        "\U0001F4DA In-depth analysis: skincare cycle recommendation",
        "Generate daily skincare steps and timing from your skin type and goal.",
        "Adjust your care frequency when the season turns or after an acid peel.",
        "A skincare advisor copies the plan to the client as an everyday reference.",
        "Oily skin oil-control example",
        "For oily skin with an oil-control goal: morning amino acid cleanser, toner, niacinamide serum, light lotion, sunscreen. Cycle dimension: cleansing twice a day, clay mask once a week, acids twice a week (at night), and reduce frequency during a sensitive period. The output is sorted by ascending molecule size.",
        "Why should steps go from small molecules to large?",
        "Toner and serum have a small",
        "molecular size",
        "so they penetrate first, while the larger molecules in lotion and cream lock water in afterwards. Reversing the order blocks absorption or causes breakouts.",
        "Can I just increase the frequency?",
        "No. Cleansing, acids and masks all have frequency caps, and over-caring damages the barrier and can trigger breakouts and redness. Increase gradually within what your skin tolerates.",
        "About the Care (product/technique/cycle) recommendation",
        "Care (product/technique/cycle) recommendation. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))

    write('recommender-face-shape', build('recommender-face-shape', [
        "\U0001F484 Face shape and hairstyle matching system",
        "Online face shape and hairstyle matching recommendation system",
        "Analyse face shape using the three-court five-eye proportions and match shaping hairstyles: a long mid-face is shortened with bangs, and a square face uses a side part to cover the jaw corners. When proportions are slightly off but still balanced, the hairstyle visually corrects the facial balance.",
        "\U0001F4DA In-depth analysis: face shape hairstyle recommendation system",
        "Use the three-court five-eye proportions to analyse face shape and match a shaping hairstyle.",
        "A high hairline or prominent cheekbones that you want a hairstyle to disguise.",
        "A stylist combines facial proportions with a cutting plan.",
        "Three-court five-eye example",
        "Measure the three segments from hairline to brow, brow to the base of the nose, and nose base to chin; equal segments mean the three-court standard. Eye width \u00D7 5 \u2248 face width is the five-eye standard. If the mid-face is long, use bangs to shorten it and add volume at the sides to balance the proportions, matching the \"shorten the mid-face\" strategy.",
        "Does not meeting the three-court five-eye standard mean you do not look good?",
        "No. The standard is a reference average and many people deviate slightly while still looking balanced. Hairstyles exist precisely to correct proportions visually, such as a wispy fringe for a high hairline.",
        "How do I soften a square face?",
        "Use a side part to cover the jaw corners and add top volume to elongate the face, avoiding ear-length straight hair that exposes the angles. Curly hair softens the lines more than straight hair.",
        "About the Face shape and hairstyle matching system",
        "Face shape and hairstyle matching system. A beauty and skincare tool that helps calculate product dosage and mixing ratios.",
    ]))

    write('skin-tewl', build('skin-tewl', [
        "\u26A1 Skin transepidermal water loss (TEWL) self-assessment",
        "Assess your skin's transepidermal water loss through 8 self-assessment questions and get skincare advice",
        "Skin water loss self-assessment",
        " / Skin water loss self-assessment",
        "Graded by water loss rate: normal under 10, mildly damaged 10-20, severely damaged over 20 g/(m\u00B2\u00B7h). The questionnaire maps tightness, flaking and stinging frequency onto these bands; a high value indicates barrier damage needing ceramides and a pause on acids.",
        "What is TEWL?",
        "TEWL (transepidermal water loss) measures how well the skin barrier holds water. The higher the TEWL, the poorer the skin's water retention. This tool assesses it indirectly through a self-report questionnaire.",
        "\U0001F4CA Assessment result",
        "\U0001F4DA In-depth analysis: skin transepidermal water loss (TEWL) self-assessment",
        "Skin turns red and flaky when the season changes and you want to check whether the barrier is damaged.",
        "Monitor water loss after an acid peel to judge how well it has recovered.",
        "Skincare R and D teams segment users by barrier condition.",
        "TEWL grading example",
        "Normal water loss is under 10 g/(m\u00B2\u00B7h), mild damage 10-20 and severe damage over 20. The questionnaire scores tightness, flaking and stinging frequency and maps them to a band: with stinging 4 times a week and visible flaking, the mapped TEWL \u2248 18 g/(m\u00B2\u00B7h), indicating mild damage that calls for barrier repair (ceramides, pause acids).",
        "Does high TEWL mean dry skin?",
        "Not necessarily. High TEWL means the barrier retains water poorly, which can mean oily outside and dry inside. Dry skin is about low sebum; the mechanisms differ but both need hydration and repair.",
        "How do I lower TEWL?",
        "Add ceramides and cholesterol to repair the brick-wall structure, avoid over-cleansing and acids, use occlusives such as petroleum jelly to reduce evaporation, and humidifying the air also helps.",
        "About the Skin water loss self-assessment",
        "Skin transepidermal water loss (TEWL) self-assessment. An everyday-life utility, close to daily needs, practical and convenient.",
    ]))


if __name__ == '__main__':
    main()
