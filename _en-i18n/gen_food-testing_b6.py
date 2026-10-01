#!/usr/bin/env python3
# gen_food-testing_b6.py — food-testing b6 (2 slugs): sugar-fehling/total-migration
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'food-testing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'food-testing')

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
    out = {'slug': slug, 'industry': 'food-testing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


B = {}

B['sugar-fehling'] = [
 '🔄 Total Sugar Fehling Reagent Reducing Sugar Converter',
 'Per the GB 5009.7 direct titration method (Lane-Eynon), it computes the reducing sugar and total sugar content of a food.',
 '📖 Read the "Fehling Reagent Reducing Sugar / Total Sugar Usage Guide"',
 'Reducing sugar content = F × V₁ ÷ (m × V₂) × 100, where F is the Fehling reagent equivalent (mg), V₁ the volume the sample was made up to (mL), V₂ the titration volume consumed (mL) and m the sample mass (g); the conversion factor 0.95 converts to total sugar, and sucrose = total sugar − reducing sugar.',
 'Fehling reagent concentration factor F (mg/mL)',
 'Sample titration volume consumed V₂ (mL)',
 'Reducing sugar (as glucose)',
 'Total sugar (after hydrolysis, as glucose)',
 'Sucrose = total sugar - reducing sugar',
 'Reducing sugar content (%)',
 'Total sugar content (%)',
 '= (F × V₁) / (m × V₂) × 100 × 0.95 (the hydrolysis conversion factor)',
 'Sucrose content (%)',
 '= total sugar - reducing sugar',
 'F is the Fehling reagent concentration factor, the mg of glucose that 1 mL of Fehling solution is equivalent to',
 '📚 Deep Dive: Fehling Reagent Reducing Sugar and Total Sugar',
 'Determining reducing sugar in food',
 'Determining total sugar after hydrolysis',
 'Back-calculating sucrose content',
 'Reducing sugar (%) = (F × V₁)/(m × V₂) × 100, where F is the Fehling factor in g/mL, V₁ the test solution volume, m the sample and V₂ the volume consumed; sucrose = total sugar − reducing sugar.',
 'F = 0.005 g/mL (glucose), test solution 250 mL, sample 5.00 g, titration volume 15.20 mL: reducing sugar = (0.005 × 250)/(5.00 × 15.20) × 100 ≈ 1.65%; for a sucrose-type sample, measure total sugar and subtract reducing sugar to get sucrose.',
 'How is the F factor determined?',
 'Standardize the Fehling solution with standard glucose to find how many grams of glucose 1 mL is equivalent to; it changes with the reagent batch.',
 'Why is total sugar higher?',
 'Total sugar is measured after acid hydrolysis converts sucrose and starch into reducing sugars, so it includes reducing sugar plus hydrolysed sugar and is therefore at least as high.',
 'About the Total Sugar Fehling Reagent Reducing Sugar Converter',
 'A total sugar Fehling reagent reducing sugar converter. A cooking helper for keeping ingredient ratios and nutrition precise.',
 'Fill in when calculating sucrose',
]

B['total-migration'] = [
 '🍳 Total Migration Calculator for Food Contact Materials',
 'Per GB 31604.1, it computes the total migration of food contact materials and judges whether they meet the overall migration limit of 10 mg/dm² or less (OML).',
 'Core formulas (by input variables): Math.round(migrationDM×10000)÷10000; Math.round(migrationKg×10000)÷10000; migrationDM×6',
 '📖 Read the "Total Migration of Food Contact Materials Usage Guide"',
 'Mass of specimen plus container before the immersion test m₁ (mg)',
 'Mass of specimen plus container after the immersion test m₂ (mg)',
 'Mass of the blank container m₀ (mg)',
 'Specimen contact area S (dm²)',
 '10% ethanol',
 '20% ethanol',
 '50% ethanol',
 '95% ethanol',
 '3% acetic acid',
 'Isooctane',
 'Vegetable oil',
 'Immersion conditions',
 '40 °C for 10 days (long-term storage)',
 '70 °C for 2 hours (high temperature, short time)',
 '100 °C for 1 hour (boiling water)',
 '121 °C for 30 minutes (sterilization)',
 'Room temperature for 24 hours',
 'Limit standard (mg/dm²)',
 'Calculate total migration',
 'Total migration (mg/dm²)',
 'm₁ is the specimen plus container mass before immersion and m₂ the evaporated residue plus container mass after immersion',
 'S is the contact area between the specimen and the food simulant (dm²)',
 'Overall migration limit OML',
 '= 10 mg/dm² (GB 9685); for materials in contact with infant food it is 60 mg/kg.',
 '💡 When the area to volume ratio does not match the 6 dm²/kg standard, mg/kg can be used instead: total migration (mg/kg) = migrated mass (mg) / simulant volume (L).',
 '📚 Deep Dive: Total Migration of Food Contact Materials',
 'Judging total migration compliance',
 'Safety assessment of packaging materials',
 'Comparison against the OML limit',
 'Migrated mass = m₂ − m₁ (mass after immersion minus mass before); total migration (mg/dm²) = migrated mass / contact area; converting to mg/kg of food multiplies by 6.',
 'Specimen 50.000 g before immersion and 50.015 g after (blank 48.000 g), area 3 dm²: migration = 15 mg, total migration = 15/3 = 5 mg/dm², which meets the OML of 10 mg/dm² or less.',
 'What is OML?',
 'The overall migration limit, normally 10 mg/dm² or 60 mg/kg, set out in GB 31604.1.',
 'What is the blank specimen for?',
 'It deducts interference from the simulant itself evaporating or being absorbed, so the migrated mass comes only from the material.',
 'About the Total Migration Calculator for Food Contact Materials',
 'A total migration calculator for food contact materials. A cooking helper for keeping ingredient ratios and nutrition precise.',
]

for s, lst in B.items():
    write(s, build(s, lst))
