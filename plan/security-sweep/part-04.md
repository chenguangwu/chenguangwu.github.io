## 19. 属性上下文 / localStorage 回灌 XSS 专项（2026-11-05）

### 19.1 硬性坑：`escHtml` 对 `on*="…"` 内联 JS 字符串上下文无效

- **现象**：`style="background:${c}" title="${c}" onclick="loadHistoryColor('${c}')"`，`c` 来自 localStorage 回灌，页面存得住、读回即炸。
- **机制**：`ToolBox.escHtml` 把 `'` 转成 `&#39;`；但 **HTML 属性值在 DOM 解析阶段会把实体解码回 `'`**，再交给内联事件处理器编译。攻击串 `');window.__xss=1;('` 因此仍能逃出字符串字面量 —— 实体转义在文本节点上下文有效，在 `on*` 的 JS 字符串字面量上下文**无效**。
- **正解（按优先级）**：
  1. 改用 `data-*` 承载值 + 静态处理器 `onclick="loadHistoryColor(this.getAttribute('data-hex'))"`（或 `el.dataset.x`）；
  2. 整类改用 `addEventListener` 事件委托，HTML 里不出现任何用户数据；
  3. 必须内联时先 `encodeURIComponent`，再显式把 `'` 替换成 `%27`，并在处理器内 `decodeURIComponent`。
- **实例**：`tools/design/color-picker.html`（commit `c6dd677805`）。

### 19.2 命中一处不等于修完：必须整页复测到 0

- **实例**：`tools/decor/scheduler.html` 先修了 3 处名称回显（甘特条文字、条 `title` 属性、关键路径 `map(...).join()`），复测**仍 `xss=1`、注入 6 个 `<img>`**；第 4 处 `__decTable()` 把 `labels` 裸拼进 `<td>` 才归零。
- **纪律**：每修一处立即复测，直到 `window.__xss === undefined && injectedImg === 0` 才算收口；禁止「改一处就收」。
- **探针常驻项**：`prompt/confirm/alert` 桩必须写进探针（`tools/fitness/cycle-5.html` 的 `add*` 调 `prompt()` 会让无头浏览器阻塞并 TIMEOUT；加桩后复测 `xss=undefined`，页面本身已 `escHtml`，无漏洞）。
- **localStorage 回灌密度**：前两批 40 页命中 2 页（5%）、本批 40 页 + 12 页补充命中 0；属性上下文 4 目录 384 页命中 0。据此定为「回灌优先、属性托底」。

### 19.3 URL 参数反射面：密度低，探针已加正控

- 静态：全站 `URLSearchParams` 56 页、`location.search` 276 页、`location.hash` 1 页；真正「读 `?param`/`#hash` 的值」的页极少，绝大多数是 `?lang=en-US` 的 `/lang=/` 测试或「生成分享链接」的写入端。
- 交叉筛（值来自 URL 参数且进 `innerHTML`/属性/`document.write`）得 36 条，逐条核对后**全部为 i18n 变量（`lang/__EN/EN`）误报**；唯一读 hash 的 `tools/it/regex.html` 只写入 `input.value`（不解析 HTML）。
- 实测：`it/data/text/encode` 优先采样 30 页，对每页同时跑「query 全参注入」「`#<payload>`」「`#q=…&regex=…`」三态 → **0/30 命中**（`xss=undefined && injectedImg=0`）。
- 正控（防假阴）：合成页 `?q=<img onerror>` → `xss=1 img=1`；合成页 `#<payload>` → `xss=1 img=1`。探针对 query/hash 两路反射均能报红，0/30 可信。
- 结论：**URL 参数反射面密度低**，暂不再扩大样本；后续维持 1 目录/批属性托底（本批 `eco` 40 页，0 交叉）。

### 19.4 跳转 / 资源赋值面：0 命中，探针已有正控

- 静态口径：把用户输入（表单值 / `localStorage` / URL 参数 / `prompt`）赋给 `location.href` / `location.assign` / `location.replace` / `window.open` / `a.href` / `img.src` / `iframe.src` / `form.action`，且**无 `http(s)` 白名单**的交叉项。
- 结果：**14 页**命中静态交叉，逐页核对**全部安全**：
  - `security/emergency-contacts.html:435`：`location.href='tel:'+num.replace(/-/g,'')`，前缀固定 `tel:`，`javascript:` 无法构造；
  - `design/mesh-gradient`、`identicon-generator`、`biz/text-to-banner`、`it/svg-placeholder-generator`、`it/lorem`、`math/function-plotter`、`image/image-crop`、`encode/image-to-base64`：`a.href = canvas.toDataURL(...)`（服务端不可控的 data URL 下载）；
  - `design/image-to-ascii`、`it/base64-converter`、`image/image-watermark`、`design/palette-extractor`、`audio/audio-speed`：`img.src` 来自 `FileReader` 的 `data:` 或 `/^data:image\//` 前置校验；
  - 全站 `window.open` 动态调用 0 处。
