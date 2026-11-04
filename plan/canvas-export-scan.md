# 全站图片/画布导出族普查（只读台账）

> 状态：**只读静态取证**，未跑真机、未改任何工具页。生成于 2026-11-05。
> 范围：`tools/**/*.html` 内联脚本 + 被工具页引用的 `js/tools/*.js`（3 个外置模块）。
> 触发口径：出现 `toBlob(` 或 `toDataURL(`。
> 结果：**61 页 / 75 次调用**。**A = 2，B = 37，C = 22**。

本文档只回答「谁会导出图片、谁没有兜底、谁可能被污染」。CSV/JSON 文本导出不在本台账内（上一批已收口）。

---

## 一、扫描口径（可复现）

1. **文件枚举**：`tools/**/*.html` 全量；另外补扫被页面引用的 `js/tools/*.js`（本次命中 3 个：`colorblind-simulator.js`、`bigfive-personality-test.js`、`cognitive-assessment.js`）。外置模块的存在说明「只扫 HTML」会漏页，后续复扫必须带上这一层。
2. **调用点**：`toBlob(` / `toDataURL(` 每一次出现都算一次调用，同页多次分别记录。
3. **A 档（已兜底）**：该页**所有**调用点同时满足
   ① 调用前 260 字符内出现 `try {`；
   ② 调用后 700 字符内出现 `catch(`；
   ③ catch 体内含 `showToast` / `alert` / `失败` / `error` 之一；
   ④ 不属于 C 档（污染优先，一票否决）。
4. **C 档（污染风险）**：满足任一条静态证据即归 C，无论有没有 try/catch：
   - 页面/模块自有 SVG 输出含 `<foreignObject`；
   - 自有静态外链图像 `<img src="https?://…">`；
   - 自有 CSS `url(https?://…)` 或 `@font-face` 指向外链；
   - **用户可控 SVG 输入**：`accept="image/*"`（含 `image/svg+xml`），或任意 SVG 文本输入，且页面有 `drawImage(`；
   - 导出调用位于 `img.onload` 等**异步回调内**（外层同步 try 覆盖不到）。
5. **B 档（无兜底）**：其余出现调用、但不满足 A 的页面。
6. **已知不覆盖**（须真机补证）：`toBlob` 返回 `null` 的静默失败、canvas 尺寸 0 / OOM、`beforeunload` 期间导出、Safari 的 canvas 面积上限。

> **污染证据的边界**：C 档 22 页的自有标记里 `<foreignObject` / 外链 `<img>` / 外链 CSS / `@font-face` **全部为 0**。也就是说，污染源不在页面自己的 SVG 里，而在**用户上传的 SVG**（`image/*` 允许 SVG，若其中含 `foreignObject` 即污染画布）。因此 C 档的静态证据是「入口存在 + 无 sanitize + `drawImage`」，具体 `foreignObject` 数量只能等真机喂样本后判定。

### 证据字段表

| 字段 | 含义 | 本次结果 |
|---|---|---|
| `fo` | 自有标记里 `<foreignObject` 数量 | 除 `office/mindmap`（JS 转换代码内 5 处、输出 SVG 为 0）外全为 0 |
| `accept` | 文件输入接受类型 | C 档 21 页为 `image/*`（含 SVG） |
| `extImg` | 静态外链 `<img src>` | 全站 0 |
| `extCSS` | CSS `url(https?://…)` | 全站 0 |
| `fontFace` | `@font-face` | 全站 0 |
| `drawImage` | 页面/模块内 `drawImage(` 次数 | 1–6（C 档） |

---

## 二、A 档：已兜底且已验证（2 页）

