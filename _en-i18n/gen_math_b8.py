#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""math 第8批（收尾）：slope-line / index"""
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


# ---------------- slope-line (19) ----------------
write('slope-line', build('slope-line', [
    "Compute a line's slope from the coordinates of two points.",
    "Line Slope Calculator",
    "/ Line Slope",
    "Line Slope",
    '📖 View the "Line Slope Calculator Guide"',
    "(1,2)→(4,8) has slope 2.",
    "A zero denominator means a vertical line.",
    "📚 In-Depth Analysis: Line Slope",
    "Measuring how steeply the line through two points rises",
    "Judging whether a function increases or decreases, and its trend",
    "Converting engineering grades and road elevation angles",
    "Slope from Two Points",
    "Through (1,2) and (4,8): slope m=(8-2)/(4-1)=6/3=2, i.e. y increases by 2 for every 1 that x increases. A vertical line has no slope (denominator 0).",
    "Slope and Angle",
    "m=tanθ; m=1 corresponds to 45° and m=√3 to 60°. A negative slope means a downward trend.",
    "Which lines have slope 0 and no slope?",
    "Slope 0 is a horizontal line (constant y); no slope (denominator 0) is a vertical line (constant x).",
    "How are slope and inclination angle related?",
    "m=tanθ, where θ is the angle from the positive x-axis. This lets you go from slope back to angle, or from angle to slope.",
]))

