# -*- coding: utf-8 -*-
"""清理 chinese-cook 分类 HTML 硬编码套话。

① formula-desc 清理仅 4 页（cutting-sizes / ingredient-substitute / oil-temp / wok-heat）：
   占位「本速查内容依据权威标准与公开资料整理…工具名称：XX - …」→ 真实烹饪说明（含 <head> meta/JSON-LD 同句回灌）。
② tool-intro 场景套话清理仅 5 页（cutting-sizes / ingredient-substitute / oil-temp / sauce-ratio / wok-heat）：
   仅 <ul class="intro-scenes"> 为通用套话「日常生活中的计算需求/购物消费…」→ 真实烹饪使用场景（简介/功能已真实，不动）。
   estimate-16 无标准 tool-intro 三段块（deep-dive 由 content 驱动），保留不补。
③ opt-guide/opt-faq 套话清理仅 3 页（cutting-sizes / ingredient-substitute / oil-temp）：
   通用套话「工作与生活中的相关计算与查询。」含 JSON-LD FAQ + opt-guide <p> + opt-faq <dd> 三处同步→真实烹饪场景。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "chinese-cook")

# formula-desc 真实说明（替换整段占位 + meta 回灌）
FD = {
    "cutting-sizes": "切配尺寸对照：汇总中餐常见刀工（末、丁、丝、片、条、块）的标准毫米尺寸与适用菜品，纯前端本地查询，帮助规范切配、受热均匀。",
    "ingredient-substitute": "食材替代查询：收录中餐常见调味、香料、辅料的替代方案与替换比例，缺料或忌口时快速查找应急替换，纯前端本地查询。",
    "oil-temp": "油温烹饪指南：汇总中餐常见油温档位（三四成至九十成）的温度范围、油面特征与适用烹饪方式，纯前端本地查询，帮助判断火候油温。",
    "wok-heat": "火候控制指南：汇总中餐旺火、中火、小火、微火四档火力的火焰特征与适用烹饪方式，纯前端本地查询，掌握看菜下火的火候技巧。",
}

# tool-intro 真实使用场景（仅替换 intro-scenes，5 页）
SCENES = {
    "cutting-sizes": [
        "按菜谱下刀：对照标准尺寸切丝切块，避免大小不一、生熟不均",
        "备餐摆盘：统一切配尺寸提升宴席出品一致性与美观度",
        "学刀工带徒：用毫米尺寸量化「细丝/滚刀块」，减少模糊表达",
    ],
    "ingredient-substitute": [
        "临时缺料：如没淡奶油/黄油查替代与用量，避免半成品报废",
        "过敏忌口：查等价替代（蛋奶素、坚果等）保留菜品结构",
        "地域应季：用风味相近本地料替代缺货香料与时蔬",
    ],
    "oil-temp": [
        "滑炒上浆：三四成热下锅锁水嫩滑、不粘锅",
        "炸制定型：五六成热中温炸、升温逼油外酥里嫩",
        "爆香炝锅：七八成热入料即响、香气迸发不焦",
    ],
    "sauce-ratio": [
        "糖醋红烧：按比例批量换算保证每次口味一致",
        "凉拌多人份：按总量反推盐醋油辣用量、减少误差",
        "减盐减糖版：等比例下调并微调酸鲜，便于复刻",
    ],
    "wok-heat": [
        "爆炒绿叶菜：大火快翻保脆嫩、保翠绿",
        "煎鱼煎蛋：热锅温油中火定型、不粘皮",
        "炖卤煨汤：小火慢煮肉质酥烂、汤醇不糊底",
    ],
}

# opt 套话真实回答（含 JSON-LD/opt-guide <p>/opt-faq <dd> 三处同步）
OPT = {
    "cutting-sizes": "适用于家庭备餐、宴席拼盘与学刀工场景：按菜谱标准尺寸切配，保证食材受热均匀、成菜整齐美观；也适合餐饮新手量化刀工规格，减少「少许适量」的模糊操作。",
    "ingredient-substitute": "适用于烹饪临时缺料、家人过敏忌口或素食需求的场景：快速查找风味与质地相近的替代食材及替换比例，尽量还原原菜结构与口味，避免半成品报废。",
    "oil-temp": "适用于滑炒、炸制、爆香等不同技法的下料时机判断：对照油温档位（三四成至九十成）的温度与油面特征，选对火候让食材嫩滑酥香，避免外焦里生或油温过高发苦。",
}

PLACEHOLDER_FD = "本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。"
PLACEHOLDER_OPT = "工作与生活中的相关计算与查询。"


def repl_block(s, cls, new_lis):
    new_html = "<ul class=\"%s\">%s</ul>" % (cls, "".join("<li>%s</li>" % x for x in new_lis))
    pat = re.compile(r"<ul class=\"%s\">.*?</ul>" % cls, re.S)
    return pat.sub(new_html, s, count=1)


def process(dry=False):
    changed = []
    # ① formula-desc（+ meta 回灌）
    for name, real in FD.items():
        f = os.path.join(TOOLS, name + ".html")
        s = open(f, encoding="utf-8").read()
        if PLACEHOLDER_FD not in s:
            print("  ⚠ formula-desc 无占位，跳过：%s" % name)
            continue
        new = re.sub(r"<p class=\"formula-desc\">.*?</p>",
                     "<p class=\"formula-desc\">%s</p>" % real, s, count=1, flags=re.S)
        new = new.replace(PLACEHOLDER_FD, real)
        if dry:
            print("  [dry] formula-desc → %s : %s" % (name, real[:38]))
        else:
            open(f, "w", encoding="utf-8").write(new)
            changed.append(f)
            print("  ✔ formula-desc 真实化：%s" % name)

    # ② tool-intro 场景套话（仅 intro-scenes）
    for name, scenes in SCENES.items():
        f = os.path.join(TOOLS, name + ".html")
        s = open(f, encoding="utf-8").read()
        if "日常生活中的计算需求" not in s and "购物消费的比价与换算" not in s:
            print("  ⚠ tool-intro 场景无套话，跳过：%s" % name)
            continue
        if dry:
            print("  [dry] tool-intro 场景 → %s : %s" % (name, scenes[0][:30]))
        else:
            new = repl_block(s, "intro-scenes", scenes)
            open(f, "w", encoding="utf-8").write(new)
            changed.append(f)
            print("  ✔ tool-intro 场景真实化：%s" % name)

    # ③ opt-guide/opt-faq 套话（三处同步）
    for name, real in OPT.items():
        f = os.path.join(TOOLS, name + ".html")
        s = open(f, encoding="utf-8").read()
        if PLACEHOLDER_OPT not in s:
            print("  ⚠ opt 套话无，跳过：%s" % name)
            continue
        c = s.count(PLACEHOLDER_OPT)
        if dry:
            print("  [dry] opt 套话 → %s : %d 处 → %s" % (name, c, real[:30]))
        else:
            new = s.replace(PLACEHOLDER_OPT, real)
            open(f, "w", encoding="utf-8").write(new)
            changed.append(f)
            print("  ✔ opt 套话真实化：%s（%d 处）" % (name, c))

    return changed


def main():
    dry = "--dry" in sys.argv
    if dry:
        print("==== DRY 预览（不写盘）====")
    process(dry=dry)
    print("\n完成。" if not dry else "\nDry 完成，未写盘。")


if __name__ == "__main__":
    main()
