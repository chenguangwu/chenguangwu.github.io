#!/usr/bin/env python3
"""realize(stone): 替换真占位键 stone/detector-strength-color-diff（质量（色差/强度/标准）检测）为真实 deep-dive 内容。

诊断：原 deep-dive 为六型占位套话同义变体（"在stone场景下先确认Detector Strength Color Diff口径与边界，再输出
可复核结论""适用于流程复用、异常复核、版本变更对照""降低追溯成本"），含大写未替换变量名 "Detector Strength Color
Diff"（basename 直译），被旧 scanner 精确指纹词规避而漏报（补强 scanner 后捕获）。本脚本以真实质量色差/强度检测内容
覆盖，键数守恒（不删键），ci 5022。
"""
import json
import sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

KEY = "stone/detector-strength-color-diff"
assert KEY in data, f"键 {KEY} 不存在"

before = len(data)
assert before == 5022, f"键数异常: {before}"

data[KEY] = {
    "title": "质量（色差/强度/标准）检测",
    "scenarios": [
        "色差判定：输入样品与标样的 Lab 色值，计算 ΔE（CIEDE2000）色差，对照客户或行业允差（如 ΔE≤1.5 严控、≤2.0 一般可接受）判定合格与否。",
        "强度检测判定：输入抗压/抗折/抗拉强度实测值，对照标准等级（如石材抗折强度、混凝土强度等级）判定达标情况。",
        "多批次一致性比对：同批次多样品色差/强度横向比对，识别离散过大或超差项，辅助工艺调整与分档。"
    ],
    "examples": [
        {
            "title": "石材色差判定示例",
            "body": "标样 L=75.2 a=2.1 b=18.3，样品 L=74.8 a=2.4 b=19.0，计算得 ΔE≈0.9，低于客户允差 ΔE≤1.5 → 判定色差合格；若另一块 ΔE=2.3 则超差需剔除。"
        }
    ],
    "faqs": [
        {
            "q": "色差用什么标准判定？",
            "a": "常用 CIEDE2000 的 ΔE 值，允差由客户或行业标准（石材、涂料、塑料等）规定，需先确认适用的允差范围再判定。"
        },
        {
            "q": "强度单位不一致怎么办？",
            "a": "先统一单位与试验条件（如 MPa、同尺寸试样、同加载速率）再比对，避免口径不同导致误判。"
        }
    ]
}

after = len(data)
assert after == 5022, f"键数守恒失败: {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"[OK] {KEY} 已替换为真实质量（色差/强度/标准）检测内容；键数守恒 {before} -> {after}")
