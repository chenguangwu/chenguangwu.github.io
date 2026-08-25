# -*- coding: utf-8 -*-
"""B-OPT11：补齐缺 <h2> 标题的工具页，消除静态检查的「缺少 <h2> 标题」告警。

根因：一部分公式域工具（statistics/banking/aerospace/...）由「formula-box 前置」模板
生成，<div class="card"> 内直接以 <div class="formula-box"> 起头，漏写了工具标题 <h2>
（其他标准工具均有 <h2>工具名</h2>）。_test_static 要求页面至少含一个 <h2>。

修复：对全站「真实工具页（非重定向桩）且正文无 <h2>」的文件，提取其规范名称
（优先 <h1 class="sr-only"> 文本，回退 <title> 去 " - ToolBox"），在第一个
<div class="card"> 之后插入 <h2>名称</h2>。幂等：已含 <h2> 或已是桩则跳过。

用法：
  python3 scripts/fix_missing_h2.py --dry-run
  python3 scripts/fix_missing_h2.py
"""
import os, re, sys, json, argparse, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
TOOLS = json.load(open(os.path.join(ROOT, "json", "tools.json"), encoding="utf-8"))

CARD = re.compile(r'(<div class="card"[^>]*>)')
H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
TITLE = re.compile(r'<title>(.*?)</title>', re.S)
HAS_H2 = re.compile(r'<h2[\s>]')


def name_of(c):
    m = H1.search(c)
    if m:
        n = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if n:
            return n
    t = TITLE.search(c)
    if t:
        n = re.sub(r'\s*-\s*ToolBox\s*$', '', t.group(1)).strip()
        if n:
            return n
    return ''


def fix_one(path):
    fp = os.path.join(TOOLS_DIR, path)
    if not os.path.exists(fp):
        return 'missing'
    c = open(fp, encoding='utf-8').read()
    if 'TOOLBOX-REDIRECT' in c:
        return 'stub'
    if HAS_H2.search(c):
        return 'skip'
    name = name_of(c)
    if not name:
        return 'no-name'
    m = CARD.search(c)
    if not m:
        return 'no-card'
    fb = '\n    <h2>%s</h2>' % html.escape(name)
    c2 = c[:m.end()] + fb + c[m.end():]
    open(fp, 'w', encoding='utf-8').write(c2)
    return 'ok'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    stats = {}
    for t in TOOLS:
        p = t.get('path') or t.get('file')
        if not p:
            continue
        r = fix_one(p) if not args.dry_run else 'would-fix' if (
            os.path.exists(os.path.join(TOOLS_DIR, p))
            and 'TOOLBOX-REDIRECT' not in open(os.path.join(TOOLS_DIR, p), encoding='utf-8').read()
            and not HAS_H2.search(open(os.path.join(TOOLS_DIR, p), encoding='utf-8').read())
            and name_of(open(os.path.join(TOOLS_DIR, p), encoding='utf-8').read())
        ) else 'skip'
        if args.dry_run and r == 'would-fix':
            print("  [fix] %s  ::  %s" % (p, name_of(open(os.path.join(TOOLS_DIR, p), encoding='utf-8').read())))
        stats[r] = stats.get(r, 0) + 1
    print("结果:", stats)


if __name__ == "__main__":
    main()
