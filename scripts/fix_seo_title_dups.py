#!/usr/bin/env python3
"""
fix_seo_title_dups.py —— 自模拟搜索引擎体检后的安全 on-page 修复（非破坏性，不动 URL）

处理三类问题（均不改变页面 URL，仅修正 <title> 文本）：
  1. 裸 < > 未转义：标题里出现裸尖括号（如 combined-ratio 的「（<100%」），
     会被浏览器截断 title / 触发 audit 误判。转义为 &lt; / &gt;。
  2. tool×guide 标题重复（30 组）：指南页标题与工具页完全相同。
     指南页追加「使用指南」(zh) / 「 Guide」(en) 后缀差异化。
  3. tool×tool 跨行业同名（5 组）：同工具落在两个行业，标题相同。
     追加行业限定词（如「（统计学）」）差异化，避免 Google 视为重复标题。

用法：
  python3 scripts/fix_seo_title_dups.py            # 试运行（仅打印将改项）
  python3 scripts/fix_seo_title_dups.py --apply    # 实际写入
"""
import os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--apply' not in sys.argv

# 行业目录 -> 中文限定词
IND_ZH = {
    'statistics': '统计学', 'it': 'IT', 'securities': '证券', 'investment': '投资',
    'niche': '垂直', 'pet': '宠物', 'hr': '人力', 'legal': '法律',
    'economics': '经济', 'insurance': '保险', 'science': '科学', 'math': '数学',
    'finance': '金融', 'livestock': '畜牧', 'reproductive-medicine': '生殖医学',
    'agriculture': '农业', 'video': '视频', 'legal2': '法律',
}

def read(p):
    return open(p, encoding='utf-8', errors='ignore').read()

def write(p, s):
    if DRY:
        return
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)

def title_of(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return m.group(1).strip() if m else None

def strip_suffix(t):
    return t[:-len(' - ToolBox')] if t.endswith(' - ToolBox') else t

def set_title(html, new_core):
    """把 <title>X - ToolBox</title> 的 X 换成 new_core，og:title/twitter:title 同步。"""
    # title
    def repl(m):
        return '<title>%s - ToolBox</title>' % new_core
    html2, n = re.subn(r'<title>.*?</title>', lambda m: '<title>%s - ToolBox</title>' % new_core, html, count=1, flags=re.S)
    # og:title
    html2 = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                   lambda m: m.group(1) + new_core + ' - ToolBox' + m.group(2), html2, count=1)
    # twitter:title
    html2 = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")',
                   lambda m: m.group(1) + new_core + ' - ToolBox' + m.group(2), html2, count=1)
    return html2

# ---------- 收集页面 ----------
tool_pages, guide_pages = [], []
for p in glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True):
    if p.endswith('/index.html'):
        continue
    if 'TOOLBOX-REDIRECT' in read(p):
        continue
    tool_pages.append(p)
for p in glob.glob(os.path.join(ROOT, 'guides', '**', '*.html'), recursive=True):
    if 'TOOLBOX-REDIRECT' in read(p):
        continue
    guide_pages.append(p)

tool_titles = {}   # core -> [paths]
for p in tool_pages:
    t = title_of(read(p))
    if t:
        tool_titles.setdefault(strip_suffix(t), []).append(p)

changes = []

# ---------- 1. 裸 < 转义（仅标题区；只转义非 & 前缀的裸 <，避免二次转义 &lt;）----------
print("【1】裸 < 转义")
def fix_title_block(h):
    m = re.search(r'(<title>)(.*?)(</title>)', h, re.S)
    if not m:
        return h
    body = m.group(2)
    # 标题里只有裸 <（如 combined-ratio 的「（<100%」），无裸 >；仅转义裸 <（非 & 前缀）
    fixed = re.sub(r'(?<!&)<', '&lt;', body)
    return h[:m.start()] + m.group(1) + fixed + m.group(3) + h[m.end():]
for p in tool_pages + guide_pages:
    html = read(p)
    if 'TOOLBOX-REDIRECT' in html:
        continue
    new2 = fix_title_block(html)
    if new2 != html:
        changes.append((p, 'escape raw < in title'))
        write(p, new2)

# ---------- 2. tool×guide 标题重复 ----------
print("【2】tool×guide 标题重复 -> 指南页加后缀")
for gp in guide_pages:
    html = read(gp)
    t = title_of(html)
    if not t:
        continue
    core = strip_suffix(t)
    if core in tool_titles:   # 该指南标题与某工具页完全相同
        is_en = gp.endswith('-guide.en.html')
        new_core = (core + ' Guide') if is_en else (core + '使用指南')
        new_html = set_title(html, new_core)
        if new_html != html:
            changes.append((gp, 'guide title -> %s' % new_core))
            write(gp, new_html)

# ---------- 3. tool×tool 跨行业同名 ----------
print("【3】tool×tool 跨行业同名 -> 加行业限定词")
for core, paths in tool_titles.items():
    if len(paths) < 2:
        continue
    rels = [os.path.dirname(p).split(os.sep)[-1] for p in paths]
    for p, ind in zip(paths, rels):
        html = read(p)
        t = title_of(html)
        if not t:
            continue
        cur = strip_suffix(t)
        if cur != core:   # 已被改过
            continue
        zh = IND_ZH.get(ind, ind)
        new_core = '%s（%s）' % (core, zh)
        new_html = set_title(html, new_core)
        if new_html != html:
            changes.append((p, 'tool title -> %s' % new_core))
            write(p, new_html)

print('\n=== 共将修改 %d 个文件 ===' % len(changes))
for p, why in changes:
    print('  %s  [%s]' % (os.path.relpath(p, ROOT), why))
if DRY:
    print('\n（试运行模式，未写入。加 --apply 实际执行）')
else:
    print('\n（已写入）')
