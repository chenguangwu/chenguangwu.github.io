#!/usr/bin/env python3
"""
B5-03 修复：生成器把每个结果表达式都写成 `const __v = (...)`，
导致含 2+ 条结果表达式的工具出现重复 const 声明 -> SyntaxError -> 整段脚本失效（calc 未定义）。

本脚本将每个 `const __v =` 与紧随其后的 `__v` 引用按顺序重命名为 __v0/__v1/...，
保持声明-使用一一对应（生成器结构为「声明后立即在下一行模板中引用」），语义不变。
仅处理 const __v 出现 >=2 次的文件。
"""
import os, re

ROOT = os.path.abspath('.')
targets = []
for root, _, files in os.walk(os.path.join(ROOT, 'tools')):
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        try:
            c = open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        if c.count('const __v =') >= 2:
            targets.append(fp)

fixed = 0
for fp in targets:
    c = open(fp, encoding='utf-8').read()
    idx = [0]
    cur = [0]
    def repl(m):
        tok = m.group(0)
        if tok.startswith('const __v'):
            i = idx[0]
            idx[0] += 1
            cur[0] = i
            return 'const __v%d =' % i
        return '__v%d' % cur[0]
    c2 = re.sub(r'const __v\s*=|__v', repl, c)
    if c2 != c:
        open(fp, 'w', encoding='utf-8').write(c2)
        fixed += 1

print('scanned broken files:', len(targets), ' fixed:', fixed)
