#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 content_deepdive.json 的 eco 段补 4 个缺失键。

缺失页：carbon-offset / convert-air-aqi / recycling-guide / waste-calculator
（这 4 页历史上未纳入 i18n 管道，故无 deep-dive 键。）

保持该文件自定义格式（顶层键 1 空格缩进），用精确文本插入，不做 json.dump 重写。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "i18n/tools/content_deepdive.json")
ANCHOR = ' "eco/afforestation-cost": {'

ENTRIES = [
    (
        "eco/carbon-offset",
        {
            "title": "碳足迹计算与抵消",
            "scenarios": [
                "个人年度盘点：录入通勤里程、用电用气、饮食结构与消费次数，定位排放大头。",
                "家庭减排对比：把燃油车换成电动车、少飞一次后再算一遍，量化年减排量。",
                "组织低碳宣导：以月度估算作为员工低碳活动的基线，展示植树与光伏抵消方案。",
            ],
            "examples": [
                {
                    "title": "可复现算例：一次日常排盘",
                    "body": "输入：私家车 500 km/月、公交 200 km/月、月用电 200 kWh、天然气 20 m³、饮食「少量肉食」、外卖 10 次/月、购物 5 单/月、新衣 8 件/年。\n交通=500×0.192+200×0.089=96+17.8=113.8 kg；能源=200×0.583+20×2.04=116.6+40.8=157.4 kg；\n饮食=250/12≈20.8 kg；外卖=10×1.5=15 kg；购物=5×5=25 kg；衣物=8×25/12≈16.7 kg；\n月度合计≈348.7 kg，年约 4.18 t → 判为「较为环保，符合全球平均」。抵消估算：需植树 ceil(4184/21)≈200 棵，或装 ceil(4184/1300)≈4 kW 光伏。",
                }
            ],
            "faqs": [
                {
                    "q": "抵消要种多少棵树？",
                    "a": "按一棵树年吸收约 21 kg CO₂ 折算；也可按 1 kW 光伏年减约 1300 kg 折算成装机容量。两者均为公开经验系数，仅供方案估算与科普，正式核算以 GHG Protocol 与实测数据为准。",
                },
                {
                    "q": "哪一类排放通常最大？",
                    "a": "多数城市家庭中交通与电力占大头：私家车 0.192 kg/km、短途航班 0.255 kg/km 远高于公交 0.089 kg/km；饮食从高肉降到少肉每年还可再减数百千克。",
                },
                {
                    "q": "结果能直接用于碳核查吗？",
                    "a": "不能。本工具用通用排放因子做粗略估算，覆盖交通/能源/饮食/消费四类，家庭差异较大；对外披露或交易请使用官方方法学与经核证的因子。",
                },
            ],
            "summary": "按交通、能源、饮食与消费四类排放因子估算月度/年度碳足迹，并给出植树、光伏与行为减排建议。",
        },
    ),
    (
        "eco/convert-air-aqi",
        {
            "title": "空气质量指数（AQI）类别换算",
            "scenarios": [
                "解读监测日报：把 PM2.5 24h 浓度换算成 AQI，快速看懂污染等级与健康提示。",
                "数据展示：为环境大屏或报表把浓度序列转成 AQI 数值与对应色阶。",
            ],
            "examples": [
                {
                    "title": "可复现算例：PM2.5 35 µg/m³",
                    "body": "浓度 35 落在断点档 [12.1, 35.4] → [51, 100]。\nAQI=(100−51)/(35.4−12.1)×(35−12.1)+51=49/23.3×22.9+51≈48.2+51=99.2 → 四舍五入 99，属「良」。\n若浓度取 150，落在 [55.5, 150.4] → [151, 200]：AQI=(200−151)/(150.4−55.5)×(150−55.5)+151≈49/94.9×94.5+151≈199.8 → 200，属「中度污染」。",
                }
            ],
            "faqs": [
                {
                    "q": "用的是哪套断点表？",
                    "a": "US EPA 的 PM2.5 24 小时分段线性断点表。中国 HJ 633-2012 的 PM2.5 档位不同（如 0–35 为优），同一浓度换算出的 AQI 会有差异，请按用途选择口径。",
                },
                {
                    "q": "为什么浓度很高时显示「超标(>500)」？",
                    "a": "断点表上限为 500.4 µg/m³，更高浓度已超出表内范围，工具不再外推而直接标记超标，避免给出无依据的数值。",
                },
            ],
            "summary": "按 US EPA 分段线性断点，把 PM2.5 24h 浓度换算为 AQI 与污染类别。",
        },
    ),
    (
        "eco/recycling-guide",
        {
            "title": "垃圾分类指南",
            "scenarios": [
                "居家分类：拿到一件垃圾拿不准投哪一类时，输入关键词秒查归属。",
                "社区宣教：向居民演示四分类归属与常见易错物品的投放要点。",
                "活动筹备：布置分类回收点时，核对某类物品是否属于可回收物。",
            ],
            "examples": [
                {
                    "title": "可复现查询：塑料瓶与电池",
                    "body": "输入「塑料瓶」→ 命中「可回收物」，投放要点为清空残液、压扁投放。\n输入「电池」→ 命中「有害垃圾」，需送有害垃圾收集点，切勿混入其他垃圾或厨余。\n输入「剩菜」→ 命中「厨余垃圾」，需沥干水分后投放。",
                }
            ],
            "faqs": [
                {
                    "q": "收录了多少物品？查不到怎么办？",
                    "a": "内置常见生活垃圾词条，支持关键词模糊匹配。查不到时按顺序判断：是否有毒有害 → 是否可回收 → 是否易腐烂 → 其余归入其他垃圾。",
                },
                {
                    "q": "各地标准不同，以哪个为准？",
                    "a": "词条按中国生活垃圾四分类（可回收物/有害垃圾/厨余垃圾/其他垃圾）整理，属通用口径；上海、北京等地细则与叫法略有差异，实际投放以当地规定为准。",
                },
            ],
            "summary": "搜索常见生活垃圾的归属类别与投放建议，按四分类口径整理。",
        },
    ),
    (
        "eco/waste-calculator",
        {
            "title": "垃圾产生量计算器",
            "scenarios": [
                "家庭自查：按人口与生活习惯估算月度垃圾量，并与人均 1–1.2 kg/天对照。",
                "减量规划：对比减少外卖、合并快递后包装垃圾的下降幅度。",
                "社区宣传：用不同参数演示一次性餐具与衣物消费对垃圾量的影响。",
            ],
            "examples": [
                {
                    "title": "可复现算例：3 人城区家庭",
                    "body": "输入：3 人、城区、每周多次做饭、偶尔剩菜、外卖 3 次/月、快递 2 件/月、偶尔用一次性餐具、少量添衣。\n基础量=3×1.2×(1+0)=3.6 kg；食品残渣=3×(1.5+0.3)×30=162 kg；\n包装=(3×4×0.4)+(2×4×0.15)=4.8+1.2=6 kg；一次性=3×1.0×30=90 kg；衣物=5 kg；\n月度合计≈266.6 kg，年约 3.20 t，人均≈2.92 kg/天 → 判为「偏高，需要减少」。减少外卖与一次性餐具是最直接的降量手段。",
                }
            ],
            "faqs": [
                {
                    "q": "人均多少算正常？",
                    "a": "中国人均生活垃圾约 1–1.2 kg/天。低于 1.0 显示环保良好，1.0–1.5 提示接近平均，高于 1.5 提示需减量。",
                },
                {
                    "q": "哪几项对结果影响最大？",
                    "a": "按系数看，一次性餐具高档为 2.0 kg/人/天、餐餐做饭为 2.5 kg/人/天，二者对总量影响最大；外卖与快递按次数线性累加，减少频次见效快。",
                },
            ],
            "summary": "按人口与做饭、外卖、快递、一次性用品、衣物等习惯估算家庭月度垃圾产生量并给出减量建议。",
        },
    ),
]


