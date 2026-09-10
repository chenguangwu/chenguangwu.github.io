#!/usr/bin/env python3
"""realize(outdoor): 替换真占位键 outdoor/analysis-spacing（攀岩挂片间距与受力分析）为真实 deep-dive 内容。

诊断：原 deep-dive 为六型占位套话同义变体（"在outdoor场景下先确认Analysis Spacing口径与边界，再输出可复核结论"
"适用于流程复用、异常复核、版本变更对照""降低追溯成本"），含大写未替换变量名 "Analysis Spacing"，被旧 scanner 精确
指纹词规避而漏报（补强 scanner 后捕获）。本脚本以真实攀岩保护站受力分析内容覆盖，键数守恒（不删键），ci 5022。
"""
import json
import sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

KEY = "outdoor/analysis-spacing"
assert KEY in data, f"键 {KEY} 不存在"

before = len(data)
assert before == 5022, f"键数异常: {before}"

data[KEY] = {
    "title": "攀岩挂片间距与受力分析",
    "scenarios": [
        "多锚点保护站受力分配：输入各挂片间距与夹角，计算单锚点分担的力，判断是否满足单锚额定强度。",
        "夹角因子评估：根据两挂片与受力方向的夹角计算角度因子（如 60° 夹角下每锚约分担 0.58×总力），避免单锚过载。",
        "顶绳/先锋布点校验：核对挂片水平间距与坠落系数，给出间距建议，降低锚点失效风险。"
    ],
    "examples": [
        {
            "title": "双挂片保护站受力示例",
            "body": "总受力 10 kN、两挂片夹角 60°，角度因子 0.58，则每片分担约 5.8 kN；若单挂片额定 12 kN 则安全。若夹角扩大到 90°，因子升至约 0.71，单锚 7.1 kN，仍安全但余量减小。"
        }
    ],
    "faqs": [
        {
            "q": "夹角越大越安全吗？",
            "a": "不一定。夹角越大（越接近平行）单锚分担越小，但夹角过小（<30°）会使单锚接近总力且产生外拔力，建议控制在 60°–90° 之间。"
        },
        {
            "q": "间距和受力有什么关系？",
            "a": "间距决定夹角：固定受力方向时，两挂片间距越小夹角越小、单锚分担越大；需结合锚点强度与地形合理布点。"
        }
    ]
}

after = len(data)
assert after == 5022, f"键数守恒失败: {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"[OK] {KEY} 已替换为真实攀岩挂片间距与受力分析内容；键数守恒 {before} -> {after}")
