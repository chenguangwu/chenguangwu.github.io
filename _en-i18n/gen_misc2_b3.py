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
    write('luggage-size', build('luggage-size', [
        "⚖️ Luggage Size Reference",
        "Luggage size specs compared with airline carry-on/checked baggage rules",
        "Luggage is distinguished by the sum of three sides (length + width + height) and capacity: 20-inch about 55 × 40 × 20 cm (three-side sum about 115 cm) is carry-on, 24-inch about 65 × 42 × 26 cm needs checking, 28-inch about 76 × 51 × 32 cm, 30-inch about 81 × 55 × 35 cm; carry-on is usually limited to three-side sum not over 115 cm and weight 7 to 10 kg, checked baggage limited to three-side sum not over 158 cm and weight 20 to 32 kg.",
        "Luggage Size",
        "18 inch",
        "20 inch",
        "22 inch",
        "24 inch",
        "26 inch",
        "28 inch",
        "30 inch",
        "✈️ Airline Baggage Rules Reference",
        "Tip: airline baggage rules vary by route and cabin class; the above is a common economy-class reference, and you should check the airline's official website before traveling.",
        "📦 Luggage Size Specs Table",
        "📚 In-Depth Analysis: Luggage Size Reference",
        "Before traveling, choose luggage by airline carry-on/checked limits: short trips choose 20-inch carry-on, long trips choose 24–28 inch checked.",
        "Compare length/width/height and three-side sums of different sizes (18–30 inch) to judge whether limits are exceeded.",
        "When multiple people or multiple legs are involved, distribute luggage to avoid boarding obstruction or overweight.",
        "Example: \"24-inch luggage\"",
        "Size about 60×41×26 cm, three-side sum = 127 cm, carry method = needs checking (exceeds most airlines' carry-on limit of 55×40×20 cm); suitable for mainstream checking on 7–10 day trips. 20-inch (50×34×24, sum 108) is mostly carry-on; 28-inch (72×50×30, sum 152) must be checked and watch the weight.",
        "How is carry-on luggage size calculated?",
        "Airlines usually limit by length+width+height three-side sum or single side length; the common international carry-on limit is about 55×40×20 cm (sum ≈ 115 cm), and low-cost carriers are stricter. This table gives three-side sums and carry methods for each size; the actual rules are subject to the latest regulations of the airline you fly.",
        "How do size and capacity correspond?",
        "Size refers to the longest side of the case in inches; 18/20/22/24/26/28/30 inch correspond to different length/width/height and capacity gradients; the larger the size, the higher the capacity but the easier to exceed weight (checked often limited to 20–23 kg), so choose by both size and weight limits.",
        "About \"Luggage Size Reference\"",
        "The luggage size reference table collects 18-30 inch luggage specs and compares carry-on and checked baggage rules of major airlines, helping travelers choose luggage and plan baggage allowances.",
        "18-30 inch full-spec comparison",
        "Marks carry-on/checked attributes",
        "Summarizes major airline baggage rules",
        "Three-side sum at a glance",
        "Luggage Size Reference - airline baggage rules comparison table, 20/24/28 inch luggage sizes and carry-on/checked rules, Air China, China Eastern, China Southern baggage allowance reference. Travel tools, essential for trips, supports offline use.",
    ]))
    write('screen-size', build('screen-size', [
        "🧮 Screen Size Calculator",
        "Enter resolution and diagonal inches to calculate PPI, aspect ratio, and actual screen width/height",
        "Screen Size Calculation",
        "/ Screen Size Calculation",
        "Diagonal pixels = √(width pixels² + height pixels²); PPI pixel density = diagonal pixels ÷ diagonal inches (1920 × 1080, 24-inch about 92 PPI); physical width = diagonal × width pixels ÷ diagonal pixels, physical height likewise; PPI below 110 shows visible pixels, above 200 displays finely; screen area = physical width × physical height, aspect ratio = width pixels ÷ height pixels.",
        "Diagonal (inches)",
        "= √(width² + height²)",
        "= diagonal pixels ÷ diagonal inches",
        "Physical width per inch",
        "= resolution width ÷ PPI",
        "Aspect Ratio",
        "= width : height (simplified)",
        "Dot Pitch",
        "Tip: higher PPI means finer display; phones generally at 300+ PPI are Retina level. Aspect ratio simplification uses the greatest common divisor.",
        "📚 In-Depth Analysis: Screen Size Calculator",
        "When buying a monitor/phone/projector, compute PPI from resolution and diagonal to judge whether clarity is sufficient.",
        "Compare pixel density differences of the same resolution at different sizes (e.g. 24-inch 1080p vs 27-inch 1080p).",
        "Convert actual display width/height (inches/cm) and aspect ratio to confirm desktop or wall-mount fit.",
        "Example: \"resolution 1920×1080, diagonal 23.8 inches\"",
        "Diagonal pixels = √(1920²+1080²) ≈ 2202.9, PPI = 2202.9/23.8 ≈ 92.56; actual display width = 1920/92.56 ≈ 20.74 inches, height ≈ 11.67 inches; aspect ratio = 1920:1080 simplified to 16:9; dot pitch = 25.4/92.56 ≈ 0.274 mm. If switched to 27-inch 2560×1440, PPI rises to 108.79, text is finer.",
        "How high a PPI counts as sharp?",
        "About 90–110 PPI is a common comfortable desktop range; phones often 400+ PPI due to close viewing distance. At the same resolution, smaller size means higher PPI (denser pixels), but too small strains the eyes; projectors or TVs at far viewing distance are clear even at low PPI.",
        "How is the aspect ratio obtained from resolution?",
        "Take the",
        "greatest common divisor",
        "of width and height, then simplify, e.g. 1920/1080 has gcd=120 → 16:9; ultra-wide 3440×1440 → 43:18 (about 21:9). It determines picture shape and affects movie letterboxing and multi-window layout.",
        "About \"Screen Size Calculation\"",
        "The screen size calculator computes PPI pixel density, aspect ratio, physical width/height, and dot pitch from resolution and diagonal inches, suitable for analyzing screen parameters of phones, monitors, etc.",
        "Screen Size Calculator - enter resolution and diagonal inches to calculate PPI pixel density, aspect ratio, actual screen width/height, phone screen size and resolution conversion. Online tools built for developers, running purely front-end, code never leaves the browser.",
    ]))
if __name__ == '__main__':
    main()
