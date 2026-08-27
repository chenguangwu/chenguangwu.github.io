#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2b 跨目录同描述重复合并：保留更完整/文件名更清晰的一方（keeper），
其余同描述文件原地改写为重定向桩（TOOLBOX-REDIRECT），旧 URL 不丢、无死链。

磁盘已缺失的文件视为「此前已删除」，自动跳过（重建 tools.json 会同步剔除其陈旧条目）。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://chenguangwu.github.io"

# (被合并文件相对 tools/ 的路径, keeper 所在行业, keeper 文件名)
PAIRS = [
    # 样本量
    ("marketing/sample-size.html", "marketing", "sample-size.html"),
    # 百分位数
    ("statistics/statistics-14.html", "science", "percentile-calculator.html"),
    # 拉伸动作随机生成器
    ("fitness/generator-random-motion.html", "health", "stretch-generator.html"),
    # 成绩计算器
    ("exam/score-calculator.html", "edu", "grade-calculator.html"),
    # 置信区间
    ("marketing/confidence-interval.html", "stats", "confidence-interval.html"),
    # 正则（it/regex.html 为最完整版，另两个指向它）
    ("it/regex-tester.html", "it", "regex.html"),
    ("edu/tester.html", "it", "regex.html"),
    # 旋转功率
    ("energy/rotational-power.html", "dynamics", "power-rotational.html"),
    # PV = FV/(1+r)^t
    ("banking/discount-lump.html", "economics", "present-value.html"),
    # 欧姆定律
    ("science/calc-3.html", "electronics", "ohms-law.html"),
    # 课程表冲突
    ("edu/detector-1.html", "edu2", "schedule-conflict.html"),
    # 雨水收集（同目录 eco 内去重，保留清晰命名）
    ("eco/eco-12.html", "eco", "rainwater-harvest.html"),
    # 雨水收集（跨目录 energy/calc-area 亦为同描述，合并到 eco 规范页）
    ("energy/calc-area.html", "eco", "rainwater-harvest.html"),
    # 睡眠周期
    ("fitness/calculator-calc-cycle.html", "health", "sleep-cycle-calculator.html"),
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
