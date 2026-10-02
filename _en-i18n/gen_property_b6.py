#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'property')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'property')
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
    out = {'slug': slug, 'industry': 'property', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('elevator-energy', build('elevator-energy', [
        "⚡ Lift Energy Consumption Estimate",
        "Estimate lift energy consumption from floor count, power rating and daily trip count, supporting property electricity cost accounting",
        "📖 Read the \"Lift Energy Consumption Estimate\" guide",
        "Lift energy = trip count × energy per trip",
        "Number of lifts (units)",
        "Floor height (metres)",
        "Rated power (kW)",
        "Average load factor (%)",
        "Daily trips (per lift)",
        "Average floors travelled per trip",
        "Daily standby hours (hours)",
        "Standby power (kW)",
        "Estimate energy consumption",
        "📚 Deep dive: lift energy consumption estimate",
        "Property management estimates the annual lift electricity use of a whole building for the energy budget",
        "Compare energy saved before and after switching to energy-saving control or off-peak operation",
        "Estimate the total before disclosing shared lift electricity charges to owners",
        "Daily energy per lift",
        "12 floors, 3 m floor height, 11 kW power, 600 trips per day, 8 floors per trip, load factor 0.5 → running energy about 600×8×3×11×0.5/3600 ≈ 29.3 kWh; standby 20 h×0.3 kW = 6 kWh; about 35.3 kWh per lift per day, roughly 1060 kWh per month.",
        "Annual consumption for the whole building",
        "4 lifts × 35.3 kWh × 365 days ≈ 51538 kWh; at 0.6 CNY/kWh the annual electricity cost is about 30900 CNY, usable as the base for allocating shared lift charges.",
        "Which factors affect lift electricity use most?",
        "Trip count, floors served, load factor and",
        "standby power",
        "; off-peak scheduling plus variable frequency drives typically reduces consumption by 15%-30%.",
        "What if the estimate differs a lot from the meter?",
        "The meter governs; the estimate is for budgeting and disclosure baselines. A large gap means the trip or load assumptions are off, so adjust the parameters.",
        "About \"Lift Energy Consumption Estimate\"",
        "Estimates lift running and standby energy from floor count, power rating, daily trip count and load factor, outputting daily, monthly and annual consumption plus electricity cost.",
        "Separate running and standby energy",
        "Load factor modelling",
        "Daily, monthly and annual estimates",
        "Electricity cost conversion",
        "Lift Energy Estimate Tool - estimate daily lift trips and power consumption. Free online property management tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('irrigation-schedule', build('irrigation-schedule', [
        "🏦 Greening Irrigation Schedule",
        "Generate a zoned irrigation schedule from simulated weather and plant water demand, skipping rainy days and adding extra watering in hot weather",
        "📖 Read the \"Greening Irrigation Schedule\" guide",
        "Irrigation schedule = water demand / flow rate",
        "Number of scheduling days",
        "Random seed",
        "Rainy day probability (%)",
        "Irrigation zone (name + plant type + area in ㎡)",
        "+ Add zone",
        "Generate schedule",
        "Copy schedule",
        "📚 Deep dive: greening irrigation schedule",
        "The property greening team sets weekly watering plans by season and vegetation type, avoiding rainy days",
        "Increase lawn watering frequency during droughts and reduce it automatically in the rainy season",
        "Intensify watering for the first 30 days after planting, then fall back to the normal frequency",
        "Routine lawn schedule",
        "Lawn demand 8 L/㎡·session, twice weekly, area 1200 ㎡ → 9600 L per session and 19200 L per week. When the chance of rain that day exceeds 60%, skip and defer, preventing root rot and waste.",
        "Staggering trees and shrubs",
        "Trees 15 L/plant·session (once a week), shrubs 6 L/plant·session (twice a week), 80 trees + 200 shrubs → 1200 + 2400 = 3600 L per week; scheduling lawns separately avoids overpressuring the pipe network.",
        "How do you decide whether a day needs watering?",
        "Look at the rain probability and soil moisture: skip if rain is likely or it just rained; only water on schedule after sustained hot dry weather with low moisture, avoiding waterlogging and waste.",
        "Can different vegetation share one schedule?",
        "No. Lawns, trees and shrubs differ greatly in water demand and frequency, so schedule by type and compute workload separately.",
        "About \"Greening Irrigation Schedule\"",
        "Automatically generates a multi-day irrigation schedule from simulated weather (sunny/cloudy/rainy) and per-zone plant water demand, skipping rainy days and adding extra watering in hot weather.",
        "Random weather simulation",
        "Per-zone plant types",
        "Temperature-adjusted water volume",
        "Calendar-style schedule",
        "Greening Irrigation Schedule Generator - generate an irrigation schedule from weather simulation. Free online property management tool. Business and office tool to improve work efficiency, data processed locally to protect privacy.",
    ]))

    write('index', build('index', [
        "🏢 Property Management Tools",
        "Property Management",
        "Property Management Tools",
        "Enter total community property costs plus per-household areas or counts; the tool allocates them proportionally (switchable between area-based and per-household) to each unit, supports importing custom household details and generates a per-household payable list, simplifying charge accounting for homeowners committees and property companies.",
        "Enter floor area, gross-up coefficient, property fee unit price and payment period to compute in-unit area, common area, property fee and common area fee, and summarise the total payable.",
        "The benchmarking comparison, learning and surpassing analysis tool compares gaps between your own metrics and the benchmark target by indicator and outputs improvement directions, suitable for benchmarking improvement in property and operations management.",
        "Enter the area and cleaning difficulty coefficient of each zone; the tool converts them into standard workload and balances the assignment across multiple cleaning staff, outputting each person's zones and man-hours so property management can schedule fairly by area and difficulty and avoid overload.",
        "Enter the floor count, lift rated power and daily trips (up and down); the tool estimates average daily and monthly lift consumption, supporting electricity cost accounting, comparing energy-saving retrofit benefits and allocating shared energy.",
        "Using simulated weather (skip on rain, add extra in heat) and per-zone plant water demand, it automatically generates a zoned greening irrigation schedule that arranges water volume and frequency sensibly and saves water.",
        "The property budget preparation tool projects project profit and loss from the cost, income and profit structure, suitable for financial calculation of annual budgets, pricing and service package design at property companies.",
        "Enter fire drill assessment (10 items) and routine facility inspection (10 items) to automatically generate drill assessment reports and rectification lists, standardising fire drill and facility inspection records.",
        "PDCA-cycle-based property service quality management assessment, evaluating maturity across standard setting, inspection execution and problem rectification",
        "Performance (assessment / scoring) system",
        "Weighted scoring across six dimensions (customer satisfaction 20% + facility maintenance 20% + response timeliness 15% + collection rate 15% + safety compliance 15% + environmental quality 15%), automatically producing an assessment grade",
        "The property service quality inspection system weighted-scores 23 items across cleaning, security, greening and facility maintenance, outputting a quality grade and rectification list, suitable for property assessment.",
        "Suppliers are weighted-scored across qualification assessment (30%), contract compliance (30%) and process supervision (40%), producing a composite rating, weak links and management recommendations.",
        "Log space occupancy and fee records to compute turnover and revenue by time band, for car park operational accounting; entirely front-end and nothing leaves the browser.",
        "Property finance income, expenditure, reporting and audit management tools apply standard financial rules to operating income and expenditure and generate reports, suitable for property company accounting and compliance audit.",
        "Lift maintenance and annual inspection cycle management, auto-deriving the next due date from fortnightly/quarterly/half-yearly/annual maintenance and the statutory annual inspection, with overdue compliance warnings.",
        "Enter the area of common area components such as lift shafts, stairwells and corridors; the tool totals the common area, computes the gross-up coefficient, allocates it to each unit by floor area and gives the usable area ratio, helping homebuyers check whether the title area composition is compliant.",
        "Inspection (route / cycle) planning",
        "Build inspection routes and checkpoints, schedule them automatically by cycle, record completion and compute the completion rate and issue count.",
        "The maintenance response, completion and follow-up timeliness tool segments each stage duration and closure rate from the input parameters, suitable for end-to-end timeliness control and satisfaction improvement in property services.",
        "The maintenance repair request response timeliness tool computes the duration from request to response and the compliance rate, suitable for property customer service SLA management and service efficiency assessment.",
        "The energy (utilities / gas) allocation tool spreads common energy costs across tenancies by area or meter, suitable for settlement and transparency management of energy costs in commercial properties and office buildings.",
        "About \"Property Management Tools\"",
        "The Property Management Tools collection contains 20 free online tools covering the common calculation, conversion and lookup needs of property management scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find practical tools here that are ready to use the moment you open them. All tools run entirely in the front end and upload no data to the server, protecting privacy and security.",
        "The property management tools collected on this page include (representative tools):",
        "These tools help you complete common property management tasks quickly without memorising complex formulas or manual conversions - just enter the values and get the result.",
        "Do the property management tools need downloading or registration?",
        "No. All property management tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the property management tool results accurate, and is the data secure?",
        "The tools are based on public mathematical formulas and general industry standards, computing locally in your browser for instant results. All computation happens on your own device and data is never uploaded to the server, so privacy and security are assured.",
    ]))


if __name__ == '__main__':
    main()