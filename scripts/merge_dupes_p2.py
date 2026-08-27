#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 工具去重：把同目录内的高置信度重复文件替换为重定向桩（TOOLBOX-REDIRECT）。

规则：
- 仅处理「同目录、不同文件名、描述完全相同」且一方为明显自动编号/劣质命名的重复。
- 被合并方原地改写为重定向桩，指向规范文件；旧 URL 不丢 SEO。
- _build.py / _audit_links 会跳过含 TOOLBOX-REDIRECT 的文件。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = "https://chenguangwu.github.io"

# (被合并文件相对 tools/ 的路径, 规范文件同目录下的文件名)
PAIRS = [
    ("ai/ai-2.html", "cross-entropy.html"),
    ("ai/ai-3.html", "lr-decay.html"),
    ("it/qrcode-generator.html", "qrcode.html"),
    ("life/converter.html", "unit-converter.html"),
    ("eco/eco-2.html", "noise-addition.html"),
    ("eco/eco-13.html", "ecological-footprint.html"),
    ("geology/assessor-32.html", "hazard.html"),
    ("healthcare/bmi.html", "bmi-calculator.html"),
    ("healthcare/bsa.html", "bsa-calculator.html"),
    ("fun/recorder-heatmap.html", "keyboard-heatmap.html"),
]


def read_title(path):
    try:
        s = open(path, encoding="utf-8").read()
    except Exception:
        return "ToolBox"
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    return m.group(1).strip() if m else "ToolBox"


def main():
    done = []
    for rel_remove, canonical in PAIRS:
        ind = rel_remove.split("/", 1)[0]
        remove_path = os.path.join(ROOT, "tools", rel_remove)
        canonical_path = os.path.join(ROOT, "tools", ind, canonical)
        if not os.path.exists(remove_path):
            print("SKIP (missing):", rel_remove)
            continue
        if not os.path.exists(canonical_path):
            print("SKIP (canonical missing):", canonical_path)
            continue
        title = read_title(canonical_path)
        url = f"{BASE}/tools/{ind}/{canonical}"
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
            f'<p>页面已迁移至 <a href="/tools/{ind}/{canonical}">新地址</a>。</p>\n'
            f"<script>window.location.href='{url}';;;;</script>\n"
            "</body>\n"
            "</html>\n"
        )
        with open(remove_path, "w", encoding="utf-8") as f:
            f.write(stub)
        done.append(rel_remove)
        print("REDIR:", rel_remove, "->", f"/tools/{ind}/{canonical}")
    print(f"\n完成：{len(done)} 个文件已替换为重定向桩。")


if __name__ == "__main__":
    main()
