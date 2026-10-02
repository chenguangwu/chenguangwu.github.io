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

DISCL_C = " A professional civil engineering tool based on authoritative structural codes, for reference only."


def main():
    write('concrete-volume', build('concrete-volume', [
        "\U0001F4D0 Concrete member volume calculation (civil)",
        "Concrete volume and mass from member dimensions (length \u00D7 width \u00D7 height, or cross-sectional area \u00D7 length).",
        "Concrete member volume calculation",
        "Length a (m)",
        "Width b (m)",
        "Height/thickness c (m)",
        "Concrete density (kg/m\u00B3)",
        "Normal concrete is about 2400 kg/m\u00B3 (the C20 to C40 range)",
        "Results are for quantity take-off; the drawings and measurement rules govern",
        "\U0001F4DA In-depth analysis: concrete member volume calculation (civil)",
        "Quantity take-off for pile caps and ground beams: the rectangular volume is length \u00D7 width \u00D7 height, less the voids occupied by pile heads and embedded parts.",
        "Floor slabs: thickness \u00D7 area, with composite beams accumulated from the net section, used to order ready-mix concrete by truck.",
        "Waste and allowance: add 1-2% for actual placement and allow for pump line residue and test cubes, so you do not run short.",
        "Volume of an isolated footing",
        "For a rectangular footing 2.0 \u00D7 2.0 \u00D7 0.5 m with no voids: V = 2 \u00D7 2 \u00D7 0.5 = 2.0 m\u00B3. With 1.5% waste order 2.03 m\u00B3, and add about 0.4 m\u00B3 for a 0.1 m blinding layer.",
        "How do volume and formwork area relate?",
        "They are unrelated: volume is used for",
        "ordering concrete, while formwork area is used for shoring. Both come from the dimensions but they serve different purposes, so do not mix them up.",
        "What waste rate is typical?",
        "Cast-in-place structures usually take 1-2%, a little more for pumped concrete and irregular members. Follow the company quota and crew skill level: too much wastes material, too little interrupts the pour.",
        "How do I calculate a sloped member?",
        "Split it into frusta or wedges and use the frustum formula V = h/3(S1+S2+\u221A(S1S2)), or approximate in segments. A steep slope cannot simply be taken at the average thickness.",
    ]))

    write('concrete-wb-ratio', build('concrete-wb-ratio', [
        "\U0001F9EE Concrete water-binder ratio calculation (civil)",
        "Water-binder ratio W/B from the target strength and the binder strength using the Bolomey formula.",
        "Concrete water-binder ratio calculation",
        "Binder strength at 28 d f_b (MPa)",
        "Coefficient \u03B1_a",
        "Coefficient \u03B1_b",
        "Bolomey formula: W/B = \u03B1_a\u00B7f_b / (f_cu,0 + \u03B1_a\u00B7\u03B1_b\u00B7f_b)",
        "For ordinary Portland cement \u03B1_a \u2248 0.53 and \u03B1_b \u2248 0.20",
        "The result is a theoretical water-binder ratio; it must still satisfy the durability maximum",
        "\U0001F4DA In-depth analysis: concrete water-binder ratio calculation (civil)",
        "Back-calculate the allowable maximum water-binder ratio from the trial strength, then fix the final value against durability and workability.",
        "With fly ash or slag blended in, the water-binder ratio counts the total binder (cement plus admixture), not cement alone.",
        "Evaluate the water-reducing effect of admixtures: at the same water-binder ratio, cutting the water content improves workability.",
        "Back-calculated W/B for C30",
        "With fcu = 38.2 MPa (trial), cement fb = 42.5 MPa, \u03B1a = 0.53 and \u03B1b = 0.20: w/b = 0.53 \u00D7 42.5 / (38.2 + 0.53 \u00D7 0.20 \u00D7 42.5) \u2248 22.5/42.7 \u2248 0.527. Taking 0.50 satisfies durability better.",
        "Are the water-binder ratio and the water content the same thing?",
        "No. The water-binder ratio is water divided by (cement plus admixture), while the water content only affects workability. Cutting water content does not change the ratio; lowering the ratio requires cutting water or adding binder at the same time.",
        "How are admixtures counted?",
        "The denominator of the water-binder ratio uses the total binder (cement plus active admixtures such as fly ash or slag). Looking at cement alone gives a wrong result and a lower actual strength.",
        "Is the maximum water-binder ratio mandatory?",
        "Yes, it is the durability floor (frost, impermeability, chloride resistance). Even when the strength is sufficient it must not exceed the value for the exposure class, otherwise the service life falls short.",
    ]))

    write('excavation-earth', build('excavation-earth', [
        "\U0001F39A\uFE0F Excavation active earth pressure estimate (civil)",
        "Active earth pressure resultant on a vertical excavation face using Rankine theory.",
        "Excavation active earth pressure estimate",
        "Excavation depth H (m)",
        "Ground surcharge q (kPa)",
        "With surcharge q, E_a = \u00BD\u03B3H\u00B2K_a + qHK_a",
        "The support structure should be designed for this earth pressure",
        "\U0001F4DA In-depth analysis: excavation active earth pressure estimate (civil)",
        "Deep excavations for metro or basement projects: compute Ka layer by layer down the depth and add the ground surcharge q, giving a trapezoidal pressure distribution on the retaining structure.",
        "Strut axial force estimate: take the earth pressure resultant for a stage and distribute it across the struts to get each strut force.",
        "Water level and dewatering: the choice between separate and combined soil-water calculation changes the earth pressure, so be careful in soft ground.",
        "Earth pressure distribution for a uniform soil excavation",
        "With \u03B3 = 19 kN/m\u00B3, \u03C6 = 20\u00B0, c = 10 kPa, H = 8 m and surcharge q = 20 kPa: Ka \u2248 0.49. The surcharge adds p = Ka\u00B7q \u2248 9.8 kPa at the top and pa \u2248 Ka\u00B7\u03B3H \u2212 2c\u221AKa + Ka\u00B7q \u2248 0.49 \u00D7 19 \u00D7 8 \u2212 2 \u00D7 10 \u00D7 0.7 + 9.8 \u2248 64 kPa at the base, a trapezoidal distribution.",
        "Separate or combined soil-water calculation?",
        "Sandy and silty soils are usually calculated separately with water pressure listed on its own. Cohesive soils are often combined using the submerged unit weight. The wrong choice either over- or under-estimates the lateral pressure.",
        "How is the surcharge added?",
        "Multiply the ground surcharge q by Ka to get an additional uniform pressure superposed on the earth pressure at every depth. Piling material close to the excavation edge is especially dangerous.",
        "Does the number of struts affect the earth pressure?",
        "It does not change the pressure distribution itself, but it affects how much each strut carries and the deflection. More struts reduce the axial force per strut and the wall movement.",
        "How to use the excavation active earth pressure estimate (civil)",
        "An earth pressure estimate for deep excavation support design in basements and metro projects: enter soil parameters, wall height and surcharge to get the pressure distribution and resultant acting on the secant piles or diaphragm wall, which helps size strut forces and embedment depth. Choose separate or combined soil-water calculation according to the soil type.",
        "What is the excavation active earth pressure estimator (civil) for?",
        "An estimator that computes the active earth pressure resultant on a vertical excavation face using Rankine theory, for excavation support design.",
        "How do I use the excavation active earth pressure estimate (civil)?",
        "Which scenarios suit the excavation active earth pressure estimate (civil)?",
    ]))

    write('isolated-footing', build('isolated-footing', [
        "\U0001F4D0 Isolated footing base area calculation (civil)",
        "Base dimensions of an isolated footing from the column axial force and moment, checked against the soil bearing capacity.",
        "Isolated footing base area calculation",
        "Column axial force N (kN)",
        "Soil bearing capacity f_a (kPa)",
        "Average unit weight of footing and soil (kN/m\u00B3)",
        "Footing embedment depth d (m)",
        "Footing side length B (m)",
        "Average base pressure p = (N + \u03B3\u00B7A\u00B7d) / A",
        "Under eccentricity p_max/min = p \u00B1 M / W, where W = B\u00B3/6 (square footing)",
        "Check condition: p_max \u2264 1.2f_a and p_min \u2265 0",
        "This tool assumes a square footing; calculate rectangular footings separately",
        "\U0001F4DA In-depth analysis: isolated footing base area calculation (civil)",
        "Frame column footings: with the axial force N and the bearing capacity characteristic value f_a of the bearing layer known, solve for the base dimensions so pmax \u2264 f_a and the average p \u2264 f_a.",
        "Embedment correction: the deeper the footing, the higher the bearing capacity, which can shrink the base but adds excavation.",
        "Eccentric loading: recheck the edge pressure with pkmax = N/A + M/W to avoid lift-off on one side.",
        "Isolated footing under axial compression",
        "For column N = 800 kN, f_a = 200 kPa, embedment d = 1.5 m and soil \u03B3 = 18 kN/m\u00B3: A \u2248 N/(f_a \u2212 \u03B3d) = 800/(200 \u2212 18 \u00D7 1.5) = 800/173 \u2248 4.62 m\u00B2. Take 2.2 \u00D7 2.2 = 4.84 m\u00B2, giving an average p \u2248 165 kPa < 200 kPa, which satisfies the check.",
        "Do both the average and the maximum pressure need checking?",
        "Yes. Under axial load the average p \u2264 f_a governs; under eccentric load you also need pkmax \u2264 1.2f_a with no lift-off (pkmin > 0). Corner lift-off means the base is too large or the eccentricity too high.",
        "When does punching shear govern?",
        "When the base is large enough but the punching check around the column fails. Then thicken the footing or add a pedestal. Punching and bending reinforcement are the two independent governing checks for an isolated footing.",
        "Does the bearing capacity need depth and width corrections?",
        "It depends on the soil and the footing width; for cohesive soil the width correction factor may be taken as 0. Per GB 50007, correct f_a with \u03B7b, \u03B7d and the embedment depth.",
    ]))


if __name__ == '__main__':
    main()
