#!/usr/bin/env python3
# gen_geometry_b3.py — geometry b3 (5 slugs): dot-product-2d/ellipse-area/ellipsoid-volume/midpoint-2d/parabola-vertex
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

DP2 = [
 "Scalar product and projection from two vectors",
 "Enter two vectors' components to get the dot product and the length of a's projection onto b.",
 "2D Dot Product Calculator",
 "/ 2D Dot Product Calculator",
 "📖 View Guide: \"Scalar product and projection from two vectors\"",
 "📚 Deep Dive: Scalar product and projection of 2D vectors",
 "Mechanics: resolve a force into projection components along a direction",
 "Graphics: judge whether the",
 " vector angle",
 " is acute / obtuse, and measure similarity",
 "Geometric analysis: read a vector's components on a basis from the projection length",
 "Algorithm: dot product a·b = ax·bx + ay·by; the signed projection length of a onto b is a·b / |b| with |b| = sqrt(bx2+by2), e.g. b=(3,4) gives |b|=5. A positive projection means a component along b and negative means opposite. Requires b non-zero.",
 "Example: a=(3,4), b=(1,0) gives a·b=3, |b|=1.000 and projection=3.000 (a's projection onto the x-axis equals its x component). If a=(1,2), b=(3,4), then a·b=11, |b|=5.000 and projection=2.200; a positive dot product means an acute angle.",
 "Are projection length and projection vector the same?",
 "No. The projection length is a scalar (what this tool gives), while the projection vector points along b and equals (a·b/|b|2)·b. Multiply by b's unit vector to get the vector form.",
 "What does a negative dot product mean?",
 "Since a·b = |a||b|cos(theta), a negative value means cos(theta)<0 and theta>90 degrees, i.e. an obtuse angle; a·b=0 means orthogonal (perpendicular).",
 "How to use Scalar product and projection from two vectors",
 "What does Scalar product and projection from two vectors do?",
 "Enter the components of two 2D vectors to compute their dot product a·b=a_x·b_x+a_y·b_y and the projection length of a onto b, for mechanics decomposition, graphics and geometric analysis of the vector angle.",
 "How do I use Scalar product and projection from two vectors?",
 "Which scenarios suit Scalar product and projection from two vectors?",
]

ELA = [
 "Ellipse area from the semi-major and semi-minor axes",
 "Enter the semi-major axis a and semi-minor axis b to get the ellipse area.",
 "Ellipse Area Calculator",
 "/ Ellipse Area Calculator",
 "📖 View Guide: \"Ellipse area from the semi-major and semi-minor axes\"",
 "Semi-major Axis a (m)",
 "Semi-minor Axis b (m)",
 "📚 Deep Dive: Ellipse area (A = pi·a·b)",
 "Machine parts: area estimates for elliptical holes and elliptical flanges",
 "Beds / sites: footprint and paving quantities for elliptical plots",
 "Duct sections: flow area of elliptical pipes",
 "Algorithm: the ellipse",
 " area",
 "A = pi·a·b with a the semi-major and b the semi-minor axis. When a=b it reduces to the circle A=pi·r2. Requires a,b>0.",
 "Example: a=5m, b=3m gives A=pi x 15=47.1239 m2. If a=10m, b=6m (both axes doubled), A=pi x 60=188.4956 m2, which is 4x larger because both semi-axes scale linearly.",
 "Why is there no separate 'semi-axis squared' in the ellipse area?",
 "A circle's area is pi·r2, and an ellipse can be seen as a circle stretched by a/r and b/r in two directions, scaling the area by ab/r2; taking r=1 gives pi·a·b. It amounts to multiplying the two semi-axes and then by pi.",
 "How do I use known major and minor axes?",
 "Since the major axis is 2a and the minor axis 2b, divide by 2 to get a and b before substituting; this tool uses semi-axes, not full axis lengths.",
]

ELV = [
 "Ellipsoid volume from the three semi-axes",
 "Enter the three semi-axes a, b and c to get the ellipsoid volume.",
 "Ellipsoid Volume Calculator",
 "/ Ellipsoid Volume Calculator",
 "📖 View Guide: \"Ellipsoid volume from the three semi-axes\"",
 "Semi-axis a (m)",
 "Semi-axis b (m)",
 "Semi-axis c (m)",
 "📚 Deep Dive: Ellipsoid volume (V = 4/3·pi·a·b·c)",
 "Celestial bodies / cells: approximate volume of ellipsoid-shaped objects",
 "Pills / tanks: capacity estimates for capsules and ellipsoidal tanks",
 "3D modelling: the unified relation with the sphere volume formula",
 "Algorithm: the ellipso",
 "id volume",
 "V = 4/3·pi·a·b·c (a,b,c are the three semi-axes). When a=b=c=r it reduces to the sphere V=4/3·pi·r3. Requires a,b,c>0.",
 "Example: a=3m, b=2m, c=1m gives V=4/3·pi·6=25.1327 m3. If a=b=c=2m (a sphere), V=4/3·pi·8=33.5103 m3, exactly matching the sphere formula.",
 "How is the ellipsoid related to",
 " ellipse area",
 "?",
 "Just as for circle and sphere: the ellipse",
 " area",
 " pi·a·b versus ellipsoid volume 4/3·pi·a·b·c; adding the third axis c and multiplying by 4/3 gives the volume, the natural extension from 2D to 3D.",
 "Does it apply to oblate spheroids (Earth's shape)?",
 "Yes; Earth is roughly an oblate spheroid with a=b (equatorial radius) slightly larger than c (polar radius). Substituting the three semi-axes gives an approximate volume, and this formula does not distinguish prolate from oblate.",
]

