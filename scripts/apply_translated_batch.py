#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一批人工/AI 翻译结果落盘到 phrases 数据文件（每批复用）。

分流规则
--------
- 短语出现在 >= min-common 个行业 → 写入 i18n/tools/common-phrases.json（全站加载一次）
- 否则 → 写入该短语出现的各行业 -phrases.json（行业独有）
- 清单里查不到行业信息 → 归入 common

写入策略（保证 diff 最小 + 幂等）
------------------------------
- 既有文件：保留原有键顺序，只追加新键 / 更新值变化，**不重排**（重排会造成全文件大 diff）
- 新文件：按键排序写入
- 内容一致则不写盘（幂等，避免每次运行产生无意义变更）

用法
----
    python3 scripts/apply_translated_batch.py --batch /tmp/batch1.json
    python3 scripts/apply_translated_batch.py --batch /tmp/batch1.json --min-common 3
"""
import argparse
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, 'i18n', 'tools')
PENDING = os.path.join(ROOT, 'phrases-pending.json')


def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, OSError, ValueError):
        return None


def save(path, data, sort_keys):
    if sort_keys:
        data = dict(sorted(data.items()))
    text = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if f.read() == text:
                return False          # 内容一致 → 不写盘（幂等）
    except (IOError, OSError):
        pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', required=True, help='翻译结果 JSON：{中文: 英文}')
    ap.add_argument('--min-common', type=int, default=3,
                    help='出现在 >=N 个行业则归入 common（默认 3）')
    ap.add_argument('--pending', default=PENDING)
    args = ap.parse_args()

    batch = load_json(args.batch)
    if not isinstance(batch, dict) or not batch:
        print('ERROR: 批次文件为空或格式不对: %s' % args.batch, file=sys.stderr)
        return 1

    pending = load_json(args.pending) or []
    ind_of = {x['zh']: list((x.get('industries') or {}).keys()) for x in pending}

    common = {}
    by_ind = defaultdict(dict)
    unknown = 0
    for zh, en in batch.items():
        if not zh or not en or zh == en:
            continue
        inds = ind_of.get(zh, [])
        if not inds:
            common[zh] = en
            unknown += 1
        elif len(inds) >= args.min_common:
            common[zh] = en
        else:
            for ind in inds:
                by_ind[ind][zh] = en

    written_common = 0
    p = os.path.join(I18N_DIR, 'common-phrases.json')
    data = load_json(p) or {}
    existed = os.path.exists(p)
    changed = False
    for zh, en in common.items():
        if data.get(zh) != en:
            data[zh] = en
            changed = True
    if common and (changed or not existed):
        if save(p, data, sort_keys=not existed):
            written_common = 1

    written_ind = 0
    total_ind_entries = 0
    for ind, mapping in by_ind.items():
        p = os.path.join(I18N_DIR, ind + '-phrases.json')
        existed = os.path.exists(p)
        data = load_json(p) or {}
        changed = False
        for zh, en in mapping.items():
            if data.get(zh) != en:
                data[zh] = en
                changed = True
        if changed or not existed:
            if save(p, data, sort_keys=not existed):
                written_ind += 1
            total_ind_entries += len(mapping)

    print('本批翻译条目: %d' % len(batch))
    print('  归入 common-phrases.json : %d 条' % len(common))
    print('  归入行业文件            : %d 个文件 / %d 条次' % (len(by_ind), sum(len(m) for m in by_ind.values())))
    if unknown:
        print('  清单中无行业信息（归入 common）: %d 条' % unknown)
    print('写盘文件: common %d 个, 行业 %d 个' % (written_common, written_ind))
    return 0


if __name__ == '__main__':
    sys.exit(main())
