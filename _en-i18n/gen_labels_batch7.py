#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_labels_batch7.py — 交互态标签二批（长键优先 + 公式型标签）

问题1：`计算步骤：` 被更短的 colon 键 `步骤：` 先命中 ⇒ 只译后半，留下 `计算Steps:`。
      修法：补更长键 `计算步骤：`（replaceColonLabelsAll 按长度降序，先命中长键）。
问题2：统计量标签后接公式/字母（`方差 np(1−p)`、`中位数 ln2/λ`、`临界值 z* = …`）
      ⇒ 非冒号短键只串首匹配，需带空格前缀键。
运行：python3 _en-i18n/gen_labels_batch7.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = os.path.join(ROOT, "i18n/tools/en/_prefix.json")
COMMON = os.path.join(ROOT, "i18n/tools/en/_common.json")

PREFIX_ADD = {
    # 长键优先（覆盖 `步骤：` 造成的半译）
    "计算步骤：": "Calculation steps: ",
    "计算过程：": "Calculation process: ",
    "推导步骤：": "Derivation steps: ",
    # 公式型标签（带尾随空格前缀键）
    "方差 ": "Variance ",
    "中位数 ": "Median ",
    "众数 ": "Mode ",
    "平均值 ": "Mean ",
    "均值 ": "Mean ",
    "算术平均 ": "Arithmetic mean ",
    "总和 ": "Sum ",
    "平方和 ": "Sum of squares ",
    "标准差 ": "Standard deviation ",
    "标准差倍数 ": "SD multiplier ",
    "最小值 ": "Minimum ",
    "最大值 ": "Maximum ",
    "极差 ": "Range ",
    "中程数 ": "Midrange ",
    "临界值 ": "Critical value ",
    "检验统计量 ": "Test statistic ",
    "显著性水平 ": "Significance level ",
    "置信区间 ": "Confidence interval ",
    "置信水平 ": "Confidence level ",
    "自由度 ": "Degrees of freedom ",
    "决定系数 ": "Coefficient of determination ",
    "频率 ": "Frequency ",
    "样本量 ": "Sample size ",
    "样本数 ": "Sample size ",
    "期望值 ": "Expected value ",
    "期望 ": "Expected ",
    "标准误差 ": "Standard error ",
    "非中心参数 ": "Noncentrality parameter ",
    "效应量 ": "Effect size ",
    "功效 ": "Power ",
}

COMMON_ADD = {
    "YAML 输出": "YAML Output",
    "JSON 输出": "JSON Output",
    "XML 输出": "XML Output",
    "CSV 输出": "CSV Output",
    "TOML 输出": "TOML Output",
    "qrcode.js 未加载，请检查文件路径": "qrcode.js not loaded; check the file path",
    "请输入有效的数值（支持 255 / 0xff / 0b1111）": "Please enter a valid number (supports 255 / 0xff / 0b1111)",
    "误报 P(E|¬H₁)": "False positive P(E|¬H₁)",
    "证据 P(E)": "Evidence P(E)",
    "贝叶斯因子 BF": "Bayes factor BF",
}


def merge(d, add, path, minlen=2):
    n = 0
    for k, v in add.items():
        assert not re.search(r"[\u4e00-\u9fff]", v), "ZH in value: %r -> %r" % (k, v)
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
a = merge(pf, PREFIX_ADD, PREFIX, minlen=2)
b = merge(cm, COMMON_ADD, COMMON, minlen=2)
print("prefix +%d -> %d ; common +%d -> %d" % (a, len(pf), b, len(cm)))
