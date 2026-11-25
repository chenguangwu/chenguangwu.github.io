#!/usr/bin/env python3
"""中文态 data-zh 还原覆盖门禁。

背景：构建期会把英文预渲染进静态 HTML，中文原文保存在 data-zh；运行时
js/tool-i18n.js::restoreAllDataZh() 只还原「白名单标签 + 无子元素」的节点。
新增带 data-zh 的标签、或带子标记的节点若未纳入还原逻辑，中文默认态会残留英文。
本脚本静态扫描 tools/**/*.html，断言：
  1) data-zh 含汉字的标签都在还原白名单内；
  2) 含子元素的节点只允许 td/p（HTML 级还原），且不含交互控件/多外链；
  3) 非 td/p 白名单标签不得带子元素。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u4e00-\u9fff]")
# 只匹配带 data-zh 的真实开标签；公式里的 "<0.01"/"<i<4" 不进入候选。
TAG_OPEN = re.compile(r'<([a-zA-Z][a-zA-Z0-9-]*)[^>\n]*\bdata-zh="([^"]*)"[^>\n]*>', re.S)
REAL_TAG = re.compile(r"<([a-zA-Z][a-zA-Z0-9-]*)(?=[\s/>])")
ALLOWED = {"p", "h2", "h3", "th", "td", "span", "label", "summary", "strong", "b", "button", "div", "li", "option"}
HTML_RESTORE = {"td", "p"}
INTERACTIVE = {"input", "select", "textarea", "button"}


def scan_file(path: Path) -> list[str]:
    s = path.read_text(encoding="utf-8", errors="ignore")
    problems = []
    for m in TAG_OPEN.finditer(s):
        tag, zh = m.group(1).lower(), m.group(2)
        if not CJK.search(zh) or "data-i18n=" in m.group(0):
            continue
        start = m.end()
        close = s.find("</" + tag, start)
        inner = s[start:close if close >= 0 else start]
        children = [c.lower() for c in REAL_TAG.findall(inner)]
        rel = path.relative_to(ROOT)
        if tag not in ALLOWED:
            problems.append(f"{rel}: <{tag} data-zh> 未纳入 restoreAllDataZh 白名单")
        elif children:
            if tag not in HTML_RESTORE:
                problems.append(f"{rel}: <{tag} data-zh> 带子元素，运行时不会还原")
            elif INTERACTIVE & set(children):
                problems.append(f"{rel}: <{tag} data-zh> 含交互子元素，运行时拒绝还原")
            elif children.count("a") > 1:
                problems.append(f"{rel}: <{tag} data-zh> 含多个外链，运行时仅处理单外链")
            elif "<a" in zh.lower() and "a" in children:
                problems.append(f"{rel}: <{tag} data-zh> 自身含 <a>，运行时拒绝还原")
    return problems


def main() -> int:
    problems = []
    for f in sorted((ROOT / "tools").rglob("*.html")):
        problems.extend(scan_file(f))
    if problems:
        print("中文态 data-zh 还原覆盖检查失败：")
        for x in problems[:80]:
            print(" -", x)
        print(f"共 {len(problems)} 项")
        return 1
    print("PASS: 中文态 data-zh 还原覆盖完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
