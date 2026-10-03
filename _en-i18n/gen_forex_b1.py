#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'forex')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'forex')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'forex', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    # ===== cross-rate (41) =====
    write('cross-rate', build('cross-rate', [
        'Cross Rate Calculator',
        'Compute the cross rate between two non-USD currency pairs via the USD intermediate rate.',
        '“Compute the cross rate between two non-USD currency pairs via the USD intermediate rate” performs a professional calculation from the inputs and outputs the result.',
        '/ Cross Rate',
        'View the Cross Rate Calculator User Guide',
        'Base currency (the currency to convert)',
        'EUR Euro',
        'GBP Pound',
        'JPY Yen',
        'CHF Franc',
        'CAD Dollar',
        'AUD Dollar',
        'CNY Yuan',
        'USD Dollar',
        'Quote currency (target currency)',
        '1 base currency = ? USD',
        '1 quote currency = ? USD',
        'Amount to convert (base currency)',
        'Swap currencies',
        'Cross Rate Formula',
        'Cross rate',
        '= (base to USD) ÷ (quote to USD)',
        'i.e. A/B = (A/USD) ÷ (B/USD)',
        'Converted amount',
        '= amount × cross rate',
        'Common Cross Rate Examples',
        'Cross pair',
        'USD Rate Reference (example)',
        'This tool takes each currency’s rate to USD (how many USD per 1 unit). For USD-based currencies like JPY, convert to how many USD per 1 unit.',
        'Deep Dive: Cross Rate Calculator',
        'Convert a non-USD pair (e.g. EUR/JPY): given EUR/USD and USD/JPY, derive the cross quote directly, skipping the mental USD pivot.',
        'Cross-border e-commerce and study-abroad exchange: compare bank rates with the cross rate to judge which exchange path is cheaper.',
        'Multi-currency bookkeeping: unify minor-currency amounts into a base currency (USD or CNY) for asset tallying.',
        'Cross rate = base to USD ÷ quote to USD. I.e. (Base/USD) ÷ (Quote/USD) = Base/Quote; amount conversion = amount × cross rate; USD equivalent = amount × base to USD.',
        'Enter EUR/USD=1.0850, USD/JPY=0.00665 (i.e. 1 USD=150.38 JPY, JPY/USD=0.00665), amount=1000 EUR: cross rate EUR/JPY = 1.0850 ÷ 0.00665 = 163.1579, i.e. 1 EUR≈163.1579 JPY; converted 1000×163.1579=163157.89 JPY; USD equivalent=1000×1.0850=1085.00 USD.',
        'How does it differ from quoting EUR/JPY directly from the market?',
        'The cross rate is derived from two USD legs; versus a broker’s direct EUR/JPY quote there is usually a tiny spread (from bid/ask and liquidity); this tool uses the mid price to demonstrate the principle — for live trading use the broker’s quote.',
        'Can the result be used directly in live trading?',
        'No. This tool is a pure calculation demo; rates are entered manually and no live quotes are fetched. For real orders use your platform’s live bid/ask and contract specs.',
        'About the Cross Rate Calculator',
        'Cross Rate Calculator - compute cross rates via USD, an online FX rate conversion tool, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.',
    ]))

    # ===== leverage-calc (35) =====
    write('leverage-calc', build('leverage-calc', [
        'FX Leverage Calculator',
        'Compute the required margin, leverage multiple, and liquidation risk of FX trades.',
        'Core formulas (by input variable): lots × 100000 × baseUsdRate; balance × stopOut ÷ 100',
        '/ Leverage Calculation',
        'View the FX Leverage Calculator User Guide',
        'Base currency',
        'Base currency to USD rate',
        'Stop-out ratio (%)',
        'Position value',
        '= lots × 100,000 × base-to-USD rate',
        'Required margin',
        '= position value ÷ leverage',
        'Margin usage ratio',
        '= required margin ÷ account balance × 100%',
        'Liquidation price move',
        '= (account balance × stop-out ratio − required margin) ÷ position value × 100%',
        'Leverage and Risk',
        'Leverage',
        'Margin ratio',
        'Low (conservative)',
        'Medium (common)',
        'Higher leverage means greater liquidation risk. At 1:100, about a 1% adverse move can trigger liquidation. Beginners are advised not to exceed 1:50.',
        'Deep Dive: FX Leverage Calculator',
        'Estimate margin usage before opening: given lots, contract size, and leverage, compute required margin and margin usage to avoid over-sizing and forced liquidation.',
        'Risk control: under account-balance and stop-out constraints, back-calculate how much adverse price move',
        'would trigger a forced liquidation.',
        'Position planning: compare capital efficiency and liquidation risk across leverages (e.g. 1:50 vs 1:500) to pick a suitable multiple.',
        'Position value = lots × 100000 × base-to-USD rate; required margin = position value ÷ leverage; margin usage = margin ÷ balance × 100%; free margin = balance − margin; loss buffer to liquidation = free margin − balance×StopOut%; liquidation price move% = loss buffer ÷ position value × 100%.',
        'Input 1 lot, leverage 1:100, base-to-USD=1, balance=10000, StopOut=50%: position value=1×100000×1=100000; margin=100000÷100=1000 (usage 10%); free margin=9000; liquidation threshold=10000×50%=5000, loss buffer=9000−5000=4000; adverse move 4000÷100000×100%=4% triggers liquidation.',
        'Is higher leverage better?',
        'No. High leverage amplifies capital efficiency but also loss speed; in this example just 4% adverse move liquidates — pick a multiple with stop-loss and account tolerance in mind.',
        'At what margin usage is it dangerous?',
        'The closer usage is to 100% the more dangerous; when equity falls below the broker’s Stop Out level (commonly 20%–50%) you get force-closed — keep ample free margin.',
        'About the FX Leverage Calculator',
        'FX Leverage Calculator - compute leverage and margin, an online FX risk-management tool, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.',
    ]))

    # ===== lot-size (36) =====
    write('lot-size', build('lot-size', [
        'FX Lot Size Calculator',
        'Compute a suitable lot size from account funds and stop-loss pips.',
        'Core formulas (by input variable): balance × riskPct ÷ 100; min(calcLots, maxLots)',
        '/ Lot Size Calculation',
        'View the FX Lot Size Calculator User Guide',
        'Stop-loss pips',
        'Take-profit pips (optional)',
        'Max lot limit',
        'Lot Size Formula',
        'Risk amount',
        '= account balance × risk ratio',
        'Value per pip per lot',
        '= 100000 × pip size ÷ quote-to-USD rate',
        'Suggested lots',
        '= risk amount ÷ (stop-loss pips × value per pip per lot)',
        'Risk-reward ratio',
        '= take-profit pips ÷ stop-loss pips',
        'Risk Management Suggestions',
        'Risk per trade',
        'Steady, good for beginners',
        'Common standard',
        'Aggressive',
        'Very high liquidation risk',
        'A reasonable risk-reward ratio is at least 1:2. This tool sizes lots by the maximum loss when the stop is hit.',
        'Deep Dive: FX Lot Size Calculator',
        'Size by risk budget: given account funds, per-trade risk ratio, and stop-loss pips, back-calculate the lots so each stop loss is fixed and controlled.',
        'Risk-reward planning: with target take-profit pips, compute potential profit and the risk-reward ratio (R multiple) to filter setups matching your strategy.',
        'Multi-instrument fit: different pairs have different pip values (e.g. USD/JPY one pip=0.01); the lot size auto-converts by the selected pair’s pip value.',
        'Risk amount = balance × risk ratio%; pip value/lot = 100000 × pip size ÷ quote-to-USD; risk per lot = stop-loss pips × pip value/lot; suggested lots = risk amount ÷ risk per lot (subject to max-lot limit); actual loss = suggested lots × risk per lot; potential profit = target pips × suggested lots × pip value/lot; risk-reward = target pips ÷ stop-loss pips.',
        'Account 10000, risk 2%, EURUSD (pip size 0.0001), stop 50 pips, quote-to-USD=1, target 100 pips, max 10 lots: risk amount=200; pip/lot=100000×0.0001÷1=10; risk per lot=50×10=500; suggested lots=200÷500=0.40 lots; actual loss=0.4×500=200 (2% risk); potential profit=100×0.4×10=400; risk-reward=2.',
        'Why divide pip value by the quote-to-USD rate?',
        'A standard lot is 100,000 units of base currency; times pip size gives the pip value in quote currency, then divided by quote-to-USD to express the risk in the account settlement currency (USD).',
        'What if the suggested lots are capped by the max-lot limit?',
        'It means per-trade risk is too large for the account or the stop is too wide; reduce the risk ratio, tighten the stop, or accept a smaller position — never exceed the max-lot limit just to fill the account.',
        'About the FX Lot Size Calculator',
        'FX Lot Size Calculator - compute trade lots by risk, an online FX money-management tool, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.',
    ]))

    # ===== pip-calc (50) =====
    write('pip-calc', build('pip-calc', [
        'FX Pip Value Calculator',
        'Compute the pip value and profit/loss for different currency pairs.',
        'Core formulas (by input variable): pipValueUsd × 7.25; lots × 100000',
        '/ Pip Value Calculation',
        'View the FX Pip Value Calculator User Guide',
        'EUR/USD (Euro-Dollar)',
        'GBP/USD (Pound-Dollar)',
        'USD/JPY (Dollar-Yen)',
        'USD/CHF (Dollar-Franc)',
        'AUD/USD (Aussie-Dollar)',
        'USD/CAD (Dollar-Loonie)',
        'NZD/USD (Kiwi-Dollar)',
        'EUR/JPY (Euro-Yen)',
        'GBP/JPY (Pound-Yen)',
        '0.01 lot (micro)',
        '0.1 lot (mini)',
        '1 lot (standard)',
        '5 lots',
        '10 lots',
        'Quote-to-USD rate (fill if not USD)',
        'Pips moved',
        'Account currency',
        'CNY (Yuan)',
        'Pip Value Formula',
        '1 standard lot',
        '= 100,000 units of base currency',
        'Pip value (quote currency)',
        '= lots × 100000 × pip size',
        'Pip value (USD)',
        '= pip value (quote currency) ÷ quote-to-USD rate',
        'For pairs quoted in USD (e.g. EUR/USD), the pip value is directly in USD',
        'For pairs quoted in JPY, one pip = 0.01',
        'Pip Size Reference',
        'Pair type',
        'Pip size',
        'USD as quote currency',
        'JPY as quote currency',
        'Pip value changes with the live rate (when quote currency is not USD). Positive pips mean profit, negative means loss.',
        'Deep Dive: FX Pip Value Calculator',
        'Position P/L estimate: given lots, pips, and rate, compute pip value and total P/L to quickly gauge position risk exposure.',
        'Account currency switch: toggle between USD and CNY settlement, showing pip value and P/L in the local currency at a fixed rate (USD→CNY=7.25).',
        'Strategy backtest: plug in historical pips moved to estimate the P/L size per trade at different lot sizes.',
        'Contract units = lots × 100000; quote-currency pip value = contract units × pip size; USD pip value = quote-currency pip value ÷ quote-to-USD; if account is CNY then CNY pip value = USD pip value × 7.25; total P/L = pip value × pips.',
        'EURUSD, 1 lot, rate 1.0850, quote-to-USD=1, pips 50, account USD: contract units=100000; quote pip value=100000×0.0001=10; USD pip value=10÷1=10 ($10 per pip); P/L=10×50=500 USD. If account is CNY: pip value=10×7.25=72.5 yuan, P/L=72.5×50=3625 yuan.',
        'Why use a fixed 7.25 for USD→CNY?',
        'This tool is an offline demo using a fixed 7.25 rate for illustration; for real exchange use bank live rates — rate changes affect the CNY-denominated pip value.',
        'Why do JPY pairs have different pip values?',
        'For pairs quoted in JPY like USD/JPY, the pip size is 0.01 (not 0.0001); pip value is computed with that pip size, so the number differs noticeably.',
        'About the FX Pip Value Calculator',
        'FX Pip Value Calculator - compute pip value for different pairs, an online FX trading tool, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.',
    ]))

    # ===== spread-cost (40) =====
    write('spread-cost', build('spread-cost', [
        'FX Spread Cost Calculator',
        'Compute the spread cost and total trading cost of FX trades.',
        '“Compute the spread cost and total trading cost of FX trades” performs a professional calculation from the inputs and outputs the result.',
        '/ Spread Cost',
        'View the FX Spread Cost Calculator User Guide',
        'Ask',
        'Bid',
        'Commission per lot (USD, round-turn)',
        'Swap (USD/lot/day)',
        'Holding days',
        'Spread Cost Formula',
        'Spread',
        '= Ask − Bid (converted to pips)',
        'Spread cost',
        '= lots × pips × value per pip',
        'Value per pip',
        '= 100000 × pip size ÷ quote-to-USD rate',
        'Total cost',
        '= spread cost + commission + swap',
        'Typical Spreads of Major Pairs',
        'Major-platform spreads',
        '0.5 - 2 pips',
        '1 - 3 pips',
        '1 - 2 pips',
        '3 - 8 pips',
        '1.5 - 3 pips',
        'Spread cost arises at opening (a hidden cost). ECN accounts have low spreads but charge commission; standard accounts have no commission but higher spreads. Swap is the cost of holding overnight.',
        'Deep Dive: FX Spread Cost Calculator',
        'Scalping/high-frequency cost accounting: total trading cost = spread + commission + swap, to judge whether a strategy',
        'breaks even',
        'Broker comparison: same instrument, different platforms’ spreads and commissions — compute round-turn cost per lot to pick the better channel.',
        'Position budget: given lots and spread, estimate the hidden cost at opening and fold it into stop-loss design.',
        'Spread = Ask − Bid; spread (pips) = spread ÷ pip size; value per pip/lot = 100000 × pip size ÷ quote-to-USD; spread cost = lots × spread(pips) × value per pip/lot; total commission = lots × one-way commission; swap cost = lots × per-lot overnight interest × days; total cost = spread cost + total commission + swap cost.',
        'EURUSD, 1 lot, Ask=1.0852, Bid=1.0850, quote-to-USD=1, commission 7/lot, swap −3.5/lot, hold 0 days: spread=0.0002, spread(pips)=0.0002÷0.0001=2 pips; value/lot=100000×0.0001÷1=10; spread cost=1×2×10=20 USD; total commission=1×7=7; swap cost=0; total cost=27 USD (if held 1 day, swap −3.5 added, net cost 23.5).',
        'Which matters more, spread cost or commission?',
        'Both. Spread is the hidden cost deducted at opening; commission is the broker’s disclosed fee; under high-frequency/scalping strategies the spread often dominates total cost, so pick a low-spread account.',
        'What does a negative swap mean?',
        'A minus sign means holding overnight incurs interest (buying a high-yield currency / selling a low-yield one may be positive); here −3.5 means net −3.5 per lot per day, so long-term holds must count swap into cost.',
        'About the FX Spread Cost Calculator',
        'FX Spread Cost Calculator - compute spread trading cost, an online FX cost-analysis tool, free to use. A professional financial tool using standard formulas; data is processed locally and not leaked.',
    ]))


if __name__ == '__main__':
    main()
