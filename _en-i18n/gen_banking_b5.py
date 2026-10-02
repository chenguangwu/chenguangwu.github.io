#!/usr/bin/env python3
# gen_banking_head.py — shared head for banking batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'banking')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'banking')
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
    out = {'slug': slug, 'industry': 'banking', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('perpetuity-pv', build('perpetuity-pv', [
        "Perpetuity Present Value from Periodic Cash Flow and Discount Rate",
        "Enter periodic cash flow C and discount rate r to find the perpetuity present value.",
        "Perpetuity Present Value Calculator",
        "/ Perpetuity Present Value Calculator",
        'View "Perpetuity Present Value from Periodic Cash Flow and Discount Rate User Guide"',
        "PV = C ÷ r, with C the periodic cash flow and r the discount rate, suited to consols, preferred stock and other infinite cash flows. In reality most carry call or default clauses; a strict perpetuity exists only in models.",
        "Periodic cash flow C (yuan)",
        "PV = C / r (perpetuity).",
        "C=100, r=5% → 2,000 yuan.",
        "📚 In-Depth: Perpetuity Present Value",
        "Value infinite cash flows such as preferred stock and consols.",
        "Estimate a stock's intrinsic value with the dividend-discount model.",
        "Price 'fixed annual, perpetual' style liabilities.",
        "Perpetuity present value at 100 per year, discount rate 5%",
        "PV = C ÷ r = 100 ÷ 0.05 = 2,000 yuan. This is the theoretical price of that perpetual cash flow at the current rate.",
        "Do perpetuities exist in reality?",
        "Approximately: UK Consols, preferred-stock fixed dividends and some annuity products. A strict infinite term holds in models; in reality most carry call/default clauses.",
        "What if the growth rate is not zero?",
        "Use the growing perpetuity PV = C ÷ (r − g), requiring r > g. This extends the 'perpetuity + growth' in preferred-stock/dividend models.",
    ]))
    write('present-value-annuity-due', build('present-value-annuity-due', [
        "Present Value of an Annuity Due from Periodic Payment, Rate and Periods",
        "Enter periodic payment PMT, periodic rate r and periods n to find the annuity-due present value.",
        "Annuity-Due Present Value Calculator",
        "/ Annuity-Due Present Value Calculator",
        'View "Present Value of an Annuity Due from Periodic Payment, Rate and Periods User Guide"',
        "PV = PMT × [1 − (1+r)^(−n)] ÷ r × (1+r); each annuity-due payment occurs one period earlier and is discounted one fewer period, so its present value exceeds the same-parameter ordinary annuity (e.g. a mortgage monthly payment).",
        "100 yuan, 0.5%/period, 12 periods → about 1,168 yuan.",
        "📚 In-Depth: Annuity-Due Present Value",
        "Value the current worth of beginning-of-period payment streams such as rent and insurance.",
        "Estimate the present value of lease options.",
        "Compare beginning-of-period with end-of-period",
        "annuity present value",
        "difference.",
        "Annuity-due PV at 1,000 per period, monthly rate 0.5%, 12 periods",
        "PV = PMT × [1 − (1+r)^(−n)] ÷ r × (1+r) = 1,000 × [1 − 1.005^(−12)] ÷ 0.005 × 1.005 = 1,000 × [1 − 0.9419] ÷ 0.005 × 1.005 = 1,000 × 11.618 × 1.005 ≈ 11,676 yuan.",
        "Why is the annuity-due present value higher than the ordinary?",
        "Each payment occurs one period earlier and is discounted one fewer period, so the PV is higher. The difference is about the present value of one period of interest.",
        "What is its relation to the mortgage monthly-payment present value?",
        "A mortgage monthly payment is an ordinary annuity (funded at month start, first repayment at month end) using ordinary-annuity PV; rent is a typical annuity due — the two formulas differ by a (1+r) factor.",
    ]))
    write('rd-maturity', build('rd-maturity', [
        "Recurring Deposit Maturity Calculator",
        "The maturity amount of a recurring deposit with fixed monthly deposits and quarterly compounding.",
        "/ Recurring Deposit (Monthly Deposit, Quarterly Compounding)",
        "Recurring Deposit (Monthly Deposit, Quarterly Compounding)",
        'View "Recurring Deposit Maturity Calculator User Guide"',
        "Monthly deposit P",
        "1,000 deposited monthly, 8%, 1 year → maturity about 12,531.",
        "The denominator contains (1+i)^(−1/3).",
        "📚 In-Depth: Recurring Deposit Maturity",
        "Set up a fixed monthly forced-savings plan.",
        "Compare recurring-deposit and lump-sum-deposit returns.",
        "Estimate savings for goals like travel and education.",
        "Deposit 1,000 monthly, annual 2%, 1 year (12 times)",
        "Principal totals 12,000. Interest accrues arithmetically: the 1st deposit sits 12 months, the 12th sits 1 month, interest = 1,000 × (2% ÷ 12) × (12+11+…+1) = 1,000 × 0.001667 × 78 ≈ 130 yuan, maturity about 12,130 yuan.",
        "What if a deposit is missed mid-term in a recurring deposit?",
        "Most banks allow a catch-up deposit the next month (limited times); beyond that it accrues at the demand rate or converts to a demand account, forfeiting the agreed interest.",
        "Why is the return lower than a lump-sum deposit?",
        "Recurring-deposit funds are put in month by month with a short average holding time, while a lump-sum deposit occupies the full year, so at the same rate the recurring deposit earns less interest.",
    ]))
    write('savings-goal-monthly', build('savings-goal-monthly', [
        "Monthly Savings Goal Deposit Calculator",
        "The amount to deposit each period to reach the target amount after N periods.",
        "/ Monthly Savings Goal Deposit",
        "Monthly Savings Goal Deposit",
        'View "Monthly Savings Goal Deposit Calculator User Guide"',
        "Target amount FV",
        "Target 200,000, 4%, 10 years → monthly deposit about 1,361.37.",
        "i is the monthly rate.",
        "📚 In-Depth: Monthly Savings Goal Deposit",
        "Set a monthly deposit amount for a home down payment, travel and similar goals.",
        "Back-solve the saving pace given a time horizon and return rate.",
        "Adjust the target amount or term to see the monthly deposit change.",
        "Monthly deposit to save 100,000 in 3 years at monthly rate 0.3%",
        "PMT = FV × r ÷ ((1+r)^n − 1) = 100,000 × 0.003 ÷ ((1.003)^36 − 1) = 300 ÷ (1.1133 − 1) = 300 ÷ 0.1133 ≈ 2,648 yuan/month. Over 36 months about 95,328 is deposited, interest makes up to 100,000.",
        "What if the assumed return is set too high?",
        "A higher assumed return means a lower required monthly deposit, but harder to achieve. Conservatively use a risk-free rate (money fund / time deposit) to avoid missing the goal.",
        "Can you pause or add mid-way?",
        "Yes. The formula gives a 'constant monthly deposit' baseline; in practice you can use variable amounts (e.g. a year-end bonus top-up) to reach it faster, checking period by period with cash-flow discounting.",
    ]))
    write('tax-equivalent-yield', build('tax-equivalent-yield', [
        "Tax-Equivalent Yield from Tax-Exempt Yield and Tax Rate",
        "Enter the tax-exempt yield and marginal tax rate to find the tax-equivalent taxable yield.",
        "TEY = Tax-Exempt Yield / (1 − Tax Rate)",
        "/ Tax-Equivalent Yield Calculator",
        "Tax-Equivalent Yield Calculator",
        'View "Tax-Equivalent Yield from Tax-Exempt Yield and Tax Rate User Guide"',
        "TEY = Tax-Exempt Yield / (1 − Tax Rate)",
        "TEY = tax-exempt yield ÷ (1 − marginal tax rate). A taxable product is only better when its yield exceeds the TEY, so compare using your own marginal rate; capital gains tax is not included.",
        "Tax-exempt yield",
        "Marginal tax rate",
        "TEY = Tax-Exempt Yield / (1 − Tax Rate).",
        "📚 In-Depth: Tax-Equivalent Yield (TEY)",
        "Compare the true return of tax-exempt (e.g. treasury interest) versus taxable fixed income.",
        "Judge whether tax-exempt products are better at high tax rates.",
        "Price-compare products within a fixed-income portfolio.",
        "Tax-exempt yield 3%,",
        "20% tax-equivalent taxable yield",
        "TEY = tax-exempt yield ÷ (1 − tax rate) = 3% ÷ 0.8 = 3.75%. That is, this tax-exempt product equals a pre-tax 3.75% taxable product; only a taxable product yielding >3.75% is better.",
        "Are all tax-exempt products better?",
        "Not necessarily. At low tax rates the TEY uplift is limited, and if a taxable product's coupon is far above the tax-exempt one it may still win. Compare using your own marginal rate.",
        "Capital gains tax",
        "— is it included?",
        "TEY usually handles only the 'interest tax' basis. If trading-spread capital gains tax is involved, it must be converted separately and the model gets more complex.",
    ]))

if __name__ == "__main__":
    main()
