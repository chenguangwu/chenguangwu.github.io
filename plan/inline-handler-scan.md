# 内联事件 → 全局函数扫描（全站）

扫描器：[scripts/scan_inline_handlers.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/scan_inline_handlers.js)
口径：内联事件属性在**全局作用域**求值（隐式 `with(document)`）；定义位于 `type="module"`、IIFE、
块级 `{}`、`DOMContentLoaded` 回调内均**不算全局**。同名函数只要有一处在全局即判正常。

## 总量统计（2026-11-05）

| 指标 | 数值 |
|---|---|
| 扫描页面 | 4916（`tools/**/*.html`） |
| 内联事件属性 | 38476 |
| 候选函数名（含 `window.x` / `ToolBox.x` 带前缀） | 6888 |
| **真缺陷** | **6 页 / 6 个函数（已全部修复，复扫 0）** |
| 可能缺陷 | 4 页 / 6 处（module 内定义 + 同页 `window.X=` 显式导出，运行时可达） |
| 正常 | 其余全部 |
| 解析失败脚本 | 5 个（已用行首声明兜底，宁可多算全局，不误报真缺陷） |

解析失败页（兜底处理后无真缺陷）：`tools/it/typescript-compiler.html`、`tools/it/url-params.html`、
`tools/life/color-name-finder.html`、`tools/math/equation-solver.html`、
`tools/reproductive-medicine/reproductive-hormones.html`。

## 三档表

### 真缺陷（6 页，已修）

| 页面 | 事件属性 | 函数名 | 定义位置（修前） | 档位 | 处理 |
|---|---|---|---|---|---|
| tools/astronomy/hubble-redshift-distance.html | oninput | `__charDistUpdate` | 页面内 IIFE（`(function(){ var REFS … })()`） | 真缺陷 | 删除重复 IIFE，改引 `/js/tools/char-distance-ref.js`（共享实现已 `window.__charDistUpdate = …`） |
| tools/legal/calc-16.html | onclick | `__c16Export` | 经典脚本顶层 `function c16Export()`（无 `__` 前缀） | 真缺陷 | 追加 `window.__c16Export = c16Export;` |
| tools/legal/calc-17.html | onclick | `__c17Export` | 经典脚本顶层 `function c17Export()` | 真缺陷 | 追加 `window.__c17Export = c17Export;` |
| tools/legal/calc-96.html | onclick | `__c96Export` | 经典脚本顶层 `function c96Export()` | 真缺陷 | 追加 `window.__c96Export = c96Export;` |
| tools/legal/calculator-calc-6.html | onclick | `__cc6Export` | 经典脚本顶层 `function cc6Export()` | 真缺陷 | 追加 `window.__cc6Export = cc6Export;` |
| tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html | onclick | `__jyExport` | 经典脚本顶层 `function jyExport()` | 真缺陷 | 追加 `window.__jyExport = jyExport;` |

共性根因：内联 `onclick="__xExport()"` 写的是带双下划线的别名，实现函数名没有该前缀（或实现被
IIFE 包住），内联属性只能看见全局，点击即抛 `__xExport is not defined`。

### 可能缺陷（4 页，判定为可接受）

| 页面 | 事件属性 | 函数名 | 定义位置 | 档位 |
|---|---|---|---|---|
| tools/ai/ocr.html | onclick | `copyResult` | module 内 `window.copyResult = function(){}`（约 L304） | 可能缺陷（有显式全局导出） |
| tools/ai/sentiment-analysis.html | onclick | `copyResult` | module 内 `window.copyResult`（约 L286） | 可能缺陷（同上） |
| tools/ai/sentiment-analysis.html | onclick | `__sxExport` | module 内 `window.__sxExport=function(){…}`（约 L350） | 可能缺陷（同上） |
| tools/ai/speech-to-text.html | onclick | `copyResult` | module 内 `window.copyResult`（约 L289） | 可能缺陷（同上） |
| tools/ai/text-summarization.html | onclick | `copyResult` | module 内 `window.copyResult`（约 L291） | 可能缺陷（同上） |
| tools/ai/text-summarization.html | onclick | `__tsExport` | module 内 `window.__tsExport=function(){…}`（约 L341） | 可能缺陷（同上） |

这 6 处实现虽在 `type="module"` 内，但同文件已有 `window.X =` 显式挂载，module 执行后内联属性可解析；
headless 实测 4 页 `typeof window.X === "function"`、点击无报错，故不修（符合「定义在 module 但页面
同文件已 `window.X=` 导出」的判定）。

### 正常（其余 4906 页）

经典 `<script>` 顶层 `function X()` / `var|let|const X` / 隐式 `X = function`、任意作用域
`window.X =`、外部经典 JS 顶层声明、浏览器内建（`window.print`、`alert` 等白名单）均判正常。
带前缀调用（`ToolBox.toggleToolTheme()` / `document.…`）按根对象归属独立归类，根对象为宿主对象时跳过。

## onclick 语义核对

| 检查项 | 结果 |
|---|---|
| `return false` 用法 | 0 处（无「靠 `return false` 阻止默认行为」的写法，不存在失效风险） |
| 传 `event` 入参 | 162 处 / 121 页；逐条比对函数签名，均为 `function f(e)` / `function f(ev)` / `function f(event)` 或直接 `if(event.key…)`，无「把 event 传给期望其他参数函数」的错位 |
| `this` 用法 | 1521 处，均为内联事件标准语义（指向元素本身） |
| 空处理器 / 裸表达式 | 0 处 |
| `<form>` 内按钮缺 `type` | 0 处（3 个含 `<form>` 的页面里按钮均在表单外，不会误触发提交） |

## 回归用例

新增 [scripts/verify_inline_handlers.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/verify_inline_handlers.js)，
并接入 [scripts/run_gates.py](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/run_gates.py) 的
`inline handler global` 门禁：

1. **六个已修页真触发内联事件**（hubble 输入 `#__charDistVal`、其余五页点击导出按钮）→ 不抛
   `is not defined`，且 `window.__x` 为 `function`。jsdom 不加载外链，故 hubble 用例内联注入共享脚本、
   并给 `ToolBox` 打桩（`setResult` / `toggleToolTheme`）。
2. **全站静态断言**：所有 `__` 前缀内联处理函数必须在页面内可见（`window.X =` / 顶层 `function X(`），
   共享脚本 `char-distance-ref.js` 单独放行——防止「写别名不挂全局」再次复发。

当前：`==== inline handler global 2/2 ====`。
