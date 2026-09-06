#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_community_content.py — 真实化 community 分类 3 个工具的 content_deepdive 条目。

背景：community 3 工具页（analysis-74 竞争分析 / analysis-cost-9 成本体系 / stats-13 预售统计）
原 content_deepdive 3 key 为**第十六种占位变体**（「在community场景下，先把 XX 标准化，再批量执行
可追溯流程。适合做统一复核点输出，减少重复确认成本。边界样本建议单独标注…」，summary 原 None、
scenarios/examples/faqs 偏通用流程描述）。formula-desc 仅 analysis-cost-9 为财务变体占位（由
opt_community_hardcode.py 清），另 2 页已是真实数学文本。本脚本补真实 deep-dive。

字段结构（与 cnc/detector-23 模板一致）：
  title(str) / summary(str) / scenarios(list[3×str]) / examples(list[1×{title,body}]) / faqs(list[3×{q,a}])

原则：
  - 真实社区运营/竞品分析/成本拆解/预售统计场景，去伪科学、非决策/非财务/非战略确诊免责。
  - 不覆盖 title（标题已是真实工具名）。
  - 仅改写缺失/占位 key；已真实 key 跳过（幂等）。
  - indent=1, ensure_ascii=False。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

DATA = {
    "community/analysis-74": {
        "title": "竞争（分析/应对/差异化）",
        "summary": "竞品分析工具用结构化象限与对标维度，把功能、价格、渠道、口碑等维度量化，辅助定位差异化卖点与竞争应对优先级。",
        "scenarios": [
            "竞品对标：把候选竞品按关键维度打分，生成象限图识别自身定位与空白区。",
            "差异化梳理：对比功能重叠与缺口，明确可主打的差异化卖点。",
            "应对优先级：按威胁度与可攻性排序竞争动作，把资源分配到高杠杆项。",
        ],
        "examples": [
            {
                "title": "象限定位",
                "body": "取 5 个竞品在「价格」「功能丰富度」两轴打分（1–5），自身落在高价低功能象限则建议补功能或调价；落在低价高功能则强化性价比叙事，输出象限与建议动作。",
            }
        ],
        "faqs": [
            {"q": "维度怎么选才客观？", "a": "选用户决策真正关心的 4–6 个维度（价格/功能/服务/口碑/渠道），尽量用可验证数据打分，避免主观拍脑袋导致象限失真。"},
            {"q": "竞品少时象限还有用吗？", "a": "有用但样本少时结论脆弱，建议仅作方向参考并补充定性调研，不宜据此做重大决务决策。"},
            {"q": "结果能直接用于战略吗？", "a": "不能。它给出的是结构化对标视图，最终策略仍需结合资源、时机与一手调研，本工具仅辅助梳理。"},
        ],
    },
    "community/analysis-cost-9": {
        "title": "成本（控制/优化/分析）体系",
        "summary": "成本分析工具按固定/变动、单位/总、历史/预算等口径拆解成本结构，定位可控项与优化空间，辅助降本优先级排序。",
        "scenarios": [
            "成本结构拆解：把总成本按物料、人工、费用等口径归集，看占比与变动趋势。",
            "降本优先级：按金额与可控性排序优化项，先动高金额高可控项。",
            "预算对照：实际与预算偏差归因，识别超支环节。",
        ],
        "examples": [
            {
                "title": "单位成本与偏差",
                "body": "月产量 1 万、总成本 40 万，单位成本 40 元；预算单位 38 元，偏差 +2 元（+5.3%）；其中物料占 60% 且价格波动大，列为首要优化项，测算单价降 3% 可省约 0.72 万/月。",
            }
        ],
        "faqs": [
            {"q": "固定成本和变动成本怎么分？", "a": "固定成本不随产量变（租金/折旧），变动成本随产量线性变（物料/计件人工），先分清楚才能正确算单位成本与盈亏平衡点。"},
            {"q": "降本只看金额大的吗？", "a": "金额大但不可控（如合规刚性支出）优先度低，应优先「金额大且可控」项，并结合实施难度综合排序。"},
            {"q": "结果能当财务决策依据吗？", "a": "不能。本工具做结构梳理与估算，正式预算与税务以财务制度与最新法规为准，结果仅供参考。"},
        ],
    },
    "community/stats-13": {
        "title": "预售（发布/接龙/统计）工具",
        "summary": "预售/接龙统计工具聚合报名人数、付款状态与时段分布，实时输出参与结构与转化漏斗，辅助活动节奏与库存预备。",
        "scenarios": [
            "报名聚合：按渠道、时段汇总报名与付款，看转化与峰值。",
            "转化漏斗：未付、已付、已取消分层，定位流失环节。",
            "库存预备：按确认量预估备货与发车，降低超卖或积压。",
        ],
        "examples": [
            {
                "title": "转化与备货",
                "body": "发布后报名 800、已付 560、取消 40，支付转化率 70%；按已付 560 加 10% 缓冲预备 616 份，结合时段峰值（晚 8–10 点占 45%）安排客服与发货节奏。",
            }
        ],
        "faqs": [
            {"q": "转化率多少算正常？", "a": "不同品类差异大，预售常见 50%–80%，受价格、紧迫感、信任影响，单点仅作相对参考。"},
            {"q": "为什么出现大量未付款？", "a": "多为占坑未决或支付中断，可通过限时优惠、提醒与简化支付降低；本工具仅统计，不代为催收。"},
            {"q": "数据能用于正式财报吗？", "a": "不能。统计为活动运营参考，正式财务以对账与系统数据为准，本工具结果仅供参考。"},
        ],
    },
}


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    changed, skipped = [], []
    for key, val in DATA.items():
        if key not in data:
            print("WARN 缺失 key(跳过):", key)
            continue
        old = data[key]
        old_blob = " ".join(old.get("scenarios", [])) + " " + " ".join(
            x.get("title", "") for x in old.get("examples", [])) + " " + " ".join(
            x.get("q", "") for x in old.get("faqs", []))
        placeholder = ("在community场景下" in old_blob) or (old.get("summary") is None)
        if not placeholder:
            skipped.append(key)
            continue
        # 字段完整性校验
        assert set(val.keys()) == {"title", "summary", "scenarios", "examples", "faqs"}, f"字段不符: {key}"
        assert len(val["scenarios"]) == 3, f"scenarios 应为3: {key}"
        assert len(val["examples"]) == 1 and set(val["examples"][0].keys()) == {"title", "body"}, f"examples 结构: {key}"
        assert len(val["faqs"]) == 3 and all(set(x.keys()) == {"q", "a"} for x in val["faqs"]), f"faqs 结构: {key}"
        # 仅覆盖占位字段，保留 title
        data[key] = {
            "title": old.get("title", val["title"]),
            "summary": val["summary"],
            "scenarios": val["scenarios"],
            "examples": val["examples"],
            "faqs": val["faqs"],
        }
        changed.append(key)
    json.dump(data, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"真实化 key: {len(changed)}，跳过(已真实): {len(skipped)}")
    for k in changed:
        print("  +", k)
    if skipped:
        for k in skipped:
            print("  = (已真实,跳过)", k)
    return 0


if __name__ == "__main__":
    sys.exit(main())
