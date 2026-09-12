#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
science 分类旗舰计算器「使用指南」生成器（批次 D · 指南精选）。

- 数据驱动：每个 slug 的标题/简介/章节/FAQ/相关工具写在 CONTENT 字典里。
- 模板严格对齐现有 guides/physics-calculator-guide.html（head 元信息 + JSON-LD
  Article/BreadcrumbList/FAQPage + 内联 CSS + breadcrumb/h1/lead/章节/相关工具/FAQ/back）。
- sitemap 由 _build.py 自动扫描 guides/，新增 .html 会被收录，无需手工登记。
- 用法：
    python3 scripts/gen_science_guides.py --dry-run
    python3 scripts/gen_science_guides.py --apply
仅生成中文版（与现有 15 篇 science 指南一致，未生成 .en.html）。
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, "guides")
DATE = "2026-09-12"
SITE = "https://chenguangwu.github.io"

CONTENT = {
    "newtons-second": {
        "title": "牛顿第二定律计算器",
        "desc": "牛顿第二定律 F=ma 使用指南：输入质量与加速度，求合外力。",
        "lead": "根据牛顿第二定律 F = m·a，输入物体的质量 m 与加速度 a，即可求得合外力 F，适用于中学物理、工程受力与运动分析。",
        "sections": [
            ("公式与原理", "<p>牛顿第二定律：<strong>F = m·a</strong>，其中 m 为质量（kg），a 为加速度（m/s²），F 为合外力（N）。合外力方向与加速度方向一致。</p>"),
            ("使用步骤", "<ol><li>在「质量」输入物体的质量，单位为千克（kg）。</li><li>在「加速度」输入加速度，单位为米每二次方秒（m/s²）。</li><li>结果区自动显示合外力 F，单位为牛（N），保留 1 位小数。</li></ol>"),
            ("常见场景", "<ul><li>水平推箱子：已知推力产生的加速度求所需力。</li><li>自由落体：加速度取 g≈9.81 m/s²，F = m·g 即重力。</li><li>汽车加速：由质量与加速度估算发动机牵引力。</li></ul>"),
            ("注意事项", "<p>务必使用<strong>国际单位制</strong>：质量用 kg 而非 g（差 1000 倍），加速度为负表示减速（方向与运动方向相反）。</p>"),
        ],
        "faqs": [
            ("质量用克可以吗？", "不可以。需先换算为 kg（1 kg = 1000 g），否则结果会差 1000 倍。"),
            ("加速度为负表示什么？", "表示减速，即加速度方向与物体运动方向相反。"),
        ],
        "related": ["kinetic-energy", "pendulum-period", "physics-calculator"],
    },
    "kinetic-energy": {
        "title": "动能计算器",
        "desc": "动能 E=½mv² 使用指南：输入质量与速度求物体动能。",
        "lead": "动能 E_k = ½mv²，输入质量 m（kg）与速度 v（m/s），求得物体动能（J），适用于运动、碰撞与能量分析。",
        "sections": [
            ("公式与原理", "<p>动能：<strong>E_k = ½·m·v²</strong>，m 为质量（kg），v 为速度（m/s），E_k 单位焦耳（J）。</p>"),
            ("使用步骤", "<ol><li>输入质量（kg）。</li><li>输入速度（m/s）。</li><li>结果区显示动能 E_k，保留 1 位小数。</li></ol>"),
            ("常见场景", "<ul><li>车辆碰撞能量估算。</li><li>抛体运动出手动能。</li><li>风机/水轮机可用能量评估。</li></ul>"),
            ("注意事项", "<p>速度为<strong>平方项</strong>：速度翻倍，动能变为 4 倍；速度单位必须用 m/s（km/h 需 ÷3.6 换算）。</p>"),
        ],
        "faqs": [
            ("速度单位必须是 m/s 吗？", "是。若手头是 km/h，先除以 3.6 得到 m/s 再输入。"),
            ("为什么速度影响这么大？", "因为动能与速度平方成正比，速度小幅增加会显著放大能量。"),
        ],
        "related": ["newtons-second", "physics-calculator"],
    },
    "pendulum-period": {
        "title": "单摆周期计算器",
        "desc": "单摆周期 T=2π√(L/g) 使用指南：输入摆长求周期。",
        "lead": "小角度近似下 T = 2π√(L/g)，输入摆长 L（m）与重力加速度 g（默认 9.81 m/s²），求得单摆周期 T（s）。",
        "sections": [
            ("公式与原理", "<p>单摆周期：<strong>T = 2π·√(L/g)</strong>，L 为摆长（m），g 为重力加速度（m/s²），T 单位秒（s）。</p>"),
            ("使用步骤", "<ol><li>输入摆长 L（悬点到摆球中心的距离，单位 m）。</li><li>重力加速度 g 默认 9.81，月球等场景可改。</li><li>结果区显示周期 T，保留 3 位小数。</li></ol>"),
            ("常见场景", "<ul><li>机械钟摆设计。</li><li>物理实验测重力加速度（反解 g = 4π²L/T²）。</li></ul>"),
            ("注意事项", "<p>公式仅在<strong>小角度（≈&lt;15°）</strong>近似成立；周期与摆球质量无关，只取决于摆长与 g。</p>"),
        ],
        "faqs": [
            ("摆球质量影响周期吗？", "不影响。理想单摆周期与质量无关。"),
            ("大角度为什么不准？", "大角度时回复力不再是线性近似，周期会略长于公式值。"),
        ],
        "related": ["physics-calculator", "newtons-second"],
    },
    "ohms-law-calculator": {
        "title": "欧姆定律计算器",
        "desc": "欧姆定律 V=IR 使用指南：已知任意两量求第三量及功率。",
        "lead": "欧姆定律 V = I·R，选择求解量（电压 / 电流 / 电阻），填入已知两量，自动求解并给出功率 P=VI、电导等派生量。",
        "sections": [
            ("公式与原理", "<p>欧姆定律：<strong>V = I·R</strong>（电压 = 电流 × 电阻）。派生量：功率 P = V·I，电导 G = 1/R。</p>"),
            ("使用步骤", "<ol><li>选择要解的未知量（电压 / 电流 / 电阻）单选。</li><li>填入另外两个已知量。</li><li>结果区显示求解量、功率、电导与电荷量。</li></ol>"),
            ("常见场景", "<ul><li>电路设计选型。</li><li>家电电流估算（已知电压与电阻求电流）。</li></ul>"),
            ("注意事项", "<p>求解电阻时电流不能为 0（否则除零）；电阻单位默认 Ω，注意 kΩ/MΩ 换算。</p>"),
        ],
        "faqs": [
            ("选错求解量怎么办？", "切换单选按钮并重新填入已知两量即可。"),
            ("功率有什么用？", "功率 P=VI 用于判断元器件发热与额定功率是否匹配。"),
        ],
        "related": ["physics-calculator"],
    },
    "molar-mass-calculator": {
        "title": "摩尔质量计算器",
        "desc": "化学式摩尔质量计算指南：输入分子式求摩尔质量。",
        "lead": "输入化学式（如 H₂O、C₆H₁₂O₆），自动解析元素组成并求和原子量，输出摩尔质量（g/mol）与逐元素明细。",
        "sections": [
            ("使用方法", "<p>在输入框填写<strong>标准化学式</strong>，元素符号首字母大写、下标用普通数字（如 H2O、CaCO3）。</p>"),
            ("示例", "<ul><li>H₂O：1.008×2 + 16.00 = <strong>18.016 g/mol</strong>。</li><li>NaCl：22.99 + 35.45 = 58.44 g/mol。</li><li>C₆H₁₂O₆：180.16 g/mol。</li></ul>"),
            ("常见场景", "<ul><li>配制溶液换算质量与物质的量。</li><li>化学计量比计算。</li></ul>"),
            ("注意事项", "<p>元素符号<strong>大小写敏感</strong>（Co 是钴，CO 是一氧化碳）；无法识别的元素会提示错误。</p>"),
        ],
        "faqs": [
            ("怎么输入下标？", "直接写数字即可，如 H2O、Fe2O3，无需特殊上标。"),
            ("括号怎么写？", "支持圆括号与倍数，如 Ca(OH)2。"),
        ],
        "related": ["ph-calculator", "chemistry-calculator"],
    },
    "ph-calculator": {
        "title": "pH 计算器",
        "desc": "pH 与氢离子浓度换算指南：pH、[H⁺]、[OH⁻]、pOH 互算。",
        "lead": "在 pH、[H⁺]、[OH⁻]、pOH 四种模式间换算：pH = -log₁₀[H⁺]，范围 0–14，并给出酸碱性质判断。",
        "sections": [
            ("公式与原理", "<p>pH = -log₁₀[H⁺]；pOH = 14 − pH；[H⁺] = 10⁻ᵖᴴ；[OH⁻] = 10⁻ᵖᴼᴴ。pH 限定在 0–14。</p>"),
            ("使用步骤", "<ol><li>选择输入模式（pH / [H⁺] / [OH⁻] / pOH）。</li><li>填入对应数值。</li><li>结果区显示其余三种量及酸碱性。</li></ol>"),
            ("常见场景", "<ul><li>溶液酸碱度评估。</li><li>滴定终点判断。</li></ul>"),
            ("注意事项", "<p>pH=7 在 25℃ 为中性；温度不同中性 pH 会偏移。</p>"),
        ],
        "faqs": [
            ("pH=7 一定是中性吗？", "在 25℃ 下是；温度变化会改变中性点的 pH。"),
            ("[H⁺] 单位是什么？", "mol/L（摩尔每升）。"),
        ],
        "related": ["molar-mass-calculator", "chemistry-calculator"],
    },
    "z-score-calculator": {
        "title": "Z 分数（标准分数）计算器",
        "desc": "Z 分数 Z=(x−μ)/σ 使用指南：标准化数据与异常检测。",
        "lead": "标准分数 Z = (x−μ)/σ，将原始值标准化为以标准差为单位的偏离度，并给出 P(X&lt;x) 等概率。",
        "sections": [
            ("公式与原理", "<p>Z = (x − μ) / σ，x 为观测值，μ 为总体均值，σ 为总体标准差。Z 表示 x 偏离均值多少个标准差。</p>"),
            ("使用步骤", "<ol><li>输入观测值 x。</li><li>输入总体均值 μ 与标准差 σ（σ &gt; 0）。</li><li>结果区显示 Z 值、偏差、P(X&lt;x) 与 P(X&gt;x) 概率。</li></ol>"),
            ("结果解读", "<ul><li>|Z| ≤ 1：接近均值（正常）。</li><li>1 &lt; |Z| ≤ 2：偏离 1–2 个标准差。</li><li>2 &lt; |Z| ≤ 3：异常值（罕见）。</li><li>|Z| &gt; 3：高度异常（3σ 之外）。</li></ul>"),
            ("常见场景", "<ul><li>成绩标准化比较。</li><li>统计异常检测。</li></ul>"),
        ],
        "faqs": [
            ("Z=0 表示什么？", "表示观测值恰好等于均值。"),
            ("标准差能为 0 吗？", "不能，σ 必须为正数，否则公式无意义。"),
        ],
        "related": ["mean-calculator", "statistics"],
    },
    "mean-calculator": {
        "title": "平均数计算器",
        "desc": "算术/几何/调和平均数计算指南：一组数据多口径平均。",
        "lead": "输入一组数据（逗号分隔），同时计算算术平均、几何平均、调和平均，以及总和与数据个数。",
        "sections": [
            ("公式与原理", "<p>算术平均 x̄ = Σx / n；几何平均 = (∏x)^(1/n)；调和平均 = n / Σ(1/x)。几何与调和要求数据为正。</p>"),
            ("使用步骤", "<ol><li>在文本框输入数据，用逗号或空格分隔（如 1, 2, 4）。</li><li>结果区显示三种均值、总和 Σ 与个数 n。</li></ol>"),
            ("常见场景", "<ul><li>成绩、指标的平均水平。</li><li>速率平均优先用调和平均。</li></ul>"),
            ("注意事项", "<p>几何平均与调和平均仅对<strong>正数</strong>有意义；含非正数时只给出算术平均。</p>"),
        ],
        "faqs": [
            ("几何与调和平均有什么区别？", "调和平均适合速率类平均（如往返速度），几何平均适合比例/增长率。"),
            ("数据用什么分隔？", "逗号或空格均可，工具会自动解析。"),
        ],
        "related": ["median-calculator", "z-score-calculator"],
    },
}


