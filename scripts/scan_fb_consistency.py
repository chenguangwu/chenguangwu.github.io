#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 自动探测 formula-box 与 calc 逻辑可能不一致的高风险工具。
# 三类信号：
#  1) no_math    : formula-eq 完全不含数学符号/函数/数字 → 疑似描述型假公式
#  2) var_mismatch: formula-eq 引用的变量在 calc 中不存在（且非常数/函数名）→ 可能公式与代码脱节
#  3) trivial    : formula-eq 仅单 token 或纯 "结果=X" 式 → 疑似空壳
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

EQ = re.compile(r'<div class="formula-eq">(.*?)</div>', re.S)
FBLOCK = re.compile(r'<div class="formula-box".*?</div>\s*</div>', re.S)
IND = re.compile(r'/tools/([^/]+)/')

FUNCS = {"sin","cos","tan","log","ln","exp","sqrt","pow","abs","min","max","sum",
         "asin","acos","atan","floor","ceil","round","sign","mean","std","var",
         "pi","e"}

# 数学信号：运算符 / 数字 / 常见数学函数 / 希腊字母 / 上下标 / 函数调用 / 幂
MATHSIG = re.compile(
    r'[+\-*/^=×÷·]|'
    r'\d|'
    r'(?:Math\.)?(?:sin|cos|tan|asin|acos|atan|log|ln|exp|sqrt|pow|abs|floor|ceil|round)|'
    r'[α-ωΑ-Ω]|'
    r'[A-Za-z][²³ⁿ]|'
    r'[A-Za-z]+\(|'
    r'\^|'
    r'√|'
    r'\%'
)

# 抽取 calc 函数源码（括号配对）
def extract_calc(h):
    i = h.find("function calc(")
    if i < 0:
        i = h.find("calc=function")
    if i < 0:
        i = h.find("calc = function")
    if i < 0:
        return None
    depth = 0; started = False; j = h.find("{", i)
    if j < 0:
        return None
    for k in range(j, len(h)):
        c = h[k]
        if c == "{":
            depth += 1; started = True
        elif c == "}":
            depth -= 1
            if started and depth == 0:
                return h[i:k+1]
    return None

# 变量 token（拉丁字母开头，排除纯函数名/中文/常数）
VAR = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')

def strip(s):
    return re.sub(r'\s+', ' ', s or '').strip()

rows = []
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try:
        h = open(hp, encoding="utf-8").read()
    except Exception:
        continue
    if "formula-box" not in h:
        continue
    eqs = EQ.findall(h)
    eq = strip(eqs[0]) if eqs else ""
    calc = extract_calc(h)
    m = IND.search(hp)
    ind = m.group(1) if m else "?"
    rel = os.path.relpath(hp, ROOT)

    flags = []
    # 1) no math
    if not MATHSIG.search(eq):
        flags.append("no_math")
    # 3) trivial
    et = re.sub(r'[^\w]', '', eq)
    if len(et) <= 2:
        flags.append("trivial")
    # 2) var mismatch
    if calc:
        calc_vars = set(VAR.findall(calc))
        # 公式里的拉丁标识符
        fvars = [v for v in VAR.findall(eq) if v not in FUNCS and not v.startswith("Math")]
        missing = [v for v in set(fvars) if v not in calc_vars and v.lower() not in ("x","y","n","i","e","pi")]
        if missing:
            flags.append("var_mismatch:" + ",".join(missing[:4]))
    if flags:
        rows.append({"file": rel, "ind": ind, "eq": eq[:120], "flags": flags})

print(f"命中可疑工具: {len(rows)}\n")
for r in rows:
    print(f"[{','.join(r['flags'])}] {r['file']}")
    print(f"    eq: {r['eq']}")

with open(os.path.join(ROOT, "scripts", "_fb_suspect.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print(f"\n已写出 scripts/_fb_suspect.json ({len(rows)} 条)")
