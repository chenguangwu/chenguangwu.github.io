#!/usr/bin/env python3
# gen_obstetrics_b1.py — obstetrics b1 (5 slugs): afi-normal/bishop-score/calc-50/calc-risk/ctg-fhr
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'obstetrics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'obstetrics')

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
    out = {'slug': slug, 'industry': 'obstetrics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

# body: obstetrics b6
def main():
    taipanchengshudu_grannumfenji_en = [
        '🤱 Placental Maturity (Grannum Grading)',
        'Automatically determine Grannum grade and clinical meaning from ultrasound chorionic plate, parenchyma and basal plate.',
        '📖 View "Placental Maturity (Grannum Grading) User Guide"',
        'Chorionic plate',
        'Smooth, no indentations',
        'Slightly wavy, not reaching basal layer',
        'Marked indentations, not reaching basal layer',
        'Indentations deep to basal layer, forming placental lobules',
        'Uniform fine granules',
        'Scattered punctate bright echoes',
        'Comma-shaped bright echoes, near basal layer',
        'Extensive calcification ring, central anechoic zone',
        'No or mild calcification',
        'Linear calcification',
        'Extensive dense calcification',
        '💡 Grannum grading runs from 0 (immature) to III (mature/aged); assess placental function with gestational age.',
        'Grade III before 37 wks may suggest premature placental aging; intensify monitoring.',
        'Placental maturity is not identical to function; judge with fetal movement, amniotic fluid, fetal growth, etc.',
        '📚 In-Depth: Placental Maturity Grannum Grading (Gestational-Age Link)',
        'Interpret by gestational age whether grading is prematurely mature.',
        'Identify the link between premature grading and fetal growth restriction.',
        'Ultrasound report interpretation.',
        'Premature placental aging',
        'Grade III at 32 wks: III before term suggests premature aging; combine AFI, umbilical flow and FHR.',
        'Normal maturation',
        'Grade III at 39 wks: normal maturation matching fetal age; if no other abnormality, await spontaneous labor.',
        'How do gestational age and grade correspond?',
        'Roughly grade 0 <28 wks, I 29-36 wks, II 33-40 wks, III >=37 wks; higher grade before its week range is premature.',
        'What to check for abnormal grading?',
        'Check AFI, umbilical S/D, fetal growth curve and CTG; judge function comprehensively, not grade alone.',
        'About the "Placental Maturity (Grannum Grading)"',
        'Grannum grading observes the chorionic plate, parenchyma and basal plate on ultrasound to classify placental maturity 0 to III.',
        'Auto-determine Grannum grade from ultrasound findings',
        'Flag premature or delayed maturation by gestational age',
        'Provide each grade\'s description and clinical meaning',
        'Obstetric ultrasound report interpretation',
        'Fetal monitoring and placental function assessment',
    ]
    yangshuizhishu_afi_zhengchangfanwei_en = [
        '📋 Amniotic Fluid Index (AFI) Normal Range',
        'Supports four-quadrant AFI and maximal vertical pocket (MVP) modes to quickly judge amniotic fluid volume.',
        '📖 View "Amniotic Fluid Index (AFI) Normal Range User Guide"',
        'AFI four quadrants',
        'MVP single pocket',
        'AFI = sum of four-quadrant pocket depths; MVP = deepest vertical pocket depth',
        'AFI <5 cm oligohydramnios, 5-8 cm borderline, 8-25 cm normal, >25 cm polyhydramnios; MVP <2 too low, 2-8 normal, >8 too high.',
        'Quadrant 1 (cm)',
        'Quadrant 2 (cm)',
        'Quadrant 3 (cm)',
        'Quadrant 4 (cm)',
        'Deepest vertical pocket depth (cm)',
        '💡 Reference: AFI <5 cm oligohydramnios, 5-8 cm borderline, 8-25 cm normal, >25 cm polyhydramnios; MVP <2 cm oligohydramnios, 2-8 cm normal, >8 cm polyhydramnios.',
        'AFI and MVP each have pros/cons; clinicians often combine with gestational age and fetal status.',
        'Abnormal fluid needs to exclude PROM, fetal anomaly, placental insufficiency, etc.',
        '📚 In-Depth: AFI Normal-Range Interpretation',
        'Ultrasound measures AFI to judge whether fluid is normal.',
        'At borderline/abnormal AFI, decide recheck and intervention.',
        'Screen for PROM/fetal anomalies.',
        'Four quadrants 4+4+5+3 = 16 cm, within 8-25 cm normal; continue routine care.',
        'Oligohydramnios',
        'AFI 4.5 cm (<5): oligohydramnios; rule out PROM and urinary anomalies; at term consider delivery.',
        'What is the normal AFI range?',
        'Generally 8-25 cm normal; 5-8 cm borderline low, <5 cm low, >25 cm high; guidelines vary slightly.',
        'What do low and high each warn about?',
        'Low warns of PROM, fetal anomaly, placental insufficiency; high warns of GDM, fetal GI anomaly; both need further evaluation.',
        'About the "Amniotic Fluid Index (AFI) Normal Range"',
        'Supports four-quadrant AFI and MVP, the two common ultrasound methods, to auto-judge oligohydramnios, borderline, normal or polyhydramnios.',
        'AFI four-quadrant and MVP single-pocket dual modes',
        'Auto-interpret and give clinical advice',
        'Real-time calculation, clean interface',
        'Quick obstetric ultrasound report check',
        'Outpatient amniotic-fluid assessment',
    ]
    write('taipanchengshudu-grannumfenji', build('taipanchengshudu-grannumfenji', taipanchengshudu_grannumfenji_en))
    write('yangshuizhishu-afi-zhengchangfanwei', build('yangshuizhishu-afi-zhengchangfanwei', yangshuizhishu_afi_zhengchangfanwei_en))

if __name__ == '__main__':
    main()
