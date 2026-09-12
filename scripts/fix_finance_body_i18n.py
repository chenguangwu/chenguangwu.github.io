#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""finance 分类英文态数据源根治：同步三端 + 补缺失条目 + 清孤儿键。

背景（与 general 同坑，§6「英文态数据源三处」）：
  页面可见英文（p / desc-en meta / ed）只是表象；`?lang=en-US` 与 industry JSON 的 ed
  还取决于三个数据源，只改页面会导致英文态仍是占位串 / 工具代号：
    ① i18n/tools/finance-body.json   -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
    ② i18n/tools/finance.json en-US  -> industry JSON 的 ed 最高优先级源（tool_desc_source.en_desc）
    ③ i18n/tools/_en_override.json   -> 运行时 en（h2/h1）与 ed

用法：
  python3 scripts/fix_finance_body_i18n.py --dry-run
  python3 scripts/fix_finance_body_i18n.py --apply
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'finance')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'finance-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'finance.json')

PH = 'is available directly in your browser'
OLD_PH = 'supports a focused'

# 说明：NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
# 每条 INTRO 依据页面 zh-CN intro 的用途说明撰写，避免 "free online tool" 类套话。
NAME = {
    'aadhaar-validator': 'India Aadhaar Number Validator',
    'aba-validator': 'ABA Routing Number Validator',
    'abn-validator': 'Australian ABN Validator',
    'amount-in-words': 'Amount to Words Converter',
    'analysis-5': 'Liquidity & Solvency Ratio Analysis',
    'analysis-cost-1': 'Cost Accounting & Allocation Model',
    'analysis-risk': 'Financial Risk, Leverage & Sensitivity Analysis',
    'assessor-manager': 'Credit Assessment & Line Manager',
    'bic-lookup': 'BIC / SWIFT Code Lookup',
    'bic-validator': 'BIC / SWIFT Code Validator',
    'bond-yield-calculator': 'Bond Yield Calculator',
    'break-even-calculator': 'Break-Even Analysis Calculator',
    'calc-2': 'IRR Calculator',
    'calc-3': 'NPV Calculator',
    'calc-4': 'Loan Monthly Payment Calculator',
    'calc-5': 'ROI Calculator',
    'car-loan-calculator': 'Car Loan Calculator',
    'cnpj-validator': 'Brazil CNPJ Validator',
    'compound-interest': 'Compound Interest Calculator',
    'cpf-validator': 'Brazil CPF Validator',
    'credit-card-bin': 'Credit Card BIN Lookup',
    'credit-card-grace-period': 'Credit Card Grace Period Calculator',
    'credit-card-interest': 'Credit Card Interest Calculator',
    'credit-card-luhn': 'Credit Card Luhn Checker',
    'credit-card-type': 'Credit Card Type Detector',
    'credit-card-validator': 'Credit Card Number Validator',
    'curp-validator': 'Mexico CURP Validator',
    'currency-converter': 'Currency Converter',
    'currency-lookup': 'Currency Code Lookup',
    'currency-symbol': 'Currency Symbol Reference',
    'dca-calculator': 'Dollar-Cost Averaging (DCA) Calculator',
    'dea-validator': 'US DEA Number Validator',
    'depreciation-calculator': 'Depreciation Calculator',
    'discount-calculator': 'Discount Calculator',
    'dni-validator': 'Spain DNI Validator',
    'dns-record-info': 'DNS Record Type Reference',
    'driver-license-validator': 'Driver License Number Validator',
    'ein-validator': 'US EIN Validator',
    'esn-validator': 'ESN Number Validator',
    'futures-pnl-calculator': 'Futures P&L Calculator',
    'generator-report-1': 'Financial Statements Generator',
    'gold-price-calculator': 'Gold Weight & Price Converter',
    'gst-validator': 'India GST Number Validator',
    'gstin-validator': 'India GSTIN Validator',
    'iban-validator': 'IBAN Validator',
    'iccid-validator': 'ICCID (SIM Card) Validator',
    'ifsc-validator': 'India IFSC Code Validator',
    'imei-validator': 'IMEI Number Validator',
    'imsi-validator': 'IMSI Validator',
    'inflation-calculator': 'Inflation Calculator',
    'installment-real-rate': 'Credit Card Installment Real Rate Calculator',
    'insurance-calculator': 'Life Insurance Needs Calculator',
    'investment-calculator': 'Investment Return Calculator',
    'invoice-generator': 'Invoice Amount Splitter',
    'ird-validator': 'New Zealand IRD Number Validator',
    'irr-calculator': 'IRR Calculator',
    'isbn-validator': 'ISBN Validator & Converter',
    'lease-payment-calculator': 'Lease Payment Calculator',
    'license-key-validator': 'License Key Validator',
    'loan-amortization': 'Loan Amortization Calculator',
    'loan-comparison': 'Loan Plan Comparator',
    'lottery-odds-calculator': 'Lottery Odds Calculator',
    'meid-validator': 'MEID Number Validator',
    'mirror-text': 'Mirror Text Generator',
    'mortgage-calculator': 'Mortgage Calculator',
    'mortgage-prepayment': 'Mortgage Prepayment Calculator',
    'msisdn-validator': 'MSISDN (Mobile Number) Validator',
    'mutual-fund-calculator': 'Mutual Fund SIP Calculator',
    'nie-validator': 'Spain NIE Validator',
    'npi-validator': 'US NPI Validator',
    'npv-calculator': 'NPV Calculator',
    'nric-validator': 'Singapore NRIC Validator',
    'number-to-words-chinese': 'Number to Chinese Words',
    'number-to-words': 'Number to English Words',
    'option-profit-calculator': 'Option Profit Calculator',
    'pan-validator': 'India PAN Validator',
    'password-generator-advanced': 'Advanced Password Generator',
    'password': 'Finance Password Generator',
    'payroll-calculator': 'Payroll & Income Tax Calculator',
    'points-redemption-value': 'Points Redemption Value Calculator',
    'position-size-calculator': 'Position Size Calculator',
    'postal-code-validator': 'International Postal Code Validator',
    'profit-margin-calculator': 'Profit Margin Calculator',
    'rental-yield-calculator': 'Rental Yield Calculator',
    'report-1': 'Consolidated Statements & Minority Interest',
    'retirement-calculator': 'Retirement Savings Calculator',
    'roi-calculator': 'ROI Calculator',
    'routing-number-validator': 'US Routing Number Validator',
    'salary-after-tax': 'Salary After Tax Calculator',
    'salary-calculator': 'Salary & Income Tax Calculator',
    'simple-interest': 'Simple Interest Calculator',
    'sin-validator': 'Canada SIN Validator',
    'sort-code-validator-validator': 'UK Sort Code Validator',
    'stock-profit-calculator': 'Stock Profit Calculator',
    'swift-bic-validator': 'SWIFT / BIC Code Validator',
    'tax-bracket': 'Tax Bracket Reference',
    'tax-calculator': 'Personal Income Tax Calculator',
    'text-reverse-words': 'Word Order Reverser',
    'tfn-validator': 'Australia TFN Validator',
    'tin-validator': 'US TIN Validator',
    'uan-validator': 'India UAN Validator',
    'vat-calculator': 'VAT Calculator',
    'vcard-qr': 'vCard QR Code Generator',
    'vin-validator': 'VIN Validator',
    'voter-id-validator': 'India Voter ID Validator',
    'wifi-password-show': 'WiFi Password Viewer',
    'word-counter': 'Word Counter',
    'word-frequency': 'Word Frequency Counter',
    'word-scramble': 'Word Scramble',
    'word-search': 'Word Search Puzzle',
    'word-wrap': 'Text Word Wrap',
    'zip-code-validator': 'US ZIP Code Validator',
}

