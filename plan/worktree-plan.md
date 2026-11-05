# Worktree 并行分层方案（下一批起生效）

> 生成：2026-11-05｜基线 commit `840020995e`（各 worktree 建时 HEAD）
> 原则：**页面/字典按行业独占分到 worktree；共享单点（`_build.py`、229 门禁、`push`、`zh-tw/`）只留在主库。**

## 1. 分配表（目录白名单）

| worktree | 建议归属线 | 目录白名单（只许写这些） | 预期页数 |
|---|---|---|---|
| `/private/tmp/wt-i18n` | i18n 盘点线 | `i18n/tools/en/machinery/**`、`i18n/tools/en/automotive/**` | 字典条目，非页数；覆盖 machinery+automotive 两行业 |
| `/private/tmp/wt-safety` | 安全线（待其报命中目录） | 待确认（报来后补，仅限 `tools/<单一行业>/`） | 待确认 |
| `/private/tmp/wt-zero` | 零覆盖线（待其报行业批次） | 待确认（按行业逐批写入，一批一行业） | 111 页零覆盖分摊，一批 ≤30 页 |
| `/private/tmp/wt-fake` | 假工具线（待其报可开工行业） | 待确认（仅 `tools/<行业>/*.html`，禁碰 `scripts/verify_general_calc.js`） | 待确认 |
| `/private/tmp/wt-interact` | 交互缺陷线（待其报反向不一致集群） | 待确认（仅 `tools/<行业>/*.html`） | 待确认 |

**硬约束**：一个 worktree 只写自己白名单里的目录；跨行业一律回主库申请，不许自行扩围。
**共享单点文件禁止在 worktree 改**：`_build.py`、`scripts/run_gates.py`、`scripts/verify_it_calc.js`、`scripts/verify_general_calc.js`、`js/tool-i18n.js`、`css/**`、`i18n/tools/_en_override.json`、`json/**`。

## 2. worktree 内验收口径（只跑与改动相关，不跑 229）

| 本批改了什么 | worktree 里必须跑 | 不用跑 |
|---|---|---|
| 仅 i18n 字典（`i18n/tools/en/<行业>/**`） | `scripts/_en_i18n_probe.mjs --check <目录>` + 该目录抽 6 页真机英文探针 | 229 / 全站静态 |
| 仅工具页文案/公式框（`tools/<行业>/*.html`） | `node scripts/verify_<行业>_calc.js` + `python3 _test_static.py` + `node scripts/audit_inline_marker_placement.js` | 229 |
| 动了 `calc()` / 默认值 / 输入 id | 行业 verify + `node scripts/discriminate_check.js verify_<行业>_calc.js`（四项：已检/变红/逃生/跳过）+ `node scripts/audit_verify_input_ids.js` | 229 |
| 动了用例（`verify_<行业>_calc.js`） | 行业 verify + `discriminate_check` 四项（逃生必须 0） | 229 |
| 动门禁脚本自身（`scripts/audit_*.js`） | 该脚本 + 构造 1 假红 1 假绿，证明不误报、不假绿 | 229 |
| 任何 worktree | — | `_build.py`、`zh-tw/` 相关、229 全套 |

> `zh-tw/` 相关门禁（繁体死链、繁体产物一致性）**只在主库构建后由集成线跑**；各线 worktree 不生成 `zh-tw/`。

## 3. 合并协议

1. **回主库只用两种方式**：`git -C <worktree> format-patch -1 --stdout | git am -3`，或按路径 `git checkout <worktree-commit> -- <文件清单>`（逐条列明路径）。**禁 `git add -A` / `git add .` / 通配 `git checkout .`。**
2. **一次只合一条线**，合完立刻跑主库全量门禁兜底；局部门禁只是前置筛，不是最终判据。
3. 不同线目录不重叠 ⇒ 冲突应为 0；**一旦出现冲突立刻停手回报**，不许强推、不许 `reset --hard`。
4. **合并顺序**：先合「纯页面/纯字典」批，最后才合共享脚本与字典交叉项；所有批合完后主库统一 `python3 _build.py` → 全量 229 → 唯一一次 push。
5. push 前主库必须跑**全量 229**；`--only` 仅用于 worktree/合并前预检，**不得替代 push 前的全量**。
6. 每条线收口即 `git worktree remove --force <path>`，台账写「已合并 / 可回收」。

