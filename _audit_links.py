#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站内部链接完整性审计（维护迭代模式 · 死链检查）。

扫描仓库内所有 HTML 文件，提取内部链接（相对路径 / 根绝对路径），
验证目标文件是否存在。

两种模式：
  - 默认（报告模式）：输出 _audit_links_report.txt / .json / _audit_links_broken.json，
    退出码恒为 0（仅报告，不阻断）。
  - --check（门禁模式）：仅校验、不写报告文件；存在死链时退出码为 1，
    可用于发布前门禁（如本地发布脚本 / CI）。

不发送任何网络请求；纯本地文件系统校验。会智能排除 <script>/<style> 块内的
教学示例源码与 JS 运行时伪链（$1 / ${} 等），避免误报。
"""
import os, re, sys, json
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

SKIP_PREFIX = ('http://', 'https://', '//', 'mailto:', 'tel:', 'data:',
               'javascript:', '#')
HREF_RE = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.I)
# JS 运行时伪链（正则替换反引用 / 模板字面量），不是静态死链，必须排除
JS_ARTIFACT = re.compile(r'\$\d|\$\{')
# 示例/教学代码常出现在 <script>/<style> 块内（如代码高亮工具展示的源码），
# 其中的 href 并非真实导航链接，扫描前应剔除，避免误报。
SCRIPT_RE = re.compile(r'<script[\s>].*?</script>', re.I | re.S)
STYLE_RE = re.compile(r'<style[\s>].*?</style>', re.I | re.S)

def build_existing():
    existing = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # 跳过开发/构建/隐藏目录
        parts = dirpath[len(ROOT):].split(os.sep)
        if any(p in ('.git', 'node_modules', '.workbuddy', 'scripts',
                     '_regression_shots', '__pycache__', 'venv') for p in parts):
            continue
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, '/')
            existing.add(rel)
    return existing

def is_internal(target):
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

def resolve(target, src_rel, existing):
    """返回 (resolved_rel_or_none, is_dir_route)"""
    t = target.strip()
    if t.startswith('/'):
        cand = t[1:].lstrip('/')
    else:
        base = os.path.dirname(src_rel)
        cand = os.path.normpath(os.path.join(base, t)).replace(os.sep, '/')
    # 去掉 fragment
    cand = cand.split('#')[0]
    if cand == '' or cand.endswith('/'):
        # 目录路由 → 尝试 index.html
        idx = (cand + 'index.html').lstrip('/')
        if idx in existing:
            return idx, True
        return None, True
    if cand in existing:
        return cand, False
    # 尝试补 index.html
    idx = cand.rstrip('/') + '/index.html'
    if idx in existing:
        return idx, True
    return None, False

def main():
    import argparse
    ap = argparse.ArgumentParser(description='全站内部链接完整性审计 / 发布门禁')
    ap.add_argument('--check', action='store_true',
                    help='门禁模式：仅校验，不写入报告文件；存在死链则返回退出码 1')
    ap.add_argument('--quiet', action='store_true',
                    help='静默进度输出（stderr）')
    args = ap.parse_args()

    def log(*a):
        if not args.quiet:
            print(*a, file=sys.stderr)

    existing = build_existing()
    log('候选文件数: %d' % len(existing))

    html_files = sorted(f for f in existing if f.endswith('.html'))
    log('待扫描 HTML 文件数: %d' % len(html_files))

    # 统计：broken_target -> Counter(src_file -> count)
    broken = defaultdict(Counter)
    total_links = 0
    checked_links = 0
    scanned = 0

    for f in html_files:
        try:
            with open(os.path.join(ROOT, f), 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
        except Exception:
            continue
        scanned += 1
        # 仅审计 href（导航/内链）；先剔除 <script>/<style> 块（示例源码非真实链接）
        content = SCRIPT_RE.sub('', content)
        content = STYLE_RE.sub('', content)
        for m in HREF_RE.finditer(content):
            target = m.group(1)
            if not is_internal(target):
                continue
            total_links += 1
            resolved, _ = resolve(target, f, existing)
            if resolved is None:
                checked_links += 1
                broken[target][f] += 1

    by_impact = sorted(broken.items(), key=lambda kv: sum(kv[1].values()), reverse=True)
    total_broken = sum(sum(c.values()) for c in broken.values())

    # —— 门禁模式：仅校验，不落盘，存在死链返回 1 ——
    if args.check:
        if broken:
            print('❌ 死链门禁失败：%d 个死链目标 / %d 处引用' % (len(broken), total_broken),
                  file=sys.stderr)
            for t, s in by_impact[:20]:
                print('   - %s  [%d 次 / %d 页]' % (t, sum(s.values()), len(s)),
                      file=sys.stderr)
            return 1
        print('✅ 死链门禁通过：扫描 %d 文件 / %d 内链，0 死链' % (scanned, total_links),
              file=sys.stderr)
        return 0

    # —— 报告模式：写报告文件（不改变退出码） ——
    lines = []
    lines.append('=' * 70)
    lines.append('ToolBox 全站内部链接完整性审计')
    lines.append('=' * 70)
    lines.append('扫描 HTML 文件 : %d' % scanned)
    lines.append('内部链接总数   : %d' % total_links)
    lines.append('死链目标数     : %d' % len(broken))
    lines.append('死链引用次数   : %d' % total_broken)
    lines.append('')
    if not broken:
        lines.append('✅ 未发现任何死链（所有内部链接均可解析到现有文件）。')
    else:
        lines.append('— 按影响面排序的死链目标（Top 60）—')
        for i, (target, srcs) in enumerate(by_impact[:60], 1):
            cnt = sum(srcs.values())
            lines.append('%2d. [%d 次 / %d 页] %s' % (i, cnt, len(srcs), target))
            # 列出最多 3 个来源
            for sf, c in srcs.most_common(3):
                lines.append('       ↳ %s (%d)' % (sf, c))
    report = '\n'.join(lines)

    with open(os.path.join(ROOT, '_audit_links_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write(report + '\n')
    with open(os.path.join(ROOT, '_audit_links_report.json'), 'w', encoding='utf-8') as fh:
        json.dump({
            'scanned': scanned,
            'total_links': total_links,
            'broken_targets': len(broken),
            'broken_refs': total_broken,
            'top': [{'target': t, 'refs': sum(s.values()), 'pages': len(s),
                     'sample_sources': s.most_common(5)} for t, s in by_impact[:60]]
        }, fh, ensure_ascii=False, indent=2)
    # 全量死链 + 分类，便于后续修复
    import re as _re
    def _cat(t):
        if _re.match(r'^/about|^/privacy|^/terms|^/contact', t):
            return 'site_page_missing'
        if 'tools/tools/' in t or t.count('tools/') > 1:
            return 'double_prefix'
        if _re.search(r'tool-\d+-\d+\.html', t):
            return 'old_toolname'
        if t.startswith('tools/') and t.endswith('.html'):
            return 'tools_pinyin_missing'
        return 'other'
    cat_counter = Counter(_cat(t) for t in broken)
    full = [{'target': t, 'refs': sum(s.values()), 'pages': len(s), 'cat': _cat(t),
             'sources': s.most_common(3)} for t, s in
            sorted(broken.items(), key=lambda kv: sum(kv[1].values()), reverse=True)]
    with open(os.path.join(ROOT, '_audit_links_broken.json'), 'w', encoding='utf-8') as fh:
        json.dump({'categories': dict(cat_counter), 'broken': full}, fh,
                  ensure_ascii=False, indent=2)
    print('分类汇总: %s' % dict(cat_counter), file=sys.stderr)

    print(report)
    return 0

if __name__ == '__main__':
    sys.exit(main())
