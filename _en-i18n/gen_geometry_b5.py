#!/usr/bin/env python3
# gen_geometry_b5.py — geometry b5 (5 slugs): rectangular-prism-volume/regular-polygon-area/sector-area/sphere-surface-area/sphere-volume
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

RPV = [
 "Volume from length, width and height",
 "Enter length, width and height to get the volume and surface area of a rectangular prism.",
 "Rectangular Prism Volume Calculator",
 "/ Rectangular Prism Volume Calculator",
 "📖 View Guide: \"Volume from length, width and height\"",
 "Length l (m)",
 "Width w (m)",
 "📚 Deep Dive: Rectangular prism volume and surface area (V=l·w·h)",
 "Capacity estimates: volumes for packing, rooms and warehouse space",
 "Material use: six-face surface area for packaging / coating quantities",
 "Magnitude checks: volume-surface area relation under 3D scaling",
 "Algorithm: volume V=l·w·h and surface area A=2(lw+wh+hl) (the sum of six faces). Requires l,w,h>0; units must be consistent, with volume cubic and area square.",
 "Example: l=4m, w=3m, h=2m gives V=24.000 m3 and A=2(12+6+8)=52.000 m2. If l=5, w=4, h=3, then V=60.000 m3 and A=94.000 m2.",
 "How many faces does the surface area include?",
 "A rectangular prism has 6 faces equal in pairs: 2 of lw, 2 of wh and 2 of hl, totalling 2(lw+wh+hl); for lateral area only (excluding top and bottom) subtract 2lw.",
 "How does volume scale with edge length?",
 "Volume is linear in any one edge (holding the others fixed); scaling all three dimensions by k multiplies the volume by k3, the square-cube law, while the surface area scales by k2.",
 "What is the total edge length?",
 "A rectangular prism has 12 edges (4 each of length, width and height), so the total is 4(l+w+h), not 2(l+w+h). For 4x3x2 it is 4x9=36 m.",
]

RPA = [
 "Regular Polygon Area (A = n·s2 / (4·tan(pi/n)))",
 "Area of a regular polygon from its side count and side length (n>=3).",
 "Regular Polygon Area Calculator",
 "/ Regular Polygon Area",
 "Regular Polygon Area",
 "📖 View Guide: \"Regular Polygon Area (A = n·s2 / (4·tan(pi/n)))\"",
 "Side Length (m)",
 "A regular hexagon with s=1 has area about 2.598.",
 "📚 Deep Dive: Regular polygon area (A=n·s2/(4·tan(pi/n)))",
 "Engineering sections: areas of floor tiles, nut cross-sections and other regular shapes",
 "Beds / sites: footprint estimates for regular n-gon plots",
 "Geometric design: how area converges as the side count grows (approaching the circle)",
 "Algorithm: a regular n-gon with side s has area A=n·s2/(4·tan(pi/n)), and the inradius is r_in=s/(2·tan(pi/n)). n must be an integer >=3 and s>0; as n grows it approaches the",
 " circle area",
 " pi·r2 (r being r_in).",
 "Example: a regular hexagon n=6, s=1m gives tan(30 degrees)=0.5774, A=6/(4x0.5774)=2.5981 m2 and inradius=0.8660m. A square n=4, s=2m gives A=4x4/(4x1)=4.0000 m2 (matching a square of side 2) and inradius=1.0000m.",
 "Why does the formula contain tan(pi/n)?",
 "A regular n-gon splits into n isosceles",
 " triangles (apex angle 2pi/n), each of area=1/2·s·r_in with r_in=s/(2tan(pi/n)); summing gives the formula.",
 "Is it accurate for large n?",
 "Larger n approaches the circle; from n>=12 the difference from the circle area is already tiny, so it can serve as a circle approximation.",
]

