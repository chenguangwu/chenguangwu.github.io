# 全站真实浏览器运行时错误扫描

- 扫描时间：2026/11/5 03:28:01
- 覆盖页数：**4912**
- 有运行时错误的页数：**1923**
- 错误类型聚合条数：**1**
- 导航超时/崩溃页：**4912**
- 填充输入后点击：**0** 页（fill 阶段）

> 口径：console error（已剔除资源 404 / net::ERR 等环境噪音）+ 未捕获 pageerror（含首个堆栈帧）；`requestfailed` 仅记录不算缺陷。触发方式：load=页面加载、click=默认值直接点主按钮、fill=填充空输入后点主按钮。点击后结果区无变化**只作线索**（页面可能在 load 时已自动执行同名初始化）。

## 按影响页数降序

| # | 页数 | 触发 | 错误文本 | 代表页面 |
|---|---|---|---|---|
| 1 | 1923 | load | `FILL is not defined` | `tools/accessibility/accessible-restroom.html`<br>`tools/accessibility/braille-translator.html`<br>`tools/accessibility/index.html`<br>`tools/accessibility/ramp-slope.html`<br>`tools/accessibility/sign-language.html` |

## 复核结论（2026-11-06 核验）

- **#1 `FILL is not defined`（1923 页）根因不在网站页面，而在审计扫描脚本自身**：`scripts/runtime_scan.js:233` 的 `if (FILL) {` 引用了从未声明的开关变量 `FILL`（配置区 22–61 行的 LIMIT/FILTER/INTERACT 等均未定义 FILL），导致每页扫描 load 阶段执行到该行即抛 `ReferenceError: FILL is not defined`，被扫描器记为「页面运行时错误」，故 1923 页（近半站点）被误判；fill 阶段也因此从未执行（报告「填充输入后点击：0 页」同因）。
- **修复**：在 `scripts/runtime_scan.js` 配置区补 `const FILL = process.env.FILL === '1';`（默认关闭，与既有报告一致；`FILL=1` 环境变量可启用真实使用路径填充扫描）。重跑扫描后该 1923 页误报应消失。
- **结论**：此 1923 页「运行时错误」为**扫描脚本 bug 导致的假阳性**，非网站页面缺陷，无需改工具页源码。

