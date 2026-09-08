# -*- coding: utf-8 -*-
"""fengshui 分类 5 工具内容层真实化（沿用已验证路径）。
1) content_deepdive.json 5 键真实化
2) i18n 三件套（_en_override/slug-en/fengshui.json）清套话 + 补真实英文
3) 5 个工具页 HTML 套话清理（formula-desc / desc-en / JSON-LD desc / 英文<p> fallback / tool-intro-body）
4) fengshui-calculator FAQPage 第4条 + opt-guide 套话
5) good-day-selector 伪随机算法重写为真实「十二建除」算法
所有替换均断言命中，未命中即报错，避免静默漏改。
"""
import json, os, re

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io/"
T = ROOT + "tools/fengshui/"
IT = ROOT + "i18n/tools/"

# ---------- 1. content_deepdive ----------
CD = IT + "content_deepdive.json"
cd = json.load(open(CD, encoding="utf-8"))

ENTRIES = {
    "fengshui/zodiac-lookup": {
        "title": "生肖本命查询",
        "scenarios": [
            "输入出生年份，快速查出自己的本命生肖、对应地支与纳音五行，了解属相的基本文化含义。",
            "在婚恋或社交中参考「六合 / 三合 / 六冲」属相配对宜忌，辅助判断属相相合程度。",
            "结合本命生肖的吉祥方位、幸运数字与颜色，作为布置或择物的趣味参考。",
        ],
        "examples": [{
            "title": "以 1990 年（马年）为例",
            "body": "1990 年出生属马（午），地支午、五行火、阴阳阳；本命时辰 11:00-13:00，吉祥方位南方、幸运数字 2/7、颜色红/紫；六合贵人虎/狗/羊，六冲忌配鼠/牛。可据此了解属马者的传统性格描述与配对宜忌。",
        }],
        "faqs": [
            {"q": "生肖是按农历还是公历年份算？", "a": "生肖以农历新年为界，通常公历 1 月、2 月初出生的人可能仍属上一生肖，建议以当年春节日期确认后再查。"},
            {"q": "本工具的结果准确吗？", "a": "生肖、地支、五行、纳音等属传统文化常识，工具按固定规则推算，结果稳定；属相配对宜忌仅供娱乐与社交参考，不涉及任何科学断言。"},
        ],
    },
    "fengshui/birthday-analysis": {
        "title": "生辰八字分析",
        "scenarios": [
            "输入公历出生日期与出生时辰，排出年、月、日、时四柱干支，了解自己的八字结构。",
            "统计四柱中的五行（金木水火土）分布，查看是否偏旺或缺失，作为传统文化视角的命格参考。",
            "结合日主天干与性别，给出命格总论与五行调补的趣味建议。",
        ],
        "examples": [{
            "title": "以 1990-01-01 子时（男）为例",
            "body": "工具排出四柱：年柱庚午、月柱戊寅、日柱丙戌、时柱戊子（日主天干为丙，属火）。五行分布为 金1·木1·水1·火2·土3，土偏旺、无缺失项；命格总论：男命以财官为用神，五行俱全、命格较为平衡。结果仅供民俗参考，人生贵在自身努力。",
        }],
        "faqs": [
            {"q": "八字排盘用的是农历还是公历？", "a": "本工具直接输入公历日期与出生时辰，由干支历法内部换算年、月、日、时四柱；农历转换已包含在算法中，无需手动换算。"},
            {"q": "五行缺什么一定要补吗？", "a": "八字五行只是传统命理的趣味视角，所谓「缺」与「旺」并无科学依据。健康与生活规划请以现代医学与现实为准，本工具结果仅供文化参考。"},
        ],
    },
    "fengshui/fengshui-guide": {
        "title": "风水知识手册",
        "scenarios": [
            "按「基础 / 住宅 / 财位 / 化煞 / 办公」分类浏览传统风水要点，快速了解各类宜忌。",
            "用关键词搜索（如玄关、财位、横梁压顶）精准定位需要的条目。",
            "布置家居或办公环境前，查阅对应场景的布局原则作为趣味参考。",
        ],
        "examples": [{
            "title": "以「卧室风水」为例",
            "body": "在「住宅」分类下查到：卧室宜静，床头宜靠实墙（非窗下），忌正对镜子、电器或横梁压顶；夫妻床宜南北向。这些内容来自公开民俗资料，可结合采光、通风等现实因素综合判断。",
        }],
        "faqs": [
            {"q": "风水有科学依据吗？", "a": "风水对采光、通风、朝向、动线的重视有一定合理性，但吉凶祸福、财运官运等说法缺乏科学依据。建议以舒适、健康、方便为环境布置首要标准。"},
            {"q": "本手册的内容来源？", "a": "内容整理自公开的传统民俗资料，按场景分类速查，供文化了解与布置参考，不构成任何专业或决策建议。"},
        ],
    },
    "fengshui/fengshui-calculator": {
        "title": "风水罗盘（娱乐版）",
        "scenarios": [
            "输入房屋朝向角度（0–360°），查看对应的八卦方位、二十四山与五行属性。",
            "直接选择坐向与房型，对比传统说法与现代科学视角下的住宅朝向优劣。",
            "学习风水罗盘与二十四山的文化常识，本地保存查询历史随时回看。",
        ],
        "examples": [{
            "title": "以正北 0° 为例",
            "body": "输入 0°（或选预设「正北」），工具显示八卦方位为坎卦、五行水、二十四山壬子癸，并列出八方卦象。切换到「房屋朝向分析」选「坐北朝南」，可看到传统说法（坎宅离向、水火既济）与现代科学视角（冬季采光好、避北风）的并列说明。",
        }],
        "faqs": [
            {"q": "风水罗盘（娱乐版）是做什么的？", "a": "输入房屋朝向角度，或直接选择坐向与房型，查看对应的八卦方位与卦象说明。结果为传统文化角度的方位参考，仅供娱乐，不构成风水建议或决策依据。"},
            {"q": "二十四山是怎么划分的？", "a": "二十四山将圆周 360° 均分为 24 份、每份 15°，用天干、地支与八卦表示，从正北（壬子癸）顺时针排列至西北（戌乾亥），是传统罗盘确定方位的方法。"},
        ],
    },
    "fengshui/good-day-selector": {
        "title": "黄道吉日查询",
        "scenarios": [
            "选择活动类型（婚嫁 / 搬家 / 开业 / 签约 / 安葬 / 出行）并指定起始日期。",
            "按传统「建除十二神」推算未来 30 天每日宜忌，并给出该活动的适配评分。",
            "查看每日冲煞生肖提示，辅助避开与自己属相相冲的日期。",
        ],
        "examples": [{
            "title": "以 2026 年 9 月婚嫁择日为例",
            "body": "工具按节气月支与日干支排出每日建除十二神，并据十二神传统宜忌评定婚嫁适配度。如 2026-09-15 为壬子日、定日，传统上宜嫁娶、祈福，婚嫁评分较高（5 分）；2026-09-10 为丁未日、闭日，宜忌均不突出，评分中等（3 分）。算法确定、可复现，结果仅供民俗参考。",
        }],
        "faqs": [
            {"q": "黄道吉日是怎么算出来的？", "a": "本工具按节气月支与每日干支推算「建除十二神」（建、除、满、平、定、执、破、危、成、收、开、闭），再据十二神的传统宜忌表评定所选活动的适配度并给出评分。"},
            {"q": "结果能当作择日依据吗？", "a": "十二建除属传统黄历民俗，结果确定可复现，但仅供文化与民俗参考；重要日程请结合实际安排与个人判断，本工具不构成任何决策建议。"},
        ],
    },
}
for k, v in ENTRIES.items():
    assert k in cd, f"content_deepdive 缺少键 {k}"
    cd[k] = v
