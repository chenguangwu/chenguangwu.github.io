#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'logistics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'logistics')
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
    out = {'slug': slug, 'industry': 'logistics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "🚚 Logistics & Shipping Tools",
        "Logistics & Shipping",
        "Logistics and shipping tools",
        "Express Freight Cost Calculator",
        "An online express freight cost calculator that takes weight, volume and destination and estimates the charge under the billing rules, supporting multiple carriers and volumetric weight, helping you compare carriers before shipping. Runs entirely in the browser.",
        "Package Volume Calculator",
        "An online package volume calculator that derives volume and volumetric weight from length × width × height, for logistics billing and loading plans. Runs entirely in the browser.",
        "A vehicle loading calculator that estimates volume and weight utilization and the number of loadable boxes for the selected vehicle type, supporting fleet dispatch and loading plan optimization for transport scheduling and cost accounting.",
        "Takes the larger of actual weight and volumetric weight as the chargeable weight, then combines distance, cargo class and transport mode to compute base freight, fuel surcharge and total cost.",
        "Competition (analysis / strategy / differentiation)",
        "Normalizes the range of each carrier's transit time, price and damage rate, then weights them (transit time 0.4 / price 0.3 / damage rate 0.3) to get a composite score and ranking, and combines the weak spots to give a differentiated position and improvement suggestions.",
        "The quality control (operation / quality / inspection) process is a free online logistics and shipping tool. This express service quality control metrics calculator takes the handled volume and the counts of lost, delayed, damaged and appealed items, and automatically computes four quality control rates and rates the grade against the YZ/T 0168 standard. Runs entirely in the browser, data is not uploaded, and no sign-up is needed.",
        "Transport Fuel Cost",
        "Enter mileage, fuel consumption per 100 km, fuel price plus tolls and depreciation, and compute total transport fuel cost, fuel expense and combined cost, for logistics quoting and cost accounting.",
        "Quality Control (process / standard / inspection) mechanism",
        "The quality control (process / standard / inspection) mechanism is a free online logistics and shipping tool. This fresh produce quality assessment tool takes appearance, odor, texture scores and storage temperature, and comprehensively rates the freshness grade while estimating the remaining shelf life. Runs entirely in the browser, data is not uploaded, no sign-up is required, just open it in a browser.",
        "Returns (reverse / inspection) process",
        "The returns reverse-logistics process inspection tool covers four modules of return receiving, quality inspection, sorting and record traceability with 20 key points in total, quantifying process maturity and generating an improvement checklist to raise returns handling efficiency.",
        "Green (new energy / carbon) assessment",
        "Computes the carbon emissions of different transport modes, compares the emission reduction of new-energy vehicles, assesses green logistics level, and outputs a carbon emission report with reduction suggestions.",
        "KPI (on-time / intact) statistics",
        "Enter the on-time and intact status of each waybill to compute the on-time rate and the intact rate and roll them up by period, for logistics service quality assessment. Pure front-end statistics, nothing leaves the browser.",
        "The stocktake (cycle / circulation / variance) analysis is a free online logistics and shipping tool, stocktake (cycle / circulation / variance) analysis. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected. Runs entirely in the browser, data is not uploaded, no sign-up is needed, just open it in a browser.",
        "The finance (profitability / cash flow / statements) analysis is a free online logistics and shipping tool, results are computed in real time from your inputs; runs entirely in the browser, data is not uploaded, no sign-up is needed, just open it in a browser.",
        "KPI (order fill / cycle / quality)",
        "The KPI (order fill / cycle / quality) is a free online logistics and shipping tool, comparing KPI trends across periods, with bars scaled relative to the maximum value. Runs entirely in the browser, data is not uploaded, no sign-up is needed, just open it in a browser.",
        "Loss (control / prevention / analysis) system",
        "The loss (control / prevention / analysis) system is a free online logistics and shipping tool, loss (control / prevention / analysis) system. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected. Runs entirely in the browser, data is not uploaded, no sign-up is needed, just open it in a browser.",
        "About \"Logistics & Shipping Tools\"",
        "The Logistics & Shipping Tools collection gathers 15 free online tools covering the common calculation, conversion and lookup needs of logistics and shipping scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use practical tools here. Every tool runs purely in the browser and never uploads data to a server, so your privacy is protected.",
        "Logistics and shipping tools included on this page (some representative tools):",
        "These tools help you finish common logistics and shipping tasks quickly, with no need to memorize complex formulas or convert by hand — enter the inputs and you get the result.",
        "Do the logistics and shipping tools need a download or sign-up?",
        "No. Every tool on this page is a pure front-end online tool. Open the page and you can use it right away, with no software to install, no account to create, and no data uploaded at all.",
        "Are the results of the logistics and shipping tools accurate? Is the data secure?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device and data is never uploaded to a server, so privacy and security are guaranteed.",
    ]))
    write('cycle-16', build('cycle-16', [
        "⚖️ Supply Chain KPI Dashboard",
        "Enter supply chain operations data to automatically compute core KPIs such as order fill rate, on-time delivery rate, defect rate, inventory turnover and cash conversion cycle, with red-yellow-green scoring and benchmark comparison.",
        "\"Enter supply chain operations data to automatically compute core KPIs such as order fill rate, on-time delivery rate, defect rate, inventory turnover and cash conversion cycle, with red-yellow-green scoring and benchmark comparison.\" Computed professionally from the input parameters, with results output.",
        "KPI (order fill / cycle / quality)",
        "/ KPI (order fill / cycle / quality)",
        "Data entry for this period",
        "Period name",
        "Total orders",
        "On-time delivered orders",
        "Defect / return count",
        "Order delivery cycle (days)",
        "Inventory turnover (times/year)",
        "Accounts payable period (days)",
        "Accounts receivable period (days)",
        "Compute KPI",
        "Save this period",
        "KPI scorecard",
        "Benchmark comparison",
        "Trend tracking",
        "KPI trends compared across periods, with bars scaled relative to the maximum value.",
        "📚 Deep dive: Supply Chain KPI Dashboard",
        "Fulfillment and delivery monitoring: aggregates order fulfillment rate, on-time delivery rate, stockout rate and other metrics, generating weekly/monthly trend boards to quickly locate problem stages.",
        "Inventory efficiency assessment: computes inventory turnover and the share of slow-moving stock, identifying low-efficiency SKUs that tie up capital, supporting clearance and replenishment decisions.",
        "Supplier delivery comparison: compares on-time rate and batch pass rate across suppliers side by side, supporting sourcing concentration and backup plans.",
        "Monthly supply chain KPI board example",
        "Input: order fulfillment rate 96%, on-time delivery rate 92%, inventory turnover 8 times/year, stockout rate 2%. After aggregation the system flags that the on-time delivery rate is below the 95% target and raises an alert, and points out the high slow-moving stock share, for operational review and improvement.",
        "What if the metric definitions are inconsistent?",
        "First unify the definition and statistical period of each metric (for example a rolling month basis), then aggregate and compare, to avoid misjudgments caused by different bases.",
        "Where does the data come from, and is it uploaded?",
        "You enter it locally or paste exports from each system. The tool computes only inside the browser, uploads nothing, and is safe to use.",
        "Order fill rate = on-time delivered orders / total orders × 100%",
        "Defect rate = defect count / total orders × 100%",
        "Days inventory outstanding = 365 / inventory turnover",
        "Cash conversion cycle = days inventory outstanding + accounts receivable period - accounts payable period",
        "Green light = excellent, yellow light = needs attention, red light = needs improvement",
        "Competition (analysis / strategy / differentiation)",
        "About \"KPI (order fill / cycle / quality)\"",
        "A supply chain core KPI dashboard calculator. Enter order, delivery, defect and inventory operations data to automatically compute order fill rate, on-time delivery rate, defect rate, inventory turnover and cash conversion cycle, with red-yellow-green scoring and trend tracking.",
        "Automatic computation of 6 core supply chain KPIs",
        "Red-yellow-green scorecard visualization",
        "Industry benchmark comparison table",
        "Multi-period trend tracking",
        "Historical data saved locally",
        "Monthly / quarterly supply chain performance assessment",
        "Operational improvement tracking",
        "Supplier performance management",
        "KPI reporting for management",
        "e.g. July 2026",
    ]))
    write('calc-78', build('calc-78', [
        "🚚 Freight Rate Calculation (Charges / Surcharges)",
        "Takes the larger of actual weight and volumetric weight as the chargeable weight, then combines distance, cargo class and transport mode to compute base freight, fuel surcharge and total freight cost.",
        "Core formulas (by input variable): chargeable×classRate×(dist÷100); max(1,Math.ceil(chargeable÷cap)); max(weight,volWeight)",
        "/ Freight Rate Calculation (Charges / Surcharges)",
        "Transport mode",
        "Less-than-truckload LTL",
        "Full-truckload FTL",
        "Actual weight (kg)",
        "Volume (m³)",
        "Distance (km)",
        "Cargo class (determines the rate)",
        "Class 50 (heavy goods)",
        "Class 70 (general goods)",
        "Class 100 (light goods)",
        "Class 150 (volumetric goods)",
        "Volumetric factor (kg/m³, default 333)",
        "Fuel surcharge rate (%)",
        "Other surcharges (CNY)",
        "Full-truckload unit price (CNY/km·truck)",
        "Single-truck payload (kg)",
        "💡 Chargeable weight = max(actual weight, volume × volumetric factor); LTL base freight = chargeable weight × rate × distance/100; FTL is billed by whole-truck count.",
        "Volumetric factor: 333 kg/m³ is common for road freight, 167 for air freight, 1000 for sea freight",
        "The rate unit is CNY/(kg·100km), selected according to cargo class",
        "In full-truckload mode, billing is based on the number of whole trucks required by the chargeable weight",
        "Actual freight rates are also affected by dedicated-line services, backhaul, transit time, season and other factors",
        "📚 Deep dive: LTL / FTL freight rate and surcharge calculation",
        "Before shipping LTL, take the larger of actual weight and volumetric weight as the chargeable weight, estimate base freight plus fuel surcharge, then quote the customer.",
        "For full-truckload transport, back out how many trucks are needed from the single-truck payload, then multiply by the full-truck unit price and mileage, and compare which of FTL and LTL is cheaper.",
        "Reconcile carrier invoices: enter the fuel surcharge rate and other surcharges from the statement to verify whether the total matches your quote.",
        "LTL quote for 1200 km",
        "Actual weight 800 kg, volume 3 m³, volumetric factor 333 → volumetric weight 999 kg, so the chargeable weight takes the larger value 999 kg. At a Class 85 rate of 0.10 and 1200 km: base freight = 999×0.10×(1200/100) = 1 198.80 CNY; fuel surcharge 15% = 179.82 CNY; other surcharges 200 CNY; total 1 578.62 CNY, which works out to 1.58 CNY/kg. If volume is compressed to 2.4 m³ (volumetric weight 799 kg), the chargeable weight falls back to the actual 800 kg and freight drops to about 1 300 CNY.",
        "Why is the chargeable weight the larger of actual and volumetric weight?",
        "Volumetric goods are bulky but light, so billing by actual weight would leave the carrier short of capacity. Volumetric weight = volume × volumetric factor (167 is common for air freight, 333 for domestic road LTL), and taking the larger value is an industry rule.",
        "How do you choose between LTL and FTL?",
        "LTL is billed by chargeable weight × class rate × mileage/100; FTL is billed by truck count × full-truck unit price × mileage. When the cargo approaches a single-truck payload, FTL is usually cheaper, so compute both once and compare.",
        "About \"Freight Rate Calculation\"",
        "A logistics freight rate calculator that takes the larger of actual weight and volumetric weight as the chargeable weight, combines distance and cargo class to compute base freight, adds fuel and other surcharges to reach total freight cost, and supports both LTL and FTL modes.",
        "Chargeable weight automatically takes the larger value",
        "Rate grading by cargo class",
        "Fuel and other surcharges",
        "Dual LTL / FTL modes",
        "Shipment freight estimation",
        "Logistics quoting and cost accounting",
        "FTL vs LTL selection decisions",
        "Comparing volumetric and heavy goods billing",
    ]))

if __name__ == '__main__':
    main()