| # | 页面 | 调用点 | 兜底形态 | 验证方式与结果 |
|---|---|---|---|---|
| 1 | `tools/office/flowchart.html` | `downloadPNG()` 内 `canvas.toBlob`（异步 `img.onload` 回调内） | `try { canvas.toBlob(...) } catch (e) { ToolBox.showToast('导出失败：' + (e.name \|\| e.message \|\| e), 'error') }` | 真机：PNG 462×1556 / 69,686 B；导出 SVG 内 `foreignObject` = 0（`mermaid.initialize({ htmlLabels:false, flowchart:{htmlLabels:false,useMaxWidth:false} })` 三处）；长节点名实测 399.8 px < 节点 415 px 无溢出；断 CDN 时中英依赖提示正常 |
| 2 | `tools/office/mindmap.html` | `canvas.toBlob` | `setTimeout` 回调外层 try/catch + 内层 `toBlob` catch，消息取 `e.name \|\| e.message` | 真机：PNG 698×956 / 72,308 B；父级 `translate(549,3)` / `(388,161)` 下，`getBBox()` 局部坐标 8.0 对应屏幕 280.3 / 201.8，文字与 SVG 参考对齐；转换后 `foreignObject` = 0 |

> 这两页是**上一批**修好并验收的，作为 A 档的基准样本；其余页面没有任何一页达到 A 档。

---

## 三、B 档：无兜底（37 页 / 42 次调用）

成本档定义：

- **T0**（最便宜）：已有 `try/catch`，但 catch 体为空 / 无提示 → 只补一句提示。
- **T1**：单点裸调用、同步 canvas 绘制 → 外层补 `try/catch` + toast。
- **T2**：同页多处调用 → 逐点补。
- **T3**：Promise 包装 + `blob === null` 静默失败 → 补 reject / null 分支。

| # | 页面 | 调用点（函数 @ 行 / API） | 成本档 |
|---|---|---|---|
| 1 | `tools/it/qrcode.html` | downloadQR() L511 `toDataURL` | T0 |
| 2 | `tools/library/generator-label.html` | downloadLabel() L339 `toDataURL` | T0 |
| 3 | `tools/biz/barcode-generator.html` | downloadPNG() L445 `toDataURL` | T1 |
| 4 | `tools/cognition/cognitive-assessment.html` | 外置模块 `js/tools/cognitive-assessment.js` L1114 `toBlob` | T1 |
| 5 | `tools/cognition/human-benchmark.html` | exportPng() L1081 `toBlob` | T1 |
| 6 | `tools/design/avatar-generator.html` | generate() L356 `toDataURL` | T1 |
| 7 | `tools/design/aztec-code.html` | generate() L305 `toDataURL` | T1 |
| 8 | `tools/design/cvd-safe-palette.html` | renderResult() L628 `toBlob`（`blob` 为空时静默 return） | T1 |
| 9 | `tools/design/data-matrix.html` | generate() L294 `toDataURL` | T1 |
| 10 | `tools/design/favicon-from-emoji.html` | generate() L274 `toDataURL` | T1 |
| 11 | `tools/design/favicon-from-text.html` | generate() L283 `toDataURL` | T1 |
| 12 | `tools/design/identicon-generator.html` | generate() L290 `toDataURL` | T1 |
| 13 | `tools/design/initials-avatar.html` | generate() L344 `toDataURL` | T1 |
| 14 | `tools/design/mesh-gradient.html` | downloadPNG() L401 `toDataURL` | T1 |
| 15 | `tools/design/pixel-art.html` | exportPNG() L628 `toDataURL` | T1 |
| 16 | `tools/design/qr-code-styled.html` | generate() L289 `toDataURL` | T1 |
| 17 | `tools/design/signature-pad.html` | exportPNG() L548 `toDataURL` | T1 |
| 18 | `tools/design/spectrum-visualizer.html` | copyResult() L339 `toDataURL` | T1 |
| 19 | `tools/design/waveform-visualizer.html` | copyResult() L322 `toDataURL` | T1 |
| 20 | `tools/image/wechat-cover-maker.html` | download() L288 `toBlob`（`if(!blob) return` 静默） | T1 |
| 21 | `tools/it/barcode-codabar.html` | downloadBarcodePNG() L301 `toDataURL` | T1 |
| 22 | `tools/it/barcode-code128.html` | downloadBarcodePNG() L257 `toDataURL` | T1 |
| 23 | `tools/it/barcode-code39.html` | downloadBarcodePNG() L297 `toDataURL` | T1 |
| 24 | `tools/it/barcode-ean.html` | downloadBarcodePNG() L301 `toDataURL` | T1 |
| 25 | `tools/it/barcode-itf.html` | downloadBarcodePNG() L285 `toDataURL` | T1 |
| 26 | `tools/it/barcode-msi.html` | downloadBarcodePNG() L303 `toDataURL` | T1 |
| 27 | `tools/it/barcode-upc.html` | downloadBarcodePNG() L292 `toDataURL` | T1 |
| 28 | `tools/math/function-plotter.html` | downloadPlot() L570 `toDataURL` | T1 |
| 29 | `tools/ophthalmology/amsler-grid-test.html` | snapshotCanvas() L690 `toDataURL` | T1 |
| 30 | `tools/ophthalmology/astigmatism-chart.html` | snapshotUrl() L615 `toDataURL` | T1 |
| 31 | `tools/ophthalmology/eye-chart-toolkit.html` | recalcPpi() L767 `toBlob` | T1 |
| 32 | `tools/psychology/bigfive-personality-test.html` | 外置模块 `js/tools/bigfive-personality-test.js` L897 `toBlob` ＋ L900 `toDataURL`（无 `toBlob` 时回退） | T1 |
| 33 | `tools/psychology/bubble-tea-personality-quiz.html` | exportPng() L830 `toBlob` | T1 |
| 34 | `tools/psychology/enneagram-test.html` | exportPng() L788 `toBlob` | T1 |
| 35 | `tools/design/favicon-generator.html` | downloadCanvas() L506 `toBlob`；copyDataURL() L537 `toDataURL` | T2 |
| 36 | `tools/it/captcha-generator.html` | exportImage() L814；onclick() L888；batchExportAll() L917（均 `toDataURL`） | T2 |
| 37 | `tools/image/gif-split.html` | makeThumb() L916 `toDataURL`；canvasToBlob() L940 `toBlob`（Promise 包装） | T3 |

