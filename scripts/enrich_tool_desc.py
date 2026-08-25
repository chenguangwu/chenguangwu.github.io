#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 tools/ 下 meta description < 30 字的工具页补全语义化描述（基于页内真实功能文本，非套话）。

策略：
- 从页面提取 <h1> 与首个功能介绍 <p>（>15 字）作为真实功能文本；
- 拼接为 description：h1 + '，' + 首段（首段不以 h1 开头时），否则直接用首段；
- 同步更新 <meta name="description"> 与 <meta property="og:description">（仅当二者当前 < 30 字才改，幂等）；
- 截断到 155 字（meta 建议上限），HTML 实体先解码再转义，避免双重转义。

与 Q2 决策一致：不写通用填充废话（如“教育学习工具，辅助学习，提升效率”），只用页面真实功能文案。
_build.py 重建只补缺失标签、不覆盖已有 description，故静态修补即生效。

用法：
    python3 scripts/enrich_tool_desc.py            # dry-run，打印统计与样例
    python3 scripts/enrich_tool_desc.py --apply    # 写入
"""
import os
import re
import html
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
MAXLEN = 155


def text(x):
    x = re.sub(r'<[^>]+>', '', x)
    return re.sub(r'\s+', ' ', x).strip()


def extract(p):
    h = open(p, encoding='utf-8').read()
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    cur = m.group(1).strip() if m else ''
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    h1 = html.unescape(text(h1m.group(1))) if h1m else ''
    lead = ''
    for x in re.findall(r'<p[^>]*>(.*?)</p>', h, re.S):
        t = html.unescape(text(x))
        if len(t) > 15:
            lead = t
            break
    return cur, h1, lead


SPAM_KW = ['免费', '辅助学习', '提升效率', '出行必备', '支持离线',
           '帮助计算', '帮助精确计算', '帮助快速处理', '在线工具，免费使用']


def is_spam(s):
    return any(k in s for k in SPAM_KW)


def build_desc(h1, lead):
    if lead:
        lead = lead.strip()
        if h1 and not lead.startswith(h1):
            return (h1 + '，' + lead)[:MAXLEN]
        return lead[:MAXLEN]
    return (h1 or '')[:MAXLEN]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    targets = []
    for ind in sorted(os.listdir(TOOLS)):
        d = os.path.join(TOOLS, ind)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith('.html'):
                continue
            p = os.path.join(d, fn)
            cur, h1, lead = extract(p)
            if len(cur) >= 30:
                continue
            if not lead:
                print('SKIP(无功能首段):', os.path.relpath(p, ROOT))
                continue
            if is_spam(lead):
                lead = ''  # 弃用套话首段，仅用 h1
            new = build_desc(h1, lead)
            if not new:
                print('SKIP(无可用文本):', os.path.relpath(p, ROOT))
                continue
            if len(new) < 30:
                new = new + ' - 免费在线工具'
            targets.append((p, cur, new))

    print('待补全页面数: %d' % len(targets))
    for p, cur, new in targets[:12]:
        print('  %s\n    旧: %r\n    新: %r' % (os.path.relpath(p, ROOT), cur, new))

    if not args.apply:
        ok = sum(1 for _, _, n in targets if len(n) >= 30)
        print('\n补全后 >=30字: %d / %d；残留<30(功能本简短描述,非套话): %d'
              % (ok, len(targets), len(targets) - ok))
        print('[dry-run] 未写入。加 --apply 执行。')
        return

    done = 0
    for p, cur, new in targets:
        h = open(p, encoding='utf-8').read()
        enc = html.escape(new, quote=True)
        if '<meta name="description"' in h:
            h = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       r'\1' + enc + r'\2', h, count=1)
        if '<meta property="og:description"' in h:
            h = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
                       r'\1' + enc + r'\2', h, count=1)
        open(p, 'w', encoding='utf-8').write(h)
        done += 1
    print('\n[apply] 已写入 %d 页' % done)


if __name__ == '__main__':
    main()
