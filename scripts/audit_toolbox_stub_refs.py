#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审计：ToolBox stub 死引用风险扫描

背景
----
页面 <head> 的内联脚本会创建 window.ToolBox 的「入队占位(stub)」实现
（方法体只把调用 push 进 window.__tbq）。js/common.js 就绪后会用
`global.ToolBox = { ... }` **整体替换** window.ToolBox。

因此：任何在 common.js 之前执行、并把 window.ToolBox（或其方法）缓存进
闭包变量的脚本，其缓存引用会永久指向旧的 stub 对象，表现为
「按钮点击无反应、且不报任何错」。

本脚本扫描全站 HTML 的内联脚本块与 js/ 下的外部脚本，找出这类缓存写法，
输出风险清单供人工确认。

用法
----
    python3 scripts/audit_toolbox_stub_refs.py            # 扫描并打印
    python3 scripts/audit_toolbox_stub_refs.py --json out.json
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 跳过：构建产物、依赖、缓存目录
SKIP_DIRS = {'zh-tw', 'node_modules', '.git', '.github', '__pycache__',
             '.workbuddy', 'scripts', '_regression_shots'}

# 内联 script 块（不含 src 属性）
SCRIPT_BLOCK_RE = re.compile(
    r'<script(?![^>]*\bsrc\s*=)[^>]*>(.*?)</script>', re.S | re.I)

# 判定为「stub 定义块」的特征——这些块本身就是占位实现，跳过
STUB_MARKERS = ('__tbq', '__stubV')

# 风险模式：把 ToolBox 对象或其方法缓存进变量
PATTERNS = [
    # var TB = window.ToolBox;  /  const T = ToolBox;
    (r'\b(?:var|let|const)\s+(\w+)\s*=\s*(?:window\.)?ToolBox\s*[;)]',
     'object'),
    # var TB = window.ToolBox || {};
    (r'\b(?:var|let|const)\s+(\w+)\s*=\s*(?:window\.)?ToolBox\s*\|\|',
     'object-fallback'),
    # var copy = ToolBox.copyText;   （缓存方法本身）
    # 负向前瞻排除 var ok = ToolBox.copyText(url) 这类「立即调用并接收返回值」
    (r'\b(?:var|let|const)\s+(\w+)\s*=\s*(?:window\.)?ToolBox\.(\w+)\b(?!\s*\()',
     'method'),
]

# 需要人工确认但实际无害的常见写法（用于降噪说明）
BENIGN_IF_NAMED = ('__stub', 'stub')

# ── 关键区分 ────────────────────────────────────────────────────────────
# 页面 head 的 stub 并非全是占位实现：escHtml / formatNumber / createTable /
# debounce / $ / qs / qsa / validateNumberInput 在 stub 里就已给出**真实实现**，
# common.js 里的同名方法行为一致 —— 缓存这些方法是安全的。
#
# 真正危险的是下列「入队占位」方法：stub 版本只把调用 push 进 window.__tbq。
# 而 __tbq 仅在 common.js 加载时回放一次；用户在**点击时**才入队的调用
# 永远不会再被回放，于是永久失效、且不报任何错。
STUB_QUEUE_METHODS = {
    'initToolTheme', 'addToolStyles', 'showToast', 'toast',
    'copyText', 'copyToClipboard', 'copyFromElement', 'downloadText',
    'injectPrivacyBadge', 'toggleFavTool', 'addToRecentTool',
    'toggleToolTheme', 'applyTheme',
    'setResult', 'markInvalid', 'clearInvalid',
}

# stub 中已有真实实现、被缓存也安全的方法
STUB_REAL_METHODS = {
    'escHtml', 'formatNumber', 'createTable', 'debounce',
    '$', 'qs', 'qsa', 'validateNumberInput',
}


def classify(kind, member):
    """返回 'high'（高危/占位方法）、'safe'（stub 已含真实实现）或 'unknown'。"""
    if kind in ('object', 'object-fallback'):
        return 'unknown'
    if member in STUB_QUEUE_METHODS:
        return 'high'
    if member in STUB_REAL_METHODS:
        return 'safe'
    return 'unknown'


def scan_text(text, source):
    """扫描一段脚本文本，返回风险项列表。"""
    hits = []
    for pat, kind in PATTERNS:
        for m in re.finditer(pat, text):
            var = m.group(1)
            if var.lower() in BENIGN_IF_NAMED:
                continue
            line = text[:m.start()].count('\n') + 1
            detail = m.group(0).strip()
            if len(detail) > 90:
                detail = detail[:90] + '…'
            member = m.group(2) if kind == 'method' and m.lastindex >= 2 else ''
            hits.append({
                'source': source,
                'line': line,
                'kind': kind,
                'var': var,
                'member': member,
                'risk': classify(kind, member),
                'code': detail,
            })
    return hits


def iter_html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith('.html'):
                yield os.path.join(dirpath, fn)


def iter_js_files():
    jsdir = os.path.join(ROOT, 'js')
    for fn in sorted(os.listdir(jsdir)):
        if fn.endswith('.js'):
            yield os.path.join(jsdir, fn)


def main():
    results = []

    # 1) 全站 HTML 的内联脚本块
    for path in iter_html_files():
        try:
            with open(path, encoding='utf-8', errors='ignore') as f:
                html = f.read()
        except OSError:
            continue
        rel = os.path.relpath(path, ROOT)
        for block in SCRIPT_BLOCK_RE.findall(html):
            if any(mk in block for mk in STUB_MARKERS):
                continue  # stub 定义块，非风险
            base_line = html[:html.find(block)].count('\n') + 1 if block in html else 0
            for h in scan_text(block, rel):
                h['line'] = base_line + h['line'] - 1
                results.append(h)

    # 2) 外部脚本 js/*.js
    for path in iter_js_files():
        try:
            with open(path, encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except OSError:
            continue
        rel = os.path.relpath(path, ROOT)
        results.extend(scan_text(text, rel))

    out_json = None
    if '--json' in sys.argv:
        idx = sys.argv.index('--json')
        if idx + 1 < len(sys.argv):
            out_json = sys.argv[idx + 1]

    if out_json:
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print('已写入 %s（%d 项）' % (out_json, len(results)))
        return 0

    buckets = {'high': [], 'unknown': [], 'safe': []}
    for h in results:
        buckets.setdefault(h.get('risk', 'unknown'), []).append(h)

    print('扫描完成：共 %d 处缓存写法 —— 高危 %d / 待确认 %d / 安全(可忽略) %d\n'
          % (len(results), len(buckets['high']), len(buckets['unknown']),
             len(buckets['safe'])))

    if buckets['high']:
        print('🔴 高危：缓存了「入队占位」方法，点击时调用永久失效且不报错')
        for h in buckets['high']:
            print('   %s:%s  %s' % (h['source'], h['line'], h['code']))
        print()
    if buckets['unknown']:
        print('🟡 待确认：缓存了整个 ToolBox 对象，需看后续是否调用占位方法')
        for h in buckets['unknown']:
            print('   %s:%s  %s' % (h['source'], h['line'], h['code']))
        print()
    if buckets['safe']:
        print('🟢 安全（stub 已含真实实现），共 %d 处，示例：' % len(buckets['safe']))
        for h in buckets['safe'][:5]:
            print('   %s:%s  %s' % (h['source'], h['line'], h['code']))
        if len(buckets['safe']) > 5:
            print('   … 其余省略')
    return 0


if __name__ == '__main__':
    sys.exit(main())
