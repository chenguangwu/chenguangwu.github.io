#!/usr/bin/env python3
# gen_geometry_b2.py — geometry b2 (5 slugs): cone-frustum-volume/cone-volume/cube-properties/cylinder-volume/distance-3d
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

CFV = [
 "Volume of a frustum from the top and bottom radii and height",
 "Enter the top radius r, bottom radius R and height h to get the frustum volume.",
 "Frustum Volume Calculator",
 "/ Frustum Volume Calculator",
 "📖 View Guide: \"Volume of a frustum from the top and bottom radii and height\"",
 "Bottom Radius R (m)",
 "Top Radius r (m)",
 "📚 Deep Dive: Frustum volume (V = pi·h/3·(R2+R·r+r2))",
 "Civil works / vessels: capacities of truncated-cone tanks and hoppers",
 "Math teaching: cone and cylinder as degenerate cases of the frustum",
 "Layout and cutting: estimating frustum lateral area and volume",
 "Algorithm: frustum (truncated cone) volume V = pi·h/3·(R2+R·r+r2), with R the bottom radius, r the top radius and h the height. Special cases: R=r degenerates to the cylinder V=pi·r2·h; r=0 degenerates to the cone V=pi·R2·h/3. Requires R,r,h>0.",
 "Example: R=3m, r=1m, h=4m gives R2+Rr+r2=9+3+1=13 and V=pi x 4/3 x 13=54.4543 m3. If R=r=2m and h=4m (a cylinder), V=pi x 4/3 x 12=50.2655 m3, exactly matching the cylinder formula pi·r2·h=pi x 4 x 4.",
 "How do I remember the frustum and cone formulas together?",
 "See the frustum as what remains after cutting off a small cone with a parallel section; r=0 (top shrinks to a point) gives the cone, R=r (equal bases) gives the cylinder, and all three share the same radius / height parameters for easy switching.",
 "How is the lateral area computed?",
 "Frustum lateral area S=pi·(R+r)·l (l is the slant height, l=sqrt((R-r)2+h2)). The tool also outputs the slant height and lateral area; e.g. R=3, r=1, h=4 gives l=sqrt(4+16)=4.472 and S=pi x 4 x 4.472=56.20 m2.",
]

CNV = [
 "Cone Volume (V = pi·r2·h / 3)",
 "Get the cone volume from the base radius and height.",
 "Cone Volume Calculator",
 "/ Cone Volume",
 "Cone Volume",
 "📖 View Guide: \"Cone volume (V = pi·r2·h / 3)\"",
 "V = pi·r2·h/3 (a third of the cylinder with the same base and height).",
 "r=3 and h=4 give about 37.70 m3.",
 "📚 Deep Dive: Cone volume (V = pi·r2·h / 3)",
 "Container capacity: conical hoppers, sand piles and cone-bottom tanks",
 "Fill quantities: cone earthwork and",
 " frustum fill",
 "Geometric modelling: solid of revolution and classic examples like the 5-12-13 right",
 " rotation",
 "Algorithm: cone volume V = pi·r2·h/3 and base area A = pi·r2 (both output). Requires r>0 and h>0. It is one third of the",
 "cylinder volume",
 " with the same base and height (by Cavalieri's principle).",
 "Example: r=3m, h=4m gives V=pi x 9 x 4/3=37.6991 m3 and base area=28.2743 m2. If r=5m, h=12m, V=pi x 25 x 12/3=314.1593 m3 (the classic cone obtained by rotating a 5-12-13 right triangle about a leg).",
 "Why is a cone one third of a cylinder?",
 "It follows from integration or Cavalieri's principle: for equal base and height the cone is exactly one third of the cylinder. In engineering you simply divide by 3 when estimating hopper contents.",
 "Does it apply to oblique cones?",
 "This formula covers only right cones (axis perpendicular to the base). An oblique cone still has volume 1/3 x base area x height, where height is the perpendicular distance from the apex rather than the slant length; this tool treats right cones.",
]

