# 门禁「假绿」体检（2026-11-05）

**触发**：`_test_static.py` 的汇总行在最后一个检查 `check_related_slug_map()` 之前打印，导致 `slug-en` 810 个游离键的告警不进 stdout 的 `⚠️ 警告` 计数，也不进退出码。

**判红口径结论（先回答关键问题）**：`scripts/run_gates.py` 判红**只看子进程退出码**，不解析 stdout、也不读 JSON。证据：[run_gates.py:338](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/run_gates.py#L338) `exit_code = completed.returncode`，之后仅按 `exit_code != 0` 收集失败。

因此，清理前那 810 个游离键对 CI 是**完全隐形**的：`_test_static.py` 旧退出码只判断 `failed`（[旧逻辑] `return 0 if stats['failed'] == 0 else 1`），`warnings` 再多也返回 0。两条线看到的「810 / 0」并不是两份基线，而是同一份运行的两种输出通道（stdout 汇总 vs 报告 JSON / 尾部 ⚠️ 行），详见 §1。

## 1. 已修（每项均自证会变红）

| # | 脚本 | 缺陷类型 | 证据 | CI 生效 | 修法 | 自证 |
|---|---|---|---|---|---|---|
| 1 | `_test_static.py` | 汇总先打印、后跑检查；退出码忽略告警 | [L403-L404](file:///Users/cgw/project/cgw/chenguangwu.github.io/_test_static.py#L403-L404) 现为「先检查」；[L469](file:///Users/cgw/project/cgw/chenguangwu.github.io/_test_static.py#L469) 退出码含 warnings | 是（此前隐形） | ①两个检查移到汇总前；②退出码改为 `failed==0 and warnings==0` | 临时注入 `__gate_selftest__/ghost`：stdout `⚠️ 警告: 1 条`、JSON `warnings=1`、退出码 1；复原后 0/0/exit 0 |
| 2 | `scripts/check_expect_antipattern.py` | 空跑假绿：0 个 expect 数组仍 ✅ | [L106-L109](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/check_expect_antipattern.py#L106-L109) | 是 | `files` 为空或 `scanned==0` → return 1 | 用 monkeypatch 把 glob 指向不存在文件 → ❌ 且 exit 1 |
| 3 | `scripts/selfcheck_false_pass.js` | 静默跳过：用例 eval 失败记 `skip` 后不计检查、仍报绿；`totalChecked==0` 也报绿 | [L228-L236](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/selfcheck_false_pass.js#L228-L236) | 是 | `totalChecked===0` 或 `skipped>0` → exit 1 | `node scripts/selfcheck_false_pass.js /tmp/emptycases` → 判红 exit 1 |
| 4 | `_audit_links.py` | 空跑假绿：读文件异常 `continue`，0 文件 / 0 内链仍报「0 死链」 | [L134-L138](file:///Users/cgw/project/cgw/chenguangwu.github.io/_audit_links.py#L134-L138)（新增 `read_errors`） | 是 | `scanned==0 或 total_links==0 或 read_errors>0` → return 1 | 空 `tools/` 临时仓库跑 `--check` → ❌ exit 1 |
| 5 | `_audit_assets.py` | 空跑假绿：0 页面扫描仍 ✅ | [L226-L229](file:///Users/cgw/project/cgw/chenguangwu.github.io/_audit_assets.py#L226-L229) | 是 | `scanned==0` → return 1 | 同上空仓库 → ❌ exit 1 |
| 6 | `scripts/check_inline_js_syntax.js` | 空跑假绿：`checked==0`（目录缺失/正则失配）仍 ✅ | [L66-L69](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/check_inline_js_syntax.js#L66-L69) | 是 | `checked===0` → `process.exit(1)` | 空 `tools/` 临时仓库 → ❌ exit 1 |
| 7 | `scripts/_ux_baseline.py --gate` | 覆盖收缩被吞：基线有、当前没有的分类 `if not b: continue`；分类/全站页数减少不检查 | [L166-L180](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/_ux_baseline.py#L166-L180) | 是 | 反向遍历基线：分类消失、分类页数下降、全站页数下降全部记 regression；`total==0` 显式 exit 1 | 快照临时加 `__ghost_gate__` 分类 → ❌「分类页数 → 0」exit 1；复原后通过 |

## 2. 已核实无害（不改）

| 脚本 | 结论 | 证据 |
|---|---|---|
| `scripts/discriminate_check.js` | 用户提到的「静默 exit 0」已在现行代码修复：有 `--selftest`、`REAL_PROCESS.exitCode` 全链路、无统计行/用例内 `process.exit(0)` 都会被判红（非本批改动） | [L28](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L28)、[L250](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L250)、[L314-L319](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L314-L319) |
| `scripts/verify_psych_kit.cjs` | `catch(e){}` 只影响计数，但阈值是「注入页面数 **>=** 40」；计数变少会判红，不会假绿 | [L198](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_psych_kit.cjs#L198)、[L201](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_psych_kit.cjs#L201) |
| `_build.py` | 多处 `except Exception` 仅用于可选数据加载；构建末尾一致性检查失败会 `raise SystemExit(1)`，不是吞掉的检查 | [L2799](file:///Users/cgw/project/cgw/chenguangwu.github.io/_build.py#L2799)、[L4877-L4878](file:///Users/cgw/project/cgw/chenguangwu.github.io/_build.py#L4877-L4878) |
| 200+ 个 `scripts/verify_*_calc.js` | 机扫全部：均有 `process.exit(fails.length ? 1 : 0)`，统计行在 exit 之前；无「无条件 exit 0」、无「汇总在退出之后」 | 机扫 `verify_*_calc.js`：ALWAYS-EXIT0=0、NO-EXIT=0、SUMMARY-AFTER-EXIT=0 |
| `scripts/run_gates.py` | 本身无吞异常：`returncode != 0` 收集失败，`--skip-build` 仅本地调试用（CI 不用）；构建失败直接 `return 1` | [L338](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/run_gates.py#L338) |

## 3. 结论与后续

- 本轮体检 **14 个门禁面**：已修 **7 条**（全部含防回归守卫并逐条自证变红），核实无害 **5 条**，已由他线修复 **1 条**，口径澄清 **1 条**。
- 系统性教训：**「检查跑完再打印汇总、退出码必须包含告警、任何扫描型门禁不得以 0 样本判绿」**。后续新增门禁脚本应按此三条自检。
- 本轮未改工具页、未改 `i18n/`、未跑 `_build.py`、未 push。
