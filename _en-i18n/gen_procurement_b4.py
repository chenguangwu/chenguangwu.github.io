#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'procurement')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'procurement')
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
    out = {'slug': slug, 'industry': 'procurement', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('zhaobiao-gongkai-yaoqing-jingzheng-fangshi', build('zhaobiao-gongkai-yaoqing-jingzheng-fangshi', [
        "🛒 Bidding (Open/Invited/Competitive) Method",
        "Recommend the applicable bidding procurement method based on project amount and openness requirements.",
        "📖 View \"Bidding (Open/Invited/Competitive) Method Guide\"",
        "Amount ≥400 and open → open bidding; amount ≥400 and restricted → invited bidding; amount <400 → competitive negotiation",
        "Bidding methods match by amount and openness: large amount and must-be-open uses open bidding; large amount but restricted scope uses invited bidding; smaller amount or urgent uses competitive negotiation, balancing compliance and efficiency.",
        "Project Amount (10k CNY)",
        "Openness (1=open/0=restricted)",
        "💡 Amount ≥400 and open → open bidding; restricted → invited bidding; <400 → competitive negotiation.",
        "📚 In-Depth Analysis: Bidding (Open/Invited/Competitive) Method",
        "Open vs invited bidding price comparison: fill the estimated total cost of both methods into A and B to quantify the cost gap, assisting compliant selection.",
        "Cycle comparison of two procurement methods: fill the estimated days of open bidding and competitive negotiation to see time-cost differences.",
        "Compliance cost analysis: compare the input of different procurement methods in announcement, evaluation, and archiving steps, and choose a method that is both compliant and economical.",
        "Example: \"open bidding cost 50,000 CNY vs invited bidding cost 35,000 CNY\"",
        "A=open 50,000, B=invited 35,000: ratio (A/B)=50000/35000≈1.4286, difference=15,000.00, A as % of B=142.86%, average=42,500.00, larger=open bidding. This shows open bidding has higher compliance transparency but an estimated extra spend of about 15,000 CNY, to be weighed against amount and compliance requirements.",
        "What scenarios do open bidding and invited bidding each apply to?",
        "Per regulations such as the Government Procurement Law, open bidding applies to generic, fully competitive standardized procurement with the highest transparency; invited bidding applies to technically complex, specially required, or naturally constrained situations where procurement can only be from a limited supplier range. Specific applicable conditions are subject to current regulations and the unit's internal control system.",
        "What to watch when comparing values?",
        "A and B should be comparable values under the same comparison dimension (e.g. both 'full-process cost' or both 'average cycle days') with consistent caliber. The tool only does numerical comparison and does not judge compliance; method selection must meet statutory limits and approval processes.",
        "About \"Bidding (Open/Invited/Competitive) Method\"",
        "Bidding (Open/Invited/Competitive) Method. Free online tool, pure front-end processing, no data uploaded, protecting privacy and security.",
        "Open",
        "Invited",
    ]))
if __name__ == '__main__':
    main()
