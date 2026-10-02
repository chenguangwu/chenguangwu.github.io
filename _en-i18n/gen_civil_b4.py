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
    write('load-combination', build('load-combination', [
        "\u2696\uFE0F Basic load combination calculation (civil)",
        "Design value of the combined effect under the basic combination of the ultimate limit state.",
        "Basic load combination calculation",
        "Dead load effect S_Gk",
        "Variable load effect S_Qk",
        "Partial factor for dead load \u03B3_G",
        "Partial factor for variable load \u03B3_Q",
        "S = \u03B3_G\u00B7S_Gk + \u03B3_Q\u00B7S_Qk (basic combination)",
        "\u03B3_G is usually 1.2 to 1.3 and \u03B3_Q usually 1.4 to 1.5",
        "With several variable loads, take the one with the largest effect as the leading load",
        "\U0001F4DA In-depth analysis: basic load combination calculation (civil)",
        "Frame beam and column design: take combinations such as 1.2D+1.4L (plus 1.4 \u00D7 0.6W or 1.3E) and detail the steel for the most adverse internal force.",
        "Compare dead-load-controlled and live-load-controlled cases: which combination governs shifts with the D/L ratio.",
        "Wind and seismic do not act together: take the more adverse of the two instead of superposing them, which would overestimate internal forces.",
        "Basic dead plus live combination",
        "For a beam end with D = 50 kN\u00B7m and L = 80 kN\u00B7m: the combined M = 1.2D + 1.4L = 1.2 \u00D7 50 + 1.4 \u00D7 80 = 60 + 112 = 172 kN\u00B7m. If wind participates, take 1.2D + 1.4L + 1.4 \u00D7 0.6W, adding another 16.8 kN\u00B7m when W = 20.",
        "What do the 0.6 and 0.9 factors mean?",
        "They are combination values for frequent and quasi-permanent effects of wind or seismic action (such as 0.6W), meaning the load is discounted in the combination because it does not reach its full value at the same time as the live load.",
        "Is one combination always the largest?",
        "Not necessarily. With small live load and large dead load the dead-load-controlled combination is larger. Compute every prescribed combination and take the envelope rather than looking at just one.",
        "Which factors apply to the serviceability combination?",
        "The characteristic combination (partial factors = 1) governs deformation and cracking, while the basic combination (1.2/1.4) governs capacity. They serve different purposes, so do not mix them.",
    ]))

    write('masonry-bearing', build('masonry-bearing', [
        "\U0001F9EE Masonry wall compressive capacity calculation (civil)",
        "Axial compressive capacity from the masonry compressive strength and section area, including the slenderness stability factor.",
        "Masonry wall compressive capacity calculation",
        "Masonry compressive capacity N = \u03C6 \u00D7 f \u00D7 A, where f is the design masonry compressive strength (MPa), A is the wall cross-sectional area (mm\u00B2) and \u03C6 is the capacity influence factor (set by the slenderness ratio \u03B2 = H\u2080 \u00F7 h and the eccentricity; the larger \u03B2 is, the smaller \u03C6). f comes from a table by block and mortar grade (MU10 brick with M5 mortar is about 1.5 MPa). N must not fall below the design load.",
        "Masonry compressive strength f (MPa)",
        "Wall thickness b (mm)",
        "Wall length L (mm)",
        "N = \u03C6\u00B7f\u00B7A (f in N/mm\u00B2 and A in mm\u00B2 give N)",
        "The stability factor \u03C6 is set from a table by the slenderness ratio",
        "Walls with openings should use the net area",
        "\U0001F4DA In-depth analysis: masonry wall compressive capacity calculation (civil)",
        "Load-bearing wall and brick column checks: take the masonry compressive strength f and the slenderness influence factor \u03C6 to obtain the allowable axial force.",
        "Choosing brick and mortar grades: raising MU and M directly raises f, so optimise wall thickness and openings.",
        "Slenderness over the limit: a wall that is too tall becomes unstable and \u03C6 drops, so add piers or reduce the storey height.",
        "Compression check of a load-bearing brick wall",
        "For a 240 mm wall with MU10 brick and M5 mortar, f \u2248 1.5 MPa, \u03C6 = 0.9 and A = 0.24 \u00D7 3 = 0.72 m\u00B2: N \u2264 \u03C6\u00B7f\u00B7A = 0.9 \u00D7 1.5e3 \u00D7 0.72 \u2248 972 kN, adopted after correction for openings and slenderness.",
        "What determines f?",
        "Both the block strength and the mortar strength determine it, and the value corresponds to the lower of the two. Mortar grade has a noticeably larger effect than small changes in brick grade.",
        "How does the slenderness ratio affect the result?",
        "The larger the slenderness ratio \u03B2, the smaller the stability factor \u03C6 and the lower the capacity. A wall over the limit behaves like a slender column and can buckle, so add construction columns and ring beams or reduce the height.",
        "How is eccentric compression handled?",
        "Eccentricity makes the section stress uneven, so reduce the capacity by e/h and check local compression. Large eccentricity requires a larger section or intermediate piers.",
    ]))

    write('one-way-slab', build('one-way-slab', [
        "\U0001F9EE One-way slab reinforcement calculation (civil)",
        "Tension steel area for a unit-width one-way slab from the bending moment.",
        "One-way slab reinforcement calculation",
        "Moment per metre M (kN\u00B7m/m)",
        "Slab thickness h (mm)",
        "\u03B1_s = M/(\u03B1\u2081\u00B7f_c\u00B7b\u00B7h\u2080\u00B2), with b = 1000 mm (a unit-width strip)",
        "\u03BE = 1\u2212\u221A(1\u22122\u03B1_s); the singly reinforced upper limit is \u03BE_b \u2248 0.44",
        "\U0001F4DA In-depth analysis: one-way slab reinforcement calculation (civil)",
        "Residential one-way slabs (long side / short side \u2265 2): provide bottom steel for the short-span moment and distribution steel for the long span.",
        "Continuous slabs use plastic or elastic coefficients: the negative moment at an interior support exceeds the mid-span value, so use split or bent-up reinforcement.",
        "Minimum reinforcement ratio and cracking: thin slabs must satisfy \u03C1min and limit the bar spacing to control cracking.",
        "Mid-span reinforcement of a 3 m one-way slab",
        "With h = 100, h0 = 80, q = 8 kN/m\u00B2 and L = 3 m: M = ql\u00B2/8 = 8 \u00D7 9/8 = 9 kN\u00B7m/m. For C25 with HRB400, \u03B1s = M/(\u03B1\u2081fc b h0\u00B2) \u2248 0.043, \u03BE \u2248 0.044 and As = \u03BE\u00B7b\u00B7h0\u00B7\u03B1\u2081\u00B7fc/fy \u2248 0.044 \u00D7 1000 \u00D7 80 \u00D7 11.9/360 \u2248 117 mm\u00B2/m, so adopt \u03A68@200 (251).",
        "How do you tell a one-way slab from a two-way slab?",
        "A long-to-short side ratio \u2265 2 makes it a one-way slab (short span carries the load); below 2 it is two-way (both directions act). Misjudging it changes the reinforcement direction and leaves the member under-reinforced.",
        "What is the minimum reinforcement ratio?",
        "For flexural slabs \u03C1min \u2248 0.15% (HRB400) is common, with at least construction steel of the \u03A68@200 order per metre to control shrinkage and temperature cracking.",
        "Why is there more negative steel at the supports of a continuous slab?",
        "The support negative moment of a continuous slab is often larger than the mid-span positive moment, and the negative steel (top layer) carries the support tension. Split reinforcement therefore needs top bars at the supports and bottom bars at mid-span.",
    ]))

    write('pile-capacity', build('pile-capacity', [
        "\U0001F9EE Single pile vertical capacity calculation (civil)",
        "Characteristic vertical capacity of a single pile from empirical formulas for shaft friction and base resistance.",
        "Single pile vertical capacity calculation",
        "Average shaft friction q_s (kPa)",
        "Base resistance q_p (kPa)",
        "A_p = \u03C0d\u00B2/4 is the pile base area and u = \u03C0d is the pile perimeter",
        "The safety factor K is usually taken as 2 (to convert the standard value into a characteristic value)",
        "Shaft and base resistance should come from the geotechnical report; this tool is an empirical estimate",
        "\U0001F4DA In-depth analysis: single pile vertical capacity calculation (civil)",
        "Bored piles: multiply the layer-by-layer shaft friction qsi by the pile segment length and accumulate, then add the base resistance to obtain the ultimate capacity of the single pile.",
        "Per the code characteristic value: divide Quk by the safety factor 2 to get Ra, which is used to distribute the superstructure load.",
        "Negative skin friction and weak underlying layers: under-consolidated soil alongside the pile produces a downdrag load, or the toe lands on a weak layer that must be penetrated.",
        "Vertical capacity of a bored pile",
        "With D = 0.8 m, L = 15 m, uniform shaft friction 40 kPa and base resistance qp = 2000 kPa: Qs = \u03C0 \u00D7 0.8 \u00D7 15 \u00D7 40 \u2248 1508 kN, Qp = \u03C0 \u00D7 0.4\u00B2 \u00D7 2000 \u2248 1005 kN, Quk \u2248 2513 kN and Ra \u2248 1256 kN.",
        "How far apart are empirical formulas and a static load test?",
        "Empirical formulas are strongly affected by scatter in the soil parameters, so important projects should take Ra from a static load test. The formulas serve only for preliminary sizing and layout reference.",
        "What is negative skin friction?",
        "Under-consolidated soil beside the pile settles and applies downward friction to the pile, increasing the load. Collapsible soils, fill and zones with a falling groundwater table must include the downdrag load.",
        "What is the difference between end-bearing and friction piles?",
        "An end-bearing pile relies mainly on a hard layer at the toe while a friction pile relies on shaft friction. Pile length and bearing layer selection strategies differ, and so does the focus of settlement control.",
    ]))


if __name__ == '__main__':
    main()
