"""P4 补丁：剥离已烘焙到各工具页的面包屑(nav + BreadcrumbList JSON)，
让 _build.py 的 fix_tool_pages_seo 用新的 INDUSTRY_DEFS 中文名重新生成。
仅剥离 nav 与 BreadcrumbList；保留 h1 / related / WebApplication 等其它 SEO 块。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")

nav_re = re.compile(r'\n<nav class="breadcrumb".*?</nav>\n', re.S)
bc_re = re.compile(
    r'\n<script type="application/ld\+json">\n'
    r'\{"@context":"https://schema\.org","@type":"BreadcrumbList".*?</script>\n',
    re.S,
)

count = 0
for ind in os.listdir(TOOLS_DIR):
    dp = os.path.join(TOOLS_DIR, ind)
    if not os.path.isdir(dp):
        continue
    for fn in os.listdir(dp):
        if not fn.endswith('.html') or fn == 'index.html':
            continue
        fp = os.path.join(dp, fn)
        try:
            c = open(fp, encoding='utf-8').read()
        except Exception:
            continue
        if 'data-breadcrumb' not in c and 'BreadcrumbList' not in c:
            continue
        c2 = nav_re.sub('\n', c)
        c2 = bc_re.sub('\n', c2)
        if c2 != c:
            open(fp, 'w', encoding='utf-8').write(c2)
            count += 1

print("Stripped breadcrumbs from %d tool pages" % count)
