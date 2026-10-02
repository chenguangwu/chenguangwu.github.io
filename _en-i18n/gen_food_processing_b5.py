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
    write('filtration-rate', build('filtration-rate', [
        "\U0001F4A7 Filtration Rate Calculator",
        "Compute the filtrate volume and instantaneous flow rate from the Ruth constant-pressure filtration equation, including cake and medium resistance",
        " / Filtration Rate Calculation",
        "\U0001F4D6 See the \"Filtration Rate (Constant Pressure) Estimation User Guide\"",
        "Filtration area A (m\u00B2)",
        "Filtration pressure difference \u0394P (kPa)",
        "Filtrate viscosity \u03BC (mPa\u00B7s)",
        "Water about 1, juice 1.5-3, syrup higher",
        "Specific cake resistance \u03B1 (m/kg)",
        "Compressible cake 1e9-1e12, diatomaceous earth pre-coating lowers it",
        "Slurry concentration c (kg dry cake/m\u00B3 filtrate)",
        "Medium resistance Rm (1/m)",
        "Filtration time t (min)",
        "Ruth constant-pressure filtration equation: t/V = (\u03BC \u03B1 c)/(2 A\u00B2 \u0394P)\u00B7V + (\u03BC Rm)/(A \u0394P), where V is the filtrate volume, \u03B1 the specific cake resistance, c the concentration and Rm the medium resistance. Solving gives V = [\u2212b + \u221A(b\u00B2 + 4 a t)] / (2a). The instantaneous flow is dV/dt = A \u0394P / [\u03BC (\u03B1 c V/A + Rm)].",
        "\U0001F4DA In-depth analysis: Filtration Rate (Constant Pressure) Estimation",
        "Filtration equipment selection for juice and syrup",
        "Optimising cake resistance and filtration area",
        "Filtration cycle and capacity accounting",
        "Constant-pressure filtration: \u03B1\u00B7c/(2A\u00B2\u0394P)\u00B7V\u00B2 + \u03BCR_m/(A\u0394P)\u00B7V = t; the filtrate volume V follows, and the mean flow rate = V/t\u00D73600/A.",
        "With A=1 m\u00B2, \u0394P=100 kPa, \u03BC=1 mPa\u00B7s, \u03B1=1\u00D710\u00B9\u00B9 m/kg, c=20 kg/m\u00B3, R_m=1\u00D710\u00B9\u2070 m and t=30 min: the filtrate is about 419.5 L and the mean flow about 839 L/(m\u00B2\u00B7h).",
        "Where does cake resistance come from?",
        "It is set by the solids content of the slurry and the particle specific resistance; the higher the solids the faster resistance grows, so pre-coating or cross-flow filtration helps.",
        "Does a bigger pressure difference always mean faster?",
        "The flow rises with \u0394P, but too much compacts the cake and actually raises resistance while energy use climbs, so a balance is needed.",
        "About \"Filtration Rate Calculator\"",
        "The Filtration Rate Calculator is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('homogenization-pressure', build('homogenization-pressure', [
        "\U0001F39A\uFE0F Homogenisation Pressure and Particle Size Calculator",
        "Estimate the effect of homogenisation pressure on emulsion droplet size from an empirical power-law model",
        " / Homogenisation Pressure and Particle Size",
        "\U0001F4D6 See the \"Homogenisation Pressure and Particle Size User Guide\"",
        "Reference pressure P\u2080 (MPa)",
        "Reference particle size d\u2080 (\u03BCm)",
        "Mean particle size measured at P\u2080 (D50 or D[3,2])",
        "Target pressure P (MPa)",
        "Pressure decay exponent b",
        "Particle size decays as a power law of pressure d \u221D P^(\u2212b), typically 0.5-0.8",
        "Number of homogenisation passes N",
        "Multi-stage or repeated homogenisation refines further, corrected by N^(\u2212c) (c\u22480.1)",
        "Empirical model: d = d\u2080 \u00D7 (P/P\u2080)^(\u2212b) \u00D7 N^(\u22120.1). Higher pressure and more passes give smaller droplets and a more stable emulsion but raise energy use. Milk is typically homogenised at 20-40 MPa, and reducing fat globules below 1\u03BCm prevents creaming.",
        "\U0001F4DA In-depth analysis: Homogenisation Pressure and Particle Size",
        "Particle refinement in dairy drinks",
        "Controlling sauce texture and stability",
        "Optimising homogenisation energy use",
        "Mean particle size d = d\u2080 \u00D7 (P/P\u2080)^(\u2212b) \u00D7 N^(\u22120.1), where b is the particle size sensitivity exponent and N the number of homogenisation stages.",
        "Baseline P\u2080=20 MPa, d\u2080=1.5 \u03BCm, b=0.6, single stage: raising it to 40 MPa gives d=1.5\u00D7(40/20)^(\u22120.6)\u22480.99 \u03BCm, a particle size drop of about 34%.",
        "Is higher pressure always better?",
        "Particle size falls with pressure but with diminishing returns; beyond a point the gain is small while energy climbs steeply, so 15-40 MPa balances texture and cost.",
        "What does multi-stage homogenisation do?",
        "Increasing N refines further and narrows the distribution, but the improvement is limited and the equipment and investment grow.",
        "About \"Homogenisation Pressure and Particle Size Distribution Calculator\"",
        "\uFE0F Homogenisation Pressure and Particle Size Distribution Calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('material-balance', build('material-balance', [
        "\U0001F3ED Material Balance (Input-Output) Calculator",
        "Account for total production input and output, losses and yield, with entries you can add and remove dynamically",
        "\"Account for total production input and output, losses and yield, with entries you can add and remove dynamically\" is computed from the input parameters and the result is reported.",
        "Material Balance Calculator",
        " / Material Balance Accounting",
        "\U0001F4D6 See the \"Material Balance (Input-Output) Accounting User Guide\"",
        "Input materials",
        "+ Add input",
        "Output materials",
        "+ Add output",
        "Material balance: total input \u2212 total output = loss (water evaporation, rejects, wall sticking and so on). Yield = total output \u00F7 total input \u00D7 100%. A sound process gives a stable yield with explainable losses; abnormal yield swings point to process or metering problems.",
        "\U0001F4DA In-depth analysis: Material Balance (Input-Output) Accounting",
        "Batch production yield accounting",
        "Locating processing losses",
        "Cost and ingredient balance",
        "Yield = total output \u00F7 total input \u00D7 100%; loss amount = total input \u2212 total output; loss rate = loss \u00F7 total input \u00D7 100%.",
        "Input flour 1000 g + sugar 200 g + water 500 g = 1700 g; output product 1500 g + by-product 150 g = 1650 g: yield=1650/1700\u00D7100%\u224897.1% with 2.9% loss (50 g).",
        "Do by-products count as output?",
        "Yes. Yield counts all valuable output; if a by-product is discarded it counts as loss, so keep the basis consistent throughout.",
        "How does this relate to cost?",
        "Input minus output gives the loss, and the loss is hidden cost; material balance is the basis of cost accounting and traceability.",
        "About \"Material Balance Calculator\"",
        "\uFE0F Material Balance (Input-Output) calculator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))


if __name__ == '__main__':
    main()
