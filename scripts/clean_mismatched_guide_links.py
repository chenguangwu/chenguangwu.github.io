#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理工具页中跨行业错配的「使用指南」链接。

背景：
    _build.py 历史版本按 basename 全局匹配 json/guides.json，而 calc-1.html 这类
    文件名在多个行业目录重名，导致「增值税计算使用指南」被注入到 fire-rescue /
    ent / steel 等无关行业的页面；反之，某行业目录下同名工具页也会被注入成
    「他行业指南」（如 tools/accounting/calc-1.html 曾指向 hydraulic 的
    guides/calc-1-guide.html）。

    构建器只在页面缺少 data-guide-link 标记时才注入，因此历史遗留的错配块
    不会自动消失，需要本脚本清理。

判定规则（精确归属，2026-09-14 加固）：
    1) 以 json/guides.json 为准：仅当某指南条目的 `tool`（basename）与目标页
       basename 相同，且该指南页正文用绝对 URL 反链 `tools/<行业>/<tool>`，
       才记为该「行业/basename」的候选指南。
    2) 候选唯一（恰好 1 个）且与页面现有 href 不同 → 判定错配，重写为候选指南。
        候选不唯一（如跨行业重名经前缀消歧后残留的重复指南文件）→ 跳过并提示，
        避免误改语义正确的链接。
    3) 候选为空（归属未知）→ 跳过。

    旧版仅按「指南 basename -> 归属行业集合」判断，同 basename 的重复指南会互相
    污染集合，导致漏报（accounting/calc-1 实例）。改用「行业/basename」精确键后
    不再漏报。

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
# 从指南页正文反查归属工具页。
# 兼容两代指南：新格式用绝对 URL，旧格式（2026-09 早期）用根相对 /tools/<行业>/<file>。
OWNER_RE = re.compile(
    r"(?:https://chenguangwu\.github\.io)?/tools/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+\.html)"
)


def build_expect_index() -> tuple[dict, dict]:
    """返回 (唯一期望映射, 歧义提示)。

    期望映射键 = '<行业>/<basename>.html'，值 = (指南相对路径, 指南标题)。
    仅收录候选唯一的条目。
    """
    cands: dict[str, dict[str, str]] = {}
    titles: dict[str, str] = {}
    if not os.path.isfile(GUIDE_JSON):
        return {}, {}
    for g in json.load(open(GUIDE_JSON, encoding="utf-8")):
        tool = g.get("tool") or ""
        gp_rel = (g.get("guide") or "").replace("../../", "")
        if not tool or not gp_rel:
            continue
        gp = os.path.join(ROOT, gp_rel)
        if not os.path.isfile(gp):
            continue
        try:
            body = open(gp, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in OWNER_RE.finditer(body):
            if m.group(2) != tool:
                continue
            key = m.group(1) + "/" + tool
            cands.setdefault(key, {})[os.path.basename(gp_rel)] = os.path.basename(gp_rel)
            titles[os.path.basename(gp_rel)] = g.get("title", "") or ""
            break

    expected, ambiguous = {}, {}
    for key, files in cands.items():
        if len(files) == 1:
            (base,) = files.values()
            expected[key] = (base, titles.get(base, ""))
        else:
            ambiguous[key] = sorted(files)
    return expected, ambiguous


def main() -> int:
    apply = "--apply" in sys.argv
    expected, ambiguous = build_expect_index()
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
            m = BLOCK_RE.search(src)
            if not m:
                continue
            cur = os.path.basename(m.group(1))
            exp = expected.get(industry + "/" + fn)
            if not exp:
                continue
            exp_file, exp_title = exp
            if cur == exp_file:
                continue
            title = exp_title if exp_title else m.group(2)
            new_block = (
                '\n<div class="tool-guide-link" data-guide-link="1">\n'
                '  <a href="../../guides/%s">📖 查看「%s」</a>\n'
                '</div>\n' % (exp_file, title)
            )
            new = src[: m.start()] + new_block + src[m.end():]
            if new != src:
                changed.append((os.path.relpath(path, ROOT), cur, exp_file))
                if apply:
                    open(path, "w", encoding="utf-8").write(new)

    print("扫描工具页: %d" % scanned)
    print("错配 guide-link: %d 个页面" % len(changed))
    for rel, cur, exp in changed[:30]:
        print("  - %-40s %s -> %s" % (rel, cur, exp))
    if len(changed) > 30:
        print("  ... 其余 %d 个" % (len(changed) - 30))
    if ambiguous:
        print("候选不唯一（已跳过，需人工确认）: %d 处" % len(ambiguous))
        for k in list(ambiguous)[:10]:
            print("  ? %s -> %s" % (k, ", ".join(ambiguous[k])))
    print("模式: %s" % ("已落盘" if apply else "预览（加 --apply 落盘）"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
