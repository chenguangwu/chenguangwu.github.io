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
    # ===== index (22) =====
    en = [
        "💐 Floral Design Tools",
        "Floral Design",
        "Floral Design Tools",
        "Spiral Bouquet Calculator",
        "Enter the bouquet diameter (size) and style (tight or loose) to compute the total stem count, each layer's stem length ratio, and the spiral crossing distribution for assembling a spiral bouquet, guiding florists to control flower usage and form layering.",
        "Wedding Flower Estimator",
        "Enter banquet tables, guest count and floral items (bouquet, table flowers, arch, etc.) to estimate the total quantity and cost range of various wedding flowers, helping couples and planners control the fresh-flower budget and purchase volume.",
        "Floral Golden Ratio",
        "Floral golden ratio calculator. Based on vase height and classic ratios (e.g. 1.5×) it computes the ideal height of different-style floral works and gives a visualization diagram, assisting floral design and display.",
        "Preservative Ratio",
        "Enter vase capacity and target preservative concentration to compute the Chrysal and clean-water ratio, or convert a homemade recipe (sugar, disinfectant, etc.) dosage to extend cut-flower display life.",
        "Bloom Stage",
        "Click the corresponding bloom stage of a flower (from bud, breaking bud to full bloom, 6 levels) to see that level's form description, best display and harvest timing, and care or usage-scenario suggestions, for floristry, harvest and gift-timing reference.",
        "Basket/Wreath quantity and price distribution calculator. Enter budget and unit-price ranges to estimate the purchasable basket/wreath quantity and price-tier distribution, used for funeral and celebration flower procurement budget planning.",
        "About 'Floral Design Tools'",
        "The Floral Design Tools collection includes 6 free online tools covering common calculation, conversion and lookup needs in floral design scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use mini tools here. All tools run purely front-end, data is not uploaded to servers, protecting privacy and security.",
        "The floral design tools included on this page are (some representative tools):",
        "These tools help you quickly complete common floral-design tasks without memorizing complex formulas or manual conversion; enter to get results.",
        "Do the floral design tools need download or registration?",
        "No. All floral design tools on this page are pure front-end online tools; open the webpage and use directly, no software install, no account registration, and no data upload.",
        "Are the floral design tool results accurate? Is data safe?",
        "Tools compute locally in your browser based on public math formulas and general industry standards, results are instant. All computation happens locally on your device, data is not uploaded to servers, privacy and security are guaranteed.",
    ]
    mp = build('index', en); write('index', mp)

    # ===== spiral-bouquet (50) =====
    en = [
        "🧮 Spiral Bouquet Calculator",
        "Compute the required flower material count and each layer's length ratio from bouquet size and style",
        "Core formula (by input variables): Math.round(cfg.total×mainPct÷100); Math.round(remaining×0.6); stemLen×0.75",
        "Spiral Bouquet Calculation",
        "/ Spiral Bouquet Calculation",
        "📖 View the usage guide for Spiral Bouquet (main/ filler/ foliage ratio and stem length)",
        "Bouquet Size",
        "Small (hand bouquet)",
        "Medium (daily bouquet)",
        "Large (celebration bouquet)",
        "Extra large (wedding bouquet)",
        "Bouquet Style",
        "Round",
        "Natural",
        "Main flower material length (cm)",
        "Main flower share (%)",
        "📖 Spiral Bouquet Making Points",
        "Spiral technique",
        ": each stem is crossed and stacked clockwise to form a natural spiral",
        "Layered structure",
        ": center main flower → middle filler → outer foliage fill",
        "Length grading",
        ": outer material is about 3-5 cm shorter than center, forming an arc",
        "Flower count",
        ": medium bouquet about 15-25 stems, large 30-50 stems",
        "Handle position",
        ": handheld point is about 1/3 of total bouquet length",
        "Binding point",
        ": fix at the stem spiral crossing with twine or tape",
        "💡 Main flower 60%, filler 25%, foliage 15% is the classic ratio. Natural-style bouquets can increase foliage ratio to 30%.",
        "📚 Deep Dive: Spiral Bouquet (main/ filler/ foliage ratio and stem length)",
        "When making hand/daily bouquets, set total stem count by size (small/medium/large/extra-large), then split into main, filler, foliage.",
        "Set each layer's stem length by main-flower share and style (round/ cascade/ natural), creating the spiral structure.",
        "Before purchasing, use the ratio to estimate each material's usage, controlling cost and form fullness.",
        "Reproducible example: medium round, main flower 60%, stem length 45 cm",
        "Input: size=Medium (total=18 stems), style=Round (fillerRatio 0.7, outerRatio 0.85), main share 60%, main stem length 45 cm.\nMain = round(18×60/100) = round(10.8) = 11 stems; remaining = 18-11 = 7; filler = round(7×0.6) = round(4.2) = 4 stems; foliage = 7-4 = 3 stems.\nStem length: main 45 cm, filler = 45×0.7 = 31.5 cm, outer = 45×0.85 = 38.25 cm, foliage = 45×0.75 = 33.75 cm.\nConclusion: a medium round bouquet needs 18 stems total (main 11 + filler 4 + foliage 3), main 45 cm, filler about 31.5 cm, outer about 38.3 cm, foliage about 33.8 cm, forming a hemispherical layering.",
        "What is the spiral structure for?",
        "All stems meet at one point into a spiral; the bouquet handle is tidy, the front is radial and it can stand to take up water — the basis of professional bouquets. Main flower on top, filler fills gaps, foliage at base, ratio tuned by size and style.",
        "How much main-flower share is appropriate?",
        "Daily/bouquet main flower 50-70% is most common; more main flower is more focused, less is fluffier. This tool splits by share and remaining 0.6 filler, foliage fills the rest; large/wedding bouquets can reach 30+ main stems, raise total accordingly.",
        "About 'Spiral Bouquet Calculation'",
        "Spiral bouquet calculator, computing the required flower material count and each layer's length ratio from bouquet size and style.",
        "4 bouquet sizes selectable",
        "3 bouquet styles switchable",
        "Main/ filler/ foliage ratio calculation",
        "Each layer's stem length suggestion",
        "Procurement calculation before bouquet making",
        "Floral design length planning",
        "Learn spiral bouquet structure",
        "Wedding bouquet budget estimation",
    ]
    mp = build('spiral-bouquet', en); write('spiral-bouquet', mp)

    # ===== wedding-flowers (84) =====
    en = [
        "💍 Wedding Flower Estimator",
        "Estimate total wedding flower material from tables, guest count and floral items",
        "Core formula (by input variables): ITEM_CONFIG.corsage.perUnit×2; ITEM_CONFIG.welcome.perUnit×1; ITEM_CONFIG.bridal.perUnit×1",
        "Wedding Flower Estimation",
        "/ Wedding Flower Estimation",
        "📖 View the usage guide for Wedding Flower Estimation (item × tables → total and cost)",
        "Banquet Tables",
        "Guest Count",
        "Table Flower Shape",
        "Small (low, about 8 stems/table)",
        "Medium (moderate, about 15 stems/table)",
        "Large (tall, about 25 stems/table)",
        "Luxury (full, about 35 stems/table)",
        "Unit price per stem (CNY)",
        "Floral Item Selection",
        "👰 Bride Bouquet",
        "👩‍💼 Bridesmaid Bouquet",
        "🤵 Groom Corsage",
        "👩 Mother Wrist Flower",
        "🌹 Table Flowers",
        "⛪ Flower Arch",
        "🛤️ Aisle Petals",
        "📸 Welcome Floral",
        "Bridesmaid count",
        "Corsage count",
        "Estimated total flower usage",
        "Estimated cost: 0 CNY",
        "📖 Wedding Flower Usage Reference",
        "Floral Item",
        "Flower Usage",
        "Bride Bouquet",
        "20-30 stems",
        "Main + filler + foliage",
        "Bridesmaid Bouquet",
        "10-15 stems/person",
        "Slightly smaller than bride",
        "Corsage",
        "3-5 stems/each",
        "Main 1 + filler foliage",
        "Wrist Flower",
        "5-8 stems/each",
        "Delicate and small",
        "Table Flower (Small)",
        "8 stems/table",
        "Low vase",
        "Table Flower (Medium)",
        "15 stems/table",
        "Medium vase",
        "Table Flower (Large)",
        "25 stems/table",
        "Tall vase",
        "Table Flower (Luxury)",
        "35 stems/table",
        "Full large vase",
        "Flower Arch",
        "200-400 stems",
        "Large installation",
        "Aisle Petals",
        "About 5 stems/meter",
        "For scattering petals",
        "Welcome Floral",
        "50-100 stems",
        "Check-in desk + welcome area",
        "💡 Reserve 10-15% spare flowers for loss. Seasonal flower prices fluctuate greatly; booking 3-6 months ahead is recommended.",
        "📚 Deep Dive: Wedding Flower Estimation (item × tables → total and cost)",
        "Newlyweds/planners estimate total wedding flower stems and budget from tables, guest count and floral items.",
        "Check bouquet, bridesmaid, corsage, table flowers, arch, etc., accumulate usage per item.",
        "Use unit price × total (including 12% spare) to quickly derive the purchase cost range, controlling budget.",
        "Reproducible example: 15 tables, bride bouquet + 4 bridesmaids + 8 corsages + table flowers + arch",
        "Input: tables 15, unit price 5 CNY/stem, bridesmaids 4, corsages 8, table flowers=Medium (15 stems/table), checked items=bride bouquet/bridesmaid/corsage/table flowers/arch.\nStems per item: bride bouquet 25×1=25; bridesmaid 12×4=48; corsage 4×8=32; table flowers 15×15=225; arch 300×1=300.\nTotal stems = 25+48+32+225+300 = 630 stems.\nEstimated cost = 630×5×1.12 (including 12% spare) = 3528 CNY.\nConclusion: this plan needs about 630 stems, budget about CNY 3528; adding mother wrist flower (+12), welcome floral (+75), aisle petals (+5) etc. will increase further.",
        "How are table flower stems derived?",
        "Take stems per table by table-flower shape: small 8 / medium 15 / large 25 / luxury 35, then × tables. 15 tables medium is 15×15=225 stems, the bulk of usage; to control budget, downgrade shape or reduce tables.",
        "What does 12% spare mean?",
        "Fresh flowers have loss (transport damage, uneven opening, on-site refill); the tool adds 12% on total × unit price as spare fund to avoid running short on site. Actual purchase can reserve 10-15%, and raise the spare ratio further when valuable flowers take a high share.",
        "About 'Wedding Flower Estimation'",
        "Wedding flower estimator, computing total wedding flower usage and cost estimate per item from tables, guest count and floral items.",
        "8 floral items selectable",
        "Auto-calculate by tables and table-flower shape",
        "Includes 12% spare flowers",
        "Cost estimate and itemized list",
        "Wedding floral budget planning",
        "Flower purchase list",
        "Wedding prep floral quote",
        "Learn wedding floral usage",
    ]
    mp = build('wedding-flowers', en); write('wedding-flowers', mp)

if __name__ == '__main__':
    main()