SCA = [
 "Sector Area (A = r2·theta / 2, theta in radians)",
 "Get the sector area from the radius and central angle in radians.",
 "Sector Area Calculator",
 "/ Sector Area",
 "Sector Area",
 "📖 View Guide: \"Sector Area (A = r2·theta / 2, theta in radians)\"",
 "A = r2·theta / 2, theta in radians",
 "A = r2·theta/2 (theta in radians); also pi·r2·(deg/360).",
 "r=10 at 90 degrees gives about 78.54 m2.",
 "📚 Deep Dive: Sector area (A=r2·theta/2, theta in radians)",
 "Sector area: the proportional area of circular sectors and pie-chart wedges",
 "Geometric modelling: find the partial",
 " circle area from the central angle and radius",
 "Proportion conversion: the sector's share of the full circle (deg/360)",
 "Algorithm: sector area A=r2·theta/2 (theta in radians); equivalently A=pi·r2·(deg/360) with deg in degrees. theta must be in radians, so convert degrees first (theta=deg·pi/180). Requires r>0 and deg>=0.",
 "Example: r=10m, theta=90 degrees gives radians=pi/2 and A=100x1.5708/2=78.5398 m2 (a quarter of the full circle pi·100, matching pi·100·90/360=78.5398). For theta=60 degrees, A=52.3599 m2 (one sixth of the circle).",
 "How are sector area and arc length related?",
 "A sector is the region bounded by an arc and two radii, with area=1/2·r·arc length (since L=r·theta, A=1/2·r2·theta=1/2·r·L); the two share a source, so knowing the arc length gives the area directly.",
 "What if the central angle exceeds 360 degrees?",
 "Geometrically a sector is usually 0-360 degrees; entering more gives an area exceeding the full circle, which may not match the figure's definition, so stay within 0-360 degrees.",
]

SSA = [
 "Sphere surface area from the radius",
 "Enter the sphere radius to get the surface area.",
 "Sphere Surface Area Calculator",
 "/ Sphere Surface Area Calculator",
 "📖 View Guide: \"Sphere surface area from the radius\"",
 "📚 Deep Dive: Sphere surface area (A=4·pi·r2)",
 "Packaging / coating: outer area of spherical tanks and spheres",
 "Heat transfer: heat dissipation / exchange area of a sphere",
 "Geometric modelling: the square relation between surface area and radius",
 "Algorithm: sphere surface area A=4·pi·r2, which is 2/3 of the circumscribed cylinder's lateral area (Archimedes' theorem). For volume see the",
 " sphere volume",
 " tool V=4/3·pi·r3. Requires r>0; the area is proportional to r2.",
 "Example: r=3m gives A=4·pi x 9=113.097 m2. If r=5m, A=4·pi x 25=314.159 m2 (radius x5/3 gives area x(5/3)2=2.78).",
 "How is sphere surface area related to",
 " circle area",
 "?",
 "Sphere surface area equals 4 great circles of radius r (each pi·r2), hence 4·pi·r2; it differs from the 2D circle area pi·r2 by a factor of 4.",
 "Why 4·pi·r2 and not 2·pi·r2?",
 "A sphere cannot be flattened without wrinkling (positive Gaussian curvature), and integration or Archimedes' theorem gives 4·pi·r2; intuitively the sphere covers more than two great-circle caps, exactly 4 great-circle areas.",
]

SPV = [
 "Sphere volume from the radius",
 "Enter the sphere radius to get the volume.",
 "Sphere Volume Calculator",
 "/ Sphere Volume Calculator",
 "📖 View Guide: \"Sphere volume (V=4/3·pi·r3)\"",
 "📚 Deep Dive: Sphere volume (V=4/3·pi·r3)",
 "Container capacity: volumes of spherical tanks and storage spheres",
 "Material volume: total volume estimates for sphere packings and particles",
 "Geometric modelling: the cubic relation between volume and radius",
 "Algorithm: sphere volume V=4/3·pi·r3 and surface area A=4·pi·r2 (see the",
 " sphere surface area",
 " tool). Requires r>0; the volume is proportional to r3 (the cube law).",
 "Example: r=3m gives V=4/3·pi·27=113.097 m3. If r=5m, V=4/3·pi·125=523.599 m3 (radius x5/3 gives volume x(5/3)3=4.63).",
 "How does sphere volume relate to a cylinder?",
 "With the same radius and height (=2r), the",
 " cylinder volume",
 " is pi·r2·2r=2·pi·r3, and the sphere volume 4/3·pi·r3 is exactly 2/3 of it (Cavalieri's principle / Archimedes).",
 "What about a hemisphere's volume?",
 "A hemisphere is 1/2·V=2/3·pi·r3; including the base, the total surface area is the hemisphere surface 2·pi·r2 plus the base pi·r2, i.e. 3·pi·r2.",
 "How do I convert cubic metres to litres?",
 "1 m3 = 1000 L (not 1/1000 L). For example a sphere of r=3 m has volume 113.097 m3 = 113,097 L = 1.131x10^8 cm3.",
]

write('rectangular-prism-volume', build('rectangular-prism-volume', RPV))
write('regular-polygon-area', build('regular-polygon-area', RPA))
write('sector-area', build('sector-area', SCA))
write('sphere-surface-area', build('sphere-surface-area', SSA))
write('sphere-volume', build('sphere-volume', SPV))
