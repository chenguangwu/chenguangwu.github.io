#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'startup')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'startup')
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
    out = {'slug': slug, 'industry': 'startup', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- index (23) ----------------
    write('index', build('index', [
        "🚀 Startup Incubation Tools",
        "Startup Incubation",
        "Startup Incubation Tools",
        "Business Plan Generator",
        "Guided entry across nine sections covering product, market and team to generate a complete business plan with export and local save, for fundraising materials and internal planning.",
        "Burn Rate Calculator",
        "Enter a startup's cash inflow and outflow to compute the monthly net consumption, cash runway and the date funds run out, for fundraising pacing and financial health monitoring.",
        "Equity Split Calculator",
        "Enter founder contribution weights to compute the equity split, supporting option pool reservation and multi-round dilution simulation for team splits, financing negotiations and equity planning.",
        "Startup Valuation Calculator",
        "Five methods to estimate a startup's valuation (pre-money), outputting a combined valuation range. Amount unit: 10,000 CNY",
        "Pitch Deck Outline Generator",
        "Based on a standard 10-page structure, guides you through filling in each page to generate a complete pitch outline, with export and local save support",
        "Startup Cost Estimate",
        "Enter startup one-off investment and monthly operating expenses by category to estimate total initial funding and early-stage cash needs, for startup budgeting and fundraising amount estimates.",
        "About \"Startup Incubation Tools\"",
        "The Startup Incubation Tools collection gathers 6 free online tools covering the common calculation, conversion and lookup needs of startup incubation scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The startup incubation tools listed on this page include (a few representative tools):",
        "These tools help you finish common startup incubation tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the startup incubation tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the startup incubation tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
