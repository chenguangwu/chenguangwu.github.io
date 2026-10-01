#!/usr/bin/env python3
# gen_tax_b3.py — tax b3 (5 slugs): gift-tax/gst-calculator/interest-income-tax/marginal-tax-rate/payroll-tax
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

GFT = [
 "Compute gift tax from gift amount, exemption and rate",
 "Enter gift amount, exemption and rate to get the gift tax.",
 "T = max(Gift - Exemption, 0) x Rate",
 "/ Gift Tax Calculator",
 "Gift Tax Calculator",
 "📖 View Guide: \"Compute gift tax from gift amount, exemption and rate\"",
 "Gift Amount (CNY)",
 "Exemption (CNY)",
 "Only the amount above the exemption is taxed.",
 "(1M-200K)x20% -> 160K.",
 "📚 Deep Dive: Gift Tax",
 "Levy on net gifted property (gift amount - exemption) x rate.",
 "Estimate the tax cost of large wealth transfers.",
 "Compare tax due under different exemptions.",
 "Gift 1M, exemption 200K, rate 20%",
 "Taxable net = max(1000000 - 200000, 0) = 800,000; gift tax = 800000 x 0.20 = 160,000.",
 "Below the exemption",
 "If gift 150K, exemption 200K, taxable net 0, tax 0, no payment due.",
 "How is gift tax related to estate tax?",
 "The two are often paired to prevent avoidance; gift tax targets lifetime transfers, estate tax targets post-death inheritance.",
 "Is the exemption per gift or cumulative?",
 "Depends on the system: per-gift or lifetime cumulative per taxpayer; follow local rules.",
]

GST = [
 "🧾 GST (Goods and Services Tax) Calculator",
 "GST is adopted by many countries; invoices often show tax-inclusive prices. Enter the inclusive or pre-tax amount and rate to split out the tax, easing reimbursement, filing and reconciliation.",
 "/ GST (Goods and Services Tax) Calculator",
 "📖 View the GST Calculator Guide",
 "GST: pre-tax price x rate = tax; tax-inclusive = pre-tax x (1 + rate); reverse from inclusive: pre-tax = inclusive / (1 + rate); common rates: Singapore 9%, Australia 10%, India 18%, for cross-border quoting and invoice checks.",
 "Tax Rate (%)",
 "Amount Type",
 "Inclusive price -> pre-tax / tax",
 "Pre-tax price -> inclusive / tax",
 "Inclusive = pre-tax x (1 + rate); pre-tax = inclusive / (1 + rate). Always distinguish the two bases when splitting tax.",
 "Common GST rates: Australia 10%, New Zealand 15%, Singapore 9%, Canada federal 5% (provinces add PST/HST); this tool handles any rate.",
 "If an invoice marks 'inclusive' but you tax it as pre-tax, you double-count; confirm the amount type before reimbursement.",
 "📋 Formula",
 "Given",
 "Find",
 "Inclusive",
 "Inclusive / (1+r%)",
 "Pre-tax x (1+r%)",
 "Any",
 "📚 Deep Dive: GST inclusive / exclusive conversion",
 "Back-solve pre-tax price and tax from an inclusive amount, or the reverse.",
 "Split price and tax for cross-border e-commerce and invoicing.",
 "Compare across",
 "tax rates' inclusive prices.",
 "Inclusive 110, rate 10% (incl mode)",
 "Pre-tax = 110 / (1 + 0.10) = 100; tax = 110 - 100 = 10; inclusive 110.",
 "Ex-tax 110, rate 10% (ex mode)",
 "Tax = 110 x 0.10 = 11; inclusive = 110 + 11 = 121.",
 "How to tell inclusive from exclusive price?",
 "Inclusive price embeds GST; exclusive is the tax base. Convert: inclusive / (1+rate) = exclusive; exclusive x rate = tax.",
 "Is a negative rate rejected?",
 "This tool warns and halts on a negative rate; the rate must be non-negative.",
]

