# 全站安全复扫清单（只读扫描）

- 扫描日期：2026-11-04
- 扫描范围：`tools/**/*.html` 共 **4916** 个页面
- 扫描方式：静态扫描（ripgrep/Python 逐文件逐行 + 同函数内轻量污点传播启发式），**未**逐页做运行时利用验证；已确认条目均人工阅读源码核对
- 扫描口径：
  - 危险落点：`innerHTML` / `outerHTML` / `insertAdjacentHTML` / `document.write`
  - 动态执行：`eval` / `new Function` / `setTimeout("字符串")` / `new Worker` / `srcdoc` / `allow-same-origin`
  - 敏感持久化：`localStorage.setItem` 键名含 password/secret/token/apikey/credential
  - 站外外传：`fetch` / `XMLHttpRequest` / `sendBeacon` / `WebSocket` / `EventSource` 出现站外绝对 URL
- 命中统计：**高危 13 条 / 12 页**（12 条已修、1 条转交；含候选复核新增的 jwt-parser 与审计线新增 2 页）；**中危 71 条**（系统性属性注入 66 条/53 页已随根因修复 + 其它 5 条已处理/确认无需修）；1795 处启发式候选已完成三档复核（见 2.4）

> 说明：本文件随修复批次持续更新状态；修复提交不 push、不跑 `_build.py`，只 add 具体路径。
>
> 校正：`tools/edu/exam-gpa-calculator.html` **不存在 `eval(` / `new Function`**，此前「eval」为模板字符串插值的误报；该页真实风险是 `c.name` 未转义拼 `innerHTML`，已由运行时扫描线修复。
>
> 回归护栏：`scripts/verify_esc_html.js`（锁定 `escHtml` 五类字符编码、禁止回退 `textContent→innerHTML`、抽查 3 个真实调用页），运行 `node scripts/verify_esc_html.js` 通过；**需集成线将该脚本注册进 `run_gates.py` / CI 门禁**（本批只提供脚本与说明）。
>
> 第三批（传输面与隐私：SRI / `target=_blank` / `postMessage` / 上传回显 / 敏感存储）见 **第七节**（2026-11-04）。

---

## 一、高危（Confirmed，可利用）

| # | 页面 | 行号 | 风险类型 | 是否已修 |
|---|---|---|---|---|
| 1 | `tools/it/json-path.html` | 386（调用）、509（`eval`） | 动态执行：过滤表达式 `eval(filter)`，`?(@.price<10 || alert(1))` 可执行任意 JS | **已修**（改为受限解析：仅 `@.prop`、字面量、比较、`&& \|\| !`、括号） |
| 2 | `tools/it/json-path.html` | 516–525（`highlightJSON`，落点 643/645） | DOM XSS：JSON 字符串值未 HTML 转义即拼 `innerHTML`，`<img onerror>` 触发 | **已修**（先转义 `& < >` 再做语法高亮） |
| 3 | `tools/it/charset-detector.html` | 259–263（`#out` 落点 263） | DOM XSS：textarea 原文（修复输出）直接拼 `innerHTML`，页面一载入即执行 | **已修**（`extra`/`fixed` 均转义后拼装） |
| 4 | `tools/sports/stats-11.html` | 245、246、250（`#res` 落点 254） | DOM XSS：姓名从「姓名,成绩」文本解析后未转义拼 `<td>` | **已修**（新增 `escHtml()` 覆盖表格/排名/摘要三处） |
| 5 | `tools/math/equation-solver.html` | 433 | 动态执行：`eval(expr)` 直接求值用户多项式，且被迭代调用 | **已修**（移除 `eval`，改受限递归下降解析；表达式回显改 `ToolBox.escHtml`） |
| 6 | `tools/math/function-plotter.html` | 291 | 动态执行：`new Function('x','with(Math){return ('+expr+')}')` 用户函数表达式 | **已修**（移除 `new Function`，改白名单递归下降，拒绝成员访问/未知标识符） |
| 7 | `tools/math/calculus-tools.html` | 357 | 动态执行：`new Function('x','return '+replaced)` 用户函数 | **已修**（同上，按表达式缓存编译结果） |
| 8 | `tools/science/calculator.html` | 409 | 动态执行：`new Function('_d2r','return '+expr)` 用户表达式 | **已修**（同上，保留角度/弧度三角函数与 `log`/`ln` 语义） |
| 9 | `tools/clinical-lab/tumor-marker-doubling.html` | 291 | DOM XSS：非法输入的 `daysRaw` 原文拼进错误提示 `innerHTML` | **已修**（`ToolBox.escHtml(daysRaw)`） |
| 10 | `tools/edu/exam-gpa-calculator.html` | 389–394（`${c.name}` 在 392） | DOM XSS：课程名未转义拼课程列表 `innerHTML` | 转交另一条线（该页 `.scale-btn` 崩溃修复中，按约定避让；无 `eval`/`new Function`） |
| 11 | `tools/it/jwt-parser.html` | 390、393 | DOM XSS：`headerEl.textContent`（含 JWT payload 原文）二次拼回 `innerHTML` | **已修**（改 DOM：`createElement` + `textContent` + `createTextNode`） |
| 12 | `tools/automotive/driver-license-validator.html` | 265 | DOM XSS：用户输入 `raw` 直拼结果 `innerHTML`（反射型） | **已修**（`ToolBox.escHtml(raw)`，校验逻辑与匹配结果不变） |
| 13 | `tools/science/chemistry-calculator.html` | 588、596、822 | DOM XSS：分子式与历史记录（`h.type` / `resStr` / `h.time`）未转义拼 `innerHTML` | **已修**（三处均 `ToolBox.escHtml`；由安全线接手，集成线已跳过该页） |

补充（同页 / 同因但未单列）：

- `tools/it/json-path.html` 386 行是过滤入口，509 行是执行点，两处同一漏洞，已一并处理。
- 上述 5 页（表达式动态执行 4 页 + 文本拼接 1 页）已在本轮修复：表达式一律改「运算符 + 函数白名单 + 递归下降」，不再保留 `new Function` 兜底；文本一律转义。`exam-gpa-calculator` 因另一条线正在改该页运行时崩溃，按约定转交。

---

## 二、中危

### 2.1 系统性问题：`ToolBox.escHtml` 不转义引号，却被用于 HTML 属性上下文（66 处 / 53 页）

