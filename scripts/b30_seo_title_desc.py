#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B-OPT30: 加长过短的 <title> 与 <meta name="description">，并统一 6 个 SEO 标签。
- 副标题源优先级: 页面「工具简介」intro 首句 > description 实质句
- 新 title/og:title/twitter:title = "NAME - 副标题 - ToolBox"（无副标题则保持 "NAME - ToolBox"）
- 新 description/og:description/twitter:description = "NAME - intro全文(≤120)" 或兜底通用后缀
- 幂等: 内容无变化则跳过; 跳过 TOOLBOX-REDIRECT 桩与分类索引页(index.html)
用法: python3 scripts/b30_seo_title_desc.py [--apply]
"""
import re, glob, sys, random, html as _html

TOOLBOX = ' - ToolBox'
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
INTRO_RE = re.compile(r'工具简介</h4>\s*<p>(.*?)</p>', re.S)
TMPL_SUFFIXES = [
    '免费在线工具，纯前端处理，数据不上传。',
    '免费在线工具，纯前端本地处理，数据不上传。',
    '免费在线工具，纯前端处理。',
    '免费在线工具。',
]

# 泛化占位 intro（与具体工具无关，会污染 description/副标题）
PLACEHOLDER_PAT = re.compile(r'帮助计算种植参数与产量|农业种植工具')

def is_placeholder(txt):
    return bool(PLACEHOLDER_PAT.search(txt))

def clean_text(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def first_sentence(s):
    parts = re.split(r'[。！？!?\n]', s)
    return parts[0].strip() if parts and parts[0].strip() else s.strip()

def strip_tmpl(s):
    for suf in TMPL_SUFFIXES:
        if s.endswith(suf):
            s = s[:-len(suf)]
    return s.strip()

def extract_name(title):
    full = title[:-len(TOOLBOX)] if title.endswith(TOOLBOX) else title
    if ' - ' in full:
        return full.split(' - ', 1)[0].strip()
    return full.strip()

def refine_sub(s, name):
    """去掉 NAME 前缀与冗余起始词，在逗号/顿号处自然截断，返回合格副标题或 None。"""
    s = s.strip('，。、 ')
    if s.startswith(name):
        s = s[len(name):].strip('，。、 ')
    s = re.sub(r'^(是一款?|是|用于|可|可以|提供)', '', s).strip('，。、 ')
    if len(s) < 4:
        return None
    if len(s) > 28:
        cut = s[:28]
        idx = max((cut.rfind(c) for c in '，、；,; '), default=-1)
        s = cut[:idx] if idx > 4 else cut
    if 4 <= len(s) <= 28:
        return s
    return None

def get_sub(html, name):
    # 优先 intro 首句（去 NAME 前缀，排除占位）
    m = INTRO_RE.search(html)
    if m:
        txt = clean_text(m.group(1))
        if not is_placeholder(txt):
            sub = refine_sub(first_sentence(txt), name)
            if sub:
                return sub
    # 兜底 desc 实质句（模板废话不作为副标题）
    m = DESC_RE.search(html)
    if m:
        d = m.group(1)
        if d.startswith(name + ' - '):
            d = d[len(name) + 3:]
        elif d.startswith(name):
            d = d[len(name):]
        d = strip_tmpl(d).strip('，。、 ')
        if '免费在线工具' not in d and '纯前端' not in d:
            sub = refine_sub(first_sentence(d), name)
            if sub:
                return sub
    return None

def get_desc(html, name):
    m = INTRO_RE.search(html)
    if m:
        txt = clean_text(m.group(1))[:120]
        if txt and not is_placeholder(txt):
            if txt.startswith(name):
                txt = txt[len(name):].strip('，。、 ')
            return f'{name} - {txt}'
    m = DESC_RE.search(html)
    d = m.group(1) if m else ''
    if len(d) >= 50:
        return d
    return f'{name} - 免费在线工具，纯前端处理，数据不上传。'

def esc(s):
    return s.replace('"', '&quot;')

def process(html):
    m_t = re.search(r'<title>([^<]*?)</title>', html)
    if not m_t:
        return html, None
    name = extract_name(m_t.group(1))
    sub = get_sub(html, name)
    new_title = f'{name} - {sub}{TOOLBOX}' if sub else f'{name}{TOOLBOX}'
    new_desc = get_desc(html, name)
    new = html
    new = re.sub(r'(<title>)[^<]*?(</title>)', lambda m: m.group(1)+esc(new_title)+m.group(2), new, count=1)
    new = re.sub(r'(<meta property="og:title" content=")[^"]*?(">)', lambda m: m.group(1)+esc(new_title)+m.group(2), new, count=1)
    new = re.sub(r'(<meta name="twitter:title" content=")[^"]*?(">)', lambda m: m.group(1)+esc(new_title)+m.group(2), new, count=1)
    new = re.sub(r'(<meta name="description" content=")[^"]*?(">)', lambda m: m.group(1)+esc(new_desc)+m.group(2), new, count=1)
    new = re.sub(r'(<meta property="og:description" content=")[^"]*?(">)', lambda m: m.group(1)+esc(new_desc)+m.group(2), new, count=1)
    new = re.sub(r'(<meta name="twitter:description" content=")[^"]*?(">)', lambda m: m.group(1)+esc(new_desc)+m.group(2), new, count=1)
    return new, (name, sub, new_title, new_desc)

def main():
    apply = '--apply' in sys.argv
    changed = 0; skipped = 0; samples = []
    t_before = []; t_after = []; d_before = []; d_after = []
    for f in glob.glob('tools/**/*.html', recursive=True):
        try:
            raw = open(f, 'rb').read()
            html = raw.decode('utf-8')
        except Exception:
            continue
        if 'TOOLBOX-REDIRECT' in html:
            continue
        if f.endswith('/index.html'):
            continue
        m_t = re.search(r'<title>([^<]*?)</title>', html)
        m_d = DESC_RE.search(html)
        if not m_t or not m_d:
            continue
        t_before.append(len(m_t.group(1)))
        d_before.append(len(m_d.group(1)))
        new, info = process(html)
        if new == html:
            skipped += 1
            t_after.append(len(m_t.group(1)))
            d_after.append(len(m_d.group(1)))
            continue
        changed += 1
        t_after.append(len(info[2]))
        d_after.append(len(info[3]))
        if len(samples) < 14:
            samples.append((f, m_t.group(1), info[2], m_d.group(1), info[3]))
        if apply:
            open(f, 'wb').write(new.encode('utf-8'))
    if not apply:
        print('[DRY] 将修改文件数:', changed, '| 跳过(已一致):', skipped)
        if t_before:
            print('[DRY] title 长度: 前均值=%.1f 后均值=%.1f | desc 长度: 前均值=%.1f 后均值=%.1f' % (
                sum(t_before)/len(t_before), sum(t_after)/len(t_after),
                sum(d_before)/len(d_before), sum(d_after)/len(d_after)))
        print('\n[DRY] 抽样 before -> after:')
        for f, ot, nt, od, nd in samples:
            print(f'  文件: {f}')
            print(f'    title: {ot}\n        -> {nt}')
            print(f'    desc : {od}\n        -> {nd}\n')
    else:
        print('[APPLY] 已修改文件数:', changed, '| 跳过:', skipped)

if __name__ == '__main__':
    main()
