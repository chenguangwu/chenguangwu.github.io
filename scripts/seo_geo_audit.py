#!/usr/bin/env python3
"""SEO/GEO 问题复核：验证历史截图中列出的 7 类问题当前状态。

范围：全站 HTML（跳过重定向桩 TOOLBOX-REDIRECT）。
输出：逐项计数、长度分布、典型示例。
"""
import glob, re, html, collections, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

h1_pat = re.compile(r'<h1[^>]*>', re.I)
meta_desc_pat = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
title_pat = re.compile(r'<title>([^<]*)</title>', re.I)
img_pat = re.compile(r'<img[^>]*>', re.I)

multi_h1 = []
missing_desc = []
desc_lens = []
short_desc = []
title_lens = []
short_title = []
img_missing_alt = []
indexnow_refs = []

total_html = 0
for f in files:
    try:
        raw = open(f, 'rb').read()
        text = raw.decode('utf-8')
    except Exception:
        continue
    total_html += 1
    rel = os.path.relpath(f, ROOT)
    if 'TOOLBOX-REDIRECT' in text:
        continue

    # 1. multiple h1
    h1s = h1_pat.findall(text)
    if len(h1s) > 1:
        multi_h1.append((rel, len(h1s)))

    # 2 & 4. description
    m = meta_desc_pat.search(text)
    if not m:
        missing_desc.append((rel, None))
    else:
        desc = html.unescape(m.group(1)).strip()
        l = len(desc)
        desc_lens.append(l)
        if l == 0:
            missing_desc.append((rel, ''))
        elif l < 50:
            short_desc.append((rel, l, desc[:80]))

    # 5. title length
    tm = title_pat.search(text)
    if tm:
        title = tm.group(1).strip()
        l = len(title)
        title_lens.append(l)
        if l < 10:
            short_title.append((rel, l, title[:80]))

    # 7. img missing alt
    for img_tag in img_pat.findall(text):
        if re.search(r'\salt\s*=\s*["\']', img_tag, re.I):
            continue
        # ignore some decorative patterns if needed
        img_missing_alt.append((rel, img_tag[:120]))

    # 3. indexnow references
    if 'indexnow' in text.lower() or 'bing' in text.lower() and 'api-key' in text.lower():
        indexnow_refs.append(rel)

print('=' * 60)
print('SEO/GEO 复核报告')
print('扫描 HTML 文件数:', total_html)
print('=' * 60)

# 1
print('\n1. 多个 <h1> 标记')
print('   问题文件数:', len(multi_h1))
for rel, n in multi_h1[:10]:
    print('     ', rel, 'h1 数=', n)

# 2
print('\n2. 缺少/空 <meta name="description">')
print('   问题文件数:', len(missing_desc))
for rel, d in missing_desc[:10]:
    print('     ', rel, ('(空字符串)' if d == '' else '(缺失)'))

# 3
print('\n3. IndexNow / 搜索引擎索引提交')
if indexnow_refs:
    print('   发现 IndexNow/Bing 相关代码的文件数:', len(set(indexnow_refs)))
    for rel in sorted(set(indexnow_refs))[:10]:
        print('     ', rel)
else:
    print('   项目代码中未发现 IndexNow/Bing 提交相关代码。')
    print('   当前由用户侧 cron 自动运行（工作记忆约定），"IndexNow is in batch mode" 属于外部配置。')

# 4
print('\n4. Meta description 长度')
if desc_lens:
    print('   总数:', len(desc_lens))
    print('   平均:', round(sum(desc_lens)/len(desc_lens), 1))
    print('   最小:', min(desc_lens), '| 最大:', max(desc_lens))
    bins = [(0, 0, '空'), (1, 49, '1-49'), (50, 119, '50-119'), (120, 160, '120-160'), (161, 999, '>160')]
    for lo, hi, label in bins:
        cnt = sum(1 for x in desc_lens if lo <= x <= hi)
        print(f'     {label}: {cnt}')
    print('   典型过短示例（<50 字符）:')
    for rel, l, d in short_desc[:10]:
        print(f'     {rel} ({l} 字符): {d}')

# 5
print('\n5. <title> 长度')
if title_lens:
    print('   总数:', len(title_lens))
    print('   平均:', round(sum(title_lens)/len(title_lens), 1))
    print('   最小:', min(title_lens), '| 最大:', max(title_lens))
    bins = [(0, 9, '0-9'), (10, 19, '10-19'), (20, 29, '20-29'), (30, 59, '30-59'), (60, 999, '>60')]
    for lo, hi, label in bins:
        cnt = sum(1 for x in title_lens if lo <= x <= hi)
        print(f'     {label}: {cnt}')
    print('   典型过短示例（<10 字符）:')
    for rel, l, t in short_title[:10]:
        print(f'     {rel} ({l} 字符): {t}')

# 6
print('\n6. 高质量域入站链接')
print('   无法从代码库内部验证；属于站外 SEO/外链因素。')

# 7
print('\n7. <img> 缺少 alt 属性')
print('   问题 <img> 数:', len(img_missing_alt))
print('   涉及文件数:', len(set(r for r, _ in img_missing_alt)))
for rel, tag in img_missing_alt[:10]:
    print('     ', rel, tag)
