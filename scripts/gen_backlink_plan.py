# -*- coding: utf-8 -*-
"""
gen_backlink_plan.py — ToolBox 外链建设作战清单生成器

扫描全站工具 (json/tools.json)，为每个工具匹配「真实竞品站 / 行业资源页投稿目标」，
并产出：
  1. backlink-plan.md      —— 站级作战手册（平台清单 / 竞品库 / 提交模板 / 头部工具示例）
  2. backlink-targets.csv  —— 全量 5023 工具 → 竞品关联 / 资源页 / 建议平台

用法：
  python3 scripts/gen_backlink_plan.py
纯标准库，可复跑（幂等覆盖）。产物不影响站点，不被 _build.py 收录。
"""
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chenguangwu.github.io"
TOOLS_JSON = os.path.join(ROOT, "json", "tools.json")
OUT_MD = os.path.join(ROOT, "backlink-plan.md")
OUT_CSV = os.path.join(ROOT, "backlink-targets.csv")

# ---------------------------------------------------------------------------
# 1) 工具 → 真实竞品站映射（按 slug 关键词子串匹配，顺序即优先级）
#    仅收录真实存在、业界公认的头部单工具站，绝不编造。
# ---------------------------------------------------------------------------
COMPETITOR_MAP = [
    ("base64", "Base64 Decode", "https://www.base64decode.org"),
    ("json", "JSON Formatter / jsonformatter.org", "https://jsonformatter.org"),
    ("qr", "QR Code Generator", "https://www.qr-code-generator.com"),
    ("qrcode", "QR Code Generator", "https://www.qr-code-generator.com"),
    ("password", "Passwords Generator", "https://passwordsgenerator.net"),
    ("uuid", "UUID Generator", "https://www.uuidgenerator.net"),
    ("timestamp", "Epoch Converter", "https://www.epochconverter.com"),
    ("epoch", "Epoch Converter", "https://www.epochconverter.com"),
    ("color", "HTML Color Codes", "https://htmlcolorcodes.com"),
    ("cron", "Crontab Guru", "https://crontab.guru"),
    ("jwt", "JWT.io", "https://jwt.io"),
    ("regex", "Regex101", "https://regex101.com"),
    ("word-count", "WordCounter", "https://wordcounter.net"),
    ("wordcount", "WordCounter", "https://wordcounter.net"),
    ("lorem", "Lorem Ipsum Generator", "https://lipsum.com"),
    ("pdf", "Smallpdf", "https://smallpdf.com"),
    ("yaml", "YAML Validator / Convert", "https://www.json2yaml.com"),
    ("csv", "CSV to JSON / ConvertCSV", "https://www.convertcsv.com"),
    ("markdown", "Markdown Live Preview", "https://stackedit.io"),
    ("diff", "Diffchecker", "https://www.diffchecker.com"),
    ("compare", "Diffchecker", "https://www.diffchecker.com"),
    ("bmi", "BMI Calculator (NIH)", "https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm"),
    ("roman", "Roman Numerals Converter", "https://www.rapidtables.com/convert/number/roman-numerals-converter.html"),
    ("binary", "Binary Converter / RapidTables", "https://www.rapidtables.com/convert/number/binary-to-decimal.html"),
    ("ascii", "ASCII Table / RapidTables", "https://www.rapidtables.com/computer/basic/ascii-table.html"),
    ("morse", "Morse Code Translator", "https://morsedecoder.com"),
    ("md5", "MD5 Online", "https://www.md5online.org"),
    ("sha", "SHA Hash / Browserling", "https://www.browserling.com/tools"),
    ("hash", "Hash Generator / Browserling", "https://www.browserling.com/tools"),
    ("url-encode", "URL Encode / Decode", "https://www.url-encode-decode.com"),
    ("url-decode", "URL Encode / Decode", "https://www.url-encode-decode.com"),
    ("case", "Case Converter", "https://convertcase.net"),
    ("resize", "Image Resizer / ResizePixel", "https://www.resizepixel.com"),
    ("compress", "TinyPNG / Compress", "https://tinypng.com"),
    ("png", "TinyPNG", "https://tinypng.com"),
    ("jpg", "iLoveIMG", "https://www.iloveimg.com"),
    ("html", "HTML Formatter / FreeFormatter", "https://www.freeformatter.com/html-formatter.html"),
    ("css", "CSS Formatter / FreeFormatter", "https://www.freeformatter.com/css-beautifier.html"),
    ("sql", "SQL Formatter / FreeFormatter", "https://www.freeformatter.com/sql-formatter.html"),
    ("invoice", "Invoice Generator / FreeInvoiceBuilder", "https://www.freeinvoicebuilder.com"),
    ("resume", "Resume Builder / Novoresume", "https://novoresume.com"),
    ("loan", "Mortgage Calculator / NerdWallet", "https://www.nerdwallet.com/mortgages/mortgage-calculator"),
    ("mortgage", "Mortgage Calculator / NerdWallet", "https://www.nerdwallet.com/mortgages/mortgage-calculator"),
    ("tax", "Tax Calculator / TaxAct", "https://www.taxact.com"),
    ("percentage", "Percentage Calculator / Calculator.net", "https://www.calculator.net/percent-calculator.html"),
    ("unit", "Unit Converter / RapidTables", "https://www.rapidtables.com/convert/"),
    ("currency", "Calculator.net Currency", "https://www.calculator.net/currency-calculator.html"),
    ("countdown", "Time and Date Countdown", "https://www.timeanddate.com/countdown/"),
    ("age", "Age Calculator / Calculator.net", "https://www.calculator.net/age-calculator.html"),
    ("gpa", "GPA Calculator / Calculator.net", "https://www.calculator.net/gpa-calculator.html"),
    ("grade", "Grade Calculator / Calculator.net", "https://www.calculator.net/grade-calculator.html"),
    ("tip", "Tip Calculator / Calculator.net", "https://www.calculator.net/tip-calculator.html"),
    ("emoji", "EmojiCopy", "https://emojicopy.com"),
    ("slug", "Slug Generator / CodeBeautify", "https://codebeautify.org/slug-generator"),
    ("lorem-ipsum", "Lorem Ipsum Generator", "https://lipsum.com"),
]

