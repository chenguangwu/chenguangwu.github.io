# 222 道门禁「CI 可执行性」普查（2026-11-05）

**审计基线**：干净 worktree `78150c6a6b00`（`/tmp/gate-ci-audit`，**无 node_modules、无 Chrome、无外部网络**）。
主工作区 HEAD 随后前移到 `908628aa6dc8`（他线提交）：期间仅 18 个 calc 门禁脚本新增用例、未新增依赖，已在主工作区逐个复跑，**18/18 exit 0**（含 `verify_it_calc` 987/987、`verify_ai_calc` 121/121 + DOM 4/4），结论不变。

## 0. 结论（先看）

| 档位 | 数量 | 门禁 |
|---|---|---|
| 真绿（含 4 道动态段 SKIP） | **220** | 其余全部门禁 |
| 真红（依赖缺失，CI 由 npm ci 提供） | **1** | `build`（缺 opencc-js） |
| 真红（他线在途，非本批） | **1** | `anti-regression: case discrimination`（ecommerce 4 条逃生项） |
| 假红（依赖缺失即崩，**已修**） | **2 → 0** | `ai calc correctness`、`psych-kit behavior (jsdom)` |
| 假绿（0 用例 / 0 文件仍 exit 0） | **0** | — |
| 挂死（单道 >120s） | **0** | — |

**「假红」清单（按门禁名，修前）**

1. `ai calc correctness` —— 顶层 `require("jsdom")`，干净环境 `Cannot find module 'jsdom'` → exit 1；
2. `psych-kit behavior (jsdom)` —— 同上。

两处均已改为惰性加载 + 显式 SKIP，修后干净环境 exit 0。`build` 的 `opencc-js` 是 `package.json` 声明、CI `npm ci` 必装的合法依赖，报错文本明确（`OpenCC locale build failed`），不算门禁缺陷。

## 1. 普查口径

```bash
git worktree add /tmp/gate-ci-audit HEAD        # 78150c6a6b00，不装依赖
export PUPPETEER_EXECUTABLE_PATH=/nonexistent/no-chrome-binary
export CHROME_PATH=/nonexistent/no-chrome-binary
export HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9
export NO_PROXY=127.0.0.1,localhost
export HOME=/tmp/gate-ci-home TMPDIR=/tmp/gate-ci-tmp
```

