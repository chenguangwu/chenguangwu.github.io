# -*- coding: utf-8 -*-
"""对齐 EN 残留形态 ↔ zh 源文（坑 23/26）。
EN 态抽取的 `zh` 可能已被 _common/_prefix 半翻译；字典键必须是 zh 源文。
用 difflib 在「同页全部 zh 源串」中找与 EN 残留最相似的候选，
比率落在 (lo, hi) 且不等者即「形态≠源文」，须以源文为键。
用法：python3 _en-i18n/align_source.py <industry> [--dump]
"""
import json, io, glob, os, sys, difflib

IND = sys.argv[1] if len(sys.argv) > 1 else 'sports'
DUMP = '--dump' in sys.argv


def load(p):
    return json.load(io.open(p, encoding='utf-8'))['items']


def main():
    out = {}
    for f in sorted(glob.glob('_en-i18n/work/%s/*.json' % IND)):
        slug = f.split('/')[-1][:-5]
        zf = '_en-i18n/work_zh/%s/%s.json' % (IND, slug)
        if not os.path.exists(zf):
            continue
        en = load(f)
        zh = [it['zh'] for it in load(zf)]
        zset = list(dict.fromkeys(zh))
        pairs = []
        for it in en:
            e = it['zh']
            best, ratio = None, 0.0
            for z in zset:
                if z == e:
                    best, ratio = z, 1.0
                    break
                if abs(len(z) - len(e)) > max(40, len(e)):
                    continue
                r = difflib.SequenceMatcher(None, e, z).ratio()
                if r > ratio:
                    best, ratio = z, r
            if best and best != e and ratio >= 0.55:
                pairs.append((e, best, round(ratio, 2)))
        if pairs:
            out[slug] = pairs
    tot = sum(len(v) for v in out.values())
    print('形态≠源文: 页 %d / 条 %d' % (len(out), tot))
    for s in out:
        print('==', s)
        for e, z, r in out[s]:
            print('   [%.2f] EN: %s' % (r, e[:76]))
            print('          ZH: %s' % z[:76])
    if DUMP:
        json.dump(out, io.open('/tmp/en_audit/align_%s.json' % IND, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('-> /tmp/en_audit/align_%s.json' % IND)


main()
