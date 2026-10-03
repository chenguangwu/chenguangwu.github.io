#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'misc2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'misc2')
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
    out = {'slug': slug, 'industry': 'misc2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('shoe-size', build('shoe-size', [
        "🧵 Sneaker Size Conversion",
        "Enter foot length (mm) to automatically match EU/US/CN sneaker sizes",
        "Shoe size converts by foot length: CN value = foot length (cm) (foot length 250 mm is CN 250); EU = foot length (cm) × 1.5 + 2 (with 0.5 as the smallest step); UK ≈ EU − 33, US men ≈ EU − 32, US women ≈ EU − 30.5; sizing is based on the measured length from heel to longest toe, and sneakers usually reserve 5 to 10 mm to accommodate foot swelling during exercise.",
        "Men's",
        "Women's",
        "📐 Size Conversion Formula",
        "China Size CN",
        "= foot length mm ÷ 10 (e.g. 255 mm → 25.5)",
        "EU Size",
        "≈ foot length cm × 1.5 + 2 (e.g. 25.5 cm → 40.25 ≈ 40)",
        "US Men's",
        "≈ foot length cm × 3 ÷ 2 − 22 (e.g. 25.5 cm → 7.25 ≈ 7.5)",
        "US Women's",
        "≈ men's size + 1.5",
        "UK Size",
        "≈ US size − 1",
        "Note: different sneaker brands (Nike runs half a size small, Adidas true to size) have differences; it is recommended to refer to the brand's official size chart.",
        "Tip: measure foot length in the afternoon (feet swell slightly) and measure wearing socks for accuracy. Wide feet/high instep suggest choosing half a size up.",
        "📚 In-Depth Analysis: Sneaker Size Conversion",
        "When buying sneakers online, convert foot length (mm) to CN/EU/US/UK sizes to avoid wrong sizes.",
        "Compare US size differences for the same foot length between men and women (women's ≈ men's + 1.5).",
        "When crossing brands (e.g. Nike runs narrow and needs half a size up), fine-tune by foot shape.",
        "Example: \"foot length 260 mm (men)\"",
        "cm = 26.0, CN = 26.0; EU = round((26 × 1.5 + 2) × 2)/2 = 41; US men = round((26 × 1.5 − 22) × 2)/2 = 17; UK = US − 1 = 16; US women = 17 + 1.5 = 18.5. If foot length is 250 mm: EU = 39.5, US men = 15.5, UK = 14.5. For narrow-fit brands like Nike, try half a size up in actual wear.",
        "Why are shoe sizes different across countries?",
        "CN size ≈ foot length in cm; EU = foot length cm × 1.5 + 2 roughly; US/UK sizes are based on inches and differ by gender baseline (women's is about +1.5 over men's at the same foot length). The formula is an approximate conversion; different brand lasts (width/toe) cause deviations in actual fit.",
        "Foot length measured accurately but still rubbing?",
        "Measure foot length standing with weight bearing, from longest toe tip to heel, and reserve about 1 thumb width (≈1 cm) of room; wide feet or high instep should choose wide lasts or half a size up. This table gives standard conversion; final fit is subject to try-on or the brand size chart.",
        "About \"Sneaker Size Conversion\"",
        "The sneaker size conversion table quickly converts EU, US, CN, and UK sizes from foot length, and provides men's/women's difference conversion, convenient for overseas and cross-border shoe shopping.",
        "One-click conversion of foot length to four-country sizes",
        "Distinguishes men's and women's differences",
        "Provides brand selection advice",
        "Sneaker Size Conversion Table - EU/US/CN sneaker size comparison, enter foot length to auto-match each country's sneaker size, Nike/Adidas size reference. Daily life tools, close to life, practical and convenient.",
    ]))
    write('tax-refund', build('tax-refund', [
        "🧾 Overseas Shopping Tax Refund Estimator (Comprehensive)",
        "Enter shopping amount and destination to estimate refundable tax and actual spending after refund",
        "Core formula (by input variables): tax × 0.05",
        "United States (no federal tax refund)",
        "Shopping Amount (local currency)",
        "Exchange Rate (per 1 CNY)",
        "🌍 Country Tax Refund Reference",
        "Tip: refund rates and minimum thresholds vary by country and product category; the actual rules are subject to local customs and refund companies. Refund companies usually charge a service fee.",
        "📚 In-Depth Analysis: Overseas Shopping Tax Refund Estimator (Comprehensive)",
        "Before outbound shopping, estimate refundable amounts by destination country's refund rate and threshold, comparing how worthwhile different destinations are.",
        "Convert foreign-currency refunds to CNY to see the actual take-home benefit (after deducting fees).",
        "Judge whether single-store spending reaches the threshold to decide whether to combine purchases for refund.",
        "Example: \"Japan shopping 100,000 JPY, exchange rate 0.048, single store over 5,000 JPY refunds 10%\"",
        "Reaches threshold: refundable tax = 100,000 × 10% = 10,000 JPY; refund company fee about 5% = 500 JPY; actual refund = 9,500 JPY ≈ ¥456 (at 0.048). Germany (19%, threshold 25 EUR) shopping 2,000 EUR: refund 380 EUR, fee 19 EUR, actual refund 361 EUR ≈ ¥2,815.8. The US has no federal tax refund; the tool prompts to consult locally.",
        "Is the refund on the full amount or only the excess?",
        "Most countries calculate the refund on the full amount after reaching the threshold (e.g. Japan 10%, Germany 19%), not only the excess; if the threshold is not reached (e.g. Japan single store < 5,000 JPY) no refund. Some countries also have per-receipt or per-store thresholds.",
        "Why does the fee eat into the refund?",
        "Airport refund companies or merchant agents usually charge about 5% (or a fixed fee) service fee; the share is small for large purchases and high for small ones; credit card refund exchange rates may also have discounts. It is recommended to concentrate large amounts at refundable stores and compare cash vs credit card refund arrival differences.",
        "About \"Overseas Shopping Tax Refund Estimator\"",
        "The overseas shopping tax refund estimator helps outbound tourists quickly understand each country's refund policy and refundable amount; enter shopping amount and exchange rate to estimate the actual take-home refund.",
        "Covers popular destinations such as Japan, Korea, Europe, US, Thailand",
        "Automatically judges the threshold",
        "Estimates fees and CNY equivalent",
        "Overseas Shopping Tax Refund Calculator. Travel tools, essential for trips, supports offline use.",
    ]))
if __name__ == '__main__':
    main()