# ---------------- index (77) ----------------
write('index', build('index', [
    "🧮 Math Calculators",
    "Math",
    "Math Calculators",
    "Percentage Change Calculator",
    "Δ% = (New − Old) / Old × 100%",
    "Quadratic Equation Solver",
    "The quadratic equation solver uses the discriminant Δ=b²−4ac to find the two roots of ax²+bx+c=0, supporting both real and complex roots, ideal for algebra homework and engineering equation solving.",
    "Law of Cosines Side Calculator",
    "Enter two sides a, b and their included angle C (degrees) to compute the third side by c = √(a²+b²−2ab·cosC), useful for solving non-right triangles.",
    "Exponential Equation Solver",
    "Enter the base a and the result b to solve the exponential equation a^x = b for the exponent x via x = ln b/ln a, used in logarithmic and exponential work.",
    "Quadratic Discriminant Calculator",
    "Enter the quadratic coefficients a, b, c to compute the discriminant Δ = b²−4ac, from which the number and nature of the real roots follow.",
    "Logarithm with Any Base Calculator",
    "The any-base logarithm calculator uses the change-of-base formula to find a logarithm with any base, handy for logarithm conversion and inverse-exponential work in mathematics, information theory and engineering.",
    "Vector Dot Product Calculator",
    "The dot product calculator sums the component-wise products A·B of two vectors, supports 3D, and suits projections, angles and similarity in geometry, physics and machine learning.",
    "Geometric Sequence nth Term Calculator",
    "Enter the first term a₁, the common ratio r and the number of terms n to compute the nth term of a geometric sequence by aₙ = a₁·r^(n−1).",
    "Law of Sines Side Calculator",
    "Find an unknown side from a known side, angle and opposite angle",
    "Heron's Formula Area Calculator",
    "Enter the three sides a, b, c of a triangle to compute its area by Heron's formula A = √[s(s−a)(s−b)(s−c)], with no height required.",
    "Arithmetic Series Sum Calculator",
    "Sum an arithmetic series from the number of terms and the first and last terms",
    "Geometric Series Sum Calculator",
    "Sum a geometric series from the first term, common ratio and number of terms",
    "GCD / LCM Calculator",
    "Enter two or more integers to find the greatest common divisor (GCD) by the Euclidean algorithm and from it the least common multiple (LCM), used for reducing and comparing fractions.",
    "2×2 Determinant Calculator",
    "Enter the 2×2 matrix entries a, b, c, d to compute the determinant |A| = ad−bc, a basic linear-algebra operation.",
    "Circular Permutation Calculator",
    "The circular permutation calculator uses P=(n−1)! to find the number of ways n elements can be arranged around a circle, suited to combinatorics, seating plans and probability problems.",
    "Distance Between Two Points Calculator",
    "The 2D distance calculator finds the Euclidean distance between two points from their coordinates, supports batches, and suits distance measurement in geometry, mapping and graphics.",
    "Line Slope Calculator",
    "The line slope calculator finds the slope k of a line from two points' coordinates, suited to analytic geometry, function plotting and the grade of engineering slopes such as roads and roofs.",
    "Prime Check Calculator",
    "The prime checker uses trial division to decide whether a given positive integer is prime, showing the result and the factors, ideal for number-theory study, cryptography basics and algorithm practice.",
    "Arithmetic Mean Calculator",
    "Enter a set of values separated by commas or spaces to compute their arithmetic mean x̄ = Σx/n, a quick way to get a statistical average.",
    "The geometry calculator handles area, volume and perimeter for common 2D/3D shapes, covering circles, triangles, spheres, cylinders and more, suited to study, engineering and everyday geometric quantities.",
    "Combinations with Repetition Calculator",
    "Compute combinations with repetition from the number of types and the number chosen",
    "Multinomial Coefficient Calculator",
    "Compute a multinomial coefficient from the total and each category count",
    "Fibonacci nth Term Calculator",
    "The Fibonacci nth term calculator uses iteration to find the nth term of the sequence quickly, suited to sequence study, algorithm demos and calculations tied to natural patterns such as the golden ratio.",
    "Root Calculator",
    "The root calculator finds square roots, cube roots and roots of any degree, accepts positive and negative input, and suits radical work and size derivation in mathematics, geometry and engineering.",
    "Factorial Calculator",
    "The factorial calculator finds the factorial n! of a non-negative integer, defines 0!=1, supports large numbers, and suits factorial work in permutations, probability and series.",
    "Combination Calculator",
    "The combination calculator finds the number of ways to choose r items from n, C(n,r), supports large numbers, and suits probability, statistics, lotteries and combinatorics.",
    "Permutation Calculator",
    "The permutation calculator finds the number of arrangements of r items chosen from n, P(n,r), suited to ordered selection in combinatorics, scheduling and probability.",
    "Supports many common percentage operations (finding a percentage, increase/decrease, proportion and more); enter any two known values to get the third automatically, for everyday and financial ratio work.",
    "Based on the proportion A:B=C:D, enter any three terms to solve for the unknown fourth, useful for recipe scaling, map scales and similar-figure calculations.",
    "Common Formulas",
    "A quick reference to common formulas: built-in mathematics, physics, chemistry and geometry formulas; fill in the parameters to compute, with unit-convention hints.",
    "Power",
    "The power calculator finds a base x raised to the power y, x^y, supports integer and fractional exponents, and suits exponential work in mathematics, compound interest and scientific computing.",
    "Modulo Operation",
    "The modulo calculator finds the remainder of a divided by b, supports positive and negative numbers, and suits modulo verification in programming, hashing and periodic problems.",
    "Circle Area / Circumference",
    "Enter any one of radius, diameter, area or circumference to compute the other three automatically, for converting a circle's geometric parameters.",
    "Enter any two sides of a right triangle to compute the third side and the two acute angles automatically, for geometric and engineering measurement.",
    "The calculus toolkit supports derivatives, indefinite integrals, limits and series expansion, returning results as you type the expression; suited to advanced-math study, homework checking and engineering function analysis.",
    "The equation solver handles linear and quadratic equations in one unknown and 2- and 3-variable linear systems, returning roots or solutions as you enter coefficients; suited to math homework, engineering computation and system verification.",
    'About "Math Calculators"',
    "The Math Calculators collection brings together 36 free online tools covering the common calculation, conversion and lookup needs in mathematics. Whether you work in the field, are a student, or are a general user, you will find practical tools you can pick up and use. All tools run entirely in the front end, with no data uploaded to any server, protecting your privacy.",
    "The math tools on this page include (a selection of representative tools):",
    "These tools help you finish common math tasks quickly - no need to memorize complex formulas or convert by hand, just enter your values and get the result.",
    "Do the math tools require a download or sign-up?",
    "No. Every math tool on this page is a purely front-end online tool you can use directly as soon as the page opens - no software to install, no account to create, and no data uploaded.",
    "Are the math tools' results accurate and is my data safe?",
    "The tools compute locally in your browser from published mathematical formulas and widely accepted industry standards, giving instant results. All computation happens on your own device, no data is uploaded to any server, and your privacy is protected.",
]))
