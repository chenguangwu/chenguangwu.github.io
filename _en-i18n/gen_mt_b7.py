#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'metallurgy')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'metallurgy')
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
    out = {'slug': slug, 'industry': 'metallurgy', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-88', build('calc-88', [
        "🧮 Charge Mix Ratio Calculator",
        "Enter the target composition together with the composition and ratio of each charge material to compute the weighted average charge composition, compare it with the target after element burn-off, and support cupola melting charge planning for cast iron and cast steel.",
        "Core formula (by input variable): |(totalRatio-100)| < 0.5",
        "Alloy type",
        "Gray cast iron HT250",
        "Ductile iron QT500",
        "Malleable iron KTH350",
        "Cast steel ZG270",
        "🎯 Target composition (%)",
        "C carbon",
        "Si silicon",
        "Mn manganese",
        "🔥 Element burn-off rate (%)",
        "C burn-off",
        "Si burn-off",
        "Mn burn-off",
        "📋 Charge composition and ratio",
        "➕ Add charge material",
        "💡 Charge composition = Σ(charge composition × ratio%) ÷ total ratio; final composition = charge composition × (1 - burn-off rate); the total ratio should equal 100%.",
        "📐 Cross method (solve the ratio of two charge materials)",
        "Element % of charge A",
        "Target element %",
        "Element % of charge B",
        "The burn-off rates are empirical values: induction furnace melting burns off less, cupola melting burns off more, and the real values must be tuned to the actual process.",
        "The cross method suits adjusting a single element with two charge materials; a multi-element case requires solving a linear system of equations.",
        "📚 Deep dive: charge mix ratio calculation",
        "The charge composition is obtained as the ratio-weighted average of every charge composition, then burn-off is deducted to yield the final melt composition.",
        "Reverse-solve the pig iron, scrap and return-scratch ratios from the nominal target composition (for example HT250 or QT500).",
        "Use the cross method to get a quick two-material ratio, then iterate to correct it when more than two materials are involved.",
        "Charge mix and burn-off",
        "Charge composition = Σ(charge composition × ratio%) / total ratio; final composition = charge composition × (1 - burn-off%). Nominal target examples: gray cast iron HT250 C 3.2 / Si 2.0 / Mn 0.6; ductile iron QT500 C 3.6 / Si 2.5 / Mn 0.4; malleable iron KTH350 C 2.6 / Si 1.3 / Mn 0.5; cast steel ZG270 C 0.35 / Si 0.4 / Mn 0.6. Burn-off: C 5% / Si 15% / Mn 20%.",
        "Cross method worked example",
        "Pig iron C 4.3% and scrap steel C 0.2%, target HT250 C 3.2% (ignoring burn-off for now): ratio = (4.3-3.2):(3.2-0.2) = 1.1:3.0, so pig iron is 3.0/(1.1+3.0) = 23.4% and scrap steel is 76.6%. Then fold in Si/Mn burn-off and the ferro-alloy addition, and iterate until every element meets the target.",
        "Why compute the charge first and deduct burn-off afterwards?",
        "What the charge materials bring in is the charge composition, and easily oxidized elements (Si, Mn, C) burn off during melting, so the final melt composition = charge × (1 - burn-off); the order cannot be reversed.",
        "How should return scratch be handled?",
        "Return scratch composition is close to the nominal grade, so it can join the weighted average using its known composition; when its share is too high, watch for impurity build-up, and it still participates in the weighting during ratio calculation.",
        "About \"Charge Mix Ratio Calculator\"",
        "This tool is used for melting charge calculation of cast iron and cast steel. Enter the target alloy composition plus the composition and ratio of several charge materials (pig iron, scrap steel, return scratch, ferro-alloys and so on); it automatically computes the weighted average charge composition, applies element burn-off to give the final composition, compares it against the target, and adds the cross method for a fast two-material ratio solution.",
        "Presets for gray iron, ductile iron, malleable iron and cast steel",
        "Customizable element burn-off rates",
        "Cross method solves the ratio of two charge materials quickly",
        "Charge planning for foundry melting shops",
        "Charge cost optimization and material selection",
        "Composition deviation analysis and correction",
        "How to use the Charge Mix Ratio Calculator",
        "What does the Charge Mix Ratio Calculator do?",
        "How do I use the Charge Mix Ratio Calculator?",
        "Which scenarios suit the Charge Mix Ratio Calculator?",
        "Target carbon",
        "Target silicon",
        "Target manganese",
        "Carbon burn-off",
        "Silicon burn-off",
        "Manganese burn-off",
        "Element content of charge A",
        "Target element content",
        "Element content of charge B",
    ]))

if __name__ == '__main__':
    main()
