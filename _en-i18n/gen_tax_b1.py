#!/usr/bin/env python3
# gen_tax_b1.py — tax b1 (5 slugs): ad-valorem-duty/average-tax-rate/break-even-taxable/capital-gains-effective/capital-gains-tax
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tax')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tax')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'tax', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

AVD = [
 "Ad valorem duty from taxable price and ad valorem rate",
 "Enter the taxable price and ad valorem rate to compute the ad valorem duty.",
 "T = Taxable price x Rate",
 "/ Ad Valorem Duty Calculator",
 "Ad Valorem Duty Calculator",
 "📖 View the Ad Valorem Duty Guide",
 "Ad valorem duty = Taxable price x Rate",
 "Taxable price (CNY)",
 "Ad valorem duty is levied as a proportion of the price.",
 "1000 CNY x 10% -> 100 CNY.",
 "📚 Deep Dive: Ad Valorem Duty (rate by value)",
 "For imports, duties and ad valorem excise are levied on the dutiable value x ad valorem rate; a quick tax estimate is needed.",
 "Given the goods value and rate, back-solve the tax payable or the tax-inclusive cost.",
 "Compare how ad valorem vs specific duty affects the tax burden on the same goods.",
 "Dutiable value 1000, rate 10%",
 "Ad valorem duty T = 1000 x 0.10 = 100 CNY; if value rises to 5000, T = 500 CNY; tax grows linearly with price.",
 "Back-solve tax-inclusive cost",
 "If target tax-inclusive cost is 1100 and rate 10%, dutiable value = 1100 / 1.10 = 1000 CNY, tax 100 CNY.",
 "How does ad valorem differ from specific duty?",
 "Ad valorem is levied by price proportion (higher price, higher tax); specific duty is a fixed amount per unit (e.g., per ton or per item) and unrelated to price.",
 "How are the exchange rate and taxable price determined?",
 "Import ad valorem duty usually uses the customs-approved dutiable value (CIF) times the applicable rate; foreign currency is converted to CNY at the filing-date exchange rate.",
]

ATR = [
 "Average tax rate from total tax and total income",
 "Enter total tax and total income to compute the average tax rate.",
 "Average Tax Rate Calculator",
 "/ Average Tax Rate Calculator",
 "📖 View the Average Tax Rate Guide",
 "Average tax rate = Total tax / Total income",
 "Total tax T (CNY)",
 "Total income Y (CNY)",
 "ATR = Total tax / Total income.",
 "30k / 100k -> 30%.",
 "📚 Deep Dive: Average Tax Rate",
 "Measures the overall tax burden: annual total tax divided by the total tax base.",
 "Compare average tax burdens across income groups or countries.",
 "Beyond the",
 "marginal tax rate",
 ", assess the actual share of income paid as tax.",
 "Total tax 30000, income 100000",
 "Average tax rate ATR = 30000 / 100000 = 0.30, i.e. 30%.",
 "Average tax rate under a progressive tax",
 "If 30k tax comes from 100k income, ATR=30%; if income doubles to 200k and tax only rises to 50k, ATR drops to 25%, showing progressivity.",
 "How does average tax rate differ from marginal tax rate?",
 "Average rate is total tax over total income, reflecting the overall burden; marginal rate is the rate on the last unit of income, driving incremental incentives.",
 "Why is the average tax rate always below the marginal rate?",
 "Under a progressive system, lower income faces lower brackets and only the excess faces higher ones, so the average stays below the marginal rate.",
]

BET = [
 "Taxable income = Fixed deduction / Marginal rate",
 "Estimate the taxable income needed to reach an after-tax target.",
 "Break-Even Taxable Income Calculator",
 "/ Break-Even Taxable Income",
 "Break-Even Taxable Income",
 "📖 View the Break-Even Taxable Income Guide",
 "Pre-tax = After-tax / (1 - r).",
 "Target after-tax income",
 "Exemption / deduction",
 "After-tax 750k, 25% -> taxable 1M.",
 "📚 Deep Dive: Back-solving taxable income from a target after-tax amount",
 "A shareholder or owner wants to take home target CNY; back-solve how much taxable income to report.",
 "Given a fixed deduction and proportional rate r, find the pre-tax threshold for the target net income.",
 "Estimate the pre-tax break-even point for dividends or compensation design.",
 "Target take-home 750k, rate 25%, no deduction",
 "Required taxable income = (750000 + 0) / (1 - 0.25) = 1,000,000 CNY; tax = 1,000,000 x 0.25 = 250,000 CNY, after-tax exactly 750k.",
 "Case with deduction",
 "If a 100k deduction applies (deduct=100000), taxable income = (750000 + 100000) / 0.75 = 1,133,333 CNY, 133k less than with no deduction.",
 "Why is the formula (target+deduct)/(1-r)?",
 "After-tax income = taxable income x (1-r) - deduct; rearranging gives taxable income = (after-tax + deduct) / (1-r).",
 "Is rate r entered as decimal or percent?",
 "Enter r as a percent (e.g., 25 means 25%); it is converted to 0.25 internally for the (1-r) calculation.",
]

