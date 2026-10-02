#!/usr/bin/env python3
# gen_clinical_nursing_head.py — shared head for clinical-nursing batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'clinical-nursing')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'clinical-nursing')
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
    out = {'slug': slug, 'industry': 'clinical-nursing', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('generator-pressure', build('generator-pressure', [
        "Pressure-Injury (Stage) Description Generator",
        "All stages",
        'View "Pressure-Injury (Stage) Description Generator User Guide"',
        "Pressure injury staged by NPIAP/EPUAP: Stage 1 = non-blanchable erythema; Stage 2 = partial-thickness loss or serous blister; Stage 3 = full-thickness skin loss with visible fat not to fascia; Stage 4 = full-thickness tissue loss with exposed fascia/muscle/bone; Unstageable = wound covered by eschar, judge after debridement; Deep tissue injury = persistent non-blanchable purple/maroon area.",
        "📚 In-Depth: Pressure-Injury (Stage) Description Generator",
        "Record the difference between Stage 1 (non-pale erythema) and Stage 2 (partial-thickness loss).",
        "Stages 3-4 generate structured descriptions by tissue-loss depth and necrosis extent.",
        "Suspected deep tissue injury and unstageable are marked by covering features.",
        "Review a sacral Stage 2 description",
        "Input stage=2, site=sacrum; tool generates partial-thickness loss, pink granulation-bed text, matching the assessment.",
        "Can this tool replace the physician's diagnosis?",
        "No; it is a description template. Staging follows wound-specialist assessment.",
        "How to tell Stage 1 from Stage 2?",
        "Stage 1: intact skin with non-fading erythema; Stage 2: broken to dermis. Key is skin integrity.",
        "Why is deep tissue injury hard to judge?",
        "Epidermis may be intact while subcutaneous tissue is necrotic; keep watching color, temperature and firmness.",
        "About the Pressure-Injury (Stage) Description Generator",
        "Generates NPUAP-stage pressure-injury description text to aid nursing records.",
        "Stages 1-4 templates",
        "Unstageable/deep marking",
        "Structured output",
        "Stages 1-2 integrity",
        "Stages 3-4 tissue loss",
        "Deep injury by covering",
    ]))

if __name__ == "__main__":
    main()