INTRO = {
    'aadhaar-validator': 'Validate a 12-digit Aadhaar number with the Verhoeff checksum. Format check only, not a real identity lookup.',
    'aba-validator': 'Validate a 9-digit US ABA routing number with the mod-3 checksum before bank transfers or cheque entry.',
    'abn-validator': 'Validate an 11-digit Australian Business Number with the official weighted checksum. Format check only.',
    'amount-in-words': 'Convert numeric amounts into English words for cheques, invoices and legal documents.',
    'analysis-5': 'Turn current assets, inventory and liabilities into current, quick and debt ratios to gauge financial health.',
    'analysis-cost-1': 'Allocate overheads across cost objects and derive unit cost and cost structure for pricing decisions.',
    'analysis-risk': 'Compute financial leverage and sensitivity indicators from debt, interest and key variables for risk screening.',
    'assessor-manager': 'Score creditworthiness from debt ratio, liquidity and income, then suggest a lending limit and risk grade.',
    'bic-lookup': "Look up a bank's name and country by BIC/SWIFT code, or reverse-search codes by bank name for remittance forms.",
    'bic-validator': 'Check that an 8- or 11-character BIC/SWIFT code has valid length and structure for international transfers.',
    'bond-yield-calculator': 'From price, face value, coupon and holding period, compute yield to maturity, current yield and holding-period return.',
    'break-even-calculator': 'Work out break-even units, margin of safety and operating leverage from fixed cost, price and variable cost.',
    'calc-2': 'Compute the internal rate of return from a series of cash flows by solving for the discount rate that makes NPV zero.',
    'calc-3': 'Discount a series of cash flows to net present value; a positive NPV means the project is worth pursuing.',
    'calc-4': 'Compute the equal monthly payment and total interest from loan principal, annual rate and term.',
    'calc-5': 'Measure return on investment from gain and cost, with an annualised figure for comparing projects of different lengths.',
    'car-loan-calculator': 'Estimate monthly payment plus purchase tax, insurance and registration for the full cost of buying a car.',
    'cnpj-validator': 'Validate a 14-digit Brazilian company tax number with its two official check digits. Format check only.',
    'compound-interest': 'Project future value from principal, annual rate, compounding frequency and regular contributions, with a Rule of 72 estimate.',
    'cpf-validator': 'Validate an 11-digit Brazilian individual tax number with the mod-11 check digits. Format check only.',
    'credit-card-bin': 'Identify the issuing bank, card network and card type from the first six digits (BIN) of a card number.',
    'credit-card-grace-period': 'Enter statement and due dates to find the longest and shortest interest-free periods and the best day to spend.',
    'credit-card-interest': 'Compare interest and fees for full, minimum and instalment repayment of a card statement to pick the cheaper option.',
    'credit-card-luhn': 'Validate a card number with the Luhn mod-10 algorithm to catch typos or fabricated numbers before payment.',
    'credit-card-type': 'Detect the card network and tier (Visa, Mastercard, UnionPay and more) from the number prefix, entirely offline.',
    'credit-card-validator': 'Check a card number against the Luhn algorithm, the same mod-10 method used for IMEIs and other ID numbers.',
    'curp-validator': 'Validate an 18-character Mexican CURP code for length, character set and check digit. Format check only.',
    'currency-converter': 'Convert between 20+ major currencies using built-in reference rates, handy for travel or cross-border quotes.',
    'currency-lookup': 'Look up ISO 4217 currency codes in both directions and see the symbol and decimal places for financial documents.',
    'currency-symbol': 'Find the symbol, three-letter code and country of a currency by ISO code, country or region.',
    'dca-calculator': 'Simulate regular fixed-amount investing to see total contributions, final value and returns versus a lump sum.',
    'dea-validator': 'Validate a 9-digit DEA registration number for format and checksum in medical and compliance screening.',
    'depreciation-calculator': "Compare straight-line, double-declining, sum-of-years and units-of-production depreciation and print each period's charge.",
    'discount-calculator': 'Apply a discount rate to a list price to get the sale price and savings, with a reverse tax-inclusive mode.',
    'dni-validator': 'Validate a 9-character Spanish DNI with the mod-23 check letter. Format check only.',
    'dns-record-info': 'A static reference of common DNS record types and their purpose; use dig or nslookup for live lookups.',
    'driver-license-validator': 'Check a driver licence number against common format and check-digit rules and infer the issuing region.',
    'ein-validator': 'Validate a 9-digit US Employer Identification Number for structure and format in tax and business screening.',
    'esn-validator': 'Validate an 8-character hexadecimal ESN for CDMA device identity and inventory checks. Format check only.',
    'futures-pnl-calculator': 'Compute long or short futures profit and loss, margin used and fees from open/close prices, lots and leverage.',
    'generator-report-1': 'Generate sample balance sheet, income statement, cash-flow statement and notes from a template for demos and teaching.',
    'gold-price-calculator': 'Convert gold weight and purity to value across units and two currencies, with a scrap-price estimate.',
    'gst-validator': 'Validate a 15-character Indian GST number for structure and check digit. Format check only.',
    'gstin-validator': 'Validate a 15-character GSTIN including state code, entity part and check digit. Format check only.',
    'iban-validator': "Validate an IBAN's country code and check digits with the ISO 13616 mod-97 algorithm, with sample IBANs per country.",
    'iccid-validator': 'Validate a SIM card ICCID with the Luhn algorithm for device and IoT identity checks. Format only.',
    'ifsc-validator': 'Validate an 11-character Indian IFSC bank branch code for format and structure. Format check only.',
    'imei-validator': 'Validate a 14- or 15-digit IMEI with the Luhn algorithm for device identification and second-hand checks.',
    'imsi-validator': "Check an IMSI's prefix and length and read the MCC/MNC meaning for telecom data verification.",
    'inflation-calculator': "Project the future nominal price of today's money at a given inflation rate, or the amount needed to keep purchasing power.",
    'installment-real-rate': 'Turn a flat instalment fee rate into the true annualised interest rate using the IRR method, with a comparison verdict.',
    'insurance-calculator': 'Estimate life and critical-illness cover using income-multiple and needs methods for family protection planning.',
    'investment-calculator': 'Compute the cumulative return from cost and end value and annualise it to compare different investments.',
    'invoice-generator': 'Split tax-inclusive or net invoice amounts into net and tax parts, with rounding for multi-invoice allocation.',
    'ird-validator': 'Validate an 8- or 9-digit New Zealand IRD number with the official checksum. Format check only.',
    'irr-calculator': "Compute IRR, NPV and payback period from custom cash flows to judge a project's true return.",
    'isbn-validator': 'Validate ISBN-10 (mod-11) and ISBN-13 (mod-10) check digits and convert between the two formats.',
    'lease-payment-calculator': 'Compute the equal periodic lease payment and schedule from asset value, rate and term, showing the interest-first pattern.',
    'license-key-validator': "Check a software licence key's segments, length and check character against common format rules. Offline only.",
    'loan-amortization': 'Build a full period-by-period amortization schedule from principal, rate and term, with prepayment simulation and charts.',
    'loan-comparison': 'Compare two or more loan offers side by side on monthly payment, total interest and total cost.',
    'lottery-odds-calculator': 'Compute winning odds and total combinations for Double Color Ball, Super Lotto, 3D and more, or any custom draw.',
    'meid-validator': 'Validate a 14-character hexadecimal MEID for CDMA device identity and inventory checks. Format check only.',
    'mirror-text': 'Flip text left-to-right as copyable characters or a preview image for playful signatures, art and watermarks.',
    'mortgage-calculator': 'Compute monthly payment, total interest and repayment schedule under equal-instalment or equal-principal mortgages.',
    'mortgage-prepayment': 'Estimate the interest saved and the change in remaining payments after a lump-sum mortgage prepayment.',
    'msisdn-validator': 'Validate an international mobile number with country code, allowing digits, + and separators. Format check only.',
    'mutual-fund-calculator': 'Project SIP total investment, final value and real return, including subscription fees and dividend reinvestment.',
    'nie-validator': 'Validate a 9-character Spanish NIE with the mod-23 check letter for residency and tax forms. Format check only.',
    'npi-validator': 'Validate a 10-digit US National Provider Identifier for structure and checksum in healthcare screening.',
    'npv-calculator': 'Discount custom cash flows to net present value and also report IRR, profitability index and payback period, with charts and CSV.',
    'nric-validator': 'Validate a 9-character Singapore NRIC for prefix, check letter and format. Format check only.',
    'number-to-words-chinese': 'Convert integers, decimals and negatives into Chinese reading with correct zeros and units for invoices and finance.',
    'number-to-words': 'Spell out numbers in English words, for example 123 to one hundred twenty-three, for cheques and forms.',
    'option-profit-calculator': 'Compute expiry profit and break-even for call/put buyers and sellers from strike, premium and underlying price.',
    'pan-validator': 'Validate a 10-character Indian PAN for prefix, entity-type character and format. Format check only.',
    'password-generator-advanced': 'Generate strong passwords with custom length, character sets, exclusions and a passphrase mode, all offline.',
    'password': 'Generate strong random passwords with configurable length and character sets, created locally and never uploaded.',
    'payroll-calculator': 'Compute income tax, social insurance and take-home pay from gross salary and deductions, monthly or annual.',
    'points-redemption-value': 'Work out the cash value per 10,000 points from points needed and item value, and compare redemption channels.',
    'position-size-calculator': 'Size a trade from account equity, risk per trade and stop distance using Kelly, fixed-fraction or risk-budget methods.',
    'postal-code-validator': 'Validate postal codes against per-country rules such as US 5/9-digit and China 6-digit formats. Offline.',
    'profit-margin-calculator': 'Compute gross, net, operating and EBITDA margins, with reverse calculation and DuPont analysis.',
    'rental-yield-calculator': 'Compute gross and net rental yield and payback period from property price, rent and holding costs, comparing up to three properties.',
    'report-1': 'Work out consolidation, elimination entries and minority interest from parent/subsidiary equity and intercompany deals.',
    'retirement-calculator': 'Estimate the retirement nest egg you need using the 4% rule from current assets, annual savings and years to retire.',
    'roi-calculator': 'Compute simple and annualised ROI plus dollar-cost-averaging return, with plan comparison and a growth curve.',
    'routing-number-validator': 'Validate a 9-digit ABA routing number with the mod-3 checksum for transfers, cheques and ACH.',
    'salary-after-tax': 'Compute taxable income and take-home pay from gross salary, social insurance and special deductions under cumulative withholding.',
    'salary-calculator': 'Work out income tax, social insurance and net pay from monthly or annual salary, social insurance base and deductions.',
    'simple-interest': 'Compute simple interest and total amount from principal, annual rate and term with a clear breakdown.',
    'sin-validator': 'Validate a 9-digit Canadian Social Insurance Number with the mod-10 Luhn check. Format check only.',
    'sort-code-validator-validator': 'Validate a 6-digit UK sort code for length and digits before setting up local transfers.',
    'stock-profit-calculator': 'Compute trading profit from buy and sell prices and quantity, breaking out stamp duty, commission and transfer fees.',
    'swift-bic-validator': 'Validate an 8- or 11-character SWIFT/BIC code for length, country code and character set.',
    'tax-bracket': 'Look up the tax bracket and quick deduction for a taxable income across common tax tables. Reference only.',
    'tax-calculator': 'Compute taxable income and after-tax income from monthly or annual income and deductions under progressive rates.',
    'text-reverse-words': 'Reverse the order of words in an English sentence, optionally keeping punctuation in place.',
    'tfn-validator': 'Validate an 8- or 9-digit Australian Tax File Number with the official weighted checksum. Format check only.',
    'tin-validator': 'Validate a 9-digit US Taxpayer Identification Number for structure and format in tax and account screening.',
    'uan-validator': 'Validate a 12-digit Indian Universal Account Number for length and digits. Format check only.',
    'vat-calculator': 'Convert between VAT-inclusive and exclusive prices and split the tax out, with batch line-by-line calculation.',
    'vcard-qr': 'Build a scannable vCard QR code from name, phone, email and company details, generated locally.',
    'vin-validator': 'Validate a 17-character VIN and decode the model year and world manufacturer identifier.',
    'voter-id-validator': 'Validate a 10-character Indian voter ID (EPIC) for length and character format. Format check only.',
    'wifi-password-show': 'Parse pasted WiFi connection details locally to reveal a saved network password. Never uploaded.',
    'word-counter': 'Count words, characters and Chinese characters while excluding whitespace, for essay limits and proofreading.',
    'word-frequency': 'Tokenise text and rank word frequency, with stop-word filtering, for keyword extraction and text analysis.',
    'word-scramble': 'Shuffle word letters into a guessing puzzle with adjustable difficulty and word lists for spelling practice.',
    'word-search': 'Hide target words in a letter grid and hunt them down, with custom word lists and grid sizes.',
    'word-wrap': 'Wrap paragraphs at a chosen width for tidy report notes and document alignment.',
    'zip-code-validator': 'Validate US ZIP and ZIP+4 formats and hint at the state and region. Offline, no lookup.',
}

