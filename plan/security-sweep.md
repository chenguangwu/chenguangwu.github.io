# 全站安全复扫清单（只读扫描）

- 扫描日期：2026-11-04
- 扫描范围：`tools/**/*.html` 共 **4916** 个页面
- 扫描方式：静态扫描（ripgrep/Python 逐文件逐行 + 同函数内轻量污点传播启发式），**未**逐页做运行时利用验证；已确认条目均人工阅读源码核对
- 扫描口径：
  - 危险落点：`innerHTML` / `outerHTML` / `insertAdjacentHTML` / `document.write`
  - 动态执行：`eval` / `new Function` / `setTimeout("字符串")` / `new Worker` / `srcdoc` / `allow-same-origin`
  - 敏感持久化：`localStorage.setItem` 键名含 password/secret/token/apikey/credential
  - 站外外传：`fetch` / `XMLHttpRequest` / `sendBeacon` / `WebSocket` / `EventSource` 出现站外绝对 URL
- 命中统计：**高危 11 条 / 10 页**（其中 4 条 3 页为本轮新修，7 条 6 页待修）；**中危 71 条**（系统性属性注入 66 条/53 页 + 其它 5 条）；另有 1795 处启发式候选（1114 页）待复核，不计入中危确认数

> 说明：本次只新增本文件，未改动任何页面以外的仓库文件；修复的 3 页单独提交。

---

## 一、高危（Confirmed，可利用）

| # | 页面 | 行号 | 风险类型 | 是否已修 |
|---|---|---|---|---|
| 1 | `tools/it/json-path.html` | 386（调用）、509（`eval`） | 动态执行：过滤表达式 `eval(filter)`，`?(@.price<10 || alert(1))` 可执行任意 JS | **已修**（改为受限解析：仅 `@.prop`、字面量、比较、`&& \|\| !`、括号） |
| 2 | `tools/it/json-path.html` | 516–525（`highlightJSON`，落点 643/645） | DOM XSS：JSON 字符串值未 HTML 转义即拼 `innerHTML`，`<img onerror>` 触发 | **已修**（先转义 `& < >` 再做语法高亮） |
| 3 | `tools/it/charset-detector.html` | 259–263（`#out` 落点 263） | DOM XSS：textarea 原文（修复输出）直接拼 `innerHTML`，页面一载入即执行 | **已修**（`extra`/`fixed` 均转义后拼装） |
| 4 | `tools/sports/stats-11.html` | 245、246、250（`#res` 落点 254） | DOM XSS：姓名从「姓名,成绩」文本解析后未转义拼 `<td>` | **已修**（新增 `escHtml()` 覆盖表格/排名/摘要三处） |
| 5 | `tools/math/equation-solver.html` | 433 | 动态执行：`eval(expr)` 直接求值用户多项式，且被迭代调用 | 待修 |
| 6 | `tools/math/function-plotter.html` | 291 | 动态执行：`new Function('x','with(Math){return ('+expr+')}')` 用户函数表达式 | 待修 |
| 7 | `tools/math/calculus-tools.html` | 357 | 动态执行：`new Function('x','return '+replaced)` 用户函数 | 待修 |
| 8 | `tools/science/calculator.html` | 409 | 动态执行：`new Function('_d2r','return '+expr)` 用户表达式 | 待修 |
| 9 | `tools/clinical-lab/tumor-marker-doubling.html` | 291 | DOM XSS：非法输入的 `daysRaw` 原文拼进错误提示 `innerHTML` | 待修 |
| 10 | `tools/edu/exam-gpa-calculator.html` | 389–394（`${c.name}` 在 392） | DOM XSS：课程名未转义拼课程列表 `innerHTML` | 待修 |

补充（同页 / 同因但未单列）：

- `tools/it/json-path.html` 386 行是过滤入口，509 行是执行点，两处同一漏洞，已一并处理。
- 上述待修 6 页为同一模式（用户表达式/文本 → 执行或拼接），修复方式与前 4 条一致：表达式改受限解析或白名单化，文本改 `textContent` / 转义。

