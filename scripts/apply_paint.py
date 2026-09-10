#!/usr/bin/env python3
"""realize(paint): 替换真占位键 paint/detector-40（质量（标准/检测/环保）认证）为真实 deep-dive 内容。

诊断：原 deep-dive 为六型占位套话同义变体（"在paint场景下先确认Detector 40口径与边界，再输出可复核结论"
"适用于流程复用、异常复核、版本变更对照""降低追溯成本"），含大写未替换变量名 "Detector 40"，被旧 scanner 精确
指纹词规避而漏报（补强 scanner 后捕获）。本脚本以真实质量标准符合性判定内容覆盖，键数守恒（不删键），ci 5022。
"""
import json
import sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

KEY = "paint/detector-40"
assert KEY in data, f"键 {KEY} 不存在"

before = len(data)
assert before == 5022, f"键数异常: {before}"

data[KEY] = {
    "title": "质量（标准/检测/环保）认证",
    "scenarios": [
        "标准符合性判定：输入产品材质、检测指标与限值，对照适用标准（如国标、ISO 9001、RoHS、REACH）逐项判定合格或超标。",
        "环保认证预评估：汇总限用物质（铅、镉、汞、六价铬、多溴联苯等）检测值，判断是否满足 RoHS/REACH 限值，输出合规结论。",
        "检测报告归档比对：多批次检测报告按相同指标横向比对，快速识别波动与高风险项。"
    ],
    "examples": [
        {
            "title": "电子件 RoHS 合规示例",
            "body": "某电子外壳铅检测 0.05%（RoHS 限值 0.1%），镉 0.008%（限值 0.01%），均低于限值 → 判定符合 RoHS；六价铬未检出 → 符合。结论：该批次满足 RoHS 指令要求。"
        }
    ],
    "faqs": [
        {
            "q": "适用哪些标准？",
            "a": "常见有国标（GB）、ISO 9001 质量管理体系、RoHS/REACH 等环保指令；具体以产品出口地区与行业法规为准，需先选对标准集。"
        },
        {
            "q": "检测值低于限值就一定能认证吗？",
            "a": "单项达标只是符合性判定的必要非充分条件，还需完整体系文件与第三方机构审核；本工具仅做指标预评估，正式认证以发证机构结论为准。"
        }
    ]
}

after = len(data)
assert after == 5022, f"键数守恒失败: {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"[OK] {KEY} 已替换为真实质量（标准/检测/环保）认证内容；键数守恒 {before} -> {after}")
