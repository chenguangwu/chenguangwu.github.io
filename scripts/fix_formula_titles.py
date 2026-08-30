#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch2 修复 P1-09：164 个工具的名称被「公式字符串」替换（如 "= (y₂ − y₁)/(x₂ − x₁)"）。

根因：per-industry 字典 i18n/tools/<industry>.json 的 zh-CN.title 被写成了公式，
_build.py 在 fix_tool_pages_seo 阶段用该 title 重写 HTML <title>/og:title 并生成
search-index.json 的 n 字段，导致全站（搜索结果/分享卡片/浏览器标签）显示公式。

修复策略（与构建系统对齐，避免手工改 HTML 后被下次 build 覆盖）：
  把每个坏条目的 zh-CN.title 改为其页面 <h1> 的正确中文名（已抽样验证 164 个 h1 均正确），
  然后由 _build.py 统一重写 HTML title + 重建索引。

用法：python3 scripts/fix_formula_titles.py
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS = os.path.join(ROOT, 'json', 'search-index.json')
I18N_DIR = os.path.join(ROOT, 'i18n', 'tools')

FORMULA_OPS = set('=+-−×÷√∑≈')

def is_broken(name):
    n = (name or '').strip()
    if not n:
        return False
    has_cjk = bool(re.search(r'[\u4e00-\u9fff]', n))
    if n[0] in FORMULA_OPS:
        return True
    if not has_cjk and re.search(r'[=+\-−×÷√∑≈]', n):
        return True
    return False

def extract_h1(html):
    m = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', html)
    if not m:
        return ''
    txt = re.sub(r'<[^>]+>', '', m.group(1))
    return re.sub(r'\s+', ' ', txt).strip()

def detect_indent(raw):
    # 取首个以空白开头且含双引号键的行，其前导空格数即为 indent 单位
    for line in raw.splitlines():
        if re.match(r'^\s+"', line):
            return len(line) - len(line.lstrip(' '))
    return 2

def main():
    data = json.load(open(SYS, encoding='utf-8'))
    broken = [t for t in data if is_broken(t.get('n', ''))]
    print('坏名称总数:', len(broken))

    touched = {}  # filepath -> {base: (old_title, new_title)}
    skipped = []
    for t in broken:
        ind = t.get('i')
        path = t.get('u')
        if not ind or not path or not os.path.isfile(path):
            skipped.append((path, '文件缺失/无行业'))
            continue
        html = open(path, encoding='utf-8', errors='ignore').read()
        h1 = extract_h1(html)
        if not h1:
            skipped.append((path, 'h1 为空'))
            continue
        fp = os.path.join(I18N_DIR, ind + '.json')
        if not os.path.isfile(fp):
            skipped.append((path, '字典缺失 %s' % fp))
            continue
        raw = open(fp, encoding='utf-8').read()
        d = json.loads(raw)
        base = os.path.splitext(os.path.basename(path))[0]
        entry = d.get(base)
        if not isinstance(entry, dict):
            skipped.append((path, '字典无 %s 条目' % base))
            continue
        zh = entry.setdefault('zh-CN', {})
        if not isinstance(zh, dict):
            skipped.append((path, 'zh-CN 非对象'))
            continue
        old = zh.get('title')
        zh['title'] = h1
        # h1 也一并修正（保持一致，避免后续误用）
        if 'h1' in zh and zh['h1'] != h1:
            zh['h1'] = h1
        indent = detect_indent(raw)
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=indent, separators=(',', ': '))
            f.write('\n')
        touched.setdefault(fp, {})[base] = (old, h1)

    print('已修正字典条目:', sum(len(v) for v in touched.values()))
    print('跳过:', len(skipped))
    for p, why in skipped:
        print('  SKIP', p, '-', why)
    # 写一份变更清单便于 review
    with open(os.path.join(ROOT, '_fix_formula_titles_log.txt'), 'w', encoding='utf-8') as f:
        for fp, items in touched.items():
            f.write('FILE: %s\n' % fp)
            for base, (old, new) in items.items():
                f.write('  %s: %r -> %r\n' % (base, old, new))
    print('变更清单 -> _fix_formula_titles_log.txt')

if __name__ == '__main__':
    main()
