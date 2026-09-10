import json, os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

assert "beauty/self-assess-1" in data, "self-assess-1 key missing"
before = len(data)
assert before == 5022, f"keys before = {before}"

# self-assess-1 是 skin-tewl 的孤儿重复占位键（无 self-assess-1.html，真实页 skin-tewl.html 由 beauty/skin-tewl 注入）。
# 保键(5022)、替换为真实 TEWL 自评内容（同域）。
data["beauty/self-assess-1"] = {
    "title": "皮肤水分流失（TEWL）自评问卷",
    "scenarios": [
        "换季泛红脱皮，想评估屏障是否受损。",
        "刷酸后监测经皮失水判断恢复情况。",
        "护肤研发做用户屏障状态分层。"
    ],
    "examples": [
        {
            "title": "TEWL 分级算例",
            "body": "经皮失水率正常 < 10 g/(m²·h)，轻度受损 10–20，重度 > 20。问卷按紧绷、脱屑、刺痛频次计分映射到区间：设刺痛周 4 次、脱屑明显，映射 TEWL ≈ 18 g/(m²·h)，提示轻度受损需修护屏障（神经酰胺、停酸）。"
        }
    ],
    "faqs": [
        {"q": "TEWL 高就是干性皮肤吗？", "a": "不一定。TEWL 高表示屏障锁水差，可能外油内干；干性是皮脂少，二者机制不同但都需保湿修护。"},
        {"q": "怎么降低 TEWL？", "a": "补充神经酰胺/胆固醇修复砖墙结构、避免过度清洁与刷酸、用封闭剂（凡士林）减少蒸发；环境加湿也有助。"}
    ]
}

after = len(data)
assert after == 5022, f"keys after = {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"OK: beauty/self-assess-1 已替换为真实 TEWL 自评内容；键数守恒 {before}->{after}")