---

## 二、中危

### 2.1 系统性问题：`ToolBox.escHtml` 不转义引号，却被用于 HTML 属性上下文（66 处 / 53 页）

`js/common.js` 的 `escHtml` 走 `textContent → innerHTML`，只转义 `& < >`，**不转义 `"` / `'`**；凡用于 `value="..."`、`placeholder="..."` 等属性拼接处，输入含 `"` 即造成属性逃逸（可注入 `onfocus`/`autofocus` 等）。

| 页面 | 行号 | 风险类型 | 是否已修 |
|---|---|---|---|
| `tools/advertising/storyboard-timeline.html` | 294、303、306、307 | 属性注入（`value=` + escHtml） | 待修 |
| `tools/pr/press-conference.html` | 324、328、329 | 属性注入 | 待修 |
| `tools/museum/visitor-route.html` | 274、275、308 | 属性注入 | 待修 |
| `tools/marketing/utm-builder.html` | 490、491、492 | 属性注入 | 待修 |
| `tools/it/url-encode.html` | 604、605 | 属性注入（参数键值回填输入框） | 待修 |
| `tools/edu2/wrong-book.html` | 318、323 | 属性注入 | 待修 |
| `tools/life/bill-splitter.html` | 384、490 | 属性注入 | 待修 |
| `tools/hr/performance-score.html` | 267、280 | 属性注入 | 待修 |
| `tools/edu/grade-calculator.html` | 401 | 属性注入 | 待修 |
| `tools/edu/grade-weight-calculator.html` | 237 | 属性注入 | 待修 |
| `tools/edu/gpa-calculator.html` | 463 | 属性注入 | 待修 |
| `tools/restaurant/dish-cost-card.html` | 250 | 属性注入 | 待修 |
| 其余 41 页（共 66 处，分布见下） | — | 属性注入 | 待修 |

其余 41 页：`advertising/`、`pr/`、`marketing/`、`museum/`、`edu/edu2/`、`it/`、`life/`、`hr/`、`restaurant/`、`health/` 等目录下的表单回填页，均属同一根因；建议统一修复 `js/common.js` 的 `escHtml`（补 `"` `'` 转义）后一次性收敛（该文件不在本批改动范围）。

### 2.2 其它中危

| 页面 | 行号 | 风险类型 | 是否已修 |
|---|---|---|---|
| `tools/it/js-formatter.html` | 465 | `new Function(src)`：仅编译不执行（无即时 RCE，但语法校验依赖动态编译） | 待修（建议改静态语法校验或加标识符/字符限制） |
| `tools/aerospace/weight-balance.html` | 274–276、297 | escHtml 用于 `value="..."`（同 2.1 根因；当前仅静态默认值回填，暂未构成可达利用） | 待修（随 2.1） |
| `tools/it/regex.html` | 约 520 | `new Worker(blobURL)`，worker 源码为页面内静态字符串，不含用户输入 | 无需修（已确认非可控） |
| `tools/ophthalmology/astigmatism-chart.html` | 约 715 | `document.write` 弹窗，参数已 `esc()` | 无需修（已转义） |
| `tools/ophthalmology/amsler-grid.html` | 约 706 | 同上 | 无需修（已转义） |
| `tools/legal/will-template-generator.html` | 313 | `insertAdjacentHTML`，用户值经 `escapeAttr`（引号已转义，`&` 未转义） | 低风险（可加 `&` 转义） |

---

## 三、已修批次（本轮之前 8 页，复扫复核确认无回归）

