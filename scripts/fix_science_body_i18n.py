#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""science 分类英文态数据源根治：同步三端 + 补缺失条目 + 清孤儿键。

背景（与 general / finance / design 同坑，§6「英文态数据源三处」）：
  页面可见英文（p / desc-en meta / ed）只是表象；`?lang=en-US` 与 industry JSON 的 ed
  还取决于三个数据源，只改页面会导致英文态仍是占位串 / 工具代号：
    ① i18n/tools/science-body.json   -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
    ② i18n/tools/science.json en-US  -> industry JSON 的 ed 最高优先级源（tool_desc_source.en_desc）
    ③ i18n/tools/_en_override.json   -> 运行时 en（h2/h1）与 ed

用法：
  python3 scripts/fix_science_body_i18n.py --dry-run
  python3 scripts/fix_science_body_i18n.py --apply
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'science')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'science-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'science.json')

PH = 'is available directly in your browser'
OLD_PH = 'supports a focused'

# NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
# 每条 INTRO 依据页面 zh-CN intro 的实际用途撰写，避免 "free online tool" 类套话。
NAME = {
    'anova-calculator': 'One-Way ANOVA Calculator',
    'astro-geo-calculator': 'Astronomy & Geography Calculator',
    'astronomy-toolkit': 'Astronomy Observation Toolkit',
    'barcode-pharmacode': 'Pharmacode Barcode Generator',
    'battery-life-calculator': 'Battery Life Calculator',
    'calc-1': 'Free Fall Motion Calculator',
    'calc-2': 'Ideal Gas Law Calculator (PV = nRT)',
    'calc-4': 'Density / Mass / Volume Converter',
    'calc-5': 'Speed / Distance / Time Calculator',
    'calc-cycle': 'Molar Mass Calculator',
    'calc-distance': 'Geographic Distance Calculator (Lat/Lon)',
    'calc-stats': 'Descriptive Statistics Calculator',
    'calculator': 'Scientific Calculator',
    'centripetal-force': 'Centripetal Force Calculator',
    'chemistry-calculator': 'Chemistry Calculator',
    'chi-square-calculator': 'Chi-Square Test Calculator',
    'combination-calculator': 'Combinations Calculator C(n,r)',
    'convert-power': 'Physics Unit Converter (Force, Work, Power)',
    'correlation-calculator': 'Pearson Correlation Calculator',
    'coulomb-force': "Coulomb's Law Calculator",
    'cycle': 'Interactive Periodic Table',
    'density-physics': 'Density Calculator (ρ = m/V)',
    'doppler-effect': 'Doppler Effect Calculator',
    'effect-size-calculator': "Effect Size Calculator (Cohen's d)",
    'electric-field-point': 'Point Charge Electric Field Calculator',
    'equation-balancer': 'Chemical Equation Balancer',
    'exp-calculator': 'Exponential Function Calculator',
    'factorial-calculator': 'Factorial Calculator',
    'fibonacci': 'Fibonacci Sequence Generator',
    'fraction-calculator': 'Fraction Calculator',
    'gcd-calculator': 'Greatest Common Divisor (GCD) Calculator',
    'geo-distance-calculator': 'Geography Distance Calculator',
    'gravitational-potential': 'Gravitational Potential Energy Calculator',
    'heat-transfer-calculator': 'Heat Transfer Calculator',
    'hookes-law': "Hooke's Law Calculator (F = kx)",
    'kinetic-energy': 'Kinetic Energy Calculator',
    'latlon-utm-converter': 'Latitude/Longitude to UTM Converter',
    'lcm-calculator': 'Least Common Multiple (LCM) Calculator',
    'led-resistor-calculator': 'LED Current-Limiting Resistor Calculator',
    'log-calculator': 'Logarithm Calculator',
    'logic-gate-simulator': 'Logic Gate Simulator',
    'matrix-calculator': 'Matrix Calculator',
    'mean-calculator': 'Mean Calculator',
    'mechanical-power': 'Mechanical Power Calculator (P = F·v)',
    'median-calculator': 'Median Calculator',
    'meteor-crater-estimator': 'Meteor Crater Estimator',
    'mode-calculator': 'Mode Calculator',
    'molar-mass-calculator': 'Molar Mass Calculator',
    'nato-phonetic': 'NATO Phonetic Alphabet Converter',
    'newtons-second': "Newton's Second Law Calculator (F = ma)",
    'nth-root-calculator': 'Nth Root Calculator',
    'ohms-law-calculator': "Ohm's Law Calculator",
    'p-value-calculator': 'P-Value Calculator',
    'passphrase-generator': 'Passphrase Generator',
    'pcb-trace-width': 'PCB Trace Width Calculator (IPC-2221)',
    'pendulum-period': 'Pendulum Period Calculator',
    'percentile-calculator': 'Percentile Calculator',
    'periodic-table': 'Periodic Table of Elements',
    'permutation-calculator': 'Permutations Calculator P(n,r)',
    'ph-calculator': 'pH Calculator',
    'phone-lookup': 'Phone Number Lookup',
    'phone-qr': 'Phone Number QR Code Generator',
    'physics-calculator': 'Physics Formula Calculator',
    'pi-digits': 'Pi Digits Explorer',
    'polar-day-night': 'Polar Day & Night Calculator',
    'power-calculator': 'Exponent (Power) Calculator',
    'prime-number': 'Prime Number Tool',
    'probability-calculator': 'Probability Calculator',
    'projectile-range': 'Projectile Motion Calculator',
    'provident-fund': 'Housing Provident Fund Calculator',
    'quadratic-equation': 'Quadratic Equation Solver',
    'quartile-calculator': 'Quartile Calculator',
    'range-calculator': 'Range Calculator',
    'rc-time-constant': 'RC Time Constant Calculator',
    'resistor-color-code': 'Resistor Color Code Decoder',
    'rfc-validator': 'Mexican RFC Validator',
    'root-calculator': 'Square Root Calculator',
    'sample-size-calculator': 'Sample Size Calculator',
    'science-flow-rate': 'Pipe Flow Rate Calculator',
    'science-pressure-converter': 'Pressure Unit Converter',
    'si-unit-converter': 'SI Unit Converter',
    'significant-figures': 'Significant Figures Calculator',
    'spring-oscillation-period': 'Spring Oscillation Period Calculator',
    'star-magnitude-compare': 'Star Magnitude Brightness Comparison',
    'statistics-calculator': 'Statistics Calculator',
    't-score-calculator': 'T-Score Calculator',
    'text-extract-phones': 'Phone Number Extractor',
    'tide-height-estimator': 'Tide Height Estimator',
    'torque-converter': 'Torque Unit Converter',
    'trigonometry-calculator': 'Trigonometry Calculator',
    'variance-calculator': 'Variance Calculator',
    'vector-calculator': 'Vector Calculator',
    'voltage-divider-calculator': 'Voltage Divider Calculator',
    'wavelength-to-rgb': 'Wavelength to RGB Converter',
    'wire-gauge-converter': 'AWG Wire Gauge Converter',
    'work-done': 'Work Done Calculator',
    'xianxingfangchengzuqiujie-2yuan-3yuan': 'Linear Equation System Solver (2 or 3 Unknowns)',
    'yiyuanercifangchengqiujie': 'Quadratic Equation Solver (Step by Step)',
    'z-score-calculator': 'Z-Score Calculator',
}