`js/common.js` 的 `escHtml` 走 `textContent → innerHTML`，只转义 `& < >`，**不转义 `"` / `'`**；凡用于 `value="..."`、`placeholder="..."` 等属性拼接处，输入含 `"` 即造成属性逃逸（可注入 `onfocus`/`autofocus` 等）。

**已修（根因）**：`ToolBox.escHtml` 改为字符串级转义，同时编码 `& < > " '`；已核对全站 1436 处调用无「嵌套 `escHtml(escape(...))`」二次转义模式，53 页属性注入一次性收敛。无头浏览器抽查 4 个属性上下文页面（`url-encode`、`storyboard-timeline`、`visitor-route`、`utm-builder`）注入 `"` + 标签载荷：0 弹窗、0 pageerror、0 新属性/注入元素，正常文本回填不变。

| 页面 | 行号 | 风险类型 | 是否已修 |
|---|---|---|---|
| `tools/advertising/storyboard-timeline.html` | 294、303、306、307 | 属性注入（`value=` + escHtml） | **已修（根因）** |
| `tools/pr/press-conference.html` | 324、328、329 | 属性注入 | **已修（根因）** |
| `tools/museum/visitor-route.html` | 274、275、308 | 属性注入 | **已修（根因）** |
| `tools/marketing/utm-builder.html` | 490、491、492 | 属性注入 | **已修（根因）** |
| `tools/it/url-encode.html` | 604、605 | 属性注入（参数键值回填输入框） | **已修（根因）** |
| `tools/edu2/wrong-book.html` | 318、323 | 属性注入 | **已修（根因）** |
| `tools/life/bill-splitter.html` | 384、490 | 属性注入 | **已修（根因）** |
| `tools/hr/performance-score.html` | 267、280 | 属性注入 | **已修（根因）** |
| `tools/edu/grade-calculator.html` | 401 | 属性注入 | **已修（根因）** |
| `tools/edu/grade-weight-calculator.html` | 237 | 属性注入 | **已修（根因）** |
| `tools/edu/gpa-calculator.html` | 463 | 属性注入 | **已修（根因）** |
| `tools/restaurant/dish-cost-card.html` | 250 | 属性注入 | **已修（根因）** |
| 其余 41 页（共 66 处，分布见下） | — | 属性注入 | **已修（根因）** |

其余 41 页：`advertising/`、`pr/`、`marketing/`、`museum/`、`edu/edu2/`、`it/`、`life/`、`hr/`、`restaurant/`、`health/` 等目录下的表单回填页，均属同一根因；已统一修复 `js/common.js` 的 `escHtml`（补 `"` `'` 转义）后一次性收敛。

### 2.2 其它中危

| 页面 | 行号 | 风险类型 | 是否已修 |
|---|---|---|---|
| `tools/it/js-formatter.html` | 465 | `new Function(src)`：仅编译不执行（无即时 RCE，但语法校验依赖动态编译） | **已修**（移除动态编译，改为括号配对/关键字静态检查，页内说明局限） |
| `tools/aerospace/weight-balance.html` | 274–276、297 | escHtml 用于 `value="..."`（同 2.1 根因；当前仅静态默认值回填，暂未构成可达利用） | **已修（随 2.1 根因）** |
| `tools/it/regex.html` | 约 520 | `new Worker(blobURL)`，worker 源码为页面内静态字符串，不含用户输入 | 无需修（已确认非可控） |
| `tools/ophthalmology/astigmatism-chart.html` | 约 715 | `document.write` 弹窗，参数已 `esc()` | 无需修（已转义） |
| `tools/ophthalmology/amsler-grid.html` | 约 706 | 同上 | 无需修（已转义） |
| `tools/legal/will-template-generator.html` | 313 | `insertAdjacentHTML`，用户值经 `escapeAttr`（引号已转义，`&` 未转义） | **已修**（`escapeAttr` 补 `&` 转义；真机校验 `a&b"c<d>` → `a&amp;b&quot;c&lt;d&gt;`） |

### 2.3 iframe 沙箱 / outerHTML / document.domain（全站 grep）

- `allow-same-origin`：**0 处遗留**。唯一沙箱 iframe（`tools/it/code-runner.html:494`）为 `sandbox="allow-scripts allow-modals"`，未给 `allow-same-origin`，与「同时给 allow-scripts + allow-same-origin 必须去除后者」的规则一致。
- `outerHTML =`：仅 `tools/edu/exam-gpa-calculator.html` 1 处，已由运行时扫描线在本轮修复。
- `document.domain`：0 处。

### 2.4 1795 处启发式候选三档复核

复跑「表达式/变量拼 sink」启发式并对字符串字面量做剥离（避免把 HTML 里的 `class="value"` 误当用户输入）：

- 全站 sink 命中 21549 处（行级/表达式级，含同一语句多模式重复计数）；历史记录的 1795 为去重后的行级候选，两者统计粒度不同。
- **A 档（确认高危）**：4 处命中，逐条人工复核后确认 **1 页 2 行真高危**：
  - `tools/it/jwt-parser.html:390/393` —— 先把 JWT payload 写入 `textContent`，再把 `headerEl.textContent` 拼回 `innerHTML`；payload 内的 `<img onerror>` 会被二次解析执行。**已修**：改为 `createElement('span')` + `textContent` + `createTextNode`，真机注入 JWT（payload 含 `<img src=x onerror=…>`）0 弹窗/0 pageerror/0 注入元素。
  - 其余 2 处为误报：`science/physics-calculator.html:781`（静态常量表 `c.value`）、`sports/climbing-grade-converter.html:346`（静态选项数组 `o.value`），均无用户输入来源。
- **B 档（需上下文判断）**：8 处 / 5 页，均已确认不构成可达注入：
  - `it/code-runner.html`（`postMessage(..., "*")` ×2 + `srcdoc` ×2）：iframe 为不透明源沙箱，跨源消息只含 console 输出，属工具设计；`srcdoc` 内容即用户主动运行的代码。
  - `it/regex.html`（`postMessage` ×2）：消息只在页面与其自建 Blob Worker 之间传递，无跨源窗口。
  - `ophthalmology/astigmatism-chart.html`、`amsler-grid-test.html`（`document.write` ×2）：打印弹窗参数经 `esc()` 转义，快照 URL 来自 canvas。
- **C 档（误报）**：其余约 21537 处，统一理由为：静态模板/常量表、已 `escHtml`/`escape`/`encodeURIComponent` 转义、`parseFloat`/`toFixed`/`Math` 数值化、或 `textContent` 赋值（非 HTML sink）。

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

