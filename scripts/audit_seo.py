#!/usr/bin/env python3
"""全站 SEO 审计：扫描工具页/分类落地页/核心页的元数据覆盖与质量问题。"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools_dir = os.path.join(ROOT, 'tools')

def read(p):
    try:
        return open(p, encoding='utf-8').read()
    except Exception:
        return None

def audit_html(p, html):
    issues = collections.defaultdict(list)
    title = re.search(r'<title>([^<]*)</title>', html)
    t = title.group(1).strip() if title else ''
    if not t: issues['title_missing'].append(p)
    elif '- ToolBox' not in t: issues['title_suffix'].append(p)
    elif len(t) > 60: issues['title_too_long'].append(p)
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    d = desc.group(1).strip() if desc else ''
    if not d: issues['desc_missing'].append(p)
    elif len(d) < 30: issues['desc_short'].append(p)
    elif len(d) > 165: issues['desc_long'].append(p)
    if not re.search(r'<meta name="description"', html): issues['desc_attr_missing'].append(p)
    if not re.search(r'<link rel="canonical"', html): issues['canonical_missing'].append(p)
    for tag in ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']:
        if not re.search(r'<meta property="%s"' % re.escape(tag), html):
            issues['og_missing_' + tag.split(':')[1]].append(p)
    if not re.search(r'<meta name="twitter:card"', html): issues['tw_card'].append(p)
    if not re.search(r'<meta name="twitter:title"', html): issues['tw_title'].append(p)
    if not re.search(r'<meta name="twitter:image"', html): issues['tw_image'].append(p)
    if 'application/ld+json' not in html: issues['jsonld'].append(p)
    if not re.search(r'<html[^>]*lang="zh-CN"', html): issues['lang'].append(p)
    if 'viewport' not in html: issues['viewport'].append(p)
    if not re.search(r'<h1[^>]*>', html) and not re.search(r'<h2[^>]*>', html): issues['h1_h2'].append(p)
    return issues, (t, d)

# 收集页面
tool_pages, cat_pages, core_pages = [], [], []
for ind in sorted(os.listdir(tools_dir)):
    ind_dir = os.path.join(tools_dir, ind)
    if not os.path.isdir(ind_dir): continue
    for fn in os.listdir(ind_dir):
        if not fn.endswith('.html'): continue
        p = os.path.join(ind_dir, fn)
        (tool_pages if fn != 'index.html' else cat_pages).append(p)
for fn in ['index.html', 'sitemap.html', 'search.html', 'chains.html', '404.html']:
    p = os.path.join(ROOT, fn)
    if os.path.exists(p): core_pages.append(p)
guides_dir = os.path.join(ROOT, 'guides')
guide_pages = [os.path.join(guides_dir, f) for f in os.listdir(guides_dir) if f.endswith('.html')] if os.path.isdir(guides_dir) else []

all_pages = tool_pages + cat_pages + core_pages + guide_pages
agg = collections.Counter()
samples = {}
desc_map = collections.defaultdict(list)
title_map = collections.defaultdict(list)
redirect_n = 0
for p in all_pages:
    html = read(p)
    if not html: continue
    if 'TOOLBOX-REDIRECT' in html:   # 合并残留重定向桩：已 noindex+canonical，非真工具页，排除
        redirect_n += 1
        continue
    issues, (t, d) = audit_html(p, html)
    for k, v in issues.items():
        agg[k] += len(v)
        if k not in samples: samples[k] = v[:3]
    if d: desc_map[d].append(p)
    if t: title_map[t].append(p)

print(f'扫描页面总数: {len(all_pages)}（工具 {len(tool_pages)} / 分类 {len(cat_pages)} / 核心 {len(core_pages)} / 指南 {len(guide_pages)}）\n')
print(f'排除重定向桩(TOOLBOX-REDIRECT): {redirect_n}（已 noindex+canonical，非真工具页）\n')
print('== 问题统计 ==')
for k, c in agg.most_common():
    print(f'  {k}: {c}')
print('\n== 样例（每个问题前 3 个文件）==')
for k in samples:
    print(f'  {k}:')
    for s in samples[k]: print(f'    - {os.path.relpath(s, ROOT)}')

# description / title 重复
print('\n== description 重复（同 desc ≥2 页）==')
dup_desc = {d: ps for d, ps in desc_map.items() if len(ps) >= 2}
print(f'  重复 desc 组数: {len(dup_desc)}，涉及页面: {sum(len(v) for v in dup_desc.values())}')
for d, ps in sorted(dup_desc.items(), key=lambda x: -len(x[1]))[:5]:
    print(f'    [{len(ps)}] {d[:60]}... -> {[os.path.relpath(p,ROOT) for p in ps[:3]]}')
print('\n== title 重复（同 title ≥2 页）==')
dup_title = {t: ps for t, ps in title_map.items() if len(ps) >= 2}
print(f'  重复 title 组数: {len(dup_title)}，涉及页面: {sum(len(v) for v in dup_title.values())}')
for t, ps in sorted(dup_title.items(), key=lambda x: -len(x[1]))[:5]:
    print(f'    [{len(ps)}] {t[:60]} -> {[os.path.relpath(p,ROOT) for p in ps[:3]]}')

# 空泛 description
print('\n== 空泛/占位 description（前 10）==')
placeholder_re = re.compile(r'(待补充|占位|TODO|暂无描述|^[^，。；,]{0,8}$|默认描述|工具描述)')
cnt = 0
for p in all_pages:
    html = read(p)
    if not html: continue
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if m and placeholder_re.search(m.group(1).strip()):
        print(f'    {os.path.relpath(p,ROOT)}: {m.group(1).strip()[:60]}')
        cnt += 1
        if cnt >= 10: break
print(f'  （空泛 desc 总数 ≥{cnt}）')
