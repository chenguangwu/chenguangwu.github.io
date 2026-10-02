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
    write('tree-volume', build('tree-volume', [
        "⚖️ Single Standing Tree Volume Calculator",
        "One-entry and two-entry volume tables, experimental form factor method, top height method, comparison of multiple formulas",
        "\"One-entry and two-entry volume tables, experimental form factor method, top height method, comparison of multiple formulas\" runs a professional calculation from the input parameters and outputs the result.",
        "📖 Read the \"Single standing tree volume (two-entry / form factor) calculation usage guide\"",
        "📋 Volume table",
        "Form factor",
        "Number of trees",
        "⚖️ Calculate volume",
        "📐 Standing tree volume formulas",
        "1. Two-entry volume formula:",
        "V = aDbHc (requires breast diameter D and tree height H)",
        "2. One-entry volume formula:",
        "V = aDb (needs only breast diameter D)",
        "3. Experimental form factor method:",
        "4. Mean form factor method:",
        "g1.3 = π/4 × D² (basal area at breast height)",
        "📋 Chinese fir two-entry volume table (m³)",
        "Breast diameter\\Tree height",
        "📚 Deep dive: Single Standing Tree Volume (two-entry / form factor) Calculation",
        "Single-tree volume and output estimation",
        "Comparing results across multiple formulas",
        "Forest asset valuation",
        "Two-entry volume V=a·D^b·H^c (for example 0.00005877·D^1.963·H^0.859); the experimental form factor method gives V=g₁.₃×(H+3)×fε; the mean form factor method gives V=g₁.₃×H×f₁.₃ (g₁.₃=πD²/4/10000). When comparing formulas, take the conservative value.",
        "Breast diameter 20 cm, tree height 14 m: two-entry volume = 0.00005877×20^1.963×14^0.859 ≈ 0.2033 m³; the experimental form factor method (f=0.42) gives ≈0.2243 m³. The two are close, with a single-tree output of about 0.20 m³.",
        "Which formula is the most accurate?",
        "The (local) two-entry volume table is the most accurate while the form factor method is an approximation; a universal form factor across species and regions introduces bias, so important assessments should use the local two-entry table.",
        "Why does the experimental form factor use H+3?",
        "The form factor method approximates the trunk as extended to the top (adding 3 m to represent the top of the bole), and the experimental form factor fε already contains this correction, so a measured bole without the top can still approximate the whole-tree volume.",
        "About \"Single Standing Tree Volume Calculator\"",
        "The Single Standing Tree Volume Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

    write('calc-57', build('calc-57', [
        "🌳 Forest Canopy Closure Calculation",
        "Enter the total number of sample points and the number covered by tree crowns to compute the stand canopy closure and determine the closure class (point-sampling method)",
        "📖 Read the \"Canopy closure (point-sampling method) estimation usage guide\"",
        "Canopy closure = points covered by tree crowns ÷ total sample points",
        "Total sample points",
        "Sample points covered by tree crowns",
        "💡 Formula: canopy closure = points covered by tree crowns ÷ total sample points. The classes follow the national continuous forest inventory standards.",
        "Point-sampling method: lay out sample points systematically in the plot, look up vertically and judge whether the point is shaded by a crown",
        "Canopy closure runs from 0 to 1 and keeps two decimal places; the covered point count should not exceed the total",
        "The results are for reference only; official surveys follow the professional protocols",
        "📚 Deep dive: Canopy Closure (point-sampling method) Estimation",
        "Measuring canopy closure in forest resource inventories",
        "Rapid stand density assessment",
        "Judging the timing of tending thinning",
        "Canopy closure = points covered by tree crowns ÷ total sample points (0 to 1); classes: <0.20 open forest land, 0.20-0.39 low closure, 0.40-0.69 medium closure, 0.70-0.89 high closure, ≥0.90 very high closure.",
        "100 sample points with 65 covered by crowns: canopy closure = 65/100 = 0.65, which is medium closure (0.40-0.69), so the stand structure is moderate and growth is good, with no thinning needed yet.",
        "Is the point-sampling method very accurate?",
        "It depends on the number and representativeness of the points; too few points (<30) fluctuate a lot. Systematic layout avoiding the forest edge, with a consistent viewing angle when judging, reduces subjective error.",
        "Is canopy closure the same as forest coverage?",
        "No. Canopy closure is the share of the plot covered by the vertical projection of the canopy (a stand-level index), while forest coverage is the share of total land area taken by tree forest land (a regional index).",
        "About \"Forest Canopy Closure Calculation\"",
        "The forest canopy closure tool uses the point-sampling method: enter the total sample points and the points covered by tree crowns to compute the stand canopy closure and determine the closure class, suitable for forest resource inventories and stand quality assessment.",
        "Rapid canopy closure calculation by the point-sampling method",
        "Automatic five-level closure class determination",
        "Visual progress bar for a direct readout",
        "National continuous forest inventory",
        "Stand quality assessment",
        "Afforestation effectiveness acceptance",
        "Total sample points",
        "Sample points covered by crowns",
    ]))

    write('concentration-5', build('concentration-5', [
        "📋 Negative Ion Concentration Assessment",
        "Enter the air negative ion concentration (per cm³) to rate air quality and forest wellness suitability",
        "📖 Read the \"Air negative ion concentration grading (wellness suitability) usage guide\"",
        "Air negative ion concentration (per cm³) grading: up to 200 not fresh, 200 to 500 fairly fresh, 500 to 1000 fresh, 1000 to 3000 very fresh (suitable for forest wellness), above 3000 extremely fresh (near waterfalls and streams). Wellness suitability is best at 1000 per cm³ or above. Urban indoor levels are often below 100 per cm³, while humid forest areas and waterfall surroundings reach the highest concentrations, so you can use this to site wellness bases and assess scenic area environments.",
        "Negative ion concentration (per cm³)",
        "💡 Based on the air negative ion concentration grading standard and the forest wellness base construction standard, the higher the negative ion concentration the fresher the air and the greater the wellness value.",
        "Reference concentrations: urban indoor 40-50 per cm³, urban outdoor 100-200 per cm³, forests and waterfalls can reach 10000+ per cm³",
        "This is a general grading; the specific environmental quality needs a combined judgement with PM2.5, temperature and humidity",
        "📚 Deep dive: Air Negative Ion Concentration Grading (wellness suitability)",
        "Environmental assessment of forest wellness bases",
        "Air quality monitoring in scenic areas",
        "Negative ion concentration class determination",
        "By negative ion concentration c (per cm³): <200 not fresh, 200-600 average, 600-900 fresh, 900-1200 fairly fresh, 1200-1500 very fresh, 1500-1800 extremely fresh, 1800-3000 particularly fresh. Judge wellness suitability together with PM2.5, temperature and humidity.",
        "A measured negative ion concentration of c=1800 per cm³ falls in the 1500-1800 band, which is extremely fresh (approaching particularly fresh), a high-quality forest wellness environment well suited to wellness and therapy activities.",
        "What are typical negative ion levels in a city?",
        "Urban indoor is about 40-50 and outdoor about 100-200 per cm³, while forests, waterfalls and streams can reach thousands and even 10000+, so the gap is striking and forest wellness value stands out.",
        "Is a higher concentration always better?",
        "High concentrations are usually associated with clean, low-negative-ion environments, but a single index cannot represent overall air quality, so combine it with PM2.5, ozone, temperature and humidity for a full assessment.",
        "About \"Negative Ion Concentration Assessment\"",
        "The air negative ion concentration assessment tool takes a concentration value and automatically rates air quality and forest wellness suitability, suitable for forest parks and wellness base environmental assessment.",
        "Eight-level fine air quality assessment",
        "Simultaneous wellness suitability rating",
        "Visual concentration progress bar",
        "Forest wellness base evaluation",
        "Forest park environmental monitoring",
        "Air assessment in ecotourism areas",
        "Livability environment research",
        "Negative ion concentration",
    ]))

    write('density-5', build('density-5', [
        "🌳 Stand Density Structure",
        "Enter the sample plot area, tree count and mean breast diameter to compute trees per hectare, the stand density index (SDI) and the stand basal area",
        "Core formula (by input variable): N×(dbh÷25)^1.6; π×dbh×dbh÷4÷10000; n÷area×10000",
        "📖 Read the \"Stand density index (SDI) and basal area usage guide\"",
        "💡 Formula: trees per hectare N = tree count ÷ plot area × 10000; stand density index SDI = N × (D÷25)^1.6 (Reineke); basal area G = N × π×D²÷4 ÷ 10000 (m²/ha).",
        "The SDI reference diameter is 25cm; the larger the SDI the denser the stand, and ≥600 is generally taken as over-dense",
        "Basal area reflects how fully the stand uses space and is an important basis for tending thinning",
        "📚 Deep dive: Stand Density Index (SDI) and Basal Area",
        "Stand density evaluation and grading",
        "Tending thinning intensity decisions",
        "Trees per unit area and basal area accounting",
        "Trees per hectare N=n/area×10000; stand density index SDI=N×(DBH/25)^1.6 (reference diameter 25 cm); single-tree basal area g=π·DBH²/4/10000, basal area per hectare G=N×g. SDI classes: <200 too sparse, 200-350 somewhat sparse, 350-550 moderate, 550-700 somewhat dense, ≥700 over-dense.",
        "A 600 m² plot with 80 trees and a mean breast diameter of 16 cm: N=1333 trees/ha, SDI=1333×(16/25)^1.6≈652.9 (somewhat dense, thinning recommended), G=1333×0.0201≈26.8 m²/ha.",
        "Does a larger SDI mean denser?",
        "Yes. SDI combines tree count and diameter, cancelling out the trade-off between density and mean diameter; ≥600 is generally treated as over-dense and is an important thinning reference, but it must be read together with species and site.",
        "Why is the reference diameter 25 cm?",
        "25 cm is the standard North American SDI reference diameter, which makes different stands comparable; using another baseline means stating and converting it so the conclusion stays consistent.",
        "About \"Stand Density Structure\"",
        "The stand density structure tool computes trees per hectare, the stand density index (SDI) and the basal area from sample plot survey data to judge whether the density structure is reasonable, suitable for preparing forest management plans and designing tending thinning.",
        "Computes trees per hectare and basal area",
        "Reineke stand density index SDI",
        "Five-level density structure evaluation",
        "Stand structure regulation",
        "Forest resource inventory analysis",
        "Sample plot area",
        "Number of trees in the plot",
        "Mean breast diameter",
    ]))

if __name__ == '__main__':
    main()
