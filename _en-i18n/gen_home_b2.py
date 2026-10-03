#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'home')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'home')
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
    out = {'slug': slug, 'industry': 'home', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== index (23) =====
    en = [
        "🏡 Home Renovation Tools",
        "Home Renovation",
        "Home Renovation Tools",
        "Paint Usage Calculator",
        "Enter wall and ceiling area (or length×width×height), coat count and paint theoretical coverage (m²/L) to estimate total paint liters and purchase cost, with door/window deduction, helping owners control latex paint usage and budget.",
        "Lighting Calculator",
        "Estimate required total luminous flux and fixture count by room area, ceiling height and recommended illuminance, assisting home and office lighting layout; front-end adjustable parameters.",
        "Room Area Calculator",
        "Choose rectangular, L-shape, trapezoid, circular or triangular room shapes, enter dimensions to compute area and perimeter, assisting home renovation estimating tiles, wallpaper usage and space layout planning.",
        "Washer Capacity Selector",
        "The washer capacity selector is a free online home renovation tool. How to choose washer capacity? Recommend 5-10 kg range by household size, and judge whether larger capacity is needed by bulky bedding/curtains, with single-use water estimate. Runs purely front-end, no data upload, no registration...",
        "Furniture Layout",
        "Drag bed, sofa, table and other furniture onto the floor plan locally in the browser, place and avoid in real time by room size, estimate passages and space utilization; all computation is local, no upload, helping preview layout reasonableness before renovation.",
        "Renovation Budget",
        "Enter hard decor, main material, furniture, appliances and other renovation expenses by item, summarize total amount, each share and cumulative progress in real time, support local draft saving, helping owners track budget execution throughout and identify overrun items.",
        "About 'Home Renovation Tools'",
        "The Home Renovation Tools collection includes 6 free online tools covering common calculation, conversion and query needs in home renovation scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find ready-to-use mini tools here. All tools run purely front-end, data is not uploaded to servers, protecting privacy and security.",
        "The home renovation tools included on this page are (some representative tools):",
        "These tools help you quickly complete common home-renovation tasks without memorizing complex formulas or manual conversion; enter to get results.",
        "Do the home renovation tools need download or registration?",
        "No. All home renovation tools on this page are pure front-end online tools; open the webpage and use directly, no software install, no account registration, and no data upload.",
        "Are the home renovation tool results accurate? Is data safe?",
        "Tools compute locally in your browser based on public math formulas and general industry standards, results are instant. All computation happens locally on your device, data is not uploaded to servers, privacy and security are guaranteed.",
    ]
    mp = build('index', en); write('index', mp)

    # ===== renovation-budget (17) =====
    en = [
        "💰 Renovation Budget",
        "Manage renovation budget by item, compute total and share in real time, support local saving",
        "'Manage renovation budget by item, compute total and share in real time, support local saving' computes professionally by input parameters and outputs results.",
        "/ Renovation Budget",
        "📖 View the usage guide for Renovation Budget",
        "📚 Deep Dive: Renovation Budget",
        "Hard decor / main material / furniture / appliances listed by item, see each share in real time; if main material exceeds 40%, adjust structure promptly.",
        "Set a total budget cap, use cumulative progress to see spent ratio, avoid running out of money at the end.",
        "Use browser localStorage to save drafts, enter multiple times; screenshot/export backup before changing devices.",
        "Example (hard decor 8 + main material 12 + furniture 5 + appliances 4, unit: 10,000 CNY)",
        "Total 290,000 CNY; share hard decor 27.6%, main material 41.4%, furniture 17.2%, appliances 13.8%. If the total cap is 300,000 CNY, main material is near the ceiling; compress or lower the appliance tier.",
        "How to read each share as healthy?",
        "Common ranges: hard decor 25-35%, main material 30-45%, furniture 15-25%, appliances 10-20%. Main material >45% or hard decor <20% are both unbalanced; the former squeezes soft decor, the latter may hide extra items.",
        "Where is the data stored, will it be lost?",
        "Stored only in browser localStorage (isolated by domain); clearing cache/changing browser loses it. Important budgets screenshot or export yourself; this tool does not network, does not upload.",
        "About 'Renovation Budget'",
        "e.g.: kitchen cabinet",
    ]
    mp = build('renovation-budget', en); write('renovation-budget', mp)

    # ===== room-calculator (16) =====
    en = [
        "📐 Room Area Calculator",
        "Supports area and perimeter calculation for rectangular, L-shape, trapezoid, circular, triangular and other shapes",
        "/ Room Area Calculator",
        "📖 View the usage guide for Room Area Calculator",
        "Area and perimeter by shape formulas: rectangle = length × width, perimeter = 2 × (length + width), diagonal = √(length² + width²); L-shape = large rectangle area − missing rectangle area; trapezoid = (upper base + lower base) × height ÷ 2; triangle = base × height ÷ 2; circle = π × radius², perimeter = 2πr; usage estimate by area × (1 + loss rate 5% to 10%) to convert tiles or wallpaper usage.",
        "📚 Deep Dive: Room Area Calculator",
        "Rectangular room length × width gives area directly, then divide by tile single area (800×800=0.64 m²) to estimate count and add loss.",
        "L-shape split into two rectangles and sum; trapezoid uses (upper base + lower base) × height ÷ 2; circle uses πr²; each fits different layouts.",
        "Irregular room uses 'bounding box − notch' approximation, or block accumulation, to quickly estimate wallpaper/floor usage.",
        "Example (rectangle 4×3.5 m / L-shape)",
        "Rectangle 4×3.5=14 m², 800×800 tile 0.64 m²/piece → 14÷0.64≈22 pieces, +5% loss ≈ 23 pieces. L-shape = 3×2 + 2×1.5 = 6+3 = 9 m². Perimeter is for wall painting/baseboard: rectangle perimeter = 2×(length+width).",
        "How much loss to add?",
        "Floor tile 5%, wall tile 8-10% (more cutting), wallpaper 10-15%; irregular room takes high value. This tool gives net area; loss added separately at purchase.",
        "What is perimeter used for?",
        "Wall painting, baseboard, corner line all by perimeter × ceiling height (or line width). Rectangle perimeter = 2×(length+width), L-shape sums each outer contour segment.",
        "About 'Room Area Calculator'",
    ]
    mp = build('room-calculator', en); write('room-calculator', mp)

    # ===== washer-capacity (22) =====
    en = [
        "/ Washer Capacity Selector",
        "📖 View the usage guide for washer-capacity",
        "🧊 Washer Capacity Selector",
        "How to choose washer capacity? Recommend 5-10 kg range by household size, and judge whether larger capacity is needed by bulky bedding/curtains, with single-use water estimate.",
        "Washer capacity recommendation by household size and laundry: single 3-5 kg, 2-3 people 6-7 kg, 4-5 people 8-9 kg, 5+ people 10 kg; when washing bedding or curtains, capacity floats up about 2 kg (a double duvet spread occupies about 4-5 kg capacity); single-use water about capacity(kg) × 10-15 L (pulsator higher, drum lower); selection suggestion by daily need × 1.2 reserve margin.",
        "Often wash bulky items (sheets/duvet covers/curtains)",
        "Drum",
        "Pulsator",
        "📚 Deep Dive: Washer Capacity Selection",
        "Three-person family choose 7-8 kg; often wash sheets/duvet covers need ≥8 kg, ensure winter duvet washed once without tangling.",
        "Five-person / large household choose 10 kg; bulky items like curtains ≥9 kg washed in one go, reducing batches.",
        "Water-sensitive families: drum about 9 L/kg, pulsator about 30 L/kg, same capacity pulsator uses about 3× water.",
        "Example (4-person family, often wash bulky items)",
        "4-person → baseline 8-9 kg; often wash winter duvet/curtains → take 9 kg. Drum 9 L/kg×9=81 L/time, pulsator 30×9=270 L/time; if washed 20 times a month, drum saves (270-81)×20=3780 L/month vs pulsator.",
        "Capacity by household or by load?",
        "First baseline by household: 1-2 people 5-6 kg, 3 people 7-8 kg, 4 people 8-9 kg, 5+ people 10 kg; then raise by bulky items (sheets/duvet covers ≥8 kg, curtains ≥9 kg).",
        "Drum or pulsator?",
        "Drum saves water and protects clothes, but costs more; pulsator is cheaper and uses more water, less cloth damage. Small units check water pressure and install space; bulky-item households choose large-capacity drum; renters/low-frequency choose pulsator more cost-effective.",
        "Capacity reference: 1-2 people 5-6 kg, 3 people 7-8 kg, 4 people 8-9 kg, 5+ people 10 kg",
        "Often wash sheets/duvet covers suggest ≥8 kg, curtains and other bulky items ≥9 kg",
        "Drum about 9 L/kg, pulsator about 30 L/kg water usage differs obviously",
        "Results are for reference only, choose by install space and budget",
    ]
    mp = build('washer-capacity', en); write('washer-capacity', mp)

if __name__ == '__main__':
    main()
