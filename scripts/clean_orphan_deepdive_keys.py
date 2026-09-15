#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 content_deepdive.json 的无源孤儿键（A 项批2-⑨）。

判定：键在 json/tools.json 中找不到对应工具页 ⇒ 该页面已迁移到其它分类。
删除前逐条核对"新键"是否已持有等同或更全的内容，确认无损才删；
若新键缺失或内容更少，则跳过并报告，绝不静默丢内容。

其中 finance/lottery-odds-calculator 为已下架的博彩类工具（内容合规红线），
无对应页面且不得保留入口，直接删除。
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD_PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

# 孤儿键 → 目标键（页面迁移后的真实归属），None 表示页面已下架
PAIRS = [
    ('wedding/budget-planner', 'wedding/wedding-budget-planner'),
    ('martial-arts/convert-29', 'sports/convert-29'),
    ('martial-arts/assessor-hardness', 'sports/assessor-hardness'),
    ('sports-event/stats-11', 'sports/stats-11'),
    ('sports-event/assessor-csat', 'sports/assessor-csat'),
    ('warehouse/analysis-cycle-1', 'logistics/analysis-cycle-1'),
    ('warehouse/analysis-report', 'logistics/analysis-report'),
    ('livestream/analysis-70', 'ecommerce/analysis-70'),
    ('livestream/analysis-71', 'ecommerce/analysis-71'),
    ('timber/analysis-cost-price', 'woodwork/analysis-cost-price'),
    ('timber/detector-37', 'woodwork/detector-37'),
    ('municipal/calc-power-spacing', 'general/calc-power-spacing'),
    ('municipal/checker-2', 'general/checker-2'),
    ('municipal/checker-spacing', 'general/checker-spacing'),
    ('yoga/analysis-retention', 'fitness/analysis-retention'),
    ('yoga/assessor-64', 'fitness/assessor-64'),
    ('landscape/analysis-23', 'life/analysis-23'),
    ('landscape/cycle-pruning-lawn', 'life/cycle-pruning-lawn'),
    ('finance/lottery-odds-calculator', None),  # 博彩类，已下架
    ('knowledge/assessor-27', 'edu/assessor-27'),
    ('it/git-cheatsheet', None),   # 页面已不存在
    ('it/calc-6', None),           # 页面已不存在
    ('it/sn-generator', None),     # 序列号生成器：内容合规红线，页面已下架
]


def size(v):
    if not v:
        return (0, 0, 0, 0)
    return (1, len(v.get('scenarios') or []), len(v.get('examples') or []), len(v.get('faqs') or []))


def has_page(slug):
    cat, base = slug.split('/', 1)
    return os.path.exists(os.path.join(ROOT, 'tools', cat, base + '.html'))


def main(apply=False):
    DD = json.load(open(DD_PATH, encoding='utf-8'))
    tools = json.load(open(os.path.join(ROOT, 'json', 'tools.json'), encoding='utf-8'))
    live = set()
    for t in tools:
        u = t.get('url') or ''
        if not u.startswith('tools/'):
            continue
        base = u.split('/')[-1].replace('.html', '')
        ind = t.get('industry') or ''
        if ind and base:
            live.add(ind + '/' + base)

    safe, skip = [], []
    for orph, tgt in PAIRS:
        if orph not in DD:
            skip.append((orph, '键已不存在'))
            continue
        if orph in live:
            skip.append((orph, '仍有对应页面，非孤儿'))
            continue
        if tgt is None:
            if has_page(orph):
                skip.append((orph, '页面仍存在'))
                continue
            safe.append((orph, '页面已下架（博彩类，红线）'))
            continue
        vt = DD.get(tgt)
        if not vt:
            skip.append((orph, '目标键 %s 缺失，需先迁移内容' % tgt))
            continue
        so, st = size(DD[orph]), size(vt)
        if st >= so:
            safe.append((orph, '目标键 %s 内容等同或更全 %s >= %s' % (tgt, st, so)))
        else:
            skip.append((orph, '目标键内容更少 %s < %s，需先迁移' % (st, so)))

    print('可安全删除 %d 条：' % len(safe))
    for o, why in safe:
        print('  DEL %-40s %s' % (o, why))
    if skip:
        print('跳过 %d 条：' % len(skip))
        for o, why in skip:
            print('  SKIP %-40s %s' % (o, why))
    if apply and safe:
        for o, _ in safe:
            del DD[o]
        cur = open(DD_PATH, encoding='utf-8').read()
        new = json.dumps(DD, ensure_ascii=False, indent=1)
        if cur.endswith('\n'):
            new += '\n'
        open(DD_PATH, 'w', encoding='utf-8').write(new)
        print('已删除 %d 条并落盘' % len(safe))
    else:
        print('（dry-run）')


if __name__ == '__main__':
    main('--apply' in sys.argv)
