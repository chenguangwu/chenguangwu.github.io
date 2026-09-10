#!/usr/bin/env python3
"""realize(food-safety): 替换真占位键 food-safety/summary（重金属（限量）汇总）为真实 deep-dive 内容。

诊断：原 deep-dive 正文为六型占位套话（"在food-safety场景下先把Summary标准化""适合做统一复核点输出
减少重复确认成本""边界样本建议单独标注"等，且出现大写变量名 "Summary" 未替换），属模板未填真实内容。
本脚本以真实重金属限量汇总工程内容覆盖，键数守恒（不删键），ci 5022。
"""
import json
import sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

KEY = "food-safety/summary"
assert KEY in data, f"键 {KEY} 不存在"

before = len(data)
assert before == 5022, f"键数异常: {before}"

data[KEY] = {
    "title": "重金属（限量）汇总",
    "scenarios": [
        "多批次原料合规筛查：把不同批次原料的铅、镉、汞、砷等检出值集中录入，按 GB 2762 对应食品类别的限量逐项判定合格或超标，生成比对汇总表。",
        "成品多元素终检汇总：成品检测报告中铅、镉、总汞、无机砷、铬等汇总，自动匹配食品类别限量，输出超标项与超标倍数清单，辅助出厂放行决策。",
        "供应商横向比对：同一指标多家供应商数据并列，快速定位高风险来源批次，便于溯源整改与复检闭环。"
    ],
    "examples": [
        {
            "title": "稻米重金属汇总示例",
            "body": "稻米中铅 0.18 mg/kg（GB 2762 谷物限量 0.2，合格）、镉 0.22（限量 0.2，超标 1.10×）、总汞 0.01（限量 0.02，合格）、无机砷 0.15（限量 0.2，合格）→ 仅镉超标，结论：镉不符合、其余符合，建议复检并追溯该批次来源。"
        }
    ],
    "faqs": [
        {
            "q": "限量依据哪个标准？",
            "a": "默认依据 GB 2762《食品安全国家标准 食品中污染物限量》；谷物、蔬菜、水产、乳与乳制品等类别限量不同，使用前需先选对食品类别再比对。"
        },
        {
            "q": "检出值低于检测限怎么记？",
            "a": "低于方法检测限的一般按“未检出”计，不参与超标判定，但建议在汇总表备注实际检出限，便于复核与追溯。"
        },
        {
            "q": "同一指标多批次如何汇总？",
            "a": "按批次分列，超标项高亮并给出超标倍数（检出值÷限量），便于整改跟踪与复检闭环。"
        }
    ]
}

after = len(data)
assert after == 5022, f"键数守恒失败: {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"[OK] {KEY} 已替换为真实重金属限量汇总内容；键数守恒 {before} -> {after}")
