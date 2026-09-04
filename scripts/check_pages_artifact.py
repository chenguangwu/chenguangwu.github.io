#!/usr/bin/env python3
"""Fail before deployment when the GitHub Pages artifact grows too large."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_ROOT_DIRS = {".git", ".github", "node_modules"}
MAX_ARTIFACT_BYTES = 900 * 1024 * 1024


def artifact_size(root: Path) -> tuple[int, int]:
    total_bytes = 0
    file_count = 0

    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        if current_path == root:
            dirs[:] = [name for name in dirs if name not in EXCLUDED_ROOT_DIRS]

        for name in files:
            path = current_path / name
            try:
                total_bytes += path.stat().st_size
            except FileNotFoundError:
                continue
            file_count += 1

    return total_bytes, file_count


def main() -> int:
    total_bytes, file_count = artifact_size(ROOT)
    total_mib = total_bytes / 1024 / 1024
    limit_mib = MAX_ARTIFACT_BYTES / 1024 / 1024

    print(f"Pages artifact: {file_count} files, {total_mib:.1f} MiB")
    print(f"Safety limit: {limit_mib:.0f} MiB (GitHub Pages limit: 1 GB)")

    if total_bytes >= MAX_ARTIFACT_BYTES:
        print("FAIL: Pages artifact exceeds the configured safety limit.")
        return 1

    print("PASS: Pages artifact is below the configured safety limit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
