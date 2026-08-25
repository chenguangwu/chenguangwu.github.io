#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# B-OPT23 审计报告：对每个候选，打印正文抽到的等式 + calc 函数体关键计算行，
# 供人工判定"等式↔calc 一致"，一致才注入 formula-box。
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
data = json.load(open(os.path.join(ROOT, "tools.json"), encoding="utf-8"))
grade = {d["path"]: d.get("quality") for d in data}

EQ = re.compile(r'=')
OP = re.compile(r'[+\-*/^×÷·√]|[α-ωΑ-Ω]|[A-Za-z][²³ⁿ]|'
                r'(?:Math\.)?(?:sin|cos|tan|sqrt|log|ln|exp|pow|abs)|'
                r'\([^)]*[-+*/]')

def extract_eqs(h):
    body = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    body = re.sub(r'<style.*?</style>', ' ', body)
    txt = re.sub(r'<[^>]+>', '\n', body)
    out = []
    for line in txt.split('\n'):
        line = line.strip()
        if 4 <= len(line) <= 220 and EQ.search(line) and OP.search(line):
            out.append(line)
    return out

def extract_calc(h):
    m = re.search(r'function\s+calc\s*\([^)]*\)\s*\{', h)
    if not m:
        m = re.search(r'calc\s*=\s*function\s*\([^)]*\)\s*\{', h)
        if not m:
            return ""
    start = m.end() - 1
    depth = 0
    i = start
    while i < len(h):
        c = h[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return h[start+1:i]
        i += 1
    return ""

def calc_key_lines(body):
    out = []
    for line in body.split('\n'):
        s = line.strip()
        if not s or s.startswith('//') or s.startswith('*'):
            continue
        if re.search(r'[=*/]|Math\.|return|pow|sqrt|log|sin|cos', s) and len(s) <= 160:
            out.append(s)
    return out[:14]

# 用 scan 名单
cands = []
for hp in glob.glob(os.path.join(TOOLS, "*", "*.html")):
    try: h = open(hp, encoding="utf-8").read()
    except: continue
    if "formula-box" in h: continue
    if not re.search(r'function\s+calc\s*\(|calc\s*=\s*function', h): continue
    rel = os.path.relpath(hp, ROOT); p = rel.replace("tools/", "")
    if grade.get(p) != "B": continue
    eqs = extract_eqs(h)
    if not eqs: continue
    cands.append((rel, eqs, extract_calc(h)))

report = []
report.append(f"候选 {len(cands)} 个\n")
for rel, eqs, calc in sorted(cands):
    report.append("="*70)
    report.append(f"### {rel}")
    report.append("-- 正文抽到等式 --")
    for e in eqs[:3]:
        report.append(f"   {e[:170]}")
    report.append("-- calc 关键计算行 --")
    kl = calc_key_lines(calc)
    if not kl:
        report.append("   (calc 无显式计算行/或空)")
    for k in kl:
        report.append(f"   {k[:150]}")

open(os.path.join(ROOT, "scripts", "_b23_audit.txt"), "w", encoding="utf-8").write("\n".join(report))
print(f"已写出审计报告 scripts/_b23_audit.txt，候选 {len(cands)} 个")
