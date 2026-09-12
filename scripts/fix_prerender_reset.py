#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重置分类页面被 _build.py 预渲染的 h2 / intro <p> / formula-desc，使新英文数据源得以生效（§4.1.5）。

问题：_build.py 的 _prerender_tool_body 是幂等的——只要 h2 / 首个 <p> 已是英文（无 CJK）就跳过，
不会用新数据源更新。因此仅改 <ind>-body.json / _en_override.json 不会传播到已预渲染的页面。
（general 与 finance 均踩此坑，见 §6「build 预渲染陷阱」）

做法（按 --industry 指定分类目录）：
  1) 首个 <h2 data-zh="中文原文">英文…</h2> → <h2>中文原文</h2>（还原中文，build 会重新注入新英文名）
  2) --intro-p 时，首个 <p data-zh="中文">英文…</p> → <p>中文</p>
     （finance 的首页 intro 段落是历史套话英文，必须还原为 data-zh 中文后由 build 重新注入）
  3) <p class="formula-desc" …>…</p> → <div class="formula-desc">中文</div>
     formula-box 插在 intro 之前时 formula-desc 会成为「首个 <p>」，被预渲染注入 intro（曾致占位串）；
     改为 <div> 后 build 不再触碰，中文原样保留，CSS `.formula-box .formula-desc` 渲染一致。

用法：
  python3 scripts/fix_prerender_reset.py --industry general --dry-run
  python3 scripts/fix_prerender_reset.py --industry finance --intro-p --apply
"""
import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def reset_h2(html):
    """首个含 data-zh 的 h2 还原为纯中文。"""
    n = 0

    def rep(m):
        nonlocal n
        if n >= 1:
            return m.group(0)
        n += 1
        attrs_before, zh, attrs_after = m.group(1), m.group(2), m.group(3)
        other = (attrs_before + attrs_after).strip()
        other = re.sub(r'\s+', ' ', other)
        head = (' <h2 %s>' % other) if other else ' <h2>'
        return head + zh + '</h2>'

    out = re.sub(r'<h2([^>]*?)\sdata-zh="([^"]*)"([^>]*?)>[\s\S]*?</h2>', rep, html, count=1)
    return out, n


def reset_intro_p(html):
    """首个 <p data-zh> 且 inner 为英文（无 CJK）时，还原为 data-zh 中文并去掉 data-zh。"""
    n = 0

    def rep(m):
        nonlocal n
        if n >= 1:
            return m.group(0)
        open_tag, attrs, inner, close = m.group(1), m.group(2), m.group(3), m.group(4)
        zh = re.search(r'data-zh="([^"]*)"', attrs)
        if not zh:
            return m.group(0)
        if re.search(r'[\u4e00-\u9fff]', inner):
            return m.group(0)  # 已是中文，不动
        n += 1
        attrs2 = re.sub(r'\s*data-zh="[^"]*"', '', attrs)
        return '%s%s>%s%s' % (open_tag, attrs2, zh.group(1), close)

    out = re.sub(r'(<p\b)([^>]*>)([\s\S]*?)(</p>)', rep, html, count=1)
    return out, n


def reset_formula_desc(html):
    """所有 formula-desc 的 <p> 改 <div>；有 data-zh 用其中文，否则用原 inner。"""
    cnt = 0

    def rep(m):
        nonlocal cnt
        attrs, inner = m.group(1), m.group(2)
        zh = re.search(r'data-zh="([^"]*)"', attrs)
        text = zh.group(1) if zh else inner.strip()
        cnt += 1
        return '<div class="formula-desc">%s</div>' % text

    out = re.sub(r'<p class="formula-desc"([^>]*)>([\s\S]*?)</p>', rep, html)
    return out, cnt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--industry', default='general', help='tools/<industry>/ 目录名')
    ap.add_argument('--intro-p', action='store_true', help='同时还原首个 <p data-zh> 的英文 inner')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        print('请指定 --dry-run 或 --apply')
        return 2

    gdir = os.path.join(ROOT, 'tools', a.industry)
    files = [f for f in sorted(glob.glob(os.path.join(gdir, '*.html'))) if os.path.basename(f) != 'index.html']
    if not files:
        print('未找到页面:', gdir)
        return 2
    tot_h2 = tot_fd = tot_p = changed = 0
    preview = []
    for f in files:
        html = open(f, encoding='utf-8').read()
        h2, n1 = reset_h2(html)
        fd, n2 = reset_formula_desc(h2)
        p, n3 = reset_intro_p(fd) if a.intro_p else (fd, 0)
        tot_h2 += n1
        tot_fd += n2
        tot_p += n3
        if p != html:
            changed += 1
            if len(preview) < 3:
                preview.append((os.path.basename(f), n1, n3, n2))
            if a.apply:
                open(f, 'w', encoding='utf-8').write(p)
    print(f'[{a.industry}] 页面 {len(files)}；h2 还原 {tot_h2} 处；intro <p> 还原 {tot_p} 处；'
          f'formula-desc 改 div {tot_fd} 处；有改动文件 {changed}')
    for pv in preview:
        print('  预览 %s: h2=%d intro_p=%d formula_desc=%d' % pv)
    if a.dry_run:
        return 0
    print('已写入')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
