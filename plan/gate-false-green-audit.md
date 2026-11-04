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

## 6. 混合锚逃生项全站普查（2026-11-05，只读）

### 6.1 机制与口径

`verify_*_calc.js` 的 `expect` 是「**数组中任一命中即通过**」。因此一条用例只要混进一个「**不注入输入、页面默认态本来就存在**」的字符串，其余精确断言全部作废——整条退化成逃生项（土建线实例：会变的 `M_k=180.00` 与不变的 `δ=24.01` 写进同一条，`δ` 默认态即命中）。

普查方法（只读，不改任何用例）：

1. 对每条 `CASES` 用例以 `inputs:{}`、`checkIds:[]`、`radios:{}`、`checks:[]`、`clicks:[]`、`expect:[]` 跑一遍（`expect` 置空 ⇒ 必失败 ⇒ harness 返回默认态全量文本 blob `fullBlob`）；
2. 逐项做 `blob.includes(expectItem)`，记录**默认态已命中**的项；
3. 与注入后命中项比对：只有 `hit` 无 `miss` = 整条退化；`hit` 与 `miss` 并存 = 同源混合锚。

范围：`scripts/verify_*.js` 中 207 个 `*_calc.js`（`verify_calc.js` 是冒烟式目标清单，无 `CASES/expect` 结构，不在口径内）；逐用例 8s 超时，`uncaughtException`/`unhandledRejection` 兜底推进。

### 6.2 总量

| 指标 | 数量 |
|---|---|
| 参与扫描用例 | **9126**（207 文件） |
| `expect` 混入默认态命中项 | **56** |
| 整条退化（默认态命中全部 expect，**真逃生**） | **49** |
| 同源混合锚（默认态命中部分 expect） | **7** |
| `expect` 长度 ≥3 | **7** |
| 超时无法判定 | 2 |
| 取不到 blob 无法判定 | 19 |

> 56 条里，43 条是 `expect` 只有 1 项的单锚用例（默认态即命中，整条完全判别力为 0）；13 条 `expect` ≥2，因 OR 语义同样整条退化。

### 6.3 清单① 疑似混合锚（`expect` ≥2 且至少一项默认态命中）——13 条，全部退化

| 判定 | 文件 | 用例 | expLen | 默认态命中项 | 仅注入后命中 |
|---|---|---|---|---|---|
| 整条退化 | verify_aerospace_calc.js | aerospace/flight-time | 2 | 16 小时 15 分钟 实际飞行时长；-13.0 时差 | - |
| 整条退化 | verify_design_calc.js | design/spacing-scale | 2 | space-4 9.8px；29.8px | - |
| 整条退化 | verify_engineering_calc.js | engineering/heat-transfer | 2 | 传热量 Q 40.00 W；热阻 R 0.5000 K/W | - |
| 整条退化 | verify_general_calc.js | general/calc-13 | 2 | 100 自然日；2400 小时数 | - |
| 整条退化 | verify_hydraulic_calc.js | hydraulic/pressure-drop | 3 | 1.168；2.67；0.00584 | - |
| 同源混合 | verify_hydraulic_calc.js | hydraulic/qudao-buchong-buyu-liusu | 3 | 0.7708；2.57（默认态计算值，非不变量） | 34.47 |
| 整条退化 | verify_hydraulic_calc.js | hydraulic/daohongxi-shuitousunshi-maishen | 3 | 0.2548；0.3058；0.5607 | - |
| 同源混合 | verify_life_calc.js | life/workday-calculator（3 条） | 3 | 周末（已排除）：0 天（合法恒值） | 自然日总数 / 工作日数 |
| 同源混合 | verify_psychiatry_calc.js | psychiatry/rater-23 | 4 | 默认 LSAS 整段（总分 0/144） | 重度社交焦虑；144/144；78/78 |
| 同源混合 | verify_psychology_calc.js | psychology/calc-12 | 2 | 最短板：生活满意度（0 分） | 幸福感总分 90/100 |
| 同源混合 | verify_science_calc.js | science/science-pressure-converter | 2 | 1.0000 m（默认单位） | 1.0000 μ |

