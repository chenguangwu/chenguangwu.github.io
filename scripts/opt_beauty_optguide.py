# -*- coding: utf-8 -*-
"""清理 beauty 3 个工具页 opt-guide 内「如何使用」套话步骤，替换为真实用法说明；并清除 assessor-risk-12 参数说明中未渲染的模板串。"""
import re, glob, os

USAGE = {
    "assessor-risk-12": "逐项录入产品名称、产品类别与成分清单，工具按《化妆品安全技术规范》禁用/限用清单逐条比对，输出风险项与合规结论，可作为新品备案前的自查依据。",
    "analysis-detector-diagnosis": "将皮肤检测仪测得的水分、油分、色素、毛孔等数据逐条录入，工具对照分值区间判定干性/油性/混合性/敏感等肤质类型并给出护理方向。",
    "calc-1": "按问卷逐题选择当前皮肤状态（洁面后感觉、毛孔、敏感、痘痘、上妆、光泽等），提交后工具按加权规则给出皮肤类型与护理建议。",
}

n = 0
still = 0
for f in sorted(glob.glob("tools/beauty/*.html")):
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
    # 顺手清除 assessor-risk-12 参数说明里的未渲染模板串
    if base == "assessor-risk-12" and "+'(i+1)+'. '+item.q+'" in s:
        s3 = open(f, encoding="utf-8").read()
        s3 = s3.replace("+'(i+1)+'. '+item.q+'", "成分项（按清单逐项填写）")
        open(f, "w", encoding="utf-8").write(s3)
        print("CLEARED template str", base)
    if "在对应的输入框或选项中填写" in open(f, encoding="utf-8").read():
        still += 1
        print("STILL", base)

print("cleaned", n, "| still", still)