## 4. 报告模板（各线统一）

```
① 数字：本批 X 条 / Y 页，前后对比（例：探针残留 3→0）
② 三栏证据：实跑值 / 旧值 / 新值（页面与用例同批改动时必给）
③ 未决项与在途冲突（无则写「无」）
④ git status --short 条数
```
长清单落 `/tmp/<线名>-<批号>.txt` 或 plan 文件，不进回复正文。

## 5. 当前 worktree 台账（2026-11-05 11:55 快照）

| 路径 | HEAD | 归属线 | 已合并 | 可回收 |
|---|---|---|---|---|
| `/private/tmp/wt-i18n` | `840020995e` | i18n 盘点（machinery/automotive） | 否（同线产出实际在 `wt-i18n-ma`） | 待该线确认 |
| `/private/tmp/wt-i18n-ma` | `d9053ee4a8` | 同一字典线（`3a51c3e953` 来源） | 是（`f5d53cbada`） | 可 |
| `/private/tmp/wt-i18n2` | `29c04d8392` | realestate / hydraulic / finance 字典 | 否 | 使用中 |
| `/private/tmp/wt-i18n3` | `29c04d8392` | 备用字典线 | 否 | 空闲 |
| `/private/tmp/wt-i18n4` | `29c04d8392` | agriculture / marketing 字典 | 否 | 使用中 |
| `/private/tmp/wt-clinical` | `6696e2261b` | 临床与教育线 | 是（`e0d0efbf7e`） | 可 |
| `/private/tmp/wt-zero` | `a3e50d8588` | 零覆盖线 | 是（`3aace3ca0e`） | 可 |
| `/private/tmp/wt-safety` | `ccda8b6ec0` | 安全线 | 是（`737df494b4`+`031a64d40e`） | 可 |
| `/private/tmp/wt-interact` | `7b062b7d3a` | 交互缺陷线 | 否 | 使用中（有进程） |
| `/private/tmp/wt-fake` | `840020995e` | 假工具线 | 否 | 空闲 |
| `/tmp/wt_b1` | `3b18edad61` | 假工具线 | 是（`edd7874f4c`） | 可 |
| `/private/tmp/dd-base` | `290c6d8e88` | 机械/detector 指南线 | 历史提交已在 master | 可（status=0、无进程） |

> 回收动作由集成线执行；使用中的 worktree 不动。`dd-base` 无未纳入内容，确认后 `git worktree remove --force`。

## 6. 本轮合并记录（2026-11-05）

| commit | 来源 | 内容 | 主库落地 |
|---|---|---|---|
| `737df494b4` | wt-safety | 4 页用户输入 XSS 源头转义 | 同 hash |
| `031a64d40e` | wt-safety | image-to-base64 属性逃逸 | 同 hash |
| `e0d0efbf7e` | wt-clinical | NCS/EMG、泡水检测未检查态 + process 13 页 oninput | 同 hash |
| `3aace3ca0e` | wt-zero | 5 页零覆盖用例 | 同 hash |
| `edd7874f4c` | wt_b1 | 频谱/HTTP Cookie/铸件缺陷三页宣称对齐 | 同 hash |
| `f5d53cbada` | wt-i18n-ma | machinery/automotive 125 个字典文件 | 同 hash |

- 六个来源 commit 均**无构建产物**，与主库脏文件 0 重叠；`i18n/tools/design.json`、`it.json` 两侧改的是不同 key，`cherry-pick -n` 三方合并 0 冲突，已逐键校验共存。
- 合并后同一次构建窗口重跑 `_build.py`，使 `i18n/tools/en/**` 变更进入 SW 版本戳。
