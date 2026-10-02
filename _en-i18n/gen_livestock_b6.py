#!/usr/bin/env python3
# gen_livestock_head.py — shared head for livestock batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'livestock')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'livestock')
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
    out = {'slug': slug, 'industry': 'livestock', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('withdrawal-period', build('withdrawal-period', [
        "📅 Drug Withdrawal Period Countdown",
        "Select the veterinary drug and enter the last medication date to calculate the withdrawal-period end time and ensure food safety.",
        'View "Drug Withdrawal Period Countdown User Guide"',
        "Drug Name",
        "Doxycycline (Vibramycin)",
        "Ceftiofur",
        "Tylosin",
        "Lincomycin",
        "Tilmicosin",
        "Gentamicin",
        "Ivermectin",
        "Albendazole",
        "Sulfadiazine",
        "Sulfamethoxazole",
        "Custom Drug",
        "Withdrawal Period (days)",
        "Last Medication Date",
        "Animal Treated",
        "Common Drug Withdrawal-Period Reference",
        "Withdrawal Period (days)",
        "Applicable Animals",
        "Pig/Chicken/Cattle",
        "Pig/Chicken",
        "28 (Pig)/14 (Chicken)",
        "Pig/Cattle",
        "Pig/Cattle/Sheep",
        "Animal products slaughtered within the withdrawal period may contain drug residues, violating food-safety regulations. Withdrawal-period data are for reference only; follow the drug leaflet. Different formulations, administration routes and dosages may affect the actual withdrawal period.",
        "📚 In-Depth: Withdrawal Period Countdown",
        "Calculate the sale date from the last medication date and the withdrawal period.",
        "Observe the standard withdrawal period by drug (penicillin/tetracycline, etc.).",
        "Avoid marketing animals with excessive drug residues.",
        "Pig penicillin 28 days",
        "Last medication 2026-01-01 → Sale allowed 2026-01-29 (28-day withdrawal completed).",
        "Remaining Days",
        "There are N days left until sale is allowed; do not market or slaughter before then.",
        "Why is it important?",
        "Marketing before the withdrawal period ends causes excessive drug residues in meat, which is non-compliant and endangers safety.",
        "Withdrawal-Period Differences?",
        "It depends on drug metabolism and animal species; penicillin in pigs is about 28 days, shorter for poultry.",
        'About "Drug Withdrawal Period Countdown"',
        "⏰ Drug Withdrawal Period Countdown. " + DISCL,
    ]))

if __name__ == "__main__":
    main()
