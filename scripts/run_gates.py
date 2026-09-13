#!/usr/bin/env python3
"""Run the ToolBox build and release quality gates in a fixed order.

The runner deliberately performs no Git or index-submission actions. It is
safe to use locally and from CI, and it stops at the first failed gate while
preserving the original command output and exit code.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


GATES = (
    ("build", ("python3", "_build.py")),
    ("static tests", ("python3", "_test_static.py")),
    ("dead-link audit", ("python3", "_audit_links.py", "--check")),
    ("asset audit", ("python3", "_audit_assets.py", "--check")),
    ("calculation regression", ("node", "scripts/verify_calc.js")),
    # 与上一项区别：verify_calc 是「冒烟」（不报错即可），本项是「正确性」
    # ——注入已知输入后按权威测试向量断言输出（§4.1.1）。用例写在脚本内，逐分类扩充。
    ("it calc correctness", ("node", "scripts/verify_it_calc.js")),
    # general 分类的正确性验证（工程标准公式 / 独立复算），与 it 分开维护用例集。
    ("general calc correctness", ("node", "scripts/verify_general_calc.js")),
    # finance 分类的正确性验证（校验位算法 / 金融公式），用例集独立维护。
    ("finance calc correctness", ("node", "scripts/verify_finance_calc.js")),
    # design 分类的正确性验证（单位换算 / 色度学 / 摄影光学），用例集独立维护。
    ("design calc correctness", ("node", "scripts/verify_design_calc.js")),
    # science 分类的正确性验证（经典力学 / 电学 / 化学 / 统计），用例集独立维护。
    ("science calc correctness", ("node", "scripts/verify_science_calc.js")),
    # sports 分类的正确性验证（力量 1RM / VO2max / 心率 / 氧脉搏 / 齿比 / 坡度 / SWOLF / 出汗率）。
    ("sports calc correctness", ("node", "scripts/verify_sports_calc.js")),
    # fun 分类的正确性验证（烧烤/火锅分量、冥想分段、婚宴桌数、步幅速度换算）。
    ("fun calc correctness", ("node", "scripts/verify_fun_calc.js")),
    # ai 分类的正确性验证（混淆矩阵四指标 / 欧氏曼哈顿余弦 / 交叉熵 / Sigmoid / Softmax /
    # Cohen's Kappa / AUC 秩次 / 学习率衰减 / Transformer 参数量）。
    ("ai calc correctness", ("node", "scripts/verify_ai_calc.js")),
    # biz 分类的正确性验证（服务质量加权评分 / 会议人·小时成本 / 岗位权重胜任力 /
    # 单价单位归一化 / 风险矩阵分级 / 演示计时均分 / 定长折行 / 字符画视觉宽度）。
    ("biz calc correctness", ("node", "scripts/verify_biz_calc.js")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run ToolBox build and quality gates in the required order."
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip _build.py for local re-checks only; do not use for release or CI.",
    )
    return parser.parse_args()


def run_gate(number: int, total: int, name: str, command: tuple[str, ...]) -> int:
    print(f"\n[{number}/{total}] {name}: {' '.join(command)}", flush=True)
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=ROOT, check=False)
    except FileNotFoundError as exc:
        executable = command[0]
        print(f"FAIL: required executable is not available: {executable}", file=sys.stderr)
        print(f"detail: {exc}", file=sys.stderr)
        return 127

    elapsed = time.monotonic() - started
    if completed.returncode == 0:
        print(f"PASS: {name} ({elapsed:.1f}s)", flush=True)
    else:
        print(
            f"FAIL: {name} exit={completed.returncode} ({elapsed:.1f}s)",
            file=sys.stderr,
            flush=True,
        )
    return completed.returncode


def main() -> int:
    args = parse_args()
    gates = list(GATES)
    if args.skip_build:
        gates = gates[1:]
        print("WARNING: build gate skipped; use this mode for local re-checks only.")

    for number, (name, command) in enumerate(gates, start=1):
        exit_code = run_gate(number, len(gates), name, command)
        if exit_code:
            print(f"\nQuality gates stopped after: {name}", file=sys.stderr)
            return exit_code

    print(f"\nAll {len(gates)} quality gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
