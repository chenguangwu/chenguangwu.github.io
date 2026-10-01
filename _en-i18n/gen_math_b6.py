import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
 'modulo-calc': [
  "Find the remainder of a divided by b.",
  "Modulo Calculator",
  "/ Modulo",
  "Modulo",
  "📖 View the \"mod b Guide\"",
  "a mod b = a − b × ⌊a ÷ b⌋, the remainder of a divided by b, with the sign following the dividend a; e.g. 17 mod 5 = 2; commonly used for periodic modulo, circular indices, and hash bucket selection (the congruence a ≡ a mod b is congruent modulo b).",
  "Dividend a",
  "Divisor b",
  "Used for periodicity and congruences.",
  "📚 In-Depth Analysis: Modulo",
  "Check parity (mod 2) and periodicity (e.g. computing the day of the week)",
  "Hashing and circular buffer indices",
  "Congruence cryptography (e.g. modular exponentiation in RSA)",
  "Cycle Calculation",
  "Today is Wednesday; what day is it 10 days later? (3+10) mod 7 = 13 mod 7 = 6, i.e. Saturday (with Sunday=0).",
  "Negative Modulo",
  "Languages differ on negative modulo: −7 mod 3 is 2 under mathematical congruence (since −7+9=2), but some languages return −1; mind the convention of your environment.",
  "Are modulo and remainder the same?",
  "They are the same for positive numbers; for negatives the definition differs by language (whether the quotient rounds toward 0 or toward −∞). When writing cross-",
  "language code",
  ", test the boundaries.",
  "Where is modulo commonly used?",
  "Periodicity (clocks, weekdays), hash indices (index mod size), and divisibility checks (a",
  " ==0 means b divides a).",
 ],
 'multinomial-coefficient': [
  "Multinomial Coefficient from the Total and Category Counts",
  "Enter the total n and three category counts k₁, k₂, k₃ (summing to n) to compute the multinomial coefficient.",
  "Multinomial Coefficient Calculator",
  "/ Multinomial Coefficient Calculator",
  "📖 View the \"Multinomial Coefficient from the Total and Category Counts Guide\"",
  "Category k₁",
  "Category k₂",
  "Category k₃",
  "The coefficients of multinomial expansion terms.",
  "📚 In-Depth Analysis: Multinomial Coefficient from the Total and Category Counts",
  "The multinomial coefficient C(n; k₁,k₂,…,k_m) appears as the coefficients in the multinomial expansion (x₁+…+x_m)ⁿ.",
  "It is also used to split n distinguishable objects into groups of specified sizes (allocation/grouping counting).",
  "The constraint k₁+k₂+…+k_m = n must hold, otherwise it is meaningless.",
  "Example: C(5; 2, 2, 1)",
  "= 5! / (2!×2!×1!) = 120 / (2×2×1) = 30. That is, the number of ways to split 5 distinct elements into 3 groups (sizes 2, 2, 1).",
  "Example: C(6; 3, 2, 1)",
  "How do multinomial and binomial coefficients relate?",
  "The binomial coefficient is the special case m=2: C(n;k,n−k) = n!/(k!(n−k)!) = C(n,k). The multinomial coefficient generalizes it to multiple groups.",
  "When do you use the multinomial coefficient?",
  "Use it when the expansion has more than two terms (e.g. (a+b+c)ⁿ) or when n objects must be split into multiple groups of fixed sizes. Order within groups is ignored and the group sizes are fixed — its typical features.",
 ],
 'nth-term-geometric': [
  "n-th Term from First Term, Ratio, and Count",
  "Enter the first term a₁, the ratio r, and the count n to find the n-th term.",
  "Geometric Sequence n-th Term Calculator",
  "/ Geometric Sequence n-th Term Calculator",
  "📖 View the \"n-th Term from First Term, Ratio, and Count Guide\"",
  "The basic formula for exponential growth.",
  "📚 In-Depth Analysis: n-th Term from First Term, Ratio, and Count",
  "The geometric sequence's n-th term aₙ = a₁·rⁿ⁻¹ is used for compound interest, radioactive decay, population growth, and depreciation modeling.",
  "The ratio r determines the trend: |r|>1 grows, 0<|r|<1 decays, r<0 oscillates.",
  "Unlike arithmetic sequences (linear), geometric sequences use multiplicative recurrence (exponential).",
  "Example: a₁=2, r=3, n=5",
  "Example: a₁=1, r=2, n=6",
  "a₆ = 1 × 2⁵ = 32.000. When the ratio is greater than 1, it grows exponentially.",
  "What is the difference between geometric and arithmetic sequences?",
  "Arithmetic adds a constant (aₙ=a₁+(n−1)d, linear), while geometric multiplies by a constant (aₙ=a₁·rⁿ⁻¹, exponential). The former increases by a fixed amount, the latter scales by a ratio — completely different growth shapes.",
  "What happens to the sequence when the ratio r<1?",
  "When 0<r<1 the sequence decreases toward 0 (e.g. decay, depreciation); when −1<r<0 it oscillates and decays; when r=0 every term from the second onward is 0. Note the formula still applies for small n, but interpret its physical meaning in context.",
 ],
 'percent-change': [
  "Δ% = (New − Old) / Old × 100%",
  "Compute the percentage change of a value.",
  "Percent Change Calculator",
  "/ Percent Change",
  "Percent Change",
  "📖 View the \"Percent Change Calculator Guide\"",
  "Δ% = (New−Old)/Old × 100%",
  "80→100 is +25%.",
  "A negative value indicates a decrease.",
  "📚 In-Depth Analysis: Percent Change",
  "Compute year-over-year growth rates and price swings",
  "Compare metric changes before and after an experiment",
  "Month-over-month / year-over-year in financial statements",
  "Price Swing",
  "Original price 80, new price 100: change rate = (100−80)/80×100% = 25% (a 25% rise). Reversed, 100→80 gives (80−100)/100 = −20% (a 20% fall). Note the base differs, so the results differ.",
  "Successive Changes",
  "A 10% rise then a 10% fall: 100×1.1×0.9=99, not back to 100, because the second 10% is based on the larger base.",
  " change: how is the base chosen?",
  "Always use \"(new−old)/old×100%\". Rises and falls are asymmetric: from 80 to 100 is +25%, from 100 back to 80 is −20%, because the denominator changed.",
  "Can multiple percentages be added directly?",
  "They cannot be added directly. Compound changes use multiplication (1+r1)(1+r2)…−1, because each is based on a new base.",
 ],
 'permutation': [
  "The number of permutations of r items chosen from n elements.",
  "Permutation Calculator",
  "Permutation Count",
  "📖 View the \"Permutation Calculator Guide\"",
  "Order matters.",
  "📚 In-Depth Analysis: Permutation P(n,k)",
  "Count ordered arrangements, such as passwords, queues, and schedules",
  "The number of ways to place n items in the top k positions",
  "Compute the size of an ordered sample space in probability",
  "Seating Arrangement",
  "Choosing the top 3 award seats from 10 people, the ",
  " P(10,3)=10×9×8=720. Every change of seating order counts as a different result.",
  "Full Permutation",
  "The full permutation of n items is n!=n×(n−1)×…×1; 3 books on a shelf = 3! = 6 ways.",
  "What is the P(n,k) formula?",
  "P(n,k)=n!/(n−k)!, i.e. multiply k numbers starting from n. E.g. P(10,3)=10!/7!=10×9×8.",
  "When do you use the full permutation n!?",
  "When k=n (everything is arranged), P(n,n)=n!. Whenever all items take part in the ordering, use the full permutation.",
 ],
}

EXTRA = {
 'percent-change': {'百分比': 'Percentage'},
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
