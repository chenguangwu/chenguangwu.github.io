#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 audit 源 html 中可见旧套话（三处同清之一：可见 opt 区块 + formula-desc）。
- depreciation-compare 带旧 opt-faq（"在对应的输入框或选项中填写"）+ 适用场景套话 + 旧 FAQPage LD
   → opt-faq section 整段替换为 content_deepdive 真实 faqs；
   → opt-guide"适用场景"套话段落替换为 scenarios[0]；
   → 使用说明短语规范化为"按页面提示逐项填写或选择所需参数。"。
- 其余 4 个文件仅 deep-dive 套话，由 _build.py 从 content_deepdive 重建时自动变真实，无需手动清。
- 无 formula-desc 套话文件（audit 全 5 文件 fd=0），故无需第二阶段。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CAT = "audit"
CLICHE = ("在对应的输入框或选项中填写、选择所需参数。",)

data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


for f in sorted(glob.glob("tools/%s/*.html" % CAT)):
    if f.endswith("index.html"):
        continue
    s = open(f, encoding="utf-8").read()
    if not any(c in s for c in CLICHE):
        continue
    base = os.path.basename(f)[:-5]
    key = "%s/%s" % (CAT, base)
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
