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

**本轮全量门禁新增红项（219/222 通过；3 项红均为他线在途页面/用例，按约记录路径后跳过）**：

| 红项 | 路径 | 归属判断 |
|---|---|---|
| `aerospace calc correctness`：`aerospace/weight-balance` 未匹配期望值 | `tools/aerospace/weight-balance.html`、`scripts/verify_aerospace_calc.js` | 两文件 `M`（他线在途），非本批 |
| `data calc correctness`：`data/random-3` 未匹配期望值 | `tools/data/random-3.html`、`scripts/verify_data_calc.js` | 两文件 `M`（他线在途），非本批 |
| `anti-regression: case discrimination`：逃生项 4 > 基线 0 | 由 `scripts/verify_data_calc.js` 在途新增用例引入 | 同上，非本批 |

- 本批两道门禁在最终全量运行中均 **PASS**：`history field guard 3/3`；`inline handler global` 静态 2/2 + 动态真触发 6/6。
- 首轮运行中的 `_test_static` 5 个 `__b3base_*` 反链失败与 `_audit_links` 13 个读取失败，均为并发写入竞态（第二轮已自动消失），不列入红项。
- 本轮未改工具页、未改 `i18n/`、未 push。

## 5. 续章：224 道门禁「负向自证」覆盖率普查（2026-11-05，只读）

**问题**：门禁数量已到 224 道，但绝大多数从未被验证「它到底会不会红」。本续章逐项打标，只做统计与出方案，不造红、不改代码。

**口径**：

- **有（直接）**：有实跑证据 —— 故意注入缺陷后，该门禁本身 `exit != 0`。
- **有（共享）**：由已在门禁内运行的元门禁逐用例证明 —— `discriminate_check.js` 把 inputs 换回页面默认值（模拟注入失败），要求每条用例 FAIL；`selfcheck_false_pass.js` 结构判定假用例。二者覆盖的 `verify_*_calc.js` 共用同一判定与退出码。
- **无**：找不到任何「注入缺陷 → 变红」证据，只有失败路径代码。
- **无法自证**：原理上无法在本地/CI 造红（如依赖线上数据）。

**覆盖率**：**224 = 有 218（直接 13 + 共享 205）+ 无 6 + 无法自证 0**，有自证率 **97.3%**。

### 5.1 有自证 · 直接 13 项

| # | 门禁 | 造红证据 | 红的是什么 |
|---|---|---|---|
| 1 | expect anti-pattern | 本文件 §1 #2；[check_expect_antipattern.py:107-109](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/check_expect_antipattern.py#L107-L109) | 空扫描 / 0 个 expect 数组 → exit 1 |
| 3 | static tests | §1 #1；[_test_static.py:469](file:///Users/cgw/project/cgw/chenguangwu.github.io/_test_static.py#L469) | 注入 `__gate_selftest__/ghost` → warnings=1、exit 1 |
| 4 | dead-link audit | §1 #4；[_audit_links.py:134-138](file:///Users/cgw/project/cgw/chenguangwu.github.io/_audit_links.py#L134-L138) | 空仓库（0 文件/0 内链）→ exit 1 |
| 5 | asset audit | §1 #5；[_audit_assets.py:226-229](file:///Users/cgw/project/cgw/chenguangwu.github.io/_audit_assets.py#L226-L229) | 空仓库（0 页面）→ exit 1 |
| 6 | local storage audit | 本会话造红（探针已删） | `_probe_cookie.html` 含 `document.cookie =` → `Cookie 写入 1`、exit 1；删后 exit 0 |
| 7 | external dependency audit | 本会话造红（探针已删） | `_probe_cdn.html` 含未锁版本 lodash → `[FAIL] 外部脚本未锁定精确版本`、exit 1 |
| 8 | inline js syntax | §1 #6；[check_inline_js_syntax.js:67](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/check_inline_js_syntax.js#L67) | 空 `tools/` → `checked===0` → exit 1 |
| 9 | history field guard | §2 模拟环境表 | 必败输入（`rec.conf=conf` 不转义）→ exit 1 |
| 10 | inline handler global | §2 模拟环境表 | 静态 `onclick="__badExport()"` 未定义 → 1/2、exit 1 |
| 17 | science calc correctness | 本次全量日志（`/tmp/gates_full.log`，未入库） | 203 例中 3 例不匹配 → `FAIL ... exit=1`（红因他线在途用例，但证明本门禁判定链路会红） |
| 222 | anti-regression: no fake gates | §1 #3；[selfcheck_false_pass.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/selfcheck_false_pass.js) | 空用例目录 → `totalChecked===0` → exit 1；本次实跑 `checked=9039 risk=0 skipped=0` |
| 223 | anti-regression: case discrimination | [discriminate_check.js:66-73](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L66-L73)、`--selftest` | 未打统计行/0 已检/低于 8000/新增逃生项 → exit 1；本次实跑 `8980/8980 变红、逃生 0、跳过 55` |
| 224 | ux baseline regression | §1 #7；[_ux_baseline.py:142-144](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/_ux_baseline.py#L142-L144) | 快照注入 `__ghost_gate__` 分类 → 分类页数下降、exit 1；`total==0` → exit 1 |

