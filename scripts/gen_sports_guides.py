#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sports 分类旗舰计算器「使用指南」生成器（批次 D · 指南精选）。

- 数据驱动：每个 slug 的标题/简介/章节/FAQ/相关工具写在 CONTENT 字典里。
- 模板对齐现有 guides/physics-calculator-guide.html（head 元信息 + JSON-LD
  Article/BreadcrumbList/FAQPage + 内联 CSS + breadcrumb/h1/lead/章节/相关工具/FAQ/back）。
- sitemap 由 _build.py 自动扫描 guides/，新增 .html 会被收录，无需手工登记。
- 用法：
    python3 scripts/gen_sports_guides.py --dry-run
    python3 scripts/gen_sports_guides.py --apply
仅生成中文版（与 science 指南一致，未生成 .en.html）。
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, "guides")
DATE = "2026-09-12"
SITE = "https://chenguangwu.github.io"

CONTENT = {
    "estimate-tester": {
        "title": "最大摄氧量（VO2max）计算器",
        "desc": "VO2max 估算使用指南：通过 Cooper 12 分钟跑等测试估算最大摄氧量，评估有氧耐力。",
        "lead": "最大摄氧量 VO2max 反映心肺与耐力上限。输入 Cooper 12 分钟跑距离或 1.5 英里跑时间，按标准公式估算 VO2max（ml/kg/min），并给出体能等级。",
        "sections": [
            ("公式与原理", "<p>Cooper 12 分钟跑：<strong>VO2max = (距离m − 504.9) / 44.73</strong>；1.5 英里跑：VO2max = 483 / 时间(秒) + 3.5。结果单位 ml/kg/min，保留 1 位小数。</p>"),
            ("使用步骤", "<ol><li>选择测试方法（Cooper 12 分钟跑 / 1.5 英里跑）。</li><li>输入跑动距离或用时。</li><li>结果区显示 VO2max、年龄推算的最大心率与体能等级。</li></ol>"),
            ("体能等级参考", "<ul><li>男性：≥52 优秀 / 43–52 良好 / 35–43 一般 / &lt;35 偏低。</li><li>女性标准略低，请结合年龄与项目综合判断。</li></ul>"),
            ("注意事项", "<p>公式为<strong>经验估算</strong>，个体差异较大；高原、热环境与近期训练状态会影响实测值，结果仅供参考。</p>"),
        ],
        "faqs": [
            ("Cooper 测试怎么测最准？", "在平整跑道尽全力匀速跑 12 分钟，记录里程；测前充分热身，避免起跑过快。"),
            ("VO2max 能提升吗？", "能。持续有氧训练（尤其接近乳酸阈强度）可在数月内显著提升。"),
        ],
        "related": ["xuerusuanyuzhiceding", "calc-heart-rate-1", "tester-7"],
    },
    "tester-1": {
        "title": "自重动作 1RM（最大力量）推算器",
        "desc": "俯卧撑/引体向上 1RM 推算指南：输入体重与力竭次数，用 Epley/Brzycki 公式估算一次最大重复。",
        "lead": "通过力竭次数推算自重动作（俯卧撑/引体向上）的一次最大重复 1RM 与相对力量，辅助力量训练负荷设定。",
        "sections": [
            ("公式与原理", "<p>Epley：<strong>1RM = 负荷 × (1 + 次数/30)</strong>；Brzycki：1RM = 负荷 / (1.0278 − 0.0278×次数)。自重动作负荷 = 体重 × 自重比例（俯卧撑约 64%）或 体重+附加负重（引体向上）。</p>"),
            ("使用步骤", "<ol><li>选择动作类型（俯卧撑 / 引体向上）。</li><li>输入体重与可完成的力竭次数。</li><li>结果区显示 Epley、Brzycki 与均值 1RM 及相对力量（1RM/体重）。</li></ol>"),
            ("常见场景", "<ul><li>设定自重训练强度（如 70%–80% 1RM 用于增肌）。</li><li>追踪相对力量进步。</li></ul>"),
            ("注意事项", "<p>次数越多（&gt;15）推算精度越差；超过 15 次建议直接测试真实 1RM 或缩短次数。</p>"),
        ],
        "faqs": [
            ("力竭次数越多越准吗？", "不是。1RM 公式在低次数（1–10）更可靠，次数过高误差增大。"),
            ("相对力量有什么用？", "消除体重差异，便于不同体重者横向比较力量水平。"),
        ],
        "related": ["convert-47", "strength-5", "jixianwei-kuai-man-leixingtuice"],
    },
    "calc-heart-rate-1": {
        "title": "最大心率与训练心率区间计算器",
        "desc": "Karvonen 心率储备法指南：输入年龄与静息心率，计算最大心率与科学训练心率区间。",
        "lead": "基于 Karvonen 公式，输入年龄、静息心率并选择最大心率公式（Fox 220−年龄 / Tanaka 208−0.7×年龄），划分热身、燃脂、有氧、无氧与 VO2max 五档训练区间。",
        "sections": [
            ("公式与原理", "<p>最大心率 HRmax：Fox 法 <strong>220 − 年龄</strong>；Tanaka 法 208 − 0.7×年龄。心率储备法：目标心率 = (HRmax − 静息) × 强度% + 静息。</p>"),
            ("使用步骤", "<ol><li>选择最大心率公式。</li><li>输入年龄与静息心率（晨起静息最佳）。</li><li>结果区显示最大心率与五档强度区间（含 bpm 范围）。</li></ol>"),
            ("强度区间含义", "<ul><li>50%–60% 热身恢复；60%–70% 燃脂；70%–80% 有氧；80%–90% 无氧；90%–100% VO2max。</li></ul>"),
            ("注意事项", "<p>公式法为<strong>群体估计</strong>，个体实测最大心率可能偏差 ±10 bpm；用药（如 β 受体阻滞剂）会影响心率反应。</p>"),
        ],
        "faqs": [
            ("哪种最大心率公式更好？", "Tanaka 法对中老年人更准；Fox 法简单常用，年轻人误差小。"),
            ("静息心率怎么测？", "晨起未下床、安静状态下测 1 分钟脉搏，连续几天取平均更准。"),
        ],
        "related": ["heart-rate-2", "heart-rate-3", "estimate-tester"],
    },
    "calculator-calc-time": {
        "title": "马拉松配速计算器",
        "desc": "马拉松配速与分段指南：输入目标完赛时间或目标配速，计算每公里配速与分段用时。",
        "lead": "输入目标完赛时间（或目标配速），自动计算马拉松每公里配速、平均速度与各公里分段用时，辅助跑步训练与比赛配速策略。",
        "sections": [
            ("公式与原理", "<p>配速 = 完赛时间 / 距离（42.195 km）。分段用时 = 目标配速 × 分段距离；平均速度 = 距离 / 完赛时间。</p>"),
            ("使用步骤", "<ol><li>选择输入模式（目标时间 / 目标配速）。</li><li>填入对应数值。</li><li>结果区显示每公里配速、平均速度与各分段（5k/10k/半马/全马）用时。</li></ol>"),
            ("配速策略", "<ul><li>负分割（后程快于前程）通常比匀速更省力。</li><li>按海拔与天气微调目标配速。</li></ul>"),
            ("注意事项", "<p>配速单位常用 min/km；英制 min/mi 需换算（1 mi ≈ 1.609 km）。</p>"),
        ],
        "faqs": [
            ("配速和速度有什么区别？", "配速是每公里用时（越小越快），速度是单位时间距离（越大越快），互为倒数。"),
            ("新手目标配速怎么定？", "以近期 5k/10k 成绩推算，或按能轻松对话的强度作为有氧基础配速。"),
        ],
        "related": ["sports-calculator", "calc-61", "triathlon-transition"],
    },
    "swimming-stroke-efficiency": {
        "title": "游泳划水效率（SWOLF）计算器",
        "desc": "SWOLF 游泳效率指南：输入泳池长度、划水次数与用时，计算 SWOLF、DPS 与划频。",
        "lead": "SWOLF = 单趟时间(秒) + 划水次数，综合评估游泳技术经济性；同时给出每划距离 DPS 与划频 SR，越低/越优越高效。",
        "sections": [
            ("公式与原理", "<p><strong>SWOLF = 单趟时间(秒) + 划水次数</strong>；每划距离 DPS = 池长 / 划次；划频 SR = 划次 / 时间 × 60。25m 自由泳参考：&lt;35 精英 / 35–42 优秀 / 43–50 良好 / 51–60 中等 / 61–70 初级 / &gt;70 入门。</p>"),
            ("使用步骤", "<ol><li>选择泳姿与泳池长度。</li><li>输入单趟划水次数与用时。</li><li>结果区显示 SWOLF、DPS、SR 与效率等级。</li></ol>"),
            ("提升方向", "<ul><li>降低 SWOLF：减少划水次数（提升滑行性）同时保持速度。</li><li>提高 DPS：强化划水力与身体流线。</li></ul>"),
            ("注意事项", "<p>SWOLF 跨泳姿不可直接比较；同泳姿纵向对比才有意义。</p>"),
        ],
        "faqs": [
            ("SWOLF 越低越好吗？", "在同泳姿同池长下，越低代表技术经济性越高。"),
            ("划频越高越好吗？", "不是。过高划频往往伴随打滑，应追求 DPS 与 SR 的平衡。"),
        ],
        "related": ["youyonghuashuixiaolv-swolf", "time-30", "sports-stats"],
    },
    "calculator-calc-9": {
        "title": "骑行齿比计算器",
        "desc": "自行车齿比与速度指南：输入牙盘、飞轮齿数与轮径，计算齿比、行进距离与不同踏频速度。",
        "lead": "输入牙盘齿数、飞轮齿数与轮周长（或轮径），计算齿比、每圈行进距离（齿轮英寸）以及不同踏频对应的骑行速度，辅助公路与山地车选型调校。",
        "sections": [
            ("公式与原理", "<p>齿比 = 牙盘 / 飞轮；每圈行进距离 = 齿比 × 轮周长；齿轮英寸 = 齿比 × 轮径(英寸)；速度 = 每圈距离 × 踏频。</p>"),
            ("使用步骤", "<ol><li>输入牙盘、飞轮齿数与轮周长（或选预设轮径）。</li><li>输入目标踏频或目标速度。</li><li>结果区显示齿比、齿轮英寸与对应速度/踏频。</li></ol>"),
            ("选型建议", "<ul><li>大齿比适合平路冲刺；小齿比适合爬坡。</li><li>公路车常用 50/34 牙盘配 11–28t 飞轮。</li></ul>"),
            ("注意事项", "<p>轮周长需实测（轮胎充气后略有变化）；速度含滚阻与风阻近似，实测会略低。</p>"),
        ],
        "faqs": [
            ("齿比越大骑得越快吗？", "同踏频下齿比大速度快，但所需踩踏力也更大，爬坡会更吃力。"),
            ("踏频多少合适？", "休闲骑行 80–90 rpm，冲刺可更高；过高踏频低效，过低伤膝。"),
        ],
        "related": ["sports-calculator", "speed-5", "simulator-18"],
    },
    "estimate-35": {
        "title": "出汗率估算器",
        "desc": "出汗率估算指南：输入运动前后体重、时长、补液与排尿，估算出汗速率与脱水程度。",
        "lead": "通过称重法（运动前后体重差）估算出汗量与出汗速率，结合补液与排尿给出脱水百分比，用于耐力训练与比赛的科学补水策略。",
        "sections": [
            ("公式与原理", "<p>出汗量 = (运动前体重 − 运动后体重) + 补液量 − 排尿量；出汗率 = 出汗量 / 运动时长(小时)；脱水% = 体重差 / 运动前体重 × 100。</p>"),
            ("使用步骤", "<ol><li>记录运动前、后净重（排尿后、少量着装）。</li><li>输入运动时长、期间补液与排尿量。</li><li>结果区显示出汗率(L/h)、脱水百分比与补水建议。</li></ol>"),
            ("补水建议", "<ul><li>出汗率 &lt;1 L/h 轻；1–1.5 中；&gt;1.5 高。</li><li>训练中按出汗率的 80% 左右补液，赛后补足差额。</li></ul>"),
            ("注意事项", "<p>称重法需<strong>统一着装与排空膀胱</strong>；高温高湿环境下出汗率显著升高，需增加补液。</p>"),
        ],
        "faqs": [
            ("为什么要用称重法？", "它是估算出汗量最简便可靠的方法，比体感准确。"),
            ("脱水多少算危险？", "脱水 &gt;2% 体重即影响运动表现，&gt;4% 危险，需及时补液。"),
        ],
        "related": ["estimate-22", "dianjiezhi-diushi-buchong", "hongxibao-xieyang-shiyingxing"],
    },
    "xuerusuanyuzhiceding": {
        "title": "血乳酸阈值测定指南",
        "desc": "血乳酸阈值指南：依据逐级负荷测试的心率与血乳酸数据，估算乳酸阈值心率。",
        "lead": "通过逐级递增负荷测试记录心率与血乳酸，拟合曲线后在血乳酸 ≈ 4 mmol/L 处读取乳酸阈值心率，用于划分耐力训练强度区间。",
        "sections": [
            ("公式与原理", "<p>乳酸阈值（LT）是血乳酸开始非线性累积的拐点，常用 <strong>血乳酸 = 4 mmol/L</strong> 对应强度作为阈值；在逐级负荷曲线上该点的心率即乳酸阈心率。</p>"),
            ("使用步骤", "<ol><li>按递增负荷（如每级 3–4 分钟）记录心率与血乳酸。</li><li>输入各级数据。</li><li>结果区显示拟合曲线与乳酸阈心率。</li></ol>"),
            ("训练应用", "<ul><li>阈值强度是耐力训练的核心区间。</li><li>阈值心率以上为无氧/高强度区间。</li></ul>"),
            ("注意事项", "<p>需采血或佩戴无创乳酸设备；不同实验室阈值定义（2/4 mmol/L）略有差异，纵向对比应固定标准。</p>"),
        ],
        "faqs": [
            ("乳酸阈和通气阈一样吗？", "相关但不等同；通气阈是无创估算，乳酸阈更直接但需采血。"),
            ("多久测一次？", "训练周期关键节点（如周期初/中/末）测，观察阈值心率变化。"),
        ],
        "related": ["estimate-tester", "tongqibizhifenxi", "tester-7"],
    },
}


def render(slug: str, c: dict) -> str:
    sections_html = "\n".join(f"<h2>{h}</h2>\n{b}" for h, b in c["sections"])
    faq_html = "\n".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in c["faqs"])
    related_html = "\n".join(
        f'<a class="tool-chip" href="{SITE}/tools/sports/{r}.html">{r}</a>' for r in c["related"]
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
<div class="back"><a href="{SITE}/tools/sports/{slug}.html">→ 打开 {c['title']} 工具</a></div>
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
