#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""building-material：清理工具页 tool-intro「功能特点/使用场景」通用套话，仅命中套话页才替换。

判定：读功能特点 ul 文本，若含通用套话特征词（操作简单，一键完成 / 日常办公与学习 /
开发调试与数据处理 / 实时显示结果，所见即所得）则判定为套话并替换；否则跳过（保留真实页，
如 detector-35 的功能特点已是真实建材内容）。

- 使用场景：取 content_deepdive.json 该工具 scenarios 前 3 条（真实建材场景）。
- 功能特点：替换为对所有 ToolBox 工具都成立的真实通用描述。

正则精确锚定「功能特点/使用场景」h4（仿 opt_bonding_optguide.py，保留「工具简介」块）。
幂等：s2==s 不写。支持 --dry 预览。仅处理 tools/building-material/*.html（跳过 index.html）。
"""
import re, glob, json, os, sys

DATA = "i18n/tools/content_deepdive.json"
CAT = "building-material"
data = json.load(open(DATA, encoding="utf-8"))
dry = "--dry" in sys.argv

# 通用套话特征词：命中任一即判定为套话页
PH_WORDS = ["操作简单，一键完成", "日常办公与学习", "开发调试与数据处理", "实时显示结果，所见即所得"]


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
    r'<h4>(?:(?!</h4>).)*功能特点</h4>\s*<ul class="intro-features">.*?</ul>', re.S)
PAT_SCENE = re.compile(
    r'<h4>(?:(?!</h4>).)*使用场景</h4>\s*<ul class="intro-scenes">.*?</ul>', re.S)
PAT_FEAT_UL = re.compile(
    r'<h4>(?:(?!</h4>).)*功能特点</h4>\s*<ul class="intro-features">(.*?)</ul>', re.S)


def is_placeholder(s):
    m = PAT_FEAT_UL.search(s)
    if not m:
        return False
    return any(w in m.group(1) for w in PH_WORDS)


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
    s = open(f, encoding="utf-8").read()
    if not is_placeholder(s):
        skipped += 1
        print("REAL-SKIP", base)
        continue
    scen = e.get("scenarios") or []
    if not scen:
        skipped += 1
        continue
    scene_items = "".join("<li>%s</li>" % esc(x) for x in scen[:3])
    scene_html = '<ul class="intro-scenes">\n      %s\n    </ul>' % scene_items
    s2 = PAT_FEAT.sub('<h4><span class="h4-icon">✨</span>功能特点</h4>\n    ' + FEAT_HTML, s, count=1)
    s2 = PAT_SCENE.sub('<h4><span class="h4-icon">🎯</span>使用场景</h4>\n    ' + scene_html, s2, count=1)
    if s2 != s:
        changed += 1
        if not dry:
            open(f, "w", encoding="utf-8").write(s2)
        print(("DRY " if dry else "OK ") + base)
    else:
        skipped += 1
        print("UNMATCH", base)
print("changed=%d skipped=%d" % (changed, skipped))