- `eval`：可控执行已全部移除（json-path、equation-solver 各 1 处已修；math-evaluator 121 行为文档文本；其余为示例代码/正则匹配误报）
- `new Function`：可控执行已移除 5 处（math-evaluator 白名单化；science/calculator、calculus-tools、function-plotter 改受限解析；js-formatter 改静态检查）
- `setTimeout/setInterval("字符串")`：0 处
- `new Worker`：1 处（regex.html，静态源码）
- `srcdoc`：2 处（code-runner.html，已由另一条线移除 `allow-same-origin`，沙箱隔离）
- `allow-same-origin`：0 处（code-runner.html 已由运行时扫描线移除该属性）
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

---

## 七、第三批：传输面与隐私（2026-11-04）

扫描口径：`tools/**/*.html` 4916 页（不含 `zh-tw/` 构建产物），按 5 类问题静态扫描 + 本地无头浏览器复验。

### 7.1 外部 CDN 脚本 SRI

- 非本站 `<script src="https://…">` 共 15 处 / 13 页；外部 `<link rel=stylesheet>` 仅 `it/html-tags.html` 教学示例（example.com，非真实引用）与 `design/font-pairing.html` 动态 Google Fonts。
- **已补 `integrity` + `crossorigin="anonymous"` 8 处 / 6 页**（固定版本，哈希取自实际下载文件并二次拉取校验一致）：
  - `office/pdf-merge.html`、`office/pdf-split.html`、`office/pdf-rotate.html` —— pdf-lib 1.17.1 / pdf.js 3.11.174
  - `it/bcrypt.html` —— bcryptjs 2.4.3
  - `it/sqlite-runner.html` —— sql.js 1.8.0
  - `it/typescript-compiler.html` —— TypeScript 5.3.3
- **无法提供 SRI 7 处**（浮动版本号，内容哈希不稳定，按约定不瞎编）：`mermaid@10`、`d3@7`、`markmap-view`（无版本）、`markmap-lib@0.17`、`js-yaml@4`、`less@4`、`acorn@8`。
- 动态加载类同样无法 SRI：`js/ai-core.js` 的 transformers（运行时拼版本 + 远端模型分片）、`font-pairing` 的 Google Fonts CSS（按 UA 下发）、全站构建注入的 TTZZ 统计脚本（URL 带服务端 token）。
- 顺带修复：`it/bcrypt.html` 原代码直接用 `bcrypt` 全局，而 bcryptjs 2.4.3 只暴露 `dcodeIO.bcrypt`（页面此前点击即报 `bcrypt is not defined`）；补一行带守卫的别名脚本，真机 `hashSync` 实测可用。
- 真机复验：6 页外链脚本全部加载成功，0 pageerror、0 CDN 请求失败。

### 7.2 `target="_blank"` 缺 `rel`

- `tools/` 共 8 处，其中 6 处已带 `rel`；**补 `rel="noopener noreferrer"` 2 处**：`biz/markdown.html`（渲染链接模板）、`it/mac-lookup.html`（IEEE OUI 外链）。
- 剩余 2 处为 `it/html-tags.html` 的 `<base>` / `<a>` 属性教学示例，非真实链接，不改。
- `ui/tool-editor.html`（内部编辑页）同步补 `rel`。

### 7.3 `postMessage` 校验

- 全站 `addEventListener('message')` 仅 `it/code-runner.html` 1 处：消息源为 `sandbox="allow-scripts allow-modals"`、无 `allow-same-origin` 的隔离 iframe，且只接受 `type === 'console'`、输出经 `escapeConsoleHtml`；**已知安全，不处理**。
- `it/regex.html` 的 `postMessage` 仅用于页面与自建同源 Worker 通信，无跨源消息面；**已知安全，不处理**。

### 7.4 文件上传回显

- `input[type=file]` 共 55 页，逐页检查文件名 / 文件内容是否拼 HTML 或 `document.write`。**真 XSS 4 页已修**：
  - `it/md5.html`、`it/sha.html`：`file.name` 直拼 `#fileInfo` 的 `innerHTML` → 改 `ToolBox.escHtml(file.name)`。
  - `image/image-converter.html`：`file.name` / `file.type` 直拼 `#info` → 改 `ToolBox.escHtml`。
  - `biz/markdown.html`：导入 `.md` 后原文直渲染（`<img onerror>` 可执行），链接 / 图片 `href`、`src`、`alt` 存在属性注入与 `javascript:` 协议 → 先整体转义 HTML，链接改为协议白名单（http(s) / mailto / 相对 / 锚点），`href`/`src`/`alt` 属性转义，图片仅额外放行 `data:image`；渲染回归（标题 / 粗斜体 / 引用 / 列表 / 表格 / 代码块）全部通过。
- 其余上传页均为 `textContent`、已转义、或文件名仅用于下载，无需修改。

### 7.5 敏感存储

- localStorage / sessionStorage 键名含 password / token / secret / key / auth 的 3 页逐个核查：
  - `safety/manager.html`：`tb_pwd_master`（口令派生哈希）+ `tb_pwd_vault`（XOR 密文），非明文；键名与实际内容一致，不改名（改名会使既有用户保险库失联）。
  - `security/virtual-safe.html`：仅存口令哈希，页内有「勿存真实口令、仅教学演示」显著警示。
  - `it/password-generator.html`：生成历史存 `sessionStorage`（`password_generator_session_history`），随标签页关闭清除，UI 明示「本次会话记录」。
- 结论：**0 处明文口令/令牌**；键名无误导，无需改中性名。

### 7.6 门禁与验证

- `verify_office_calc.js` 3/3、`verify_image_calc.js` 23/23、`verify_it_calc.js` 852/852、`verify_biz_calc.js` 144/144。
- `discriminate_check.js` 对应四类：逃生项 0（office 检 2 跳 1、image 检 22 跳 1、it 检 851 跳 1、biz 检 144 跳 0）。
- `selfcheck_false_pass.js` 四类 risk 0（no_inputs=0 / all_default=0）。
- `python3 _test_static.py` exit 0（仅 1 条既有 slug-en 冗余告警，与本次无关）。
- 真机载荷复验：md5 / sha / image-converter 注入 `x"><img src=x onerror=alert(1)>.png` → 0 弹窗、0 pageerror、0 注入元素；markdown 注入原始 `<img onerror>` 与属性逃逸链接 → 0 弹窗、0 事件属性、`javascript:` 不生成链接。

