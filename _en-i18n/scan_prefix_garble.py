# -*- coding: utf-8 -*-
"""全站 prefix-garble 静态模拟器（只读诊断）
复刻 js/tool-i18n.js 的文本节点替换：pickEn(精确) → replaceColonLabelsAll(冒号全量) → longestPrefixKey(最长前缀)。
garble 判据：源文「不含拉丁字母」，替换结果「含拉丁且仍含汉字」⇒ 半译（前缀替了不完整词）。
"""
import json, io, re, os, glob, collections

CJK = re.compile(r'[\u4e00-\u9fff]')
LAT = re.compile(r'[A-Za-z]')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

common = json.load(io.open(os.path.join(ROOT, 'i18n/tools/en/_common.json'), encoding='utf-8'))
prefix = json.load(io.open(os.path.join(ROOT, 'i18n/tools/en/_prefix.json'), encoding='utf-8'))
# 运行时 EN_PREFIX_KEYS 按长度降序（longestPrefixKey 依赖）
PKEYS = sorted(prefix.keys(), key=len, reverse=True)
COLON_KEYS = [k for k in PKEYS if k.endswith('：')]


def simulate(key, perdict):
    if key in perdict or key in common:
        return None
    # replaceColonLabelsAll
    out = key
    changed = False
    guard = 0
    while guard < 40:
        guard += 1
        hit = None
        for k in COLON_KEYS:
            if k in out:
                hit = k; break
        if not hit:
            break
        out = out.replace(hit, prefix[hit], 1)
        changed = True
    if changed:
        return out
    for k in PKEYS:
        if len(key) >= len(k) and key.startswith(k):
            return prefix[k] + key[len(k):]
    return None


TEXT_RE = re.compile(r'>([^<>]+)<')


def main():
    files = glob.glob(os.path.join(ROOT, 'tools/**/*.html'), recursive=True)
    garble_pages = collections.defaultdict(list)
    perdict_cache = {}
    n = 0
    for fp in files:
        rel = os.path.relpath(fp, ROOT)
        m = re.match(r'tools/([a-z0-9-]+)/([a-z0-9-]+)\.html$', rel)
        if not m:
            continue
        ind, slug = m.group(1), m.group(2)
        if slug == 'index':
            continue
        dp = os.path.join(ROOT, 'i18n/tools/en/%s/%s.json' % (ind, slug))
        if dp not in perdict_cache:
            perdict_cache[dp] = json.load(io.open(dp, encoding='utf-8')).get('map', {}) if os.path.exists(dp) else {}
        perdict = perdict_cache[dp]
        try:
            s = io.open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
        n += 1
        for tm in TEXT_RE.finditer(s):
            t = tm.group(1).strip()
            if not t or not CJK.search(t):
                continue
            if LAT.search(t):      # 源文本就含拉丁 ⇒ 跳过（非纯中文源）
                continue
            res = simulate(t, perdict)
            if res and LAT.search(res) and CJK.search(res):
                garble_pages[rel].append((t, res))
    print('scanned pages', n, '| garble pages', len(garble_pages))
    tot = sum(len(v) for v in garble_pages.values())
    print('total garble strings', tot)
    # 汇总高频 garble 源文
    cnt = collections.Counter()
    for v in garble_pages.values():
        for t, r in v:
            cnt[(t, r)] += 1
    for (t, r), c in cnt.most_common(40):
        print('%3d  %s  ->  %s' % (c, t[:40], r[:60]))
    # 落盘完整清单
    with io.open('/tmp/en_audit/garble_report.txt', 'w', encoding='utf-8') as f:
        for p in sorted(garble_pages):
            for t, r in garble_pages[p]:
                f.write('%s\t%s\t%s\n' % (p, t, r))
    print('report -> /tmp/en_audit/garble_report.txt')


if __name__ == '__main__':
    main()
