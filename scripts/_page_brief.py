#!/usr/bin/env python3
"""输出单个工具页的「补用例所需摘要」：输入控件、入口函数、输出写入点、计算公式行。
用法: python3 scripts/_page_brief.py <ind>/<slug> [--full]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

slug = sys.argv[1]
full = "--full" in sys.argv
p = os.path.join(TOOLS, slug + ".html")
html = open(p, encoding="utf8", errors="ignore").read()

print("=" * 72)
print("SLUG:", slug, f"| {len(html)} bytes")

print("\n--- 输入控件 ---")
for m in re.finditer(r"<input\b([^>]*)>", html, re.I):
    a = m.group(1)
    gid = re.search(r'id="([^"]+)"', a)
    gv = re.search(r'value="([^"]*)"', a)
    gt = re.search(r'type="([^"]*)"', a)
    if gid:
        print(f'  input  id={gid.group(1):22} type={gt.group(1) if gt else "?":8} value={gv.group(1) if gv else ""!r}')
for m in re.finditer(r"<select\b([^>]*id=\"([^\"]+)\"[^>]*)>([\s\S]*?)</select>", html, re.I):
    sid = m.group(2)
    opts = re.findall(r'<option[^>]*value="([^"]*)"', m.group(3))
    sel = re.search(r'<option[^>]*\sselected\b[^>]*value="([^"]*)"', m.group(3))
    print(f'  select id={sid:22} options={opts[:8]}{"..." if len(opts)>8 else ""} default={sel.group(1) if sel else opts[0] if opts else ""}')
for m in re.finditer(r"<textarea\b([^>]*id=\"([^\"]+)\"[^>]*)>([\s\S]{0,80}?)</textarea>", html, re.I):
    print(f'  textar id={m.group(2):22} default={m.group(3)[:40]!r}')

print("\n--- 内联脚本块 / 入口函数 ---")
chunks = re.findall(r"<script\b([^>]*)>([\s\S]*?)</script>", html, re.I)
n = 0
for attrs, body in chunks:
    if "src=" in (attrs or ""):
        continue
    funcs = re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(", body)
    if funcs:
        n += 1
        print(f"  block#{n} len={len(body)} funcs={funcs[:12]}")

print("\n--- 输出写入点 ---")
seen = set()
for m in re.finditer(r"(getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\.\s*(\w+)\s*=|ToolBox\.setResult\(\s*['\"]([^'\"]+)['\"])", html):
    key = m.group(0)[:60]
    if key in seen:
        continue
    seen.add(key)
    tgt = m.group(2) or m.group(4)
    prop = m.group(3)
    line = html[:m.start()].count("\n") + 1
    print(f"  line{line:5} -> #{tgt}.{prop or 'innerHTML'}")

print("\n--- 计算公式行（含数值运算）---")
lines = html.split("\n")
hit = 0
for i, ln in enumerate(lines):
    s = ln.strip()
    if len(s) < 8 or len(s) > 300:
        continue
    if s.startswith("//") or s.startswith("*") or s.startswith("/*"):
        continue
    # 含赋值 + 算术运算符，且出现数字常量
    if re.search(r"=\s*[^=].*[*/+\-^]\s*[\d.]+", s) and re.search(r"\d", s):
        print(f"  {i+1:5}: {s[:150]}")
        hit += 1
        if hit >= (200 if full else 22):
            break
print("=" * 72)
