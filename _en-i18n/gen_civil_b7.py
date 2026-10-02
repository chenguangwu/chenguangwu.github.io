#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'civil')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'civil')
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
    out = {'slug': slug, 'industry': 'civil', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3


def main():
    write('index', build('index', [
        "\U0001F3D7\uFE0F Civil engineering tools",
        "Civil engineering",
        "Civil engineering tools",
        "Rock mass rating RMR calculation",
        "Enter rock strength, RQD and joint parameters and compute the RMR total with the Bieniawski rock mass rating method to classify the rock, informing support scheme decisions for tunnels and underground works.",
        "Isolated footing base area calculation",
        "Enter the column axial force, moment and soil bearing capacity to compute the isolated footing base dimensions and check the maximum and minimum base pressures, ensuring no tensile stress and controllable settlement for structural design.",
        "One-way slab reinforcement calculation",
        "A one-way slab reinforcement calculator that derives the tension steel area per unit width from the moment, for reinforced concrete one-way slab design.",
        "Infinite slope stability factor calculation",
        "An infinite slope stability factor calculator that estimates the factor of safety Fs of a long uniform slope with a simplified slice method, for slope stability assessment.",
        "Concrete water-binder ratio calculation",
        "A concrete water-binder ratio calculator that solves W/B from the target strength and binder strength using the Bolomey formula, ensuring strength while controlling cement content.",
        "Rectangular beam flexural reinforcement calculation",
        "A rectangular beam flexural reinforcement calculator that derives the required tension steel area from the design moment for a singly reinforced rectangular section, for beam detailing.",
        "Rebar anchorage length calculation",
        "A rebar anchorage length calculator that derives the anchorage length from the reinforcement and concrete strengths using the basic anchorage formula, ensuring reliable anchorage.",
        "Rankine active earth pressure calculation",
        "Active earth pressure resultant and critical depth on a vertical wall back for cohesionless or cohesive backfill, using Rankine theory.",
        "Simply supported beam under uniformly distributed load",
        "Enter the span, section stiffness and uniformly distributed load of a simply supported beam to compute the maximum moment, shear, mid-span deflection and bending stress, for structural verification and preliminary beam sizing.",
        "Concrete member volume calculation",
        "A concrete member volume calculator that computes volume and mass from length \u00D7 width \u00D7 height or cross-sectional area \u00D7 length, for quantity take-off and material planning.",
        "Masonry wall compressive capacity calculation",
        "Enter the masonry strength, wall dimensions and loads to compute the compressive capacity of a masonry wall per the code, for brick-concrete structure design and safety checks.",
        "Basic load combination calculation",
        "A basic load combination calculator that returns the design value of the combined effect under the ultimate limit state basic combination, for structural member design.",
        "Rebar theoretical weight calculation",
        "Theoretical weight from bar diameter, length and count using the density \u03C1 = 7850 kg/m\u00B3.",
        "Wind load characteristic value calculation",
        "A wind load characteristic value calculator that returns the wind load normal to the building surface per the load code, for structural wind design.",
        "Single pile vertical capacity calculation",
        "A single pile vertical capacity calculator that estimates the characteristic value from empirical shaft and base resistance formulas, for pile foundation design and verification.",
        "Cut length from the overall outside dimensions, bend angles and bend inner radius, automatically deducting the measurement deduction and adding the hook length.",
        "Enter the strength grade, aggregate parameters and water content to compute the mass ratio of cement, sand, coarse aggregate and water, for concrete mix design and construction proportioning.",
        "Two-way slab moment estimate",
        "A two-way slab moment calculator that estimates the moments in the short and long span directions using the empirical coefficients of elastic theory, for two-way slab reinforcement design.",
        "Concrete carbonation depth estimate",
        "A concrete carbonation depth calculator that estimates the depth for a given service life using the square-root diffusion law, assessing rebar corrosion risk and durability.",
        "Concrete-filled steel tube axial capacity estimate",
        "A concrete-filled steel tube axial capacity calculator that estimates the axial compressive capacity of a circular CFST short column with a simplified superposition model, supporting member design.",
        "Excavation active earth pressure estimate",
        "An excavation active earth pressure calculator that estimates the active earth pressure resultant on a vertical face using Rankine theory, for excavation support design.",
        "About the Civil engineering tools",
        "This collection brings together 21 free online tools covering the common calculation, conversion and lookup needs of civil engineering. Whether you are a practitioner, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and uploads no data, so your privacy is protected.",
        "The civil engineering tools collected on this page include (a few representative tools):",
        "These tools help you finish common civil engineering tasks quickly, with no need to memorize formulas or convert by hand \u2014 enter the input and you get the result.",
        "Do the civil engineering tools require a download or registration?",
        "No. Every tool on this page runs entirely in the browser: open the page and start using it. No software to install, no account to create, and no data is uploaded.",
        "Are the results accurate, and is my data safe?",
        "The tools compute locally in your browser using public mathematical formulas and general industry standards, so results appear instantly. All computation happens on your own device and no data is uploaded to any server, so your privacy is protected.",
    ]))


if __name__ == '__main__':
    main()
