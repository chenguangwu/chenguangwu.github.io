import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
 'factorial-calc': [
  "The factorial of a non-negative integer, with 0! = 1.",
  "Factorial Calculator",
  "/ Factorial",
  "Factorial",
  "📖 View the \"Factorial Calculator (Math) Guide\"",
  "📚 In-Depth Analysis: Factorial n!",
  "Compute the denominator/numerator in permutations and combinations",
  "The coefficients when expanding Taylor series and probability formulas",
  "Estimate the scale of permutations of large numbers",
  "Basic Calculation",
  "5! = 5×4×3×2×1 = 120; 0! = 1 (a convention that keeps the formulas consistent, e.g. C(n,0)=1).",
  "Overflow Note",
  "20! ≈ 2.43×10^18, beyond the 64-bit integer limit; larger factorials need logarithms or an approximation (Stirling's formula n! ≈ √(2πn)(n/e)^n).",
  "Why is 0! = 1?",
  "It is both a convention and a combinatorial meaning: choosing 0 out of n has only 1 way (choosing nothing), and it keeps C(n,0)=n!/(0!×n!)=1 consistent.",
  "How fast does the factorial grow?",
  "Very fast, roughly exponential-of-exponential. 10! = 3628800, and 20! already exceeds 2×10^18, far beyond the ordinary integer range, so large values need logarithms or approximation.",
  "The factorial n! = 1×2×…×n (0!=1) gives the number of permutations of n distinct elements; it grows extremely fast — 13! already exceeds 6 billion.",
  "Limits",
  "Ordinary numeric types overflow around n≈170; large factorials need high precision or a logarithmic approximation (log(n!)). This tool computes within its supported range and warns when exceeded.",
 ],
 'fibonacci-n': [
  "Iteratively compute the n-th Fibonacci number.",
  "n-th Fibonacci Number Calculator",
  "Fibonacci Sequence",
  "📖 View the \"n-th Fibonacci Number Calculator Guide\"",
  "📚 In-Depth Analysis: Fibonacci Sequence",
  "F(n)=F(n−1)+F(n−2), modeling natural growth and rabbit breeding",
  "The recurrence that approaches the golden ratio φ≈1.618",
  "A classic case in algorithm problems and dynamic programming",
  "Recurrence",
  "F(0)=0, F(1)=1, so F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8. The ratio of adjacent terms F(n+1)/F(n) approaches the golden ratio φ=(1+√5)/2≈1.618.",
  "Closed-Form Formula",
  "Binet's formula F(n)=[φ^n−(1−φ)^n]/√5 computes the n-th term directly without recursion, since (1−φ)^n quickly approaches zero.",
  "What is the relationship between Fibonacci and the golden ratio?",
  "The ratio of adjacent terms approaches the golden ratio φ≈1.618, widely used for aesthetic proportions (e.g. a 1:1.618 layout).",
  "Is F(0) 0 or 1?",
  "Both conventions exist; the common one starts with F(0)=0, F(1)=1. When coding, be careful which one you use, or you will be off by one.",
 ],
 'formula-calculator': [
  "🏋️ Common Formula Quick Reference",
  "Math / physics / chemistry / geometry formulas",
  "Common Formulas",
  "/ Common Formulas",
  "📖 View the \"Formula Calculator Guide\"",
  "Common formula quick reference: it covers math (circle area πr², sphere volume 4πr³÷3, trigonometric functions), physics (kinematics v = v₀ + at, Ohm's law I = U ÷ R, power P = U × I), chemistry (molar concentration c = n ÷ V, ideal gas PV = nRT) and geometry (Pythagorean theorem a² + b² = c²), etc. Pick a formula, fill in the parameters, and get the result.",
  "📚 In-Depth Analysis: Common Formula Quick Reference",
  "The quick reference is used to look up common formulas fast in engineering and study scenarios (geometry, kinematics, algebra, finance, etc.), avoiding repeated manual searching.",
  "Filter by category and use (e.g. \"area\", \"kinematics\", \"compound interest\") to locate the target formula and its variable meanings.",
  "The result gives the formula form and unit notes, so you can plug it directly into a calculation tool.",
  "Example: looking up area formulas by category",
  "Under the \"geometry\" category you can find: circle S=πr², rectangle S=w·h, triangle S=½bh, trapezoid S=(a+b)h/2. Select one and view the variable definitions to plug in values.",
  "Example: filtering by use (kinematics)",
  "Under the \"kinematics\" use you can find: uniform acceleration v=v₀+at, displacement s=v₀t+½at², v²−v₀²=2as. Choose the suitable formula given the knowns, then move to the numerical calculator.",
  "Can the quick reference replace a standard handbook?",
  "No. The quick reference is an overview for fast review; precise coefficients, applicable conditions, and dimensions should follow the latest national standards, textbooks, or official handbooks. This tool provides common forms; refer to authoritative sources for specifics.",
  "Which categories are covered?",
  "It typically covers geometry, algebra, trigonometry, kinematics, finance (compound interest / present value), and more. If a needed formula is not listed, check a professional handbook to avoid missing assumptions (e.g. uniform motion, ideal gas).",
  "About \"Common Formulas\"",
  "Common Formulas is an online tool in the math category. A math tool that supports multiple parameters for accurate calculation.",
  "🔍 Search formulas...",
 ],
 'gcd-lcm': [
  "Find the greatest common divisor by the Euclidean algorithm, then the least common multiple.",
  "GCD / LCM Calculator",
  "/ Greatest Common Divisor and Least Common Multiple",
  "Greatest Common Divisor and Least Common Multiple",
  "📖 View the \"GCD / LCM Calculator Guide\"",
  "Integer a",
  "Integer b",
  "📚 In-Depth Analysis: Greatest Common Divisor and Least Common Multiple",
  "Reduce fractions: divide numerator and denominator by the ",
  "greatest common divisor",
  "Find a common denominator or overlapping cycles: use the ",
  "least common multiple",
  "Check coprimality in cryptography and number theory",
  "Reducing and Common Denominators",
  "GCD(12,18)=6, so 12/18 reduces to 2/3; LCM(4,6)=12, so the common denominator of 1/4 and 1/6 is 12. Relation: LCM(a,b)=a×b/GCD(a,b), i.e. 4×6/2=12.",
  "Coprimality Check",
  "GCD(8,15)=1, so the two numbers are coprime; when coprime, LCM = the product of the two numbers.",
  "What is the relationship between GCD and LCM?",
  "For any positive integers a,b: GCD(a,b)×LCM(a,b)=a×b. Compute the GCD (Euclidean algorithm) first, then divide to get the LCM — faster than direct enumeration.",
  "How does the Euclidean algorithm compute the GCD?",
  "Repeatedly replace with \"larger mod smaller\": GCD(48,18)=GCD(18,12)=GCD(12,6)=GCD(6,0)=6, until the remainder is 0; the last divisor is the GCD.",
  "The greatest common divisor (GCD) is the largest shared factor of two integers; the least common multiple (LCM) is the smallest common multiple. They satisfy GCD(a,b)·LCM(a,b)=|a·b|.",
  "Reducing fractions, common denominators, cycle alignment, modular arithmetic, and more. The Euclidean algorithm (repeated division) solves it efficiently.",
 ],
 'geometric-series-sum': [
  "Geometric Series Sum from First Term, Ratio, and Count",
  "Enter the first term a, the ratio r, and the count n to compute the sum of the first n terms.",
  "Geometric Series Sum Calculator",
  "/ Geometric Series Sum Calculator",
  "📖 View the \"Geometric Series Sum from First Term, Ratio, and Count Guide\"",
  "First term a",
  "The series converges when |r|<1.",
  "📚 In-Depth Analysis: Geometric Series Sum",
  "Compute the cumulative total of proportional growth/decay such as compound interest and depreciation",
  "Find the sum of an infinite geometric series (converges when |r|<1)",
  "Model exponential processes such as viral spread and population growth",
  "Finite Sum",
  "First term a1=1, ratio r=2, n=10 terms: S=1×(2^10−1)/(2−1)=1023. That is, 1+2+4+…+512=1023.",
  "Infinite Series",
  "When |r|<1 the infinite sum is S=a1/(1−r); e.g. 1+1/2+1/4+…=1/(1−0.5)=2, converging to 2.",
  "What are the two versions of the geometric sum formula?",
  "For finitely many terms S=a1(1−r^n)/(1−r); for infinitely many terms with |r|<1, S=a1/(1−r). An infinite series with |r|≥1 diverges and has no finite sum.",
  "What if the ratio r=1?",
  "When r=1 the denominator is 0 and the formula fails; every term is then equal, so the sum is simply n×a1.",
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
