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

## 5. 当前活着的 worktree 台账

见每轮集成报告「worktree 台账」一节（路径 / commit / 归属 / 已合并 / 可回收）。