- 实测：14 页静态命中页 + 16 页 `it/marketing/office/data` 有文本输入且含导航语法的页 = **30 页**；对每页「填 `javascript:window.__xss=1` → 调用 `go/open/jump/visit/redirect/nav/download/link/preview/run/create/save/add` 等全局动作函数 → 点击 `a[href^="javascript:"]`」→ **0/30 命中**（`xss=undefined && img=0 && nav=no && jsHref=0`）。
- 正控（防假阴）：合成页 `location.href = input.value`（加载即执行）→ `xss=1`；同一探针在真实页为 0，结论可信。
- 协议相对跳转 `//evil.example`：全站无「用户输入 → `location`/`window.open`」的赋值点，无从触达，记为不适用。

## 20. 安全清扫总览（2026-11-05 收面）

### 20.1 已扫面与产出

| 注入面 | 样本 | 命中页 | 漏洞类型 |
|---|---|---|---|
| 用户输入 → `innerHTML` 文本回显 | 第一批 9 目录 124 页 + 后续抽检 | 4 | DOM XSS（文本节点未转义） |
| 属性上下文（转义器 × 属性拼接） | 310 个转义器 / 1118 处拼接 / 8 目录 384 页 | 3 | 属性逃逸（`"`/`'` 未转义；含 `src=` data-URL 预览） |
| localStorage 回灌（对象数组 + `map/join`） | 20 + 20 + 40 + 12 = 72 页 | 3 | 存得住、读回炸（`menu-margin`/`scheduler`/`color-picker`） |
| URL 参数反射（`?q` / `#hash`） | 282 页静态 + 30 页实测 | 0 | —（交叉项全为 i18n 误报） |
| 跳转 / 资源赋值（`javascript:` / 外域） | 14 页静态 + 30 页实测 | 0 | —（全部前缀限定或 data: 校验） |

### 20.2 累计修复（10 页 / 5 个修复提交）

| 提交 | 页面 | 类型 |
|---|---|---|
| `ba7e2b98b8` | `admin/detector-time`、`energy/stats-energy`、`general/convert-22`、`life/clothing-size-converter` | 文本回显未转义 |
| `ccda8b6ec0` | `encode/image-to-base64` | `esc()` 只转 `&<>` → `src="…"` 属性逃逸 |
| `6e4ae6d78e` | `food-processing/material-balance`、`recipe-cost-calculator` | `value="…"` 属性逃逸 |
| `1673b215b4` | `restaurant/menu-margin` | localStorage 回灌 → `map(...).join()` 裸拼 |
| `c6dd677805` | `decor/scheduler`、`design/color-picker` | 回灌 + `on*` 内联 JS 字符串逃逸 |

误报 0（所有修复均有修前 `xss=1` / 修后 `xss=undefined` 的真实浏览器证据，且做过还原版正控）。

### 20.3 尚未覆盖的面（供下一轮决策）

- **CSS 注入**：`style="${userInput}"` / CSS 变量值的 `url()`、`expression`、`@import`（当前只挡了 HTML 属性逃逸，未评估 CSS 侧信道）。
- **`srcdoc` / 动态 `<iframe>` 内容**：全站静态 0 处动态 `srcdoc`，未做真机验证。
- **`postMessage` 来源校验**：仅 `it/code-runner` 1 处接收端，数据已转义，但**未校验 `event.origin`**（低危）。
- **第三方 CDN 脚本完整性**：`ttzz` 等外链无 SRI / 无 `crossorigin`，供应链风险未纳入本轮。
- **文件内容解析器**：PDF/DOCX/XLSX/SQLite 解析库（pdf.js、sql.js、SheetJS）对恶意文件的行为未做 fuzz。
- **SVG 上传/渲染**：`image/*` 与 SVG 字符串进入 `img.src`/canvas 的边界未系统测（SVG 内联脚本在 `img` 下不执行，但 `srcdoc`/`innerHTML` 路径需复核）。
- **`eval` / `new Function` / 字符串定时器**：`it/code-runner`、`it/sqlite-runner` 等「本地代码执行」页属产品功能，未按漏洞处理，但需确认不接收外部传入。
- **剪贴板与拖拽**：`navigator.clipboard.readText()` 内容进入 DOM 的路径未扫。
- **Web Components / Shadow DOM**：`innerHTML` 写入 shadow root 的路径未单独统计。

