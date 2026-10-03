#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hotel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hotel')
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
    out = {'slug': slug, 'industry': 'hotel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('currency-exchange', build('currency-exchange', [
        '💱 Currency Exchange (Manual Rate)',
        'Enter the rate manually to convert, supporting bidirectional conversion and a quick reference table',
        'Core formula (from input variables): amount × fee ÷ 100; needed × fee ÷ 100',
        'Currency exchange',
        '/ Currency Exchange',
        '📖 Read the "Currency Exchange (Manual Rate) User Guide"',
        'Source currency',
        'Target currency',
        'Rate (1 source = ? target)',
        'Exchange amount',
        'Source → Target',
        'Target → Source',
        '⇅ Swap',
        'Quick reference for common amounts',
        '💡 Currency exchange tips',
        'Getting the rate:',
        'Use the live quote from a bank counter or an authoritative forex platform, then enter it manually',
        'Cash vs remittance:',
        'The bank cash buying rate is usually lower than the remittance buying rate',
        'Fees:',
        'Bank exchange usually has no extra fee, while airports and hotels have a wide spread',
        'Bidirectional conversion:',
        'There is a spread between the bid and ask rates, so round-trip conversion loses value',
        '📚 Deep dive: currency exchange (manual rate)',
        'Before travel abroad or shopping overseas, manually enter the live bank or platform rate to convert local currency into the target currency and estimate offline how much you can get, without being misled by vague counter quotes.',
        'When comparing two exchange channels (bank quote vs airport or merchant), enter the rate and fee for each to compute the net amount and pick the better one.',
        'Holding multiple currencies, convert bidirectionally with "1 source = ? target" to build a quick reference table for fast mental math on small purchases.',
        'Worked example (10,000 CNY → USD)',
        'Entering rate 1 CNY=0.138 USD and fee 0%: net = 10,000×0.138×(1-0) = 1,380 USD. If the channel charges 1.5% fee: net = 10,000×0.138×0.985 = 1,359.3 USD, and the 20.7 USD difference is the fee cost. In reverse USD→CNY use rate 1/0.138≈7.246, so 100 USD≈724.6 CNY. Note: the rate depends on the live quote you enter; bank buy and sell rates differ, and the actual net amount uses the cash buying rate.',
        'Which rate should I enter?',
        'Use the "ask rate" of your actual exchange channel (the price at which you buy foreign currency with local currency); if you found the mid rate, the net amount is slightly lower. Cash and remittance quotes also differ, and the cash buying rate is lower.',
        'Why does it differ from what my mobile banking app shows?',
        'This tool is purely front-end and the result depends entirely on the rate and fee you enter, with no hidden spread; differences from a bank app come from quote timing and buy/sell direction, not from a calculation error.',
        'About "Currency Exchange"',
        'The Currency Exchange tool completes conversion calculations by manually entering the rate, supporting bidirectional conversion, fee deduction and a quick reference table of common amounts.',
        'Manual rate entry, works offline',
        'Supports bidirectional conversion and swap',
        'Automatic fee calculation',
        'Quick reference table for common amounts',
        'Currency conversion for travel',
        'Overseas shopping cost calculation',
        'Cross-border spending estimates',
        'Exchange rate learning',
    ]))

    write('luggage-weight', build('luggage-weight', [
        '⚖️ Luggage Weight Recommendation',
        'Recommend luggage weight by trip length and travel type, with a reference table of common airline checked-baggage allowances',
        '📖 Read the "Luggage Weight Recommendation User Guide"',
        'Recommended luggage weight = base weight 4.5 kg + daily increment × trip days; the daily increment by travel type is: business 0.9, leisure 1.3, backpack 0.7, winter 1.8 kg; then adjust by gender and number of children traveling together; economy checked baggage is usually limited to 20 to 23 kg and carry-on to 7 to 10 kg, with overweight fees charged per airline rules.',
        'Travel type',
        'Leisure travel',
        'Backpack hiking',
        'Winter travel',
        'Traveling with children items?',
        '✈️ Free checked baggage allowance reference for common airlines',
        'Airline / cabin',
        'Checked pieces',
        'Per-piece weight limit',
        'Carry-on weight limit',
        'Domestic economy',
        '1 piece',
        'Domestic business class',
        'International economy (Asia routes)',
        '1-2 pieces',
        'International economy (US routes)',
        '2 pieces',
        'International business class',
        '2-3 pieces',
        'Low-cost airline (no free checked baggage)',
        '0 pieces',
        'Must purchase',
        'Note: airline policies differ; the above is a common reference, please follow the airline rules at the time of purchase.',
        '📚 Deep dive: luggage weight recommendation',
        'Before departure, estimate the total carry-on plus checked weight from days, type (business/leisure/outdoor), gender and transport mode, then compare against airline limits to judge whether overweight fees apply.',
        'Outdoor and skiing gear is heavy, so calculate the checked range in advance to avoid being forced to split bags or pay excess fees on site.',
        'With multi-leg transport (plane + train + self-drive), work backward from the strictest checked allowance to determine how much you can bring.',
        'Worked example (female, 5 days leisure, domestic flight)',
        'Leisure 5-day baseline: checked 15-23 kg, carry-on 7-10 kg; gender adjustment female -2 kg → checked 13-21 kg, carry-on 5-8 kg. Airline economy free checked allowance is typically 20-23 kg (varies domestic vs international), so keep checked at ≤23 kg to avoid fees; carry-on 5-8 kg fits cabin bag limits (most airlines 5-10 kg). Outdoor baselines are higher (checked 20-30 kg); if over 23 kg, buy excess allowance in advance or split into two bags.',
        'Which checked allowance governs?',
        'Use the free allowance printed on your airline ticket (economy is commonly 20-23 kg per piece, low-cost 0-15 kg varies); this tool gives an empirical range, and the final answer is the baggage allowance of your flight. Excess is charged at airline rates, and buying allowance in advance is cheaper than on the day.',
        'How do I split carry-on and checked?',
        'Put valuables, urgent items and over-limit liquids in checked baggage; keep documents, power banks, common medicine and a change of clothes on board. Cabin bags face both weight and size limits, and an oversized bag may be checked even when it is not overweight.',
        'About "Luggage Weight Recommendation"',
        'The Luggage Weight Recommendation tool recommends total luggage weight and the checked / carry-on split by trip length, travel type and gender, and includes a reference table of common airline checked allowances.',
        'Multi-dimension personalized recommendation',
        'Smart checked / carry-on allocation',
        'Airline allowance reference table',
        'Pre-trip packing planning',
        'Avoid excess baggage fees',
        'Business / leisure travel preparation',
        'International flight baggage estimates',
    ]))

    write('tip-calculator', build('tip-calculator', [
        '🧮 Tip Calculator',
        'Compute the tip, total and per-person split from the bill amount and tip percentage',
        '📖 Read the "Tip Calculator User Guide"',
        'Tax amount = bill × tax rate; tip amount = bill × tip percentage (North America commonly 15%, 18%, 20%, choose by service level); amount payable = bill + tax + tip; per-person split = amount payable ÷ number of diners, for quick estimates when dining abroad.',
        'Bill amount',
        'Tip percentage (%)',
        'Tax rate (%, shown for reference only)',
        '🌍 Tipping customs by country',
        'Restaurant tipping',
        'Almost mandatory; below 15% is viewed as dissatisfaction',
        'Similar to the US',
        'Some restaurants already include a service charge',
        'Included',
        'The bill includes a 15% service charge; extra cash is optional',
        'Do not tip',
        'Tipping may be considered offensive',
        'Tipping usually not needed',
        'Fine at upscale restaurants, just leave some cash',
        'Not mandatory, common at upscale restaurants',
        '📚 Deep dive: tip calculator',
        'Before dining abroad, compute the tip, the total including tip and the per-person split from local tipping custom (percentage or fixed) so you are never caught guessing on site.',
        'When splitting a group bill, fold the tip into the per-person amount and quote each person directly to reduce arguing.',
        'Compare the "by percentage" and "by service level preset" approaches and pick an amount that matches local custom without looking stingy.',
        'Worked example (4-person meal, 800 CNY, 15% tip)',
        'Tip = amount × rate = 800×15% = 120 CNY; total including tip = 800+120 = 920 CNY; per person = 920/4 = 230 CNY. If local custom is 18%: tip = 144, total = 944, per person = 236. When switching currencies, convert the amount to local currency at the current rate first to avoid a currency mismatch.',
        'What tip percentage do countries use?',
        'US dine-in 15-20% (higher for good service), bars around 1-2 USD per drink; Japan and Korea usually do not tip; European restaurant bills often include service (look for "service compris"), so extra cash is enough. Follow destination custom; this tool only does the math, not the etiquette advice.',
        'Should I still tip if service charge is already added?',
        'When the bill states "service charge included / service charge", usually no extra tip is needed; if the service was excellent you may leave some cash. The tip in this tool is computed independently from the rate you enter, and whether to stack them is your call.',
        'About "Tip Calculator"',
        'The Tip Calculator tool quickly computes tips, total payment and per-person splits from the bill amount and tip percentage, with quick preset ratios and a reference table of tipping customs by country.',
        'One-click preset ratios',
        'Automatic per-person split',
        'Supports tax reference',
        'Tipping customs reference table by country',
        'Dining cost calculation abroad',
        'Group bill splitting',
        'Hotel service tips',
        'Learning tipping etiquette',
    ]))


if __name__ == '__main__':
    main()
