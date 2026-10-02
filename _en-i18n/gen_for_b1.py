#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'forestry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'forestry')
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
    out = {'slug': slug, 'industry': 'forestry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('forest-area', build('forest-area', [
        "📐 Forest Land Area Calculator",
        "Multiple land parcel shapes, GPS coordinates, slope-to-flat projection, and mu/hectare/square metre conversion",
        "Core formula (by input variable): Math.cos(slope×π÷180); Sflat÷10000; Sflat÷1000000",
        "📖 Read the \"Forest Land Area (mu/hectare) conversion and slope-to-flat usage guide\"",
        "📋 Conversion table",
        "Parcel shape",
        "Slope (degrees)",
        "Slope aspect",
        "Flat ground",
        "Sunny slope",
        "Shady slope",
        "Half-sunny / half-shady",
        "📐 Calculated area",
        "📐 Area formulas",
        "Rectangle:",
        "S = length × width",
        "Triangle:",
        "S = (base × height) / 2",
        "Trapezoid:",
        "S = (top base + bottom base) × height / 2",
        "Circle:",
        "Polygon (GPS):",
        "Shoelace formula",
        "Slope to flat:",
        "Flat area = sloped area × cos(slope)",
        "📏 Unit conversion",
        "1 hectare (ha) = 15 mu = 10000 m²",
        "1 mu = 666.67 m² = 60 square zhang",
        "1 km² = 100 hectares = 1500 mu",
        "1 acre = 0.4047 hectare = 6.07 mu",
        "📊 Slope and site conditions",
        "Flat area coefficient",
        "Soil and water conservation",
        "Suitable use",
        "Flat slope",
        "Good",
        "Farming / forestry / fruit",
        "Gentle slope",
        "Forestry / fruit / farming",
        "Steep slope",
        "Forest land / economic forest",
        "Very steep slope",
        "Ecological forest / closed",
        "Very steep slope",
        "Closed for protection",
        "📚 Deep dive: Forest Land Area (mu/hectare) conversion and slope-to-flat",
        "Forest land rights confirmation",
        "Area calculation",
        "Projecting sloped surface area to flat",
        "mu/hectare/m² conversion",
        "Area by shape (rectangle a×b, triangle a×h/2, trapezoid (a+b)×h/2, circle πr²); for sloped ground flat area = sloped area × cos(slope). Convert between mu (666.67 m²), hectares (10000 m² = 15 mu) and square metres.",
        "Rectangular forest land 100 m × 60 m: sloped area = 6000 m²; at a slope of 0° the flat area is 6000 m² = 9.0 mu = 0.60 ha; at a slope of 30° the flat area is 6000×cos30° ≈ 5196 m² = 7.79 mu.",
        "Why use the flat area on sloped ground?",
        "Forest land rights confirmation and stock volume are both calculated on the horizontal projected area; on a steep slope the surface area is significantly larger than the projection, so using the sloped area directly overestimates both the area and the resource volume.",
        "How many mu is one hectare?",
        "1 hectare = 10000 m² = 15 mu, and 1 mu ≈ 666.67 m²; mountain areas commonly use mu while resource surveys use hectares, so keep the units consistent.",
        "About \"Forest Land Area Calculator\"",
        "The Forest Land Area Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

    write('planting-density', build('planting-density', [
        "🧮 Planting Density Calculator",
        "Planting density calculation and recommendation across tree species, site conditions and spacing configurations",
        "\"Planting density calculation and recommendation across tree species, site conditions and spacing configurations\" runs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Planting density and seedling requirement calculation usage guide\"",
        "📋 Reference densities",
        "Tree spacing (m)",
        "Row spacing (m)",
        "Planting area (mu)",
        "Site condition",
        "Good (Class I land)",
        "Medium (Class II land)",
        "Poor (Class III land)",
        "Include 10% loss for replanting",
        "Rectangular layout",
        "Trees per unit area = 666.67 ÷ (tree spacing × row spacing)",
        "Note: 1 mu = 666.67 m²",
        "🌳 Layout options",
        "Square",
        ": tree spacing equals row spacing, giving even distribution and balanced crown development",
        "Rectangular",
        ": row spacing exceeds tree spacing, easing mechanized work and improving ventilation and light",
        ": a staggered arrangement that uses space fully at a higher density",
        "📋 Principles for setting planting density",
        "Species characteristics: light-demanding species are planted sparsely, shade-tolerant species densely",
        "Site condition: good land sparsely planted, poor land densely planted",
        "Management purpose: timber plantations sparsely, economic and protective forests densely",
        "Rotation length: short rotation densely, long rotation sparsely",
        "🌲 Reference planting densities for major species",
        "Tree spacing × row spacing (m)",
        "Density (trees/mu)",
        "Timber forest",
        "Timber/paper",
        "Fast-growing timber",
        "Economic forest",
        "Fruit economic forest",
        "Chestnut",
        "Mao bamboo",
        "Dual-purpose bamboo and shoot",
        "📚 Deep dive: Planting Density and Seedling Requirement Calculation",
        "Recommended density by species suitability",
        "Spacing and seedling requirement estimation",
        "Density adjustment by site condition",
        "Trees per mu = 666.67 ÷ (tree spacing × row spacing); seedling requirement = trees per mu × area, and with 10% loss you add ceil(requirement × 0.1). Suitable density is recommended from the baseline density of the species combined with the site condition (good land sparse, poor land dense).",
        "Tree spacing 2 m, row spacing 3 m, planting 100 mu: 666.67/6 = 111.1 trees per mu, so about 11111 seedlings net, or about 12223 including 10% loss; on good site land you can lower it to the recommended density.",
        "Why sparsely plant on good land?",
        "On good land each tree grows fast with a large crown, so an overly dense stand leads to intense competition and severe differentiation; sparse planting favors individual development and wood quality, while poor land relies on dense planting to hold yield.",
        "Is the loss rate always 10%?",
        "No. It depends on seedling quality, transport distance, season and replanting requirements, and usually runs 5%-10%; precious species or long hauls may need a bit more, so adjust based on reality.",
        "About \"Planting Density Calculator\"",
        "The Planting Density Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

    write('tree-age', build('tree-age', [
        "🔮 Tree Age Estimator",
        "Annual ring method, increment borer method, breast diameter regression method, multi-method age estimation",
        "Core formula (by input variable): Math.round(dbh÷(g×0.7)×adj+seed); Math.round(dbh÷(g×1.3)×adj+seed); Math.round(dbh÷g×adj+seed)",
        "📖 Read the \"Tree age (annual ring / increment borer / diameter regression) estimation usage guide\"",
        "🔮 Estimate",
        "📋 Parameter table",
        "Mean annual breast diameter growth (cm)",
        "Planting seedling age (years)",
        "Adjust for site condition",
        "🔮 Estimate tree age",
        "📐 Tree age estimation methods",
        "1. Breast diameter growth method:",
        "Tree age = (breast diameter / mean annual growth) + seedling age",
        "2. Annual ring method (most accurate):",
        "directly count the rings on a felled stump or an increment borer core",
        "3. Branch whorl method (conifers):",
        "count the number of whorls of branches, one whorl per year",
        "4. Check the planting records:",
        "in plantations the exact age comes from the planting records",
        "⚠️ Note",
        ": naturally grown trees are affected by site conditions, competition and climate, so estimates carry a ±10-20% error. For ancient and notable trees a professional increment borer measurement is recommended.",
        "🌲 Mean annual breast diameter growth of common species (cm)",
        "Middle age",
        "Reference rotation",
        "20-30 years",
        "10-15 years",
        "30-50 years",
        "5-15 years",
        "50-80 years",
        "Camphor tree",
        "40-60 years",
        "📚 Deep dive: Tree Age (annual ring / increment borer / diameter regression) estimation",
        "Age appraisal of ancient and notable trees",
        "Tree age in forest asset valuation",
        "Back-calculating age from growth rate",
        "Diameter regression method: age ≈ diameter ÷ mean annual breast diameter growth + seedling age (with a site factor adj; on good land adj≈1.15). The annual ring method is the most accurate; the increment borer takes a core and counts rings for non-destructive estimation. The range is given from the upper and lower growth-rate bounds",
        "Breast diameter 20 cm, mean annual breast diameter growth 0.8 cm, seedling age 2 years, no site adjustment: central age = 20/0.8+2 = 27 years, and with a growth-rate range of 0.7-1.3 times the range is about 21-38 years. The annual ring method takes the actual ring count as authoritative.",
        "Is the diameter regression method accurate?",
        "It is rough. It is strongly affected by species, density and site, so treat it as a quick estimate;",
        "an exact age",
        "requires cutting the trunk to count rings or taking a core with an increment borer, and for ancient trees the latter is recommended.",
        "How do I choose the site factor?",
        "On good land growth is fast so the same diameter means a younger age (adj>1 makes the estimate smaller), and on poor land the opposite applies; determine it from the local growth process table or experience to avoid systematic bias.",
        "About \"Tree Age Estimator\"",
        "The Tree Age Estimator is an online tool for forestry resources. It is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

if __name__ == '__main__':
    main()
