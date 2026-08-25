#!/usr/bin/env python3
# B-OPT27: 修复 og:title 中的 " - 工具，" 怪异拼接格式（如 "灌溉用水量估算 - 工具，根据面积…计算总用水量"）
# 这类是早期生成逻辑把 "name - 工具，desc" 拼进 og:title 的残留瑕疵；统一修正为 "name - ToolBox"（与 <title> 品牌格式一致）。
# 仅处理精确匹配 " - 工具，" 的 78 个，不动其它可读格式（name-desc / name / name-XX工具 等），幂等。
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apply = '--apply' in sys.argv
pat = re.compile(r'<meta property="og:title" content="([^"]*?) - 工具，[^"]*">')
n = 0
samples = []
for dp, dn, fn in os.walk(os.path.join(ROOT, 'tools')):
    for f in fn:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        c = open(fp, encoding='utf-8').read()
        if 'TOOLBOX-REDIRECT' in c:
            continue
        m = pat.search(c)
        if not m:
            continue
        name = m.group(1)
        new_og = '<meta property="og:title" content="%s - ToolBox">' % name
        if apply:
            open(fp, 'w', encoding='utf-8').write(c.replace(m.group(0), new_og, 1))
        n += 1
        if len(samples) < 6:
            samples.append((fp.replace(ROOT + '/', ''), m.group(0), new_og))
print(('[APPLY] ' if apply else '[DRY] '), '修复 og:title 怪格式数=%d' % n)
for s in samples:
    print('  文件:', s[0])
    print('    旧:', s[1])
    print('    新:', s[2])
