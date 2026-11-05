# worktree 登记表

> 一树一线；回收前必须核对「提交已并入 master + 该线回报本批完成 + 无进程占用」三项全部成立。
> 拿不准的一律不删，报集成线裁决。本表由集成线维护，各线开工/收口后回报状态。

**长期规矩（2026-11-05 起）**

1. 一条线一收工就**主动**报「可删 <路径>」，不等催。
2. 存在期间只留「正在推进」的树；**同一线不得按行业拆多棵**（字典线曾拆 `wt-i18n2/3/4` 三棵，最终都停在 `29c04d8392`，已全部回收，属教训）。
3. 回收三条件不变（status 为空 + HEAD 已并入 master + 无进程占用），**永不加 `--force`**。
4. **拆树前先保命**：HEAD 不是 master 祖先的，先打轻量标签 `keep/<树名>-<短hash>` 并确认 `git tag -l 'keep/*'` 可见，才允许 `remove`。
5. **临时构建树用完即删**，不留 `/tmp/tb-*`、`/tmp/ci-sim` 等长期驻留副本。

快照时间：2026-11-05（收敛为单棵 + 1 棵待裁决）　｜　主库 HEAD：`b423c1273b`

| 路径 | HEAD | 归属线 | 状态 | 可否回收 |
|---|---|---|---|---|
| `/Users/cgw/project/cgw/chenguangwu.github.io` | `b423c1273b` [master] | 集成线（唯一构建/push 方） | 使用中 | — |
| `/private/tmp/tb-psqi` | `d715f3fbc7` | psqi 字典线（临时构建树，HEAD 已在 master） | **80 个源码文件 + `i18n/tools/_en_override.json` 未提交**（含 `edu/calc-4`、`dermatology/vasi-vitiligo`、`fishery/feed-protein-fat` 等已确认错值页），非纯产物 | 否（待裁决，不代提交） |

## 存档分支保护（禁止合并）

| 分支 | commit / tag | 性质 | 禁止合并 | 处置条件 | 登记日期 |
|---|---|---|---|---|---|
| `wip/tools-audit-84`（本地，**未推 origin**） | `12c22fba9f` / tag `do-not-merge/tools-audit-84` | 66 页批量改写存档（65 文件 +229/−222），含已确认错值，只能当存档 | 是：禁止整体 merge / cherry-pick / 推送 | 等 64 页全部修正且已并入 master 后，该存档分支与 tag 才可删除 | 2026-11-05 |

## keep 标签（无 worktree 支撑的提交保命）

| 标签 | 原树 | 原 HEAD | 说明 |
|---|---|---|---|
| `keep/wtb2-0850d17` | `wtb2` | `0850d17d9b` | 量表批 4 半成品（缺 pulmonology 6 条用例 + 8 个英文词典 + 三态），**8 页唯一副本** |
| `keep/wt-audit84-6107e9a` | `wt-audit84` | `6107e9a9d4` | 66 页重写线收口点（内容已 pick 进 master） |
| `keep/wt-clinical-24c0bbb` | `wt-clinical` | `24c0bbbf9c` | 临床与教育线 6 批（已 pick 进 master） |
| `keep/wt-interact-7b062b7` | `wt-interact` | `7b062b7d3a` | 交互缺陷线 3 批（已 pick 进 master） |
| `keep/wt-safety-1673b21` | `wt-safety` | `1673b215b4` | 安全线旧树（内容等价补丁已在 master） |
| `keep/wt-safety2-2b7e676` | `wt-safety2` | `2b7e676d26` | 安全线文档面 3 批（已 pick 进 master） |
| `keep/wt-zero-36f1c52` | `wt-zero` | `36f1c52e33` | 用例/零覆盖线（已 pick 进 master） |

## 回收记录

| 时间 | 路径 | 当时 commit | 依据 | 备注 |
|---|---|---|---|---|
| 2026-11-05 12:05 | `/private/tmp/dd-base` | `290c6d8e88` | 提交已在 master、status 0、无进程、线已回报 | 合规 |
| 2026-11-05 12:05 | `/private/tmp/wt-clinical` | `6696e2261b` | **误删**：该线随后重建并继续提交 | 已由该线重建，教训：回收前必须确认「本批完成」回报 |
| 2026-11-05 12:05 | `/private/tmp/wt-zero` | `a3e50d8588` | **误删**：该线随后重建并提交 `ed67923290` | 同上 |
| 2026-11-05 12:05 | `/private/tmp/wt-safety` | `6e4ae6d78e` | **误删**：该线随后重建为 `wt-safety2` | 同上 |
| 2026-11-05 12:05 | `/private/tmp/wt-i18n-ma` | `3a51c3e953` | 已并入 `f5d53cbada`、无进程 | 合规 |
| 2026-11-05 12:05 | `/tmp/wt_b1` | `21099e5026` | 已并入 `0d4e418c70`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wt-fake` | `840020995e` | 三条件全真 | 合规 |
| 2026-11-05 | `/private/tmp/wt-i18n` | `840020995e` | 三条件全真 | 合规 |
| 2026-11-05 | `/private/tmp/wt-i18n2` | `29c04d8392` | 三条件全真 | 合规（空壳） |
| 2026-11-05 | `/private/tmp/wt-i18n3` | `29c04d8392` | 三条件全真 | 合规（空壳） |
| 2026-11-05 | `/private/tmp/wt-i18n4` | `29c04d8392` | 三条件全真 | 合规（空壳） |
| 2026-11-05 | `/private/tmp/ci-sim` | `b423c1273b`（已并入） | 仅 134 个 `_build.py` 产物，清产物与 `node_modules` 软链后删 | 合规（临时构建树） |
| 2026-11-05 | `/private/tmp/wt-audit84` | `6107e9a9d4` | status 0、`keep/wt-audit84-6107e9a`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wt-clinical` | `24c0bbbf9c` | status 0、`keep/wt-clinical-24c0bbb`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wt-interact` | `7b062b7d3a` | status 0、`keep/wt-interact-7b062b7`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wt-safety` | `1673b215b4` | status 0、`keep/wt-safety-1673b21`、`http.server 8148` 已自行结束 | 合规 |
| 2026-11-05 | `/private/tmp/wt-safety2` | `2b7e676d26` | status 0、`keep/wt-safety2-2b7e676`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wt-zero` | `36f1c52e33` | status 0、`keep/wt-zero-36f1c52`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wtb2` | `0850d17d9b` | status 0、`keep/wtb2-0850d17`、无进程 | 合规 |

## 规则

1. 一树一线；不同线不得共用同一 worktree（会抢 `index.lock`）。
2. 线内只 `git commit --only <精确路径>`，禁 `git add -A`；不跑 `_build.py`、不跑全量 229、不生成 `zh-tw/`。
3. 合并由集成线按线逐个执行；冲突即停手回报，不许强推。
4. 回收三项全满足才执行，否则保留并报裁决。
