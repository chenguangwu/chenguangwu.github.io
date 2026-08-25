#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 靶向扫描：公式框含 聚合语义(加权/Σ/平均/均值/求和) 的工具，
# 检查 calc 是否实际用了 max/Math.max（与"平均/加权"矛盾），命中交人工复核。
import os, re, glob, html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

AGG = re.compile(r'加权|Σ|∑|平均|均值|求和|∑|算术')
MAXSIG = re.compile(r'Math\.max|\.max\(|maxIAQI|maxAqi|max\b')

def find_block(h, cls):
    pat = re.compile(r'<div class="%s"[^>]*>' % re.escape(cls))
    m = pat.search(h)
    if not m: return None
    i = m.end(); depth=1; j=i
    while j < len(h):
        if h.startswith("<div", j):
            depth+=1; j=h.find(">",j)+1
        elif h.startswith("</div>", j):
            depth-=1; j+=6
            if depth==0: return h[m.end():j-6]
        else: j+=1
    return None

def strip_tags(s):
    s = re.sub(r'<[^>]+>',' ',s or '')
    return htmlmod.unescape(re.sub(r'\s+',' ',s)).strip()

def get_eq(h):
    fb = find_block(h,"formula-box")
    if fb is None: return None
    cleaned = fb
    for cls in ("formula-title","formula-desc"):
        cb = find_block(cleaned,cls)
        if cb is not None:
            seg_full = cleaned[cleaned.find(f'<div class="{cls}"'):]
            seg_full = seg_full[:seg_full.find("</div>")+6]
            cleaned = cleaned.replace(seg_full,"",1)
    for cls in ("formula-eq","formula"):
        sub = find_block(cleaned,cls)
        if sub is not None: return strip_tags(sub)
    return strip_tags(cleaned)

def extract_calc(h):
    for key in ("function calc(","calc=function","calc = function"):
        i = h.find(key)
        if i>=0:
            j=h.find("{",i)
            if j<0: return None
            depth=0
            for k in range(j,len(h)):
                if h[k]=="{": depth+=1
                elif h[k]=="}":
                    depth-=1
                    if depth==0: return h[i:k+1]
    return None

rows=[]
for hp in glob.glob(os.path.join(TOOLS,"*","*.html")):
    try: h=open(hp,encoding="utf-8").read()
    except: continue
    if "formula-box" not in h: continue
    eq=get_eq(h)
    if not eq: continue
    if not AGG.search(eq): continue
    calc=extract_calc(h) or ""
    # 矛盾信号：公式说聚合平均/加权，但 calc 用 max
    contradiction = MAXSIG.search(calc) and not re.search(r'平均|加权|Σ|∑|均值|求和', calc)
    rows.append((os.path.relpath(hp,ROOT), eq[:120], bool(contradiction)))

print(f"公式框含聚合语义的工具: {len(rows)}\n")
for rel,eq,flag in rows:
    mark = "  <== 可能矛盾(calc用max)" if flag else ""
    print(f"[{rel}]{mark}")
    print(f"    eq: {eq}")
