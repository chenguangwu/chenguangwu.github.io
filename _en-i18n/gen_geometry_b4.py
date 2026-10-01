#!/usr/bin/env python3
# gen_geometry_b4.py — geometry b4 (5 slugs): point-line-distance/polygon-interior-angle/pyramid-volume/pythagorean/rectangle-diagonal
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

PLD = [
 "Distance (d = |Ax0+By0+C| / sqrt(A2+B2))",
 "The shortest distance from point (x0,y0) to the line Ax+By+C=0.",
 "Point-to-Line Distance Calculator",
 "/ Point-to-Line Distance",
 "Point-to-Line Distance",
 "📖 View Guide: \"Distance (d = |Ax0+By0+C| / sqrt(A2+B2))\"",
 "d = |Ax0+By0+C| / sqrt(A2+B2). The origin to x+y-1=0 gives 0.7071.",
 "Point x0",
 "Point y0",
 "The origin to x+y-1=0 gives distance 0.7071.",
 "📚 Deep Dive: Point-to-line distance (d=|Ax0+By0+C|/sqrt(A2+B2))",
 "Geometric construction: find the shortest perpendicular length from a point to a known line",
 "Collision detection / path planning: determine the minimum distance between a point and an obstacle line",
 "Coordinate checks: a distance of 0 means the point lies on the line",
 "Algorithm: the shortest distance from P(x0,y0) to the line Ax+By+C=0 is d=|Ax0+By0+C|/sqrt(A2+B2), the denominator being the normal's magnitude sqrt(A2+B2). When the point lies on the line, d=0. A and B must not both be 0 (otherwise it is not a line).",
 "Example: for the line x+y-1=0 (A=1,B=1,C=-1) and point (0,0), |0+0-1|/sqrt(2)=0.7071m and the normal magnitude is 1.4142. For the vertical line x=5 (i.e. x+0·y-5=0) and point (0,0), |-5|/1=5.0000m.",
 "What is the denominator sqrt(A2+B2)?",
 "It is the magnitude of the line's normal vector (A,B), normalising the scaled algebraic distance into the true",
 " distance; if A and B are both zero the equation is not a line.",
 "How can the distance be 0?",
 "When the point lies exactly on the line the numerator Ax0+By0+C=0 and d=0; this is exactly the test for whether a point lies on the line.",
]

PIA = [
 "Each interior angle of a regular polygon from the number of sides",
 "Enter the number of sides n to get the interior angle of a regular polygon.",
 "Regular Polygon Interior Angle Calculator",
 "/ Regular Polygon Interior Angle Calculator",
 "📖 View Guide: \"Each interior angle of a regular polygon from the number of sides\"",
 "Interior angle = (n-2)·180 degrees/n",
 "Interior angle = (n-2)·180 degrees/n.",
 "A hexagon's interior angle is 120 degrees.",
 "📚 Deep Dive: Regular polygon interior angle from the number of sides (theta=(n-2)·180 degrees/n)",
 "Tiling / drawing: fix each interior angle from the side count for layout",
 "Angle-sum check: whether an n-gon's interior angles sum to (n-2)·180 degrees",
 "Geometry teaching: demonstrating how interior angle varies monotonically with side count",
 "Algorithm: each interior angle of a regular n-gon is theta=(n-2)·180 degrees/n and the angle sum is (n-2)·180 degrees. n must be an integer >= 3; more sides means interior angles closer to 180 degrees.",
 "Example: a regular hexagon n=6 gives interior angle=(6-2)·180/6=120.00 degrees and angle sum=720 degrees (6x120). An octagon n=8 gives 135.00 degrees and sum=1080 degrees; a regular",
 " triangle with n=3 gives 60.00 degrees.",
 "Why (n-2)·180 degrees?",
 "From one vertex a regular n-gon splits into n-2 triangles, each summing to 180 degrees, so the interior sum is (n-2)·180 degrees; all angles are equal in a regular polygon, so dividing by n gives each interior angle.",
 "Can an interior angle exceed 180 degrees?",
 "Regular (convex) polygons always have interior angles <180 degrees, approaching 180 degrees as n grows (nearing a circle). Interior angles >=180 degrees belong to concave / star polygons, to which this formula does not apply.",
]

