# -*- coding: utf-8 -*-
"""清理 archive 工具页的 formula-desc 套话，改写为真实用途说明。convert-ref-cite 无 FD 套话自动跳过。"""
import re, glob, os

FD_REPLACE = {
    "archive/stats-report": "输入台账或明细数据，自动汇总总件数、各类型数量与占比，并按利用率=利用件次÷总件数×100% 计算活跃度，支持按年度、类型、机构等维度交叉汇总。计算在浏览器本地完成，数据不上传服务器。",
    "archive/generator-label": "依据档案盒规格与脊背字数，按全宗号、年度、机构、起止件号、盒号等字段生成可批量打印的盒脊标签排版，字号随盒型厚度（30/40/50mm）自动调整。结果可直接复制使用，数据不离开浏览器。",
}

n = 0
for f in sorted(glob.glob("tools/archive/*.html")):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    key = "archive/" + base
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
