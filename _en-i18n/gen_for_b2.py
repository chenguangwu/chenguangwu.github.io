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
    write('log-volume', build('log-volume', [
        "⚖️ Log Volume Calculator",
        "National GB4814-84 standard, multiple formulas, multi-log totals",
        "Core formula (by input variable): 0.00007854×L×(D+0.8×L)×(D+0.8×L); V×density×1000×q",
        "📖 Read the \"Log volume (GB4814-84) calculation usage guide\"",
        "📋 Volume table",
        "Formula selection",
        "Measurement diameter (cm)",
        "Measurement length (m)",
        "General species",
        "Chinese fir (dedicated)",
        "⚖️ Calculate volume",
        "➕ Add to the total",
        "📦 Log totals",
        "📏 Measurement rules",
        "Measurement diameter",
        ": the small-end diameter, rounded up in 2cm steps, and below 14cm in 1cm steps",
        "Measurement length",
        ": rounded in 0.2m or 0.5m steps, with the remainder discarded",
        "Length tolerance",
        ": +6cm / -2cm is allowed",
        "📐 Formulas (GB4814-84)",
        "Small diameter (≤12cm):",
        "Large diameter (≥14cm):",
        "where: V = volume (m³), L = measurement length (m), D = measurement diameter (cm)",
        "⚠️ Scope of application",
        ": for calculating log volume with a measurement diameter of 4-120cm and a measurement length of 1-10m",
        "📋 Quick log volume reference table (m³)",
        "Diameter class (cm)",
        "📚 Deep dive: Log Volume (GB4814-84) Calculation",
        "Log measurement and volume tally",
        "Multi-log totals in timber trade",
        "Small-end diameter and log length accounting",
        "Per GB4814-84: for a large diameter (≥14cm), V=0.00007854·L·(D+0.5L+0.005L²+0.000125L(14−L)²(D−10))² (D = small-end diameter, L = measurement length); for a small diameter (≤12cm) the (D+0.45L+0.2)² form applies. Multiple logs are accumulated by count, and estimated weight = volume × density × count.",
        "Small-end diameter D=20 cm, measurement length L=4 m, 1 log: GB V ≈ 0.1602 m³, and with a wood density of 0.55 the estimated weight is about 88.1 kg; for 10 logs the total volume is about 1.602 m³.",
        "Why is the measurement diameter taken at the small end?",
        "The small-end face of a log is regular and varies little, and the national standard specifies the small-end diameter as the measurement diameter with rounding rules applied, which keeps measurement consistent and trade fair.",
        "Is the weight estimate formula accurate?",
        "Estimated weight = volume × air-dry density, and density varies a lot with species and moisture content (0.4-0.9), so it is a reference only; an exact weight must be measured.",
        "About \"Log Volume Calculator\"",
        "The Log Volume Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

    write('strength-4', build('strength-4', [
        "📐 Harvest Intensity Design",
        "Enter the stand stock volume, harvest ratio and recurrence year (harvest cycle) to compute the harvest volume, the retained stock and the annual allowable harvest",
        "Core formula (by input variable): stock×ratio÷100; area÷15",
        "📖 Read the \"Harvest volume and annual allowable harvest usage guide\"",
        "Stand stock volume (m³/ha)",
        "Harvest ratio (%)",
        "Recurrence year (years)",
        "Harvest type",
        "Tending thinning",
        "Selective harvest",
        "Growth harvest",
        "Sanitary harvest",
        "Working area (mu, optional)",
        "💡 Formula: harvest volume = stock volume × harvest ratio; retained stock = stock volume − harvest volume; annual harvest = harvest volume ÷ recurrence year.",
        "Tending thinning intensity generally does not exceed 25%-30%, and selective harvest intensity generally does not exceed 40%",
        "The retained stock must meet the stand's recovery needs, and canopy closure after harvest must not fall below 0.6",
        "An actual harvest design must obtain a harvest permit according to law and comply with quota management",
        "📚 Deep dive: Harvest Volume and Annual Allowable Harvest",
        "Tending thinning intensity design",
        "Total harvest accounting for the working block",
        "Control of retained stock after harvest",
        "Harvest volume = stock × harvest ratio; retained stock = stock − harvest volume; annual harvest = harvest volume ÷ recurrence year (harvest cycle). Intensity classes: <15% light, 15-25% moderate, 25-35% heavy, ≥35% very heavy. The block total = the per-hectare amount × area (ha).",
        "Stock of 180 m³ per hectare, harvest ratio 25%, recurrence year 10, working block 500 mu (≈33.3 ha): harvest volume = 45 m³/ha, retained = 135 m³/ha, annual = 4.5 m³/ha·a, which counts as moderate harvesting; the block total harvest is about 1500 m³.",
        "What is the upper limit on harvest intensity?",
        "Tending thinning generally stays within 25%-30% and selective harvest within 40%, and canopy closure after harvest must not drop below 0.6 so the stand can recover and stay ecologically stable.",
        "How do I use the annual allowable harvest?",
        "It serves as the annual ceiling for the sustainable management quota, with block total ÷ recurrence year giving the annual figure, which prevents over-harvesting. In practice it must go into the harvest quota and the operating design approval.",
        "About \"Harvest Intensity Design\"",
        "The forest harvest intensity design tool takes the stand stock volume, harvest ratio and recurrence year to compute the harvest volume, retained stock and annual allowable harvest, suitable for preparing forest management plans and harvest quota management.",
        "Compute harvest volume and retained stock",
        "Supports annual harvest derivation",
        "Harvest intensity class determination",
        "Extensible to working block totals",
        "Harvest quota management",
        "Selective harvest operation planning",
        "Stand stock volume",
        "Harvest ratio",
        "Recurrence year",
        "Working area",
    ]))

    write('growth-rate', build('growth-rate', [
        "🧮 Tree Growth Rate Calculator",
        "Pressler formula, compound formula, annual increment and mean annual increment",
        "Core formula (by input variable): (v2-v1)÷(v2+v1)×200÷n; ((v2÷v1)^1÷n-1)×100",
        "📖 Read the \"Tree growth rate (Pressler/compound) calculation usage guide\"",
        "📋 Reference values",
        "Starting volume/diameter (V₁)",
        "Ending volume/diameter (V₂)",
        "Interval in years (n)",
        "Breast diameter",
        "Tree height",
        "🧮 Calculate the growth rate",
        "📐 Growth rate formulas",
        "1. Pressler formula:",
        "2. Compound formula:",
        "3. Annual increment:",
        "4. Mean annual increment:",
        "θ = V/a (a is the age)",
        "🌲 Growth stage classification",
        "Juvenile stage",
        ": high growth rate (10-20%), small absolute growth",
        "Rapid growth stage",
        ": relatively high growth rate (8-15%), largest absolute growth",
        "Near-mature stage",
        ": growth rate declining (3-8%), volume accumulating fast",
        "Mature stage",
        ": low growth rate (1-3%), numerically mature",
        "📊 Reference growth rates by species (annual average)",
        "📚 Deep dive: Tree Growth Rate (Pressler/compound) Calculation",
        "Monitoring annual and mean increment",
        "Judging maturity age and harvest period",
        "Comparing volume and diameter growth rates",
        "Pressler growth rate P=(V₂−V₁)/((V₂+V₁)/2)/n×100%; compound growth rate=(V₂/V₁)^(1/n)−1; annual increment z=(V₂−V₁)/n; total growth rate=(V₂/V₁−1)×100%. Used to judge numerical maturity and the growth inflection point.",
        "Two measurements V₁=0.10, V₂=0.15 m³, 5 years apart: Pressler=(0.05/0.125)/5×100=8.0%, compound=(1.5^0.2−1)×100≈8.45%, annual increment=0.01 m³/year, total growth rate=50%.",
        "How do the Pressler and compound formulas differ?",
        "Pressler uses the mean volume as the denominator (common in forestry and sensitive to the middle of the growth period), while the compound formula uses the geometric mean (approximating continuous compounding). The two are close, so read the trend consistently.",
        "Can the growth rate set the harvest period?",
        "You can watch when the annual increment falls below the mean increment (numerical maturity), but the decision still has to combine technical maturity, economic maturity and management goals.",
        "About \"Tree Growth Rate Calculator\"",
        "The Tree Growth Rate Calculator is a forestry resource tool that helps you calculate forestry parameters and output.",
    ]))

    write('estimate-33', build('estimate-33', [
        "🌲 Wildlife Population Estimation",
        "Enter the transect length, mean detection distance on one side and the observed tracks or individuals to estimate population density with the line transect method",
        "Core formula (by input variable): w÷1000",
        "Wildlife Population",
        "/ Wildlife Population",
        "📖 Read the \"Line transect population density estimation usage guide\"",
        "Total transect length (km)",
        "Mean detection distance on one side (m)",
        "Observed tracks / individuals",
        "Total survey area (km², optional)",
        "💡 Formula (line transect method): population density D = N ÷ (2 × L × W), where L is the transect length (km) and W is the one-sided detection distance (km); the result is in individuals/km².",
        "The line transect method assumes a uniform animal distribution and a detection probability that declines with distance, so it suits estimation over fairly large areas",
        "The one-sided detection distance W is the mean detection distance perpendicular to the transect",
        "The result is an approximation; an accurate population survey should combine repeated surveys",
        "📚 Deep dive: Line Transect Population Density Estimation",
        "Wildlife population density survey",
        "Transect coverage",
        "Area calculation",
        "Regional population extrapolation",
        "Transect covered area = 2 × transect length × mean one-sided detection distance (converted to km); population density = observed individuals (tracks) ÷ covered area (individuals/km²); regional population = density × regional area (assuming uniform distribution).",
        "Transect 5 km, mean one-sided detection distance 25 m, 12 individuals observed, area 50 km²: covered area = 2×5×0.025 = 0.25 km², density = 12/0.25 = 48 individuals/km², regional population ≈ 48×50 = 2400 individuals.",
        "What are the assumptions of the line transect method?",
        "It assumes a uniform animal distribution, a detection probability that declines with perpendicular distance and a stable observer ability; schooling or cryptic species lead to over- or under-estimation, so repeat transects and detection-function corrections are needed.",
        "How do I estimate the one-sided detection distance?",
        "It is the mean perpendicular distance at which tracks or individuals are sighted; measure it on site or compute it later in GIS. Errors in the distance estimate directly amplify the density error.",
        "About \"Wildlife Population Estimation\"",
        "The wildlife population density estimation tool uses the line transect method: enter the transect length, detection distance and observed track count to estimate population density and regional population, suitable for wildlife resource surveys and protected area monitoring.",
        "Estimating population density by the line transect method",
        "Automatic transect covered area calculation",
        "Supports extrapolating the regional population total",
        "Wildlife resource survey",
        "Nature reserve monitoring",
        "Population dynamics assessment",
        "Habitat management",
        "Transect length",
        "Detection distance",
        "Track count",
        "Area",
    ]))

if __name__ == '__main__':
    main()
