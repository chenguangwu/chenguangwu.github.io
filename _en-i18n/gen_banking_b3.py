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
    write('fd-quarterly', build('fd-quarterly', [
        "Time Deposit Maturity Calculator",
        "The maturity amount of a time deposit compounded quarterly.",
        "/ Time Deposit (Quarterly Compounding)",
        "Time Deposit (Quarterly Compounding)",
        'View "Time Deposit (Quarterly Compounding) User Guide"',
        "Time deposit (quarterly compounding): maturity A = P × (1 + annual rate ÷ 4)^(4t); total interest = A − P; principal-plus-interest multiple = A ÷ P; effective annual rate EAR = (1 + r ÷ 4)^4 − 1, slightly above the same-tenor simple interest, used for deposit and wealth-management return accounting.",
        "100,000 at 3% for 5 years (quarterly) → about 116,075.",
        "Quarterly compounding rolls interest.",
        "📚 In-Depth: Time Deposit Maturity (Quarterly Compounding)",
        "Estimate the maturity interest and principal-plus-interest of a lump-sum time deposit.",
        "Compare time-deposit returns across tenors and banks.",
        "Compare quarterly-compounded deposits with simple-interest deposits side by side.",
        "Principal 50,000, annual 2.6%, 1 year (quarterly compounding)",
        "Quarterly rate = 2.6% ÷ 4 = 0.65%. Maturity = 50,000 × (1 + 0.0065)^4 ≈ 50,000 × 1.02626 = 51,313 yuan, interest about 1,313 yuan (about 13 yuan more than the 1,300 simple interest).",
        "How is interest calculated if withdrawn before maturity?",
        "Early withdrawal usually accrues at the demand rate on the withdrawal day; whether already-credited quarterly interest is kept depends on the bank. Urgent cash needs forfeit most of the time-deposit interest.",
        "At what rate is automatic rollover credited?",
        "Automatic rollover at maturity generally uses the bank's posted same-tenor rate on the rollover day, not the original rate. When rates fall, the rollover rate may be lower than before.",
    ]))
    write('fisher-real-rate', build('fisher-real-rate', [
        "Fisher Real Interest Rate Calculator",
        "Compute the real interest rate from the nominal rate and inflation using the exact Fisher equation.",
        "/ Fisher Real Interest Rate",
        "Fisher Real Interest Rate",
        'View "Fisher Real Interest Rate Calculator User Guide"',
        "Exact Fisher: (1+nominal) = (1+real)(1+inflation), so real = (1+nominal) ÷ (1+inflation) − 1. The approximation 'nominal − inflation' only holds at low rates and low inflation; at high inflation the cross term is not negligible and the exact form must be used.",
        "Nominal rate (%)",
        "Inflation rate (%)",
        "Nominal 6%, inflation 2% → real about 3.922%.",
        "The approximation is nominal − inflation.",
        "📚 In-Depth: Fisher Real Interest Rate",
        "Assess an investment's true purchasing-power return after stripping out inflation.",
        "Compare real returns across countries with the same nominal rate but different inflation.",
        "Judge whether money is truly growing when planning long-term savings.",
        "Real rate at nominal 5%, inflation 3%",
        "Exact Fisher: (1+nominal) = (1+real)(1+inflation) → real = (1.05 ÷ 1.03) − 1 = 1.019417 − 1 = 1.9417%. The approximation nominal − inflation = 2%, exact value slightly lower; the gap widens at high inflation.",
        "Where does the exact Fisher differ from the approximation i ≈ n − π?",
        "The approximation ignores the cross term (real × inflation) and is close only at low rates and low inflation. At high inflation the cross term is not negligible and the exact (1+n)/(1+π) − 1 must be used.",
        "What does a negative real rate mean?",
        "When the nominal rate is below inflation, the real rate is negative and deposit purchasing power falls over time — money 'shrinks as it sits'. Real assets or inflation-hedging vehicles then become more attractive.",
        "How to use the Fisher real interest rate calculator",
        "Enter the nominal rate (e.g. the bank's posted annual rate) and the expected inflation rate, choose exact or approximate basis, and click calculate to get the inflation-stripped real rate, used to judge whether purchasing power truly grows.",
        "Fisher equation real rate r ≈ (1+nominal rate)/(1+inflation rate) − 1, approx r ≈ nominal − inflation. The true growth rate of funds after removing price changes.",
        "At nominal 5%, inflation 2% the real rate is about 2.94% (exact) or 3% (approx). A negative real rate means purchasing power declines.",
    ]))
    write('future-value-annuity-due', build('future-value-annuity-due', [
        "Future Value of an Annuity Due from Periodic Payment, Rate and Periods",
        "Enter periodic payment PMT, periodic rate r and periods n to find the annuity-due future value.",
        "Annuity-Due Future Value Calculator",
        "/ Annuity-Due Future Value Calculator",
        'View "Future Value of an Annuity Due from Periodic Payment, Rate and Periods User Guide"',
        "FV = PMT × [(1+r)^n − 1] ÷ r × (1+r); each annuity-due payment earns one extra period of interest, so FV = same-parameter ordinary annuity × (1+r). Applies to rent, insurance premiums and other beginning-of-period payment streams.",
        "100 yuan, 0.5%/period, 12 periods → about 1,240 yuan.",
        "📚 In-Depth: Annuity-Due Future Value",
        "The maturity accumulation of beginning-of-period payment streams such as rent and insurance.",
        "Estimate the maturity principal-plus-interest of a start-of-month recurring investment.",
        "Compare the annuity due with the ordinary",
        "annuity future value",
        "difference.",
        "1,000 per period, monthly rate 0.5%, 12-period annuity due",
        "FV = PMT × [(1+r)^n − 1] ÷ r × (1+r) = 1,000 × [(1.005^12 − 1) ÷ 0.005] × 1.005 = 1,000 × [0.061678 ÷ 0.005] × 1.005 = 1,000 × 12.3356 × 1.005 ≈ 12,397 yuan. One extra period of interest versus the ordinary annuity.",
        "How much does an annuity due differ from an ordinary annuity?",
        "Each annuity-due payment earns one extra period of interest, so FV = ordinary annuity × (1+r). The gap widens with more periods in long-term investing.",
        "Which cash flows are annuities due?",
        "Rent, insurance premiums and pension contributions are mostly paid at the beginning and are annuities due; wages and interest are mostly at period end and are ordinary annuities.",
    ]))
    write('growing-annuity-pv', build('growing-annuity-pv', [
        "Present Value of a Growing Annuity from First Cash Flow, Growth and Discount Rate",
        "Enter first cash flow C, discount rate r, growth rate g and periods n to find the growing-annuity present value.",
        "Growing Annuity Present Value Calculator",
        "/ Growing Annuity Present Value Calculator",
        'View "Present Value of a Growing Annuity from First Cash Flow, Growth and Discount Rate User Guide"',
        "C=100, r=5%, g=2%, n=10 → about 840 yuan.",
        "PV = C ÷ (r − g) × [1 − ((1+g)/(1+r))^n], where C is the first cash flow, r the discount rate, g the growth rate and n the periods. Requires r > g, otherwise the PV diverges and the formula fails.",
        "First cash flow C (yuan)",
        "📚 In-Depth: Growing Annuity Present Value",
        "Value a dividend/rent stream that grows at a fixed rate each year.",
        "Value inflation-linked pension liabilities.",
        "Discount growing cash flows in corporate finance.",
        "First 1,000, discount rate 8%, growth rate 3%, 10 periods",
        "PV = C ÷ (r − g) × [1 − ((1+g)/(1+r))^n] = 1,000 ÷ 0.05 × [1 − (1.03/1.08)^10] = 20,000 × [1 − 0.6188] = 20,000 × 0.3812 ≈ 7,624 yuan.",
        "Can the growth rate exceed the discount rate?",
        "No. The growing-annuity formula requires r > g, otherwise the PV diverges and the formula fails. If g ≥ r, use a perpetuity or another model with care.",
        "How is it related to the growing perpetuity?",
        "The finite-n growing annuity is the perpetuity PV = C ÷ (r − g) minus the present value of the tail after period n, i.e. the [1 − ((1+g)/(1+r))^n] correction term in the formula.",
    ]))
    write('loan-remaining-balance', build('loan-remaining-balance', [
        "Loan Remaining Principal Calculator",
        "The unpaid principal balance after k periods have been repaid.",
        "/ Loan Remaining Principal",
        "Loan Remaining Principal",
        'View "Loan Remaining Principal Calculator User Guide"',
        "Periods repaid k",
        "500,000 at 4.9%, 30 years, 60 periods repaid → balance about 451,000.",
        "k must not exceed the total periods N.",
        "📚 In-Depth: Loan Remaining Principal",
        "Early repayment",
        "Query the current remaining principal beforehand to work out the interest that can be saved.",
        "Settle the loan balance to be cleared when selling the home or refinancing.",
        "Reconcile the remaining principal against the bank statement.",
        "Balance of a 1,000,000 loan, monthly rate 0.4083%, after 60 periods repaid",
        "B_k = P(1+r)^k − PMT × ((1+r)^k − 1) ÷ r. Substituting P=1,000,000, r=0.004083, k=60, PMT=5,307: B_60 ≈ 1,000,000 × 1.2786 − 5,307 × 682.0 ≈ 907,300 yuan.",
        "Is remaining principal the same as principal already repaid?",
        "No. Principal repaid = total paid − interest paid; remaining principal = original loan − principal repaid. Under equal installments the early interest paid is large, so remaining principal falls slowly.",
        "How much interest can early repayment save?",
        "What is saved is the interest that would otherwise have been paid on the remaining principal in future periods. The more and earlier you repay, the more you save; some banks charge a prepayment penalty, so compare after netting it out.",
    ]))

if __name__ == "__main__":
    main()
