#!/usr/bin/env python3
"""realize(outdoor): 清理 outdoor/analysis-spacing.html 的 area4 通用 intro-scenes 占位（日常办公与学习等 4 条），替换为真实攀岩场景。"""
import sys
import os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"

GENERIC = [
    "      <li>日常办公与学习</li>",
    "      <li>开发调试与数据处理</li>",
    "      <li>快速计算与格式转换</li>",
    "      <li>信息查询与参考</li>",
]
GENERIC_STR = "\n".join(GENERIC)

REPL = [
    "      <li>保护站挂片布点规划</li>",
    "      <li>多锚点受力分配核算</li>",
    "      <li>夹角因子与安全性评估</li>",
    "      <li>顶绳 / 先锋锚点校验</li>",
]

PATH = os.path.join(ROOT, "tools/outdoor/analysis-spacing.html")

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    with open(PATH, encoding="utf-8") as f:
        txt = f.read()
    if GENERIC_STR not in txt:
        print("[SKIP] 未找到通用占位块")
    elif dry:
        print("[DRY] 将替换为 ->")
        for l in REPL:
            print("       " + l.strip())
    else:
        txt2 = txt.replace(GENERIC_STR, "\n".join(REPL), 1)
        with open(PATH, "w", encoding="utf-8") as f:
            f.write(txt2)
        print("[DONE] area4 通用占位 -> 真实攀岩场景")
