# -*- coding: utf-8 -*-
"""给「intro 段落是英文自然语言、却没注册 data-i18n」的工具页补上 i18n 注册。

现象：这些页的 intro <p> 在构建期被 _prerender_tool_body 预渲染成英文（或本来就是英文），
      但既没有 data-zh（中文原文），也没有 data-i18n + data-i18n-fb（运行时翻译通道），
      于是中文用户打开页面看到英文简介。

修法：补 data-i18n="<industry>.<slug>.intro" data-i18n-fb="<中文简介>"，
      与已正常工作的手工页（如 design/color-picker）写法保持一致。
      中文简介取自 i18n/tools/<industry>.json 的 zh-CN.intro（权威源）。

判定会跳过：公式/缩写/标签型段落（L = ½ρV²SC_L、HbA1c 等跨语言符号本就无需翻译）。

用法：python3 scripts/fix_intro_i18n.py          # dry-run
      python3 scripts/fix_intro_i18n.py --apply  # 落盘
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
INTRO_STYLE = 'font-size:13px;color:var(--text-muted)'
P_TAG = re.compile(r'<p\b([^>]*)>')
GREEK = 'αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΠΣΦΨΩ₀₁₂₃₄₅₆₇₈₉½·×÷√∝∞∑∏∫≈≠≤≥±'


def esc_attr(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def load_json(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return {}


def needs_fix(inner):
    """仅修「英文自然语言句」，跳过公式/缩写/标签。"""
    if not inner.strip():
        return False
    if '=' in inner:
        return False                      # 公式
    if any(c in GREEK for c in inner):
        return False                      # 含希腊字母的变量式
    words = re.findall(r'[A-Za-z]{4,}', inner)
    return len(words) >= 4                # 至少 4 个实词才算自然语言句


def first_intro_span(src):
    """返回页面首个 intro 样式 <p> 的 (属性起始, 标签结束, 属性串)。"""
    for m in re.finditer(r'<p\b([^>]*)>', src):
        if INTRO_STYLE in m.group(1):
            return m
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='落盘（默认干跑）')
    args = ap.parse_args()

    cache = {}
    plan = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True)):
        rel = os.path.relpath(path, ROOT)
        rel_page = rel[len('tools/'):-len('.html')]
        if '/' in rel_page:
            ind, slug = rel_page.split('/', 1)
        else:
            ind, slug = '', rel_page
        src = open(path, encoding='utf-8', errors='replace').read()

        m = first_intro_span(src)
        if not m:
            continue
        attrs = m.group(1)
        if 'data-zh=' in attrs or 'data-i18n=' in attrs:
            continue                       # 已有中文通道
        # 取该 p 的内容（到 </p>）
        end = src.find('</p>', m.end())
        inner = re.sub(r'<[^>]+>', '', src[m.end():end if end > 0 else m.end() + 400])
        inner = inner.strip()
        if CJK.search(inner) or not needs_fix(inner):
            continue

        if ind not in cache:
            cache[ind] = load_json(os.path.join(ROOT, 'i18n', 'tools', '%s.json' % ind))
        zh_intro = ((cache[ind] or {}).get(slug, {}).get('zh-CN') or {}).get('intro', '').strip()
        if not zh_intro:
            continue

        key = '%s.%s.intro' % (ind, slug)
        new_attrs = attrs.rstrip()
        if not new_attrs.endswith(' '):
            new_attrs += ' '
        new_attrs += 'data-i18n="%s" data-i18n-fb="%s"' % (key, esc_attr(zh_intro))
        plan.append((path, key, inner[:56], zh_intro[:44], m.start(1), m.end(1), new_attrs))

    print('待修复页面数: %d%s' % (len(plan), '' if args.apply else '  (dry-run，加 --apply 落盘)'))
    for path, key, cur, zh, *_ in plan:
        print('  %s' % os.path.relpath(path, ROOT))
        print('      data-i18n = %s' % key)
        print('      当前(英文) = %r' % cur)
        print('      fb(中文)   = %r' % zh)

    if not args.apply or not plan:
        return

    # 落盘（按文件倒序替换 offset，避免位移）
    by_file = {}
    for path, key, cur, zh, s, e, new_attrs in plan:
        by_file.setdefault(path, []).append((s, e, new_attrs))
    n = 0
    for path, edits in by_file.items():
        src = open(path, encoding='utf-8', errors='replace').read()
        for s, e, new_attrs in sorted(edits, key=lambda x: -x[0]):
            src = src[:s] + new_attrs + src[e:]
        open(path, 'w', encoding='utf-8').write(src)
        n += 1
    print('已落盘: %d 个文件' % n)


if __name__ == '__main__':
    sys.exit(main())
