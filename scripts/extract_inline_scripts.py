#!/usr/bin/env python3
"""把超大内联 <script> 块外置为可缓存的外部 JS 文件。

背景（2026-09-05）：tools/ 下少数页的单个内联 script 达 49–74KB（多为题库 /
词库 / 色彩矩阵等数据常量 + 其消费逻辑）。内联会让 HTML 体积直接膨胀，且
无法被浏览器缓存复用。本脚本把整块原样搬移到 js/tools/<name>.js，HTML 改用
同步 <script src> 引用，逻辑零改动。

关键约束：
1. 引用路径一律用绝对路径 /js/tools/... —— 简体页在 /tools/<ind>/ 下，繁体页
   在 /zh-tw/tools/<ind>/ 下（zh-tw 无 js 副本），相对路径在繁体页必然 404。
2. 不加 defer/async —— 保持与原内联一致的执行时机（同步、按序），
   顶层 const 的全局词法绑定对后续脚本可见，行为不变。
3. 繁体安全：gen_opencc_locales.mjs 的 SKIP_TAGS 保护 script 块不做简繁转换，
   外置后繁体页引用同一份文件，与现状完全一致，不存在繁体倒退。

用法:
    python3 scripts/extract_inline_scripts.py            # 实际执行
    python3 scripts/extract_inline_scripts.py --dry-run  # 只报告不改
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_DIR = os.path.join(ROOT, 'js', 'tools')
# 只处理达到该体积的内联块，避免把小段的初始化代码也拆出去
MIN_BYTES = 30 * 1024

SCRIPT_RE = re.compile(r'(<script\b([^>]*)>)([\s\S]*?)(</script>)', re.I)


def is_inline(attrs):
    return 'src=' not in attrs.lower()


def process(path, dry_run):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    best = None
    for m in SCRIPT_RE.finditer(html):
        tag, attrs, js, close = m.group(1), m.group(2), m.group(3), m.group(4)
        if not is_inline(attrs):
            continue
        if len(js) < MIN_BYTES:
            continue
        if best is None or len(js) > len(best[2]):
            best = (m.start(), tag, js, close, m.group(0))

    if best is None:
        return 0, 0, None

    start, tag, js, close, whole = best
    base = os.path.basename(path)[:-len('.html')]
    rel_js = 'js/tools/%s.js' % base
    abs_path = os.path.join(JS_DIR, base + '.js')

    # 幂等：已外置过（HTML 已引用且 JS 文件存在）则跳过
    if ('/js/tools/%s.js' % base) in html and os.path.isfile(abs_path):
        return 0, 0, 'skipped'

    saved = len(whole) - len('<script src="/%s"></script>' % rel_js)
    if not dry_run:
        os.makedirs(JS_DIR, exist_ok=True)
        header = ('/* %s\n'
                  ' * 自动外置自 tools/%s —— 由 scripts/extract_inline_scripts.py 生成。\n'
                  ' * 请勿直接编辑本文件；修改请改源 HTML 后重跑脚本。\n'
                  ' */\n') % (base + '.js', os.path.relpath(path, ROOT))
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(header + js.strip('\n') + '\n')
        new_html = html.replace(whole, '<script src="/%s"></script>' % rel_js, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
    return len(js), saved, 'done'


def main():
    dry_run = '--dry-run' in sys.argv
    targets = [
        'tools/chinese/chinese-culture.html',
        'tools/psychology/bigfive-personality-test.html',
        'tools/colorvision/colorblind-simulator.html',
        'tools/psychology/scl90-assessment.html',
        'tools/cognition/cognitive-assessment.html',
    ]
    total_js = 0
    total_saved = 0
    for rel in targets:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            print('  跳过（不存在）: %s' % rel)
            continue
        js_len, saved, status = process(path, dry_run)
        if status == 'skipped':
            print('  已外置，跳过: %s' % rel)
            continue
        total_js += js_len
        total_saved += saved
        print('  %-52s 外置 %5.1f KB, HTML 减少 %5.1f KB'
              % (rel, js_len / 1024, saved / 1024))

    prefix = '[dry-run] ' if dry_run else ''
    print('%s内联脚本外置: 共搬移 %.1f KB, HTML 共减少 %.1f KB'
          % (prefix, total_js / 1024, total_saved / 1024))
    return 0


if __name__ == '__main__':
    sys.exit(main())
