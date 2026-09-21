#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给「中文 <title> 漏翻成英文」的工具页补全中文 title。

事实依据(2026-09-21 核验):
- 全站 5003 个简体源 HTML, 仅 87 个 <title> 完全无汉字(英文真名兜底)
- 这 87 个的 <h1> 与正文全是中文真名(如 Washer Capacity -> h1「洗衣机容量选择器」)
- 仅 <title> 标签漏翻, 属 title 翻译缺失小缺陷, 非「无名工具」
- h1 无汉字的仅 1 个(favicon-from-emoji.html), 用预定义中文名映射

修复: 将 <title> 改为 h1 中文名 + " - ToolBox"(与页面语义一致, 不瞎编)。
favicon 那个 h1 也连带改中文。

用法:
  python3 scripts/fill_zh_title.py            # dry-run 打印将改内容
  python3 scripts/fill_zh_title.py --apply    # 写盘
"""
import re, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZH = re.compile(r'[\u4e00-\u9fff]')
SITE = ' - ToolBox'

# h1 也无汉字的特殊工具 -> 预定义准确中文名(基于真实功能, 不瞎编)
SPECIAL_H1_CN = {
    'tools/design/favicon-from-emoji.html': 'Emoji 网站图标生成器',
}

def clean_h1(s):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.I | re.S)
    if not m:
        return ''
    return re.sub(r'<[^>]+>', '', m.group(1)).strip()

def get_title(s):
    m = re.search(r'<title>(.*?)</title>', s, re.I | re.S)
    return re.split(r'\s*[-|_]\s*ToolBox', m.group(1))[0].strip() if m else ''

def main():
    apply = '--apply' in sys.argv
    files = [f for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))
             if not f.endswith('.en.html')]
    targets = []
    for f in files:
        s = open(f, encoding='utf-8', errors='ignore').read()
        title = get_title(s)
        if not title or ZH.search(title):
            continue  # 已有中文 title, 跳过
        rel = os.path.relpath(f, ROOT)
        h1 = clean_h1(s)
        if ZH.search(h1):
            cn = h1
        elif rel in SPECIAL_H1_CN:
            cn = SPECIAL_H1_CN[rel]
        else:
            print('  [跳过] %s h1 也无汉字且无预定义映射' % rel)
            continue
        targets.append((rel, f, title, cn, h1))
    print('待补中文 title 工具数: %d' % len(targets))
    for rel, f, old, cn, h1 in targets[:15]:
        print('  %s\n     旧title: %s\n     新title: %s\n     h1: %s' % (rel, old, cn + SITE, h1))
    if len(targets) > 15:
        print('  ... 其余 %d 个略' % (len(targets) - 15))
    if not apply:
        print('\n[dry-run] 未写盘。加 --apply 执行。')
        return
    n = 0
    for rel, f, old, cn, h1 in targets:
        s = open(f, encoding='utf-8', errors='ignore').read()
        # 改 <title>
        s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % (cn + SITE), s, count=1, flags=re.I | re.S)
        # favicon 连带改 h1
        if rel in SPECIAL_H1_CN:
            s = re.sub(r'(<h1[^>]*>).*?(</h1>)', r'\1%s\2' % cn, s, count=1, flags=re.I | re.S)
        open(f, 'w', encoding='utf-8').write(s)
        n += 1
    print('\n[apply] 已写盘 %d 个文件' % n)

if __name__ == '__main__':
    main()
