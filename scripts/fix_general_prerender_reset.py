#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重置 general 页面被 _build.py 预渲染的 h2 / formula-desc，使新英文数据源得以生效（§4.1.5）。

问题：_build.py 的 _prerender_tool_body 是幂等的——只要 h2 / 首个 <p> 已是英文（无 CJK）就跳过，
不会用新数据源更新。因此仅改 general-body.json / _en_override.json 不会传播到已预渲染的页面。

做法：
  1) 首个 <h2 data-zh="中文原文">英文…</h2> → <h2>中文原文</h2>（还原中文，build 会重新注入新英文名）
  2) <p class="formula-desc" …>…</p> → <div class="formula-desc">中文</div>
     formula-box 插在 intro 之前时 formula-desc 会成为「首个 <p>」，被预渲染注入 intro（曾致占位串）；
     改为 <div> 后 build 不再触碰（与 it 分类同法），中文原样保留，CSS `.formula-box .formula-desc` 渲染一致。
  3) 其余 intro <p>（data-zh + 真实英文）保持不变——英文即 EN_MAP，与 general-body.json 同源。

用法：
  python3 scripts/fix_general_prerender_reset.py --dry-run
  python3 scripts/fix_general_prerender_reset.py --apply
"""
import argparse, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDIR = os.path.join(ROOT, "tools", "general")


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
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        print("请指定 --dry-run 或 --apply")
        return 2

    files = [f for f in sorted(glob.glob(os.path.join(GDIR, "*.html"))) if os.path.basename(f) != "index.html"]
    tot_h2 = tot_fd = changed = 0
    preview = []
    for f in files:
        html = open(f, encoding="utf-8").read()
        h2, n1 = reset_h2(html)
        fd, n2 = reset_formula_desc(h2)
        tot_h2 += n1
        tot_fd += n2
        if fd != html:
            changed += 1
            if len(preview) < 3:
                preview.append((os.path.basename(f), n1, n2))
            if a.apply:
                open(f, "w", encoding="utf-8").write(fd)
    print(f"页面 {len(files)}；h2 还原 {tot_h2} 处；formula-desc 改 div {tot_fd} 处；有改动文件 {changed}")
    for p in preview:
        print("  预览 %s: h2=%d formula-desc=%d" % p)
    if a.dry_run:
        return 0
    print("已写入")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
