# -*- coding: utf-8 -*-
"""清理 automotive 7 个工具页 opt-guide 内「如何使用」套话步骤（在对应的输入框或选项中填写…），替换为真实用法说明。保留参数说明与适用场景。"""
import re, glob, os

USAGE = {
    "brake-pad-life": "输入新片厚度、当前厚度、已行驶里程与年均里程，选择刹车片类型、驾驶环境与位置，点击计算即可得到剩余可用里程与建议更换时点。",
    "calc-1": "输入目标车速、整备质量、发动机最大功率与传动效率，点击计算即可得到 0–100km/h 加速时间估算。",
    "cycle-belt": "选择车型并输入当前里程、上次更换里程与年均里程，点击计算即可得到正时皮带剩余更换里程与到期提醒。",
    "fuel-anomaly": "逐次录入加油日期、里程、加油量与油价，点击计算即可自动算出各期油耗并标出异常波动。",
    "pressure-fuel-oil": "输入喷油嘴流量、额定与实际轨压、喷油脉宽、缸数、转速、排量与充气效率，点击计算即可评估喷油量与实际轨压匹配。",
    "tire-wear": "输入新胎花纹深度与已行驶里程，选择轮胎档次、四轮定位状况、路况与驾驶习惯，点击计算即可估算磨损速率与剩余寿命。",
    "voltage-1": "输入发电机额定电流、系统电压、电池充电电流，并逐条添加用电器名称与电流，点击计算即可判断是否超额并提示是否需要增发电。",
}

n = 0
still = 0
for f in sorted(glob.glob("tools/automotive/*.html")):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    real = USAGE.get(base)
    if not real:
        continue
    s = open(f, encoding="utf-8").read()
    pat = re.compile(r'(<h2>如何使用[^<]*</h2>)\s*<ol>.*?</ol>', re.S)
    if pat.search(s):
        s2 = pat.sub(lambda m: m.group(1) + "<p>" + real + "</p>", s, count=1)
        open(f, "w", encoding="utf-8").write(s2)
        n += 1
        print("OK", base)
    else:
        print("NO MATCH", base)
    if "在对应的输入框或选项中填写" in open(f, encoding="utf-8").read():
        still += 1
        print("STILL", base)

print("cleaned", n, "| still", still)
