import os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
CAT = "food-testing"
OLD = '''    <ul class="intro-scenes">
      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>
    </ul>'''

# 各文件真实食品检测使用场景，替换通用 intro
SCEN = {
    "convert-36": [
        "油脂酸价/过氧化值实验室滴定数据换算与记录",
        "煎炸油品质监控与废弃判定",
        "食品标签营养与保质期评估",
        "教学演示油脂氧化程度计算",
    ],
    "convert-37": [
        "食品蛋白质含量按不同换算系数折算",
        "动植物源食品含氮量折算蛋白质",
        "配方与营养标签蛋白声称核算",
        "教学演示凯氏定氮计算",
    ],
    "generator-27": [
        "出厂与抽检平板计数报告生成",
        "生熟食品微生物限量符合性判定",
        "冷链与卫生监控趋势记录",
        "教学演示菌落计数与报告",
    ],
}

for base, scenes in SCEN.items():
    path = f"{ROOT}/tools/{CAT}/{base}.html"
    with open(path, encoding="utf-8") as f:
        t = f.read()
    assert OLD in t, f"{base}: 未找到通用 intro-scenes 块"
    new = '    <ul class="intro-scenes">\n' + "\n".join(f"      <li>{s}</li>" for s in scenes) + "\n    </ul>"
    t2 = t.replace(OLD, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(t2)
    print(f"OK: {base} intro-scenes 已替换为 {len(scenes)} 条真实场景")
