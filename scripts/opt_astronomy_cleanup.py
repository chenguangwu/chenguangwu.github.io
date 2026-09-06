#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 astronomy 源 html 中可见旧套话（三处同清之一：可见 opt 区块 + formula-desc）。
- 第一阶段：含「在对应的输入框或选项中填写、选择所需参数。」或「工作与生活中的相关计算与查询。」的文件
   → opt-faq section 整段替换为 content_deepdive 真实 faqs；
   → opt-guide"适用场景"套话段落替换为 scenarios[0]；
   → 使用说明短语规范化为"按页面提示逐项填写或选择所需参数。"。
- 第二阶段：formula-desc 含模板套话（"本工具用于单位与格式换算…工具名称："）的 3 个文件
   → 替换为该工具真实计算原理说明。
- 其余 20 个文件仅 deep-dive 套话，由 _build.py 从 content_deepdive 重建时自动变真实，无需手动清。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CATS = ["astronomy"]
CLICHE = ("在对应的输入框或选项中填写、选择所需参数。", "工作与生活中的相关计算与查询。")

# 真实 formula-desc（3 个模板残留文件）
FORMULA_DESC = {
    "convert-15": "本工具按 Gutenberg-Richter 关系 log₁₀E=4.8+1.5M（E 单位焦耳）在里氏/矩震级与释放能量之间换算，并给出对应的 TNT 当量参考；纯前端本地换算，结果仅供科普估算。",
    "convert-17": "本工具在内置全球时区之间按 UTC 偏移做时间换算，并依据所选日期的夏令时规则调整；纯前端本地计算，不改变设备时区设置。",
    "convert-18": "本工具按气压—高度近似 h=44330·(1−(P/P₀)^(1/5.255)) 在气压计读数与海拔之间换算，P₀ 取标准海平面气压 1013.25 hPa；纯前端本地计算，结果受温压天气影响仅供参考。",
}
FD_CLICHE = ("本工具用于单位与格式换算", "工具名称：", "本计算器基于标准数学运算", "本工程计算", "本工具用于")

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
