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
    write('slope-stability-fos', build('slope-stability-fos', [
        "\U0001F9EE Infinite slope stability factor calculation (civil)",
        "Factor of safety Fs for an infinite slope using a simplified slice approach.",
        "Infinite slope stability factor calculation",
        "Slip surface depth z (m)",
        "Slope angle \u03B1 (\u00B0)",
        "Infinite slope: F_s = (c + \u03B3z\u00B7cos\u00B2\u03B1\u00B7tan\u03C6) / (\u03B3z\u00B7sin\u03B1\u00B7cos\u03B1)",
        "Ordinary engineering practice requires F_s \u2265 1.3 (permanent slopes)",
        "Suited to preliminary estimates for homogeneous, long uniform slopes",
        "\U0001F4DA In-depth analysis: infinite slope stability factor calculation (civil)",
        "Road cuttings and excavation batters: compute Fs from the soil c', \u03C6', slope angle \u03B2; only Fs \u2265 1.3 to 1.5 is safe.",
        "Groundwater effect: pore water pressure u reduces the effective stress and lowers Fs markedly, so dewatering or a flatter slope is needed.",
        "Comparing flatter slopes: reducing \u03B2 raises Fs quickly, so balance the earthworks volume against safety.",
        "Factor of safety of an infinite slope",
        "With \u03B3 = 19, c' = 10 kPa, \u03C6' = 25\u00B0, \u03B2 = 30\u00B0, z = 5 m and u = 0: Fs = (c'/(\u03B3z cos\u00B2\u03B2 tan\u03C6')) + (1)tan\u03C6'/tan\u03B2 = (10/(19 \u00D7 5 \u00D7 0.75 \u00D7 0.466)) + 0.466/0.577 \u2248 0.30 + 0.807 \u2248 1.11 < 1.3, so the slope must be flattened or a retaining wall added.",
        "What is the difference between infinite and finite slopes?",
        "An infinite slope assumes the failure plane is parallel to the face, which suits long slopes. A finite slope such as a circular arc failure uses a slice method with a different Fs formula, so do not apply it to deep slopes.",
        "Why is water so dangerous?",
        "Water reduces effective stress and matrix suction and lubricates weak planes. As u rises Fs drops clearly, which is why landslides after rainfall are mostly driven by a sudden jump in pore water pressure.",
        "How large should Fs be to count as safe?",
        "Temporary slopes typically take 1.2 to 1.3 and permanent slopes 1.5, set by the code and the consequences. Below 1.0 the slope is unstable, and 1.0 to 1.2 is only marginal and not suitable long term.",
    ]))

    write('two-way-slab', build('two-way-slab', [
        "\U0001F52E Two-way slab moment estimate (civil)",
        "Moments in the short and long span directions of a two-way slab using the empirical coefficients of elastic theory.",
        "Two-way slab moment estimate",
        "\u03B1x \u2248 0.10 and the long-span coefficient \u03B1y \u2248 0.06, with M = \u03B1\u00B7q\u00B7l\u00B2; actual design should use the two-way slab coefficient table",
        "Uniform load q (kN/m\u00B2)",
        "Short span l_x (m)",
        "Long span l_y (m)",
        "Uses the empirical coefficients of elastic theory (simplified)",
        "Short-span coefficient \u03B1x \u2248 0.10, long-span coefficient \u03B1y \u2248 0.06",
        "M = \u03B1\u00B7q\u00B7l\u00B2; actual design should use the two-way slab coefficient table",
        "\U0001F4DA In-depth analysis: two-way slab moment estimate (civil)",
        "Rectangular two-way slabs: look up the coefficient from the long-to-short side ratio to get the moments in both directions at mid-span and supports and distribute the steel.",
        "Continuous two-way slabs use different coefficients for the interior, edge and corner panels, and the large negative corner moment needs extra steel.",
        "Thickness and deflection: two-way slab thickness is usually governed by stiffness and punching, with the steel adjusted within the slab strip.",
        "Moment coefficient of a square two-way slab",
        "For a 3 m \u00D7 3 m slab fixed on all four edges with q = 10 kN/m\u00B2: the tabulated mid-span coefficients give mx = my \u2248 0.036\u00B7q\u00B2 \u2248 0.036 \u00D7 10 \u00D7 9 \u2248 3.24 kN\u00B7m/m. Provide bottom steel in both directions and additional negative steel in the support zones.",
        "How do I look up the two-way slab coefficients?",
        "Use the moment coefficient table by boundary condition (simply supported or fixed) and Lx/Ly, for example the yield-line method. Edge and corner coefficients differ, so you cannot use the mid-span value over the whole slab.",
        "Why not reinforce it as a one-way slab?",
        "When the short-to-long side ratio is below 2 both directions act. Reinforcing only the short direction misses the long-span moment, and the upturned corners need negative steel, so mis-reinforcement leads to cracking.",
        "How is the slab thickness set?",
        "Two-way slabs often take 1/40 to 1/50 of the short span while satisfying punching and the minimum thickness. Too thick is uneconomic, too thin gives excessive deflection and crack width, so size it from the span first and then check.",
    ]))

    write('wind-load', build('wind-load', [
        "\u2696\uFE0F Wind load characteristic value calculation (civil)",
        "Characteristic wind load normal to the building surface, per the load code.",
        "Wind load characteristic value calculation",
        "w_k = \u03B2_z\u00B7\u03BC_z\u00B7\u03BC_s\u00B7\u03C9_0  where \u03C9_0 is the basic wind pressure looked up by return period and region, and \u03BC_z, \u03BC_s come from the code tables",
        "Basic wind pressure \u03C9_0 (kN/m\u00B2)",
        "Wind pressure height coefficient \u03BC_z",
        "Shape coefficient \u03BC_s",
        "Gust coefficient \u03B2_z",
        "\u03C9_0 is the basic wind pressure looked up by return period and region",
        "\u03BC_z and \u03BC_s are taken from the code tables",
        "\U0001F4DA In-depth analysis: wind load characteristic value calculation (civil)",
        "High-rise and long-span structures: compute the wind load at each level from the basic wind pressure w0, height coefficient \u03BCz, shape coefficient \u03BCs and gust factor \u03B2z.",
        "Curtain wall and cladding: use the local shape coefficient \u03BCs (amplified at corners) to get the pressure on the panels and design the panels and connections.",
        "Wind direction and openings: positive pressure on the windward face, negative on the leeward face, and the overall wind force of an open structure differs from an enclosed one.",
        "Wind pressure on a 30 m building",
        "With w0 = 0.45 kN/m\u00B2, \u03BCz (30 m, terrain class B) \u2248 1.39 (GB 50009-2012 table 8.2.1), \u03BCs (rectangular windward) \u2248 0.8 and \u03B2z \u2248 1.6: wk = 1.6 \u00D7 0.8 \u00D7 1.39 \u00D7 0.45 \u2248 0.80 kN/m\u00B2, used for the wall and the primary structure at that height.",
        "How is the shape coefficient \u03BC_s chosen?",
        "Look it up in the code by plan shape: 0.8 for a rectangular windward face and -0.5 for the leeward face, with rounded or curved surfaces reducing wind suction. Local shape coefficients at corners can reach 1.5 to 2.0, which matters for curtain walls.",
        "Why does the height coefficient \u03BC_z grow with height?",
        "Near-ground wind speed increases with height (the wind profile), so \u03BC_z rises with the distance above ground and the wind pressure at the top of a high-rise is clearly higher than at the base. Compute it level by level.",
        "What is the gust coefficient \u03B2_z?",
        "It reflects the amplification of instantaneous pressure by fluctuating wind. Flexible structures (tall and slender, long-span) have a large \u03B2_z while low-rise rigid buildings may take 1.0 to 1.1. It affects the dynamic response.",
    ]))


if __name__ == '__main__':
    main()
