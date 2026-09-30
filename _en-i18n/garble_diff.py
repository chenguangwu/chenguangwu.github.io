# -*- coding: utf-8 -*-
"""对照 before/after 真机 garble 探针结果，输出修复量、残留清单与「新增残留」（覆盖损失）清单。

用法：python3 _en-i18n/garble_diff.py before.json after.json
"""
import json, io, sys, collections

ADJ = None


def is_adj(s):
    # 拉丁紧邻汉字 或 汉字紧邻拉丁（无空格）
    for i in range(len(s) - 1):
        a, b = s[i], s[i + 1]
        ca = ('a' <= a.lower() <= 'z')
        cb = ('a' <= b.lower() <= 'z')
        ha = u'\u4e00' <= a <= u'\u9fff'
        hb = u'\u4e00' <= b <= u'\u9fff'
        if (ca and hb) or (ha and cb):
            return True
    return False


def load(p):
    d = json.load(io.open(p, encoding='utf-8'))
    out = {}
    for k, v in d.items():
        if not isinstance(v, list):
            continue
        out[k] = set(x['t'] for x in v if isinstance(x, dict) and 't' in x)
    return out


def main():
    before = load(sys.argv[1])
    after = load(sys.argv[2])
    b_all = set()
    a_all = set()
    b_adj, a_adj = set(), set()
    for p, ss in before.items():
        for s in ss:
            b_all.add(s)
            if is_adj(s):
                b_adj.add(s)
    for p, ss in after.items():
        for s in ss:
            a_all.add(s)
            if is_adj(s):
                a_adj.add(s)
    print('pages with garble/mixed: before=%d after=%d' % (len(before), len(after)))
    print('distinct mixed strings : before=%d after=%d' % (len(b_all), len(a_all)))
    print('   of which ADJ(broken) : before=%d after=%d' % (len(b_adj), len(a_adj)))
    fixed = b_adj - a_adj
    print('\nfixed broken-word strings: %d' % len(fixed))
    for s in sorted(fixed)[:25]:
        print('  -', s[:90])
    new = a_all - b_all
    print('\nNEW mixed strings (coverage loss candidates): %d' % len(new))
    for s in sorted(new)[:40]:
        print('  +', s[:100])
    newadj = a_adj - b_adj
    print('\nNEW broken-word strings: %d' % len(newadj))
    for s in sorted(newadj)[:20]:
        print('  !', s[:100])


if __name__ == '__main__':
    main()
