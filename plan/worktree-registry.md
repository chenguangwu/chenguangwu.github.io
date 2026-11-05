# worktree 登记表

> 一树一线；回收前必须核对「提交已并入 master + 该线回报本批完成 + 无进程占用」三项全部成立。
> 拿不准的一律不删，报集成线裁决。本表由集成线维护，各线开工/收口后回报状态。

快照时间：2026-11-05 12:20　｜　主库 HEAD：`e6a98a2540`

| 路径 | HEAD | 归属线 | 状态 | 可否回收 |
|---|---|---|---|---|
| `/Users/cgw/project/cgw/chenguangwu.github.io` | `e6a98a2540` [master] | 集成线（唯一构建/push 方） | 使用中 | — |
| `/private/tmp/wt-clinical` | `6696e2261b` | 临床与教育线 | 使用中（17 条在途） | 否 |
| `/private/tmp/wt-safety` | `1673b215b4` | 安全线 | 已并入 master，无进程 | 待该线回报本批完成 |
| `/private/tmp/wt-safety2` | `1673b215b4` | 安全线（重建） | 使用中（1 条在途） | 否 |
| `/private/tmp/wt-zero` | `ed67923290` | 用例/零覆盖线 | 已并入 master，无进程 | 待该线回报本批完成 |
| `/private/tmp/wt-interact` | `7b062b7d3a` | 交互缺陷线 | 使用中 | 否 |
| `/private/tmp/wtb2` | `e56f59f0c8` | 假工具线 | 已并入 master，无进程 | 待该线回报本批完成 |
| `/private/tmp/wt-fake` | `840020995e` | 假工具线（旧树） | 空闲，已被 `wtb2` 取代 | 待该线确认后回收 |
| `/private/tmp/wt-i18n` | `840020995e` | i18n 盘点线 | 空闲 | 待该线确认 |
| `/private/tmp/wt-i18n2` | `29c04d8392` | realestate / hydraulic / finance 字典线 | 使用中 | 否 |
| `/private/tmp/wt-i18n3` | `29c04d8392` | 备用字典线 | 空闲 | 否（保留待派） |
| `/private/tmp/wt-i18n4` | `29c04d8392` | agriculture / marketing 字典线 | 使用中 | 否 |

## 回收记录

| 时间 | 路径 | 当时 commit | 依据 | 备注 |
|---|---|---|---|---|
| 2026-11-05 12:05 | `/private/tmp/dd-base` | `290c6d8e88` | 提交已在 master、status 0、无进程、线已回报 | 合规 |
| 2026-11-05 12:05 | `/private/tmp/wt-clinical` | `6696e2261b` | **误删**：该线随后重建并继续提交 | 已由该线重建，教训：回收前必须确认「本批完成」回报 |
| 2026-11-05 12:05 | `/private/tmp/wt-zero` | `a3e50d8588` | **误删**：该线随后重建并提交 `ed67923290` | 同上 |
| 2026-11-05 12:05 | `/private/tmp/wt-safety` | `6e4ae6d78e` | **误删**：该线随后重建为 `wt-safety2` | 同上 |
| 2026-11-05 12:05 | `/private/tmp/wt-i18n-ma` | `3a51c3e953` | 已并入 `f5d53cbada`、无进程 | 合规 |
| 2026-11-05 12:05 | `/tmp/wt_b1` | `21099e5026` | 已并入 `0d4e418c70`、无进程 | 合规 |

## 规则

1. 一树一线；不同线不得共用同一 worktree（会抢 `index.lock`）。
2. 线内只 `git commit --only <精确路径>`，禁 `git add -A`；不跑 `_build.py`、不跑全量 229、不生成 `zh-tw/`。
3. 合并由集成线按线逐个执行；冲突即停手回报，不许强推。
4. 回收三项全满足才执行，否则保留并报裁决。
