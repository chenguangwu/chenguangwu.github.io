#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""interior 分类 1 工具 deep-dive 真实化：替换弱泛化模板（无六型词但无真实算例）。
范式对齐前述 apply 脚本。detector-28 为室内环保(材料/标准/检测)控制，基于 GB 50325 限值构造真实算例。
用法：--dry 仅校验；默认 --apply 写入 JSON。
"""
import json, re, sys

PATH = "i18n/tools/content_deepdive.json"

DATA = {
    "interior/detector-28": {
        "title": "室内环保控制（材料/标准/检测判定）",
        "scenarios": [
            "装修选材时，按 GB 50325 限值预判板材、油漆、胶粘剂、地板的污染物是否达标。",
            "完工后对照检测结果判断是否超标，决定通风时长或治理方案。",
        ],
        "examples": [
            {"title": "甲醛释放量判定（I 类民用建筑限值 0.08）", "body": "板材 0.05、油漆 0.06、胶粘剂 0.08、地板 0.07 mg/m³，对照 I 类限值 0.08：胶粘剂恰好达标(=0.08)，其余均低于限值，整体判定合格但胶粘剂余量最小需重点关注。"},
            {"title": "TVOC 与分级", "body": "若测得当量浓度 0.50 mg/m³（I 类 TVOC 限值），达限即临界；>0.50 判超标，建议延长通风或活性炭/新风治理后复测。"},
        ],
        "faqs": [
            {"q": "0.08 是什么限值？", "a": "指 GB 50325 中 I 类民用建筑甲醛浓度限量 0.08 mg/m³（II 类为 0.10）。选材检测值应低于对应类别限值才有余量。"},
            {"q": "达标了为什么还建议通风？", "a": "多种材料叠加会使室内综合浓度升高；单材料达标不代表房间整体达标，入住前仍建议通风并复测综合值。"},
        ],
    },
}

def main():
    apply = "--apply" in sys.argv
    d = json.load(open(PATH, encoding="utf-8"))
    fp = re.compile(r"统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板")
    weak = re.compile(r"先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|乘以 10%|两档复算|先用一组可复现输入|同一输入样本测试默认和边界情况")
    changed = 0
    for k, v in DATA.items():
        if k not in d:
            print("  SKIP 缺失:", k); continue
        d[k] = v
        changed += 1
    if apply:
        json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("APPLIED 写入 %d 条" % changed)
    else:
        print("DRY 拟写 %d 条" % changed)
    hit = [k for k in DATA if k in d and (fp.search(json.dumps(d[k], ensure_ascii=False)) or weak.search(json.dumps(d[k], ensure_ascii=False)))]
    print("泛化/弱模板残留:", hit if hit else "无(全清零)")

if __name__ == "__main__":
    main()
