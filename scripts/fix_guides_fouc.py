#!/usr/bin/env python3
"""
修复 guides/ 页面因异步加载 common.css 导致的 FOUC（无样式内容闪烁）。
把 <link rel="preload" as="style" href="../css/common.css" onload="..."> + <noscript>
替换为同步的 site-chrome.css + common.css，确保 common.js 注入的统一导航
在首屏即可拿到样式，避免 .nav-mobile 与 .nav-top 同时闪现。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDES = ROOT / 'guides'

# 匹配两种前置形式：
# 1) 单独一行： <link rel="preload" ...>
# 2) 前面紧粘 <meta name="title-zh" ...>（无换行），需保留 title-zh
PRELOAD_RE = re.compile(
    r'(<meta[^>]*name="title-zh"[^>]*>)?\s*'
    r'<link\s+rel="preload"\s+as="style"\s+href="\.\./css/common\.css"\s+onload="[^"]*"\s*>\s*'
    r'<noscript>\s*<link\s+rel="stylesheet"\s+href="\.\./css/common\.css"\s*>\s*</noscript>',
    re.IGNORECASE | re.DOTALL
)

CSS_LINKS = (
    '<link rel="stylesheet" href="../css/site-chrome.css">\n'
    '<link rel="stylesheet" href="../css/common.css">'
)


def _replacer(m: re.Match) -> str:
    title_zh = m.group(1) or ''
    prefix = title_zh if title_zh else ''
    return prefix + '\n' + CSS_LINKS


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if 'preload' not in text or '../css/common.css' not in text:
        return False
    new_text, count = PRELOAD_RE.subn(_replacer, text)
    if count == 0:
        return False
    # 保守写入：仅当内容真正变化
    if new_text == text:
        return False
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    files = sorted(GUIDES.glob('*.html'))
    fixed = 0
    skipped = 0
    for p in files:
        try:
            if fix_file(p):
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f'ERR {p.name}: {e}')
    print(f'fixed={fixed} skipped={skipped} total={len(files)}')


if __name__ == '__main__':
    main()
