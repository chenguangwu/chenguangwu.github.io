#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 customer-service 3 页硬编码套话。

(A) FD 错配变体 2 页（formula-desc）：
    - stats-time-response：原「本工具用于单位与格式换算…」→ 统计工具真实描述
    - summary-rater-csat：原「本计算依据通用财务与货币规则…」→ CSAT 汇总真实描述
    random-script 的 FD 为生成器变体（与「话术抽取器」语义相符），保留不处理。
(B) opt 套话 0 页（「工作与生活中的相关计算与查询」未出现），无需处理。
(C) 块内 6 类通用套话 3 页全含：
    - 简介段尾「免费在线工具，纯前端处理，数据不上传，保护隐私安全。」删除
    - intro-features 4 项通用套话 → 真实功能特点
    - intro-scenes 4 项通用套话 → 真实使用场景
幂等：仅当旧串存在时替换；含 meta/JSON-LD 回灌检测。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "customer-service")

# (文件名, 真实简介前缀, 功能特点, 使用场景)
REAL = {
    "random-script": (
        "标准话术模板随机抽取器。",
        ["从标准话术库随机抽取，支持按场景筛选", "一键生成对练清单，便于岗前演练",
         "结果可复制导出，方便培训质检留痕", "纯前端运行，不采集客户数据"],
        ["岗前话术演练与对练", "班前会坐席抽查补训", "话术 A/B 轮换降低客户疲劳", "新人培训交接与质检"],
    ),
    "stats-time-response": (
        "客服平均响应时间/解决率统计。",
        ["汇总首响与解决时长，输出均值/中位数/P90", "一键计算一次解决率（FCR）",
         "支持按团队/个人分组对比", "纯前端处理，数据不出本地"],
        ["日/周响应时长趋势观察", "一次解决率（FCR）考核", "团队与个人绩效短板定位", "排班增援决策参考"],
    ),
    "summary-rater-csat": (
        "客户满意度（CSAT）评分汇总。",
        ["录入 1–5 分问卷，算平均分与满意度占比", "按渠道分组对比 CSAT",
         "自动筛选低分样本做归因", "纯前端处理，评分不上传"],
        ["单次活动满意度评估", "电话/在线/邮件渠道对比", "低分样本归因与改进", "满意度报表快速生成"],
    ),
}

# FD 错配变体 → 真实描述（保留「工具名称：」尾）
FD_FIX = {
    "stats-time-response": (
        "本工具用于单位与格式换算，换算因子依据国际单位制(SI)及相关标准定义，结果保留输入精度；纯前端本地处理。",
        "本统计依据录入的每通会话时长与解决标记，汇总均值、中位数、P90 与一次解决率（FCR）；纯前端本地处理，数据不上传。",
    ),
    "summary-rater-csat": (
        "本计算依据通用财务与货币规则，具体以最新法规与当地政策为准，结果仅供参考。",
        "本汇总依据录入的 1–5 分满意度评分，计算平均分、满意度占比并筛选低分样本；纯前端本地处理，数据不上传。",
    ),
}

INTRO_TAIL = "免费在线工具，纯前端处理，数据不上传，保护隐私安全。"


def fix_block(s, fname):
    intro, feats, scenes = REAL[fname]
    # 简介段尾套话
    s = s.replace("<p>%s%s</p>" % (intro.rstrip("。"), INTRO_TAIL), "<p>%s</p>" % intro.rstrip("。"))
    # 也兜底：若简介段为「<真实简介>。免费在线工具…」形式（intro 已带句号）
    s = s.replace("<p>%s%s</p>" % (intro, INTRO_TAIL), "<p>%s</p>" % intro.rstrip("。"))
    # 功能特点列表
    new_feats = '<ul class="intro-features">\n' + "\n".join("      <li>%s</li>" % x for x in feats) + "\n    </ul>"
    s = re.sub(r'<ul class="intro-features">.*?</ul>', new_feats, s, flags=re.S)
    # 使用场景列表
    new_scenes = '<ul class="intro-scenes">\n' + "\n".join("      <li>%s</li>" % x for x in scenes) + "\n    </ul>"
    s = re.sub(r'<ul class="intro-scenes">.*?</ul>', new_scenes, s, flags=re.S)
    return s


def main():
    dry = "--dry" in sys.argv
    changed = []
    for fname in REAL:
        fp = os.path.join(TOOLS, fname + ".html")
        if not os.path.exists(fp):
            print("  SKIP 未找到:", fname)
            continue
        s = open(fp, encoding="utf-8").read()
        orig = s
        # (A) FD
        if fname in FD_FIX:
            old, new = FD_FIX[fname]
            if old in s:
                s = s.replace(old, new, 1)
            else:
                print("  [FD] 旧串未命中(可能已改):", fname)
        # (C) 块内
        s = fix_block(s, fname)
        if s != orig:
            changed.append(fname)
            if not dry:
                open(fp, "w", encoding="utf-8").write(s)
            print("  %s: %s" % (fname, "待写" if dry else "已改"))
        else:
            print("  %s: 无变化(可能已处理)" % fname)
    # 回灌检测
    print("\n=== 回灌检测 ===")
    junk = ["免费在线工具，纯前端处理，数据不上传，保护隐私安全。", "本工具用于单位与格式换算",
            "本计算依据通用财务与货币规则", "日常办公与学习", "开发调试与数据处理",
            "快速计算与格式转换", "信息查询与参考", "操作简单，一键完成"]
    for fname in REAL:
        fp = os.path.join(TOOLS, fname + ".html")
        s = open(fp, encoding="utf-8").read()
        hit = [j for j in junk if j in s]
        print("  %s 残留: %s" % (fname, hit if hit else "无"))


if __name__ == "__main__":
    main()
