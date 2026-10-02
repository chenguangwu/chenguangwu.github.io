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
    write('amortization-first-interest', build('amortization-first-interest', [
        "First-Month Loan Interest Calculator",
        "The interest portion of the first installment under equal-monthly-installment (amortizing) repayment.",
        "/ First-Month Interest",
        "First-Month Interest",
        'View "First-Month Loan Interest Calculator User Guide"',
        "First-month interest = total loan × monthly rate, where monthly rate = annual rate / 12. Under equal installments the first-period remaining principal is the full amount, so the first-month interest is highest and then declines monthly as principal is amortized.",
        "500,000, 4.9% → first-month interest about 2041.67.",
        "Equal installments put a larger share into interest in the early period.",
        "📚 In-Depth: First-Month Loan Interest",
        "After taking out an equal-installment mortgage, see clearly how much of the first monthly payment is interest and how much is principal.",
        "Compare the first-month interest composition across loan plans to assess early repayment pressure.",
        "Explain the principal-amortization pattern of equal installments to a relationship manager.",
        "1,000,000 loan, annual rate 4.9%, first-month interest",
        "Monthly rate r=4.9%/12=0.4083%. The first-month remaining principal is the full loan 1,000,000, so first-month interest=1,000,000×0.4083%=4,083. The first-month principal repaid = monthly payment − 4,083, and rises monthly as the remaining principal falls.",
        "Why is more interest paid early under equal installments?",
        "Equal installments keep the monthly payment fixed, but interest is charged on remaining principal × monthly rate. Early on the remaining principal is highest, so the interest share is largest; as principal is gradually amortized, the interest share falls and the principal share rises.",
        "How much does the first-month interest differ from the second?",
        "Second-month interest = second-month remaining principal × monthly rate. The second-month remaining principal = first-month principal − the principal portion repaid in the first month, so the second-month interest is slightly lower, by the first-month principal repayment × monthly rate.",
    ]))
    write('apy-calculator', build('apy-calculator', [
        "Actual Annual Yield from Nominal Rate and Compounding Frequency",
        "Enter the nominal annual rate r and compounding frequency n per year to find the APY.",
        "APY (Annual Percentage Yield) Calculator",
        "/ APY (Annual Percentage Yield) Calculator",
        'View "Actual Annual Yield from Nominal Rate and Compounding Frequency User Guide"',
        "APY=(1+r/n)^n−1, where r is the nominal annual rate and n is the compounding frequency per year; it reflects the true annualized return at different compounding frequencies, which rises with frequency and is capped by continuous compounding e^r−1.",
        "Nominal annual rate r",
        "5%, monthly compounding → about 5.116%.",
        "📚 In-Depth: Actual Annual Yield (APY)",
        "Compare the true returns of two products with the same nominal rate but different compounding frequencies.",
        "Convert a bank's stated 'annualized X%, compounded monthly' into a comparable actual annual yield.",
        "Assess the compounding gain from daily interest on demand/money-market funds.",
        "Nominal 5%, monthly compounding actual annual yield",
        "APY=(1+0.05/12)^12−1=1.004167^12−1≈0.05116=5.116%. Monthly compounding yields 0.116 percentage points more than the nominal 5% simple rate.",
        "What is the difference between APY and EAR?",
        "Numerically both use the same formula (1+r/n)^n−1. APY usually refers to the deposit/money-fund '",
        "actual yield",
        "' basis, while EAR usually refers to the loan '",
        "' basis; the calculation is the same.",
        "Does a higher compounding frequency yield more?",
        "With a fixed nominal rate, more frequent compounding (daily > monthly > annual) gives a higher actual annual yield, but there is a cap — continuous compounding A=P·e^(rt) — beyond which no frequency exceeds e^r−1.",
    ]))
    write('bond-current-yield', build('bond-current-yield', [
        "Current Yield from Annual Coupon and Bond Price",
        "Enter the annual coupon and the bond's market price to find the current yield.",
        "CY = Annual Coupon / Market Price",
        "/ Bond Current Yield Calculator",
        "Bond Current Yield Calculator",
        'View "Current Yield from Annual Coupon and Bond Price User Guide"',
        "Current yield = annual coupon / price",
        "Current yield = coupon / price, where coupon = face value × coupon rate. Buying at a discount (price < face) gives a yield higher than the coupon rate, and at a premium lower; it ignores capital gain and term factors.",
        "Bond market price (yuan)",
        "CY = annual coupon / market price.",
        "Coupon 50, price 980 → 5.10%.",
        "📚 In-Depth: Bond Current Yield",
        "Assess the spot coupon return when buying bonds at a discount or premium in the secondary market.",
        "Compare bonds of the same maturity by",
        "current yield",
        "to aid bond selection.",
        "Track how market-price swings affect current yield while holding the bond.",
        "Current yield for face 100, coupon 5%, price 95",
        "Coupon=100×5%=5. Annual current yield CY=coupon/price=5/95=5.26%. When price is below face (discount), CY exceeds the coupon rate.",
        "Is current yield the same as YTM?",
        "No. Current yield only computes coupon/price, ignoring capital gain/discount amortization and remaining term; YTM includes the price difference to maturity and discounted cash flows, so it is more complete.",
        "Why is current yield lower than the coupon when bought at a premium?",
        "When price exceeds face, the denominator grows while the coupon is unchanged, so CY is below the coupon rate; conversely a discount purchase gives CY above the coupon rate.",
    ]))
    write('break-even-savings', build('break-even-savings', [
        "Net Interest Breaks Even at Save X, Borrow (1−X)",
        "The deposit share that makes the overall net interest spread zero, given deposit rate r_d and loan rate r_l.",
        "Save-or-Borrow Break-Even Calculator",
        "/ Save-or-Borrow Break-Even Point",
        "Save-or-Borrow Break-Even Point",
        'View "Net Interest Breaks Even at Save X, Borrow (1−X) User Guide"',
        "Let deposit share be X, net interest = X·r_d − (1−X)·r_l; setting it to zero gives X = r_l / (r_d + r_l). To its left saving is better, to its right repaying the loan is better; liquidity, risk and tax are not included.",
        "Deposit rate r_d (%)",
        "Loan rate r_l (%)",
        "Save 2%, borrow 5% → net interest is zero at a 71.43% deposit share.",
        "Assumes assets equal liabilities in size.",
        "📚 In-Depth: Save-or-Borrow Net-Interest Break-Even",
        "With a sum of money, find the balance between paying off the loan early to save interest and saving it to earn interest.",
        "Assess whether to reduce",
        "early repayment",
        "Quantify the net interest cost of debt versus savings when allocating household assets.",
        "Break-even at deposit rate 2%, loan rate 4%",
        "Let deposit share X, loan share 1−X, net interest = X·r_d − (1−X)·r_l. Set to zero: X = r_l/(r_d+r_l) = 0.04/0.06 = 66.7%. That is, overall net interest is zero when at least 66.7% goes to loan repayment and 33.3% stays as savings.",
        "Does this break-even point consider risk?",
        "No. The model only compares the rate spread, ignoring liquidity needs, early-repayment penalties, tax and investment opportunities. In practice keep emergency cash before considering repayment.",
        "Does tax rate affect the break-even point?",
        "Yes. Deposit interest may be tax-exempt or taxable, and loan interest may be partly deductible. Substituting the after-tax rates r_d(1−t_d) and r_l(1−t_l) shifts the break-even point right or left.",
    ]))
    write('continuous-compounding', build('continuous-compounding', [
        "Continuous Compounding Future Value Calculator",
        "The future value when the compounding frequency tends to infinity.",
        "/ Continuous Compounding Future Value",
        "Continuous Compounding Future Value",
        'View "Continuous Compounding Future Value Calculator User Guide"',
        "Continuous compounding: A = P × e^(rt), where e is the natural constant; total interest = A − P; annual effective return = e^r − 1; compared with annual compounding, continuous compounding is the limiting upper bound, used in financial mathematics and continuous-growth models.",
        "10,000, 5%, 10 years → about 16,487.21.",
        "e is the natural constant.",
        "📚 In-Depth: Continuous Compounding Future Value",
        "Study the mathematical limit of compounding and compare with ordinary compounding.",
        "Understand e^(rt) discounting in financial engineering and derivatives pricing.",
        "Estimate the upper bound of return at very high compounding frequencies.",
        "Principal 10,000, annual 6%, continuous compounding 5 years",
        "A=P·e^(rt)=10,000×e^(0.06×5)=10,000×e^0.30≈10,000×1.34986=13,498.6. Slightly higher than monthly compounding (13,488.5) by about 10, already near the limit.",
        "Does continuous compounding exist in reality?",
        "Banks do not truly compound instantaneously, but it is the theoretical abstraction of infinite compounding frequency, widely used for discounting and growth in continuous-time finance models (e.g. Black-Scholes).",
        "How do continuous and ordinary compounding formulas convert?",
        "Take the limit e^r = (1+i/n)^n. For a given annual r, any ordinary compounding frequency is strictly less than the continuous upper bound e^r−1.",
    ]))

if __name__ == "__main__":
    main()
