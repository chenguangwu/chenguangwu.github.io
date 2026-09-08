#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""food-safety（2 工具）deep-dive 由套话占位全量重写为真实内容。

数据源：i18n/tools/content_deepdive.json（_build.py 重建工具页时覆盖源 HTML 内联 deep-dive）。
算例数字按工具 JS 计分逻辑手算核对。
用法：python3 scripts/apply_food_safety_deepdive.py --apply
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

CONTENT = {
    "food-safety/assessor-risk-6": {
        "title": "微生物（致病菌）风险评估",
        "scenarios": [
            "出厂检验合规判定",
            "市场监管抽检风险分级",
            "企业品控批次放行",
        ],
        "examples": [
            {"title": "评分规则", "body": "依据 GB 29921-2021：沙门氏菌/O157 不得检出（检出各 +5）；金葡菌、李斯特、副溶血性弧菌 >100 CFU(MPN)/g 各 +3~4；菌落总数超类别限值（肉/水产 5×10⁴、乳/即食 1×10⁴）+2。合计 rs：0 安全、≤3 低风险、≤8 中风险、>8 高风险。"},
            {"title": "算例", "body": "即食食品：沙门0、金葡50、O157 0、李斯特0、弧菌0、菌落总数8000(≤1×10⁴) → rs=0，安全，合格。肉制品：沙门检出(+5)、李斯特250(+4)、金葡150(+3)、菌落总数6×10⁴(+2) → rs=14，高风险，批次不合格不得销售。"},
        ],
        "faqs": [
            {"q": "为何致病菌不得检出？", "a": "沙门氏菌、大肠埃希氏菌 O157 为致病菌零容忍，GB 29921 规定 n=0（25 g 不得检出），检出即判不合格。"},
            {"q": "菌落总数限值怎么分？", "a": "按食品类别：肉制品/水产制品 ≤5×10⁴ CFU/g，乳制品/即食食品 ≤1×10⁴ CFU/g；超限提示卫生状况不佳。"},
        ],
    },
    "food-safety/generator-31": {
        "title": "食品追溯编码生成",
        "scenarios": [
            "标签追溯码批量生成",
            "生产台账批次编码",
            "召回与溯源码管理",
        ],
        "examples": [
            {"title": "编码结构", "body": "追溯码 = GTIN(690+8位) − 批次(B+6位) − 日期(YYYYMMDD) − 流水(L+4位)，本地随机生成、不上传服务器。"},
            {"title": "算例", "body": "一次生成示例：69012345678-B120908-20260908-L0007；批量生成 n 条时每位流水递增，便于按码反向定位 GTIN/批次/生产日期，支撑正向追踪与反向追溯。"},
        ],
        "faqs": [
            {"q": "编码能当 GS1 正式条码吗？", "a": "本工具为本地演示编码，GTIN 前缀 690 为示例；正式商品条码须向 GS1 申请注册前缀，避免与市场码冲突。"},
            {"q": "数据会上传吗？", "a": "不会。编码在浏览器本地随机拼装，仅用于标签/台账辅助，不上传任何服务器。"},
        ],
    },
}

def main():
    apply = "--apply" in sys.argv
    d = json.load(open(SRC, encoding="utf-8"))
    for k, v in CONTENT.items():
        assert k in d, "条目缺失: " + k
        d[k] = v
    if apply:
        json.dump(d, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("已写入 %d 条" % len(CONTENT))
    else:
        print("[dry-run] 将写入 %d 条" % len(CONTENT))

if __name__ == "__main__":
    main()