CBP = [
 "Volume, surface area and space diagonal from the edge length",
 "Enter the cube edge length a to get the volume, surface area and space diagonal.",
 "Cube Properties Calculator",
 "/ Cube Properties Calculator",
 "📖 View Guide: \"Volume, surface area and space diagonal from the edge length\"",
 "Edge Length a (m)",
 "📚 Deep Dive: Cube geometry (volume / surface area / space diagonal)",
 "Packaging design: compute volume and surface area from the edge to estimate material use",
 "Space dimensions: the space diagonal gives the largest straight dimension when packing",
 "Geometry teaching: how the three properties scale with edge length (cubic / square / linear)",
 "Algorithm: cube edge a gives volume V=a3, surface area A=6a2 and space diagonal d=a·sqrt(3). Their dimensions are cubic, square and linear length respectively. Requires a>0.",
 "Example: a=2m gives V=8.000 m3, A=24.000 m2 and d=2x1.7321=3.464m. If a=5m, V=125.000 m3, A=150.000 m2 and d=8.660m.",
 "How does the space diagonal differ from an ordinary diagonal?",
 "The space diagonal runs through the cube joining opposite vertices (d=a·sqrt(3)), while a face diagonal lies within a plane (a·sqrt(2)); packing uses the space diagonal as the maximum straight length, so transport height and width limits must be checked against it.",
 "What happens when the edge doubles?",
 "V grows 8x (a3), A 4x (a2) and d 2x (a1), matching the volume, area and length scaling laws respectively.",
]

CYV = [
 "Cylinder Volume (V = pi·r2·h)",
 "Get the cylinder volume from the base radius and height.",
 "Cylinder Volume Calculator",
 "/ Cylinder Volume",
 "Cylinder Volume",
 "📖 View Guide: \"Cylinder volume (V = pi·r2·h)\"",
 "r=2 and h=5 give about 62.83 m3.",
 "📚 Deep Dive: Cylinder volume (V = pi·r2·h)",
 "Tanks / pipes: cylindrical capacities and pipe internal volume",
 "Column fill:",
 " columns and pile shafts",
 "Geometric modelling: comparing the volume relations of cylinder, cone and frustum",
 "Algorithm: cylinder volume V = pi·r2·h and lateral area S = 2·pi·r·h (both output; total surface area additionally adds the two bases 2·pi·r2). Requires r>0 and h>0.",
 "Example: r=2m, h=5m gives V=pi x 4 x 5=62.8319 m3 and lateral area=2·pi x 2 x 5=62.8319 m2 (here r=2 makes 2·pi·r·h=pi·r2·h, so the numbers coincide). If r=3m, h=10m, V=282.7433 m3 and lateral area=188.4956 m2.",
 "Can lateral area and volume be numerically equal?",
 "Only coincidentally for particular dimensions (here r=2, h=5 satisfies 2·pi·r·h=pi·r2·h, i.e. r=2). They have different dimensions (area vs volume), so equality is a numeric coincidence and not a general rule.",
 "How do I compute total surface area?",
 "Total surface area = lateral area + 2 x base area = 2·pi·r·h + 2·pi·r2. Use the total for closed cylinders such as tanks and only the lateral area for open tubes.",
]

D3D = [
 "Spatial distance from two points' coordinates",
 "Enter two points (x1,y1,z1) and (x2,y2,z2) to get the 3D distance.",
 "3D Distance Calculator",
 "/ 3D Distance Calculator",
 "📖 View Guide: \"Spatial distance from two points' coordinates\"",
 "📚 Deep Dive: Distance between two points in 3D space",
 "Spatial positioning: find the straight-line distance between two 3D coordinates",
 "Engineering survey: point distances across floors, tunnels and 3D models",
 "Graphics: initial values for collision detection and nearest-neighbour distance",
 "Algorithm: in three dimensions",
 "d = sqrt((x2-x1)2 + (y2-y1)2 + (z2-z1)2), the natural 3D extension of the two-dimensional",
 " case. Coordinates can be any real numbers and the distance is always non-negative.",
 "Example: P1=(0,0,0), P2=(3,4,12) gives d=sqrt(9+16+144)=sqrt(169)=13.000m. If P1=(1,2,2), P2=(4,6,6), the delta is (3,4,4) and d=sqrt(9+16+16)=sqrt(41)=6.403m.",
 "How does 3D distance relate to 2D?",
 "3D distance = sqrt(2D planar distance2 + height difference2); if z is equal it reduces to the 2D distance. It is essentially the Pythagorean theorem applied dimension by dimension.",
 "Can coordinates be negative?",
 "Yes; squaring the deltas removes the sign, so distance is independent of coordinate sign and depends only on relative position.",
]

write('cone-frustum-volume', build('cone-frustum-volume', CFV))
write('cone-volume', build('cone-volume', CNV))
write('cube-properties', build('cube-properties', CBP))
write('cylinder-volume', build('cylinder-volume', CYV))
write('distance-3d', build('distance-3d', D3D))
