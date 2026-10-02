#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'astronomy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'astronomy')
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
    out = {'slug': slug, 'industry': 'astronomy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('crater-estimator', build('crater-estimator', [
        "🔮 Meteorite Impact Crater Diameter Estimator",
        "Enter meteorite parameters to estimate the impact kinetic energy, TNT equivalent, crater diameter, depth and damage radius based on the Schmidt-Holsapple scaling law. All calculations are performed locally in the browser.",
        "Core formulas (by input variable): 1.161 x (rho_i/rho_t)^(1/3) x (D)^0.78 x (v)^0.44; 0.67 x log10(E) - 5.87; rho_i x (pi/6) x D x D x D",
        "Meteorite impact crater estimator",
        "📖 View the usage guide for the Meteorite Impact Crater Diameter Estimator",
        "Meteorite diameter D (m)",
        "Meteorite density rho",
        "Impact velocity v (km/s)",
        "Incidence angle theta (degrees, 1-90)",
        "Surface material rho",
        "Crystalline rock (2700)",
        "Sedimentary rock (2400)",
        "Loose sediment (1800)",
        "Water / ocean (1000)",
        "Ice (917)",
        "🌲 Tunguska event",
        "🌑 Barringer crater",
        "🔮 Chicxulub",
        "📊 Crater diameter comparison",
        "The current estimate (purple) compared with the final diameters of known terrestrial impact craters (logarithmic bars, for easy reading across orders of magnitude).",
        "Data source: public geological records. Chicxulub, Sudbury, Vredefort and others are giant basin structures whose actual diameters are given as interval estimates in the literature; the commonly used values are taken here.",
        "📐 Formulas and notes",
        "1. Meteorite mass and kinetic energy",
        "2. TNT equivalent",
        "1 megaton (Mt) TNT = 4.184 x 10^15 J",
        "3. Transient crater diameter (Schmidt-Holsapple pi scaling, gravity-dominated regime)",
        "4. Final crater diameter and depth (morphology correction)",
        "Simple crater (D",
        ", depth about 0.25 x D",
        "Complex crater (D",
        ", depth about 0.08 x D",
        "5. Blast damage radius (Y is the TNT equivalent in Mt)",
        "Severe (20 psi) about 0.9 x Y^(1/3)",
        ", moderate (5 psi) about 2.3 x Y^(1/3)",
        ", light (1 psi) about 6.0 x Y^(1/3)",
        "Model assumptions and limitations:",
        "Gravity g is taken as the Earth constant 9.81 m/s2, applicable to vertical or oblique impacts on the Earth's surface.",
        "The pi scaling applies to gravity-dominated medium and large impacts; for very large basins (such as Chicxulub) the actual diameter is often larger than the simplified estimate because of ring or multi-ring structural evolution.",
        "The damage radius is based on airburst or surface blast wave scaling and does not include thermal radiation, ejecta or global dust effects.",
        "The Tunguska event was a high-altitude airburst that formed no crater; the crater diameter shown by the tool is an equivalent estimate for a hypothetical ground impact.",
        "📚 Deep dive: Meteorite Impact Crater Diameter Estimator",
        "Estimate the impact kinetic energy, TNT equivalent and crater size from the diameter, density, velocity and incidence angle of an incoming meteorite.",
        "In popular science or disaster-prevention education, compare the damage scope (local, regional or global) of impacts by bodies of different sizes.",
        "Combine the gravity and crust parameters of the target body (Earth, Moon, Mars) to compare impacts across different bodies.",
        "Example: a meteorite 100 m in diameter with a density of 3000 kg/m3 and a velocity of 20 km/s",
        "Mass m = 4/3 x pi x r^3 x rho, about 4/3 x pi x 50^3 x 3000, about 1.57 x 10^9 kg; kinetic energy E = 1/2 m v^2, about 1/2 x 1.57 x 10^9 x (2 x 10^4)^2, about 3.1 x 10^17 J, about 75 megatons of TNT. On this basis the Schmidt-Holsapple scaling gives a crater diameter on the order of several hundred metres.",
        "Why is the crater much larger than the meteorite?",
        "The impact energy is far greater than the meteorite's own chemical energy; it comes mainly from the high-speed kinetic energy converted into a shock wave and excavation, so the crater diameter can reach several to tens of times the meteorite diameter.",
        "Does the incidence angle matter much?",
        "A vertical impact concentrates the energy most; at a large incidence angle (grazing) the effective energy and the crater shape change, with a flatter and more elongated damage zone but smaller peak compression.",
        "The estimates are based on empirical scaling laws and are order-of-magnitude estimates, for reference and popular science only",
        "The actual crater morphology is affected by many factors such as the target rock, porosity, incidence angle and weathering",
        "About the Meteorite Impact Crater Diameter Estimator",
        "The Meteorite Impact Crater Diameter Estimator is an online tool for astronomy enthusiasts and popular science education. Enter the meteorite diameter, density, impact velocity and incidence angle, and it estimates the impact kinetic energy, TNT equivalent, transient and final crater diameter, crater depth, blast damage radius and equivalent earthquake magnitude based on the Schmidt-Holsapple scaling law, and compares them intuitively with classic impact events such as Tunguska, Barringer and Chicxulub. Pure front-end calculation; data is not uploaded.",
        "Uses the Schmidt-Holsapple pi scaling law",
        "Automatically distinguishes simple and complex crater morphology corrections",
        "Kinetic energy, TNT equivalent, crater diameter, crater depth and damage radius calculated in one click",
        "Built-in classic scenarios: Tunguska, Barringer and Chicxulub",
        "Visual comparison with known terrestrial crater diameters",
        "Real-time calculation, with dark mode and mobile support",
        "Popular science teaching in astronomy and planetary science",
        "Science fiction writing and modeling of real impact events",
        "Help with student physics and astronomy assignments",
        "Order-of-magnitude assessment of meteorite impact risk",
        "Reference for geological heritage and impact structure research",
        "Satisfying curiosity about the dinosaur-killer asteroid",
    ]))

    write('earth-curvature', build('earth-curvature', [
        "🧮 Earth Curvature Visible Distance Calculator",
        "Enter the observer height and the target distance or height to calculate the visible horizon distance, the Earth curvature drop and the hidden height of the target, and draw a curvature diagram.",
        "Core formulas (by input variable): ((d - horizon) x (d - horizon)) / (2 x R) x 1000; (d x d) / (2 x R) x 1000; coeff x sqrt(h1)",
        "Earth curvature calculator",
        "📖 View the usage guide for the Earth Curvature Visible Distance Calculator",
        "Observer height (m)",
        "Target distance (km)",
        "Target height (m, optional)",
        "Consider atmospheric refraction (standard refraction, coefficient 3.86)",
        "Standing, 1.7 m",
        "10th floor, about 30 m",
        "100 m tower",
        "Mountain top, 500 m",
        "Aircraft, 10 km",
        "Observer",
        "Horizon",
        "Visible part of the target",
        "Hidden part",
        "Line of sight",
        "Earth surface",
        "The vertical scale of the diagram is exaggerated for visibility; it is an intuitive reference only and not to true scale.",
        "Horizon distance (visible distance)",
        "Geometric:",
        "km (h is the observer height in metres)",
        "With atmospheric refraction:",
        "Earth curvature drop (at a distance d from the observer)",
        "Drop = d^2 / (2R)",
        ", R = 6371 km (mean Earth radius), d in km, result converted to metres",
        "Hidden height of the target",
        "When the target distance exceeds the horizon:",
        "Hidden height = (d - d_horizon)^2 / (2R)",
        "Visible height of the target = target height - hidden height (not less than 0)",
        "Note: atmospheric refraction increases the horizon distance by about 8%. When refraction is enabled this tool corrects only the horizon distance; the curvature drop is still calculated with the geometric radius R = 6371 km.",
        "Visible distance standing at 1.7 m (km)",
        "Visible distance from a 100 m tower (km)",
        "Drop at 10 km (m)",
        "Mean Earth radius (km)",
        "📚 Deep dive: Earth Curvature Visible Distance Calculator",
        "Judge whether a distant landmark, ship or building is hidden by the curve of the Earth, and estimate the farthest visible horizon.",
        "In siting for wireless communication, radar or observation decks, assess the line-of-sight distance of an antenna or observation point.",
        "Demonstrate intuitively that the higher you stand, the farther you see: compare the sight distance at different observation heights.",
        "Example: horizon distance at an eye height of 1.7 m",
        "Taking the Earth radius R as about 6371 km, the sight distance d is about sqrt(2Rh) = sqrt(2 x 6371000 x 1.7) = sqrt(21661400), about 4653 m, about 4.65 km. Standing on a 100 m building, d is about sqrt(2 x 6371000 x 100), about 35700 m, about 35.7 km.",
        "Why is the horizon actually seen farther away?",
        "Atmospheric refraction",
        "bends light from distant objects slightly, equivalent to reducing the Earth radius to about 4/3 R, making the sight distance about 8% greater than the purely geometric value.",
        "How is the part of two targets that hides each other calculated?",
        "Calculate the horizon distance for the observation height at each end, add them and compare with the actual separation; if terrain in between rises above the connecting line of sight, the target is hidden.",
        "The formula approximates the Earth as an ideal sphere (R = 6371 km) and does not account for terrain relief or altitude differences",
        "The atmospheric refraction coefficient takes the standard value (an equivalent radius of about 7/6); in reality it fluctuates with air temperature, pressure and humidity",
        "The results are for reference only; rely on the actual application scenario and on professional measurement",
        "About the Earth Curvature Visible Distance Calculator",
        "The Earth Curvature Visible Distance Calculator is an online astronomy and geography tool that calculates the visible horizon distance for an observer at a given height, the Earth curvature drop at a given distance, and the height of a distant target hidden by the Earth's curvature. It includes a built-in Canvas curvature diagram that intuitively shows the geometric relationship between observer, horizon and target, and supports standard atmospheric refraction correction.",
        "Dual geometric and refraction modes for the horizon distance",
        "Real-time calculation of the Earth curvature drop",
        "Analysis of the target's hidden height and visible height",
        "Automatic drawing of the Canvas curvature diagram",
        "Real-time calculation, updating as you type",
        "Estimating visibility range for navigation and aviation",
        "Assessing the visible range of high observation decks",
        "Long-distance photography and signal tower coverage planning",
        "Geography and astronomy teaching demonstrations",
        "Verifying horizon-related phenomena",
        "Calculating the field of view when hiking and climbing",
        "Earth curvature diagram",
    ]))

    write('gravitational-force', build('gravitational-force', [
        "Gravitation (F = G x m1 x m2 / r^2)",
        "The universal gravitation between two point masses.",
        "Universal gravitation calculator",
        "/ Universal gravitation",
        "Universal gravitation",
        "📖 View the usage guide for Gravitation (F = G x m1 x m2 / r^2)",
        "F = G x m1 x m2 / r^2; the Earth-Moon gravitational force is about 1.98 x 10^20 N.",
        "📚 Deep dive: gravitation (F = G x m1 x m2 / r^2)",
        "Calculate the magnitude of the interaction force from the masses of two bodies and their separation using Newton's law of universal gravitation.",
        "Compare the decay of gravitation at short and long distances to understand the effect of the inverse-square law on celestial orbits.",
        "In classroom demonstrations, convert the gravitation of macroscopic bodies into force values that can be felt in daily life.",
        "Example: the gravitation between two 1 kg objects 1 m apart",
        "F = G x m1 x m2 / r^2 = 6.674 x 10^-11 x 1 x 1 / 1^2, about 6.67 x 10^-11 N, extremely weak. If instead the Earth and a 1 kg object close to the surface are used, with m2 = 5.97 x 10^24 and r = 6.37 x 10^6, then F is about 9.8 N (that is, the weight of about 1 kg).",
        "Why is gravitation called an inverse-square law?",
        "The magnitude of the force is inversely proportional to the square of the distance, so doubling the distance reduces the force to a quarter. This is the core law behind the stability of celestial orbits.",
        "What is G, and why is it so small?",
        "G is the gravitational constant. Its extremely small value means that at everyday scales gravity is far weaker than the electromagnetic force and becomes significant only at the mass scale of celestial bodies.",
    ]))

    write('horizon-distance', build('horizon-distance', [
        "Horizon Line-of-Sight Distance Calculator",
        "The horizon distance visible from the observer's eye height h (ignoring atmospheric refraction).",
        "/ Horizon distance",
        "Horizon distance",
        "📖 View the usage guide for the Horizon Line-of-Sight Distance Calculator",
        "Horizon distance approximation: d = sqrt(2 x R x h), where R is the Earth radius of 6371 km and h is the observer's altitude. The formula is derived from the Pythagorean theorem as an approximation for small h/R. The horizon dip angle is about acos(R/(R+h)). The actual visible distance is also affected by atmospheric refraction and is usually slightly farther than the geometric value.",
        "Eye height (m)",
        "d = sqrt(2Rh); at an eye height of 1.7 m the horizon is seen about 4.65 km away.",
        "📚 Deep dive: Horizon Line-of-Sight Distance Calculator",
        "When estimating visibility for navigation, sightseeing or radio and television coverage, quickly obtain the farthest visible horizon distance from the eye height.",
        "Compare the sight distance at ground level with that from a height such as a mountain top or a tall building.",
        "At the seaside, judge whether a distant ship or island is still within sight.",
        "Example: horizon distance at an eye height of 2 m",
        "Using the geometric approximation d about 3.57 x sqrt(h) (d in km, h in m), at h = 2, d is about 3.57 x 1.414, about 5.05 km. At an eye height of 50 m, d is about 3.57 x 7.07, about 25.2 km.",
        "How does this formula differ from the",
        "Earth curvature calculator",
        "?",
        "They are essentially the same in origin: d about sqrt(2Rh) simplifies to about 3.57 sqrt(h) (km/m), and this tool focuses on the sight distance of a single observer.",
        "Does the result change when",
        "atmospheric refraction",
        "is taken into account?",
        "Yes. Refraction increases the effective sight distance by about 8%, and in engineering a coefficient of 3.86 is often used instead of 3.57 as a conservative correction.",
    ]))

    write('hubble-redshift-distance', build('hubble-redshift-distance', [
        "Approximate distance (d = c x z / H0)",
        "At low redshift the recession velocity is linearly related to the distance.",
        "Hubble redshift distance calculator",
        "/ Hubble redshift distance",
        "Hubble redshift distance",
        "📖 View the usage guide for Approximate distance (d = c x z / H0)",
        "Redshift z",
        "d about c x z / H0 (low-redshift approximation); H0 = 70 km/s/Mpc.",
        "At z = 0.01 it is about 42.8 Mpc.",
        "📚 Deep dive: approximate distance (d = c x z / H0)",
        "For low-redshift galaxies, use Hubble's law d = c x z / H0 for a rough distance estimate, suitable for an introduction to cosmology.",
        "From the measured redshift z and the Hubble constant H0, estimate the recession velocity and distance of a galaxy.",
        "In popular science, show intuitively the expanding-universe relation that the greater the redshift, the farther away the object is.",
        "Example: the distance of a galaxy at redshift z = 0.01",
        "Taking c = 3 x 10^5 km/s and H0 about 70 km/s/Mpc, d = c x z / H0 = 3 x 10^5 x 0.01 / 70, about 42.9 Mpc, about 140 million light-years. Its recession velocity v is about cz, about 3000 km/s.",
        "Up to what redshift is this formula suitable?",
        "It is only suitable at low redshift (z much less than 1). At high redshift the expansion history of the universe and dark energy must be considered, using the full cosmological distance integral.",
        "Does the choice of the Hubble constant H0 matter much?",
        "Very much. Current measurements of H0 disagree between about 70 and 73 km/s/Mpc, which changes the distance estimates proportionally.",
    ]))


if __name__ == '__main__':
    main()
