#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legal 分类「使用指南」生成器（收口批次 E，2→54）。

数据驱动（不手写文案，全部取自已有真实数据源，避免套话）：
  - 标题 / 简介：i18n/tools/legal.json 的 zh-CN.title / intro
  - 公式与依据：scripts/fix_legal_formula_map.py 的 MAP（已逐条对照页面实现撰写）
  - 场景 / 示例 / FAQ：i18n/tools/content_deepdive.json 的 scenarios / examples / faqs
  - 使用步骤：由页面 <input>/<select> 的中文标签与 id 自动生成

模板对齐 scripts/gen_statistics_guides.py（head 元信息 + JSON-LD
Article/BreadcrumbList/FAQPage + 内联 CSS + breadcrumb/h1/lead/章节/相关工具/FAQ/back）。

克制原则：纯展示 / 低专业度的工具（日历、万年历、法律查询 hub、法律计算器 hub）不生成指南。

用法：
    python3 scripts/gen_legal_guides.py            # dry-run
    python3 scripts/gen_legal_guides.py --apply    # 写入 guides/ 并追加 guides.json
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

GUIDES_DIR = os.path.join(ROOT, "guides")
TOOLS_DIR = os.path.join(ROOT, "tools", "legal")
IND = "legal"
DATE = "2026-09-13"
SITE = "https://chenguangwu.github.io"

# 纯展示 / 低专业度，不生成指南
EXCLUDE = {"calendar-qr", "calendar", "legal-reference", "legal-calculator"}

# 跨行业重名 slug：calc-8 与 agriculture/calc-8（土壤pH）冲突，需消歧文件名，
# 否则会覆盖 agriculture 的正确指南；正文以 tools/legal/calc-8.html 绝对 URL 让
# _build.py 的 GUIDE_MAP_IND 精确命中 legal，不影响 agriculture。
FILE_OVERRIDE = {"calc-8": "legal-calc-8-guide.html"}

from fix_legal_formula_map import MAP as FORMULA_MAP  # noqa: E402


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def input_labels(slug):
    """提取页面 input/select 的中文标签与 id，用于生成使用步骤。"""
    src = open(os.path.join(TOOLS_DIR, slug + ".html"), encoding="utf-8").read()
    pairs = []
    for m in re.finditer(
        r'<(?:label|div|span)[^>]*>\s*([^<>]{1,40}?)\s*<[^>]*>\s*<(?:input|select)\b[^>]*\bid="([^"]+)"',
        src,
    ):
        label = m.group(1).strip()
        if label and (m.group(2), label) not in pairs:
            pairs.append((m.group(2), label))
    return pairs


def build_content():
    gis = load_json(os.path.join(ROOT, "i18n", "tools", "legal.json"))
    deep = load_json(os.path.join(ROOT, "i18n", "tools", "content_deepdive.json"))
    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS_DIR, "*.html"))
        if os.path.basename(f) != "index.html" and os.path.basename(f)[:-5] not in EXCLUDE
    )
    out = {}
    for i, slug in enumerate(slugs):
        zh = gis.get(slug, {}).get("zh-CN", {})
        title = (zh.get("title") or slug).strip()
        intro = (zh.get("intro") or "").strip()
        if not intro:
            intro = f"{title}：在线输入参数即可即时得到结果，无需安装与注册。"
        d = deep.get(f"{IND}/{slug}", {})
        scenarios = [s for s in (d.get("scenarios") or []) if isinstance(s, str)]
        examples = d.get("examples") or []
        faqs = d.get("faqs") or []

        related = [slugs[(i + k) % len(slugs)] for k in (1, 2, 3, 4)]

        sections = []
        fm = FORMULA_MAP.get(slug)
        if fm and fm.get("eq"):
            sections.append((
                "计算公式与原理",
                "<p><strong>%s</strong></p><p>%s</p>" % (esc(fm["eq"]), esc(fm.get("desc", ""))),
            ))
        elif fm and fm.get("desc"):
            sections.append(("计算口径与说明", "<p>%s</p>" % esc(fm["desc"])))
        else:
            sections.append(("功能说明", "<p>%s</p>" % esc(intro)))

        labels = input_labels(slug)
        if labels:
            steps = "".join("<li>填写「%s」。</li>" % esc(lb) for _, lb in labels)
            sections.append((
                "使用步骤",
                "<ol>%s<li>结果区会即时更新；可一键复制结果用于记录或汇报。</li></ol>" % steps,
            ))

        if scenarios:
            sections.append((
                "典型使用场景",
                "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(s) for s in scenarios),
            ))
        if examples:
            ex_html = "".join(
                "<li><strong>%s</strong>：%s</li>"
                % (esc(e.get("title", "")), esc(e.get("body", "")))
                for e in examples
                if isinstance(e, dict)
            )
            if ex_html:
                sections.append(("算例参考", "<ul>%s</ul>" % ex_html))

        sections.append((
            "注意事项",
            "<p>本工具纯前端运行，输入内容不上传服务器；"
            "结果为按上述口径得到的<strong>理论估算值</strong>，"
            "涉及具体争议请以证据与司法机关认定为准，必要时咨询执业律师。</p>",
        ))

        qa = []
        for q in faqs:
            if isinstance(q, dict) and q.get("q"):
                qa.append((q["q"], q.get("a", "")))
        if not qa:
            qa = [("这个工具怎么用？", "在对应输入框填入参数，结果区会即时给出计算结果。"),
                  ("结果准确吗？", "按标准口径与公式估算，属理论参考；具体案件请结合证据与专业意见。")]

        out[slug] = {
            "title": title + " 使用指南",
            "desc": (intro[:70] if intro else title + "使用指南"),
            "lead": intro,
            "sections": sections,
            "faqs": qa,
            "related": related,
        }
    return out


