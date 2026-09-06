#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""biz 全量：把可见 tool-intro-body 的「功能特点」「使用场景」通用套话 ul 替换为真实内容。

- 使用场景：取 content_deepdive.json 中该工具 scenarios 前 3 条（真实、有针对性）。
- 功能特点：替换为对所有 ToolBox 工具都成立的真实通用描述（纯前端不上传 / 免费无需注册 / 三语界面）。

对齐 agriculture 的 opt_agriculture_optguide.py 思路（套话替换为真实内容），适配 biz 的
<h4> 结构（非 agriculture 的 <h2>）。幂等：s2==s 不写。支持 --dry 预览。
仅处理 tools/biz/*.html（跳过 index.html）。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CAT = "biz"
data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


FEAT_HTML = (
    '<ul class="intro-features">\n'
    '      <li>纯前端运行，数据不上传服务器</li>\n'
    '      <li>免费使用，无需注册登录</li>\n'
    '      <li>支持简体 / 繁体 / 英文界面</li>\n'
    '    </ul>'
)

PAT_FEAT = re.compile(
    r'<h4>.*?功能特点.*?</h4>\s*<ul class="intro-features">.*?</ul>', re.S)
PAT_SCENE = re.compile(
    r'<h4>.*?使用场景.*?</h4>\s*<ul class="intro-scenes">.*?</ul>', re.S)

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
        print("NOKEY", base)
        continue
    scen = e.get("scenarios") or []
    if not scen:
        skipped += 1
        continue
    s = open(f, encoding="utf-8").read()
    scene_items = "".join("<li>%s</li>" % esc(x) for x in scen[:3])
    scene_html = '<ul class="intro-scenes">\n      %s\n    </ul>' % scene_items
    s2 = PAT_FEAT.sub("<h4><span class=\"h4-icon\">✨</span>功能特点</h4>\n    " + FEAT_HTML, s, count=1)
    s2 = PAT_SCENE.sub("<h4><span class=\"h4-icon\">🎯</span>使用场景</h4>\n    " + scene_html, s2, count=1)
    if s2 != s:
        changed += 1
        if not dry:
            open(f, "w", encoding="utf-8").write(s2)
        print(("DRY " if dry else "OK ") + base)
    else:
        skipped += 1
        print("UNMATCH", base)
print("changed=%d skipped=%d" % (changed, skipped))
