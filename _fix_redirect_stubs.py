#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复重定向存根（TOOLBOX-REDIRECT）中的兜底链接死链。

旧存根仅有一行：<a href="tools/<ind>/<name>.html">新地址</a>
从存根自身目录解析会变成 tools/<ind>/tools/<ind>/<name>.html（双重前缀）而失效。
改为根绝对路径 href="/tools/<ind>/<name>.html" 即可在任意位置正确解析。

构建脚本 _build.py 会跳过 TOOLBOX-REDIRECT 文件，因此本脚本的直接修改不会被覆盖。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STUB_RE = re.compile(r'^tool-.*\.html$')
FIX_RE = re.compile(r'href="tools/')

def main():
    count_files = 0
    count_links = 0
    changed = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, 'tools')):
        for fn in filenames:
            if not STUB_RE.match(fn):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
            except Exception:
                continue
            if 'TOOLBOX-REDIRECT' not in content:
                continue
            if 'href="tools/' not in content:
                continue
            new, n = FIX_RE.subn('href="/tools/', content)
            if n:
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(new)
                count_files += 1
                count_links += n
                changed.append(os.path.relpath(fp, ROOT))
    print('已修复存根文件数: %d' % count_files)
    print('已修复兜底链接数: %d' % count_links)
    with open(os.path.join(ROOT, '_fix_redirect_stubs.json'), 'w', encoding='utf-8') as fh:
        import json
        json.dump({'files': count_files, 'links': count_links,
                   'sample': changed[:10]}, fh, ensure_ascii=False, indent=2)
    return 0

if __name__ == '__main__':
    sys.exit(main())
