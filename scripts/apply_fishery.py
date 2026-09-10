# -*- coding: utf-8 -*-
"""真实化 fishery 分类 deep-dive 占位。键数守恒 5022。
说明：fishery 46→39 键中仅 fishery/estimate-emission-wastewater 为 STY3 孤儿占位
（无对应 HTML，线上页由 fishery/wastewater-cod 真实注入）；其余 38 键 + wastewater-cod 早已真实化。
本脚本仅替换该 1 孤儿键为真实工程内容（不删键，保 5022）。
"""
import json
import os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = os.path.join(ROOT, "i18n/tools/content_deepdive.json")

d = json.load(open(P, encoding="utf-8"))
before = len(d)
assert "fishery/estimate-emission-wastewater" in d, "孤儿键缺失"

d["fishery/estimate-emission-wastewater"] = {
    "title": "养殖废水排放COD估算",
    "scenarios": [
        "排放前合规自检：按日投饵量与 COD 产生系数估算废水 COD 负荷与排放浓度，判断是否超过《污水综合排放标准》或地方养殖尾水标准（通常 30–50 mg/L），避免超标排放被处罚。",
        "处理工艺选型：根据超标倍数反算所需稀释水量或氧化/生化处理削减率，比选曝气、人工湿地、生物滤池等工艺的经济性与可行性。",
        "总量核算与申报：多塘/多池并联时汇总各单元 COD 产生量，按排污许可要求核算年排放总量并留痕，便于环保核查与溯源。"
    ],
    "examples": [
        {
            "title": "算例：日投饵 100 kg 的排放 COD 核算",
            "body": "输入：日投饵 100 kg、COD 产生系数 0.35 kg COD/kg 饲料、排水量 500 m³/天、排放标准 30 mg/L。计算：COD 负荷 = 100 × 0.35 = 35.0 kg/天；排放浓度 = 35.0×1000 ÷ 500 = 70.0 mg/L；超标倍数 = 70.0 ÷ 30 ≈ 2.33 倍；若仅靠稀释达标，需补充水量 = (70.0−30)×500÷30 ≈ 666.7 m³/天。结论：该场排放 COD 超标约 2.33 倍，须配套处理设施或增大尾水交换量，不可直排。"
        }
    ],
    "faqs": [
        {
            "q": "COD 产生系数 0.35 是怎么来的？",
            "a": "水产养殖废水的 COD 主要来源于残饵与粪便，经验上可按饲料投喂量的 0.3–0.5 倍（kg COD/kg 饲料）估算，常用 0.35 作为综合系数；具体取值应结合养殖品种、投饵率与残饵率修正，本工具仅作快速估算，正式环评以实测或地方系数手册为准。"
        },
        {
            "q": "排放浓度超标就一定要建处理设施吗？",
            "a": "不一定。轻度超标（如 1–2 倍）可通过增加尾水交换量、种植水生植物或建设人工湿地自然净化来削减；超标数倍时单靠稀释不经济且可能受取水限制，需上曝气、生物滤池或絮凝沉淀等工程措施。最终以当地生态环境部门核发的排放标准与排污许可为准。"
        }
    ]
}

after = len(d)
assert before == after, f"键数变化 {before}->{after}"
assert before == 5022, f"键数不为 5022: {before}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"OK fishery 孤儿键真实化完成: 键数守恒 {before}（estimate-emission-wastewater 1 键已替换为真实内容）")
