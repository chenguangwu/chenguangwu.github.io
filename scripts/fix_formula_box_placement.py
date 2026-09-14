#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 formula-box 误插入 <script>/模板字符串 的问题（幂等，全站扫描）。

背景：add_fitness_formula.py / add_math_formula.py 等生成器的锚点搜索遍历全文，
命中 JS 模板串里的 `class="input-row"` / `class="tip-box"`，把公式框插进 JS 源码
（单引号串会直接 SyntaxError；模板串虽能解析但会把公式框渲染进输入区）。

本脚本对全站被污染页做两步修复：
  1) 用 div 配平精确摘除「位于 <script>/<style> 块内」的注入型 formula-box；
     若摘除点在 script 内，顺带清掉接缝处的裸换行（否则 JS 字符串仍被撕裂）。
  2) 按项目惯例重新插到 markup 内首个输入容器之前（介绍段落之后）。

用法：python3 scripts/fix_formula_box_placement.py [--apply]
"""
import argparse
import glob
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 与各 add_*_formula.py 保持一致的锚点优先级
ANCHORS = ["tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row"]
# 无锚点时的兜底插入点（同为「介绍段落之后的第一个容器」）
FALLBACKS = ['<div class="type-grid"', '<div class="input-area"', '<div class="toolbar"',
             '<div class="result-box"', '<div id="inputArea"']
# 仅由生成器插入的精确签名（页面自带的动态 formula-box 不带 card 前缀）
SIG = '<div class="card formula-box">'


def script_spans(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<script\b[\s\S]*?</script>', s, re.I)]


def style_spans(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<style\b[\s\S]*?</style>', s, re.I)]


def in_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)


def box_span(s, i):
    """从 formula-box 起点做 div 配平，返回 (start, end)。"""
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[i:]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return (i, i + m.end())
        else:
            depth += 1
    return (-1, -1)


def markup_anchor(s, spans):
    """首个位于 markup（非 script/style）内的锚点位置。"""
    for a in ANCHORS:
        for m in re.finditer(r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s):
            if in_spans(m.start(), spans):
                continue
            return m.start()
    for f in FALLBACKS:
        i = s.find(f)
        if i >= 0 and not in_spans(i, spans):
            return i
    return -1


def js_ok(content, tag="probe"):
    """抽取内联 JS 块用 node --check 逐个校验（过滤 JSON-LD）。"""
    tmp = "/tmp/_fbfp_js"
    os.makedirs(tmp, exist_ok=True)
    for k, m in enumerate(re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', content, re.I)):
        if "src=" in m.group(1) or "application/" in m.group(1):
            continue
        fp = os.path.join(tmp, "%s_%d.js" % (tag, k))
        open(fp, "w", encoding="utf-8").write(m.group(2))
        r = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
        if r.returncode != 0:
            return False, (r.stderr.strip().splitlines() or [""])[0][:90]
    return True, ""


def fix_one(fp, apply_writes):
    rel = os.path.relpath(fp, ROOT)
    s = open(fp, encoding="utf-8").read()
    sp = script_spans(s) + style_spans(s)
    found = None
    for m in re.finditer(re.escape(SIG), s):
        if in_spans(m.start(), sp):
            found = box_span(s, m.start())
            break
    if not found or found[0] < 0:
        return ("skip", "无注入型公式框落在 script/style 内", "")

    start, end = found
    inside_script = in_spans(start, script_spans(s))
    box = s[start:end]
    out = s[:start] + s[end:]
    # 接缝处裸换行清理：清掉紧邻的换行（script 内的裸换行会撕裂 JS 字符串）
    if inside_script:
        k = start
        while k < len(out) and out[k] == "\n":
            out = out[:k] + out[k + 1:]
        # 前向：若摘除点前紧邻换行且其后是 markup 标签衔接处，也清一个
        while start > 0 and out[start - 1] == "\n":
            out = out[:start - 1] + out[start:]
            start -= 1

    pos = markup_anchor(out, script_spans(out) + style_spans(out))
    if pos < 0:
        return ("fail", "无 markup 锚点，跳过", "")
    final = out[:pos] + box + "\n" + out[pos:]

    # 自检 1：公式框不得再落在 script/style 内
    sp2 = script_spans(final) + style_spans(final)
    i2 = final.find(SIG)
    if not (i2 > 0 and not in_spans(i2, sp2)):
        return ("fail", "修复后仍落在 script 内", "")
    # 自检 2：node --check 全部内联 JS（dry-run 也验，probe 用临时文件）
    ok, err = js_ok(final, tag=os.path.basename(fp))
    if not ok:
        return ("fail", "修复后 JS 仍报错: " + err, "")
    if apply_writes:
        open(fp, "w", encoding="utf-8").write(final)
    return ("ok", "box %d 字节 → markup pos %d%s" % (len(box), pos, "（含接缝换行清理）" if inside_script else ""), "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    pages = sorted(glob.glob(os.path.join(ROOT, "tools", "*", "*.html")))
    hits = []
    for fp in pages:
        if os.path.basename(fp) == "index.html":
            continue
        s = open(fp, encoding="utf-8", errors="ignore").read()
        if SIG not in s:
            continue
        sp = script_spans(s) + style_spans(s)
        if any(in_spans(m.start(), sp) for m in re.finditer(re.escape(SIG), s)):
            hits.append(fp)

    print("命中页面 %d 个" % len(hits))
    nok = 0
    for fp in hits:
        status, msg, _ = fix_one(fp, a.apply)
        print("  [%s] %s :: %s" % (status, os.path.relpath(fp, ROOT), msg))
        if status == "ok":
            nok += 1
    print("完成%s：修复 %d/%d" % ("（--apply）" if a.apply else "（dry-run，未落盘）", nok, len(hits)))


if __name__ == "__main__":
    main()
