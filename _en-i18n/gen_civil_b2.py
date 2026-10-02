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
    write('calc-2', build('calc-2', [
        "\U0001F4CF Rebar cut length calculation",
        "Cut length from the overall outside dimensions, bend angles and bend inner radius, automatically deducting the measurement deduction and adding the hook length.",
        "D = coefficient \u00D7 d,",
        "Straight segment length L\u2081 (mm)",
        "Straight segment length L\u2082 (mm)",
        "Rebar diameter d (mm)",
        "Bend angle \u03B8\u2081 (\u00B0)",
        "Bend angle \u03B8\u2082 (\u00B0)",
        "Bend inner radius coefficient",
        "Hook type",
        "No hook",
        "180\u00B0 semicircular hook",
        "135\u00B0 slanted hook",
        "90\u00B0 standard hook",
        "Cover thickness c (mm)",
        "Calculate the cut length",
        "Measurement deduction \u0394 = (D/2 + d) \u00D7 \u03B8_rad \u2212 (D/2 + d) \u00D7 sin(\u03B8_rad), where D is the bend inner diameter",
        "A 180\u00B0 semicircular hook adds about 6.25d; a 135\u00B0 slanted hook about 4.9d; a 90\u00B0 standard hook about 3.5d",
        "Cut length = sum of outside dimensions \u2212 measurement deduction + hook addition",
        "Bend inner diameter D = coefficient \u00D7 d; this tool defaults to 2.5d",
        "\U0001F4DA In-depth analysis: rebar cut length calculation",
        "Bar bending schedule for longitudinal and stirrup reinforcement: outside dimensions minus the 90\u00B0/135\u00B0 bend adjustment, plus the hook increment, gives the actual cut length.",
        "Bent bars such as canopies and cantilevers: look up the bend adjustment from the bend diameter D and bar diameter d so the finished piece is not too short.",
        "Batch cutting optimisation: nest the stock lengths of 9 m and 12 m to reduce joints and offcuts.",
        "Cut length adjustment for a 90\u00B0 hook",
        "For a 3000 mm straight outside dimension with a 90\u00B0 hook at the end (D = 5d, d = 20 mm): the bend adjustment \u2248 2 \u00D7 the outer-skin increment, so a single bend deducts about 2d = 40 mm. Adding the hook growth gives a net cut length \u2248 3000 \u2212 40 + hook increment, taken from the bar bending schedule table.",
        "Where does the bend adjustment come from?",
        "From the geometric difference between tension of the outer skin and compression of the inner skin at the bend, which depends on the bend centre diameter D and d (roughly 2d at 90\u00B0, 3d at 135\u00B0). Take it from 16G101 or the manufacturer's table.",
        "How much does a 180\u00B0 hook add?",
        "For plain round bars (HPB300) a 180\u00B0 end hook adds about 6.25d including the straight tail; it can be ignored when mechanical anchorage or welding is used.",
        "What are the consequences of an over-length or short cut?",
        "Too long wastes steel and clashes at the joint; too short gives insufficient anchorage and weakens the member. Bar bending schedules must balance cover, laps and anchorage, and leave an allowance for measurement tolerance.",
    ]))

    write('carbonation-depth', build('carbonation-depth', [
        "\U0001F4CF Concrete carbonation depth estimate (civil)",
        "Estimate the carbonation depth of concrete for a given service life using the square-root diffusion law.",
        "Concrete carbonation depth estimate",
        "x = 2.56\u00B7K\u00B7\u221At (K is the carbonation rate coefficient)  K is affected by concrete strength, curing and ambient humidity  Reinforcement starts to corrode once carbonation reaches the cover thickness",
        "Carbonation coefficient K (mm/\u221Aa)",
        "Service life t (years)",
        "Common model: x = 2.56\u00B7K\u00B7\u221At (K is the carbonation rate coefficient)",
        "K is affected by concrete strength, curing and ambient humidity",
        "Reinforcement starts to corrode once carbonation reaches the cover thickness",
        "\U0001F4DA In-depth analysis: concrete carbonation depth estimate (civil)",
        "Durability assessment of existing buildings: use the exposure class and the measured carbonation rate to project the depth several years ahead and judge when it approaches the cover.",
        "Compare how the water-binder ratio and admixtures affect k, to demonstrate",
        "high-performance carbonation resistance.",
        "Combine with rebar corrosion risk: when carbonation reaches the bar surface in the presence of chlorides, corrosion accelerates, so a maintenance interval must be set.",
        "Carbonation depth after 20 years",
        "With a carbonation coefficient k = 1.0 mm/\u221Aa (ordinary C30 outdoors) and t = 20 a: x = k\u00B7\u221At = 1.0 \u00D7 \u221A20 \u2248 4.5 mm. With a 25 mm cover the bar is not reached in the near term, but members with thin cover need close attention.",
        "What affects k the most?",
        "The water-binder ratio (larger ratio means larger k), admixtures (fly ash and slag reduce porosity and lower k), and curing and humidity. Indoors k is far smaller than in alternating wet-dry exposure.",
        "Does carbonation reaching the bar always mean it corrodes?",
        "Carbonation lowers the pore solution pH and breaks down the passive film, but whether corrosion occurs also depends on moisture and chlorides. Reaching the bar surface is the risk threshold, not a certainty.",
        "How is carbonation depth measured on site?",
        "Take a core or spray phenolphthalein on a fresh section: the uncarbonated zone turns pink while the carbonated zone does not, and the distance from the colour boundary to the surface is the carbonation depth.",
    ]))

    write('cft-capacity', build('cft-capacity', [
        "\U0001F52E Concrete-filled steel tube axial capacity estimate (civil)",
        "Axial compressive capacity of a circular concrete-filled steel tube short column using a simplified superposition model.",
        "Concrete-filled steel tube axial capacity estimate",
        "N = A_s\u00B7f_y + 1.2\u00B7A_c\u00B7f_c (confinement enhancement included, conservative)  In practice compute the confined concrete constitutive law per the code",
        "Steel tube outer diameter D (mm)",
        "Steel tube wall thickness t (mm)",
        "Core concrete f_c (MPa)",
        "Steel f_y (MPa)",
        "A_c and A_s are the cross-sectional areas of the core concrete and the steel tube respectively",
        "The capacity is taken as N = A_s\u00B7f_y + 1.2\u00B7A_c\u00B7f_c (confinement enhancement included, conservative)",
        "In practice compute the confined concrete constitutive law per the code",
        "\U0001F4DA In-depth analysis: concrete-filled steel tube axial capacity estimate (civil)",
        "For high-rise or bridge heavy-load columns: use a steel tube to",
        "raise axial capacity and ductility, replacing an equal-section RC column with a smaller section.",
        "Compare the contributions of the hollow tube and the core concrete: the confinement effect varies with steel ratio and diameter-to-thickness ratio, so optimise the tube diameter and wall thickness.",
        "Construction stage check: before pouring the tube carries the load alone and afterwards the composite section does, so check each stage separately.",
        "Axial estimate for a circular concrete-filled steel tube",
        "With D = 500 mm, t = 12 mm, C40 and Q345: Ac \u2248 0.187 m\u00B2 and As \u2248 0.0184 m\u00B2. Taking fck = 26.8 MPa and fy = 345 MPa, N0 \u2248 fck\u00B7Ac + fy\u00B7As \u2248 26.8e3 \u00D7 0.187 + 345e3 \u00D7 0.0184 \u2248 5.0 + 6.35 \u2248 11.4 MN (before multiplying by the confinement enhancement factor).",
        "Why is it stronger than an RC column?",
        "The tube confines the core concrete in triaxial compression, raising both strength and ductility, and the tube doubles as formwork and longitudinal reinforcement, which speeds construction.",
        "How is the confinement factor chosen?",
        "It depends on the steel ratio, steel yield strength and the section shape (circular or square); circular tubes confine better than square ones. Determine it from the code formula or tests \u2014 this tool gives an approximation.",
        "How are eccentric and large-eccentric compression handled?",
        "This axial estimate suits small eccentricity only. Large eccentric compression needs the composite section N-M interaction curve; treat the tool result as preliminary and use the code formulas for final design.",
        "How to use the concrete-filled steel tube axial capacity estimate (civil)",
        "A quick axial capacity estimate for heavy-load columns in high-rise and bridge structures: enter the tube diameter, wall thickness, steel grade and concrete grade to get the composite axial capacity and compare it with an RC column to help pick the section. Final design must still be checked against the code formulas and detailing requirements.",
        "What is the concrete-filled steel tube axial capacity estimator (civil) for?",
        "A concrete-filled steel tube axial capacity estimator that computes the axial compressive capacity of a circular CFST short column with a simplified superposition model to support member design.",
        "How do I use the concrete-filled steel tube axial capacity estimate (civil)?",
        "Which scenarios suit the concrete-filled steel tube axial capacity estimate (civil)?",
    ]))


if __name__ == '__main__':
    main()
