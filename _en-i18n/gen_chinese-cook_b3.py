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
    # ===== sauce-ratio (35) =====
    write('sauce-ratio', build('sauce-ratio', [
        '🧮 Sauce-ratio calculator',
        'Select sauce type and base spoon count to auto-compute each seasoning amount',
        '📖 View "Sauce-ratio calculator user guide"',
        'Each seasoning amount = base spoon count × that seasoning ratio coefficient; common flavor-profile coefficients: sweet-and-sour sugar:vinegar:soy:water = 1:1:0.5:2, fish-fragrant sugar:vinegar:soy:cooking-wine:water = 2:2:1:1:4, kung-pao sugar:vinegar:soy:cooking-wine = 1:1:1:1; total amount = base spoon count × sum of coefficients; when scaling up by ratio keep the coefficients unchanged to stably recreate the flavor; output taste deviation rate = measured amount deviation ÷ standard amount × 100%.',
        'Sauce type',
        'Sweet-and-sour',
        'Fish-fragrant',
        'Kung-pao',
        'Spicy-numbing',
        'Garlic',
        'Braised-red',
        'Base spoon count (soup spoon)',
        '📖 Classic sauce base ratios',
        'Tip: 1 soup spoon ≈15ml. Ratios are general base recipes; adjust by taste in practice. Sweet-and-sour dishes can add a little salt for umami; fish-fragrant dishes need minced pickled chili prepared separately.',
        '📚 In-depth: sauce-ratio calculator',
        'For sweet-and-sour sauce, teriyaki sauce, convert by fixed ratio (e.g. sugar:vinegar:soy ≈ 1:1:0.5) in batch, ensuring consistent taste each time, avoiding flops by feel.',
        'For cold dishes reverse-derive salt, vinegar, oil, chili amounts by total; especially for multi-portion or takeout standardized output to reduce error.',
        'Reduced-salt reduced-sugar version: lower proportionally and fine-tune acid/umami balance, record the recipe for recreation.',
        'Sweet-and-sour ratio conversion',
        'Common sweet-and-sour sauce sugar:vinegar:soy:water ≈ 2:2:1:1 (plus a little starch to thicken); if total sauce 200ml needed, then sugar and vinegar each about 57ml, soy and water each about 28ml, fine-tune sweet/sour by taste.',
        'Is the ratio by volume or weight?',
        'Home liquid seasonings are mostly approximated by volume (spoon / ml), solids (sugar, salt) more accurate by weight; this tool mainly converts by volume ratio, adjustable by your available measure.',
        'Difference between fish-fragrant and sweet-and-sour?',
        'Fish-fragrant sauce adds pickled chili / bean paste, ginger scallion garlic on the sweet-sour base into a salty-sweet-sour-spicy compound taste; sweet-and-sour is pure sweet-sour, with different ratio and flavoring focus.',
        'Why sometimes salty with same ratio?',
        'Different brands of soy saltiness and vinegar acidity vary greatly; after mixing by ratio always taste and fine-tune; tool ratio is a starting point, not an absolute standard.',
        'About "sauce-ratio calculator"',
        'Sauce-ratio calculator collects base ratios of classic Chinese sauces like sweet-and-sour, fish-fragrant, kung-pao, spicy-numbing, auto-converting each seasoning amount by required portion, saying goodbye to seasoning by feel.',
        '6 classic sauce recipes',
        'Auto-convert amounts by spoon count',
        'Output ml for easy measuring',
        'Chinese sauce-ratio calculator - base ratios of classic sauces like sweet-and-sour, fish-fragrant, kung-pao, spicy-numbing, auto-converting each seasoning amount by portion. A daily-life tool, close to life, practical and convenient.',
        'Sweet-and-sour and braised-red: batch convert by ratio for consistent taste every time',
        'Cold dishes multi-portion: reverse-derive salt/vinegar/oil/chili amounts by total, reduce error',
        'Reduced-salt reduced-sugar version: lower proportionally and fine-tune acid/umami, easy to recreate',
    ]))

    # ===== wok-heat (41) =====
    write('wok-heat', build('wok-heat', [
        '📚 Heat-control guide',
        'Chinese-cooking heat-gear comparison; select a heat level to view traits and suitable cooking methods',
        '📖 View "Heat-control guide user guide"',
        'Heat-control guide: summarizes the flame traits and suitable cooking methods of four Chinese-cooking heat levels — high, medium, low, simmer — pure front-end local lookup, mastering the "match fire to dish" heat skill.',
        'Heat level',
        'High heat (big fire / wu-fire)',
        'Medium heat',
        'Low heat (wen-fire)',
        'Simmer',
        '📋 Heat-level comparison table',
        'Tip: the core of heat is "match fire to dish" — flash-fry needs high heat for quick finish, braise needs low heat slow simmer. Heat must pair with oil temperature and ingredient thickness to make a good dish.',
        '🎯 Heat-use mnemonic',
        'High heat quick finish',
        'Flash-fry, blanch, fragrance-pop use high heat to lock moisture and keep crisp-tender, emphasizing "wok hei" (breath of the wok).',
        'Medium heat shape-setting',
        'Pan-fry, stick-fry, dry-fry use medium heat for crisp outside tender inside with good color, less likely to scorch.',
        'Low heat slow braise',
        'Braise, simmer, stew, red-cook use low heat for flavor penetration, soft tenderness and rich broth; never rush with high heat.',
        'Simmer keep-warm',
        'Soup finishing, keep-warm, sauce reduction use simmer for long slow flavor release.',
        '📚 In-depth: heat-control guide',
        'Flash-fry (high heat) suits leafy greens, kidney etc. quick-cooking ingredients; out fast to keep crisp-tender and color; insufficient heat makes them water-logged and steamed.',
        'Pan-fry (medium) fish, steak need hot-pan-then-warm-oil, shape-set before flipping to avoid skin sticking and breaking; low slow fry for egg dumplings, glutinous cakes.',
        'Braise, stew, red-cook (low / simmer) long heating makes meat tender and broth rich; high heat scorches the bottom; first boil on high then turn to low.',
        'Heat for stir-fried greens',
        'Heat the wok until smoking, add oil (high heat), greens in, quick-toss 30–60 seconds until wilted and just done, out of the pan to keep emerald green and crisp-tender; medium-heat long stir makes them water out, yellow and soft.',
        'How to tell high from medium heat?',
        'High heat flame leaps past the wok rim, blue flame concentrated; medium heat flame stays at the wok bottom, not spreading out; home stove judges by flame contact area and sound (sizzle).',
        'Why braise meat high first then low?',
        'High heat boils off foam and sets flavor; low slow braise turns collagen and fat, meat tender and broth clear not cloudy; long high heat scorches bottom and dries meat.',
        'Is sticking related to heat?',
        'Yes. Pan-frying fish and egg needs "hot-pan-cool-oil" medium heat, ingredient surface dry before adding; too-eager fire or not-hot-enough wok both stick; you can heat the wok first then pour oil.',
        'About "heat-control guide"',
        'Heat-control guide summarizes the flame traits and suitable cooking methods of four Chinese-cooking heat levels — high, medium, low, simmer — helping master the core "match fire to dish" heat skill.',
        'Four-level heat trait comparison',
        'Flame appearance description for easy judgment',
        'Provides heat-use mnemonic',
        'Heat-control guide - Chinese big/medium/low heat comparison table, high/wu-fire/wen-fire heat traits and suitable cooking methods, heat-mastery tricks. A daily-life tool, close to life, practical and convenient.',
        'Flash-fry leafy greens: high heat quick-toss for crisp-tender, emerald green',
        'Pan-fry fish and egg: hot-pan-warm-oil medium heat to set shape, no skin sticking',
        'Braise red-cook stew soup: low heat slow boil for tender meat, rich broth, no scorched bottom',
    ]))

    print('body_chinese-cook_b3 done')

if __name__ == '__main__':
    main()