CGE = [
 "Tax due from capital gain and preferential rate",
 "Enter the capital gain and applicable preferential rate to compute capital gains tax.",
 "T = Gain x Preferential rate",
 "/ Preferential Capital Gains Tax Calculator",
 "Preferential Capital Gains Tax Calculator",
 "📖 View the Preferential Capital Gains Tax Guide",
 "Tax due = Gain x Preferential rate",
 "Capital gain (CNY)",
 "Preferential rate",
 "Long-term holding often enjoys a preferential rate.",
 "100k x 10% -> 10k.",
 "📚 Deep Dive: Capital Gains Tax (levied on gain)",
 "Selling an asset produces a gain, taxed as gain x proportional rate",
 "capital gains tax",
 "Compare tax and take-home across gain sizes.",
 "Assess how holding period and exemption affect the real tax burden.",
 "Gain 100k, rate 10%",
 "Capital gains tax T = 100000 x 0.10 = 10,000 CNY; if gain doubles to 200k, tax is 20k.",
 "No tax on negative gains",
 "If the gain is -30000 (loss), most rules take tax = max(0, gain x r) = 0, and the loss can be carried forward to offset future gains.",
 "How does capital gains tax differ from income tax?",
 "Capital gains tax is levied specifically on asset appreciation (buy-sell spread); its rate or exemption usually differs from wage income tax.",
 "How are losses handled?",
 "Losses generally incur no tax that year and can be carried forward within the allowed years to offset future realized gains.",
]

CGT = [
 "Capital Gains Tax Calculator",
 "Compute capital gains tax from the asset transfer price spread and rate.",
 "/ Capital Gains Tax",
 "Capital Gains Tax",
 "📖 View the Capital Gains Tax Calculator Guide",
 "Capital gains tax: gain = selling price - purchase price (incl. fees); tax due = gain x applicable rate; effective rate = tax due / selling price x 100%; whether a loss year can be carried forward depends on the tax system. For investment tax reference.",
 "Selling price",
 "Spread 50k, 20% -> tax 10k.",
 "Loss is usually tax-free (take max(0, gain)).",
 "📚 Deep Dive: Capital Gains Tax (selling price - cost)",
 "Given selling price, purchase cost and rate, compute gain, tax and after-tax take-home.",
 "Compare tax burdens of long-term holding vs short-term trading.",
 "Estimate real returns on property, stock or equity exits.",
 "Sell 150k, cost 100k, rate 20%",
 "Capital gain = 150000 - 100000 = 50,000 CNY; tax = 50000 x 0.20 = 10,000 CNY; after-tax take-home = 150000 - 10000 = 140,000 CNY.",
 "Break-even or loss",
 "If selling price equals cost 100k, gain 0, tax 0, take-home 100k; if sold at 90k, gain -10k, tax = 0 (or carry forward the loss).",
 "What does cost include?",
 "Usually includes purchase price, trading fees and capitalized improvements; the taxable cost base follows the tax law.",
 "Why is after-tax take-home selling price minus tax, not minus gain?",
 "Take-home is total selling price minus tax, i.e. selling price - capital gains tax; here 150k - 10k tax = 140k.",
 "How to use the Capital Gains Tax Calculator",
 "What does the Capital Gains Tax Calculator do?",
 "Capital Gains Tax Calculator: Enter the asset purchase price, selling price and applicable rate to compute the gain and tax due, for investment tax reference.",
 "How do I use the Capital Gains Tax Calculator?",
 "Which scenarios suit the Capital Gains Tax Calculator?",
]

write('ad-valorem-duty', build('ad-valorem-duty', AVD))
write('average-tax-rate', build('average-tax-rate', ATR))
write('break-even-taxable', build('break-even-taxable', BET))
write('capital-gains-effective', build('capital-gains-effective', CGE))
write('capital-gains-tax', build('capital-gains-tax', CGT))
