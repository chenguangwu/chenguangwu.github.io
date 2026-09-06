# -*- coding: utf-8 -*-
"""清理 banking/fisher-real-rate 的 opt-guide 内「如何使用」套话，替换为真实用法说明。"""
import re, glob, os

USAGE = {
    "fisher-real-rate": "输入名义利率（如银行挂牌年利率）与预期通胀率，选择精确或近似口径，点击计算即可得到剔除通胀后的实际利率，用于判断购买力是否真正增长。",
}

n = 0
still = 0
for f in sorted(glob.glob("tools/banking/*.html")):
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