## 21. 样式 / 嵌入 / 消息三面专项（2026-11-05）

### 21.1 CSS 注入面：30 页 0 命中

- 静态：`style="…"` 字符串拼接全站 **3513** 处（绝大多数拼的是数值/常量色，不是用户输入）；按「变量来自 `.value` + 同行出现在 `style` 拼接」精筛后取**颜色类候选 17 页**，补 13 页高密度 `style` 拼接页，共 **30 页**。
- 判据（按本轮要求）：只认「能越出 `style` 属性、改 DOM 结构或执行脚本」；仅改颜色/尺寸不算漏洞。`url(javascript:)` 在现代浏览器不执行，`expression()` 仅 IE，均不计。
- 实测：填入 `red" onmouseover="window.__xss=1` → 触发 `calc/render/update/apply/generate/draw/refresh/convert/build/preview/run` → 遍历所有元素的 `on*` 属性找 `__xss` 并派发 `mouseover`。
- 结果：**0/30 命中**（`xss=undefined && injAttr=0`）。
- 正控：合成页 `style="color:'+input+'"` → **`xss=1 injAttr=1`**，探针对属性闭合逃逸可报红。

### 21.2 `srcdoc` / 动态 iframe：0 可利用

- 静态：`srcdoc` 仅 4 处文本命中 —— `it/code-runner.html:726/759/892`（**产品功能**：本地代码运行器，iframe 为 `sandbox="allow-scripts allow-modals"`，**无 `allow-same-origin`**）与 `it/rich-text-editor.html:364`（**清洗器**，显式移除 `srcdoc`/`on*`/`formaction`）。
- `iframe.contentDocument.write` / `createElement('iframe')` 后写内容：**0 处**。
- 结论：`code-runner` 的 srcdoc 内容是用户自己输入的代码，页面无 URL 参数可注入，且 sandbox 已阻断父页访问；`rich-text-editor` 主动剥离危险属性。
- 正控（双态）：
  - 无 `sandbox` 的 `srcdoc`（`parent.__xss=…`）→ **`xss=srcdoc-unsandboxed`**（逃逸成功，证明该判据有效）；
  - 加 `sandbox="allow-scripts"` 的同段代码 → 脚本仍执行（`GOOD_RAN`），但 **`parent.__xss` 未被置位**（跨源不透明 origin 阻断）；
  - `code-runner` 的 sandbox 配置与「安全态」一致 ⇒ 0 可利用。

### 21.3 `postMessage`：1 处接收端，转义安全、缺 origin 校验（低危）

- 发送端 5 处：`it/regex.html:521`（Worker）、`it/text-replace.html:1009`（Worker）、`it/code-runner.html:746/753`（预览 iframe → 父页控制台）、`it/text-replace.html:1066/1068`（Worker 回传）。
- 接收端 3 处：`it/regex.html:519`、`it/text-replace.html:1007`（均为**同源 Worker**，不可被外部页面触达）、`it/code-runner.html:763`（`window` 级监听，任意窗口可投递）。
- `code-runner` 接收逻辑：仅接受 `{type:'console'}`，`data` 经 `escapeConsoleHtml`（`textContent→innerHTML`）后放入 `<span>` 文本上下文（引号无逃逸风险）。
- 实测（真机）：向 `code-runner` 投递 `{type:'console',method:'log',data:['<img src=x onerror="parent.__xss=1">']}` → **`escaped=yes`、`img=0`、`xss=undefined`**，控制台新增 1 行（`lines=3`），注入串以 `&lt;img` 文本呈现。
- 正控：合成页接收端直接 `innerHTML = e.data.v` → **`xss=1 img=1`**，探针可报红。
- 唯一缺陷：**未校验 `event.origin`**，任意页面可在用户打开 `code-runner` 时伪造控制台日志（文本欺骗），**不可执行脚本**，列低危、暂不改（改动会引入来源白名单维护成本）。

## 22. 剪贴板 / SVG / Shadow DOM 三面专项（2026-11-05）

