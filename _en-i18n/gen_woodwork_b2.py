#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'woodwork')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'woodwork')
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
    out = {'slug': slug, 'industry': 'woodwork', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== analysis-cost-price (27) =====
    write('analysis-cost-price', build('analysis-cost-price', [
        '💰 Wood price and cost fluctuation analysis',
        'Price fluctuation analysis',
        'Wood price and cost fluctuation analysis',
        '/ Wood price and cost fluctuation analysis',
        'Sample std dev s = √[Σ(xᵢ−x̄)²/(n−1)]; fluctuation coefficient CV = s / x̄ × 100%; latest-price deviation = (latest price − base price) / base price × 100%.',
        'Wood prices fluctuate with supply/demand and seasonality; use the mean and median to describe the center, std dev and CV to measure fluctuation, and latest-price deviation from base to spot short-term anomalies; when |deviation| exceeds the warning threshold a fluctuation alert triggers, aiding procurement timing and inventory control. For reference only.',
        'Price / cost series (CNY, comma- or newline-separated, latest last)',
        'Reference base price (CNY)',
        'Fluctuation warning threshold (%)',
        'Compute fluctuation',
        '📚 In-depth: wood price and cost fluctuation analysis',
        'Procurement timing: track the mean and',
        'and fluctuation coefficient of the price series to judge whether the current price is high or low relative to the center.',
        'Inventory cost control: use the latest-price deviation from base to spot short-term anomalies; when alerted, restock or lock price prudently.',
        'Fluctuation assessment: quantify wood-price uncertainty and risk level with',
        'and CV.',
        'Example (5 periods, base 3000)',
        'Price series (CNY/m³): 3200, 3300, 3100, 3400, 3500. Mean 3300.00, median 3300.00, sample',
        'std dev 132.29, fluctuation coefficient 4.01%; latest price 3500.00, deviation from base 3000 is +16.67%, threshold 10% triggers fluctuation alert.',
        'What is the difference between CV and std dev?',
        'Std dev is the absolute fluctuation magnitude, affected by the price scale; CV is relative fluctuation (std dev / mean), convenient for horizontal comparison across series at different price levels. The higher the price, the smaller the CV for the same std dev, so the fluctuation looks smoother.',
        'Once an alert triggers, must we stop procurement?',
        'Not necessarily. The alert only signals short-term deviation beyond the threshold; judge with supply/demand trend, inventory and capital together. Persistent triggering may mean the price center has shifted up, so locking price opportunistically may be the right move.',
        'Mass (grade / moisture / standard) inspection',
        'About "wood price and cost fluctuation analysis"',
        'Wood price and cost fluctuation analysis tool. Enter a price series and a reference base price to compute the mean, median, sample std dev, fluctuation coefficient CV and latest-price deviation, and judge fluctuation alert by the warning threshold, for wood procurement and inventory cost control.',
        'Example: 3200,3300,3100,3400,3500',
    ]))

    # ===== desk-dimensions (22) =====
    write('desk-dimensions', build('desk-dimensions', [
        '"Desk Dimensions" performs professional calculations and outputs results based on input parameters.',
        'Desk dimension planning calculator',
        '/ Desk dimension planning calculator',
        '📖 View "Ergonomic desk and chair height recommendation guide"',
        '📐 Desk dimension planning calculator',
        'How tall should the desk and chair be? By height and usage scenario, recommend desk height, chair height, screen-center height and desktop depth by ergonomic ratios.',
        'Monitor size (inches)',
        '📚 In-depth: ergonomic desk/chair height recommendation',
        'Home / office desk and chair selection',
        'Standing-desk setup',
        'Screen-center height calibration',
        'By height: sitting desk height ≈ height × 0.46, chair height ≈ height × 0.26, screen-center height ≈ height × 0.71, desktop depth about 70 cm for computer use; standing desk height ≈ height × 0.62, screen-center ≈ height × 0.95.',
        'Height 170 cm: sitting desk height 170×0.46≈78 cm, chair 170×0.26≈44 cm, screen-center 170×0.71≈121 cm, depth 70 cm; standing mode desk height 170×0.62≈105 cm, screen-center 170×0.95≈162 cm. For reference in selection; an adjustable model is more stable.',
        'Why are these ratios set this way?',
        'Based on statistical means of sitting elbow height and eye-sight height (about height 0.46 / 0.71), these are empirical recommended ranges; individuals with different arm/leg proportions can fine-tune.',
        'What if my height is out of range?',
        'The formula fits most people 150–200 cm; for very tall/short, compute by ratio then measure actual elbow and sight height.',
        'Desk height ≈ height × 0.46, chair height ≈ height × 0.26 (sitting)',
        'Standing desk height ≈ height × 0.62',
        'Desktop depth ≥70cm recommended for computer work, 60cm for writing',
        'Standard: elbows at 90°, monitor top at eye level, lumbar supported',
        'Mass (standard / inspection / certification) assurance',
    ]))

    print('body_woodwork_b2 done')

if __name__ == '__main__':
    main()
