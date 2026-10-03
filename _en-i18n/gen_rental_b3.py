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
    write('recommender-5', build('recommender-5', [
        '🌐 Network (Broadband / Installation) Recommendation',
        'Broadband / installation',
        '📖 View the User Guide for Network (Broadband / Installation) Recommendation',
        'Broadband bandwidth is recommended by number of users and usage: 1–2 people daily surfing 50–100 Mbps, 3–4 people multi-device and HD video 200–300 Mbps, 4+ people or 4K and gaming 500–1000 Mbps; actual usable bandwidth ≈ nominal bandwidth × (1 − line loss 10%–20%) ÷ simultaneously online devices; equipment essentials include gigabit optical modem, WiFi 6 dual-band router (2.4G and 5G) and Cat-5e or better cable; before installation verify whether the community is already covered.',
        '📚 Deep Dive: Broadband Bandwidth and Installation Quick Reference',
        'Before renting or moving, quickly list the bandwidth tiers and access methods for several typical network scenarios, as a purchase reference.',
        'Before talking to the operator, review common installation notes (modem deposit, contract period, early-termination penalty, peak-hour stability).',
        'Explain to co-tenants or family why a certain tier is needed, communicating by scenario rather than parameters.',
        'What does the generated result look like',
        'After setting the generation count, the tool outputs line by line "usage scenario — recommended bandwidth + access type" with one installation tip, e.g. "home remote work — recommended 500M fiber to the home (FTTH) / installation tip: watch the contract period and early-termination penalty". Scenarios, bandwidth tiers, access types and tips are all sampled from common combinations, so the same setting generates different entries each time.',
        'Why does it not ask me to enter the number of users and unit type?',
        'This tool is a quick-reference list; it only samples from common scenario combinations by the count you set, and does not compute bandwidth by number of users/area. When you need a precise estimate by device count, accumulate yourself per "about 25 Mbps per 4K stream, about 4 Mbps per video conference".',
        'Can the recommendation be used as an operator quote?',
        'No. It contains no real-time tariff or coverage information, and is for purchase comparison only; for actual plan prices, installation fees and coverage, please refer to your local operator.',
        'About the Network (Broadband / Installation) Recommendation',
        'Network (Broadband / Installation) Recommendation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))
    write('reminder-4', build('reminder-4', [
        '⏰ Lease Term (Start/End/Renewal) Reminder',
        'Manage lease-expiry reminders for rental properties, with color-graded warnings by remaining days, track renewal status and provide landlord action suggestions.',
        '📖 View the User Guide for Lease Term (Start/End/Renewal) Reminder',
        'Add lease',
        'Property address',
        'Tenant name',
        'Lease start',
        'Lease end',
        'Contact phone',
        'Expiry warning overview',
        '📚 Deep Dive: Lease Expiry Reminder and Renewal Tracking',
        'When managing multiple rentals, register each lease start/end and tenant contact; auto-sort and warn by remaining days.',
        'Start following up on renewal intent 30 days before expiry, to avoid vacancy-period losses.',
        'At move-out settlement, combine the monthly rent with remaining days to estimate the early-termination penalty or refundable rent.',
        'Graded warning by remaining days',
        'Days to expiry <0 shows "expired"; <7 days red; <30 days orange; <90 days yellow; ≥90 days green. For example a property with monthly rent 4,500 CNY and lease until 2026-10-05, if viewed on 2026-09-20 (15 days left) it is an orange warning and you should immediately contact the tenant to confirm renewal; if left unhandled until 10-06 it turns to "expired" and must be handled per the overdue clause in the contract.',
        'Where is the data stored?',
        'Stored locally in the browser, never uploaded to servers. Records are lost after switching devices or clearing browser data; please back up important leases separately.',
        'Can multiple properties be managed at once?',
        'Yes. Add address, tenant, monthly rent, start/end dates and phone one by one; the list sorts by remaining days and colors each, easing centralized follow-up.',
        'Green = remaining >90 days, yellow = 30–90 days, orange = 7–30 days, red = <7 days',
        'Expired leases are highlighted in red',
        'It is recommended to start communicating renewal with the tenant 60 days before lease end',
        'Data is stored locally in the browser; clearing the browser cache will lose it',
        'About the Lease Term (Start/End/Renewal) Reminder',
        'A lease-expiry reminder management tool for rental properties. Records lease start/end dates, color-graded warnings by remaining days (green/yellow/orange/red), tracks renewal status and provides landlord action suggestions.',
        'Four-level color expiry warning',
        'Renewal status tracking (to contact / renewed / not renewing)',
        'Smart landlord action suggestions',
        'Warning overview dashboard',
        'Lease list CSV export',
        'Multi-property lease management',
        'Landlord expiry renewal reminder',
        'Move-out handover planning',
        'Vacancy-period re-letting planning',
        'E.g.: No.1 xx Road, Chaoyang District',
        'Tenant phone (optional)',
    ]))
    write('rent-2', build('rent-2', [
        '💰 Rent (Market Comparison / Dynamic) Pricing',
        'Enter the rents of multiple comparable listings and correction factors such as floor, orientation, decoration and amenities, to auto-compute a weighted reference rent, rent range and annual growth suggestion.',
        'The tool that "enters the rents of multiple comparable listings and correction factors such as floor, orientation, decoration and amenities to auto-compute a weighted reference rent, rent range and annual growth suggestion" performs professional calculation and outputs results based on input parameters.',
        '📖 View the User Guide for Rent (Market Comparison / Dynamic) Pricing',
        'Target property area (m², optional)',
        'Annual rent growth rate assumption (%)',
        'Comparable listing A',
        'Area (m²)',
        'Floor/orientation composite correction (%)',
        'Similarity weight (optional)',
        'Comparable listing B',
        'Comparable listing C',
        '💡 First convert comparable rent to unit price (CNY/m²·month), then multiply by (1 + composite correction coefficient) to get the target property adjusted unit price, and finally multiply by the target area or average by weight.',
        'Composite correction coefficient: positive if the comparable is better than the target, negative if worse',
        'The larger the similarity weight, the greater the case impact on the final result',
        'Comparable cases should be in the same area as the target, with similar building age and configuration',
        'The rent range is affected by seasonality, lease cycle and bargaining power',
        '📚 Deep Dive: Market-Comparison Rent Pricing',
        'Use the unit prices of 2–3 nearby comparable listings, corrected by floor/orientation/decoration, then weighted, to estimate the target reference monthly rent.',
        'Give a rent range (lowest–highest comparable unit price × area) as the listing upper/lower bounds.',
        'Estimate next-year rent by the annual growth rate assumption, for designing step-up clauses in multi-year leases.',
        'Estimate 90 m² rent from two comparable listings',
        'A: monthly rent 5,000 CNY / 80 m² / correction +5% / weight 3 → unit price 62.50, adjusted 65.63 CNY/m²·month; B: monthly rent 6,500 CNY / 100 m² / correction 0% / weight 2 → unit price 65.00, adjusted 65.00 CNY/m²·month. Weighted unit price = (65.63×3 + 65.00×2) ÷ 5 = 65.38 CNY/m²·month. Target 90 m² → suggested monthly rent 65.38×90 ≈ 5,884 CNY; range 5,850–5,906 CNY; at 3% annual growth, next year about 6,060 CNY.',
        'How to fill the correction coefficient?',
        'Fill by the comparable relative to the target, better or worse',
        ': if the target is better, give the comparable a positive value; if worse, a negative value. Common dimensions are floor, orientation, decoration and amenities; merge them into one composite percentage.',
        'What happens if the target area is not filled?',
        'The tool falls back to the first valid comparable',
        "'s area calculation",
        '. It is recommended to always fill the target area, otherwise the reference rent will not match the actual layout.',
        'About the Rent (Market Comparison / Dynamic) Pricing',
        'A market-comparison rent pricing tool that, based on comparable listings monthly rent, area and composite correction coefficient, computes the target suggested monthly rent, unit price, rent range and dynamic growth expectation.',
        'Multi-case rent correction',
        'Auto unit-price conversion',
        'Similarity weight adjustment',
        'Rent range and growth forecast',
        'Rental property pricing',
        'Rental budget assessment',
        'Rent increase negotiation',
        'Lease investment return estimation',
    ]))
    write('rental-yield', build('rental-yield', [
        '🧮 Rental Yield Calculator',
        'Estimate the annualized return and payback period from the purchase price and monthly rent.',
        '/ Rental Yield Calculator',
        '📖 View the User Guide for Rental Yield Calculator',
        'Annual rent = monthly rent × 12; net income = annual rent − annual expenses (property, maintenance, vacancy and management fees); rental yield = net income ÷ property total price × 100% (gross yield uses annual rent ÷ total price); payback years = 1 ÷ yield; in international comparison, yield below 3% is low, 4%–6% is reasonable, above 6% is good, and a rising vacancy rate significantly lowers the actual return.',
        'Annual holding cost (tax/maintenance etc., CNY)',
        'Calculate return',
        '📚 Deep Dive: Rental Yield and Payback Years',
        'Before buying to rent, use total price, monthly rent and annual holding cost to compute net yield, judging whether it beats wealth management or mortgage cost.',
        'Compare the payback years of different properties as a quantitative basis for selection.',
        'Assess the sensitivity of yield to rising holding costs (tax, property, maintenance, vacancy).',
        'Net return of a 1.8 million CNY property',
        'Total price 1,800,000 CNY, monthly rent 5,000 CNY, annual holding cost 12,000 CNY: annual rent income = 5,000×12 = 60,000 CNY, annual net income = 60,000 − 12,000 = 48,000 CNY, annualized yield = 48,000 ÷ 1,800,000 = 2.67%, payback years = 1,800,000 ÷ 48,000 ≈ 37.5 years. If annual holding cost rises to 24,000 CNY, the yield drops to 2.00%, payback 50 years.',
        'Why not consider the mortgage and property price changes?',
        'This tool computes the pre-tax all-cash basis',
        ', excluding leverage and capital gains. If there is a loan, the monthly interest should be counted as cost and the cash flow computed separately; property price changes need separate evaluation.',
        'What should holding costs include?',
        'Common ones include property fees,',
        ' (if any), insurance, maintenance fund, agency custody fee and estimated vacancy loss. Filling only the actual rent overstates the yield; it is recommended to estimate annually in one go and then enter it.',
    ]))

if __name__ == '__main__':
    main()
