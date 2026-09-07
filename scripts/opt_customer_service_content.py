#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 content_deepdive 中 customer-service 3 key（第二十二种占位变体）。

占位特征：summary 原 None；scenarios 为
  「在customer-service场景下，先把<Title>标准化，再批量执行可追溯流程。」
  「适合做统一复核点输出，减少重复确认成本。」
  「边界样本建议单独标注，避免按默认规则误判。」
faqs 仅 2 条（缺第 3 条真实 FAQ）；example 已用 body 字段（渲染正确，仅替换文案）。

真实化：summary + 3 scenarios + 1 example(body) + 3 faqs，覆盖话术抽取 / 响应时长解决率
统计 / CSAT 汇总等真实客服场景；统一补「数据仅在本地浏览器处理、不上传，统计仅供参考」
隐私与统计免责（不覆盖 title）。幂等：仅当 summary is None 且 scenarios[0] 含占位短语时改写。
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

PLACEHOLDER = "在customer-service场景下，先把"

REAL = {
    "customer-service/random-script": {
        "summary": "面向客服团队的标准话术模板随机抽取器，用于岗前演练、班前抽查与话术轮换，纯前端运行、不采集客户数据。",
        "scenarios": [
            "岗前话术演练：从标准话术库随机抽取若干条，模拟客户提问做一对多对练，快速熟悉应答口径。",
            "班前会抽查：主管随机抽话术核验坐席熟练度，对薄弱项即时补训，降低上线差错。",
            "话术 A/B 轮换：避免机械重复同一套话术引起客户疲劳，按场景轮换提升沟通自然度。",
        ],
        "examples": [
            {"title": "催付话术对练示例", "body": "从「售后催付」话术库随机抽 5 条，生成对练清单：① 先确认订单状态再提醒② 说明逾期影响③ 给出支付方式④ 留复核入口⑤ 礼貌收尾；坐席逐条模拟应答并自评。"},
        ],
        "faqs": [
            {"q": "为何要生成可复核输出？", "a": "抽取记录可回溯，便于培训质检与交接，发现话术偏差并加快问题定位。"},
            {"q": "对新成员交接友好吗？", "a": "可直接沿用模板逐项核对，降低上手门槛，缩短岗前培训周期。"},
            {"q": "随机抽取会泄露客户数据吗？", "a": "不会。仅从本地话术库抽取，不采集任何客户信息，符合隐私合规要求。"},
        ],
    },
    "customer-service/stats-time-response": {
        "summary": "客服平均响应时间与一次解决率（FCR）统计工具，支持均值、中位数、P90 与分组对比，纯前端处理、数据不出本地。",
        "scenarios": [
            "响应时长趋势：录入每通会话的首响时长与解决时长，汇总均值、中位数与 P90，观察日/周波动。",
            "一次解决率（FCR）：按「是否一次解决」标记，统计一次解决占比，衡量一次到位能力。",
            "团队/个人对比：分组汇总响应时长与解决率，定位响应慢或返工多的短板坐席。",
        ],
        "examples": [
            {"title": "周响应统计示例", "body": "录入 20 条会话的首响与解决时长，得团队平均首响 38 秒、P90 72 秒、平均解决 4.2 分钟、FCR 86%；其中 3 条超时集中在午高峰，建议增援排班。"},
        ],
        "faqs": [
            {"q": "数据要上传服务器吗？", "a": "不需要。所有录入仅在浏览器本地处理，不上传，保护客户与运营数据隐私。"},
            {"q": "样本很少时统计可信吗？", "a": "样本少于 30 条时均值易波动，建议仅作参考并注明统计口径与周期。"},
            {"q": "中位数和均值哪个更准？", "a": "响应时长多为长尾分布，中位数与 P90 比均值更稳，不易被个别极端值拉偏。"},
        ],
    },
    "customer-service/summary-rater-csat": {
        "summary": "客户满意度（CSAT）评分汇总工具，支持平均分、满意度占比与低分归因，纯前端、数据不出浏览器。",
        "scenarios": [
            "单次活动 CSAT：录入 1–5 分问卷，算平均分与「4–5 分」满意度占比，评估本次体验。",
            "多渠道对比：按电话、在线、邮件分组汇总 CSAT，定位渠道体验差异。",
            "低分归因：筛选 ≤2 分样本，归纳共性痛点，驱动流程改进。",
        ],
        "examples": [
            {"title": "活动满意度汇总示例", "body": "120 份问卷平均分 4.3，CSAT（4–5 分）占比 82%，低分 9 份集中于「等待时长」；导出低分样本做归因，推动排队策略优化。"},
        ],
        "faqs": [
            {"q": "CSAT 和 NPS 有什么区别？", "a": "CSAT 衡量单次体验满意度，NPS 衡量推荐意愿；本工具聚焦 CSAT 汇总，不替代 NPS 调研。"},
            {"q": "评分要上传吗？", "a": "不需要。评分仅在本地浏览器处理，不上传服务器，保障调研数据隐私。"},
            {"q": "低分样本怎么用？", "a": "导出低分样本做归因分析，定位共性痛点，形成可执行的流程改进项。"},
        ],
    },
}


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    done, skip, ph = 0, 0, 0
    for key, real in REAL.items():
        if key not in d:
            print("  SKIP 未找到 key:", key)
            skip += 1
            continue
        v = d[key]
        if v.get("summary") is not None and not (v.get("scenarios") and PLACEHOLDER in v["scenarios"][0]):
            print("  SKIP 已真实化:", key)
            skip += 1
            continue
        # 占位残留检测（写前）
        blob = " ".join(v.get("scenarios", []))
        if PLACEHOLDER in blob:
            ph += 1
        v["summary"] = real["summary"]
        v["scenarios"] = real["scenarios"]
        v["examples"] = real["examples"]
        v["faqs"] = real["faqs"]
        d[key] = v
        done += 1
        print("  真实化:", key)
    json.dump(d, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("完成：真实化 %d | 跳过 %d | 命中占位 %d" % (done, skip, ph))


if __name__ == "__main__":
    main()
