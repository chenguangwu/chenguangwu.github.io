#!/usr/bin/env python3
# gen_metrology_b6.py — metrology b6 (3 slugs): type-b-uncertainty/uncertainty-propagation-product/uncertainty-propagation-sum
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metrology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metrology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'metrology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

TBU = [
 "From prior information, u_B = half-width a / coverage factor k.",
 "Type B Uncertainty",
 "/ Type B Standard Uncertainty",
 "Type B Standard Uncertainty",
 "📖 View Guide: \"Type B Uncertainty\"",
 "Interval half-width a",
 "For a rectangular distribution k = √3 ≈ 1.732.",
 "For a normal 95% interval k = 1.96/2.",
 "📚 Deep Dive: Type B uncertainty",
 "Evaluate uB from certificates or data",
 "Calibration certificates",
 "Uniform distribution",
 "u_B = a/√3 (half-width a of a uniform distribution). Example: a certificate value of ±0.5 μm treated as rectangular gives u_B = 0.5/1.732 = 0.29 μm.",
 "Half-width a=0.08, coverage factor k=2",
 "u_B = a/k = 0.04000; the share is 50.00%, meaning the standard uncertainty is exactly half the half-width, which corresponds to the common rectangular distribution /",
 "assumption difference.",
 "Distribution assumption?",
 "Use √3 for rectangular, √6 for triangular, and U/k for normal.",
 "Where does it come from?",
 "Certificates, handbooks, experience and resolution are all Type B sources.",
]

UPP = [
 "Find the combined relative uncertainty from the relative uncertainties of product-type variables",
 "Enter the variables x1, x2 and their standard uncertainties u1, u2 to get the combined relative uncertainty.",
 "Uncertainty Propagation (Product) Calculator",
 "/ Uncertainty Propagation (Product) Calculator",
 "📖 View Guide: \"Find the combined relative uncertainty from the relative uncertainties of product-type variables\"",
 "Variable x1",
 "Variable x2",
 "Product and quotient functions use the RSS of relative uncertainties.",
 "📚 Deep Dive: Product uncertainty propagation",
 "y = a*b type multiplicative models",
 "Reporting",
 "Error combination",
 "(u_y/y)^2 = (u_a/a)^2 + (u_b/b)^2 (independent). Example: relative values of 1% and 2% combine to sqrt(1+4) = 2.24%.",
 "Relative combined = sqrt((0.05/4)^2 + (0.06/8)^2) x 100% = 1.458%. In a product or quotient model each component's",
 "relative uncertainty",
 "is squared, summed and then square-rooted.",
 "Logarithmic method?",
 "Taking logs turns a product into a sum, so the relative uncertainties combine as a root sum square.",
 "Correlation?",
 "Positive correlation requires adding covariance terms.",
]

UPS = [
 "Find the combined uncertainty from sensitivity coefficients and component standard uncertainties",
 "Enter the sensitivity coefficients c1, c2 and the component standard uncertainties u1, u2 to get the combined uncertainty.",
 "Uncertainty Propagation (Linear) Calculator",
 "/ Uncertainty Propagation (Linear) Calculator",
 "📖 View Guide: \"Find the combined uncertainty from sensitivity coefficients and component standard uncertainties\"",
 "Sensitivity coefficient c1",
 "Component u1",
 "Sensitivity coefficient c2",
 "Component u2",
 "Propagation formula for a linear function.",
 "📚 Deep Dive: Sum and difference uncertainty propagation",
 "y = a ± b type linear models",
 "Reporting",
 "Error combination",
 "u_y^2 = u_a^2 + u_b^2 (independent). Example: u_a=1, u_b=2 gives u_y = sqrt(5) = 2.24.",
 "u_c = sqrt((2 x 0.15)^2 + (3 x 0.08)^2) = sqrt(0.09 + 0.0576) = 0.3842. The sensitivity coefficient amplifies the real influence of the second component.",
 "Coefficients?",
 "For y = c1*a + c2*b we have u_y^2 = (c1*u_a)^2 + (c2*u_b)^2.",
 "Versus products?",
 "Sums and differences use absolute uncertainty, products use",
 "relative uncertainty",
 "propagation.",
]

write('type-b-uncertainty', build('type-b-uncertainty', TBU))
write('uncertainty-propagation-product', build('uncertainty-propagation-product', UPP))
write('uncertainty-propagation-sum', build('uncertainty-propagation-sum', UPS))
