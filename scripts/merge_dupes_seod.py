#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO-D 待确认重复对补全合并：复用 p2d 重定向桩模式。

合并对象：DEV-PLAN SEO-D「待确认」清单经源码核对后判定为 merge 的 13 对真重复。
被合并文件（随机/模糊命名方）原地改写为 TOOLBOX-REDIRECT 桩，旧 URL 不丢、无死链。
规范命名方保留为 keeper（满功能工具页）。

未纳入本批：
- 3 对 separate（功能确实不同）：agriculture/calc-11<->machinery-efficiency、
  fishery/estimate-emission-wastewater<->wastewater-cod、safety/drill-timer<->assessor-drill
- 1 对 rename（命名 Bug，非重复）：process/pp-index<->ppk-index（改标题区分，见本脚本末尾说明）
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://chenguangwu.github.io"

# (被合并文件相对 tools/ 的路径, keeper 所在行业, keeper 文件名)
PAIRS = [
    ("encode/utf8-bytes.html", "encode", "utf-8.html"),
    ("construction/estimate-area-dosage-1.html", "construction", "soundproof-material.html"),
    ("food-testing/rater-risk.html", "food-testing", "allergen-cross-risk.html"),
    ("it/git-cheatsheet.html", "it", "git-commands.html"),
    ("pet/pet-food.html", "pet", "pet-feeding-calc.html"),
    ("design/color-scheme-generator.html", "design", "color-palette.html"),
    ("energy/calculator-calc-power.html", "energy", "standby-power-calculator.html"),
    ("it/sn-generator.html", "it", "serial-key-generator.html"),
    ("energy/calc-area-air.html", "energy", "air-purifier-area.html"),
    ("meteorology/wind-beaufort.html", "meteorology", "beaufort-scale.html"),
    ("hydraulic/estimate-18.html", "hydraulic", "calc-54.html"),
    ("construction/estimate-volume-load.html", "construction", "radiator-calculator.html"),
    ("legal/estimate-accident.html", "legal", "traffic-accident-compensation.html"),
]


def read_title(path):
    try:
        s = open(path, encoding="utf-8").read()
    except Exception:
        return "ToolBox"
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    return m.group(1).strip() if m else "ToolBox"


def main():
    done, skipped = [], []
    for rel_remove, k_ind, k_file in PAIRS:
        remove_path = os.path.join(ROOT, "tools", rel_remove)
        keeper_path = os.path.join(ROOT, "tools", k_ind, k_file)
        if not os.path.exists(remove_path):
            skipped.append(rel_remove + " (磁盘缺失,跳过)")
            continue
        if not os.path.exists(keeper_path):
            skipped.append(f"{rel_remove} -> keeper 缺失({k_ind}/{k_file}),跳过")
            continue
        title = read_title(keeper_path)
        url = f"{BASE}/tools/{k_ind}/{k_file}"
        stub = (
            "<!DOCTYPE html>\n"
            "<!-- TOOLBOX-REDIRECT -->\n"
            '<html lang="zh-CN">\n'
            "<head>\n"
            '<meta charset="UTF-8">\n'
            f'<meta http-equiv="refresh" content="0;url={url}">\n'
            f'<link rel="canonical" href="{url}">\n'
            '<meta name="robots" content="noindex,follow">\n'
            '<script src="/js/analytics.js" defer></script>\n'
            f"<title>{title}</title>\n"
            "</head>\n"
            "<body>\n"
            f'<p>页面已合并至 <a href="{url}">新地址</a>。</p>\n'
            f"<script>window.location.href='{url}';</script>\n"
            "</body>\n"
            "</html>\n"
        )
        with open(remove_path, "w", encoding="utf-8") as f:
            f.write(stub)
        done.append(f"{rel_remove} -> /tools/{k_ind}/{k_file}")
        print("REDIR:", rel_remove, "->", f"/tools/{k_ind}/{k_file}")
    print(f"\n完成：{len(done)} 个文件已替换为重定向桩；跳过 {len(skipped)} 个。")
    for s in skipped:
        print("SKIP:", s)


if __name__ == "__main__":
    main()
