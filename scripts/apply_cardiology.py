import json, os, sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

assert "cardiology/calc-2" in data, "calc-2 key missing"
before = len(data)
assert before == 5022, f"keys before = {before}"

# calc-2 是 chads2-vasc 的孤儿重复占位键（calc-2.html 已并入 chads2-vasc.html）。
# 保键(5022)、替换为真实 CHA2DS2-VASc 内容，消除占位指纹。
data["cardiology/calc-2"] = {
    "title": "房颤 CHA₂DS₂-VASc 栓塞风险评估",
    "scenarios": [
        "CHA₂DS₂-VASc 评分累加：充血性心衰、高血压、年龄≥75岁（计2分）、糖尿病、卒中/TIA/血栓栓塞史（计2分）、血管疾病（心梗/外周动脉病/主动脉斑块）、年龄65–74岁、女性各计1分，总分0–9分。",
        "抗凝指征：非瓣膜性房颤中，男性≥2分、女性≥3分推荐口服抗凝；男性1分或女性2分为个体化权衡区间；0分（男）/1分（女）通常不需抗凝。",
        "出血风险评估：启动抗凝前以 HAS-BLED 评估（高血压、肾/肝功能异常、卒中史、出血史、INR 波动、老年、药物/酒精各1分），≥3分为高出血风险，应纠正可逆因素而非停抗凝。"
    ],
    "examples": [
        {
            "title": "基线算例（女性 73 岁高血压）",
            "body": "输入：女性、73岁、高血压、余无。累加：年龄65–74（+1）+高血压（+1）=2分（单纯女性不再独立计分）。抗凝建议：女性2分为灰色地带，需结合出血风险与意愿个体化决策；HAS-BLED 另行评估。注：具体药物与剂量由医师依肾功能、依从性确定。"
        }
    ],
    "faqs": [
        {
            "q": "为什么年龄≥75岁计2分而65–74岁只计1分？",
            "a": "年龄是房颤卒中最强的独立危险因素之一，≥75岁卒中风险陡增，指南赋予双倍权重；65–74岁为中等风险计1分。切点来自队列研究的剂量-反应关系。"
        },
        {
            "q": "女性是否独立作为危险因素？",
            "a": "现行指南不再将「单纯女性」作为独立抗凝指征；女性仅在达到相应总分阈值（女性≥3分）时才推荐抗凝，以避免对低危女性过度抗凝。"
        },
        {
            "q": "HAS-BLED 高就要停抗凝吗？",
            "a": "否。高出血风险（≥3）提示需积极纠正可逆因素（控制血压、稳定 INR、停用不必要抗血小板/NSAID、限酒），而非停用抗凝；停用后卒中风险上升更快。"
        }
    ]
}

after = len(data)
assert after == 5022, f"keys after = {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"OK: cardiology/calc-2 已替换为真实 CHA₂DS₂-VASc 内容；键数守恒 {before}->{after}")