IIT = [
 "Tax = Interest x Rate",
 "Compute withholding tax from interest income and the applicable rate.",
 "Interest Income Tax Calculator",
 "/ Interest Income Tax",
 "Interest Income Tax",
 "📖 View Guide: \"Tax = Interest x Rate\"",
 "= Interest",
 "Interest Amount",
 "Interest 5000, 20% -> Tax 1000.",
 "Some government-bond interest is tax-exempt.",
 "📚 Deep Dive: Interest Income Tax",
 "Levy interest income x rate to compute after-tax interest.",
 "Compare tax-inclusive returns on deposits vs bonds.",
 "Assess the difference from tax-exempt interest (e.g. government bonds).",
 "Interest 5000, rate 20%",
 "Interest income tax = 5000 x 0.20 = 1,000; after-tax interest = 5000 - 1000 = 4,000.",
 "Tax-exempt case",
 "If interest is from a tax-exempt item (rate 0), tax 0 and after-tax interest is the full 5000.",
 "Which interest may be exempt?",
 "Interest on treasury and local bonds is often exempt; follow current tax law.",
 "Enter rate as decimal or percent?",
 "Enter r as a percent (e.g. 20 means 20%); it is treated as 0.20 internally.",
]

MTR = [
 "Marginal rate from tax difference over income difference of adjacent brackets",
 "Enter two income levels and their tax payable to compute the marginal rate.",
 "Marginal Tax Rate Calculator",
 "/ Marginal Tax Rate Calculator",
 "📖 View Guide: \"Marginal rate from tax difference over income difference\"",
 "MTR = ΔTax / ΔIncome. Income +50K, tax +15K -> 30%.",
 "Income 1 Y1 (CNY)",
 "Tax 1 T1 (CNY)",
 "Income 2 Y2 (CNY)",
 "Tax 2 T2 (CNY)",
 "MTR = ΔTax / ΔIncome.",
 "Income +50K, tax +15K -> 30%.",
 "📚 Deep Dive: Marginal Tax Rate",
 "Tax difference between two income tiers divided by income difference gives the marginal rate on incremental income.",
 "Assess the extra tax from a raise or a side job.",
 "Compare incentive changes at progressive bracket boundaries.",
 "Income 100K->150K, tax 20K->35K",
 "MTR = (35000 - 20000) / (150000 - 100000) = 15000 / 50000 = 0.30, i.e. 30%.",
 "Cross-bracket check",
 "If the next bracket adds only 10K tax, MTR=20%, meaning incremental income falls in a lower bracket.",
 "What does the marginal rate indicate?",
 "It shows how much tax per extra yuan earned; key for decisions on incremental actions (overtime, investment).",
 "Average tax rate",
 "How to read it together?",
 "Marginal views the increment, average the whole; under high progressivity marginal far exceeds average, dampening the marginal incentive for extra income.",
]

PRT = [
 "Compute total payroll tax from wage and both-side rates",
 "Enter total wage, employer rate and employee rate to get the payroll tax.",
 "T = Wage x (Employer Rate + Employee Rate)",
 "/ Payroll Tax Calculator",
 "Payroll Tax Calculator",
 "📖 View Guide: \"Compute total payroll tax from wage and both-side rates\"",
 "Payroll tax = wage x (employer + employee rate). 10K x (0.2+0.08) -> 2,800.",
 "Total Wage (CNY)",
 "Employer Rate",
 "Employee Rate",
 "Payroll tax = wage x (employer + employee rate).",
 "10K x (0.2+0.08) -> 2,800.",
 "📚 Deep Dive: Payroll Tax (Employer + Employee)",
 "Sum payroll tax as wage x (employer rate + employee rate).",
 "Employers estimate total labor cost; employees see the actual deduction.",
 "Compare social-security-plus-payroll rates across regions.",
 "Wage 10K, employer 20% + employee 8%",
 "Payroll tax T = 10000 x (0.20 + 0.08) = 2,800; employer bears 2,000 and employee 800.",
 "Change in combined rate",
 "If the combined rate drops to 24%, tax = 10000 x 0.24 = 2,400, saving 400 vs 28%.",
 "Who bears the payroll tax?",
 "Legally employer and employee pay separately, but the employee's burden shows through wage bargaining; the combined rate sets total cost.",
 "Is there a contribution-base cap?",
 "Most social-security payroll taxes cap the contribution base; excess is untaxed. This tool is a simplified proportional model.",
]

write('gift-tax', build('gift-tax', GFT))
write('gst-calculator', build('gst-calculator', GST))
write('interest-income-tax', build('interest-income-tax', IIT))
write('marginal-tax-rate', build('marginal-tax-rate', MTR))
write('payroll-tax', build('payroll-tax', PRT))
