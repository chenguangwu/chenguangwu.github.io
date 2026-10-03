#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'parenting')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'parenting')
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
    out = {'slug': slug, 'industry': 'parenting', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- index (23) ----------------
    write('index', build('index', [
        "👶 Parenting and Baby Tools",
        "Parenting and Baby",
        "Parenting and Baby Tools",
        "Pumping Plan Calculator",
        "The Pumping Plan Calculator is a free online parenting and baby tool: wondering how to pump after returning to work without the chaos? Enter the working hours and the baby's age in months, and following the \"pump once every 3-4 hours\" principle it gives the number of daily pumping sessions, the interval and the per-session and total volume. It runs entirely in the browser, uploads no data and needs no registration, so you can...",
        "Formula Mixing Calculator",
        "The Formula Mixing Calculator is a free online parenting and baby tool: do not mix formula by feel. Enter the target milk volume and the can's mixing ratio (water per scoop), and it automatically computes the scoops and water needed, avoiding formula that is too strong or too weak. It runs entirely in the browser, uploads no data and needs no registration, so just open a browser to use it.",
        "Baby Feeding Amount Estimator",
        "The Baby Feeding Amount Estimator is a free online parenting and baby tool, and the question new parents ask most is how much per feeding. Based on age in months and weight, and combining \"daily milk volume = approx. weight x 150 ml/kg\" with the age reference values, it gives the per-feeding and daily volume ranges. It runs entirely in the browser, uploads no data and needs no...",
        "Diaper Usage Estimator",
        "The Diaper Usage Estimator is a free online parenting and baby tool: the biggest risk when stockpiling diapers is buying the wrong size or too many. Look up the reference daily count by age in months, enter the unit price, and it automatically computes the monthly quantity and cost to help you plan purchases. It runs entirely in the browser, uploads no data and needs no registration, so just open a browser to use it.",
        "Child Growth Chart",
        "Enter the age, gender, height, weight and head circumference of a child aged 0-5, and compare against WHO growth standard curves to assess development percentiles and growth trends. Used for routine child health monitoring and developmental delay screening.",
        "Baby Feeding Plan",
        "The Baby Feeding Plan tool generates a scientifically sound feeding plan from the age in months (frequency, milk volume, solid introduction), helping parents record and schedule infant feeding for everyday parenting management.",
        "About \"Parenting and Baby Tools\"",
        "The Parenting and Baby Tools collection gathers 6 free online tools covering the common calculation, conversion and lookup needs of parenting and baby scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The parenting and baby tools listed on this page include (a few representative tools):",
        "These tools help you finish common parenting and baby tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the parenting and baby tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the parenting and baby tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
