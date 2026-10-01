#!/usr/bin/env python3
# machinery batch6 (5 slugs)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'stretch': [
"🧮 Spring Parameter Calculator",
"Stiffness and strength verification of cylindrical helical springs (compression / extension / torsion)",
'📖 View the "Spring Parameter Calculator Guide"',
"Spring stiffness k = G·d⁴/(8D³n)",
"Compression spring",
"Extension spring",
"Torsion spring",
"Wire diameter d (mm)",
"Mean diameter D (mm)",
"Free length L₀ (mm)",
"Carbon spring steel (G=79 GPa, τ=560)",
"Piano wire (G=79 GPa, τ=640)",
"Stainless steel 304 (G=73 GPa, τ=440)",
"Tin bronze (G=44 GPa, τ=320)",
"Allowable shear stress τ (MPa)",
"💡 Stiffness k=Gd⁴/(8D³n); spring index C=D/d; Wahl factor Kw=(4C-1)/(4C-4)+0.615/C; maximum load Fmax=τ·πd³/(8Kw·C).",
"📚 In-Depth Analysis: Torsion Bar / Spring Torsion",
"Torsional stiffness kT=E·d⁴/(10.8·D·n) (torsion bar).",
"Maximum torque Mmax=τ·π·d³/32, maximum angle=Mmax/kT.",
"Helical spring k=G·d⁴/(8·D³·n), δ=F/k.",
"Torsion bar",
"Helical spring",
"G=79000, d=3, D=20, n=10: k=79000×81/(8×8000×10)=6399000/640000≈10.0 N/mm; at F=100 N, δ=10 mm.",
"Are the stiffness formulas for a torsion bar and a helical spring different?",
"Yes. A torsion bar works by circular-shaft torsion (E, d⁴, with D as the lever arm), while a helical spring works by cylindrical coiling (G, d⁴, D³, n); their dimensions and meanings differ.",
"What is the solid length?",
"The length when all coils are pressed together, Lb=n·d; deformation beyond L0−Lb causes solid stacking and failure, so the design must leave travel margin.",
"Wire diameter",
"Spring mean diameter",
"Number of active coils",
"Free length",
],
'tanhuangsheji': [
"📐 Spring Design Calculator",
"Enter the wire diameter, mean diameter, number of active coils and material to compute the spring stiffness, maximum deflection, shear stress and natural frequency",
"Spring Design",
"/ Spring Design",
'📖 View the "Spring Design Calculator Guide"',
"Spring design k = G·d⁴/(8D³n)",
"Wire diameter d (mm)",
"Carbon spring wire (G=79300, [τ]=560)",
"Piano wire (G=79300, [τ]=680)",
"Silicon-manganese alloy wire (G=79300, [τ]=640)",
"Stainless steel 304 (G=70000, [τ]=440)",
"Tin bronze (G=43000, [τ]=350)",
"Beryllium bronze (G=130000, [τ]=500)",
"Working load F (N)",
"💡 Formula: spring index C=D/d; Wahl factor K=(4C-1)/(4C-4)+0.615/C; stiffness k=G·d⁴/(8·D³·n); shear stress τ=K·8F·D/(π·d³); maximum deflection δmax=[τ]·π·D²·n/(K·G·d)",
"The spring index C is usually 4-16; too small is hard to machine, too large tends to buckle",
"Springs under variable load should be checked for fatigue strength; this tool uses static strength",
"When the slenderness ratio (free length / mean diameter) exceeds 3.7, buckling must be checked",
"The allowable stress depends on the load nature: class I (variable load) takes the lower value, class III (static load) the higher value",
"The natural frequency should be more than about 10 times the working frequency to avoid resonance",
"📚 In-Depth Analysis: Cylindrical Helical Spring Design",
"Stiffness k=G·d⁴/(8·D³·n), working stress τ=8·F·D/(π·d³).",
"Free length Lf, solid length Ls and natural frequency fn checks.",
"Safety factor sf=[τ]/τ.",
"Compression spring",
"d=3, D=20, n=10, G=79000, F=100 N: k=79000×81/(8×8000×10)=10.0 N/mm; τ=8×100×20/(π×27)=16000/84.8≈188.7 MPa; δ=100/10=10 mm. If [τ]=500, sf=500/188.7≈2.65.",
"Natural frequency",
"Mass m=0.2 kg: fn=(1/(2π))√(k·1000/m)=(1/6.283)√(10000/0.2)=(0.159)×√50000=0.159×223.6≈35.6 Hz. The excitation frequency should be kept away to prevent resonance.",
"Where does τ=8FD/πd³ come from?",
"The maximum torsional shear stress of a cylindrical helical spring (the simple form before curvature correction); d is the wire diameter and D the mean diameter.",
"Why compute the natural frequency?",
"If the working frequency approaches fn, resonance amplifies the stress; the stiffness/mass must be adjusted so the frequency ratio avoids the region near 1.",
'About "Spring Design"',
"A cylindrical helical compression spring design calculator: from the wire diameter, spring mean diameter, number of active coils and material parameters it computes the spring index, Wahl factor, stiffness, maximum deflection, shear stress, natural frequency and geometry, aiding spring parameter design and verification.",
"Built-in parameters for six common spring materials",
"Computes the spring index and judges its reasonableness",
"Outputs stiffness, maximum load and natural frequency",
"Stress and safety factor check under the working load",
"Cylindrical helical compression spring parameter design",
"Spring stiffness and travel calculation",
"Spring material selection comparison",
"Variable-load spring strength verification",
],
'temp-hardness': [
"🌡️ Heat-Treatment Hardness / Temperature Curve",
"Estimate the post-tempering hardness (HRC) from the steel grade and heat-treatment process",
'📖 View the "Heat-Treatment Hardness / Temperature Curve Guide"',
"Heat-treatment hardness = f(temperature, cooling)",
"45 steel (medium carbon steel)",
"40Cr (alloy quenched and tempered steel)",
"42CrMo (chrome-molybdenum quenched and tempered steel)",
"35CrMo (chrome-molybdenum steel)",
"20CrMnTi (carburising steel)",
"65Mn (spring steel)",
"T8 (carbon tool steel)",
"T10 (carbon tool steel)",
"9SiCr (alloy tool steel)",
"GCr15 (bearing steel)",
"Cr12MoV (die steel)",
"Quenching medium",
"Water quench",
"Oil quench",
"Air cool",
"Maximum quenched hardness (HRC)",
"Tempering softening coefficient k",
"Critical hardening diameter (mm)",
"Tempering temperature (°C)",
"Section size (mm)",
"🧮 Compute hardness",
"💡 Tempered hardness ≈ quenched hardness − k×(T_temper−150)/100, then reduced according to the section size and hardenability. The data are empirical estimates.",
"Heat-treatment parameters of common steel grades",
"Quenching temp. °C",
"Water-quench HRC",
"Tempering softening k",
"Critical diameter mm",
"Shafts, gears",
"Shafts, connecting rods",
"High-strength shafts",
"Cutting tools, dies",
"Bearings, gauges",
"Cold-work dies",
"📚 In-Depth Analysis: Hardenability and Section Hardness",
"Judge whether the core is fully hardened from the section size and the critical hardening diameter.",
"Compare the hardened-case depth of different steel grades.",
"Select a higher-hardenability steel grade for large sections.",
"Critical hardening diameter",
"For a steel with critical hardening diameter D0=30 mm (oil quench), a 50 mm section > 30 mm means the core cannot be fully hardened and its hardness is markedly lower than the surface (e.g. 55 HRC at the surface, 35 HRC at the core); switch to a steel with a larger D0 or use water quenching.",
"Hardness gradient",
"The surface hardness decreases with distance from the surface; the effective case depth is defined where the HRC drops by 50%.",
"Hardenability vs achievable hardness?",
"Hardenability = the section size that can be fully hardened (influenced by alloying elements); achievable hardness = the maximum hardness that can be reached (determined by carbon content). The two differ.",
"What if the section exceeds the limit?",
"Choose a higher-hardenability steel, increase the cooling severity (water quench / quenchant) or switch to surface hardening (induction / carburising) to harden only the surface layer.",
"Tempering temperature",
"Section size",
],
'thread-drive': [
"📐 Screw Drive Design",
"Enter the thread mean diameter, lead, axial load and friction coefficient to compute the drive efficiency and driving torque and determine the self-locking condition",
'📖 View the "Screw Drive Design Guide"',
"Thread lead angle λ = arctan(p/(πd))",
"Thread mean diameter d2 (mm)",
"Lead L (mm)",
"Axial load F (kN)",
"Thread friction coefficient μ",
"Thrust bearing friction coefficient μc",
"Thrust bearing equivalent diameter dc (mm)",
"💡 Formula: lead angle λ=arctan(L/(π·d2)); friction angle ρ=arctan(μ); driving torque T=F·[d2/2·tan(λ+ρ)+μc·dc/2]; efficiency η=tan(λ)/tan(λ+ρ); self-locking condition λ≤ρ",
"The trapezoidal thread (Tr) is the common transmission thread, with a mean diameter about the major diameter minus 0.5 of the pitch",
"The friction coefficient depends on lubrication: well lubricated 0.06-0.1, normally lubricated 0.1-0.15, dry friction 0.15-0.25",
"The self-locking condition λ≤ρ is an important safety index for drives and must be met by lifting mechanisms",
"Thrust bearing friction lowers the drive efficiency; for a rolling bearing μc≈0.005-0.01",
"The results suit preliminary design verification; detailed calculation must consider the thread-tooth strength",
"📚 In-Depth Analysis: Screw Drive Driving Torque",
"Thread-pair torque T_thread=F·d2/2·tan(λ+ρ).",
"Thrust bearing friction T_collar=F·μc·dc/2.",
"Total torque T_total and drive power P=T_total·ω.",
"Lifting screw",
"F=5 kN, mean diameter d2=20 mm, lead angle λ=3°, friction angle ρ=9°: T_thread=5000×10×tan12°=50000×0.2126≈10630 N·mm=10.63 N·m; with thrust μc=0.1, dc=30: T_collar=5000×0.1×15=7500 N·mm=7.5 N·m; T_total≈18.1 N·m.",
"Ideal work=F·L (L=lead), input work=2π·T_total; efficiency=useful/input. In the example L=π·d2·tanλ≈π×20×0.0524≈3.29 mm and efficiency≈(5000×3.29)/(2π×18100)≈0.144=14.4%.",
"Why add the friction angle ρ?",
"The thread lead angle λ and the friction angle ρ combine into an equivalent lead angle; the self-locking condition is λ≤ρ (i.e. efficiency ≤50%).",
"Does a larger lead angle give higher efficiency?",
"Yes, but too large loses self-locking (for example, a jack requiring self-locking uses a single-start thread with a small lead angle).",
'About "Screw Drive Design"',
"A screw drive design calculator: from the thread mean diameter, lead, axial load and friction coefficient it computes the thread lead angle, equivalent friction angle, driving torque and transmission efficiency and determines whether the self-locking condition is met, suitable for screw mechanism design.",
"Computes the thread lead angle and equivalent friction angle",
"The driving torque includes the thread pair and thrust bearing parts",
"Outputs the overall efficiency and the thread-pair efficiency separately",
"Automatically determines the self-locking condition and gives a hint",
"Design of screw lifts and jack drives",
"Machine-tool lead-screw drive parameter calculation",
"Valve actuation mechanism efficiency verification",
"Screw press drive scheme design",
],
'thread-recognize': [
"🔍 Thread Identification (Metric / Unified)",
"Enter the outer diameter and pitch (or TPI) to automatically match the standard thread specification",
'📖 View the "Thread Identification (Metric / Unified) Guide"',
"Thread identification = parameter lookup",
"Pitch (mm)",
"Threads per inch (TPI)",
"Outer / major diameter (mm)",
"Thread angle",
"Auto-detect",
"60° (metric / unified)",
"55° (British Whitworth)",
"30° (trapezoidal / pipe thread)",
"🔍 Identify",
"💡 Metric threads have a 60° thread angle and use pitch in mm; British Whitworth threads have a 55° thread angle and use TPI; Unified (UN) threads have a 60° thread angle and use TPI.",
"Common metric coarse thread specifications",
"Pitch mm",
"📚 In-Depth Analysis: Thread Parameter Identification",
"Match the standard thread (metric / imperial / TPI) from the measured outer diameter and pitch.",
"Derive the mean diameter d2, minor diameter d1 and thread height H.",
"Metric-imperial conversion (TPI=25.4/pitch).",
"M10×1.5 identification",
"Outer diameter≈10, pitch 1.5, thread angle 60°: H=p/(2·tan30°)=1.5/1.1547≈1.299 mm; d2=10−0.75×1.299×cos30°=10−0.843≈9.157 mm; d1=10−1.0825×1.5≈8.376 mm. Matches the standard M10×1.5.",
"Imperial conversion",
"1/2-20 UNF: TPI=20 → pitch=25.4/20=1.27 mm; outer diameter 12.7 mm.",
"Why use 0.75H·cos(α/2) for the mean diameter?",
"For the theoretical profile of a 60° metric triangular thread, mean diameter = major diameter − 2×(H/2 projected axially), which geometrically yields this expression (H is the theoretical thread height).",
"Can measuring the outer diameter uniquely determine the thread?",
"No, the pitch (or TPI) and thread angle must also be measured; the same outer diameter with a different pitch is a different specification.",
"Outer diameter",
"Pitch",
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
