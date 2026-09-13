#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
realestate 分类「使用指南」生成器（收口批次 E，3→54）。

数据驱动（不手写文案，全部取自已有真实数据源，避免套话）：
  - 标题 / 简介：i18n/tools/realestate.json 的 zh-CN.title / intro
  - 公式：页面 formula-box 的 formula-eq；formula-desc 若为「输入两个参数…」占位文案则回退用 intro
  - 场景 / 示例 / FAQ：i18n/tools/content_deepdive.json 的 scenarios / examples / faqs
  - 使用步骤：由页面 <input>/<select> 的中文标签自动生成

模板对齐 scripts/gen_legal_guides.py（head 元信息 + JSON-LD
Article/BreadcrumbList/FAQPage + 内联 CSS + breadcrumb/h1/lead/章节/相关工具/FAQ/back）。

跨行业重名处理（与 legal 版的关键差异）：
  calc-1 / calc-2 在 40+ 个行业存在同名 slug，而 json/guides.json 以 tool basename 为键，
  按 legal 版「同键即覆盖」的写法会顶掉 hydraulic 已有的正确映射。
  本脚本改用「追加」语义：仅当现有条目并非归属 realestate 时才新增一条。
  可行性依据：_build.py 的 GUIDE_MAP_IND 通过反查指南正文里的绝对 URL
  （https://chenguangwu.github.io/tools/<行业>/<tool>.html）判定归属，
  因此同一 basename 的多条记录可各自精确命中本行业，互不干扰。
  指南文件名另用 realestate- 前缀消歧，避免覆盖他行业已生成的指南文件。

排除：
  - index.html（行业落地页，非工具）
  - summary-second-hand：名为「二手房税费汇总」而 calc() 实为通用统计（n/均值/方差），
    名实不符待内容整改，暂不生成指南以免固化错误语义（见 DEV-PLAN §9.3）。

用法：
    python3 scripts/gen_realestate_guides.py            # dry-run
    python3 scripts/gen_realestate_guides.py --apply    # 写入 guides/ 并追加 guides.json
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GUIDES_DIR = os.path.join(ROOT, "guides")
TOOLS_DIR = os.path.join(ROOT, "tools", "realestate")
IND = "realestate"
DATE = "2026-09-13"
SITE = "https://chenguangwu.github.io"

# 名实不符待整改，暂不生成（见模块 docstring）
EXCLUDE = {"summary-second-hand"}

# 跨行业重名 slug：改用 realestate- 前缀文件名，避免覆盖 hydraulic 等同名指南文件
FILE_OVERRIDE = {
    "calc-1": "realestate-calc-1-guide.html",
    "calc-2": "realestate-calc-2-guide.html",
}

# 占位文案：出现在 formula-desc 里说明该框说明文字尚未真实化，不可搬进指南
PLACEHOLDER_HINTS = ("输入两个参数", "自动计算常用结果")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fname_of(slug):
    return FILE_OVERRIDE.get(slug, f"{slug}-guide.html")


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


def page_formula(slug):
    """读取页面 formula-box；desc 为占位文案时返回空字符串，由调用方回退。"""
    src = open(os.path.join(TOOLS_DIR, slug + ".html"), encoding="utf-8").read()
    m = re.search(r'<div class="formula-eq">([\s\S]*?)</div>', src)
    d = re.search(r'<p class="formula-desc">([\s\S]*?)</p>', src)
    eq = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    desc = re.sub(r"<[^>]+>", "", d.group(1)).strip() if d else ""
    if any(h in desc for h in PLACEHOLDER_HINTS):
        desc = ""
    return eq, desc


def build_content():
    gis = load_json(os.path.join(ROOT, "i18n", "tools", "realestate.json"))
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
        eq, fdesc = page_formula(slug)
        if eq:
            body = "<p><strong>%s</strong></p>" % esc(eq)
            body += "<p>%s</p>" % esc(fdesc or intro)
            sections.append(("计算公式与原理", body))
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
            "<p>本工具纯前端运行，输入内容不上传服务器；结果为按上述口径得到的"
            "<strong>理论估算值</strong>。房地产交易受当地限购、信贷与税费政策影响，"
            "各城市执行口径存在差异，实际操作请以网签合同、评估报告与主管部门规定为准，"
            "重大决策建议咨询专业估价师或经纪人。</p>",
        ))

        qa = []
        for q in faqs:
            if isinstance(q, dict) and q.get("q"):
                qa.append((q["q"], q.get("a", "")))
        if not qa:
            qa = [
                ("这个工具怎么用？", "在对应输入框填入参数，结果区会即时给出计算结果。"),
                ("结果准确吗？", "按行业通用口径与公式估算，属理论参考；实际交易请以合同、评估报告与当地政策为准。"),
            ]

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
    fname = fname_of(slug)
    url = f"{SITE}/guides/{fname}"
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
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ToolBox", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "使用指南", "item": f"{SITE}/guides/index.html"},
            {"@type": "ListItem", "position": 3, "name": c["title"], "item": url}]},
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
<meta property="og:url" content="{url}">
<meta property="og:description" content="{esc(c['desc'])}">
<meta name="twitter:title" content="{esc(c['title'])}">
<meta name="twitter:description" content="{esc(c['desc'])}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
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


