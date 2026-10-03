#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'legal2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'legal2')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
# 与 gardening2/pruning-time 同类：术语内链（法条引用 / 高频词）被 per-tool 字典译掉后，
# 同一元素剩下的「：…」碎片脱离了行业 phrases 整串匹配，变残留。补进 EXTRA 兜底。
# ⚠️ 只补「该元素内 <strong> 标签已在 per-tool 字典里」的碎片；若 <strong> 本身没译
# （如 contract-dates 的 生效日/终止日），补碎片反而会让 phrases 整串失配、
# 把 <strong> 暴露成新残留 —— 那种情况交给 phrases 整节点命中，不要动。
EXTRA = {
    'keyword-extract': {
        '：识别《XX法》第X条等法条引用。':
            ': recognizes statutory citations such as Article X of the Law on XX.',
        '：统计文书中的高频实词（2字以上）。':
            ': counts frequent content words in the document (2 characters or more).',
        '：内置常见法律术语词典匹配，如违约、诉讼、判决、管辖等。':
            ': matches against a built-in dictionary of common legal terms, such as breach, litigation, judgment and jurisdiction.',
        '：识别「原告XX」「被告XX」「甲方XX」等主体称谓。':
            ': recognizes designations of parties such as Plaintiff XX, Defendant XX and Party A XX.',
    },
}


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
    out = {'slug': slug, 'industry': 'legal2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
