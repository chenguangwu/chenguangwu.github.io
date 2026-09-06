#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agriculture 全量：把可见 <section class="opt-guide"> 的 <h2>适用场景</h2><p>.*?</p>
替换为 content_deepdive.json 中该工具 scenarios[0] 的真实描述（三处同清之一）。
对已被 opt_agriculture_cleanup.py 处理过的 13 个 CLICHE 文件是幂等的（s2==s 不写）。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CAT = "agriculture"
data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


changed = 0
skipped = 0
for f in sorted(glob.glob("tools/%s/*.html" % CAT)):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    key = "%s/%s" % (CAT, base)
    e = data.get(key)
    if not e:
        skipped += 1
        continue
    scen = e.get("scenarios") or []
    if not scen:
        skipped += 1
        continue
    s = open(f, encoding="utf-8").read()
    newp = "<h2>适用场景</h2><p>%s</p>" % esc(scen[0])
    s2 = re.sub(r"<h2>适用场景</h2><p>.*?</p>", newp, s, count=1, flags=re.S)
    if s2 != s:
        changed += 1
        if not dry:
            open(f, "w", encoding="utf-8").write(s2)
        print(("DRY " if dry else "OK ") + base)
    else:
        skipped += 1
print("changed=%d skipped=%d" % (changed, skipped))
