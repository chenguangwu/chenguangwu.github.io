#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToolBox 资产完整性审计（维护迭代用）

检查仓库内所有 HTML 文件的：
  1. 局部资产死链：<img src> / <source src> / <video src> / <audio src> /
     <link rel="icon|apple-touch-icon" href> 指向的本地文件是否真实存在
     （CDN / data: / javascript: / 根绝对路径 / 纯锚点 均跳过）
  2. <html lang> 是否缺失（SEO/可访问性）
  3. 页面内重复 id= （HTML 有效性，会破坏锚点与 getElementById）

智能排除 <script>/<style> 块内示例代码，避免误报（与 _audit_links.py 一致）。
纯本地文件系统校验，不发送任何网络请求。

用法：
  python3 _audit_assets.py            # 生成报告（_audit_assets_report.txt/json）
  python3 _audit_assets.py --check    # 门禁模式：存在任何问题 exit 1，否则 exit 0
  python3 _audit_assets.py --quiet    # 静默进度
"""

import os
import re
import sys
import json
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.workbuddy', 'scripts', '_regression_shots',
             '__pycache__', 'venv', 'vendor'}

# 跳过非本地 / 伪链
SKIP_PREFIX = ('http://', 'https://', '//', 'data:', 'javascript:', 'mailto:', 'tel:')
SCRIPT_RE = re.compile(r'<script[\s>].*?</script>', re.I | re.S)
STYLE_RE = re.compile(r'<style[\s>].*?</style>', re.I | re.S)
# 资源引用（只取本地；排除 JS 运行时伪链 $1 / ${}）
ASSET_RE = re.compile(
    r'''(?:<img\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']|<source\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']|'''
    r'''<video\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']|<audio\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']|'''
    r'''<link\b[^>]*\brel\s*=\s*["\'](?:icon|apple-touch-icon|shortcut icon)["\'][^>]*\bhref\s*=\s*["\']([^"\']+)["\'])''',
    re.I)
ID_RE = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.I)
LANG_RE = re.compile(r'<html\b([^>]*)>', re.I)
JS_ARTIFACT = re.compile(r'\$\d|\$\{')


def build_existing():
    existing = set()
    for dp, dn, fn in os.walk(ROOT):
        parts = dp[len(ROOT):].split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        for f in fn:
            existing.add(os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/'))
    return existing


def is_local(target):
    if not target:
        return False
    t = target.strip()
    if any(t.startswith(p) for p in SKIP_PREFIX):
        return False
    if t.startswith('#'):
        return False
    if JS_ARTIFACT.search(t):
        return False
    return True


def resolve(target, src, existing):
    """返回 (exists:bool|None, resolved_path:str)。None=非本地/跳过。"""
    if not is_local(target):
        return None, ''
    t = target.strip()
    if t.startswith('/'):
        cand = t[1:].lstrip('/')
    else:
        base = os.path.dirname(src)
        cand = os.path.normpath(os.path.join(base, t)).replace(os.sep, '/')
    cand = cand.split('#')[0].split('?')[0]
    if cand == '':
        return None, ''
    # 精确
    if cand in existing:
        return True, cand
    # 目录 -> index.html
    if cand.rstrip('/') + '/index.html' in existing:
        return True, cand.rstrip('/') + '/index.html'
    # 含扩展名但可能大小写/尾斜杠
    if cand.endswith('/') and cand + 'index.html' in existing:
        return True, cand + 'index.html'
    return False, cand


def main():
    check_mode = '--check' in sys.argv
    quiet = '--quiet' in sys.argv

    def log(*a):
        if not quiet:
            print(*a, file=sys.stderr)

    existing = build_existing()
    log('候选文件数: %d' % len(existing))

    html_files = sorted(f for f in existing if f.endswith('.html'))
    log('待扫描 HTML 文件数: %d' % len(html_files))

    broken_assets = defaultdict(Counter)   # target -> Counter(src -> count)
    lang_missing = []                       # rel paths
    dup_ids = []                            # (rel, [ids])
    checked_assets = 0
    scanned = 0

    for f in html_files:
        try:
            with open(os.path.join(ROOT, f), 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
        except Exception:
            continue
        scanned += 1
        # 跳过非真实页面（如 GSC/Bing 验证文件，内容为纯文本、无 <html> 标签）
        if not re.search(r'<html', content, re.I):
            scanned -= 1
            continue
        body = SCRIPT_RE.sub('', content)
        body = STYLE_RE.sub('', body)

        # 1) 局部资产
        for m in ASSET_RE.finditer(body):
            target = next((g for g in m.groups() if g), '')
            ok, _ = resolve(target, f, existing)
            if ok is None:
                continue  # 非本地跳过
            checked_assets += 1
            if ok is False:
                broken_assets[target][f] += 1

        # 2) lang 缺失（仅检查 <html> 标签本身，含 script/style 不影响）
        hm = LANG_RE.search(content)
        if hm:
            if not re.search(r'\blang\s*=', hm.group(1), re.I):
                lang_missing.append(f)
        else:
            lang_missing.append(f)

        # 3) 重复 id（剔除 script/style 后的可见文档）
        ids = ID_RE.findall(body)
        seen = set()
        dups = []
        for i in ids:
            if i in seen and i not in dups:
                dups.append(i)
            seen.add(i)
        if dups:
            dup_ids.append((f, dups))

    # ---- 汇总 ----
    total_broken = sum(sum(c.values()) for c in broken_assets.values())
    lines = []
    lines.append('=' * 70)
    lines.append('ToolBox 资产完整性审计')
    lines.append('=' * 70)
    lines.append('扫描 HTML 文件 : %d' % scanned)
    lines.append('局部资产引用   : %d' % checked_assets)
    lines.append('资产死链数     : %d (目标 %d)' % (total_broken, len(broken_assets)))
    lines.append('lang 缺失页数  : %d' % len(lang_missing))
    lines.append('含重复 id 页数 : %d' % len(dup_ids))
    lines.append('')

    if not broken_assets:
        lines.append('✅ 局部资产：未发现死链。')
    else:
        lines.append('— 资产死链目标（按引用次数排序）—')
        for tgt, srcs in sorted(broken_assets.items(), key=lambda kv: sum(kv[1].values()), reverse=True):
            cnt = sum(srcs.values())
            lines.append('[%d 次 / %d 页] %s' % (cnt, len(srcs), tgt))
            for sf, c in srcs.most_common(3):
                lines.append('       ↳ %s (%d)' % (sf, c))

    lines.append('')
    if lang_missing:
        lines.append('— lang 缺失页面（前 20）—')
        for p in lang_missing[:20]:
            lines.append('  ' + p)
        if len(lang_missing) > 20:
            lines.append('  ... 共 %d 页' % len(lang_missing))
    else:
        lines.append('✅ 所有页面均含 <html lang>。')

    lines.append('')
    if dup_ids:
        lines.append('— 含重复 id 的页面（前 20，含示例 id）—')
        for p, ids in dup_ids[:20]:
            lines.append('  %s  -> 重复: %s' % (p, ', '.join(ids[:6])))
        if len(dup_ids) > 20:
            lines.append('  ... 共 %d 页' % len(dup_ids))
    else:
        lines.append('✅ 未发现页面内重复 id。')

    report = '\n'.join(lines)

    with open(os.path.join(ROOT, '_audit_assets_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write(report + '\n')
    with open(os.path.join(ROOT, '_audit_assets_report.json'), 'w', encoding='utf-8') as fh:
        json.dump({
            'scanned': scanned,
            'checked_assets': checked_assets,
            'broken_asset_targets': len(broken_assets),
            'broken_asset_refs': total_broken,
            'lang_missing': len(lang_missing),
            'dup_id_pages': len(dup_ids),
            'broken_assets': [{'target': t, 'refs': sum(s.values()),
                               'pages': [x[0] for x in s.most_common(3)]}
                              for t, s in sorted(broken_assets.items(),
                                                key=lambda kv: sum(kv[1].values()), reverse=True)],
            'lang_missing_samples': lang_missing[:50],
            'dup_id_samples': [{'page': p, 'ids': ids[:8]} for p, ids in dup_ids[:50]],
        }, fh, ensure_ascii=False, indent=2)

    log('资产死链:%d  lang缺失:%d  重复id页:%d' % (
        len(broken_assets), len(lang_missing), len(dup_ids)))

    if check_mode:
        problems = (len(broken_assets) > 0) or (len(lang_missing) > 0) or (len(dup_ids) > 0)
        if problems:
            print(report)
            return 1
        print('OK: 资产完整性审计通过（0 死链 / 0 lang缺失 / 0 重复id）')
        return 0

    print(report)
    return 0


if __name__ == '__main__':
    sys.exit(main())
