# -*- coding: utf-8 -*-
"""express 批（单工具 checker-6）：真实化内容层 + 清理英文套话 + cat 错标修正。

- content_deepdive.json : express/checker-6 整体替换（title+3 场景+1 算例+3 FAQ）
- _en_override.json / slug-en.json : 全 slug，更新 en / ed
- express.json : 裸 slug，更新 en-US.title/h1/intro
- tools/express/checker-6.html : h2 英文名、<p> 英文 fallback、cat=validator→calculator
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
EN_OVERRIDE = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
SLUG_EN = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')
EXPRESS = os.path.join(ROOT, 'i18n', 'tools', 'express.json')
HTML = os.path.join(ROOT, 'tools', 'express', 'checker-6.html')

FULL = "express/checker-6"
BARE = "checker-6"
EN_NAME = "Express QC Metrics"
ED_OVERRIDE = ("Compute express/courier quality-control rates — loss, delay, damage and "
               "complaint rates — against the YZ/T 0168 standard, then grade service A–E. "
               "Browser-only, no data uploaded.")
EN_INTRO = ("Enter total parcels handled plus lost, delayed, damaged and complained counts to "
            "compute express quality-control rates against YZ/T 0168 and get a service grade (A–E). "
            "Runs entirely in your browser.")

CONTENT_ENTRY = {
    "title": "品控（操作/质量/检查）流程",
    "scenarios": [
        "快递网点在月度考核时录入总处理量与丢失/延误/损毁/申诉件数，自动算四项品控率并对照 YZ/T 0168 限值判定达标与否。",
        "服务质量改进复盘时，对比不同周期（月/季/年）品控等级变化，定位持续超标的环节重点整改。",
        "对内审或监管检查，一键生成品控报告（含标准限值、实测值与 A–E 等级），作为合规留痕材料。",
    ],
    "examples": [
        {
            "title": "品控报告示例",
            "body": "总处理量 10 万件、丢失 3 件、延误 20 件、损毁 15 件、有效申诉 1 件、满意度 96%：丢失率 0.003%、延误率 0.02%、损毁率 0.015%、有效申诉率 1 件/百万，四项均达标，综合等级「良好（B级）」。",
        }
    ],
    "faqs": [
        {
            "q": "标准限值从哪来？",
            "a": "丢失率≤0.01%、延误率≤0.05%、损毁率≤0.03%、有效申诉率≤2 件/百万，依据 YZ/T 0168《快递服务》国家标准；满意度≥95% 用于区分 A/B 级。正式考核请以最新标准文本为准。",
        },
        {
            "q": "等级怎么判？",
            "a": "四项指标全达标且满意度≥95% 为优秀（A级），全达标为良好（B级），达标 3 项为合格（C级），2 项为基本合格（D级），少于 2 项为不合格（E级）。",
        },
    ],
}

HTML_EDITS = [
    (
        '<meta name="toolbox" content="cat=validator,industry=express,icon=🔧,bg=#eceff1">',
        '<meta name="toolbox" content="cat=calculator,industry=express,icon=🔧,bg=#eceff1">',
    ),
    (
        '<h2 data-zh="🔧 品控（操作/质量/检查）流程">🔧 Checker 6</h2>',
        '<h2 data-zh="🔧 品控（操作/质量/检查）流程">🔧 Express QC Metrics</h2>',
    ),
    (
        '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="快递服务质量品控指标计算，输入业务数据自动计算丢失率/延误率/损毁率/申诉率，对照YZ/T 0168标准判定等级">Checker 6 - check and validate online, free.</p>',
        '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="快递服务质量品控指标计算，输入业务数据自动计算丢失率/延误率/损毁率/申诉率，对照YZ/T 0168标准判定等级">Express QC Metrics computes courier quality-control rates against the YZ/T 0168 standard and grades service A–E, entirely in your browser with no data uploaded.</p>',
    ),
]


def load(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump(p, obj):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    # content_deepdive
    cd = load(CONTENT)
    if FULL not in cd:
        raise SystemExit("缺少 content_deepdive 键: " + FULL)
    cd[FULL] = CONTENT_ENTRY
    dump(CONTENT, cd)

    # i18n
    en = load(EN_OVERRIDE)
    sl = load(SLUG_EN)
    ex = load(EXPRESS)
    if FULL not in en:
        raise SystemExit("缺少 _en_override 键: " + FULL)
    if FULL not in sl:
        raise SystemExit("缺少 slug-en 键: " + FULL)
    if BARE not in ex:
        raise SystemExit("缺少 express.json 键: " + BARE)
    en[FULL]["en"] = EN_NAME
    en[FULL]["ed"] = ED_OVERRIDE
    sl[FULL]["en"] = EN_NAME
    sl[FULL]["ed"] = EN_INTRO
    ex[BARE]["en-US"]["title"] = EN_NAME
    ex[BARE]["en-US"]["h1"] = EN_NAME
    ex[BARE]["en-US"]["intro"] = EN_INTRO
    dump(EN_OVERRIDE, en)
    dump(SLUG_EN, sl)
    dump(EXPRESS, ex)

    # html
    with open(HTML, 'r', encoding='utf-8') as f:
        s = f.read()
    for old, new in HTML_EDITS:
        assert old in s, "未找到待替换串: " + old[:40]
        s = s.replace(old, new, 1)
    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(s)

    print("express/checker-6 真实化完成（content + i18n + html）")


if __name__ == '__main__':
    main()
