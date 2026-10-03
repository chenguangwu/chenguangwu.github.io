#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'futures')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'futures')
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
    out = {'slug': slug, 'industry': 'futures', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('futures-pricing', build('futures-pricing', [
        '💰 Futures Pricing Calculator',
        'Cost of carry model — computes the theoretical futures price and the basis',
        'Core formula (by input variables): spot × Math.exp(carry × time)',
        '/ Futures Pricing',
        '📖 View the guide to the theoretical futures price (cost of carry model)',
        'Spot price (CNY)',
        'Convenience yield / dividend yield (%)',
        'Storage cost rate (%/year)',
        'Continuous compounding',
        'Discrete compounding',
        'Actual futures price (CNY, optional)',
        '🔢 Cost of Carry Model',
        'Where: S = spot price, r = risk-free rate, u = storage cost rate, q = convenience yield / dividend yield, T = time to maturity',
        'Basis',
        '= spot price - futures price',
        'Cost of carry',
        '= F - S (cost of holding the spot to maturity)',
        '📚 Futures Pricing Principles',
        'Contango',
        ': futures price > spot price (cost of carry is positive)',
        'Backwardation',
        ': futures price < spot price (high convenience yield)',
        'Arbitrage',
        ': an arbitrage opportunity exists when the actual price deviates from the theoretical price',
        'Convergence',
        ': near expiration, the futures price converges to the spot price',
        'This model applies to financial futures and storable commodity futures. Non-storable goods (such as electricity or fresh produce) do not fit this model.',
        '📚 In-depth: theoretical futures price (cost of carry model)',
        'Pricing reference for hedging',
        'Basis analysis for cash-and-carry arbitrage',
        'Identifying contango / backwardation',
        'Cost of carry model: theoretical price F = S × (1 + (r + u − q) × T) (simple interest) or S · e^((r+u−q)T) (continuous), where S is the spot price, r the interest rate, u the storage rate, q the dividend yield and T the years to maturity; F − S is the cost of carry and S − F is the basis.',
        'Spot 5000, r = 4%, u = 0.5%, q = 1%, T = 0.25 years → net cost of carry rate 3.5%, F = 5000 × (1 + 3.5% × 0.25) = 5043.75 (5043.94 with continuous compounding); cost of carry 43.75, basis −43.75, and F above spot means contango. For pricing reference only, not investment advice.',
        'What does a negative basis mean?',
        'In contango the futures price is above spot and a negative basis is normal; a widening or narrowing basis reflects changes in carrying costs and expectations, and is used in arbitrage and hedging decisions.',
        'Can the result be used as a transaction price?',
        'No. The theoretical price is only a model estimate; the actual price is affected by liquidity, delivery and sentiment. This tool is a pure calculation demo and does not fetch live quotes.',
        'About the Futures Pricing Calculator',
        'Futures Pricing Calculator — a cost-of-carry online calculator for theoretical futures prices, free to use. A professional financial calculator using standard finance formulas; data is processed locally and never leaked.',
    ]))

    write('hedge-ratio', build('hedge-ratio', [
        '🧮 Hedge Ratio Calculator',
        'Computes the minimum-variance hedge ratio, the number of futures contracts to hedge with, and hedging effectiveness',
        'Core formula (by input variables): Math.round(hedgeContracts)',
        '/ Hedge Ratio',
        '📖 View the guide to the minimum-variance optimal hedge ratio',
        'Std. dev. of the spot price change σS (%)',
        'Std. dev. of the futures price change σF (%)',
        'Correlation coefficient ρ',
        'Total spot value (CNY)',
        'Futures contract price',
        'Futures contract multiplier',
        'Short hedge (long spot)',
        'Long hedge (short spot)',
        '🔢 Minimum-Variance Hedge Ratio',
        'Hedge ratio',
        'where ρ is the correlation coefficient between spot and futures price changes',
        'Hedging effectiveness',
        'R² = ρ² (the share of risk removed by the hedge)',
        'Number of contracts',
        '= spot value × h* ÷ futures contract value',
        '📚 Types of Hedging',
        'Short hedge',
        ': hold the spot and sell futures to lock in the selling price',
        'Long hedge',
        ': buy futures to lock in the purchase price when the spot must be bought later',
        'Cross hedge',
        ': when the spot and the futures are different products, adjust using the correlation coefficient',
        '📊 Evaluating Hedging Effectiveness',
        'Excellent (low basis risk)',
        'Poor (limited hedging value)',
        'The closer the hedge ratio is to 1, the stronger the co-movement of spot and futures prices. In a cross hedge the correlation is usually below 1, leaving basis risk.',
        '📚 In-depth: the minimum-variance optimal hedge ratio',
        'Hedging program design',
        'Estimating the number of contracts',
        'Assessing hedging effectiveness',
        'Minimum-variance method: h* = ρ · σS / σF; R² = ρ² measures effectiveness. Suggested contracts = spot exposure × h* / value per contract, then rounded.',
        'σS = 3%, σF = 3.5%, ρ = 0.85 → h* = 0.85 × 3 / 3.5 = 0.7286, R² = 72.25% (good); spot 1,000,000 with contract price 3800 × 300 = 1,140,000 per contract → 1 contract suggested, hedged value about 1,140,000, coverage 114%. Pure calculation demo, not investment advice.',
        'How should ρ be chosen?',
        'Estimate it from the historical',
        'correlation of spot and futures price changes',
        '; results change with the sample period and market structure, so refresh it regularly.',
        'What if R² is low?',
        'R² below 0.5 means weak hedging; switch to a more correlated instrument or add options to reduce basis risk.',
        'About the Hedge Ratio Calculator',
        'Hedge Ratio Calculator — computes the optimal hedge ratio for futures hedging, free to use. A professional financial calculator using standard finance formulas; data is processed locally and never leaked.',
    ]))

    write('margin-calc', build('margin-calc', [
        '📉 Futures Margin Calculator',
        'Calculates futures contract margin, the number of contracts you can open, and the leverage multiple',
        'Computes futures contract margin, openable contracts and the leverage multiple from the inputs and outputs the result.',
        '/ Margin Calculation',
        '📖 View the guide to futures margin and leverage',
        'Contract price',
        'Margin rate (%)',
        'Available funds (CNY)',
        'Contracts to open (optional)',
        'Commission (CNY/contract)',
        'CSI 300 example',
        '= contract price × contract multiplier',
        'Margin per contract',
        '= contract value × margin rate',
        'Maximum contracts',
        '= available funds ÷ margin per contract (rounded down)',
        'Leverage multiple',
        '= contract value ÷ margin = 1 ÷ margin rate',
        '📊 Common Futures Contracts Reference',
        'Margin rate',
        'CSI 300 index (IF)',
        'SSE 50 index (IH)',
        'CSI 500 index (IC)',
        '10-year government bond (T)',
        'Copper (CU)',
        'Gold (AU)',
        'Rebar (RB)',
        'Crude oil (SC)',
        'Futures trading uses leverage, which magnifies both gains and losses. Positions may be force-liquidated when margin is insufficient, so keep ample funds in reserve.',
        '📚 In-depth: futures margin and leverage',
        'Capital management for opening positions',
        'Measuring actual leverage',
        'Margin per contract = contract price × multiplier × margin rate; maximum contracts = floor(funds / margin per contract); leverage = 1 / margin rate.',
        'Contract price 3800, multiplier 300, margin 12%, funds 200,000 → contract value 1,140,000, margin per contract 136,800, maximum 1 contract, leverage 8.33x. Higher leverage means greater risk; for capital planning reference only.',
        'How do leverage and the margin rate relate?',
        'Leverage = 1 / margin rate; a 12% margin rate corresponds to about 8.3x leverage. The lower the rate, the higher the leverage and the greater the liquidation risk.',
        'Is commission included?',
        'The tool deducts commission by contract count and computes the remaining funds; actual rates depend on your broker. This tool is a demo.',
        'About the Futures Margin Calculator',
        'Futures Margin Calculator — a tool for futures margin, openable contracts and leverage, free to use. A professional financial calculator using standard finance formulas; data is processed locally and never leaked.',
    ]))

    write('option-greeks', build('option-greeks', [
        '🧮 Option Greeks Calculator',
        'Black-Scholes model: computes Delta / Gamma / Theta / Vega / Rho and the theoretical price',
        'Core formula (by input variables): (-S × nd1 × sigma × eqT ÷ (2 × sqrtT) + r × K × erT × normCDF(-d2) - q × S × eqT × normCDF(-d1)) ÷ 365; (-S × nd1 × sigma × eqT ÷ (2 × sqrtT) - r × K × erT × normCDF(d2) + q × S × eqT × normCDF(d1)) ÷ 365; (Math.log(S ÷ K) + (r - q + sigma × sigma ÷ 2) × T) ÷ (sigma × sqrtT)',
        '/ Option Greeks',
        '📖 View the guide to option Greeks (Black-Scholes)',
        'Underlying price S',
        'Annualized volatility (%)',
        'Dividend yield (%)',
        'Call option',
        'Put option',
        '📋 Greeks Explained',
        '🔢 Black-Scholes Formula',
        'Call price',
        'Put price',
        '📊 Meaning of the Greeks',
        'Change in option price per 1 unit move in the underlying',
        'unit/unit',
        'Change in Delta per 1 unit move in the underlying',
        '1/unit',
        'Change in option price per 1 day of time passing',
        'unit/day',
        'Change in option price per 1% move in volatility',
        'unit/1%',
        'Change in option price per 1% move in the interest rate',
        'Theta has been converted to a daily figure. Vega and Rho are price changes per 1% move. This tool models European options; American options differ slightly.',
        '📚 In-depth: option Greeks (Black-Scholes)',
        'Option pricing and hedging',
        'Risk exposure monitoring',
        'Strategy P&L analysis',
        'Black-Scholes: d1 = (ln(S/K) + (r + σ²/2) × T) / (σ√T), d2 = d1 − σ√T; these give Delta / Gamma / Theta / Vega / Rho and the theoretical price, measuring sensitivity to price, time, volatility and rates.',
        'Call with S = 100, K = 100, r = 3%, σ = 20%, T = 0.5 → d1 ≈ 0.177, d2 ≈ 0.035; Delta ≈ 0.570, Gamma ≈ 0.0278, Theta ≈ −0.0194/day, Vega ≈ 0.278/1%, Rho ≈ 0.253/1%, theoretical price ≈ 6.37. Pure model demo, not investment advice.',
        'What does a negative Theta mean?',
        'Theta is usually negative for a buyer, meaning time value is lost each day; for a seller it is the opposite, profiting from time decay.',
        'What is the risk of a high Vega?',
        'A high Vega means the price is sensitive to volatility, so a volatility drop erodes the buyer’s value; the seller must guard against volatility spikes.',
        'About the Option Greeks Calculator',
        'Option Greeks Calculator — Black-Scholes computation of Delta / Gamma / Theta / Vega / Rho, free to use. A professional financial calculator using standard finance formulas; data is processed locally and never leaked.',
    ]))

    write('option-payoff', build('option-payoff', [
        '📈 Option Payoff Chart',
        'Visualizes call and put expiration payoff curves for long and short positions',
        'Visualizes call and put expiration payoff curves for buyers and sellers based on the inputs.',
        '📖 View the guide to option expiration payoff analysis',
        '📈 Long call',
        '📉 Long put',
        '📊 Short call',
        '📈 Short put',
        'Premium p',
        '📉 Expiration Payoff Curve',
        'Break-even point',
        'Profit zone',
        '📈 Long Call',
        'Payoff = max(S - K, 0) - p | Break-even = K + p | Max loss = p | Max profit unlimited',
        '📉 Long Put',
        'Payoff = max(K - S, 0) - p | Break-even = K - p | Max loss = p | Max profit = K - p',
        '📊 Short Call',
        'Payoff = p - max(S - K, 0) | Break-even = K + p | Max profit = p | Max loss unlimited',
        '📈 Short Put',
        'Payoff = p - max(K - S, 0) | Break-even = K - p | Max profit = p | Max loss = K - p',
        'The payoff chart shows P&L if the option is held to expiration and ignores time value. In real trading, option prices are also affected by volatility and time decay.',
        '📚 In-depth: option expiration payoff analysis',
        'Strategy P&L visualization',
        'Estimation',
        'Buyer vs seller risk comparison',
        'Long call payoff = max(price at expiration − strike, 0) − premium. The',
        'break-even',
        'point = K + premium; max loss is the premium and max profit is theoretically unlimited. Puts and short positions follow symmetric rules.',
        'Long call with K = 100 and premium 5 → break-even at 105; below 100 the loss is capped at 5 (the premium), and above 105 each 1-point rise earns 1, so profit is theoretically unlimited. The seller’s profit is capped at 5 while the loss is theoretically unlimited. For strategy understanding only, not investment advice.',
        'Is the buyer always better off than the seller?',
        'No. Buyers have limited losses but usually a low win rate, while sellers have a high win rate but large tail risk; match the position to your view and capital.',
        'Does the break-even include the premium?',
        'Yes. A long call must rise above K + premium to break even — a cost that is often overlooked.',
        'About the Option Payoff Chart',
        'Option Payoff Chart — visualize call and put payoff curves with a Canvas chart, free to use. A professional financial calculator using standard finance formulas; data is processed locally and never leaked.',
        'Payoff structure',
        'Long call payoff = max(price at expiration − strike, 0) − premium; a put is the reverse. Break-even = strike ± premium. A short position mirrors the long and caps profit at the premium.',
        'Plot P&L at different expiration prices to assess strategy risk and reward; leverage and time decay (Theta) materially affect real results.',
        'Boundaries',
        'This chart uses static expiration payoff and excludes dynamic Greeks and margin. Options are high risk; for learning only. Trade in compliance and at your own risk.',
    ]))


if __name__ == '__main__':
    main()
