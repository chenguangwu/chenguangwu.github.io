#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 对未覆盖行业分层抽样：每个目标行业取最多 N 个含数学公式的工具，
# 打印 鲁棒公式文本 + calc 前 520 字符，供人工核对 公式文本↔calc 一致性。
import os, re, glob, json, html as htmlmod

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

# 目标行业（B-OPT17 未覆盖的高量级）
targets = ["ai","energy","hydraulic","fishery","realestate","machinery","legal",
           "healthcare","insurance","eco","aerospace","photo","securities","materials",
           "investment","metrology","nuclear","acoustics","robotics","electromagnetism",
           "tax","thermodynamics","encode","fluid","kinematics","structural","geometry",
           "metalwork","signal","dynamics","banking","optics","quantum","dentistry",
           "meteorology","optical","civil","geology","life","general","marketing"]

PER = 1
out = []
for ind in targets:
    d = os.path.join(TOOLS, ind)
    if not os.path.isdir(d): continue
    cnt = 0
    for hp in sorted(glob.glob(os.path.join(d,"*.html"))):
        h = open(hp,encoding="utf-8").read()
        if "formula-box" not in h: continue
        eq = get_eq(h)
        if not eq or not MATHSIG.search(eq): continue
        calc = extract_calc(h)
        if not calc: continue
        out.append((os.path.relpath(hp,ROOT), eq[:130], calc[:520]))
        cnt += 1
        if cnt >= PER: break

for rel,eq,calc in out:
    print("="*80)
    print("FILE:", rel)
    print("EQ  :", eq)
    print("CALC:")
    print(calc)
print(f"\n共采样 {len(out)} 个工具（每行业最多 {PER} 个，仅含数学公式框）")
