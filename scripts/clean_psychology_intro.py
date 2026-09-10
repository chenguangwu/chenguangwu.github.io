#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 psychology 分类工具页 tool-intro-body 的 intro-scenes 通用占位（DEV-PLAN §4.5.4 第四处）。

仅替换 generator-20（哲学流派词云生成）与 random-12（认知偏差卡片）两页的
< ul class="intro-scenes"> 内 4 条通用占位项（日常办公与学习 / 开发调试与数据处理 /
快速计算与格式转换 / 信息查询与参考）为各自真实场景。

tester-3 的 opt-guide/opt-faq 为真实 VARK 内容（无占位套话），扫描属误报，不处理。
phq9-assessment 的「快速复核」为真实 FAQ 标题，误报，不处理。

用法:
    python3 scripts/clean_psychology_intro.py --dry
    python3 scripts/clean_psychology_intro.py
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENES = {
    "generator-20": [
        "梳理存在主义、功利主义、康德伦理等流派的核心主张与代表人物",
        "准备哲学入门分享或课程讲义时，快速生成各流派关键词词云",
        "写作或思辨中对照不同流派的世界观、价值排序与方法论",
        "用可视化词云辅助记忆流派特征与其经典代表作",
    ],
    "random-12": [
        "自我觉察日常决策中的启发式偏差（锚定、确认偏误、可得性偏差等）",
        "产品与运营设计防错时，识别并规避常见认知陷阱",
        "阅读新闻与论证时辨析信息被扭曲的来源与机制",
        "教学或分享中举例说明典型认知偏差，提升批判性思维",
    ],
}


def replace_scenes(text, items):
    """替换第一个 <ul class="intro-scenes">...</ul> 内的 <li> 列表。"""
    pat = re.compile(r'(<ul class="intro-scenes">).*?(</ul>)', re.S)
    new_list = "<ul class=\"intro-scenes\">\n" + "\n".join(
        "      <li>%s</li>" % it for it in items
    ) + "\n    </ul>"
    return pat.sub(lambda m: new_list, text, count=1)


def main():
    dry = "--dry" in sys.argv[1:]
    total = 0
    for base, items in SCENES.items():
        f = os.path.join(ROOT, "tools/psychology/%s.html" % base)
        t = open(f, encoding="utf-8").read()
        before = "日常办公与学习" in t
        new = replace_scenes(t, items)
        after = "日常办公与学习" in new
        total += int(before)
        if not dry:
            open(f, "w", encoding="utf-8").write(new)
        print("  %-16s 通用占位前=%s 后=%s%s" % (
            base, before, after, "（dry 未落盘）" if dry else ""))
    print("合计替换文件数: %d%s" % (total, "（dry-run）" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
