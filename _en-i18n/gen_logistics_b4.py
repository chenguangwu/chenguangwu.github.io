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
    write('fuel-calculator', build('fuel-calculator', [
        "💰 Transport Fuel Consumption and Cost",
        "Fuel consumption per 100 km + fuel cost + tolls + depreciation",
        "Core formulas (by input variable): c × (1 + max(0, load - v.load) × 0.02); d × adjFuel ÷ 100; d × 0.5",
        "Transport fuel cost",
        "/ Transport Fuel Consumption",
        "Fuel price (CNY/L)",
        "Tolls (CNY)",
        "Payload (tons)",
        "💰 Compute cost",
        "📚 Deep dive: Transport Fuel Consumption and Combined Cost",
        "Before quoting, estimate fuel cost from mileage, consumption per 100 km and fuel price, then add tolls, depreciation and labor to get the combined cost.",
        "Compare unit cost across vehicle types (CNY per ton-km) to inform in-house versus outsourced decisions.",
        "Assess the cost of overloading: once payload exceeds the vehicle's rated value, consumption is scaled up 2% for each extra ton.",
        "Cost of a medium truck over 600 km",
        "Default medium truck (rated payload 5 t, depreciation 0.5 CNY/km). Mileage 600 km, consumption 20 L per 100 km, fuel price 7.5 CNY/L, tolls 800 CNY, payload 5 t (not overloaded, factor 1.0): consumption 120 L, fuel cost 900 CNY, depreciation 600×0.5=300 CNY, driver 600×0.5=300 CNY, total 2 300 CNY; 3.83 CNY per km, 0.77 CNY per ton-km. If loading 8 t (3 t over): adjusted consumption 20×(1+3×0.02)=21.2 L/100km, consumption 127.2 L, fuel cost 954 CNY, total 2 354 CNY, and cost per ton-km drops to 0.49 CNY.",
        "Which items does the cost include?",
        "Fuel cost (mileage × adjusted consumption ÷ 100 × fuel price) + tolls + vehicle depreciation (mileage × vehicle depreciation factor) + driver cost (mileage × 0.5 CNY/km). Insurance and maintenance are not included and must be added separately.",
        "What happens when the payload exceeds the rated value?",
        "Consumption is scaled by 2% for each extra ton, i.e. adjusted consumption = consumption ×(1 + excess tons × 0.02). This is only a fuel estimate; there are also safety and compliance risks, so overloading is not recommended.",
        "About \"Transport Fuel Cost\"",
        "Transport fuel cost. A logistics and shipping tool that helps compute freight and plan routes.",
    ]))
    write('load-calculator', build('load-calculator', [
        "🧮 Vehicle Loading Calculation",
        "Volume / weight utilization, loadable quantity",
        "Core formulas (by input variable): Math.floor(cap × 1000 ÷ boxWeight); totalWeight ÷ (cap × 1000) × 100; (bL÷100) × (bW÷100) × (bH÷100)",
        "/ Loading Calculation",
        "Cargo box length (m)",
        "Cargo box width (m)",
        "Cargo box height (m)",
        "Payload limit (tons)",
        "Single box size L×W×H (cm)",
        "Single box weight (kg)",
        "🧮 Compute loading",
        "📚 Deep dive: Box Count and Utilization per Vehicle",
        "Before dispatching, estimate how many boxes fit in the cargo box and determine whether volume or payload is the limit, then adjust the vehicle type or packaging accordingly.",
        "Compare loading plans across vehicle types (mini / small / medium / large / semi-trailer) and pick the most cost-effective type.",
        "Reconcile container quantity with the customer, using volume utilization and weight utilization to explain why more cannot be loaded.",
        "Loading 40×30×30 cm cartons into a medium truck",
        "Cargo box 4.2×1.8×1.8 m = 13.608 m³, single box 0.4×0.3×0.3 = 0.036 m³. Theoretical box count = 13.608 ÷ 0.036 = 378; allowing 0.75 for stacking gaps → 283 boxes. With a payload limit of 5 t and 5 kg per box, weight would allow 1 000 boxes, so volume is the limit: 283 boxes actually loaded (1 415 kg). Volume utilization 74.9%, weight utilization 28.3% — there is plenty of payload headroom left, so switch to lighter packaging or a smaller truck.",
        "Why apply a 0.75 factor?",
        "Real loading involves stacking gaps, irregular goods and loading aisles, so the theoretical box count is usually discounted by about a quarter. The tool has this factor built in; if your goods are regular and stack tightly you may estimate upward from the theoretical value.",
        "How do I use the \"limiting factor\" showing volume or weight?",
        "Volume means there is payload headroom left, so you can stack higher or use a larger cargo box; weight means the box is not full but is near the weight limit, so switch to a higher-payload vehicle or reduce the weight per box.",
        "About \"Vehicle Loading Calculation\"",
        "Vehicle loading calculation. A logistics and shipping tool that helps compute freight and plan routes.",
    ]))
    write('package-volume-calc', build('package-volume-calc', [
        "⚖️ Package Volume Calculator",
        "Supports volume and volumetric weight estimation, suitable for logistics quoting.",
        "/ Package Volume Calculator",
        "Volume (cm³) = length × width × height, volume (m³) = cubic centimeters ÷ 1,000,000; volumetric weight (kg) = length × width × height ÷ volumetric divisor (6000 is common for air, 8000 for road express); chargeable weight = max(actual weight, volumetric weight); loading rate = cargo volume ÷ container volume × 100%; for container estimates (20-foot about 33 m³, 40-foot about 67 m³), container load count = container volume ÷ single box outer volume.",
        "Height (cm)",
        "Volumetric divisor (e.g. 5000)",
        "📚 Deep dive: Package Volume and Volumetric Weight Conversion",
        "Before shipping, compute volume and volumetric weight from length × width × height to judge whether billing will use volumetric weight.",
        "Optimize packaging: compare the volumetric weight of different box types and pick the size with the lowest freight.",
        "For a whole batch, add up the dimensions of many items to estimate total volume for booking space or calling a truck.",
        "Volumetric weight of a 50×40×30 cm box",
        "Volume = 50×40×30 = 60 000 cm³ = 0.0600 m³. At a divisor of 6000 the volumetric weight = 60 000 ÷ 6000 = 10.00 kg; at 5000 it is 12.00 kg. If the actual weight is only 8 kg, a carrier using 6000 bills by 10 kg, which is 2 kg more than actual; compressing the height to 24 cm (volume 48 000 cm³) drops the volumetric weight to 8.00 kg, so billing follows actual weight.",
        "What divisor should I enter?",
        "Domestic express commonly uses 6000 or 8000; international express (DHL/UPS/FedEx) mostly 5000; air freight commonly 6000. Defer to the carrier's published rules, since a wrong entry skews the chargeable weight.",
        "What if the volumetric weight exceeds actual weight?",
        "Billing uses the larger value. Compress the package dimensions (especially the height), use vacuum bags, or remove redundant filler to directly lower volumetric weight and freight.",
    ]))
    write('stats-on-time', build('stats-on-time', [
        "📊 KPI (On-Time / Intact) Statistics",
        "On-time / intact",
        "📐 How It Works",
        "Enter total logistics orders, on-time delivered orders and intact delivered orders to automatically compute the on-time rate, the intact rate and the composite KPI, for carrier assessment. Computation happens locally in the browser.",
        "Total orders",
        "On-time delivered orders",
        "Intact delivered orders",
        "📚 Deep dive: Descriptive Statistics for On-Time / Intact KPI",
        "Enter the delay minutes of each waybill and use the mean and",
        "to measure the stability of delivery timeliness.",
        "Enter on-time as 1/0 (1 on time, 0 delayed); the mean is exactly the on-time rate, and multiplying by 100 gives",
        "Record one batch of data before and after an improvement measure and compare the mean and range to verify the effect.",
        "Delay minutes for 10 orders",
        "Input 0,0,15,0,30,5,0,0,45,0:",
        "10, sum 95, mean 9.5 minutes,",
        "0 minutes (6 orders with zero delay), range 45 minutes, standard deviation 15.07 minutes. The mean of 9.5 minutes is pulled up sharply by the two orders at 30 and 45 minutes, while the median of 0 shows most orders were on time — so target the route or time slot of those two orders specifically instead of applying blanket pressure.",
        "How do I use it to compute the on-time rate?",
        "Enter 1 for each on-time waybill and 0 for each delayed one; the mean output is the on-time rate (a mean of 0.94 means 94%). The sample size is the total number of waybills.",
        "What does a large standard deviation indicate?",
        "It means large timeliness fluctuations and unstable service. Use the range to find the worst orders and attribute the cause, which improves customer experience more than simply lowering the average delay.",
        "About \"KPI (On-Time / Intact) Statistics\"",
        "KPI (on-time / intact) statistics. A logistics and shipping tool that helps compute freight and plan routes.",
    ]))

if __name__ == '__main__':
    main()