#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OPTIMIZE-TASKS.md 任务清单进度管理。

用法：
    python3 scripts/opt_task.py show               # 打印进度总览
    python3 scripts/opt_task.py next [N]           # 列出接下来 N 个待办（默认 5）
    python3 scripts/opt_task.py done <path> [...]  # 完成：从清单中删除条目并更新进度
    python3 scripts/opt_task.py done --batch N     # 标记整批完成

设计要点：
  * done 采用「删除条目」而非打勾，符合老板「完成一个删除一个」的要求。
  * 删除后若某批次已空，则移除该批次标题，保持文档精简。
  * 进度表（总数/已完成/剩余/当前批次）自动重算。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "OPTIMIZE-TASKS.md"

ENTRY_RE = re.compile(r"^- \[[ x]\] #(?P<no>\d+) `(?P<path>[^`]+)`.*$")
BATCH_RE = re.compile(r"^## 批次 (?P<n>\d+)（.*$")
TOTAL_RE = re.compile(r"^\| (?P<total>\d+) \| (?P<done>\d+) \| (?P<left>\d+) \| (?P<cur>.*?) \|$", re.M)


def read_lines():
    return TASKS.read_text(encoding="utf-8").split("\n")


def write_lines(lines):
    TASKS.write_text("\n".join(lines), encoding="utf-8")


def parse_total(lines):
    """从文档头部的体检总览里取原始总数（首行 '| 750 | ...' 之前的总数）"""
    head = "\n".join(lines[:60])
    m = re.search(r"^> 数据源：`analytics_traffic_merged\.csv`（共 (\d+) 个工具页", head, re.M)
    return int(m.group(1)) if m else 0


def show():
    lines = read_lines()
    entries = [ENTRY_RE.match(l) for l in lines if ENTRY_RE.match(l)]
    batches = [BATCH_RE.match(l).group("n") for l in lines if BATCH_RE.match(l)]
    total = parse_total(lines)
    done = total - len(entries) if total else 0
    print(f"总数 {total} | 已完成 {done} | 剩余 {len(entries)} | 剩余批次 {len(batches)}")
    if batches:
        print(f"当前批次：{batches[0]}（该批 {count_in_batch(lines, batches[0])} 个）")


def count_in_batch(lines, n):
    c, inb = 0, False
    for l in lines:
        if BATCH_RE.match(l):
            inb = BATCH_RE.match(l).group("n") == str(n)
            continue
        if inb and l.startswith("## "):
            break
        if inb and ENTRY_RE.match(l):
            c += 1
    return c


def next_items(n=5):
    lines = read_lines()
    out = []
    for l in lines:
        m = ENTRY_RE.match(l)
        if m:
            out.append((m.group("no"), m.group("path")))
            if len(out) >= n:
                break
    for no, p in out:
        print(f"#{no} {p}")
    return out


def update_progress(lines, total):
    left = sum(1 for l in lines if ENTRY_RE.match(l))
    done = total - left
    # 当前批次 = 第一个仍有条目的批次
    cur, inb, cur_has = "—", None, False
    for l in lines:
        bm = BATCH_RE.match(l)
        if bm:
            if cur_has:
                break
            inb, cur_has = bm.group("n"), False
            continue
        if inb and l.startswith("## "):
            break
        if inb and ENTRY_RE.match(l):
            cur_has = True
    if cur_has and inb:
        cur = f"批次 {inb}"
    new = f"| {total} | {done} | {left} | {cur} |"
    out = []
    replaced = False
    for l in lines:
        if not replaced and TOTAL_RE.match(l) and l.startswith("| "):
            out.append(new)
            replaced = True
        else:
            out.append(l)
    return out


def drop_empty_batches(lines):
    """删除已清空批次的多余标题与空行"""
    out = []
    i = 0
    while i < len(lines):
        bm = BATCH_RE.match(lines[i])
        if bm:
            # 向后扫描该批次区段
            j = i + 1
            has = False
            while j < len(lines) and not lines[j].startswith("## "):
                if ENTRY_RE.match(lines[j]):
                    has = True
                    break
                j += 1
            if not has:
                # 跳过该标题以及其后紧跟的空行
                i += 1
                while i < len(lines) and lines[i].strip() == "":
                    i += 1
                continue
        out.append(lines[i])
        i += 1
    return out


def mark_done(paths):
    targets = set()
    for p in paths:
        p = p.strip().strip("`").lstrip("/")
        targets.add(p)
        targets.add(p.replace("\\", "/"))

    lines = read_lines()
    total = parse_total(lines)
    kept, removed = [], []
    for l in lines:
        m = ENTRY_RE.match(l)
        if m and m.group("path") in targets:
            removed.append(m.group("path"))
            continue
        kept.append(l)

    if not removed:
        print("未匹配到任何条目，请检查路径是否与清单一致")
        return 1

    kept = drop_empty_batches(kept)
    kept = update_progress(kept, total)
    write_lines(kept)
    print(f"已删除 {len(removed)} 条：")
    for r in removed:
        print(f"  - {r}")
    left = sum(1 for l in kept if ENTRY_RE.match(l))
    print(f"剩余 {left} / {total}")
    return 0


def done_batch(n):
    lines = read_lines()
    paths, inb = [], False
    for l in lines:
        bm = BATCH_RE.match(l)
        if bm:
            inb = bm.group("n") == str(n)
            continue
        if inb and l.startswith("## "):
            break
        if inb:
            m = ENTRY_RE.match(l)
            if m:
                paths.append(m.group("path"))
    if not paths:
        print(f"批次 {n} 无条目")
        return 1
    return mark_done(paths)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "show":
        show()
    elif cmd == "next":
        next_items(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    elif cmd == "done":
        args = sys.argv[2:]
        if args and args[0] == "--batch":
            return done_batch(int(args[1]))
        return mark_done(args)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
