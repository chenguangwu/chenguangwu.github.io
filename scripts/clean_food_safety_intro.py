#!/usr/bin/env python3
"""realize(food-safety): 清理 2 个工具页 area4 通用 intro-scenes 占位（日常办公与学习等 4 条），替换为真实食品检测场景。

- tools/food-safety/generator-31.html（食品（追溯）编码生成）
- tools/food-safety/summary.html（重金属（限量）汇总）
"""
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

REPL = {
    "tools/food-safety/generator-31.html": [
        "      <li>GS1-128 / SSCC 物流单元条码编码生成</li>",
        "      <li>批次号与生产的日期、产线组合编码</li>",
        "      <li>冷链追溯标签（GTIN + 批次 + 有效期）编排</li>",
        "      <li>出入库与分拣环节追溯码打印核对</li>",
    ],
    "tools/food-safety/summary.html": [
        "      <li>多元素限量合规比对（铅 / 镉 / 汞 / 砷 / 铬）</li>",
        "      <li>GB 2762 分类限量判定汇总</li>",
        "      <li>原料与成品检测报告归档对比</li>",
        "      <li>供应商多批次风险横向比对</li>",
    ],
}

def process(path, repl_lines, dry):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        txt = f.read()
    if GENERIC_STR not in txt:
        print(f"[SKIP] {path}: 未找到通用占位块")
        return 0
    new_block = "\n".join(repl_lines)
    if dry:
        print(f"[DRY] {path}: 将替换通用占位块为 ->")
        for l in repl_lines:
            print("       " + l.strip())
        return 1
    txt2 = txt.replace(GENERIC_STR, new_block, 1)
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(txt2)
    print(f"[DONE] {path}: area4 通用占位 -> 真实食品检测场景")
    return 1

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    for path, repl in REPL.items():
        process(path, repl, dry)
