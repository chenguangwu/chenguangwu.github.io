import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
 'determinant-2x2': [
  "2x2 Determinant from the Four Matrix Elements",
  "Enter the four elements a, b, c, d of a 2x2 matrix to compute its determinant.",
  "2x2 Determinant Calculator",
  "/ 2x2 Determinant Calculator",
  "📖 View the \"2x2 Determinant from the Four Matrix Elements Guide\"",
  "A zero determinant means the matrix is singular.",
  "📚 In-Depth Analysis: 2x2 Determinant",
  "Decide whether a system of two linear equations has a unique solution",
  "Find the area scaling factor of a 2D linear transformation",
  "A quick invertibility check (the matrix is invertible only if the determinant is non-zero)",
  "The determinant of the matrix [[a,b],[c,d]] = ad−bc. For example, [[3,1],[2,4]] has determinant 3×4−1×2 = 10 ≠ 0, so the matrix is invertible and the corresponding system has a unique solution.",
  "Geometric Meaning",
  "The absolute value of the 2x2 determinant equals the area of the parallelogram spanned by the two column vectors; a value of 0 means the vectors are collinear (the transformation collapses the plane onto a line).",
  "What does a zero determinant mean?",
  "The matrix is non-invertible (singular), its column vectors are linearly dependent, the corresponding linear system has either no solution or infinitely many, and the transformation reduces dimension.",
  "How do you remember the 2x2 determinant?",
  "The product of the main diagonal minus the product of the anti-diagonal: ad−bc. Higher orders use row/column expansion or simplification, but for 2x2 it is just this one rule.",
 ],
 'distance-2d': [
  "Compute the distance between two points in the 2D plane.",
  "2D Distance Between Two Points Calculator",
  "/ Distance Between Two Points",
  "Distance Between Two Points",
  "📖 View the \"2D Distance Between Two Points Calculator Guide\"",
  "(0,0)→(3,4) distance 5.",
  "Pythagorean triple 3-4-5.",
  "📚 In-Depth Analysis: 2D Distance Between Two Points",
  "Compute the straight-line distance between two coordinate points on a map or plane",
  "Check whether a point is within a radius (collision detection)",
  "The distance metric in clustering and nearest-neighbor methods",
  "Plane Distance",
  "A(1,2), B(4,6): distance = √[(4−1)²+(6−2)²] = √(9+16) = √25 = 5, i.e. ",
  " applied directly on the plane.",
  "versus Manhattan Distance",
  "For the same two points the Manhattan distance = |4−1|+|6−2| = 7, larger than the ",
  " of 5; when paths can only move horizontally and vertically, Manhattan is more appropriate.",
  "What is the difference between Euclidean and Manhattan distance?",
  "Euclidean is the straight line (√(Δx²+Δy²)), Manhattan is the axis-aligned path (|Δx|+|Δy|). The former suits free space, the latter grid streets.",
  "How is 3D distance",
  " calculated?",
  "Just add one dimension: √[(x2−x1)²+(y2−y1)²+(z2−z1)²], the principle is the same.",
 ],
 'dot-product': [
  "Dot Product of Two 3D Vectors",
  "Enter the components of two vectors to compute their dot product.",
  "Vector Dot Product Calculator",
  "/ Vector Dot Product Calculator",
  "📖 View the \"Dot Product of Two 3D Vectors Guide\"",
  "A zero dot product means the two vectors are orthogonal.",
  "📚 In-Depth Analysis: Vector Dot Product",
  "Determine the two vectors' ",
  "included angle",
  ", and whether they are orthogonal (dot product 0)",
  "Projection length, and work in mechanics W=F·s",
  "In machine learning, the ",
  " numerator",
  "Coordinate Calculation",
  "a=(1,2,3), b=(4,5,6): dot product = 1×4+2×5+3×6 = 4+10+18 = 32. Magnitudes |a|=√14≈3.742 and |b|=√77≈8.775, so cosθ=32/(3.742×8.775)≈0.975 and θ≈12.9°.",
  "Orthogonality Check",
  "a=(1,0), b=(0,1) has dot product = 0, so the two vectors are perpendicular (orthogonal).",
  "What is the difference between the dot product and the cross product?",
  "The dot product is a scalar measuring how aligned the vectors are (it includes the cosine of the angle); the cross product is a vector perpendicular to the plane of the two vectors, whose magnitude equals the parallelogram area, and is defined only in 3D.",
  "What does a zero dot product mean?",
  "The two vectors are orthogonal (perpendicular), or one of them is the zero vector. Geometrically they do not affect each other and the projection is 0.",
 ],
 'equation-solver': [
  "🧮 Equation Solver",
  "One/two-variable linear, quadratic, and systems of equations",
  "/ Equation Solver",
  "📖 View the \"Equation Solver Guide\"",
  "Equation type",
  "Linear: x = −b / a; quadratic: x = (−b ± √Δ) / 2a, Δ = b² − 4ac; cubic: Newton iteration + bisection to find all real roots",
  "Linear equations are solved directly; for quadratics compute the discriminant Δ = b² − 4ac first — Δ > 0 gives two real roots, Δ = 0 a repeated root, and Δ < 0 a pair of complex conjugate roots; cubics use Newton's method with interval scanning to find all real roots.",
  "🧮 Solve",
  "👆 Select a type",
  "📚 In-Depth Analysis: Equation Solver",
  "Linear equations in one variable and ",
  "quadratic equation solving",
  " are used for ",
  "physics formula",
  " rearrangements, ",
  "break-even points",
  ", and solving for time in kinematics.",
  "The discriminant Δ determines how many real roots a quadratic has, and is the first test when solving.",
  "To verify a root, substitute it back into the original equation and check that it is approximately 0, which quickly reveals input errors.",
  "Example: linear equation 2x − 6 = 0",
  "x = −b/a = −(−6)/2 = 3.000000; check 2×3 − 6 = 0.000000.",
  "Example: quadratic equation x² − 5x + 6 = 0",
  "What does the discriminant Δ represent?",
  "Δ = b²−4ac: Δ>0 gives two distinct real roots, Δ=0 two equal real roots (a repeated root), and Δ<0 no real roots but a pair of complex conjugate roots. It is the first checkpoint for the nature of the roots.",
  "What if a quadratic has no real roots?",
  "There is no solution over the reals, but the complex roots x = (−b ± i√|Δ|)/(2a) are still meaningful (e.g. in circuits and vibration analysis). If the use case requires real numbers, report \"no real solution\" rather than throwing an error.",
  "About \"Equation Solver\"",
  "Equation Solver is an online tool in the math category. A math tool that supports multiple parameters for accurate calculation.",
 ],
 'exponent-solve': [
  "Exponent from a Base and a Result",
  "Enter the base a and the result b to find the exponent x.",
  "Exponential Equation Solver",
  "/ Exponential Equation Solver",
  "📖 View the \"Exponent from a Base and a Result Guide\"",
  "Base a",
  "Result b",
  "The logarithm of b to base a.",
  "📚 In-Depth Analysis: Exponent from a Base and a Result",
  "Solving the exponential equation aˣ = b (for x) is used for ",
  ", compound-interest periods, and pH/decibel back-calculation.",
  "The core is the change of base: x = log(b) / log(a), independent of the base chosen.",
  "The base a must be >0 and ≠1, and the argument b must be >0.",
  "Example: 2ˣ = 8",
  "x = log(8)/log(2) = 3.0000 (since 2³=8).",
  "Example: 3ˣ = 81 and 10ˣ = 1000",
  "x = log(81)/log(3) = 4.0000; x = log(1000)/log(10) = 3.0000. The change-of-base formula makes any base computable.",
  "What is the change-of-base formula?",
  "logₐ(b) = ln(b)/ln(a) = log(b)/log(a), the ratio of any two logarithms of the same base. It turns exponential equations with a base other than 10 or e into ordinary logarithm operations.",
  "What restrictions apply to the base and the argument?",
  "The base a>0 and a≠1 (when a=1, 1ˣ is always 1 and cannot be inverted), and the argument b>0 (the domain of the logarithm). Entering 0 or a negative number yields NaN/invalid, so validate in advance.",
 ],
}

EXTRA = {
 'distance-2d': {'勾股定理': 'the Pythagorean theorem', '欧氏距离': 'Euclidean distance'},
 'dot-product': {'余弦相似度': 'cosine similarity'},
 'exponent-solve': {'半衰期': 'half-life'},
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
