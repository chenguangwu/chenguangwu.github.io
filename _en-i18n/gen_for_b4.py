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
    write('index', build('index', [
        "🌲 Forestry Resource Tools",
        "Forestry Resources",
        "Forestry resource tools",
        "Enter the stand stock, wood density and carbon fraction to estimate the forest carbon sink and the tradable carbon sink value along the biomass - carbon stock - CO₂ equivalent chain, for forestry carbon sink project accounting.",
        "Enter the log small-end diameter and log length to compute the volume of a single log with the national GB4814-84 standard formulas (covering several diameter classes) and total up multiple logs, for log measurement and timber trade metering.",
        "Enter two volume measurements and the interval between them to compute the annual and mean annual increment and the growth rate with the Pressler and compound formulas, for tree growth monitoring and maturity age judgement.",
        "Enter the breast diameter and tree height to compute the volume of a single standing tree with a one-entry or two-entry volume table, the experimental form factor method or the top height method, and compare results across formulas, for single-tree output estimation.",
        "Choose the angle-gauge cruising, sample plot or mean experimental form factor method, enter the breast diameter, tree height and form factor to compute stock volume per hectare, for forest resource inventories and harvest volume assessment.",
        "Enter the parcel shape dimensions or GPS boundary coordinates to compute the area with slope-to-flat projection, converting between mu, hectares and square metres, for forest rights confirmation, afforestation planning and resource inventories.",
        "Enter the species, site condition and spacing to compute trees per unit area and recommend a suitable density, avoiding over-dense or over-sparse planting, for afforestation design and seedling requirement estimation.",
        "Uses the point-sampling method to count the crown cover ratio and estimate canopy closure (0-1), supporting sample point layout and result verification, for forest resource inventories and stand density assessment, entirely in the front end.",
        "Enter the sample plot area, mean breast diameter, mean tree height and tree count to estimate the volume of a single tree and the stock per unit area with the experimental form factor method, for forest resource inventories and stand assessment.",
        "Biodiversity Shannon",
        "Biodiversity Shannon Index",
        "Choose the annual ring, increment borer or breast diameter regression method and enter the corresponding parameters to estimate tree age, for forest asset valuation, ancient tree appraisal and growth research.",
        "Enter the planting area, trees per mu, yield per tree and unit price to forecast the total yield and total value of an economic forest, for management planning and revenue estimation of orchards, oil tea and other economic forests.",
        "Forest Rights Area Survey",
        "Enter the vertices of the forest parcel polygon (one per line, format x,y) in clockwise or counter-clockwise order to automatically compute the area and perimeter",
        "Wildlife Population",
        "Enter the transect length, mean one-sided detection distance and observed tracks or individuals to estimate population density with the line transect method",
        "Enter the air negative ion concentration (per cm³) to rate air quality and the suitability of forest wellness, as a reference for scenic area assessment, wellness base siting and ecological monitoring.",
        "Record the damage class and incidence of pests and diseases on sample trees, tallying affected area and trends by light, moderate and severe class to support forest management decisions, with registration data staying local in the front end.",
        "Enter the sample plot area, tree count and mean breast diameter to compute trees per hectare, the stand density index (SDI) and the stand basal area",
        "Enter the stand stock, harvest ratio and recurrence year (harvest cycle) to compute the harvest volume, the retained stock and the annual allowable harvest",
        "Enter the tree spacing, row spacing, planting area and per-tree seedling cost to compute trees per mu, the total tree count and the planting cost",
        "About \"Forestry Resource Tools\"",
        "This collection gathers 19 free online tools covering the common calculations, conversions and lookups of forestry resources. Whether you are a practitioner, a student or an ordinary user, you will find practical ready-to-use mini tools here. Every tool runs entirely in the browser, no data is uploaded to a server, and your privacy is protected.",
        "The forestry resource tools collected on this page include (a few representative ones):",
        "These tools help you finish common forestry resource tasks quickly, with no need to memorize complex formulas or convert anything by hand — type and you get the result.",
        "Do the forestry resource tools need a download or registration?",
        "No. Every tool on this page is a pure front-end online tool: open the page and start using it. No software to install, no account to register, and no data is uploaded.",
        "Are the results accurate? Is the data safe?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are instant. All computation happens on your own device, no data is uploaded to a server, and your privacy is fully protected.",
    ]))

    write('estimate-32', build('estimate-32', [
        "🌳 Stock Volume Estimation",
        "Enter the sample plot area, mean breast diameter, mean tree height and tree count to estimate the stand stock with the experimental form factor method",
        "Core formula (by input variable): totalV÷area×10000; π×dbh×dbh÷4÷10000; mPerHa÷15",
        "📖 Read the \"Experimental form factor stock estimation usage guide\"",
        "Mean tree height (m)",
        "Experimental form factor f",
        "💡 Formula: single-tree volume V = g × H × f, where g = π×D²÷4 ÷ 10000 (m²); stock per unit area M = V × N ÷ sample plot area × 10000 (m³/ha). The experimental form factor is usually taken as 0.40-0.52.",
        "Experimental form factor f: 0.45-0.50 for conifers and 0.40-0.45 for broadleaves, adjustable from the reference dropdown",
        "This method is an approximation; the exact stock should come from the local two-entry volume table",
        "📚 Deep dive: Experimental Form Factor Stock Estimation",
        "Single-tree volume estimation on a sample plot",
        "Stock per unit area calculation",
        "Stand assessment in forest resource inventories",
        "Single-tree basal area g=π·DBH²/4/10000; single-tree volume v=g × tree height × experimental form factor f (conifers f≈0.45-0.50, broadleaves ≈0.40-0.45); the plot total is Σv, stock per hectare = plot total / plot area × 10000, and per mu = per hectare / 15.",
        "A 667 m² plot with 120 trees, 14 cm breast diameter, 12 m height and f=0.5: g=0.0154 m², v=0.0154×12×0.5=0.0924 m³, total stock=11.08 m³, stock per hectare=11.08/667×10000≈166.2 m³/ha (≈11.1 m³/mu).",
        "How much do the form factor and the two-entry volume table differ?",
        "The form factor method is an approximation while the two-entry volume table is more accurate; large-area surveys should follow the local volume table, and the form factor method serves only for quick estimates.",
        "Why do conifers and broadleaves use different form factors?",
        "Because the trunk forms differ: conifers have straight boles with a larger form factor, while broadleaves often fork and have a smaller one, so different ranges are used to improve estimation accuracy.",
        "About \"Stock Volume Estimation\"",
        "The forest stock estimation tool uses the experimental form factor method: enter sample plot survey data to estimate the single-tree volume and the stock per unit area, suitable for forest resource inventories and stand stock assessment.",
        "Volume estimated with the experimental form factor method",
        "Supports a custom form factor f",
        "Outputs hectares, mu and other units",
        "Forest resource stock inventory",
        "Stand stock assessment",
        "Basis for harvest volume design",
        "Foundation for carbon stock estimation",
        "Sample plot area",
        "Number of trees in the plot",
        "Mean breast diameter",
        "Mean tree height",
        "Experimental form factor",
    ]))

    write('shengwuduoyangxingshannon', build('shengwuduoyangxingshannon', [
        "🌲 Biodiversity Shannon Index",
        "Enter the individual count of each species (one per line, or separated by commas or spaces) to compute the Shannon-Wiener diversity index, Pielou evenness and Simpson dominance",
        "Biodiversity Shannon",
        "/ Biodiversity Shannon",
        "📖 Read the \"Biodiversity Shannon index calculation usage guide\"",
        "Shannon-Wiener diversity index H = -Σ(pᵢ × ln pᵢ), where pᵢ = the individual count of species i ÷ the total individual count; the larger H is the higher the diversity (2 to 4 is common in forest communities). Pielou evenness J = H ÷ ln S (S being the number of species) runs from 0 to 1, and the closer to 1 the more even it is. Simpson dominance D = 1 - Σpᵢ². Margalef richness R = (S - 1) ÷ ln N (N being the total individual count). Used together, the four indices fully characterize the community structure.",
        "Individual count of each species (one per line, or separated by commas or spaces)",
        "💡 Shannon-Wiener index H' = -Σ(pᵢ·ln pᵢ), pᵢ = nᵢ/N; Pielou evenness J = H' ÷ ln(S); Simpson dominance D = 1 - Σpᵢ²; Margalef richness d = (S-1) ÷ ln(N).",
        "Each number represents the individual count of one species, and at least 2 species are needed",
        "The larger H' is the higher the diversity; the closer J is to 1 the more evenly the species are distributed",
        "This tool uses the natural logarithm (ln), consistent with most ecology textbooks",
        "📚 Deep dive: Biodiversity Shannon Index Calculation",
        "Community species diversity assessment",
        "Evenness and dominance analysis",
        "Ecological restoration effectiveness monitoring",
        "Shannon-Wiener index H′=-Σpᵢ·ln(pᵢ) (pᵢ is the share of individuals of species i, natural logarithm); Pielou evenness J=H′/ln(S); Simpson dominance D=1-Σpᵢ²; Margalef richness=(S-1)/ln(N). The larger H′ and the closer J is to 1, the higher the diversity.",
        "Individual counts for 4 species [50,30,15,5] (N=100): p=[0.5,0.3,0.15,0.05], H′≈1.142, J≈0.824 (fairly even), D≈0.635, Margalef≈0.651; a moderately diverse community.",
        "Which logarithm does H′ use?",
        "Ecology textbooks mostly use the natural logarithm ln; with log₂ or log₁₀ the numbers differ but the conclusion is the same, so state the base to allow horizontal comparison.",
        "Is H′ alone enough?",
        "No. H′ includes richness and evenness, but many rare species inflate it; judge the community structure together with Simpson dominance and Margalef richness.",
        "About \"Biodiversity Shannon Index\"",
        "The biodiversity Shannon index tool takes the individual count of each species and computes the Shannon-Wiener diversity index, Pielou evenness, Simpson dominance and Margalef richness in one go, suitable for community ecology research.",
        "Four major diversity indices at once",
        "Automatic count of species and individuals",
        "Species relative abundance table",
        "Diversity grade assessment",
        "Community ecology diversity research",
        "Forest community structure analysis",
        "Ecological restoration effectiveness evaluation",
        "Biodiversity monitoring",
        "For example: \n23,15,12,8,5",
    ]))

    write('pest-1', build('pest-1', [
        "🌲 Pest and Disease Monitoring",
        "Enter the number of affected trees and the total number surveyed to compute the incidence rate, determine the damage class and get control advice",
        "📖 Read the \"Pest incidence rate and damage class usage guide\"",
        "Incidence rate = affected trees ÷ total trees × 100%",
        "Number of affected trees (trees)",
        "Total trees surveyed (trees)",
        "💡 Formula: incidence rate = affected trees ÷ total trees × 100%. The classes follow the national occurrence and disaster standards for forest pests.",
        "The survey sample should be representative; at least 50 sample trees are recommended",
        "Class standards: slight <5%, light 5-10%, moderate 10-20%, severe 20-40%, very severe >40%",
        "Actual control should be judged together with the pest species and its occurrence pattern",
        "📚 Deep dive: Pest Incidence Rate and Damage Class",
        "Incidence statistics on sample trees",
        "Light/moderate/severe grading",
        "Forest management and control decisions",
        "Incidence rate = affected trees ÷ total trees × 100%; grading by rate: <5% slight, 5-10% light, 10-20% moderate, 20-40% severe, ≥40% very severe, with matching control advice (monitor / prevent / control promptly / call in professional control immediately).",
        "200 trees surveyed with 35 affected: incidence rate = 35/200×100 = 17.5%, which is moderate; control promptly to stop it spreading and avoid escalating to a severe outbreak.",
        "How many trees make a representative survey?",
        "At least 50 sample trees placed randomly is recommended, with stratified sampling when the distribution is uneven; too small a sample makes the incidence rate fluctuate and the class unreliable.",
        "Can the incidence rate directly set the control intensity?",
        "No. You also need the insect or disease species, its occurrence pattern and the host value; quarantine pests must be strictly controlled even at a low rate.",
        "About \"Pest and Disease Monitoring\"",
        "The forest pest monitoring tool takes the number of affected trees and the total surveyed to compute the incidence rate, determine the damage class and automatically give control advice, suitable for monitoring forest pests and making control decisions.",
        "Fast pest incidence rate calculation",
        "Five-level damage class determination",
        "Automatic control advice",
        "Forest pest monitoring",
        "Pest control decisions",
        "Disaster loss assessment",
        "Forest health monitoring",
        "Number of affected trees",
        "Total trees",
    ]))

if __name__ == '__main__':
    main()
