#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 agriculture 源 html 中可见旧套话（三处同清之一：可见 opt 区块 + formula-desc）。
- 第一阶段：含"在对应的输入框或选项中填写、选择所需参数。"的文件（13 个，均带旧 FAQPage LD）
   → opt-faq section 整段替换为 content_deepdive 真实 faqs；
   → opt-guide"适用场景"套话段落替换为 scenarios[0]；
   → 使用说明短语规范化为"按页面提示逐项填写或选择所需参数。"。
- 第二阶段：formula-desc 含模板套话（"工具名称："/"本校验工具"等）的 5 个文件
   → 替换为该工具真实计算原理说明。
- 其余 42 个文件仅 deep-dive 套话，由 _build.py 从 content_deepdive 重建时自动变真实，无需手动清。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CATS = ["agriculture"]
CLICHE = ("在对应的输入框或选项中填写、选择所需参数。",)

# 真实 formula-desc（5 个模板残留文件）
FORMULA_DESC = {
    "assessor-1": "依据 GB/T 8097 谷物收获损失测定，损失率=(落粒+漏割+夹带损失量)/实测可收总量×100%。本工具按样点输入估算机收或人工收获损失，辅助调整割台高度与行进速度；纯前端计算，数据不出浏览器。",
    "calc-2": "每亩株数 = 666.7 / (株距m × 行距m)，单株占地 = 株距 × 行距。本工具按株行距与面积计算理论种植密度与总用苗量，供合理密植参考；纯前端计算。",
    "convert-content-1": "干物质 = 鲜重 × (1 − 含水率)。本工具按质量守恒在鲜重与干物质、不同含水率间换算，用于粮食与饲草贸易计价；换算基于干物质守恒。",
    "estimate-analysis": "覆盖度 = 图像中绿色（植被）像素面积 / 图像总面积。本工具基于阈值分割估算作物冠层覆盖度，用于长势监测；结果依赖拍摄条件一致性。",
    "irrigation-uniformity": "克里斯琴森均匀系数 CU = 1 − Σ|x_i − x̄| / (n·x̄)；分布均匀度 DU 取低四分位测点均值/总均值。本工具按各测点水量评估喷滴灌均匀性；纯前端计算。",
}
FD_CLICHE = ("工具名称：", "本校验工具", "本工程计算", "本工具用于", "本计算器基于")

data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- 第一阶段：CLICHE 文件（opt-faq / 适用场景 / 短语） ----------
for cat in CATS:
    for f in sorted(glob.glob("tools/%s/*.html" % cat)):
        if f.endswith("index.html"):
            continue
        s = open(f, encoding="utf-8").read()
        if not any(c in s for c in CLICHE):
            continue
        base = os.path.basename(f)[:-5]
        key = "%s/%s" % (cat, base)
        e = data.get(key)
        if not e:
            print("NO KEY:", key)
            continue
        faqs = e.get("faqs") or []
        scen = e.get("scenarios") or []
        items = "".join(
            "<dt>%s</dt><dd>%s</dd>" % (esc(q.get("q", "")), esc(q.get("a", "")))
            for q in faqs if q.get("q") and q.get("a")
        )
        new_faq = '<section class="opt-faq"><h2>常见问题</h2><dl class="faq-list">%s</dl></section>' % items

        old_faq_m = re.search(r'<section class="opt-faq">.*?</section>', s, re.S)
        old_faq = old_faq_m.group(0) if old_faq_m else ""
        s2 = re.sub(r'<section class="opt-faq">.*?</section>', new_faq, s, count=1, flags=re.S)

        sc_replaced = 0
        if scen:
            s2, n = re.subn(
                r"<h2>适用场景</h2><p>.*?</p>",
                "<h2>适用场景</h2><p>%s</p>" % esc(scen[0]),
                s2, count=1, flags=re.S,
            )
            sc_replaced = n

        s2 = s2.replace(
            "在对应的输入框或选项中填写、选择所需参数。",
            "按页面提示逐项填写或选择所需参数。",
        )

        still = sum(1 for c in CLICHE if c in s2)
        if dry:
            print("DRY[opt] %s: faq_old_dt=%d faq_new_dt=%d scen_replaced=%d still_cliche=%d"
                  % (key, old_faq.count("<dt>"), new_faq.count("<dt>"), sc_replaced, still))
        else:
            if s2 != s:
                open(f, "w", encoding="utf-8").write(s2)
            print("OK[opt] %s: faq_new_dt=%d scen_replaced=%d still_cliche=%d"
                  % (key, new_faq.count("<dt>"), sc_replaced, still))

# ---------- 第二阶段：formula-desc 模板残留 ----------
for cat in CATS:
    for f in sorted(glob.glob("tools/%s/*.html" % cat)):
        if f.endswith("index.html"):
            continue
        base = os.path.basename(f)[:-5]
        if base not in FORMULA_DESC:
            continue
        s = open(f, encoding="utf-8").read()
        m = re.search(r'<p class="formula-desc">(.*?)</p>', s, re.S)
        if not m:
            print("NO FD:", base)
            continue
        fd = m.group(1)
        if not any(c in fd for c in FD_CLICHE):
            print("FD clean skip:", base)
            continue
        new_fd = '<p class="formula-desc">%s</p>' % FORMULA_DESC[base]
        s2 = re.sub(r'<p class="formula-desc">.*?</p>', new_fd, s, count=1, flags=re.S)
        still = any(c in s2 for c in FD_CLICHE)
        if dry:
            print("DRY[fd] %s: replaced=%d still_cliche=%d" % (base, 1, 1 if still else 0))
        else:
            if s2 != s:
                open(f, "w", encoding="utf-8").write(s2)
            print("OK[fd] %s: still_cliche=%d" % (base, 1 if still else 0))
