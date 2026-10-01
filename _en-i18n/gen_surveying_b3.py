#!/usr/bin/env python3
# surveying batch3 (10 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'surveying')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'surveying')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'coordinate-distance-3d': [
"Spatial Distance Between Two Points",
"3D Coordinate Distance",
"/ 3D Coordinate Distance",
"📖 View the \"Spatial Distance Between Two Points User Guide\"",
"Point 1 X (m)",
"Point 1 Y (m)",
"Point 1 Z (m)",
"Point 2 X (m)",
"Point 2 Y (m)",
"Point 2 Z (m)",
"3D Euclidean distance.",
"Coordinates must share the same datum.",
"📚 In-depth: 3D Coordinate Distance",
"Compute the spatial slant distance from N/E/H in 3D.",
"Include the point elevation difference.",
"3D staking-out / monitoring.",
"Spatial distance",
"Elevation contribution",
"Horizontal 500 m plus elevation 120 m gives a spatial distance of only 514 m; elevation's effect on total length is relatively small but sensitive in monitoring.",
"How much do 3D and 2D distances differ?",
"One extra squared elevation term; at horizontal 500, elevation 120, 3D is about 514, a 2.8% difference.",
"Which to use for monitoring?",
"Deformation monitoring commonly uses 3D, separating horizontal displacement and settlement for sharper criteria.",
],
'coordinate-rotation': [
"Rotate a Plane Point About the Origin",
"Coordinate rotation",
"/ Coordinate rotation",
"📖 View the \"Rotate a Plane Point About the Origin User Guide\"",
"Point X (m)",
"Point Y (m)",
"Rotation angle θ (°)",
"Counterclockwise is positive.",
"Often used in coordinate conversion.",
"📚 In-depth: Coordinate Rotation",
"Rotate a point about the origin by θ to get new coordinates.",
"Axis alignment / local system setup.",
"Figure orientation.",
"(1,0) rotated 90° about origin → x' = 1·cos90 − 0·sin90 = 0, y' = 1·sin90 + 0 = 1 → (0,1).",
"θ=30°, point (2,0) → x' = 2×0.866 = 1.732, y' = 2×0.5 = 1.0 → (1.732,1.0), used to rotate a building axis to true north.",
"What is the rotation formula?",
"x' = x cosθ − y sinθ, y' = x sinθ + y cosθ; counterclockwise positive; mind the sign and radians.",
"And",
"coordinate conversion?",
"Rotation is part of conversion; together with translation/scale it is complete (four-parameter).",
],
'cut-fill-volume': [
"Adjacent Section Volume",
"Average End-Area Earthwork",
"/ Average End-Area Earthwork",
"📖 View the \"Adjacent Section Volume User Guide\"",
"V = (A₁+A₂)/2 · L (adjacent sections)",
"Section 1 area (m²)",
"Section 2 area (m²)",
"The average end-area method is an approximation.",
"Section areas must share the same datum plane.",
"📚 In-depth: Cut and Fill Volume (Average End-Area)",
"Compute volume from adjacent section areas by the average end area.",
"Road / site-grading earthwork.",
"Rough cut-fill balance estimate.",
"End area",
"Section A₁=100 m², A₂=60 m², spacing L=20 m → V = (100+60)/2×20 = 1600 m³.",
"Balance",
"Sum cut and fill along the line; a positive difference needs borrow/ waste soil, and balancing optimizes haul distance to cut cost.",
"Is the average end area accurate?",
"Acceptable when sections change linearly; for large variation use the prismoidal formula for better accuracy, otherwise under/over-estimate.",
"Does spacing affect accuracy?",
"Smaller spacing is more accurate but more work; sparse on plains, dense in complex terrain, set per specification.",
],
'distance-calc': [
"📏 Distance Calculation",
"Forward and inverse plane-coordinate computation: from two points' coordinates find distance and azimuth, or from one point, distance and azimuth find the other point",
"📖 View the \"Distance Calculation User Guide\"",
"Inverse (two points → distance and azimuth)",
"Forward (one point + distance and azimuth → another point)",
"Point A x (m)",
"Point A y (m)",
"Point B x (m)",
"Point B y (m)",
"Start x (m)",
"Start y (m)",
"Horizontal distance S (m)",
"Azimuth α (°)",
"Azimuth is measured clockwise from true north, 0–360°. Inverse: S = √(Δx²+Δy²), α = atan2(Δx,Δy); forward: x₂ = x₁ + S·sinα, y₂ = y₁ + S·cosα.",
"📚 In-depth: Distance Calculation (Multi-mode)",
"Plane / slant distance /",
"3D distance",
"Compute by input.",
"Total-station data processing.",
"Convert among multiple distance conventions.",
"Slant-distance reduction",
"Slant 100.5 m, zenith angle 84.29° (i.e. depression 5.71°) → horizontal = 100.5×sin(84.29°) = 100.0 m, height diff = 100.5×cos(84.29°) = 10.0 m.",
"3D",
"Add elevation to get spatial distance; combine horizontal + elevation to check total-station results.",
"How to reduce slant to horizontal?",
"Horizontal = slant × sin(zenith) or × cos(depression); height diff = slant × cos(zenith).",
"Zenith and depression angles?",
"Zenith angle is measured from the zenith (0–180°), depression = 90° − zenith; do not mix the signs.",
"About \"Distance Calculation\"",
"Distance Calculation is an online tool in the scientific research domain. A scientific tool using standard scientific formulas for accurate computation.",
],
'earthwork-pyramid-volume': [
"Pyramid Volume from Base Area and Height",
"Enter base area A and height h to obtain the pyramid volume.",
"Pyramid (Embankment/Excavation) Earthwork Calculator",
"/ Pyramid (Embankment/Excavation) Earthwork Calculator",
"📖 View the \"Pyramid Volume from Base Area and Height User Guide\"",
"Base area A (m²)",
"Height h (m)",
"Works for pyramids and cones.",
"100×3/3 → 100 m³.",
"📚 In-depth: Pyramid/Cone Earthwork",
"Estimate the volume of a heap (cone/pyramid) as 1/3 × base area × height.",
"Material pile / excavation volume.",
"Approximation of irregular heaps.",
"Pyramid",
"Base area 100 m², height 9 m → V = 1/3×100×9 = 300 m³; quick estimate for soil piles / fill.",
"A prism of same base and height is 900 m³; the pyramid is only 1/3, so do not compute a heap as a prism or you overestimate 3×.",
"What is the pyramid formula?",
"V = 1/3 × base area × height, same shape as a cone (a cone is the limit of a circular-base pyramid).",
"When to use it?",
"Natural heaps / conical excavation; regular excavations use prisms / prismoidal for better accuracy.",
],
'elevation-diff': [
"Closed Leveling Route",
"Σh = Σ(backsight − foresight).",
"Leveling Height-Difference Accumulation",
"/ Leveling Height-Difference Accumulation",
"📖 View the \"Closed Leveling Route User Guide\"",
"Misclosure f_h = Σh − (H_end − H_start)",
"Backsight readings (comma separated) (m)",
"Foresight readings (comma separated) (m)",
"Height difference = backsight − foresight, accumulated station by station.",
"The misclosure should be within the limit.",
"📚 In-depth: Height-Difference Computation",
"Compute height difference from backsight and foresight readings.",
"Height-difference accumulation along a leveling route.",
"Settlement / heave monitoring.",
"Height difference",
"Backsight 1.500, foresight 0.950 → height diff = backsight − foresight = +0.550 m (front point is 0.55 m higher).",
"Accumulate",
"The algebraic sum of multi-station height differences gives the total between two points; misclosure = Σh − (known end − known start) for checking.",
"Height-difference sign?",
"Backsight − foresight positive means the front point is higher than the back point; keep the convention consistent.",
"Leveling vs trigonometric height difference?",
"Leveling measures directly and is most accurate; trigonometric height diff = slant × cos(zenith) ± instrument height, affected by atmospheric refraction.",
],
'end-area-volume': [
"Earthwork Volume from End Areas and Spacing",
"Enter the two end section areas A₁, A₂ and spacing L to obtain the volume.",
"Average End-Area Earthwork Calculator",
"/ Average End-Area Earthwork Calculator",
"📖 View the \"Earthwork Volume from End Areas and Spacing User Guide\"",
"Section area A₁ (m²)",
"Section area A₂ (m²)",
"Average adjacent sections and multiply by spacing.",
"(10+20)/2×50 → 750 m³.",
"📚 In-depth: Average End-Area Volume",
"Average the two section areas and multiply by spacing.",
"Canal / roadbed earthwork.",
"Cut-fill zonal statistics.",
"Section",
"Segment",
"Compute adjacent station sections along the whole line pairwise then sum to get total cut / fill.",
"How does it differ from prismoidal?",
"Average end-area = (A₁+A₂)/2×L; prismoidal = L/6(A₁+4Am+A₂) is more accurate (includes mid section); equal under linear change.",
"Is spacing uniform?",
"Spacing should be equal or use the matching L per segment; mixing distances in one formula is wrong.",
],
'external-distance-curve': [
"External Distance from Radius and Deflection Angle",
"Enter circular-curve radius R and deflection angle Δ (degrees) to obtain the external distance.",
"Circular Curve External Distance Calculator",
"/ Circular Curve External Distance Calculator",
"📖 View the \"External Distance from Radius and Deflection Angle User Guide\"",
"The external is the distance from the midpoint of the long chord to the intersection.",
"100×(sec30°−1) → 15.47 meters.",
"📚 In-depth: Circular Curve External Distance",
"Compute external E from radius and deflection angle.",
"Perpendicular distance from intersection to curve midpoint.",
"One of the curve elements.",
"External distance",
"E is used to set the curve-midpoint stake and for checking, with T/L for full horizontal-curve staking.",
"What is the relation between external and tangent length?",
"E = R(sec(Δ/2)−1), T = R tan(Δ/2); both small for small Δ, and E is always less than T.",
"What is sec?",
"sec = 1/cos; the E formula comes from geometry, the curve midpoint is E closer than the intersection.",
"How to use External Distance from Radius and Deflection Angle",
"What does External Distance from Radius and Deflection Angle do?",
"Enter circular-curve radius R and route deflection Δ (degrees), compute the curve external by E = R·(sec(Δ/2)−1), i.e. the perpendicular distance from intersection to curve midpoint, for horizontal-curve element computation and superelevation layout in route design.",
"How do I use External Distance from Radius and Deflection Angle?",
"What scenarios suit External Distance from Radius and Deflection Angle?",
"Curve external E: in road/rail circular curves, the vertical offset from the intersection (JD) to the curve midpoint, E = R·(sec(Δ/2)−1) (R radius, Δ deflection angle).",
"Used for route staking and land-acquisition extent estimate; a larger E means a sharper turn or smaller radius, needing more land.",
],
'grade-angle': [
"Angle ↔ Percent",
"Percent = tan(θ) × 100.",
"Slope angle",
"/ Slope Angle Conversion",
"Slope Angle Conversion",
"📖 View the \"Angle ↔ Percent User Guide\"",
"Slope i = tanα × 100%",
"Slope angle θ (°)",
"In slope ratio 1:n, n = 1/tan(θ).",
"Common road slopes are 3%–8%.",
"📚 In-depth: Slope and Angle Conversion",
"Slope % ↔ angle.",
"Used for road longitudinal-grade design.",
"Unify slope-ratio expression.",
"Mutual conversion",
"Slope 10% → angle = atan(0.10) = 5.71°; conversely a 5.71° slope is 10%. Codes commonly ≤8% (about 4.57°).",
"Slope ratio",
"A 10% slope = ratio 1:10 (rises 1 m per 10 m horizontal), more intuitive in engineering.",
"Is slope % an angle?",
"No. % = tan(θ) × 100; 10% ≈ 5.71°, easily mistaken for 10°.",
"Longitudinal-grade limit?",
"By highway class: expressway generally ≤3%–5%, urban ≤8%; too steep is hard to drive and brake.",
],
'grade-intersection-elev': [
"Elevation at Any Point on a Vertical Curve from Grades and Curve Length",
"Enter fore grade g₁, back grade g₂, curve length L and distance x from start to obtain the relative elevation y.",
"Vertical Curve Elevation Calculator",
"/ Vertical Curve Elevation Calculator",
"📖 View the \"Elevation at Any Point on a Vertical Curve User Guide\"",
"Fore grade g₁",
"Back grade g₂",
"Curve length L (m)",
"Distance from start x (m)",
"Common formula for parabolic vertical curves.",
"g1=2%,g2=−1%,L=200,x=100 → 1.25 meters.",
"📚 In-depth: Grade Intersection Elevation",
"Find the intersection elevation and station from two grade lines.",
"Vertical-curve start/end point alignment.",
"Road profile design.",
"Intersection",
"Grade 1: start 100 m, +2%/100 m; Grade 2: from 300 m at 110 m, −3%/100 m. Intersection: 100+0.02x = 110−0.03(x−300) → 100+0.02x = 110−0.03x+9 → 0.05x = 19 → x = 380 m, elevation = 100+0.02×380 = 107.6 m.",
"Vertical curve",
"After the intersection, set a parabolic transition by vertical-curve radius R to avoid a kink.",
"What is the intersection elevation for?",
"It is the vertical-curve vertex (grade-break point) elevation, the basis for profile design and elevation control.",
"Why use a vertical curve?",
"A direct kink is bumpy to drive and drains poorly; a parabolic / R transition is smoother and safer.",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    name = ''
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'surveying', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_surveying_b3 done')
