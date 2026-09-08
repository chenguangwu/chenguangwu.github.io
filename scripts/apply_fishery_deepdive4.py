# -*- coding: utf-8 -*-
"""fishery 第三批（5 个修复后的壳工具）deep-dive 真实内容写入。

这 5 个工具原为共用"通用计算器"模板的壳（输出恒空），已由 scripts/fix_fishery_shells.py
重写为领域专用真实算法。本脚本为其补真实 deep-dive（示例数字来自修复后算法实测）：
  calc-power     电功率 P=V×I：220V×10A=2200W=2.2kW
  density-1     放养密度：1000尾/1亩=1000尾/亩≈1.5尾/m²
  estimate-23   增长估算：100×(1+20%)=120
  ratio-hormone 配比：100:50→最简2:1，占比200%，A是B的2倍
  temp-density  水温—饱和溶氧：25℃饱和约8.18mg/L，实测6.5→饱和度79.5%
用法：python3 scripts/apply_fishery_deepdive4.py --apply
"""
import os, json, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD_PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

CONTENT = {
    "fishery/calc-power": {
        "title": "用电功率计算",
        "scenarios": [
            "养殖户估算增氧机、水泵等设备的用电功率与电费",
            "核对铭牌电压/电流是否与线路容量匹配",
            "多台设备同时运行的合计功率核算"
        ],
        "examples": [
            {"title": "增氧机功率核算", "body": "输入电压 220 V、电流 10 A：功率 P = 220 × 10 = 2200 W = 2.2 kW。提示 1 kW = 1000 W，选配线缆与漏保须按功率留足余量。"}
        ],
        "faqs": [
            {"q": "功率怎么算？", "a": "直流或纯阻性负载功率 P = 电压 × 电流；异步电机等有功率因数，实际输入功率略高，估算时可先按 P=V×I 取整。"},
            {"q": "为什么要留余量？", "a": "启动电流常为额定数倍，且多台设备叠加易超线路负荷；选配开关、线缆与发电机应按总功率的 1.2~1.5 倍预留。"}
        ]
    },
    "fishery/density-1": {
        "title": "放养密度计算",
        "scenarios": [
            "新塘放苗前按面积规划总尾数",
            "评估当前密度是否超出水体承载",
            "分塘或并塘时的密度重算"
        ],
        "examples": [
            {"title": "常规放养密度", "body": "总尾数 1000 尾、面积 1 亩：放养密度 = 1000 / 1 = 1000 尾/亩，折合约 1.5 尾/m²（1 亩≈666.67 m²）。实际宜结合鱼种、规格与增氧能力综合确定。"}
        ],
        "faqs": [
            {"q": "放养密度怎么定？", "a": "由鱼种、目标规格、水深、增氧与换水能力共同决定；密度越高单产越高但风险越大，须匹配溶氧与排污能力。"},
            {"q": "尾/亩和尾/m² 怎么换算？", "a": "1 亩 ≈ 666.67 m²，尾/m² = 尾/亩 ÷ 666.67；小水体（如水箱）常用尾/m² 更直观。"}
        ]
    },
    "fishery/estimate-23": {
        "title": "增长估算计算",
        "scenarios": [
            "按增长率预估产量、体重或规模的未来值",
            "投苗量与预期增重后的总量测算",
            "对比不同增长率方案的结果差异"
        ],
        "examples": [
            {"title": "产量增长预估", "body": "基准值 100、增长率 20%：估算结果 = 100 × (1 + 20/100) = 120，增长量 20。适用于线性比例增长的快速测算。"}
        ],
        "faqs": [
            {"q": "适合什么场景？", "a": "适用于按固定百分比线性增长的情形，如估算投苗后按增重率得到的总量；复合增长应改用多次连乘。"},
            {"q": "负增长率怎么处理？", "a": "增长率填负值即可，例如 -10% 表示缩减 10%，结果 = 基准 ×(1-10%)。"}
        ]
    },
    "fishery/ratio-hormone": {
        "title": "配比与比例计算",
        "scenarios": [
            "药物/饲料添加剂的两种成分配比换算",
            "浓度或剂量之间的比例关系核对",
            "按最简整数比配制混合液"
        ],
        "examples": [
            {"title": "两种成分配比", "body": "数值 A=100、B=50：最大公约数 50，最简整数比 = 2:1；A 占 B 的 200%，即 A 是 B 的 2 倍。用于药剂或营养配比的快速折算。"}
        ],
        "faqs": [
            {"q": "最简整数比怎么来？", "a": "先求两数的最大公约数 g，再约分为 A/g : B/g；如 100:50 约分为 2:1。"},
            {"q": "占比和倍数有什么区别？", "a": "占比 = A/B×100%（相对 B 的百分量），倍数 = A/B（纯比值）；两者描述同一比例关系，表达角度不同。"}
        ]
    },
    "fishery/temp-density": {
        "title": "水温—饱和溶氧与饱和度",
        "scenarios": [
            "按水温估算该温度下的饱和溶氧参考值",
            "由实测溶氧算饱和度，判断溶氧是否充足",
            "高温季节夜间缺氧风险的快速评估"
        ],
        "examples": [
            {"title": "25℃ 溶氧饱和度", "body": "水温 25℃、实测溶氧 6.5 mg/L：该温度饱和溶氧约 8.18 mg/L，饱和度 = 6.5 / 8.18 × 100% ≈ 79.5%，属可接受区间；夜间与凌晨易继续下降，须关注。"}
        ],
        "faqs": [
            {"q": "饱和溶氧随温度怎么变？", "a": "随水温升高而下降（气体溶解度降低），因此夏季高温时更易缺氧，须加强增氧与巡塘。"},
            {"q": "饱和度多少算安全？", "a": "一般要求 ≥5 mg/L、饱和度尽量≥70%~80%；凌晨与高密度时是最易缺氧时段，建议留有余地。"}
        ]
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dd = json.load(open(DD_PATH, encoding='utf-8')) if os.path.exists(DD_PATH) else {}
    n_new = sum(1 for k in CONTENT if k not in dd)
    n_upd = sum(1 for k in CONTENT if k in dd)
    for k, v in CONTENT.items():
        dd[k] = v
    print("待写入条目: %d（新增 %d，覆盖 %d）" % (len(CONTENT), n_new, n_upd))
    if args.apply:
        json.dump(dd, open(DD_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print("已写入: %s" % DD_PATH)
    else:
        print("预览模式（加 --apply 落盘）")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