MP2 = [
 "Midpoint of a segment from two points",
 "Enter two points' coordinates to get the midpoint.",
 "Midpoint Coordinate Calculator",
 "/ Midpoint Coordinate Calculator",
 "📖 View Guide: \"Midpoint of a segment from two points\"",
 "Midpoint = arithmetic mean of the two endpoints. 1,2 and 5,8 -> (3,5).",
 "Midpoint = arithmetic mean of the two endpoints.",
 "1,2 and 5,8 -> (3,5).",
 "📚 Deep Dive: Midpoint of a segment (M = ((x1+x2)/2, (y1+y2)/2))",
 "Figure splitting: use the midpoint for symmetry and interpolated positioning",
 "Centroid initial value: the simplified case of averaging polygon vertices",
 "Coordinate positioning: insert equally spaced points between two points",
 "Algorithm: the segment midpoint is M = ((x1+x2)/2, (y1+y2)/2), i.e. the arithmetic mean coordinate by coordinate. Useful for figure symmetry and interpolated positioning. Inputs must be real numbers.",
 "Example: P1=(1,2), P2=(5,8) gives M=(3.000, 5.000). If P1=(-2,4), P2=(6,-2), then M=(2.000, 1.000) (averaging x and y separately works even across quadrants).",
 "Can the midpoint formula extend to three dimensions?",
 "Yes, by averaging coordinate by coordinate: M=((x1+x2)/2,(y1+y2)/2,(z1+z2)/2). This tool is the 2D version; use a spatial distance / midpoint tool for 3D.",
 "How do I find the 'midpoint' of several points?",
 "The centre (centroid) of several points is the average of each coordinate, not limited to two points; the two-point midpoint is just the n=2 special case.",
 "How to use Midpoint of a segment from two points",
 "What does Midpoint of a segment from two points do?",
 "A segment midpoint calculator. Enter two points (x1,y1) and (x2,y2) and get the midpoint as M = ((x1+x2)/2, (y1+y2)/2), for geometry, graphics processing and coordinate positioning.",
 "How do I use Midpoint of a segment from two points?",
 "Which scenarios suit Midpoint of a segment from two points?",
]

PVT = [
 "Vertex (x_v = -b/2a, y_v = f(x_v))",
 "The vertex coordinates of the quadratic y = ax2 + bx + c.",
 "Parabola Vertex Calculator",
 "/ Parabola Vertex",
 "Parabola Vertex",
 "📖 View Guide: \"Vertex (x_v = -b/2a, y_v = f(x_v))\"",
 "x_v = -b/(2a), y_v = a·x_v2+b·x_v+c. For y=x2-4x+3 the vertex is (2, -1).",
 "Vertex x_v = -b/(2a), y_v = a·x_v2+b·x_v+c.",
 "y=x2-4x+3 has vertex (2, -1).",
 "📚 Deep Dive: Vertex and axis of symmetry from a quadratic (x_v=-b/2a, y_v=f(x_v))",
 "Trajectory vertex: the highest / lowest point of projectile motion is the parabola vertex",
 "Optimisation: the extremum position (x_v) of objective functions such as profit or area",
 "Graphing: sketch the parabola quickly from its vertex and axis of symmetry",
 "Algorithm: the abscissa is x_v=-b/(2a) and the ordinate y_v=f(x_v)=a·x_v2+b·x_v+c; the axis of symmetry is x=x_v. If a=0 it is not a quadratic and the tool outputs nothing. Requires a not equal to 0.",
 "Example: y=x2-4x+3 (a=1,b=-4,c=3) gives x_v=-(-4)/(2x1)=2.0000 and y_v=1x4-4x2+3=-1.0000, so the vertex is (2,-1) and the curve opens upward (a>0). For y=2x2+4x (a=2,b=4,c=0), x_v=-1.0000 and y_v=-2.0000, giving vertex (-1,-2).",
 "How do I tell whether the vertex is an extremum?",
 "If a>0 the parabola opens upward and the vertex is a minimum; if a<0 it opens downward and the vertex is a maximum; x_v is where the extremum occurs and y_v is its value.",
 "What if a=0?",
 "With a=0 it degenerates to the linear function y=bx+c (a straight line) with no parabola vertex; this tool requires a not equal to 0, so check whether a coefficient was entered wrongly.",
]

write('dot-product-2d', build('dot-product-2d', DP2))
write('ellipse-area', build('ellipse-area', ELA))
write('ellipsoid-volume', build('ellipsoid-volume', ELV))
write('midpoint-2d', build('midpoint-2d', MP2))
write('parabola-vertex', build('parabola-vertex', PVT))
