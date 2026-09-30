#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_labels_batch8.py — 交互态标签三批（统计量符号标签收尾）"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = os.path.join(ROOT, "i18n/tools/en/_prefix.json")
COMMON = os.path.join(ROOT, "i18n/tools/en/_common.json")

PREFIX_ADD = {
    "几何平均 ": "Geometric mean ",
    "调和平均 ": "Harmonic mean ",
    "四分位距 ": "Interquartile range ",
    "合计 ": "Total ",
    "数量级 ": "Order of magnitude ",
    "每组样本量 ": "Sample size per group ",
    "理论值 ": "Theoretical value ",
    "偏差 ": "Deviation ",
    "投影 ": "Projection ",
    "偏度 ": "Skewness ",
    "峰度 ": "Kurtosis ",
    "总和 ": "Sum ",
    "平方和 ": "Sum of squares ",
    "样本相关系数 ": "Sample correlation ",
    "组间 ": "Between groups ",
    "组内 ": "Within groups ",
}

COMMON_ADD = {
    "中位数 (median)": "Median",
    "众数 (mode)": "Mode",
    "方差 (variance)": "Variance",
    "标准差 (σ)": "Standard deviation (σ)",
    "极差 (range)": "Range",
    "极差 (Range)": "Range",
    "中程数 (Midrange)": "Midrange",
    "总和 (sum)": "Sum",
    "四分位距 (IQR)": "Interquartile range (IQR)",
    "偏度 (skewness)": "Skewness",
    "峰度 (kurtosis)": "Kurtosis",
    "算术平均 (AM)": "Arithmetic mean (AM)",
    "几何平均 (GM)": "Geometric mean (GM)",
    "调和平均 (HM)": "Harmonic mean (HM)",
}


def merge(d, add, path, minlen=2):
    n = 0
    for k, v in add.items():
        assert not re.search(r"[\u4e00-\u9fff]", v), "ZH in value: %r" % k
        assert len(k) >= minlen, "short key: %r" % k
        if k in d:
            continue
        d[k] = v
        n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return n


pf = json.load(open(PREFIX, encoding="utf-8"))
cm = json.load(open(COMMON, encoding="utf-8"))
a = merge(pf, PREFIX_ADD, PREFIX, 2)
b = merge(cm, COMMON_ADD, COMMON, 2)
print("prefix +%d -> %d ; common +%d -> %d" % (a, len(pf), b, len(cm)))