def render(slug, c):
    sections_html = "\n".join(f"<h2>{h}</h2>\n{b}" for h, b in c["sections"])
    faq_html = "\n".join(f"<dt>{esc(q)}</dt><dd>{esc(a)}</dd>" for q, a in c["faqs"])
    related_html = "\n".join(
        f'<a class="tool-chip" href="{SITE}/tools/{IND}/{r}.html">{esc(c["related_titles"][r])}</a>'
        for r in c["related"]
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
<title>{esc(c['title'])} - ToolBox</title>
<meta name="description" content="{esc(c['desc'])}">
<meta property="og:title" content="{esc(c['title'])}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{SITE}/guides/{slug}-guide.html">
<meta property="og:description" content="{esc(c['desc'])}">
<meta name="twitter:title" content="{esc(c['title'])}">
<meta name="twitter:description" content="{esc(c['desc'])}">
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
</head>
<body>
<nav class="breadcrumb"><a href="{SITE}/">ToolBox</a> / <a href="{SITE}/guides/index.html">使用指南</a> / <span>{esc(c['title'])}</span></nav>
<main>
<h1>{esc(c['title'])}</h1>
<p class="lead">{esc(c['lead'])}</p>
{sections_html}
<div class="related">
<h3>相关工具</h3>
{related_html}
</div>
<dl class="faq">
{faq_html}
</dl>
<div class="back"><a href="{SITE}/tools/{IND}/{slug}.html">→ 打开{esc(c['title'].replace(' 使用指南', ''))}工具</a></div>
</main>
</body>
</html>
"""


def update_guides_json(created, titles):
    """追加 / 更新本批次生成的指南到 json/guides.json（按 tool basename 去重；已存在则同步路径与中文标题）。"""
    gp = os.path.join(ROOT, "json", "guides.json")
    with open(gp, encoding="utf-8") as f:
        arr = json.load(f)
    by_tool = {e.get("tool"): e for e in arr}
    added, updated = [], []
    for slug in created:
        tool = slug + ".html"
        fname = FILE_OVERRIDE.get(slug, f"{slug}-guide.html")
        title = (titles.get(slug) or slug.replace("-", " ").title()) + " 使用指南"
        entry = {
            "tool": tool,
            "guide": f"../../guides/{fname}",
            "title": title,
        }
        if tool in by_tool:
            if by_tool[tool].get("guide") != entry["guide"] or by_tool[tool].get("title") != entry["title"]:
                by_tool[tool]["guide"] = entry["guide"]
                by_tool[tool]["title"] = entry["title"]
                updated.append(tool)
        else:
            arr.append(entry)
            by_tool[tool] = entry
            added.append(tool)
    if added or updated:
        with open(gp, "w", encoding="utf-8") as f:
            json.dump(arr, f, ensure_ascii=False, indent=1)
    return added, updated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="写入 guides/ 并追加 guides.json；缺省为 dry-run")
    ap.add_argument("--force", action="store_true", help="覆盖已存在指南（统一质量）")
    args = ap.parse_args()

    content = build_content()
    titles = {s: c["title"].replace(" 使用指南", "") for s, c in content.items()}
    for c in content.values():
        c["related_titles"] = titles

    os.makedirs(GUIDES_DIR, exist_ok=True)
    created, skip = [], []
    for slug, c in content.items():
        fname = FILE_OVERRIDE.get(slug, f"{slug}-guide.html")
        out = os.path.join(GUIDES_DIR, fname)
        if os.path.exists(out) and not args.force:
            skip.append(slug)
            continue
        html = render(slug, c)
        if args.apply:
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            created.append(slug)
        else:
            created.append(slug + " (dry)")
    print(f"待生成/已生成: {len(created)} | 跳过(已存在): {len(skip)} | 排除纯工具: {len(EXCLUDE)}")
    for s in created[:8]:
        print("  +", s)
    if len(created) > 8:
        print(f"  ... 共 {len(created)} 篇")
    for s in skip:
        print("  =", s, "(已存在，跳过)")

    if args.apply and created:
        real = [s[:-5] if s.endswith("(dry)") else s for s in created if not s.endswith("(dry)")]
        added, updated = update_guides_json(real, titles)
        print(f"guides.json 新增: {len(added)} 条 | 更新: {len(updated)} 条")


if __name__ == "__main__":
    main()
