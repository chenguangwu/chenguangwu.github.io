#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 guides/ 目录主页面的 hreflang 声明错误（幂等，默认 dry-run）。

背景
----
_build.py 的 inject_hreflang() 只给工具页注入 hreflang（调用点在 3273 / 3908 行），
guids/ 下的指南页**不参与构建重写**（_build.py 对 guides 只 os.listdir 做统计
与 sitemap/hreflang XML），所以其 head 里的 hreflang 是早期各批次手写遗留，
长期无人校正，形成三类确凿错误：

  A. en-US 自指：zh-CN / en-US / x-default 三条 href 全部指向同一 URL，
     等于告诉搜索引擎"这个中文页面同时是它的英文版"，英文 UA 会被判不匹配。
  B. 缺 return tag：有独立 .en.html 英文版，但主页面完全没回引它
     （GSC 报 "Missing return tag"，.en.html 侧的 hreflang 整块失效）。
  C. 残缺：有 hreflang 块但漏了 en-US 这一条。

修法
----
按 _build.py::localized_i18n_url() 的全站既有口径，主页面块归一为三元组：

    <link rel="alternate" hreflang="zh-CN"    href="<self>">
    <link rel="alternate" hreflang="en-US"    href="<self>.en.html 或 <self>?lang=en-US">
    <link rel="alternate" hreflang="x-default" href="<self>">

English 能力判据（本批只修「有英文能力却声明错」的页）：
  * 有同名 .en.html        -> en-US 指向该独立英文页（与 17 篇已正确页同一写法）
  * 只有 guide-en-pack.js  -> en-US 指向 <self>?lang=en-US（与工具页 localized_i18n_url 同口径）

不予处理的情形（避免「声明一个不存在的英文版」这类反向误伤）：
  * 既无 .en.html 也无 guide-en-pack.js 的纯中文页 —— 它们没有 en-US 声明是**正确**的，
    即便其 head 里写着 zh-CN/x-default 自指也保持原样（4 篇残缺页属此类）；
    完全无 hreflang 的 3276 篇同理。**2026-09-17 取证：这批页面无 i18n、无英文包、
    无独立英文页，给它们补 en-US 属于制造缺陷，不是修复。**

用法
----
    python3 scripts/fix_guides_hreflang.py                 # dry-run
    python3 scripts/fix_guides_hreflang.py --apply
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES = os.path.join(ROOT, 'guides')
BASE = 'https://chenguangwu.github.io/guides/'

LINK_RE = re.compile(
    r'[ \t]*<link[^>]*?hreflang="([^"]+)"[^>]*?href="([^"]+)"[^>]*>\s*\n?'
)
# 连续 hreflang 行构成的整体块（用于幂等替换）
BLOCK_RE = re.compile(
    r'(?:[ \t]*<link[^>]*?hreflang="[^"]+"[^>]*?href="[^"]+"[^>]*>\s*\n?)+'
)
CANON_RE = re.compile(r'(<link rel="canonical" href="[^"]+"[^>]*>\s*\n?)')


def expected_block(self_url, en_url):
    lines = [
        '<link rel="alternate" hreflang="zh-CN" href="%s">' % self_url,
        '<link rel="alternate" hreflang="en-US" href="%s">' % en_url,
        '<link rel="alternate" hreflang="x-default" href="%s">' % self_url,
    ]
    return '\n'.join(lines) + '\n'


def current_map(content):
    return dict((l, h) for l, h in LINK_RE.findall(content))


def main(argv):
    apply_ = '--apply' in argv
    files = sorted(f for f in os.listdir(GUIDES)
                   if f.endswith('.html') and f != 'index.html'
                   and not f.endswith('.en.html'))
    ens = set(f for f in os.listdir(GUIDES) if f.endswith('.en.html'))

    plan = []          # (file, old_map, new_en, had_block)
    skip_clean = 0
    no_en_capability = 0
    for fn in files:
        path = os.path.join(GUIDES, fn)
        content = open(path, encoding='utf-8').read()
        self_url = BASE + fn
        cur = current_map(content)
        en_fn = fn[:-len('.html')] + '.en.html'
        has_en_file = en_fn in ens
        has_pack = 'guide-en-pack.js' in content   # 运行时英文版
        if has_en_file:
            en_url = BASE + en_fn
        elif has_pack:
            en_url = self_url + '?lang=en-US'
        else:
            # 纯中文页：没有英文版，缺 en-US 是正确的，一律不动
            no_en_capability += 1
            continue
        exp = {'zh-CN': self_url, 'en-US': en_url, 'x-default': self_url}
        if cur == exp:
            skip_clean += 1
            continue
        plan.append((fn, cur, en_url, bool(cur)))

    print('guids 主页面总数 %d | 纯中文页(无英文能力,不动) %d | 已正确 %d | 待修 %d'
          % (len(files), no_en_capability, skip_clean, len(plan)))
    kinds = {'A-en-US自指': 0, 'B-指向别处': 0, 'D-完全无hreflang': 0}
    for fn, cur, en_url, had in plan:
        if not had:
            kinds['D-完全无hreflang'] += 1
        elif cur.get('en-US') == cur.get('zh-CN'):
            kinds['A-en-US自指'] += 1
        else:
            kinds['B-指向别处'] += 1
    print('  缺陷分布:', kinds)
    print('  样例:')
    for fn, cur, en_url, had in plan[:8]:
        print('    %-46s old=%s' % (fn, (cur.get('en-US') or '(none)').rsplit('/', 1)[-1]))
        print('    %-46s new=%s' % ('', en_url.rsplit('/', 1)[-1]))
    if not apply_:
        print('\n[dry-run] 未写盘。确认无误后加 --apply')
        return 0

    wrote = 0
    for fn, cur, en_url, had in plan:
        path = os.path.join(GUIDES, fn)
        content = open(path, encoding='utf-8').read()
        self_url = BASE + fn
        block = expected_block(self_url, en_url)
        if had:
            new, n = BLOCK_RE.subn(lambda m: block, content, count=1)
            if n != 1:
                print('  !! 替换失败(块匹配异常) 跳过:', fn)
                continue
        else:
            m = CANON_RE.search(content)
            if m:
                new = content[:m.end()] + block + content[m.end():]
            else:
                hp = content.find('</head>')
                if hp < 0:
                    print('  !! 无 </head> 跳过:', fn)
                    continue
                new = content[:hp] + block + content[hp:]
        if new != content:
            open(path, 'w', encoding='utf-8').write(new)
            wrote += 1
    print('[apply] 已写入 %d 篇' % wrote)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