---

## 八、第四批：审计线 Z 批 XSS 收口（2026-11-04）

审计线 Z 批报 4 处 DOM/存储型 XSS，本线负责其中 3 处（`fun/raffle-picker.html` 已由设计与生活线修复）。

### 8.1 修复清单（3 页）

- `automotive/countdown-engine-oil.html`（**存储型自 XSS**）：`renderGarage()` 把 `r.car` 直拼 `<td>`，删除按钮又把车名直拼进 `onclick` 的 JS 字符串；车名来自 `localStorage`（`toolbox_auto_oil_countdown`），被污染的记录在**打开页面即触发**。
  - 新增页内 `escXss()`（`& < > " '` 五字符转义）用于车名列。
  - 删除按钮改为索引参数 `delCarAt(i)`：渲染前按 `kmLeftOf` 排序后按位删除，彻底移除 `onclick` 里的车名插值（HTML 转义无法阻止 JS 字符串上下文逃逸）。
- `metalwork/analysis-36.html`：缺陷类型名拼明细表 `<td>` 与「数量最多 / 加权最高缺陷」两处 `<strong>` → 全部 `escXss()`。
- `metalwork/analysis-cost-price-5.html`：期次名拼表格首列 → `escXss()`。

### 8.2 真机复验

- `countdown-engine-oil`：先写入 `[{car:'<svg/onload=alert(1)>', …}]` 到 localStorage 再**刷新页面**（验证存储型路径）→ 0 弹窗 / 0 pageerror / 车库表内 0 个 `<svg>` 元素 / 任何属性值不含 `alert(1)` / HTML 为 `&lt;svg/onload=alert(1)&gt;` / 单元格文本为原样纯文本；`delCarAt(0)` 删除后 localStorage 记录归零、表格回到空态。
- `analysis-36`：`data` 注入 `<svg/onload=alert(1)>,45,2` 后点「统计缺陷」→ 0 弹窗 / 0 pageerror / 0 `<svg>` / 0 属性命中 / 输出为转义文本。
- `analysis-cost-price-5`：`data` 注入 `<svg/onload=alert(1)>,52000` 后点「价格分析」→ 同上全部通过。

### 8.3 防回退

- `scripts/verify_automotive_calc.js` 新增存储型用例：`clicks` 覆写 `localStorage.getItem` 返回恶意记录后调 `renderGarage()`，`expect` 命中 `&lt;svg/onload=alert(1)&gt;`。
- `scripts/verify_metalwork_calc.js` 为两页各新增一条恶意名称用例（`expect` 同上）。
- `verify_automotive_calc.js` 73/73、`verify_metalwork_calc.js` 71/71 全过；`discriminate_check.js` 两脚本合计 144 例、逃生项 0；`selfcheck_false_pass.js` 两脚本 risk 0；`_test_static.py` 0 失败。

---

## 九、第五批：SRI 收敛 / 全局名审计 / 上传抽检 / 外传核查（2026-11-04）

### 9.1 浮动版本 CDN 收敛（7/7）

- 7 处浮动版本全部固定到同 major 的确切版本，并补 `integrity` + `crossorigin="anonymous"`；哈希按实际下载字节计算并二次拉取核对一致：
  - `office/flowchart.html`：mermaid `@10` → `10.9.8`
  - `office/mindmap.html`：d3 `@7` → `7.9.2`；markmap-view（无版本）→ `0.17.2`；markmap-lib `@0.17` → `0.17.2`
  - `it/yaml-validator.html`：js-yaml `@4` → `4.1.0`
  - `it/less-compiler.html`：less `@4` → `4.9.1`
  - `it/ast-viewer.html`：acorn `@8` → `8.19.0`
- **保留浮动版本清单：0 处**。这 7 处均能确定确切版本并稳定取到哈希，无需保留浮动。仍无法固定/SRI 的只有动态下发类（见 9.4 与第十节）。
- 真机复验：5 页 HTTP 200、库全局可用（`mermaid.render` / `d3` + `window.markmap.Markmap/Transformer` / `jsyaml.loadAll` / `less.render` / `window.acorn.parse`）、0 pageerror、0 CDN 请求失败。

### 9.2 库全局名审计

- 逐页真机检查第三方库实际暴露的全局名与页面调用名是否一致：pdf-lib（`PDFLib`）、pdf.js（`pdfjsLib`）、bcryptjs（`dcodeIO.bcrypt`）、sql.js（`initSqlJs`）、TypeScript（`ts`）、mermaid、d3、markmap、jsyaml、less、acorn，共 11 页。
- **本批新命中 0 处**；上一批已修的 `it/bcrypt.html`（裸 `bcrypt` vs `dcodeIO.bcrypt`）是唯一实际缺陷。11 页真机功能调用全部通过、0 pageerror。

### 9.3 上传回显抽检（10/55）

- 从剩余 51 个上传页抽取 10 页：`speech-to-text`、`audio-volume`、`image-to-ascii`、`png-to-svg`、`image-to-base64`、`base64-converter`、`code-line-counter`、`csv-to-html-table`、`rich-text-editor`、`safety/manager`。
- 真机注入文件名 `x"><img src=x onerror=alert(1)>.png`：**10/10 全部 0 弹窗、0 pageerror、0 属性和值含 `alert(1)` 的注入元素**，`textContent` / 已转义判断成立，无新反例。

### 9.4 第三方脚本外传核查

- 全站注入脚本：TTZZ（字节 push.js）、51.la、微软 Clarity、百度统计、AdSense、淘宝客与社交分享。
- 核查结论：**0 处把用户输入/文件内容写入 URL query、`sendBeacon` 或 `fetch` 请求体**；统计仅上报页面路径/工具标识与常规浏览器指标。唯一待处置项是 Clarity 会话回放可能采集文本输入（见第十节）。

### 9.5 门禁

- `verify_office_calc.js` 3/3、`verify_it_calc.js` 866/866。
- `discriminate_check.js` office 检 2 跳 1、it 检 865 跳 1，**逃生项均为 0**。
- `selfcheck_false_pass.js` office risk 0（all_default=1 为既有基线）、it risk 0。
- `python3 _test_static.py` 0 失败。

---

## 十、剩余风险（按严重度）

