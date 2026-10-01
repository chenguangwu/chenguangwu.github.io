#!/usr/bin/env python3
# gen_tax_b6.py — tax b6 (4 slugs): vat-from-exclusive/vat-inclusive-to-exclusive/vat-output/withholding-tax
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

VFE = [
 "Tax = Exclusive x Rate",
 "Compute VAT amount and inclusive price directly from exclusive sales.",
 "VAT from Exclusive Calculator",
 "/ VAT from Exclusive Price",
 "VAT from Exclusive Price",
 "📖 View Guide: \"Tax = Exclusive x Rate\"",
 "= Exclusive",
 "Exclusive 100, 13% -> tax 13, inclusive 113.",
 "Inclusive = Exclusive x (1+rate).",
 "📚 Deep Dive: VAT (Exclusive -> Inclusive)",
 "Given exclusive sales and rate, compute output tax and inclusive total.",
 "Sum price and tax for quotes and invoicing.",
 "Compare the inclusive-price difference between 13% and 9% rates.",
 "Exclusive 100, rate 13%",
 "VAT",
 "Tax = 100 x 0.13 = 13; inclusive = 100 + 13 = 113.",
 "Rate 9%",
 "Tax 9, inclusive 109, 4 less tax than at 13%.",
 "How to interpret the exclusive price?",
 "It is the VAT base, excluding this stage's VAT; inclusive = exclusive x (1+rate).",
 "Can input tax be credited?",
 "A general taxpayer's output tax can offset input tax; this tool only computes a single output, no credit.",
]

VIE = [
 "Exclusive = Inclusive / (1 + Rate)",
 "Split a tax-inclusive amount into exclusive sales and tax by VAT rate.",
 "Inclusive to Exclusive Calculator",
 "/ Inclusive to Exclusive Price (VAT)",
 "Inclusive to Exclusive Price (VAT)",
 "📖 View Guide: \"Exclusive = Inclusive / (1 + Rate)\"",
 "= Inclusive",
 "Inclusive 113, 13% -> exclusive 100, tax 13.",
 "Tax = Inclusive - Exclusive.",
 "📚 Deep Dive: VAT (Inclusive -> Exclusive)",
 "Back-solve exclusive amount and",
 "VAT",
 "amount from a known inclusive amount.",
 "Separate price and tax for purchasing and reimbursement entries.",
 "Confirm how much of the inclusive price is creditable tax.",
 "Inclusive 113, rate 13%",
 "Exclusive = 113 / (1 + 0.13) = 100; VAT = 113 - 100 = 13.",
 "Rate 9%",
 "At inclusive 109, exclusive = 109/1.09 = 100, tax 9.",
 "Why inclusive / (1+rate)?",
 "Because inclusive = exclusive x (1+rate), reverse requires dividing by (1+rate).",
 "Which part can a general taxpayer credit?",
 "The VAT stated on a special invoice (the tax computed here, when compliant) is creditable.",
]

VOP = [
 "Compute output VAT from sales and VAT rate",
 "Enter sales and VAT rate to get the output tax.",
 "T = Sales x Rate",
 "/ VAT Output Tax Calculator",
 "VAT Output Tax Calculator",
 "📖 View Guide: \"Compute output VAT from sales and VAT rate\"",
 "Output tax = sales x rate",
 "Sales (CNY)",
 "VAT Rate",
 "Output tax = exclusive sales x rate.",
 "10K x 13% -> 1,300.",
 "📚 Deep Dive: VAT Output Tax",
 "Compute current-period output tax as sales x rate.",
 "Filing estimates for general taxpayers.",
 "Compare output scale across sales tiers.",
 "Sales 10K, rate 13%",
 "Output tax T = 10000 x 0.13 = 1,300; sales 100K gives 13,000.",
 "Mixed rates",
 "If part is at 9%, account separately; this is a single-rate output example.",
 "Is output tax the same as tax payable?",
 "No; tax payable = output - input (with carryforward); this tool only computes output.",
 "Does it apply to small-scale taxpayers?",
 "Small-scale taxpayers usually use a levy rate (e.g. 3%) with simple calculation and no input credit; the model differs.",
 "How to use Compute output VAT from sales and VAT rate",
 "What does Compute output VAT from sales and VAT rate do?",
 "VAT Output Tax Calculator: enter sales and VAT rate; compute output tax as sales x rate, for general-taxpayer filing.",
 "How do I use Compute output VAT from sales and VAT rate?",
 "Which scenarios suit Compute output VAT from sales and VAT rate?",
 "VAT output = exclusive sales x applicable rate; inclusive = exclusive x (1+rate). The result is the output tax to accrue on that sale.",
 "Rate brackets",
 "Common China rates: 13% (general goods), 9% (agriculture/transport), 6% (services); small-scale levy mostly 3%. Follow the latest tax law.",
 "Output tax offsets input tax; actual payable = output - input. This tool estimates by input rate; for filing follow invoices and policy.",
]

WHT = [
 "Tax = Payment x Withholding Rate",
 "Source withholding on income earned by non-resident enterprises.",
 "Withholding Income Tax Calculator",
 "/ Withholding Income Tax",
 "Withholding Income Tax",
 "📖 View Guide: \"Tax = Payment x Withholding Rate\"",
 "= Payment",
 "Payment",
 "Withholding Rate (%)",
 "Payment 100K, 10% -> withholding 10K.",
 "Tax treaties can lower the rate.",
 "📚 Deep Dive: Withholding Income Tax",
 "Withhold tax as payment x rate on non-resident entities/individuals.",
 "Cross-border payments of dividends, interest, royalties.",
 "Compute the actual net payment and withheld amount.",
 "Payment 100K, withholding rate 10%",
 "Withholding tax = 100000 x 0.10 = 10,000; net payment = 100000 x (1 - 0.10) = 90,000.",
 "Treaty preferential rate 5%",
 "If a treaty lowers it to 5%, tax 5000, net 95000, saving 5000.",
 "Is withholding tax final?",
 "Often a final source tax for non-residents, but a treaty can grant a lower rate.",
 "How is the net payment computed?",
 "Net = payment x (1 - rate); the withholding agent deducts tax before paying.",
]

write('vat-from-exclusive', build('vat-from-exclusive', VFE))
write('vat-inclusive-to-exclusive', build('vat-inclusive-to-exclusive', VIE))
write('vat-output', build('vat-output', VOP))
write('withholding-tax', build('withholding-tax', WHT))
