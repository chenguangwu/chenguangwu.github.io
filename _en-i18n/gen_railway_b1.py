#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'railway')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'railway')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'railway', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('diaoche-zuoye-xiaolv-youhua', build('diaoche-zuoye-xiaolv-youhua', [
        '⚡ Rail Shunting (Operation / Efficiency) Optimizer',
        'Compute the average time per shunting cut, cuts per hour, daily cut output and the efficiency deviation from the benchmark from the operation time and the number of cuts completed.',
        '/ Rail Shunting (Operation / Efficiency) Optimizer',
        '📖 View the Rail Shunting (Operation / Efficiency) Optimizer user guide',
        'Time per cut = operation time ÷ number of cuts (min per cut); cuts per hour = number of cuts ÷ time × 60; daily cut output = cuts per hour × 20 h',
        'The core indicator of shunting efficiency is the average time per cut, for which the industry benchmark is commonly 8 min per cut; the tool also gives cuts per hour, the daily cut output calculated on a 20-hour shift, and the efficiency deviation from the benchmark.',
        'Shunting operation time (min)',
        'Number of cuts completed (cuts)',
        '💡 Time per cut (min per cut) = operation time ÷ number of cuts; cuts per hour = number of cuts ÷ time × 60; the common benchmark is 8 min per cut.',
        '📚 In-depth analysis: Shunting Operation Efficiency Optimisation',
        'Operation statistics for marshalling yards and district stations: derive the average time per cut from the shunting time per shift and the cuts actually completed, compare it with the industry reference benchmark of 8 min per cut, and judge the efficiency level of the shift.',
        'Estimating daily throughput capacity: convert cuts per hour into daily cut output on the basis of a 20-hour shift, for shift planning and capacity assessment.',
        'Verifying improvements in working method: re-measure the time per cut after switching to hump or push-pull operations, quantify the improvement with the efficiency deviation from the benchmark, and provide the basis for technical renovation.',
        'Worked example: 240 min of operation, 36 cuts completed',
        'Average time per cut = 240 ÷ 36 = 6.67 min per cut; cuts per hour = 36 ÷ 240 × 60 = 9.00 cuts/h; daily cut output = 9.00 × 20 = 180.00 cuts; the efficiency deviation from the 8 min per cut benchmark = (8 − 6.67) ÷ 8 × 100% = 16.67%, better than the benchmark.',
        'What kind of unit is a cut?',
        'It is the basic unit of measurement for shunting work: one complete operating cycle of pulling out, pushing in and coupling or uncoupling a car. The counting basis for cuts may differ between pick-up and set-out trains and between marshalling operations, so unify it when comparing.',
        'How is the 8 min per cut benchmark used?',
        'This is a common reference value for flat shunting lead track operations. Mechanised humps, direct access on dedicated lines and sending or collecting car groups differ considerably, so substitute the historical average or the surveyed value of your own station before comparing.',
        'What should the operation time include?',
        'It should include only the time directly related to shunting (pulling out, pushing in, coupling and changing tracks), excluding waiting for the locomotive, shift handover and shunting plan preparation; otherwise the time per cut is significantly overestimated.',
        'About Rail Shunting (Operation / Efficiency) Optimizer',
        'Shift plan workload statistics and efficiency accounting at marshalling yards',
        'Bottleneck identification in collecting, delivering, breaking up and humping operations',
        'Station work organisation optimisation and efficiency improvement assessment',
        'Operation',
        'Efficiency',
    ]))

    write('power-5', build('power-5', [
        '⚡ Locomotive (Tractive Effort / Power) Matching',
        'Convert locomotive tractive power, the power demand per unit of tractive effort and the rated diesel engine power from tractive effort and running speed.',
        '/ Locomotive (Tractive Effort / Power) Matching',
        '📖 View the Locomotive (Tractive Effort / Power) Matching user guide',
        'Tractive power = tractive effort (kN) × speed (km/h) ÷ 3.6 (kW); rated diesel engine power = tractive power ÷ 0.85 (transmission efficiency)',
        '1 kN × 1 km/h = 277.8 W, so tractive power (kW) = tractive effort × speed ÷ 3.6; then back-calculate the rated diesel engine power with a transmission efficiency of 0.85, for locomotive selection and tonnage rating checks.',
        'Tractive effort (kN)',
        'Running speed (km/h)',
        '💡 Tractive power (kW) = tractive effort (kN) × speed (km/h) ÷ 3.6; rated diesel engine power = tractive power ÷ 0.85 (transmission efficiency).',
        '📚 In-depth analysis: Locomotive Tractive Effort and Power Matching',
        'Locomotive selection and tonnage rating checks: substitute the tractive effort demand and running speed of the section to convert the required power at the wheel rim, compare it with the rated power of the locomotive type, and judge whether the tonnage rating and section running time can be met.',
        'Back-calculating rated diesel engine power: derive the rated diesel engine power from the power at the wheel rim using a transmission chain efficiency of 0.85, so that looking only at wheel-rim power does not lead to choosing too small a type and running it at full load for long periods.',
        'Traction energy and fuel checks: once the power demand is fixed, estimate the section fuel consumption and running cost from the specific fuel consumption, for comparing locomotive operation schemes.',
        'Worked example: tractive effort 300 kN, running speed 80 km/h',
        'Tractive power = 300 × 80 ÷ 3.6 = 6666.67 kW; each kN of tractive effort needs 80 ÷ 3.6 = 22.22 kW/kN; tractive effort per unit speed = 300 ÷ 80 = 3.750 kN per km/h; equivalent per km/h = 300 × 3.6 ÷ 80 = 13.5000 kN; back-calculating with a transmission efficiency of 0.85 gives a rated diesel engine power = 6666.67 ÷ 0.85 = 7843.14 kW.',
        'Why divide by 3.6?',
        'Because 1 kN × 1 km/h = 1000 N × 0.2778 m/s = 277.8 W, so P (kW) = F (kN) × v (km/h) ÷ 3.6. The coefficient is tied to the unit system; switching to tf or m/s requires a new conversion.',
        'What does the transmission efficiency of 0.85 mean?',
        'It is the overall transmission efficiency from the diesel engine to the wheel rim, covering the main generator, traction motors and gearbox; diesel-electric locomotives are usually 0.82-0.88, while hydraulic transmission types are slightly lower. Take the value from the actual curve of the locomotive type.',
        'Which pair of tractive effort and speed values should be used?',
        'For tonnage rating calculations use the continuous regime, that is continuous speed and continuous tractive effort; the starting regime gives greater tractive effort but cannot be sustained for long, and calculating power with the starting value significantly overestimates the demand.',
        'About Locomotive (Tractive Effort / Power) Matching',
        'Locomotive selection and power margin verification',
        'Matching train formation mass with speed limits',
        'Traction capacity accounting for mountain and long steep-gradient lines',
        'Tractive effort',
    ]))


if __name__ == '__main__':
    main()
