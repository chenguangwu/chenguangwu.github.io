#!/usr/bin/env python3
"""相关工具推荐去重门禁。

扫描 tools/**/*.html 中每个 `.related-tools-grid`，按规范化目标（去掉 ?query/#fragment，
统一为仓库内相对路径）检查同一推荐区是否重复指向同一工具。

退出码：0=无重复；1=存在重复（打印文件、区块序号与重复目标）。
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')

GRID_RE = re.compile(r'<div[^>]*class="[^"]*related-tools-grid[^"]*"[^>]*>(.*?)</div>\s*</div>', re.S)
LINK_RE = re.compile(r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*related-tool-card', re.S)


def normalize(page, href):
    href = href.strip().split('#', 1)[0].split('?', 1)[0]
    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return None
    if href.startswith('/'):
        target = href.lstrip('/')
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(os.path.relpath(page, ROOT)), href))
    return target.replace(os.sep, '/')


def main():
    problems = []
    pages = 0
    for dirpath, _dirnames, filenames in os.walk(TOOLS):
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(dirpath, fn)
            pages += 1
            text = open(path, encoding='utf-8', errors='replace').read()
            for idx, block in enumerate(GRID_RE.finditer(text), 1):
                links = []
                for m in LINK_RE.finditer(block.group(1)):
                    target = normalize(path, m.group(1))
                    if target:
                        links.append(target)
                dup = [t for t, c in Counter(links).items() if c > 1]
                if dup:
                    problems.append('%s [grid#%d]: %s' % (
                        os.path.relpath(path, ROOT), idx, ', '.join(sorted(dup))))

    if problems:
        print('related-tools duplicate targets: %d' % len(problems))
        for p in problems[:80]:
            print('  ✗ ' + p)
        if len(problems) > 80:
            print('  ... %d more' % (len(problems) - 80))
        return 1
    print('OK: %d tool pages, no duplicate related-tool targets' % pages)
    return 0


if __name__ == '__main__':
    sys.exit(main())