| # | 风险项 | 严重度 | 状态 | 说明 |
|---|--------|--------|------|------|
| 1 | 微软 Clarity 会话回放会随 DOM 快照上传页面可见文本 | 高 | **已处置（2026-11-04 移除脚本）** | 实测工具页回显的用户输入（哨兵串）出现在 Clarity 上传的 DOM 快照中，服务端脱敏无法自证；按 AGENTS.md §2 直接移除，详见第十一节。 |
| 2 | GitHub Pages 无 CSP / X-Frame-Options / COOP 等安全响应头 | 中 | **待处置** | 平台不允许自定义响应头；`<meta http-equiv="Content-Security-Policy">` 试点扫描显示 0 个页面可在严格策略下运行（全部含内联脚本/内联事件），详见第十二节。 |
| 3 | TTZZ / 51.la / 百度 / Clarity / AdSense 动态下发脚本无法 SRI | 中 | 接受风险 | URL 带服务端 token、内容随请求变化，无法固定哈希；来源为各厂商官方 CDN。被投毒时与同源脚本同等失效，已通过「不上传用户数据」降低影响面。 |
| 4 | transformers 运行时拼版本 + 远端模型分片 | 中 | 接受风险 | 模型文件体积大、按运行时版本动态分片，无法 SRI；仅在浏览器本地推理，输入不出本机。 |
| 5 | localStorage 弱加密（XOR 密钥流）用于口令保险库 | 中 | 接受风险 | `safety/manager.html` 等页仅作本地演示，页内有显著警示；升级为 WebCrypto 派生需另立工具并迁移既有数据，暂不处理。 |
| 6 | pdf.js worker 运行时动态加载 | 低 | 接受风险 | worker 与主库版本一致、同 CDN 同源，无 SRI；主库已固定 3.11.174 + SRI，worker 仅执行 PDF 解析。 |
| 7 | Google Fonts CSS 动态下发（`design/font-pairing.html`） | 低 | **已确认安全** | 仅按 UA 下发样式表，不含用户数据；请求携带常规 UA 属浏览器行为，无 PII。 |
| 8 | sql.js wasm 运行时加载 | 低 | **已确认安全** | 库固定 1.8.0 + SRI，wasm 路径由该版本决定；SQL 全程本地执行，不上传数据库内容。 |
| 9 | 淘宝客 / AdSense / 社交分享外链 | 低 | **已确认安全** | 推广链接与分享参数均为静态值，不拼接用户输入；分享仅使用页面标题/URL。 |
| 10 | 严格 CSP（`script-src 'self'`）无法落地 | 中 | 接受风险 | 全站 0 个工具页满足「无内联脚本 + 无内联事件」；要落地需构建期为每个内联脚本生成 nonce/hash，并移除全部 `onclick` 等属性，改造面过大，暂接受风险。 |

**合计 10 条**：已确认安全 3 条、接受风险 5 条、待处置 1 条、已处置 1 条。

---

## 十一、Clarity 判定与移除（2026-11-04）

### 11.1 实测证据

- 探针页面：`it/hash.html`、`healthcare/egfr.html`、`finance/salary-after-tax.html`、`legal/will-template-generator.html`。
- 方法：真机无头 Chrome 输入哨兵串 `SENTINEL-7f3a`（数字控件用 `987654321`），同时在页面注入普通可见文本节点 `PLAINSENTINELabc9`；抓取 `*.clarity.ms/collect` 的 POST 体，按 gzip 解压后检索。
- 判定结果：
  - **普通可见文本 `PLAINSENTINELabc9` 原样出现在上传的 DOM 快照中** → Clarity 确实上传页面文本。
  - 表单控件快照中 `value=` 为空、`placeholder=` 显示为圆点，说明 SDK 会对输入框做本地掩码；但工具页把输入回显到普通 DOM（如 `it/hash` 的历史列表 `<span>`）时，回显文本以**明文**进入快照。
  - 哨兵串在 `it/hash.html` 的上传 payload 中被命中；脱敏只可能发生在服务端，客户端无法自证「未留存」。
- 结论：Clarity 与 `AGENTS.md` §2「禁止任何数据上传到服务器」冲突，**默认执行移除**。

### 11.2 处置

- 已从 `js/analytics.js` 移除 Clarity 初始化、`window.clarity` 桩、`tb-clarity-sdk` 加载，以及 `ToolBox.Analytics.track()` 内的 clarity 事件上报。
- 保留基础统计：51.la、百度统计、百度自动推送、TTZZ（仅页面上报，不含用户输入）。
- 清理验证（4 个哨兵页真机）：
  - `clarity.ms` 请求数 **0/0/0/0**；
  - `window.clarity` 全部为 `undefined`，`__tbClarityLoaded` 为 false；
  - 0 pageerror；
  - `#ttzz` 标签存在且 `push.js` 正常 GET；51.la `collect-v6.51.la`、百度 `hm.gif`、`zz.bdstatic.com/push.js` 均正常上报。

### 11.3 待办（阻塞项）

- **`js/analytics.js` 已改，但未运行构建**：SW 版本戳（`sw.js` 的 `const BUILD`）仍是旧值。
- **需集成线执行 `python3 _build.py` 后本次移除才会随 SW 版本更新生效**；在此之前，联网访问会因 `analytics.js` 网络优先策略即时拿到新文件，但离线/弱网回退仍可能命中旧缓存，且在旧 SW 完全失效前存在残留窗口。
- 恢复录屏分析前，必须先实现「客户端可验证的全量 mask」方案（例如 body 级 `data-clarity-mask` + 复测哨兵不出现在 payload），否则不得重新引入。

---

## 十二、CSP 试点结论（2026-11-04）

- 扫描全站 8344 个 HTML：**0 个工具页满足「无内联可执行脚本 + 无内联事件属性」**，因此无法在 `script-src 'self'` 下做无风险试点。
- 根页面中仅 `ByteDanceVerify.html`、`google*.html` 之类无脚本验证文件满足，但属平台验证文件，不适用 CSP。
- 可选方案与代价：
  - 保留 `'unsafe-inline'`：对 XSS 基本无防护价值，不做；
  - 构建期为内联脚本生成 nonce/hash，并把 `onclick` 等内联事件全部改为事件委托：改造面覆盖全站，暂不实施。
- 处置：**接受风险**，不新增 CSP meta；列入第十节第 10 条。后续若做，先从纯静态展示页（`about`/`privacy`/`404`）试点，再逐步推进工具页。

---

## 十三、上传回显与 iframe 全量结论（2026-11-04）