# 缺失 zh-CN 条目的工具（页面中文标题存在但 i18n 无条目）：slug -> (中文名, 中文简介)
ZH_FILL = {
    'amount-in-words': ('数字大写转换器', '输入阿拉伯数字，转换为英文单词大写，适用于支票、发票与法律文书填写。'),
    'credit-card-grace-period': ('信用卡免息期计算器', '输入信用卡账单日与还款日，计算最长/最短免息期，并找出最佳消费日期。'),
    'installment-real-rate': ('信用卡分期真实利率计算器', '输入分期本金、期数与每期手续费率，用 IRR 法还原真实年化利率，并给出对比结论。'),
    'points-redemption-value': ('积分兑换价值计算器', '输入积分数与兑换商品的现金价值，算出每万分价值，对比常见兑换渠道判断划算与否。'),
    'salary-after-tax': ('工资税后计算器', '输入应发工资、个人缴纳的五险一金与专项附加扣除，按现行个税累计预扣法计算应纳税额与到手工资。'),
    'loan-comparison': ('贷款方案对比器', '输入多组贷款方案的金额、利率与期限，横向对比月供、总利息与总成本，辅助选型。'),
    'mortgage-prepayment': ('提前还款计算器', '输入贷款余额、利率与提前还款金额，测算可节省的利息与剩余还款变化。'),
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov = load(OV)
    body = load(BODY)
    gis = load(GIS)

    chg_en = chg_ed = chg_body = chg_gis = added_body = added_gis = added_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'finance/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'finance'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'finance')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + finance-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + finance.json 新增条目:', slug)
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if slug in ZH_FILL:
            if not isinstance(g.get('zh-CN'), dict):
                zh_name, zh_intro = ZH_FILL[slug]
                g['zh-CN'] = {'h1': zh_name, 'title': zh_name, 'intro': zh_intro, 'desc': zh_name}
                added_zh += 1
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿键：body 中存在但全站无对应页面（与 general 的 random-10 同类）
    orphans = []
    all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
    for key in list(body.keys()):
        if key not in all_basenames:
            orphans.append(key)
    print('\n--- 汇总 ---')
    print('finance 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('finance-body 更新:', chg_body, ' 新增:', added_body)
    print('finance.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 补 zh-CN:', added_zh)
    print('finance-body 孤儿键:', orphans)

    if a.dry_run:
        for s in slugs[:3]:
            print('\n预览 %s:\n  name = %r\n  intro= %r' % (s, NAME[s], INTRO[s]))
        return 0

    json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(body, open(BODY, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(gis, open(GIS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('\n已写入：_en_override.json(indent=1) / finance-body.json(indent=2) / finance.json(indent=2)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
