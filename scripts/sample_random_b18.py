#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 全站随机抽检 20 个 formula-box 工具（seed 固定可复现），打印 公式文本 + calc 片段，人工核对一致。
import os, re, glob, html as htmlmod, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
MATHSIG = re.compile(r'[+\-*/^=×÷·]|\d|(?:Math\.)?(?:sin|cos|tan|asin|acos|atan|log|ln|exp|sqrt|pow|abs|floor|ceil|round)|[α-ωΑ-Ω]|[A-Za-z][²³ⁿ]|[A-Za-z]+\(|[\^√％%]|mod|MOD')

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

files=[]
for hp in glob.glob(os.path.join(TOOLS,"*","*.html")):
    h=open(hp,encoding="utf-8").read()
    if "formula-box" not in h: continue
    eq=get_eq(h)
    if not eq or not MATHSIG.search(eq): continue
    if not extract_calc(h): continue
    files.append(hp)
random.seed(20260813)
pick=random.sample(files, min(20,len(files)))
for hp in pick:
    h=open(hp,encoding="utf-8").read()
    eq=get_eq(h); calc=extract_calc(h)
    print("="*80)
    print("FILE:", os.path.relpath(hp,ROOT))
    print("EQ  :", eq[:140])
    print("CALC:")
    print(calc[:560])