INTRO = {
    'anova-calculator': 'Compare the means of three or more groups with one-way ANOVA: between/within sum of squares, the F statistic and a significance hint.',
    'astro-geo-calculator': 'Six astronomy and geography calculators in one: sunrise/sunset, earthquake energy, earth curvature, Beaufort wind scale, relative humidity and altitude pressure.',
    'astronomy-toolkit': 'Moon phase lookup, magnitude brightness comparison, impact crater estimation, lat/lon to UTM conversion, polar day/night check and observing-condition assessment.',
    'barcode-pharmacode': 'Generate a Pharmacode (pharmaceutical binary) barcode from any integer between 1 and 131070, rendered as wide and narrow bars for packaging.',
    'battery-life-calculator': 'Estimate how long a device runs from battery capacity (mAh/Ah), load current or power and circuit efficiency, for power-budget and runtime planning.',
    'calc-1': 'Solve free-fall time and impact velocity from drop height, initial velocity and gravity, with an optional air-resistance note.',
    'calc-2': 'Enter any three of pressure, volume, moles and temperature to solve the fourth with the ideal gas law PV = nRT (R = 8.314 J/mol·K).',
    'calc-4': 'Input any two of density, mass and volume to compute the third with ρ = m/V, with a preset table of common material densities.',
    'calc-5': 'Enter any two of speed, distance and time to solve the third for uniform-motion problems, with selectable speed units.',
    'calc-cycle': 'Parse a chemical formula including brackets and nesting, and compute its molar mass using the atomic weights of all 118 elements.',
    'calc-distance': 'Compute the great-circle distance between two points with the Haversine formula, accepting decimal degrees or degrees-minutes-seconds.',
    'calc-stats': 'Turn a data set into descriptive statistics: arithmetic mean, variance and standard deviation, for quick dispersion checks.',
    'calculator': 'A browser scientific calculator with the four operations, powers, logarithms, trigonometry, brackets and history, all offline.',
    'centripetal-force': 'Compute the centripetal force needed for uniform circular motion from mass, linear speed and radius with F = mv²/r.',
    'chemistry-calculator': 'Compute molar mass from a formula, and solve solution concentration, pH and the ideal gas law in one place for lab prep and study.',
    'chi-square-calculator': 'Compute the chi-square statistic and degrees of freedom from observed and expected frequencies, with a significance hint for independence tests.',
    'combination-calculator': 'Compute the number of ways to choose r items from n without repetition using C(n,r) = n! / (r!(n−r)!).',
    'convert-power': 'Convert between force, work and power units such as newtons, joules and watts, handling common metric prefixes.',
    'correlation-calculator': 'Compute the Pearson correlation coefficient from paired X and Y data to quantify the strength and direction of a linear relationship.',
    'coulomb-force': "Compute the electrostatic force between two point charges with F = k·q₁q₂/r² (k = 8.988×10⁹ N·m²/C²) in vacuum.",
    'cycle': 'An interactive periodic table: click any of the 118 elements for details, search by name, symbol or atomic number, and colour by category.',
    'density-physics': 'Compute density from mass and volume with ρ = m/V in g/cm³ or kg/m³, for material identification and buoyancy checks.',
    'doppler-effect': "Compute the observed frequency shift from wave speed, source frequency and the velocities of observer and source with f' = f(v+v_o)/(v−v_s).",
    'effect-size-calculator': "Compute Cohen's d and related effect sizes from group means, standard deviations and sample sizes for research reporting.",
    'electric-field-point': 'Compute the electric field strength at a distance from a point charge with E = k·q/r² (k = 8.988×10⁹) in vacuum.',
    'equation-balancer': 'Balance a chemical equation automatically to the smallest integer coefficients and verify atom conservation; supports brackets and hydrates.',
    'exp-calculator': 'Compute eˣ and related exponential expressions such as aˣ or e^(kx) for maths and science work.',
    'factorial-calculator': 'Compute n! = n × (n−1) × … × 2 × 1 with big-integer support, recommended up to n = 10,000.',
    'fibonacci': 'Generate a Fibonacci sequence of any length and watch the ratio of adjacent terms approach the golden ratio φ.',
    'fraction-calculator': 'Add, subtract, multiply and divide fractions with automatic reduction, and convert between fractions, mixed numbers and decimals.',
    'gcd-calculator': 'Find the greatest common divisor of two or more integers with the Euclidean algorithm, useful for fraction reduction and number theory.',
    'geo-distance-calculator': 'Compute the great-circle distance between two coordinates with the Haversine formula, plus bearing and a map preview.',
    'gravitational-potential': 'Compute gravitational potential energy from mass, gravity and height with E_p = mgh, referenced to a chosen datum.',
    'heat-transfer-calculator': 'Compute conductive, convective and radiative heat transfer from temperature difference, specific heat, mass and coefficients using Q = mcΔT and the Stefan-Boltzmann law.',
    'hookes-law': 'Compute the restoring force of a spring from its stiffness and extension with Hooke’s law F = kx.',
    'kinetic-energy': 'Compute translational kinetic energy from mass and speed with E_k = ½mv², with unit conversion.',
    'latlon-utm-converter': 'Convert between WGS84 latitude/longitude and UTM easting/northing coordinates based on the WGS84 ellipsoid.',
    'lcm-calculator': 'Compute the least common multiple of several positive integers with LCM(a,b) = |a·b| / GCD(a,b), for common denominators and period alignment.',
    'led-resistor-calculator': 'Compute the series current-limiting resistor, its power dissipation and the nearest standard value from supply voltage, LED forward voltage and rated current.',
    'log-calculator': 'Compute base-10 logarithms, natural logarithms and logs to any base, with base-change support for decibels and scaling work.',
    'logic-gate-simulator': 'Toggle inputs on AND, OR, NOT and XOR gates to see the live output level and boolean expression, and chain gates to explore combinational logic.',
    'matrix-calculator': 'Add, subtract and multiply matrices, transpose, and compute determinant, inverse, rank and powers for linear algebra and equation solving.',
    'mean-calculator': 'Compute the arithmetic, geometric and harmonic means of a data set for statistical and scientific analysis.',
    'mechanical-power': 'Compute mechanical power from force and aligned speed with P = F·v, with unit conversion for motors and conveyors.',
    'median-calculator': 'Sort a list of numbers and return the median, resistant to outliers, for skewed data such as scores, salaries and house prices.',
    'meteor-crater-estimator': 'Estimate impact crater diameter, released energy in TNT equivalent and affected range from meteor diameter, density, velocity and impact angle.',
    'mode-calculator': 'Find the most frequent value or values in a data set, including multi-modal and no-mode cases, for frequency analysis.',
    'molar-mass-calculator': 'Compute the molar mass of a chemical formula such as H2O, NaCl, C6H12O6 or H2SO4 from standard atomic weights.',
    'nato-phonetic': 'Convert any text letter by letter into the NATO phonetic alphabet (Alpha, Bravo, Charlie…) to avoid mishearing on radio and calls.',
    'newtons-second': "Compute the net force from mass and acceleration with Newton's second law F = ma, with unit conversion.",
    'nth-root-calculator': 'Compute the nth root of a number and show the steps, supporting any positive real radicand and non-zero root index.',
    'ohms-law-calculator': "Enter any two of voltage, current and resistance to solve the third with V = I×R and also compute power P = VI.",
    'p-value-calculator': 'Compute a p-value from a test statistic and degrees of freedom for t, chi-square and related tests, with a significance-level hint.',
    'passphrase-generator': 'Generate memorable high-entropy passphrases from a word list, choosing the number of words and the separator, all locally.',
    'pcb-trace-width': 'Compute the required copper trace width for a given current, copper weight and allowed temperature rise following the IPC-2221 standard.',
    'pendulum-period': 'Compute the small-angle period of a simple pendulum from its length and gravity with T = 2π√(L/g).',
    'percentile-calculator': 'Compute the value at a given percentile of a data set, for rank, growth-curve and distribution analysis.',
    'periodic-table': 'Browse all 118 chemical elements and click any one for atomic number, symbol, atomic weight, electron configuration and physical properties.',
    'permutation-calculator': 'Compute the number of ordered arrangements of r items from n with P(n,r) = n! / (n−r)!.',
    'ph-calculator': 'Convert between hydrogen-ion concentration, pH and pOH with pH = −log₁₀[H⁺] for chemistry and water-quality analysis.',
    'phone-lookup': 'Look up the number range, region and carrier of a phone number from built-in prefix data to identify where a call comes from.',
    'phone-qr': 'Turn a phone number into a scannable QR code that dials on scan, handy for business cards and posters, generated locally.',
    'physics-calculator': 'Solve common physics formulas across mechanics, thermodynamics and electromagnetism: pick a formula, enter the knowns and see the derivation.',
    'pi-digits': 'Display the first N decimal places of π, or find a specific digit or pattern, for maths demos and precision tests.',
    'polar-day-night': 'For a given latitude, compute the start and end dates and duration of polar day and polar night plus the annual sunlight profile.',
    'power-calculator': 'Compute a base raised to an exponent, with support for negative and fractional exponents in maths and engineering.',
    'prime-number': 'Test whether an integer is prime, generate prime tables in a range, or factorise a number into primes for number theory and coding.',
    'probability-calculator': 'Compute event probabilities for common discrete and continuous distributions and visualise the distribution curve.',
    'projectile-range': 'Compute horizontal range and maximum height from launch speed and angle with R = v²sin(2θ)/g and H = v²sin²θ/(2g).',
    'provident-fund': 'Compute monthly employee and employer housing-fund contributions and estimate the loan amount and monthly payment from salary base and rates.',
    'quadratic-equation': 'Solve ax² + bx + c = 0 and return real or complex roots along with the discriminant for algebra and parabola analysis.',
    'quartile-calculator': 'Compute the first, second and third quartiles and the interquartile range for distribution description and box-plot work.',
    'range-calculator': 'Compute the range of a data set from its maximum and minimum, with summary statistics for a quick spread check.',
    'rc-time-constant': 'Compute the RC time constant τ = R×C and the time to charge or discharge to a chosen percentage for filter and delay design.',
    'resistor-color-code': 'Decode 4- and 5-band resistor colour codes into resistance and tolerance, or reverse-search the colours from a resistance value.',
    'rfc-validator': 'Validate a Mexican RFC taxpayer registration number for length, structure and check digit. Format check only.',
    'root-calculator': 'Compute the principal square root of a number and return an imaginary result for negative inputs.',
    'sample-size-calculator': 'Compute the minimum survey sample size from population, confidence level, margin of error and expected proportion, with finite-population correction.',
    'science-flow-rate': 'Compute volumetric flow from pipe cross-section (or diameter) and flow velocity, or average flow from container volume and fill time.',
    'science-pressure-converter': 'Convert pressure values between pascals, bar, PSI, standard atmospheres and millimetres of mercury for engineering and meteorology.',
    'si-unit-converter': 'Convert across the seven SI base quantities, metric prefixes and derived units for consistent scientific notation.',
    'significant-figures': 'Normalise, round and format numbers to a specified number of significant figures for lab reports and data handling.',
    'spring-oscillation-period': 'Compute the oscillation period of a spring-mass system from mass and stiffness with T = 2π√(m/k).',
    'star-magnitude-compare': 'Compare the brightness of two stars from their magnitudes, or pick objects from a built-in star table, using the 100× per 5-magnitude rule.',
    'statistics-calculator': 'Compute descriptive statistics, a frequency distribution and a histogram, including sample variance, for data analysis and teaching.',
    't-score-calculator': 'Compute a t-score from sample mean, population mean, standard deviation and sample size, and convert Z or T scores for significance tables.',
    'text-extract-phones': 'Paste free text and extract every phone number it contains, mobile or landline, listed line by line for easy copying.',
    'tide-height-estimator': 'Estimate theoretical tide height from date, moon phase and latitude using a lunar-gravity model for coastal and fishing reference.',
    'torque-converter': 'Convert torque values between newton-metres, pound-feet and kilogram-force-metres for machinery and automotive selection.',
    'trigonometry-calculator': 'Compute inverse trigonometric angles from values with degree and radian modes, for trigonometric equations and geometric measurement.',
    'variance-calculator': 'Compute sample or population variance and standard deviation from a data set to quantify spread.',
    'vector-calculator': 'Add, subtract, dot and cross 2D or 3D vectors, compute magnitudes and angles, and visualise the vectors.',
    'voltage-divider-calculator': 'Compute the output voltage of a two-resistor divider from input voltage and resistor values, with unit conversion, for sensor biasing and level shifting.',
    'wavelength-to-rgb': 'Convert a visible wavelength between 380 and 780 nm into an approximate RGB colour and colour name for spectrum visualisation.',
    'wire-gauge-converter': 'Convert AWG wire gauge to metric diameter, cross-sectional area and resistance per kilometre, or reverse-look up the gauge.',
    'work-done': 'Compute the work done by a constant force from its magnitude, displacement and included angle with W = F·d·cosθ.',
    'xianxingfangchengzuqiujie-2yuan-3yuan': 'Solve a system of two or three linear equations with Cramer’s rule or elimination, showing the unknowns for algebra and engineering work.',
    'yiyuanercifangchengqiujie': 'Solve a quadratic equation step by step from coefficients a, b and c, returning real or complex roots from the discriminant.',
    'z-score-calculator': 'Compute the standard score Z from a value, population mean and standard deviation to standardise scores and detect outliers.',
}