# ---------------------------------------------------------------------------
# 2) 站级平台清单（手动提交，AI 无法代操作；需注册/登录/验证码）
# ---------------------------------------------------------------------------
SITE_PLATFORMS = [
    {
        "name": "AlternativeTo",
        "url": "https://alternativeto.net",
        "weight": "DR 83 / 高",
        "type": "软件导航站（DoFollow）",
        "action": "为「ToolBox」建产品条目，关联竞品（it-tools.tech、Toolfk、其他在线工具聚合站）；"
                  "用户自然投票带来外链 + 直接流量。",
        "template": "Product: ToolBox — 5000+ 免费在线工具百科，纯前端、数据不上传。\n"
                    "Alternatives to: it-tools.tech, toolfk.com, smallpdf.com",
    },
    {
        "name": "Product Hunt",
        "url": "https://www.producthunt.com",
        "weight": "DR 90 / 极高",
        "type": "产品发布平台（高权重外链 + 流量）",
        "action": "发一次 Launch（需准备首图、标语、前 100 字描述）。建议周五 UTC 档期。",
        "template": "Tagline: 5000+ free online tools, 100% in-browser, no data upload.\n"
                    "Topics: Productivity, Developer Tools, Web App\n"
                    "First Comment: 为什么做 / 与 it-tools 的差异（更全、中文友好）",
    },
    {
        "name": "Hacker News (Show HN)",
        "url": "https://news.ycombinator.com/submit",
        "weight": "DR 88 / 极高",
        "type": "社区（DoFollow，流量大）",
        "action": "发「Show HN: ToolBox, 5000+ free client-side web tools」。标题克制、正文讲技术取舍（纯前端/零后端）。",
        "template": "Title: Show HN: ToolBox – 5000+ free, fully client-side web tools\n"
                    "Text: 纯静态、零后端、数据不上传；覆盖 IT/金融/设计/生活。求反馈。",
    },
    {
        "name": "少数派（效率工具）",
        "url": "https://sspai.com",
        "weight": "DR 78 / 高（中文权重）",
        "type": "中文科技媒体（客座/矩阵）",
        "action": "写「我用 5000+ 在线工具搭建了一个零后端工具站」类文章，自然带站链；或投稿效率工具清单。",
        "template": "标题: 收藏这个零后端工具站，5000+ 需求一站搞定\n正文: 按场景挑 10 个工具演示，结尾放 ToolBox 总入口",
    },
    {
        "name": "V2EX「分享发现 / 创造」",
        "url": "https://www.v2ex.com",
        "weight": "DR 72 / 中高",
        "type": "中文社区（自然露出）",
        "action": "发「做了一个纯前端工具站」帖，给价值、不硬广；回帖答疑带链接。",
        "template": "标题: 做了一个 5000+ 工具的纯前端站，数据全在本地\n正文: 技术选型 + 几个好用工具举例",
    },
    {
        "name": "Reddit (r/usefulwebsites 等)",
        "url": "https://www.reddit.com/r/usefulwebsites",
        "weight": "DR 91 / 极高",
        "type": "社区（DoFollow，大流量）",
        "action": "在 r/usefulwebsites、r/software、r/SideProject 发帖；遵守版规、先给价值。",
        "template": "Title: I built a 5000+ free client-side tool site (no backend, no upload)\n"
                    "Body: what it covers + a few examples",
    },
    {
        "name": "GitHub awesome-* 列表",
        "url": "https://github.com/sindresorhus/awesome",
        "weight": "DR 96 / 极高",
        "type": "开源清单（高权重）",
        "action": "若站点/部分工具开源，PR 提交到 awesome-web-tools / awesome-selfhosted 等列表。",
        "template": "PR to sindresorhus/awesome: 添加 ToolBox 到 'Tools' 分类",
    },
    {
        "name": "资源页 Link Building（按行业）",
        "url": "Google: \"best free online {行业} tools\" + \"add your site\"",
        "weight": "中-高（按目标页定）",
        "type": "资源页投稿（精准、相关性强）",
        "action": "搜「best free online {industry} tools」「{industry} tools list」类资源页，邮件联系站长把 ToolBox 加入。",
        "template": "邮件: Hi, 我发现你的 {行业} 工具清单很棒，可否把 ToolBox（5000+ 工具含 {行业} 分类）加进去？",
    },
]