判定口径：默认命中项是**默认态计算值**（qudao / pressure-converter / rater-23 / calc-12）⇒ 真逃生；是**与注入无关的合法恒值**（workday 的「周末 0 天」）⇒ 恒值本身合法，但因 OR 语义让整条失效，仍需拆条或改 AND 语义。

### 6.4 清单② 同源混合锚（恒定值 + 变化值同条）——7 条

即上表 6 条「同源混合」用例（workday ×3 计 3 条）。**共同缺陷**：不变量/默认值单独即可让整条 PASS，变化值断言等于没写。修法二选一：① 把不变量移出 `expect`（只留变化值）；② 若确需同时校验，把该条改用「全部命中才 PASS」的语义（需改 harness，影响面大，先做①）。

### 6.5 清单③ `expect` 长度 ≥3 ——7 条（风险最高）

| 文件 | 用例 | expLen | 判据 |
|---|---|---|---|
| verify_hydraulic_calc.js | hydraulic/pressure-drop | 3 | 3 项全在默认态命中 ⇒ 注入完全无效 |
| verify_hydraulic_calc.js | hydraulic/daohongxi-shuitousunshi-maishen | 3 | 同上 |
| verify_hydraulic_calc.js | hydraulic/qudao-buchong-buyu-liusu | 3 | 2 项默认命中，仅 34.47 需注入 |
| verify_life_calc.js | life/workday-calculator ×3 | 3 | 恒值「周末 0 天」默认命中，两条变化值作废 |
| verify_psychiatry_calc.js | psychiatry/rater-23 | 4 | 默认 LSAS 整段命中，3 条注入断言作废 |

### 6.6 真逃生高亮（49 条整条退化）

这 49 条的**分类门禁现在绿得毫无意义**（不注入任何输入也 100% PASS）：

| 文件（简写） | 用例 |
|---|---|
| acupuncture | needle-retention、needling-depth |
| admin | detector-time |
| aerospace | flight-time |
| agriculture | machinery-efficiency |
| audio | audio-cut |
| beauty | calc-2、skincare-routine |
| ceramics | glaze-temp |
| chess | xiangqi-endgame |
| chinese-cook | wok-heat |
| cognition | human-benchmark |
| dentistry | tongue-oral-health、wisdom-tooth |
| design | photo-print-size、spacing-scale |
| edu | convert-area-volume |
| electromagnetism | free-space-impedance |
| electronics | resistor-calculator |
| engineering | heat-transfer |
| film | color-grading |
| forensic-medicine | drowning-diatom |
| gardening2 | pest-control |
| general | calc-13 |
| hydraulic | pressure-drop、daohongxi-shuitousunshi-maishen |
| image | nine-grid-cutter |
| kids | stroke-order |
| language | idiom-solitaire |
| legal | court-fee |
| library | citation-format |
| life | age-in-days |
| mechanical | spring-rate |
| misc2 | travel/luggage-size |
| misc | science/physics-constants |
| music | ear-trainer |
| office | ~~mindmap~~ **已修复（2026-11-05）**：降级大纲 + 2 条判别用例，跳过 55→54 |
| ophthalmology | amblyopia-stereopsis |
| paper | paper-grade |
| pet | training-planner |
| rheumatology | anca-classification、behcet-hla、ssa-ssb |
| science | convert-power |
| startup | equity-calculator |
| stats | sample-size |
| tcm-diagnosis | etiology-tree |
| text | convert-6 |
| wedding | wedding-banquet |

典型形态：`expect` 锚的是**默认态就存在的静态表/空状态/错误提示**（`请添加会议日程并填写时间`、`请先上传图片`、`请检查网络连接后刷新页面重试`、`请至少输入一台有效农机数据`），或**默认输入的输出值**（`376.73`、`0.224809`、`3.842`、`14 桌`、`2,300`）。

### 6.7 结论

