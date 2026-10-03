#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'chinese-cook')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'chinese-cook')
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
    out = {'slug': slug, 'industry': 'chinese-cook', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== ingredient-substitute (40) =====
    write('ingredient-substitute', build('ingredient-substitute', [
        '📚 Ingredient substitution finder',
        'Enter an ingredient name to search substitution options, or select from the list to view replacement suggestions',
        '📖 View "Ingredient substitution finder user guide"',
        'Ingredient substitution finder: collects substitution options and ratios for common Chinese-cooking seasonings, spices and auxiliaries; quickly find emergency replacements when short or on a restricted diet, pure front-end local lookup.',
        'Search ingredient',
        '📚 Common ingredient substitution quick reference',
        'Tip: substitution affects flavor; use the original ingredient if you can buy it. Ratios are for reference; taste a small amount first before adjusting.',
        '📚 In-depth: ingredient substitution finder',
        'When baking and you find no heavy cream / butter, look up substitutes (e.g. milk + oil for heavy cream, vegetable oil for butter) and check amount and texture difference, avoiding scrapping the half-finished product.',
        'Family allergy (e.g. egg, gluten, nuts) or vegetarian needs: look up substitute ingredients and cautions, keeping the dish structure and flavor as much as possible.',
        'Seasonal or regional out-of-stock (e.g. a spice, a vegetable): look up a locally available substitute with similar flavor, keeping the dish workable.',
        'What if no baking powder?',
        'Per 1 tsp baking powder ≈ 1/4 tsp baking soda + 1/2 tsp cream of tartar (or equal yogurt / lemon juice replacing part of the acidic liquid); halve the baking soda to avoid alkaline taste, and activate with acidic ingredient.',
        'Is the substitute amount proportional?',
        'Most are not equal-ratio. E.g. butter → vegetable oil about 0.8×, baking powder → baking soda about 1/4×; consider recipe and acid-base balance; the tool gives common approximations.',
        'What to watch in allergy substitution?',
        'Confirm cross allergens (nut oils, dairy residues); for vegetarian substitution watch hidden animal ingredients (gelatin, fish sauce); label when necessary to avoid accidental eating.',
        'Does substitution affect texture?',
        'Usually yes. E.g. vegetable oil for butter loses the milky aroma and flakiness; milk for heavy cream is thinner; it is a flavor/texture trade-off, choose by dish tolerance.',
        'About "ingredient substitution finder"',
        'Ingredient substitution finder collects substitution options and ratios for common Chinese-cooking seasonings, spices and auxiliaries; quickly find emergency replacements when cooking short of an item, so cooking never stalls.',
        'Supports keyword search',
        'Provides multiple substitution options',
        'Marks replacement ratio',
        'Quick-reference table at a glance',
        'Ingredient substitution finder - common Chinese-cooking ingredient substitutes, search an ingredient for available alternatives and replacement ratios, cooking emergency substitution reference. A daily-life tool, close to life, practical and convenient.',
        'Temporary shortage: e.g. no heavy cream / butter, look up substitute and amount, avoid scrapping the half-finished product',
        'Allergy / dietary restriction: look up equivalent substitutes (egg/dairy/vegetarian, nuts, etc.) keeping dish structure',
        'Regional / seasonal: use a locally available ingredient of similar flavor for out-of-stock spices and vegetables',
        'How to use ingredient substitution finder',
        'E.g.: oyster sauce, cooking wine, star anise...',
        'For scenarios of temporary cooking shortage, family allergy / dietary restriction or vegetarian need: quickly find substitute ingredients of similar flavor and texture and the replacement ratio, restoring the original dish structure and taste as much as possible, avoiding scrapping the half-finished product.',
        'What does ingredient substitution finder do?',
        'Ingredient substitution finder; enter an ingredient to search substitution options or view replacement suggestions and ratios, solving cooking substitution when short of an item.',
        'How to use ingredient substitution finder?',
        'Which scenarios is ingredient substitution finder suitable for?',
        'Substitution logic',
        'Ingredient substitution matches by similar flavor / function (e.g. liquid amount, acidity, coagulation), for temporary replacement when short or allergic.',
        'Substitution changes the finished texture and flavor; for precise scenarios like baking convert by ratio; allergy sufferers must check cross allergens.',
        'E.g.: oyster sauce, cooking wine, star anise...',
    ]))

    # ===== oil-temp (49) =====
    write('oil-temp', build('oil-temp', [
        '🍳 Oil-temperature cooking guide',
        'Chinese-cooking oil-temperature table; select an oil-temperature gear to view temperature, traits and suitable cooking methods',
        '📖 View "Oil-temperature cooking guide user guide"',
        'Oil-temperature cooking guide: summarizes the temperature range, oil-surface traits and suitable cooking methods of common Chinese-cooking oil-temperature gears (30%–90% heat), pure front-end local lookup, helping judge heat and oil temperature.',
        'Oil-temperature gear',
        '30%–40% heat (warm oil)',
        '50%–60% heat (medium)',
        '70%–80% heat (hot oil)',
        '90% heat (high oil)',
        '🔥 Oil-temperature gear table',
        'Safety tip: too-high oil temperature smokes and may even self-ignite (about 300°C and above); never leave unattended. When blue smoke rises from the oil surface it has reached the limit; turn off the heat and cool immediately.',
        '👁️ Oil-temperature judgment tricks',
        '30%–40% heat (90–130°C)',
        'Oil surface calm, no smoke, no sizzle; a chopstick dipped in gives tiny bubbles slowly rising. Suits velveting and soft-frying.',
        '50%–60% heat (140–180°C)',
        'Oil surface slightly moving with light blue smoke; more bubbles around the chopstick and a sizzle. Suits stir-fry, deep-fry, pan-fry.',
        '70%–80% heat (190–230°C)',
        'Oil surface smoking; vigorous bubbling around the chopstick. Suits flash-fry, re-fry and fragrance-popping.',
        '📚 In-depth: oil-temperature cooking guide',
        'Velvet-stir pork shreds and battered fish fillets go in at low temperature (30%–40% heat about 120–150°C) to lock moisture, stay tender and not stick; too high burns outside while raw inside.',
        'Deep-frying (50%–60% heat about 160–190°C) is staged by ingredient: first medium heat to set shape, then raise heat to drive out oil, achieving crisp outside tender inside.',
        'Fragrance-pop scallion/ginger/garlic and fragrant oil use 70%–80% heat (about 200°C around); in goes the ingredient with a sizzle, aroma bursts without burning; beyond that it smokes and turns bitter.',
        'Chopstick test for 30%–40% heat',
        'Insert a bamboo chopstick into the oil; tiny dense bubbles around (about 120–150°C) means 30%–40% heat, good for velveting; if lots of rapid bubbles with light blue smoke (about 200°C+) it is too high, remove from heat and cool before adding food.',
        'How many degrees per oil-temperature gear?',
        'Roughly: 30%–40% heat 120–150°C, 50%–60% heat 160–180°C, 70%–80% heat 190–220°C, 90% heat 230°C+ near smoking; different oils have different smoke points, observe primarily.',
        'Why low temperature for velvet-stir?',
        'Battered ingredients at low temperature: starch gelatinizes into a protective film, locking moisture; high temperature instantly crusts and sticks while the inside stays uncooked.',
        'Is smoking oil still usable?',
        'Smoking means the smoke point is reached; further heating produces harmful substances and a burnt bitter taste; remove from heat to cool or change oil, do not force the ingredient in.',
        'About "oil-temperature cooking guide"',
        'Oil-temperature cooking guide summarizes the temperature range, oil-surface traits and suitable cooking methods of common Chinese-cooking oil-temperature gears (30%–90% heat), helping master heat and oil-temperature judgment tricks.',
        'Four-gear oil-temperature temperature table',
        'Detailed oil-surface trait descriptions',
        'Provides safety tips',
        'Oil-temperature cooking guide - Chinese-cooking oil-temperature table, 30%–70% heat traits and cooking methods, oil-temperature judgment tricks. A daily-life tool, close to life, practical and convenient.',
        'Velvet-stir and batter: 30%–40% heat in the pan to lock moisture, tender and non-stick',
        'Deep-fry setting: 50%–60% heat medium fry, raise heat to drive out oil for crisp outside tender inside',
        'Fragrance-pop: 70%–80% heat in goes the ingredient with a sizzle, aroma bursts without burning',
        'How to use oil-temperature cooking guide',
        'For judging the timing of adding ingredients in different techniques like velvet-stir, deep-fry and fragrance-pop: compare the oil-temperature gear (30%–90% heat) temperature and oil-surface traits, pick the right heat to make ingredients tender/crisp/aromatic, avoiding burnt-outside-raw-inside or over-high-temperature bitterness.',
        'What does oil-temperature cooking guide do?',
        'Chinese-cooking oil-temperature guide; by oil-temperature gear view the temperature range, traits and suitable cooking methods (30%–90% heat), aiding heat control.',
        'How to use oil-temperature cooking guide?',
        'Which scenarios is oil-temperature cooking guide suitable for?',
        'Oil-temperature grading',
        'Chinese-cooking oil temperature (empirical): 30%–40% heat ≈ 120–140°C (calm surface, no bubbles when adding food, suits velvet-stir); 50%–60% heat ≈ 150–180°C (light smoke, bubbles around food, suits first deep-fry); 70%–80% heat ≈ 190–210°C (clear smoke, suits re-fry coloring); 90% heat ≥220°C (heavy smoke, use with caution).',
        'Pick cooking method by oil temperature: low heat velvet-tender, medium heat fry-cooked, high heat re-crisp and color.',
        'Different oils have different smoke points (e.g. olive oil low, peanut oil high); verify with an oil thermometer or the wooden-chopstick bubble method for safety.',
    ]))

    print('body_chinese-cook_b2 done')

if __name__ == '__main__':
    main()
