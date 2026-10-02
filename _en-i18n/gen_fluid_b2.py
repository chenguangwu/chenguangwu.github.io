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
    write('froude-number', build('froude-number', [
        "Find the Froude Number from Velocity and Characteristic Length",
        "Enter the velocity v, characteristic length L and g to find the Froude number.",
        "Froude Number Calculator",
        "/ Froude Number Calculator",
        "\U0001F4D6 View the \"Froude Number Guide\"",
        "Fr above 1 is supercritical flow and below 1 subcritical flow.",
        "\U0001F4DA In-depth Analysis: Froude Number",
        "Judging the flow regime in open channels",
        "Ship model testing",
        "Free surface flows",
        "Fr = v/sqrt(g*L). Example: with v=2 m/s and L=1 m, Fr=2/sqrt(9.81)=0.639; above 1 is supercritical and below 1 subcritical.",
        "What about critical flow?",
        "Fr=1 is critical, separating supercritical from subcritical flow and governing how surface waves travel.",
        "What about similarity in ship models?",
        "Fr must be kept the same to achieve gravity similarity.",
    ]))

    write('hydraulic-diameter', build('hydraulic-diameter', [
        "Find the Hydraulic Diameter from Flow Area and Wetted Perimeter",
        "Enter the flow area A and wetted perimeter P to find the hydraulic diameter.",
        "Hydraulic Diameter Calculator",
        "/ Hydraulic Diameter Calculator",
        "\U0001F4D6 View the \"Hydraulic Diameter Guide\"",
        "D_h = 4A/P, and for a circular pipe D_h=D. With A=0.01 and P=0.4 the result is 0.1 m.",
        "Wetted perimeter P (m)",
        "D_h = 4A/P, and for a circular pipe D_h=D.",
        "\U0001F4DA In-depth Analysis: Hydraulic Diameter",
        "Compute the equivalent diameter of a non-circular duct",
        "Rectangular ducts",
        "Dh = 4*A/P, where A is the cross-section and P the wetted perimeter. Example: a 0.2 by 0.1 m rectangle gives Dh=4*0.02/0.6=0.133 m.",
        "What about circular pipes?",
        "Dh=D, since 4*pi*D^2/4 divided by pi*D gives D.",
        "What is it used for?",
        "Dh replaces D in circular pipe theory when computing Re and the friction factor.",
    ]))

    write('hydrostatic-pressure', build('hydrostatic-pressure', [
        "Pressure produced inside a liquid by depth.",
        "Hydrostatic Pressure Calculator",
        "/ Hydrostatic Pressure",
        "Hydrostatic Pressure",
        "\U0001F4D6 View the \"Hydrostatic Pressure Guide\"",
        "P = \u03c1gh. A 10 m water column is about 98 kPa.",
        "A 10 m water column is about 98 kPa.",
        "\U0001F4DA In-depth Analysis: Hydrostatic Pressure",
        "Compute the pressure in a liquid",
        "Pressure on dams or tank bottoms",
        "Diving depth",
        "p = p0 + rho*g*h. Example: at a depth of 10 m of water, p=101325 + 1000*9.81*10 = 199425 Pa, a gauge pressure of about 98 kPa.",
        "Does the shape matter?",
        "It depends only on the depth and the density, not on the shape of the container, for a static liquid.",
        "What about direction?",
        "It is isotropic and acts perpendicular to the wall.",
    ]))

    write('index', build('index', [
        "\U0001F4A7 Fluid Mechanics Tools",
        "Fluid Mechanics",
        "Fluid Mechanics Tools",
        "Venturi Flow Meter Calculator",
        "Enter the inlet and throat areas A1 and A2, the pressure difference \u0394P and the fluid density \u03c1, and use the Venturi formula to find the volume flow rate, for selecting pipe flow meters and checking flow online.",
        "Stokes Settling Velocity Calculator",
        "Stokes settling velocity calculator: enter the particle radius, the density difference and the fluid viscosity to find the uniform terminal settling velocity of small particles at low Reynolds number, for suspension settling and water treatment design.",
        "Volume Flow Rate Calculator",
        "Volume flow rate calculator: enter the pipe cross-sectional area and the mean velocity and use Q = A\u00b7v to find the volume flow rate, for flow accounting in water supply, ventilation and chemical pipelines.",
        "Bernoulli pressure calculator: enter the fluid velocity, height and pressure and use the Bernoulli equation p + \u00bd\u03c1v\u00b2 + \u03c1gh = constant to find the pressure change along a streamline, for pressure analysis in pipes and aerofoils.",
        "Capillary Rise Height Calculator",
        "Capillary rise height calculator: enter the liquid surface tension, contact angle and capillary radius and use Jurin's law to find the rise height in a narrow tube, for analysing capillary action in soil, paper and microfluidics.",
        "Laplace Spherical Bubble Pressure Calculator",
        "Find the pressure difference across a spherical bubble from the surface tension and radius of curvature",
        "Pitot Tube Velocity Calculator",
        "Enter the dynamic pressure difference \u0394P measured with a Pitot tube and the fluid density \u03c1, and use v = \u221a(2\u0394P/\u03c1) to compute the flow velocity, for measuring actual flow in air or water ducts using a Pitot tube.",
        "Continuity equation calculator: enter the cross-sectional area and the velocity and use A\u2081v\u2081 = A\u2082v\u2082 to find the velocity change of an incompressible fluid in a pipe of varying section, for flow conservation and pipe diameter design.",
        "Hydrostatic Pressure Calculator",
        "Hydrostatic pressure calculator: enter the liquid density, depth and gravitational acceleration and use p = \u03c1gh to find the pressure produced by depth inside a liquid, for pressure design of tanks, dams and diving equipment.",
        "Stagnation Pressure Calculator",
        "Stagnation pressure calculator: enter the static pressure and the velocity and use p\u2080 = p + \u00bd\u03c1v\u00b2 to find the total pressure at a stagnation point, for Pitot tube velocimetry, intakes and wind tunnel pressure conversion.",
        "Orifice discharge calculator: enter the orifice area, head and discharge coefficient and use the thin-wall orifice free discharge formula to find the flow rate, for design checks on tanks, irrigation and discharge structures.",
        "Minor Loss Head Calculator",
        "Find the head loss from the minor loss coefficient and the velocity",
        "Manning Formula Velocity Calculator",
        "Manning formula velocity calculator: enter the hydraulic radius, bed slope and roughness coefficient and use the Manning formula to find the mean velocity and discharge of uniform open channel flow, for hydraulic design of rivers, drains and canals.",
        "Poiseuille Flow Calculator",
        "Poiseuille flow calculator: enter the pipe diameter, pressure difference and viscosity and use Poiseuille's law to find the laminar volume flow in a circular pipe, for laminar flow analysis in microfluidics, blood flow and lubrication systems.",
        "Cavitation Number Calculator",
        "Enter the local pressure p, saturation vapour pressure p_v, density \u03c1 and velocity v to find the cavitation number, judging the risk and operating condition of cavitation erosion in pumps, propellers and other hydraulic machinery.",
        "Darcy Pressure Drop Calculator",
        "Find the pipe pressure drop from the friction factor and the velocity",
        "Archimedes buoyancy calculator: enter the density and volume of the displaced fluid and use F = \u03c1gV to find the buoyant force on an object, for force analysis of ships, buoys and submerged bodies.",
        "Chezy Velocity Calculator",
        "Find the velocity from the Chezy coefficient, hydraulic radius and bed slope",
        "Froude Number Calculator",
        "Find the Froude number from the velocity and characteristic length",
        "Capillary Pressure Difference Calculator",
        "Find the capillary pressure difference from the surface tension and tube diameter",
        "Hydraulic Diameter Calculator",
        "Find the hydraulic diameter from the flow area and wetted perimeter",
        "Find the kinematic viscosity from the dynamic viscosity and density",
        "Weber Number Calculator",
        "Find the Weber number from the velocity, length scale and surface tension",
        "About \"Fluid Mechanics Tools\"",
        "The Fluid Mechanics tools collection gathers 23 free online tools covering the common calculations, conversions and lookups needed in fluid mechanics scenarios. Whether you are a practitioner in the field, a student or a casual user, you will find handy tools here that work the moment you open them. All tools run purely in the browser and no data is uploaded to a server, so your privacy stays safe.",
        "The fluid mechanics tools listed on this page include (a selection of representative tools):",
        "These tools help you finish common fluid mechanics tasks quickly, with no need to memorize complex formulas or convert values by hand \u2014 just enter them and get results.",
        "Do the fluid mechanics tools need to be downloaded or registered?",
        "No. Every fluid mechanics tool on this page is a pure front-end online tool \u2014 open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the fluid mechanics tools' results accurate? Is my data safe?",
        "The tools compute locally in your browser using public formulas and common industry standards, so results appear instantly. All calculations run on your own device and no data is uploaded to a server, keeping your privacy secure.",
    ]))

    write('kinematic-viscosity', build('kinematic-viscosity', [
        "Find the Kinematic Viscosity from Dynamic Viscosity and Density",
        "Enter the dynamic viscosity \u03bc and the density \u03c1 to find the kinematic viscosity.",
        "\U0001F4D6 View the \"Kinematic Viscosity Guide\"",
        "\u03bd = \u03bc/\u03c1. Water at 20 \u00b0C gives 1.0\u00d710\u207b\u2076 m\u00b2/s.",
        "Water at 20 \u00b0C gives 1.0\u00d710\u207b\u2076 m\u00b2/s.",
        "\U0001F4DA In-depth Analysis: Kinematic Viscosity",
        "Compute",
        "and select a fluid",
        "nu = mu/rho. Example: water at 20 \u2103 with mu=1.002e-3 Pa\u00b7s and rho=998 gives nu=1.004e-6 m\u00b2/s.",
        "How does it relate to dynamic viscosity?",
        "Dividing the dynamic viscosity mu, in Pa\u00b7s, by the density gives the kinematic viscosity nu in m\u00b2/s.",
        "What about temperature?",
        "For liquids nu falls as temperature rises, while for gases it rises.",
    ]))


if __name__ == '__main__':
    main()
