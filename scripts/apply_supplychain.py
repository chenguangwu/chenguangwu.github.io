#!/usr/bin/env python3
"""realize(supplychain): 替换真占位键 supplychain/cycle-16（供应链 KPI 仪表盘）为真实 deep-dive 内容。

诊断：原 deep-dive 为六型占位套话同义变体（"在supplychain场景中先确认Cycle 16口径与边界，再输出可复核结论"
"适用于流程复用、异常复核、版本变更对照""降低追溯成本"），含大写未替换变量名 "Cycle 16"，被旧 scanner 精确
指纹词规避而漏报。本脚本以真实供应链 KPI 工程内容覆盖，键数守恒（不删键），ci 5022。
"""
import json
import sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

KEY = "supplychain/cycle-16"
assert KEY in data, f"键 {KEY} 不存在"

before = len(data)
assert before == 5022, f"键数异常: {before}"

data[KEY] = {
    "title": "供应链 KPI 仪表盘",
    "scenarios": [
        "履约与交付监控：汇总订单履约率、准时交付率、缺货率等指标，按周/月生成趋势看板，快速定位异常环节。",
        "库存效率评估：计算库存周转率、呆滞库存占比，识别占用资金较多的低效 SKU，辅助清仓与补货决策。",
        "供应商交付对比：多家供应商的准时率、批次合格率横向比对，支撑采购集中度与备选方案决策。"
    ],
    "examples": [
        {
            "title": "月度供应链 KPI 看板示例",
            "body": "输入：订单履约率 96%、准时交付率 92%、库存周转率 8 次/年、缺货率 2%。系统汇总后标注准时交付率低于目标 95% 触发预警，并提示呆滞库存占比偏高项，便于运营复盘与改进。"
        }
    ],
    "faqs": [
        {
            "q": "指标口径不一致怎么办？",
            "a": "先统一各指标定义与统计周期（如按月滚动），再汇总对比，避免口径不同导致误判。"
        },
        {
            "q": "数据从哪来、会上传吗？",
            "a": "由你本地录入或粘贴各系统导出数据，工具仅在浏览器内计算，不上传任何数据，可放心使用。"
        }
    ]
}

after = len(data)
assert after == 5022, f"键数守恒失败: {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"[OK] {KEY} 已替换为真实供应链 KPI 仪表盘内容；键数守恒 {before} -> {after}")
