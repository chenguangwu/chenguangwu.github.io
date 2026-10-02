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
    write('laplace-sphere-pressure', build('laplace-sphere-pressure', [
        "Find the Pressure Difference Across a Spherical Bubble from Surface Tension and Radius of Curvature",
        "Enter the surface tension \u03b3 and the radius of curvature R to find the pressure difference.",
        "Laplace Spherical Bubble Pressure Calculator",
        "/ Laplace Spherical Bubble Pressure Calculator",
        "\U0001F4D6 View the \"Laplace (Spherical) Pressure Guide\"",
        "\u0394P = 2\u03b3/R, or 4\u03b3/R for a spherical liquid film. Water, R=1 mm \u2192 144 Pa.",
        "Radius of curvature R (m)",
        "\u0394P = 2\u03b3/R, or 4\u03b3/R for a spherical liquid film.",
        "Water, R=1 mm \u2192 144 Pa.",
        "\U0001F4DA In-depth Analysis: Laplace (Spherical) Pressure",
        "Compute the pressure difference across a bubble",
        "Surface tension",
        "Foam stability",
        "\u0394p = 2\u03b3/R for a single spherical interface, while a soap bubble with two interfaces gives \u0394p=4\u03b3/R.",
        "\u0394p=2\u03b3/R. Example: water with \u03b3=0.0728 N/m and a radius of curvature R=1 mm gives \u0394p=2\u00d70.0728/0.001=145.6 Pa for a single interface; a soap bubble, with two interfaces, gives \u0394p=4\u00d70.0728/0.001=291.2 Pa, so small bubbles carry a higher internal pressure.",
        "Capillary pressure",
        "The same expression, describing the interfacial pressure difference caused by curvature.",
        "What about small bubbles?",
        "A smaller R gives a larger \u0394p, so small bubbles are at higher internal pressure and readily merge into larger ones.",
    ]))

    write('manning-velocity', build('manning-velocity', [
        "Mean velocity of uniform open channel flow.",
        "Manning Formula Velocity Calculator",
        "/ Manning Formula",
        "\U0001F4D6 View the \"Manning Formula Guide\"",
        "v = (1/n)R^(2/3)S^(1/2). A concrete channel has n of about 0.013.",
        "A concrete channel has n of about 0.013.",
        "\U0001F4DA In-depth Analysis: Manning Formula",
        "Compute the velocity in an open channel",
        "River discharge",
        "Drainage design",
        "V = (1/n)\u00b7R^(2/3)\u00b7S^(1/2). Example:",
        "a channel with n=0.013, hydraulic radius R=0.5 and bed slope S=0.001 gives V=(1/0.013)\u00d70.5^(2/3)\u00d7\u221a0.001\u224876.92\u00d70.630\u00d70.0316\u22481.53 m/s, matching the tool's live calculation.",
        "How is n chosen?",
        "About 0.012 for smooth concrete, 0.03-0.04 for natural rivers and 0.05 for rubble.",
        "When does it apply?",
        "Uniform turbulent flow in open channels; it is the most widely used formula for rivers and canals.",
    ]))

    write('minor-loss-head', build('minor-loss-head', [
        "Find the Head Loss from the Minor Loss Coefficient and Velocity",
        "Enter the minor loss coefficient K, velocity v and g to find the head loss.",
        "Minor Loss Head Calculator",
        "/ Minor Loss Head Calculator",
        "\U0001F4D6 View the \"Minor Head Loss Guide\"",
        "Loss coefficient K",
        "\U0001F4DA In-depth Analysis: Minor Head Loss",
        "Compute losses in bends and valves",
        "Pipe network design",
        "Pump head",
        "hL = K*v^2/(2*g). Example: a 90-degree bend with K=0.9 and v=2 m/s gives hL=0.9*4/19.62=0.183 m.",
        "How does it relate to friction loss?",
        "The friction loss is hf=f*L/D*v^2/(2g), and the minor losses are added on to give the total loss.",
        "Where does K come from?",
        "From tables for bends, valves and inlets; accumulated, they affect the pump head required.",
    ]))

    write('orifice-discharge', build('orifice-discharge', [
        "Free discharge through a thin-wall orifice.",
        "/ Orifice Discharge",
        "Orifice Discharge",
        "\U0001F4D6 View the \"Orifice Flow Guide\"",
        "Q = C_d A\u221a(2\u0394P/\u03c1). For gravity driven discharge \u0394P=\u03c1gh.",
        "Discharge coefficient C_d",
        "Orifice area A (m\u00b2)",
        "For gravity driven discharge \u0394P=\u03c1gh.",
        "\U0001F4DA In-depth Analysis: Orifice Flow",
        "Compute the discharge through a small orifice",
        "Emptying a tank",
        "Nozzles",
        "Q = Cd*A*sqrt(2*g*h). Example: with A=1 cm\u00b2, h=2 m and Cd=0.62, Q=0.62*1e-4*sqrt(39.24)=3.88e-4 m\u00b3/s=0.388 L/s.",
        "The discharge coefficient of a small thin-wall orifice is about 0.61-0.62.",
        "What about contraction?",
        "The jet contracts so that Ae is smaller than C*A, with Cd = Cc*Cv.",
    ]))

    write('pitot-velocity', build('pitot-velocity', [
        "Find the Velocity from the Dynamic Pressure Difference",
        "Enter the dynamic pressure difference \u0394P and the density \u03c1 to find the velocity.",
        "Pitot Tube Velocity Calculator",
        "/ Pitot Tube Velocity Calculator",
        "\U0001F4D6 View the \"Pitot Tube Guide\"",
        "Dynamic pressure difference \u0394P (Pa)",
        "\U0001F4DA In-depth Analysis: Pitot Tube",
        "Measuring velocity from a pressure difference",
        "Wind tunnels and airspeed",
        "v = sqrt(2*\u0394p/rho). Example: with \u0394p=6000 Pa and air rho=1.2, v=sqrt(12000/1.2)=100 m/s.",
        "What pressure does it measure?",
        "Total pressure minus static pressure equals the dynamic pressure, from which the velocity is derived.",
        "What are the applications?",
        "Aircraft airspeed tubes, wind tunnels and flue velocity measurement.",
    ]))

    write('poiseuille-flow', build('poiseuille-flow', [
        "Volume flow rate for laminar flow in a circular pipe.",
        "Poiseuille Flow Calculator",
        "/ Poiseuille Flow",
        "Poiseuille Flow",
        "\U0001F4D6 View the \"Poiseuille Flow Guide\"",
        "Q = \u03c0\u0394P r\u2074/(8\u03bcL). The flow is extremely sensitive to the radius, to the fourth power.",
        "The flow is extremely sensitive to the radius, to the fourth power.",
        "\U0001F4DA In-depth Analysis: Poiseuille Flow",
        "Compute the laminar flow rate in a circular pipe",
        "Microfluidics",
        "Blood vessels",
        "Q = pi*\u0394p*R^4/(8*mu*L). Example: with R=1 mm, L=1 m, \u0394p=1000 Pa and water mu=1e-3, Q=pi*1000*1e-12/(8e-3)=3.93e-7 m\u00b3/s.",
        "How does the radius matter?",
        "Q is proportional to R^4, so even a small increase in radius greatly increases the flow.",
        "What about laminar flow?",
        "It holds only while Re stays below about 2300; beyond that, use turbulent flow formulas.",
    ]))


if __name__ == '__main__':
    main()
