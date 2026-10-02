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
    write('loan-tenure', build('loan-tenure', [
        "Derive the Repayment Term from Loan Amount, Rate and Monthly Payment",
        "Enter loan principal P, periodic rate r and periodic payment PMT to find the number of repayment periods.",
        "Loan Term Calculator",
        "/ Loan Term Calculator",
        'View "Derive the Repayment Term from Loan Amount, Rate and Monthly Payment User Guide"',
        "n = ln(PMT ÷ (PMT − P·r)) ÷ ln(1+r), with P principal, r periodic rate and PMT payment. If payment ≤ periodic interest (PMT ≤ P·r) the denominator is non-positive and there is no solution — principal grows; the payment must be raised.",
        "Loan principal P (yuan)",
        "Periodic payment PMT (yuan)",
        "Solve n from the annuity present-value formula.",
        "10,000, 0.5%/period, 200/period → about 57.7 periods.",
        "📚 In-Depth: Loan Term Back-Solving",
        "Given the affordable monthly payment, work out how long it takes to clear the loan.",
        "Plan the repayment pace of an auto or mortgage loan.",
        "Compare how much the term shortens when the payment is raised.",
        "Payoff periods for a 500,000 loan, monthly rate 0.4%, monthly payment 3,000",
        "n = ln(PMT ÷ (PMT − P·r)) ÷ ln(1+r) = ln(3,000 ÷ (3,000 − 500,000 × 0.004)) ÷ ln(1.004) = ln(3,000 ÷ 2,000) ÷ 0.003992 ≈ ln(1.5) ÷ 0.003992 ≈ 101.7 periods, about 8.5 years.",
        "What if the payment is below the interest?",
        "If PMT ≤ P·r (periodic interest), the denominator PMT − P·r ≤ 0 and the formula has no solution — the principal is never cleared and grows, a 'interest on interest' vicious cycle; the payment must be raised.",
        "What if n is not an integer?",
        "The last period is settled separately on the remaining principal. Usually the first n−1 periods use the full payment, and the final period uses remaining principal + interest to square up, with a slightly different amount.",
    ]))
    write('loan-to-value', build('loan-to-value', [
        "Loan-to-Value from Loan Amount and Collateral Value",
        "Enter the loan amount and the collateral's appraised value to find the loan-to-value ratio.",
        "LTV = Loan Amount / Collateral Value",
        "/ Loan-to-Value (LTV) Calculator",
        "Loan-to-Value (LTV) Calculator",
        'View "Loan-to-Value from Loan Amount and Collateral Value User Guide"',
        "LTV = Loan / Collateral Value × 100%",
        "LTV = loan amount ÷ collateral appraised value. The denominator usually takes the lower of appraised value and transaction price to prevent 'over-appraisal lending'; a lower LTV means safer leverage and stronger resistance to negative equity when prices fall.",
        "Loan amount (yuan)",
        "Collateral value (yuan)",
        "The lower the LTV, the lower the risk.",
        "800,000 / 1,000,000 → 80%.",
        "📚 In-Depth: Loan-to-Value (LTV)",
        "Assess whether the mortgage pledge ratio meets the threshold when applying.",
        "Banks set LTV caps in risk control to limit exposure.",
        "Estimate the lendable headroom before a second charge or top-up.",
        "LTV for a 2,000,000 loan and 3,000,000 property appraisal",
        "LTV = loan amount ÷ collateral value = 200 ÷ 300 = 66.7%. Below the 70% first-home cap for most residences, so there is still lendable headroom.",
        "Is a lower LTV always better?",
        "For the bank, lower risk is better; for the borrower, lower LTV means a larger down payment and smaller leverage. High LTV gives high leverage but weak downside protection, and prices falling easily create 'negative equity'.",
        "Which is the denominator, appraised value or transaction price?",
        "Banks usually use the 'appraised value' rather than the transaction price (taking the lower one) to guard against over-appraisal lending. When the appraisal is below the transaction price, the LTV runs high.",
    ]))
    write('loan-total-interest', build('loan-total-interest', [
        "Total Interest = EMI × N − P",
        "The total interest paid over the whole loan cycle under equal installments.",
        "Loan Total Interest Calculator",
        "/ Loan Total Interest",
        "Loan Total Interest",
        'View "Total Interest = EMI × N − P User Guide"',
        "Total interest = total repayment − principal.",
        "Total interest = monthly payment × periods − principal. Under equal installments the early interest share is high and principal amortizes slowly; shortening the term or raising the payment significantly cuts total interest; equal principal costs less total interest but has higher early payments.",
        "500,000 at 4.9%, 30 years → total interest about 455,307.",
        "📚 In-Depth: Loan Total Interest",
        "Assess the full-cycle interest cost before borrowing.",
        "Compare total-interest differences across term options.",
        "Use as a baseline for",
        "early repayment",
        "interest-saving estimates.",
        "Total interest at payment 5,307, 360 periods, principal 1,000,000",
        "Total interest = EMI × N − P = 5,307 × 360 − 1,000,000 = 1,910,520 − 1,000,000 = 910,520 yuan. That is, 30-year mortgage interest nearly equals the principal.",
        "Why does total interest often approach or exceed the principal?",
        "Under long terms with low payments, most early payments go to interest and principal amortizes slowly, so cumulative interest is huge. Shortening the term or raising the payment significantly cuts total interest.",
        "How is the equal-principal total interest calculated?",
        "Equal principal fixes the monthly principal and declines the interest; total interest = Σ(remaining principal × monthly rate), less than equal installments but with higher early payments.",
    ]))
    write('net-worth', build('net-worth', [
        "Net Worth from Assets and Liabilities",
        "Enter total assets and total liabilities to find net worth.",
        "NW = Total Assets − Total Liabilities",
        "/ Net Worth Calculator",
        "Net Worth Calculator",
        'View "Net Worth from Assets and Liabilities User Guide"',
        "Net worth = assets − liabilities",
        "Net worth = total assets − total liabilities, including property, deposits, investments and mortgage, credit loans, etc. The own home counts as an asset but is illiquid; when analyzing solvency, 'investable net worth' is often listed separately.",
        "NW = assets − liabilities.",
        "500,000 − 200,000 → 300,000.",
        "📚 In-Depth: Net Worth",
        "Tally the true wealth level when taking stock of household finances.",
        "Demonstrate asset strength when applying for large credit facilities.",
        "Track net-worth trends periodically.",
        "Net worth at assets 5,000,000, liabilities 2,000,000",
        "Net worth = total assets − total liabilities = 500 − 200 = 300 (ten-thousand). If the own home is included but liabilities are mostly mortgage, distinguish 'net worth' from 'investable net worth'.",
        "Does the own home count as an asset?",
        "Yes. Net worth = all assets (property, deposits, investments) minus all liabilities (mortgage, auto loan, credit loan). But the own home is illiquid, so 'investable net worth' is often listed separately when analyzing solvency.",
        "Can net worth be negative?",
        "Yes. When liabilities exceed assets (e.g. a sharp price drop with high leverage) net worth is negative — colloquially 'insolvent' — so watch liquidity and default risk.",
    ]))
    write('nominal-from-effective', build('nominal-from-effective', [
        "Nominal Rate from Effective Annual Rate and Compounding Frequency",
        "Enter effective annual rate EAR and compounding times per year n to find the nominal annual rate.",
        "Derive Nominal Rate from Effective Rate",
        "/ Derive Nominal Rate from Effective Rate",
        'View "Nominal Rate from Effective Annual Rate and Compounding Frequency User Guide"',
        "Nominal r = n × ((1+EAR)^(1/n) − 1), back-solving the posted nominal annual rate from the true annualized EAR, used to unify the rate basis of products with different compounding frequencies; n is the compounding times per year.",
        "Effective annual rate EAR",
        "EAR = 5.116%, monthly compounding → 5.0%.",
        "📚 In-Depth: Nominal Rate Back-Solving",
        "Given a product's true annualized EAR, back-solve the posted nominal annual rate.",
        "Unify the rate basis of products with different compounding frequencies.",
        "Convert and compare rates across product brochures.",
        "Nominal rate at effective annual 6.18%, monthly compounding",
        "r = n × ((1+EAR)^(1/n) − 1) = 12 × ((1.0618)^(1/12) − 1) = 12 × (1.005 − 1) = 12 × 0.005 = 6.00%. That is, nominal 6% compounded monthly gives EAR 6.18%.",
        "Why is the nominal rate lower than the effective annual rate?",
        "Because compounding frequency amplifies returns. Nominal 6% compounded monthly actually yields 6.18%; the nominal is the 'posted basis' and the EAR is the 'received basis'.",
        "Does this conversion also apply to loans?",
        "The same math applies, only with reversed meaning: for a loan the EAR is the true cost and the nominal is the contractual figure, and cost comparison likewise looks at the EAR.",
    ]))

if __name__ == "__main__":
    main()
