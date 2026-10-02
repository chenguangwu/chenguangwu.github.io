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
    write('rc-beam-rebar', build('rc-beam-rebar', [
        "\U0001F4D0 Rectangular beam flexural reinforcement calculation (civil)",
        "Required tension steel area for a singly reinforced rectangular section from the design bending moment.",
        "Rectangular beam flexural reinforcement calculation",
        "Design bending moment M (kN\u00B7m)",
        "\u03BE = 1 \u2212 \u221A(1 \u2212 2\u03B1_s); the singly reinforced upper limit is \u03BE_b \u2248 0.44 (HRB400)",
        "Results are for preliminary estimates only; final design must follow the code and detailing requirements",
        "\U0001F4DA In-depth analysis: rectangular beam flexural reinforcement calculation (civil)",
        "Flexure of a rectangular beam section: given the moment M, solve for the bottom steel As and check \u03BE \u2264 \u03BEb to avoid an over-reinforced brittle section.",
        "Doubly reinforced section: when \u03BE > \u03BEb, add compression steel, or enlarge the section or raise the",
        "concrete grade.",
        "Cracking and deflection: once the strength is satisfied, the service stage still has to be checked.",
        "Flexural reinforcement of a rectangular beam",
        "With b = 200, h = 500, h0 = 465, C30/HRB400 and M = 120 kN\u00B7m: \u03B1s = M/(\u03B1\u2081fc b h0\u00B2) = 120e6/(1.0 \u00D7 14.3 \u00D7 200 \u00D7 465\u00B2) \u2248 0.195, \u03BE = 1\u2212\u221A(1\u22122 \u00D7 0.195) = 0.219 < \u03BEb = 0.518, and As = \u03BEbh0\u03B1\u2081fc/fy = 0.219 \u00D7 200 \u00D7 465 \u00D7 14.3/360 \u2248 808 mm\u00B2. Adopt 3\u03A620 (942).",
        "What if \u03BE > \u03BEb?",
        "The section is over-reinforced and would fail in a brittle, unsafe manner. Enlarge the section, raise the concrete grade, or switch to a doubly reinforced section with compression steel to control the depth of the compression zone. Adding bottom steel alone is not enough.",
        "Why is there a minimum reinforcement ratio?",
        "It prevents a lightly reinforced beam from snapping as soon as it cracks (brittle failure). \u03C1 \u2265 \u03C1min (about 0.2%). Below that ratio, treating the member as plain concrete would in fact be more economical.",
        "What else is checked once the strength is adequate?",
        "Crack width and deflection at the service stage, since excessive values affect durability and appearance. For long spans it is often",
        "deflection",
        "rather than strength that governs the reinforcement.",
    ]))

    write('rebar-anchorage', build('rebar-anchorage', [
        "\U0001F4CF Rebar anchorage length calculation (civil)",
        "Anchorage length from the basic formula using the reinforcement and concrete strengths.",
        "Rebar anchorage length calculation",
        "l_a = \u03B6\u00B7l_ab, corrected for cover in the anchorage zone and other factors",
        "Concrete tensile strength f_t (MPa)",
        "Anchorage correction factor \u03B6_a",
        "l_ab = \u03B1\u00B7\u03B6_a\u00B7(f_y/f_t)\u00B7d, with \u03B1 = 0.14 (the profile coefficient for deformed bars)",
        "Take \u03B6_a = 1.1 when d > 25 mm and 1.25 for epoxy-coated bars, etc.",
        "Tension anchorage length l_a = \u03B6\u00B7l_ab, corrected for cover in the anchorage zone and other factors",
        "\U0001F4DA In-depth analysis: rebar anchorage length calculation (civil)",
        "Beam-column joint anchorage: the longitudinal bars extend into the support by at least laE, and where a straight anchorage is insufficient, use a hooked or mechanical anchorage.",
        "Revisions to the coefficient: deformed bars, thick cover and closely spaced transverse steel allow l_a to be reduced.",
        "Mechanical or welded anchorage: replaces hooks to reduce joint congestion and is checked against the equivalent anchorage length.",
        "Basic anchorage for HRB400",
        "With d = 20 mm, C30 (f_t = 1.43), HRB400 (f_y = 360) and \u03B1 = 0.14: l_a = \u03B1\u00B7(f_y/f_t)\u00B7d = 0.14 \u00D7 (360/1.43) \u00D7 20 \u2248 705 mm. For seismic design l_aE = \u03B6aE\u00B7l_a (with \u03B6aE = 1.15 for seismic grades one and two) \u2248 811 mm.",
        "Why is the seismic anchorage l_aE longer?",
        "Seismic design requires that bars in the plastic hinge region do not slip under repeated loading, so l_a is multiplied by \u03B6aE (1.15 for grades one and two, 1.05 for grade three) to make anchorage more reliable.",
        "Which cases allow l_a to be reduced?",
        "Stirrups in the anchorage zone, thick cover, deformed bars and prestressing all allow a correction factor below 1. Even so, if the straight anchorage is insufficient you must use a hooked or mechanical anchorage.",
        "Is mechanical anchorage enough on its own?",
        "End plates welded to the bar, hooks and similar details with an equivalent projected anchorage length of at least 0.6l_a that meet the detailing requirements are accepted. This shortens anchorage and saves joint space, but follow the standard atlas.",
    ]))

    write('rebar-weight', build('rebar-weight', [
        "\u2696\uFE0F Rebar theoretical weight calculation (civil)",
        "Theoretical weight from bar diameter, length and count using the density \u03C1 = 7850 kg/m\u00B3.",
        "Rebar theoretical weight calculation",
        "Weight per metre = 0.00617 \u00D7 d\u00B2 (kg/m), equivalent to \u03C0/4\u00B7d\u00B2\u00B7\u03C1 with \u03C1 = 7850 kg/m\u00B3",
        "Length per bar L (m)",
        "Number of bars n",
        "Total weight = weight per metre \u00D7 length \u00D7 count",
        "This is the theoretical weight; the permitted deviation of the actual weight is set out in the relevant standard",
        "\U0001F4DA In-depth analysis: rebar theoretical weight calculation (civil)",
        "Material planning: sum the mass by diameter, length and count from the bar bending schedule to get the total and prepare the steel delivery plan.",
        "Waste and joints: add lap and weld waste plus a tonnage margin to the theoretical weight so material does not run short.",
        "Cost estimate: weight times unit price gives the steel cost share, which helps optimise the reinforcement economy.",
        "Weight per metre of \u03A620 rebar",
        "With d = 20 mm: W = 0.00617 \u00D7 d\u00B2 = 0.00617 \u00D7 400 = 2.468 kg/m. Ten bars each 9 m long weigh 2.468 \u00D7 90 \u2248 222 kg in total.",
        "Is the formula the same for deformed and plain round bar?",
        "Both use the nominal diameter in W = 0.00617d\u00B2 (a circular section approximation). The ribs on deformed bar add a little actual section, but quantity take-off uses the nominal diameter and the difference is acceptable in practice.",
        "How different are theoretical and actual weight?",
        "Theoretical weight uses nominal dimensions, so steel with a negative tolerance is slightly lighter in reality. Scheduling and settlement are based mainly on the theoretical weight; weighbridge checks are for reconciling bulk purchases.",
        "How are square and flat bars calculated?",
        "Use volume times density 7.85 g/cm\u00B3: square bar 0.00785a\u00B2 and flat bar 0.00785 \u00D7 width \u00D7 thickness (kg/m). For special sections, look them up in the steel section tables.",
    ]))

    write('rock-mass-rating', build('rock-mass-rating', [
        "\U0001F3CB\uFE0F Rock mass rating RMR calculation (civil)",
        "Rock mass rating total from the Bieniawski RMR method.",
        "Rock mass rating RMR calculation",
        "Rock mass rating RMR calculation: sum the five ratings for uniaxial rock strength, RQD, joint spacing, joint condition and groundwater, then apply the strike and dip correction to obtain the RMR that fixes the rock class. It runs entirely in the browser and is used for tunnel and cavern support design.",
        "Rock strength rating (0-15)",
        "RQD rating (0-20)",
        "Joint spacing rating (0-20)",
        "Joint condition rating (0-25)",
        "Groundwater rating (0-15)",
        "RMR = the sum of the five ratings (100 maximum)",
        "Rating items: rock strength (15) + RQD (20) + joint spacing (20) + joint condition (25) + groundwater (15)",
        "RMR \u2265 81 is class I, decreasing by class",
        "\U0001F4DA In-depth analysis: rock mass rating RMR calculation (civil)",
        "Tunnel and cavern",
        "support design",
        ": use the RMR to set the rock class (I to V) and pick support parameters such as shotcrete with rock bolts and steel ribs.",
        "Compare different joint orientations: when the joint strike is parallel to the tunnel axis with an adverse dip, the correction deducts points and affects the stability class.",
        "Cross-check the exploration report: validate the RMR against the Q system and the BQ method so no single indicator skews the result.",
        "RMR rating and classification",
        "UCS 80 MPa (12 points), RQD 70% (13 points), joint spacing 0.3 m (10 points), fair joint condition (20 points) and damp groundwater (7 points): the sum is 62, the strike correction gives -5, so RMR = 57, class III (fairly good rock). Adopt systematic rock bolts plus mesh and shotcrete.",
        "How does the RMR differ from the Q system?",
        "The RMR is a straightforward score that is easy to use on site, while the Q system is more detailed and includes a stress ratio. The two are related and can be converted, so important projects use both for cross-validation.",
        "How is the strike and dip correction chosen?",
        "The largest deduction applies when the joint strike is parallel to the tunnel axis with a dip of 20-45\u00B0 (most adverse); joints perpendicular to the axis or gently dipping deduct less. Look up the correction table by excavation shape and orientation.",
        "Is the groundwater rating critical?",
        "Yes. Water-bearing weak discontinuities lose shear strength abruptly and can burst or collapse, and the rating differs greatly between damp and pressurised water, directly lowering the class and the support level.",
    ]))


if __name__ == '__main__':
    main()
