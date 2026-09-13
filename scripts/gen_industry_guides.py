#!/usr/bin/env python3
"""通用单分类「使用指南」生成器（收口批次 E）。

用法：
    python3 scripts/gen_industry_guides.py --ind energy              # dry-run
    python3 scripts/gen_industry_guides.py --ind energy --apply      # 写入
    python3 scripts/gen_industry_guides.py --ind energy --apply --force
    python3 scripts/gen_industry_guides.py --ind energy --apply --note "行业化注意事项…"
    python3 scripts/gen_industry_guides.py --ind energy --apply --exclude slug-a,slug-b

数据源：
  - 标题 / 简介：i18n/tools/<ind>.json 的 zh-CN.title / intro
  - 场景 / 算例 / FAQ：i18n/tools/content_deepdive.json 的 '<ind>/<slug>'
  - 公式与输入框：tools/<ind>/<slug>.html

跨行业重名消歧（与 legal 版「同 basename 即覆盖」不同）：
  同一 slug 在多个行业普遍同名（如 calc-1）。_build.py 靠指南正文里的绝对 URL
  反查行业归属，故同 basename 可在 guides.json 中共存、各自精确命中。
  本脚本自动判定：若某 slug 已存在归属「其他行业」的指南，则改用
  '<ind>-<slug>-guide.html' 文件名并以「追加」语义写入 guides.json，
  绝不覆盖他行业既有映射。
"""
import argparse
import glob
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, "guides")
SITE = "https://chenguangwu.github.io"
DATE = date.today().isoformat()

DEFAULT_NOTE = (
    "本工具纯前端运行，输入内容不上传服务器；结果为按上述口径得到的"
    "<strong>理论估算值</strong>。实际应用受设备参数、测量条件与当地规范影响，"
    "请以设备铭牌、检测报告与现行标准为准，重大决策建议咨询专业人士。"
)

_ap = argparse.ArgumentParser()
_ap.add_argument("--ind", required=True, help="分类目录名，如 energy")
_ap.add_argument("--apply", action="store_true", help="写入 guides/ 与 guides.json；缺省为 dry-run")
_ap.add_argument("--force", action="store_true", help="覆盖已存在指南（统一质量）")
_ap.add_argument("--exclude", default="", help="排除的 slug，逗号分隔")
_ap.add_argument("--note", default="", help="「注意事项」段落的行业化文案；缺省用通用文案")
_a = _ap.parse_args()

IND = _a.ind
TOOLS_DIR = os.path.join(ROOT, "tools", IND)
EXCLUDE = {s.strip() for s in _a.exclude.split(",") if s.strip()}
NOTE = _a.note.strip() or DEFAULT_NOTE

if not os.path.isdir(TOOLS_DIR):
    raise SystemExit("错误: tools/%s 不存在" % IND)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def owner_inds_of_file(path):
    if not os.path.isfile(path):
        return set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        s = f.read()
    return set(re.findall(r"https://chenguangwu\.github\.io/tools/([A-Za-z0-9_-]+)/", s))


_guides_arr = None


def guides_arr():
    global _guides_arr
    if _guides_arr is None:
        _guides_arr = load_json(os.path.join(ROOT, "json", "guides.json"))
    return _guides_arr


def fname_of(slug):
    """跨行业重名判定：已归属他行业则用 '<ind>-' 前缀文件名，避免覆盖。"""
    plain = "%s-guide.html" % slug
    mine = "%s-%s-guide.html" % (IND, slug)
    # 归属不明（无绝对 URL）时也按「非本行业」处理，避免覆盖他行业既有指南
    for e in guides_arr():
        if e.get("tool") != slug + ".html":
            continue
        p = os.path.join(ROOT, (e.get("guide") or "").replace("../../", ""))
        if IND not in owner_inds_of_file(p):
            return mine
    p = os.path.join(GUIDES_DIR, plain)
    if os.path.isfile(p) and IND not in owner_inds_of_file(p):
        return mine
    return plain


def input_labels(slug):
    p = os.path.join(TOOLS_DIR, slug + ".html")
    if not os.path.isfile(p):
        return []
    s = open(p, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<label[^>]*for="([^"]+)"[^>]*>([\s\S]*?)</label>', s):
        lb = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if lb and len(lb) < 40:
            out.append((m.group(1), lb))
    return out[:8]


def page_formula(slug):
    p = os.path.join(TOOLS_DIR, slug + ".html")
    if not os.path.isfile(p):
        return None, None
    s = open(p, encoding="utf-8").read()
    m = re.search(r'<div class="formula-eq">([\s\S]*?)</div>', s)
    d = re.search(r'<p class="formula-desc">([\s\S]*?)</p>', s)
    eq = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    de = re.sub(r"<[^>]+>", "", d.group(1)).strip() if d else ""
    if not eq or "输入两个参数" in eq or "自动计算常用结果" in eq:
        return None, None
    return eq, de


