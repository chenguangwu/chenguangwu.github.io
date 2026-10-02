#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'logistics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'logistics')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {
    'analysis-75': {
        "品控（流程/标准/检测）机制 - 生鲜商品品质评估工具，输入外观、气味":
            "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
    },
    'analysis-76': {
        "品控（流程/标准/检测）机制 - 生鲜商品品质评估工具，输入外观、气味":
            "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
    },
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
    out = {'slug': slug, 'industry': 'logistics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
EXTRA = {
    'analysis-75': {
        "品控（流程/标准/检测）机制 - 生鲜商品品质评估工具，输入外观、气味":
            "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
    },
    'analysis-76': {
        "品控（流程/标准/检测）机制 - 生鲜商品品质评估工具，输入外观、气味":
            "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
    },
}

def main():
    write('checker-4', build('checker-4', [
        "✅ Returns Reverse Logistics Process Inspection",
        "Check the returns reverse logistics process item by item against four modules — return receiving, quality inspection, sorting and handling, and record traceability — automatically computing each module's compliance rate and the overall process maturity, and outputting an improvement checklist.",
        "Returns (reverse / inspection) process",
        "/ Returns (reverse / inspection) process",
        "Process maturity = Σpoints actually earned ÷ full score ×100%",
        "Assess process maturity",
        "Score each item by degree of execution: not established 0 points / established but incomplete 1 point / established and in execution 2 points",
        "≥90% process complete, 75-89% basically complete, 60-74% needs improvement, <60% needs rebuilding",
        "The reverse logistics return rate should be kept below 5%; if it is too high, investigate quality control problems",
        "📚 Deep dive: Returns Reverse Logistics Process Maturity Inspection",
        "After a major e-commerce promotion, self-check whether the returns handling chain (receiving, inspection, sorting, traceability) is properly covered and output an improvement checklist.",
        "Run a baseline assessment before a new warehouse or team takes over reverse logistics, and rank remediation priority by module compliance rate.",
        "Re-score during the quarterly review and use the change in compliance rate to verify whether remediation measures have landed.",
        "Scoring example for 20 key points",
        "The four modules have 20 items in total, each not established 0 points / to be completed 1 point / executed 2 points, for a full score of 40. If 12 items are executed (24 points), 5 are to be completed (5 points) and 3 are not established (0 points), the score is 29/40 = 72.5%, rated \"needs improvement\" (the 60–74% band). The tool lists the 8 items scoring below 2 points in the improvement checklist, and the 3 not-established items should be handled first.",
        "How are the rating bands defined?",
        "Compliance rate = score ÷ 40 × 100%. ≥90% process complete, 75–89% basically complete, 60–74% needs improvement, <60% needs rebuilding.",
        "What do 0 / 1 / 2 points each represent?",
        "Not established 0 points, to be completed 1 point (there is activity but it is non-standard or unrecorded), executed 2 points (there is a system and there are records). All items below 2 points automatically enter the improvement checklist.",
        "About \"Returns Reverse Logistics Process Inspection\"",
        "A returns reverse logistics process inspection tool covering four modules — return receiving, quality inspection, sorting and handling, and record traceability — with 20 key points in total, quantifying returns reverse logistics process maturity and generating an improvement checklist.",
        "Checklist-style self-inspection across the receiving / inspection / handling / traceability modules",
        "Per-module compliance rate and overall process maturity",
        "Returns process optimization for e-commerce / retail companies",
        "Reverse logistics system build-out assessment",
        "After-sales service quality improvement",
        "Supply chain management process audit",
    ]))

if __name__ == '__main__':
    main()