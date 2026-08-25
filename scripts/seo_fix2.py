#!/usr/bin/env python3
"""全站 SEO 补齐（2026-08-07 第二轮）：desc 缺失/过短、og 全量、twitter 全量、canonical、lang。
只做插入/替换，不重写文件其他内容。幂等：已有标签跳过。
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://chenguangwu.github.io'
OG_IMG = SITE + '/og-image.png'

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def get_title(html):
    m = re.search(r'<title>([^<]*)</title>', html)
    return m.group(1).strip() if m else ''

def build_block(url, name, desc):
    """构造缺失标签块（在 </head> 前插入）"""
    abs_url = SITE + '/' + url if not url.startswith('http') else url
    lines = []
    if not re.search(r'<meta name="description"', html_ctx := ''):
        pass  # 占位，实际由调用方控制
    return lines

def fix_page(p, url, name_hint=''):
    """p: 绝对路径; url: 相对 URL 如 tools/it/xxx.html"""
    try:
        html = open(p, encoding='utf-8').read()
    except Exception:
        return ['READ_FAIL:' + url]
    changed = []
    title = get_title(html)
    name = title.replace(' - ToolBox', '').strip() or name_hint or os.path.basename(url).replace('.html', '')
    abs_url = SITE + '/' + url

    # 1. lang
    if not re.search(r'<html[^>]*lang=', html):
        html = re.sub(r'<html(?=[\s>])', '<html lang="zh-CN"', html, count=1)
        changed.append('lang')

    # 2. description
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not m:
        new_desc = f'{name} - 免费在线工具，纯前端运行，数据不出浏览器，无需注册登录。支持在线计算、转换与生成，安全可靠。'
        ins = f'<meta name="description" content="{esc(new_desc)}">'
        html = html.replace('</head>', '    ' + ins + '\n</head>', 1)
        desc = new_desc
        changed.append('desc_missing')
    else:
        desc = m.group(1).strip()
        if len(desc) < 30:
            new_desc = desc.rstrip('。.') + '。支持在线免费使用，纯前端运行，数据不出浏览器，安全可靠。'
            html = html.replace(m.group(0), f'<meta name="description" content="{esc(new_desc)}">', 1)
            desc = new_desc
            changed.append('desc_short')

    # 3. canonical
    if not re.search(r'<link rel="canonical"', html):
        ins = f'<link rel="canonical" href="{abs_url}">'
        html = html.replace('</head>', '    ' + ins + '\n</head>', 1)
        changed.append('canonical')

    # 4. og
    og_defs = [
        ('og:title', 'property', name),
        ('og:description', 'property', desc),
        ('og:type', 'property', 'website'),
        ('og:url', 'property', abs_url),
        ('og:image', 'property', OG_IMG),
    ]
    for key, attr, val in og_defs:
        if not re.search(r'<meta %s="%s"' % (attr, re.escape(key)), html):
            ins = f'<meta {attr}="{key}" content="{esc(val)}">'
            html = html.replace('</head>', '    ' + ins + '\n</head>', 1)
            changed.append(key)

    # 5. twitter
    tw_defs = [
        ('twitter:card', 'summary'),
        ('twitter:title', name),
        ('twitter:description', desc),
        ('twitter:image', OG_IMG),
    ]
    for key, val in tw_defs:
        if not re.search(r'<meta name="%s"' % re.escape(key), html):
            ins = f'<meta name="{key}" content="{esc(val)}">'
            html = html.replace('</head>', '    ' + ins + '\n</head>', 1)
            changed.append(key)

    if changed:
        open(p, 'w', encoding='utf-8').write(html)
    return changed

def main():
    tools = json.load(open(os.path.join(ROOT, 'json/tools.json'), encoding='utf-8'))
    total_changed = {}
    files_modified = 0
    for t in tools:
        p = os.path.join(ROOT, t['url'])
        if not os.path.exists(p):
            print('SKIP missing file:', t['url'])
            continue
        ch = fix_page(p, t['url'], t['name'])
        if ch:
            files_modified += 1
            for c in ch:
                total_changed[c] = total_changed.get(c, 0) + 1
    print(f'工具页已修改: {files_modified}/{len(tools)}')
    print('修复项统计:', dict(total_changed))

    # 分类落地页 + 核心页（补 og/twitter 若缺）
    extra = []
    for ind in os.listdir(os.path.join(ROOT, 'tools')):
        ip = os.path.join(ROOT, 'tools', ind, 'index.html')
        if os.path.exists(ip):
            extra.append((ip, f'tools/{ind}/index.html', ind))
    for fn in ['index.html', 'sitemap.html', 'search.html', 'chains.html']:
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            extra.append((p, fn, fn))
    for p, url, hint in extra:
        ch = fix_page(p, url, hint)
        if ch:
            files_modified += 1
            print(f'  extra {url}: {ch}')

    print(f'\n共修改 {files_modified} 个文件')

if __name__ == '__main__':
    main()