def dump_entry(key, obj) -> str:
    """按文件既有缩进（键 1 空格、字段 2 空格、数组项 3、内层对象 4…）生成文本。"""
    out = [' "%s": {' % key]
    out.append('  "title": %s,' % json.dumps(obj["title"], ensure_ascii=False))
    out.append('  "scenarios": [')
    for i, s in enumerate(obj["scenarios"]):
        out.append('   %s%s' % (json.dumps(s, ensure_ascii=False), ',' if i < len(obj["scenarios"]) - 1 else ''))
    out.append('  ],')
    out.append('  "examples": [')
    for i, e in enumerate(obj["examples"]):
        out.append('   {')
        out.append('    "title": %s,' % json.dumps(e["title"], ensure_ascii=False))
        out.append('    "body": %s' % json.dumps(e["body"], ensure_ascii=False))
        out.append('   }%s' % (',' if i < len(obj["examples"]) - 1 else ''))
    out.append('  ],')
    out.append('  "faqs": [')
    for i, f in enumerate(obj["faqs"]):
        out.append('   {')
        out.append('    "q": %s,' % json.dumps(f["q"], ensure_ascii=False))
        out.append('    "a": %s' % json.dumps(f["a"], ensure_ascii=False))
        out.append('   }%s' % (',' if i < len(obj["faqs"]) - 1 else ''))
    out.append('  ],')
    out.append('  "summary": %s' % json.dumps(obj["summary"], ensure_ascii=False))
    out.append(' },')
    return '\n'.join(out)


def main() -> int:
    apply = "--apply" in sys.argv
    raw = open(P, encoding="utf-8").read()
    data = json.loads(raw)
    existing = [k for k, _ in ENTRIES if k in data]
    if existing:
        print("已存在，跳过:", existing)

    block = "\n".join(dump_entry(k, v) for k, v in ENTRIES if k not in data)
    if not block:
        print("无需写入")
        return 0

    idx = raw.find(ANCHOR)
    if idx < 0:
        print("未找到锚点，终止")
        return 1
    new = raw[:idx] + block + "\n" + raw[idx:]

    chk = json.loads(new)
    for k, v in ENTRIES:
        assert chk.get(k) == v, "内容不一致: " + k
    print("新增键: %s | eco 段旧键 %d -> 新键 %d | 非 eco 段键数不变: %s" % (
        ", ".join(k for k, _ in ENTRIES if k not in data),
        len([k for k in data if k.startswith("eco/")]),
        len([k for k in chk if k.startswith("eco/")]),
        len([k for k in data if not k.startswith("eco/")]) == len([k for k in chk if not k.startswith("eco/")]),
    ))
    if apply:
        open(P, "w", encoding="utf-8").write(new)
        print("已落盘")
    else:
        print("预览（加 --apply 落盘）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
