#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_labels_batch5.py — 前缀字典第五批（report10 残留的安全 2 字标签，末批）

策略：
- 只收 2 字键，且经 report10 残留核验：无「拉丁紧接无空格」(Latin-direct-after) garble 风险、
  无未配对中文复合词。
- 排除：红外/佩戴/完整（Latin-direct garble）、三星/小米/华为/一加（产品名）、
  文分/分词/试文/试中/词效/词测（打字样本）、足金/购物/输入/高于/电机/较新/每月（OUTPUT/句子/碎片）、数组（代码碎片）。
- 译文零中文校验；不引入尾随空格（这些键的后续字符均为 冒号/（/空格/数字，不会 Latin 紧接）。
运行：python3 _en-i18n/gen_labels_batch5.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = os.path.join(ROOT, "i18n/tools/en/_prefix.json")

B = {
    "尺寸": "Size",
    "个税": "Personal tax",
    "波长": "Wavelength",
    "焦深": "Depth of focus",
    "铸铁": "Cast iron",
    "焊丝": "Welding wire",
    "高碳": "High carbon",
    "月增": "Monthly increase",
    "推荐": "Recommended",
    "设计": "Design",
    "判定": "Judgment",
    "过剩": "Excess",
    "卡诺": "Carnot",
    "移位": "Shift",
    "斜率": "Slope",
    "预览": "Preview",
    "耗时": "Elapsed",
    "大小": "Size",
    "编码": "Encoding",
    "压强": "Pressure",
    "质量": "Mass",
    "速度": "Velocity",
    "比容": "Specific volume",
    "动能": "Kinetic energy",
    "功率": "Power",
    "误差": "Error",
}

def main():
    pf = json.load(open(PREFIX, encoding="utf-8"))
    orig = len(pf)
    added = 0
    bad = []
    for k, v in B.items():
        if k in pf:
            continue
        if any("\u4e00" <= c <= "\u9fff" for c in v):
            bad.append((k, v))
            continue
        pf[k] = v
        added += 1
    if bad:
        print("REJECTED (contains CJK):", bad)
        sys.exit(1)
    json.dump(pf, open(PREFIX, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    open(PREFIX, "a").write("\n")
    print(f"added {added} (total {orig} -> {len(pf)}); zero-CJK check passed")

if __name__ == "__main__":
    main()