### 22.1 剪贴板 / 拖拽 / 文件内容入 DOM：0 命中

- 静态：`paste`/`drop` 监听共 **45 处**（去重后约 41 个页面）：
  - `paste` 3 处：`it/rich-text-editor.html:632`（**唯一**把剪贴板 HTML 写进编辑区）、`it/json-formatter.html:726`（仅对 `textarea.value` 触发校验，不解析 HTML）、`cognition/human-benchmark.html:769`（**显式拦截**粘贴）。
  - `drop` 其余：全部走 `e.dataTransfer.files[0]` → `handleFile(s)` → `FileReader` / `createObjectURL` → canvas/`<img>`，无文本入 `innerHTML`；`design/farnsworth-d15-test` 只取 `getData('text/plain')` 后 `parseInt`。
- 实测（真机）：`it/rich-text-editor` 派发 `ClipboardEvent`（`text/html = <img src=x onerror="window.__xss=1">`）到 `#editor` → **`xss=undefined`、`img=0`、无 `onerror` 残留**；其 `sanitizeHtml()` 走 DOMParser 白名单，删除 `on*` / `srcdoc` / `formaction` / 非白名单 `href|src`，`style` 含 `expression(|javascript:|url(|@import` 时整条移除。
- 正控：合成页 `paste` → `innerHTML = clipboardData.getData('text/html')`（无清洗）→ **`xss=1 img=1`**，证明探针能捕获粘贴注入。

### 22.2 SVG 上传 / 渲染边界：0 命中

- 静态：动态构造 `<svg>` 并写 DOM 的页面 **10 个**；其中真正接收**用户 SVG 文本**的只有 2 个：
  - `design/svg-viewer.html:269-282`：`sanitizeSvg()` 字符串清洗后 `preview.innerHTML = safe.html`；
  - `design/svg-to-png.html:343-393`：`__svgSanitize()` 去 `foreignObject` / 外链 `href|src` / `@import`，再以 `Blob → <img> → canvas` 解码导出（**不插入实时 DOM**）。
  - 其余 8 个（`transport/calc-53`、`meteorology/calc-55`、`electronics/smt-stencil`、`math/geometry-calculator`、`data/data-visualizer` 等）`<svg>` 只拼计算出的数值坐标，无用户文本。
- 实测（5 种向量，`svg-viewer`）：`<svg onload>`、`<script>`、`<foreignObject><img onerror>`、`<a xlink:href="javascript:">`（并派发 click）、`<image href="data:image/svg+xml,<svg onload=…>">` → **全部 `xss=undefined`，预览中 `on*` / `javascript:` / `foreignObject` / `<script>` 均为 no**。
- 实测（`svg-to-png`，2 种向量）：`onload` SVG 与 `foreignObject+onerror` SVG → 均成功转出 PNG（`img=1`），**`xss=undefined`、预览无 `on*`**（`<img>` 解码上下文不执行脚本）。
- 正控：合成页 `innerHTML = '<svg onload="window.__xss=1">'` → **`xss=1`**，证明「SVG 事件执行」判据可报红。

### 22.3 Shadow DOM / Web Components：全站 0 触达

- `attachShadow`：**0 处**；`customElements.define`：**0 处**（`tools/` + `js/` 全量 grep）。
- 结论：不存在 shadow root 内 `innerHTML` 写入通路，本面无攻击面可测。

## 23. 安全线收面总结（2026-11-05）

### 23.1 扫过的面 × 样本 × 命中 × 修复

| # | 注入面 | 页 / 点 | 命中 | 修复 | 正控 |
|---|---|---|---|---|---|
| 1 | 用户输入 → 文本回显 | 9 目录 124 页 + 抽检 | 4 | 4 | 通（注入串报红） |
| 2 | 属性上下文（转义器 × 拼接） | 384 页 / 1118 点 | 3 | 3 | 通（`value=` 逃逸复红） |
| 3 | localStorage 回灌 | 72 页 | 3 | 3 | 通（还原版复红） |
| 4 | URL 参数反射 | 282 页静态 / 30 页实测 | 0 | 0 | 通（query+hash 双态） |
| 5 | 跳转 / 资源赋值 | 14 页静态 / 30 页实测 | 0 | 0 | 通（`location.href` 复红） |
| 6 | CSS 注入 | 3513 点 → 30 页实测 | 0 | 0 | 通（属性闭合复红） |
| 7 | `srcdoc` / 动态 iframe | 4 处 / 2 页 | 0 | 0 | 通（无 sandbox vs 有 sandbox 双态） |
| 8 | `postMessage` | 5 发 / 3 收 | 0 | 0 | 通（裸 `innerHTML` 复红） |
| 9 | 剪贴板 / 拖拽 / 文件 | 45 点 / 41 页 | 0 | 0 | 通（粘贴复红） |
| 10 | SVG 上传 / 渲染 | 10 页 / 2 个用户 SVG 入口 | 0 | 0 | 通（`<svg onload>` 复红） |
| 11 | Shadow DOM / Web Components | 0 触达 | — | — | 不适用 |