PYV = [
 "Pyramid volume from the base area and height",
 "Enter the base area and height to get the pyramid volume.",
 "V = (1/3) · Base Area · Height",
 "/ Pyramid Volume Calculator",
 "Pyramid Volume Calculator",
 "📖 View Guide: \"Pyramid volume from the base area and height\"",
 "Base Area A (m2)",
 "Base 9, height 4 -> V=12.",
 "📚 Deep Dive: Pyramid volume (V=1/3·base area·height)",
 "Cone estimates: volumes of pyramids, tents and frustum-type solids",
 "Earthwork / fill: quantity checks for pyramid-shaped stockpiles",
 "Geometric modelling: the unified relation with the",
 " cone volume",
 " formula",
 "Algorithm: pyramid volume V=1/3·base area·height (i.e. A·h/3), independent of base shape, given base area A and perpendicular height h. Requires A>0 and h>0. It equals 1/3 of the prism with the same base and height.",
 "Example: base area A=9 m2 and height h=4m give V=9x4/3=12.000 m3. If A=16 m2 and h=9m, V=16x9/3=48.000 m3 (e.g. a square pyramid with base edge 4m and height 9m).",
 "Must the base be square?",
 "No, any polygonal base works given its area A; this tool computes from the base",
 " area",
 ", and the base shape does not affect the formula.",
 "Do pyramid and cone share a formula?",
 "Yes: both are 1/3 x base area x height. A cone's base is a circle (A=pi·r2) and a pyramid's is a polygon, essentially the same and both use the formula.",
 "How to use Pyramid volume from the base area and height",
 "What does Pyramid volume from the base area and height do?",
 "A pyramid volume calculator. Enter the base area and height and compute V = (1/3)·base area·height for pyramids, tents and frustum-type solids.",
 "How do I use Pyramid volume from the base area and height?",
 "Which scenarios suit Pyramid volume from the base area and height?",
 "Pyramid volume V=1/3·base area·height: regardless of base shape it is 1/3 of the prism with the same base and height.",
 "Volume is in cubic length units (e.g. m3, cm3); the base area and height units must be consistent.",
]

PYT = [
 "Hypotenuse (c = sqrt(a2 + b2))",
 "The hypotenuse length of a right triangle.",
 "Pythagorean Theorem Calculator",
 "/ Pythagorean Hypotenuse",
 "Pythagorean Hypotenuse",
 "📖 View Guide: \"Hypotenuse (c = sqrt(a2 + b2))\"",
 "Leg a (m)",
 "Leg b (m)",
 "3-4 gives hypotenuse 5.",
 "📚 Deep Dive: Pythagorean hypotenuse (c=sqrt(a2+b2))",
 "Right",
 " triangle: find the hypotenuse from the two legs",
 "Planar distance: get the straight distance from the coordinate-difference legs",
 ": convert the diagonal size from a width-height ratio",
 "Algorithm: legs a, b give hypotenuse c=sqrt(a2+b2); angle A is the acute angle opposite side a, so tan A = a/b and A=arctan(a/b), while B=90 degrees-A=arctan(b/a). Requires a,b>0.",
 "Example: a=3, b=4 gives c=sqrt(9+16)=5.0000 m; A=arctan(3/4)=36.87 degrees and B=arctan(4/3)=53.13 degrees. If a=5, b=12, c=13.0000 m and A=arctan(5/12)=22.62 degrees (the classic 5-12-13 right triangle).",
 "What if I know the hypotenuse and one leg?",
 "Rearrange: b=sqrt(c2-a2). This tool is designed for 'find the hypotenuse from both legs'; to find the other leg, swap a and b or compute c2-a2 and take the square root.",
 "Which angle is A?",
 "A is the acute angle opposite side a, with tan A = opposite/adjacent = a/b, so A=arctan(a/b); B is opposite side b, with B=arctan(b/a)=90 degrees-A. The longer side faces the larger angle.",
]

RCD = [
 "Diagonal (d = sqrt(w2 + h2))",
 "The diagonal length of a rectangle.",
 "Rectangle Diagonal Calculator",
 "/ Rectangle Diagonal",
 "Rectangle Diagonal",
 "📖 View Guide: \"Diagonal (d = sqrt(w2 + h2))\"",
 "A 3x4 rectangle has diagonal 5.",
 "📚 Deep Dive: Rectangle diagonal (d=sqrt(w2+h2))",
 "Size conversion: diagonal lengths of screens, panels and frames",
 "Maximum straight dimension: diagonal checks against packing / transport limits",
 "Spatial layout: joint estimation of a rectangular area's diagonal and area",
 "Algorithm: rectangle diagonal d=sqrt(w2+h2) (i.e. the",
 " Pythagorean theorem), and the area A=w·h is also output. Requires w,h>0. When w=h (a square), d=w·sqrt(2)=1.414w.",
 "Example: width w=3m, height h=4m gives d=5.0000m and area=12.0000 m2 (a 3-4-5 right",
 " triangle). If w=6m, h=8m, d=10.0000m and area=48.0000 m2.",
 "How does the diagonal relate to the sides?",
 "The diagonal is the hypotenuse of the right triangle formed by two adjacent sides; by the Pythagorean theorem d=sqrt(w2+h2), giving d=w·sqrt(2) for a square.",
 "How is it computed?",
 "A monitor 'size' is its diagonal in inches; derive the pixel width and height from the resolution aspect ratio and apply the formula above for the inch diagonal. This tool works in length units, so keep the units consistent.",
]

write('point-line-distance', build('point-line-distance', PLD))
write('polygon-interior-angle', build('polygon-interior-angle', PIA))
write('pyramid-volume', build('pyramid-volume', PYV))
write('pythagorean', build('pythagorean', PYT))
write('rectangle-diagonal', build('rectangle-diagonal', RCD))
