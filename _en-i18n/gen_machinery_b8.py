#!/usr/bin/env python3
# machinery batch8 (index)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'machinery')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'machinery')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'index': [
"⚙️ Mechanical Manufacturing Tools",
"Mechanical Manufacturing",
"Mechanical Manufacturing Tools",
"Enter the number of teeth, module, pressure angle and root form to compute the pitch circle, major diameter, minor diameter and base circle of an involute spline",
"Select a mechanism type such as a four-bar, cam or gear and enter the geometric parameters to compute kinematic characteristics like displacement and velocity together with key dimensions, aiding theory-of-machines courses and mechanism design.",
"Casting Pouring Weight and Solidification Time",
"The belt drive calculator handles open belt drives, computing geometric parameters (center distance, wrap angle) and mechanical parameters (tension, power), suitable for belt drive selection in mechanical transmission design.",
"Vibration Isolation",
"Enter the mass, spring stiffness and excitation frequency to compute the system's natural frequency, frequency ratio, transmissibility and isolation efficiency",
"Enter the module, tooth count and other parameters of a standard spur or helical cylindrical gear to compute the pitch diameter, center distance and other basic parameters per GB/T 1356, used in gear drive design.",
"Enter the weld type (fillet, butt, spot) together with the geometry, weld leg and other parameters to compute the weld load capacity and allowable load, for the strength verification of welded structures.",
"Enter the basic size and upper/lower deviations of the hole and shaft to automatically determine the fit type (clearance, transition, interference) and compute the fit clearance or interference, used in mechanical assembly tolerance design.",
"Enter the circular shaft diameter, loads and material parameters to compute the combined stress and safety factor of a solid circular shaft using the fourth strength theory, assessing its strength and fatigue reliability under torsion and bending.",
"Select the gear type (spur, helical, bevel) and enter the module, tooth count and other parameters to compute the pitch circle, addendum circle and other geometry, aiding gear design and selection.",
"Enter the module, number of teeth and pressure angle to compute the pitch circle, addendum circle, dedendum circle and base circle of a standard spur cylindrical gear",
"Enter the friction-disc dimensions, friction coefficient, spring force, number of friction surfaces and speed to compute the clutch's transmitted torque and power",
"Enter the rivet diameter, plate thickness, rivet count, plate width and load to check the shear, crushing and tearing strength and compute the riveted joint efficiency",
"Select the cylindrical helical spring type (compression, extension, torsion) and enter the wire diameter, mean diameter and number of coils to compute the stiffness, deflection and strength and verify them, used in spring design.",
"Enter the basic size and fit designation (e.g. H7/g6) to compute the hole and shaft limit deviations and the fit clearance/interference",
"The pin (locating/connecting) size tool computes the key dimensions and fit tolerance of locating or connecting pins from the input parameters, suitable for pin selection and verification in mechanical assembly design.",
"The intelligent, unmanned and high-efficiency comparison calculator takes the parameters of an R&D scheme and quantitatively compares the metric differences between the intelligent, unmanned and high-efficiency routes, aiding innovation R&D decisions.",
"Enter the transmitted power, small-sprocket speed and tooth count to compute the recommended chain pitch, chain speed and circumferential force and check the static and fatigue strength of the roller chain, aiding drive selection design.",
"The part mass and center-of-gravity estimation tool computes the mass of a single part and estimates the combined center of gravity of a multi-part assembly, suitable for structural design, counterweighting and balancing analysis.",
"Sheet-Metal Bend Unfolding",
"Enter the sheet thickness, bend angle, inside bend radius and K-factor to compute the bend allowance, bend deduction and unfolded length",
"Select the steel grade and heat-treatment process (such as tempering) to estimate the resulting hardness (HRC) from empirical relations, providing a reference for heat-treatment planning and quality prediction.",
"The casting draft-angle design tool computes the casting draft angle and size compensation from the input parameters, avoiding release difficulty and dimensional deviation, suitable for casting process design and mould release schemes.",
"⏱️ Rolling Bearing Rated Life L10 Estimation",
"The reliability analysis tool assesses the life, failure rate and maintenance strategy of mechanical parts or systems, giving reference data based on standard engineering models, suitable for equipment O&M and life prediction.",
"Enter the thread outer diameter and pitch (or TPI) to automatically match and identify the corresponding standard thread specification (metric, unified), used for thread part identification, repair and procurement.",
"Enter the basic dynamic load rating C, equivalent dynamic load P and speed n to compute the L10 basic rating life (in million revolutions and hours)",
"Bearing Selection",
"Enter the load, shaft diameter, width-to-diameter ratio, speed and required life to compute the pV value and recommend the bearing type and required dynamic load rating",
"Enter the coating area, dry film thickness, volume solids and transfer efficiency to compute the theoretical and actual paint usage",
"Enter the thread mean diameter, lead, axial load and friction coefficient to compute the drive efficiency and driving torque and determine the self-locking condition",
"Enter the moment of inertia, the speeds before and after braking and the braking time to compute the required braking torque, total braking energy and average braking power, for energy assessment of motor and mechanical braking systems.",
"The worm drive efficiency and self-locking verification tool computes the efficiency of a worm gear drive and judges whether the self-locking condition is met, suitable for the safety verification of transmission schemes in reducer and hoisting-equipment design.",
"Enter the shaft diameter, key width and height, transmitted torque and material allowable stress to check whether the crushing and shear stresses of a parallel key joint are safe and give a strength pass/fail judgement.",
"Geometric Tolerance Marking",
"Per GB/T 1184 Annex B, select the tolerance type, nominal size and tolerance grade to look up the geometric tolerance value",
"Spring Design",
"Enter the wire diameter, mean diameter, number of active coils and material to compute the spring stiffness, maximum deflection, shear stress and natural frequency",
"Enter the bearing diameter, length, speed, load and operating conditions to compute the contact pressure, PV value and required oil quantity, and recommend a lubrication method",
'About "Mechanical Manufacturing Tools"',
"The Mechanical Manufacturing Tools collection includes 35 free online tools covering common calculation, conversion and lookup needs in mechanical manufacturing scenarios. Whether you are a practitioner, student or casual user, you will find practical, ready-to-use tools here. All tools run entirely on the client side, with no data uploaded to a server, protecting your privacy.",
"The mechanical manufacturing tools on this page include (selected representative tools):",
"These tools help you quickly complete common mechanical-manufacturing tasks, with no need to memorise complex formulas or convert by hand: just enter the values to get results.",
"Do the mechanical manufacturing tools require downloading or registration?",
"No. All the mechanical manufacturing tools on this page are pure client-side online tools: just open the page and use them, with no software to install, no account to register and no data uploaded.",
"Are the results of the mechanical manufacturing tools accurate? Is my data safe?",
"The tools compute locally in your browser based on public mathematical formulas and general industry standards, giving instant results. All computations are done locally on your device, data is not uploaded to a server, and your privacy is protected.",
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
