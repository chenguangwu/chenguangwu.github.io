import json, os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

assert "food-testing/rater-risk" in data, "rater-risk key missing"
before = len(data)
assert before == 5022, f"keys before = {before}"

# rater-risk 是 allergen-cross-risk 的孤儿重复占位键（无 rater-risk.html，真实页由 food-testing/allergen-cross-risk 注入）。
# 保键(5022)、替换为真实过敏原交叉污染风险评分内容。
data["food-testing/rater-risk"] = {
    "title": "过敏原交叉污染风险评分",
    "scenarios": [
        "共线生产过敏原管控：评估同一产线先后生产不同致敏原产品时的交叉污染风险。",
        "清洁验证与切换评估：量化清洗后残留风险，决定是否需加强清洁或延长间隔。",
        "标签「可能含有」判定：依风险等级给出是否标注致敏提示的合规建议。"
    ],
    "examples": [
        {
            "title": "评分规则",
            "body": "8 项因子（过敏原类型/设备共用/清洁验证/切换间隔/形态/添加量/空气传播/包装隔离）各 0–5 分，满分 40；≤8 低风险、≤16 中低风险、≤24 中风险、>24 高风险。"
        },
        {
            "title": "算例",
            "body": "共用设备4+清洁验证3+切换2+形态3+添加量2+空气1+包装1+类型2 = 18 分 → 中风险，建议加强清洁验证与切换间隔，评估标注「可能含有」。"
        }
    ],
    "faqs": [
        {"q": "何时标「可能含有」？", "a": "当共线且无法完全排除微量交叉污染（中风险以上）时，依法规建议标注致敏提示。"},
        {"q": "设备专用最稳妥？", "a": "是。高致敏原（花生/坚果/乳/蛋）专用线或末道生产可降至低风险，避免交叉。"}
    ]
}

after = len(data)
assert after == 5022, f"keys after = {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"OK: food-testing/rater-risk 已替换为真实过敏原交叉污染风险内容；键数守恒 {before}->{after}")
