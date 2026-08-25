#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2c 跨目录/错标 industry 的真实同描述重复合并（按磁盘真实路径）。
loser 文件多带有与所在目录不符的 industry 元数据（如 pr/ 下 meta=marketing），
合并后这些错标条目随之消失。保留更完整/命名更清晰的一方为 keeper。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://chenguangwu.github.io"

# (被合并文件真实相对路径, keeper 所在行业, keeper 文件名)
PAIRS = [
    ("pr/sentiment-analysis.html", "ai", "sentiment-analysis.html"),
    ("procurement/delivery-rate.html", "procurement", "stats-on-time-qualified.html"),
    ("agriculture/greenhouse-monitor.html", "agriculture", "recorder-humidity.html"),
    ("textile/cutting-layout.html", "textile", "cutting-1.html"),
    ("textile/fabric-usage.html", "textile", "estimate-dosage-fabric-qty.html"),
    ("procurement/total-cost.html", "procurement", "cost.html"),
    ("quality/aql-sampling.html", "quality", "table-sampling.html"),
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
            '<script src="/js/clarity.js" defer></script>\n'
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
