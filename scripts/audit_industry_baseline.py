# -*- coding: utf-8 -*-
"""§9.2 单分类八项基线审计（A/B/C/D/E 前置）

用法: python3 scripts/audit_industry_baseline.py --ind <行业名>
只读，不改任何文件。
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = 'is available directly in your browser'


def find_cat_defs():
    """从 _build.py 抓 CAT_DEFS 的键集合（须定位定义处 `CAT_DEFS = {`，非用法处）"""
    src = open(os.path.join(ROOT, '_build.py'), encoding='utf-8').read()
    m = re.search(r'^CAT_DEFS\s*=\s*\{', src, re.M)
    if not m:
        # 兼容缩进/字典推导等写法
        m = re.search(r'CAT_DEFS\s*=\s*\{', src)
    if not m:
        return None
    j = src.find('{', m.start())
    depth = 0
    k = j
    while k < len(src):
        if src[k] == '{':
            depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0:
                break
        k += 1
    block = src[j:k + 1]
    keys = set(re.findall(r"^\s+'([a-zA-Z0-9_\-]+)':", block, re.M))
    if not keys:
        keys = set(re.findall(r"'([a-zA-Z0-9_\-]+)'\s*:", block))
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ind', required=True)
    a = ap.parse_args()
    ind = a.ind
    TOOLS = os.path.join(ROOT, 'tools', ind)
    if not os.path.isdir(TOOLS):
        print('ERROR: 目录不存在', TOOLS)
        sys.exit(1)

    pages = sorted(f[:-5] for f in os.listdir(TOOLS)
                  if f.endswith('.html') and f != 'index.html')
    print('=' * 70)
    print('行业: %s   磁盘工具页: %d' % (ind, len(pages)))
    print('=' * 70)

    # --- cat 有效性 ---
    catdefs = find_cat_defs()
    print('\n[0] cat 有效性')
    if catdefs is not None:
        print('    CAT_DEFS 键数:', len(catdefs))
        print('    `%s` ∈ CAT_DEFS: %s' % (ind, ind in catdefs))
    else:
        print('    未能在 _build.py 定位 CAT_DEFS')

    # --- deep-dive ---
    dd_path = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
    dd = json.load(open(dd_path, encoding='utf-8'))
    dd_keys = sorted(k for k in dd if k.startswith(ind + '/'))
    dd_slugs = set(k.split('/', 1)[1] for k in dd_keys)
    print('\n[A] deep-dive: %d 键' % len(dd_keys))
    dd_orphan = [k for k in dd_keys if k.split('/', 1)[1] not in pages]
    dd_missing = [p for p in pages if (ind + '/' + p) not in dd]
    print('    孤儿键(无磁盘页): %d %s' % (len(dd_orphan), dd_orphan[:10]))
    print('    缺解析的页: %d %s' % (len(dd_missing), dd_missing[:10]))

    # --- body json / enmap ---
    body_path = os.path.join(ROOT, 'i18n', 'tools', '%s-body.json' % ind)
    if os.path.exists(body_path):
        body = json.load(open(body_path, encoding='utf-8'))
        bkeys = list(body.keys())
        print('\n[B1] %s-body.json: %d 键' % (ind, len(bkeys)))
        sample = bkeys[0] if bkeys else None
        print('     键格式示例:', repr(sample))
        if sample and '/' in sample:
            bslugs = set(k.split('/', 1)[1] for k in bkeys)
        else:
            bslugs = set(bkeys)
        print('     孤儿(无磁盘页):',
              sorted(s for s in bslugs if s not in pages))
    else:
        print('\n[B1] body json 缺失:', body_path)

    print('     enmap 是否存在:',
          os.path.exists(os.path.join(ROOT, 'scripts', 'enmap', ind + '.json')))

    # --- industry json cat ---
    ij_path = os.path.join(ROOT, 'json', 'industry-%s.json' % ind)
    if os.path.exists(ij_path):
        ij = json.load(open(ij_path, encoding='utf-8'))
        from collections import Counter
        print('\n[B2] industry-%s.json: %d 条' % (ind, len(ij)))
        print('     cat 分布:', dict(Counter(x.get('cat') for x in ij)))
        for x in ij:
            if x.get('cat') != ind:
                print('     非本行业 cat:',
                      x.get('file'), x.get('name'), '->', x.get('cat'))
    else:
        print('\n[B2] industry json 缺失:', ij_path)

    # --- 逐页 UI / 英文 / formula ---
    print('\n[B3][C] 逐页审计（英文占位 / formula 框 / number input）')
    en_placeholder = []
    desc_en_missing = []
    no_formula_needing = []
    no_formula_ok = []
    for s in pages:
        t = open(os.path.join(TOOLS, s + '.html'), encoding='utf-8').read()
        if PLACEHOLDER in t:
            en_placeholder.append(s)
        # desc-en 占位判定：存在 data-en 的 description 为空/含占位
        md = re.search(
            r'<meta\b[^>]*\bname="description"[^>]*\bcontent="([^"]*)"', t)
        desc = md.group(1) if md else ''
        if not desc or PLACEHOLDER in desc:
            desc_en_missing.append(s)
        nnum = len(re.findall(r'type="number"', t))
        has_fb = 'formula-box' in t
        if has_fb:
            continue
        if nnum >= 2:
            no_formula_needing.append((s, nnum))
        else:
            no_formula_ok.append((s, nnum))
    print('     English placeholder 套话页数:', len(en_placeholder))
    print('     desc 空/占位页数:', len(desc_en_missing))
    print('     formula 已覆盖:', len(pages) - len(no_formula_needing)
          - len(no_formula_ok))
    print('     缺框且 number>=2（须补）: %d %s'
          % (len(no_formula_needing), no_formula_needing[:12]))
    print('     无框但 number<2（豁免）: %d %s'
          % (len(no_formula_ok), no_formula_ok[:12]))

    # --- 计算函数形态 ---
    print('\n[D] 计算函数形态')
    fnmap = {}
    for s in pages:
        t = open(os.path.join(TOOLS, s + '.html'), encoding='utf-8').read()
        fns = []
        for fn in ('calcTool', 'calc', 'calculate', 'compute', 'convert'):
            if re.search(r'function\s+%s\s*\(' % fn, t):
                fns.append(fn)
        fnmap[s] = fns
    from collections import Counter as C2
    print('     ', dict(C2(tuple(v) for v in fnmap.values())))
    for s in pages:
        if not fnmap[s]:
            print('     无已知计算函数:', s)

    # --- guides ---
    gj_path = os.path.join(ROOT, 'json', 'guides.json')
    gj = json.load(open(gj_path, encoding='utf-8'))
    # guides.json 为 list[{"tool","guide","title"}]，tool 用相对行业目录的文件名
    if isinstance(gj, list):
        gj_keys = set(str(x.get('tool', '')) for x in gj)
        sample = list(gj_keys)[:2] if gj_keys else None
    else:
        gj_keys = set(gj.keys())
        sample = list(gj_keys)[:2]
    have = [s for s in pages if ('%s.html' % s) in gj_keys
            or ('%s/%s.html' % (ind, s)) in gj_keys]
    print('\n[E] guides.json 条目总数:', len(gj))
    print('     %s 命中: %d / %d' % (ind, len(have), len(pages)))
    print('     guides key 样例:', sample)
    if not have and pages:
        print('     ⚠ 该行业 0 指南覆盖 → Step E 需执行 gen_industry_guides.py')

    print('\n' + '=' * 70)
    print('审计完成')


if __name__ == '__main__':
    main()
