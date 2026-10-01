import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
 'geometry-calculator': [
  "🧮 Geometry Calculator",
  "2D/3D shapes: area, volume, perimeter",
  "/ Geometry",
  "📖 View the \"Geometry Calculator Guide\"",
  "Area / volume = geometric formulas",
  "👆 Select a shape",
  "📚 In-Depth Analysis: Geometry Calculator",
  "Rectangle, square, circle, ",
  " and other basic shapes' area, perimeter, and diagonal — common quantities for renovation, land measurement, and material estimation.",
  "Formulas differ greatly between shapes, so choose the correct figure first, then plug into its formula.",
  "All lengths must be in the same unit (e.g. all in m); the resulting area unit is automatically squared.",
  "Example: rectangle 4×5 m",
  "Area S = w×h = 20.00 m²; perimeter C = 2(w+h) = 18.00 m; diagonal = √(w²+h²) = 6.40 m.",
  "Example: square with side 4 m",
  "Area S = a² = 16.00 m²; perimeter C = 4a = 16.00 m; diagonal = a√2 = 5.66 m.",
  "Why unify units before calculating?",
  "The formula itself does not do ",
  ". If you multiply a length in m by a width in cm directly, the area is off by 100×. Always normalize all inputs to the same unit first.",
  "Why do the area formulas for a circle and a rectangle differ?",
  "They come from the underlying geometry: rectangle = length×width, circle = πr² (obtained by a limiting process), triangle = ½base×height. They correspond to different boundary shapes and cannot be mixed; this tool switches formulas automatically based on the selected shape.",
  "About \"Geometry Calculator\"",
  "Geometry Calculator is an online tool in the math category. A math tool that supports multiple parameters for accurate calculation.",
 ],
 'herons-area': [
  "Triangle Area from Three Side Lengths",
  "Enter the three side lengths a, b, c of a triangle to compute its area.",
  "Heron's Formula Area Calculator",
  "/ Heron's Formula Area Calculator",
  "📖 View the \"Triangle Area from Three Side Lengths Guide\"",
  "Side c",
  "Only the three sides are needed to find the area.",
  "3,4,5 → area 6.",
  "📚 In-Depth Analysis: Heron's Formula for Triangle Area",
  "Find the area from three known side lengths without angles or height",
  "In surveying and CAD, compute side lengths from coordinates and then the area",
  "Verify whether the three sides can form a ",
  "Area from Three Sides",
  "Sides a=3, b=4, c=5: semi-perimeter p=(3+4+5)/2=6, area S=√(6×3×2×1)=√36=6. It happens to be a right triangle (3-4-5), consistent with ½×3×4=6.",
  "Degeneracy Check",
  "If the three sides do not satisfy \"the sum of the two shorter sides is greater than the longest\" (e.g. 1,2,4), then p minus some side is negative, the value under the root is non-positive, and the tool reports that no triangle can be formed.",
  "What are the conditions for Heron's formula?",
  "Any three side lengths that can form a triangle work; the value under the root must be positive, otherwise the sides cannot form a triangle (they degenerate to a line or do not exist).",
  "What is the relation between Heron's formula and ½base×height?",
  "They are equivalent. When the height is known, ½ah is simpler; when only the three sides are known, Heron's formula eliminates the height and depends only on the sides, so it is more general.",
 ],
 'law-of-cosines': [
  "Third Side from Two Sides and the Included Angle",
  "Enter the two sides a, b and the included angle C (degrees) to find the third side c.",
  "Law of Cosines Side Calculator",
  "/ Law of Cosines Side Calculator",
  "📖 View the \"Third Side from Two Sides and the Included Angle Guide\"",
  "Included angle C (degrees)",
  "At C=90° it reduces to the Pythagorean theorem.",
  "📚 In-Depth Analysis: Law of Cosines",
  "Find the third side from two sides and the included angle (SAS)",
  "Find any angle from three sides (SSS)",
  "Non-right ",
  " side-length / ",
  "angle conversion",
  "Finding the Third Side",
  "a=5, b=7, included angle C=60°: c²=5²+7²−2×5×7×cos60° = 25+49−70×0.5 = 39, c=√39≈6.245.",
  "Finding an Angle",
  "Sides a=3, b=4, c=5: cosC=(a²+b²−c²)/(2ab)=(9+16−25)/24=0, so C=90°, confirming a right triangle.",
  "How does the law of cosines relate to ",
  "?",
  "The law of cosines generalizes the Pythagorean theorem: when C=90°, cosC=0 and it reduces to c²=a²+b². The right angle is a special case.",
  "When do you use the law of cosines instead of the ",
  "law of sines",
  "Use the law of cosines for two sides plus the included angle (to find the third side) or three sides (to find an angle); use the law of sines for two angles plus one side, or two sides plus the angle opposite one of them.",
 ],
 'law-of-sines': [
  "Unknown Side from a Known Side, Angle, and Opposite Angle",
  "Enter the known side b, its opposite angle B, and the angle A opposite the unknown side (degrees) to find side a.",
  "Law of Sines Side Calculator",
  "/ Law of Sines Side Calculator",
  "📖 View the \"Unknown Side from a Known Side, Angle, and Opposite Angle Guide\"",
  "Known side b",
  "Angle A (degrees)",
  "Angle B (degrees)",
  "The law of sines is used to solve oblique triangles.",
  "📚 In-Depth Analysis: Law of Sines",
  "Find the remaining sides from two angles and one side (AAS/ASA)",
  "Find an angle from two sides and the angle opposite one of them (SSA, possibly two solutions)",
  " side-angle ratio conversion",
  "Two Angles and One Side",
  "A=30°, B=45°, a=10, so C=105°; from a/sinA=b/sinB, b=10×sin45°/sin30°=10×0.707/0.5≈14.14.",
  "The Ambiguous Case",
  "Given a, b, and angle A (SSA), there may be no solution, one solution, or two, because sin is symmetric over 0~180°; use the figure to decide.",
  "Law of Sines",
  " formula?",
  "a/sinA=b/sinB=c/sinC=2R (R is the circumradius). That is, each side is proportional to the sine of its opposite angle.",
  "Why can SSA have two solutions?",
  "Because sinθ=sin(180°−θ); once one side and its opposite angle are fixed, the other angle may be acute or the supplement, giving two different triangles (unless excluded by a side constraint).",
 ],
 'log-base': [
  "Compute the logarithm in any base using the change-of-base formula.",
  "Logarithm in Any Base Calculator",
  "/ Logarithm in Any Base",
  "Logarithm in Any Base",
  "📖 View the \"Logarithm in Any Base Calculator Guide\"",
  "Argument x",
  "Base b",
  "Change of base: ln x/ln b.",
  "📚 In-Depth Analysis: Logarithm Computation",
  "Change of base for any base: log_b(x)=ln(x)/ln(b)",
  "Solve exponential equations and compute decibels/pH/Richter magnitude",
  "Compute information content in information theory (base 2)",
  "Change-of-Base Formula",
  "log_2(8)=ln8/ln2≈2.079/0.693≈3; you can also use log_2(8)=3 directly (since 2³=8). The change of base lets any base be computed with natural or common logarithms.",
  "Exponential Equation",
  "Solving 2^x=10: x=log_2(10)=ln10/ln2≈3.322.",
  "What is the change-of-base formula?",
  "log_b(x)=log_k(x)/log_k(b), commonly with k=e (natural log) or k=10. This way a calculator with only ln/lg can still handle any base.",
  "Can logarithms turn multiplication and division into addition and subtraction?",
  "Yes, log(ab)=log a+log b, log(a/b)=log a−log b, log(a^c)=c·log a. This is exactly its value for simplifying calculations.",
  "Change-of-base formula log_b(x)=ln(x)/ln(b): convert a logarithm in any base into natural (or common) logarithms for computation.",
  "The result means \"b to what power equals x\". It increases monotonically when b>1 and decreases when b∈(0,1). x>0, b>0 and b≠1.",
 ],
}

EXTRA = {
 'geometry-calculator': {'三角形': 'triangle', '单位换算': 'unit conversion'},
 'herons-area': {'三角形': 'triangle'},
 'law-of-cosines': {'三角形': 'triangle', '勾股定理': 'the Pythagorean theorem'},
 'law-of-sines': {'三角形': 'Triangle'},
}

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
            print('BAD EN', slug, repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(en)); sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'math', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, slug + '.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
