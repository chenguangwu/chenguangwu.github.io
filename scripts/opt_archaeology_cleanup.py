# -*- coding: utf-8 -*-
"""清理 archaeology 6 个工具页的 formula-desc 套话，改写为真实用途说明。"""
import re, glob, os

# 各工具的 formula-desc 真实用途说明（替换整段）
FD_REPLACE = {
    "archaeology/artifact-measurement": "按考古测量规范录入遗物的长、宽、厚（cm）与重量（g），自动换算体积与密度，并计算形制指数，生成可归档的标准测量记录。所有计算在浏览器本地完成，数据不上传服务器。",
    "archaeology/dating-method": "对照碳-14、热释光、光释光、树轮、钾-氩等测年方法的适用范围、材料与精度，便于按出土样品选择手段并交叉校验。内容为依据公开考古文献整理，仅供学习参考。",
    "archaeology/pottery-typology": "按中国主要考古学文化期（仰韶、龙山、二里头、商周等）列出陶质、陶色、纹饰与典型器形，辅助田野陶片辨识与类型学归组。内容为依据公开考古文献整理，仅供学习参考。",
    "archaeology/site-grid": "根据遗址范围与探方规格（常用 5×5m 或 10×10m）计算探方数量、发掘面积与西南角坐标网格，生成探方编号方案。计算在浏览器本地完成，数据不上传服务器。",
    "archaeology/stats-density": "按探方或采样单元统计单位面积（m²）内出土遗物件数，计算遗物密度（件/m²）以对比各层位与文化堆积的丰富程度，辅助发掘记录。计算在浏览器本地完成。",
    "archaeology/stratum-identify": "对照地质时代与中国主要考古学文化期特征，辅助遗址地层划分、叠压—打破关系判定与相对年代定位。内容为依据公开考古文献整理，仅供学习参考。",
}

n = 0
for f in sorted(glob.glob("tools/archaeology/*.html")):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    key = "archaeology/" + base
    new = FD_REPLACE.get(key)
    if not new:
        continue
    s = open(f, encoding="utf-8").read()
    pat = re.compile(r'<p class="formula-desc">.*?</p>', re.S)
    if not pat.search(s):
        print("NO FD:", base)
        continue
    s2 = pat.sub('<p class="formula-desc">' + new + "</p>", s, count=1)
    open(f, "w", encoding="utf-8").write(s2)
    n += 1
    print("OK:", base)

print("cleaned", n)
