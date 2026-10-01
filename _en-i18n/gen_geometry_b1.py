#!/usr/bin/env python3
# gen_geometry_b1.py — geometry b1 (5 slugs): angle-between-vectors/arc-length/chord-length/circle-area/circle-circumference
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

ABV = [
 "Find the angle from two vectors",
 "Enter the components of two vectors to find the angle between them.",
 "Vector Angle Calculator",
 "/ Vector Angle Calculator",
 "📖 View Guide: \"Find the angle from two vectors\"",
 "theta=arccos(a·b/(|a||b|)). The x- and y-axis unit vectors give 90 degrees.",
 "The x- and y-axis unit vectors give 90 degrees.",
 "📚 Deep Dive: Finding the angle from two vectors (theta = arccos(a·b/(|a|·|b|)))",
 "Direction test: enter two vectors' components and get the angle to judge collinear, orthogonal, acute or obtuse relations",
 "Mechanics / physics decomposition: use the angle to further split force or velocity into directional components",
 "Machine learning / graphics:",
 " it is the cosine of the angle, used as a vector similarity measure",
 "Algorithm: dot product a·b = ax·bx + ay·by, |a| = sqrt(ax2+ay2), |b| = sqrt(bx2+by2); angle theta = arccos(a·b/(|a|·|b|)), output in degrees (radians x 180/pi). Dot product >0 means acute, =0 orthogonal, <0 obtuse. Both vectors must be non-zero (otherwise the denominator is 0 and undefined).",
 "Example: a=(1,0), b=(0,1) gives a·b=0, |a|=1, |b|=1, theta=arccos(0)=90.000 degrees (orthogonal). If a=(1,1), b=(1,0), then a·b=1, |a|=1.414, |b|=1, cos(theta)=0.7071, theta=45.000 degrees (the vectors meet at 45 degrees).",
 "Why is the angle limited to 0-180 degrees?",
 "The range of arccos is [0,pi], matching the smallest angle between two vectors and the geometric definition; to distinguish clockwise from counter-clockwise you need atan2 or a signed angle, which this tool does not output.",
 "What happens with a zero vector?",
 "A zero",
 " vector makes the denominator 0 and the angle undefined. Ensure both vectors are non-zero; if a component set is all 0 the tool reports an invalid input rather than a wrong value.",
]

ARL = [
 "Arc Length (L = r·theta, theta in radians)",
 "Arc length equals radius times the central angle in radians.",
 "Arc Length Calculator",
 "/ Arc Length",
 "Arc Length",
 "📖 View Guide: \"Arc Length (L = r·theta, theta in radians)\"",
 "L = r·theta, theta in radians",
 "L = r·theta (theta in radians); a 90 degree arc has length r·pi/2.",
 "r=10 at 90 degrees gives about 15.71 m.",
 "📚 Deep Dive: Arc length (L = r·theta, theta in radians)",
 "Engineering drawing: get the arc cut length from radius and central angle",
 "Machine design: arc dimensions for gears, cams and pipe elbows",
 "Teaching: the degree-radian conversion and how arc length varies linearly with angle",
 "Algorithm: arc length L = r·theta (theta must be in radians); degrees to radians theta = deg·pi/180. Degrees can be entered and are converted automatically. Requires r>0 and deg>=0 (the result grows linearly with deg).",
 "Example: r=10m, theta=90 degrees gives radians=90xpi/180=1.5708, L=10x1.5708=15.7080m. For theta=60 degrees, radians=1.0472 and L=10.4720m (a 90 degree arc is exactly 1.5x that of 60 degrees, matching the 1/4 vs 1/6 circle ratio).",
 "Must theta be in radians?",
 "Yes, L=r·theta holds only for theta in radians; substituting degrees directly gives a wrong result. The tool converts degrees internally, so enter the angle but mind the unit labels.",
 "What is the arc length of a full circle?",
 "At theta=360 degrees=2pi radians, L=r·2pi equals the circumference, so the arc length reduces to the full",
 " circumference",
 "; a semicircle (180 degrees) gives L=pi·r, matching intuition.",
]