- **累计修复 10 页 / 5 个修复提交**（见 §20.2），误报 0；每页修后均复测到 `xss=undefined && injectedImg=0`，并做正常值逐字符回归。
- 剩余低危留档 1 条：`it/code-runner` 的 `postMessage` 未校验 `origin`（仅文本伪造，不可执行）。

### 23.2 明确未覆盖的面

1. **第三方 CDN 供应链**：`ttzz` 等外链脚本无 SRI、无 `crossorigin`。**定位为供应链风险，不是本站「输入 → DOM」漏洞**；不通过加 SRI 修复（会让 CDN 版本更新失败）。
2. **本地文件解析器**：pdf.js / sql.js / SheetJS 对恶意 PDF/DOCX/XLSX/SQLite 的行为未做 fuzz（属解析库安全问题，非本站代码注入）。
3. **`eval` / `new Function` 本地执行页**：`it/code-runner`、`it/sqlite-runner` 属产品功能，输入不来自 URL/外部页面，未按漏洞处理。
4. **剪贴板读取 API**：`navigator.clipboard.readText()` 的内容入 DOM 路径未单独统计（当前全站无该调用）。
5. **DOM clobbering / CSP / 浏览器扩展**：已在 §24 补扫（clobbering 0 可利用、全站 0 处 CSP、构建期注入全静态）；浏览器扩展仍不在本站代码范围。
6. **构建期产物**：已在 §24.3 确认 `_build.py` 注入的 TTZZ / ToolBox 桩均为静态常量，无用户可控拼接。

### 23.3 一句话结论

**「用户输入 → DOM」的可执行通路已全部扫过（11 个面、正控全覆盖），未发现剩余未扫的注入通路；残留风险只在第三方供应链与本地文件解析库，不在本站输入链。** 

## 24. 三个窄面补扫（DOM clobbering / CSP / 构建期注入，2026-11-05）

> 本节只做定位与台账，**未改动任何页面代码**；补齐 §23.2 未覆盖清单第 5、6 条后，安全线正式封账。

### 24.1 DOM clobbering：20 页采样，0 可利用

- 采样口径：`tools/it` 输入框最多的 10 页 + `tools/admin` 输入框最多的 5 页 + 全站输入框最多的 5 页（去重）= **20 页**。
- 静态命中：页面元素 `id`/`name` 与脚本同名全局（`function X` / `var X` / `window.X=`）撞名 **8/20 页、20 个名字**：
  - `it/hash.html`（batchResults / hmacKey / hmacMode / textResults / verifyHash）
  - `admin/travel-subsidy.html`（mealStd / transStd）、`admin/detector-time.html`（rows）、`admin/supplies-forecast.html`（itemName）、`admin/version-control.html`（author）
  - `library/citation-format.html`（seq / title）、`math/equation-solver.html`（a / c / d）、`tcm-diagnosis/tcm-medical-record.html`（advice / analysis / chief / past / present）
- 真机（同源 iframe 读 `typeof window[name]`）：撞名名字全部解析为 `object`（对应 `INPUT`/`DIV`/`TEXTAREA` 元素），即「命名元素暴露」确实成立；唯一例外是 `it/hash.html` 的 `verifyHash` = `function`（顶层 `function verifyHash` 为 own property，命名元素不生效）。
- 反向核查（真正会读全局的写法）：全站 `window.<name>` 读法精筛，要求 `name` 同时是该页元素 `id`/`name` → **仅 2 页**：
  - `it/hash.html` → `window.verifyHash`，有 `function verifyHash` own 声明，元素不生效；
  - `sales/conversion-funnel.html` → `window.stages`，有 `var stages` own 声明，元素不生效。
