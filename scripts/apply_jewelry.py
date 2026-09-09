#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jewelry 分类 6 工具 deep-dive 真实化：替换第六型「快速复核」泛化模板。
范式对齐前述 apply 脚本：title/scenarios/examples/faqs 四字段覆盖，json.dump(indent=1) 保持仓库规范。
检测词（六型+弱模板）全规避。jewelry 为珠宝/贵金属换算类，算例基于真实标准与典型数字。
用法：--dry 仅校验；默认 --apply 写入 JSON。
"""
import json, re, sys

PATH = "i18n/tools/content_deepdive.json"

DATA = {
    "jewelry/convert-31": {
        "title": "黄金纯度换算（K 金 ↔ 千分比/百分比）",
        "scenarios": [
            "买金饰看 K 数或印记(如 Au916)，互算实际纯度。",
            "对比不同 K 金的含量与硬度取舍。",
        ],
        "examples": [
            {"title": "18K 纯度多少", "body": "纯度% = K数×4.1667；18K = 18×4.1667 ≈ 75%，即 Au750。24K 理论 100%，市售千足金记 999.9‰(99.99%)。"},
            {"title": "Au916 是几 K", "body": "916‰ ÷ 41.667 ≈ 22K，即 22K 金(纯度 91.6%)；常用于硬金与婚庆金饰。"},
        ],
        "faqs": [
            {"q": "K 和千分比怎么换？", "a": "1K ≈ 4.1667%(41.667‰)。K数×4.1667=百分比；千分比÷41.667≈K数。印记 Au750=18K、Au916=22K、Au999=24K(千足)。"},
        ],
    },
    "jewelry/diamond-carat": {
        "title": "钻石克拉与重量换算",
        "scenarios": [
            "克拉与「分」「克」互换，读懂证书重量。",
            "不同琢型(round/princess 等)对显大效果的影响。",
        ],
        "examples": [
            {"title": "0.5 克拉是多少分/克", "body": "1 克拉 = 0.2 克 = 100 分；0.5 克拉 = 50 分 = 0.1 克。即常说「50 分钻」即半克拉。"},
            {"title": "1 克拉显多大", "body": "圆钻 1ct 直径约 6.5mm；同重下公主方/椭圆视觉更大，垫形显小，选琢型也影响观感。"},
        ],
        "faqs": [
            {"q": "克拉和价格线性吗？", "a": "不。大克拉稀缺，单价随重量指数上升；同等级 1ct 单价远高于 0.9ct，整克拉是价格跳点。"},
        ],
    },
    "jewelry/gem-hardness": {
        "title": "宝石硬度对照（莫氏硬度）",
        "scenarios": [
            "按莫氏硬度判断宝石耐刮与佩戴场景。",
            "避免硬物混放互相刮花。",
        ],
        "examples": [
            {"title": "常见宝石硬度", "body": "钻石 10、红蓝宝(刚玉) 9、托帕石 8–8.5、石英 7–7.5、珍珠/珊瑚约 3–4（有机宝石软）。硬度差≥2 级才明显互刮。"},
            {"title": "为什么珍珠要单放", "body": "珍珠硬度仅 3–4，与金属或硬石同盒会被划伤；应软布分隔存放，远离 7 级以上宝石。"},
        ],
        "faqs": [
            {"q": "莫氏硬度是线性吗？", "a": "不是等比。10 级是 ordinal 排序，钻石(10)远超刚玉(9)的差距远大于 9 与 8 之间，仅表示能否互划伤。"},
        ],
    },
    "jewelry/gold-purity": {
        "title": "黄金纯金量计算（总重×千分比）",
        "scenarios": [
            "知首饰总重与印记千分比，算其中纯金重量。",
            "回收估价时核纯金含量。",
        ],
        "examples": [
            {"title": "10g 的 Au916 纯金多少", "body": "纯金量 = 总重 × 千分比/1000 = 10 × 916/1000 = 9.16 克。即 10 克 22K 金含纯金 9.16 克。"},
            {"title": "Au999 与 Au916 差", "body": "同重 10g，Au999 纯金 9.99g、Au916 纯金 9.16g，差 0.83g 纯金；纯度越高越软、越适合素金。"},
        ],
        "faqs": [
            {"q": "印记 Au750/Au916 什么意思？", "a": "Au 后数字是含金量千分比：Au750=75%(18K)、Au916=91.6%(22K)、Au999=99.9%(千足金)。"},
        ],
    },
    "jewelry/pearl-grading": {
        "title": "珍珠品质分级（光泽/瑕疵/形状/匹配）",
        "scenarios": [
            "按多维度给珍珠定级，判断价值。",
            "对比不同等级的外观差异。",
        ],
        "examples": [
            {"title": "等级 4/3/2/1 含义", "body": "以光泽为主、瑕疵形状匹配为辅：4 级最强光泽近乎镜面、5 无瑕级稀少；3 级强光泽微瑕；2 级中等；1 级弱光泽明显瑕。分级越高越稀有价高。"},
            {"title": "项链匹配度", "body": "多珠首饰额外看大小/色/光的匹配度；同串偏差小(匹配 4 级)比单珠等级更影响整体价。"},
        ],
        "faqs": [
            {"q": "光泽为什么最重要？", "a": "光泽(晕彩)是珍珠灵魂，强光泽可弥补微瑕；瑕疵不可逆但可被设计与镶嵌遮，故分级以光为先。"},
        ],
    },
    "jewelry/ring-size": {
        "title": "戒指尺寸换算（周长↔直径）",
        "scenarios": [
            "用软尺量指围算直径，对照圈号。",
            "不同国家尺码体系互转。",
        ],
        "examples": [
            {"title": "指围 55mm 对应直径", "body": "直径 = 周长 ÷ π = 55 ÷ 3.14159 ≈ 17.5mm。港码约 14 号(内圈 17.5mm)，欧码常标 55。"},
            {"title": "下午量更准", "body": "手指早晚/冷热胀缩约 ±0.5 号；建议下午温暖时量，取略紧不脱落为准，宽版戒需加半号。"},
        ],
        "faqs": [
            {"q": "港码和欧码怎么对？", "a": "欧码多直接标内圈周长(mm，如 55)；港码=内圈直径(mm)−? 约 14 号对应 17.5mm。各品牌有偏差，以实测内径为准。"},
        ],
    },
}

def main():
    apply = "--apply" in sys.argv
    d = json.load(open(PATH, encoding="utf-8"))
    fp = re.compile(r"统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板")
    weak = re.compile(r"先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|乘以 10%|两档复算|先用一组可复现输入|同一输入样本测试默认和边界情况")
    changed = 0
    for k, v in DATA.items():
        if k not in d:
            print("  SKIP 缺失:", k); continue
        d[k] = v
        changed += 1
    if apply:
        json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("APPLIED 写入 %d 条" % changed)
    else:
        print("DRY 拟写 %d 条" % changed)
    hit = [k for k in DATA if k in d and (fp.search(json.dumps(d[k], ensure_ascii=False)) or weak.search(json.dumps(d[k], ensure_ascii=False)))]
    print("泛化/弱模板残留:", hit if hit else "无(全清零)")

if __name__ == "__main__":
    main()
