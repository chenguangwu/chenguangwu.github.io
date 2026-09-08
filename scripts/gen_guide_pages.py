# -*- coding: utf-8 -*-
"""通用使用指南页生成器（基于 deep-dive 真实内容派生，去英文 .en.html）。

用法：
  python3 scripts/gen_guide_pages.py --industry fishery
  python3 scripts/gen_guide_pages.py --industry fishery --slugs density-1,pond-capacity
  python3 scripts/gen_guide_pages.py --industry fire-rescue --slugs calc-1,hydrant-flow

行为：
  - 对每个 slug 读 i18n/tools/content_deepdive.json 的 <industry>/<slug> 条目
  - 由真实 deep-dive（场景/算例/FAQ）派生指南页字段，生成 guides/<slug>-guide.html
  - 合并 json/guides.json（按 tool basename 去重），并向 guides/index.html 追加条目
  - 模板去除独立英文 .en.html 链接与英文 hreflang（英文走 ?lang=en-US），并引 common.js
无 deep-dive 的 slug 会跳过并告警（指南需专业内容支撑，缺失则不应补）。
"""
import os, re, json, html, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'
DD_PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
GJ_PATH = os.path.join(ROOT, 'json', 'guides.json')

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}使用指南 - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}使用指南 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}使用指南 - ToolBox">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<link rel="canonical" href="{canonical}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{{"@type":"Organization","name":"ToolBox"}}}}
</script>
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}}
header{{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;margin-right:6px;}}
main{{max-width:780px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;margin:0 0 8px;}}
.lead{{font-size:16px;color:var(--muted);margin:0 0 22px;}}
h2{{font-size:20px;margin:28px 0 10px;color:var(--primary);}}
ul,ol{{padding-left:22px;}}
li{{margin:6px 0;}}
dl{{margin:0;}}
dt{{font-weight:700;margin-top:12px;}}
dd{{margin:4px 0 0;color:var(--muted);}}
.back{{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.back a{{color:var(--primary);font-weight:700;text-decoration:none;}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}}
</style>
<script src="/js/analytics.js" defer></script>
<script src="../js/common.js" defer></script>
<link rel="stylesheet" href="../css/common.css">
</head>
<body>
<header><nav class="breadcrumb"><a href="{home}">ToolBox</a> / <a href="{home}#guides">使用指南</a> / <span>{title}</span></nav></header>
<main>
<h1>{title} 使用指南</h1>
<p class="lead">{intro}</p>
<h2>核心功能</h2>
<ul>{features}</ul>
<h2>适用场景</h2>
<ul>{scenarios}</ul>
<h2>使用步骤</h2>
<ol>{steps}</ol>
<h2>实用技巧</h2>
<ul>{tips}</ul>
<h2>常见问题</h2>
<dl>{faqs}</dl>
<div class="back"><a href="{tool_url}">→ 去使用 {title}（免费 · 纯前端 · 数据不上传）</a></div>
</main>
<footer>© 2026 ToolBox · 纯前端在线工具 · 数据不上传，安全可靠</footer>
</body>
</html>
'''


def li(items):
    return ''.join('<li>%s</li>' % html.escape(str(x)) for x in items)


def extract_tips(faqs, scenarios):
    tips = []
    keys = ['注意', '须', '应', '避免', '建议', '务必', '不要', '不能', '不宜', '一般', '通常']
    for f in faqs:
        a = f.get('a', '')
        for sent in re.split(r'[。！？\n]', a):
            s = sent.strip()
            if any(k in s for k in keys) and 6 <= len(s) <= 64:
                tips.append(s)
        if len(tips) >= 4:
            break
    if len(tips) < 3:
        tips += scenarios[len(tips):]
    return tips[:5] if tips else ['结果以工具实时计算为准，输入参数请使用真实数据。']


def derive(v):
    title = v.get('title', '') or ''
    sc = v.get('scenarios', []) or []
    ex = v.get('examples', []) or []
    faqs = v.get('faqs', []) or []
    features = v.get('features') or (sc[:4] if sc else ['本工具提供专业计算与结果解读'])
    scenarios = sc or ['—']
    steps = v.get('steps') or [e.get('title', '') for e in ex if e.get('title')] or ['输入参数，点击计算查看结果。']
    tips = v.get('tips') or extract_tips(faqs, sc)
    faqs_pairs = [(f.get('q', ''), f.get('a', '')) for f in faqs] or [
        ('本工具适合谁用？', title + '适用于相关专业人员与爱好者，结果仅供参考。')]
    intro = v.get('intro') or ((ex[0].get('body', '')[:90] + '…') if ex else title)
    desc = v.get('desc') or (title + '使用指南：' + (sc[0][:40] if sc else '提供专业在线计算与结果解读。'))
    return title, desc, intro, features, scenarios, steps, tips, faqs_pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--industry', required=True)
    ap.add_argument('--slugs', default='', help='逗号分隔的 slug；留空则扫描该分类全部工具')
    ap.add_argument('--dry', action='store_true', help='只预览不落盘')
    args = ap.parse_args()

    dd = json.load(open(DD_PATH, encoding='utf-8')) if os.path.exists(DD_PATH) else {}
    ind = args.industry

    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(',') if s.strip()]
    else:
        tdir = os.path.join(ROOT, 'tools', ind)
        slugs = [f[:-5] for f in os.listdir(tdir) if f.endswith('.html') and f != 'index.html']

    os.makedirs(GUIDES_DIR, exist_ok=True)
    guide_map = []
    generated, skipped = [], []

    for slug in slugs:
        key = '%s/%s' % (ind, slug)
        v = dd.get(key)
        if not v:
            print('SKIP (无 deep-dive): %s' % key)
            skipped.append(key)
            continue
        title, desc, intro, features, scenarios, steps, tips, faqs_pairs = derive(v)
        fn = '%s-guide.html' % slug
        canonical = '%s/guides/%s' % (SITE, fn)
        page = (TPL
                .replace('{title}', html.escape(title))
                .replace('{desc}', html.escape(desc))
                .replace('{canonical}', canonical)
                .replace('{intro}', html.escape(intro))
                .replace('{features}', li(features))
                .replace('{scenarios}', li(scenarios))
                .replace('{steps}', li(steps))
                .replace('{tips}', li(tips))
                .replace('{faqs}', ''.join('<dt>%s</dt><dd>%s</dd>' % (html.escape(q), html.escape(a)) for q, a in faqs_pairs))
                .replace('{tool_url}', '%s/tools/%s/%s.html' % (SITE, ind, slug))
                .replace('{home}', SITE + '/'))
        if args.dry:
            print('DRY: guides/%s (%s)' % (fn, key))
            generated.append(key)
            continue
        open(os.path.join(GUIDES_DIR, fn), 'w', encoding='utf-8').write(page)
        guide_map.append({'tool': '%s.html' % slug, 'guide': '../../guides/%s' % fn, 'title': title + '使用指南'})
        print('OK: guides/%s' % fn)
        generated.append(key)

    if args.dry:
        print('预览 %d 篇，跳过 %d 篇' % (len(generated), len(skipped)))
        return 0

    # 合并 guides.json（按 tool 去重）
    old = json.load(open(GJ_PATH, encoding='utf-8')) if os.path.exists(GJ_PATH) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(GJ_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（新增 %d）' % (len(merged), len(guide_map)))

    # 指南中心 index.html 追加
    ip = os.path.join(GUIDES_DIR, 'index.html')
    if os.path.exists(ip) and guide_map:
        s = open(ip, encoding='utf-8').read()
        new_li = ''.join(
            '<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s使用指南</a>'
            '<span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
            % (m['guide'].split('/')[-1].replace('-guide.html', ''), html.escape(m['title'].replace('使用指南', '')),
               html.escape(desc[:50])) for m in guide_map)
        if '</ul>' in s:
            s = s.replace('</ul>', new_li + '</ul>', 1)
            open(ip, 'w', encoding='utf-8').write(s)
            print('guides/index.html 追加 %d 条' % len(guide_map))

    print('完成：生成 %d 篇，跳过 %d 篇' % (len(guide_map), len(skipped)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
