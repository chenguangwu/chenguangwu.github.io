#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'floral')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'floral')
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
    out = {'slug': slug, 'industry': 'floral', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== bloom-stage (56) =====
    en = [
        "💐 Bloom Stage Levels",
        "Click a bloom stage to see flower status, judgment, and usage-scenario suggestions",
        "Bloom Stage",
        "/ Bloom Stage",
        "📖 View the usage guide for Bloom Stage Levels (6-stage bud-to-full-bloom judgment)",
        "Cut flowers are graded into 6 bloom stages: bud (tight, unopened), breaking bud (outer petals slightly spread), half-open (about 50% open), near-full (about 80% open), fully open (fully spread with visible stamens), and over-ripe (petals drooping). Harvest and display are best at breaking-bud to half-open (longest vase life); the near-full stage suits same-day use, and gift flowers should use the breaking-bud stage. Vase life shortens as bloom stage increases; after over-ripe, flowers wilt every 1 to 2 days.",
        "📖 Common Flowers Bloom-Stage Reference",
        "Flower",
        "Best Harvest Stage",
        "Vase Life",
        "Rose",
        "Calyx reflexed, petals loose (stages 2-3)",
        "Too tight will not open; too open falls apart",
        "Lily",
        "Bud shows color, slightly open (stages 1-2)",
        "Remove anthers to prevent staining",
        "Carnation",
        "Petals about half spread (stages 2-3)",
        "Stores well, can be cut early",
        "Tulip",
        "Bud shows translucent color (stages 1-2)",
        "Keeps growing taller in vase",
        "Sunflower",
        "Petals fully spread (stages 4-5)",
        "Harvest only when fully open",
        "Chrysanthemum",
        "Petals spread over 2/3 (stages 3-4)",
        "10-20 days",
        "Long vase life",
        "Lisianthus",
        "2-3 flowers open (stages 2-3)",
        "Buds open in succession",
        "Hydrangea",
        "Fully colored (stage 4)",
        "5-10 days",
        "High water demand, prone to dehydration",
        "💡 When choosing bloom stage, consider transport distance, usage time, and flower traits. For nearby immediate use pick the near-full stage; for long-distance transport pick the bud stage.",
        "📚 Deep Dive: Bloom Stage Levels (6-stage bud-to-full-bloom judgment)",
        "Judge bloom stage when cutting or buying flowers to match the usage date (low stage for transport, high stage for same-day use).",
        "During vase care, estimate remaining display life by stage to decide whether to force opening or use soon.",
        "For floral design choose stage 2-3 (half-open) material, balancing form and vase life.",
        "Stage Comparison and Timing (6 stages)",
        "Stage 0 Bud: closed, for long-distance transport/long storage but slow to open in vase.\nStage 1 Color-showing: tip slightly loose, for use in 2-3 days (lily/tulip best cut at this stage).\nStage 2 Breaking bud: about 1/3 open, the best cutting stage for most flowers, balancing openness and life.\nStage 3 Half-open: 1/2-2/3 open, common stage for bouquets, use same/next day.\nStage 4 Near-full: fully open, best appearance but life starts shortening (sunflower/chrysanthemum best at this stage).\nStage 5 Full bloom: petals reflexed, for instant display/photos, wilts soon.\nConclusion: need 2-3 days ahead choose stages 1-2, same-day choose 3-4, instant display choose 5; bouquet making prefer stages 2-3.",
        "Which stage should I buy?",
        "Depends on usage time: 2-3 days ahead choose color-showing/breaking-bud (stages 1-2), same-day choose half-open (stage 3), immediate photo/display choose near-full (stages 4-5). Bouquets commonly use stages 2-3, open enough yet still good for several more days in the vase.",
        "What if a low-stage bud will not open?",
        "You can force opening: wake flowers in deep warm water (≈40°C), raise room temperature slightly, avoid direct light; most buds open in 1-2 days. Some varieties (e.g. carnation) open slowly by nature. For high-stage flowers do the opposite: use soon, keep cool and away from light to extend life.",
        "About 'Bloom Stage'",
        "A bloom-stage judgment tool that grades flowers from bud to full bloom into 6 levels, with status descriptions and usage-scenario suggestions.",
        "6-level bloom grading",
        "Detailed status per level",
        "Common flower cutting-stage reference",
        "Judge bloom stage when buying flowers",
        "Choose suitable material for floral design",
        "Flower cutting-timing reference",
        "Learn flower opening knowledge",
    ]
    mp = build('bloom-stage', en); write('bloom-stage', mp)

    # ===== golden-ratio (50) =====
    en = [
        "💎 Floral Golden Ratio Calculator",
        "Compute the ideal floral design height from vase height, following the floral golden-ratio rule",
        "Floral Golden Ratio",
        "/ Floral Golden Ratio",
        "📖 View the usage guide for Floral Golden Ratio (vase × style factor sets height)",
        "Floral height follows classic ratios: main-flower height = vase height × 1.5 to 2.0 (Western triangle or fan commonly 1.5 to 1.8, spherical 1.0 to 1.5); the golden ratio 1:1.618 sets the main visual division (flower-body height ÷ vase height ≈ 1.618); total height = vase height + flower-body height, width = 2 × height (common for table designs); the container mouth-width to height ratio should approach the golden ratio for harmony.",
        "🔺 Triangle (1.5×)",
        "⭕ Round (1.5-2×)",
        "💎 L-shape (2-2.5×)",
        "💧 Cascade (1-1.5×)",
        "Vase height (cm)",
        "Vase diameter (cm)",
        "📖 Floral Proportion Rules",
        "Style",
        "Height ratio",
        "1.5 × vase height",
        "Symmetric and stable, classic style",
        "Round/Hemisphere",
        "1.5-2 × vase height",
        "Full and round, commonly used",
        "L-shape/Asymmetric",
        "2-2.5 × vase height",
        "Dynamic, suits modern style",
        "1-1.5 × vase height",
        "Extends downward, elegant",
        "Horizontal",
        "Width = 2 × height",
        "Common for table florals",
        "💡 Floral golden ratio: the ratio of work height to vase height is about 1:1.5 to 1:2.5. The golden section 1.618 is a classic aesthetic ratio.",
        "📚 Deep Dive: Floral Golden Ratio (vase × style factor sets height)",
        "After choosing a vase, set the ideal main-flower height for the arrangement, avoiding top-heavy or unbalanced proportions.",
        "By style (",
        "/round/ L-shape/ cascade) apply different height factors to make shapes that follow aesthetic conventions.",
        "For series works like table flowers, reception desk flowers, and wedding aisle markers, unify the ratio to keep overall harmony.",
        "Reproducible example: vase height 15 cm, round/hemisphere style",
        "Input: vase height 15 cm, style=Round/Hemisphere (ideal 1.75, min 1.5, max 2.0).\nIdeal floral height = 15 × 1.75 = 26.25 cm; shortest = 15 × 1.5 = 22.5 cm; tallest = 15 × 2.0 = 30 cm.\nSo the main-flower top height is controlled within 22.5-30 cm, ideally about 26.3 cm.\nCompared with other styles: triangle 15 × 1.5 = 22.5 cm (fixed), L-shape 15 × 2.25 = 33.75 cm, cascade 15 × 1.25 = 18.75 cm.\nConclusion: a 15 cm vase with round style, main-flower height about 26 cm is most stable; for a more dynamic look use L-shape about 34 cm, for a drooping look use cascade about 19 cm.",
        "Why base height on a multiple of the vase?",
        "This is a classic floral ratio: the tallest flower is about 1.5-2.5 times the container, so the visual center of gravity stays stable. Too small a multiple looks shrunken, too large looks top-heavy; different styles use different ranges (e.g. triangle fixed at 1.5, cascade can go as low as 1.25 for a drooping feel).",
        "How to set the width?",
        "Width generally tracks height; round/hemisphere is near equal diameter overall; L-shape/cascade is low-front high-back and left-right asymmetric. This tool gives a height range; let width spread naturally with the material, keeping an overall 'height:width ≈ 1.5-2' look.",
        "About 'Floral Golden Ratio'",
        "A floral golden-ratio calculator that computes the ideal height of different-style floral works from vase height, with a visualization diagram.",
        "4 floral style ratios",
        "Ideal/shortest/tallest height calculation",
        "Visual ratio diagram",
        "Floral proportion rule reference table",
        "Floral design height planning",
        "Choose vase and material pairing",
        "Learn floral proportion aesthetics",
        "Ikebana composition reference",
    ]
    mp = build('golden-ratio', en); write('golden-ratio', mp)

    # ===== preservative (45) =====
    en = [
        "💐 Fresh-Cut Flower Preservative Ratio Calculator",
        "Compute the preservative (e.g. Chrysal) to water ratio from vase capacity",
        "Preservative Ratio",
        "/ Preservative Ratio",
        "📖 View the usage guide for Fresh-Cut Flower Preservative Ratio (commercial/homemade)",
        "Preservative amount = vase water × commercial preservative recommended concentration (Chrysal usually 1 packet per 500 mL to 1 L water); homemade recipe per liter of water adds white sugar 10-20 g (nutrients) + white vinegar or citric acid 1-2 mL (acidify and inhibit bacteria, pH 3.5-4.5) + bleach 0.1-0.2 mL (disinfect); change the solution every 2-3 days and re-cut stems diagonally 1-2 cm to reopen water uptake, extending vase life by 30%-50%.",
        "Vase water (ml)",
        "Preservative type",
        "Chrysal (standard)",
        "Chrysal (clear)",
        "Huazhishou",
        "Homemade preservative",
        "📖 Preservative Ratio Reference",
        "Preservative",
        "Ratio",
        "1 packet (10g) : 500 ml water",
        "Contains sugar + bactericide, general use",
        "1 packet (5g) : 500 ml water",
        "Clear water, no staining",
        "Complete nutrition, extends bloom life",
        "See recipe below",
        "Made from household materials",
        "🏠 Homemade Preservative Recipe",
        "When no professional preservative is available, make one from common household materials",
        "💡 Homemade preservative principle: sugar provides nutrition (like nectar), white vinegar/citric acid inhibits bacteria, bleach kills bacteria. Change the preservative every 2-3 days and re-cut stems diagonally.",
        "📚 Deep Dive: Fresh-Cut Flower Preservative Ratio (commercial/homemade)",
        "Prepare preservative by water volume before vase use to extend cut-flower display life and reduce bent necks and wilting.",
        "Use commercial preservative (Chrysal/Huazhishou) at packet-to-water ratio, or make a basic preservative from household materials.",
        "Adjust sugar and bacteriostat for different materials (herbaceous/woody/droopy-prone) to avoid over-decay.",
        "Reproducible example: 500 ml water, two plans",
        "Input: water 500 ml.\nPlan A Chrysal (standard, ratio=1/500, 1 packet 10g per 500 ml): amount = 500 × (1/500) = 1 g, about 0.1 standard packet (at 10g/packet), i.e. 1/10 of a packet per 500 ml.\nPlan B homemade: per 500 ml water → white sugar 500/500 × 2 = 2 g + white vinegar 500/500 × 1 = 1 ml + bleach 500/500 × 0.5 = 0.5 ml.\nConclusion: for 500 ml vase water, commercial standard Chrysal takes about 1 g (or clear/Huazhishou at 1 packet 5g per 500 ml takes 5g); homemade can use 2 g sugar + 1 ml vinegar + 0.5 ml bleach, where sugar supplies energy and acid and bleach inhibit bacteria.",
        "Is homemade preservative reliable?",
        "The basic version (sugar + weak acid + trace bleach) can extend bloom life short-term and suits emergencies; but it lacks the ethylene inhibitor and chelating agent of professional preservatives, so it is weaker than commercial. Do not overuse sugar (rots stems), keep bleach truly trace (a few drops), and use unscented.",
        "Can all flowers use the same ratio?",
        "Woody flowers (rose/hydrangea) can take slightly more sugar to promote opening; sensitive flowers (gerbera/iris) should use low sugar; remove all leaves below the waterline, re-cut stems 1-2 cm daily, and keep away from light with ventilation — these affect life more than the ratio alone.",
        "About 'Preservative Ratio'",
        "A fresh-cut flower preservative ratio calculator that computes professional preservative amounts like Chrysal from vase water, and provides a homemade recipe.",
        "Multiple professional preservative ratios",
        "Auto-calculate by vase water",
        "Homemade preservative recipe",
        "Ratio reference table",
        "Fresh-cut flower preservative mixing",
        "Extend fresh-flower vase life",
        "Homemade preservative from household materials",
        "Learn fresh-flower care knowledge",
    ]
    mp = build('preservative', en); write('preservative', mp)

    # ===== price (24) =====
    en = [
        "📊 Basket/Wreath Quantity and Price Distribution",
        "Online tool for basket/wreath quantity and price distribution",
        "📖 View the usage guide for Basket/Wreath Quantity and Price Distribution",
        "Single-item average price = (lower price + upper price) ÷ 2; combined average price = basket average × basket share + wreath average × (1 - basket share); affordable quantity = budget ÷ combined average, rounded down. Substituting the lower price gives the upper bound of affordable quantity, substituting the upper price gives the lower bound, forming the budget's affordable quantity range.",
        "Budget total (CNY)",
        "Basket lower price (CNY)",
        "Basket upper price (CNY)",
        "Wreath lower price (CNY)",
        "Wreath upper price (CNY)",
        "Basket quantity share (%)",
        "📚 Deep Dive: from budget and basket/wreath price ranges, estimate the purchasable quantity mix, amount composition and quantity range, to assist florist quoting and stocking.",
        "When taking orders, florists reverse-calculate the affordable basket and wreath quantities from the client budget, quickly giving the quantity and amount composition.",
        "When unit prices fluctuate, recompute with lower and upper bounds separately to give the affordable quantity range, avoiding quotes that exceed the budget.",
        "Before bulk celebration/funeral flowers, adjust the mix structure by basket share and compare total quantity and total amount under different combinations.",
        "Reproducible example: budget 8800 CNY, basket 200-400 CNY, wreath 100-260 CNY, basket share 50%",
        "Input: budget 8800 CNY, basket unit price 200-400 CNY, wreath unit price 100-260 CNY, basket quantity share 50%.\nCalculation: basket average = (200+400)÷2 = 300 CNY, wreath average = (100+260)÷2 = 180 CNY; combined average = 300×0.5 + 180×0.5 = 240 CNY/item.\nTotal affordable = 8800 ÷ 240 = 36.67, rounded down to 36 items, of which 18 baskets and 18 wreaths; amount = 18×300 + 18×180 = 8640 CNY.\nQuantity range: at lower unit price (combined 150 CNY) can buy 58 items, at upper unit price (combined 330 CNY) can buy 26 items, so the range is 26 - 58 items.\nConclusion: with budget 8800 CNY at average pricing one can buy 36 items for 8640 CNY; when actual price is higher the quantity trends toward 26, so stocking at the lower bound of the range is safer for quoting.",
        "How is the combined average price calculated?",
        "First take the midpoint of each basket and wreath price range as the average, then weight by basket quantity share: combined average = basket average × share + wreath average × (1 - share). Raising the share shifts the whole toward the basket average.",
        "Why give a quantity range?",
        "Because unit price is a range, not a fixed value. Substituting the lower price gives the upper bound of affordable quantity, substituting the upper price gives the lower bound, forming a range that hints 'how many items the actual price fluctuation will cost', avoiding a decision based on a single average.",
        "Can this amount be used directly as a quote?",
        "No. The result only covers the goods value of baskets and wreaths, excluding shipping, arranging labor, packaging supplies and delivery fees; actual quotes must add your operating cost and profit on top of these results.",
        "About 'Basket/Wreath Quantity and Price Distribution'",
        "Basket/wreath quantity and price distribution. Free online tool, front-end only, no data uploaded, privacy and security protected.",
    ]
    mp = build('price', en); write('price', mp)

if __name__ == '__main__':
    main()