- **56/9126 ≈ 0.61%** 的用例存在默认态命中项；其中 **49 条完全丧失判别力**（`office/mindmap` 已于 2026-11-05 修复，**待修 48 条**）。
- 这批不是「用例写得不够精确」，而是**门禁语义（OR）与用例设计（多锚）冲突**。只要 harness 保持「任一命中即通过」，多锚用例必须满足「**每一项都只能由注入输入产生**」。
- 只出清单，不改用例；各分类线按 §6.3–§6.5 自行修条。优先级：清单③（expect≥3）→ 清单② → 清单① → 剩余单锚全命中。
- 2 条超时与 19 条无 blob 的用例**未判定**（可能含同类缺陷），需各线在页面可跑后复扫。

### 6.8 mindmap 修复记录（2026-11-05，本线）

- **页面**：库缺失分支新增纯 JS 降级大纲（嵌套 `<ul>` + `data-zh` 双语提示 + 「大纲节点：N」计数），并绑定 `input` 实时刷新；保留原加载失败提示，**未改** PNG/SVG 导出路径。
- **用例**：`office/mindmap` 由锚「库加载失败文案」（默认态必命中）重写为锚降级产物；另加 1 条反向用例（仅该条注入 `window.markmap` 桩，断言 `MARKMAP-STUB-OK` 只可能来自 markmap 分支）。
- **判别**：office 单文件 `已检 9 / 正确变红 9 / 逃生 0 / 跳过 0`；跳过基线 55 → 54（已检 4920 → 4922）。
- **断 CDN 真机**（Chrome headless，拦截 `cdn.jsdelivr.net` 3 个请求）：中/英两态均渲染 7 节点、层级 `1,2,3,3,2,3,4`，`pageerror = 0`。

### 6.9 待修 48 条的分派建议（按分类归属）

| 建议归属 | 条数 | 用例 |
|---|---|---|
| 临床/医学线 | 9 | dentistry/tongue-oral-health、dentistry/wisdom-tooth、ophthalmology/amblyopia-stereopsis、rheumatology/anca-classification、behcet-hla、ssa-ssb、forensic-medicine/drowning-diatom、tcm-diagnosis/etiology-tree、psychiatry/rater-23（同源）、psychology/calc-12（同源） |
| 土建/工程线 | 8 | hydraulic/pressure-drop、daohongxi-shuitousunshi-maishen、qudao-buchong-buyu-liusu（同源）、engineering/heat-transfer、mechanical/spring-rate、ceramics/glaze-temp、agriculture/machinery-efficiency、gardening2/pest-control |
| 数理/科学线 | 10 | science/convert-power、science/science-pressure-converter（同源）、stats/sample-size、misc/science/physics-constants、electromagnetism/free-space-impedance、electronics/resistor-calculator、general/calc-13、edu/convert-area-volume、aerospace/flight-time、design/spacing-scale |
| 生活/文化线 | 11 | life/age-in-days、life/workday-calculator ×3（同源）、wedding/wedding-banquet、kids/stroke-order、music/ear-trainer、chess/xiangqi-endgame、language/idiom-solitaire、library/citation-format、text/convert-6、chinese-cook/wok-heat |
| 设计/影像/内容线 | 6 | design/photo-print-size、image/nine-grid-cutter、film/color-grading、audio/audio-cut、beauty/calc-2、beauty/skincare-routine |
| 杂项线 | 5 | admin/detector-time、pet/training-planner、startup/equity-calculator、legal/court-fee、cognition/human-benchmark、misc2/travel/luggage-size、paper/paper-grade |
| 办公线（本线） | 0（已修） | office/mindmap（降级渲染 + 反向桩用例） |

注：同源混合锚的修法统一为「把恒定值/默认值移出 `expect`，只留注入后才出现的变化值」；`expect≥3` 的三条（pressure-drop / daohongxi / qudao）需优先拆条。

## 7. 新增门禁登记（两条均已接入：verify input ids #228 / deepdive source sync #229）

