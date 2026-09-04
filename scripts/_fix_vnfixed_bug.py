#!/usr/bin/env python3
# 修复 __vN.toFixed 误用：字符串变量误接 .toFixed -> NaN
# 将 ${__vN.toFixed(N)} 改为 ${__vN}（仅对检测为 string 返回的 __vN）
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
tofixed_re = re.compile(r'__v(\d+)\.toFixed')

def extract_rhs(src, eq_pos):
    i, depth, n, started = eq_pos, 0, len(src), False
    while i < n:
        c = src[i]
        if c in '([{':
            depth += 1; started = True
        elif c in ')]}':
            depth -= 1
            if started and depth == 0:
                j = i + 1
                while j < n and src[j] != ';': j += 1
                return src[eq_pos:j]
        elif c == ';' and depth == 0:
            return src[eq_pos:i]
        i += 1
    return src[eq_pos:]

def returns_string(rhs):
    m = re.search(r'=>\s*\{([\s\S]*)\}\(\)\)', rhs)
    body = m.group(1) if m else rhs
    rm = re.search(r'return\s+([\s\S]*?);', body)
    if not rm:
        return bool(re.search(r'["\']', rhs))
    return bool(re.search(r'["\']', rm.group(1)))

fixed_files = {}
for dirpath, _, files in os.walk(TOOLS):
    for fn in files:
        if not fn.endswith('.html'): continue
        p = os.path.join(dirpath, fn)
        try: src = open(p, encoding='utf-8').read()
        except Exception: continue
        used = set(tofixed_re.findall(src))
        if not used: continue
        for m in re.finditer(r'(?:const|let|var)\s+(__v\d+)\s*=', src):
            name = m.group(1)
            if name[3:] not in used: continue
            is_str = returns_string(extract_rhs(src, m.end()-1))
            if not is_str: continue
            # 替换该文件内所有 ${__vN.toFixed(N)} -> ${__vN}
            new_src, cnt = re.subn(r'\$\{%s\.toFixed\(\d+\)\}' % re.escape(name), '${%s}' % name, src)
            if cnt:
                open(p, 'w', encoding='utf-8').write(new_src)
                src = new_src
                fixed_files[os.path.relpath(p, ROOT)] = fixed_files.get(os.path.relpath(p, ROOT), 0) + cnt

print("=== 已修复文件 ===")
for f, c in sorted(fixed_files.items()):
    print("  %s  (%d 处)" % (f, c))
print("共修复 %d 个文件, %d 处" % (len(fixed_files), sum(fixed_files.values())))
