#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 edu2 分类硬编码套话。

- C 类：5 页 tool-intro-body 含与 edu 同款通用套话（通用 li 8 类 + 简介后缀「教育学习工具，辅助学习，提升效率」），
  删通用 li 与空 ul/h4，保留真实 li。
- B 类：study-progress 3 处 opt 套话「工作与生活中的相关计算与查询」→真实场景（JSON-LD 合法）。
- A 类：schedule-conflict 的 formula-desc 为工程错配（"本工程计算基于标准物理与材料公式"），→真实课程表冲突描述。
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
B_PLACE = "工作与生活中的相关计算与查询。"
B_REAL = "用于按目标总量与已完成量追踪学习完成度、预估完工日期，辅助备考节奏管理与学情自查。"
A_PLACE = "本工程计算基于标准物理与材料公式，输入为标准工程单位，结果仅供参考。"
A_REAL = "本工具按课程时间表的周次、星期与节次规则检测时间重叠冲突，结果仅供参考；正式排课以学校教务安排为准。"


def clean_body(body):
    new = body
    for x in GENERIC:
        new = re.sub(r'<li[^>]*>\s*' + re.escape(x) + r'\s*</li>', '', new)
    new = re.sub(r'<ul[^>]*>\s*</ul>', '', new)
    new = re.sub(r'<h4[^>]*>(?:(?!</h4>).)*?(功能特点|使用场景)(?:(?!</h4>).)*?</h4>\s*(?!<ul)', '', new, flags=re.S)
    new = new.replace(SUFFIX, '')
    new = re.sub(r'\n\s*\n\s*\n+', '\n\n', new)
    return new


total_c = total_b = total_a = 0
for h in sorted(glob.glob("tools/edu2/*.html")):
    if h.endswith("index.html"):
        continue
    t = open(h, encoding="utf-8").read()
    c_n = 0
    m = re.search(r'<div class="tool-intro-body"[^>]*>(.*?)</div>', t, re.S)
    if m:
        body = m.group(1)
        c_n = sum(body.count(x) for x in GENERIC) + body.count(SUFFIX)
    b_n = t.count(B_PLACE)
    a_n = t.count(A_PLACE)
    if DRY:
        if c_n or b_n or a_n:
            print(os.path.basename(h), "C套话:", c_n, "B套话:", b_n, "A错配:", a_n)
        continue
    new_t = t
    if c_n:
        new_body = clean_body(body)
        new_t = re.sub(r'(<div class="tool-intro-body"[^>]*>)(.*?)(</div>)',
                       lambda mm: mm.group(1) + new_body + mm.group(3), new_t, count=1, flags=re.S)
        total_c += c_n
    if b_n:
        new_t = new_t.replace(B_PLACE, B_REAL)
        total_b += b_n
    if a_n:
        new_t = new_t.replace(A_PLACE, A_REAL)
        total_a += a_n
    if new_t != t:
        open(h, "w", encoding="utf-8").write(new_t)

if DRY:
    print("dry 完成；无输出即无套话")
else:
    print(f"已清理：C套话 {total_c} 处，B套话 {total_b} 处，A错配 {total_a} 处")
    # JSON-LD 合法性快速校验
    import json
    for h in glob.glob("tools/edu2/*.html"):
        if h.endswith("index.html"):
            continue
        tt = open(h, encoding="utf-8").read()
        mm = re.search(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', tt, re.S)
        if mm:
            try:
                json.loads(mm.group(1))
            except Exception as e:
                print("JSON-LD 解析失败:", os.path.basename(h), e)
