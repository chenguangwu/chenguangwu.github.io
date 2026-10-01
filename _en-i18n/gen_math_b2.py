import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
 'calc-4': [
  "📏 Circle Area / Circumference",
  "Enter any one of radius, diameter, area, or circumference and the other three are computed automatically.",
  "📖 View the \"Circle Area / Circumference Guide\"",
  "Circle area A = πr², circumference C = 2πr",
  "Radius r",
  "Diameter d",
  "Area S",
  "Formula: d = 2r, S = πr², C = 2πr = πd. π is taken as 3.14159265359.",
  "Enter at least one valid value; leave the rest blank and they are computed automatically.",
  "If several quantities are entered, the tool recomputes using radius as the priority.",
  "📚 In-Depth Analysis: Circle Area / Circumference",
  "Knowing any one circle quantity (radius, diameter, area, circumference) lets you derive the rest, useful for machinery, UI corner radii, and site design.",
  "Back-solving the radius from area or circumference is common when sizing from a known material amount.",
  "Keep units consistent (do not confuse radius and diameter); area and circumference have different dimensions and cannot be compared.",
  "Example: given radius r=5",
  "Diameter d = 2r = 10.0000; area S = πr² = 78.5398; circumference C = 2πr = 31.4159.",
  "Example: back-solving from area S=78.5398",
  "Radius r = √(S/π) = √(78.5398/3.14159) = 5.0000; from r, d=10.0000 and C=31.4159.",
  "How many digits of π are used?",
  "3.14159 (or Math.PI) is generally used, and 4 decimal places suffice for engineering precision; area/circumference are sensitive to the digits of π, and rounding to 3.14 introduces about 0.05% error.",
  "What if I mix up diameter and radius?",
  "The diameter d = 2r is the full length through the center, while the radius r is from the center to the edge. Read the labels carefully: the diameter is often marked ⌀ or d, the radius r. Mixing them up doubles or halves the result.",
  "About \"Circle Area / Circumference\"",
  "The circle is one of the most basic geometric shapes. This tool derives the other three quantities from any one of radius, diameter, area, or circumference.",
  "Four quantities interconvert with flexible input",
  "Automatically detects the priority input",
  "High-precision π",
  "Primary and secondary math homework",
  "Estimating circular site area",
  "Pipe circumference and cross-section",
  "Design and engineering drawing",
  "Enter or leave blank",
 ],
 'calculus-tools': [
  "🧮 Calculus Tools",
  "Derivatives / integrals / limits / series expansion",
  "/ Calculus",
  "📖 View the \"Calculus Tools Guide\"",
  "Derivative / integral = calculus operations",
  "Preset function",
  "Function f(x)",
  "Derivative f'(x)",
  "Definite integral ∫f(x)dx",
  "Limit lim x→0",
  "Taylor expansion (x=0, order 5)",
  "Root finding (numeric)",
  "Area under curve (numeric)",
  "Lower limit a",
  "Upper limit b",
  "Evaluation point x₀",
  "👆 Shown after calculation",
  "📚 In-Depth Analysis: Calculus Tools",
  "Numerical differentiation, integration, limits, and Taylor expansion are fundamental tools for physical modeling, engineering optimization, and marginal economic analysis.",
  "When an analytical solution is hard (e.g. involving transcendental functions), numerical methods give usable approximations at the cost of truncation/rounding error.",
  "Derivatives capture the instantaneous rate of change, integrals the accumulated quantity, limits the approaching behavior, and Taylor series a local polynomial approximation.",
  "Example: the derivative of f(x)=x² is 6 (at x=3)",
  "Central difference f'(3) = [f(3+1e-5)−f(3−1e-5)]/(2×1e-5) = 6.000000; the analytical 2x at x=3 is also 6, matching.",
  "Example: ∫₀¹ x²dx and lim x→0 x²",
  "Trapezoidal rule (n=1000) ∫₀¹ x²dx = 0.333333 (analytical value 1/3); lim x→0 x² = 0.000000 (sampled symmetrically at x=±1e-6, no longer averaging in x=0 — otherwise functions undefined at 0 such as sin(x)/x would be misjudged as \"limit does not exist\" even though the true limit is 1); the order-5 Taylor expansion of f(x)=x² at x=0 is simply x².",
  "What are the sources of error in numerical differentiation?",
  "Mainly from the step size h: too large gives large truncation error, too small amplifies rounding error. The central difference is an order of magnitude more accurate than the forward difference, and h≈1e-5 is commonly used to balance the two.",
  "How accurate is the trapezoidal integration?",
  "The trapezoidal error is about O(1/n²), more accurate as n grows. It suffices for smooth functions; functions with kinks/singularities need segmentation or a better method (Simpson). This tool fixes n=1000.",
  "Why doesn't the limit just plug in x=0?",
  "A limit describes the approaching behavior, not the value at that point. f can be undefined at 0 yet still have a limit (e.g. sin(x)/x → 1), so this tool samples symmetrically at x=±1e-6 and considers the limit to exist only when both sides are close; cases like 1/x that diverge to ±∞ on the two sides are judged not to exist.",
  "About \"Calculus Tools\"",
  "Calculus Tools is an online tool in the math category. A math tool that supports multiple parameters for accurate calculation.",
 ],
 'circular-permutation': [
  "Circular Permutations from the Number of Elements",
  "Enter the number of elements n to compute the number of circular permutations.",
  "Circular Permutation Calculator",
  "/ Circular Permutation Calculator",
  "📖 View the \"Circular Permutations from the Number of Elements Guide\"",
  "Circular permutation count = (n−1)!",
  "Number of elements n",
  "Circular permutations have one less degree of freedom than linear ones.",
  "📚 In-Depth Analysis: Circular Permutation",
  "Seating arrangements around a round table, where rotations count as the same",
  "Counting for rotation-equivalent cases such as circular necklaces and turntables",
  "Circular schedules or circular seating design",
  "Round-Table Seating",
  "When n people sit around a round table, the circular ",
  "permutation count",
  "= (n−1)!. For example, 4 people seated = (4−1)! = 6 ways, since fixing one person reduces the rest to a linear arrangement of the other 3, and rotations produce no new arrangement.",
  "Why is the circular permutation (n−1)! instead of n!?",
  "Rotating the whole round table does not create a new arrangement; fixing one person removes the rotational freedom, leaving n−1 people in a linear arrangement, hence (n−1)!.",
  "What is the difference between circular permutations and bracelets (which can be flipped)?",
  "A bracelet can also be flipped, so when flips are equivalent divide by 2, giving (n−1)!/2; a plain round table cannot be flipped and stays at (n−1)!.",
  "The circular permutation count A(n)=(n−1)! gives the number of distinct ways n different elements can be arranged in a ring; arrangements that coincide after rotation count as the same.",
  "Difference from Linear Arrangement",
  "A linear arrangement is n!; circular permutations divide by n because rotations are equivalent, giving (n−1)!. If flips are also equivalent (bracelets/necklaces), divide by another 2 to obtain (n−1)!/2.",
  "Scenarios that count modulo rotation, such as circular seating, combination locks, and molecular conformations.",
 ],
 'combination-repetition': [
  "Combinations with Repetition from Type and Pick Counts",
  "Enter the number of types n and the pick count r to compute combinations with repetition.",
  "Combination with Repetition Calculator",
  "/ Combination with Repetition Calculator",
  "📖 View the \"Combinations with Repetition from Type and Pick Counts Guide\"",
  "Combination with repetition C(n+k−1, k)",
  "Number of types n",
  "Pick count r",
  "The classic stars-and-bars count.",
  "📚 In-Depth Analysis: Combinations with Repetition",
  "Choose k items from n types, where the same type can be picked more than once (e.g. buying k candies with repeatable flavors)",
  "Count the number of sampling methods that allow repetition",
  "Counting in the balls-and-boxes model where a box may hold multiple balls",
  "Repeatable Flavors",
  "Choosing 2 cups from 3 flavors (same flavor allowed), with repetition the ",
  "combination count",
  "= C(n+k−1,k)=C(3+2−1,2)=C(4,2)=6 ways: AA/AB/AC/BB/BC/CC.",
  "Comparison with No Repetition",
  "Without repetition (one cup per flavor) there are C(3,2)=3 ways; allowing repetition raises it to 6, because same-flavor combinations like AA/BB/CC appear.",
  "What is the combinations-with-repetition formula?",
  "C(n+k−1, k), where n is the number of types and k is the pick count. It is equivalent to the \"stars and bars\" count of n categories and k indistinguishable picks.",
  "When do you use combinations with repetition?",
  "Use it when you can pick the same thing again — e.g. taking multiple portions at a buffet, repeatable flavors, or drawing categories with replacement. When there is no replacement and each type is unique, use the ordinary combination C(n,k).",
 ],
 'combination': [
  "The number of combinations of r items chosen from n elements.",
  "Combination Calculator",
  "Combination",
  "📖 View the \"Combination Calculator Guide\"",
  "Order does not matter.",
  "📚 In-Depth Analysis: Combination C(n,k)",
  "Count the ways to choose k out of n without regard to order, e.g. drawing lots or forming teams",
  "Estimate the number of possible outcomes in a lottery or raffle",
  "In probability problems, count the number of ways an event can occur (the denominator)",
  "Picking People for a Team",
  "Choosing 2 people from 5, the combination count C(5,2)=5!/(2!×3!)=(5×4)/(2×1)=10 ways. Unlike permutations, {A,B} and {B,A} count as the same.",
  "Comparison with Permutation",
  "For the same 5-choose-2, if order matters (e.g. first and second place) use the permutation P(5,2)=5×4=20, twice the combination, because each pair has two orders.",
  "What is the core difference between combinations and permutations?",
  "Combinations ignore order (just choose them), while permutations count order (who comes first matters). Formally C(n,k)=P(n,k)/k!, i.e. dividing out the orderings.",
  "When does C(n,k) equal C(n,n−k)?",
  "Always: choosing k to keep out of n is equivalent to choosing n−k to remove, a one-to-one correspondence, so C(n,k)=C(n,n−k).",
 ],
}

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
