#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'misc')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'misc')
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
    out = {'slug': slug, 'industry': 'misc', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('statistics-distribution', build('statistics-distribution', [
        "📊 Statistical Distribution Calculator",
        "Computes the probability density and cumulative probability of the normal, Poisson and binomial distributions.",
        "Normal distribution",
        "Poisson distribution",
        "Binomial distribution",
        "📐 Distribution Notes",
        "📚 In-Depth: Statistical Distribution Calculator",
        "In quality control, use",
        "to estimate the probability that a product falls within specification limits, for yield and CpK evaluation.",
        "In reliability and queueing analysis, use",
        "to characterize the number of events per unit time (e.g. call volume, defect count).",
        "In clinical trials and A/B testing, use",
        "binomial distribution calculation",
        "the probability of the number of successes, assisting",
        "with significance judgment.",
        "Example: Normal Distribution Cumulative Probability",
        "For the standard normal N(0,1), the cumulative probability at x=1 is Φ(1)=P(X≤1)≈0.8413, i.e. about 84.13% of observations fall within 1",
        "standard deviation to the left of the mean. Formula: Φ(x)=∫₋∞ˣ φ(t)dt.",
        "Example: Poisson and Binomial Probabilities",
        "Poisson (λ=3), P(X=2)=e⁻³·3²/2!≈0.2240. Binomial (n=10, p=0.5), P(X=5)=C(10,5)·0.5¹⁰=252/1024≈0.2461. The two can approximate each other when n is large and p is small.",
        "How to read probabilities for continuous and discrete distributions?",
        "For continuous distributions (normal, uniform) the point probability is always 0; look at interval probability (CDF difference); discrete distributions (Poisson, binomial) can directly give P(X=k). Do not treat the density value as a probability - density can exceed 1, only the probability integral is ≤1.",
        "What is the relation between p-value and distribution calculation?",
        "A p-value is the probability of observing a 'more extreme' result under the null hypothesis; essentially it is the tail probability of a distribution (e.g. for a two-sided test, 2×(1-Φ(|z|))). Accurate distribution probability mass / density is the prerequisite for correctly interpreting significance conclusions.",
        "About 'Statistical Distribution Calculator'",
        "The statistical distribution calculator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
    ]))
    write('truth-table', build('truth-table', [
        "✨ Logic Truth Table Generator",
        "Enter a logical expression; variables are auto-detected and a complete truth table is generated. Supports AND, OR, NOT, XOR, implication, equivalence, etc.",
        "Logical expression (use letters for variables, e.g. A, B, C)",
        "Generate truth table",
        "Copy truth table",
        "OR",
        "NOT",
        "XOR",
        "NAND",
        "NOR",
        "Implication",
        "Equivalence",
        "📚 In-Depth: Logic Truth Table Generator",
        "In digital circuit design, list the output for each input combination to verify whether the combinational logic of AND, OR, XOR etc. is correct.",
        "In Boolean algebra and discrete math, use truth tables to prove equivalence laws (e.g. De Morgan's laws) or simplify expressions.",
        "In formal logic and programming conditionals, check the precedence and short-circuit behavior of complex Boolean expressions (including AND/OR/NOT and parentheses).",
        "Example: Expression A ∧ (B ∨ ¬C)",
        "Three variables give 2³=8 combinations. Traverse 000...111 in order A, B, C (high bit to low bit); the output sequence is 00001011 (true only when A=1 and (B=1 or C=0)).",
        "Example: Verifying De Morgan's Laws",
        "Compare the two columns ¬(A∧B) and (¬A∨¬B); if all 8 rows match, equivalence is proven. Similarly ¬(A∨B)≡(¬A∧¬B). The truth table is the most direct way to verify logical identities.",
        "Does the truth table explode when variables grow?",
        "Yes. n variables give 2ⁿ rows; n=10 is already 1024 rows, n=20 exceeds a million rows, impractical by hand. Then switch to algebraic simplification (Karnaugh map, Boolean algebra) or programmatic generation; the tool is generally display-friendly for n≤6 or so.",
        "How is operator precedence determined?",
        "Usually NOT > AND > OR (consistent with everyday and most languages), but parentheses take priority over everything. For complex expressions, add parentheses explicitly; the truth table tool evaluates by fixed precedence, so if the result differs from expectation, first check for missing parentheses.",
        "About 'Logic Truth Table Generator'",
        "The logic truth table generator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
        "A truth table lists the true/false (1/0 or T/F) of a proposition under all combinations of variable values, used to verify logical equivalence, tautologies and contradictions.",
        "Number of columns = variable count + result column; number of rows = 2^variable count. It can be used to check the truth values of compound propositions such as AND/OR/XOR/implication.",
        "e.g. A and B, A xor B, A -> B",
    ]))
    write('unit-prefix', build('unit-prefix', [
        "🔄 Unit Prefix Converter",
        "Convert values among SI unit prefixes (nano / micro / milli / kilo / Mega / Giga / Tera, etc.).",
        "Unit name (optional, e.g. m, Hz, W)",
        "From (source prefix)",
        "To (target prefix)",
        "Swap prefixes",
        "All prefix reference",
        "📐 Conversion Principle",
        "Method:",
        "First convert the source-prefix value to the base unit (multiply by 10^sourceExponent), then divide by 10^targetExponent to get the target-prefix value.",
        "Example:",
        "Power of 10",
        "📚 In-Depth: Unit Prefix Converter",
        "Engineering and",
        "physics calculation",
        "in which lengths, voltages and frequencies are converted among SI prefixes like km, m, mm, μm to avoid magnitude errors.",
        "In data processing, convert byte counts between KB, MB, GB and KiB, MiB (binary prefixes), distinguishing the 1000 and 1024 bases.",
        "In teaching and popular science, use the prefix table to quickly estimate orders of magnitude and understand the correspondence of Chinese/English number scales like thousand, million, billion.",
        "Example: Length Prefix Conversion",
        "1 km = 1×10³ m = 1000 m; 1 mm = 1×10⁻³ m = 0.001 m; 1 km = 1×10⁶ mm = 1,000,000 mm. General formula: value × 10^fromExp / 10^toExp.",
        "Example: SI vs Binary Prefix Difference",
        "1 KB (decimal) = 1000 B, while 1 KiB (binary) = 1024 B. 1 GB = 10⁹ B, 1 GiB = 2³⁰ ≈ 1.074×10⁹ B. Storage vendors mostly use decimal (GB), OSes mostly show binary (GiB); the difference is about 7%.",
        "How to distinguish k (kilo) and K (Kelvin)?",
        "Lowercase k is the prefix 'kilo' (10³), uppercase K is the temperature unit Kelvin. Prefixes",
        "are case-sensitive: m=10⁻³ (milli), M=10⁶ (mega); μ=10⁻⁶ (micro), must not be written as u (u is not a valid prefix).",
        "Why does a 1TB hard drive show only about 931GB?",
        "Vendors use decimal 1 TB=10¹² B, the system uses binary 1 TiB=2⁴⁰≈1.0995×10¹² B, so 1 TB≈0.909 TiB, and after file-system overhead it shows about 931 GiB. The essence is the difference between decimal and binary prefixes, not 'shrinkage'.",
        "About 'Unit Prefix Converter'",
        "The unit prefix converter is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
        "e.g. m, Hz",
    ]))

if __name__ == '__main__':
    main()
