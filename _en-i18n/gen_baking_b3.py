#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'baking')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'baking')
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
    out = {'slug': slug, 'industry': 'baking', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "🧁 Baking & Dessert Tools",
        "Baking & Dessert",
        "Baking & Dessert Tools",
        "Recipe Scaler",
        "Recipe Scaler is a free online baking tool. When changing a recipe from 2 servings to 6, or from small batch to large batch, all ingredients scale by the same ratio. Enter the original amounts and the factor to convert them in bulk, avoiding manual errors. Runs entirely in the browser, no data uploaded, no registration needed, ope...",
        "Oven Temperature Converter",
        "Oven temperature converter, two-way Celsius/Fahrenheit conversion with convection-oven temperature compensation, plus a reference of common baking-temperature uses.",
        "Baker's percentage converter, using flour weight as 100% to convert each ingredient by ratio and supporting recipe scaling, suitable for home and bakery recipe work.",
        "Ingredient Conversion by Baker's Percentage (flour = 100%)",
        "Using flour weight as 100%, calculate the proportion of other ingredients; enter the flour amount to get the amounts of water, sugar, yeast, etc., suitable for bread recipe scaling and baking ratio conversion.",
        "Oven Temperature (Celsius/Fahrenheit) Converter and Convection Compensation",
        "Convert oven temperature between Celsius and Fahrenheit and provide the convection-versus-conventional compensation temperature, helping set the baking temperature accurately per recipe and avoid over-baking.",
        "Fermentation Time Adjustment",
        "Fermentation time adjuster, correcting the standard fermentation time by the Q10 coefficient based on ambient temperature and humidity, improving bread and pastry fermentation success.",
        "Mold Volume Matcher, calculating the volume of different-shaped molds and scaling the batter fill proportionally, avoiding overflow or under-fill in baking.",
        "Dough Hydration",
        "Enter the weight of flour and water to calculate dough hydration (baker's percentage), and with a reference table suggest the corresponding bread texture and suitable categories.",
        "About 'Baking & Dessert Tools'",
        "The baking & dessert tools collection includes 8 free online tools, covering common calculation, conversion and lookup needs in baking and dessert scenarios. Whether you are a professional, student or general user in the field, you can find ready-to-use handy tools here. All tools run entirely in the browser, no data uploaded to servers, your privacy and security protected.",
        "The baking & dessert tools on this page include (representative tools):",
        "These tools help you quickly complete common baking and dessert tasks without memorizing complex formulas or manual conversion; enter values to get results.",
        "Do the baking & dessert tools need download or registration?",
        "No. All baking & dessert tools on this page are pure front-end online tools; open the page to use them directly, no software installation, no account registration, and no data upload.",
        "Are the baking & dessert tools' calculation results accurate? Is the data safe?",
        "The tools calculate locally in your browser based on public math formulas and common industry standards, with instant results. All computation is done on your device locally, data is never uploaded to servers, and privacy and security are guaranteed.",
    ]))
    write('mold-volume', build('mold-volume', [
        "🧊 Mold Volume Matcher",
        "Calculate the volume of molds of different shapes and scale the batter fill by volume ratio",
        "Core formula (by input variables): toVol × 0.65",
        "📦 Original mold",
        "⭕ Round",
        "⬛ Square",
        "▭ Rectangle",
        "Volume (ml)",
        "🎁 Target mold",
        "📖 Common Mold Volume Reference",
        "Mold",
        "6-inch round pan",
        "Diameter 15cm × height 7cm",
        "about 1237",
        "Small cake",
        "8-inch round pan",
        "Diameter 20cm × height 7cm",
        "about 2199",
        "Standard cake",
        "10-inch round pan",
        "Diameter 25cm × height 7cm",
        "about 3436",
        "Large cake",
        "450g toast pan",
        "about 2289",
        "6-inch square pan",
        "about 1575",
        "Pound cake",
        "8-inch square pan",
        "about 2800",
        "Large pound cake",
        "💡 Generally fill the mold to 60-70% full. Volume = base area × height × fill factor. Round volume = π × r² × h; square = side² × h; rectangle = length × width × h.",
        "📚 In-Depth: Mold Volume Matching",
        "When switching to a differently shaped mold for the same recipe, adjust the fill by volume ratio.",
        "Splitting one large mold into several small molds requires redistributing the batter and fine-tuning the time.",
        "When the mold volume is insufficient, reduce the total recipe amount proportionally.",
        "Ratio adjustment when replacing a large mold with two small molds",
        "Originally a 1500cm³ large mold, now changed to 2 small molds of 700cm³ (total 1400cm³). Volume is about 1400 / 1500 ≈ 93% of the original, so reduce the total recipe by about 7%; small molds heat faster, so shorten baking time slightly.",
        "What to do when the combined volume of two small molds differs from the large mold?",
        "Scale the total recipe by the actual volume ratio so the batter fill is consistent; also, small molds have a larger surface area and heat faster, so usually reduce time slightly or lower by a few degrees to avoid over-drying the edges.",
        "How to estimate the volume of differently shaped molds?",
        "Cylinder V = π r² h, rectangular prism V = length × width × height, for a truncated cone or irregular shape use the water-fill method to measure directly (fill with water and weigh, 1g ≈ 1cm³). Direct measurement is most accurate, especially for irregular molds.",
        "About 'Mold Volume Matcher'",
        "The mold volume matcher calculator computes the volume of round, square and rectangular molds and scales the batter fill proportionally.",
        "Supports round / square / rectangular molds",
        "Automatic volume calculation",
        "Scaling ratio conversion between molds",
        "Suggested fill reference",
        "Adjusting recipe when changing molds",
        "Calculating batter fill amount",
        "Converting different-size cakes",
        "Learning mold volume knowledge",
    ]))

if __name__ == '__main__':
    main()