| 项 | 状态 | 条目原文 | 脚本 / 语义 | 造红方式 | CI 耗时 | 当前是否预期红 |
|---|---|---|---|---|---|---|
| `verify input ids` | **已接入（#228）** | `("verify input ids", ("node", "scripts/audit_verify_input_ids.js"))` | `scripts/audit_verify_input_ids.js`：扫描 207 个 verify 文件 / 8963 条用例 / 28180 个注入键，比对注入键在对应页面 HTML 是否存在；**僵尸 id 即 exit 1**（动态生成/模板拼接判为存疑不算违规） | 修好某条僵尸 id 用例前天然红；绿路径已用 `verify_sports_calc.js` 单文件验证 exit 0 | **1.3s**（纯 node 标准库，无 node_modules/浏览器） | **是，41 条僵尸 id**（22 条 `detector-*` 优先），由用例修复线收口，禁止调口径改绿 |
| `deepdive source sync` | **已接入（#229）** | `("deepdive source sync", ("python3", "scripts/audit_deepdive_source_sync.py", "--check"))` | 页面 deep-dive 段与 `content_deepdive.json` 逐字不一致即 exit 1（`--report` 只列不判红） | 临时改某页 deep-dive 段一个字 → `--check` 必须 exit 1 | **0.9s**（扫描 4573 页，纯 python3 标准库） | 接入时已绿：土建线 `a9c57d5a2f` 已同步 `civil/rc-beam-rebar` scenarios，`--check` 0 不一致 |

### 7.1 验收时发现并修复的脚本缺陷（verify input ids）

`audit_verify_input_ids.js` 通过 `require(verify_it_calc.js)` 复用 `extractCases`，而 harness 的 `beforeExit` 兜底会在「0 用例执行」时打印 `❌ 0 个用例实际执行…` 并**覆盖 `process.exitCode = 1`** —— 即使 41 条僵尸 id 全部修完，该门禁也**永远无法转绿**。已加 1 行 `process.env.TB_DISCRIM_PARENT = "1"`（harness 已有的父进程逃生口）抑制兜底；已验证：全量 exit 1（41 条僵尸）、`verify_sports_calc.js` 单文件 exit 0，且不再出现该误导行。

### 7.2 条目数口径

- 当前：**229**（227 + `verify input ids` #228 + `deepdive source sync` #229）；
- `--skip-build` 后实际执行 **228**（摘除 `build`，首项仍为 `expect anti-pattern`）；
- 每次变更必须同批更新 `scripts/gates_manifest.txt`，否则清单棘轮在启动时判红（已验证「少一条 / 多一条 / 乱序」三个方向均 `SystemExit`）。

背景：设计生活线普查 4726 条 deep-dive（一致 4569 / 无对应页面 153 / **有差异 4**）。那 4 条（`dic-scoring`、`ipss-r`、`cml-monitoring`、`mpn-scoring`）页面已由临床线修正，但 `content_deepdive.json` 仍是 2026-09-09 旧值；`_build.py` 在页面找不到 deep-dive 段时会用 JSON **重建整段**，因此跑一次构建就会把修复回退。门禁用于拦截「页面已改、JSON 未同批改（indent=1）」的状态。

接入约束（插入时必做）：

1. **条目总数 227 → 228**，同批更新 `scripts/gates_manifest.txt`（清单棘轮会拦「多一条未登记」）；
2. 插入位置按运行时线惯例放 `GATES` 末尾（不影响「首项 expect anti-pattern」与「--skip-build 摘除恰为 {build}」两条断言）；
3. 插后重跑 `--skip-build` 造红（首项改名 / build 改名），并在干净 worktree 口径验证脚本无依赖（纯 python3 标准库）；
4. 造红：临时把某页 deep-dive 段改一个字 → `--check` 必须 exit 1 并报「页面与 source 不一致」。

### 7.3 【硬条款】全量门禁只在 detached worktree 跑，主工作区只允许 `--skip-build`

