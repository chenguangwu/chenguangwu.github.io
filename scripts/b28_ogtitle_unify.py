#!/usr/bin/env python3
"""B-OPT28: 统一全站 og:title 为 `NAME - ToolBox` 风格。

规则（以 <title> 为唯一真值源，天然幂等）：
  - 取 <title> 第一个 " - " 之前的内容作为 NAME
  - 重设 <meta property="og:title" content="NAME - ToolBox">
  - 跳过：重定向桩(TOOLBOX-REDIRECT)、无 <title>、<title> 无 " - "、无 og:title 标签
仅修改「已有 og:title 且内容非目标格式」的文件，避免无意义 churn。
"""
import re, glob, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = '--apply' in sys.argv

OG_RE = re.compile(r'<meta property="og:title" content="[^"]*">')
TITLE_RE = re.compile(r'<title>([^<]*?)</title>')
CONTENT_RE = re.compile(r'content="([^"]*)"')


def process(path):
    try:
        raw = open(path, 'rb').read()
        html = raw.decode('utf-8')
    except Exception:
        return 'skip'
    if 'TOOLBOX-REDIRECT' in html:
        return 'skip'
    m_t = TITLE_RE.search(html)
    if not m_t:
        return 'skip'
    title = m_t.group(1).strip()
    if ' - ' not in title:
        return 'skip'
    name = title.split(' - ')[0].strip()
    if not name:
        return 'skip'
    target = f'{name} - ToolBox'
    m_og = OG_RE.search(html)
    if not m_og:
        return 'skip'
    cur = CONTENT_RE.search(m_og.group(0)).group(1)
    if cur == target:
        return 'same'
    if not APPLY:
        return 'dry'
    new_tag = f'<meta property="og:title" content="{target}">'
    new_html = OG_RE.sub(lambda m: new_tag, html, count=1)
    if new_html != html:
        with open(path, 'wb') as f:
            f.write(new_html.encode('utf-8'))
        return 'changed'
    return 'skip'


def main():
    files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
    changed = same = skipped = 0
    for f in files:
        r = process(f)
        if r in ('changed', 'dry'):
            changed += 1
        elif r == 'same':
            same += 1
        else:
            skipped += 1
    if APPLY:
        print(f'[APPLY] 修改 og:title 数={changed} (已一致={same}, 跳过桩/无title/无og={skipped})')
    else:
        print(f'[DRY] 将修改 og:title 数={changed} (已一致={same}, 跳过={skipped})')


if __name__ == '__main__':
    main()
