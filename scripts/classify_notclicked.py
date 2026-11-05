#!/usr/bin/env python3
"""聚合 scripts/interaction_probe.js 的分桶输出并做一致性断言（唯一数据源，禁止第二套字段）。

  python3 scripts/classify_notclicked.py --probe A.json --probe2 B.json \
      --out /tmp/notclicked-new.json --old /tmp/notclicked-653-classified.json --md /tmp/notclicked-new.md

- 分桶规则归探针所有；本脚本只聚合、断言（自己按同一规则复算一遍，必须与探针 bucket 完全一致）。
- --probe2 用于一致性断言：同页两次运行，分桶相关字段必须一致，否则 exit 1。
"""
import argparse
import collections
import json
import os
import sys

FIELDS = [
    'changedAll', 'changedByInputText', 'changedBySearch', 'changedByNonText',
    'changedBySelect', 'changedByRangeColor', 'changedByFile', 'changedByClick',
]


def load(path):
    doc = json.load(open(path, encoding='utf-8'))
    return {r['path']: r for r in doc.get('pages', []) if r.get('path')}


def derive(r):
    """与 interaction_probe.js 里的分桶规则逐条对应（用于断言，不是第二数据源）。"""
    if r.get('changedByInputText') or r.get('changedBySearch'):
        return 'B'
    if r.get('changedByNonText'):
        return 'C'
    if r.get('clickTargets') and any(c.get('kind') == 'button' for c in r['clickTargets']):
        return 'A'
    if (r.get('entityAdd') or {}).get('grew'):
        return 'D-a'
    if r.get('changedByOtherButton'):
        return 'D-a'
    return 'D-b'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--probe', required=True)
    ap.add_argument('--probe2', default='')
    ap.add_argument('--out', required=True)
    ap.add_argument('--old', default='')
    ap.add_argument('--md', default='')
    args = ap.parse_args()

    a = load(args.probe)
    b = load(args.probe2) if args.probe2 else {}

    diffs = []
    for f in sorted(set(a) & set(b)):
        ra, rb = a[f], b[f]
        for k in FIELDS:
            if ra.get(k) != rb.get(k):
                diffs.append((f, k, ra.get(k), rb.get(k)))
        ea = (ra.get('entityAdd') or {}).get('grew')
        eb = (rb.get('entityAdd') or {}).get('grew')
        if ea != eb:
            diffs.append((f, 'entityAdd.grew', ea, eb))
        if len(ra.get('fields') or []) != len(rb.get('fields') or []):
            diffs.append((f, 'fieldCount', len(ra.get('fields') or []), len(rb.get('fields') or [])))
        if ra.get('bucket') != rb.get('bucket'):
            diffs.append((f, 'bucket', ra.get('bucket'), rb.get('bucket')))
    common = len(set(a) & set(b))
    if diffs:
        print('一致性断言失败：%d 处不一致（同页两次运行）' % len(diffs))
        for d in diffs[:20]:
            print('  %s | %s: %r vs %r' % d)
        sys.exit(1)

    # 探针 bucket 必须与规则复算一致（防止探针内部两套判据）
    mismatch = [f for f, r in a.items() if not r.get('errors') and derive(r) != r.get('bucket')]
    if mismatch:
        print('分桶规则不一致：%d 页（探针 bucket 与字段复算不符）' % len(mismatch))
        for f in mismatch[:10]:
            print('  %s 探针=%s 复算=%s' % (f, a[f].get('bucket'), derive(a[f])))
        sys.exit(1)

    pages = []
    for f, r in sorted(a.items()):
        if r.get('errors'):
            continue
        pages.append({
            'file': f,
            'industry': f.split('/')[1] if len(f.split('/')) > 1 else '?',
            'bucket': r.get('bucket'),
            'sub': r.get('sub'),
            'textInputs': len([x for x in (r.get('fields') or []) if x.get('type') not in ('select', 'range', 'color', 'checkbox', 'radio', 'file', 'search')]),
            'searchInputs': len([x for x in (r.get('fields') or []) if x.get('type') == 'search']),
            'selectInputs': len([x for x in (r.get('fields') or []) if x.get('type') == 'select']),
            'fileInputs': len([x for x in (r.get('fields') or []) if x.get('type') == 'file']),
            'changedAll': bool(r.get('changedAll')),
            'changedByInputText': bool(r.get('changedByInputText')),
            'changedBySearch': bool(r.get('changedBySearch')),
            'changedByNonText': bool(r.get('changedByNonText')),
            'changedByClick': bool(r.get('changedByClick')),
            'changedByOtherButton': r.get('changedByOtherButton'),
            'entityAdd': (r.get('entityAdd') or {}).get('grew', False),
            'primaryButton': next((c.get('label') for c in (r.get('clickTargets') or []) if c.get('kind') == 'button'), None),
            'drivers': [(x.get('type') or '?') + ('#' + x.get('id') if x.get('id') else '') for x in (r.get('changedByField') or []) if x.get('changed')][:6],
        })

    totals = collections.Counter(p['bucket'] for p in pages)
    out = {
        'generated': __import__('datetime').datetime.now().isoformat(timespec='seconds'),
        'source': args.probe,
        'consistency': {'checkedPages': common, 'mismatches': len(diffs)},
        'criteria': {
            'B': '全填基线后逐字段改值（含 type=search）任一改变结果签名（可见文本≤6000 字 + 只读结果框 + canvas/svg 的 FNV 哈希）',
            'C': '文本/搜索改值无变化，但 select/file/range/color/复选/画布改变结果 ⇒ 控件驱动',
            'A': '改值无变化且存在语义主按钮 ⇒ 真需点击（含「加载即算」点击前后签名相同的页）',
            'D-a': '无主按钮，但「填表→添加」列表增长或其它按钮点击后结果变化 ⇒ 需多步/预设',
            'D-b': '无 select/file/canvas/按钮可改变结果 ⇒ 无可驱动交互（待人工确认是否缺陷）',
        },
        'totals': dict(totals),
        'pages': pages,
    }

    matrix = {}
    changed = []
    if args.old and os.path.exists(args.old):
        old = json.load(open(args.old, encoding='utf-8'))
        old_pages = {p['file']: p for p in (old.get('pages') or [])}
        # 旧版把 D 家族记成一个桶、子类写在 sub（"D-a …" / "D-b …"）；新探针直接给 D-a/D-b。
        # 归一后再比，否则矩阵里会把「同族子类」误算成换桶。
        for op in old_pages.values():
            if op.get('bucket') == 'D' and isinstance(op.get('sub'), str):
                if op['sub'].startswith('D-a'):
                    op['bucket'] = 'D-a'
                elif op['sub'].startswith('D-b'):
                    op['bucket'] = 'D-b'
        m = collections.Counter()
        for p in pages:
            op = old_pages.get(p['file'])
            if not op:
                continue
            m['%s→%s' % (op.get('bucket'), p['bucket'])] += 1
            if op.get('bucket') != p['bucket']:
                changed.append({'file': p['file'], 'from': op.get('bucket'), 'to': p['bucket'], 'reason': p['sub'], 'oldSub': op.get('sub')})
        matrix = dict(sorted(m.items()))
        out['migration'] = {'matrix': matrix, 'changedPages': changed}
        out['totals']['old'] = dict(collections.Counter(op.get('bucket') for op in old_pages.values()))

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('分桶完成：%d 页 → %s' % (len(pages), args.out))
    print('分布：' + ' / '.join('%s %d' % (k, v) for k, v in sorted(totals.items())))
    if matrix:
        print('迁移：' + ' / '.join('%s %d' % (k, v) for k, v in matrix.items()))
        print('换桶页数：%d' % len(changed))

    if args.md:
        L = ['# not-clicked 分桶（探针直出 + 聚合断言）', '', '- 页数：**%d**' % len(pages),
             '- 一致性断言：同页两次运行检查 **%d** 页，不一致 **%d** 处' % (common, len(diffs)), '', '## 分布', '', '| 桶 | 页数 |', '|---|---|']
        L += ['| %s | %d |' % (k, v) for k, v in sorted(totals.items())]
        if matrix:
            L += ['', '## 迁移矩阵（旧→新）', '', '| 迁移 | 页数 |', '|---|---|']
            L += ['| %s | %d |' % (k, v) for k, v in matrix.items()]
            L += ['', '### 换桶明细（%d 页）' % len(changed), '', '| 页面 | 旧 | 新 | 新判据（字段派生） |', '|---|---|---|---|']
            L += ['| `%s` | %s | **%s** | %s |' % (c['file'], c['from'], c['to'], c['reason']) for c in changed]
        open(args.md, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        print('报告 → %s' % args.md)


if __name__ == '__main__':
    main()
