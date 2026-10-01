#!/usr/bin/env python3
# gen_tax_b2.py — tax b2 (5 slugs): corporate-income-tax/customs-duty/effective-tax-rate/excise-tax/foreign-tax-credit
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

CIT = [
 "Tax = Taxable Income x Rate",
 "Compute corporate income tax from taxable income and the applicable rate.",
 "Corporate Income Tax Calculator",
 "/ Corporate Income Tax",
 "Corporate Income Tax",
 "📖 View Guide: \"Tax = Taxable Income x Rate\"",
 "= Taxable Income",
 "1M, 25% -> Tax 250K.",
 "Small low-profit enterprises enjoy preferential rates.",
 "📚 Deep Dive: Corporate Income Tax",
 "Corporate taxable income x applicable rate gives income tax payable.",
 "Compare after-tax profit across profit scales and preferential rates.",
 "Estimate the gap between the 15% high-tech preferential and statutory 25% rates.",
 "Profit 1M, rate 25%",
 "Corporate income tax = 1,000,000 x 0.25 = 250,000; after-tax profit = 750,000.",
 "Preferential rate 15%",
 "If eligible for the 15% high-tech rate, tax = 150,000, after-tax profit = 850,000, leaving 100K more than at 25%.",
 "Does taxable income equal accounting profit?",
 "Not necessarily; tax adjustments per tax law (e.g. entertainment expense caps, super deductions) often create differences.",
 "What preferential treatment applies to small businesses?",
 "Eligible small businesses usually enjoy lower effective burden or tiered relief; follow the current-year policy.",
]

CDU = [
 "Duty = Dutiable Value x Tariff Rate",
 "Compute import duty from the assessed dutiable value and tariff rate.",
 "Import Customs Duty Calculator",
 "/ Import Customs Duty",
 "Import Customs Duty",
 "📖 View Guide: \"Duty = Dutiable Value x Tariff Rate\"",
 "= Dutiable Value",
 "Dutiable Value",
 "Tariff Rate (%)",
 "50K, 10% -> Duty 5K.",
 "Dutiable value includes freight and insurance (CIF).",
 "📚 Deep Dive: Import Duty (Ad Valorem)",
 "Import dutiable value x tariff rate yields duty, then add",
 "VAT",
 "Compare landed duty-paid cost under different HS-code rates.",
 "Estimate cost savings from FTA preferential rates.",
 "Dutiable value 50K, tariff rate 10%",
 "Import duty = 50000 x 0.10 = 5,000; duty-paid cost = 50000 + 5000 = 55,000 (excl. import VAT).",
 "Rate reduced to 5%",
 "Duty drops to 2,500, duty-paid cost 52,500, saving 2,500 vs 10%.",
 "Does dutiable value include freight and insurance?",
 "Ad valorem import duty usually uses CIF (cost + insurance + freight) as the dutiable value, subject to customs assessment.",
 "How do duty and import VAT stack?",
 "Compute duty first; import VAT is generally levied on (dutiable value + duty) as the tax base.",
]

ETR = [
 "Effective Rate = Total Tax / Pre-tax Income",
 "Comprehensively measures the actual tax burden borne.",
 "Effective Tax Rate Calculator",
 "/ Effective Tax Rate",
 "Effective Tax Rate",
 "📖 View Guide: \"Effective Rate = Total Tax / Pre-tax Income\"",
 "= Total Tax",
 "Total Tax",
 "Pre-tax Income",
 "250K / 1M = 25%.",
 "Below the statutory rate indicates exemptions or reductions.",
 "📚 Deep Dive: Effective Tax Rate (Composite)",
 "Use total tax / pre-tax profit to measure true burden, net of preferences and deductions.",
 "Compare effective tax rate (ETR) across years and jurisdictions.",
 "Assess the impact of book-tax differences and relief on overall burden.",
 "Tax 250K, pre-tax profit 1M",
 "Effective rate = 250000 / 1000000 x 100% = 25%; after-tax income = 1,000,000 - 250,000 = 750,000.",
 "After enjoying preferences",
 "If tax falls to 150K via relief while pre-tax profit holds, ETR=15%, 10 points below the statutory 25%.",
 "Why does effective differ from statutory rate?",
 "Statutory rate is the nominal bracket; effective rate is usually lower due to preferences, deductions, and loss carryforwards.",
 "Is a lower ETR always better?",
 "Not necessarily; an overly low ETR may stem from one-off relief or temporary differences, judged on sustainability.",
]

