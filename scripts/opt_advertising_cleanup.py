#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 advertising 源 html 中 opt-guide/opt-faq 可见旧套话区块（吸取12文件遗漏教训：清旧套话必须三处同清）。
- opt-faq section：整段替换为 content_deepdive 真实 faqs（dt=q / dd=a），与已注入的 FAQPage LD 一致。
- opt-guide 的"适用场景"套话段落：替换为 content_deepdive scenarios[0] 真实场景。
- opt-guide "如何使用" ol 里的套话短语：替换为"按页面提示逐项填写或选择所需参数。"。
- 只处理含旧套话标记的文件，其它文件不动。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CATS = ["advertising"]
CLICHE = ("工作与生活中的相关计算", "在对应的输入框或选项中填写", "记账、报表与财务比率的快速核算")


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv

files = []
for cat in CATS:
    for f in glob.glob("tools/%s/*.html" % cat):
        if f.endswith("index.html"):
            continue
        s = open(f, encoding="utf-8").read()
        if any(c in s for c in CLICHE):
            files.append((cat, f))

for cat, f in files:
    base = os.path.basename(f)[:-5]
    key = "%s/%s" % (cat, base)
    e = data.get(key)
    if not e:
        print("NO KEY:", key)
        continue
    faqs = e.get("faqs") or []
    scen = e.get("scenarios") or []
    s = open(f, encoding="utf-8").read()

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
        print("DRY %s: faq_old_dt=%d faq_new_dt=%d scen_replaced=%d still_cliche=%d"
              % (key, old_faq.count("<dt>"), new_faq.count("<dt>"), sc_replaced, still))
    else:
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
        print("OK %s: faq_new_dt=%d scen_replaced=%d still_cliche=%d"
              % (key, new_faq.count("<dt>"), sc_replaced, still))
