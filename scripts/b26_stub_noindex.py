#!/usr/bin/env python3
# B-OPT26: 给所有 TOOLBOX-REDIRECT 重定向桩补 <meta name="robots" content="noindex,follow">
# 目的：桩是保留旧 URL 的纯跳转页，加 noindex 防止低质跳转页被搜索引擎单独收录，
#       将权重集中到 canonical 指向的分类页。零外观/计算回归、幂等（已含 robots 则跳过）。
# 不影响用户访问（meta refresh / location 跳转仍生效，noindex 仅约束爬虫）。
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
redir_file = '/tmp/redir.txt'
if not os.path.exists(redir_file):
    os.system('grep -rl TOOLBOX-REDIRECT %s/tools --include="*.html" > %s' % (ROOT, redir_file))
stubs = [l.strip() for l in open(redir_file, encoding='utf-8') if l.strip()]

apply = '--apply' in sys.argv
n_add = 0
n_skip = 0
for fp in stubs:
    if not os.path.exists(fp):
        continue
    c = open(fp, encoding='utf-8').read()
    if 'TOOLBOX-REDIRECT' not in c:
        continue
    if 'name="robots"' in c:
        n_skip += 1
        continue
    m = re.search(r'(<link rel="canonical"[^>]*>)', c)
    if m:
        ins = m.group(1) + '\n<meta name="robots" content="noindex,follow">'
        c2 = c.replace(m.group(1), ins, 1)
    else:
        c2 = c.replace('<head>', '<head>\n<meta name="robots" content="noindex,follow">', 1)
    if apply:
        open(fp, 'w', encoding='utf-8').write(c2)
    n_add += 1

print(('[APPLY] ' if apply else '[DRY] '), '桩补 noindex 数=%d, 跳过(已含)=%d, 桩总数=%d' % (n_add, n_skip, len(stubs)))
