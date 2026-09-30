# -*- coding: utf-8 -*-
"""对照测量：prefix 守卫(G1) / colon 位置守卫(C1) 对断词 garble 的消除量与副作用。

判据 A（MIX，断词签名）：替换结果里出现「拉丁紧邻汉字」或「汉字紧邻拉丁」。
判据 B（isg，混排）：替换结果同时含汉字与拉丁。
副作用：原规则输出「非 MIX」却在守卫下结果改变（丢掉了本来正确的翻译）。
"""
import json, io, re, glob, os, collections

CJKc = u'\u4e00-\u9fff'
CJK = re.compile(u'[%s]' % CJKc)
LAT = re.compile(r'[A-Za-z]')
MIX = re.compile(u'(?:[A-Za-z][%s]|[%s][A-Za-z])' % (CJKc, CJKc))
TEXT_RE = re.compile(r'>([^<>]+)<')

common = json.load(io.open('i18n/tools/en/_common.json', encoding='utf-8'))
prefix = json.load(io.open('i18n/tools/en/_prefix.json', encoding='utf-8'))
PKEYS = sorted(prefix.keys(), key=len, reverse=True)
COLON = [k for k in PKEYS if k.endswith(u'：')]
NONCOLON = [k for k in PKEYS if not k.endswith(u'：')]

perdict = {}


def pdict(dp):
    if dp not in perdict:
        perdict[dp] = (json.load(io.open(dp, encoding='utf-8')).get('map', {})
                       if os.path.exists(dp) else {})
    return perdict[dp]


def collect():
    texts = set()
    for fp in glob.glob('tools/**/*.html', recursive=True):
        rel = os.path.relpath(fp, '.')
        m = re.match(r'tools/([a-z0-9-]+)/([a-z0-9-]+)\.html$', rel)
        if not m or m.group(2) == 'index':
            continue
        dp = 'i18n/tools/en/%s/%s.json' % (m.group(1), m.group(2))
        pd = pdict(dp)
        try:
            s = io.open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
        for tm in TEXT_RE.finditer(s):
            t = tm.group(1).strip()
            if not t or not CJK.search(t) or LAT.search(t):
                continue
            texts.add((dp, t))
    return texts


def run(t, pd, gp, gc):
    """gp=prefix 守卫（键后紧邻汉字则跳过）；gc=colon 守卫（键前紧邻汉字则跳过）。"""
    if t in pd or t in common:
        return None
    out, ch, g = t, False, 0
    while g < 40:
        g += 1
        hit, hi = None, -1
        for k in COLON:
            i = out.find(k)
            if i >= 0:
                if gc and i > 0 and CJK.match(out[i - 1]):
                    continue
                hit, hi = k, i
                break
        if hit is None:
            break
        out = out[:hi] + prefix[hit] + out[hi + len(hit):]
        ch = True
    if ch:
        return out
    for k in NONCOLON:
        if len(t) >= len(k) and t.startswith(k):
            if gp and len(t) > len(k) and CJK.match(t[len(k)]):
                continue
            return prefix[k] + t[len(k):]
    return None


def main():
    texts = collect()
    print('distinct (dict,text) pairs:', len(texts))
    variants = [('base', False, False), ('G1', True, False),
                ('C1', False, True), ('G1C1', True, True)]
    mix = collections.Counter()
    isg = collections.Counter()
    results = {}
    for dp, t in texts:
        pd = pdict(dp)
        rs = {}
        for tag, gp, gc in variants:
            r = run(t, pd, gp, gc)
            rs[tag] = r
            if r and MIX.search(r):
                mix[tag] += 1
            if r and LAT.search(r) and CJK.search(r):
                isg[tag] += 1
        results[(dp, t)] = rs
    print('\n%-8s %8s %8s' % ('variant', 'MIX', 'mixed'))
    for tag, _, _ in variants:
        print('%-8s %8d %8d' % (tag, mix[tag], isg[tag]))
    # 副作用：base 输出非 MIX，但守卫下改变
    coll = collections.Counter()
    samples = collections.defaultdict(list)
    for (dp, t), rs in results.items():
        b = rs['base']
        if b is None or MIX.search(b):
            continue
        for tag in ('G1', 'C1', 'G1C1'):
            if rs[tag] != b:
                coll[tag] += 1
                if len(samples[tag]) < 15:
                    samples[tag].append((os.path.basename(dp), t, b, rs[tag]))
    print('\nside-effects (base non-MIX yet changed):')
    for tag in ('G1', 'C1', 'G1C1'):
        print('  %-6s %d' % (tag, coll[tag]))
    for tag in ('G1', 'C1'):
        print('\n--- %s side-effect samples' % tag)
        for a, b_, c, d in samples[tag]:
            print('  %s | %s\n      cur: %s\n      new: %s' % (a, b_[:30], str(c)[:60], str(d)[:60]))


if __name__ == '__main__':
    main()
