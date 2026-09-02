#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从一个工具页 HTML 中抽取「可见中文串」，供 i18n/tools/<industry>-phrases.json 使用。

输出格式：  标签名\t是否纯文本\t中文串
  - 纯文本 = 该节点内部没有任何子元素（textContent 替换安全，可直接进 phrases）
  - 非纯文本 = 含子元素（进 phrases 会吞掉子元素，必须先拆成纯文本片段）

抽取范围（与 js/tool-i18n.js translateBodyPhrases 的 selector 对齐）：
  h1 h3 h4 p:not(.intro) li th td label button.btn select>option textarea span a div
  外加属性：placeholder / title / aria-label / alt

用法：
  python3 scripts/extract_zh_phrases.py tools/colorvision/colorblind-simulator.html
"""
import re
import sys

# translateBodyPhrases 实际处理的标签
SEL = ('h1', 'h3', 'h4', 'p', 'li', 'th', 'td', 'label', 'button', 'option',
       'textarea', 'span', 'a', 'div')
SKIP_TAGS = ('script', 'style', 'noscript', 'svg')
ATTRS = ('placeholder', 'title', 'aria-label', 'alt')

TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>')
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


def strip_noise(html: str) -> str:
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    for tag in SKIP_TAGS:
        html = re.sub(r'<%s\b.*?</%s>' % (tag, tag), '', html, flags=re.S | re.I)
    return html


def has_zh(s: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', s))


def norm(s: str) -> str:
    import html as _h
    return re.sub(r'\s+', ' ', _h.unescape(s)).strip()


def main(path: str):
    raw = open(path, encoding='utf-8').read()
    body = strip_noise(raw)

    rows = []       # (tag, pure, text)
    seen = set()

    def add(tag, pure, text):
        t = norm(text)
        if not t or not has_zh(t):
            return
        key = (tag, pure, t)
        if key in seen:
            return
        seen.add(key)
        rows.append((tag, pure, t))

    # 栈元素：[tag, textbuf, has_child]
    stack = []

    def add_attrs(tag, attrs):
        for a in ATTRS:
            am = re.search(r'\b%s\s*=\s*"([^"]*)"' % a, attrs)
            if am:
                add(tag + '@' + a, True, am.group(1))
            am2 = re.search(r"\b%s\s*=\s*'([^']*)'" % a, attrs)
            if am2:
                add(tag + '@' + a, True, am2.group(1))

    for m in re.finditer(r'<[^>]+>|[^<]+', body):
        s = m.group(0)
        if not s.startswith('<'):
            if stack:
                stack[-1][1] += s
            continue
        tm = TAG_RE.match(s)
        if not tm:
            continue
        closing, tag, attrs = tm.group(1), tm.group(2).lower(), tm.group(3)
        if closing:
            buf = []
            child = False
            while stack:
                top = stack.pop()
                buf.insert(0, top[1])
                child = child or top[2]
                if top[0] == tag:
                    break
            if tag in SEL:
                add(tag, not child, ''.join(buf))
        elif tag in VOID or attrs.rstrip().endswith('/'):
            # input/br/img 等 void 元素同样是子元素：textContent 替换会把它们一起清掉
            if stack:
                stack[-1][2] = True
            add_attrs(tag, attrs)
        else:
            # 有父节点 => 父节点含子元素
            if stack:
                stack[-1][2] = True
            stack.append([tag, '', False])
            add_attrs(tag, attrs)

    for tag, pure, t in rows:
        print('%s\t%s\t%s' % (tag, 'PURE' if pure else 'MIXED', t))
    n_mixed = sum(1 for r in rows if not r[1])
    print('\n# TOTAL %d   MIXED(需拆分) %d' % (len(rows), n_mixed), file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
