# -*- coding: utf-8 -*-
"""清理 civil 分类 HTML 硬编码套话。

探查结论：civil 全部 21 工具页**均无标准 tool-intro 三段块**（其「常见使用场景/FAQ」由已真实化的 content_deepdive 驱动），故不清理 tool-intro。
① formula-desc 清理仅 1 页（rock-mass-rating）：占位变体「本工程计算基于标准物理与材料公式…」→ 真实岩土说明（含 <head> meta/JSON-LD 同句回灌）。
② opt-guide/opt-faq 套话清理仅 2 页（cft-capacity / excavation-earth）：通用套话「工作与生活中的相关计算与查询。」含 JSON-LD FAQ + opt-guide <p> + opt-faq <dd> 三处同步→真实工程场景。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "civil")

# formula-desc 真实说明（替换整段占位 + meta 回灌）
FD = {
    "rock-mass-rating": "围岩分级评分 RMR 计算：按岩石单轴强度、RQD、节理间距、节理条件、地下水五项评分求和并作走向修正，得 RMR 定围岩级别，纯前端本地计算，用于隧道洞室支护设计。",
}

# opt 套话真实回答（含 JSON-LD/opt-guide <p>/opt-faq <dd> 三处同步）
OPT = {
    "cft-capacity": "适用于高层与桥梁重载柱的轴压承载力快速估算：输入钢管直径、壁厚、钢材与混凝土等级，得组合轴压承载力并对比 RC 柱，辅助截面比选；正式设计仍须按规范公式与构造要求复核。",
    "excavation-earth": "适用于地下室、地铁等深基坑支护设计的土压力估算：输入土层参数、墙高与超载，得作用在排桩/地连墙上的土压力分布与合力，辅助支撑轴力与嵌固深度；水土分合算按土质选取。",
}

PLACEHOLDER_FD = "本工程计算基于标准物理与材料公式，输入为标准工程单位，结果仅供参考。"
PLACEHOLDER_OPT = "工作与生活中的相关计算与查询。"


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
            print("  [dry] formula-desc → %s : %s" % (name, real[:36]))
        else:
            open(f, "w", encoding="utf-8").write(new)
            changed.append(f)
            print("  ✔ formula-desc 真实化：%s" % name)

    # ② opt-guide/opt-faq 套话（三处同步）
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