> 分档修正说明：`gif-split` 原按 `accept="image/*"` 归 C，复核后其入口为 `accept="image/gif"`（GIF 为位图、不可能含 `foreignObject`）⇒ 无污染路径，落回 B。

---

## 四、C 档：污染风险（22 页 / 31 次调用）

**公共证据**：入口 `accept="image/*"`（含 `image/svg+xml`）＋ 有 `drawImage` ＋ 无任何 `foreignObject` / 外链过滤或 sanitize；自有标记 `fo=0 / extImg=0 / extCSS=0 / fontFace=0`。风险形态为「用户上传带 `foreignObject` 的 SVG ⇒ canvas tainted ⇒ `toBlob`/`toDataURL` 抛 `SecurityError`」。

| # | 页面 | 入口证据 | 调用点 | 其他静态证据 | 成本档 |
|---|---|---|---|---|---|
| 1 | `tools/design/colorblind-simulator.html` | `accept=image/*`（file input 1 个） | 外置模块 `js/tools/colorblind-simulator.js` L616 / L635 / L647 `toDataURL`（预览），L819 `toBlob`（导出） | `drawImage` 6 次；`im.src = ev.target.result` 走用户文件 | C1 |
| 2 | `tools/design/color-palette-generator.html` | `accept=image/*` | exportImage() L820 `toDataURL` | `drawImage`=1，无 try/catch | C1 |
| 3 | `tools/design/image-cropper.html` | `accept=image/*` | generate() L304 `toDataURL`；L310 `toBlob` | `drawImage`=2，0/2 有 catch | C1 |
| 4 | `tools/design/image-flipper.html` | `accept=image/*` | flip() L302 `toDataURL`；L311 `toBlob` | `drawImage`=1，1/2 有 catch | C1 |
| 5 | `tools/design/image-format-converter.html` | `accept=image/*` | convertAll() L1038 `toBlob` | `drawImage`=1，1/1 有 catch（异步回调内仍可能漏） | C1 |
| 6 | `tools/design/image-resizer.html` | `accept=image/*` | generate() L299 `toDataURL` | `drawImage`=2，0/1 有 catch | C1 |
| 7 | `tools/design/image-rotator.html` | `accept=image/*` | generate() L291 `toDataURL` | `drawImage`=1，0/1 有 catch | C1 |
| 8 | `tools/design/image-rounded-corners.html` | `accept=image/*` | downloadResult() L1160 `toDataURL` | `drawImage`=1，1/1 有 catch | C1 |
| 9 | `tools/design/svg-to-png.html` | 任意 SVG 文本 `<textarea id="svgInput">`（无 accept） | generate() L289 `toDataURL`（位于 `img.onload` 回调内） | `drawImage`=2；`new Blob([svg], {type:'image/svg+xml'})` → `img.src` → 绘制；外层 try 在 L274，**覆盖不到 L289 回调内异常**；`img.onerror` 只提示加载失败 | **C2** |
| 10 | `tools/fun/sliding-puzzle.html` | `accept=image/*` | useDefaultImage() L592；applyImageTile() L762（`toDataURL`） | `drawImage`=1，0/2 有 catch | C1 |
| 11 | `tools/image/id-photo-crop.html` | `accept=image/*` | download() L354 `toBlob` | `drawImage`=1，0/1 有 catch | C1 |
| 12 | `tools/image/image-collage.html` | `accept=image/*` | download() L700 `toBlob` | `drawImage`=4，0/1 有 catch | C1 |
| 13 | `tools/image/image-compress.html` | `accept=image/*` | compressImage() L525 `toBlob` | `drawImage`=1，0/1 有 catch | C1 |
| 14 | `tools/image/image-converter.html` | `accept=image/*` | convertAll() L316 `toBlob` | `drawImage`=1，0/1 有 catch | C1 |
| 15 | `tools/image/image-crop.html` | `accept=image/*` | downloadCrop() L948 `toBlob` | `drawImage`=5，0/1 有 catch | C1 |
| 16 | `tools/image/image-filter.html` | `accept=image/*` | downloadFiltered() L364 `toBlob` | `drawImage`=1，0/1 有 catch | C1 |
| 17 | `tools/image/image-mosaic.html` | `accept=image/*` | downloadImage() L687 `toBlob` | `drawImage`=6，0/1 有 catch | C1 |
| 18 | `tools/image/image-resize.html` | `accept=image/*` | render() L774 `toBlob`；copyPreviewData() L830 `toDataURL` | `drawImage`=3，1/2 有 catch | C1 |
| 19 | `tools/image/image-rotate.html` | `accept=image/*` | downloadImage() L626 `toBlob` | `drawImage`=2，0/1 有 catch | C1 |
| 20 | `tools/image/image-watermark.html` | `accept=image/*`（2 个 file input） | downloadImg() L976 `toBlob` | `drawImage`=4，0/1 有 catch | C1 |
| 21 | `tools/image/nine-grid-cutter.html` | `accept=image/*` | splitAndRender() L386；downloadOne() L393（`toBlob`） | `drawImage`=1，2/2 有 catch（污染仍会抛） | C1 |
| 22 | `tools/it/qr-beautify.html` | `accept=image/*`（Logo 上传） | downloadPng() L398；copyBase64() L406（`toDataURL`） | `drawImage`=1，0/2 有 catch | C1 |

