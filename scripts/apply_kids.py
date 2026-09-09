#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kids 分类 5 工具 deep-dive 真实化：替换弱泛化模板（无六型词但无真实内容）。
范式对齐前述 apply 脚本：title/scenarios/examples/faqs 四字段覆盖，json.dump(indent=1) 保持仓库规范。
检测词（六型+弱模板）全规避。kids 为儿童教育练习类，基于真实使用场景写具体算例/步骤。
用法：--dry 仅校验；默认 --apply 写入 JSON。
"""
import json, re, sys

PATH = "i18n/tools/content_deepdive.json"

DATA = {
    "kids/focus-timer": {
        "title": "专注计时（番茄工作法）",
        "scenarios": [
            "用 25 分钟专注 + 5 分钟休息的节奏提升孩子专注力。",
            "写作业时分段计时，避免久坐疲劳。",
        ],
        "examples": [
            {"title": "3 个番茄钟安排", "body": "3 段专注各 25 分钟 = 75 分钟，中间休息 2 次各 5 分钟 = 10 分钟，合计 85 分钟；完成 3 段后做一次长休 15–30 分钟。"},
            {"title": "低龄缩短时长", "body": "低年级可用 15 分钟专注 + 3 分钟休息的简化节奏；每段结束起身活动，避免眼睛与坐姿疲劳。"},
        ],
        "faqs": [
            {"q": "为什么是 25 分钟？", "a": "番茄钟是经实践验证的注意力单位，约等于小学生单科作业舒适时长；过长易走神、过短难进入状态。"},
        ],
    },
    "kids/memory-palace": {
        "title": "记忆宫殿法（地点桩记忆）",
        "scenarios": [
            "把要记的内容挂到熟悉空间的固定位置，练联想记忆。",
            "背单词、记清单、备赛时用。",
        ],
        "examples": [
            {"title": "10 个购物项分 5 桩", "body": "选家里 5 个位置(门/沙发/桌/窗/床)，每桩挂 2 件：门口放「牛奶+鸡蛋」、沙发放「苹果+面包」… 按顺序游走回忆，10 项不易漏。"},
            {"title": "背 5 个英语词", "body": "把 apple/book/cat/dog/sun 分别「放」在 5 个房间桩，闭眼走一遍空间即复述，比死记硬背更牢。"},
        ],
        "faqs": [
            {"q": "桩怎么选？", "a": "用最熟的路径(回家动线)且顺序固定；桩要鲜明有反差，挂的意象越夸张越好记。桩数随内容增，10–20 桩常见。"},
        ],
    },
    "kids/mirror-letter": {
        "title": "镜像字辨析（b/d/p/q）",
        "scenarios": [
            "低龄儿童常把左右镜像字母写反，做对照练习。",
            "用基准线法区分易混字形。",
        ],
        "examples": [
            {"title": "b 与 d 怎么分", "body": "以竖线为身体基准：b 是「身子+肚子在右」(圈在右)，d 是「圈在左」；口诀「b 先竖再圈右、d 先圈左再竖」。"},
            {"title": "p 与 q 区分", "body": "p 圈在右、竖向下出头；q 圈在左、竖向下出头。对比 b(竖向上)/d(竖向上)，四者按「圈左右+竖上下」两维定位。"},
        ],
        "faqs": [
            {"q": "镜像字要纠正吗？", "a": "学龄前常见、多随发育缓解；若一年级后仍频繁反写，用描红+基准线+多感官(描沙)练习，避免贴负面标签。"},
        ],
    },
    "kids/multiplication-practice": {
        "title": "乘法口算练习",
        "scenarios": [
            "限定范围随机出题，计时练口算熟练度。",
            "统计正确率定位薄弱表。",
        ],
        "examples": [
            {"title": "2–9 表随机一题", "body": "范围内随机出 7×8，答对 56；连做 20 题计时，正确 18 题则正确率 90%，错在 6/7/8 段需补。"},
            {"title": "限定某数专项", "body": "只练 ×9：9×1…9×9，用「十位数减1、个位补到10」窍门(9×7=63：6=7−1、3=10−7)提速。"},
        ],
        "faqs": [
            {"q": "为什么限时？", "a": "限时逼出自动化反应，暴露「想」而非「背」的薄弱点；正确率比速度先抓，再逐步提速。"},
        ],
    },
    "kids/stroke-order": {
        "title": "汉字笔顺查询",
        "scenarios": [
            "查单字标准书写顺序，纠正常见倒笔。",
            "配合描红练规范书写。",
        ],
        "examples": [
            {"title": "「水」字笔顺", "body": "水(4 画)：竖钩 → 横撇 → 撇 → 捺(中间竖钩先，再左横撇、右撇、收捺)。常见错是把左撇放第一。"},
            {"title": "「火」字笔顺", "body": "火(4 画)：点 → 短撇 → 长撇 → 捺(先两点、再人字撇捺)。「先两边后中间」适用于火/小等。"},
        ],
        "faqs": [
            {"q": "笔顺有强制标准吗？", "a": "有《现代汉语通用字笔顺规范》；虽不影响认读，但影响书写速度与书法美感，考试书写也按规范。"},
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
