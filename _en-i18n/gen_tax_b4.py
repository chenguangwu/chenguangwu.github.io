#!/usr/bin/env python3
# gen_tax_b4.py — tax b4 (5 slugs): progressive-income-tax/property-tax/reverse-charge/sales-tax-addon/social-security-tax
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

PIT = [
 "Tiered sum: each bracket (taxable - lower) x bracket rate",
 "Income tax under three progressive brackets (brackets and rates customizable).",
 "Progressive Income Tax Calculator",
 "/ Progressive Income Tax",
 "Progressive Income Tax",
 "📖 View Guide: \"Tiered sum: each bracket (taxable - lower) x bracket rate\"",
 "3000=6000. Adjust brackets to simulate personal/corporate income tax.",
 "Taxable Income",
 "Bracket 1 Upper",
 "Bracket 1 Rate (%)",
 "Bracket 2 Upper",
 "Bracket 2 Rate (%)",
 "Bracket 3 Rate (%)",
 "30000, 10/20/30 three brackets -> 1000+2000+3000=6000.",
 "Adjust brackets to simulate personal/corporate income tax.",
 "📚 Deep Dive: Excess Progressive Personal Income Tax",
 "Split income into tiers with different rates to compute tax due and",
 "effective rate",
 "Compare how tax burden jumps across incomes under progressivity.",
 "Verify the marginal effect that 'earning more does not cost too much more'.",
 "Income 30K, three tiers 10%/20%/30%",
 "Tax = 10000x10% + 10000x20% + 10000x30% = 1000+2000+3000 = 6,000; effective rate = 6000/30000 = 20%.",
 "Income rises to 50K",
 "First 30K still 6000; the extra 20K at 30% adds 6000; total 12000, effective rate up to 24%.",
 "Difference between excess and full progressive?",
 "Excess progressive taxes only the part above each tier at the higher rate; full progressive jumps the whole income to the higher bracket, so the former is smoother.",
 "Why is the effective rate below the top",
 "marginal rate",
 "Because lower income faces lower brackets, the overall average effective rate stays below the top marginal rate.",
 "How to use Tiered sum: each bracket (taxable - lower) x bracket rate",
 "What does Tiered sum: each bracket (taxable - lower) x bracket rate do?",
 "Enter taxable income and customize each bracket's lower bound and rate; compute three-or-more-bracket progressive tax by tiered sum (each bracket (taxable - lower) x rate), for wage and business income grading.",
 "How do I use Tiered sum: each bracket (taxable - lower) x bracket rate?",
 "Which scenarios suit Tiered sum: each bracket (taxable - lower) x bracket rate?",
]

PRY = [
 "Tax = Taxable Residual Value x Rate",
 "Levy on the residual value after deducting a ratio from the original value (or on rent).",
 "Property Tax Calculator",
 "/ Property Tax",
 "Property Tax",
 "📖 View Guide: \"Tax = Taxable Residual Value x Rate\"",
 "= Taxable Residual Value",
 "Taxable Residual Value",
 "Residual 800K, 1.2% -> annual tax 9,600.",
 "Rent-based levy uses a rent percentage.",
 "📚 Deep Dive: Property Tax (by original value / rent)",
 "Estimate annual property tax as original value x annual rate.",
 "Compare owner-occupied vs rented (rent-based) levy methods.",
 "Assess the tax cost of holding multiple properties.",
 "Original value 800K, annual rate 1.2%",
 "Annual property tax = 800000 x 0.012 = 9,600; if original value 1M, tax is 12,000.",
 "Rent-based levy comparison",
 "If switched to rent-based (e.g. 12%), annual rent 60K gives tax 7,200, below the 9,600 ad-valorem.",
 "How to choose ad-valorem vs rent-based?",
 "Owner-used property is mostly ad-valorem (original value minus deduction x rate); rented property by rent, per local rules.",
 "Are there exempt area or deductions?",
]

