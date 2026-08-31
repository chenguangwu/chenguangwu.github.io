#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO-D 残留重复/薄内容识别（仅识别，不改文件）。

数据驱动依据：复用 _build.py 权威质量分级（json/tools.json 的 quality 字段）
与跨行业名称相似度，产出待确认的候选清单，供后续人工决策合并/noindex/补充。

- 薄内容：当前 quality 分布（C 级即薄内容）。
- 重复功能：同 industry 内两两名称 difflib 相似度 >= 阈值 的对。
输出：json/seo_d_dup_candidates.json + 终端摘要。
"""
import json, difflib, collections, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRESH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.82

d = json.load(open(os.path.join(ROOT, 'json', 'tools.json'), encoding='utf-8'))
print('工具总数:', len(d))

# ---- 1. 质量分级分布（薄内容）----
q = collections.Counter(t['quality'] for t in d)
print('质量分级:', dict(q))
c = [t for t in d if t['quality'] == 'C']
print('C 级(薄内容)数量:', len(c))
if c:
    by_ind = collections.Counter(t['industry'] for t in c)
    print('  C级行业分布 Top10:', by_ind.most_common(10))

# ---- 2. 同行业名称相似度重复对 ----
by_ind = collections.defaultdict(list)
for t in d:
    by_ind[t['industry']].append(t)

# 末尾后缀词（中/英），用于判定「仅差后缀=高置信重复」
SUFFIXES = ['计算器', '生成器', '校验器', '检查器', '转换器', '速查表', '自评问卷',
            '估算器', '评估器', '分析器', '测试器', '速查', '自评', '分级器',
            '风险评分', '风险', '指数估算', '估算', '评估', '测试', '计算',
            '生成', '校验', '检查', '转换', '查询', '分析', '分级', '指数', '问卷',
            '表', '器',
            'calculator', 'generator', 'converter', 'validator', 'checker',
            'tester', 'assessor', 'estimator', 'analyzer', 'tool']

def strip_suffix(name):
    s = name
    changed = True
    while changed:
        changed = False
        for suf in SUFFIXES:
            if s.lower().endswith(suf.lower()) and len(s) > len(suf):
                s = s[:len(s) - len(suf)]
                changed = True
                break
    return s.strip()

cands = []
for ind, items in by_ind.items():
    n = len(items)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = items[i]['name'], items[j]['name']
            if a == b:
                r = 1.0
            else:
                r = difflib.SequenceMatcher(None, a, b).ratio()
            if r >= THRESH:
                sa, sb = strip_suffix(a), strip_suffix(b)
                conf = 'high' if (sa and sa == sb) else 'review'
                cands.append({
                    'ratio': round(r, 3),
                    'industry': ind,
                    'name_a': a, 'path_a': items[i]['path'],
                    'name_b': b, 'path_b': items[j]['path'],
                    'conf': conf,
                    'stripped_a': sa, 'stripped_b': sb,
                })
cands.sort(key=lambda x: (-x['ratio']))
print('\n名称相似度 >= %.2f 的候选重复对: %d' % (THRESH, len(cands)))

# 去重：每个 path 最多出现在一次候选（取最高相似度）
seen = set()
dedup = []
for c in cands:
    key = frozenset((c['path_a'], c['path_b']))
    if key & seen:
        continue
    seen |= key
    dedup.append(c)
print('去重后候选对: %d' % len(dedup))
high = [c for c in dedup if c['conf'] == 'high']
print('  其中「仅差后缀、高置信重复」: %d 对' % len(high))
print('  「需人工确认(差核心限定词)」: %d 对' % (len(dedup) - len(high)))

out = os.path.join(ROOT, 'json', 'seo_d_dup_candidates.json')
json.dump({'threshold': THRESH, 'total_tools': len(d),
           'quality': dict(q),
           'high_conf_dups': high, 'review_dups': [c for c in dedup if c['conf'] != 'high']},
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入', out)

print('\n--- 高置信重复（建议合并，保留规范命名方）---')
for c in high:
    print('  %.3f [%s] %s  <=>  %s' % (c['ratio'], c['industry'], c['name_a'], c['name_b']))
    print('         %s  |  %s' % (c['path_a'], c['path_b']))
