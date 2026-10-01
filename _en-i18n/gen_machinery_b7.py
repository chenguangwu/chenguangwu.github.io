#!/usr/bin/env python3
# machinery batch7 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'tolerance': [
"🧮 Fit Tolerance Calculator",
"Enter the basic size and fit designation (e.g. H7/g6) to compute the hole and shaft limit deviations and the fit clearance/interference",
'📖 View the "Fit Tolerance Calculator Guide"',
"Fit tolerance = hole/shaft deviation",
"Fit designation (hole/shaft)",
"Basis system",
"Hole-basis system (H basis)",
"Shaft-basis system (h basis)",
"💡 IT value: i=0.45·D^(1/3)+0.001·D, IT6=10i, IT7=16i, IT8=25i; shaft deviations a-h are the upper deviation es and j-zc the lower deviation ei; hole deviations A-H are the lower deviation EI=-es",
"Fit designation format: hole code / shaft code, e.g. H7/g6, H7/k6, H7/p6",
"In the hole-basis system H is the basis hole (lower deviation EI=0); in the shaft-basis system h is the basis shaft (upper deviation es=0)",
"Clearance fit (a-h/A-H), transition fit (j-n/J-N), interference fit (p-zc/P-ZC)",
"The deviation values are computed per the GB/T 1800.2 ISO tolerance formulas and may differ slightly from the standard tables",
"This tool applies to the common fit range of D≤500 mm and IT5-IT11",
"📚 In-Depth Analysis: Fit Tolerance Calculation",
"Find ES/EI/es/ei and the limit clearances from the hole/shaft fundamental deviations.",
"Fit tolerance Tfit=Xmax−Xmin.",
"Clearance / transition / interference fit discrimination.",
"Hole H7: ES=+0.025, EI=0; shaft g6: es=−0.009, ei=−0.025: Xmax=(0.025+0.025)/1000=0.050 mm, Xmin=(0+0.009)/1000=0.009 mm, Tfit=0.041 mm. Clearance fit.",
"Interference fit",
"H7/p6: ei is positive and Xmin negative (interference), used for tight fits that transmit torque.",
"What do the fundamental deviation letters mean?",
"Uppercase for holes, lowercase for shafts; H is the hole basis (lower deviation 0) and h the shaft basis (upper deviation 0); the different positions of the a-zc deviations determine how tight the fit is.",
"What does a large fit tolerance indicate?",
"A large Tfit means a wide clearance/interference range and poor assembly consistency; for high precision choose a tighter grade combination.",
'About "Fit Tolerance Calculator"',
"A fit tolerance calculator: per the GB/T 1800 ISO limits and fits system, enter the basic size and fit designation (e.g. H7/g6) and it automatically computes the hole and shaft upper/lower deviations, maximum/minimum clearance or interference and fit tolerance, and determines the fit type.",
"Parses any hole/shaft fit designation",
"Automatically recognises hole-basis, shaft-basis and mixed systems",
"Computes clearance/interference and fit tolerance",
"Determines clearance, transition and interference fits",
"Fit selection and verification in mechanical design",
"Dimension tolerance marking on part drawings",
"Assembly clearance/interference verification",
"Machining fit-accuracy planning",
],
'tolerance-1': [
"📐 Geometric Tolerance Lookup",
"Per GB/T 1184 Annex B, select the tolerance type, nominal size and tolerance grade to look up the geometric tolerance value",
"Geometric Tolerance Marking",
"/ Geometric Tolerance Marking",
'📖 View the "Geometric Tolerance Lookup Guide"',
"Geometric tolerance = marking lookup",
"Tolerance type",
"Roundness / cylindricity",
"Straightness / flatness",
"Parallelism / perpendicularity / angularity",
"Coaxiality / symmetry / position",
"Circular runout / total runout",
"Nominal size D (mm)",
"Tolerance grade",
"💡 Per GB/T 1184-1996 Annex B reference values: roundness/cylindricity are looked up by diameter (grades 0-12); straightness/flatness by length (grades 1-12); other tolerance types are converted within the same size range",
"GB/T 1184 Annex B provides reference values; geometric tolerances not specified by the standard can be looked up by the corresponding grade",
"Roundness/cylindricity uses diameter D as the main parameter and straightness/flatness uses the measured length L",
"The coaxiality and symmetry tolerance values are diameter φ values (table value ×2)",
"Position tolerance is usually per the GB/T 1184 annex or specified by the designer",
"Unspecified geometric tolerances follow GB/T 1184 classes K, L and M",
"📚 In-Depth Analysis: Geometric Tolerance Lookup",
"Look up the geometric tolerance value by nominal size and accuracy grade (μm→mm).",
"Roundness/cylindricity/flatness/position and other types.",
"Marking examples and accuracy evaluation.",
"Roundness IT grade",
"Nominal size D=50 mm, a certain geometric tolerance grade: the table gives a tolerance value tUm=8 μm=0.008 mm; mark ⌖0.008. The higher the grade (smaller number), the tighter the tolerance.",
"Grade conversion",
"For the same size the tolerance value ranges from 8 μm (higher precision) to 25 μm (lower precision), corresponding to different machining methods (grinding vs milling).",
"Geometric tolerance and dimensional tolerance?",
"Dimensional tolerance controls size and geometric tolerance controls shape/position; the two are either independent (principle of independence) or linked (maximum material requirement).",
"Why are tolerance values in μm?",
"Geometric tolerances of precision parts are usually a few to a few tens of microns; μm is intuitive and converted to mm (÷1000) for marking.",
'About "Geometric Tolerance Marking"',
"A geometric tolerance lookup tool: per the GB/T 1184-1996 Annex B reference values, it supports five geometric tolerance categories - roundness/cylindricity, straightness/flatness, parallelism/perpendicularity/angularity, coaxiality/symmetry/position and circular/total runout - and quickly gives the tolerance value by nominal size and tolerance grade.",
"Covers five major geometric tolerance categories",
"Built-in GB/T 1184 Annex B standard data tables",
"Automatically matches the size segment and tolerance grade",
"Outputs both mm and μm units with an accuracy evaluation",
"Geometric tolerance marking on mechanical part drawings",
"Machining accuracy grade selection and verification",
"Geometric tolerance design of mating surfaces",
"Tolerance-zone determination in quality inspection",
"How to use the Geometric Tolerance Lookup",
"What does the Geometric Tolerance Lookup do?",
"How do I use the Geometric Tolerance Lookup?",
"What scenarios suit the Geometric Tolerance Lookup?",
],
'xiao-dingwei-lianjie-chicun': [
"⚙️ Pin (Locating / Connecting) Size",
"Compute the diameter and cross-sectional area of a locating/connecting pin from the transmitted force and allowable shear stress, for mechanical connections and fixture locating design.",
'📖 View the "Pin (Locating / Connecting) Size Guide"',
"Pin diameter d = √(4F ÷ (π·τ)); F is the transmitted force and τ the allowable shear stress",
"Locating and connecting pins mainly carry load in shear; the diameter is back-calculated from τ = 4F/(πd²): d = √(4F/(πτ)). F in kN (×1000 to N) and τ in MPa (=N/mm²) give the pin diameter in mm directly, to compare against standard pin sizes.",
"Transmitted force F (kN)",
"Allowable shear stress τ (MPa)",
"💡 Pin diameter d = √(4F ÷ (π·τ)); F (kN)×1000 to N and τ (MPa)=N/mm² give the result in mm.",
"📚 In-Depth Analysis: Pin Locating/Connecting Size",
"Select the diameter d and length L of a cylindrical/taper pin from the shear and crushing.",
"Shear τ=F/(π·d²/4·n), crushing σc=F/(d·t) check.",
"Locating accuracy and fit (interference/transition) selection.",
"Cylindrical pin shear",
"F=4 kN, pin d=8, n=1 (single shear), plate thickness t=10: As=π×8²/4=50.27 mm²; τ=4000/50.27≈79.6 MPa; σc=4000/(8×10)=50 MPa. Allowable [τ]=100, [σc]=120, satisfied.",
"Taper pin",
"A taper pin locates by friction and can be assembled and disassembled repeatedly; its diameter is nominal at the small end, its load capacity is lower than a cylindrical pin but its locking is better.",
"Can a pin joint transmit torque?",
"It can transmit small torques (by shear); large torques need a key/spline; pins are mostly used for locating and overload protection (shear pins).",
"Why use a transition fit for locating?",
"A locating pin must not be loose yet remain removable, so a transition fit (such as H7/m6) is common; too much interference makes removal hard and too much clearance loses accuracy.",
'About "Pin (Locating / Connecting) Size"',
"A pin (locating/connecting) size calculator. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
"Locating",
],
'zhineng-wurenyugaoxiaoduibijisuanqi': [
"⚙️ Intelligent, Unmanned and High-Efficiency Comparison Calculator",
"Compare the intelligent and high-efficiency scores to give a recommendation on the emphasis of the equipment R&D route.",
"/ Innovation (Intelligent / Unmanned / High-Efficiency) R&D",
'📖 View the "Intelligent, Unmanned and High-Efficiency Comparison Calculator Guide"',
"Composite gap = |intelligent − high-efficiency|; intelligent weight ratio = intelligent ÷ (intelligent + high-efficiency) × 100%",
"Equipment-manufacturing upgrading balances intelligence and efficiency: the intelligent score reflects autonomous decision-making capability and the high-efficiency score reflects the capacity/energy-consumption ratio. Comparing the two gives the R&D emphasis, and the weight ratio quantifies the relative share, aiding technical resource allocation.",
"Intelligent score (0-100)",
"High-efficiency score (0-100)",
"💡 Composite gap = |intelligent − high-efficiency|; intelligent weight ratio = intelligent ÷ (intelligent + high-efficiency).",
"📚 In-Depth Analysis: UAV Operation Parameter Comparison",
"Side-by-side comparison of endurance, speed, payload and operating altitude of multiple models.",
"Operation efficiency = swath × speed × time to estimate the coverage area.",
"Composite-score ranking aids model selection.",
"Coverage efficiency",
"Swath B=5 m, speed v=5 m/s, single sortie t=600 s: coverage area≈B·v·t=5×5×600=15000 m²=1.5 hectares per sortie. When comparing two models, choose the more efficient one.",
"Operating altitude",
"Flight altitude h=50 m, swath 5 m: ground resolution and overlap determine the modelling accuracy; a lower altitude gives higher resolution but lower efficiency.",
"Why use swath × speed for the coverage area?",
"Aerial operation approximates strip coverage: the area per unit time = swath × ground speed, multiplied by the sortie time to give the total coverage.",
"What should be noted in the comparison?",
"Endurance is affected by wind and temperature, and payload trades off against endurance; selection must consider the mission (surveying / plant protection / inspection) and local altitude regulations.",
'About "Innovation (Intelligent / Unmanned / High-Efficiency) R&D"',
"An innovation (intelligent/unmanned/high-efficiency) R&D calculator. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
"Intelligent",
"Unmanned",
],
'zhujian-bamoxiedu-sheji': [
"📐 Casting (Draft Angle) Design",
"Determine the draft-angle tier by casting height and compute the dimensional difference caused by the taper and the allowance at the top outer diameter.",
'📖 View the "Casting (Draft Angle) Design Guide"',
"Draft angle is tiered by height: ≤10 mm uses 3.0°, 10-50 mm uses 1.5°, 50-200 mm uses 1.0°, >200 mm uses 0.5°",
"The draft angle decreases as the casting height increases: the greater the height, the larger the dimensional deviation caused by the same angle. This tool takes the taper from the height tier and then uses tanα to find the dimensional difference in the height direction and the allowance at the top outer diameter, avoiding mould-drag damage to the sand mould.",
"Casting height (mm)",
"Casting outer diameter (mm)",
"💡 Draft angle is tiered by height (≤10→3.0°, 10-50→1.5°, 50-200→1.0°, >200→0.5°); dimensional difference = height × tanα.",
"📚 In-Depth Analysis: Casting Draft Angle Design",
"Sand-casting draft design: determine the draft-angle tier by casting height and compute the radial dimensional difference and top allowance caused by the taper, avoiding mould-drag damage to the sand mould or out-of-tolerance casting dimensions.",
"Height-direction size compensation: the height difference from tanα is used to correct the mould machining size; deep-cavity parts especially need to be machined to the top size while the bottom stays at the nominal size.",
"Tier verification: compare the dimensional difference caused by 1.0° and 1.5° at the same height to assess the effect of increasing the taper on dimensional accuracy and subsequent machining allowance.",
"Example: casting height 120 mm, outer diameter 200 mm",
"A height of 120 mm falls in the 50-200 mm tier → draft angle 1.0°; dimensional difference caused by the taper = 120 × tan1.0° = 2.09 mm; top outer diameter = 200 + 2 × 2.09 = 204.19 mm; top outer-diameter enlargement ratio = 2 × 2.09 ÷ 200 × 100% = 2.09%.",
"Why is the draft angle smaller for a taller casting?",
"At the same angle, a greater height causes a larger radial dimensional deviation (dimensional difference = height × tanα), so above 200 mm it drops to 0.5° to keep the dimensional difference within an acceptable range.",
"Are the draft angle and the drawing angle the same thing?",
"They mean the same: sand casting calls it the mould-draft angle, while permanent-mould casting and injection moulding call it the draft angle; both are tapers set to ease release, differing only in the specification and typical values.",
"Should the taper be added to the cavity or the outer shape?",
"Usually the cavity taper should be larger than the outer-shape taper, because the sand mould or core experiences greater friction during release; the outer-shape taper can be reduced to control the dimensional difference.",
"How should the computed dimensional difference be used?",
"Top outer diameter = nominal outer diameter + 2 × dimensional difference; the mould is machined to the top size while the bottom stays at the nominal size. Also confirm whether the dimensional difference exceeds the subsequent machining allowance, otherwise a black skin (unmachined surface) will appear.",
'About "Casting (Draft Angle) Design"',
"A casting (draft angle) design calculator. Free online tool, processed entirely on the client side; data is not uploaded, protecting your privacy.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
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
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
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
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'machinery', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
