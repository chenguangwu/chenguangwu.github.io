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
    write('residual-oxygen', build('residual-oxygen', [
        "\U0001F4E6 Packaging Residual Oxygen Estimator",
        "Estimate the headspace residual oxygen in nitrogen-flushed packaging and how oxygen concentration changes during storage, accounting for packaging permeability",
        " / Packaging Residual Oxygen Estimate",
        "\U0001F4D6 See the \"Packaging Residual Oxygen Estimation User Guide\"",
        "Headspace volume = total package volume (mL) \u2212 product volume (mL); initial oxygen = headspace volume \u00D7 initial oxygen concentration (%) \u00F7 100; oxygen after storage = initial oxygen + oxygen transmission rate OTR (mL/(m\u00B2\u00B7day)) \u00D7 area (m\u00B2) \u00D7 days \u2212 oxygen consumed by the product; residual oxygen rate = oxygen after storage \u00F7 headspace volume \u00D7 100%. Food packaging usually needs a residual oxygen rate below 1%-2% to extend shelf life, and nitrogen flushing markedly lowers the initial oxygen concentration.",
        "Total package volume (mL)",
        "Volume taken by the product (mL)",
        "Initial headspace oxygen concentration after flushing (%)",
        "Air is 21%; after nitrogen flushing it is usually brought down to 0.5-3%",
        "Packaging oxygen transmission rate (cc/m\u00B2\u00B724h\u00B7atm)",
        "Aluminium foil about 0.5, EVOH 0.5-5, PET 50-100, PE over 2000 (typical values)",
        "Packaging oxygen transmission area (cm\u00B2)",
        "Storage days",
        "Headspace volume = total package volume \u2212 product volume. Initial residual oxygen = headspace volume \u00D7 initial oxygen %. During storage, Fick's law gives the ingress as oxygen transferred \u2248 OTR \u00D7 area (m\u00B2) \u00D7 days \u00D7 (21% \u2212 internal oxygen %). Too much residual oxygen leads to fat oxidation and aerobic bacterial growth.",
        "\U0001F4DA In-depth analysis: Packaging Residual Oxygen Estimation",
        "Designing residual oxygen for nitrogen-flushed packs",
        "Controlling oxidation risk in high-oil products",
        "Selecting barrier materials",
        "Headspace volume = total package volume \u2212 product volume; initial oxygen = headspace volume \u00D7 initial O\u2082%; ingress during storage \u2248 OTR\u00D7area\u00D7days\u00D7(21\u2212internal O\u2082%)/100.",
        "For a 500 mL pack with 400 mL of product: 100 mL of headspace at 2% initial residual oxygen gives 2 mL of oxygen; with OTR=20, an area of 300 cm\u00B2 and 30 days, about 3.4 mL permeates in, giving a residual oxygen concentration of about (2+3.4)/100\u00D7100%=5.4%, which is high and needs a stronger barrier or more thorough nitrogen flushing.",
        "How do I lower the residual oxygen?",
        "Raise the nitrogen flush rate, choose high-barrier (low OTR) materials, shrink the headspace and seal as soon as possible.",
        "How high is residual oxygen dangerous?",
        "For oily or oxidation-prone products below 1% is safest; above 3% oxidation accelerates, so pair it with antioxidants or vacuum packing.",
        "About \"Packaging Residual Oxygen Estimator\"",
        "The Packaging Residual Oxygen Estimator is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('shelf-life-aslt', build('shelf-life-aslt', [
        "\U0001F373 Product Shelf Life (Accelerated Stability Test) Estimator",
        "Extrapolate shelf life at the real storage temperature from accelerated test conditions using the Q\u2081\u2080 model",
        "Product Shelf Life (ASLT) Estimator",
        " / Shelf Life ASLT Extrapolation",
        "\U0001F4D6 See the \"Shelf Life (Accelerated Stability Test) Extrapolation User Guide\"",
        "Accelerated test temperature T_t (\u00B0C)",
        "Actual storage temperature T_s (\u00B0C)",
        "Time to reach the endpoint in the accelerated test \u03B8_t (days)",
        "Q\u2081\u2080 value (temperature coefficient)",
        "The factor by which the reaction rate rises for a 10\u00B0C temperature rise, commonly 2-3 for hydrolysis and oxidation",
        "ASLT accelerated shelf life test: \u03B8_s = \u03B8_t \u00D7 Q\u2081\u2080^((T_t \u2212 T_s)/10). In other words a hot, short test extrapolates to a long, cool real storage period. Q\u2081\u2080 reflects how temperature affects the spoilage rate, and it differs by failure mechanism (microorganisms 3-5, oxidation 2-3).",
        "\U0001F4DA In-depth analysis: Shelf Life (Accelerated Stability Test) Extrapolation",
        "Shelf life compliance assessment",
        "Extrapolating room-temperature shelf life from accelerated ageing",
        "Verifying formula and packaging improvements",
        "Room-temperature shelf life \u03B8_s = \u03B8_t \u00D7 Q\u2081\u2080^((T_t \u2212 T_s)/10), where \u03B8_t and T_t are the failure time and temperature under acceleration and T_s is the actual storage temperature.",
        "30 days to failure at 37\u00B0C with Q\u2081\u2080=2 extrapolated to 25\u00B0C: \u03B8_s=30\u00D72^((37\u221225)/10)=30\u00D72^1.2\u224868.9 days (about 2.3 months), which should be calibrated against the measured spoilage point.",
        "What Q\u2081\u2080 should I use?",
        "For most foods spoilage has Q\u2081\u2080 around 2-3 and fat oxidation can be higher; determine it experimentally per product and failure mode.",
        "Can ASLT results set the label directly?",
        "They are an estimate only; the official shelf life follows real long-term storage at the actual temperature and humidity with microbiological and sensory endpoints.",
        "About \"Product Shelf Life (Accelerated Stability Test) Estimator\"",
        "The Product Shelf Life (Accelerated Stability Test) estimator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('spray-drying', build('spray-drying', [
        "\u26C5 Spray Drying Tower Water Evaporation Calculator",
        "Compute the powder output and water evaporated by spray drying from a material balance",
        " / Spray Drying Evaporation",
        "\U0001F4D6 See the \"Spray Drying Tower Water Evaporation User Guide\"",
        "Dry solids = feed \u00D7 solids content (%) \u00F7 100; powder output = dry solids \u00D7 recovery (%) \u00F7 100; water evaporated = feed \u2212 powder output; finished moisture = (powder output \u2212 dry solids) \u00F7 powder output \u00D7 100%; heat demand is about water evaporated \u00D7 (latent heat of vaporisation 2260 kJ/kg plus sensible heat); inlet temperature is typically 150 to 220 \u00B0C and outlet temperature 80 to 100 \u00B0C.",
        "Feed rate (kg/h)",
        "Feed solids content (%)",
        "Moisture content of the finished powder (%)",
        "Powder recovery rate (%)",
        "Tower bottom plus cyclone recovery efficiency, typically 95-99%",
        "Material balance: dry solids are conserved. Dry solids = feed \u00D7 solids %; theoretical powder = dry solids \u00F7 (1 \u2212 moisture %); actual powder = theoretical powder \u00D7 recovery; water evaporated = feed \u2212 theoretical powder. Concentration ratio = finished solids \u00F7 feed solids.",
        "\U0001F4DA In-depth analysis: Spray Drying Tower Water Evaporation",
        "Capacity accounting for milk and instant powder",
        "Balance between inlet air and powder output",
        "Effect of recovery rate on yield",
        "Dry solids = feed \u00D7 solids %; theoretical powder = dry solids; actual powder = dry solids \u00D7 recovery %; water evaporated = feed \u2212 actual finished weight.",
        "Feed 500 kg at 40% solids with 98% recovery: dry solids=200 kg, theoretical powder 200 kg and actual about 196 kg; at 4% finished moisture the total weight is about 204.2 kg, so about 295.8 kg of water is evaporated.",
        "How do I raise the recovery rate?",
        "Improve cyclone and bag filter efficiency, control the inlet temperature and atomisation droplet size, and reduce fine powder carried out with the exhaust.",
        "What is the water evaporation figure used for?",
        "Sizing the heater and fan load, and accounting for",
        "thermal efficiency",
        " and energy use per unit of product.",
        "About \"Spray Drying Tower Water Evaporation Calculator\"",
        "\uFE0F Spray Drying Tower Water Evaporation Calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))


if __name__ == '__main__':
    main()
