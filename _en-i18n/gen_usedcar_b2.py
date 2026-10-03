#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'usedcar')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'usedcar')
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
    out = {'slug': slug, 'industry': 'usedcar', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('ershouchetanpanyijiakongjianyuce', build('ershouchetanpanyijiakongjianyuce', [
        "🔮 Used Car Negotiation Space Forecast",
        "Enter the seller's quote, condition, market heat, age and mileage to forecast a reasonable deal range, negotiable margin and suggested opening strategy.",
        "Core formula (by input variable): max(0.01,min(0.30,suggestedSpace)); max(0.02,min(0.35,baseSpace)); ask×(1-baseSpace×0.5)",
        "📖 View the \"Used Car Negotiation Space Forecast User Guide\"",
        "Seller's quote (10k CNY)",
        "Mental max budget (10k CNY, optional)",
        "Condition grade",
        "Excellent / near-new",
        "Market heat",
        "Hot model / undersupply",
        "Cold / high inventory",
        "Negotiation style",
        "Conservative and steady",
        "Routine probing",
        "Aggressive price push",
        "💡 The negotiation space is affected by condition defects, excess mileage, market heat and age; it is advised to open at the \"acceptable floor price\" first, then keep a 3%–8% negotiation buffer.",
        "The forecast is an empirical range; the actual deal depends on both sides' psychology, information symmetry and negotiation skill",
        "Accident, flooded and odometer-rolled cars should be pressed hard on price and require professional inspection",
        "Hot models have limited negotiation space; cold models can win larger discounts",
        "It is advised to reserve budget for inspection, reconditioning and transfer fees",
        "📚 In-Depth Analysis: Used Car Negotiation Space Forecast",
        "Before viewing, enter the seller's quote, condition, market heat, age and mileage to forecast a reasonable deal range and negotiable margin.",
        "Set an opening strategy: the conservative / routine / aggressive styles correspond to different first offers and price-push room.",
        "Combine your own budget to judge whether the quote falls in the dealable range and avoid blind bidding-up.",
        "Example: seller quote 200k CNY, budget 180k, age 5 years, mileage 120k km, annual base 20k, good condition, normal market, routine style",
        "Base space = good condition (5%) + normal market (0%) + age bonus min(8%,5×1%=5%) + mileage correction (12/10=1.2 → +20% → +2%) = 12%, capped at 12%. Reasonable deal range = 200k×(1-12%) ~ 200k×(1-6%) = 176k~188k CNY; suggested first offer = 200k×(1-12%) = 176k, target deal ≈ 182k. Budget 180k is close to the target, so the floor must be fought for.",
        "What is the upper limit of the negotiation space?",
        "The base space (condition + heat + age + mileage) is capped at 2%~35%, then multiplied by the style coefficient (conservative 0.6 / routine 1.0 / aggressive 1.4) and capped at 1%~30%. That is, no matter how bad the condition, the suggested first offer bottoms at 70% of the quote (aggressive ceiling).",
        "Is the forecast deal range accurate?",
        "The model estimates from empirical coefficients; what it gives is a \"negotiation anchor\" rather than an exact deal price; the real deal is affected by source scarcity, buyer urgency and regional market. It is advised to cross-verify with recent same-model deal prices and an inspection report; this tool only assists pricing strategy.",
        "About Used Car Negotiation Space Forecast",
        "Used-car negotiation assistant tool; integrating the seller's quote, condition, market heat, age and mileage, it forecasts a reasonable deal range and negotiable margin, and gives first-offer and target-price advice under different negotiation styles.",
        "Multi-factor modelling of condition, market heat, age and mileage",
        "Reasonable deal range and target-price forecast",
        "Three negotiation strategies: conservative / routine / aggressive",
        "Budget vs forecast-range comparison hint",
        "Budget assessment before on-site viewing",
        "Negotiation prep with dealers / private sellers",
        "Horizontal comparison of multiple sources",
        "Avoid impulsive high-price deals",
        "Optional",
    ]))

    write('estimate-38', build('estimate-38', [
        "💰 Transfer (fee / process) Estimator",
        "Enter the deal price, displacement, first-registration year and region type to estimate the purchase tax, transfer fee, plate fee, compulsory insurance and agency fee involved in a used-car transfer.",
        "Core formula (by input variable): price÷1.13×0.10; max(0,age)",
        "📖 View the \"Transfer (fee / process) Estimator User Guide\"",
        "Vehicle deal price (10k CNY)",
        "First registration year",
        "Displacement (L)",
        "1.0L and below",
        "1.0L–1.6L (incl.)",
        "1.6L–2.0L (incl.)",
        "2.0L–2.5L (incl.)",
        "2.5L–3.0L (incl.)",
        "3.0L–4.0L (incl.)",
        "4.0L and above",
        "City tier",
        "Tier 3 and below",
        "Agency service fee (CNY)",
        "Whether to re-plate",
        "💡 Used cars are usually exempt from purchase tax (paid on the new car); but if the new car was untaxed or the deal price is well above the tax base, the tax authority may tax by assessed value. This tool handles the usual exemption and provides a theoretical estimate.",
        "Transfer fees vary greatly by city, vehicle-management office, displacement and age; results are for reference only",
        "The vehicle-and-vessel tax is levied by displacement and standards differ by locality; this tool uses empirical ranges",
        "Compulsory traffic insurance floats by seat count and prior-year claims; it decreases yearly if no claim",
        "Actual fees are subject to the vehicle-management office, tax authority and insurance company",
        "📚 In-Depth Analysis: Transfer (fee / process) Estimator",
        "Before closing, estimate the fees of a used-car transfer: transfer transaction fee, plate fee, vehicle-and-vessel tax, compulsory insurance and agency fee.",
        "Compare fee differences across regions (tier1/2/3 cities) and whether to re-plate.",
        "Understand that the purchase tax is usually exempt in the used-car stage, and only a theoretical price is given as reference.",
        "Example: deal price 100k CNY, registered 2020 (age 6), displacement 1.6L, tier2 city, agency 300 CNY, needs re-plate",
        "Transfer fee TRANSFER[tier2]=600 CNY; plate fee PLATE[tier2]=300 CNY; annual vehicle-and-vessel tax VVT[1.6L]=300 CNY; compulsory insurance 950 CNY; agency 300 CNY; normal total transfer fee = 600+300+300+300+950 = 2450 CNY. Theoretical purchase tax = 100000÷1.13×10%≈8849.56 CNY (used cars usually exempt, for reference only); with tax included the total is about 11299.56 CNY.",
        "Do used cars still pay purchase tax?",
        "A registered used car is no longer levied vehicle purchase tax on ownership transfer (the original owner paid it); the tool's \"theoretical purchase tax\" is only a formula-based theoretical value clearly marked \"exempt\" and is not an actual charge. What really occurs is the transfer fee, plate fee, vehicle-and-vessel tax (annual), compulsory insurance (annual) and possible agency fee.",
        "Do fees differ much by city?",
        "By city tier tier1/2/3, the transfer fee is 800/600/400 CNY and the plate fee 500/300/200 CNY; the vehicle-and-vessel tax varies markedly by displacement (1.0L 180 CNY to 4.0L+ 4500 CNY). Specifics are subject to the local vehicle-management office and tax window; this tool gives a range reference.",
        "About Transfer (fee / process) Estimator",
        "Used-car transfer fee estimator; considering deal price, displacement, age, city tier and whether to re-plate, it computes the transfer fee, plate fee, vehicle-and-vessel tax, compulsory insurance and agency fee, and notes the purchase-tax exemption rule.",
        "Estimate transfer fee by city tier",
        "Estimate vehicle-and-vessel tax by displacement",
        "Re-plate / keep original plate optional",
        "Fee breakdown and total split",
        "Used-car trade budget",
        "Agency service quote check",
        "Car purchase on-road cost estimate",
    ]))

    write('index', build('index', [
        "🚙 Used Car Tools",
        "Used Cars",
        "Used Car Tools",
        "Car Purchase Cost Calculator",
        "The Car Purchase Cost Calculator is a free online used-car tool; the Car Purchase Cost Calculator is a free online used-car tool, enter the parameters to get real-time results; runs purely on the front end, data not uploaded, no registration, just open the browser to use. Runs purely on the front end, data not uploaded, no registration…",
        "Compare actual mileage with the age-based reference mileage, compute the excess-mileage charge and value-adjustment ratio, and judge whether wear is in the normal range, for residual-value assessment and leasing-return settlement.",
        "Used Car Residual Value / Retention Rate",
        "Enter purchase price, age, mileage, brand and condition to compute the current valuation and retention rate along a depreciation curve, and forecast the 5-year residual change.",
        "Used Car Valuation",
        "An online used-car valuation tool: enter model, registration year, mileage and condition, combine the condition rate and depreciation model to estimate a residual-value range, assisting buy/sell pricing, computed locally on the front end.",
        "Used-car flood-damage detection checklist, item-by-item checking of 15 flood indicators such as interior musty smell, water stains, silt buildup and abnormal rust, to judge the flood-risk level",
        "Used-car electrical-system test checklist covering 14 electrical functions such as lights, wipers, windows, AC, audio and charging, generating a fault-diagnosis report",
        "Used-car engine comprehensive score covering 10 key indicators such as start performance, idle stability, acceleration response, leakage and abnormal noise",
        "Used-car chassis-system item-by-item inspection checklist covering 12 key parts such as frame rust, suspension noise and exhaust leakage, generating a condition assessment report",
        "Enter the vehicle deal price, displacement, first-registration year and region type to estimate the purchase tax, transfer fee, plate fee, compulsory insurance and agency fee involved in a used-car transfer.",
        "Used Car Negotiation Space Forecast",
        "Enter the seller's quote, condition, market heat, age and mileage to forecast a reasonable deal range, negotiable margin and suggested opening strategy.",
        "Enter maintenance details (item, mileage, cost, 4S store or repair shop) to score maintenance completeness by current mileage and estimate the value-add effect on used-car residual, supporting an exported assessment report.",
        "About Used Car Tools",
        "The Used Car Tools collection gathers 11 free online tools covering the common calculation, conversion and lookup needs of used-car scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run purely on the front end, data is not uploaded to a server, and your privacy and security are protected.",
        "The used car tools collected on this page include (representative tools):",
        "These tools help you quickly finish common used-car tasks without memorising complex formulas or doing manual conversions — just enter the values and get the result.",
        "Do the Used Car Tools require a download or registration?",
        "No. All used car tools on this page are purely front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the calculation results of the Used Car Tools accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available immediately. All operations run locally on your device, data is never uploaded to a server, and your privacy and security are guaranteed.",
    ]))

    write('rater-37', build('rater-37', [
        "🚗 Engine (running / leakage) Rating",
        "Used-car engine comprehensive score covering 10 key indicators such as start performance, idle stability, acceleration response, leakage and abnormal noise",
        "Core formula (by input variable): Math.round(totalScore÷totalWeight)",
        "📖 View the \"Engine (running / leakage) Rating User Guide\"",
        "Engine inspection items",
        "Select each result; the system auto-weights the comprehensive engine score",
        "Engine displacement (L)",
        "Generate score report",
        "📚 In-Depth Analysis: Engine (running / leakage) Rating",
        "Before buying, score the engine on 10 key indicators: start performance, idle stability, acceleration response, leakage, abnormal noise, etc.",
        "Merge the engine score with chassis and electrical scores to form an overall vehicle condition rating.",
        "Use abnormal items (such as oil seepage, knocking noise) as a key basis for bargaining or reconditioning.",
        "Example: cold start normal, idle slight shake, no leakage, good acceleration response",
        "The 10 items are each scored by weight (normal = full, slight = partial, abnormal = 0 and counted into problems). Idle slight shake deducts partial points while the rest are normal, so the engine total is in the upper-middle band and flags the \"idle slight shake\" risk point; if oil leakage and metal noise appear together, several items score 0, the total drops sharply and is judged high-risk, advising to abandon or assess a major overhaul.",
        "How is the engine score weighted?",
        "Core conditions such as start, idle and acceleration weigh higher; fault signs like noise / leakage score 0 by severity and are listed separately; the total is weighted and mapped to excellent / good / fair / poor grades. Specific weights are built into each item's configuration.",
        "Can the score detect oil burning?",
        "Indirectly. Long-term oil burning shows in exhaust, oil consumption and carbon-buildup indicators, but this tool is a static checklist; confirming oil burning still needs professional cylinder-pressure testing and measured oil consumption.",
        "Engine inspection is advised in two stages: cold start + warm running",
        "Scoring standard: excellent / good / fair / poor / severe, focusing on leakage and noise",
        "Engine repair costs are high; for severe issues advise abandoning the purchase",
        "About Engine (running / leakage) Rating",
        "Used-car engine comprehensive rating tool covering 10 key indicators of running performance (start / idle / acceleration / vibration), leakage (engine oil / coolant / transmission oil) and sound/exhaust/instrument, weighting a comprehensive score and giving repair advice.",
        "10 key engine indicators assessed item by item",
        "Five-level scoring (excellent / good / fair / poor / severe)",
        "Repair-cost estimate by mileage",
        "Pre-purchase engine inspection",
        "Engine repair and maintenance assessment",
        "Pre-major-overhaul engine assessment",
    ]))


if __name__ == '__main__':
    main()