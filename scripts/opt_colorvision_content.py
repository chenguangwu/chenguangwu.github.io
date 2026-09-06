#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opt_colorvision_content.py — 为 colorvision 分类 4 个工具新建真实 content_deepdive 条目。

背景：colorvision 4 工具页（colorblind-simulator / cvd-safe-palette / farnsworth-d15-test
/ palette-cvd-checker）原 content_deepdive **0 key**（内容层全缺），formula-desc 已是真实
色觉科学文本（Machado 矩阵/OKLCH/CIE，无需清）。本脚本补真实 deep-dive。

字段结构（与 cnc/detector-23 模板一致）：
  title(str) / summary(str) / scenarios(list[3×str]) / examples(list[1×{title,body}]) / faqs(list[3×{q,a}])

原则：
  - 真实色觉缺陷科学（Machado 变换矩阵/OKLCH 感知均匀空间/D-15 色相分型/可辨识度量化），
    去伪科学、非临床确诊免责。
  - 不覆盖 title（标题已是真实工具名）。
  - 仅新建缺失 key；已存在 key 跳过（幂等）。
  - indent=1, ensure_ascii=False。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

DATA = {
    "colorvision/colorblind-simulator": {
        "title": "色盲模拟器",
        "summary": "色盲模拟器用 Machado 等（2009）提出的线性 RGB 变换矩阵，把正常视觉图像模拟为红、绿、蓝各型色觉缺陷下的观感，帮助设计师与开发者预判配色在色觉缺陷人群中的可读性。",
        "scenarios": [
            "设计自查：UI、图表、地图配色在红绿/蓝黄色盲视角下模拟，提前发现「靠色不可分」的问题。",
            "无障碍评审：对海报、仪表盘、教学图做色盲视角复核，满足 WCAG 对比与可辨识要求。",
            "科普演示：把同一图在各类色觉缺陷下并排展示，直观说明观感差异。",
        ],
        "examples": [
            {
                "title": "红绿色盲模拟",
                "body": "取图像线性光 RGB，按 Machado 红色盲（protan）严重度矩阵变换后回 gamma；若原图用红/绿编码两组数据，模拟后两色趋近黄棕、难以区分，提示改用蓝/橙或叠加形状编码。",
            }
        ],
        "faqs": [
            {"q": "模拟器能替代真实色觉检测吗？", "a": "不能。它展示的是近似观感，用于设计预判与科普，真实色觉评估需由眼科或专业色觉测试完成。"},
            {"q": "为什么同一红绿色盲不同人差异大？", "a": "色觉缺陷有程度之分（轻度/中度/重度），且红（protan）/绿（deutan）类型不同，矩阵严重度参数不同，模拟结果随之变化。"},
            {"q": "模拟矩阵的原理是什么？", "a": "主流用 Machado、Oliveira 与 Fernandes（2009）提出的按严重度插值的线性 RGB 变换，作用于线性光空间再回显，比简单去色更接近真实色觉偏移。"},
        ],
    },
    "colorvision/cvd-safe-palette": {
        "title": "色盲安全配色生成器",
        "summary": "色盲安全配色生成器在 OKLCH 等感知均匀色彩空间采样候选色，对每对颜色做色觉缺陷变换后检查可辨识度，输出在红绿/蓝黄/全色盲下仍可区分的调色板。",
        "scenarios": [
            "数据可视化配色：为图表、地图生成在色盲视角下仍两两可分的分类色板。",
            "品牌与 UI 规范：产出主色/辅助色组合，满足无障碍可辨识基线。",
            "教学/科研作图：避免红绿配对，改用蓝橙或加纹理与标注。",
        ],
        "examples": [
            {
                "title": "可辨识度校验",
                "body": "在 OKLCH 采样 6 色，逐对做 8 型色觉变换（红/绿用 Machado 矩阵、全色盲用去色）后比较；若某对变换后感知距离过小，剔除其一并补采，最终 6 色在各类色觉缺陷下最小感知距离均超阈值。",
            }
        ],
        "faqs": [
            {"q": "为什么用 OKLCH 而不是 RGB/HSL？", "a": "OKLCH 在感知上近似均匀，按它采样与比较距离更贴近「人眼觉得差多少」，避免 RGB/HSL 等距却观感不等的问题。"},
            {"q": "安全配色是否意味着颜色不好看？", "a": "不是。安全是指「在色觉缺陷下仍可区分」，仍可在 OKLCH 内按明度/色相约束挑选美观且对比充分的组合。"},
            {"q": "仅靠换颜色够吗？", "a": "关键区分建议「颜色+形状/纹理/标注」多重编码，单靠配色在重度缺陷下仍可能吃力，多重编码更稳妥。"},
        ],
    },
    "colorvision/farnsworth-d15-test": {
        "title": "Farnsworth D-15 色相排列测试",
        "summary": "Farnsworth D-15 用 15 个固定亮度的色帽，要求按色相顺序排列，通过错误连线的方向与数量评估色觉缺陷的类型与严重程度，常用于快速筛查与分型。",
        "scenarios": [
            "色觉筛查：将 15 色帽按色相环排列，记录跨轴错误（红绿轴、蓝黄轴）判型。",
            "培训/科普：演示正常色觉与各类缺陷者在排列路径上的典型错误模式。",
            "辅助评估：作为详细检测前的快速分类，指向需进一步正式测试的方向。",
        ],
        "examples": [
            {
                "title": "错误模式判型",
                "body": "正常排列呈连续色相环；若出现沿红-绿轴的跨位连线（如把红与绿相邻误排），提示红绿（protan/deutan）缺陷；沿蓝-黄轴跨位提示蓝黄（tritan）缺陷；错误数越多严重度越高。",
            }
        ],
        "faqs": [
            {"q": "D-15 能确诊色盲吗？", "a": "不能。它是快速筛查与分型工具，正式诊断需结合更全的色觉检测由专业机构作出。"},
            {"q": "蓝黄轴错误少见吗？", "a": "tritan（蓝黄）类型本身较少见，若出现蓝黄轴跨位连线应特别注意，必要时进一步评估。"},
            {"q": "排列受照明影响吗？", "a": "会。应在标准光源或自然日光下、避免偏色屏幕与环境光干扰，否则错误可能由照明而非色觉引起。"},
        ],
    },
    "colorvision/palette-cvd-checker": {
        "title": "调色板色觉可辨识度检查器",
        "summary": "调色板色觉可辨识度检查器对已有配色逐对做色觉缺陷变换，量化每对在红绿/蓝黄/全色盲下的感知距离，标出「可能混淆」的组合，辅助配色复审。",
        "scenarios": [
            "现有配色复审：导入调色板，逐对检查在各类色觉缺陷下的可区分性并高亮风险对。",
            "数据图表验收：核对分类色在色盲视角是否仍两两可分，避免图例误读。",
            "无障碍合规：为设计交付提供「色觉可辨识」复核依据，配合 WCAG 使用。",
        ],
        "examples": [
            {
                "title": "风险对标注",
                "body": "对 5 色板逐对做 Machado 矩阵（按严重度）与去色变换，比较变换后感知距离；红色 #E74C3C 与绿色 #27AE60 在某些绿缺陷下距离过小被标黄，建议把绿改为蓝青 #16A085 拉开可辨识度。",
            }
        ],
        "faqs": [
            {"q": "检查器给出的是绝对结论吗？", "a": "不是。它给出的是按变换模型的近似可辨识度提示，用于复审与改进，真实可读性仍建议在目标设备上由色觉缺陷用户实测。"},
            {"q": "全色盲（achromatopsia）怎么处理？", "a": "全色盲下去色后仅剩明度差异，检查器会提示「仅靠明度区分」的风险，建议同步用形状/纹理/文字编码。"},
            {"q": "严重度参数怎么选？", "a": "常用轻度到中度插值；若面向广泛人群，建议按中度（较严苛）评估，确保多数色觉缺陷用户仍可区分。"},
        ],
    },
}


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    added, skipped = [], []
    for key, val in DATA.items():
        if key in data:
            skipped.append(key)
            continue
        assert set(val.keys()) == {"title", "summary", "scenarios", "examples", "faqs"}, f"字段不符: {key}"
        assert len(val["scenarios"]) == 3, f"scenarios 应为3: {key}"
        assert len(val["examples"]) == 1 and set(val["examples"][0].keys()) == {"title", "body"}, f"examples 结构: {key}"
        assert len(val["faqs"]) == 3 and all(set(x.keys()) == {"q", "a"} for x in val["faqs"]), f"faqs 结构: {key}"
        data[key] = val
        added.append(key)
    json.dump(data, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"新增 key: {len(added)}，跳过(已存在): {len(skipped)}")
    for k in added:
        print("  +", k)
    if skipped:
        for k in skipped:
            print("  = (已存在,跳过)", k)
    return 0


if __name__ == "__main__":
    sys.exit(main())
