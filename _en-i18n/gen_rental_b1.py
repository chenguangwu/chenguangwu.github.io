#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'rental')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'rental')
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
    out = {'slug': slug, 'industry': 'rental', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('assessor-24', build('assessor-24', [
        '📋 Tenant (Credit / Background) Assessment',
        'Enter the tenant income, credit, employment and other information to comprehensively assess the tenant credit risk level',
        '📖 View the User Guide for Tenant (Credit / Background) Assessment',
        'The tenant credit score is weighted by dimensions: income-to-rent ratio (rent ÷ monthly income: ≤25% scores 100, 25%–33% scores 80, 33%–50% scores 50, >50% scores 20) + job stability (years employed, capped at 100) + linearly converted credit score + age and guarantor bonus; the total is converted to Excellent (≥80), Medium (60–79), Poor (<60); for the Poor tier, raise the deposit or require a guarantor.',
        'Employment tenure (years)',
        'Credit score (350–950)',
        'Tenant age',
        'Has guarantor',
        '📚 Deep Dive: Tenant Credit and Background Scoring',
        'Before renting, score tenants by rent-to-income ratio, employment tenure, credit score, age and guarantor status to quickly screen out high-risk applicants.',
        'Compare multiple applicants horizontally on the composite score, and weigh against the suggested deposit tier.',
        'When co-renting or leasing to a company, trade a lower risk tier for a shorter rent-free period or a higher deposit.',
        'Score for monthly rent 4,000 / income 12,000',
        'Monthly income 12,000, monthly rent 4,000 (rent-to-income ratio 33.3%, falls in the >33% tier → income score 50); 5 years employed → 100; credit score 700 → (700−350)/6 = 58; age 32 (25–55 range) → 100; no guarantor → 50. Composite = 50×0.35 + 100×0.20 + 58×0.25 + 100×0.10 + 50×0.10 = 67.1 → Tier B (medium-low risk), suggested deposit 2 months. If monthly rent drops to 3,000 (ratio 25.0% → income score 100), composite rises to 84.6 → Tier A, deposit 1 month.',
        'What are the weights of each factor?',
        'Rent-to-income ratio 35%, job stability 20%, credit score 25%, age 10%, guarantor 10%. The rent-to-income ratio has the highest weight because it is the single strongest predictor of default.',
        'How do score tiers map to the deposit?',
        '≥80 Tier A suggests 1 month deposit, 60–79 Tier B 2 months, 45–59 Tier C 3 months, <45 Tier D suggests rejecting or requiring a guarantor.',
        'Rent-to-income ratio is the core metric; keep it ≤33% (i.e. income ≥ 3× rent)',
        'Reference the central bank credit report or a third-party credit score for the credit score',
        'Longer employment tenure means more stable income',
        'Having a guarantor lowers default risk',
        'Recommend verifying the original ID, employment certificate and credit report',
        'About the Tenant (Credit / Background) Assessment',
        'A tenant credit assessment tool that comprehensively evaluates the tenant risk tier from five dimensions: income ratio, job stability, credit score, age and guarantor.',
        'A–D four-tier risk rating',
        'Auto calculation of rent-to-income ratio',
        'Deposit suggestions',
        'Landlord tenant selection',
        'Agent tenant screening',
        'Long-rent apartment risk control',
        'Rental credit assessment',
    ]))
    write('calc-commission-1', build('calc-commission-1', [
        '🧮 Agency (Commission / Service Fee) Calculator',
        'Enter the transaction amount, commission rate, service fee and sharing method to quickly compute the agency fee borne by each side of the buyer/seller or landlord/tenant.',
        'Core formula (by input variables): max(0,min(1,buyerPct))',
        '📖 View the User Guide for Agency (Commission / Service Fee) Calculator',
        'Transaction amount (10,000 CNY)',
        'Commission rate (%)',
        'Fixed service fee (CNY)',
        'Transaction type',
        'Home purchase and sale',
        'Home rental',
        'Sharing method',
        'Buyer / tenant pays all',
        'Seller / landlord pays all',
        'Split equally',
        'Buyer / tenant share ratio (%)',
        '💡 Agency fee = transaction amount × commission rate + fixed service fee. For rentals, common is 50%–100% of monthly rent; for sales, common is 1%–3% of the transaction price.',
        'For home rental, enter the monthly rent in "transaction amount"; the result is that month commission',
        'Actual commission rates vary by city, agency brand and housing scarcity',
        'Fixed service fees apply to value-added items such as loan agency and title-transfer agency',
        'Results are for reference only; the actual contract terms prevail',
        '📚 Deep Dive: Agency Commission and Sharing Calculation',
        'Before closing, calculate the total of commission + fixed service fee and the blended rate, to avoid discovering the cost exceeded expectations only after signing.',
        'Split the fee between buyer and seller (or tenant and landlord) by the agreed ratio, clarifying each party payable amount.',
        'Compare quotes from different agencies: convert quotes with different rates into actual amounts and blended rates before comparing.',
        '3,000,000 CNY',
        "'s transaction commission",
        'Transaction amount 3,000,000 CNY, commission rate 2%, fixed service fee 2,000 CNY: commission = 3,000,000 × 2% = 60,000 CNY, total fee 62,000 CNY, blended rate = 62,000 ÷ 3,000,000 = 2.07%. If the sale is split equally, each side pays 31,000 CNY; if the buyer bears 100%, the buyer pays 62,000 CNY and the seller 0 CNY.',
        'Why is the blended rate different from the commission rate?',
        'Blended rate = (commission + fixed service fee) ÷ transaction amount, including the fixed service fee that does not scale with the transaction amount. The smaller the transaction amount, the more the fixed service fee lifts the blended rate.',
        'How to fill the custom sharing ratio?',
        'After selecting custom, enter the "buyer / tenant share ratio"; the remainder automatically goes to the other party. Enter 0 to assign all to the other party, 100 to assign all to yourself.',
        'About the Agency (Commission / Service Fee) Calculator',
        'A home purchase/sale and rental agency fee calculator that supports transaction amount, commission rate, fixed service fee and multiple sharing methods, quickly producing each party payable fee and blended rate.',
        'Purchase/sale and rental transaction types',
        'Multiple fee sharing methods',
        'Commission and service fee breakdown',
        'Blended rate comparison',
        'Home buying/renting budget planning',
        'Agency quote verification',
        'Rental commission comparison',
    ]))

if __name__ == '__main__':
    main()
