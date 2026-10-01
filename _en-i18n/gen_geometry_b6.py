#!/usr/bin/env python3
# gen_geometry_b6.py — geometry b6 (3 slugs): torus-volume/trapezoid-area/triangle-heron
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'geometry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'geometry')

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
    out = {'slug': slug, 'industry': 'geometry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

TRV = [
 "Torus volume from the major and tube radii",
 "Enter the major radius R (to the tube centre) and tube radius r to get the torus volume.",
 "Torus (Tyre) Volume Calculator",
 "/ Torus (Tyre) Volume Calculator",
 "📖 View Guide: \"Torus volume from the major and tube radii\"",
 "Major Radius R (m)",
 "📚 Deep Dive: Torus (doughnut) volume (V=2·pi2·R·r2)",
 "Torus parts: volumes of pipe elbows and ring seals",
 "Doughnut vessels: volume estimates for toroidal bodies",
 "Math model: the square relation between torus volume and tube diameter",
 "Algorithm: torus volume V=2·pi2·R·r2, with R the major radius (centre to tube centre) and r the tube radius; equivalently the tube cross-section pi·r2 times the swept circumference 2·pi·R. Requires R,r>0.",
 "Example: R=5m, r=1m gives V=2·pi2 x 5 x 1=98.696 m3. With r=2m (same R=5), V=2·pi2 x 5 x 4=394.784 m3 (doubling the tube diameter quadruples the volume because of r2).",
 "Don't mix up R and r?",
 "R is the large radius (the ring's centre circle) and r the small tube radius (tube thickness); the tube cross-section is a circle of radius r whose centre sweeps a circle of radius R to form the torus.",
 "What about the torus",
 " surface area",
 "?",
 "Torus surface area S=4·pi2·R·r, analogous to the volume (cross-section circumference 2·pi·r times the swept circumference 2·pi·R). This tool gives the volume; compute the surface area with this formula separately.",
]

TZA = [
 "Trapezoid Area (A = (a + b)·h / 2)",
 "Get the trapezoid area from the two bases and the height.",
 "Trapezoid Area Calculator",
 "/ Trapezoid Area",
 "Trapezoid Area",
 "📖 View Guide: \"Trapezoid Area (A = (a + b)·h / 2)\"",
 "A = (a+b)·h/2. Bases 3/5 with height 4 give area 16.",
 "Top Base (m)",
 "Bottom Base (m)",
 "Bases 3/5 with height 4 give area 16.",
 "📚 Deep Dive: Trapezoid area (A=(a+b)·h/2)",
 "Land / sections: areas of trapezoidal plots and roadbed cross-sections",
 "Figure estimates: find the area from the two bases and height",
 "Hydraulic works: flow-section estimates for trapezoidal channels",
 "Algorithm: trapezoid area A=(a+b)·h/2 with a and b the two bases and h the height; equivalently the midline m=(a+b)/2 times the height. Requires a,b,h>0 (the two bases parallel).",
 "Example: a=3m, b=5m, h=4m gives A=(3+5)x4/2=16.0000 m2, midline m=(a+b)/2=4.0000 m and midline x2 = the sum of the bases = 8.0000 m. If a=4, b=6, h=5, then A=(4+6)x5/2=25.0000 m2 and midline=5.0000 m.",
 "How do trapezoid and parallelogram areas relate?",
 "If a=b the trapezoid degenerates to a parallelogram with A=a·h; this tool assumes the two bases are parallel, so a=b reduces the formula to the parallelogram area automatically.",
 "What is the midline for?",
 "The midline m=(a+b)/2 joins the midpoints of the two legs, and the area equals the midline times the height, a quick method when a and b are not recorded separately.",
]

THR = [
 "Heron's Formula (A = sqrt(s(s-a)(s-b)(s-c)))",
 "Given the three side lengths, use the semiperimeter to find the triangle area.",
 "Triangle Area Calculator (Heron's Formula)",
 "/ Triangle Area (Heron)",
 "Triangle Area (Heron)",
 "📖 View Guide: \"Heron's formula area (A=sqrt(s(s-a)(s-b)(s-c)))\"",
 "A = sqrt[s(s-a)(s-b)(s-c)], s = (a+b+c)/2. A 3-4-5 right triangle has area 6.",
 "Side a (m)",
 "Side b (m)",
 "Side c (m)",
 "A 3-4-5 right triangle has area 6.",
 "📚 Deep Dive: Heron's formula area (A=sqrt(s(s-a)(s-b)(s-c)))",
 "Area from three sides: when the three sides are known but the height is not, use the",
 "Plot measurement: land area where boundary lengths are known but the height is hard to measure",
 "Geometric check: cross-validate against 1/2·base·height",
 "Algorithm: semiperimeter s=(a+b+c)/2 and area A=sqrt(s(s-a)(s-b)(s-c)). The triangle inequality such as a+b>c must hold, otherwise the radicand is negative and there is no solution. Requires all three sides >0.",
 "Example: a=3, b=4, c=5 gives s=6 and A=sqrt(6·3·2·1)=sqrt(36)=6.0000 m2 (the 3-4-5 right triangle, matching 1/2x3x4=6). If a=13, b=14, c=15, then s=21 and A=sqrt(21·8·7·6)=sqrt(7056)=84.0000 m2 (a classic Heronian triple).",
 "What if the radicand is negative?",
 "It means the three sides do not form a triangle (violating the triangle inequality, e.g. 1,2,5). Check the side lengths; this tool should report invalid rather than a wrong area when the radicand is negative.",
 "Why use Heron's formula when the height is known?",
 "Heron's formula needs only the three sides, suiting cases where the height cannot be measured or the terrain is irregular (e.g. known boundary lengths but a hard-to-measure height); if base and height are known, 1/2·base·height is faster.",
]

write('torus-volume', build('torus-volume', TRV))
write('trapezoid-area', build('trapezoid-area', TZA))
write('triangle-heron', build('triangle-heron', THR))
