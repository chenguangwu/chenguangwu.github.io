#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# B-OPT21：验证 A 级剩余两桶的真实性
#  桶X(417): 脚本>=3000 且 输入>=3  → 查代码密度是否注水
#  桶Y(106): canvas/data-viz        → 查是否真有绘图/图表库调用(防"挂属性不画"假A)
import os, re, json
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = json.load(open(os.path.join(ROOT, "tools.json"), encoding="utf-8"))

def inline_scripts(h):
    return re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h, re.S)

def strip_c(s):
    return re.sub(r'/\*.*?\*/', ' ', s, flags=re.S).replace("//", "#")

DRAW = re.compile(r'getContext|beginPath|moveTo|lineTo|arc\(|fillRect|strokeRect|fillText|'
                 r'createLinearGradient|createRadialGradient|drawImage|quadraticCurveTo|'
                 r'bezierCurveTo|closePath|\.fill\(|\.stroke\(')
CHARTLIB = re.compile(r'\bChart\b|Plotly|echarts|Chartist|ApexCharts|\bd3\b|GoogleCharts|'
                      r'google\.visualization|canvasjs|CanvasJS|\.highcharts|Highcharts')
SVG = re.compile(r'createElementNS|setAttribute\(.svg|innerHTML\s*=.*<svg')

def bucket(d):
    p = os.path.join(ROOT, "tools", d.get("path", ""))
    if not os.path.exists(p):
        return None, None
    h = open(p, encoding="utf-8").read()
    if "formula-box" in h:
        return "FB", None
    scripts = inline_scripts(h)
    total = sum(len(s) for s in scripts)
    inputs = len(re.findall(r'<input', h))
    has_calc = ("function calc(" in h) or ("calc=function" in h) or ("calc = function" in h)
    canvas = "<canvas" in h or "data-viz" in h or "data-chart" in h
    if canvas:
        return "canvas", h
    if total >= 6000:
        return "big", None
    if total >= 3000 and inputs >= 3:
        return "X(3000&in3)", h
    return "other", h

# 统计桶X密度
dens_X = []
flag_X = []
for d in data:
    if d.get("quality") != "A":
        continue
    b, h = bucket(d)
    if b != "X(3000&in3)":
        continue
    p = os.path.join(ROOT, "tools", d.get("path", ""))
    hh = open(p, encoding="utf-8").read()
    total = sum(len(s) for s in inline_scripts(hh))
    code = sum(len(l.strip()) for l in strip_c("\n".join(inline_scripts(hh))).split("\n"))
    den = round(code / total, 3) if total else 0
    dens_X.append(den)
    if den < 0.45:
        flag_X.append((d.get("path"), den, total))

dens_X.sort()
import statistics as st
print(f"桶X(脚本>=3000&输入>=3) 工具数: {len(dens_X)}")
if dens_X:
    print(f"  密度 min/median/max: {dens_X[0]} / {st.median(dens_X)} / {dens_X[-1]}")
    print(f"  密度<0.45(注水)数量: {len(flag_X)}")
for f in flag_X:
    print("    注水嫌疑:", f)

# 统计桶Y canvas 真实性
Y = []
fakeY = []
for d in data:
    if d.get("quality") != "A":
        continue
    b, h = bucket(d)
    if b != "canvas":
        continue
    p = os.path.join(ROOT, "tools", d.get("path", ""))
    hh = open(p, encoding="utf-8").read()
    has_draw = bool(DRAW.search(hh))
    has_chart = bool(CHARTLIB.search(hh))
    has_svg = bool(SVG.search(hh))
    real = has_draw or has_chart or has_svg
    Y.append(d.get("path"))
    if not real:
        fakeY.append((d.get("path"), has_draw, has_chart, has_svg))

print(f"\n桶Y(canvas/data-viz) 工具数: {len(Y)}")
print(f"  无绘图API/图表库/SVG调用(疑似挂属性不画): {len(fakeY)}")
for f in fakeY:
    print("    假Viz嫌疑:", f)
