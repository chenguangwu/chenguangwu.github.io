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
    write('area-18', build('area-18', [
        "📐 Forest Rights Area Survey",
        "Enter the vertices of the forest parcel polygon (one per line, format x,y) in clockwise or counter-clockwise order to automatically compute the area and perimeter",
        "📖 Read the \"Forest parcel polygon area (shoelace formula) calculation usage guide\"",
        "Vertex coordinates (one per line, format: easting/x, northing/y)",
        "Coordinate unit",
        "Metres (planar coordinates)",
        "Scale factor",
        "💡 Formula: the area uses the shoelace formula S = ½|Σ(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|; the perimeter is the sum of the side lengths. Coordinates are best given as planar coordinates in the same projection system.",
        "At least 3 vertices are needed, joined in order into a closed polygon (the first and last close automatically)",
        "When using GPS latitude and longitude, the earth's curvature makes a small parcel approximately planar, while a large one carries error",
        "The results are for reference only; official forest rights registration is based on field survey",
        "📚 Deep dive: Forest Parcel Polygon Area (Shoelace Formula) Calculation",
        "Measuring the area of an irregular forest boundary",
        "Batch area computation from GPS boundary coordinates",
        "Forest rights confirmation and afforestation planning",
        "By the shoelace formula, A = ½|Σ(x_i·y_{i+1} − x_{i+1}·y_i)| over the vertex sequence (x_i, y_i) of the closed polygon; vertices are entered in clockwise or counter-clockwise order and close automatically, and where necessary the result is multiplied by",
        "the square of the scale",
        "factor.",
        "Vertices (0,0)(100,0)(100,50)(0,50) (in m): A=½|0+5000+5000−0−0−0|=5000 m²=0.75 mu=0.50 ha (scale=1); if the coordinates come from a 1:2000 topographic map, multiply by scale² again.",
        "Does the vertex order affect the result?",
        "It does not affect the absolute value (the formula takes an absolute value), but the vertices must be entered continuously in a single winding direction and closed; clockwise and counter-clockwise differ only in sign, so the area is the same.",
        "Can I use GPS latitude and longitude directly over a large area?",
        "A small parcel can be approximated as planar, but a large area must first be projected into Gauss/UTM planar coordinates, otherwise",
        "the earth's curvature",
        "introduces error; use a spherical polygon formula when necessary.",
        "About \"Forest Rights Area Survey\"",
        "The forest rights area survey tool takes forest parcel polygon vertices and automatically computes the forest land area (hectares/mu/m²) and perimeter, suitable for forest rights registration, land transfer and afforestation planning.",
        "Supports arbitrary polygon vertex coordinate input",
        "Shoelace formula for precise area computation",
        "Outputs hectares, mu and square metres at once",
        "Automatic perimeter and shape factor calculation",
        "Area accounting for forest rights registration",
        "Area confirmation for forest land transfer",
        "Plot measurement for afforestation planning",
        "National forest resource inventory",
        "Scale factor",
    ]))

    write('yield', build('yield', [
        "🔮 Economic Forest Yield Forecast",
        "Enter the planting area, trees per mu, yield per tree and unit price to forecast the total yield and total value of an economic forest",
        "Core formula (by input variable): totalY÷1000; totalN×rate÷100; totalV÷10000",
        "📖 Read the \"Economic forest yield and value forecast usage guide\"",
        "Trees per mu (trees/mu)",
        "Yield per tree (kg)",
        "Unit price (CNY/kg)",
        "Bearing-stage production rate (%)",
        "💡 Formula: total trees = area × trees per mu; effective trees = total trees × production rate; total yield = effective trees × yield per tree; total value = total yield × unit price.",
        "The production rate reflects the share of trees actually carrying fruit, and in the bearing stage it is generally 80%-95%",
        "Yield per tree is affected by tree age, variety and management level, so refer to historical yields",
        "The forecast is for reference only; actual yield is influenced by climate, pests and disease and other factors",
        "📚 Deep dive: Economic Forest Yield and Value Forecast",
        "Revenue estimation for economic forests such as orchards and oil tea",
        "Production rate and effective tree count accounting",
        "Management planning and revenue assessment",
        "Effective producing trees = area × density × production rate; total yield = effective trees × yield per tree; total value = total yield × unit price; yield per mu = total yield ÷ area and value per mu = total value ÷ area. The production rate reflects the share of trees actually carrying fruit (often 80%-95% in the bearing stage).",
        "Economic forest of 100 mu, density 55 trees/mu, 15 kg per tree, unit price 8 CNY/kg, production rate 85%: effective trees = 4675, total yield = 70125 kg (70.1 t), total value = 561,000 CNY, yield per mu ≈ 701 kg and value per mu ≈ 5610 CNY.",
        "How do I estimate the production rate?",
        "It depends on tree age and variety: low in the juvenile and old stages, high in the bearing stage (80%-95%). Refer to historical yields and field surveys, and avoid overestimating revenue by assuming full production.",
        "What if the yield per tree fluctuates a lot?",
        "It is affected by the year (on-year/off-year), management and climate, so take a recent multi-year average and run a sensitivity analysis (±20%) to assess the revenue range.",
        "About \"Economic Forest Yield Forecast\"",
        "The economic forest yield forecast tool takes the planting area, trees per mu, yield per tree and unit price to forecast total yield and total value, suitable for economic forest management planning and revenue estimation.",
        "Supports discounting effective yield by the production rate",
        "Outputs tonnes, CNY and per-mu figures at once",
        "Automatic value per mu calculation",
        "Economic forest management planning",
        "Orchard revenue estimation",
        "Planting investment decisions",
        "Yield target management",
        "Planting area",
        "Trees per mu",
        "Yield per tree",
        "Production rate",
    ]))

    write('density-6', build('density-6', [
        "🚀 Planting Density Optimization",
        "Enter the tree spacing, row spacing, planting area and per-tree seedling cost to compute trees per mu, the total tree count and the planting cost",
        "\"Enter the tree spacing, row spacing, planting area and per-tree seedling cost to compute trees per mu, the total tree count and the planting cost\" runs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Planting tree count and cost estimation usage guide\"",
        "Tree spacing (m)",
        "Row spacing (m)",
        "Planting area (mu)",
        "Cost per seedling (CNY)",
        "💡 Formula: area per tree = tree spacing × row spacing; trees per mu = 666.67 ÷ area per tree; trees per hectare = 10000 ÷ area per tree; total cost = trees per mu × area × cost per tree.",
        "1 mu = 666.67 m², 1 hectare = 15 mu = 10000 m²",
        "Recommended density differs by species: Chinese fir about 110-167 trees/mu, eucalyptus about 80-110 trees/mu",
        "The cost covers seedlings only and excludes site preparation, planting and tending",
        "📚 Deep dive: Planting Tree Count and Cost Estimation",
        "Seedling requirement estimation for planting design",
        "Conversion between spacing and trees per mu",
        "Total planting cost estimation",
        "Trees per mu = 666.67 ÷ (tree spacing × row spacing) in m²; trees per hectare = trees per mu × 15; total trees = trees per mu × area; planting cost = total trees × seedling unit price (1 mu = 666.67 m², 1 hectare = 15 mu).",
        "Tree spacing 2 m, row spacing 3 m, planting 100 mu, 2.5 CNY per seedling: trees per mu = 666.67/(2×3) = 111.1, total trees ≈ 11111, planting cost ≈ 11111×2.5 = 27,800 CNY.",
        "Is the recommended density the same for all species?",
        "No. Chinese fir is about 110-167 trees/mu and eucalyptus about 80-110 trees/mu, so adjust for species characteristics and site: too dense causes competition and too sparse wastes land.",
        "Why add a loss allowance to the real seedling requirement?",
        "Replanting, dead seedlings and grading losses are commonly counted at 5%-10%, and a planning design should include the allowance so seedlings do not run short at planting time.",
        "About \"Planting Density Optimization\"",
        "The planting density optimization tool takes tree spacing, row spacing, planting area and per-tree seedling cost to compute trees per mu, trees per hectare, total trees and planting cost, suitable for planting design and investment budgeting.",
        "Built-in recommended spacing for common species",
        "Outputs density per mu and per hectare at once",
        "Automatic total planting cost calculation",
        "Planting density design",
        "Planting investment budget",
        "Seedling usage planning",
        "Economic forest planning",
        "Tree spacing",
        "Row spacing",
        "Planting area",
        "Cost per tree",
    ]))

    write('forest-volume', build('forest-volume', [
        "🌳 Stand Stock Volume Calculator",
        "Angle-gauge cruising, sample plot method, mean experimental form factor method, multiple methods",
        "\"Angle-gauge cruising, sample plot method, mean experimental form factor method, multiple methods\" runs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Stand stock volume (angle gauge / sample plot / form factor) calculation usage guide\"",
        "📋 Parameter table",
        "📐 Method notes",
        "1. Angle-gauge cruising method:",
        "Stock per hectare = angle-gauge constant × mean height of basal area × form factor",
        "2. Sample plot method:",
        "Stock per hectare = (sample plot stock / sample plot area) × 10000",
        "3. Mean experimental form factor method:",
        "🌲 Reference form factors (fε)",
        "Spruce",
        "📊 Reference stand densities",
        "Stand type",
        "Canopy closure",
        "Stock volume (m³/ha)",
        "Young stand",
        "Middle-aged stand",
        "Near-mature stand",
        "Mature stand",
        "Over-mature stand",
        "📚 Deep dive: Stand Stock Volume (angle gauge / sample plot / form factor) Calculation",
        "Rapid stock estimation with an angle gauge",
        "Stock per hectare by the sample plot method",
        "Harvest volume assessment",
        "Sample plot method: stock per hectare = sample plot stock ÷ sample plot area × 10000. The angle-gauge method derives the basal area per hectare and multiplies it by the form height to get the stock. The mean experimental form factor method uses v = g × tree height × f, summed to give the stock per unit area.",
        "A 600 m² sample plot with 9 m³ measured: stock per hectare = 9/600×10000 = 150 m³/ha; if the angle gauge gives 28 m² of basal area per hectare and a form height of 5.4, the stock is ≈28×5.4=151 m³/ha, and the two methods agree.",
        "Which is more accurate, the angle gauge or the sample plot?",
        "The sample plot is measured directly so it is more accurate but labour-intensive, while the angle gauge is fast but affected by stand uniformity; large-area inventories usually use the angle gauge and key plots use the sample plot for verification.",
        "How do I take the form height?",
        "Form height = stock ÷ basal area. It varies by species and site class, so look it up in the local form height table or a two-entry table; using the wrong form height introduces systematic bias.",
        "About \"Stand Stock Volume Calculator\"",
        "The Stand Stock Volume Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

    write('carbon-sequestration', build('carbon-sequestration', [
        "🌳 Forest Carbon Sink Calculator",
        "Tree biomass, carbon stock, CO₂ equivalent and carbon sink valuation",
        "Core formula (by input variable): carbon×3.667",
        "📖 Read the \"Forest carbon sink estimation usage guide\"",
        "📋 Parameter table",
        "🌳 Calculate the carbon sink",
        "📐 Carbon sink formulas",
        "1. Biomass method:",
        "2. Stock volume expansion method:",
        "δ = biomass expansion factor, ρ = wood density, γ = carbon fraction (0.5)",
        "where: B = biomass (t/ha), V = stock volume (m³/ha), ρ = wood density (t/m³), BEF = biomass expansion factor, CF = carbon fraction (0.5)",
        "💡 Carbon trading reference",
        "2024 CCER carbon price: 50-80 CNY per tonne CO₂",
        "1 tonne of carbon = 3.667 tonnes of CO₂ equivalent",
        "A middle-aged stand sequesters about 0.3-0.8 tonnes of CO₂ per mu per year",
        "📊 Reference parameters by species",
        "Wood density (t/m³)",
        "BEF expansion factor",
        "Carbon fraction",
        "Annual growth (m³/ha)",
        "Oak group (hardwood)",
        "Softwood group",
        "📚 Deep dive: Forest Carbon Sink Estimation",
        "Forestry carbon sink (CCER) project accounting",
        "Stand sequestration and CO₂ equivalent estimation",
        "Carbon sink valuation and trading assessment",
        "Stock volume expansion method: biomass B = V×ρ×BEF (ρ wood density, BEF biomass expansion factor), carbon stock C = B×CF (carbon fraction about 0.5), CO₂ = C×3.667; total CO₂ = CO₂/ha × area, annual = total CO₂ / stand age, and value = total CO₂ × carbon price.",
        "Chinese fir (ρ=0.307, BEF=1.53, CF=0.52) with stock V=120 m³/ha, area 10 ha, stand age 20 years and a carbon price of 60 CNY/t: B=56.4, C=29.3 t/ha, CO₂=107.5 t/ha; total CO₂ ≈ 1075 t, annual ≈ 53.7 t, value ≈ 64,500 CNY.",
        "What carbon price should I use?",
        "Refer to the CCER market of the year; in 2024 it was about 50-80 CNY per tonne of CO₂. Actual transactions follow the agreed price and require third-party verification and credit issuance before they can be traded.",
        "Why take the carbon fraction as 0.5?",
        "The carbon fraction of tree wood usually falls between 0.45 and 0.52, so 0.5 is the common average. Precise accounting should use measured values per species, with the BEF covering the whole-plant biomass of branches, leaves and roots.",
        "About \"Forest Carbon Sink Calculator\"",
        "The Forest Carbon Sink Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

if __name__ == '__main__':
    main()