成本档定义：

- **C1**（21 页）：用途本身只面向位图 → 把 `accept` 收窄为 `image/png,image/jpeg,image/webp,image/gif`（拒绝 SVG）即可根除污染；再给导出补 `try/catch`（异步回调内也要兜）+ `blob === null` 提示。
- **C2**（1 页）：`svg-to-png` 的业务就是吃任意 SVG → 不能靠收窄入口。必须：① 解析/过滤 `foreignObject` 与外链引用（或明确拒绝并提示）；② 把 `toDataURL` 的 try 下沉到 `img.onload` 回调内部。

---

## 五、修复批次建议（按成本升序，待构建窗口后执行）

1. **B-T0（2 页）**：`it/qrcode`、`library/generator-label` —— 已有 try/catch，仅补 catch 提示，改动最小。
2. **B-T1（32 页）**：补 `try/catch + ToolBox.showToast`；其中 `cvd-safe-palette`、`wechat-cover-maker`、`bigfive` 一并处理 `blob === null` 静默分支。按目录分批提交（`it/barcode-*` 7 页可合并为一个批次）。
3. **B-T2/T3（3 页）**：`favicon-generator`、`captcha-generator` 多点补齐；`gif-split` 把 Promise 包装补 reject / null 分支。
4. **C1（21 页）**：统一「收窄 `accept` + 导出兜底」；`design/image-*` 7 页与 `image/image-*` 10 页各成一批。
5. **C2（1 页）**：`design/svg-to-png` 最后做（要 sanitize + 回调内兜底 + 失败提示）。

