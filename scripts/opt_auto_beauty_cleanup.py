#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 auto-beauty 源 html 中可见旧套话（三处同清之一：formula-desc）。
- calc-1 带 formula-desc 套话（data-zh="本计算基于标准数学定义与运算规则…工具名称："）
   → 替换为真实镀晶/打蜡周期计算原理说明。
- cycle-13 无 formula-desc，无需处理。
- 两文件均无旧 opt-faq/适用场景/FAQPage LD，deep-dive 由 _build.py 从 content_deepdive 重建自动变真实。
"""
import re, glob, os, sys

CAT = "auto-beauty"
FD_CLICHE = ("本计算基于标准数学定义", "工具名称：", "本工具用于", "本计算器基于", "本工程计算")

# 真实 formula-desc（含中文 data-zh 与英文文本）
FORMULA_DESC = {
    "calc-1": '<p class="formula-desc" data-zh="本工具按「上次护理日期 + 项目建议周期」推算下次护理日期与剩余天数；周期可在镀晶（12–36 个月）、封体剂（3–6 个月）、打蜡（1–3 个月）间选择。纯前端计算，护理数据不上传服务器。">Estimate the next car-detailing date and remaining days from the last coating or waxing date and the selected interval; choose among coating (12–36 mo), sealant (3–6 mo) and wax (1–3 mo). Runs locally in your browser.</p>',
}

dry = "--dry" in sys.argv


def main():
    for f in sorted(glob.glob("tools/%s/*.html" % CAT)):
        if f.endswith("index.html"):
            continue
        base = os.path.basename(f)[:-5]
        if base not in FORMULA_DESC:
            continue
        s = open(f, encoding="utf-8").read()
        m = re.search(r'<p class="formula-desc".*?</p>', s, re.S)
        if not m:
            print("NO FD:", base)
            continue
        fd = m.group(0)
        if not any(c in fd for c in FD_CLICHE):
            print("FD clean skip:", base)
            continue
        new_fd = FORMULA_DESC[base]
        s2 = re.sub(r'<p class="formula-desc".*?</p>', new_fd, s, count=1, flags=re.S)
        still = any(c in s2 for c in FD_CLICHE)
        if dry:
            print("DRY[fd] %s: replaced=1 still_cliche=%d" % (base, 1 if still else 0))
        else:
            if s2 != s:
                open(f, "w", encoding="utf-8").write(s2)
            print("OK[fd] %s: still_cliche=%d" % (base, 1 if still else 0))


if __name__ == "__main__":
    main()
