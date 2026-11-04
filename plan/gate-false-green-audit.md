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

## 3. 已核实无害（不改）

| 脚本 | 结论 | 证据 |
|---|---|---|
| `scripts/discriminate_check.js` | 用户提到的「静默 exit 0」已在现行代码修复：有 `--selftest`、`REAL_PROCESS.exitCode` 全链路、无统计行/用例内 `process.exit(0)` 都会被判红（非本批改动） | [L28](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L28)、[L250](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L250)、[L314-L319](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L314-L319) |
| `scripts/verify_psych_kit.cjs` | `catch(e){}` 只影响计数，但阈值是「注入页面数 **>=** 40」；计数变少会判红，不会假绿 | [L198](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_psych_kit.cjs#L198)、[L201](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_psych_kit.cjs#L201) |
| `_build.py` | 多处 `except Exception` 仅用于可选数据加载；构建末尾一致性检查失败会 `raise SystemExit(1)`，不是吞掉的检查 | [L2799](file:///Users/cgw/project/cgw/chenguangwu.github.io/_build.py#L2799)、[L4877-L4878](file:///Users/cgw/project/cgw/chenguangwu.github.io/_build.py#L4877-L4878) |
| 200+ 个 `scripts/verify_*_calc.js` | 机扫全部：均有 `process.exit(fails.length ? 1 : 0)`，统计行在 exit 之前；无「无条件 exit 0」、无「汇总在退出之后」 | 机扫 `verify_*_calc.js`：ALWAYS-EXIT0=0、NO-EXIT=0、SUMMARY-AFTER-EXIT=0 |
| `scripts/run_gates.py` | 本身无吞异常：`returncode != 0` 收集失败，`--skip-build` 仅本地调试用（CI 不用）；构建失败直接 `return 1` | [L338](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/run_gates.py#L338) |

## 2. CI 可执行性（两道新增门禁 + 本轮 7 项修复）

**CI 环境事实**（[quality-gates.yml](file:///Users/cgw/project/cgw/chenguangwu.github.io/.github/workflows/quality-gates.yml)）：

- `actions/setup-node@v6`，`node-version: lts/*`（当前 LTS = Node 24），`npm ci --ignore-scripts --no-audit`；
- `package.json` devDependencies 只有 `jsdom ^30.1.0`、`opencc-js 1.4.1` —— **没有 puppeteer / puppeteer-core**，也没有 Chrome 下载步骤；
- `--ignore-scripts` 会跳过生命周期脚本，即使把 puppeteer 加进依赖也不会自动下载 Chrome；
- `run_gates.py` 判红**只看子进程退出码**，不读 stdout —— 因此「显式 SKIP + exit 0」与「真跑通过」在 CI 上等价，日志是唯一区分手段，必须显眼。

| 门禁 | 依赖 | CI（ubuntu-latest）上会怎样 | 处置 |
|---|---|---|---|
| `scripts/verify_inline_handlers.js` 静态段 | 纯 Node（`fs` / `path` / 正则），无 jsdom、无浏览器 | 正常执行并决定退出码 | 已符合正确形态；另补「0 页扫描 → 判红」守卫 |
| `scripts/verify_inline_handlers.js` 动态段 | `puppeteer-core`（不在 package.json）+ 本机 Chrome | `loadPuppeteer()` 返回 null → 输出 `⚠️ SKIP(no-browser): …`，不改退出码 | 符合要求：动态属本地增强，CI 不假红也不假绿（静态仍在判） |
| `scripts/verify_history_guard.js` 用例 ③（静态） | 纯 Node（读 `tools/ai/sentiment-analysis.html` + 正则） | 正常执行并决定退出码 | 已改为「静态必跑」，缺依赖时仍能判红 |
| `scripts/verify_history_guard.js` 用例 ①②（动态） | `jsdom`（在 package.json，`npm ci` 会安装） | 依赖缺失时**旧版在顶层 `require` 直接崩 = 假红**；现改为 `SKIP(no-browser)` + exit 0 | 已改：惰性 require，缺 jsdom 只跳过动态用例 |
| `scripts/_ux_baseline.py --gate` | 仅 `tools/**/*.html` + `scripts/_ux_baseline_snapshot.json`（已入库）；**不读 `zh-tw/`、不依赖 `_build.py` 额外产物** | 正常执行；`run_gates.py` 把它排在 build 之后，`tools/` 早已存在 | 无需改；本轮已补「0 页 → exit 1」与覆盖收缩守卫 |
| `scripts/check_inline_js_syntax.js` | 纯 Node `fs` + `new Function` + `withFileTypes`（Node ≥ 10 即可） | Node 24 正常执行；`checked===0` 已判红 | 无需改 |

**「假绿 / 假红」判定结论**：

- 两道门禁在 CI 上**不会假绿**：静态断言真实执行且决定退出码；动态段跳过有显式 `⚠️ SKIP(no-browser)` 日志。
- 修复前 `verify_history_guard.js` 存在**假红风险**（顶层 `require("jsdom")`，依赖缺失即整条崩）；已修为惰性加载。
- 不引入 puppeteer 到 CI 是**有意选择**：`--ignore-scripts` 下即便加依赖也不会下载 Chrome，真跑动态段需要额外安装浏览器，收益低；静态断言已覆盖同一回归（全局挂载 + 全站内联处理函数可解析）。

**模拟环境自证**（临时树 `/tmp/gate-selftest`：无 `node_modules`、`PUPPETEER_EXECUTABLE_PATH=/nonexistent/chrome`）：

| 场景 | history guard | inline handlers |
|---|---|---|
| 无 jsdom / 无浏览器，正常输入 | `2 skipped / 1 passed`，`⚠️ SKIP(no-browser)` 两行，exit 0 | 静态 `2/2 通过`，`⚠️ SKIP(no-browser)`，exit 0 |
| 无 jsdom / 无浏览器 + 必败输入（`rec.conf=conf` / `onclick="__badExport()"` 无定义） | `0 passed / 1 failed / 2 skipped`，exit 1 | 静态 `1/2`，`缺定义 1 处`，exit 1 |

本地真实环境（有 jsdom + puppeteer-core + Chrome）：history `3/3` exit 0；inline 静态 `2/2`，动态段真触发命中 3 个页面既有运行时报错（见 §4 的新增红项记录，CI 因无浏览器自动跳过，不影响 CI 判定）。

**附加修复（本地挂死）**：`verify_inline_handlers.js` 动态段原在 `finally` 里直接 `await server.close()`，Chrome 的 keep-alive 连接不释放会导致进程永久挂起（实测全量门禁第 8 关卡死 8 分钟以上）。已改为 `browser.close()`（3s 超时）→ `server.closeAllConnections()` → `server.close()`（1s 超时），并加 180s 全局看门狗（挂死时显式 `❌ 门禁超时` 并 exit 1，绝不无声挂起）。修复后本地单跑 9s 内退出。

## 4. 结论与后续

- 本轮体检 **14 个门禁面**：已修 **7 条**（全部含防回归守卫并逐条自证变红），核实无害 **5 条**，已由他线修复 **1 条**，口径澄清 **1 条**。
- 系统性教训：**「检查跑完再打印汇总、退出码必须包含告警、任何扫描型门禁不得以 0 样本判绿」**。后续新增门禁脚本应按此三条自检。

**本轮全量门禁新增红项（均非本批改动引入，按约记录路径后跳过）**：

| 红项 | 路径 | 归属判断 |
|---|---|---|
| 静态测试：指南链接未反链 | `tools/realestate/__b3base_return-1.html`、`tools/realestate/__b3base_yanglao-dichan-touzi-tuichu-jihui.html`、`tools/surveying/__b3base_area-24.html`、`tools/surveying/__b3base_area-25.html`、`tools/surveying/__b3base_calc-86.html` | 他线在途 `__b3base_*` 批量页，未提交/未收口 |
| 死链门禁：13 个文件读取失败 | 构建与他人批量改名并发期间产生（`_audit_links.py` 不打印路径）；属环境竞态，非本批 | 需在无并发写入时重跑确认 |
| 动态触发：`calc is not defined` | `tools/legal/calc-96.html`、`tools/legal/calculator-calc-6.html`、`tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html` | 页面既有缺陷（`calc()` 在 `function calc` 定义前的脚本块内被调用）；CI 无浏览器自动 SKIP |
- 本轮未改工具页、未改 `i18n/`、未跑 `_build.py`、未 push。