def guide_owner_inds(entry):
    """反查指南正文里的绝对 URL，得到该指南已归属的行业集合（与 _build.py 同口径）。"""
    p = os.path.join(ROOT, (entry.get("guide") or "").replace("../../", ""))
    if not os.path.isfile(p):
        return set()
    try:
        s = open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return set()
    return set(re.findall(r"https://chenguangwu\.github\.io/tools/([A-Za-z0-9_-]+)/", s))


def update_guides_json(created, titles):
    """追加 / 更新本批次指南到 json/guides.json。

    与 legal 版「同 tool basename 即覆盖」不同：这里对跨行业重名的 slug 采用追加语义，
    仅更新「已归属 realestate」的条目，避免顶掉 hydraulic 等同名工具的正确映射。
    """
    gp = os.path.join(ROOT, "json", "guides.json")
    with open(gp, encoding="utf-8") as f:
        arr = json.load(f)
    added, updated = [], []
    for slug in created:
        tool = slug + ".html"
        entry = {
            "tool": tool,
            "guide": f"../../guides/{fname_of(slug)}",
            "title": (titles.get(slug) or slug) + " 使用指南",
        }
        same_tool = [e for e in arr if e.get("tool") == tool]
        mine = [e for e in same_tool if IND in guide_owner_inds(e)]
        if mine:
            e = mine[0]
            if e.get("guide") != entry["guide"] or e.get("title") != entry["title"]:
                e["guide"] = entry["guide"]
                e["title"] = entry["title"]
                updated.append(tool)
        else:
            arr.append(entry)
            added.append(tool)
    if added or updated:
        with open(gp, "w", encoding="utf-8") as f:
            json.dump(arr, f, ensure_ascii=False, indent=1)
    return added, updated


def update_guides_index(created, content):
    """向 guides/index.html 追加本批次指南条目（格式对齐 scripts/gen_guide_pages.py）。

    幂等：已收录（index 中已存在该文件链接）的条目会跳过，重跑不产生重复。
    """
    ip = os.path.join(GUIDES_DIR, "index.html")
    if not os.path.isfile(ip):
        return 0
    s = open(ip, encoding="utf-8").read()
    fresh = [slug for slug in created if "/guides/%s" % fname_of(slug) not in s]
    if not fresh:
        print("guides/index.html 已含全部条目，跳过追加")
        return 0
    new_li = "".join(
        '<li><a href="%s/guides/%s">%s</a>'
        '<span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
        % (SITE, fname_of(slug),
           esc(content[slug]["title"].replace(" 使用指南", "") + "使用指南"),
           esc(content[slug]["desc"][:50]))
        for slug in fresh
    )
    if "</ul>" not in s:
        print("警告：guides/index.html 未找到 </ul>，跳过追加")
        return 0
    s = s.replace("</ul>", new_li + "</ul>", 1)
    open(ip, "w", encoding="utf-8").write(s)
    return len(fresh)


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
        out = os.path.join(GUIDES_DIR, fname_of(slug))
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
    print(f"待生成/已生成: {len(created)} | 跳过(已存在): {len(skip)} | 排除: {len(EXCLUDE)}")
    for s in created[:8]:
        print("  +", s)
    if len(created) > 8:
        print(f"  ... 共 {len(created)} 篇")
    for s in skip:
        print("  =", s, "(已存在，跳过)")

    if args.apply and created:
        added, updated = update_guides_json(created, titles)
        print(f"guides.json 新增: {len(added)} 条 | 更新: {len(updated)} 条")
        n = update_guides_index(created, content)
        print(f"guides/index.html 追加: {n} 条")


if __name__ == "__main__":
    main()
