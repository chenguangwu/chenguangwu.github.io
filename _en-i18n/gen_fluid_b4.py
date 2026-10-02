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
    write('pressure-drop-darcy', build('pressure-drop-darcy', [
        "Find the Pipe Pressure Drop from the Friction Factor and Velocity",
        "Enter the friction factor f, pipe length L, diameter D, density \u03c1 and velocity v to find the pressure drop.",
        "Darcy Pressure Drop Calculator",
        "/ Darcy Pressure Drop Calculator",
        "\U0001F4D6 View the \"Darcy Pressure Drop Guide\"",
        "The Darcy-Weisbach formula.",
        "Example \u2192 400 Pa.",
        "\U0001F4DA In-depth Analysis: Darcy Pressure Drop",
        "Compute the friction loss along a pipe",
        "Pump head",
        "Pipe networks",
        "\u0394p = f*(L/D)*(rho*v^2/2). Example: with f=0.02, L=10, D=0.05, v=2 and water, \u0394p=0.02*200*1000*2=8000 Pa.",
        "How is f obtained?",
        "For laminar flow f=64/Re; for turbulent flow use the Moody chart or the Colebrook equation.",
        "How does it relate to minor losses?",
        "Add the minor losses on to get the total pressure drop.",
    ]))

    write('stagnation-pressure', build('stagnation-pressure', [
        "Find the Stagnation Pressure from Static Pressure and Velocity",
        "Enter the static pressure p, density \u03c1 and velocity v to find the stagnation pressure.",
        "Stagnation Pressure Calculator",
        "/ Stagnation Pressure Calculator",
        "\U0001F4D6 View the \"Stagnation Pressure Guide\"",
        "Stagnation pressure from the Bernoulli equation: p0 = p + 0.5*rho*v*v, that is the static pressure p plus the dynamic pressure q = 0.5*rho*v*v; at the stagnation point the velocity falls to zero and all the kinetic energy becomes pressure energy; the ratio p0/p reflects how strong the compressibility effect is, and the higher the velocity the more pronounced the stagnation pressure rise.",
        "Static pressure p (Pa)",
        "p\u2080 = p + \u00bd\u03c1v\u00b2, from Bernoulli.",
        "Example \u2192 about 101825 Pa.",
        "\U0001F4DA In-depth Analysis: Stagnation Pressure",
        "Compute the total pressure",
        "Pitot tubes",
        "Compressors",
        "p0 = p + 0.5*rho*v^2 for incompressible flow. Example: a static pressure of 100 kPa with a dynamic pressure of 6 kPa gives p0=106 kPa.",
        "Total pressure and static pressure?",
        "At the stagnation point, where the velocity is zero, the total pressure measured equals the static pressure plus the dynamic pressure.",
        "What about compressible flow?",
        "At high speed use the isentropic total pressure formula with a",
        "Mach number",
        "correction.",
    ]))

    write('stokes-settling', build('stokes-settling', [
        "The uniform settling velocity of small particles at low Reynolds number.",
        "Stokes Settling Velocity Calculator",
        "/ Stokes Settling Velocity",
        "Stokes Settling Velocity",
        "\U0001F4D6 View the \"Stokes Settling Guide\"",
        "v = 2r\u00b2(\u03c1_p\u2212\u03c1_f)g/(9\u03bc), for small spheres at low Reynolds number.",
        "Particle radius r (m)",
        "Particle density \u03c1_p (kg/m\u00b3)",
        "It applies to small spheres at low Reynolds number.",
        "\U0001F4DA In-depth Analysis: Stokes Settling",
        "Compute the particle settling velocity",
        "Dust removal and sedimentation",
        "Slurries",
        "v = (rho_p-rho_f)*g*d^2/(18*mu). Example: sand with d=100 \u03bcm, \u0394rho=1600 and water mu=1e-3 gives v=1600*9.81*1e-8/(18e-3)=8.7e-3 m/s.",
        "When does it apply?",
        "To fine",
        "particles with Rep below 1 settling in laminar flow.",
        "What about large particles?",
        "Beyond the Stokes regime, switch to the drag coefficient method.",
    ]))

    write('venturi-flow-rate', build('venturi-flow-rate', [
        "Find the Volume Flow Rate from the Pressure Difference and Cross-sectional Area",
        "Enter the inlet and throat areas A1 and A2, the pressure difference \u0394P and the density \u03c1 to find the flow rate.",
        "Venturi Flow Meter Calculator",
        "/ Venturi Flow Meter Calculator",
        "\U0001F4D6 View the \"Venturi Flow Guide\"",
        "Inlet area A\u2081 (m\u00b2)",
        "Throat area A\u2082 (m\u00b2)",
        "Derived from Bernoulli together with continuity.",
        "Example \u2192 about 0.00204 m\u00b3/s.",
        "\U0001F4DA In-depth Analysis: Venturi Flow",
        "Measuring flow from a pressure difference",
        "Flow meters",
        "Energy saving",
        "Q = A2\u00b7\u221a(2\u00b7\u0394p/(rho\u00b7(1\u2212(A2/A1)\u00b2))). The throat constriction creates a pressure difference that is converted into flow, and this simplified form omits the discharge coefficient.",
        "Q=A2\u00b7\u221a(2\u0394p/(rho\u00b7(1\u2212(A2/A1)\u00b2))). Example: with A1=0.01, A2=0.0025, \u0394p=5 kPa and water rho=1000, Q=0.0025\u00b7\u221a(2\u00b75000/(1000\u00b7(1\u22120.25\u00b2)))=0.0025\u00b73.27\u22488.2e-3 m\u00b3/s, about 29.5 m\u00b3/h.",
        "Why is it energy saving?",
        "It has no moving parts and a small pressure loss, measuring flow through the pressure difference.",
        "The Cd of a Venturi meter is as high as 0.98-0.99.",
    ]))

    write('volume-flow-rate', build('volume-flow-rate', [
        "The product of cross-sectional area and velocity.",
        "Volume Flow Rate Calculator",
        "/ Volume Flow Rate",
        "\U0001F4D6 View the \"Volume Flow Rate Guide\"",
        "Volume flow rate formula: Q = A * v, where A is the flow cross-sectional area and v the mean velocity over that section; Q is given in m\u00b3/s, and multiplying by 1000 gives L/s while multiplying by 3600 gives m\u00b3/h; the area can also be recovered from the flow rate and velocity as A = Q/v.",
        "Direct estimation of pipe flow.",
        "\U0001F4DA In-depth Analysis: Volume Flow Rate",
        "Compute the volume flow rate",
        "Pipe diameter selection",
        "Pumps",
        "Q = A*v. Example: a pipe of D=0.1 m with v=1 m/s gives Q=pi*0.05^2*1=7.85e-3 m\u00b3/s=28.3 m\u00b3/h.",
        "What about mass flow rate?",
        "What are the units?",
        "m\u00b3/s, L/s and m\u00b3/h are common, so watch the conversions.",
    ]))

    write('weber-number', build('weber-number', [
        "Find the Weber Number from Velocity, Length Scale and Surface Tension",
        "Enter the density \u03c1, velocity v, characteristic length L and surface tension \u03c3 to find the Weber number.",
        "Weber Number Calculator",
        "/ Weber Number Calculator",
        "\U0001F4D6 View the \"Weber Number Guide\"",
        "Surface tension \u03c3 (N/m)",
        "We expresses the ratio of inertial force to surface tension.",
        "Water, example \u2192 5556.",
        "\U0001F4DA In-depth Analysis: Weber Number",
        "Judging whether surface tension dominates",
        "Droplet breakup",
        "Sprays",
        "We = rho*v^2*L/gamma. Example: water with gamma=0.0728 N/m, v=10 m/s and a characteristic length L=0.01 m gives We=1000*100*0.01/0.0728=1.37e4, about 13736; once We is above 1 inertia dominates and droplets break up easily.",
        "What is its physical meaning?",
        "The ratio of inertial force to surface tension; a large We means droplets break up easily.",
        "What are the applications?",
        "A similarity criterion for sprays, bubbles and capillary flows.",
    ]))


if __name__ == '__main__':
    main()
