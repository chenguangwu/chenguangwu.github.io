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
