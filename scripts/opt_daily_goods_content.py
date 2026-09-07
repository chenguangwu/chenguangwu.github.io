#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 content_deepdive 中 daily-goods 唯一 key parking-fee（第十九种占位变体）。

占位特征：summary 原 None；scenarios 为
  「在daily-goods场景下先确认停车费计算器口径与边界，再输出可复核结论。」
  「适用于流程复用、异常复核、版本变更对照。」
  「建议同步输入来源与处理假设，降低追溯成本。」
faqs 仅 2 条（缺第 3 条真实 FAQ）；example 已用 body 字段（渲染正确，仅替换文案）。

真实化：summary + 3 scenarios + 1 example(body) + 3 faqs，覆盖商场/路边按时计费封顶、
医院机场分段封顶、时段差异分段求和等真实停车费估算场景；统一补「结果仅供参考、以现场
公示费率与收费终端为准」免责（不覆盖英文 title「Parking Fee Calculator」）。
幂等：仅当 summary is None 且 scenarios[0] 含占位短语时改写。
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

PLACEHOLDER = "在daily-goods场景下先确认"

REAL = {
    "daily-goods/parking-fee": {
        "summary": "停车费估算工具，支持商场、路边、医院等多场景的费率、免费时长、封顶价与时段加价，纯前端、数据不出浏览器。",
        "scenarios": [
            "商场/路边按时计费：填入小时费率、免费时长与停放时长，估算应缴并自动对比单日封顶价，避免离场时惊讶。",
            "医院/机场分段封顶：按日或按次封顶，仅对超出免费时长的部分计费，适合长时间停放的成本预判。",
            "时段差异核对：白天与夜间费率不同或首小时优惠时，按实际入场与离场时间分段求和，得到更接近现场的应缴额。",
        ],
        "examples": [
            {"title": "商场停车计费示例", "body": "商场首小时免费、之后 8 元/小时、单日封顶 40 元；停放 5 小时 → 计费时长 4 小时，4×8=32 元，未超封顶，应缴 32 元；若停放 8 小时 → 8×8=64 元>封顶，按 40 元计。"},
        ],
        "faqs": [
            {"q": "为什么要记录假设？", "a": "费率、免费时长与封顶规则是结果可追溯的关键，建议先核对场地方公示再输入。"},
            {"q": "结果可直接执行吗？", "a": "仅供参考。以现场实际收费终端与公示费率为准，离场前请再次核对。"},
            {"q": "封顶价怎么用？", "a": "超过封顶价后按封顶计；工具自动取「按时长计算的费用」与「封顶价」的较小值作为应缴额。"},
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