def build_content():
    gis = load_json(os.path.join(ROOT, "i18n", "tools", "%s.json" % IND))
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
            intro = "%s：在线输入参数即可即时得到结果，无需安装与注册。" % title
        d = deep.get("%s/%s" % (IND, slug), {})
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
                for e in examples if isinstance(e, dict)
            )
            if ex_html:
                sections.append(("算例参考", "<ul>%s</ul>" % ex_html))

        sections.append(("注意事项", "<p>%s</p>" % NOTE))

        qa = []
        for q in faqs:
            if isinstance(q, dict) and q.get("q"):
                qa.append((q["q"], q.get("a", "")))
        if not qa:
            qa = [
                ("这个工具怎么用？", "在对应输入框填入参数，结果区会即时给出计算结果。"),
                ("结果准确吗？", "按行业通用口径与公式估算，属理论参考；实际应用请以设备铭牌、检测报告与现行标准为准。"),
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
    url = "%s/guides/%s" % (SITE, fname)
    sections_html = "\n".join("<h2>%s</h2>\n%s" % (h, b) for h, b in c["sections"])
    faq_html = "\n".join("<dt>%s</dt><dd>%s</dd>" % (esc(q), esc(aa)) for q, aa in c["faqs"])
    related_html = "\n".join(
        '<a class="tool-chip" href="%s/tools/%s/%s.html">%s</a>'
        % (SITE, IND, r, esc(c["related_titles"][r]))
        for r in c["related"]
    )
    faq_json = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": aa}}
        for q, aa in c["faqs"]
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": c["title"],
         "description": c["desc"], "author": {"@type": "Organization", "name": "ToolBox"},
         "datePublished": DATE, "dateModified": DATE,
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ToolBox", "item": "%s/" % SITE},
            {"@type": "ListItem", "position": 2, "name": "使用指南", "item": "%s/guides/index.html" % SITE},
            {"@type": "ListItem", "position": 3, "name": c["title"], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_json},
    ]
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{url}">
<meta property="og:description" content="{desc}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{ld0}</script>
<script type="application/ld+json">{ld1}</script>
<script type="application/ld+json">{ld2}</script>
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
<nav class="breadcrumb"><a href="{SITE}/">ToolBox</a> / <a href="{SITE}/guides/index.html">使用指南</a> / <span>{title}</span></nav>
<main>
<h1>{title}</h1>
<p class="lead">{lead}</p>
{sections_html}
<div class="related">
<h3>相关工具</h3>
{related_html}
</div>
<dl class="faq">
{faq_html}
</dl>
<div class="back"><a href="{SITE}/tools/{IND}/{slug}.html">→ 打开{short}工具</a></div>
</main>
</body>
</html>
""".format(title=esc(c["title"]), desc=esc(c["desc"]), url=url, SITE=SITE,
           ld0=json.dumps(ld[0], ensure_ascii=False), ld1=json.dumps(ld[1], ensure_ascii=False),
           ld2=json.dumps(ld[2], ensure_ascii=False), sections_html=sections_html,
           related_html=related_html, faq_html=faq_html, IND=IND, slug=slug,
           lead=esc(c["lead"]), short=esc(c["title"].replace(" 使用指南", "")))


def guide_owner_inds(entry):
    p = os.path.join(ROOT, (entry.get("guide") or "").replace("../../", ""))
    return owner_inds_of_file(p)


def update_guides_json(created, titles):
    """追加 / 更新本批次指南到 json/guides.json（跨行业重名采用追加语义）。"""
    gp = os.path.join(ROOT, "json", "guides.json")
    arr = guides_arr()
    added, updated = [], []
    for slug in created:
        tool = slug + ".html"
        entry = {
            "tool": tool,
            "guide": "../../guides/%s" % fname_of(slug),
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
    with open(gp, "w", encoding="utf-8") as f:
        json.dump(arr, f, ensure_ascii=False, indent=1)
    return added, updated


def update_guides_index(created, content):
    """向 guides/index.html 追加本批次条目（幂等）。"""
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
    content = build_content()
    titles = {s: c["title"].replace(" 使用指南", "") for s, c in content.items()}
    for c in content.values():
        c["related_titles"] = titles

    os.makedirs(GUIDES_DIR, exist_ok=True)
    created, skip, prefixed = [], [], []
    for slug, c in content.items():
        out = os.path.join(GUIDES_DIR, fname_of(slug))
        if fname_of(slug) != "%s-guide.html" % slug:
            prefixed.append(slug)
        if os.path.exists(out) and not _a.force:
            skip.append(slug)
            continue
        if _a.apply:
            with open(out, "w", encoding="utf-8") as f:
                f.write(render(slug, c))
        created.append(slug)
    print("待生成/已生成: %d | 跳过(已存在): %d | 排除: %d | 跨行业重名改用前缀名: %d"
          % (len(created), len(skip), len(EXCLUDE), len(prefixed)))
    if prefixed:
        print("  前缀名:", ", ".join(prefixed))
    for s in created[:8]:
        print("  +", s)
    if len(created) > 8:
        print("  ... 共 %d 篇" % len(created))

    if _a.apply and created:
        added, updated = update_guides_json(created, titles)
        print("guides.json 新增: %d 条 | 更新: %d 条" % (len(added), len(updated)))
        n = update_guides_index(created, content)
        print("guides/index.html 追加: %d 条" % n)


if __name__ == "__main__":
    main()
