#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性诊断：统计当前 zh_en_dict 引擎对全量工具名/描述的干净英文覆盖率，
并挖掘残留中文片段（最长匹配 DOMAIN 后剩余的原子中文词）的高频词，供扩充词典。"""
import json, os, sys, re
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from zh_en_dict import translate_name, translate_text, _ZH_RUN, DOMAIN, TYPE_SUFFIX  # noqa: E402

SI = os.path.join(ROOT, 'json', 'search-index.json')
si = json.load(open(SI, encoding='utf-8'))

names = [t.get('name') or t.get('n') or '' for t in si]
descs = [t.get('desc') or t.get('d') or '' for t in si]

# 覆盖率
def clean_rate(texts, fn):
    tot = 0; clean = 0
    for tx in texts:
        if not tx: continue
        tot += 1
        out = fn(tx)
        if out and not _ZH_RUN.search(out):
            clean += 1
    return tot, clean

nt, nc = clean_rate(names, translate_name)
dt, dc = clean_rate(descs, translate_text)
print('NAME  total=%d clean=%d (%.1f%%)' % (nt, nc, 100.0*nc/nt))
print('DESC  total=%d clean=%d (%.1f%%)' % (dt, dc, 100.0*dc/dt))

# 真实生词挖掘：对原始名做 DOMAIN 最长匹配切分，收集未覆盖的中文原子词
SUF = set(z for z, _ in TYPE_SUFFIX)
def unknown_atoms(text):
    atoms = []
    for run in re.findall(r'[一-鿿]+', text):
        # 先剥掉类型后缀
        r = run
        for s in sorted(SUF, key=len, reverse=True):
            if r.endswith(s):
                r = r[: -len(s)]
                break
        j = 0; buf = ''
        while j < len(r):
            matched = False
            for k in sorted(DOMAIN, key=len, reverse=True):
                if r.startswith(k, j):
                    j += len(k); matched = True; break
            if not matched:
                buf += r[j]; j += 1
        if buf:
            atoms.append(buf)
    return atoms

residue = Counter()
for tx in names:
    if not tx: continue
    for a in unknown_atoms(tx):
        residue[a] += 1
print('\n--- 工具名真实未覆盖中文原子词 Top 80 ---')
for w, c in residue.most_common(80):
    print('%-14s %d' % (w, c))
