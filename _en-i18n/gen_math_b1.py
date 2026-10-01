import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
 'arithmetic-mean-math': [
  "Arithmetic Mean from a Number Sequence",
  "Enter several numbers separated by commas or spaces to compute the arithmetic mean.",
  "Arithmetic Mean Calculator",
  "/ Arithmetic Mean Calculator",
  "📖 View the \"Arithmetic Mean from a Number Sequence Guide\"",
  "The most commonly used measure of central tendency.",
  "📚 In-Depth Analysis: Arithmetic Mean",
  "Averaging multiple ",
  "Exam Scores",
  " gives the average score to gauge overall performance.",
  "Summarize the central tendency of a sample as a baseline for further analysis",
  "When comparing the average level of two data sets, compute the mean first and then compare",
  "Find the Average Score",
  "The arithmetic mean of 80, 90, 70, 100 = (80+90+70+100)/4 = 340/4 = 85. Note that the mean can be pulled up or down by extreme values; when outliers are present, consider the median instead.",
  "Weighted Average",
  "If three tests have weights 0.2/0.3/0.5 and scores 80/90/70, the weighted average = 80×0.2+90×0.3+70×0.5 = 16+27+35 = 78, which emphasizes the higher-weighted test more than a simple average.",
  "Mean",
  ", median, and mode?",
  "The mean is the sum divided by the count and is strongly affected by extreme values; the median is the middle value after sorting and is robust to outliers; the mode is the most frequent value. When the distribution is skewed these three diverge, so choose the right one for the situation.",
  "Why is the mean affected by extreme values?",
  "The mean adds every value equally and divides by the count, so one very large or very small value shifts the total and changes the result; the median only depends on position, so it is unaffected by the magnitude of the extremes.",
 ],
 'arithmetic-series-sum': [
  "Sum of an Arithmetic Series from Count and First/Last Terms",
  "Enter the number of terms n, the first term a₁, and the last term aₙ to compute the sum of the first n terms.",
  "Arithmetic Series Sum Calculator",
  "/ Arithmetic Series Sum Calculator",
  "📖 View the \"Sum of an Arithmetic Series from Count and First/Last Terms Guide\"",
  "Last term aₙ",
  "Gauss summation formula.",
  "📚 In-Depth Analysis: Arithmetic Series Sum",
  "Compute the cumulative total of a steadily increasing sequence, e.g. a fixed additional deposit each month with interest",
  "Given the first term, common difference, and count, find the total, used for arithmetic-sequence modeling",
  "Estimate the total height of a stepwise increase (e.g. step heights in arithmetic progression)",
  "Standard Sum",
  "First term a1=2, common difference d=3, n=10 terms: last term a10=2+(10−1)×3=29, sum S=10×(2+29)/2=155; alternatively S=n/2×[2a1+(n−1)d]=10/2×(4+27)=155.",
  "How many forms does the arithmetic series sum formula have?",
  "Two equivalent forms: S = n(a1+an)/2 (using the first and last terms) and S = n/2×[2a1+(n−1)d] (using the first term and common difference). The former is convenient when the last term is known, the latter when only the difference is known.",
  "How do you tell an arithmetic series from a geometric series?",
  "In an arithmetic series the difference between adjacent terms is constant (adding the same number); in a geometric series the ratio is constant (multiplying by the same number). Their sum formulas are completely different, so decide whether it adds or multiplies before choosing a formula.",
 ],
 'calc-1': [
  "🔢 Percentage Calculator",
  "Handle several common percentage operations; enter any two values and the result is computed automatically.",
  "📖 View the \"Percentage Calculator Guide\"",
  "Percent of a Value",
  "What Percent",
  "Find the Whole",
  "Percent Change",
  "Percentage p (%)",
  "Part A",
  "Whole B",
  "Enter percentages as plain numbers, e.g. for 15% enter 15.",
  "The percent-change result can be negative, indicating a decrease.",
  "📚 In-Depth Analysis: Percentage Calculator",
  "In daily life and business, four conversions are most common: \"P% of A\", \"what percent A is of B\", \"find the whole from a known percentage value\", and \"percent change\".",
  "Discounts, tax rates, ",
  "profit margins",
  ", completion rates, and proportions all reduce to one of the four above; the key is identifying the denominator (reference value).",
  "Reports and exams often confuse the reference for \"of\" versus \"is\"; you must be clear about the percentage's divisor, or the result can be off by an order of magnitude.",
  "Example: 15% of 200",
  "200 × 15 ÷ 100 = 30.0000, i.e. \"P% of A = A×P/100\".",
  "Example: share, finding the whole, and change",
  "30 as a percentage of 200 = 30 ÷ 200 × 100 = 15.0000%; given that 15% corresponds to 30, the whole = 30 ÷ (15/100) = 200.0000; from 200 up to 230, the increase = (230−200) ÷ 200 × 100 = 15.0000% (increase).",
  "Is there a difference between \"what percent A is of B\" and \"A is what percent of B\"?",
  "The formula is the same (A÷B×100%); the difference is wording. The denominator B in \"of\" is the total, and \"is ... percent of\" uses the same denominator B. The common error is inverting the denominator, so always identify the \"who\" in \"more than whom / of whom\" first.",
  "What is the difference between growth rate and percentage points?",
  "The growth rate is a relative change ((new−old)÷old×100%), while a percentage point is the absolute difference between two percentages (e.g. 30%→35% is a rise of 5 percentage points, not 5%). Mixing them up exaggerates or understates the magnitude of change.",
  "About \"Percentage Calculator\"",
  "The percentage calculator covers the four most common percentage operations: percent of a value, what percent, finding the whole, and percent change.",
  "Four modes with one-click switching",
  "Supports positive numbers and decimals",
  "Automatically determines increase or decrease",
  "Discount price calculation",
  "Score share conversion",
  "Sales growth analysis",
  "Everyday financial estimates",
 ],
 'calc-2': [
  "🔢 Proportion Calculator",
  "For the proportion A : B = C : D, enter any three terms to solve for the fourth.",
  "📖 View the \"Proportion Calculator Guide\"",
  "Ratio a:b = a/b",
  "Proportion: A : B = C : D ⟺ A × D = B × C. Leave the term to be solved blank and the tool computes it automatically.",
  "Enter at least three valid values, leaving one blank as the target to solve.",
  "The divisor term cannot be 0.",
  "📚 In-Depth Analysis: Proportion Calculator",
  "The proportion a:b = c:d (i.e. a/b = c/d) is widely used for map scaling, recipes, similar figures, and ",
  "Given three terms, solving for the fourth (cross-multiplication a×d = b×c) is the core operation of proportion calculation.",
  "To check whether two proportions are equal, compare the cross products, avoiding mistakes from reducing term by term.",
  "Example: solving a missing term (2:3 = 4:d)",
  "From a×d = b×c → d = b×c÷a = 3×4÷2 = 6.000000; check: 2×6 = 12.000000 and 3×4 = 12.000000, so the equation holds.",
  "Example: solving the first ratio (a:5 = 3:4)",
  "a = b×c÷d = 5×3÷4 = 3.750000. General rule: to find the missing term, cross-multiply the other three and divide by its diagonal.",
  "What is the relationship between ratios and ",
  "?",
  "A percentage is a proportion with a denominator of 100. Ratios emphasize the correspondence (a:b) while percentages emphasize relative size (a/100). They are interconvertible: 3:4 equals 75:100, i.e. 75%.",
  "Why does cross-multiplication hold?",
  "Multiplying both sides of a/b = c/d by b×d gives a×d = b×c. It is an equivalent transformation of the proportion, used to solve for unknowns and to verify equalities, and is the most reliable basis for proportion operations.",
  "About \"Proportion Calculator\"",
  "The proportion calculator solves for the unknown term using the basic property of proportions (the product of the means equals the product of the extremes), suited to all kinds of proportional allocation and conversion.",
  "Solve for any one of the four terms left blank",
  "Automatically detects the position of the unknown",
  "Clean interface, easy to understand",
  "Map scale conversion",
  "Recipe ratio calculation",
  "Image scaling size conversion",
  "Financial leverage and ratio estimation",
 ],
 'calc-3': [
  "🧮 Pythagorean Theorem",
  "Enter any two sides of a right triangle to compute the third side and the acute angles.",
  "📖 View the \"Pythagorean Theorem Guide\"",
  "Leg a",
  "Leg b",
  "Hypotenuse c",
  "Decimal places",
  "Formula: a² + b² = c² (c is the hypotenuse). Enter any two sides to find the third.",
  "The hypotenuse c must be greater than either leg.",
  "Enter non-negative side lengths.",
  "📚 In-Depth Analysis: Pythagorean Theorem",
  "In a right ",
  ", given two sides to find the third, or to check whether a right angle holds, is the basis of construction, navigation, and surveying.",
  "With two sides known you can also find the acute angles (via atan), useful for slopes and elevation angles.",
  "The hypotenuse must be strictly greater than either leg, otherwise the data is invalid.",
  "Example: given both legs (3, 4)",
  "Hypotenuse c = √(3²+4²) = 5.000000; ∠A = atan(3/4)×180/π = 36.87°, ∠B = 90 − 36.87 = 53.13°.",
  "Example: verifying a right angle (3, 4, 5)",
  "From a²+b² the hypotenuse should be √25 = 5.000000, matching the input → the Pythagorean theorem holds; if the input hypotenuse ≤ a leg, it is judged invalid.",
  "What are the conditions for applying the Pythagorean theorem?",
  "It applies only to right triangles, with the equality \"sum of the squares of the legs = square of the hypotenuse\". Non-right triangles require the law of cosines. The hypotenuse must be the largest side, otherwise no right triangle is formed.",
  "Why must the hypotenuse be greater than a leg?",
  "From c = √(a²+b²), c must exceed either a or b. If the input hypotenuse ≤ a leg, it is not a right triangle or the data is wrong, and solving for the other leg yields an imaginary/invalid result.",
  "About \"Pythagorean Theorem\"",
  "The Pythagorean theorem states that in a right triangle the sum of the squares of the two legs equals the square of the hypotenuse. This tool not only finds the third side but also computes the two acute angles.",
  "Find the third side from any two sides",
  "Automatically compute both acute angles",
  "Adjustable result precision",
  "Middle-school geometry problems",
  "Measuring building diagonals",
  "Screen size conversion",
  "Engineering drawing aid",
  "Enter or leave blank",
 ],
}

EXTRA = {
 'arithmetic-mean-math': {'中位数': 'median'},
 'calc-2': {'单位换算': 'unit conversion', '百分比': 'percentages'},
 'calc-3': {'三角形': 'triangle'},
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
