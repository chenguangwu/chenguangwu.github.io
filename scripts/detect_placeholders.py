#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detect_placeholders.py — deep-dive 占位指纹通用检测（覆盖多套占位模板风格）

用法:
  python3 scripts/detect_placeholders.py                 # 全量扫描，输出每分类占位计数与汇总
  python3 scripts/detect_placeholders.py --cat text      # 仅扫描指定分类
  python3 scripts/detect_placeholders.py --self-test     # 指纹自检（占位样例应被命中、真内容样例应不命中）

退出码:
  0 = 未发现任何占位指纹（或 --self-test 通过）
  1 = 发现占位指纹（用于门禁/核验）

说明:
  deep-dive 占位存在多套模板风格，全部为"元话术"占位（谈论工具/口径/模板/
  复用/标准化本身，而非具体业务）。本脚本枚举各风格的*不变量短语*进行命中计数，
  命中即判定为占位。真内容（工具特异性、含具体数值/单位/领域概念）不应命中。
"""
import json
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

# ── 六型占位指纹（快速复核 / 统一输入单位与口径 / …）──
SIX = [
    "快速复核",
    "统一输入单位与口径",
    "先做基准算例",
    "快速核对和教学演示",
    "边界场景核验",
    "新版本口径切换",
    "值跳变或异常偏差",
    "常见场景：",
]

# ── 通用模板占位（text/pet/security/…）："当你在X相关场景中需要基于…进行快速计算或校验" ──
GEN = [
    "进行快速计算或校验时，可先用该工具生成一版标准结果",
    "可用固定样本快速复现实验流程，验证参数选择是否正确",
    "用于将人工操作转为可复用步骤",
    "快速形成操作 SOP",
    "只要数据可映射到本工具支持的参数结构",
    "结果可信度如何保证",
    "按业务口径补充必要字段",
]

# ── STY3 家族占位（口径/模板/复用/标准化 元话术，多子变体）──
# 仅收录占位专有的强指纹，避免与真内容（如"先统一目标画幅"）误判
STY3 = [
    # urban/startup/packaging/media/steel 变体
    "标准化后再执行对比，避免口径重复换算导致的偏差",
    "模板化内容能降低每次录入时的遗漏风险",
    "避免重复定义业务口径",
    "为什么该工具要保留复用模板？",
    # office/writing 变体
    "标准化后再执行批量分析，便于统一口径",
    "为什么要记录假设？",
    "口径和假设是结果可追溯的关键",
    "口径与边界，再输出可复核结论",
    # martial/legal2/accessibility/seismology/yi 变体
    "口径，再做结果验证，避免跨版本口径漂移",
    "跨版本口径漂移",
    "结果出现波动时该如何处理？",
    "先确认是否为口径变更，再核对输入边界",
    "若确属规则变化，及时同步新假设",
    # project 变体
    "口径，再做分层输出，适合连续复用",
    "如何避免重复劳动？",
    "固定模板输入和字段映射后，可复用输出结构",
    # yi/steel 变体
    "口径后再批量输出",
    # 通用复用/复核元话术（占位 FAQ 专有）
    "为何要生成可复核输出？",
    "复核记录能帮助发现规则偏差",
    "该工具的复用边界？",
    "适用可结构化输入的场景，边界情况建议加入人工复核",
]

ALL = {"SIX": SIX, "GEN": GEN, "STY3": STY3}


def hits(blob):
    out = {}
    for name, phrases in ALL.items():
        c = sum(1 for p in phrases if p in blob)
        if c:
            out[name] = c
    return out


def load_dd():
    with open(DD, encoding="utf-8") as f:
        return json.load(f)


def scan(cat=None):
    d = load_dd()
    cats = {}
    if cat:
        cats[cat] = [k for k in d if k.startswith(cat + "/")]
    else:
        from collections import defaultdict
        tmp = defaultdict(list)
        for k in d:
            c = k.split("/")[0]
            tmp[c].append(k)
        cats = dict(tmp)
    report = {}
    for c, ks in sorted(cats.items()):
        blob = " ".join(json.dumps(d[k], ensure_ascii=False) for k in ks)
        h = hits(blob)
        report[c] = (len(ks), h)
    return report


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return
    cat = None
    if "--cat" in args:
        i = args.index("--cat")
        cat = args[i + 1]
    rep = scan(cat)
    total = 0
    for c, (n, h) in rep.items():
        if h:
            total += 1
            print(f"  {c:18s} keys={n:4d} 占位={h}")
    print(f"→ 命中占位分类数: {total} / {len(rep)}")
    if cat:
        # 单分类模式：若 cat 有命中则 exit 1
        sys.exit(1 if rep.get(cat, (0, {}))[1] else 0)
    sys.exit(1 if total else 0)


def self_test():
    placeholder = {
        "title": "X",
        "scenarios": [
            "当你在text相关场景中需要基于“X”进行快速计算或校验时，可先用该工具生成一版标准结果。",
            "在office场景里，优先把X标准化后再执行批量分析，便于统一口径。",
            "先统一X口径，再做结果验证，避免跨版本口径漂移。",
        ],
        "examples": [{"title": "标准化使用示例", "body": "以一组典型输入为例：先按业务口径补充必要字段，快速形成操作 SOP。"}],
        "faqs": [
            {"q": "为什么要记录假设？", "a": "口径和假设是结果可追溯的关键。"},
            {"q": "结果出现波动时该如何处理？", "a": "先确认是否为口径变更，再核对输入边界。"},
        ],
    }
    real = {
        "title": "字数统计",
        "scenarios": [
            "长文投稿前，统计中文字符、英文单词与总字符数，确认是否超出平台字数上限。",
        ],
        "examples": [{"title": "示例", "body": "输入 500 个汉字与 200 个英文单词，中文字数 500、词数 200、总字符约 900。"}],
        "faqs": [
            {"q": "标点符号算字数吗？", "a": "默认计入总字符，可在设置中切换是否排除标点。"},
        ],
    }
    pb = json.dumps(placeholder, ensure_ascii=False)
    rb = json.dumps(real, ensure_ascii=False)
    ph = hits(pb)
    rh = hits(rb)
    print("占位样例命中:", ph, "→ 期望非空")
    print("真内容样例命中:", rh, "→ 期望空")
    ok = bool(ph) and not rh
    print("SELF-TEST:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