RVC = [
 "Compute withholding tax from withheld amount and levy rate",
 "Enter the withheld amount and levy rate to get the withholding tax.",
 "T = Amount x Levy Rate",
 "/ Withholding Tax Calculator",
 "Withholding Tax Calculator",
 "📖 View Guide: \"Compute withholding tax from withheld amount and levy rate\"",
 "Withholding = withheld amount x levy rate",
 "Withheld Amount (CNY)",
 "Levy Rate",
 "Often used to withhold on small service payments.",
 "5000x3% -> 150.",
 "📚 Deep Dive: Reverse Charge (Withholding)",
 "Cross-border services and specific dealings: the buyer withholds VAT/tax.",
 "Given the withholding base and rate, compute the amount to remit.",
 "Domestic buyer remits when the foreign supplier has no local establishment.",
 "Withholding base 5000, rate 3%",
 "Withholding T = 5000 x 0.03 = 150; base doubled to 10000 remits 300.",
 "Tax-inclusive base case",
 "If 5000 is inclusive and rate 3%, exclusive = 5000/1.03 ≈ 4854, remit ≈ 145.63.",
 "What is a reverse charge?",
 "Tax that the seller should pay is instead withheld and declared by the buyer at payment, common in cross-border services.",
 "Does the seller still pay after withholding?",
 "The seller no longer pays domestically on that item; the buyer's withholding settles the obligation.",
 "How to use Compute withholding tax from withheld amount and levy rate",
 "What does Compute withholding tax from withheld amount and levy rate do?",
 "Enter the amount to withhold and the levy rate; compute the withheld VAT or tax as amount x rate, for the payer's quick calculation under a withholding obligation.",
 "How do I use Compute withholding tax from withheld amount and levy rate?",
 "Which scenarios suit Compute withholding tax from withheld amount and levy rate?",
 "Reverse charge: the VAT obligation is declared and paid by the buyer, not the seller; the seller issues a tax-exclusive invoice.",
 "Common in B2B cross-border services/goods and specific industries' input-credit chains; the result shows who computes and declares tax when reverse charge applies. Follow the latest VAT rules.",
]

STA = [
 "Inclusive = Price x (1 + Rate)",
 "A consumption tax added as a percentage on top of the price.",
 "Sales Tax (Add-on) Calculator",
 "/ Sales Tax (Consumption Tax)",
 "Sales Tax (Consumption Tax)",
 "📖 View Guide: \"Inclusive = Price x (1 + Rate)\"",
 "= Price",
 "Pre-tax Price",
 "100, 5% -> tax 5, inclusive 105.",
 "Same as VAT, an add-on tax.",
 "📚 Deep Dive: Sales Tax (Add-on)",
 "Add sales tax by rate on the marked price; compute tax and inclusive price.",
 "US-style sales tax shown separately at checkout.",
 "Compare take-home price gaps across state sales-tax rates.",
 "List price 100, rate 5%",
 "Consumption tax = 100 x 0.05 = 5; inclusive price = 100 x (1 + 0.05) = 105.",
 "Rate 8%",
 "Tax 8, inclusive 108, paying 3 more than at 5%.",
 "Sales tax vs",
 "VAT",
 "— how do they differ?",
 "Sales tax is mostly single-stage retail and add-on; VAT is multi-stage credit and may be either; mechanisms differ.",
 "Is the list price inclusive?",
 "This tool treats the list price as the base; tax is added at checkout (add-on), inclusive = list x (1+rate).",
]

SST = [
 "Compute social-security contribution from base and rate",
 "Enter the contribution base and composite social-security rate to get the contribution.",
 "T = Contribution Base x Rate",
 "/ Social Security Contribution Calculator",
 "Social Security Contribution Calculator",
 "📖 View Guide: \"Compute social-security contribution from base and rate\"",
 "Contribution = base x rate",
 "Contribution Base (CNY)",
 "Composite rate covering pension / medical / unemployment etc.",
 "10K x 18% -> 1,800.",
 "📚 Deep Dive: Social Security Contributions",
 "Estimate contributions as base x social-security rate.",
 "Cases where employee/employer bear separately or combined.",
 "Compare the impact of different base caps.",
 "Base 10K, rate 18%",
 "Contribution T = 10000 x 0.18 = 1,800; rate up to 20% gives 2,000.",
 "Above the cap",
 "If base cap is 30K and actual wage 50K, charge on 30K: 30000 x 0.18 = 5,400.",
 "Are there base caps on contributions?",
 "Usually a base range (60%-300% of average wage); excess is capped at the upper limit.",
 "How much does unit vs individual pay?",
 "Pension, medical etc. are paid by unit and individual at separate ratios; this tool is a rate-summary example.",
]

write('progressive-income-tax', build('progressive-income-tax', PIT))
write('property-tax', build('property-tax', PRY))
write('reverse-charge', build('reverse-charge', RVC))
write('sales-tax-addon', build('sales-tax-addon', STA))
write('social-security-tax', build('social-security-tax', SST))
