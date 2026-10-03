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
    write('complex-number', build('complex-number', [
        "🧮 Complex Number Calculator (Math)",
        "Performs addition, subtraction, multiplication and division of complex numbers, converts to polar form (modulus and argument), and visualizes on the complex plane.",
        "Performs professional calculation from the input parameters and outputs the result, based on 'addition, subtraction, multiplication and division of complex numbers, polar-form (modulus and argument) conversion, and visualization on the complex plane'.",
        "Complex A = a + bi",
        "Real part a",
        "Imaginary part b",
        "Complex B = c + di",
        "Real part c",
        "Imaginary part d",
        "Conjugate Ā",
        "Modulus |A|",
        "Select an operation to view the result",
        "📐 Complex Number Formulas",
        "Addition:",
        "Multiplication:",
        "Division:",
        "Polar form:",
        "Conjugate:",
        "📚 In-Depth: Complex Number Calculator (Math)",
        "Circuit analysis",
        "Impedance is often expressed as the complex number Z = R + jX; entering the real and imaginary parts quickly gives the modulus |Z| and argument (phase), used to judge resonance and power factor.",
        "In signal and vibration problems, two sinusoids can be represented by complex phasors; complex multiplication/division yields the combined amplitude and phase difference.",
        "In complex-plane geometry or the basics of quantum mechanics, conjugates, reciprocals and rotations are needed; the complex calculator gives results directly.",
        "Example: Modulus and Argument (A=3+4i, B=1-2i)",
        "Modulus |A| = √(3²+4²) = 5; |B| = √(1²+(-2)²) = √5 ≈ 2.2361. Argument arg(A) = atan2(4,3) ≈ 53.13°, arg(B) = atan2(-2,1) ≈ -63.43° (principal range (-180°,180°]).",
        "Example: Multiplication and Division",
        "A×B = (3+4i)(1-2i) = 3-6i+4i-8i² = 11-2i. For division use the denominator's conjugate: A/B = (3+4i)(1+2i)/((1-2i)(1+2i)) = (-5+10i)/5 = -1+2i.",
        "How is the principal range of the argument defined?",
        "Most math libraries (including this tool) take the principal value arg ∈ (-π,π], i.e. (-180°,180°]. For a [0,360°) representation, add 360° to negative angles. Phases differing only by an integer multiple of 2π are physically equivalent.",
        "Why multiply by the conjugate in complex division?",
        "Turn the denominator into a real number: 1/(a+bi) = (a-bi)/(a²+b²), converting division into multiplication by a real coefficient. This also explains the geometric meaning of |A/B| = |A|/|B| and arg(A/B) = arg(A) - arg(B).",
        "About 'Complex Number Calculator'",
        "The complex number calculator is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
    ]))
    write('function-plotter', build('function-plotter', [
        "🧮 Function Graph Plotter",
        "Uses Canvas to plot common function graphs: linear, quadratic, trigonometric, exponential and logarithmic functions, with custom parameters and coordinate ranges.",
        "Performs professional calculation from the input parameters and outputs the result, based on 'uses Canvas to plot common function graphs: linear, quadratic, trigonometric, exponential and logarithmic functions, with custom parameters and coordinate ranges'.",
        "Function type",
        "Linear y = ax + b",
        "Quadratic ax² + bx + c",
        "Trigonometric",
        "Exponential a·b^x",
        "Logarithmic a·log_b(x)",
        "Custom",
        "X min",
        "X max",
        "Y min",
        "Y max",
        "Auto-fit Y range",
        "Reset view",
        "Save image",
        "Move the mouse to read coordinates",
        "📐 Usage Instructions",
        "Custom function:",
        "Enter an expression with variable x; you may use sin, cos, tan, exp, log, sqrt, abs, pow, PI, E, etc.",
        "Example:",
        "Interaction:",
        "Moving the mouse over the graph shows the corresponding coordinate values; the auto-fit Y range adjusts automatically based on the current X range.",
        "📚 In-Depth: Function Graph Plotting",
        "In function teaching, enter y=f(x) to observe the graph shape, zeros, monotonicity and extrema, aiding understanding of derivatives and integrals.",
        "In engineering waveform analysis, plot sin/cos and damped oscillation curves to read period, amplitude and phase.",
        "In data exploration, first plot the curve of an empirical formula, then compare with scatter points to judge whether the fit is reasonable.",
        "Example: Sine function f(x) = sin x",
        "Amplitude A=1, period T=2π≈6.2832, zeros at x=kπ (k∈ℤ). Within [-10,10] the zeros are k=-3...3, i.e. -9.4248, -6.2832, ..., 9.4248. Formula: f(x)=sin x, max=1, min=-1.",
        "Example: Effect of Parameters on the Graph",
        "For f(x)=A·sin(ωx+φ), the amplitude is set by A, the period T=2π/ω, and the phase shift is -φ/ω. Substituting A=2, ω=1, φ=π/2 gives amplitude 2, period 6.2832, and a left shift of π/2.",
        "What if the graph shows aliasing or breaks?",
        "Usually caused by insufficient sample points or too large a domain span. Increase sampling resolution and set a reasonable x range; near singularities (e.g. 1/x at x=0) the tool may auto-break or clip, which is normal.",
        "How to read the period and extrema?",
        "For a periodic function, the period is the horizontal distance between two adjacent in-phase points (e.g. two adjacent peaks); the peak ordinate is the maximum and the trough is the minimum. The plotter's cursor/coordinate readout helps precise positioning.",
        "About 'Function Graph Plotter'",
        "The function graph plotter is an online tool in the scientific research field. A scientific research tool that uses standard scientific formulas for accurate calculation.",
    ]))
    write('index', build('index', [
        "🧮 General Calculation Tools",
        "General Calculation",
        "General Calculation Tools",
        "Supports addition, subtraction, multiplication and division of complex numbers and mutual conversion with polar form (modulus, argument), and intuitively plots point positions on the complex plane; suitable for teaching demos in engineering math and circuit phasor analysis.",
        "Generates odd-order magic squares where every row, column and diagonal sums equally; the order is adjustable and verifiable, for math games and teaching demos; the board is generated pure-front-end and copyable.",
        "Enter a logical expression; variables are auto-detected and a complete truth table is generated. Supports AND, OR, NOT, XOR, implication, equivalence, etc.",
        "Two-way conversion between standard decimals and scientific notation (a×10^n), supporting engineering notation and E notation.",
        "Select a distribution type (normal, Poisson, binomial), enter parameters like mean/variance or success probability and trial count, and compute the corresponding probability density and cumulative distribution probabilities. Used for probability-statistics teaching, quality analysis and risk modeling.",
        "Convert values among SI unit prefixes (nano / micro / milli / kilo / Mega / Giga / Tera, etc.).",
        "Uses Canvas to plot common function graphs: linear, quadratic, trigonometric, exponential and logarithmic functions, with custom parameters and coordinate ranges.",
        "Built-in 30+ common physics constants, with values, units, symbols and descriptions, supporting search and category filtering. Data based on CODATA 2018 recommended values.",
        "24 Game",
        "Use 4 numbers and +, -, ×, ÷, parentheses to form an expression that equals 24. Each number must be used exactly once.",
        "About 'General Calculation Tools'",
        "The general calculation tools collection includes 9 free online tools, covering common calculation, conversion and lookup needs in general-calculation scenarios. Whether you are a professional, student or general user in the field, you can find ready-to-use handy tools here. All tools run entirely in the browser, no data uploaded to servers, your privacy and security protected.",
        "The general calculation tools on this page include (representative tools):",
        "These tools help you quickly complete common general-calculation tasks without memorizing complex formulas or manual conversion; enter values to get results.",
        "Do the general calculation tools need download or registration?",
        "No. All general calculation tools on this page are pure front-end online tools; open the page to use them directly, no software installation, no account registration, and no data upload.",
        "Are the general calculation tools' results accurate? Is the data safe?",
        "The tools calculate locally in your browser based on public math formulas and common industry standards, with instant results. All computation is done on your device locally, data is never uploaded to servers, and privacy and security are guaranteed.",
    ]))

if __name__ == '__main__':
    main()
