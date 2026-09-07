#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 edu 分类工具页 tool-intro-body 内的通用套话。

edu 43 页（24-point-solver 无 tool-intro-body 跳过）的 tool-intro-body 含统一通用套话：
- 简介 <p> 后缀：「教育学习工具，辅助学习，提升效率。」
- 功能特点 ul 全 4 条：辅助学习，提升效率 / 计算精准，支持多种参数 / 纯前端处理，数据不上传 / 支持手机使用，随时随地学习
- 使用场景 ul 全 4 条：学生学习与作业辅助 / 教师教学与成绩管理 / 考试备考与知识复习 / 终身学习的工具支持
- 变体：纯前端，数据不上传（1 次）
各工具还有真实 li（如「动态添加/删除科目」）保留；删除通用 li 后若 ul 空则连 h4 一并删除。
A 类 formula-desc 经核验全为真实领域描述，B 类 0 命中，均无需处理。
"""
import re, sys, glob, os

DRY = "--dry" in sys.argv
GENERIC = [
    "辅助学习，提升效率",
    "计算精准，支持多种参数",
    "纯前端处理，数据不上传",
    "纯前端，数据不上传",
    "支持手机使用，随时随地学习",
    "学生学习与作业辅助",
    "教师教学与成绩管理",
    "考试备考与知识复习",
    "终身学习的工具支持",
]
SUFFIX = "教育学习工具，辅助学习，提升效率。"


def clean_body(body):
    new = body
    for x in GENERIC:
        new = re.sub(r'<li[^>]*>\s*' + re.escape(x) + r'\s*</li>', '', new)
    new = re.sub(r'<ul[^>]*>\s*</ul>', '', new)
    # 删孤立 h4（功能特点/使用场景，其后不再跟 ul）；限定在单个 h4 内部，避免跨标签误删简介 h4
    new = re.sub(r'<h4[^>]*>(?:(?!</h4>).)*?(功能特点|使用场景)(?:(?!</h4>).)*?</h4>\s*(?!<ul)', '', new, flags=re.S)
    new = new.replace(SUFFIX, '')
    # 压缩因删除产生的连续空行
    new = re.sub(r'\n\s*\n\s*\n+', '\n\n', new)
    return new


total_li = 0
total_suf = 0
pages = 0
for h in sorted(glob.glob("tools/edu/*.html")):
    if h.endswith("index.html"):
        continue
    t = open(h, encoding="utf-8").read()
    m = re.search(r'<div class="tool-intro-body"[^>]*>(.*?)</div>', t, re.S)
    if not m:
        continue
    body = m.group(1)
    li_n = sum(len(re.findall(r'<li[^>]*>\s*' + re.escape(x) + r'\s*</li>', body)) for x in GENERIC)
    suf_n = body.count(SUFFIX)
    if DRY:
        if li_n or suf_n:
            print(os.path.basename(h), "li套话:", li_n, "简介后缀:", suf_n)
        continue
    new = clean_body(body)
    t2 = re.sub(r'(<div class="tool-intro-body"[^>]*>)(.*?)(</div>)',
                lambda mm: mm.group(1) + new + mm.group(3), t, count=1, flags=re.S)
    if t2 != t:
        open(h, "w", encoding="utf-8").write(t2)
        pages += 1
        total_li += li_n
        total_suf += suf_n

if DRY:
    print("dry 完成：以上为含套话页；无输出即无套话")
else:
    print(f"已清理页: {pages}，删除 li 套话: {total_li}，删除简介后缀: {total_suf}")