| 页面 | 原注入点 | 是否已修 |
|---|---|---|
| `tools/it/api-sign-generator.html` | 待签名串/签名结果拼 `innerHTML` | 已修（`escHtml` 转义） |
| `tools/it/url-params.html` | `esc()` 未转义引号 → `value="..."` 属性注入 | 已修（补引号转义） |
| `tools/it/math-evaluator.html` | 任意标识符 + `new Function`（原 291–320） | 已修（标识符白名单 + 拒绝成员访问；121 行仅为文档中的安全提示文本） |
| `tools/fun/random-picker.html` | 选项与历史记录拼 `innerHTML` | 已修（`textContent`） |
| `tools/biz/presentation-timer.html` | 历史主题/日期拼 `innerHTML` | 已修（`escHtml`） |
| `tools/metalwork/analysis-35.html` | 试模名称拼结果表 | 已修（`escHtml`） |
| `tools/sports/analysis-19.html` | 回合号拼结果表 | 已修（`escHtml`） |
| `tools/biz/barcode-generator.html` | 条码内容/错误提示拼 `innerHTML` | 已修（`textContent` + DOM） |

复扫复核结果：8 页均未再命中「未转义即拼 HTML」的可达路径；`url-params:356` 的 `insertAdjacentHTML` 仅替换空占位符（`{k}`/`{v}` → 空串），无可控内容。

---

## 四、动态执行与站外外传（全站结论）

- `eval`：7 处（json-path 的已修 1 处；math-evaluator 121 行为文档文本；equation-solver 1 处待修；其余为示例代码/正则匹配误报）
- `new Function`：5 处（math-evaluator（已白名单化）、science/calculator、calculus-tools、function-plotter、js-formatter）
- `setTimeout/setInterval("字符串")`：0 处
- `new Worker`：1 处（regex.html，静态源码）
- `srcdoc`：2 处（code-runner.html，已由另一条线移除 `allow-same-origin`，沙箱隔离）
- `allow-same-origin`：1 处，为 code-runner.html 的说明注释，非实际属性（已修）
- **明文存敏感信息**：`localStorage.setItem` 键名命中 password/secret/token/apikey/credential：**0 处**
- **站外数据外传**：`fetch`/`XHR`/`sendBeacon`/`WebSocket`/`EventSource` 指向站外域名：**0 处**
  - 另有 11 处 `<script src="https://...">` 第三方 CDN 依赖（如 TypeScript 编译器），属静态资源加载，非用户数据外传，单列为低风险

---

## 五、待复核（启发式候选）

按「`innerHTML` 赋值右侧出现由 `.value` / `localStorage` / URL 参数 / 剪贴板 / 文件读取赋值的变量」做轻量污点传播，得到 **1795 处候选（1114 页）**。抽样复核显示多数为数值结果模板（变量先经 `parseFloat`/`toFixed`）或已转义，但也发现若干真实可疑页（已并入上表）。候选密度最高的页面供后续复核优先参考：

| 页面 | 候选条数 |
|---|---|
| `tools/cognition/human-benchmark.html` | 20 |
| `tools/design/palette-cvd-checker.html` | 16 |
| `tools/science/probability-calculator.html` | 15 |
| `tools/it/text-similarity.html` | 13 |
| `tools/legal/calc-17.html` | 12 |
| `tools/energy/energy-calculator.html` | 8 |
| `tools/science/astro-geo-calculator.html` | 8 |
| `tools/medical/medical-calculator.html` | 7 |
| `tools/data/calc-2.html` | 7 |
| `tools/health/premature-age-calculator.html` | 6 |

> 复核方法建议：对上述页面逐一注入 `<svg/onload=alert(1)>`（无空格载荷，避免被分隔符切分），观察是否出现弹窗或注入元素。

---

## 六、扫描限制

- 纯静态启发式，未做全站运行时插桩；`innerHTML` 间接赋值（先拼变量再赋值）可能漏检。
- 未覆盖 `js/**/*.js` 公共库与 `zh-tw/` 构建产物；`i18n/**` 字典为静态文案，未纳入。
- 行号以当前工作区源码为准，页面后续被其他线改动时需重新定位。