### 5.2 有自证 · 共享 205 项

覆盖：**12、14–16、18–83、85–180、182–220**（全部 `verify_*_calc.js`，不含被隔离的 181）。

- 证据 1（逐用例判别力）：`discriminate_check.js` 对每条用例把 inputs 换回默认值后必须 FAIL —— 本次 **8980/8980 正确变红、逃生项 0**；基线与当前一致（`scripts/discriminate_baseline.json` 的 `escape=0`）。
- 证据 2（假用例结构）：`selfcheck_false_pass.js scripts` 扫描 **9039 条用例、risk=0、skipped=0**；弱用例存量被基线锁定（`no_inputs=10 / all_default=4`，只降不升）。
- 证据 3（判定链路）：200+ 脚本共用 `runCase` + `process.exit(fails.length ? 1 : 0)`（§3 机扫：ALWAYS-EXIT0=0、NO-EXIT=0、SUMMARY-AFTER-EXIT=0），且 #17 已实测该链路会红。
- 证据 4（非空跑）：本次全量日志里每个 calc 门禁都打印了非零用例数（如 `general 362/362`、`it 988/988`、`railway 2/2`），**无 0/0**。

**共享覆盖的两个缺口（已在 §5.4 列入优先项）**：`discriminate` 的 **55 条跳过用例**不参与判定（ psychiatry 6 / rheumatology 4 / hydraulic 3 / psychology 3 / pulmonology 3 等）；`verify_office_calc.js` 是**唯一无统计行的隔离文件**（4 条用例从未被判别）。

### 5.3 无自证 6 项（按风险类型排序）