- **上传回显 55/55 全量完成**：对全部含 `input[type=file]` 的 55 个页面真机注入文件名 `x"><img src=x onerror=alert(1)>.png`，统一断言：
  - 0 弹窗、0 pageerror、0 个属性值含 `alert(1)` 的注入元素、0 个 `img[src="x"]`；
  - **55/55 通过，0 反例**。此前已修的 4 页（md5/sha/image-converter 等）也纳入复测。
- **iframe/srcdoc 全量排查**：全站仅 `tools/it/code-runner.html` 有真实 `<iframe>`；其 `sandbox="allow-scripts allow-modals"` **不含 `allow-same-origin`**，`srcdoc` 仅执行用户代码且隔离于父页面。其余页面无 `<iframe>`；`embed.html` 中的 iframe 示例为 HTML 转义展示文本，不构成实际嵌入。

---

## 十四、下一批方向：开头结论（2026-11-04）

1. **可通过 meta 设置的安全头覆盖**：8344 个 HTML 中，4680 个已有 `Referrer-Policy` + `X-Content-Type-Options`，4624 个另有 `Permissions-Policy`；**3664 个缺失**，集中在根页面（`about`/`404`/`search`/`sitemap`/`ui/*`）与各行业 `index.html` 分类页，工具详情页基本全覆盖。下一批可按「先补根页面与分类页」推进，风险低。
2. **`localStorage` 键名与敏感度**：工具页共 75 个唯一键，绝大多数为历史记录/最佳分数/主题/语言等中性名；`safety/manager.html` 的 `tb_pwd_master` / `tb_pwd_vault`（变量名定义，未进上表）是仅有的敏感命名，值为口令哈希与 XOR 密文、非明文。重命名会破坏既有用户数据，需迁移方案，列为后续评估项而非立即修改。
3. **用户输入拼进 `title`/`og:` 的隐蔽外泄**：全站扫描 `document.title = <变量>`、`meta[content]` 动态写入、`og:title` 动态赋值，**命中 0 处**；页面标题与分享 meta 均为静态文案，不存在「输入进 meta 再被分享/抓取」路径。

---

## 十五、第六批：meta 安全头 / localStorage 命名评估 / 下一批方向扫描（2026-11-04）

### 15.1 meta 安全头补齐（3664 → 0 缺失）

- 缺失结构：指南页 3410、行业分类索引 211、根页面 8、`ui/*` 9、零散工具页 26。
- 是否生成的判定：
  - **行业分类 `tools/<ind>/index.html`**：由 `_build.py::generate_category_indexes()` 每次重写 → 已直接改模板（追加三条 meta + `<!-- TOOLBOX-SECURITY -->`）。
  - **指南页**：由 `scripts/gen_guide_pages.py` 等生成 → 已改该模板；其余历史指南生成器由下面这条兜底。
  - **构建末尾新增统一兜底**：`_build.py` 调用 `scripts/security_meta.py::inject()`，对所有 HTML（含根页面、指南、ui、历史遗留页）按「缺则补」注入，幂等。
- 现存文件：用 `python3 scripts/security_meta.py` 一次性注入，重复执行结果一致；再次 `--check` 为 **missing=0**。
- 覆盖口径与既有 4680 页一致：`Referrer-Policy` + `X-Content-Type-Options` + `Permissions-Policy`。
- 门禁：`_test_static.py` exit 0；`_audit_assets.py --check` exit 0（0 缺 `<html lang>` / 0 重复 id）。
- **待办（需集成线构建）**：`zh-tw/` 繁体产物与 SW 版本戳需 `python3 _build.py` 后刷新；本次未跑构建。另有 4 个分类索引页（hr / nephrology / rehabilitation / sports）同时含其他线未提交改动，未纳入本批路径提交，构建后由模板自动覆盖。

### 15.2 localStorage 敏感键改名评估（结论：不改名）

对象：`tools/safety/manager.html` 的 `tb_pwd_master`（主口令校验哈希）与 `tb_pwd_vault`（条目密文）。

- **多标签页迁移竞态**：一次性「读旧键 → 写新键 → 删旧键」在 A/B 两个标签页同时打开时，B 可能仍以旧键为数据源写回，造成新键被旧数据覆盖或迁移后新写入丢失；本项目无跨标签锁机制，风险真实存在。
- **只读兼容**：若保留旧键只读，则「删除旧键」目标无法达成，等于长期双键并存，复杂度上升而无收益。
- **安全收益**：键名可被任意同源脚本/开发者工具枚举，改名不改变值的可读性；真正敏感的是值（当前为哈希与 XOR 密文），键名本身不泄露内容。
- **结论**：**不改名**。改名收益接近于 0，却引入用户数据丢失与迁移失败风险。当前值非明文；后续若升级加密方案，应连同值格式做一次性迁移，而不是仅重命名键。

### 15.3 下一批方向扫描结果

1. **`postMessage`**：命中 3 页。
   - `it/code-runner.html`：iframe → 父页使用 `targetOrigin="*"`，父页监听未校验 `event.source`；但只接受 `type:"console"` 并把 `data` 经 `escapeConsoleHtml` 转义后写入 `innerHTML`，`method` 仅拼进 class 名，无脚本执行路径 → **接受风险**（`*` 为 srcdoc 不透明源的必需写法）。
   - `it/regex.html`、`it/text-replace.html`：同源 Worker 的 `postMessage`，无跨窗口面 → **已确认安全**。
2. **`eval` / `new Function` / 字符串定时器**：仅 `it/math-evaluator.html` 仍运行时使用 `new Function`，但入口已做字符白名单 + 标识符白名单（仅数学函数/常量）+ 拒绝成员访问，`Math`、`constructor`、`this`、`arguments` 等均被拒 → **已确认安全**；`ai-code-review.html` 中的 `eval` 仅为检测规则与示例字符串，不执行。无 `setTimeout('string')` 命中。
3. **`document.write` / `innerHTML +=` 残余**：`document.write` 仅 2 页（`ophthalmology/amsler-grid-test.html`、`astigmatism-chart.html`）向新窗口打印报告，备注字段经 `esc()` 转义 → 安全。`innerHTML +=` 多为数值/静态常量拼接；抽查 `it/whitespace`（`escH`）、`medical2/surgery-duration`（`PROCEDURES` 常量）、`clinical-lab/blood-routine-reference`（`DATA` 常量）均无用户输入未转义路径，本批 **0 新命中**。
4. **CDN 版本锁定复核**：静态 HTML 内共 15 个 jsdelivr/unpkg/cdnjs 标签，**15/15 固定到确切版本、15/15 带 SRI，未固定 0 个**。剩余无法 SRI 的仅为运行时动态下发（pdf.js worker、transformers 模型分片、sql.js wasm、统计 SDK），已在第十节列明。
5. **密码管理器加密评估**：`manager.html` 的 XOR 密钥由主口令字节循环生成，**密钥不落 localStorage**；localStorage 仅存主口令校验哈希与 XOR 密文。XOR 流对已知明文攻击强度弱，但无固定密钥硬编码、密钥也不在本地持久层 → **接受风险**（页面已有本地演示警示）。