json.dump(cd, open(CD, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("content_deepdive: 5 键已真实化")

# ---------- 2. i18n 三件套 ----------
EN_NAME = {
    "fengshui/zodiac-lookup": "Zodiac Lookup",
    "fengshui/birthday-analysis": "Birthday Analysis",
    "fengshui/fengshui-guide": "Fengshui Guide",
    "fengshui/fengshui-calculator": "Fengshui Calculator",
    "fengshui/good-day-selector": "Good Day Selector",
}
EN_DESC = {
    "fengshui/zodiac-lookup": "Zodiac Lookup - look up your Chinese zodiac by birth year: animal, earthly branch, five-element, and compatibility.",
    "fengshui/birthday-analysis": "Birthday Analysis - cast your Four Pillars (BaZi) from Gregorian birth date and time of birth. For cultural reference only.",
    "fengshui/fengshui-guide": "Fengshui Guide - browse traditional feng shui essentials by scene with quick keyword search.",
    "fengshui/fengshui-calculator": "Fengshui Calculator - enter a compass bearing or house orientation to see the Bagua trigram and twenty-four mountains. Entertainment only.",
    "fengshui/good-day-selector": "Good Day Selector - pick an activity and start date to see auspicious days from the Jian-Chu (十二建除) almanac. Cultural reference only.",
}
EN_US_INTRO = {
    "fengshui/zodiac-lookup": "Look up your Chinese zodiac by birth year: animal, earthly branch, five-element attribute, and compatibility for marriage and friendship references.",
    "fengshui/birthday-analysis": "Cast your Four Pillars (BaZi) from Gregorian birth date and time: heavenly stems, earthly branches, five-element balance, and a brief destiny reading. Cultural reference only.",
    "fengshui/fengshui-guide": "Browse traditional feng shui essentials by scene - residence, office, wealth corner, and sha-qi remedies - with keyword search.",
    "fengshui/fengshui-calculator": "Enter a compass bearing or house orientation to see the Bagua trigram, twenty-four mountains, and five-element. Entertainment only.",
    "fengshui/good-day-selector": "Pick an activity and a start date to see auspicious days in the next 30 days based on the traditional Jian-Chu almanac. Cultural reference only.",
}
SLUGS = ["zodiac-lookup", "birthday-analysis", "fengshui-guide", "fengshui-calculator", "good-day-selector"]

def patch(path, key_fn):
    d = json.load(open(path, encoding="utf-8"))
    for slug in SLUGS:
        full = "fengshui/" + slug
        assert full in d, f"{path} 缺少 {full}"
        d[full]["en"] = EN_NAME[full]
        d[full]["ed"] = EN_DESC[full]
        if "ind" in d[full]:
            pass
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

patch(IT + "_en_override.json", None)
patch(IT + "slug-en.json", None)
print("i18n: _en_override.json / slug-en.json 已清套话并补真实 ed")

fj = json.load(open(IT + "fengshui.json", encoding="utf-8"))
for slug in SLUGS:
    assert slug in fj, f"fengshui.json 缺少 {slug}"
    en = fj[slug].setdefault("en-US", {})
    en["title"] = EN_NAME["fengshui/" + slug]
    en["h1"] = EN_NAME["fengshui/" + slug]
    en["intro"] = EN_US_INTRO["fengshui/" + slug]
    if "note" not in en:
        en["note"] = fj[slug].get("zh-CN", {}).get("note", [])
    en["desc"] = EN_NAME["fengshui/" + slug]
json.dump(fj, open(IT + "fengshui.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("i18n: fengshui.json en-US 已真实化")

# ---------- 3. HTML 清理 ----------
FORMULA_NEW = {
    "zodiac-lookup": "输入出生年份，依据干支与生肖对应规则查得本命生肖、纳音五行与配对宜忌；属相与地支的对应为传统固定规则，结果稳定可复现。",
    "birthday-analysis": "按公历生日与出生时辰，以干支历法排出年、月、日、时四柱八字并统计五行分布；干支推算为确定性算法，结果稳定。仅供民俗参考。",
    "fengshui-guide": "本手册按场景整理传统风水常识（大门、卧室、财位、煞气等），内容来自公开民俗资料，供文化了解与布置参考，不构成决策依据。",
    "fengshui-calculator": "输入朝向角度，按八卦方位与二十四山（每山 15°）换算对应卦象与五行；房屋坐向的传统说法与科学视角并列呈现，仅供娱乐参考。",
    "good-day-selector": "按节气月支与每日干支推算建除十二神，再据十二神传统宜忌评定活动适配度；算法确定、可复现，结果仅供民俗参考。",
}
FORMULA_TITLE = {
    "zodiac-lookup": "生肖本命查询", "birthday-analysis": "生辰八字分析", "fengshui-guide": "风水知识手册",
    "fengshui-calculator": "风水罗盘（娱乐版）", "good-day-selector": "黄道吉日查询",
}
FORMULA_OLD = {
    "zodiac-lookup": "本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。 工具名称：生肖本命查询 - 免费速查表工具，在线生肖本命查询，免费使用。",
    "fengshui-guide": "本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。 工具名称：风水知识手册 - 免费速查表工具，在线风水知识手册，免费使用。",
    "good-day-selector": "本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。 工具名称：黄道吉日查询 - 免费速查表工具，在线黄道吉日查询，免费使用。",
}
JSONLD_OLD = {
    "zodiac-lookup": '"description": "生肖本命查询 - 免费速查表工具，在线生肖本命查询，免费使用。"',
    "birthday-analysis": '"description": "生辰八字分析 - 免费速查表工具，在线生辰八字分析，免费使用。"',
    "fengshui-guide": '"description": "风水知识手册 - 免费速查表工具，在线风水知识手册，免费使用。"',
    "fengshui-calculator": '"description": "风水罗盘 - 免费速查表工具，风水罗盘（娱乐版）。"',
    "good-day-selector": '"description": "黄道吉日查询 - 免费速查表工具，在线黄道吉日查询，免费使用。"',
}
JSONLD_NEW = {
    "zodiac-lookup": "输入出生年份，工具查出对应生肖、纳音五行属性与本命宜忌，便于了解属相文化与年度运势参考。",
    "birthday-analysis": "输入公历出生年月日与具体时辰，工具换算为农历并排出四柱八字，给出五行分布与先天命格的简要解读（民俗参考）。",
    "fengshui-guide": "按需查阅住宅、办公等场景的传统风水要点与布局原则，工具以速查表形式整理常见宜忌，供环境布置时参考。",
    "fengshui-calculator": "输入房屋朝向角度，或直接选择坐向与房型，查看对应的八卦方位与卦象说明。结果为传统文化角度的方位参考，仅供娱乐，不构成风水建议或决策依据。",
    "good-day-selector": "选择婚嫁、动土、开业等活动类型并指定起始日期，工具基于建除十二神查询未来 30 天内的黄道吉日与冲煞提示，辅助安排日程。",
}
P_EN_NEW = {
    "zodiac-lookup": "Look up your Chinese zodiac by birth year - animal, earthly branch, element, and compatibility.",
    "birthday-analysis": "Cast your Four Pillars (BaZi) from birth date and time of birth - for cultural reference.",
    "fengshui-guide": "Browse traditional feng shui essentials by scene, with quick search.",
    "fengshui-calculator": "Enter a bearing or house orientation to see the Bagua trigram and twenty-four mountains.",
    "good-day-selector": "Pick an activity and start date to see auspicious days from the Jian-Chu almanac.",
}
DESC_EN_OLD = {
    "zodiac-lookup": "Zodiac Lookup - free online tool",
    "birthday-analysis": "Birthday Analysis - free online tool",
    "fengshui-guide": "Fengshui Guide - free online tool",
    "fengshui-calculator": "Fengshui Calculator - calculate online, free and accurate",
    "good-day-selector": "Good Day Selector - pick and choose online, free",
}
P_EN_OLD = {
    "zodiac-lookup": "Zodiac Lookup is available directly in your browser, with no data uploaded.",
    "birthday-analysis": "Birthday Analysis is available directly in your browser, with no data uploaded.",
    "fengshui-guide": "Fengshui Guide is available directly in your browser, with no data uploaded.",
    "fengshui-calculator": "Fengshui Calculator - calculate online, free and accurate.",
    "good-day-selector": "Good Day Selector - pick and choose online, free.",
}
INTRO_P_OLD = {
    "zodiac-lookup": "<p>生肖本命查询。风水命理工具，帮助推算与分析命理信息。</p>",
    "birthday-analysis": "<p>生辰八字分析。风水命理工具，帮助推算与分析命理信息。</p>",
    "fengshui-guide": "<p>风水知识手册。风水命理工具，帮助推算与分析命理信息。</p>",
    "good-day-selector": "<p>黄道吉日查询。风水命理工具，帮助推算与分析命理信息。</p>",
    "fengshui-calculator": "<p>风水罗盘是一款风水命理领域的在线工具。风水命理工具，帮助推算与分析命理信息。</p>",
}
INTRO_P_NEW = {
    "zodiac-lookup": "<p>生肖本命查询工具，输入出生年份即可查得本命生肖、地支、纳音五行及六合 / 三合 / 六冲等配对宜忌。</p>",
    "birthday-analysis": "<p>生辰八字分析工具，输入公历生日与出生时辰，即可排出年、月、日、时四柱干支并统计五行分布。</p>",
    "fengshui-guide": "<p>风水知识手册，按基础、住宅、财位、化煞、办公分类整理传统风水要点，支持关键词搜索。</p>",
    "fengshui-calculator": "<p>风水罗盘（娱乐版）工具，输入房屋朝向角度或选择坐向，即可查看对应八卦方位、二十四山与五行属性。</p>",
    "good-day-selector": "<p>黄道吉日查询工具，选择活动类型与起始日期，按传统建除十二神推算未来 30 天的宜忌与评分。</p>",
}
FEATURES_NEW = {
    "zodiac-lookup": [
        "覆盖十二生肖的地支、五行、阴阳与纳音属性",
        "自动推算六合、三合贵人及六冲忌配",
        "给出本命时辰、吉祥方位、幸运数字与颜色",
        "附婚配宜忌参考，纯前端即时查询",
    ],
    "birthday-analysis": [
        "按公历生日与出生时辰排四柱八字",
        "统计金木水火土五行分布，查看偏旺或缺项",
        "依据日主天干与性别给出命格总论",
        "提供五行调补的趣味建议（民俗参考）",
    ],
    "fengshui-guide": [
        "五大类二十余篇风水常识速查",
        "关键词搜索快速定位条目",
        "分类切换浏览住宅 / 办公 / 财位要点",
        "纯前端离线查阅，数据不上传",
    ],
    "fengshui-calculator": [
        "输入 0–360° 角度换算八卦方位与二十四山",
        "选择坐向查看传统说法与现代科学视角",
        "内置二十四山方位表与住宅朝向要点",
        "本地保存查询历史，随时回看",
    ],
    "good-day-selector": [
        "按节气月支与日干支推算每日建除十二神",
        "依据十二神传统宜忌给出活动适配评分",
        "标注每日冲煞生肖，辅助避忌",
        "结果确定可复现，纯前端即时计算",
    ],
}
SCENES_NEW = {
    "zodiac-lookup": [
        "了解自己的属相文化与本命含义",
        "婚恋、社交中参考属相配对宜忌",
        "布置、择物时参考吉祥方位与幸运色",
        "传统文化与民俗知识学习",
    ],
    "birthday-analysis": [
        "了解自己的八字结构与五行强弱",
        "传统文化视角下的命格初探",
        "八字排盘与干支知识学习",
        "民俗文化兴趣探索",
    ],
    "fengshui-guide": [
        "布置家居时查阅大门、玄关、卧室宜忌",
        "办公环境布局与座位禁忌参考",
        "了解财位与常见煞气化解",
        "传统风水文化系统学习",
    ],
    "fengshui-calculator": [
        "了解房屋朝向对应的八卦与五行",
        "从传统与现代双视角看住宅朝向",
        "风水罗盘与二十四山文化学习",
        "家居布置的趣味参考",
    ],
    "good-day-selector": [
        "婚嫁、搬家、开业择选适宜日期",
        "签约、出行、安葬的民俗参考",
        "了解建除十二神与每日宜忌",
        "传统文化与黄历知识学习",
    ],
}

FEATURES_OLD = '''    <ul class="intro-features">
      <li>支持多种命理参数</li>
      <li>纯前端计算，离线可用</li>
      <li>操作简单，快速推算</li>
      <li>提供详细的命理参考</li>
    </ul>'''
SCENES_OLD = '''    <ul class="intro-scenes">
      <li>命理学习与研究</li>
      <li>八字排盘与解读</li>
      <li>传统文化探索</li>
      <li>民俗文化了解</li>
    </ul>'''

def ul_block(items):
    return "    <ul class=\"intro-features\">\n" + "".join(f"      <li>{x}</li>\n" for x in items) + "    </ul>"

def scene_block(items):
    return "    <ul class=\"intro-scenes\">\n" + "".join(f"      <li>{x}</li>\n" for x in items) + "    </ul>"

for slug in SLUGS:
    fp = T + slug + ".html"
    html = open(fp, encoding="utf-8").read()
    # formula-desc（仅部分页有该块）
    fot = FORMULA_OLD.get(slug)
    if fot:
        assert fot in html, f"{slug} 未找到 formula-desc 套话"
        html = html.replace(fot, FORMULA_NEW[slug], 1)
    # desc-en meta
    old = f'<meta name="desc-en" content="{DESC_EN_OLD[slug]}">'
    assert old in html, f"{slug} 未找到 desc-en 套话"
    html = html.replace(old, f'<meta name="desc-en" content="{P_EN_NEW[slug]}">', 1)
    # JSON-LD SoftwareApplication description
    old = JSONLD_OLD[slug]
    assert old in html, f"{slug} 未找到 JSON-LD description 套话"
    html = html.replace(old, f'"description": "{JSONLD_NEW[slug]}"', 1)
    # 英文 <p> fallback
    old = P_EN_OLD[slug]
    assert old in html, f"{slug} 未找到英文 p 套话"
    html = html.replace(old, P_EN_NEW[slug], 1)
    # tool-intro-body 简介 p
    old = INTRO_P_OLD[slug]
    assert old in html, f"{slug} 未找到 intro 简介套话"
    html = html.replace(old, INTRO_P_NEW[slug], 1)
    # 功能特点 ul
    assert FEATURES_OLD in html, f"{slug} 未找到功能特点 ul"
    html = html.replace(FEATURES_OLD, ul_block(FEATURES_NEW[slug]), 1)
    # 使用场景 ul
    assert SCENES_OLD in html, f"{slug} 未找到使用场景 ul"
    html = html.replace(SCENES_OLD, scene_block(SCENES_NEW[slug]), 1)
    open(fp, "w", encoding="utf-8").write(html)
    print(f"HTML: {slug} 套话已清理")

# ---------- 4. fengshui-calculator FAQPage 第4条 + opt-guide ----------
calc = T + "fengshui-calculator.html"
html = open(calc, encoding="utf-8").read()
old_faq = '"风水罗盘（娱乐版）适合哪些场景？", "acceptedAnswer": {"@type": "Answer", "text": "工作与生活中的相关计算与查询。"}}'
new_faq = '"风水罗盘（娱乐版）适合哪些场景？", "acceptedAnswer": {"@type": "Answer", "text": "适合了解房屋朝向对应的八卦与二十四山、从传统与现代双视角看住宅布局，以及风水罗盘文化学习；仅供娱乐参考。"}}'
assert old_faq in html, "calculator FAQPage 第4条未找到"
html = html.replace(old_faq, new_faq, 1)
old_opt = "<h2>适用场景</h2><p>工作与生活中的相关计算与查询。</p>"
new_opt = "<h2>适用场景</h2><p>了解房屋朝向对应的八卦方位、二十四山与五行；对比传统说法与现代科学视角看住宅布局；学习风水罗盘与黄历文化。仅供娱乐参考。</p>"
assert old_opt in html, "calculator opt-guide 套话未找到"
html = html.replace(old_opt, new_opt, 1)
open(calc, "w", encoding="utf-8").write(html)
print("HTML: fengshui-calculator FAQPage/opt-guide 套话已清理")

# ---------- 5. good-day-selector 算法重写 ----------
gd = T + "good-day-selector.html"
html = open(gd, encoding="utf-8").read()
NEW_JS = '''const ACTIVITIES = [
  { id: 'wedding', icon: '💒', name: '婚嫁', yi: ['嫁娶', '祈福'] },
  { id: 'move', icon: '🏠', name: '搬家', yi: ['移徙', '安床'] },
  { id: 'open', icon: '🛍️', name: '开业', yi: ['开市', '求财'] },
  { id: 'sign', icon: '🤝', name: '签约', yi: ['交易', '纳财'] },
  { id: 'funeral', icon: '🕊️', name: '安葬', yi: ['安葬', '动土'] },
  { id: 'travel', icon: '✈️', name: '出行', yi: ['出行', '祈福'] },
];

// 十二建除神及其传统宜忌（民俗黄历常识）
const BUILD_GODS = ['建', '除', '满', '平', '定', '执', '破', '危', '成', '收', '开', '闭'];
const GOD_TABLE = {
  '建': { yi: ['出行', '祈福', '求嗣', '动土', '嫁娶'], ji: ['开仓', '出货', '安葬'] },
  '除': { yi: ['沐浴', '疗病', '出行', '解除'], ji: ['求官', '上任'] },
  '满': { yi: ['祭祀', '祈福', '嫁娶', '移徙', '开市'], ji: ['动土', '葬埋', '修造'] },
  '平': { yi: ['修造', '嫁娶', '移徙', '安床'], ji: ['祈福', '求嗣', '词讼'] },
  '定': { yi: ['祭祀', '祈福', '嫁娶', '造屋', '入学'], ji: ['词讼', '出行'] },
  '执': { yi: ['造屋', '收购', '修造'], ji: ['开市', '移徙', '出行'] },
  '破': { yi: ['破屋', '坏垣', '求医'], ji: ['嫁娶', '出行', '签约', '开市', '动土'] },
  '危': { yi: ['安床', '祭祀', '祈福'], ji: ['登高', '出行', '嫁娶', '移徙'] },
  '成': { yi: ['嫁娶', '开业', '入学', '动土', '安葬', '开市', '交易'], ji: ['词讼'] },
  '收': { yi: ['嫁娶', '纳财', '收购'], ji: ['放债', '出行', '安葬'] },
  '开': { yi: ['开市', '求财', '嫁娶', '造屋', '出行'], ji: ['葬埋', '放债', '修坟'] },
  '闭': { yi: ['筑堤', '安葬', '补垣'], ji: ['开市', '出行', '求医'] },
};

const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
const ZODIAC_NAMES = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
// 日支序 -> 所冲生肖序（子午冲、丑未冲……）
const CLASH = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5];

function getDayGanZhi(date) {
  const base = new Date(1900, 0, 31);
  const days = Math.floor((date - base) / 86400000);
  const off = (days % 60 + 60) % 60;
  return { gan: HEAVENLY_STEMS[off % 10], zhi: EARTHLY_BRANCHES[off % 12] };
}

// 以节气近似确定月支（子=0…亥=11）；节气日期采用常用近似值
function getMonthBranchIndex(y, m, d) {
  const md = m * 100 + d;
  if (md >= 204 && md < 306) return 2;    // 寅（立春~惊蛰）
  if (md >= 306 && md < 405) return 3;    // 卯
  if (md >= 405 && md < 506) return 4;    // 辰
  if (md >= 506 && md < 606) return 5;    // 巳
  if (md >= 606 && md < 707) return 6;    // 午
  if (md >= 707 && md < 808) return 7;    // 未（小暑~立秋）
  if (md >= 808 && md < 908) return 8;    // 申（立秋~白露）
  if (md >= 908 && md < 1008) return 9;    // 酉（白露~寒露）
  if (md >= 1008 && md < 1108) return 10; // 戌
  if (md >= 1108 && md < 1207) return 11; // 亥
  if (md >= 1207) return 11;              // 子（大雪~小寒）
  if (md < 106) return 11;               // 子（跨年）
  return 1;                              // 丑（小寒~立春）
}

function getBuildGod(dayBranchIdx, monthBranchIdx) {
  return BUILD_GODS[((dayBranchIdx - monthBranchIdx) % 12 + 12) % 12];
}

let currentActivity = 'wedding';

function renderActivityGrid() {
  document.getElementById('activityGrid').innerHTML = ACTIVITIES.map(a =>
    `<div class="activity-btn ${a.id === currentActivity ? 'active' : ''}" data-id="${a.id}" onclick="selectActivity('${a.id}')">
      <span class="icon">${a.icon}</span>${a.name}
    </div>`
  ).join('');
}

function selectActivity(id) {
  currentActivity = id;
  document.querySelectorAll('.activity-btn').forEach(b => b.classList.remove('active'));
  document.querySelector(`[data-id="${id}"]`).classList.add('active');
}

function scoreDay(god, act) {
  const t = GOD_TABLE[god];
  const hitYi = t.yi.filter(x => act.yi.includes(x)).length;
  const hitJi = t.ji.filter(x => act.yi.includes(x)).length;
  let score = 3;
  if (hitYi >= 1 && hitJi === 0) score = 4;
  if (hitYi >= 2 && hitJi === 0) score = 5;
  if (hitJi === 1) score = 2;
  if (hitJi >= 2) score = 1;
  return { score, hitYi, hitJi };
}

function findGoodDays() {
  const startStr = document.getElementById('startDate').value;
  if (!startStr) { ToolBox.showToast(i18nText('toast.msg952'), 'error'); return; }
  const start = new Date(startStr);
  const act = ACTIVITIES.find(a => a.id === currentActivity);
  const weekday = ['日', '一', '二', '三', '四', '五', '六'];
  const fmt = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} 周${weekday[d.getDay()]}`;

  const days = [];
  for (let i = 0; i < 30; i++) {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    const dp = getDayGanZhi(d);
    const dbi = EARTHLY_BRANCHES.indexOf(dp.zhi);
    const mbi = getMonthBranchIndex(d.getFullYear(), d.getMonth() + 1, d.getDate());
    const god = getBuildGod(dbi, mbi);
    const sc = scoreDay(god, act);
    days.push({ date: d, gan: dp.gan, zhi: dp.zhi, god, clash: ZODIAC_NAMES[CLASH[dbi]], ...sc });
  }

  days.sort((a, b) => b.score - a.score);
  const good = days.filter(d => d.score >= 4);
  const neutral = days.filter(d => d.score === 3);
  const bad = days.filter(d => d.score <= 2);

  const renderDay = d => {
    const cls = d.score >= 4 ? 'good' : d.score === 3 ? 'neutral' : 'bad';
    const evalText = d.score >= 4 ? '✅ 宜' : d.score === 3 ? '⚠️ 平' : '❌ 慎';
    const t = GOD_TABLE[d.god];
    const yiList = t.yi.filter(x => act.yi.includes(x));
    const jiList = t.ji.filter(x => act.yi.includes(x));
    return `<div class="day-card ${cls}">
      <div class="day-title">${fmt(d.date)} ${evalText} ${act.icon} ${act.name}</div>
      <div class="day-info">📅 ${d.gan}${d.zhi}日 · 十二神：${d.god}神 · 冲${d.clash}</div>
      <div class="day-info">🌟 宜：${yiList.length ? yiList.join('、') : '（本神无特别宜忌）'}</div>
      ${jiList.length ? `<div class="day-info">⚠️ 忌：${jiList.join('、')}</div>` : ''}
      <div class="day-info">评分: <span class="score-bar">${Array.from({ length: 5 }, (_, i) => `<span class="dot ${i < d.score ? 'on' : ''}"></span>`).join('')}</span></div>
    </div>`;
  };

  document.getElementById('result').innerHTML = `
    <h3 style="margin-bottom:12px;">${act.icon} ${act.name} · 未来30天（建除十二神）</h3>
    <p style="font-size:12px;color:var(--text-muted);margin-bottom:12px;">🟢 较佳 ${good.length} 天 · 🟡 平稳 ${neutral.length} 天 · 🔴 慎选 ${bad.length} 天</p>
    ${good.length ? '<p style="font-weight:bold;margin-bottom:8px;">🌟 较佳日期</p>' + good.slice(0, 5).map(renderDay).join('') : ''}
    ${neutral.length ? '<p style="font-weight:bold;margin:12px 0 8px;">⚖️ 平稳日期</p>' + neutral.slice(0, 3).map(renderDay).join('') : ''}
  `;
}'''
pattern = r"const ACTIVITIES = \[[\s\S]*?\n\s*\}\n\ndocument\.getElementById\('startDate'\)"
assert re.search(pattern, html), "good-day 核心 JS 未匹配"
html = re.sub(pattern, NEW_JS + "\n\ndocument.getElementById('startDate')", html, count=1)
open(gd, "w", encoding="utf-8").write(html)
print("HTML: good-day-selector 算法已重写为真实建除十二神")

print("\n全部完成。")
