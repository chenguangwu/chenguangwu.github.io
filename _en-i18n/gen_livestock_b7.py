#!/usr/bin/env python3
# gen_livestock_head.py — shared head for livestock batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'livestock')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'livestock')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {
    'disinfectant-dilution': {"稀释倍数？": "Dilution factor?"},
}
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
    out = {'slug': slug, 'industry': 'livestock', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('yufeirizengzhong-liaoroubiquxian', build('yufeirizengzhong-liaoroubiquxian', [
        "🐄 Finishing ADG / Feed Conversion Ratio (FCR) Curve",
        "Enter the start and end weights, finishing days and total feed intake to compute average daily gain (ADG), feed conversion ratio (FCR) and feed cost per kg gain, and give a growth-performance rating by species.",
        "Core formulas (by input): Math.round(days×i÷segs); i÷segs×100; adg×1000",
        'View "Finishing ADG / FCR Curve User Guide"',
        "Cattle (beef)",
        "Final weight (kg)",
        "Finishing days (days)",
        "💡 Formula: ADG = (final weight − initial weight) ÷ days; FCR = total feed ÷ total gain; feed cost per kg gain = FCR × feed unit price.",
        "📊 Growth-Performance Reference Standard (by species)",
        "📈 Finishing-Period Weight-Gain Curve (estimated)",
        "The curve is cumulative weight estimated linearly from average daily gain, for trend reference only; actual gain is mostly S-shaped.",
        "Rating standards are general reference values; they differ by breed and feeding method.",
        "📚 In-Depth: Finishing ADG and FCR Curve",
        "Derive ADG and FCR from start/end weight, days and feed used.",
        "Estimate gain cost (yuan/kg).",
        "Benchmark against breed standards and grade.",
        "300→480 kg, 120 days, feed 1100",
        "Gain 180 kg, ADG=180/120=1.5 kg/d, FCR=1100/180=6.11, gain cost=6.11×3.2=19.55 yuan/kg, total feed cost 3520 yuan.",
        "Benchmark",
        "FCR 6.11 better/worse than the breed baseline, with a rating and improvement direction.",
        "ADG unit?",
        "Commonly kg/d or g/d (×1000); finishing cattle about 1.0~1.5 kg/d.",
        "Cost composition?",
        "Gain cost = FCR × feed price, a core indicator of finishing profitability.",
        'About "Finishing ADG / FCR Curve"',
        "Used for growth-performance evaluation of cattle, pigs and sheep in the finishing stage. Enter the start and end weights, finishing days and total feed intake to automatically compute average daily gain (ADG), feed conversion ratio (FCR) and feed cost per kg gain, with a species rating and estimated weight-gain curve.",
        "Supports rating for three species: cattle/pig/sheep",
        "Automatically plots the finishing cumulative-weight curve",
        "Supports copying results and history",
        "Beef cattle feedlot FCR evaluation",
        "Pig finishing performance measurement",
        "Feed-formula effect comparison",
        "Finishing economic-benefit accounting",
        "Initial weight",
        "Final weight",
        "Finishing days",
        "Total feed intake",
        "Feed unit price",
    ]))

if __name__ == "__main__":
    main()
