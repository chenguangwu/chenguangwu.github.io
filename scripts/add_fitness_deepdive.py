#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 content_deepdive.json 的 fitness 段补 2 个缺失键（analysis-retention / assessor-64）。

保持该文件自定义格式（顶层键 1 空格缩进），用精确文本插入，不做 json.dump 重写。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "i18n/tools/content_deepdive.json")
ANCHOR = ' "fitness/angle-motion": {'

ENTRIES = [
    (
        "fitness/analysis-retention",
        {
            "title": "数据分析（会员/课程/留存）",
            "scenarios": [
                "汇总月度留存率、出勤率等一串指标，快速得出均值/中位数/极差，判断整体水平与波动幅度。",
                "对比不同门店或不同课程的会员留存数据，用中位数与标准差识别异常店与波动大的课程。",
                "季度复盘时把每天的新增/流失/留存数粘贴进来，一次性算出总量与离散程度，作为运营 KPI 复核依据。",
            ],
            "examples": [
                {
                    "title": "可复现算例：4 个月留存率统计",
                    "body": "输入「72,75,68,80」（单位 %）。\n数据量 n=4；总和 295.00；平均值 73.75；中位数 (72+75)/2=73.50；最小值 68；最大值 80；极差 12.00；方差 19.19；标准差 4.38。\n读法：均值 73.75% 与中位数 73.50% 接近，说明 4 个月留存水平稳定；标准差 4.38 个百分点属正常波动，无需对单月下滑过度反应。\n若某月跌到 68 而其余三个月在 72–80，则极差被拉大、均值被拉低，应优先排查该月课程或教练变动。",
                }
            ],
            "faqs": [
                {
                    "q": "方差/标准差用总体还是样本口径？",
                    "a": "本工具用总体口径（除以 n），因为粘贴进来的这组数据就是你要分析的全部指标。样本口径（除以 n−1）会略大，用于由样本推断总体，两者数值接近时结论一致。",
                },
                {
                    "q": "为什么均值和中位数都要看？",
                    "a": "均值受极端值影响大，中位数不易被极端值带偏。两者接近说明数据分布均匀；均值明显低于中位数说明存在偏低异常月，需定位具体原因。",
                },
            ],
        },
    ),
    (
        "fitness/assessor-64",
        {
            "title": "质量（评估/优化/提升）机制",
            "scenarios": [
                "瑜伽馆或工作室做季度课程质量体检：从师资、课程内容、教学环境、学员效果四个维度打分，得出可对比的综合分与等级。",
                "教练自评或在评课时定位短板：任意维度低于 7 分即判「待提升」并自动列出改进项，避免只盯总分而忽略结构性问题。",
                "环境合规复核：室温、湿度、班级人数、人均面积四项按阈值判定 ✓/✗，作为场馆择址或排课的硬性依据。",
            ],
            "examples": [
                {
                    "title": "可复现算例：一节团体课的质量评估",
                    "body": "输入：认证 RYT200-500（cert=8）、从业年限 3 年；课程内容三项 7/6/8；环境室温 30°C、湿度 55%、班级 20 人、场地 60m²；学员效果 满意度 80、留存 70、续费 60、进度 65。\n师资力量=0.6×8+min(3/10,1)×4=6.0；课程内容=(7+6+8)/3=7.0；\n教学环境：室温 30°C 不达标(5)、湿度 55% 达标(10)、人数 20>15 不达标(6)、人均面积 60/20=3.0 达标(10) → 5×0.3+10×0.2+6×0.25+10×0.25=7.5；\n学员效果=(80×0.3+70×0.3+60×0.2+65×0.2)/10=7.0；\n综合评分=6.0×0.25+7.0×0.25+7.5×0.20+7.0×0.30=6.85 → 显示 6.8/10，等级「良好（B级）」，薄弱项为师资力量(6.0)与室温超标。\n对照高效班：cert=10、年限 6、课程 9/8/9、室温 24°C、湿度 50%、10 人、60m²、效果 90/80/75/85 → 综合 8.8/10，等级「卓越（S级）」。",
                }
            ],
            "faqs": [
                {
                    "q": "四个维度的权重为什么是 25/25/20/30？",
                    "a": "学员效果权重最高（30%），因为课程最终要落到留存与满意度；师资与课程内容各 25% 是质量的直接来源；教学环境 20%，是必要条件但相对可改造。权重可在评估口径调整时按同一比例替换。",
                },
                {
                    "q": "为什么 6.85 显示成 6.8？",
                    "a": "页面用 toFixed(1) 保留一位小数，而 6.85 在二进制浮点中略小于 6.85，故进位后显示 6.8。这是四舍五入的边界表现，不影响等级判定（6.0≤6.85<7.5 为良好 B 级）。",
                },
            ],
        },
    ),
]


def dump_entry(key, obj) -> str:
    """按文件既有缩进（键 1 空格、字段 2 空格、数组项 3、内层对象 4…）生成文本。"""
    out = [' "%s": {' % key]
    out.append('  "title": %s,' % json.dumps(obj["title"], ensure_ascii=False))
    out.append('  "scenarios": [')
    for i, s in enumerate(obj["scenarios"]):
        out.append('   %s%s' % (json.dumps(s, ensure_ascii=False), ',' if i < len(obj["scenarios"]) - 1 else ''))
    out.append('  ],')
    out.append('  "examples": [')
    for i, e in enumerate(obj["examples"]):
        out.append('   {')
        out.append('    "title": %s,' % json.dumps(e["title"], ensure_ascii=False))
        out.append('    "body": %s' % json.dumps(e["body"], ensure_ascii=False))
        out.append('   }%s' % (',' if i < len(obj["examples"]) - 1 else ''))
    out.append('  ],')
    out.append('  "faqs": [')
    for i, f in enumerate(obj["faqs"]):
        out.append('   {')
        out.append('    "q": %s,' % json.dumps(f["q"], ensure_ascii=False))
        out.append('    "a": %s' % json.dumps(f["a"], ensure_ascii=False))
        out.append('   }%s' % (',' if i < len(obj["faqs"]) - 1 else ''))
    out.append('  ]')
    out.append(' },')
    return '\n'.join(out)


def main() -> int:
    apply = "--apply" in sys.argv
    raw = open(P, encoding="utf-8").read()
    data = json.loads(raw)
    missing = [k for k, _ in ENTRIES if k in data]
    if missing:
        print("已存在，跳过:", missing)

    block = "\n".join(dump_entry(k, v) for k, v in ENTRIES if k not in data)
    if not block:
        print("无需写入")
        return 0

    idx = raw.find(ANCHOR)
    if idx < 0:
        print("未找到锚点，终止")
        return 1
    new = raw[:idx] + block + "\n" + raw[idx:]

    # 必须可解析，且新增键内容一致
    chk = json.loads(new)
    for k, v in ENTRIES:
        assert chk.get(k) == v, "内容不一致: " + k
    print("新增键: %s | fitness 段旧键 %d -> 新键 %d | 非 fitness 段键数不变: %s" % (
        ", ".join(k for k, _ in ENTRIES if k not in data),
        len([k for k in data if k.startswith("fitness/")]),
        len([k for k in chk if k.startswith("fitness/")]),
        len([k for k in data if not k.startswith("fitness/")]) == len([k for k in chk if not k.startswith("fitness/")]),
    ))
    if apply:
        open(P, "w", encoding="utf-8").write(new)
        print("已落盘")
    else:
        print("预览（加 --apply 落盘）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
