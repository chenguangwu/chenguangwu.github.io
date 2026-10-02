#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'forensic-medicine')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'forensic-medicine')
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
    out = {'slug': slug, 'industry': 'forensic-medicine', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('bloodstain-pattern', build('bloodstain-pattern', [
        "\u2696\ufe0f Bloodstain Morphology (Drip and Spatter) Interpreter",
        "Infer the impact angle, source location and wounding mechanism from bloodstain morphology",
        "\"Infer the impact angle, source location and wounding mechanism from bloodstain morphology\" is computed from the input parameters with professional calculations and outputs a result.",
        "/ Bloodstain Morphology Interpreter",
        "\U0001F4D6 Read the \"Guide to Interpreting Impact Angles from Bloodstain Morphology (Drip / Spatter)\"",
        "Impact Angle Calculation",
        "Blood Source Location",
        "Bloodstain Morphology Recognition",
        "Measure the major and minor axes of a single spatter stain to compute the angle at which blood struck the surface",
        "Bloodstain Major Axis L (mm)",
        "Bloodstain Minor Axis W (mm)",
        "Calculate Angle",
        "The red line represents the angle between the blood flight direction and the surface",
        "Impact angle \u03b1 = arcsin(W / L)",
        "where W is the minor axis width and L is the major axis length of the stain",
        "90\u00b0: blood strikes vertically and the stain is round (L\u2248W)",
        "45\u00b0: the stain is a typical ellipse",
        "under 30\u00b0: the stain is elongated and the tail points toward the blood source",
        "Spatial Location of the Blood Source (Convergence Point Calculation)",
        "Enter the position and direction angle of two or three stains to compute the 2D coordinates of the blood source",
        "Stain A - X coordinate (cm)",
        "Stain A - Y coordinate (cm)",
        "Stain A - direction angle (\u00b0)",
        "Stain B - X coordinate (cm)",
        "Stain B - Y coordinate (cm)",
        "Stain B - direction angle (\u00b0)",
        "Stain A - impact angle (\u00b0)",
        "Stain B - impact angle (\u00b0)",
        "Height of the Stain Above the Ground (cm)",
        "Calculate Blood Source",
        "Convergence Point Calculation Method",
        "2D Area of Convergence",
        ": extend the major axis directions of several stains backwards and their intersection is the projection of the blood source onto the surface.",
        "3D Area of Origin",
        ": compute the height of the blood source from the impact angle and the distance from the stain to the convergence point: H = D \u00d7 tan(\u03b1), where D is the distance from the stain to the convergence point and \u03b1 is the impact angle.",
        "Bloodstain Morphology Classification",
        "Select the type that best matches the observed features; the system provides the formation mechanism and forensic meaning",
        "\u26a0\ufe0f Bloodstain pattern analysis (BPA) requires professional training and rich experience. This tool is for teaching reference only; actual case analysis should be done by a professional bloodstain pattern analyst.",
        "Quick Reference for Bloodstain Morphology Classification",
        "Passive / Gravity Stains",
        "Drip stain",
        ": blood drips vertically from a wound, round, with jagged edges that become more obvious with height",
        "Flow stain",
        ": blood flows along a surface, forming a stream under gravity",
        "Pool of blood",
        ": a large accumulation of blood, indicating the source was at that position for a period",
        "Transfer stain",
        ": a pattern left by a bloodied object contacting a surface (handprint, shoeprint, weapon print)",
        "Spatter Stains (Classified by Size)",
        "Formation Mechanism",
        "Low-velocity spatter",
        "Low-energy events (walking drips, nosebleed)",
        "Medium-velocity spatter",
        "Medium energy (blunt blows, punching)",
        "High-velocity spatter",
        "High energy (gunshots, explosions, high-speed machinery)",
        "Characteristic Bloodstains",
        "Backspatter",
        ": small spatter near a gunshot entry wound, where blood is forced backwards by the pressure of the projectile entering",
        "Forward spatter",
        ": spatter in the direction of a gunshot exit wound, usually covering a wider area than backspatter",
        "Cast-off",
        ": blood is flung when a bloodied weapon is swung, distributing in linear or arc patterns",
        "Exhaled or coughed blood",
        ": blood breathed or coughed out mixed with air bubbles, indicating respiratory tract bleeding",
        "Splash or cast-off from a pool",
        ": blood splashes after falling into a pool, with secondary splash forming satellite patterns",
        "Wipe stain",
        ": a clean object wiping a bloodied surface, or a bloodied object wiping a clean surface",
        "Determine the location and sequence of events",
        "Infer the weapon and number of blows",
        "Judge the relative positions of victim and assailant",
        "Confirm or refute witness statements",
        "Judge whether the body was moved after the blows",
        "Assess the relationship between blood loss and time of death",
        "\U0001F4DA In-Depth Analysis: Interpreting Impact Angles from Bloodstain Morphology (Drip / Spatter)",
        "Computing the Impact Angle of a Single Spatter Stain",
        "Reconstructing the Rough Location of the Blood Source",
        "Inferring the Direction of the Wounding Action (Spatter / Swing)",
        "Using the impact angle \u03b1 = arcsin(W/L) (W minor axis, L major axis, in mm), the smaller the ratio W/L the steeper the angle; combine the lines through multiple stains (the chord method) to trace back to the blood source and the spatter direction.",
        "For a single spatter stain with major axis L = 10 mm and minor axis W = 6 mm: W/L = 0.6, so \u03b1 = arcsin(0.6) = 36.9\u00b0. This is a medium-angle spatter; combining the lines of adjacent stains roughly locates the blood source and indicates the direction of force.",
        "What does a larger angle mean?",
        "\u03b1 near 90\u00b0 means the drop struck nearly vertically (as in dripping), while near 0\u00b0 means it travelled nearly parallel to the surface (as in high-velocity spatter or cast-off), which distinguishes dripping from spatter morphology.",
        "Is the chord method accurate for tracing position?",
        "It is a geometric approximation affected by gravitational drop and surface irregularity. Cross-check with multiple stains and combine with scene photographs and 3D reconstruction.",
        "About \"Bloodstain Morphology Interpreter\"",
        "Based on bloodstain pattern analysis (BPA) principles, this forensic tool assists in inferring the location, angle and wounding mechanism of bleeding events at a scene through impact angle calculation, blood source localization and morphology classification.",
        "Impact angle calculation (arcsin(W/L) formula with visualisation)",
        "2D location via two-stain convergence point",
        "3D blood source height calculation (D\u00d7tan(\u03b1))",
        "Recognition of 11 bloodstain morphology types",
        "Includes grading references for passive, medium-velocity and high-velocity stains",
        "Bloodstain morphology analysis at homicide scenes",
        "Scene reconstruction",
        "Forensic bloodstain morphology teaching",
        "Supporting analysis of evidence in judicial appraisal",
        "About \"Bloodstain Morphology (Drip and Spatter) Interpreter\"",
        "Bloodstain Morphology (Drip and Spatter) Interpreter - infers the blood source location, spatter angle and wounding mechanism from bloodstain morphology; a forensic aid for bloodstain pattern analysis. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()