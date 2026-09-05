#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量去除 750 目标工具页 desc-en 中的「Free online tool on ToolBox ...」完全相同模板套话。

策略（0 成本、仅改 meta content、不引入翻译）：
- desc-en 形如「{英文工具名} - {通用短语}. Free online tool on ToolBox — 100% client-side...」
- 截断到首个「Free online tool on ToolBox」出现处，保留每个工具独有的英文前缀（含工具名，天然唯一）
- 已独立撰写的高质量 desc-en（不含该标记）原样保留
- 仅作用于 OPTIMIZE-TASKS.md 中的 750 目标页，避免大范围不可控改动
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "Free online tool on ToolBox"
DESCEN_RE = re.compile(r'(<meta\s+name=["\']desc-en["\']\s+content=["\'])([^"\']*)(["\'])', re.IGNORECASE)


def load_targets():
    out = []
    with open(os.path.join(ROOT, "OPTIMIZE-TASKS.md"), encoding="utf-8") as f:
        lines = f.read().splitlines()
    inb = False
    for ln in lines:
        if ln.startswith("## 批次"):
            inb = True
            continue
        if inb and ln.startswith("## ") and not ln.startswith("## 批次"):
            inb = False
        if not inb:
            continue
        m = re.match(r"- \[[ x]\] #\d+ `([^`]+)`", ln)
        if m:
            out.append(m.group(1))
    return out


def clean_desc(v):
    idx = v.find(MARK)
    if idx < 0:
        return None  # 无模板，保持原样
    prefix = v[:idx].strip()
    # 去掉前缀尾部残留的标点/空格（如 "Growth Chart - free online tool" 末尾无句点）
    prefix = prefix.rstrip(". ").strip()
    if not prefix:
        return None
    return prefix


def main():
    targets = load_targets()
    changed = 0
    skipped = 0
    for rel in targets:
        fp = os.path.join(ROOT, rel)
        if not os.path.exists(fp):
            skipped += 1
            continue
        s = open(fp, encoding="utf-8", errors="ignore").read()
        m = DESCEN_RE.search(s)
        if not m:
            skipped += 1
            continue
        new_val = clean_desc(m.group(2))
        if new_val is None:
            skipped += 1
            continue
        new_tag = m.group(1) + new_val + m.group(3)
        s2 = s[: m.start()] + new_tag + s[m.end():]
        if s2 != s:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(s2)
            changed += 1
    print(f"desc-en 去模板完成：修改 {changed} 页，跳过（无模板/不存在）{skipped} 页，目标总数 {len(targets)}")


if __name__ == "__main__":
    main()
