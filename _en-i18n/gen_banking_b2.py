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
    write('credit-card-interest-monthly', build('credit-card-interest-monthly', [
        "Monthly Interest from Outstanding Balance and Daily Rate",
        "Enter the outstanding balance, daily rate and days accrued to find the interest.",
        "I = Balance × Daily Rate × Days",
        "/ Credit Card Revolving Interest Calculator",
        "Credit Card Revolving Interest Calculator",
        'View "Monthly Interest from Outstanding Balance and Daily Rate User Guide"',
        "I = balance × daily rate × days. 1000 yuan, 0.05%/day, 30 days → 15 yuan.",
        "Monthly interest = balance × daily rate × days accrued. Most banks, if not paid in full, charge daily interest from each transaction's posting date and the grace period is lost; annualized this is about daily rate × 365 (e.g. 0.05%×365≈18.25%).",
        "Outstanding balance (yuan)",
        "Daily rate",
        "Days accrued (days)",
        "I = balance × daily rate × days.",
        "1000 yuan, 0.05%/day, 30 days → 15 yuan.",
        "📚 In-Depth: Credit Card Revolving Interest",
        "Estimate the monthly revolving interest cost when not paid in full.",
        "Compare the interest difference between minimum and full payment.",
        "Remind cardholders that paying within the grace period avoids interest.",
        "Balance 5,000, daily rate 0.05%, 30 days accrued",
        "Monthly interest = balance × daily rate × days = 5,000×0.0005×30 = 75 yuan. About 0.05%×30=1.5% monthly, ≈18% annualized.",
        "Why is interest so high if only the minimum is paid?",
        "The unpaid part accrues daily interest from each transaction's posting date (most banks drop the grace period), and the remaining principal keeps compounding next month, so long-run cost far exceeds installments.",
        "Is interest charged if paid within the grace period?",
        "Paying the full amount within the grace period between statement and due date usually incurs no revolving interest. Once you choose minimum payment or default, the grace treatment is lost.",
    ]))
    write('daily-interest', build('daily-interest', [
        "I = P × r × Days / 365",
        "Short-term interest computed by actual days and annual rate.",
        "Daily Interest Calculator",
        "/ Daily Interest",
        "Daily Interest",
        'View "Daily Interest Calculator User Guide"',
        "Daily rate ≈ annual / 365.",
        "Interest = principal × daily rate × actual days, where daily rate = annual rate / base (domestic practice commonly uses 360 or actual 365). 'Count head not tail' means the withdrawal day earns no interest, so cross-day funds must verify the days accrued.",
        "Days d",
        "100,000, 3.65%, 100 days → interest about 1000.",
        "📚 In-Depth: Daily Interest",
        "Demand deposits, advances and short-term lending accrue interest by actual days.",
        "Verify the bank's actual days accrued under 'count head not tail'.",
        "Estimate interest on cross-month, cross-year short-term loans.",
        "Principal 100,000, annual 3.65%, held 90 days",
        "Daily rate = 3.65%/360 ≈ 0.010139%/day (banking commonly uses a 360-day base). Interest = 100,000×0.00010139×90 ≈ 912.5 yuan. (If actual 365 days, it is 900 yuan; the difference comes from the base.)",
        "Use 360 or 365 days for accrual?",
        "Domestic RMB mostly uses actual/360 or actual/365, while foreign currency and products vary. Under the same rate the base differs by about 1.4%, so follow the product terms.",
        "What does 'count head not tail' mean?",
        "Most deposits accrue from the deposit day (head) and stop the day before withdrawal (not tail), so the withdrawal day earns no interest. This affects the interest days for cross-day funds.",
    ]))
    write('debt-to-income', build('debt-to-income', [
        "Debt-to-Income Ratio from Monthly Debt and Income",
        "Enter monthly debt payments and monthly income to find the debt-to-income ratio.",
        "DTI = Monthly Debt / Monthly Income",
        "/ Debt-to-Income (DTI) Calculator",
        "Debt-to-Income (DTI) Calculator",
        'View "Debt-to-Income Ratio from Monthly Debt and Income User Guide"',
        "DTI = monthly debt / monthly income × 100%",
        "DTI = monthly debt / monthly income; the common warning line is 43%–50%, and lower means less repayment pressure. It includes only debt payments such as mortgage, auto loan and credit-card minimum, not daily consumption.",
        "Monthly debt payment (yuan)",
        "DTI is generally advised below 43%.",
        "📚 In-Depth: Debt-to-Income Ratio (DTI)",
        "Self-test repayment capacity before applying for a mortgage.",
        "Banks assess the safe boundary of monthly payment versus income when granting credit.",
        "Control overall debt level before planning new loans.",
        "DTI for monthly debt 8,000, monthly income 20,000",
        "DTI = monthly debt / monthly income = 8,000/20,000 = 40%. Most banks require mortgage DTI not above 50% (including this loan's payment); 40% is acceptable but with limited room.",
        "What DTI is considered safe?",
        "The common warning line is 43%–50%. Higher DTI means greater default risk; below 36% is usually seen as light repayment pressure.",
        "Does DTI count living expenses?",
        "Standard DTI counts only debt payments (mortgage, auto loan, credit-card minimum, etc.), not daily consumption like food and transport. Some institutions use a separate 'DTI including living expenses' basis.",
    ]))
    write('effective-annual-rate', build('effective-annual-rate', [
        "Effective Annual Rate (EAR) Calculator",
        "The true annualized return of a nominal annual rate converted by compounding frequency.",
        "/ Effective Annual Rate (EAR)",
        'View "Effective Annual Rate (EAR) User Guide"',
        "EAR=(1+r/n)^n−1, with r the nominal annual rate and n the compounding frequency; it is the true annualized cost of a loan. Compare credit products by EAR, not the contractual APR; high-frequency compounding significantly raises the cost.",
        "Nominal annual rate r (%)",
        "6% nominal, monthly compounding → EAR≈6.168%.",
        "Larger n makes EAR closer to continuous compounding.",
        "📚 In-Depth: Effective Annual Rate (EAR)",
        "Convert a loan with 'nominal annual rate + monthly compounding' into its true annualized cost.",
        "Compare the true rates of credit products at different compounding frequencies.",
        "Identify the hidden cost of 'low nominal rate but high-frequency compounding'.",
        "Effective annual rate at nominal 12%, monthly compounding",
        "EAR=(1+0.12/12)^12−1=1.01^12−1≈0.12683=12.683%. Monthly compounding makes the true cost 0.683 percentage points above the nominal 12%.",
        "Is EAR the same as APR?",
        "No. APR (annual percentage rate) usually shows only the nominal rate and ignores compounding frequency; EAR includes it and is the true annualized cost. Compare loans by EAR.",
        "Why is EAR used for credit cards?",
        "A credit-card daily rate (e.g. 0.05%/day) underestimates if simply ×365 because of daily compounding. Converting to EAR enables fair comparison with annualized products, about 19.56%.",
    ]))
    write('emi-loan', build('emi-loan', [
        "Loan Monthly Payment (EMI) Calculator",
        "The fixed monthly payment under equal-monthly-installment repayment.",
        "/ Equal-Installment Monthly Payment (EMI)",
        "Equal-Installment Monthly Payment (EMI)",
        'View "Loan Monthly Payment (EMI) Calculator User Guide"',
        "500,000, 4.9%, 30 years → monthly payment about 2653.63.",
        "r is the monthly rate.",
        "📚 In-Depth: Loan Monthly Payment (EMI)",
        "Estimate the fixed monthly payment before applying for a mortgage or auto loan.",
        "Compare total-interest differences across terms.",
        "Assess",
        "early repayment",
        "the interest that can be saved.",
        "Monthly payment for loan 1,000,000, annual 4.9%, 30 years (360 periods)",
        "Monthly rate r=4.9%/12=0.4083%. EMI=P·r·(1+r)^n/((1+r)^n−1)=1,000,000×0.004083×1.004083^360/(1.004083^360−1)≈5,307. Total repayment about 1.91 million, interest about 0.91 million.",
        "Which saves more interest, equal installments or equal principal?",
        "Equal principal repays more principal early and costs less total interest, but has higher early payments; equal installments keep payments fixed with slightly more total interest. Choose equal installments if cash-tight, equal principal to save total interest.",
        "Is early repayment worthwhile?",
        "Early repayment reduces remaining principal and compresses later interest, especially effective early (when interest share is high). Weigh any prepayment penalty and alternative returns on the cash.",
    ]))

if __name__ == "__main__":
    main()