> 全站无「改局部坐标 / 换 htmlLabels」类工作——这两类已在上一批的 `mindmap` / `flowchart` 收口；本批全是「补兜底」与「收窄输入」。

---

## 六、复扫方法

```bash
# 1) 候选页：内联 + 外置模块
grep -rlE "toBlob\(|toDataURL\(" tools --include='*.html' | sort
grep -rlE "toBlob\(|toDataURL\(" js/tools --include='*.js' | sort

# 2) 单页证据：调用点 ± 上下文、foreignObject / 外链 / accept
#    （上一批用 /tmp/canvas_scan.py 一次性产出 JSON，未入库；复扫时按本文"一、扫描口径"重写即可）
```

## 七、限制

- 本轮**未跑真机**：所有 B/C 结论均为代码级静态证据；`toBlob` 返回 `null`、Safari 面积上限、异步回调内的真实异常栈都要等窗口后补。
- 未覆盖 `js/tool-kit.js` 等共享组件内部的导出（本次 grep 无命中）。
- 台账按「页面」计数，同页多次调用在 B 表里合并到一行、次数在调用点列标出。

---

## 八、C 项收口（2026-11-05）

口径：C 档 22 页的入口已全部收窄为位图白名单（`accept` 不含 `image/svg+xml`），`SecurityError` 不可达；本轮只在不改动异步链/回调结构的前提下补 ≤3 行同步守卫，不做统一口径重构。

**已加同步守卫（9 页）**：`image/id-photo-crop`、`image/image-collage`、`image/image-crop`、`image/image-filter`、`image/image-mosaic`、`image/image-resize`、`image/image-rotate`、`image/image-watermark`、`image/image-converter`。
做法：`try { <canvas>.toBlob(...) } catch (e) { ToolBox.showToast('导出失败：' + ((e && (e.name || e.message)) || '未知错误'), 'error'); }`；`blob === null` 分支原本已有可见提示，未改。

**无需改动（2 页）**：`design/image-format-converter`（`toBlob` 已在同步 try/catch 内，`!blob` 有 toast）、`design/image-rounded-corners`（`toDataURL` 已在 try/catch 内）。

**暂不修（1 页）**：`image/image-compress` —— `toBlob` 位于 `new Promise` executor 内，同步异常按 Promise 语义 reject，调用侧 `.catch` 已落 `item.status='error'` + `renderResults()`（失败可见）；外提 try 需动异步链。入口已拒 SVG，`SecurityError` 不可达，暂不修。

> C 档守卫仅覆盖「浏览器画布上限 / 实现 bug」等非污染型同步异常，不作为上传口污染兜底；上传口污染由 C1 的 `__svgFileBlocked` 与 `design/svg-to-png` 的 sanitize 负责。

## 九、批次纪律（本条为事故复盘，后续批次沿用）

