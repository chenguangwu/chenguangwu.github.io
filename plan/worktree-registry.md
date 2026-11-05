# worktree 登记表

> 一树一线；回收前必须核对「提交已并入 master + 该线回报本批完成 + 无进程占用」三项全部成立。
> 拿不准的一律不删，报集成线裁决。本表由集成线维护，各线开工/收口后回报状态。

**长期规矩（2026-11-05 起）**

1. 一条线一收工就**主动**报「可删 <路径>」，不等催。
2. 存在期间只留「正在推进」的树；**同一线不得按行业拆多棵**（字典线曾拆 `wt-i18n2/3/4` 三棵，最终都停在 `29c04d8392`，已全部回收，属教训）。
3. 回收三条件不变（status 为空 + HEAD 已并入 master + 无进程占用），**永不加 `--force`**。

快照时间：2026-11-05（全线收尾后）　｜　主库 HEAD：`33fde61c6e`

| 路径 | HEAD | 归属线 | 状态 | 可否回收 |
|---|---|---|---|---|
| `/Users/cgw/project/cgw/chenguangwu.github.io` | `33fde61c6e` [master] | 集成线（唯一构建/push 方） | 使用中 | — |
| `/private/tmp/ci-sim` | `3ee28abebc` (detached) | 集成线（干净构建树） | 使用中 | 否（仅集成线可删） |
| `/private/tmp/tb-psqi` | `d715f3fbc7` | psqi 字典线 | 使用中（主库已含 `29278f8519`） | 待该线回报本批完成 |
| `/private/tmp/wt-audit84` | `6107e9a9d4` | 66 页重写线 | 使用中（已并入 `c1c2f4d76c` 空提交跳过、`d8d05b94ec` 空提交跳过、`6107e9a9d4` 已并入） | 否 |
| `/private/tmp/wt-clinical` | `24c0bbbf9c` | 临床与教育线 | 已并入 6 批（`a7b0d16543`…`998f0b143d`） | 待该线回报本批完成 |
| `/private/tmp/wt-interact` | `7b062b7d3a` | 交互缺陷线 | 已并入 3 批（`cf75acad23`/`267805fdeb`/`0d0b2f5c55`） | 待该线回报本批完成 |
| `/private/tmp/wt-safety` | `1673b215b4` | 安全线（已被 `wt-safety2` 接替） | **进程占用**（`python3 -m http.server 8148`，pid 48643），内容等价补丁均已在 master | 否（进程占用，待其自然结束） |
| `/private/tmp/wt-safety2` | `2b7e676d26` | 安全线（文档面） | 已并入 3 批（`969d908e30`/`878cad2d03`/`2b7e676d26`） | 待该线回报本批完成 |
| `/private/tmp/wt-zero` | `36f1c52e33` | 用例/零覆盖线 | 已并入 `9643fb8fbf`/`36f1c52e33` | 待该线回报本批完成 |
| `/private/tmp/wtb2` | `0850d17d9b` | 量表线 | 批 1~3 已并入（`78f4bc8f9b`/`b5ecf76940`/`bc6826f008`/`6c252c5486`）；**批 4 `0850d17d9b` 未并入**（缺 pulmonology 6 条用例 + 8 个英文词典 + 三态未做） | 否 |

## 存档分支保护（禁止合并）

| 分支 | commit / tag | 性质 | 禁止合并 | 处置条件 | 登记日期 |
|---|---|---|---|---|---|
| `wip/tools-audit-84`（本地，**未推 origin**） | `12c22fba9f` / tag `do-not-merge/tools-audit-84` | 66 页批量改写存档（65 文件 +229/−222），含已确认错值，只能当存档 | 是：禁止整体 merge / cherry-pick / 推送 | 等 64 页全部修正且已并入 master 后，该存档分支与 tag 才可删除 | 2026-11-05 |

## 回收记录

| 时间 | 路径 | 当时 commit | 依据 | 备注 |
|---|---|---|---|---|
| 2026-11-05 12:05 | `/private/tmp/dd-base` | `290c6d8e88` | 提交已在 master、status 0、无进程、线已回报 | 合规 |
| 2026-11-05 12:05 | `/private/tmp/wt-clinical` | `6696e2261b` | **误删**：该线随后重建并继续提交 | 已由该线重建，教训：回收前必须确认「本批完成」回报 |
| 2026-11-05 12:05 | `/private/tmp/wt-zero` | `a3e50d8588` | **误删**：该线随后重建并提交 `ed67923290` | 同上 |
| 2026-11-05 12:05 | `/private/tmp/wt-safety` | `6e4ae6d78e` | **误删**：该线随后重建为 `wt-safety2` | 同上 |
| 2026-11-05 12:05 | `/private/tmp/wt-i18n-ma` | `3a51c3e953` | 已并入 `f5d53cbada`、无进程 | 合规 |
| 2026-11-05 12:05 | `/tmp/wt_b1` | `21099e5026` | 已并入 `0d4e418c70`、无进程 | 合规 |
| 2026-11-05 | `/private/tmp/wt-fake` | `840020995e` | status 0、HEAD 已并入 master、lsof 0 | 合规 |
| 2026-11-05 | `/private/tmp/wt-i18n` | `840020995e` | status 0、HEAD 已并入 master、lsof 0 | 合规 |
| 2026-11-05 | `/private/tmp/wt-i18n2` | `29c04d8392` | status 0、HEAD 已并入 master、pgrep/lsof 0 | 合规（空壳，同线三棵） |
| 2026-11-05 | `/private/tmp/wt-i18n3` | `29c04d8392` | status 0、HEAD 已并入 master、pgrep/lsof 0 | 合规（空壳，同线三棵） |
| 2026-11-05 | `/private/tmp/wt-i18n4` | `29c04d8392` | status 0、HEAD 已并入 master、pgrep/lsof 0 | 合规（空壳，同线三棵） |

## 规则

1. 一树一线；不同线不得共用同一 worktree（会抢 `index.lock`）。
2. 线内只 `git commit --only <精确路径>`，禁 `git add -A`；不跑 `_build.py`、不跑全量 229、不生成 `zh-tw/`。
3. 合并由集成线按线逐个执行；冲突即停手回报，不许强推。
4. 回收三项全满足才执行，否则保留并报裁决。
