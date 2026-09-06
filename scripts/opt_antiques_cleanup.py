#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 antiques 源 html 中可见旧套话（三处同清之一：formula-desc）。
- 5 个对照表工具均带 formula-desc 模板套话（"本速查内容依据权威标准…工具名称：…"），
  替换为该工具真实用途说明（对照表范围 + 仅供学习参考的免责）。
- 无旧 opt-faq / 适用场景，故只做 formula-desc 阶段；deep-dive 由 _build.py 从 content_deepdive 重建时变真实。
"""
import re, glob, os, sys

CATS = ["antiques"]
FD_CLICHE = ("本速查内容依据权威标准", "工具名称：")

# 真实 formula-desc（5 个对照表工具）
FORMULA_DESC = {
    "bronze-identification": "本对照表汇集商、西周、春秋、战国至汉各时期青铜器的器型、纹饰、铭文与铸造工艺特征，供鉴赏、断代与辨伪时快速比对。鉴定结论需结合实物与专业检测，仅供参考学习。",
    "porcelain-date": "本对照表按唐、宋、元、明、清梳理瓷器的胎釉、造型、纹饰与款识特征，供古瓷断代与辨伪时快速比对。具体年代以实物与专业检测为准，仅供参考学习。",
    "furniture-style": "本对照表对比明式与清式古典家具在用材、造型、结构（榫卯）与纹饰上的差异，供鉴赏、断代与辨伪参考。结论需结合实物包浆与工艺，仅供参考学习。",
    "seal-identification": "本对照表梳理各时期印章的材质、印钮、印文与用途特征，供篆刻与印章断代辨伪时快速比对。鉴定结论需结合实物与专业研判，仅供参考学习。",
    "calligraphy-style": "本对照表按书体演变与代表书家梳理书法风格特征，供书法鉴赏、临帖选帖与艺术史学习参考。风格判断需结合笔法、结字与传世作品综合研判。",
}

dry = "--dry" in sys.argv

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
