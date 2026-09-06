# -*- coding: utf-8 -*-
"""beneficiation 分类 content_deepdive 真实化（1 工具：尾矿品位/流失/利用分析）。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")


def main():
    data = json.load(open(JSON_PATH, encoding="utf-8"))
    key = "beneficiation/analysis-grade"

    data[key] = {
        "title": "尾矿（品位/流失/利用）分析",
        "scenarios": [
            "选矿厂做金属平衡：已知原矿处理量与原矿品位、精矿产量与精矿品位，反算尾矿品位并核对是否超出设计尾矿指标。",
            "评估资源流失：通过尾矿中有用组分品位与尾矿产率，计算随尾矿带走的金属量与流失率，判断回收率是否达标。",
            "尾矿再选与综合利用：根据尾矿剩余有用矿物品位、伴生元素含量，判断是否具有再选价值或可用于制砖、充填等综合利用。"
        ],
        "examples": [
            {
                "title": "示例：铜矿金属平衡与尾矿品位",
                "body": "原矿处理量 10000 t、原矿品位 1.0% → 原矿含铜 100 t；精矿产量 200 t、精矿品位 20% → 精矿含铜 40 t。\n尾矿含铜 = 100 − 40 = 60 t；尾矿产率 = 1 − 200/10000 = 98%。\n尾矿品位 = 60 ÷ (10000 − 200) × 100% = 0.612%。\n回收率 = (100 − 60) ÷ 100 × 100% = 40%（此例精矿产量偏低，回收率不经济，需复核选别作业）。"
            }
        ],
        "faqs": [
            {
                "q": "尾矿品位和回收率是什么关系？",
                "a": "回收率 =（原矿金属量 − 尾矿金属量）÷ 原矿金属量 × 100%。在固定原矿品位与处理量下，尾矿品位越低，尾矿带走的金属越少，回收率越高。选矿厂通常以「提高回收率、降低尾矿品位」为核心考核指标。"
            },
            {
                "q": "尾矿有利用价值吗？",
                "a": "要看剩余有用矿物与伴生元素品位。若尾矿中仍有较高品位的金属或有价元素，可再选回收；含铁、硅、钙的尾矿也常作为水泥掺合料、制砖原料或井下充填骨料实现综合利用，既减量又增值。"
            }
        ]
    }

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("beneficiation content realified: 1 entry")


if __name__ == "__main__":
    main()
