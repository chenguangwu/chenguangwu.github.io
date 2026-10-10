#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态门禁：verify 用例 expect 的「环境依赖」反模式检查。

背景（2026-10-11 CI 连续红灯的根因，防复发）：
  R1 浮点全展开：expect 含 ≥15 位有效数字 ⇒ 依赖 Number.prototype.toString() 的最短往返
     表示。Math.pow/exp/log 等在 macOS ARM 与 Linux x86 相差 1 ULP ⇒ 字符串不同
     ⇒ 「本地全绿、CI 必红且不可复现」。处置：只保留 ≤10 位有效数字。
  R2 时区格式化：expect 含 AM/PM ⇒ 依赖 toLocaleString() 的本地时区。
     实例：本地 GMT+8 输出「3:0|6:40 PM)|」巧合命中带「6:40 PM)」的 expect，
     CI(UTC) 输出「7:06:40 AM)」则不命中 ⇒ 本地绿 CI 红。
  R3 冻结日期：expect 含 harness 冻结的「今天」字面串（24-06-14 / 24-06-15 及其中文式）
     ⇒ 该值随时区偏移 1 天，跨时区必失配。锚点必须由「注入」决定而非「时钟」决定。

判据全部在「源码文本层」做（括号匹配定位 expect 数组，跟踪引号/转义），
不依赖 eval、不跑页面 ⇒ 秒级、100% 覆盖、可在 CI 稳定执行。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUM = re.compile(r"-?\d+(?:\.\d+)?(?:e[+-]\d+)?")
KEY = re.compile(r'(?:"expect"|expect)\s*:\s*\[')
AMPM = re.compile(r"\b(?:AM|PM)\b")
# harness 冻结的「今天」在本地时区呈现为 2024-06-15；跨时区会偏移到 06-14 / 06-16
FROZEN = re.compile(r"(?:\d{2})?24-06-1[3456]|2024年6月1[3456]日")


def match_bracket(src: str, i: int) -> int:
    """src[i] 应为 '['，返回配对的 ']' 索引（跟踪引号与转义）。"""
    depth, quote, esc = 0, None, False
    k = i
    while k < len(src):
        ch = src[k]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
        else:
            if ch in "\"'`":
                quote = ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return k
        k += 1
    return -1


def sig_digits(s: str) -> int:
    mant = s.split("e")[0].split("E")[0].replace("-", "").replace(".", "")
    return len(mant.strip("0"))


def main() -> int:
    files = sorted((ROOT / "scripts").glob("verify_*_calc.js"))
    problems: list[str] = []
    scanned = 0

    for p in files:
        src = p.read_text(encoding="utf-8")
        pos = 0
        while True:
            m = KEY.search(src, pos)
            if not m:
                break
            i = src.index("[", m.start(), m.end())
            j = match_bracket(src, i)
            if j == -1:
                break
            body = src[i + 1 : j]
            scanned += 1
            line_no = src[: m.start()].count("\n") + 1

            for n in NUM.findall(body):
                if not ("." in n or "e" in n or "E" in n):
                    continue
                if sig_digits(n) >= 15:
                    problems.append(
                        f"R1 浮点全展开  {p.name}:{line_no}  {n}（{sig_digits(n)} 位有效数字，"
                        f"跨平台 1ULP 即翻转 ⇒ 只保留 ≤10 位）"
                    )
            if AMPM.search(body):
                problems.append(
                    f"R2 时区格式化  {p.name}:{line_no}  含 AM/PM"
                    f"（toLocaleString() 随本地时区变 ⇒ 移除该时间片段）"
                )
            fm = FROZEN.search(body)
            if fm:
                problems.append(
                    f"R3 冻结日期    {p.name}:{line_no}  {fm.group()}"
                    f"（harness 冻结的『今天』随时区偏移 ⇒ 锚点须由注入决定）"
                )
            pos = j + 1

    print(f"expect anti-pattern: 扫描 {len(files)} 个行业脚本 / {scanned} 个 expect 数组")
    if problems:
        for x in problems:
            print("  ❌ " + x)
        print(f"\n发现 {len(problems)} 处环境依赖型 expect 反模式")
        return 1
    print("  ✅ 无环境依赖型 expect（浮点全展开 / 时区 AM-PM / 冻结日期）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
