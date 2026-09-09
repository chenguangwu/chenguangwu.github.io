#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge 分类 1 工具 deep-dive 真实化：替换弱泛化模板（无六型词但无真实内容）。
范式对齐前述 apply 脚本。assessor-27 为知识(审计/缺口/评估)工具，基于多维权重评分构造真实算例。
用法：--dry 仅校验；默认 --apply 写入 JSON。
"""
import json, re, sys

PATH = "i18n/tools/content_deepdive.json"

DATA = {
    "knowledge/assessor-27": {
        "title": "知识资产审计与缺口评估",
        "scenarios": [
            "对企业知识库按多维打分，定位薄弱项与缺口。",
            "做知识管理成熟度诊断，排整改优先级。",
        ],
        "examples": [
            {"title": "五维等权评估", "body": "维度(完整性/准确性/时效性/可获取性/安全性)得分 6/5/7/4/7，等权总分 = (6+5+7+4+7)/5 = 5.8 分(10 分制)；可获取性 4 分最低，优先补检索与权限。"},
            {"title": "加权评估", "body": "若权重(0.25/0.20/0.20/0.20/0.15)，加权 = 6×0.25+5×0.20+7×0.20+4×0.20+7×0.15 = 1.5+1.0+1.4+0.8+1.05 = 5.75 分。安全权重低时总分略降。"},
        ],
        "faqs": [
            {"q": "维度怎么选权重？", "a": "按业务痛点定：检索差是痛点则「可获取性」加权高；合规严则「安全性」加权高。权重即整改优先级信号。"},
        ],
    },
}

def main():
    apply = "--apply" in sys.argv
    d = json.load(open(PATH, encoding="utf-8"))
    fp = re.compile(r"统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板")
    weak = re.compile(r"先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|乘以 10%|两档复算|先用一组可复现输入|同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义")
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