CHL = [
 "Chord Length (c = 2r·sin(theta/2))",
 "Get the chord length from the radius and central angle in radians.",
 "Chord Length Calculator",
 "/ Chord Length",
 "Chord Length",
 "📖 View Guide: \"Chord Length (c = 2r·sin(theta/2))\"",
 "c = 2r·sin(theta/2); at 90 degrees with r=10 it is about 14.14 m.",
 "📚 Deep Dive: Chord length (c = 2r·sin(theta/2))",
 "Segments in a circle: get the chord from radius and central angle, for segment and sector design",
 "Gears / gear trains: checking pitch-circle chord length against tooth pitch",
 "Building layout: quick conversion of arch spans and chord member lengths",
 "Algorithm: chord c = 2r·sin(theta/2) (theta in radians), half-chord = c/2. At theta=180 degrees, c=2r, i.e. the diameter; for 0<=deg<=180 the chord lies within the semicircle. Requires r>0 and 0<=deg<=180.",
 "Example: r=10m, theta=90 degrees gives c=2x10xsin(45 degrees)=20x0.7071=14.1421m, half-chord=7.0711m. For theta=60 degrees, c=2x10xsin(30 degrees)=10.0000m (at radius 10, the 60 degree central angle corresponds to the side of an equilateral",
 " triangle).",
 "How do chord length and arc length differ?",
 "A chord is the straight segment joining two arc endpoints (the shortest distance), while an arc follows the circle as a curve; for the same central angle the arc is >= the chord, converging only as theta->0. This tool gives the chord; for arc length use the",
 " Arc Length Calculator",
 "Why limit theta to <=180 degrees?",
 "sin(theta/2) stays monotonic beyond 180 degrees, but geometrically a 'chord' usually subtends the minor arc; entering >180 degrees gives the long chord of the major arc, which may not match your intent, so stay within 0-180 degrees.",
]

CRA = [
 "Circle Area (A = pi·r2)",
 "Get the area from the radius.",
 "Circle Area Calculator",
 "/ Circle Area",
 "Circle Area",
 "📖 View Guide: \"Circle Area (A = pi·r2)\"",
 "Circle area A = pi x radius r squared; circumference C = 2·pi·r, also pi x diameter; diameter d = 2r; sphere volume V = 4/3 x pi x r cubed, sphere surface area S = 4·pi·r2.",
 "r=5 gives an area of about 78.54.",
 "📚 Deep Dive: Circle area (A = pi·r2)",
 "Plane geometry: get the area from the radius, for cross-sections and material estimates",
 "Material use: for circular plates, discs and pile cross-sections,",
 " / steel plate quantities",
 "Drawing checks: back-solve radius or diameter from the area",
 "Algorithm: area A = pi·r2, and circumference C = 2·pi·r is also output for cross-checking. r can be any positive length unit and the area automatically uses the corresponding square unit (e.g. m to m2). Requires r>0.",
 "Example: r=5m gives A=pi x 25=78.5398 m2 and C=2·pi x 5=31.4159m. If r=10m, A=314.1593 m2 (doubling r quadruples the area, per the square law).",
 "Why do area and circumference use different units?",
 "Area is two-dimensional and uses square units (m2), circumference is one-dimensional and uses length units (m); they have different dimensions and cannot be added. The tool outputs them separately to avoid confusion.",
 "How do I compute it if diameter d is known?",
 "First convert to radius with r=d/2, then substitute; the tool also outputs the circumference so you can recover the diameter (d=C/pi). For example r=5m corresponds to diameter 10.0000m.",
]

CRC = [
 "Circle Circumference (C = 2·pi·r)",
 "Get the circumference from the radius.",
 "Circle Circumference Calculator",
 "/ Circle Circumference",
 "Circle Circumference",
 "📖 View Guide: \"Circle Circumference (C = 2·pi·r)\"",
 "Circumference C = 2 x pi x radius r; diameter d = C divided by pi; circle area A = pi·r2; sphere surface area S = 4·pi·r2, sphere volume V = 4/3 x pi x r cubed.",
 "C = 2·pi·r, diameter d = 2r.",
 "r=5 gives a circumference of about 31.42.",
 "📚 Deep Dive: Circle circumference (C = 2·pi·r)",
 "Pipes / rims: get the outer edge length from the radius, for cutting or wrapping",
 "Ring dimensions: converting inner and outer circumferences",
 "Teaching: the linear relation between circumference and diameter (the pi factor)",
 "Algorithm: circumference C = 2·pi·r, diameter d = C/pi = 2r (both output). Pipe or rim cutting often back-solves diameter from circumference. Requires r>0.",
 "Example: r=5m gives C=2·pi x 5=31.4159m and diameter=10.0000m. If r=10m, C=62.8319m (doubling r doubles the circumference, a linear rather than square relation).",
 "Which grows faster with radius, circumference or area?",
 "Circumference is linear in r while area goes as r2; as r grows the area far outpaces the circumference, the 2D form of the square-cube law.",
 "Is C/pi always equal to 2r?",
 "Yes, C=2·pi·r directly gives d=C/pi=2r; the tool outputs both so they can validate each other, and any mismatch means rounding error or a wrong input.",
]

write('angle-between-vectors', build('angle-between-vectors', ABV))
write('arc-length', build('arc-length', ARL))
write('chord-length', build('chord-length', CHL))
write('circle-area', build('circle-area', CRA))
write('circle-circumference', build('circle-circumference', CRC))
