#!/usr/bin/env python3
# gen_livestock_head.py — shared head for livestock batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'livestock')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'livestock')
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
    out = {'slug': slug, 'industry': 'livestock', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('manure-amount', build('manure-amount', [
        "Manure handling-volume estimator",
        "Estimate livestock manure output, dry matter and storage-facility capacity needs",
        "Core formula (by inputs): totalManure \u00d7 collectRate \u00f7 100; 1000 - (100 - moisture) \u00d7 2; totalDM \u00d7 nContent \u00f7 1000",
        'View "Manure handling-volume estimator" guide',
        "Manure moisture (%)",
        "Per-head daily manure (kg/day, optional)",
        "Manure collection rate (%)",
        "Manure output reference by animal",
        "Daily output (kg/head)",
        "Dry matter (%)",
        "Dairy cow (500 kg)",
        "Beef cattle (400 kg)",
        "Finishing pig (80 kg)",
        "Sow (200 kg)",
        "Layer (2 kg)",
        "Broiler (2 kg)",
        "Sheep (50 kg)",
        "Actual output depends on feed, intake, water and temperature. Moisture directly drives storage design; solid-liquid separation greatly cuts liquid to handle.",
        "Deep dive: Manure generation estimation",
        "From head count and daily excretion estimate total manure and dry matter.",
        "Manure nutrient (N/P/K) accounting.",
        "Input for cleaning and storage design.",
        "100 pigs, 30 days",
        "Excretion 2 kg/head \u2192 200 kg/day, 30 days 6 tonnes; 90% collected = 5.4 t, 80% moisture gives dry matter 1.08 t; volume \u22485.6 m\u00b3.",
        "Nutrients",
        "Dry matter 1.08 t (N 5%): contains about 54 kg N equivalent.",
        "What is daily excretion?",
        "Pig ~2, cattle ~20\u201330, poultry ~0.1\u20130.15 kg/head\u00b7day, varying with weight and feed.",
        "What is dry matter?",
        "Manure moisture ~75%\u201385%, dry-matter rate = 1 \u2212 moisture.",
        'About "Manure handling-volume estimator"',
        "The Manure handling-volume estimator is a general-purpose online tool. " + DISCL,
        "Leave 0 to use the default value",
    ]))
    write('manure-pit-capacity', build('manure-pit-capacity', [
        "Barn cleaning frequency and manure-pit capacity calculator",
        "Compute cleaning cycle, required pit capacity and recommended cleaning frequency",
        "Core formula (by inputs): 1000 - (100 - moisture) \u00d7 2; \u221apitArea",
        'View "Barn cleaning frequency and manure-pit capacity calculator" guide',
        "Per-head daily manure (kg/day)",
        "Manure moisture (%)",
        "Cleaning cycle (days)",
        "Pit safety factor",
        "1.1 (10% margin)",
        "1.2 (20% margin)",
        "1.3 (30% margin)",
        "1.5 (50% margin)",
        "Pit depth (m)",
        "Storage-period target (days)",
        "Cleaning-management reference",
        "Recommended cleaning frequency",
        "\u2022 Dairy barn: 1\u20132 times/day (scraper/flush)",
        "\u2022 Finishing-pig barn: 1\u20132 times/day (slatted floor may extend to 2\u20133 days)",
        "\u2022 Sow barn: once/day (reduce ammonia, prevent disease)",
        "\u2022 Layer barn: once/day (belt cleaning)",
        "\u2022 Broiler barn: one-time cleanup after marketing (floor)",
        "Pit design points",
        "\u2022 Pit capacity should cover at least 90\u2013180 days of storage",
        "\u2022 Leak-proof: bottom and walls need impermeable treatment",
        "\u2022 Overflow and vent pipes to prevent overflow and biogas buildup",
        "\u2022 Separate rain and sewage to cut liquid to handle",
        "Pits are environmental facilities; construction must meet local livestock-pollution rules. Late cleaning raises ammonia and H2S, hurting health and performance.",
        "Deep dive: Manure-pit volume",
        "From head count, cleaning cycle or storage days compute pit volume.",
        "Effective volume and base area with safety margin.",
        "Cleaning-frequency advice.",
        "100 head, store 180 days",
        "200 kg/day, 180 days 36 t, density 960: volume 37.5 m\u00b3\u00d71.2 = 45 m\u00b3; depth 2 m \u2192 base area 22.5 m\u00b2 (~4.7\u00d74.7 m).",
        "Shorter storage",
        "180\u219290 days: volume halves to about 22.5 m\u00b3.",
        "What safety margin?",
        "Usually 1.1\u20131.2 against overflow and settling.",
        "What cleaning frequency?",
        "Daily cleaning: small pit, high mechanical cost; long cycle: large pit, more land.",
        'About "Barn cleaning frequency and manure-pit capacity calculator"',
        "Barn cleaning frequency and manure-pit capacity calculator. " + DISCL,
    ]))
    write('milk-yield-scc', build('milk-yield-scc', [
        "Dairy milk yield and somatic cell count trend analyzer",
        "Enter multi-day measurements to analyze milk-yield trend and somatic cell count (SCC) change, assessing udder health",
        'View "Dairy milk yield and somatic cell count trend analyzer" guide',
        "Daily milk = period total milk (kg) \u00f7 days; trend slope is the linear-regression slope of daily data (positive up, negative down); SCC grades: \u2264200k/mL normal, 200k\u2013500k watch, 500k\u20131M subclinical mastitis, >1M clinical risk; low fat/protein ratio hints at rumen acidosis, and SCC up 100k/mL cuts yield about 2%\u20133%.",
        "Enter measurement data",
        "+ Add a record",
        "Delete the last one",
        "Analyze trend",
        "Milk yield trend",
        "SCC trend",
        "SCC reference standard",
        "SCC (10k/mL)",
        "Udder healthy, no inflammation",
        "Basically normal, watch",
        "Subclinical mastitis risk",
        "Clinical/subclinical mastitis, treat",
        "SCC is the core udder-health metric. Rising SCC usually signals mastitis and lowers yield; generally SCC up 100k/mL cuts daily yield about 0.7\u20131.5 kg.",
        "Deep dive: Milk yield and SCC trend",
        "From milk and SCC records analyze trend and milk loss.",
        "Subclinical mastitis monitoring.",
        "Linear-fit yield/SCC slope.",
        "Avg yield 28 kg, SCC 250k",
        "Baseline SCC 200k: loss=(25\u221220)/10=0.5 kg/day\u00b7head; SCC up means yield down and quality worse.",
        "SCC trend rising",
        "Slope >5/day: signals subclinical mastitis spreading; isolate and treat.",
        "What does SCC mean?",
        "SCC reflects mammary health; higher means worse inflammation and quality.",
        "What is the baseline?",
        "Healthy cows mostly <200k/mL; above that yield and components clearly drop.",
        'About "Dairy milk yield and somatic cell count trend analyzer"',
        "Dairy milk yield and somatic cell count trend analyzer. " + DISCL,
    ]))
    write('mycotoxin-limit', build('mycotoxin-limit', [
        "Feed mycotoxin limit comparator",
        "Compare against national mycotoxin limits, assess feed safety and give risk hints",
        'View "Feed mycotoxin limit comparator" guide',
        "Mycotoxin type",
        "Aflatoxin B1",
        "Deoxynivalenol (DON / vomitoxin)",
        "Zearalenone (ZEN)",
        "Ochratoxin A",
        "Fumonisins (FB1+FB2)",
        "T-2 toxin",
        "Measured content (\u00b5g/kg)",
        "Feed category",
        "Piglet compound feed",
        "Growing-finishing pig compound feed",
        "Sow compound feed",
        "Layer compound feed",
        "Broiler compound feed",
        "Calf compound feed",
        "Dairy concentrate supplement",
        "Beef concentrate supplement",
        "Raw material (corn/wheat etc.)",
        "Full-limit standard comparison table",
        "Limits follow GB 13078 Feed Hygiene Standard. Mycotoxins are synergistic; even if each is within limit, co-occurrence can still harm. Test regularly, use binders and control storage.",
        "Deep dive: Mycotoxin limit comparison",
        "Look up limits by species/toxin per GB 13078.",
        "Judge the exceedance multiple of measured values.",
        "Output a side-by-side multi-toxin limit table.",
        "Pig feed AFB1 measured 80",
        "Pig compound feed AFB1 limit 50 \u00b5g/kg: 80/50 = 1.6\u00d7 over, fails.",
        "ZEN piglet",
        "Piglet feed ZEN limit stricter (e.g., 100), measured 150 fails and must be handled.",
        "How are limits tiered?",
        "Tiered by animal sensitivity (young/breeding strictest) and toxin type.",
        "Consequence of exceeding?",
        "Over-limit feed is banned; return or detoxify.",
        'About "Feed mycotoxin limit comparator"',
        "Feed mycotoxin limit comparator. " + DISCL,
    ]))
    write('poultry-light-program', build('poultry-light-program', [
        "Poultry house lighting program designer",
        "Generate a scientific lighting program by breed type and age, with duration and intensity advice",
        'View "Poultry house lighting program designer" guide',
        "Breed type",
        "Layer (egg)",
        "Broiler (meat)",
        "Parent stock (layer)",
        "Meat parent stock",
        "Current age (days)",
        "Housing method",
        "Closed house",
        "Open / semi-open house",
        "Target weight / lay stage",
        "Auto-match by age",
        "Brooding",
        "Growing",
        "Laying",
        "Lighting management points",
        "\u2022 First 3 days brooding: 23\u201324 h bright light, promote feeding/drinking",
        "\u2022 Growing: constant or decreasing light, prevent early maturity",
        "\u2022 Laying: constant 16 h, do not reduce freely",
        "\u2022 Intensity: brooding 30\u201340 lux, growing 5\u201310 lux, laying 15\u201320 lux",
        "\u2022 Light-length change matters more than absolute length for maturity",
        "\u2022 During laying, light can only increase, not decrease; so can intensity",
        "\u2022 Open houses need supplemental artificial light over natural",
        "\u2022 Use warm-white LED bulbs, color temperature 2700\u20133000 K",
        "This is a general reference; adjust flexibly by breed manual, season and flock development.",
        "Deep dive: Poultry lighting program",
        "By breed (layer/broiler/parent) and age give light duration.",
        "Closed house add light to target duration.",
        "Laying-period light-stimulation plan.",
        "Layer laying period",
        "Laying: constant 16 h (closed house natural 12 h needs +4 h) to promote ovulation.",
        "Early 23 h promotes intake; later drop to 18\u201320 h to balance growth.",
        "Why control light?",
        "Photoperiod controls maturity and laying; too long/short hurts yield and health.",
        "Open house?",
        "Natural light varies by season; add artificial to reach target duration.",
        'About "Poultry house lighting program designer"',
        "The Poultry house lighting program designer is a general-purpose online tool. " + DISCL,
    ]))

if __name__ == "__main__":
    main()
