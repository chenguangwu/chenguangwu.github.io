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
    write('fall-injury', build('fall-injury', [
        "\U0001F4CA Fall from Height (Injury Distribution) Gravity Analyzer",
        "Analyse the injury distribution of a fall from height to help infer the fall height and landing posture",
        "\"Analyse the injury distribution of a fall from height to help infer the fall height and landing posture\" is computed from the input parameters with professional calculations and outputs a result.",
        "/ Fall from Height Analyzer",
        "\U0001F4D6 Read the \"Guide to Fall from Height Injury Distribution and Mechanism Analysis\"",
        "Fall Parameters",
        "Estimated Fall Height (m)",
        "Landing Posture",
        "Head first",
        "Feet first",
        "Buttocks first",
        "Landing on the side",
        "Back first",
        "Landing Surface",
        "Concrete / asphalt (hard surface)",
        "Soil / grass (soft surface)",
        "Water",
        "Body Weight (kg)",
        "Age of the Deceased",
        "Injury Features (tick all that apply)",
        "Features of Fall-from-height Injury",
        "General Features of Fall-from-height Injury",
        "Mild outside, severe inside",
        "external surface injury is relatively mild while internal injury is severe (skin intact but viscera ruptured)",
        "Widespread injury",
        "injuries at many sites across the body, often involving multiple systems",
        "Fractures common",
        "skull, spine, pelvis and limb fractures",
        "Impact injury plus countercoup injury",
        "impact injury at the landing site with a countercoup injury on the opposite side (for example occipital landing leading to frontal-temporal countercoup injury)",
        "Consistent injury direction",
        "the injury distribution matches the direction of the fall and can be used to infer the landing posture",
        "Injury Characteristics of Different Landing Postures",
        "Head Landing",
        "skull fracture (mostly ring / depressed), skull base fracture, cerebral contusion and laceration (impact point plus countercoup), cervical fracture and dislocation",
        "Feet Landing",
        "calcaneal or talar fracture, tibia and fibula fracture, acetabular fracture, pelvic fracture, spinal compression fracture (transmitted injury)",
        "Buttocks Landing",
        "pelvic fracture, sacral fracture, lumbar compression fracture, visceral rupture (liver and spleen rupture)",
        "rib fracture (mostly flail chest), pulmonary contusion, liver or spleen rupture (depending on the landing side)",
        "Fall Height and Injury Severity",
        "Fall Height",
        "Impact Speed",
        "Common Injury",
        "Risk of Death",
        "Minor fracture and contusion",
        "Limb fracture, minor visceral injury",
        "Severe fracture, visceral rupture, craniocerebral injury",
        "Widespread whole-body injury, multiple fractures",
        "Lethal injury, body truncation",
        "almost 100%",
        "Note: impact speed v = \u221a(2gh), g = 9.8 m/s\u00b2. Actual injury severity is affected by body weight, landing posture, ground hardness and buffering by airborne obstacles.",
        "Key Points for Assessing Death from Fall from Height",
        "Scene investigation",
        ": the point of origin (window, balcony or cliff), the fall path and the landing point",
        "Origin traces",
        ": climbing marks, struggle marks and shoeprints (to judge accidental fall or being pushed)",
        "Injury distribution",
        ": whether it fits a single fall from height (force in one direction only)",
        "Excluding other causes of death",
        ": whether other fatal injuries are present (stab wounds, gunshot wounds and so on)",
        "Toxicology testing",
        ": to exclude a body thrown after poisoning",
        "Injury timing",
        ": confirm the injuries are antemortem (with vital reaction)",
        "\u26a0\ufe0f This tool is for forensic pathology teaching reference only. Real assessment must combine scene investigation and a full autopsy.",
        "\U0001F4DA In-Depth Analysis: Fall from Height Injury Distribution and Mechanism Analysis",
        "Reconstructing Fall Height and Landing Posture",
        "Explaining the Mild-outside/Severe-inside Mechanism",
        "Distinguishing Fall from Height from Homicide by Throwing",
        "Quantify the landing energy with the impact speed v = \u221a(2gh) and kinetic energy E = \u00bdmv\u00b2/1000 (kJ); combine with the landing site (feet, buttocks, head, upper limbs) to analyse fracture types and visceral distribution, and use the \"mild outside, severe inside\" and \"distant-site injury\" features to support a fall from height.",
        "With fall height h = 10 m and body weight m = 70 kg: v = \u221a(2\u00d79.81\u00d710) = 14.0 m/s and E = \u00bd\u00d770\u00d714.0\u00b2/1000 = 6.87 kJ. Feet or buttocks landing involves the calcaneus, spine and pelvis, while head landing gives severe craniocerebral injury, consistent with fall-from-height injury distribution.",
        "How are fall-from-height injuries distinguished from traffic injuries?",
        "Falls from height usually show force in a single direction, a mild-outside/severe-inside pattern and few seatbelt-like contusions, while traffic injuries often show characteristic bumper and wheel lacerations, steering wheel chest injuries, windscreen",
        "glass cutting",
        "and other multi-directional composite injuries.",
        "Does landing posture greatly affect injury?",
        "Yes. Landing on the feet transmits energy up the lower limbs (calcaneus, spine, skull base), landing on the head produces direct craniocerebral injury, and landing on the side commonly breaks ribs. Posture determines injury distribution.",
        "About \"Fall from Height Analyzer\"",
        "Compute impact speed and kinetic energy from the fall height, analyse the distribution of injuries across the body, and judge consistency of the landing posture and the features of a fall-from-height injury.",
        "Impact speed and kinetic energy calculation",
        "Analysis of 14 injury features",
        "Landing posture consistency judgement",
        "Recognition of mild-outside/severe-inside and transmitted injuries",
        "Aid to assessment of death from fall from height",
        "Reference for fall mechanics analysis",
        "About \"Fall from Height (Injury Distribution) Gravity Analyzer\"",
        "Fall from Height (Injury Distribution) Gravity Analyzer - a forensic pathology tool for analysing injury distribution in falls from height, inferring fall height and assessing deaths from falls. A professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()