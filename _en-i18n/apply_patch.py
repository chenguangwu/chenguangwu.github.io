# -*- coding: utf-8 -*-
"""EN 字典批产入库器（审计驱动 · 人工词表）
输入：_en-i18n/patches/*.json  →  {"<ind>/<slug>": {"中文原文": "English", ...}}
输出：
  - 同一中文串出现于 >=2 个工具 → i18n/tools/en/_common.json（全局兜底）
  - 仅出现于 1 个工具          → i18n/tools/en/<ind>/<slug>.json（per-tool）
硬约束：译文不得含中文；已存在的键不覆盖（保护人工校对成果），冲突计数打印。
用法: python3 _en-i18n/apply_patch.py [--dry]
"""
import json, glob, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r'[\u4e00-\u9fff]')
DRY = '--dry' in sys.argv

patches = collections.defaultdict(dict)   # (ind, slug) -> {zh: en}
occ = collections.defaultdict(set)        # zh -> {(ind,slug)}
for f in sorted(glob.glob(os.path.join(ROOT, '_en-i18n/patches/*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for key, m in d.items():
        ind, slug = key.split('/')
        for zh, en in m.items():
            patches[(ind, slug)][zh] = en
            occ[zh].add((ind, slug))

# 1) 校验译文
bad = [(zh, en) for m in patches.values() for zh, en in m.items() if CJK.search(en)]
if bad:
    print('!! 含中文译文 %d 条，已拒绝：' % len(bad))
    for zh, en in bad[:20]:
        print('   ', zh[:40], '=>', en[:40])
    for zh, en in bad:
        for k, m in patches.items():
            if m.get(zh) == en:
                del m[zh]

# 2) 分流
common_path = os.path.join(ROOT, 'i18n/tools/en/_common.json')
common = json.load(open(common_path, encoding='utf-8'))
if isinstance(common, dict) and 'map' in common:
    common = common['map']
n_common_new = 0
n_pt_new = 0
conflict = 0
per_tool = collections.defaultdict(dict)

for (ind, slug), m in patches.items():
    for zh, en in m.items():
        if len(occ[zh]) >= 2:
            if zh in common:
                conflict += 1
                continue
            common[zh] = en
            n_common_new += 1
        else:
            per_tool[(ind, slug)][zh] = en

# 3) 写 _common
if not DRY:
    with open(common_path, 'w', encoding='utf-8') as f:
        json.dump(common, f, ensure_ascii=False, indent=1)
        f.write('\n')

# 4) 写 per-tool
dirty_ind = set()
for (ind, slug), m in per_tool.items():
    if not m:
        continue
    p = os.path.join(ROOT, 'i18n/tools/en/%s/%s.json' % (ind, slug))
    if os.path.exists(p):
        obj = json.load(open(p, encoding='utf-8'))
    else:
        obj = {'slug': slug, 'industry': ind, 'name': slug, 'map': {}}
    mp = obj.setdefault('map', {})
    for zh, en in m.items():
        if zh in mp:
            conflict += 1
            continue
        mp[zh] = en
        n_pt_new += 1
    if not DRY:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.write('\n')
    dirty_ind.add(ind)

print('patch files:', len(glob.glob(os.path.join(ROOT, '_en-i18n/patches/*.json'))))
print('新增 → _common: %d（总 %d 键）' % (n_common_new, len(common)))
print('新增 → per-tool: %d（%d 个字典）' % (n_pt_new, len([1 for k in per_tool if per_tool[k]])))
print('已存在跳过（冲突）: %d' % conflict)
print('需 reindex 行业:', sorted(dirty_ind))
