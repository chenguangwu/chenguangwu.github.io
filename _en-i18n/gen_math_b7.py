#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""math 第7批：power-calc / prime-check / quadratic-discriminant / quadratic-solver / root-calc"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'math')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'math')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or '')[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'math', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- power-calc (21) ----------------
write('power-calc', build('power-calc', [
    "Compute a base x raised to the power y.",
    "Power Calculator",
    "/ Power",
    "Power",
    '📖 View the "x^y Guide"',
    "Power x^y: the result r = x to the power y; scientific notation shows r while grouped digits show the raw value; the common log log10(r) = y times log10(x); the reciprocal 1/r = x to the power -y; when the base is greater than 1 a larger exponent gives a larger result, and when the base is less than 1 the opposite holds.",
    "Base x",
    "Exponent y",
    "Fractional exponents are supported (a root is y=0.5).",
    "📚 In-Depth Analysis: Exponents aⁿ",
    "Computing compound interest, population growth and other exponential growth",
    "Powers of 10 in scientific notation",
    "Term values of a geometric series",
    "Integer Powers",
    "2^10=1024, 3^4=81. A negative exponent means the reciprocal: 2^-3=1/8=0.125; the zero exponent a^0=1 (a≠0).",
    "Fractional Exponents",
    "a^(1/2)=√a, a^(m/n)=ⁿ√(a^m). For example, 8^(2/3)=(∛8)²=2²=4.",
    "Negative and zero exponents?",
    "a^-n=1/a^n; a^0=1 (a≠0). Exponent rules: a^m·a^n=a^(m+n), (a^m)^n=a^(mn).",
    "Why is 0^0 undefined?",
    "From a^0=1 it should be 1, and from 0^a=0 it should be 0 - a conflict; so 0^0 is treated as an indeterminate form in ordinary arithmetic and must be handled by context (combinatorics, for instance, sets it to 1).",
]))

# ---------------- prime-check (20) ----------------
write('prime-check', build('prime-check', [
    "Prime Testing by Trial Division",
    "Determine whether a given positive integer is prime.",
    "Prime Check Calculator",
    "/ Prime Check",
    "Prime Check",
    '📖 View the "Prime Testing by Trial Division Guide"',
    "97 is prime.",
    "Trial division up to √n is enough.",
    "📚 In-Depth Analysis: Primality Testing",
    "Deciding whether a number is prime (divisible only by 1 and itself)",
    "Screening large primes before cryptographic key generation",
    "The basic test behind sieves and number-theory problems",
    "Trial Division",
    "To test whether 97 is prime, trial-divide only up to √97≈9.8, i.e. 2,3,5,7. None divides it, so 97 is prime. 1 is not prime; 2 is the smallest prime and the only even prime.",
    "Spotting a Composite",
    "Testing 91: √91≈9.5, and trial-dividing by 7 gives 91=7×13, so it is composite (easily mistaken for a prime).",
    "Why is trial division only needed up to √n?",
    "If n has a factor pair a×b=n with a≤b, then a≤√n; once we pass √n without finding a factor, any larger factor would pair with a smaller factor already tested, so none can remain - testing up to √n is enough.",
    "Is 1 a prime number?",
    "No. A prime is defined as a number with exactly two positive divisors (1 and itself); 1 has only one positive divisor and is therefore excluded, by modern convention.",
]))

# ---------------- quadratic-discriminant (16) ----------------
write('quadratic-discriminant', build('quadratic-discriminant', [
    "Discriminant from Quadratic Coefficients",
    "Enter the quadratic coefficients a, b, c to compute the discriminant.",
    "Quadratic Discriminant Calculator",
    "/ Quadratic Discriminant Calculator",
    '📖 View the "Discriminant from Quadratic Coefficients Guide"',
    "Δ>0: two real roots; Δ=0: a repeated root; Δ<0: complex roots.",
    "📚 In-Depth Analysis: The Quadratic Discriminant",
    "Judging the number and nature of the real roots without solving",
    "Determining how a parabola meets the x-axis",
    "Checking the existence of solutions in optimization problems",
    "Intersection Test",
    "For y=x²-4x+3 the discriminant is Δ=16-12=4>0, so the parabola meets the x-axis at two points (x=1 and x=3); Δ=0 touches at a single point, and Δ<0 gives no intersection.",
    "What does Δ<0 mean?",
    "The equation has no real roots (the two roots are complex conjugates), which corresponds to a parabola that does not meet the x-axis. In real-domain problems this means no solution, or a need to relax the constraints.",
    "How does the discriminant relate to factorization?",
    "When Δ is a perfect square the equation factors over the rationals; when it is not a perfect square the roots are irrational and must be found by radicals.",
]))

# ---------------- quadratic-solver (18) ----------------
write('quadratic-solver', build('quadratic-solver', [
    "Use the discriminant to solve for the two roots of a quadratic equation.",
    "Quadratic Equation Solver",
    "/ Quadratic Roots",
    "Quadratic Roots",
    '📖 View the "Quadratic Equation Solver Guide"',
    "x²−3x+2=0 → roots 2, 1.",
    "📚 In-Depth Analysis: Solving Quadratic Equations",
    "Finding the roots of ax²+bx+c=0, common in physics, projectiles and optimization",
    "Using the discriminant to count the real roots",
    "Root-finding for positioning in engineering models",
    "The Quadratic Formula",
    "x²-5x+6=0: Δ=b²-4ac=25-24=1>0 gives two real roots x=(5±1)/2, namely x=3 or x=2. This checks out by factoring (x-2)(x-3)=0.",
    "Meaning of the Discriminant",
    "Δ>0: two distinct real roots; Δ=0: one repeated real root; Δ<0: two complex conjugate roots. For x²+x+1=0, Δ=-3<0, so the roots are complex.",
    "How do I use the discriminant Δ?",
    "Δ=b²-4ac determines the nature of the roots: positive for two distinct real roots, zero for one repeated real root, negative for two complex roots. Compute Δ first, then decide.",
    "What is the quadratic formula?",
    "x=(-b±√Δ)/(2a). When b is even, the reduced form x=(-b/2±√(b²/4-ac))/a cuts the work.",
]))

# ---------------- root-calc (21) ----------------
write('root-calc', build('root-calc', [
    "√x and ∛x",
    "Compute square roots and cube roots.",
    "Root Calculator",
    "/ Root Calculation",
    "Root Calculation",
    '📖 View the "√x and ∛x Guide"',
    "Square root √x and cube root ∛x: √x satisfies (√x)² = x and ∛x satisfies (∛x)³ = x; the fourth root is x to the power 1/4; the reciprocal relation is 1 ÷ √x = x to the power −1/2. Over the reals the square root is defined only for non-negative numbers.",
    "📚 In-Depth Analysis: Roots and Radicals",
    "Find ",
    "Square Root",
    ", Cube Root and other nth roots",
    "Recovering a side length from an area, or an edge length from a volume",
    "Standard deviation calculation",
    " contains a square-root step",
    "√144=12 because 12²=144; √2≈1.414. Negative numbers have no real square root; in the complex numbers they are imaginary (e.g. √(-1)=i).",
    "Cube Root",
    "∛27=3, ∛(-8)=-2 (odd roots can be taken of negative numbers and keep the sign).",
    "How do square and cube roots differ for negative numbers?",
    "Even roots (square, fourth, …) cannot be taken of negative numbers over the reals; odd roots (cube, fifth, …) can, and the result keeps the sign of the radicand.",
    "Does √x² equal x?",
    "No, it equals |x| (the absolute value), because a square root is non-negative. For example √((-3)²)=√9=3=|-3|.",
]))
