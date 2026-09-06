#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 ballistics 源 html 中可见旧套话（三处同清之一：可见 opt 区块 + formula-desc）。
- 第一阶段：7 个带旧 opt-faq/适用场景 套话的文件
   → opt-faq section 整段替换为 content_deepdive 真实 faqs；
   → 适用场景 套话段落替换为 scenarios[0]。
- 第二阶段：4 个 formula-desc 含「工具名称：」模板套话的文件
   → 替换为该工具真实计算原理说明。
- 其余 17 个文件仅 deep-dive 套话，由 _build.py 从 content_deepdive 重建时自动变真实，无需手动清。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CAT = "ballistics"
CLICHE = ("在对应的输入框或选项中填写、选择所需参数。",)

# 真实 formula-desc（4 个模板残留文件）
FORMULA_DESC = {
    "analysis-16": "本工具对多组弹着点坐标计算样本均值、标准差与 CEP/2DRMS 圆概率误差，用于评估射击密集度与系统偏差；纯前端本地计算，数据不上传服务器。",
    "barrel-life": "本工具基于膛压—温度—发射频率的累计损耗模型，结合材料疲劳曲线估算枪管寿命（发数）；纯前端本地计算，数据不上传服务器。",
    "caliber-conversion": "本工具按 1 英寸=25.4 毫米的固定换算因子做毫米与英寸口径互转，霰弹号数按标准对照表换算；纯前端本地计算，数据不上传服务器。",
    "sight-adjustment": "本工具按弹着点偏差与觇孔/准星机械分划（每咔哒对应固定角分或毫米/百米）换算所需调整量与方向；纯前端本地计算，数据不上传服务器。",
}
FD_CLICHE = ("工具名称：", "本计算器基于标准数学运算", "本工程计算", "本工具用于", "本计算基于标准数学定义", "本速查内容依据权威标准", "本生成器依据指定格式规范")

data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------- 第一阶段：CLICHE 文件（opt-faq / 适用场景） ----------
for f in sorted(glob.glob("tools/%s/*.html" % CAT)):
    if f.endswith("index.html"):
        continue
    s = open(f, encoding="utf-8").read()
    if not any(c in s for c in CLICHE):
        # 也覆盖 适用场景 套话（早期残留可能无「在对应的输入框」短语但有 opt-faq 旧块）
        if 'class="opt-faq"' not in s:
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

# ---------- 第二阶段：formula-desc 模板残留 ----------
for f in sorted(glob.glob("tools/%s/*.html" % CAT)):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    if base not in FORMULA_DESC:
        continue
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<p class="formula-desc"[^>]*>(.*?)</p>', s, re.S)
    if not m:
        print("NO FD:", base)
        continue
    fd = m.group(1)
    if not any(c in fd for c in FD_CLICHE):
        print("FD clean skip:", base)
        continue
    new_fd = '<p class="formula-desc">%s</p>' % FORMULA_DESC[base]
    s2 = re.sub(r'<p class="formula-desc"[^>]*>.*?</p>', new_fd, s, count=1, flags=re.S)
    still = any(c in s2 for c in FD_CLICHE)
    if dry:
        print("DRY[fd] %s: still_cliche=%d" % (base, 1 if still else 0))
    else:
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
        print("OK[fd] %s: still_cliche=%d" % (base, 1 if still else 0))
