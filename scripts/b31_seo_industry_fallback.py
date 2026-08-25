#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B-OPT31: 行业名兜底，消除 b30 后仍残留的短 title / 短 description。
- title: 当前为 "NAME - ToolBox"(无副标题) 且 <20 字符 -> "NAME - <行业>在线工具 - ToolBox"
- description: 当前为通用短模板(含'免费在线工具'且'数据不上传'且<50) -> "NAME - 专业的<行业>在线工具，支持实时计算，纯前端本地处理，数据不上传服务器，保护隐私安全。"
- 同步 title/og:title/twitter:title 与 description/og:description/twitter:description
- 幂等; 跳过 TOOLBOX-REDIRECT 桩与分类索引页(index.html)
用法: python3 scripts/b31_seo_industry_fallback.py [--apply]
"""
import re, glob, sys, json

mapper = json.load(open('scripts/industry_map.json', encoding='utf-8'))
TOOLBOX = ' - ToolBox'

def get_ind(f):
    parts = f.split('/')
    if len(parts) >= 3 and parts[0] == 'tools':
        return parts[1]
    return None

def esc(s):
    return s.replace('"', '&quot;')

def process(html, f):
    ind = get_ind(f)
    if not ind:
        return html, False
    ind_name = mapper.get(ind, '')
    if not ind_name:
        return html, False
    m_t = re.search(r'<title>([^<]*?)</title>', html)
    m_d = re.search(r'<meta name="description" content="([^"]*)"', html, re.I)
    if not m_t or not m_d:
        return html, False
    title = m_t.group(1)
    name = title[:-len(TOOLBOX)] if title.endswith(TOOLBOX) else title
    new = html
    changed = False
    # title 兜底: 无副标题 且 <20
    if title.endswith(TOOLBOX) and title.count(' - ') == 1 and len(title) < 20:
        nt = f'{name} - {ind_name}在线工具{TOOLBOX}'
        new = re.sub(r'(<title>)[^<]*?(</title>)', lambda m: m.group(1)+esc(nt)+m.group(2), new, count=1)
        new = re.sub(r'(<meta property="og:title" content=")[^"]*?(">)', lambda m: m.group(1)+esc(nt)+m.group(2), new, count=1)
        new = re.sub(r'(<meta name="twitter:title" content=")[^"]*?(">)', lambda m: m.group(1)+esc(nt)+m.group(2), new, count=1)
        changed = True
    # description 兜底: 通用短模板 且 <50
    d = m_d.group(1)
    if len(d) < 50 and '免费在线工具' in d and '数据不上传' in d:
        nd = f'{name} - 专业的{ind_name}在线工具，支持实时计算，纯前端本地处理，数据不上传服务器，保护隐私安全。'
        new = re.sub(r'(<meta name="description" content=")[^"]*?(">)', lambda m: m.group(1)+esc(nd)+m.group(2), new, count=1)
        new = re.sub(r'(<meta property="og:description" content=")[^"]*?(">)', lambda m: m.group(1)+esc(nd)+m.group(2), new, count=1)
        new = re.sub(r'(<meta name="twitter:description" content=")[^"]*?(">)', lambda m: m.group(1)+esc(nd)+m.group(2), new, count=1)
        changed = True
    return new, changed

def main():
    apply = '--apply' in sys.argv
    n_title = 0; n_desc = 0; skipped = 0; samples = []
    for f in glob.glob('tools/**/*.html', recursive=True):
        try:
            html = open(f, 'rb').read().decode('utf-8')
        except Exception:
            continue
        if 'TOOLBOX-REDIRECT' in html or f.endswith('/index.html'):
            continue
        new, changed = process(html, f)
        if not changed:
            skipped += 1
            continue
        # 统计本次实际改了哪些标签
        m_t = re.search(r'<title>([^<]*?)</title>', new)
        m_d = re.search(r'<meta name="description" content="([^"]*)"', new, re.I)
        if apply:
            open(f, 'wb').write(new.encode('utf-8'))
        if m_t and ('在线工具' in m_t.group(1) and m_t.group(1).count(' - ') == 2):
            n_title += 1
        if m_d and '专业的' in m_d.group(1):
            n_desc += 1
        if len(samples) < 10:
            m_t0 = re.search(r'<title>([^<]*?)</title>', html)
            m_d0 = re.search(r'<meta name="description" content="([^"]*)"', html, re.I)
            samples.append((f, m_t0.group(1) if m_t0 else '', m_t.group(1) if m_t else '',
                              m_d0.group(1) if m_d0 else '', m_d.group(1) if m_d else ''))
    if not apply:
        print(f'[DRY] title兜底:{n_title} | desc兜底:{n_desc} | 跳过:{skipped}')
        for f, ot, nt, od, nd in samples:
            print(f'  文件:{f}')
            print(f'    title: {ot} -> {nt}')
            print(f'    desc : {od} -> {nd}')
    else:
        print(f'[APPLY] title兜底:{n_title} | desc兜底:{n_desc} | 跳过:{skipped}')

if __name__ == '__main__':
    main()