| # | 门禁 | 类型 | 现状 | 风险点 |
|---|---|---|---|---|
| 2 | build | 子进程型 | 有失败路径（[_build.py:4878](file:///Users/cgw/project/cgw/chenguangwu.github.io/_build.py#L4878) `raise SystemExit(1)`、L4618），但**从未造红** | 构建是后续全部门禁的输入；假绿会让全站产物错误静默通过 |
| 181 | office calc correctness | 判定型（计数） | 4 例正常跑，但判别器侧被隔离（见 [#L342-357](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/discriminate_check.js#L342-L357)） | 4 条用例从未被证明「注入失败会 FAIL」 |
| 84 | psych-kit behavior (jsdom) | 判定型（阈值 40） | 仅靠 [L213](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_psych_kit.cjs#L213) `injected >= 40`；缺 jsdom 时 [L60-61](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_psych_kit.cjs#L60-L61) `SKIP(no-jsdom)` exit 0 | 阈值/注入数从未造红；CI 有 jsdom，本地无依赖时整条不判 |
| 221 | escHtml regression | 判定型（单元断言） | 断言具体、有反例空间，但**从未反向注入** | 若被测函数被改坏仍可能因取错文件/桩而假绿 |
| 11 | calculation regression | 子进程型 | 有 0 页守卫（[verify_calc.js:143-147](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_calc.js#L143-L147)），但无「页面抛错必红」证据 | 冒烟只判「不报错」；页面异常被吞时可能全绿 |
| 13 | it security correctness | 纯文本匹配型 | 4 段正则/语法断言，但第 4 段 `hits.length===0` 仍绿（[L82-103](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_it_security.js#L82-L103)） | 扫描目标消失/正则失配时静默通过 |

> 「无法自证」= **0**：本批 224 项中没有依赖线上数据或只能人工比对的门禁（`_ux_baseline` 的快照已入库、`audit_*` 均本地可判）。

### 5.4 最该先补自证的 10 条（方案，不执行）

排序口径：**判定型（阈值/计数）> 子进程型 > 纯文本匹配型**；同级按影响面。

| 序 | 门禁 | 怎么造红 | 期望报什么 | 复原/落点 |
|---|---|---|---|---|
| 1 | 181 office calc | 先让隔离文件产出统计行（给 `verify_office_calc.js` 的 `pdfjsReady` 轮询加超时/显式汇总），再把 `TB_DISCRIM_STRICT_CHILD=1` 设为默认 | 隔离文件 1 → `❌ 有 1 个 verify 文件无统计行` exit 1；修好后隔离 0、4/4 进入判别 | 判别器 `integrityProblems` 对 `isolatedCount` 默认判红 |
| 2 | 223 discriminate 的 `--selftest` | 门禁命令改为 `node scripts/discriminate_check.js --selftest` 后再跑全站；临时注释掉 `total===0` 判定 | selftest 报「假 harness 被识别为无统计行」；去掉守卫时 selftest exit 1 | 每次 CI 先自检，防「自检本身失效」 |
| 3 | 共享覆盖的 55 条跳过 | 在 `discriminate_baseline.json` 增 `skipped` 并断言 `agg.skipped <= baseline.skipped`；临时把基线改成 54 | `❌ 跳过 55 > 基线 54，判别覆盖回退` | 先补 psychiatry(6)/rheumatology(4)/hydraulic(3) 的可解析默认值 |
| 4 | 84 psych-kit | 从 3 个 `tools/psychiatry|psychology` 页移除 `psych-kit.js` 引用 | `注入页面数 >= 40` 失败（实际 37）→ exit 1 | 造红后复原引用 |
| 5 | 221 escHtml | 临时把 `js/common.js` 的 `escHtml` 改为 `return String(s)` | `fail>=1`、`==== escHtml regression: fail=1 ====` exit 1 | 先确认脚本读的是源文件而非桩副本 |
| 6 | 2 build | 新建 `tools/__gate_probe__/no-meta.html`（缺 `<meta name="toolbox">`），或把 `i18n/tools/_en_override.json` 某值写成字符串 | 构建末尾一致性检查报错、exit 1（若仅 warn 则需升级为 exit 1） | 删探针页 → 重跑 build 恢复 |
| 7 | 11 calc smoke | 在任一被扫页 `calc()` 首行注入 `throw new Error('__probe__')` | `N FAILURES (X pages)`（[verify_calc.js:149-150](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_calc.js#L149-L150)）、exit 1 | 撤销注入（注意别与其他线同页） |
| 8 | 9/10 动态段 SKIP | 在无浏览器环境跑两条，另加 `TB_REQUIRE_DYNAMIC=1` 时 SKIP 即 exit 1 | 现状：`⚠️ SKIP(no-browser)` + exit 0；加开关后 exit 1 | CI 保持宽松，本地/发布前可强制 |
| 9 | 13 it security | 把 `tools/it/regex.html` 的 worker 改回字符串拼装 | `regex.html 仍在用字符串拼装 Worker 源码` exit 1 | 另给第 4 段补 `hits.length===0 → fail` |
| 10 | `run_gates.py --skip-build` | 临时加一个名为 `build-probe` 的门禁，验证过滤只摘 `build`；再临时改成 `gates[1:]` | 期望断言：剩余 **223** 项且首项仍为 `expect anti-pattern`；当前**没有该断言**，误删首项不会被发现 | 在 `main()` 加一行集合断言 |

### 5.5 硬约束核对：`--skip-build` 有无静默跳过

- **结论：只会跳过 `build` 这一项，其余 223 项照常执行。**
- 证据：[run_gates.py:423-427](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/run_gates.py#L423-L427) 为 `gates = [g for g in gates if g[0] != "build"]`（按名字精确过滤），并打印 `WARNING: build gate skipped`；**不存在 `gates[1:]`**。
- 全表 224 项中名字恰为 `build` 的仅第 2 项（无第二项命中）。
- CI 不使用该参数：[quality-gates.yml:45](file:///Users/cgw/project/cgw/chenguangwu.github.io/.github/workflows/quality-gates.yml#L45) 为裸 `python3 scripts/run_gates.py`。
- 残留风险：该过滤无自证（见 §5.4 #10），若将来重命名 build 门禁（如 `build (site)`），`--skip-build` 会**静默失效并真跑构建**（不是跳过，而是反向），本地复检会意外重建产物。建议把过滤改为按命令首项 `_build.py` 识别，并加「摘除集合 == {build}」断言。

### 5.6 本轮口径边界

- 计数取自**并行线有未提交改动**的工作区（`verify_science_calc.js` 等），因此 `science 203 例`、`checked=9039`、`8980/8980` 会随该线合入小幅变动；结论（覆盖机制、缺口位置）不变。
- 本续章**未造红、未改任何门禁脚本**；`plan/` 之外的改动为 0。

