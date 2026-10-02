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
    write('wound-description', build('wound-description', [
        "\u2696\ufe0f Injury (Blunt or Sharp Force) Feature Descriptor",
        "Help identify blunt force and sharp force injuries from morphology and generate standardized injury descriptions",
        "\"Help identify blunt force and sharp force injuries from morphology and generate standardized injury descriptions\" is computed from the input parameters with professional calculations and outputs a result.",
        "/ Injury Feature Descriptor",
        "\U0001F4D6 Read the \"Guide to Describing Injury (Blunt / Sharp Force) Features\"",
        "Injury Type Selection",
        "Blunt Force Injury",
        "Sharp Force Injury",
        "Firearm Injury",
        "Stellate",
        "Linear",
        "Contusion (no rupture)",
        "Marginal Features",
        "Contusion zone / abrasion",
        "Tissue bridges",
        "Relatively neat",
        "Type of Weapon",
        "Flat object (brick, wooden board)",
        "Rod-like object (iron bar, wooden stick)",
        "Irregular stone",
        "Fist or foot",
        "Fall onto ground",
        "Type of Sharp Instrument",
        "Incision (kitchen knife, blade)",
        "Stab wound (dagger, needle)",
        "Chop wound (axe, cleaver)",
        "Cut wound",
        "Fusiform (spindle-shaped)",
        "Gaping (split open)",
        "Features of the Wound Corners",
        "Both sharp",
        "One sharp and one blunt",
        "Both blunt",
        "Type of Wound Opening",
        "Range of Fire",
        "Contact Shot",
        "Close range (under 30cm)",
        "Intermediate range (30cm to 1m)",
        "Long range (over 1m)",
        "Wound Length (cm)",
        "Wound Width (cm)",
        "Generate Description",
        "Copy Description",
        "Key Points Distinguishing Blunt from Sharp Force Injury",
        "Irregular, with a contusion zone",
        "Neat, with no obvious contusion",
        "Wound Corners",
        "Blunt and rounded, irregular",
        "Sharp and neat",
        "Wound Walls",
        "Rough, with tissue bridges",
        "Smooth, with no tissue bridges",
        "Wound Track",
        "Small opening with a large base (sac-like)",
        "Large opening with a small base (shallower)",
        "Bleeding",
        "Mild outside and severe inside, with much subcutaneous haemorrhage",
        "Bleeding obvious, with much external bleeding",
        "May leave weapon fragments",
        "Little foreign material",
        "Fracture",
        "Comminuted / depressed fractures common",
        "Chop wounds may cause fractures, which are relatively neat",
        "Main Types of Blunt Force Injury",
        "Epidermal abrasion",
        ": the dermis is exposed and can reflect the morphology of the weapon's contact surface",
        "Subcutaneous haemorrhage (contusion)",
        ": skin integrity is unbroken, and the colour changes over time (red \u2192 purple \u2192 green \u2192 yellow)",
        "Laceration",
        ": blunt force splits the full thickness of the skin with uneven margins and tissue bridges",
        ": direct external force causes fracture (comminuted, depressed), indirect force causes fracture at distant sites",
        "Main Types of Sharp Force Injury",
        "Incision",
        ": cut along the long axis, fusiform wound, sharp corners, heavy bleeding",
        "Chop wound",
        ": heavy force, the wound may reach bone, often with fracture",
        "Stab wound",
        ": small opening with a deep track, often injuring viscera and highly lethal",
        ": scissor or blade shearing can produce a \"V\" or linear wound",
        "\u26a0\ufe0f This tool is for forensic teaching and descriptive reference only. Real assessment must combine full examination and laboratory findings.",
        "\U0001F4DA In-Depth Analysis: Describing Injury (Blunt / Sharp Force) Features",
        "Distinguishing Blunt from Sharp Force Injury",
        "Generating Standardized Injury Description Text",
        "Indirect Inference of Weapon Morphology",
        "By morphology: epidermal abrasion (boundary), laceration (blunt margins, blunt corners, tissue bridges), incision (neat margins, sharp corners), chop wound (deep to bone, deep isthmus). Combine with site and size (length \u00d7 width) to generate a standardized record.",
        "A 5\u00d71cm epidermal abrasion on the head with a regular boundary and parallel surface grooves indicates a blunt-force abrasion such as from a rod being dragged; in the same area a fusiform wound with blunt corners and tissue bridges in the centre indicates a laceration, supporting a blunt blow rather than a blade cut.",
        "Do blunt corners rule out a knife wound?",
        "They mostly indicate a blunt-force laceration. Incisions and chop wounds from blades have sharp corners and few tissue bridges, but repeated cutting with a thin blade or contact with bone can blunt them, so the wound walls and bridges must be judged together.",
        "What is the value of standardized description?",
        "Unified terminology improves document quality, peer review and database comparison, reduces the ambiguity of subjective words such as \"large wound\", and helps reconstruct the injury mechanism.",
        "About \"Injury Feature Descriptor\"",
        "Help identify blunt force, sharp force and firearm injuries from morphology features and generate a standardized forensic injury description report.",
        "Supports blunt force, sharp force and firearm injury categories",
        "Configurable morphology parameters",
        "Automatic standardized description generation",
        "Includes a comparison table of distinguishing points",
        "Aid to case injury analysis",
        "Reference for writing forensic assessment reports",
        "About \"Injury (Blunt or Sharp Force) Feature Descriptor\"",
        "Injury (Blunt or Sharp Force) Feature Descriptor - compares the morphological features of blunt and sharp force injuries and supports injury type identification and description. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()