> **2026-11-05 事故定论**：`run_gates.py` 第 2 项 `build`（`_build.py`）**不是只读门禁，是对共享工作区的写操作** —— 它会重写 `json/*.json`、`sitemap.xml`、`zh-tw/`，并在页面里找不到 `_dd_html` 时**用 `i18n/tools/content_deepdive.json` 整段重建 deep-dive**。实测 05:08:43/44 把 `hematology/cml-monitoring`、`hematology/mpn-scoring` 两页 clinical 线刚修好的 deep-dive 按旧 JSON 回写；**回写后全量门禁仍全绿**，因为它验证的就是回写后的状态。在 11 条线并行改同一仓库的前提下，任何一次主工作区全量都可能静默回退他线在途修复。

**硬性规矩（无例外）**：

1. **全量（含 `_build.py`）只在 detached worktree 里跑**：
   ```bash
   git worktree add --detach /tmp/gate-run HEAD
   cd /tmp/gate-run && python3 scripts/run_gates.py            # 完整 229 项
   cd /tmp/gate-run && python3 scripts/run_gates.py --skip-build  # 快速反馈
   ```
   跑完 `git worktree remove --force /tmp/gate-run`。worktree 里 `_build.py` 的写入全部落在 `/tmp/gate-run`，**主工作区字节不动**。
2. **主工作区只允许 `--skip-build`**：它摘除 `build`（按命令首项 `python3 _build.py` 识别，`prune_build_gate` 断言摘除集合恰为 `{build}`），不产生任何构建写入。
3. **每次全量跑完必须报 `git status --short` 的条数**（worktree 内跑则报主工作区的条数，作为「这次跑动了什么」的证据；条数较上次异常增减即需逐条解释）。
4. **发现他线页面/JSON 被回退，只报告清单，不得自行 revert**：涉及别线在途内容，由统一维护者处置；本线只提供证据（文件路径 + 差异字段 + 回写时间）。
5. **本线自己改页面的批次**：仍按项目原流程在**主工作区**手改 + 收尾构建 + 提交（构建是提交前的最后一步）；**门禁全量验证**改用 worktree 对同一 HEAD 复跑，避免二次构建写主工作区。
6. **【验收口径】** 全量门禁的「通过」必须来自 **detached worktree @ HEAD**，且必须同时报 `git status --short` 条数；主工作区的 `--skip-build` 结果**只作快速反馈，不作为发布依据**。理由：主工作区的树随时被 11 条线改动，**在主工作区跑出来的绿，绿的可能是别人未提交的半成品**。
7. **【构建产物归属】主工作区的构建产物不由本线 revert / 不由本线提交**：留给集成线统一入库（它们本来就是构建输出，push 时必须带上）。
   - 2026-11-05 报告时点待集成入库 **124 条**：构建产物类 **18**（`json/*.json` 14 + `sitemap.xml` + `sitemap.html` + `index.html` + `sw.js`）+ 分类索引 **15**（`tools/<行业>/index.html`）+ 工具页 **79**（他线在途源码改动）+ 源文件 **12**（i18n/js/scripts/`AGENTS.md`）；`zh-tw/` 为 gitignore，不进 status。
   - 任何人不得把上述产物当垃圾清掉；数量随他线提交变动，以跑全量时实测条数为准。

### 7.4 防回退措施有效性证据（幂等重放）

`hematology/cml-monitoring.html`、`hematology/mpn-scoring.html` 的 mtime 为 **05:09:55 / 05:09:57**（构建确实写了这两页），但**内容与 HEAD 逐字一致、`git status` 为 clean**，且全站 `audit_deepdive_source_sync.py --check` 为 **0 页不一致**。

即：当「页面修复」与 `content_deepdive.json` 源头**同批同步**之后，`_build.py` 的 deep-dive 回写从**破坏性覆盖**变成**幂等重放**（写入但产出与 HEAD 相同，不产生 diff）。这是 §7.3 与 `deepdive source sync` 门禁有效的正面证据，不只是「又加了一条门禁」。

