#!/usr/bin/env bash
# 门禁沙箱：在干净临时 worktree 中对指定 commit 跑全量门禁，用完自动清理。
# 用法：
#   bash scripts/gate_worktree.sh            # 默认验证当前 HEAD
#   bash scripts/gate_worktree.sh <commit>   # 验证指定 commit / 分支 / tag
#   bash scripts/gate_worktree.sh <commit> <worktree-path>
# 退出码：run_gates.py 的退出码（0=全过，非 0=有红项）。任何失败都会清理临时目录。
set -uo pipefail

ROOT=$(git rev-parse --show-toplevel) || exit 1
TARGET=${1:-HEAD}
SHA=$(git -C "$ROOT" rev-parse "$TARGET") || { echo "无效目标: $TARGET" >&2; exit 1; }
SHORT=${SHA:0:7}
WT=${2:-/tmp/tb-gate-$SHORT}

cleanup() {
  rm -f "$WT/node_modules" 2>/dev/null || true
  git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || rm -rf "$WT"
  git -C "$ROOT" worktree prune >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

# 幂等：同名 worktree 已存在先清掉（只允许脚本自己创建的路径）
if [ -d "$WT" ]; then
  git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || rm -rf "$WT"
fi
git -C "$ROOT" worktree prune >/dev/null 2>&1 || true

git -C "$ROOT" worktree add --detach "$WT" "$SHA" >/dev/null || { echo "创建 worktree 失败: $WT" >&2; exit 1; }
# 复用主仓库依赖，避免临时目录缺 node_modules 导致构建/门禁误红
if [ -d "$ROOT/node_modules" ]; then ln -sfn "$ROOT/node_modules" "$WT/node_modules"; fi

echo "门禁沙箱: $SHORT @ $WT"
cd "$WT" || exit 1
TZ=UTC LANG=C.UTF-8 python3 scripts/run_gates.py
code=$?
echo "门禁退出码: $code"
exit "$code"
