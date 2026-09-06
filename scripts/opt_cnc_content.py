# -*- coding: utf-8 -*-
"""真实化 cnc 分类 deep-dive：仅 1 工具 detector-23（CNC 加工尺寸检测反馈）。

content_deepdive[cnc/detector-23] 原为「在cnc场景中先确认Detector 23口径与边界，再输出可复核结论」
泛化变体（summary=None，scenarios/examples/faqs 偏通用流程描述，缺 CNC 检测 specifics）。
重写为真实 CNC 尺寸检测场景（在线/脱机/激光三方式、尺寸偏差、IT 公差等级判定、刀补与加工调整），
补 summary（原 None）。不覆盖 title（title 已真实）。
"""
import json
import os

PATH = "i18n/tools/content_deepdive.json"

with open(PATH, encoding="utf-8") as f:
    D = json.load(f)

KEY = "cnc/detector-23"

D[KEY] = {
    "title": "检测（在线/脱机/激光）反馈",
    "summary": "输入实测尺寸与理论值，按在线、脱机、激光三种检测方式计算尺寸偏差，对照 IT 公差等级判定合格性，并给出刀具补偿与加工调整建议，用于数控加工过程控制与质量验收。",
    "scenarios": [
        "在线检测（机床旁在机测量）实时反馈尺寸偏差，用于加工中动态刀补与过程控制。",
        "脱机检测（三坐标/量具离线测量）用于工序间与终检，按基本尺寸查标准公差表判定 IT 等级。",
        "激光扫描用于薄壁件、软材等非接触测量，避免装夹变形引入误差，关键尺寸以接触式复测为准。",
    ],
    "examples": [
        {
            "title": "轴径偏差核算",
            "body": "实测 Φ30.012 mm、理论 Φ30.000 mm，偏差 +0.012 mm；查该基本尺寸 IT7 公差带为 ±0.010 mm，超差 0.002 mm，建议刀补 -0.012 mm 后复加工并复测。",
        },
    ],
    "faqs": [
        {
            "q": "在线检测与脱机检测怎么选？",
            "a": "在线适合批量件的过程控制与实时补偿，节拍短；脱机（三坐标/量具）精度更高、适合验收与 SPC 统计，但测量节拍长，按精度与产能需求搭配。",
        },
        {
            "q": "IT 公差等级如何判定合格？",
            "a": "按基本尺寸查标准公差表得到公差值，实测偏差落在公差带内为合格；超差需评估可否让步接收或返修，关键配合尺寸不建议放行。",
        },
        {
            "q": "激光检测会不会不准？",
            "a": "激光非接触适合软材、薄壁与易变形件，但受表面反光与温度影响，需在恒温环境校准后测量，重要尺寸仍以接触式测量复测为准。",
        },
    ],
}

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(D, f, ensure_ascii=False, indent=1)
print("opt_cnc_content: rewrote", KEY, "(summary + 3 scenarios + 1 example + 3 faqs)")
