#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 elderly 分类硬编码套话。

- C 类：8 页 tool-intro-body 含两套通用套话 li（health 组 8 句 + assessor 组 8 句）及简介后缀，
  删通用 li 与空 ul/h4，保留真实 li（reminder-time）。简介真实前半句保留。
- A 类：assessor-35/36/37/risk-1 共 4 页的 formula-desc 为「校验工具」错配
  （实际是护理/社工/质量/防跌倒评估量表），→真实评估描述；其余 2 页保留。
- B 类：0 命中。
"""
import re, sys, glob, os

DRY = "--dry" in sys.argv
GENERIC = [
    # health-medical 组
    "基于权威健康标准计算",
    "支持多种参数输入",
    "提供详细的健康参考建议",
    "健康数据不上传，隐私安全",
    "日常健康监测与管理",
    "健身计划制定参考",
    "体检报告解读辅助",
    "健康知识学习",
    # assessor 组
    "纯前端处理，数据不上传服务器",
    "操作简单，一键完成",
    "实时显示结果，所见即所得",
    "支持复制和下载结果",
    "日常办公与学习",
    "开发调试与数据处理",
    "快速计算与格式转换",
    "信息查询与参考",
]
HEALTH_SUFFIX = "健康指标计算工具，基于权威医学标准，数据本地处理保护隐私。"
ASSESSOR_SUFFIX = "免费在线工具，纯前端处理，数据不上传，保护隐私安全。"
A_BAD = "本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；"
A_GOOD = "本评估工具依据对应量表的维度与评分规则汇总得分，给出等级或风险参考；"


def clean_body(body):
    new = body
    for x in GENERIC:
        new = re.sub(r'<li[^>]*>\s*' + re.escape(x) + r'\s*</li>', '', new)
    new = re.sub(r'<ul[^>]*>\s*</ul>', '', new)
    new = re.sub(r'<h4[^>]*>(?:(?!</h4>).)*?(功能特点|使用场景)(?:(?!</h4>).)*?</h4>\s*(?!<ul)', '', new, flags=re.S)
    new = new.replace(HEALTH_SUFFIX, '')
    new = new.replace(ASSESSOR_SUFFIX, '')
    new = re.sub(r'\n\s*\n\s*\n+', '\n\n', new)
    return new


total_c = total_a = 0
for h in sorted(glob.glob("tools/elderly/*.html")):
    if h.endswith("index.html"):
        continue
    t = open(h, encoding="utf-8").read()
    c_n = 0
    m = re.search(r'<div class="tool-intro-body"[^>]*>(.*?)</div>', t, re.S)
    if m:
        body = m.group(1)
        c_n = sum(body.count(x) for x in GENERIC) + body.count(HEALTH_SUFFIX) + body.count(ASSESSOR_SUFFIX)
    a_n = t.count(A_BAD)
    if DRY:
        if c_n or a_n:
            print(os.path.basename(h), "C套话:", c_n, "A错配:", a_n)
        continue
    new_t = t
    if c_n:
        new_body = clean_body(body)
        new_t = re.sub(r'(<div class="tool-intro-body"[^>]*>)(.*?)(</div>)',
                       lambda mm: mm.group(1) + new_body + mm.group(3), new_t, count=1, flags=re.S)
        total_c += c_n
    if a_n:
        new_t = new_t.replace(A_BAD, A_GOOD)
        total_a += a_n
    if new_t != t:
        open(h, "w", encoding="utf-8").write(new_t)

if DRY:
    print("dry 完成；无输出即无套话")
else:
    print(f"已清理：C套话 {total_c} 处，A错配 {total_a} 处")
