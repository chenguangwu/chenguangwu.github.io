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
    write('calc-73', build('calc-73', [
        "🧮 Used Car Residual Value / Retention Rate",
        "Enter purchase price, age, mileage, brand and condition to compute the current valuation and retention rate along a depreciation curve, and forecast the residual value change over the next 5 years.",
        "Core formula (by input variable): value÷price×100; Math.floor(age)",
        "/ Residual Value / Retention Rate",
        "📖 View the \"Used Car Residual Value / Retention Rate User Guide\"",
        "New car purchase price (10k CNY)",
        "Brand type",
        "Mainstream JV (high retention)",
        "Luxury brand",
        "Domestic brand",
        "New force / NEV",
        "Condition",
        "Near-new / excellent",
        "💡 Valuation = new price × depreciation factor × brand factor × condition factor × mileage correction; about 15% depreciation in the first year, then about 9% per year thereafter.",
        "The valuation model is an empirical estimate; actual transaction is affected by model, configuration, region and market conditions",
        "NEVs usually have lower retention than same-class fuel cars due to battery degradation and fast generational change",
        "Accident / flooded / odometer-rolled cars lose value sharply and need professional assessment",
        "Results are for reference only and are not the sole basis for pricing or trading",
        "📚 In-Depth Analysis: Used Car Residual Value / Retention Rate",
        "Before buying, estimate the residual value after owning a car for N years, compare retention rates across brands / conditions, and assist car selection and selling decisions.",
        "When selling, reverse-engineer a reasonable current valuation from age, mileage, brand and condition to avoid being underpriced.",
        "Do a 5-year holding-cost projection: multiply the yearly forecast residual by the depreciation factor to estimate total depreciation loss.",
        "Example: purchase price 200k CNY, age 5 years, mileage 80k km, mainstream JV brand, good condition, annual base mileage 20k km",
        "Retention coefficients: age retention retained(5)=0.85×0.91⁴≈0.5829; brand factor JV=1.05; good condition=1.00; mileage factor mileageFactor=base 100k / actual 80k=0.8<1 → 1+(1-0.8)×0.05=1.01. Residual=200000×0.5829×1.05×1.00×1.01≈123,600 CNY, retention=123600/200000=61.82%. If domestic brand (0.90) under the same caliber, residual drops to about 106k, showing the brand's significant effect on retention.",
        "Why does the retention rate accelerate downward year by year?",
        "The model uses retained(age)=0.85×0.91^(age-1), i.e. about 85% retained in the first year, then ×0.91 each year thereafter, a compound decline; depreciation is fast in the first few years and slows later, matching most models' actual residual curve. It is only an empirical estimate; in reality it is heavily affected by new-car price cuts, policy (such as emission standards) and supply-demand in the used-car market.",
        "How is the mileage factor calculated?",
        "Expected mileage = annual base mileage × age; when actual / expected > 1 (over mileage) the factor is revised down, to a floor of 0.70; when actual / expected < 1 (under mileage) the factor is revised up, to a ceiling of 1.05. The more over mileage, the greater the residual loss, which is exactly the theoretical basis for leasing return charging by excess mileage.",
        "About Residual Value / Retention Rate",
        "Used car residual value and retention-rate estimation tool; combining the depreciation curve, brand premium, condition and mileage correction, it computes the current valuation and retention rate and forecasts the 5-year residual trend.",
        "Depreciation curve model estimate",
        "Brand premium factor correction",
        "Condition and mileage adjustment",
        "5-year residual forecast curve",
        "Used car buy/sell pricing reference",
        "Trade-in residual assessment",
        "Asset depreciation management",
        "Retention rate horizontal comparison",
    ]))

    write('car-purchase-cost', build('car-purchase-cost', [
        "💰 Car Purchase Cost Calculator",
        "Calculate the total on-road cost (including purchase tax, insurance, registration).",
        "/ Car Purchase Cost Calculator",
        "📖 View the \"car-purchase-cost User Guide\"",
        "Total on-road cost = car price + purchase tax + insurance + registration fee; purchase tax = car price ÷ 1.13 × 10% (current passenger-car rate); the full-cash total outlay is the above sum; a loan adds interest separately, monthly payment = loan amount × monthly rate × (1 + monthly rate)ⁿ ÷ ((1 + monthly rate)ⁿ − 1).",
        "Bare car price (CNY)",
        "Purchase tax rate (%)",
        "Insurance fee (CNY)",
        "Registration fee (CNY)",
        "Calculate on-road price",
        "📚 In-Depth Analysis: Car Purchase Cost Calculator",
        "Account for the on-road price before budgeting: add bare car price, purchase tax, insurance and registration to avoid exceeding budget by staring only at the bare price.",
        "Compare the total outlay of full cash vs loan (this tool computes one-time fees; loan interest is separate) to see the true car-buying cost.",
        "Compare the on-road price difference of two cars under different purchase tax rates (NEV exempt / fuel car 10%).",
        "Example: bare car price 150k CNY, purchase tax rate 10%, insurance 5,000 CNY, registration 500 CNY",
        "Purchase tax=150000×10%=15000 CNY; total cost=bare 150000+purchase tax 15000+insurance 5000+registration 500=170500 CNY (on-road price). If it were a NEV (purchase tax exempt), the on-road price drops to 155500 CNY, saving 15k.",
        "Why is purchase tax bare car price × 10%?",
        "The passenger-car purchase tax base is the",
        "VAT-excluded",
        "car price, i.e. invoice price ÷ 1.13, then × 10%; the tool simplifies by estimating directly on bare price × rate, so the result is slightly higher than the precise value (about a 1.13× difference). NEV passenger cars are currently exempt from vehicle purchase tax; you can switch the rate to 0 to compare.",
        "Does this on-road price include loan interest?",
        "No. This tool only computes one-time purchase fees (purchase tax + insurance + registration, etc.); the interest and handling fees of instalment loans must be added separately to the total holding cost.",
    ]))

    write('checker-3', build('checker-3', [
        "✅ Chassis Inspection (rust / abnormal noise)",
        "A used-car chassis system item-by-item checklist covering 12 key parts such as frame rust, suspension noise and exhaust leakage, generating a condition assessment report",
        "Core formula (by input variable): Math.round(totalScore÷totalWeight)",
        "📖 View the \"Chassis (rust / noise) Inspection User Guide\"",
        "Chassis inspection checklist",
        "Select each result; the system auto-computes the overall chassis score",
        "Generate inspection report",
        "📚 In-Depth Analysis: Chassis (rust / noise) Inspection",
        "Before buying, do an item-by-item chassis-system inspection of the target car, covering 12 key parts such as frame rust, suspension noise and exhaust leakage.",
        "Re-inspect before and after a used-car dealer's reconditioning, recording each item's state (normal / slight / abnormal) to assess reconditioning quality.",
        "Quantify the inspection into a condition assessment report as a basis for bargaining or returning the car.",
        "Example: item-by-item inspection of an 8-year-old, 120k-km car",
        "The 12 inspection items are each scored by weight (normal = full, slight = partial, abnormal = 0 and counted into the problem list). If frame, suspension and exhaust show \"abnormal\", the corresponding group's weighted deduction is significant, and the total maps to poor condition with a key-risk warning; if only an individual non-structural part has slight rust, the total stays medium. The report summarises group scores and problem items by group for targeted bargaining.",
        "How are the inspection items scored?",
        "Each item has a fixed weight; selecting normal/slight/abnormal maps to different score coefficients (abnormal scores 0 and is listed in the problem list); group scores are weighted into a total, then mapped to a condition grade. Weights follow item importance: structural parts (frame, suspension) weigh more than trim.",
        "Can a chassis inspection replace a lift inspection?",
        "No. This tool is a structured checklist and scoring aid that helps record systematically; the final judgement still needs a professional technician on a lift with a real car, combined with chassis images and maintenance records.",
        "Chassis inspection is recommended on a lift, focusing on rust, deformation, leakage and noise",
        "Scoring standard: good (no issue) / fair (slight wear) / poor (obvious issue) / severe (needs repair)",
        "This tool is for used-car inspection reference; for major issues seek a professional recheck",
        "About Chassis (rust / noise) Inspection",
        "Used-car chassis-system inspection tool covering 12 key parts such as frame, floor, subframe, suspension and exhaust/oil lines, assessing rust / noise / leakage / deformation item by item, generating an overall chassis score and repair advice.",
        "12 key chassis parts inspected item by item",
        "Four-level scoring (good / fair / poor / severe)",
        "Purchase advice by age and mileage",
        "Pre-purchase chassis inspection",
        "Lift inspection record tool",
        "Vehicle repair and maintenance assessment",
        "Used-car trade bargaining reference",
    ]))

    write('detector-19', build('detector-19', [
        "🔍 Flood Damage Detection (traces / musty smell)",
        "A used-car flood-damage detection checklist, item-by-item checking of 15 flood indicators such as interior musty smell, water stains, silt buildup and abnormal rust, to judge the flood-risk level",
        "📖 View the \"Flood Damage (traces / musty smell) Detection User Guide\"",
        "Flood-damage detection checklist",
        "Select each result (normal / suspicious / confirmed); the system auto-assesses flood risk",
        "Detect flood risk",
        "📚 In-Depth Analysis: Flood Damage (traces / musty smell) Detection",
        "Before buying, screen 15 flood indicators item by item: interior musty smell, water stains, silt buildup, abnormal metal rust, etc.",
        "Mark \"confirmed flood\" and \"suspected flood\" items separately and quantify the flood-risk level.",
        "Use the result as a basis for deciding whether to go for deep detection (under carpet, wiring harness, etc.).",
        "Example: interior musty smell, seat-rail silt and seat-belt-root water stain all confirmed",
        "The 15 indicators are scored by weight; items checked \"confirmed flood\" (value=2) go into the confirmed list with accumulated weight, items checked \"suspected\" (value=1) go into suspicious. If confirmed items concentrate in interior and metal parts, the total falls in the high-risk band and is judged \"high flood-risk car\", strongly advising to abandon or deep-tear-down; if only individual suspected items, judge low risk and advise recheck.",
        "Do confirmed and suspected items weigh the same?",
        "Scoring accumulates checked value × item weight (confirmed=2, suspected=1), so a confirmed item contributes twice a suspected one; the confirmed list is also listed separately for spotting hard damage at a glance. The final risk level is set by a total-score threshold.",
        "Does a high flood-risk judgement mean it is definitely a flood car?",
        "Not necessarily. Individual indicators (such as rain ingress, car-wash residue) may false-positive, but when multiple confirmed indicators hit at once the probability is very high. The conclusion is only a risk hint; legal and trade determination needs a report from a professional appraisal agency.",
        "Flood-car detection focus: silt traces, abnormal rust, musty smell, electronic failures, interior water stains",
        "Key parts: seat-belt bottom, seat rails, under carpet, wire-harness connectors, spare-tyre well",
        "Flood cars carry serious safety hazards; if flood signs are detected, strongly advise abandoning the purchase",
        "About Flood Damage (traces / musty smell) Detection",
        "Used-car flood-damage detection tool covering 15 key flood indicators across interior traces, electrical system, engine bay, chassis and exterior, assessing musty smell / water stain / silt / abnormal rust item by item, computing a flood-risk index and judging the flood-risk level.",
        "15 key flood indicators detected item by item",
        "Three-level judgement (normal / suspicious / confirmed)",
        "Flood-risk index quantified assessment",
        "Regional risk distribution and purchase advice",
        "Pre-purchase flood screening",
        "Post-rainstorm / flood vehicle inspection",
        "Used-car trade risk assessment",
        "Water-damaged car appraisal reference for insurance claims",
    ]))


if __name__ == '__main__':
    main()