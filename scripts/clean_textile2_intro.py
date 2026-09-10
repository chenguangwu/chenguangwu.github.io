# -*- coding: utf-8 -*-
"""清理 textile2 4 个工具页 tool-intro-body 的 intro-scenes 通用默认占位
（日常办公文档处理/会议与项目管理/数据整理与汇总/团队协作辅助），
替换为真实纺织工程场景（第四处占位残留区，_build.py 不重建）。
"""
import os, re

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "textile2")

SCENES = {
  "dyeing-time.html": [
    "按排缸计划估算每缸染色总时长，核对交期与设备占用。",
    "制定多段升温工艺曲线，分色号录入保温与升温参数。",
    "复算升温速率是否满足限时要求，避免赶工导致色花。"
  ],
  "liquor-ratio.html": [
    "配缸前按织物重量与浴比核算总液量与加水量。",
    "把处方 owf% 换算成实际 g/L，统一大生产投料口径。",
    "小样放大时锁定 g/L 而非单纯保浴比，保证上色一致。"
  ],
  "dye-temp.html": [
    "按纤维与染料查染色温度区间，制定入染与保温工艺。",
    "核对升温速率与保温时间，避免初染过快产生色花。",
    "涤纶等高温品种确认是否需高温高压或载体法设备。"
  ],
  "color-fastness.html": [
    "出厂前按 GB/T 标准评定耐洗/摩擦/汗渍/唾液牢度。",
    "客诉时比对变色灰卡等级与 ΔE，判定是否达标。",
    "婴幼儿纺织品强制查耐唾液牢度是否≥4 级。"
  ]
}

OLD = re.compile(
    r"<ul class=\"intro-scenes\">.*?</ul>",
    re.DOTALL
)

for fn, items in SCENES.items():
    fp = os.path.join(BASE, fn)
    s = open(fp, encoding="utf-8").read()
    new = "<ul class=\"intro-scenes\">\n" + "".join(f"      <li>{t}</li>\n" for t in items) + "    </ul>"
    s2 = OLD.sub(new, s, count=1)
    assert s2 != s, f"{fn} 未找到 intro-scenes 占位"
    open(fp, "w", encoding="utf-8").write(s2)
    print("OK cleaned intro-scenes:", fn)
print("done")