# 缺失 zh-CN 条目的工具（页面中文标题存在但 i18n 无条目）：slug -> (中文名, 中文简介)
ZH_FILL = {
    'significant-figures': ('有效数字计算器', '按指定有效数字位数对数值进行规范化与舍入，用于实验数据记录与结果表达。'),
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov = load(OV)
    body = load(BODY)
    gis = load(GIS)

    chg_en = chg_ed = chg_body = added_body = added_gis = added_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'science/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'science'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'science')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + science-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + science.json 新增条目:', slug)
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if slug in ZH_FILL and not isinstance(g.get('zh-CN'), dict):
            zh_name, zh_intro = ZH_FILL[slug]
            g['zh-CN'] = {'h1': zh_name, 'title': zh_name, 'intro': zh_intro, 'desc': zh_name}
            added_zh += 1
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿键：body 中存在但全站无对应页面（与 general 的 random-10 同类）
    all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
    orphans = [key for key in list(body.keys()) if key not in all_basenames]
    print('\n--- 汇总 ---')
    print('science 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('science-body 更新:', chg_body, ' 新增:', added_body)
    print('science.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 补 zh-CN:', added_zh)
    print('science-body 孤儿键:', orphans)

    if a.dry_run:
        for s in slugs[:3]:
            print('\n预览 %s:\n  name = %r\n  intro= %r' % (s, NAME[s], INTRO[s]))
        return 0

    json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(body, open(BODY, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(gis, open(GIS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('\n已写入：_en_override.json(indent=1) / science-body.json(indent=2) / science.json(indent=2)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