- 登记表直接 `import run_gates` 读取 222 道，逐道串行执行；单道 `subprocess` 上限 **120s**，超时 `killpg`。
- 判红口径与 CI 一致：只看子进程退出码（[run_gates.py:338](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/run_gates.py#L338)），不解析 stdout。
- 是否「假绿」另看 stdout：calc 门禁须打印 `N/N` 且 `N>0`；审计类须打印扫描文件/页数（非零）。
- 为让后续门禁拿到 CI 同款构建产物，审计前用本地依赖临时符号链接跑了一次 `_build.py` 生成 `zh-tw/`，随后**移除符号链接**再逐道普查（门禁运行阶段无 `node_modules`）。

## 2. 三档计数与证据

- **假红 2（已修）**：见 §0 清单；修前 gate 18/82 均 `exit 1 / 0.0s / MODULE_NOT_FOUND`。
- **挂死 0**：最长 `build` 52.3s、次长 `case discrimination` 36.2s、第三 `static tests` 14.2s，均远低于 120s；无任何门禁被 `killpg`。
- **假绿 0**：206 道 calc 门禁全部打印真实用例数（最小 `railway` 2/2、`audio` 3/3），`verify_calc` 打印 `84 pages`；审计类打印 16677 文件 / 17047 inline script / 8938 checked；`ux baseline` 有基线均分。**未发现「0 用例仍 exit 0」**。
- **真红 2**：`build` 属依赖缺失（CI 安全）；`case discrimination` 属他线在途（ecommerce 4 条逃生项，基线 0）。

## 3. 修复与两向自证

| 文件 | 改动 | 覆盖 | 正常环境自证 | 注入必败自证 |
|---|---|---|---|---|
| `scripts/verify_it_calc.js` | `runCase` 统计真实执行数；`beforeExit` 时若为 0 则 exit 1 | 全部复用 harness 的 **206 道 calc 门禁** | `it` 987/987、`yi` 4/4、`edu` 88/88 均 exit 0 | 临时探针不执行任何用例 → `❌ 0 个用例实际执行` + exit 1 |
| `scripts/verify_ai_calc.js` | `jsdom` 惰性加载；缺失时仅 DOM 宿主段 `SKIP(no-jsdom)` | gate 18 | 主工作区 121/121 + DOM 4/4 | 干净环境 exit 0 + `SKIP 4` |
| `scripts/verify_psych_kit.cjs` | `jsdom` 惰性加载；缺失时全段显式 SKIP | gate 82 | 32 通过 / 0 失败 | 干净环境 exit 0 + `SKIP(no-jsdom)`（不再 require 崩溃） |
| `scripts/verify_calc.js` | 新增 `checked` 计数；0 页面实际执行 → exit 1 | gate 9 | `ALL OK (84 pages)` exit 0 | 全部目标伪装成 `TOOLBOX-REDIRECT` → exit 1 |

**未降级任何真实断言**：4 处改动均为「计数器 / 惰性依赖 / 显式跳过」，未删除或放宽任何 `expect`；`ai` 的 121 条数值用例在无 jsdom 时仍全部执行。

## 4. 此前 7 项门禁面 + 两道新门禁的 CI 依赖复核

| 门禁面 | 脚本 | 依赖 | 是否依赖 zh-tw / `_build.py` 产物 | CI 结论 |
|---|---|---|---|---|
| 静态测试汇总 | `_test_static.py` | python3 标准库 | 否（直接读 `tools/`） | 绿 |
| expect 反模式 | `scripts/check_expect_antipattern.py` | python3 标准库 | 否（扫 `scripts/`） | 绿 |
| 假绿自检 | `scripts/selfcheck_false_pass.js` | node 内建 | 否 | 绿 |
| 死链审计 | `_audit_links.py` | python3 标准库 | 否（`zh-tw/` 存在则多扫，缺失仍有 `tools/`） | 绿 |
| 资产审计 | `_audit_assets.py` | python3 标准库 | 否 | 绿 |
| 内联 JS 语法 | `scripts/check_inline_js_syntax.js` | node 内建 `new Function` | 否 | 绿（不依赖 Node 新特性，lts ≥18 可跑） |
| UX 基线 | `scripts/_ux_baseline.py --gate` | python3 标准库 | 否（只扫 `tools/`） | 绿 |
| 历史区字段守卫 | `scripts/verify_history_guard.js` | node + jsdom（惰性） | 否 | 绿：CI `npm ci` 提供 jsdom，3 用例全跑 |
| 内联事件全局函数 | `scripts/verify_inline_handlers.js` | node + Chrome/puppeteer（惰性） | 否 | 绿：静态 2 项执行；动态段 `SKIP(no-browser)`；180s watchdog |

## 5. 附注

- **CI 实际环境**（`.github/workflows/quality-gates.yml`）：`npm ci --ignore-scripts` 安装 jsdom / opencc-js，**不装 puppeteer、不下载 Chrome**。因此 `build`、`history field guard`、`ai calc`、`psych-kit` 在 CI 均完整执行；唯一按设计 SKIP 的是 `inline handler global` 的动态触发段。
- **门禁必须串行跑**：普查期间并发跑同一 worktree 时，`edu-unit-converter` 出现 `switchTab: event is not defined` 的 85/86（定时器/初始化串扰）；串行复跑稳定 86/86。CI 与本地都不应并行跑多个门禁进程。
- **120s 只是普查上限**，不是 CI 限制；`build` 在 ubuntu runner 可能更慢，现有 CI job 已有整体超时兜底。本轮未发现挂死，故未给 `run_gates.py` 统一加短超时（避免把合法的慢构建误杀）。
- 本轮只改 `scripts/` 门禁脚本，**未改工具页、未跑 `_build.py`、未 push**。