---

## 十六、第七批：AB 安全条目（2026-11-04）

### 16.1 SRI 口径统一（审计线「life 71 页缺 SRI」）

- **统一口径**：只有「静态 HTML 中的跨域 `<script src>`」需要 SRI；自站 `js/*.js`（同源）与运行时动态注入的第三方脚本不在此口径。
- **全站静态跨域 script 统计**：**需要 SRI 15 个 / 已带 SRI 15 个 / 缺失 0 个**（15/15 固定确切版本，无 `@latest`）。
- **审计线 71 页的来源**：`tools/life/*` 71 页全部含 TTZZ 统计脚本，但它是构建期写入的内联 JS，运行时用 `document.createElement("script")` + `el.src = "https://lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?<token>"` 动态插入（全站 8333 页同形态）。URL 带随机 token、内容随下发变化，**技术上无法计算稳定 SRI**，且不是静态 `<script src>`，不属于「需要 SRI」的统计范围。
- **处置**：不为 71 页静态加 SRI；TTZZ 作为已接受的运行时动态下发依赖，单列记录（与第十节 pdf.js worker / transformers / sql.js wasm 同口径）。

### 16.2 CSV 公式注入修复（含同族）

- **中心修复**：`js/tool-kit.js::exp.csv()` —— `TBKit.util.exportTable` / `exportCsv` 的唯一落地点，对以 `= + - @`、`\t`、`\r` 开头的单元格统一前置 `'`。一处覆盖 `data/`、`biz/`、`it/` 及全站所有走 TBKit 导出的 CSV 页面。
- **页面级修复（自建 Blob/文本导出）**：
  - `tools/it/csv-to-json.html`：新增 `csvExportSafe`，复制/下载用安全版，页面预览保持原始数据；
  - `tools/it/json-to-csv.html`：新增 `__jsonToCsvExportSafe`，复制/下载用安全版；
  - `tools/it/keyword-density.html`：导出前对词条加前缀。
  - `matrix-transpose`（仅数字）、`stopwatch` / `pomodoro`（仅数字/时长）经验证不含文本单元格，无需改动。
- 页面已加可见说明（`csv-to-json`、`json-to-csv`）：导出会给公式前缀加单引号。
- verify 新增两条：`it/json-to-csv`、`it/csv-to-json` 注入 `=cmd|' /C calc'!A0`，断言安全导出串以 `'=cmd|` 开头。

### 16.3 另外三条

- **`it/*` 密钥明文 localStorage**：全量检索 `localStorage` 键名与写入点，**未发现 API key/secret/token 持久化**；DES/Rabbit/HMAC/XOR 等加密工具的密钥字段无本页自动保存逻辑（`tb_uxp_` 持久化名单不含这些页面），密码类输入为 `type="password"` 且被持久化代码显式排除 → 无需改动。
- **`it/base64` 历史写入**：`addHistory()` 仅在用户点击编码/解码时调用，非加载即写；已有「清空历史」按钮 → 无需改动。
- **`it/json-formatter` 明文 JSON**：仅在用户输入事件后保存（非加载无条件写入）；`clearAll()` 之前只清空 textarea、不清 localStorage → 已补 `localStorage.removeItem('tb_uxp_tools/it/json-formatter.html#input')`，确保「清空」真正删除明文，并已有清空入口。

### 16.4 门禁与边界

- `node scripts/verify_it_calc.js it/csv-to-json it/json-to-csv` → **12/12 通过**。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 896 / 正确变红 896 / 逃生项 0 / 跳过 1。
- `node scripts/selfcheck_false_pass.js scripts/verify_it_calc.js` → checked=897 risk=0 skipped=0。
- `python3 _test_static.py` → 通过 4705 / 失败 0。
- `python3 _audit_assets.py --check` → 0 死链 / 0 lang 缺失 / 0 重复 id。
- 未跑 `_build.py`、未 push；`js/tool-kit.js` 与页面改动需集成线构建后刷新 SW 版本戳与 `zh-tw/` 产物。

---

## 十七、第八批：隐私面扫描（2026-11-04，只扫不改）

### 17.1 localStorage 全景与机制

- **根因级发现**：`js/tool-ux.js` 对所有工具页 `.container` 内的 `input/textarea/select`（排除 `password/file/hidden`）在用户输入后自动持久化，键名为 `tb_ux_<页面路径>#<字段id>`。全站约 **4705 页**默认带此行为，绝大多数页面**没有「清空本地数据」入口**。
- 另有约 90 页使用页面自有 `localStorage` 键（历史记录/清单/提醒），部分带清空按钮。
- 区分「存结果数值」与「存用户输入原文」：前者是计算参数，后者才是隐私面。以下分级只统计后者。

### 17.2 三档分级

| 档位 | 页数 | 口径 |
| --- | --- | --- |
| 高 | **594** | 健康/医学类 566 + 个人身份标识类 26 + 个人收入类 2 |
| 中 | **6** | 车辆身份/行程地点/宠物照护 |
| 低 | **约 4106** | 纯计算参数、偏好设置、公开数据 |

**高敏（个人身份标识，26 页，含清除入口标注）**：

