#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 cardiology 硬编码套话：formula-desc 占位 + tool-intro 医学版套话。

- formula-desc：6 页（antiarrhythmic-class/calc-3/chads2-vasc/nyha-classification/rater-11/rater-risk-3）
  替换标准占位为真实医学说明（依据指南标准+原理+用途+数据不出浏览器）。
- tool-intro：21 页医学版套话（基于权威医学标准/支持多种临床参数/临床计算与评估辅助…）
  替换功能特点/使用场景 ul 为真实内容；使用场景取 content_deepdive scenarios 提炼。
- 跳过：rater-11/rater-risk-3（tool-intro 已真实，仅清 formula-desc）；calc-1/calc-3（无 tool-intro 块，calc-3 仅清 formula-desc）。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "cardiology")
JSON_PATH = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

# formula-desc 真实说明（按页）
FORMULA = {
    "antiarrhythmic-class": "本工具依据抗心律失常药 Vaughan-Williams 分类与电生理机制整理，按 I/II/III/IV 类归类药物并提示适用与禁忌；计算在浏览器本地完成，数据不上传，结果仅供参考，具体用药由心血管专科医生决定。",
    "calc-3": "本工具依据 TIMI 风险评分（STEMI 30 天死亡风险）项目逐项累加，给出危险分层与再灌注参考；计算在本地完成，数据不上传，结果仅供参考，治疗以指南与床旁评估为准。",
    "chads2-vasc": "本工具依据 CHA₂DS₂-VASc 评分逐项累加评估非瓣膜性房颤卒中风险，并提示结合 HAS-BLED 权衡出血；计算在本地完成，数据不上传，结果仅供参考，抗凝方案由医生决定。",
    "nyha-classification": "本工具依据 NYHA 心功能分级与 6 分钟步行距离评估心衰严重度与运动耐量；计算在本地完成，数据不上传，结果仅供参考，分级以临床评估为准。",
    "rater-11": "本工具依据 HAS-BLED 七维度评分评估房颤抗凝出血风险；评分在本地完成，数据不上传，结果仅供参考，高出血风险应纠正可逆因素而非盲目停抗凝。",
    "rater-risk-3": "本工具依据 GRACE 注册研究评分累加评估急性冠脉综合征缺血与死亡风险；评分在本地完成，数据不上传，结果仅供参考，侵入时机以指南为准。",
}

# tool-intro 待清理页（21 页，已排除 rater-11/rater-risk-3 真实、calc-1/calc-3 无块）
INTRO_PAGES = [
    "ambulatory-bp", "antiarrhythmic-class", "aortic-dissection", "aspirin-prevention",
    "cardiac-rehab-mets", "chads2-vasc", "ckd-epi", "convert-rehab", "coronary-calcium",
    "cpet-analysis", "echo-report", "grace-score", "has-bled", "holter-grading",
    "hypertension-jnc", "myocardial-bridge", "nt-probnp", "nyha-classification",
    "pericardial-effusion", "statin-dose", "timi-score",
]

FEAT_LI = [
    "依据国际/中国心血管指南与公开公式标准（ESC/ACC/AHA 等）逐项计算",
    "实时输出风险分层、关键截断值与分级",
    "输入数值可复核，过程透明可追溯",
    "数据本地处理，不上传服务器",
]


def scene_li(s: str) -> str:
    t = s.split("：")[0].split("(")[0].strip()
    if len(t) > 26:
        t = t[:26] + "…"
    return t


def main():
    dry = "--dry" in sys.argv
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        cd = json.load(f)

    changed = []

    # 1) formula-desc 清理
    for slug, text in FORMULA.items():
        fp = os.path.join(TOOLS_DIR, slug + ".html")
        if not os.path.exists(fp):
            print("  [formuladesc] 跳过(无页面):", slug)
            continue
        s = open(fp, encoding="utf-8").read()
        new, n = re.subn(r'(?s)<p class="formula-desc">.*?</p>',
                         '<p class="formula-desc">%s</p>' % text, s, count=1)
        if n == 0:
            print("  [formuladesc] 未匹配(可能已真实):", slug)
            continue
        if not dry:
            open(fp, "w", encoding="utf-8").write(new)
        changed.append("formuladesc:%s" % slug)

    # 2) tool-intro 清理
    for slug in INTRO_PAGES:
        key = "cardiology/" + slug
        fp = os.path.join(TOOLS_DIR, slug + ".html")
        if not os.path.exists(fp):
            print("  [intro] 跳过(无页面):", slug)
            continue
        s = open(fp, encoding="utf-8").read()
        if key not in cd:
            print("  [intro] 跳过(无 content_deepdive):", slug)
            continue
        scenes = cd[key].get("scenarios", [])[:3]
        scene_lis = "".join("<li>%s</li>" % scene_li(x) for x in scenes)
        feat_lis = "".join("<li>%s</li>" % x for x in FEAT_LI)

        new, nf = re.subn(r'(?s)<ul class="intro-features">.*?</ul>',
                          '<ul class="intro-features">%s</ul>' % feat_lis, s, count=1)
        new2, ns = re.subn(r'(?s)<ul class="intro-scenes">.*?</ul>',
                           '<ul class="intro-scenes">%s</ul>' % scene_lis, new, count=1)
        if nf == 0 or ns == 0:
            print("  [intro] 未完全匹配 features=%d scenes=%d:" % (nf, ns), slug)
            continue
        if not dry:
            open(fp, "w", encoding="utf-8").write(new2)
        changed.append("intro:%s" % slug)

    print("== %s 模式：改动 %d 处 ==" % ("DRY" if dry else "正式", len(changed)))
    for c in changed:
        print("  ", c)


if __name__ == "__main__":
    main()