EXT = [
 "Compute excise tax from factory price, quantity and rate",
 "Enter factory unit price, quantity and excise rate to get the excise tax.",
 "T = Factory Price x Quantity x Rate",
 "/ Excise Tax (Ad Valorem) Calculator",
 "Excise Tax (Ad Valorem) Calculator",
 "📖 View Guide: \"Compute excise tax from factory price, quantity and rate\"",
 "Ad valorem excise = base price x quantity x rate. 10x100x20% -> 200.",
 "Factory Unit Price (CNY)",
 "Quantity (units)",
 "Excise Rate",
 "Ad valorem excise = base price x quantity x rate.",
 "10x100x20% -> 200.",
 "📚 Deep Dive: Excise Tax (Ad Valorem x Quantity)",
 "A composite ad-valorem-and-quantity excise levied on unit price x quantity x proportional rate.",
 "Model tobacco, alcohol and refined oil under per-unit and percentage bases.",
 "Compare total excise across sales volumes.",
 "Unit price 10, quantity 100, rate 20%",
 "Excise T = 10 x 100 x 0.20 = 200; doubling sales to 200 units gives 400.",
 "Impact of price increase on tax",
 "If unit price rises from 10 to 15, tax = 15 x 100 x 0.20 = 300; with price and volume up, burden grows faster.",
 "Is excise tax included in or added to the price?",
 "China's excise is included in the price, borne by consumers but paid at production/import stage.",
 "How do ad valorem and specific bases coexist?",
 "Some items use composite levy (specific quota + ad valorem rate); this tool illustrates the simplified ad-valorem x quantity model.",
]

FTC = [
 "Compute creditable amount from foreign tax paid and credit limit",
 "Enter foreign tax paid and the credit limit to get the creditable amount.",
 "Credit = min(Foreign Tax Paid, Credit Limit)",
 "/ Foreign Tax Credit Limit Calculator",
 "Foreign Tax Credit Limit Calculator",
 "📖 View Guide: \"Compute creditable amount from foreign tax paid and credit limit\"",
 "Creditable = min(Foreign Paid, Credit Limit)",
 "Foreign Tax Paid (CNY)",
 "Credit Limit (CNY)",
 "Credit does not exceed the limit (per-country / overall).",
 "min(2000,1500) -> 1,500.",
 "📚 Deep Dive: Foreign Tax Credit",
 "Resident firms credit foreign tax paid within the domestic limit, avoiding double taxation.",
 "Given foreign paid ft and credit limit lim, compute the creditable amount.",
 "Excess over the limit carries forward to later years.",
 "Foreign paid 2000, limit 1500",
 "Creditable = min(2000, 1500) = 1,500; the excess 500 carries forward to later years.",
 "Within the limit",
 "If foreign paid 1200 and limit 1500, the full 1200 is creditable with no carryforward.",
 "How is the credit limit determined?",
 "Usually the per-country / overall limit is the share of worldwide income times tax on foreign income under domestic law.",
 "What about the excess over the limit?",
 "The excess generally carries forward within a set period (e.g. 5 years) for later-year credit.",
]

write('corporate-income-tax', build('corporate-income-tax', CIT))
write('customs-duty', build('customs-duty', CDU))
write('effective-tax-rate', build('effective-tax-rate', ETR))
write('excise-tax', build('excise-tax', EXT))
write('foreign-tax-credit', build('foreign-tax-credit', FTC))
