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
    write('estimate-yield', build('estimate-yield', [
        "Biogas yield estimator",
        "Enter manure type, daily output, total solids TS (%) and hydraulic retention time HRT to estimate daily biogas, methane, power potential and reactor volume.",
        "Core formula (by inputs): slurryVol\u00d7max(hrt,0); biogas\u00d7p.ch4\u00f7100; qty\u00d7max(ts,0)\u00f7100",
        'View "Biogas yield estimator" guide',
        "Manure type",
        "Pig manure",
        "Cattle manure",
        "Chicken manure",
        "Daily output (kg/d)",
        "Total solids TS (%)",
        "Hydraulic retention time HRT (d)",
        "Daily biogas = daily output \u00d7 TS% \u00d7 gas yield (m\u00b3/kg TS); methane = biogas \u00d7 CH4 content; power = methane volume \u00d7 9.97 kWh/m\u00b3 \u00d7 efficiency (35%); reactor volume = daily slurry volume \u00d7 HRT.",
        "Common manure biogas-yield reference",
        "Gas yield is a mesophilic (~35\u00b0C) anaerobic-fermentation typical value; real values vary with temperature, inoculum and C/N ratio",
        "Reactor volume uses slurry density \u2248 water (1000 kg/m\u00b3); in practice account for solids and expansion",
        "Deep dive: Manure biogas and power potential",
        "From manure amount and total solids estimate daily biogas and power.",
        "Biogas-plant scale and reactor-volume estimation.",
        "Manure-to-energy revenue assessment.",
        "Pig manure 1000 kg/d, TS 20%",
        "TS=200 kg/d, yield 0.6 \u2192 biogas 120 m\u00b3/d, CH4 72 m\u00b3/d, power 72\u00d79.97\u00d70.35\u2248250 kWh/d (\u224891,000 kWh/year).",
        "Larger scale",
        "Manure 5000 kg/d: biogas 600 m\u00b3/d, power \u22481250 kWh/d.",
        "What is the gas yield?",
        "Pig/cattle TS yield ~0.4\u20130.6 m\u00b3/kg, affected by temperature and retention.",
        "What is power efficiency?",
        "Biogas generator efficiency ~0.3\u20130.4, CH4 heating value ~9.97 kWh/m\u00b3.",
        'About "Biogas yield estimator"',
        "For estimating livestock-manure biogas-plant gas output. Enter manure type, daily output, total solids TS and retention time HRT to estimate daily biogas, methane, annual power potential and reactor effective volume, with a common manure yield reference table.",
        "Supports pig / cattle / chicken manure",
        "Estimate power and reactor volume",
        "Includes gas-yield reference table",
        "Biogas-plant planning for large farms",
        "Rural household biogas-pit yield estimate",
        "Biomass energy feasibility analysis",
        "Manure resource-utilization assessment",
        "Daily output",
        "Total solids TS",
        "Hydraulic retention time",
    ]))
    write('fattening-pig-timeline', build('fattening-pig-timeline', [
        "Finishing-pig market-date predictor",
        "From current weight, target weight and daily gain, predict market date and feed use",
        "Core formula (by inputs): new Date(startDate.getTime() + daysNeeded \u00d7 86400000); new Date(startDate.getTime() + mDays \u00d7 86400000); Math.ceil(cw \u00f7 step) \u00d7 step + step",
        'View "Finishing-pig market-date predictor" guide',
        "Target market weight (kg)",
        "Average daily gain ADG (g/day)",
        "Current-stage FCR (feed conversion)",
        "Finishing-pig stage reference metrics",
        "\u2022 Nursery (7\u201325 kg): ADG 400\u2013550 g, FCR 1.5\u20131.8",
        "\u2022 Early growth (25\u201350 kg): ADG 600\u2013800 g, FCR 2.2\u20132.5",
        "\u2022 Late growth (50\u201380 kg): ADG 800\u2013950 g, FCR 2.6\u20133.0",
        "\u2022 Finishing (80\u2013120 kg): ADG 850\u20131000 g, FCR 3.0\u20133.5",
        "Breed, sex and season strongly affect ADG. Summer heat may cut ADG 10\u201320%. Adjust forecast parameters by measured data.",
        "Deep dive: Finishing-pig market timeline",
        "From current/target weight and ADG estimate days to market.",
        "Estimate feed use and feed cost.",
        "Schedule milestone-weight dates.",
        "30\u2192120 kg, daily gain 800 g",
        "Gain 90 kg, days=90/0.8\u2248113; feed=90\u00d73.0=270 kg, cost=270\u00d73.2=864 yuan.",
        "Higher daily gain",
        "ADG 800\u2192950 g: market in ~95 days, cost down ~12%.",
        "FCR effect?",
        "Lower feed-gain ratio means less feed per gain, directly cutting cost.",
        "Starting weight?",
        "Nursery ends ~25\u201330 kg into finishing, market at 110\u2013120 kg.",
        'About "Finishing-pig market-date predictor"',
        "The Finishing-pig market-date predictor is a general-purpose online tool. " + DISCL,
    ]))
    write('feed-conversion-ratio', build('feed-conversion-ratio', [
        "Feed conversion ratio (FCR) and daily gain calculator",
        "Compute feed conversion ratio (FCR), average daily gain (ADG) and feed cost to assess farming efficiency",
        "Compute feed conversion ratio (FCR), average daily gain (ADG) and feed cost to assess farming efficiency, and output results from inputs.",
        'View "Feed conversion ratio (FCR) and daily gain calculator" guide',
        "Basic calculation",
        "Cost analysis",
        "Final weight (kg)",
        "Total gain (kg)",
        "Live pig price (yuan/kg)",
        "Common livestock FCR reference ranges",
        "\u2022 Finishing pig (30\u2013100 kg): FCR 2.4\u20133.0",
        "\u2022 Broiler: FCR 1.5\u20131.8",
        "\u2022 Beef cattle: FCR 6.0\u20138.0",
        "\u2022 Layer rearing: FCR 3.5\u20134.5",
        "\u2022 Meat duck: FCR 2.0\u20132.5",
        "Lower FCR means higher feed efficiency. Higher ADG means faster growth. In practice judge with breed, health and temperature.",
        "Deep dive: Feed-gain ratio (FCR)",
        "From total feed and gain compute feed-gain ratio and ADG.",
        "Farming profit and feed-cost assessment.",
        "Benchmark FCR across batches.",
        "20\u2192100 kg, feed 300 kg",
        "Gain 80 kg, FCR=300/80=3.75, ADG=80/120=0.67 kg/d.",
        "After optimization",
        "FCR 3.75\u21923.2: same gain saves 44 kg feed (~14.7%).",
        "Is lower FCR always better?",
        "Yes, smaller FCR means high efficiency and low cost, but balance health.",
        "Broiler vs pig difference?",
        "Broiler ~1.5\u20131.8, pig ~2.8\u20133.5, ruminants higher.",
        'About "Feed conversion ratio (FCR) and daily gain calculator"',
        "Feed conversion ratio (FCR) and daily gain calculator. " + DISCL,
        "How to use the FCR and daily-gain calculator",
        "What does the FCR and daily-gain calculator do?",
        "How do you use the FCR and daily-gain calculator?",
        "Which scenarios suit the FCR and daily-gain calculator?",
    ]))
    write('heat-stress-index', build('heat-stress-index', [
        "Heat stress index (THI) early-warning tool",
        "From temperature and humidity compute the temperature-humidity index (THI) and assess livestock heat-stress risk level",
        "Core formula (by inputs): (1.8 \u00d7 T + 32) - (0.55 - 0.0055 \u00d7 RH) \u00d7 (1.8 \u00d7 T - 26); (adjustedThi - 68) \u00d7 0.2",
        'View "Heat stress index (THI) early-warning tool" guide',
        "Wind speed (m/s, optional)",
        "THI level reference",
        "Dairy cow impact",
        "Pig impact",
        "No stress",
        "Mild",
        "Mild stress begins",
        "Slight feed drop",
        "Milk yield down 10\u201315%",
        "Reproduction declines",
        "Milk yield down 20\u201330%",
        "Severe panting",
        "Possible death",
        "Heat-stress death risk",
        "THI = (1.8\u00d7T + 32) - (0.55 - 0.0055\u00d7RH) \u00d7 (1.8\u00d7T - 26), T is temperature (\u00b0C), RH is relative humidity (%). Wind lowers apparent temperature; each 1 m/s reduces THI by about 2\u20134 points.",
        "Deep dive: Temperature-humidity index (THI)",
        "From temperature and humidity compute THI to grade heat stress.",
        "Dairy/poultry heat stress and milk/egg loss.",
        "Wind-corrected effective THI.",
        "Dairy cow 30\u00b0C/60% RH",
        "THI=(1.8\u00d730+32)\u2212(0.55\u22120.0055\u00d760)(1.8\u00d730\u221226)=86\u22120.22\u00d728\u224879.8; >68 severe; wind 2 m/s corrected \u224875.",
        "Mild weather",
        "25\u00b0C/60%RH: THI\u224873, still moderate, milk already dropping.",
        "Dairy cow threshold?",
        "THI>68 milk drops, >72 feeding and reproduction clearly hurt.",
        "Wind effect?",
        "Wind boosts convective cooling, lowering effective THI by a coefficient.",
        'About "Heat stress index (THI) early-warning tool"',
        "Heat stress index (THI) early-warning tool. " + DISCL,
        "Is this tool free?",
        "Completely free, no registration, use directly in the browser.",
        "Will my data be uploaded?",
        "No. All processing is done locally in your browser; data is never sent to any server.",
        "Does it support mobile?",
        "Yes. The page is responsive; both phone and computer work.",
        "How to use the THI early-warning tool",
        "What does the THI early-warning tool do?",
        "Enter temperature, relative humidity and animal type (optionally wind speed) to compute THI, grade it as normal/alert/danger/emergency, for summer barn cooling and ventilation scheduling.",
        "How do you use the THI early-warning tool?",
        "Which scenarios suit the THI early-warning tool?",
    ]))
    write('inbreeding-coefficient', build('inbreeding-coefficient', [
        "Population inbreeding coefficient estimator",
        "Estimate an individual's inbreeding coefficient from pedigree relations and assess population genetic diversity",
        "Estimate an individual's inbreeding coefficient from pedigree relations and assess population genetic diversity, and output results from inputs.",
        'View "Population inbreeding coefficient estimator" guide',
        "Quick estimate",
        "Pedigree path method",
        "Estimate from population parameters",
        "Effective population size (Ne)",
        "Number of generations",
        "Compute by pedigree path",
        "Enter the common ancestor of the individual's sire and dam, and each one's generations to that ancestor",
        "Common ancestor's inbreeding (Fa)",
        "Sire-to-ancestor generations (n1)",
        "Dam-to-ancestor generations (n2)",
        "Number of common ancestors",
        "Inbreeding coefficient reference",
        "Inbreeding coefficient",
        "Low inbreeding, low genetic risk",
        "Mild inbreeding, watch",
        "Moderate inbreeding, possible depression",
        "High inbreeding, high depression risk",
        "Common inbreeding correspondences",
        "\u2022 Full-sib mating offspring: F = 25%",
        "\u2022 Half-sib mating offspring: F = 12.5%",
        "\u2022 Parent-offspring mating offspring: F = 25%",
        "\u2022 Cousin mating offspring: F = 6.25%",
        "Excess inbreeding causes depression: lower fertility, slower growth, weaker disease resistance, more defects. Keep effective size Ne \u2265 50 and F < 6.25%; conservation herds Ne \u2265 100.",
        "Deep dive: Population inbreeding coefficient",
        "From effective size Ne and generations compute cumulative F.",
        "Conservation and breeding planning to avoid depression.",
        "Single-ancestor contribution method for a specific individual's F.",
        "Ne=50 over 5 generations",
        "\u0394F=1/(2\u00d750)=1%, F=1\u2212(1\u22120.01)^5\u22484.9%; genetic diversity remaining 95.1%.",
        "Smaller Ne",
        "Ne 50\u219225: \u0394F=2%, 5-gen F\u22489.6%, depression risk doubles.",
        "What is \u0394F?",
        "Inbreeding increment per generation; smaller keeps diversity better.",
        "Ne target?",
        "Conservation often requires \u0394F\u22641% (Ne\u226550); commercial herds may relax.",
        'About "Population inbreeding coefficient estimator"',
        "The Population inbreeding coefficient estimator is a general-purpose online tool. " + DISCL,
        "How to use the population inbreeding estimator",
        "What does the population inbreeding estimator do?",
        "Enter the common ancestor of an individual's sire and dam and each one's generations to it, to estimate that offspring's inbreeding coefficient and assess population diversity and inbreeding-depression risk.",
        "How do you use the population inbreeding estimator?",
        "Which scenarios suit the population inbreeding estimator?",
    ]))

if __name__ == "__main__":
    main()