- 结论：**撞名普遍、可利用点为 0**。本站不存在「依赖全局值为非元素对象」的读法，clobbering 的后果上限是功能性遮蔽（若元素覆盖未声明全局），不构成脚本执行通路；两处真实全局读法均被 own property 覆盖。

### 24.2 CSP：全站 0 处 meta，属既有设计

- `http-equiv="Content-Security-Policy"` 全站 grep **0 处**（`tools/` + 根目录 + `guides/`）。
- 仅 2 页在教学文案里提到该词（不是策略声明）：`it/http-response-headers.html`、`it/nginx-cheatsheet.html`。
- 结论：本站为纯静态 GitHub Pages 站点，无自定义响应头能力，**无 CSP 属既有设计**；若要引入 CSP，需先完成全站 inline 脚本 / inline `style` 改造（本轮只定位、不改）。

### 24.3 构建期注入脚本：全静态常量，无拼接

- `_build.py:2884-2904` 的 `TTZZ_BLOCK` 是纯字面量字符串拼接：固定 CDN URL、固定 `el.id="ttzz"`、固定 `try/catch` 包裹，**无 `%` / `.format()` / f-string / 任何变量插值**。
- `inject_ttzz_snippet()`（`_build.py:2916`）只做两种动作：命中 `TTZZ_BLOCK_RE` 则**整块替换**，未命中则注入 `<head>`；不读取、不拼接页面内容。
- 同链路的 `_TOOLBOX_STUB_JS`（L809-816）与 `TOOLBOX_API_STUB` / `TOOLBOX_API_STUB_EXT`（L817-818）同为静态常量，构建期落盘为 `/js/toolbox-stub.js`；`SECMETA.inject` 亦为静态安全 meta 兜底。
- 结论：**构建期注入块无用户可控内容拼入**，不存在「构建产物带入注入串」的通路。

### 24.4 封账声明

三个窄面补齐后，§23.2 的「DOM clobbering / CSP / 构建期产物」三项全部关闭。安全线累计：**11 个注入面 + 3 个窄面，正控全覆盖，10 页真漏洞修复、5 个修复提交、误报 0**，本线正式封账。后续如需继续，只剩 §23.2 的供应链与解析库两类外部风险（不属本站代码层）。

### 25 正文过薄普查（只读，2026-11-05）

- 对 4705 个工具页按「body 可见纯文本（CJK 1 字 + ASCII 词 1 个，剔除 nav/header/footer/script/style/sr-only/aria-hidden/.t-en/.related-tools）」做只读普查：P1 过薄 <1200 = **4406**、P2 偏薄 1200–2000 = **297**、合格 ≥2000 = **2**，中位 753 字；其中 P1 有 4314 页含 `TBKit.matrix/chart` 运行时表格/图表（静态散文薄 ≠ 页面空），无运行时渲染的「真薄候选」92 页。清单见 `/tmp/thin-body-scan.md`；30 页无头复核显示偏差 24/30 页、平均 +234 字，方向为浏览器**多于**静态（运行时渲染），静态口径未把隐藏内容算进去。

### 25.1 92 页真薄候选三分类口径（2026-11-05）

- **R（合理不改，11 页）**：**页面主体本身即为条目表 / 标准表，正文与表自洽** —— 信息密度已在表格里（如 HTML 标签表、KeyCode 表、化妆色号表、药品信息表、汇率速查表、量表分级表），补散文只会稀释表格、不增加事实，故不改。
  - 11 页：`it/html-tags`、`it/css-properties`、`it/keycode-info`、`it/html-entity-encoder`、`beauty/makeup-shade`、`medical/drug-info`、`travel/currency-cheat-sheet`、`rehabilitation/flacc-scale`、`clinical-nursing/pain-nrs`、`ophthalmology/ishihara-test`、`security/data-erase-simulator`。
- **S（内容过薄，7 页）**：只有标题 + 输入/演示 + 一句说明，既无实质公式/阈值，也无真实条目；需补「原理/公式 + 2 个 node 实跑算例 + 边界或误用」。
  - 7 页：`image/wechat-cover-maker`、`image/gif-split`、`office/mindmap`、`pet/training-planner`、`restaurant/taste-preference`、`music/web-tuner`、`image/image-mosaic`。
- **M（中等，74 页）**：已有公式/规则，但算例模板化或数字不可复算；只补真实算例与取值依据，不硬加段落。
- 补充口径：R 的判据只用于「有真实表格内容」的页面；表格若是空壳/占位则归 S 或 M，不适用本条。