# ---------------------------------------------------------------------------
# 3) 行业中文名（用于手册可读）
# ---------------------------------------------------------------------------
INDUSTRY_CN = {
    "it": "IT/开发", "finance": "金融", "design": "设计", "biz": "商业",
    "marketing": "营销", "science": "科学", "health": "健康", "life": "生活",
    "edu": "教育", "legal": "法律", "fun": "娱乐", "travel": "旅行",
    "ai": "AI", "encode": "编码", "eco": "环保", "photo": "图片",
    "statistics": "统计", "healthcare": "医疗",
}


def slug_of(url):
    return os.path.basename(url).replace(".html", "")


def match_competitor(slug):
    s = slug.lower()
    for kw, name, url in COMPETITOR_MAP:
        # 字母边界匹配：避免 "image" 误中 "age"、"shadow" 误中 "sha"
        pat = r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])"
        if re.search(pat, s):
            return name, url, "单工具竞品"
    return None


def industry_cn(ind):
    return INDUSTRY_CN.get(ind, ind)


def main():
    tools = json.load(open(TOOLS_JSON, encoding="utf-8"))
    rows = []
    hit = 0
    miss = 0
    for t in tools:
        name = t.get("name", "")
        en = t.get("en") or name
        ind = t.get("industry", "")
        url = t.get("url", "")
        quality = t.get("quality", "")
        slug = slug_of(url)
        full = SITE + "/" + url
        m = match_competitor(slug)
        if m:
            cname, curl, ctype = m
            hit += 1
            platform = "站级(alternative.to/PH) + 资源页可引用竞品"
        else:
            cname = "行业资源页（{行业}工具清单）".format(行业=industry_cn(ind))
            curl = "Google 搜: \"best free online {ind} tools\" + \"add your site\"".format(ind=ind)
            ctype = "行业资源页"
            miss += 1
            platform = "资源页 link building（按行业找清单页投稿）"
        rows.append({
            "tool_zh": name,
            "tool_en": en,
            "url": full,
            "industry": ind,
            "quality": quality,
            "competitor": cname,
            "competitor_url": curl,
            "match_type": ctype,
            "suggest_platform": platform,
        })

    # ---- 写 CSV ----
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tool_zh", "tool_en", "url", "industry",
                                          "quality", "competitor", "competitor_url",
                                          "match_type", "suggest_platform"])
        w.writeheader()
        w.writerows(rows)

    # ---- 写 MD 手册 ----
    head_examples = [r for r in rows if r["match_type"] == "单工具竞品"][:60]
    a_count = sum(1 for r in rows if r["quality"] == "A")

    lines = []
    lines.append("# ToolBox 外链建设作战清单\n")
    lines.append("> 生成于脚本 `scripts/gen_backlink_plan.py`（可复跑）。全站 **%d** 个工具，A 级 **%d** 个。\n" % (len(rows), a_count))
    lines.append("> 外链（backlinks）= 别的网站链向 ToolBox。质量 > 数量、相关性 > 泛链接。**只做白帽**，买链/PBN/群发一律不碰（降权除名风险）。\n")

    lines.append("\n## 一、站级平台清单（手动提交，优先级从高到低）\n")
    lines.append("| 平台 | 权重 | 类型 | 怎么提交 |")
    lines.append("|------|------|------|----------|")
    for p in SITE_PLATFORMS:
        act = p["action"].replace("\n", " ")
        lines.append("| [%s](%s) | %s | %s | %s |" % (p["name"], p["url"], p["weight"], p["type"], act))

    lines.append("\n## 二、AlternativeTo 竞品关联（把 ToolBox 挂到这些竞品产品下）\n")
    lines.append("- **it-tools.tech** — 直接竞品（同纯前端工具站），ToolBox 工具更全、中文友好")
    lines.append("- **Toolfk.com** — 中文在线工具聚合站")
    lines.append("- **Smallpdf / iLovePDF** — PDF 类工具竞品（若做了 PDF 工具）")
    lines.append("- **JSON Formatter / Base64 Decode 等单工具站** — 对应分类下作为 alternative 出现")
    lines.append("\n> 在 AlternativeTo 建「ToolBox」条目后，于每类工具的 *Alternatives to* 栏填入上述竞品，"
                 "用户搜索竞品时会看到 ToolBox，自然带 DoFollow 外链。\n")

    lines.append("\n## 三、头部工具 → 真实竞品站映射（内容营销/资源页引用时用）\n")
    lines.append("匹配到真实竞品的工具共 **%d** 个（占 %.1f%%）。这些最适合写「best X tools」榜单文章时在文中自然带链：\n"
                 % (hit, 100.0 * hit / len(rows)))
    lines.append("| 工具(中文) | 工具(英文) | 行业 | 竞品站 |")
    lines.append("|-----------|-----------|------|--------|")
    for r in head_examples:
        lines.append("| %s | %s | %s | [%s](%s) |" % (
            r["tool_zh"], r["tool_en"], industry_cn(r["industry"]),
            r["competitor"], r["competitor_url"]))
    if len(head_examples) < hit:
        lines.append("\n> 仅展示前 60 条，全量见 `backlink-targets.csv`（筛选 `match_type=单工具竞品`）。\n")

    lines.append("\n## 四、提交文案模板\n")
    lines.append("### 4.1 Product Hunt Launch")
    lines.append("```")
    lines.append(SITE_PLATFORMS[1]["template"])
    lines.append("```")
    lines.append("\n### 4.2 Hacker News (Show HN)")
    lines.append("```")
    lines.append(SITE_PLATFORMS[2]["template"])
    lines.append("```")
    lines.append("\n### 4.3 资源页邮件 Outreach")
    lines.append("```")
    lines.append(SITE_PLATFORMS[7]["template"])
    lines.append("```")

    lines.append("\n## 五、铁律（决定外链有没有用）\n")
    lines.append("1. **质量 > 数量**：1 条 DR 80 外链 > 100 条 DR 5。")
    lines.append("2. **相关性**：同行业/同主题外链权重更高。")
    lines.append("3. **自然锚文本**：混用品牌词 + 泛词（「在线 Base64 工具」），别全用「ToolBox」。")
    lines.append("4. **渐进式增长**：别一天暴涨上千条，会被判作弊。")
    lines.append("5. **UGC/广告平台链接加 `rel=\"ugc\"/\"sponsored\"`**，避免被连坐。")
    lines.append("6. **站内已埋回链入口**：工具页「分享与嵌入」组件生成带品牌回链的 iframe 代码，鼓励用户自发外链（见 `embed.html`）。\n")

    lines.append("\n## 六、配套动作（已上线）\n")
    lines.append("- 工具页底部「分享与嵌入」组件（`js/common.js` `injectShareEmbed`）：嵌入码自带可抓取品牌回链，不用 `nofollow`。")
    lines.append("- `embed.html` 文档页新增「带署名回链」推荐写法，引导用户正确嵌入以传递权重。\n")

    lines.append("\n---\n*本文件为运营清单，不进 sitemap、不影响站点；如需刷新重跑 `python3 scripts/gen_backlink_plan.py`。*\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("✅ 工具总数: %d" % len(rows))
    print("✅ 真实竞品匹配: %d (%.1f%%) | 行业资源页兜底: %d" % (hit, 100.0 * hit / len(rows), miss))
    print("✅ 已生成: %s" % OUT_MD)
    print("✅ 已生成: %s" % OUT_CSV)


if __name__ == "__main__":
    main()
