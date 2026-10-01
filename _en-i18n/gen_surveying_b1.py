#!/usr/bin/env python3
# surveying batch1 (10 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'surveying')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'surveying')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'analysis-17': [
"🗺️ Buffer (Radius) Analysis",
"Radius",
"/ Buffer (Radius) Analysis",
"📖 View the \"analysis-17 User Guide\"",
"Point buffer area = π×r²; line buffer (capsule) area = 2×r×L + π×r²; buffer perimeter = 2×π×r + 2×L. Enter L = 0 to compute the point buffer only.",
"Buffer radius r (m)",
"Linear feature length L (m, enter 0 for point buffer)",
"📚 In-depth: Buffer (Radius) Area and Perimeter Analysis",
"Generate a circular buffer around a point feature (base station / monitoring station) by a radius and compute the covered area and service range.",
"Generate a capsule-shaped buffer around a linear feature (road / pipeline / riverbank) and estimate the affected-zone area and perimeter.",
"Given the line length and radius, assess the extent of construction setbacks, property boundary lines or ecological buffer zones.",
"Example: Roadside buffer",
"Buffer radius 30 m, line length 100 m: point buffer area ≈ π×30² ≈ 2827 m²; line buffer (capsule) area = 2×30×100 + π×30² ≈ 8827 m²; buffer perimeter = 2×π×30 + 2×100 ≈ 389 m. Enter L = 0 to compute only the point buffer.",
"Why does a line buffer add 2×radius×length versus a point buffer?",
"A line buffer is a rectangle (area 2rL) formed by expanding the segment outward by r on both sides plus two semicircles (together one circle πr²), total 2rL + πr²; a point buffer is only πr².",
"How is the perimeter computed?",
"Capsule perimeter = two long sides 2L plus the two end semicircles (2πr).",
"Circumference",
"2πr, i.e. 2L + 2πr; a larger radius or longer line gives a longer covered boundary.",
"Coordinate (latitude/longitude) and DMS conversion",
"Slope (percent/angle) conversion",
"About \"Buffer (Radius) Analysis\"",
"Buffer (Radius) Analysis. Free online tool, fully client-side processing, no data uploaded, privacy safe.",
],
'analysis-cycle': [
"📈 Deformation Monitoring Cycle Analysis and Warning",
"Enter cumulative deformation per cycle, compute each period's change and rate, and trigger warnings",
"Deformation monitoring uses two criteria: whether the cumulative deformation reaches a control threshold (absolute-value criterion), and whether a single-period change rate suddenly shifts (trend criterion). The average only reflects overall speed; in practice warnings rely more on the single-period rate -- a sudden acceleration in one period is often a precursor to instability, so monitoring should be intensified even if the cumulative amount is still within limits. The first-period change starts from 0. All computations run locally in the browser; no data is uploaded.",
"📖 View the \"Deformation (Monitoring/Cycle/Analysis) Chart User Guide\"",
"Current change = current cumulative deformation − previous cumulative deformation; average change rate = final cumulative deformation ÷ number of monitoring periods; threshold exceedance: cumulative deformation > warning threshold OR single-period change > rate threshold",
"Enter one row per \"period,cumulative deformation (mm)\", e.g.: Period 1,2.1",
"Period 1,2.1\nPeriod 2,4.5\nPeriod 3,7.2\nPeriod 4,8.0",
"Cumulative deformation warning threshold (mm)",
"Single-period change-rate threshold (mm/period)",
"📚 In-depth: Deformation Monitoring Cycle Analysis and Warning",
"Excavation slope / embankment deformation cycle monitoring",
"Building settlement observation",
"Warning, monitoring and intensification criteria",
"Current change = current cumulative deformation − previous cumulative deformation; average change rate = final cumulative deformation ÷ number of monitoring periods; warning: cumulative deformation > threshold OR single-period change > rate threshold.",
"W1 1.5, W2 3.8, W3 6.9, W4 9.4, W5 11.2 mm (threshold 10 mm, rate 2.5 mm/period) → periods 5, cumulative deformation 11.20 mm (over threshold); per-period changes 1.5/2.3/3.1/2.5/1.8, max single-period change 3.10 mm (W3, over rate); average change rate = 11.2/5 = 2.24 mm/period.",
"Is it safe if cumulative deformation is within limits?",
"No. A sudden shift in the single-period rate is often a precursor to instability; when the rate exceeds the threshold, intensify monitoring even if the cumulative amount is still within limits.",
"How is the first-period change computed?",
"Start from 0, i.e. first-period change = first-period cumulative deformation; later periods are current cumulative minus previous cumulative.",
"About \"Deformation (Monitoring/Cycle/Analysis) Chart\"",
"Deformation (Monitoring/Cycle/Analysis) Chart. Free online tool, fully client-side processing, no data uploaded, privacy safe.",
"e.g.: Period 1,2.1",
],
'area-24': [
"📐 Cadastral Survey (Boundary/Area/Ownership)",
"Compute parcel area, perimeter, diagonal and mu conversion from the two side lengths of a rectangular parcel, for quick cadastral surveys and real-estate mapping.",
"📖 View the \"Cadastral Survey (Boundary/Area/Ownership) User Guide\"",
"Parcel area = length × width; perimeter = 2×(length+width); diagonal = √(length²+width²); 1 mu ≈ 666.67 m²",
"A rectangular parcel is the most common plot shape; area = length×width and the perimeter and diagonal follow from the Pythagorean theorem; results are converted to mu at 1 mu ≈ 666.67 m² for comparison with land acquisition and title-confirmation standards.",
"Parcel long side (m)",
"Parcel short side (m)",
"💡 Parcel area = length × width; diagonal = √(length²+width²); 1 mu ≈ 666.67 m².",
"📚 In-depth: Cadastral Survey (Boundary/Area/Ownership)",
"Quickly estimate area from the two side lengths of a rectangular parcel.",
"Back-compute plot regularity from area and perimeter.",
"Use with mu conversion for land acquisition and title confirmation.",
"Parcel area",
"Length 150 m, width 60 m → area = 150×60 = 9000 m²; perimeter = 2×(150+60) = 420 m.",
"Mu conversion",
"9000 m² ÷ 666.67 ≈ 13.50 mu; engineering commonly uses 1 mu ≈ 666.67 m².",
"How is a rectangular parcel area computed?",
"Area = length×width; for irregular parcels use the boundary-point coordinates and the Shoelace formula for the polygon area.",
"How many m² is 1 mu?",
"1 mu ≈ 666.67 m² (15 mu = 1 hectare = 10000 m²).",
"About \"Cadastral Survey (Boundary/Area/Ownership)\"",
"Cadastral Survey (Boundary/Area/Ownership). Free online tool, fully client-side processing, no data uploaded, privacy safe.",
"Boundary",
],
'area-25': [
"📐 Real Estate Survey (Area/Title/Cadastre)",
"Compute building area, usable-area ratio, shared-area ratio and shared-area coefficient from the enclosed area and shared area, for real-estate area accounting.",
"📖 View the \"Real Estate Survey (Area/Title/Cadastre) User Guide\"",
"Building area = enclosed area + shared area; usable-area ratio = enclosed ÷ building area × 100%; shared-area ratio = shared ÷ building area × 100%",
"Building area is the enclosed area plus the apportioned common area; usable-area ratio = enclosed ÷ building area, shared-area ratio = shared ÷ building area, shared-area coefficient = shared ÷ enclosed. These three are the core metrics of real-estate area accounting and quickly indicate a unit's usable level.",
"Enclosed area (m²)",
"Shared area (m²)",
"💡 Building area = enclosed + shared; usable-area ratio = enclosed ÷ building area; shared-area coefficient = shared ÷ enclosed.",
"📚 In-depth: Real Estate Survey (Area/Title/Cadastre)",
"From the enclosed area and",
"Compare usable-area ratio and shared-area ratio across unit types.",
"Assist in checking title area against cadastral mapping.",
"Enclosed 85 m², shared 30 m² → building area = 85+30 = 115 m²; usable-area ratio = 85/115×100% = 73.91%.",
"Shared-area coefficient",
"Shared 30 m², enclosed 85 m² → shared-area coefficient = 30/85 = 0.3529; a larger coefficient means less usable area.",
"What is the difference between building area and enclosed area?",
"Building area = enclosed + apportioned common area; enclosed is the usable internal area, and usable-area ratio = enclosed ÷ building area.",
"What usable-area ratio is reasonable?",
"Residential buildings commonly 70%–80%; shared area includes elevators, stairs, lobbies, etc.; an excessive coefficient needs review of the apportionment.",
"About \"Real Estate Survey (Area/Title/Cadastre)\"",
"Real Estate Survey (Area/Title/Cadastre). Free online tool, fully client-side processing, no data uploaded, privacy safe.",
"Title",
],
'area-calc': [
"📐 Area Calculation",
"Polygon area and perimeter calculation (Shoelace formula), supports dynamic add/remove vertices and visualization",
"📖 View the \"Area Calculation User Guide\"",
"A = length × width (rectangle) or ½|Σ(x_i·y_{i+1} − x_{i+1}·y_i)|",
"Point No.",
"+ Add Vertex",
"Area formula (Shoelace): A = ½|Σ(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|; perimeter is the sum of distances between adjacent vertices. Enter vertices in clockwise or counterclockwise order.",
"📚 In-depth: Coordinate Area (Shoelace Formula)",
"Compute area and perimeter from polygon vertex coordinates.",
"Parcel / red-line area accounting.",
"Automatic visualization and mu conversion.",
"Shoelace formula",
"Four vertices (0,0)(100,0)(100,50)(0,50): area = ½|Σ(xᵢyᵢ₊₁−xᵢ₊₁yᵢ)| = ½|5000| = 5000 m² = 7.5 mu, perimeter 300 m.",
"Irregular",
"Enter many vertices in order; the formula works for both convex and concave polygons; area is the absolute value, and a wrong vertex order yields a negative value whose abs is taken.",
"Does vertex order matter?",
"Vertices must follow the boundary continuously in clockwise or counterclockwise order, head to tail; skipping points miscomputes the area.",
"How to convert to mu?",
"Area m² ÷ 666.67 = mu; common in land surveying, and hectares (10000 m²) are also used in engineering.",
"About \"Area Calculation\"",
"Area Calculation is an online tool in the scientific research domain. A scientific tool using standard scientific formulas for accurate computation.",
"How to use Area Calculation",
"What does Area Calculation do?",
"Enter the coordinates of each polygon vertex in turn (vertices can be added or removed dynamically), use the Shoelace formula to compute the area and perimeter of the closed polygon, and draw the shape in real time on screen; suited to plot and parcel area measurement.",
"How to use Area Calculation?",
"What scenarios is Area Calculation suited to?",
],
'area-coordinates': [
"Polygon Closed Area",
"Coordinate Area Method",
"/ Coordinate Area Method (Shoelace Formula)",
"Coordinate Area Method (Shoelace Formula)",
"📖 View the \"Polygon Closed Area User Guide\"",
"X coordinates (comma separated)",
"Y coordinates (comma separated)",
"The Shoelace formula auto-closes the polygon.",
"1 mu ≈ 666.67 m².",
"📚 In-depth: Coordinate Area Method",
"Compute parcel area from surveyed coordinates.",
"More accurate than measuring side lengths (eliminates cumulative error).",
"Plug CAD / RTK coordinates in directly.",
"Coordinate substitution",
"Known points A(0,0) B(120,0) C(120,60) D(0,60) → area = 120×60 = 7200 m² = 10.8 mu, consistent with Shoelace.",
"Accuracy",
"The coordinate method depends only on point accuracy and accumulates less error than measuring each side, so the official area uses the coordinate method.",
"Is the coordinate method the same as Shoelace?",
"Mathematically equivalent; both give the polygon's signed area; the coordinate method plugs RTK results in directly.",
"How to check the closing error?",
"The last point should return to the first; if the coordinate-method area differs greatly from expectation, first check the point order or input errors.",
],
'assessor-16': [
"📋 GPS (Accuracy/PDOP) Assessment",
"Enter PDOP, number of satellites, HDOP/VDOP and other parameters to assess the GPS positioning accuracy grade",
"/ GPS (Accuracy/PDOP) Assessment",
"📖 View the \"GPS Positioning Accuracy and PDOP Assessment User Guide\"",
"PDOP value",
"HDOP value",
"VDOP value",
"Number of visible satellites",
"UERE user range error (m)",
"Assess accuracy",
"📚 In-depth: GPS (Accuracy/PDOP) Assessment",
"Before fieldwork, assess whether the positioning accuracy of the current satellite geometry meets the standard.",
"Determine whether PDOP satisfies the accuracy requirements of RTK, static or fast-static surveys.",
"Combine DOP and the error grade to choose the best observation window.",
"PDOP and 3D error",
"With UERE = 3 m: PDOP=2 → 3D error ≈ ±6 m; PDOP=5 → ≈ ±15 m; PDOP=10 → ≈ ±30 m. Smaller DOP means higher accuracy; generally <5 is considered good.",
"Grade determination",
"PDOP ≤1 ideal, ≤2 excellent, ≤5 good, ≤10 fair, >10 poor; fewer than 5 visible satellites cannot give reliable 3D positioning, wait for satellites or switch to RTK.",
"What is PDOP?",
"Position Dilution of Precision; it reflects how much the satellite spatial geometry amplifies positioning error; a smaller value means better geometry and higher accuracy.",
"What is the relation among HDOP / VDOP and PDOP?",
"HDOP is the horizontal and VDOP the vertical precision factor, satisfying PDOP² = HDOP² + VDOP²; error = DOP × UERE.",
"PDOP reflects the effect of satellite geometry on positioning accuracy; smaller is better",
"PDOP = √(HDOP²+VDOP²); ideal value ≤1, acceptable value ≤5",
"Positioning error ≈ PDOP × UERE; UERE is usually 3–6 m",
"Differential GPS (RTK) can improve accuracy from meter to centimeter level",
"At least 4 visible satellites are needed for 3D positioning; 6 or more is more reliable",
"Coordinate (latitude/longitude) and DMS conversion",
"Slope (percent/angle) conversion",
"About \"GPS (Accuracy/PDOP) Assessment\"",
"GPS positioning accuracy assessment tool: enter PDOP/HDOP/VDOP values and satellite count to automatically estimate positioning error and determine the accuracy grade.",
"3D assessment of PDOP/HDOP/VDOP",
"Automatic positioning-error estimation",
"PDOP consistency verification",
"Satellite-count sufficiency check",
"Engineering survey accuracy assessment",
"GPS device calibration",
"Pre-RTK survey assessment",
"Navigation positioning quality judgment",
],
'bearing-azimuth': [
"Azimuth from Coordinate Increments (Δx,Δy)",
"α = atan2(ΔE, ΔN), normalized to 0–360°.",
"Inverse azimuth from coordinates",
"/ Inverse Azimuth from Coordinates",
"📖 View the \"Azimuth from Coordinate Increments (Δx,Δy) User Guide\"",
"Northing difference ΔN (m)",
"Easting difference ΔE (m)",
"Azimuth is measured clockwise from true north.",
"Coordinate differences must share the same datum.",
"📚 In-depth: Azimuth and Quadrant Bearing Conversion",
"Convert azimuth (0–360°) to quadrant bearing (NθE, etc.).",
"Quadrant bearings are more intuitive for staking-out / navigation.",
"Forward and back azimuths differ by 180°.",
"Convert to quadrant bearing",
"Azimuth 45°→N45°E; 135°→S45°E; 200°→S20°W; 315°→N45°W.",
"Back azimuth",
"Forward azimuth 60°, back azimuth = 60+180 = 240° (subtract 360 if over 360), used for forward/back side measurement checks.",
"What is the difference between azimuth and quadrant bearing?",
"Azimuth runs 0–360° clockwise from north; a quadrant bearing runs 0–90° from north/south toward east/west, one per quadrant.",
"Why add 180° for the back azimuth?",
"The reverse line of sight differs from the forward by 180°, used for closed-traverse and reciprocal-observation consistency checks.",
],
'bearing-from-coordinates': [
"Inverse Azimuth from Two-Point Coordinates",
"Enter the northing increment ΔN and easting increment ΔE to obtain the azimuth (0–360°).",
"Coordinate Azimuth Calculator",
"/ Coordinate Azimuth Calculator",
"📖 View the \"Inverse Azimuth from Two-Point Coordinates User Guide\"",
"Northing increment ΔN (m)",
"Easting increment ΔE (m)",
"atan2(east, north) ensures the correct quadrant.",
"📚 In-depth: Inverse Azimuth from Coordinates",
"Compute azimuth and side length from two-point coordinates.",
"Traverse-side azimuth derivation.",
"Staking-out element preparation.",
"Basic",
"A(0,0)→B(100,100): ΔN=100, ΔE=100 → azimuth = atan2(100,100) = 45° (NE quadrant); side length = √20000 ≈ 141.4 m.",
"Crossing quadrants",
"ΔN=−100, ΔE=100 → atan2(100,−100) = 135° (SE quadrant); mind the atan2(east, north) order to avoid the wrong quadrant.",
"What is the atan2 argument order?",
"Use atan2(ΔE, ΔN) (east, north), not plain atan(ΔE/ΔN), or the quadrant will be misjudged across boundaries.",
"Compute side length and azimuth together?",
"Yes. Side K = √(ΔN²+ΔE²), and the azimuth's quadrant follows the sign of Δ; both are basic traverse elements.",
],
'bearing-to-offset': [
"Coordinate Increments from Distance and Azimuth",
"Enter distance D and azimuth α (degrees) to obtain the northing and easting increments.",
"Azimuth-to-Coordinate Calculator",
"/ Azimuth-to-Coordinate Calculator",
"📖 View the \"Coordinate Increments from Distance and Azimuth User Guide\"",
"Distance D (m)",
"Azimuth α (degrees)",
"Polar to rectangular coordinate conversion.",
"📚 In-depth: Offset Calculation",
"Compute the perpendicular offset from a baseline distance and deflection angle.",
"Road edge-line / pipeline offset staking-out.",
"Lateral positioning of stakes.",
"Offset",
"Baseline distance 50 m, deflection angle 30° → perpendicular offset = 50×sin30° = 25 m; at 90° the offset equals the full 50 m.",
"Set edge stakes 25 m outside the road centerline using baseline distance + deflection angle for quick staking, avoiding per-point coordinates.",
"Is offset a perpendicular distance?",
"It is the perpendicular offset = baseline distance × sin(deflection angle); if using the slant distance, multiply by sin rather than equating directly.",
"What does a 0° deflection mean?",
"Offset 0, the point is on the baseline and needs no lateral shift.",
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
    print('gen_surveying_b1 done')
