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
    write('quick-freeze-time', build('quick-freeze-time', [
        "\U0001F52E Quick Freezing Time Estimator",
        "Estimate the time a food takes to pass through the maximum ice crystal formation zone using the Plank equation",
        " / Quick Freezing Time Estimate",
        "\U0001F4D6 See the \"Quick Freezing Time Estimation User Guide\"",
        "Food shape",
        "Slab (freezes through the thickness)",
        "Cylinder (freezes radially)",
        "Sphere (freezes radially)",
        "Characteristic dimension d (mm)",
        "Thickness for a slab, diameter for a cylinder or sphere",
        "Food freezing point T_f (\u00B0C)",
        "Refrigerant temperature T\u221E (\u00B0C)",
        "Surface heat transfer coefficient h (W/m\u00B2\u00B7K)",
        "Natural convection about 5-20, forced air about 20-100, contact freezing about 100-500, liquid nitrogen spray 500+",
        "Latent heat of the phase change \u03BB (kJ/kg)",
        "Approximated as water fraction \u00D7335 (kJ/kg); at 80% water content about 230",
        "Food density \u03C1 (kg/m\u00B3)",
        "Thermal conductivity in the frozen state k (W/m\u00B7K)",
        "Typically 1.0-2.0 for frozen foods",
        "Plank equation: t = (\u03C1 \u03BB / (T_f \u2212 T\u221E)) \u00D7 (P\u00B7d / h + R\u00B7d\u00B2 / k). Shape factors: slab P=1/2, R=1/8; cylinder P=1/4, R=1/16; sphere P=1/6, R=1/24. This covers the phase-change freezing time only, without pre-cooling or supercooling. Quick freezing requires passing the \u22121 to \u22125\u00B0C maximum ice crystal zone in under 30 minutes.",
        "\U0001F4DA In-depth analysis: Quick Freezing Time Estimation",
        "Quick freezing lines",
        "Capacity planning",
        "Judging the ice refinement process",
        "Frozen storage quality design",
        "Phase-change freezing time t = (\u03C1\u00B7L/\u0394T)\u00B7(P\u00B7d/h + R\u00B7d\u00B2/k), with \u0394T = initial food temperature minus refrigerant temperature and P, R the shape factors (slab 0.5/0.125, cylinder 0.25/0.0625, sphere 1/6/1/24).",
        "For a 50mm-thick slab starting at \u22121.5\u00B0C in a \u221235\u00B0C medium (h=50 W/m\u00B2\u00B7K, \u03C1=1000, L=230 kJ/kg, k=1.5): \u0394T=33.5\u00B0C and t\u224881.0 min, which is ordinary freezing with large ice crystals, so raise the air speed or lower the temperature.",
        "How long counts as quick freezing?",
        "It is judged by a short time for the centre to pass the maximum ice crystal zone (\u22121 to \u22125\u00B0C) and for the centre to reach \u221218\u00B0C; under 30 min is a good quick freeze.",
        "How do I choose the shape factors?",
        "Take P and R from the geometry of the smallest dimension; the thickness d dominates, so thinning the product and raising h (air speed and temperature difference) shorten the time most.",
        "About \"Quick Freezing Time Estimator\"",
        "The Quick Freezing Time Estimator is an online tool in the field of food and cooking. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))

    write('smoking-concentration', build('smoking-concentration', [
        "\U0001F9EA Smoking Concentration (Benzo[a]pyrene) Simulator",
        "Estimate the phenolic concentration in a smoking chamber and benzo[a]pyrene exposure risk to support process optimisation",
        "Smoking Concentration Simulator",
        " / Smoking Concentration Simulation",
        "\U0001F4D6 See the \"Smoking Concentration (Benzo[a]pyrene) Simulation User Guide\"",
        "Total smoke produced (g) = wood chips \u00D7 smoke yield (%) \u00F7 100 \u00D7 time, and never more than 70% of the wood chip weight; phenolic concentration in the chamber = total smoke \u00D7 phenolic share \u00F7 ventilation volume (volume \u00D7 air changes \u00D7 time); benzo[a]pyrene formation rises sharply with temperature, so keep the smoking temperature at 60 to 80 \u00B0C (staying below 300 \u00B0C markedly reduces it); the risk grade is judged by comparing the concentration with the limit (the benzo[a]pyrene limit for smoked meat products is 5 \u03BCg/kg).",
        "Smoking chamber volume (m\u00B3)",
        "Wood chip usage (g)",
        "Wood chip smoke yield (g smoke/min per 100g wood chips)",
        "Smoke produced per minute per unit mass of wood chips (empirical)",
        "Phenolic share of the smoke (%)",
        "Phenolics in hardwood smoke condensate are about 5-15%",
        "Smoking time (min)",
        "Air change rate (changes/h)",
        "More air changes lower the concentration but may increase benzo[a]pyrene deposition; traditional closed smoking runs high",
        "Smoking temperature (\u00B0C)",
        "The higher the temperature the more polycyclic aromatic hydrocarbons (including benzo[a]pyrene) form",
        "This tool gives a rough estimate from an empirical model and is for process reference only. Benzo[a]pyrene (BaP) is a carcinogen, and GB 2762 sets a limit of 5 \u03BCg/kg or less for smoked meat products. Ways to lower BaP: use a liquid smoke preparation instead, keep the temperature under 200\u00B0C, stop fat dripping onto open flame, shorten the smoking time and add filtration.",
        "\U0001F4DA In-depth analysis: Smoking Concentration (Benzo[a]pyrene) Simulation",
        "Optimising smoking time and temperature",
        "Controlling benzo[a]pyrene exposure risk",
        "Exhaust and ventilation design",
        "Phenolic concentration \u2248 phenol production rate \u00F7 ventilation flow (phenol = smoke \u00D7 phenolic share; smoke is limited by the wood chip amount); benzo[a]pyrene rises with the temperature factor (sharply above 200\u00B0C).",
        "For a 2 m\u00B3 chamber, 300 g wood chips, 5% yield, 120 min, 8% phenolic share, 3 air changes per hour at 60\u00B0C: steady-state phenolics are about 1400 mg/m\u00B3 and benzo[a]pyrene about 1.4 \u03BCg/m\u00B3 (low risk at low temperature); raising it to 300\u00B0C increases benzo[a]pyrene by orders of magnitude.",
        "How do I control benzo[a]pyrene?",
        "Keep the smoke temperature under 200\u00B0C (avoid direct flame roasting), raise the ventilation, shorten the smoking time, use clean smoke generation, and consider liquid smoke instead.",
        "Are high phenolics good or bad?",
        "Phenolics give the characteristic smoked flavour but come with harmful compounds, so balance flavour against food safety and do not overdose.",
        "About \"Smoking Concentration Simulator\"",
        "The Smoking Concentration (benzo[a]pyrene) simulator. A food and cooking tool that helps you master ingredient ratios and nutrition precisely.",
    ]))


if __name__ == '__main__':
    main()
