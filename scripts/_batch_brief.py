#!/usr/bin/env python3
"""§7.4 批量页面摘要：一次输出多个页面的「输入控件 / 入口函数 / 输出容器」结构。

用法： python3 scripts/_batch_brief.py <行业前缀 或 -> [行数上限]
输入来自 /tmp/zero_A.txt，按前缀过滤。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def brief(slug, maxinput=8, maxlog=5):
    p = os.path.join(ROOT, 'tools', slug + '.html')
    try:
        html = open(p, encoding='utf8', errors='ignore').read()
    except Exception as e:
        return f"!! {slug}: {e}"

    # --- 输入控件 ---
    ins = []
    for m in re.finditer(r'<input\b([^>]*)>', html, re.I):
        a = m.group(1)
        if re.search(r'type="(hidden|radio|checkbox)"', a, re.I):
            continue
        iid = re.search(r'id="([^"]+)"', a)
        val = re.search(r'value="([^"]*)"', a)
        if iid:
            ins.append(f"{iid.group(1)}={val.group(1) if val else ''}")
    tas = []
    for m in re.finditer(r'<textarea\b([^>]*)>', html, re.I):
        a = m.group(1)
        iid = re.search(r'id="([^"]+)"', a)
        if iid:
            tas.append(iid.group(1))
    sels = []
    for m in re.finditer(r'<select\b([^>]*id="([^"]+)"[^>]*)>([\s\S]*?)</select>', html, re.I):
        opts = re.findall(r'<option[^>]*value="([^"]*)"', m.group(3))
        sels.append(f"{m.group(2)}[{'/'.join(opts[:5])}]")

    # --- 入口函数（脚本顶层 or 常见名）---
    scripts = re.findall(r'<script\b([^>]*)>([\s\S]*?)</script>', html, re.I)
    funcs = []
    for attr, body in scripts:
        if 'src=' in attr.lower():
            continue
        for f in re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', body):
            funcs.append(f)
    # 常见入口名优先
    PREF = ['calcTool', 'calculate', 'calc', 'run', 'convert', 'generate', 'render',
            'update', 'compute', 'exec', 'format', 'escape', 'compile', 'build']
    ordered = [f for f in PREF if f in funcs] + [f for f in dict.fromkeys(funcs) if f not in PREF]

    # --- 输出容器 ---
    outs = re.findall(r'id="(result|output|out|res[a-z0-9_-]*|resultBox[^"]*)"', html, re.I)
    outs = list(dict.fromkeys(outs))

    # --- 是否自动触发 / 有按钮 ---
    has_oninput = bool(re.search(r'oninput=', html, re.I))
    has_btn = bool(re.search(r'<button\b', html, re.I))
    auto = bool(re.search(r'addEventListener\(\s*[\'"]DOMContentLoaded', html))

    lines = [f"--- {slug}"]
    if ins:
        lines.append("   IN   " + ", ".join(ins[:maxinput]))
    if tas:
        lines.append("   TA   " + ", ".join(tas[:5]))
    if sels:
        lines.append("   SEL  " + ", ".join(sels[:4]))
    lines.append("   FN   " + ", ".join(ordered[:8]))
    lines.append(f"   OUT  {', '.join(outs[:5]) or '-'}   btn={int(has_btn)} oninput={int(has_oninput)} DOMCL={int(auto)}")
    return "\n".join(lines)


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else ''
    slugs = [l for l in open('/tmp/zero_A.txt').read().split('\n') if l]
    if prefix and prefix != '-':
        slugs = [s for s in slugs if s.startswith(prefix + '/')]
    for s in slugs:
        print(brief(s))


if __name__ == '__main__':
    main()
