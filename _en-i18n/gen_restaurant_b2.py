#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'restaurant')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'restaurant')
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
    out = {'slug': slug, 'industry': 'restaurant', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('menu-margin', build('menu-margin', [
        '🏦 Menu Gross Margin Analysis',
        'Enter dish cost and selling price to compute gross margin and analyze by ranking on margin',
        'Core formula (from input variables): max(d.margin÷maxMargin×100,5)',
        '/ Menu Gross Margin Analysis',
        '📖 Read the "Menu Gross Margin Analysis User Guide"',
        'Gross margin ↓',
        'Gross profit ↓',
        'Selling price ↓',
        'Cost ↑',
        '📈 Gross Margin Analysis',
        '📚 Deep dive: menu gross margin structure analysis',
        'Enter the cost and selling price of each menu item, then rank',
        'them to spot "high-volume low-margin" risk dishes.',
        'Before quarterly repricing, check overall gross margin and the per-dish gross profit distribution to decide whether to raise prices or substitute ingredients.',
        'Benchmark a new item against the gross margin of comparable dishes before launch so it does not drag down overall profitability.',
        'Gross margin comparison of three dishes',
        'A cost 12 / price 38 → gross profit 26 CNY, margin 68.4%; B cost 18 / price 48 → gross profit 30 CNY, margin 62.5%; C cost 25 / price 58 → gross profit 33 CNY, margin 56.9%. Totals: revenue 144 CNY, cost 55 CNY, gross profit 89 CNY, blended margin 61.8%. C has the highest gross profit (33 CNY) but the lowest margin; if it also sells the most, the blended margin is pulled below 61.8%, so its cost or price should be optimized first.',
        'Should I look at gross margin or gross profit?',
        'Use gross margin for structure (it reflects pricing and cost control) and gross profit for contribution (it reflects what you actually earn). A low-profit high-margin dish does not make money; a high-profit low-margin dish may be the real profit driver - judge both together with sales volume.',
        'No. Dish records stay valid only on the current page and are cleared on refresh. For long-term tracking, copy or export the results and store them separately.',
        'About "Menu Gross Margin Analysis"',
    ]))

    write('menu-pricing', build('menu-pricing', [
        '💰 Dish Pricing Calculator',
        'Estimate the recommended selling price from ingredient cost and target gross margin.',
        '/ Dish Pricing Calculator',
        '📖 Read the "menu-pricing User Guide"',
        'Dish pricing: total cost = ingredient cost × (1 + labor share) + fixed cost allocation; recommended price = total cost ÷ (1 - target margin); gross profit = price - total cost; gross margin = (price - total cost) ÷ price × 100%; tax-inclusive price = price × (1 + tax rate).',
        'Ingredient cost (CNY)',
        'Labor cost share (%)',
        'Fixed costs such as rent / utilities (CNY)',
        'Target gross margin (%)',
        'Estimated price',
        '📚 Deep dive: dish pricing (back-solving from target margin)',
        'Given ingredient cost, labor share and allocated fixed cost, back-solve the recommended selling price from the target',
        'gross margin.',
        'Recompute the price after costs rise, to see how much of a price increase is needed to preserve the original margin.',
        'Compare prices under different margin targets to gauge customer price acceptance.',
        'Pricing at a 65% target margin',
        'Ingredient cost 18 CNY, labor share 20%, fixed cost allocation 6 CNY, target margin 65%: total cost = 18×(1+20%) + 6 = 27.60 CNY; recommended price = 27.60 ÷ (1-65%) = 78.86 CNY; gross profit per portion = 78.86 - 27.60 = 51.26 CNY. If the target margin drops to 60%, price = 27.60 ÷ 0.40 = 69.00 CNY, about 10 CNY cheaper but gross profit falls by 9.86 CNY.',
        'Why not "cost × (1 + margin)"?',
        'Restaurant gross margin is normally defined on the revenue basis: margin = (price - cost) ÷ price. So price = cost ÷ (1 - margin), not cost × (1 + margin). Using the latter understates the margin.',
        'How should fixed costs be allocated?',
        'Divide monthly fixed expenses such as rent, utilities and depreciation by the estimated monthly sales volume to get the amount allocated per portion, then enter that. The higher the estimated volume, the lower the per-portion allocation and the price, so estimate conservatively.',
    ]))

    write('safety-stock', build('safety-stock', [
        '🏬 Ingredient Safety Stock Alert',
        'Compute safety stock, reorder point and economic order quantity (EOQ) to avoid stockouts and overstock',
        'Core formula (from input variables): max(0,maxDaily×maxLead-avgDaily×avgLead); sqrt(2 × D × S ÷ H)',
        '/ Ingredient Safety Stock Alert',
        '📖 Read the "Ingredient Safety Stock Alert User Guide"',
        '🏬 Compute stock',
        '📊 Stock analysis',
        '📚 Deep dive: ingredient safety stock and EOQ',
        'Derive safety stock and the reorder point from average/max daily usage and arrival lead time, avoiding stockouts and overstock.',
        'Use EOQ to find',
        'the economic order lot',
        'and order interval, balancing ordering cost against holding cost.',
        'After entering current stock, the tool judges the status automatically: below safety stock, at reorder point, or stock sufficient.',
        'Safety stock for a main ingredient at 20 kg/day',
        'Average 20 kg/day, max daily use 30 kg, average lead time 3 days, max lead time 5 days: safety stock = 30×5 - 20×3 = 90 kg; reorder point = 20×3 + 90 = 150 kg. Annual demand = 20×360 = 7,200 kg; ordering cost 50 CNY per order, annual holding cost 12 CNY per unit → EOQ = √(2×7,200×50÷12) ≈ 245 kg, about 30 orders a year, interval about 12 days. With 45 kg on hand you have about 2 days of cover and are below safety stock, so reorder immediately.',
        'Why is safety stock "max" minus "average"?',
        'Safety stock must cover the worst case where "usage is higher than usual and arrival is slower than usual" happen at the same time, so it uses max daily usage × max lead time minus average daily usage × average lead time. If the two are close, supply and demand are both stable and safety stock is naturally low.',
        'Is the EOQ result always optimal?',
        'EOQ assumes constant demand, a fixed unit price and no stockouts. Fresh ingredients have shelf lives and price swings, so treat EOQ as a reference lot size and adjust it for shelf life and minimum order quantity.',
        'About "Ingredient Safety Stock Alert"',
    ]))


if __name__ == '__main__':
    main()
