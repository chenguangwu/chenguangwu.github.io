#!/usr/bin/env python3
# surveying batch5 (4 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'surveying')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'surveying')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'subtense-distance': [
"Distance from Subtense Bar Length and Angle",
"Enter subtense bar length c and the subtended angle θ (degrees) to obtain the distance.",
"Stadia (Subtense Bar) Distance Calculator",
"/ Stadia (Subtense Bar) Distance Calculator",
"📖 View the \"Distance from Subtense Bar Length and Angle User Guide\"",
"Subtense bar length c (m)",
"For small angles tanθ ≈ θ (radians).",
"2/tan(0.001 rad) → 2000 meters.",
"📚 In-depth: Subtense Bar Distance Measurement",
"Compute distance D = cot(θ/2)·b from the subtended angle of a fixed bar.",
"Distance measurement without an EDM.",
"Small-range precise ranging.",
"Subtended-angle ranging",
"Bar length b=2 m, subtended angle θ=2° → D = cot(1°)×2 = 57.29×2 ≈ 114.6 m.",
"Accuracy",
"Small θ makes D extremely sensitive to θ, so measure the angle precisely; large θ (close range) is more accurate, switch to stadia / EDM at long range.",
"Formula?",
"D = b/2 / tan(θ/2) = b·cot(θ/2), b is the known bar length and θ the subtended angle.",
"Is it still used?",
"Less used since EDM became common, but still used in teaching and power-free scenarios for its clear principle.",
],
'tangent-length-curve': [
"Tangent Length from Radius and Deflection Angle",
"Enter circular-curve radius R and deflection angle Δ (degrees) to obtain the tangent length.",
"Circular Curve Tangent Length Calculator",
"/ Circular Curve Tangent Length Calculator",
"📖 View the \"Tangent Length from Radius and Deflection Angle User Guide\"",
"The tangent length is the spacing between curve main points.",
"100·tan30° → 57.74 meters.",
"📚 In-depth: Circular Curve Tangent Length",
"Compute tangent length T from radius and deflection angle.",
"Measure T from the intersection to set the tangent-to-curve point.",
"One of the curve elements.",
"Tangent length",
"R=200 m, Δ=60° → T = R·tan(Δ/2) = 200×tan30° ≈ 115.5 m; measure T along each tangent from JD to get ZY/YZ.",
"Staking-out",
"T is the baseline start of curve staking, with L setting the whole alignment's stations.",
"What is the tangent length formula?",
"T = R·tan(Δ/2), Δ is the deflection angle (curve central angle).",
"What is the relation between T and E?",
"T runs along the tangent, E along the bisector; E = T·tan(Δ/4) approximately, different geometric directions.",
],
'triangulation-side': [
"Law of Sines",
"Triangulation Side Length",
"/ Triangulation Side Length",
"📖 View the \"Law of Sines User Guide\"",
"Known side a (m)",
"Angle A opposite known side (°)",
"Angle B opposite unknown side (°)",
"The law of sines applies to triangles.",
"The angles must be opposite their respective sides.",
"📚 In-depth: Triangulation Network Side Derivation",
"Find an unknown side from a known side and included angles by the law of sines.",
"Triangulation network expansion.",
"Control network layout.",
"Side by law of sines",
"Known side a=200 m, opposite A=40°, unknown b opposite B=65° → b = a·sinB/sinA = 200×sin65°/sin40° ≈ 200×0.906/0.643 ≈ 282 m.",
"Propagation",
"Use the known side as a baseline, then",
"derive the whole network's side lengths; angles must close and check.",
"Formula?",
"a/sinA = b/sinB = c/sinC; given one side and two angles find another side.",
"Angle error amplification?",
"Side-length propagation accumulates; control angle-measurement precision and figure strength (avoid too obtuse / acute angles).",
],
'vertical-curve-elev': [
"Parabolic Vertical Curve",
"Vertical Curve Elevation",
"/ Vertical Curve Elevation",
"📖 View the \"Parabolic Vertical Curve User Guide\"",
"Parabolic vertical curve y = ax²+bx+c",
"Grade-break point elevation (m)",
"Fore grade g₁ (%) (%)",
"Back grade g₂ (%) (%)",
"Curve length L (m)",
"Station spacing x (m)",
"x is measured from the grade-break point.",
"Sag / crest curve is decided by the signs of g₁, g₂.",
"📚 In-depth: Vertical Curve Elevation",
"Compute any point's elevation from the grade and vertical-curve radius.",
"Road profile design.",
"Parabolic transition at the grade-break point.",
"Parabola",
"Crest curve L=100 m, g₁=+2%, g₂=−3%, PVC elevation 100 m; at x=50 m from PVC: y = 100 + 0.02×50 + (50²/(2×100))×(−0.03−0.02) = 100 + 1 − 0.625 = 100.375 m.",
"The vertical curve ensures sight distance and comfort; radius is set by design speed, length affects the smoothing degree.",
"What is the vertical curve formula?",
"y = PVC + g₁x + (g₂−g₁)x²/(2L), x is the station from PVC, g is the grade decimal.",
"Crest and sag curves?",
"Crest curves prevent headlight / sight-distance obstruction; sag curves prevent centrifugal force and ponding; their radius requirements differ.",
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
    print('gen_surveying_b5 done')
