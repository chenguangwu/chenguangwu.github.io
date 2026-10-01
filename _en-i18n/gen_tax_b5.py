#!/usr/bin/env python3
# gen_tax_b5.py — tax b5 (5 slugs): specific-duty/stamp-duty/tax-credit/tax-on-discount/tax-to-gdp
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

SPD = [
 "Compute specific duty from taxable quantity and unit tax",
 "Enter taxable quantity and unit tax to get the specific duty.",
 "T = Quantity x Unit Tax",
 "/ Specific Duty Calculator",
 "Specific Duty Calculator",
 "📖 View Guide: \"Compute specific duty from taxable quantity and unit tax\"",
 "Specific duty = quantity x unit tax",
 "Taxable Quantity (units)",
 "Unit Tax (CNY/unit)",
 "Specific duty is levied as a fixed amount per quantity.",
 "100 units x 5 -> 500.",
 "📚 Deep Dive: Specific Duty (fixed per quantity)",
 "A fixed tax per unit, independent of price.",
 "Scenarios like refined oil, beer, cigarettes levied by quantity.",
 "Compare ad valorem vs specific impact on low/high-price goods.",
 "Quantity 100, unit tax 5",
 "Specific duty T = 100 x 5 = 500; quantity doubled to 200 gives 1000.",
 "Vs ad valorem",
 "If the same batch is worth 10K with 10% ad valorem, ad-valorem tax is 1000, specific 500; specific is lighter on cheap goods.",
 "Advantages of specific duty?",
 "Stable revenue and simple administration; it relatively burdens low-quality cheap goods, aiding quality upgrade.",
 "On what basis is unit tax set?",
 "A fixed amount per statutory unit (ton, liter, piece), unrelated to the marked price.",
]

STD = [
 "Tax = Instrument Amount x Stamp Rate",
 "Compute from the taxable instrument amount and applicable stamp rate.",
 "Stamp Duty Calculator",
 "/ Stamp Duty",
 "📖 View Guide: \"Tax = Instrument Amount x Stamp Rate\"",
 "= Instrument Amount",
 "Instrument Amount",
 "Stamp Rate (%)",
 "1M, 0.05% -> tax 500.",
 "Different instruments have different rates.",
 "📚 Deep Dive: Stamp Duty",
 "Levy on contracts and property-transfer documents as amount x stamp rate.",
 "Estimate contract tax on purchases, loans and property transfers.",
 "Compare rates across tax items.",
 "Amount 1M, rate 0.05%",
 "Stamp tax = 1000000 x 0.0005 = 500; amount 2M gives 1000.",
 "Fixed vs proportional",
 "Some certificates are fixed per item (e.g. 5/item), unrelated to amount; this is a proportional ad-valorem model.",
 "Is stamp duty an act tax?",
 "It taxes the act of writing or receiving instruments in economic activity, a document tax.",
 "Which instruments are exempt?",
 "Instruments with legal effect that match the exemption list may be exempt, per the current tax-item table.",
]

TCR = [
 "Compute net tax from tax due and tax credit",
 "Enter tax due and creditable amount to get the post-credit payable.",
 "T' = Tax Due - Credit",
 "/ Post-Credit Tax Payable Calculator",
 "Post-Credit Tax Payable Calculator",
 "📖 View Guide: \"Compute net tax from tax due and tax credit\"",
 "Payable = max(Tax Due - Credit, 0)",
 "Tax Due (CNY)",
 "Credit (CNY)",
 "Credit cuts the tax directly (not the income).",
 "5000-1000 -> 4000.",
 "📚 Deep Dive: Tax Credit",
 "Subtract creditable amount c from tax due t to get post-credit tax.",
 "Cases like investment credit, R&D super deduction.",
 "Ensure credit does not produce negative tax (take max(0, …)).",
 "Tax due 5000, credit 1000",
 "Post-credit tax = max(5000 - 1000, 0) = 4,000; if credit 6000, take 0 (no refund).",
 "Carryforward of excess credit",
 "Under some systems excess credit carries forward; this tool applies same-year credit (no negative tax).",
 "How does credit differ from deduction?",
 "Deduction lowers the tax base; credit cuts tax directly, with a more immediate effect.",
 "What if post-credit is negative?",
 "This tool takes max(0, tax - credit), no refund; carryforward follows tax law.",
]

TOD = [
 "Post-Discount Tax Calculator",
 "Levy tax on the net post-discount amount.",
 "/ Post-Discount Tax",
 "Post-Discount Tax",
 "📖 View the Post-Discount Tax Calculator Guide",
 "Discount and tax: discounted price = original x (1 - discount rate); saving = original - discounted; tax = discounted x rate; tax-inclusive total = discounted x (1 + rate); for post-promotion payable and invoiced tax.",
 "Discount Rate (%)",
 "200, 20% off, 13% -> discounted 160, tax 20.8.",
 "Deemed sales use fair value.",
 "📚 Deep Dive: Post-Discount Tax",
 "First compute the discounted price, then tax it.",
 "Tax-inclusive estimates for promotions and member discounts.",
 "Compare 'tax-then-discount' vs 'discount-then-tax'.",
 "Original 200, discount 20%, rate 13%",
 "Discounted = 200 x (1 - 0.20) = 160; tax = 160 x 0.13 = 20.8; tax-inclusive ≈ 180.8.",
 "Tax-then-discount comparison",
 "If tax first on 200 (26), then 20% off: (200+26)x0.8 = 180.8, same total but different tax base.",
 "Is the discount amount taxed?",
 "Usually taxed on the actual post-discount amount; this tool uses the 'discount-then-tax' model.",
 "Which saves more tax, discount or cashback?",
 "A direct price discount lowers the tax base more; cashback is often an extra charge, so the base may not drop.",
]

TGD = [
 "Compute macro tax burden from total tax and GDP",
 "Enter total tax and GDP to get the macro tax burden.",
 "Macro Tax Burden = Total Tax / GDP",
 "/ Macro Tax Burden Calculator",
 "Macro Tax Burden Calculator",
 "📖 View Guide: \"Compute macro tax burden from total tax and GDP\"",
 "Macro tax burden = Tax/GDP x 100%",
 "Total Tax (trillion)",
 "GDP (trillion)",
 "Macro tax burden = Tax/GDP.",
 "18T/100T -> 18%.",
 "📚 Deep Dive: Macro Tax Burden (tax concentration)",
 "Use total tax / GDP to measure a country/region's macro tax burden.",
 "Compare government extracting capacity across countries and years.",
 "Assess the impact of tax cuts on the macro tax burden.",
 "Tax 18, GDP 100",
 "Macro tax burden = 18 / 100 x 100% = 18%; if tax rises to 20, burden is 20%.",
 "International comparison",
 "18% is mid-level; Nordics often exceed 40%, low-tax regions below 15%; magnitude reference only.",
 "Is a high macro tax burden necessarily bad?",
 "Judge with public services and welfare returns; high burden often pairs with high welfare; efficiency and structure matter.",
 "Does the scope include social-security contributions?",
 "Broad macro burden often includes social-security contributions; narrow only taxes. Align the statistical scope before cross-comparison.",
]

write('specific-duty', build('specific-duty', SPD))
write('stamp-duty', build('stamp-duty', STD))
write('tax-credit', build('tax-credit', TCR))
write('tax-on-discount', build('tax-on-discount', TOD))
write('tax-to-gdp', build('tax-to-gdp', TGD))
