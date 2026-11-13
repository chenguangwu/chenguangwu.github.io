# 第339批 · 设计 · checker 色值规范化 / toast 自定义背景色 / base64 核验销账

文件：`tools/design/checker.html`、`tools/design/toast-generator.html`、`scripts/verify_design_calc.js`；核验项 `tools/design/base64-to-image.html`（本批未改该页源码）。

## D-N156 checker 输入 rgb() 时预览文字色回退旧值（真修）

### 根因
`calc()` 用 `'#' + fgStr.replace('#','')` 拼预览色，只对 3/6 位十六进制成立；`parseColor()` 明确支持 `rgb(r,g,b)`，此时拼成 `#rgb(255,0,0)` 非法值，浏览器 CSSOM 丢弃该声明，预览保留上一次颜色，与算出的对比度不同步。背景色 `preview.style.background=bgStr` 同样未走解析路径。

### 改动
新增 `cssRgb(rgb)`（含空值容错）与 `toHex6(rgb)`；预览统一写 `cssRgb(fg)` / `cssRgb(bg)`。rgb()、3 位 hex、6 位 hex 三种输入在真机下均得到规范 `rgb(...)` 色值。

## D-N158 checker 交换/取色回填把 rgb() 塞进 color input（真修）

### 根因
`swapColors()` 直接把文本值赋给 `#fgPicker/#bgPicker`，而 `<input type=color>` 只接受 `#rrggbb`；rgb() 或 3 位 hex 被清成 `#000000`，随后 `syncColor()` 又把文本覆盖为 `#000000`，原颜色丢失。

### 改动
回填前统一 `toHex6(parseColor(v))`，仅当解析成功才写取色器；非法输入不再把非法串写回（避免真机置黑）。交换方向保持：前景取色器取原背景的规范化 hex，反之亦然；文本值原样交换。

## D-N128 toast-generator 任何「生成」都把自定义背景色改回预设（真修）

### 根因
`generate()` 中 `document.activeElement.id !== 'bgColor'` 即强制把背景改成类型预设并回写取色器。除切类型外，改文案、改圆角、点「生成」、点预设都会触发，自定义背景色被静默丢弃；公式框只声明「选中类型时」才这样做。

### 改动
- `generate()` 删掉 activeElement 覆盖块，背景色始终取用户当前值。
- 新增 `applyTypePreset()`：仅在 `#toastType` 的 `change` 事件里把该类型预设色写回取色器并重新生成；改用 `addEventListener('change', ...)` 绑定，移除 `<select>` 上的内联 `onchange`（遵守 verify 覆盖工具禁内联副作用属性的硬约束）。
- 切类型仍跟随预设、自定义后改圆角/再生成仍保留，语义与公式框一致；预设条注入的 `bgColor` 也真正生效。

## D-N140 / D-N141 base64-to-image 核验销账（历史已修，未改源码）

- `generate()` 空输入分支已 `lastURL=''`；成功/失败分支各自维护 `lastURL`；`downloadImg()` 用 `(mime.split('/')[1]||'png').replace('+xml','')` 处理 `svg+xml → svg`。JSDOM 实测：清空后下载被拦截、SVG 存 `.svg`、WEBP 存 `.webp`。
- 已有 `sniffMime()` 按 4 字节魔数识别 PNG/JPEG/GIF/WEBP/SVG，无法识别回退 PNG，正是 D-N141 方案；带 `data:` 前缀时按声明 MIME。JSDOM 实测 5 种魔数全部命中。
- FAQ（来自 `i18n/tools/content_deepdive.json:1575` 注入、另有英文映射 `i18n/tools/en/design/base64-to-image.json:18`）措辞「按 data URI 中的 MIME 识别」对带前缀情形成立，纯 Base64 由魔数补足，不构成过度承诺；本批**不改 JSON 源与英文映射**，避免为措辞微调引入 i18n 风险。
- 结论：两条核心断言均已失效，按「核验销账」处理，不重复造码。

## 验证

- **verify 强锁**：`scripts/verify_design_calc.js` 新增 4 条用例（checker `PREV339=rgb(204,0,17)`、`SWAP339=#0000ff|#ff0000`；toast `KEEP339=YES_OVER=NO`、`PRESET339=#ff9800`），均锚派生结果/探针，默认态不命中。全量 design calc **345/345** ✓（341 → 345）。
- **漂移同步（铁律）**：历史自动补强用例 `design/checker`（注入 `abc123测试`）的 expect 末两行由 `ABC123测试` 改为 `abc123测试`。根因是旧 `swapColors()` 会把非法串写回 color input 形成大写回显，修复后不再写回——旧源码差分已证明该漂移来自修复本身，非回归；更新后 expect 仍含注入串且默认态不命中，判别力保留。
- **旧源码差分**（项目铁律）：两页同时换回旧版 → **341/345**，恰好 4 条新增用例全红（`PREV339=#rgb(204,0,17)`、`SWAP339=rgb(...)|rgb(...)`、toast 两条探针不命中/ReferenceError）；恢复修好版 → **345/345**。差分用 `/tmp/checker_old_339.html`、`/tmp/toast_old_339.html`、`/tmp/checker_new339_faulttolerant.html`、`/tmp/toast_new_339.html` 备份恢复，未用 `git checkout --`。
- **JSDOM 真机** `/tmp/jsdom339.js` **31/31** ✓：checker rgb()/3 位 hex 预览规范、对比度 5.87:1 不变、交换后取色器与文本正确、非法输入不置黑；toast 初始化/自定义保留/改圆角/再生成/切类型套预设/二次自定义/无内联 onchange；base64 五类魔数、清空拦截、两种扩展名、FAQ 一致性。
- `check_inline_js_syntax.js` **12141/12141** ✓；`audit_verify_input_ids.js` 扫描 207 文件 / 10589 用例 / ① 僵尸 id **0** ✓；`_build.py` **EXIT=0**（A 级 4713/4714 = 100.0%），build 后 `cssRgb/toHex6/applyTypePreset` 与无内联 `onchange` 的 `<select id="toastType">` 均保留。
- `sitemap.xml` / `sitemap_lastmod.json` 为本批 build 正常产物，随批提交。

## 销账
`plan/categories/04-设计创意/design.md` 中 `### D-N128`、`### D-N140`、`### D-N141`、`### D-N156`、`### D-N158` 五段整段删除（95 → 90 条）。保留 `D-N129`（文案承诺位置/动画）、`D-N142`（WCAG 选字）、`D-N157`（18pt/14pt 标准口径，属需查权威源的口径类，本批不擅动）。

## 状态
本地提交（新一轮第 5 批，达到攒 5 批阈值）→ 跑全量门禁 → push → 单次确认 GitHub Actions 部署成功。
