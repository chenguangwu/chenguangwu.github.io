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
