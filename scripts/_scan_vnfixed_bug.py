#!/usr/bin/env python3
# 扫描 __vN.toFixed 误用：__vN 的 IIFE 返回字符串却调用 .toFixed() -> NaN
# 健壮版：按括号深度提取赋值右值，避免被 IIFE 内部 ; 截断。
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')

tofixed_re = re.compile(r'__v(\d+)\.toFixed')

def extract_rhs(src, eq_pos):
    # 从 '=' 之后开始，按括号深度找到语句结束的 ';'
    i = eq_pos
    depth = 0
    n = len(src)
    started = False
    while i < n:
        c = src[i]
        if c in '([{':
            depth += 1
            started = True
        elif c in ')]}':
            depth -= 1
            if started and depth == 0:
                # 到达闭合括号，继续找结尾 ';'
                j = i + 1
                while j < n and src[j] != ';':
                    j += 1
                return src[eq_pos:j]
        elif c == ';' and depth == 0:
            return src[eq_pos:i]
        i += 1
    return src[eq_pos:]

def returns_string(rhs):
    # 提取箭头函数体
    m = re.search(r'=>\s*\{([\s\S]*)\}\(\)\)', rhs)
    body = m.group(1) if m else rhs
    rm = re.search(r'return\s+([\s\S]*?);', body)
    if not rm:
        return bool(re.search(r'["\']', rhs))
    expr = rm.group(1).strip()
    # 三元/字面量含引号 -> 字符串
    if re.search(r'["\']', expr):
        return True
    return False

results = []
for dirpath, _, files in os.walk(TOOLS):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dirpath, fn)
        try:
            src = open(p, encoding='utf-8').read()
        except Exception:
            continue
        used = set(tofixed_re.findall(src))
        if not used:
            continue
        # 定位所有 __vN = 赋值（含 const/let/var）
        for m in re.finditer(r'(?:const|let|var)\s+(__v\d+)\s*=', src):
            name = m.group(1)
            if name[3:] not in used:
                continue
            rhs = extract_rhs(src, m.end() - 1)  # 从 '=' 位置开始
            is_str = returns_string(rhs)
            # 行号
            ln = src[:m.start()].count('\n') + 1
            verdict = 'BUG(string.toFixed)' if is_str else 'OK(number)'
            results.append({'file': os.path.relpath(p, ROOT), 'var': name,
                            'verdict': verdict, 'line': ln})

bugs = [r for r in results if r['verdict'] == 'BUG(string.toFixed)']
print("=== BUG(string.toFixed) 共 %d 处 ===" % len(bugs))
for r in bugs:
    print("%s  %s  line %s" % (r['file'], r['var'], r['line']))
print("\n统计: BUG=%d  OK=%d" % (len(bugs), sum(1 for r in results if r['verdict']=='OK(number)')))
