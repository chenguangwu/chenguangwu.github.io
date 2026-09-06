# -*- coding: utf-8 -*-
"""清理 chinese 分类 HTML 硬编码套话。

① formula-desc 清理仅 3 页（chinese-character / chinese-radical-lookup / stroke-order-viewer）：
   占位「本速查内容依据权威标准与公开资料整理…工具名称：XX - 中华文化领域的在线工具。」→ 真实中文工具说明。
② tool-intro 三段块套话清理仅 3 页（chinese-character / chinese-culture / lunar-calendar）：
   通用科学套话「中华文化工具，传承国学经典」+ 功能(内容基于经典文献整理/搜索便捷…) + 场景(国学经典学习与查询…)
   → 真实中文工具功能特点 + 使用场景。
③ chinese-radical-lookup / stroke-order-viewer 无标准 tool-intro 三段块（仅有 deep-dive 区），保留；opt-guide/opt-faq 套话全 5 页均无，不需清。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "chinese")

# formula-desc 真实说明（替换整段占位）
FD = {
    "chinese-character": "汉字查询：输入单个汉字即时获取拼音、部首、总笔画数、字形结构与 Unicode / 输入法编码，纯前端本地解析，适合识字、查字典与规范书写核对。",
    "chinese-radical-lookup": "偏旁部首查询：按部首检索汉字，查看部首读音、笔画数及含该部首的常见字，依据《新华字典》部首检字法，纯前端本地查询。",
    "stroke-order-viewer": "笔画笔顺演示：输入汉字动态展示标准书写笔顺与逐笔动画，标注总笔画数与笔画名称，依据《现代汉语通用字笔顺规范》，纯前端本地渲染。",
}

# tool-intro 三段块真实内容（仅 chinese-character / chinese-culture / lunar-calendar）
INTRO = {
    "chinese-character": "汉字查询是一款纯前端离线工具，输入单个汉字即可获取拼音、部首、笔画数、字形结构与输入法编码，帮助识字、查字典与规范书写核对。",
    "chinese-culture": "中文文化工具箱汇集成语释义出处、古诗词检索、传统节日节气与姓名文化等国学小工具，纯前端本地查询，一站式了解汉字背后的语言文化与典故。",
    "lunar-calendar": "农历公历互转是一款纯前端离线工具，在农历与公历间双向换算日期，并可查传统节日、二十四节气与干支纪年，方便安排节庆、生日与农事参考。",
}

FEATURES = {
    "chinese-character": [
        "拼音与多音字：显示读音并标注多音字在不同语境下的释义",
        "部首笔画：给出部首与总笔画数，便于按部首检字法定位",
        "编码查询：提供 Unicode 与五笔 / 郑码等输入法编码，避免乱码缺字",
    ],
    "chinese-culture": [
        "成语典故：查释义、出处与近义反义，避免望文生义",
        "诗词检索：按作者、朝代、名句关键词检索并查看创作背景",
        "节令常识：查传统节日来源习俗与二十四节气物候含义",
    ],
    "lunar-calendar": [
        "双向换算：农历 ↔ 公历日期互转，内置闰月年份处理",
        "节日节气：标注春节端午中秋等节日与二十四节气",
        "干支纪年：显示对应干支年份，辅助传统择日参考",
    ],
}

SCENES = {
    "chinese-character": [
        "阅读遇生僻字：即时看拼音、部首与笔画，读懂读音与字形",
        "辅导作业：核对偏旁部首与笔画数，检查书写是否规范",
        "录入校对：确认生僻字码位与编码，避免选错同形字",
    ],
    "chinese-culture": [
        "写作演讲：选贴切成语并核对出处与语境",
        "节庆策划：查节日来源习俗与农历日期，安排活动",
        "文化学习：检索诗词背景与节气含义，辅助赏析",
    ],
    "lunar-calendar": [
        "农历生日：换算当年公历日期，提前安排聚会",
        "假期安排：查春节端午中秋对应公历，准备习俗",
        "节气参考：了解节气日期与物候，用于养生农事",
    ],
}


def repl_block(s, cls, new_lis):
    new_html = "<ul class=\"%s\">%s</ul>" % (cls, "".join("<li>%s</li>" % x for x in new_lis))
    pat = re.compile(r"<ul class=\"%s\">.*?</ul>" % cls, re.S)
    return pat.sub(new_html, s, count=1)


def process(dry=False):
    changed = []
    # ① formula-desc（含 <head> meta / JSON-LD 描述中同一占位句的回灌）
    for name, real in FD.items():
        f = os.path.join(TOOLS, name + ".html")
        s = open(f, encoding="utf-8").read()
        if "本速查内容依据权威标准与公开资料整理" not in s:
            print("  ⚠ formula-desc 无占位，跳过：%s" % name)
            continue
        new = re.sub(r"<p class=\"formula-desc\">.*?</p>",
                     "<p class=\"formula-desc\">%s</p>" % real, s, count=1, flags=re.S)
        # <head> 内 meta description / og:description / twitter:description / JSON-LD description
        # 同句占位回灌，整体替换为真实说明
        new = new.replace(
            "本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。",
            real,
        )
        if dry:
            print("  [dry] formula-desc → %s : %s" % (name, real[:40]))
        else:
            open(f, "w", encoding="utf-8").write(new)
            changed.append(f)
            print("  ✔ formula-desc 真实化：%s" % name)

    # ② tool-intro 三段块
    for name in INTRO:
        f = os.path.join(TOOLS, name + ".html")
        s = open(f, encoding="utf-8").read()
        need = ("中华文化工具，传承国学经典" in s) or ("内容基于经典文献整理" in s) or ("国学经典学习与查询" in s)
        if not need:
            print("  ⚠ tool-intro 无套话，跳过：%s" % name)
            continue
        if dry:
            print("  [dry] tool-intro → %s : 简介=%s" % (name, INTRO[name][:30]))
        else:
            # 简介 <p>
            new = re.sub(r"(<h4><span class=\"h4-icon\">📝</span>工具简介</h4>\s*<p>).*?(</p>)",
                         lambda m: m.group(1) + INTRO[name] + m.group(2), s, count=1, flags=re.S)
            # 功能 + 场景
            new = repl_block(new, "intro-features", FEATURES[name])
            new = repl_block(new, "intro-scenes", SCENES[name])
            open(f, "w", encoding="utf-8").write(new)
            changed.append(f)
            print("  ✔ tool-intro 真实化：%s" % name)

    return changed


def main():
    dry = "--dry" in sys.argv
    if dry:
        print("==== DRY 预览（不写盘）====")
    process(dry=dry)
    print("\n完成。" if not dry else "\nDry 完成，未写盘。")


if __name__ == "__main__":
    main()
