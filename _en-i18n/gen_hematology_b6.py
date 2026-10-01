#!/usr/bin/env python3
# gen_hematology_b6.py — hematology b6 (1 slug): transfusion-dose
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'hematology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'hematology')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

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
    out = {'slug': slug, 'industry': 'hematology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


B = {}

B['transfusion-dose'] = [
 '💊 Transfusion (Blood Component) Dose Calculator',
 'Calculates the infusion dose and expected effect of each blood component.',
 '"Calculates the infusion dose and expected effect of each blood component" is computed from the input parameters and the result is output.',
 'Transfusion Blood Component Dose Calculator',
 '/ Transfusion Dose Calculator',
 '📖 Read the "Transfusion (Blood Component) Dose Calculator Usage Guide"',
 'Red cells PRBC',
 'Platelets PLT',
 'Plasma FFP',
 'Cryoprecipitate Cryo',
 'Target HGB (g/L)',
 'Current platelets (×10⁹/L)',
 'Target platelets (×10⁹/L)',
 'Apheresis platelets (1 bag ≈2.5×10¹¹)',
 'Pooled platelets (1 unit ≈0.5×10¹¹)',
 'Dose (mL/kg)',
 'Current fibrinogen (g/L)',
 'Target fibrinogen (g/L)',
 '📋 Blood component transfusion reference',
 'Rise per unit / bag',
 'Transfusion indication',
 'Red cell suspension',
 '1 U ≈200 mL (leukoreduced)',
 'HGB ↑~10 g/L or HCT ↑~3%',
 'HGB <70 g/L or <80 g/L (symptomatic)',
 'Apheresis platelets',
 '1 bag ≈2.5×10¹¹',
 'PLT <20 or <50 (bleeding / surgery)',
 'Fresh frozen plasma',
 'Coagulation factors ↑ about 5%',
 'PT/APTT >1.5× normal',
 'Cryoprecipitate',
 '1 U contains Fib ≥150 mg',
 'Fib ↑~0.5 g/L (adult)',
 'Note: the actual rise is affected by weight, transfusion history, immune status and active bleeding. Platelet transfusion effect can be assessed by CCI (corrected count increment). For study reference only.',
 '📚 Deep Dive: Transfusion (Blood Component) Dose Calculator',
 'From current / target HGB compute red cell units and expected rise (about +10 g/L per U).',
 'For platelets, count bags by apheresis / pooled and body weight, and use CCI to judge effectiveness.',
 'For plasma (FFP) compute total by mL/kg, raising coagulation factors about 15-20%.',
 'Red cells: units = ceil((target − current) HGB / 10), each U of suspension raises HGB about 10 g/L. Platelets: 1 apheresis bag (≈2.5×10¹¹) raises about 25-30×10⁹/L (70 kg), 1 pooled U about 5×10⁹/L; CCI = (post − pre PLT) ×',
 'body surface area',
 '/ total platelets infused, 1h CCI >7.5 or 24h >4.5 suggests effective. FFP: 10-15 mL/kg, each U ≈200 mL.',
 'Example (red cells: current HGB=60, target=90, weight 70): need to raise 30 g/L → ceil(30/10)=3 U, expected HGB=60+3×10=90 g/L. Platelets (apheresis, current 10, target 40): gap 30×10⁹/L, about 1 bag (25-30 per bag) reaches target, check CCI after infusion to verify effectiveness.',
 'Does each red cell unit always raise +10 g/L?',
 'It is the adult empirical mean, affected by blood volume, bleeding and haemolysis; children convert by weight (about 4-6 mL/kg red cell suspension per kg raises about 10 g/L), and the actual result follows the post-transfusion blood count.',
 'What does a low CCI mean?',
 '1h CCI ≤7.5 or 24h ≤4.5 suggests ineffective transfusion, commonly from alloimmunisation, fever / infection / bleeding / DIC causing platelet consumption; investigate the consumption cause and consider typed / HLA-matched platelets.',
 'About the Transfusion (Blood Component) Dose Calculator',
 'A transfusion blood component dose calculator: it computes the infusion dose and expected effect of red cell suspension, platelets, fresh frozen plasma and cryoprecipitate, with weight and target-value support. A professional medical tool based on authoritative medical standards, for reference only.',
]

for s, lst in B.items():
    write(s, build(s, lst))