| 页面 | 持久化内容 | 清除入口 |
| --- | --- | --- |
| legal/will-template-generator | 立遗嘱人姓名/身份证/住址/见证人 | 无 |
| rental/reminder-4 | 租客/地址/电话/租金/租期 | 有（自有键） |
| security/emergency-contacts | 联系人姓名/电话/备注 | 无 |
| wedding/seating-chart | 宾客姓名/分组 | 无 |
| life/stats-13 | 名单/价格 | 无 |
| funeral/memorial-date、grave-design | 逝者姓名/生卒年/碑文 | 无 |
| finance/vcard-qr | 姓/名/电话/邮箱 | 无 |
| design/initials-avatar | 用户姓名 | 无 |
| biz/team-roster-generator | 成员姓名名单 | 无 |
| text/text-extract-phones、biz/text-extract-emails | 批量手机号/邮箱原文 | 有 |
| it/sms-qr、phone-qr、email-qr、phone-parser、email-normalizer | 手机号/邮箱/短信正文 | 无 |
| finance/msisdn-validator、life/phone-lookup | 手机号 | 无 |
| elderly/reminder-time | 药名/剂量/服药时间 | 有 |
| ecommerce/cycle-15 | 客户姓名 | 有 |
| edu/chinese-zodiac、fengshui/birthday-analysis、life/age-in-days | 出生日期/时辰/性别 | 部分有 |
| pr/media-invite | 媒体联系人 | 无 |
| cleaning/staff-schedule | 员工姓名/区域 | 有 |
| tcm-diagnosis/tcm-medical-record、ten-questions、nephrology/manager-1 | 患者姓名/性别/年龄/病史/检验值 | 部分有 |

**高敏（健康/医学 566 页）**：health 40、fitness 37、ophthalmology 31、clinical-nursing 26、hematology 26、neurology 25、rheumatology 25、pediatrics 24、urology/psychiatry 24、cardiology/ent/nephrology/dentistry/dermatology 23、endocrinology/clinical-lab/gastroenterology 22、rehabilitation/beauty/tcm-diagnosis/tcm-pharmacy 21、medical 14、medical2 5 等。共同点：自动保存年龄、性别、身高体重、血压血糖、检验值、症状等健康数据。
（已剔除 `food-testing` 26 页与 `tcm-chemistry` 22 页：前者是食品检测参数、后者是方剂配伍参数，不含个人健康信息。）

**高敏（个人收入 2 页）**：`tax/progressive-income-tax`、`tax/effective-tax-rate`（输入工资/收入并自动持久化）。

**中敏 6 页**：`automotive/countdown-engine-oil`（车名+保养日期）、`automotive/detector-recorder-fuel`（车辆+加油/里程记录）、`usedcar/car-purchase-cost`、`usedcar/recorder-maintenance`（车辆+维保记录）、`hotel/itinerary-planner`（行程地点）、`pet/reminder-vaccine-deworming`（宠物名+疫苗日期+体重）。

### 17.3 URL 参数 / 分享链接

- 全站工具页 **0 处自动写 `location.hash` / `location.search` / `history.pushState|replaceState`**。
- 仅两个用户主动分享入口：`geometry/triangle-heron.html`「复制分享链接」按钮、`it/regex.html` 读取 `#regex=` 回填（只读不写）。
- 结论：不存在「输入即写 URL」导致进浏览器历史/Referer 外泄的路径。

### 17.4 依赖老化（只出清单，不升级）

15 个静态 CDN 标签 / 12 个库，全部固定确切版本 + SRI（15/15/0 不变）。

| 库 | 版本 | 结论 |
| --- | --- | --- |
| pdf.js | 3.11.174 | **有公开 CVE：CVE-2024-4367**（字体处理缺失类型检查 → 任意 JS 执行；修复版 4.2.67）。使用页：office/pdf-split、pdf-rotate（本地渲染用户 PDF） |
| mermaid | 10.9.8 | CVE-2026-71436 影响 `<10.9.8`，当前版本已在修复边界；另有 HTML 注入问题 10.9.6 已修 |
| bcryptjs | 2.4.3 | 2.4.3 为末版（2021 后基本停更），未检索到针对该版本的公开 CVE |
| markmap-lib / markmap-view | 0.17.2 | 版本较旧；未检索到针对该版本的公开 CVE |
| pdf-lib | 1.17.1 | 维护缓慢；未检索到针对该版本的公开 CVE |
| sql.js | 1.8.0 | 可用；未检索到针对该版本的公开 CVE |
| typescript | 5.3.3 | 落后主线（5.x 已有更新版本），无已知 CVE |
| less | 4.9.1 | 较新，未检索到 CVE |
| js-yaml | 4.1.0 | 4.x 已修复旧的 merge-key 问题，未检索到新 CVE |
| acorn | 8.19.0 | 维护中，无已知 CVE |
| d3 | 7.9.2 | v7 末版，无已知 CVE |

唯一建议单独立项升级的是 **pdf.js → ≥4.2.67**（若继续在本地渲染用户上传 PDF）。

### 17.5 共享导出回归（CSV 前缀不误伤）

抽 3 个不同行业页面，在页面上下文直接调用 `TBKit.util.exportCsv` 并截获 Blob 文本：

| 页面 | 首行 | 首列 | 误加前缀 |
| --- | --- | --- | --- |
| agriculture/fertilizer-calculator | `项目名称,数值,备注` | `项目名称` | 否 |
| daily-goods/shoe-size | `项目名称,数值,备注` | `项目名称` | 否 |
| finance/credit-card-interest | `项目名称,数值,备注` | `项目名称` | 否 |

3/3 通过，0 pageerror；正常中文/数字单元格未加 `'`。

### 17.6 处置记录（2026-11-04）

- **pdf.js CVE-2024-4367**：`office/pdf-split`、`office/pdf-rotate` 由 CDN 3.11.174 改为自托管 4.2.67（`vendor/pdfjs/4.2.67/`，legacy ESM，主文件与 worker 同版本）。4.x 官方仅发布 `.mjs`，`import` 语句无法挂 `integrity`，因此改为同源自托管（消除第三方供应链环节，强于 SRI）；文件与 npm 包、jsDelivr 双源 sha384 一致。
  真机实测：单页 PDF 拆 1 页、6 页 PDF 拆 `2,4-5` 得 3 页且文本逐页正确；旋转 90/180/270/0 角度与页面朝向正确、文本无损；0 pageerror。
- **tool-ux 自动持久化**：新增「清空本地数据」浮动入口（按当前页路径前缀删除 `tb_ux_*` 与旧版 `tb_uxp_*`，不触碰其它页），并支持 `data-no-persist`（`<body>` 或控件级）；命中时不回填、不保存，并清除历史遗留键。29 个身份/医疗高敏页（遗嘱、急救联系人、婚宴座位、租客、名单生成、药名提醒、通讯录/电话/邮箱类、中医病历等）已加 body 属性。健康页不改行为，仅依赖统一入口。
