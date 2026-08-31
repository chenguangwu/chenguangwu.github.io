#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2d 残留重复合并：复用 P2b 重定向桩模式。

仅合并「SEO-D 高置信重复 + 被合并方为随机/混乱文件名、规范命名方含深度解析模块」的
真重复对（17 对）。被合并文件原地改写为 TOOLBOX-REDIRECT 桩，旧 URL 不丢、无死链。
磁盘缺失文件自动跳过。

未纳入本批（功能可能不同，需人工确认）的对见 DEV-PLAN SEO-D 待确认清单：
- agriculture/calc-11.html <-> agriculture/machinery-efficiency.html (对比 vs 成本)
- encode/utf-8.html <-> encode/utf8-bytes.html (编码 vs 字节)
- construction/estimate-area-dosage-1.html <-> construction/soundproof-material.html (面积剂量 vs 隔音)
- 以及 15 个双方均为规范命名、仅差后缀的「需确认」对（见 json/seo_d_dup_candidates.json review 段）。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://chenguangwu.github.io"

# (被合并文件相对 tools/ 的路径, keeper 所在行业, keeper 文件名)
PAIRS = [
    ("cardiology/calc-2.html", "cardiology", "chads2-vasc.html"),
    ("food-processing/tester-5.html", "food-processing", "emulsion-stability.html"),
    ("dentistry/ratio-13.html", "dentistry", "alveolar-bone-loss.html"),
    ("hematology/assessor-4.html", "hematology", "iron-overload.html"),
    ("nephrology/rater-15.html", "nephrology", "vascular-calcification.html"),
    ("dentistry/quankouyichi-heweiguanxi-zhuanyi.html", "dentistry", "complete-denture.html"),
    ("gastroenterology/assessor-9.html", "gastroenterology", "intestinal-metaplasia.html"),
    ("dentistry/kouqiangkuiyang-afuta-fenqi.html", "dentistry", "oral-ulcer.html"),
    ("dentistry/estimate-27.html", "dentistry", "bruxism-force.html"),
    ("agriculture/calc-4.html", "agriculture", "greenhouse-rolling-time.html"),
    ("agriculture/calc-3.html", "agriculture", "continuous-cropping-index.html"),
    ("it/calc-6.html", "it", "regex.html"),
    ("beauty/self-assess-1.html", "beauty", "skin-tewl.html"),
    ("agriculture/calc-14.html", "agriculture", "crop-water-requirement.html"),
    ("agriculture/calc-5.html", "agriculture", "greenhouse-ventilation.html"),
    ("sales/calc-1.html", "sales", "commission-calculator.html"),
    ("procurement/calc-15.html", "procurement", "eoq.html"),
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
