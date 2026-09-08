#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理工具页中跨行业错配的「使用指南」链接。

背景：
    _build.py 历史版本按 basename 全局匹配 json/guides.json，
    而 calc-1.html 这类文件名在多个行业目录重名，导致「增值税计算使用指南」
    被注入到 fire-rescue / ent / steel 等无关行业的页面。

    构建器只在页面缺少 data-guide-link 标记时才注入，因此历史遗留的错配块
    不会自动消失，需要本脚本一次性清理。

判定规则：
    读取指南页正文里指向归属工具页的绝对 URL
    （https://chenguangwu.github.io/tools/<industry>/<slug>.html），
    若其行业与当前工具页所在行业不一致，则判定为错配并整块删除。

用法：
    python3 scripts/clean_mismatched_guide_links.py            # 预览
    python3 scripts/clean_mismatched_guide_links.py --apply    # 落盘
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE_JSON = os.path.join(ROOT, "json", "guides.json")

# 匹配已注入的 guide-link 整块（含外层 div，可能跨行）
BLOCK_RE = re.compile(
    r'\n?<div class="tool-guide-link" data-guide-link="1">\s*'
    r'<a href="([^"]+)">📖 查看「([^」]*)」</a>\s*</div>\n?'
)
# 从指南页正文反查归属工具页
OWNER_RE = re.compile(
    r"https://chenguangwu\.github\.io/tools/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+\.html)"
)


def build_owner_index() -> dict:
    """指南文件名 -> set(归属行业)。"""
    owners: dict[str, set] = {}
    if not os.path.isfile(GUIDE_JSON):
        return owners
    for g in json.load(open(GUIDE_JSON, encoding="utf-8")):
        tool = g.get("tool")
        rel = (g.get("guide") or "").replace("../../", "")
        if not tool or not rel:
            continue
        gp = os.path.join(ROOT, rel)
        if not os.path.isfile(gp):
            continue
        try:
            body = open(gp, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in OWNER_RE.finditer(body):
            if m.group(2) == tool:
                owners.setdefault(tool, set()).add(m.group(1))
                break
    return owners


def main() -> int:
    apply = "--apply" in sys.argv
    owners = build_owner_index()
    changed, scanned = [], 0

    for dirpath, _dirnames, filenames in os.walk(os.path.join(ROOT, "tools")):
        industry = os.path.relpath(dirpath, os.path.join(ROOT, "tools")).replace(os.sep, "/")
        if industry == "." or "/" in industry:
            continue
        for fn in filenames:
            if not fn.endswith(".html") or fn == "index.html":
                continue
            path = os.path.join(dirpath, fn)
            src = open(path, encoding="utf-8").read()
            scanned += 1

            def _judge(m: re.Match, _ind=industry, _fn=fn) -> str:
                href, _title = m.group(1), m.group(2)
                gfile = os.path.basename(href)
                tool_key = gfile.replace("-guide.html", ".html")
                inds = owners.get(tool_key)
                # 归属已知且不含当前行业 → 错配，删除
                if inds and _ind not in inds:
                    return ""
                return m.group(0)

            new = BLOCK_RE.sub(_judge, src)
            if new != src:
                changed.append(os.path.relpath(path, ROOT))
                if apply:
                    open(path, "w", encoding="utf-8").write(new)

    print("扫描工具页: %d" % scanned)
    print("错配 guide-link: %d 个页面" % len(changed))
    for c in changed[:30]:
        print("  -", c)
    if len(changed) > 30:
        print("  ... 其余 %d 个" % (len(changed) - 30))
    print("模式: %s" % ("已落盘" if apply else "预览（加 --apply 落盘）"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
