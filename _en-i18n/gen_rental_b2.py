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
    write('cycle-11', build('cycle-11', [
        '⏱️ Utility (Meter Reading / Billing Cycle) Settlement',
        'Record electricity, water and gas meter readings, auto-calculate usage and cost, support tiered electricity pricing, and generate a settlement report.',
        'The tool that "records electricity, water and gas meter readings, auto-calculates usage and cost, supports tiered electricity pricing, and generates a settlement report" performs professional calculation and outputs results based on input parameters.',
        '📖 View the User Guide for Utility (Meter Reading / Billing Cycle) Settlement',
        '⚡ Electricity fee',
        '💧 Water fee',
        '🔥 Gas fee',
        'Reading records',
        'Add reading',
        'Calculate settlement',
        'Settlement report',
        'Historical settlement records',
        '📚 Deep Dive: Utility Meter Reading and Tiered Settlement',
        'When moving out or switching tenants, enter the previous and current meter readings; the tool auto-computes usage and cost and generates a printable settlement slip.',
        'Cost sharing for co-tenants: after computing the total cost from meter readings, split it by number of occupants per room or by area ratio.',
        'When applying tiered electricity pricing, accumulate by tier unit price and verify consistency with the utility bill.',
        'Two billing methods for 330 kWh usage',
        'Previous reading 12,450, current 12,780 → usage 330 kWh. Flat rate 0.60 CNY/kWh: 330 × 0.60 = 198.00 CNY. Under tiered pricing (tier 1: 0–200 kWh at 0.55 CNY, excess at 0.65 CNY): 200×0.55 + 130×0.65 = 110.00 + 84.50 = 194.50 CNY. The water and gas meters work the same: subtract the previous reading from the current to get usage, then accumulate by the corresponding unit price or tiers.',
        'How is tiered electricity pricing accumulated?',
        'Apply each tier unit price from low to high usage and sum them, rather than pricing all at the highest tier. The tool accumulates tier by tier per the upper limits and prices you enter; please fill in according to the tiers published by your local utility.',
        'What if a reading is entered wrong?',
        'After modifying any reading, the result recalculates in real time. It is recommended to photograph the meter face when reading it for record, to avoid disputes at move-out settlement.',
        'Electricity (kWh), water (ton/m³), gas (m³); readings must be recorded in time order',
        'Tiered electricity pricing is billed by monthly usage tiers; each tier upper limit and unit price can be customized',
        'Water and gas fees support a single unit price or two-tier pricing',
        'At settlement, take the difference between two adjacent readings to compute usage',
        'About the Utility (Meter Reading / Billing Cycle) Settlement',
        'A tool for recording utility meter readings and settling fees. Record meter readings, auto-calculate usage and cost, support tiered electricity pricing, and generate a detailed settlement report.',
        'Electricity / water / gas three-meter management',
        'Tiered electricity pricing by tier',
        'Auto calculation of usage and cost',
        'Multi-cycle settlement reports',
        'Historical settlement record saving',
        'Rental property utility settlement',
        'Cost sharing among co-tenants',
        'Property meter-reading and fee management',
        'Household utility cost tracking',
    ]))
    write('generator-32', build('generator-32', [
        '⚖️ Lease (Contract / Clause) Generator',
        'Contract / clauses',
        '📖 View the User Guide for Lease (Contract / Clause) Generator',
        'The lease contract is assembled by elements: lessor and lessee information + leased property description (address, area, ancillary facilities) + lease term and start/end dates + rent and payment method (monthly, one-month deposit with three months prepaid) + deposit (usually 1 to 3 months rent) + maintenance responsibility division + breach and termination clauses + sublease terms + dispute resolution + signature block; clauses are numbered "Article X", and blanks are marked with placeholders for filling.',
        '📚 Deep Dive: Lease Contract Clause Template Generation',
        'Before drafting a lease, list a clause checklist: rent and payment method, deposit, maintenance responsibility, sublease and move-out conditions, etc.',
        'Before negotiating with the tenant, review what standard clauses usually cover, to avoid missing key agreements.',
        'When generating contracts in bulk for multiple properties, first align the wording with a template then fill each one, reducing inconsistency.',
        'What does the generated result look like',
        'After setting the generation count, the tool produces several clause points by property type and term combination (e.g. "monthly rent ____ CNY, payable before the ____ day each month", "deposit ____ months rent, refunded within ____ days after move-out inspection", "the property main structure and natural wear are maintained by Party A, damage caused by Party B improper use is borne by Party B"); the underlined parts are placeholders to fill. Fill the placeholders with actual numbers and dates to use as a draft.',
        'Can the generated text be used directly as a contract?',
        'No. It is clause points and a fill-in template, for drafting and gap-checking, not legal advice. For a formal contract, use the model text of the local housing department; for significant value, consult a lawyer.',
        'Why is the generated content not exactly the same each time?',
        'The tool randomly samples from common clause combinations; the same parameters generate different entries each time. It is recommended to generate several times and pick the needed clauses to assemble a complete list.',
        'About the Lease (Contract / Clause) Generator',
        'Lease (Contract / Clause) Generator. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))
    write('index', build('index', [
        '🔑 Rental Management Tools',
        'Rental management',
        'Rental management tools',
        'Generate lease contract templates by property and term, with preset placeholders for rent, deposit and responsibility clauses, for drafting reference; the front-end generation is not legal advice.',
        'Rental yield calculator',
        'The rental yield calculator is a free online rental management tool that delivers results in real time from input parameters; it runs entirely in the browser, uploads no data and needs no registration, ready to use by opening the browser. Entirely front-end, no data upload, no regist...',
        'Agency (commission / service fee) calculator',
        'Enter the transaction amount, commission rate, service fee and sharing method to quickly compute the agency fee borne by each side of the buyer/seller or landlord/tenant.',
        'Recommend broadband bandwidth and plans by number of users, usage and unit type, with installation and equipment tips, for purchase reference; the front-end suggestion is not an operator quote.',
        'Enter the tenant monthly income, job stability, credit and past rental records; the tool weighted-assesses the credit risk tier (Excellent/Medium/Poor) and gives deposit and screening suggestions, helping landlords quickly filter reliable tenants before renting.',
        'Enter the rents of multiple comparable listings and correction factors such as floor, orientation, decoration and amenities, to auto-compute a weighted reference rent, rent range and annual growth suggestion.',
        'Utility (meter reading / billing cycle) settlement',
        'Record electricity, water and gas meter readings, auto-calculate usage and cost, support tiered electricity pricing, and generate a settlement report.',
        'Manage lease-expiry reminders for rental properties, with color-graded warnings by remaining days, track renewal status and provide landlord action suggestions.',
        'About the Rental Management Tools',
        'The rental management tools collection includes 8 free online tools, covering common calculation, conversion and lookup needs in rental management scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find handy tools here that work instantly. All tools run entirely in the browser, upload no data to servers, and protect your privacy.',
        'The rental management tools featured on this page include (representative tools):',
        'These tools help you quickly complete common rental-management tasks without memorizing complex formulas or manual conversion; just enter to get results.',
        'Do the rental management tools need download or registration?',
        'No. All rental management tools on this page are purely front-end online tools; open the web page to use them directly, with no software installation, no account registration, and no data upload.',
        'Are the rental management tools accurate? Is the data safe?',
        'The tools compute locally in your browser based on public math formulas and general industry standards, with results available instantly. All calculations are done on your device locally, and data is never uploaded to servers, ensuring privacy and security.',
    ]))

if __name__ == '__main__':
    main()
