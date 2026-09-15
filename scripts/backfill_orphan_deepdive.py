#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A 项批2-P0：反解析页面既有「📚 深度解析」块 → 写回 content_deepdive.json 数据源。

背景：30 个页面有深度块但 JSON 无源键，下次 _build.py 会按 _DEEP_DIVE_BLOCK_RE
清掉旧块、因无数据而不注入 → 内容永久丢失。本脚本无损回收这些既有内容。
"""
import json, os, re, sys, html as H

ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io'
DD_PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

BLOCK_RE = re.compile(
    r'<!-- TOOLBOX-DEEP-DIVE -->\s*'
    r'<style>\s*\.deep-dive[\s\S]*?</style>\s*'
    r'<section class="deep-dive"[^>]*>([\s\S]*?)</section>',
    re.I,
)
SC_RE = re.compile(r'<li>([\s\S]*?)</li>', re.I)
EX_RE = re.compile(
    r'<div class="dd-example">\s*<div class="dd-ex-title">([\s\S]*?)</div>\s*<div class="dd-ex-body">([\s\S]*?)</div>\s*</div>',
    re.I)
FAQ_RE = re.compile(r'<dt>([\s\S]*?)</dt>\s*<dd>([\s\S]*?)</dd>', re.I)


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = H.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def parse_page(path):
    h = open(path, encoding='utf-8').read()
    m = BLOCK_RE.search(h)
    if not m:
        return None
    seg = m.group(1)
    t = re.search(r'<h2>\s*📚\s*深度解析[：:]\s*([\s\S]*?)</h2>', seg)
    title = clean(t.group(1)) if t else ''
    sc_m = re.search(r'<ul class="dd-list">([\s\S]*?)</ul>', seg)
    scenarios = [clean(x) for x in SC_RE.findall(sc_m.group(1))] if sc_m else []
    scenarios = [x for x in scenarios if x]
    examples = [{'title': clean(a), 'body': clean(b)} for a, b in EX_RE.findall(seg)]
    faqs = [{'q': clean(a), 'a': clean(b)} for a, b in FAQ_RE.findall(seg)]
    if not (title or scenarios or examples or faqs):
        return None
    return {'title': title, 'scenarios': scenarios, 'examples': examples, 'faqs': faqs}


def main(apply=False):
    DD = json.load(open(DD_PATH, encoding='utf-8'))
    keys = json.load(open('/tmp/dd_nokey.json', encoding='utf-8'))
    out = []
    for k in keys:
        if k in DD:
            continue
        cat, base = k.split('/', 1)
        p = os.path.join(ROOT, 'tools', cat, base + '.html')
        if not os.path.exists(p):
            print('  MISS-PAGE', k); continue
        d = parse_page(p)
        if not d:
            print('  NO-BLOCK', k); continue
        DD[k] = d
        out.append((k, len(d['scenarios']), len(d['examples']), len(d['faqs'])))
    print('反解析回填 %d 条' % len(out))
    ok = 0
    for k, s, e, f in out:
        flag = 'OK ' if (s >= 2 and e >= 1 and f >= 2) else 'THIN'
        if flag == 'OK ': ok += 1
        print('  %s %-46s sc=%d ex=%d fa=%d' % (flag, k, s, e, f))
    print('达标 %d / %d' % (ok, len(out)))
    if apply:
        # 保持仓库规范 indent=1
        cur = open(DD_PATH, encoding='utf-8').read()
        new = json.dumps(DD, ensure_ascii=False, indent=1)
        if not cur.endswith('\n'):
            new = new  # 原文无尾换行则不加
        else:
            new += '\n'
        open(DD_PATH, 'w', encoding='utf-8').write(new)
        print('已落盘', DD_PATH)
    else:
        print('（dry-run，未落盘）')


if __name__ == '__main__':
    main('--apply' in sys.argv)
