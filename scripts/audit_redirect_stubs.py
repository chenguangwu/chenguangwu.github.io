#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重定向存根（TOOLBOX-REDIRECT）合规审计。

对照 AGENTS.md §4.6：存根最长保留 1 个月、到期必须物理删除、且必须登记在
`_redirect_stubs_todo.md`。本脚本把三件事机器化，避免「到期忘了删」和「新存根忘了登记」：

1. 未登记：磁盘上存在 TOOLBOX-REDIRECT 页，但登记表里没有对应源 URL；
2. 超期未删：登记表里状态不是「已删」且到期日已过；
3. 幽灵登记：状态写「已删」但文件还在（登记与实际不一致）。

用法：
  python3 scripts/audit_redirect_stubs.py            # 报告
  python3 scripts/audit_redirect_stubs.py --check    # 有任一类问题则 exit 1
"""
from __future__ import annotations

import html
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODO = os.path.join(ROOT, "_redirect_stubs_todo.md")
BASE = "https://chenguangwu.github.io/"


def disk_stubs() -> dict[str, str]:
    """返回 {相对路径: 目标 URL}，覆盖 tools/ 下所有 TOOLBOX-REDIRECT 页。"""
    out: dict[str, str] = {}
    tools = os.path.join(ROOT, "tools")
    for dirpath, _dirnames, filenames in os.walk(tools):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
            except OSError:
                continue
            if "TOOLBOX-REDIRECT" not in content:
                continue
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            m = re.search(r"TOOLBOX-REDIRECT\s+url=([^\"'>\s]+)", content)
            target = html.unescape(m.group(1)) if m else ""
            out[rel] = target
    return out


def registered() -> dict[str, dict]:
    """解析登记表的表格行 → {源 URL: {target, expiry, status}}。"""
    rows: dict[str, dict] = {}
    if not os.path.exists(TODO):
        return rows
    with open(TODO, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("| http"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 5:
                continue
            src, target, _created, expiry, status = cells[:5]
            try:
                exp = date.fromisoformat(expiry)
            except ValueError:
                exp = None
            rows[src] = {"target": target, "expiry": exp, "status": status}
    return rows


def main(argv: list[str]) -> int:
    check = "--check" in argv
    today = date.today()
    stubs = disk_stubs()
    table = registered()

    unregistered, ghost, expired = [], [], []
    for rel, target in sorted(stubs.items()):
        url = BASE + rel
        if url not in table:
            unregistered.append((url, target))
    for url, info in sorted(table.items()):
        if "已删" in info["status"]:
            rel = url.replace(BASE, "")
            if os.path.exists(os.path.join(ROOT, rel)):
                ghost.append(url)
        elif info["expiry"] and info["expiry"] < today:
            expired.append((url, info["expiry"].isoformat()))

    print(f"[stub-audit] 磁盘存根 {len(stubs)} 页；登记行 {len(table)} 条；今天 {today.isoformat()}")
    for url, target in unregistered:
        print(f"  ✗ 未登记：{url} → {target}")
    for url, expiry in expired:
        print(f"  ✗ 超期未删（到期 {expiry}）：{url}")
    for url in ghost:
        print(f"  ✗ 登记为已删但文件仍在：{url}")

    bad = len(unregistered) + len(expired) + len(ghost)
    if bad:
        print(f"[stub-audit] FAIL：{bad} 项")
        return 1 if check else 0
    print("[stub-audit] PASS：存根均已登记、无超期未删、无幽灵登记")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
