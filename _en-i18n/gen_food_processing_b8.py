#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food-processing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food-processing')
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
    out = {'slug': slug, 'industry': 'food-processing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('index', build('index', [
        "\U0001F3ED Food Processing Tools",
        "Food Processing Tools",
        "Freeze-thaw drip loss calculator. Enter the weights before freezing and after thawing to get the drip loss rate and see how repeated cycles accumulate in water-holding capacity, for quick-frozen food quality management.",
        "Dough absorption and final moisture calculator. Enter the flour weight, water added and the water equivalent of milk or egg to calculate dough absorption and finished product moisture, for standardised baking formulas and quality control.",
        "Spray drying tower water evaporation calculator. Enter the feed rate, solids content and recovery efficiency to compute theoretical and actual powder output, for capacity and material balance accounting in milk and instant powder drying.",
        "Filtration rate calculator. Enter the pressure difference, cake resistance and filtration area to estimate the filtration rate of food liquids such as juice or syrup, for equipment selection and process parameter optimisation.",
        "Sterilisation F Value (D Value / Z Value) Calculator",
        "Computes the thermal lethality and F value, supports D value and Z value conversion and the required sterilisation time, for canning and food sterilisation processes.",
        "pH Adjuster Dosage Calculator",
        "pH Adjustment (acidulant) Dosage Calculator",
        "Homogenisation pressure and particle size distribution calculator. Enter the reference pressure and particle size and use the power law d \u221D P^(\u2212b) to estimate the mean particle size at different homogenisation pressures, for particle size control in dairy drinks and sauces.",
        "Fermenter Brix and Alcohol Conversion Calculator",
        "Fermenter Brix and Alcohol Conversion Calculator",
        "Blanching Time-Temperature Combiner",
        "Blanching Time-Temperature (Enzyme Inactivation) Combiner",
        "Quick freezing time estimator. Enter the food dimensions, start and end temperatures and the heat transfer coefficient (natural convection, forced air or liquid nitrogen) to estimate the time needed for rapid freezing, for quick freezing processes and capacity planning.",
        "Frying oil absorption rate predictor. Enter the moisture change before and after frying and the conversion coefficient to estimate oil uptake, revealing how evaporated water is displaced by oil, for frying process and formula optimisation.",
        "Accounts for the total and unit cost of a recipe from the unit price, quantity and loss rate of each ingredient, with entries you can add and remove dynamically, for cost control in baking and catering.",
        "Packaging residual oxygen estimator. Enter the nitrogen flush ratio, packaging permeability and storage conditions to estimate the residual oxygen level in the pack, for extending shelf life and designing nitrogen-flushed packaging.",
        "Emulsion Stability Tester",
        "Emulsion Stability (centrifugal separation) Tester",
        "Material Balance Calculator",
        "Material Balance (Input-Output) Calculator",
        "Additive Use Limits (GB2760) Lookup Tool",
        "Look up the maximum permitted use levels and applicable food categories of common food additives under the GB 2760 food additive use standard",
        "Product Shelf Life (Accelerated Stability Test) Estimator",
        "Product Shelf Life (Accelerated Stability Test) Estimator",
        "Smoking Concentration Simulator",
        "Enter the chamber ventilation, temperature and material load to estimate the phenolic concentration, benzo[a]pyrene exposure level and risk grade during smoking, helping optimise temperature, time and exhaust to control carcinogens.",
        "Convert between the inner diameter of a cylindrical bottle and the fill height, or work backwards from a target volume to the fill height, for calibrating filling lines.",
        "Water Activity and Microbial Growth Assessor",
        "Water Activity (Aw) and Microbial Growth Assessor",
        "About \"Food Processing Tools\"",
        "This collection holds 20 free online tools covering the common calculations, conversions and lookups of food processing work. Whether you are a practitioner, a student or an everyday user, you will find ready-to-use utilities here. Everything runs in the browser, uploads nothing to a server and keeps your privacy safe.",
        "The food processing tools collected on this page include (a few representative tools):",
        "These tools help you finish common food processing tasks quickly, with no need to memorise formulas or convert units by hand.",
        "Do the Food Processing Tools need a download or registration?",
        "No. Every tool on this page is a pure front-end online utility: open the page and use it straight away, with no software to install, no account to create and no data uploaded.",
        "Are the Food Processing Tools accurate, and is my data safe?",
        "Each tool computes locally in your browser from public mathematical formulas and general industry standards, so results are immediate. All arithmetic runs on your own device and no data is uploaded to any server, so your privacy is protected.",
    ]))


if __name__ == '__main__':
    main()