- **整文件 `git add` 之前必须先 `git diff <file>`**，确认没有不属于本批的行；跨线文件只提交自己的 hunk（`git diff` 过滤后 `git apply --cached`）。
- 事故样例：`78dd6e3b1b` 整文件入库 `tools/design/svg-to-png.html`，把工作区里内容批（`5189f87ac1` / `content_deepdive.json`）的旧 FAQ 文案一并提交，覆盖了 `0e45be8eca` 与 `#bgMode` 自洽的新措辞 → 「旧文案回写覆盖新修正」。源头修法归设计生活线，本线不再改该页与 `content_deepdive.json`。

## 十、B 档收口（2026-11-05，D1–D3 三批）

B 档 37 页按 10/10/7 三批修完，每批独立提交（`64a7a01844` B 前 9 页；`fee40918ae` D1；`78ece2caac` D2；`033b62b912` D3）。

- **统一口径**：`toDataURL` / `toBlob` 外层补同步 `try/catch` → `showToast('导出失败：…', 'error')` 并 `return`；`toBlob` 的 `!blob` / `Promise` 拒绝路径同样落可见失败文案；失败分支一律在成功提示之前返回，避免「失败被成功消息盖掉」。
- **顺带修复**：`design/qr-code-styled` 原调用不存在的 `QRCode.toCanvas`（本地 `js/qrcode.js` 导出的是 `qrcode` 工厂），页面恒显示「未加载」→ 改为 `qrcode(0, ec)` + 手绘模块；`design/colorblind-simulator` 失败 toast 被「已载入示例图」覆盖 → `renderImagePane()` 返回 `false` 时提前 return（B 前 9 页批）。
- **桩级失败注入**：设计 7 + 图像 2 + IT 8 + 数学 1 + 眼科 3 + 心理 2 条，全部在 `scripts/verify_*_calc.js`；模块型页面（`colorblind-simulator`、`bigfive`）仅真机验证。
- **真机失败注入**：三批共 28 次（含 `gif-split` 双路径），失败文案可见、0 pageerror；无注入负向对照全部干净。
- **真机观察（已收口，见第十一节）**：7 个条码页中 5 页首屏无任何空态提示，已补静态文案；未加自动生成。

## 十一、空态与局部失败口径（2026-11-05）

- **条码族首屏空态判定（7 页）**：`barcode-codabar` / `barcode-code128` 已有默认输入且加载即自动生成（首屏可见结果卡与条码）；其余 5 页（`barcode-code39` / `barcode-ean` / `barcode-itf` / `barcode-msi` / `barcode-upc`）虽有默认示例输入，但 `#output` 为空且命中 `.result-box:empty{display:none}` ⇒ **真缺提示 5 页**。修法：只在 `#output` 加一句静态文案 `点击生成按钮`（沿用 `design/aztec-code` 等页的既有空态写法，英文态经 `BODY_PHRASE_MAP` 自动译为 `Click the Generate button`），首次生成时被结果覆盖；**未加自动生成**，避免给用户展示一个他没有主动要求的条码。
- **局部失败只降级该部分，不中断整体**（以 `tools/image/gif-split.html` 为口径）：缩略图 `toDataURL` 失败只降级该缩略图并提示，帧渲染与整批导出继续；不得让 1% 的局部失败放大成 100% 的不可用。反面：把局部异常冒泡到外层批处理，导致一个缩略图失败 = 整批导出失败。

## 十二、空态文案 i18n 规范（2026-11-05）

> **能复用现有短语层（`BODY_PHRASE_MAP` / `<ind>-phrases.json` / `_common.json`）的空态文案，不得新增独立字典键。** 每新增一个键都是后续 i18n 死键债的入口（当前全站仍有约 8292 个待清死键）。本次 5 个条码页空态即复用既有短语 `点击生成按钮`（英文态由 `BODY_PHRASE_MAP` 自动译为 `Click the Generate button`），未新增任何键。