def render(slug: str, c: dict) -> str:
    sections_html = "\n".join(f"<h2>{h}</h2>\n{b}" for h, b in c["sections"])
    faq_html = "\n".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in c["faqs"])
    related_html = "\n".join(
        f'<a class="tool-chip" href="{SITE}/tools/science/{r}.html">{r}</a>' for r in c["related"]
    )
    faq_json = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in c["faqs"]
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": c["title"],
         "description": c["desc"], "author": {"@type": "Organization", "name": "ToolBox"},
         "datePublished": DATE, "dateModified": DATE,
         "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/guides/{slug}-guide.html"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ToolBox", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "使用指南", "item": f"{SITE}/guides/index.html"},
            {"@type": "ListItem", "position": 3, "name": c["title"], "item": f"{SITE}/guides/{slug}-guide.html"}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_json},
    ]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{c['title']} - ToolBox</title>
<meta name="description" content="{c['desc']}">
<meta property="og:title" content="{c['title']}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{SITE}/guides/{slug}-guide.html">
<meta property="og:description" content="{c['desc']}">
<meta name="twitter:title" content="{c['title']}">
<meta name="twitter:description" content="{c['desc']}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}/guides/{slug}-guide.html">
<script type="application/ld+json">{json.dumps(ld[0], ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld[1], ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld[2], ensure_ascii=False)}</script>
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;margin-right:6px;}}
.breadcrumb a:hover{{text-decoration:underline;}}
main{{max-width:820px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;margin:0 0 8px;}}
.lead{{font-size:16px;color:var(--muted);margin:0 0 22px;}}
h2{{font-size:20px;margin:28px 0 10px;color:var(--primary);}}
.toc{{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin:18px 0;}}
.toc ul{{margin:0;padding-left:20px;}}
.toc a{{color:var(--text);text-decoration:none;}}
.toc a:hover{{color:var(--primary);}}
ul,ol{{padding-left:22px;}}
li{{margin:8px 0;}}
.related{{margin-top:26px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.related h3{{margin:0 0 10px;font-size:16px;color:var(--text);}}
.tool-chip{{display:inline-block;margin:4px 6px 4px 0;padding:6px 12px;border:1px solid var(--border);border-radius:999px;color:var(--primary);text-decoration:none;font-size:14px;}}
.tool-chip:hover{{background:var(--primary);color:#fff;}}
.faq{{margin-top:26px;}}
.faq dt{{font-weight:700;margin-top:14px;}}
.faq dd{{margin:4px 0 0;color:var(--muted);}}
.back{{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.back a{{color:var(--primary);font-weight:700;text-decoration:none;}}
</style>
<script src="/js/analytics.js" defer></script>
<link rel="stylesheet" href="../css/site-chrome.css">
<link rel="stylesheet" href="../css/common.css">
<script src="/js/i18n.js" defer></script>
<script src="../js/common.js" defer></script>
<meta name="title-zh" content="{c['title']} - ToolBox">
</head>
<body>
<nav class="breadcrumb"><a href="{SITE}/">ToolBox</a> / <a href="{SITE}/guides/index.html">使用指南</a> / <span>{c['title']}</span></nav>
<main>
<h1>{c['title']}</h1>
<p class="lead">{c['lead']}</p>
{sections_html}
<div class="related">
<h3>相关工具</h3>
{related_html}
</div>
<dl class="faq">
{faq_html}
</dl>
<div class="back"><a href="{SITE}/tools/science/{slug}.html">→ 打开 {c['title']} 工具</a></div>
</main>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="写入 guides/；缺省为 dry-run")
    args = ap.parse_args()
    os.makedirs(GUIDES_DIR, exist_ok=True)
    created, skip = [], []
    for slug, c in CONTENT.items():
        out = os.path.join(GUIDES_DIR, f"{slug}-guide.html")
        if os.path.exists(out):
            skip.append(slug)
            continue
        html = render(slug, c)
        if args.apply:
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            created.append(slug)
        else:
            created.append(slug + " (dry)")
    print(f"待生成/已生成: {len(created)} | 跳过(已存在): {len(skip)}")
    for s in created:
        print("  +", s)
    for s in skip:
        print("  =", s, "(已存在，跳过)")


if __name__ == "__main__":
    main()
