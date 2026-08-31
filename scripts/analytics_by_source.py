#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把流量数据按来源（bing / clarity）拆开统计。

为什么要拆
----------
Bing Webmaster 的 impressions 是**搜索结果展示次数**，
Microsoft Clarity 的 impressions 是**页面会话/浏览类指标**，
两者口径不同，直接相加会炮制出没有意义的数字，进而误判页面热度。
analytics_traffic_merged.csv 为方便排序做了合并，本脚本提供分来源的明细视图。

产出
----
analytics_traffic_by_source.csv
    page, source, impressions, clicks, ctr, position, records
    每个 URL × 来源 一行，ctr 由该来源自身的 clicks/impressions 计算。

同时打印交叉摘要：只有单一来源有数据的 URL 数、两源都有的 URL 数，
以及两源展示量差异最大的页面（最容易被"相加"误判的那些）。

用法
----
    python3 scripts/analytics_by_source.py
"""
import csv
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'analytics_traffic_by_source.csv')

SOURCES = {
    'bing': os.path.join(ROOT, 'bing_traffic_export.csv'),
    'clarity': os.path.join(ROOT, 'clarity_traffic_export.csv'),
}


def norm_page(p):
    p = (p or '').strip()
    if not p:
        return ''
    if not p.startswith('http'):
        return ''
    return p


def main():
    # (page, source) -> agg
    agg = defaultdict(lambda: {'impressions': 0.0, 'clicks': 0.0, 'pos_sum': 0.0, 'pos_n': 0, 'records': 0})

    for source, fp in SOURCES.items():
        if not os.path.isfile(fp):
            print('[skip] 缺少 %s' % fp)
            continue
        with open(fp, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                page = norm_page(r.get('page', ''))
                if not page:
                    continue
                try:
                    imp = float(r.get('impressions') or 0)
                    clk = float(r.get('clicks') or 0)
                    pos = float(r.get('position') or 0)
                except ValueError:
                    continue
                a = agg[(page, source)]
                a['impressions'] += imp
                a['clicks'] += clk
                a['records'] += 1
                if pos > 0:
                    a['pos_sum'] += pos * imp if imp else pos
                    a['pos_n'] += imp if imp else 1

    rows = []
    for (page, source), a in agg.items():
        ctr = (a['clicks'] / a['impressions']) if a['impressions'] else 0.0
        pos = (a['pos_sum'] / a['pos_n']) if a['pos_n'] else 0.0
        rows.append({
            'page': page,
            'source': source,
            'impressions': int(a['impressions']),
            'clicks': int(a['clicks']),
            'ctr': '%.6f' % ctr,
            'position': '%.2f' % pos,
            'records': a['records'],
        })
    rows.sort(key=lambda r: (-r['impressions'], r['page'], r['source']))

    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['page', 'source', 'impressions', 'clicks', 'ctr', 'position', 'records'])
        w.writeheader()
        w.writerows(rows)
    print('已写出 %s（%d 行）' % (os.path.relpath(OUT, ROOT), len(rows)))

    # 交叉摘要
    by_page = defaultdict(dict)
    for r in rows:
        by_page[r['page']][r['source']] = r

    only_bing = [p for p, s in by_page.items() if set(s) == {'bing'}]
    only_clarity = [p for p, s in by_page.items() if set(s) == {'clarity'}]
    both = [p for p, s in by_page.items() if len(s) > 1]

    print('\n来源覆盖：')
    print('  仅 Bing    : %d 个 URL' % len(only_bing))
    print('  仅 Clarity : %d 个 URL' % len(only_clarity))
    print('  两源都有   : %d 个 URL' % len(both))

    # 两源展示量差异最大的页面：这些最容易被"相加"误判
    gap = []
    for p in both:
        b = by_page[p].get('bing', {}).get('impressions', 0)
        c = by_page[p].get('clarity', {}).get('impressions', 0)
        gap.append((abs(b - c), p, b, c))
    gap.sort(reverse=True)
    print('\n两源展示量差异最大的页面（口径不同，切勿相加）：')
    for _, p, b, c in gap[:10]:
        print('  bing=%-6d clarity=%-6d  %s' % (b, c, p.replace('https://chenguangwu.github.io/', '') or '/'))

    # 分来源的高曝光低点击候选（只基于 Bing 的搜索展示，口径纯净）
    print('\n仅基于 Bing 搜索展示的高曝光低点击页面（imp>10, ctr<3%%, 位置 3~15）：')
    cand = [r for r in rows
            if r['source'] == 'bing'
            and r['impressions'] > 10
            and (r['clicks'] == 0 or float(r['ctr']) < 0.03)
            and 3 <= float(r['position']) <= 15]
    for r in cand[:20]:
        print('  %5d imp | %2d clk | pos %s | %s'
              % (r['impressions'], r['clicks'], r['position'],
                 r['page'].replace('https://chenguangwu.github.io/', '') or '/'))
    if not cand:
        print('  （无）')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
