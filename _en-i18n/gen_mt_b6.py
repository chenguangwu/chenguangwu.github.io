#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metallurgy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metallurgy')
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
    out = {'slug': slug, 'industry': 'metallurgy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('solidification-time', build('solidification-time', [
        "\U0001F9EE Solidification Time Calculation",
        "Casting solidification time calculation (modulus method / Chvorinov rule), estimating the time to full solidification from the casting modulus and solidification coefficient.",
        "Core formula (over the input variables): 2\u00d7\u03c0\u00d7r\u00d7r+2\u00d7\u03c0\u00d7r\u00d7d3; 4\u00f73\u00d7\u03c0\u00d7(rs)^3; 4\u00d7\u03c0\u00d7(rs)^2",
        "Casting Shape",
        "Plate (length \u00d7 width \u00d7 thickness)",
        "Cube (side length)",
        "Cylinder (diameter \u00d7 height)",
        "Sphere (diameter)",
        "Custom (volume / surface area)",
        "Heat Dissipation Surface Area A (cm\u00b2)",
        "Mould Material",
        "Sand Mould",
        "Metal Mould",
        "Solidification Coefficient K (min/cm\u00b2)",
        "Metal Being Cast",
        "Cast Aluminium",
        "Compute Solidification Time",
        "\U0001F4CB Chvorinov Rule",
        "Solidification time:",
        "Modulus:",
        "M = V / A (volume / heat dissipation surface area), in cm",
        "Solidification coefficient K:",
        "depends on mould material, metal type and superheat.",
        "Sand mould cast iron K\u22481.5 to 2.5, sand mould cast steel K\u22482.0 to 3.0, metal mould K\u22480.5 to 1.0 min/cm\u00b2 (empirical values).",
        "The larger the modulus, the slower the solidification; the riser modulus should exceed the casting modulus to ensure feeding.",
        "\U0001F4DA In-Depth Analysis: Solidification Time Calculation",
        "In casting process design, estimate the solidification time of a casting in the mould by the Chvorinov rule, and use it to set the shakeout time and the riser feeding window.",
        "Compare the solidification coefficients of different material and mould combinations to judge how much faster the same casting cools in a sand mould versus a metal mould.",
        "Rank the solidification sequence of several castings, or of different wall thicknesses in one casting, by relative modulus, guiding the placement of chills and risers.",
        "Chvorinov Rule",
        "Solidification time t = K \u00d7 (V/A)\u00b2 = K \u00d7 M\u00b2, where M = V/A is the casting modulus (volume to heat dissipation area ratio) and K is the solidification coefficient. Common coefficients (by mould and material): sand mould cast iron 0.094, sand mould cast steel 0.116, sand mould cast aluminium 0.170, metal mould cast iron 0.030, metal mould cast aluminium 0.015. Units follow the tool's built-in calibration.",
        "Relative Comparison Example",
        "For two cube castings of 10 cm and 20 cm side, the moduli are 10/6=1.667 cm and 20/6=3.333 cm; the solidification time ratio = (M\u2082/M\u2081)\u00b2 = (3.333/1.667)\u00b2 = 4, so the larger casting takes about 4 times as long to solidify. Doubling wall thickness doubles the modulus and makes solidification about 4 times longer, which is the key basis for riser and chill design.",
        "Why do high-modulus regions solidify last?",
        "The larger the modulus M=V/A, the smaller the heat dissipation surface per unit volume, so cooling is slower and solidification happens later. Shrinkage cavities therefore form where solidification finishes last, requiring risers there for feeding.",
        "What do the large differences between sand and metal mould coefficients mean?",
        "Metal moulds conduct heat far faster than sand, so K is smaller and solidification faster for the same casting. The coefficients are only empirical calibrations; actual results also depend on thermal parameters and chill effect, so precise scheduling should follow measurements.",
        "About \"Solidification Time Calculation\"",
        "Solidification Time Calculation is an online tool in the business and office domain. A business and office tool that improves work efficiency with local data processing that protects privacy.",
        "How to Use Solidification Time Calculation",
        "What Does Solidification Time Calculation Do?",
        "How Do I Use Solidification Time Calculation?",
        "What Scenarios Suit Solidification Time Calculation?",
    ]))
    write('calc-time-solid', build('calc-time-solid', [
        "\U0001F9EE Casting Solidification Time (Modulus Method) Calculation",
        "Based on the Chvorinov rule t = C \u00d7 (V/A)\u00b2, entering the cross-section shape and dimensions automatically computes the modulus M and solidification time t, supporting ranking of solidification order across multiple sections.",
        "Core formula (over the input variables): seq[seq.length-1]; last.Mmm\u00d71.2; C\u00d7(Mcm)^2",
        "Mould / Material",
        "Sand Mould - Cast Iron",
        "Sand Mould - Cast Steel",
        "Sand Mould - Aluminium Alloy",
        "Metal Mould - Cast Iron",
        "Metal Mould - Aluminium Alloy",
        "Solidification Constant C (min/cm\u00b2)",
        "\U0001F4D0 Casting Section",
        "\u2795 Add Section",
        "\U0001F4A1 Chvorinov rule: t = C \u00d7 M\u00b2, M = V/A (modulus = volume / cooling surface area). Longer solidification time means later solidification, and the riser modulus should exceed that of the fed region.",
        "\U0001F4CA Reference Values of Common Solidification Constants C",
        "C is an empirical constant affected by mould material, pouring temperature and alloy characteristics",
        "The modulus method suits sand casting; metal moulds need correction",
        "Riser design principle: M_riser \u2265 1.2 \u00d7 M_casting",
        "\U0001F4DA In-Depth Analysis: Casting Solidification Time (Modulus Method) Calculation",
        "Compute the modulus M=V/A directly from the casting geometry, as an input to solidification sequence and feeding design.",
        "Apply the modulus formula to typical shapes such as plate, cube, sphere, cylinder, rod and block to quickly obtain the heat dissipation characteristic.",
        "Check riser feeding capacity with the rule that the riser modulus is at least 1.2 times the casting modulus.",
        "Shape Modulus Formulas",
        "Plate (thickness T) M=T/2; cube (side a) M=a/6; sphere (diameter D) M=D/6; cylinder (diameter D, length L) M=D\u00b7L/(2D+4L); rod (section a\u00d7b) M=a\u00b7b/(2(a+b)); block (a\u00d7b\u00d7c) M=a\u00b7b\u00b7c/(2(ab+bc+ca)).",
        "For a cube casting of 100 mm side: M=100/6\u224816.7 mm. For a plate thickness of 20 mm: M=20/2=10 mm. For a cylinder with D=50 mm and L=200 mm: M=50\u00d7200/(2\u00d750+4\u00d7200)=10000/900\u224811.1 mm. Riser rule: riser modulus \u22651.2\u00d7casting modulus, so the cube needs M_riser\u226520 mm for adequate feeding.",
        "What is the relationship between modulus",
        "and solidification time",
        "?",
        "Solidification time t=K\u00b7M\u00b2, so a larger modulus solidifies more slowly. The modulus is a geometric heat dissipation characteristic, and combining it with the solidification coefficient gives an absolute time estimate.",
        "How is the modulus taken for complex parts?",
        "Decompose into several simple shapes and compute the modulus of each; the smallest modulus region is the first to solidify and the largest is the last (needing a riser). Alternatively, estimate the whole by the subdivision method.",
        "About \"Casting Solidification Time (Modulus Method) Calculation\"",
        "Computes casting solidification time on the basis of the Chvorinov rule t = C \u00d7 (V/A)\u00b2. It supports many section shapes such as flat plate, cylinder, cube, sphere, rectangular rod and rectangular block, automatically computing modulus and solidification time, ranking the solidification sequence and assisting riser design.",
        "Supports 7 section shapes with automatic modulus calculation",
        "Ranking and comparison of solidification order across multiple sections",
        "Riser modulus recommendation (M \u2265 1.2 \u00d7 M_casting)",
        "Casting Process Design and Riser Layout",
        "Casting Solidification Sequence Analysis",
        "Reference for Gating System Design",
        "Solidification Constant",
    ]))


if __name__ == '__main__':
    main()