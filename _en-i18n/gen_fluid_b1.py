#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'fluid')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'fluid')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
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
    out = {'slug': slug, 'industry': 'fluid', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

def main():
    write('bernoulli-pressure', build('bernoulli-pressure', [
        "Bernoulli Pressure Calculator",
        "The relation between velocity and pressure along a streamline for an ideal fluid.",
        "/ Bernoulli Equation",
        "\U0001F4D6 View the \"Bernoulli Equation Guide\"",
        "Pressure P\u2081 (Pa)",
        "Where the pipe narrows the velocity rises and the pressure falls.",
        "\U0001F4DA In-depth Analysis: Bernoulli Equation",
        "Compute the pressure change along a streamline",
        "Converting between pipe velocity and pressure",
        "Siphons and",
        "p + 1/2*rho*v^2 + rho*g*h = constant. Example: in a horizontal pipe with v1=1 m/s and p1=200 kPa narrowing to v2=2 m/s, p2=200000 + 0.5*1000*(1-4) = 198500 Pa.",
        "Where the velocity rises the pressure falls, the Venturi principle that underlies aircraft lift and atomisers.",
        "What conditions does it require?",
        "Ideal, incompressible, steady flow along one streamline, with viscous losses ignored.",
        "How does it relate to the energy equation?",
        "Bernoulli is a special case of mechanical energy conservation; adding a loss term for real flow gives the general energy equation.",
    ]))

    write('buoyancy-force', build('buoyancy-force', [
        "The weight of the displaced fluid equals the buoyant force.",
        "/ Buoyancy",
        "Buoyancy",
        "\U0001F4D6 View the \"Buoyancy (Archimedes) Guide\"",
        "F_b = \u03c1_f g V. Buoyancy equals the weight of the displaced fluid.",
        "Buoyancy equals the weight of the displaced liquid.",
        "\U0001F4DA In-depth Analysis: Buoyancy (Archimedes)",
        "Compute the buoyant force on an object",
        "Judge whether it sinks or floats",
        "Ship loading",
        "Fb = rho_f * g * V_sub, the weight of the displaced fluid. Example: a 1 m\u00b3 wooden block fully submerged in water gives Fb=1000*9.81*1=9810 N.",
        "Sinking and floating",
        "If the object's average density exceeds the fluid's it sinks, if the two are equal it hovers, and if it is lower the object floats.",
        "Does buoyancy depend on depth?",
        "For the same submerged volume it is independent of depth, since the hydrostatic pressure difference stays constant.",
        "Why do ships float?",
        "The average density of the hull, including its empty holds, is less than that of water.",
    ]))

    write('capillary-pressure', build('capillary-pressure', [
        "Find the Capillary Pressure Difference from Surface Tension and Tube Diameter",
        "Enter the surface tension \u03b3 and the tube inner diameter D to find the capillary pressure difference.",
        "Capillary Pressure Difference Calculator",
        "/ Capillary Pressure Difference Calculator",
        "\U0001F4D6 View the \"Capillary Pressure Guide\"",
        "\u0394P = 4\u03b3/D for a fully wetting circular tube. Water, D=1 mm \u2192 288 Pa.",
        "Tube inner diameter D (m)",
        "\u0394P = 4\u03b3/D for a fully wetting circular tube.",
        "Water, D=1 mm \u2192 288 Pa.",
        "\U0001F4DA In-depth Analysis: Capillary Pressure",
        "Compute the pressure difference across a liquid-gas interface",
        "Porous media",
        "Bubbles and droplets",
        "\u0394p = 2*gamma/R for a spherical interface. Example: water with gamma=0.0728 N/m and R=1 mm gives \u0394p=145.6 Pa.",
        "Convex or concave?",
        "On a droplet's convex surface the inner pressure is higher, while for a bubble's concave surface the outer pressure is higher; the sign follows the direction of curvature.",
        "What are the applications?",
        "Alveolar stability, capillary action and oil displacement.",
    ]))

    write('capillary-rise', build('capillary-rise', [
        "Liquid rises in a narrow tube through surface tension.",
        "Capillary Rise Height Calculator",
        "/ Capillary Rise Height",
        "Capillary rise height",
        "\U0001F4D6 View the \"Capillary Rise Guide\"",
        "h = 2\u03b3cos\u03b8/(\u03c1gr). Water rises noticeably in a fine glass tube.",
        "Contact angle \u03b8 (\u00b0)",
        "Water rises noticeably in a fine glass tube.",
        "\U0001F4DA In-depth Analysis: Capillary Rise",
        "Compute how far a liquid column rises in a narrow tube",
        "Water uptake by soil or paper towel",
        "Pore water",
        "h = 2*gamma*cos theta/(rho*g*r). Example: water with gamma=0.0728, theta=0 and r=0.1 mm gives h=2*0.0728/(1000*9.81*1e-4)=0.148 m=14.8 cm.",
        "Does a narrower tube give a higher rise?",
        "Yes, the rise height is inversely proportional to the tube radius r.",
        "Why does mercury fall?",
        "Mercury does not wet the wall, with theta above 90 degrees and cos theta below 0, so the level drops.",
    ]))

    write('cavitation-number', build('cavitation-number', [
        "Find the Cavitation Number from Pressure and Velocity",
        "Enter the local pressure p, saturation vapour pressure p_v, density \u03c1 and velocity v to find the cavitation number.",
        "Cavitation Number Calculator",
        "/ Cavitation Number Calculator",
        "\U0001F4D6 View the \"Cavitation Number Guide\"",
        "v=10 \u2192 about 1.98.",
        "Local pressure p (Pa)",
        "Vapour pressure p_v (Pa)",
        "A smaller \u03c3 means cavitation occurs more easily, with \u03c3<1 dangerous.",
        "Water at 20 \u00b0C with v=10 \u2192 about 1.98.",
        "\U0001F4DA In-depth Analysis: Cavitation Number",
        "Judging cavitation in pumps and propellers",
        "Designing to avoid cavitation erosion",
        "Hydrofoils",
        "\u03c3 = (p \u2212 pv)/(\u00bd\u00b7\u03c1\u00b7v\u00b2), where pv is the saturation vapour pressure of the liquid; the smaller \u03c3 is, the easier cavitation occurs.",
        "\u03c3 = (p \u2212 pv)/(\u00bd\u00b7\u03c1\u00b7v\u00b2). Example: clean water at room temperature with pv=2339 Pa, p=101325 Pa, \u03c1=1000 kg/m\u00b3 and v=10 m/s gives \u03c3=(101325\u22122339)/(0.5\u00d71000\u00d7100)=98986/50000\u22481.98; if the critical \u03c3 of the blade section is roughly 0.3 to 1, this case has not yet cavitated, and the lower \u03c3 is the closer it comes to the cavitation threshold.",
        "What is the critical value?",
        "It varies with geometry; once sigma falls below the critical value cavities form, bringing noise and surface erosion.",
        "Why is it harmful?",
        "Collapsing cavities generate local high-pressure shocks that erode metal surfaces.",
    ]))

    write('chezy-velocity', build('chezy-velocity', [
        "Find Velocity from the Chezy Coefficient, Hydraulic Radius and Bed Slope",
        "Enter the Chezy coefficient C, hydraulic radius R and bed slope S to find the velocity.",
        "Chezy Velocity Calculator",
        "/ Chezy Velocity Calculator",
        "\U0001F4D6 View the \"Chezy Formula Guide\"",
        "Chezy coefficient C",
        "\U0001F4DA In-depth Analysis: Chezy Formula",
        "Compute",
        "uniform flow in open channels",
        "Rivers and canals",
        "Drainage",
        "V = C\u00b7\u221a(R\u00b7S), where R is the hydraulic radius, S the hydraulic or bed slope, and C the Chezy coefficient.",
        "V = C\u00b7\u221a(R\u00b7S). Example:",
        "a canal with C=50, hydraulic radius R=0.5 m and bed slope S=0.01 gives V=50\u00d7\u221a(0.5\u00d70.01)=50\u00d70.07071\u22483.54 m/s; with a flow area A=2 m\u00b2 the discharge is Q=V\u00b7A\u22487.07 m\u00b3/s.",
        "How does it relate to Manning?",
        "Taking C=R^(1/6)/n, the Manning form, reduces it to",
        ", with Chezy the earlier formula.",
        "When does it apply?",
        "Uniform flow in open channels.",
    ]))

    write('continuity-equation', build('continuity-equation', [
        "Continuity Equation Calculator",
        "Mass conservation for an incompressible fluid.",
        "/ Continuity Equation",
        "Continuity Equation",
        "\U0001F4D6 View the \"Continuity Equation Guide\"",
        "Continuity equation: for an incompressible fluid A\u2081\u00b7v\u2081 = A\u2082\u00b7v\u2082, so the discharge Q stays constant; velocity is inversely proportional to the cross-sectional area, so a narrower section means a higher velocity; from discharge and area the mean velocity is v = Q \u00f7 A, used in pipe and open channel design.",
        "Area A\u2081 (m\u00b2)",
        "Area A\u2082 (m\u00b2)",
        "A smaller cross-section means a higher velocity.",
        "\U0001F4DA In-depth Analysis: Continuity Equation",
        "Compute the velocity across a changing section",
        "Flow conservation in pipes",
        "Nozzles",
        "A1*v1 = A2*v2 for incompressible flow. Example: a pipe with A1=0.01 m\u00b2 and v1=1 m/s narrowing to A2=0.005 m\u00b2 gives v2=2 m/s.",
        "What about compressible flow?",
        "Use rho*A*v = constant, since the density changes as well.",
        "What is the essence of it?",
        "Steady-state mass conservation: what flows in equals what flows out.",
    ]))


if __name__ == '__main__':
    main()
