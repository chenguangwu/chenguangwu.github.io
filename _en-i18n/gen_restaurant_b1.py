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
    write('delivery-time', build('delivery-time', [
        '🔮 Food Delivery Time Estimator',
        'Estimate food delivery time from distance and speed, covering prep, pickup and drop-off stages',
        'Core formula (from input variables): (distance÷speed)×60; Math.round(totalTime-5); Math.round(totalTime+5)',
        '/ Food Delivery Time Estimator',
        '📖 Read the "Food Delivery Time Estimator User Guide"',
        '🔮 Estimated time',
        '⏱️ Delivery time estimate',
        '📚 Deep dive: segmented food delivery time estimation',
        'Before the merchant promises a delivery SLA, split the total duration into four segments - prep, rider arrival, road time and doorstep - and give a ±5 minute window.',
        'Raise the coefficients during lunch/dinner peaks and in bad weather, and inform customers early to reduce chasing and negative reviews.',
        'Compare in-house delivery with platform delivery times to decide whether to cap orders during peak hours.',
        'One order: 3 km, rainy lunch peak',
        'Distance 3 km, rider speed 20 km/h → baseline riding = 3÷20×60 = 9 minutes. Traffic "normal" ×1.3, weather "light rain" ×1.2, period "lunch peak" ×1.2 → combined coefficient 1.87, adjusted riding = 9×1.87 ≈ 16.9 minutes. Add prep 12 minutes, rider pickup 3 minutes, elevator and upstairs 4 minutes → total about 36 minutes, promised window 31-41 minutes. If traffic changes to "severe congestion" ×2.5, riding rises to 32.4 minutes and total time to about 51 minutes, at which point you should cap orders or warn customers in advance.',
        'What do the three coefficients mean?',
        'Traffic (clear 1.0 / normal 1.3 / slightly congested 1.6 / congested 2.0 / severe congestion 2.5), weather (clear 1.0 / cloudy 1.1 / light rain 1.2 / heavy rain 1.4 / snow 1.5) and period (off-peak 1.0 / lunch and dinner peak 1.2 / night 0.9) are multiplied together to give the combined coefficient; it applies only to riding time and does not affect prep time.',
        'Why does the estimate differ from what the platform shows?',
        'This tool does segmented estimation purely from your parameters and excludes platform dispatch distance, pickup queueing and bundled orders along the way. Calibrate speed and coefficients once against your own order history.',
        'About "Food Delivery Time Estimator"',
    ]))

    write('dish-cost-card', build('dish-cost-card', [
        '💰 Dish Standard Cost Card Generator',
        'Enter ingredients and quantities to auto-calculate dish cost and generate a standard cost card',
        '"Enter ingredients and quantities to auto-calculate dish cost and generate a standard cost card" is computed from the input parameters and returns the result.',
        '/ Dish Standard Cost Card Generator',
        '📖 Read the "Dish Standard Cost Card Generator User Guide"',
        '📊 Cost card',
        '📚 Deep dive: dish standard cost card',
        'Enter each ingredient quantity and purchase unit price to get the per-portion cost and cost ratio, which underpin pricing and gross-margin accounting.',
        'Work backwards from the yield rate (net weight ratio) to net dish cost, avoiding under-priced dishes caused by underestimated shrinkage.',
        'Print the cost card for the kitchen as the baseline for ingredient issue and stocktaking.',
        'Kung Pao Chicken cost card (4 portions)',
        'Chicken thigh meat 500 g × 24 CNY/kg = 12.00 CNY; peanuts 80 g × 30 CNY/kg = 2.40 CNY; dried chili 15 g × 40 CNY/kg = 0.60 CNY; seasonings total 3.00 CNY. Raw ingredient total 18.00 CNY, yield rate 90% → net ingredient cost = 18.00 ÷ 0.90 = 20.00 CNY; portions 4 → per-portion cost 5.00 CNY. At a selling price of 38 CNY the cost ratio is 13.2%,',
        'and 86.8% is left for gross profit. If the yield rate is wrongly taken as 100%, the per-portion cost is underestimated by 0.50 CNY.',
        'How do g / ml and kg / L convert?',
        'When you enter in g or ml, the tool automatically converts the unit price by ÷1000 (i.e. enter the unit price as "CNY/kg" or "CNY/L"); when you enter in kg / L the tool directly uses',
        'quantity × unit price',
        'What yield rate should I fill in?',
        'Yield rate = net weight ÷ gross weight. Meat after deboning and skinning is usually 70-90%, vegetables after trimming and washing 60-85%. If unsure, start with 85%, then weigh after processing and come back to correct it.',
        'About "Dish Standard Cost Card Generator"',
    ]))

    write('index', build('index', [
        '🍽️ Restaurant Operations Tools',
        'Restaurant Operations',
        'Restaurant Operations Tools',
        'Dish Pricing Calculator',
        'Online dish pricing calculator: enter ingredient cost, target gross margin and taxes to back out the recommended selling price and estimate profit headroom, helping restaurant owners price scientifically, control margins, and run purely in the browser.',
        'Enter each dish ingredient, spec quantity and purchase unit price; the tool automatically computes per-portion cost and cost ratio and can generate a standard cost card, helping restaurants verify selling prices, control margins and count ingredients.',
        'Enter delivery distance, average rider speed and prep and pickup time; the tool estimates in segments the total time from order acceptance to drop-off and gives period volatility hints, so merchants can promise SLAs and optimize output and rider dispatch.',
        'Seasoning ratio scaler: enter the original recipe quantities and target servings to scale every seasoning proportionally while keeping the flavor balance, suitable for household and restaurant batch prep conversion.',
        'Enter business hours, table count and average dining time; the tool computes the table turnover rate and receivable guest flow, and grades them, helping restaurants spot queue bottlenecks and boost seat turnover by adjusting table assignment or time limits.',
        'Enter the cost and selling price of each dish; the tool computes gross margins, ranks them, and charts the menu profit structure so you can spot low-margin slow movers and adjust pricing or mix to raise overall profit.',
        'Record customer ratings and choices for salty, sweet and spicy preferences locally in the browser; the tool aggregates them into a preference distribution chart (data never leaves the browser) to help you read customer tastes and iterate the menu and new items.',
        'Enter average daily usage, lead time and demand fluctuation to compute ingredient safety stock, reorder point and economic order quantity (EOQ), balancing stockout against overstock risk for smarter replenishment.',
        'About "Restaurant Operations Tools"',
        'This Restaurant Operations Tools collection gathers 8 free online tools covering the common calculation, conversion and lookup needs of restaurant operations. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs purely in the browser; no data is uploaded to the server, so your privacy and security are protected.',
        'Restaurant operations tools included on this page (representative tools only):',
        'These tools help you finish common restaurant operations tasks fast, with no need to memorize complex formulas or convert by hand - input and you get the result.',
        'Do the Restaurant Operations Tools require downloads or registration?',
        'No. All Restaurant Operations Tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register, and no data uploaded.',
        'Are the Restaurant Operations Tools results accurate, and is the data safe?',
        'The tools compute in your browser using public math formulas and common industry standards, so results are available instantly. All computation happens locally on your device; no data is uploaded to the server, so privacy and security are guaranteed.',
    ]))


if __name__ == '__main__':
    main()
