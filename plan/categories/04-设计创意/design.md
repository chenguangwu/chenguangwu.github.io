# 设计创意 · tools/design（111 页）

## 2026-11-06 已修记录独立复核：像素绘制和涟漪

- **D-N92 / 台账 O-4：尚不能确认视觉效果，保留待复核。** 源码现为点击创建绝对定位色块并调用 Web Animations，浏览器确认预览元素已绑定 `onclick`；但点击后未捕获到色块或动画，浏览器自动化未能排除观察延迟或点击未触发。不能据此判定修复通过或复发。
  - 第323批补充：JSDOM 真机链路复核确认点击确实生成绝对定位带底色圆块并调用 Web Animations，源码层面「无样式、position:static」缺陷已不成立；视觉观感仍待真机浏览器确认，故条目保留、不销账。

## 2026-11-06 已修记录独立复核（设计）

- **D-N2：已于 2026-11-08 修复并移交 plan/已修复/2026-11-08-D-N2-配色生成器WCAG对比度.md。** 原 `renderPalette()` 用 YIQ 亮度阈值 (`>128` 选 `#333`/否则 `#fff`) 决定文字色，且虚标黑色对比度为按 `#000` 算的 5.32:1；修复后改为按 `#111` 真实相对亮度计算 WCAG 对比度（如 `#808080` 对 `#111`=4.78:1、对 `#fff`=3.95:1），按「白底/黑底」语义择高者并标注真实评级，图片导出同步修正；`node scripts/verify_design_calc.js` 该页 267/267 通过且无新增逃生项。此前的「仍待处理」结论以本次修复为准。
- 验证：`node scripts/verify_design_calc.js color-palette-generator typography-scale color-temperature-converter color-shade-generator` 为 16/16；该脚本使用 DOM 桩，且 expect 为命中任一输出的子串断言，不能替代真实浏览器或画布导出验证。对比度数值另以独立 WCAG 公式计算。

## 2026-11-06 交互复核：相纸方向不匹配导致错误降级（中，确认）

- 基线 `0781ef7e61`；独立 Chrome 在 `tools/design/photo-print-size.html` 选择 300 DPI，输入 1800×1300 后 6寸 (4R) 显示“基本可用”；交换为 1300×1800 即显示“像素充足”。相纸需要 1205×1796 像素，将横图旋转后两边均满足，二者应得到相同的像素判定。
- 第 284–290 行固定将照片宽对相纸窄边、高对长边，没有测试旋转方向。页面和导出的充足判定应同时考虑宽高交换；这与本文件已记载的预设一像素误差和 CSV 恒“是”问题不同。

## 已知问题
## 功能缺陷
- 颜色工具缺「对比度检查 + 色盲模拟 + 十六进制锁」三合一（WCAG 2.2 达标标注）。
- shadow-generator 预设过少（S2 补 Material/Neumorphism/Glassmorphism 风格预设）。
- 无「字体 pairing 速查」动态预览（静态页有，交互弱）。

## 优化点
- S6 输入智能化标杆页：色值框支持 css color 全语法（rgb()/hsl()/named）。
- S4 分享卡：配色结果卡（设计师转发意愿高）。

## 受影响范围
- tools/design/（111 页）

## 进度
- 🟢 批次 04-b1（2026-10-26 · S2 风格预设首批）：`css-box-shadow-generator`（shadow-generator）+10 个设计系统风格预设（Material elevation-1/4、Neumorphism 亮/暗、Glassmorphism+ 描边、Brutalism 硬阴影、Tailwind sm/md/lg/xl 四档）+ 预设标签 EN（en 字段 + __isEn 渲染，存量 presetGrid 中文标签泄漏顺带治理）。verify +3 clicks 直调 applyPreset 用例（Neu 亮/Brutal/TW xl 整串锚，index 依赖 PRESETS 追加序）→ design 185→188、判别器 0、门禁 218/218。
- 🔴 待开发

## 2026-11-03 审计补充

### 设计像素尺寸非法时静默改为 1（中，确认缺陷）
- 问题：清空、零或负数尺寸后页面仍给出 1 像素参与计算的比例和打印尺寸，而输入框未同步改值或显示错误。
- 证据：`tools/design/photo-aspect-ratio-calculator.html:162-163,264-289`：两输入 `oninput=calc()`，函数用 `+value||1` 并对小于 1 的值强制设 1，直接生成结果。浏览器行为未实测。
- 影响：`tools/design/photo-aspect-ratio-calculator.html`，结果可能被误用。
- 方案：空值与非正整数显式提示并清除结果；验证常用尺寸一键切换、复制导出与移动端布局。

### 留存优化：基于用途生成裁切建议（低，建议）
- 证据：同页 `:259-261,273-288` 已展示比例卡、预览和固定 300 DPI 打印尺寸。
- 影响：同页；方案：补可选 DPI 与按平台比例的居中裁切尺寸、损失像素说明，保留一键套用。

### 设计工具进一步抽样（2026-11-03）

#### 换图后仍可下载上一次缩放结果（高，确认源码缺陷）
- 问题与证据：`tools/design/image-resizer.html:259-274,288-307` 上传 A 并缩放后，上传 B 仅更换原图和预览，未清除 lastURL；未重新缩放就下载或复制会取得 A 的结果。浏览器交互未实测。
- 影响：`tools/design/image-resizer.html`，可能误交付旧图。
- 方案：换图或修改参数时使旧结果失效，禁用输出直至重新生成并提示状态。

#### DPI 历史恢复遗漏单位及零值静默代入（中，确认函数缺陷，两个问题）
- 问题与证据：`tools/design/image-dpi-converter.html:409-420,441-470,535-540,577-595` 保存历史含单位，恢复只设置数值不恢复 currentUnit；内存执行英寸 10×15、300 DPI 的记录在当前单位为厘米时恢复成 1181×1772，而英寸应为 3000×4500。空或零 DPI 则由 `||72` 代入，输入框不更新。
- 影响：`tools/design/image-dpi-converter.html`，历史结果或打印尺寸可能不符。
- 方案：恢复单位及按钮状态；对空值与非正 DPI 明确提示并清除结果，历史保存使用同样校验。

#### 照片打印 CSV 总标记为可打印（高，确认函数缺陷）
- 问题与证据：`tools/design/photo-print-size.html:264-285,296-317` 页面根据分辨率生成充足、基本可用、不足三档，导出虽计算 ok 却恒写“是”；内存执行一寸 295×413、300 DPI 时 A4 页面为不足、CSV 为是。
- 影响：`tools/design/photo-print-size.html`，使用者依导出清单可能误判质量。
- 方案：导出与页面共享同一状态逻辑并保留三档；增加逐行一致性回归。可附裁切比例、预计有效 DPI 和横竖方向，辅助打印决策。

#### SVG 压缩破坏文本空白或内部声明（高，确认函数缺陷）
- 问题与证据：`tools/design/svg-minifier.html:254-275` 对整串全局折叠空白，使 `<text xml:space="preserve">A  B</text>` 变成单空格；DOCTYPE 正则遇内部实体声明首个 `>` 提前终止，可能遗留无效片段和实体引用。已对页面原函数内存执行，未作浏览器 XML 解析测试。
- 影响：`tools/design/svg-minifier.html`，导出 SVG 显示变化或损坏。
- 方案：采用理解 XML 结构的保守压缩，保留有语义空白；不支持内部 DTD 时明确拒绝而非输出损坏结果。可加入前后对照及解析失败提示。

### 覆盖
- 本轮共核查 5 页：`tools/design/photo-aspect-ratio-calculator.html`、`tools/design/image-resizer.html`、`tools/design/image-dpi-converter.html`、`tools/design/photo-print-size.html`、`tools/design/svg-minifier.html`；本次新增 5 个缺陷、2 条嵌入式针对性建议。其他设计页及真实浏览器、移动端、线上状态未逐一验证。

## 2026-11-03 续查：对比度、配色与字体预览

### 留存优化（按页落点，非确认缺陷）
- `tools/design/contrast-checker.html`：缺「一键调到 AA/AAA 达标」——用户测出 3.9:1 后只能自己反复微调。建议给出最接近的达标前景/背景色候选（保持色相，只调亮度）、可对比并保存的历史色对，这是此类工具的主要留存点。
- `tools/design/color-palette-generator.html`：色板只有 CSS 变量文本，无常驻「锁定色 + 再生成」与多格式导出（JSON/SVG/PNG）。建议加锁色、色板命名与导出，避免每次重新生成整组。
- `tools/design/font-preview.html`：输入框只支持单行固定字号，缺少字号阶梯与真实段落排版预览；建议加 12/16/24/32 阶梯同时预览与行高对比，贴近实际选字场景。

### 续查覆盖
- 新抽查 `tools/design/contrast-checker.html`、`tools/design/color-palette-generator.html`、`tools/design/font-preview.html` 共 3 页，新增 5 条（0 条高优）与 3 条留存建议；为源码静态核查，未做浏览器、EN 运行态探针、移动端或门禁验证。

## 2026-11-03 续查（并行批 G）

### 留存优化
- `tools/design/depth-of-field-calculator.html`：补「套用超焦距」按钮（把对焦距离一键设为 h 并展示「近点 X 米 ~ ∞」），并画出近/远点与超焦距的相对位置；景深条目前已存在，只差数据闭环。
- `tools/design/focal-length-equivalent.html`：画幅对比行文案改为「全画幅 50mm 视角 ≈ 该画幅 31mm」，并删除未使用的 `eqFocal`；提供两画幅并排取景框预览，比单行数字更易选镜头。
- `tools/design/photo-storage-calculator.html`：补 3-2-1 备份冗余（所需总容量/卡数）与「剩余容量还能拍多少张」，贴近真实备卡场景。
- `tools/design/image-rotator.html`：增加透明/纯色背景选择、任意角度自动裁去白边、批量 90°/180°/270° 对勾选项，减少重复上传。
- `tools/design/qr-code-styled.html`：下载前展示「当前内容 + 纠错级别 + 模块数」确认条，并补 SVG 导出（印刷放大不糊）。
- `tools/design/spacing-scale.html`：允许自定义 token 前缀（`--space` / `--gap`）与导出 JSON（Tailwind/Theme UI 可直接消费），提升在设计系统里的复用率。

### 续查覆盖
- 本轮抽查 7 页：`tools/design/depth-of-field-calculator.html`、`tools/design/focal-length-equivalent.html`、`tools/design/photo-storage-calculator.html`、`tools/design/spacing-scale.html`、`tools/design/image-rotator.html`、`tools/design/qr-code-styled.html`、`tools/design/px-to-rem.html`；另对 `tools/design/rem-to-px.html` 做同构源码对照（未单独列条）。
- 新增 9 条（D-N6–D-N14，其中高优 2 条）与 6 条留存建议。证据均为源码行号 + node 内存复算或源码路径推演；未做浏览器交互、EN 运行态探针、移动端与门禁验证，涉及 Canvas/二维码回调的条目为静态确认而非运行态实测。

## 2026-11-03 续查（并行批 J）

### 留存优化
- `tools/design/breakpoint-queries.html`：断点值目前不可编辑（三档均为固定常量），建议开放自定义断点输入并回写预设，附 Tailwind/Bootstrap 对照表与「复制 CSS」按钮；另把 `vw/vh` 引据行与实际输出打通，避免引据表与产物无关。
- `tools/design/typography-scale.html`：补行高阶梯（字号 × 1.2/1.5/1.6）、真实段落排版预览与 token 命名（`--text-1…n`），并导出 JSON/Tailwind 配置；当前 deep-dive 的「6 档 / --text-1…6」与实际 7 档 `--h6-size…--display-size` 不符，可一并校正。
- `tools/design/color-temperature-converter.html`：增加「当前白平衡偏移」预览（同一色卡在 3200K/5600K 下的对比）与常见光源色卡并列，比单色块更适合摄影布光；反向换算补残差提示。
- `tools/design/png-to-svg.html`：输出没有下载按钮，且同色相邻格未合并，rect 数极易膨胀；建议合并同色矩形/颜色量化、显示 rect 数与文件体积、提供 SVG 下载。
- `tools/design/svg-to-png.html`：补「透明/底色」选择与 1x/2x/3x 倍率（与当前尺寸输入联动），并在说明中区分像素尺寸与 DPI 标签，减少印刷场景误解。
- `tools/design/image-flipper.html`：补水平/垂直/180° 批量勾选与任意角度旋转、透明通道保留提示，以及原图/结果并排对比，减少重复上传。
- `tools/design/image-rounded-corners.html`：增加导出格式（PNG/WebP/SVG 圆角蒙版）、常用圆角预设（8/12/16/24）与「背景是否填满角外」开关；现有圆角规范速查表可与预设联动。

### 续查覆盖
- 本轮新抽查 7 页：`tools/design/breakpoint-queries.html`、`tools/design/typography-scale.html`、`tools/design/color-temperature-converter.html`、`tools/design/png-to-svg.html`、`tools/design/svg-to-png.html`、`tools/design/image-flipper.html`、`tools/design/image-rounded-corners.html`。
- 新增 11 条（D-N15–D-N25，其中高优 1 条：D-N22）与 7 条留存建议。证据均为源码行号 + node 内存复算或源码路径推演；未做浏览器交互、EN 运行态探针、移动端、门禁或线上验证，涉及 Canvas 绘制/图片回调的条目中，D-N23 为静态时序推演（待验证），D-N24 为源码路径确认，均未做 Canvas 运行态实测。

## 2026-11-03 续查（并行批 K）

> 本轮实读 8 页：`color-picker.html`、`color-palette.html`、`color-shade-generator.html`、`vh-vw.html`、`css-grid-generator.html`、`image-cropper.html`、`image-format-converter.html`、`favicon-generator.html`。仅源码静态阅读 + node 内存复算（临时脚本 `/private/tmp/k_audit.js`，已删除），未开浏览器、未做 EN/移动端/门禁/线上验证。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页：`tools/design/button-generator.html`、`tools/design/text-shadow-generator.html`、`tools/design/css-animation-generator.html`、`tools/design/skeleton-loader.html`、`tools/design/palette-extractor.html`、`tools/design/image-to-ascii.html`、`tools/design/mesh-gradient.html`、`tools/design/pattern-generator.html`。仅源码 + node 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

## 2026-11-04 续查（并行批 O）

- 范围：`tools/design` 剩余生成器/互动演示 8 页（Favicon 文字、Favicon Emoji、首字母头像、Identicon、Loading Dots、Ripple、像素画、棋盘），逐页通读整份 HTML（内联 JS/CSS 生成逻辑、deep-dive、FAQ），编号续 D-N75。

### D-N92 ripple-effect 点击预览涟漪的视觉效果待真机确认（高，源码缺陷已于第323批复核不成立；台账 O-4 保留待复核）

- 第323批源码 + JSDOM 复核：点击处理已用内联 `position:absolute / border-radius:50% / background:rgba(...)` 创建 span，并调用 Web Animations（`ripple.animate`）驱动 `scale(0)→scale(4)`、`opacity 1→0`，`dur*1000` 后移除；旧缺陷「`className='ripple'` 无样式、`position:static` 挤开文字」在源码中已不成立。
- 证据：`/tmp/jsdom323.js` 修好版与旧码对照的「点击生成可见圆」项均为 PASS（span 存在、position=absolute、borderRadius=50%、background 非空）；本批设计门禁 330/330。
- 保留原因：台账 O-4 记录浏览器自动化未捕获到色块或动画，本批未新增真机浏览器视觉复核。按「不可自判收口」原则，视觉效果仍待真机确认，本条不销账。

### 留存/优势建议（逐页，具体可落地）

- `favicon-from-text`：① 一次导出 16/32/48/180/512 多尺寸 PNG + `.ico` 打包；② 增加透明底/纯色底切换与 `<link rel="icon">` 代码复制；③ 字间距/字体预设，避免用户为大圆角反复试错。
- `favicon-from-emoji`：① 内置「Apple/Noto/Twemoji」字体切换或上传 emoji SVG，解决跨平台渲染差异；② 多尺寸导出 + 透明底；③ 一键复制 HTML `<link rel="icon">`，保留「离线可用、数据不上传」卖点。
- `initials-avatar`：① 自动对比字色（按底色亮度选黑/白）替代固定白字；② 形状预设（圆形/圆角/方形）+ SVG 导出；③ 批量输入（每行一个姓名）一次生成多张并打包下载。
- `identicon-generator`：① 批量种子（CSV/多行文本）一次生成整组头像；② 算法风格切换（GitHub 5×5 / Gravatar / 对称 7×7）；③ 画廊随当前 `blocks/bg` 实时重绘，并支持复制 Data URL。
- `loading-dots`：① 「复制 HTML+CSS」一次给全可用片段；② 预设「三点弹跳 / 声波 / 打字机」；③ 提供停顿与总时长调节，并导出 SVG SMIL 版本。
- `ripple-effect`：① 导出 CSS + 完整 JS（事件委托创建涟漪）；② 支持触摸/键盘触发；③ 透明度、半径倍数、扩散曲线下拉可调，修好预览后再强调「所见即所得」。
- `pixel-art-generator`：① 导出 PNG/SVG + 复制字符画；② 撤销/重做与 localStorage 草稿（离线可用）；③ 补齐文案承诺的「导入图片量化」（纯前端 Canvas 可实现）。
- `checkerboard-generator`：① 导出无缝 tile PNG/SVG；② 棋盘格数（8×8/9×9/10×10）与方向选择；③ 相邻色对比度过低时提示，并真正支持透明底预设。

### 覆盖小结（2026-11-04 并行批 O）

- 本轮实读 8 页（整份 HTML：内联 JS/CSS 生成逻辑、deep-dive、FAQ 全读）。
- 新增 27 条：高 2（D-N92、D-N96）/ 中 20 / 低 5。
- 高优均给出可复现输入：D-N92 点击预览无涟漪（旧实现 `.ripple` 无样式，第323批源码复核已不成立、视觉待真机）；D-N96 8×8 点击命中错位（匹配 65 个元素，`idx` 整体偏移 1）。
- 同族合并：D-N77 = favicon 两页历史恢复下载，已于第321批修复；D-N83 已于第323批核验为过期条目销账、D-N84 已于第323批修复（均为 initials 独有）；D-N86/D-N89 结果区无文本致历史/CSV 恒空，已于第319批修复（与 D-N59 同族，该条已于第320批修复）；D-N91/D-N99 已于第317批修复。
- 未覆盖：`tools/design` 其余约 44 页（本文件累计覆盖 64/108）。
- 未做：浏览器交互、EN 运行态探针、移动端、门禁与线上验证；D-N96 的 DOM 命中顺序按标准文档序推演，未开浏览器。

## 2026-11-04 续查（并行批 P）

- 范围：`tools/design/` 8 页（`colorblind-simulator` / `cvd-safe-palette` / `palette-cvd-checker` / `exposure-triangle-calculator` / `shutter-speed-calculator` / `flexbox-generator` / `gradient-from-color` / `toast-generator`），整份 HTML（含内联 JS、外链 `js/tools/colorblind-simulator.js`、deep-dive、FAQ、引据表）全读。
- 方法：静态源码审计 + `node` 复算；未开浏览器、未跑构建与门禁、未做 EN 运行态探针与移动端验证，行号按当前磁盘版本。

### 留存/优势建议（逐页，具体可落地）

- `colorblind-simulator`：① 图片模式支持拖拽/粘贴与「仅导出当前类型」；② 矩阵旁给「一键把最差一对拉开明度」；③ 记住上次类型/严重度并同步到图片与调色板两个页签。
- `cvd-safe-palette`：① 结果给「复制全部 HEX / CSS 变量 / JSON」；② 锁定色支持 EyeDropper 屏幕取色（Chrome）；③ 生成时显示耗时与「取消」，候选 3600×贪心较重。
- `palette-cvd-checker`：① 修正建议给「前后 ΔE 对比」与可撤销预览；② 3 色以内提示用形状/纹理辅助编码；③ 支持粘贴设计 token JSON 批量检查。
- `exposure-triangle-calculator`：① 结果区显示绝对 EV 与噪点提示；② 支持 1/3 档微调（光圈/快门/ISO）；③ 记住机身裁切系数。
- `shutter-speed-calculator`：① 结果旁给「当前场景推荐」对照（运动/人像/风光）；② 支持高像素密度（1/(焦距×2)）与输出尺寸的安全快门；③ 一键复制「建议参数」。
- `flexbox-generator`：① 补「复制 CSS / HTML」按钮；② 控件改动即预览（实时）；③ 支持自定义项目数量与内容。
- `gradient-from-color`：① 导出 CSS 变量与 Tailwind 配置；② 多色标 + 角度滑杆；③ 基色锚定到渐变端点（配合 D-N126）。
- `toast-generator`：① 补位置/动画控件并输出含 auto-dismiss JS 的完整片段；② dark/light 两套预设；③ 一次复制 HTML+CSS。

### 覆盖小结（2026-11-04 并行批 P）

- 本轮实读 8 页（整份 HTML：内联 JS、`js/tools/colorblind-simulator.js`、deep-dive、FAQ、引据表全读）。
- 新增 29 条：高 3（D-N106、D-N112、D-N115）/ 中 18 / 低 8。
- 高优均可复现：D-N106 发散亮度 L=0.90/0.32/0.90（node）；D-N112 「#FFFF33 vs #FFFFFF」ΔE00=29.8 却被记 `oklch=1.1`（node）；D-N115 ISO 6400 + 1/60 的「等效卡」实际 EV 差 +1.06 / +2.06 档（node）。
- 同族合并：转义标签文本只记 D-N122（另 4 页同行号已在条目列出）；结果区无文本致历史/CSV 恒空记 D-N124（第318批已修，与 D-N59/N89/N91/N99 同族；N89 已于第319批修复、D-N59 已于第320批修复）。
- 未覆盖：`tools/design` 其余约 36 页（本文件累计覆盖 72/108）。
- 未做：浏览器交互、EN 运行态探针、移动端、`run_gates.py` 与线上验证；D-N112/D-N115/D-N106 的数值均为 `node` 按页面同款公式复算，未在页面内实测。

## 2026-11-04 续查（并行批 Q：8 个设计页功能 / 渲染 / 文案）

- 范围：`tools/design/` 8 页（`waveform-visualizer` / `tailwind-colors` / `base64-to-image` / `data-matrix` / `spectrum-visualizer` / `pixel-art` / `colorblind-simulator` / `signature-pad`），整份 HTML（含内联 JS/CSS、外链 `js/tools/colorblind-simulator.js`、deep-dive、FAQ、引据表）全读。
- 方法：只读源码 + `node` 内存复算（Tailwind 242 色 WCAG、CSS 拉伸后的圆环比例、Base64 扩展名正则、Data Matrix 图案）；未改代码、未跑 `_build.py`/门禁/浏览器、未做英文态与移动端实测，行号按当前磁盘版本。

### 承诺 vs 实际（Q 批专项）

| 页面 | 宣称（行号） | 实际 |
|---|---|---|
| waveform-visualizer | 上传文件、实时渲染、缩放、取峰值（`:10`、`:155`、`:207`、`:509`） | 无 file/AudioContext，纯解析式数学波形（`:282-295`） |
| spectrum-visualizer | Web Audio + AnalyserNode FFT、峰值、麦克风（`:10`、`:155`、`:205`、`:208`） | 纯 sin 动画（`:258-305`）；`microphone=()` 显式禁用麦克风（`:71`） |
| base64-to-image | 「也支持反向转换 / encode an image to Base64」（`:10`、`:15`、`:64`、`:160`）；「识别格式」（`:199`、`:202`） | 无上传/FileReader/btoa；无魔数/MIME 识别（`:256-258`） |
| data-matrix | Reed-Solomon 纠错（`:155`、`:230`）、扫码得原文（`:201`）、可直接使用（`:205`） | 哈希+LCG 随机格，无编码/无纠错；finder 方向与 ISO 相反（`:276-281`） |
| signature-pad | 导出 PNG 透明背景（`:10`） | 仅背景选「透明」时成立；白/网格背景被烘焙进导出（`:465-480`、`:532-537`） |
| pixel-art | 一键生成/复制 CSS 代码（`:719`、`:724`） | 无 clipboard/CSS，仅 PNG 导出（`:628`、`:203-204`） |
| tailwind-colors | 22 色 × 11 阶、点击复制多种格式（`:10`） | 数据与复制均真实；但「建议文字色」阈值错误（D-N142），CSS 变量名错误（D-N144） |
| colorblind-simulator | 8 型、图片变换、WCAG、ΔE（`:16`） | 均真实；局部语义问题见 D-N151/D-N152/D-N153 |

- 未发现「批量处理」「限时」「自动识别并修复」类承诺；`SVG 导出` 在本批 8 页中也无虚假承诺（pixel-art 只承诺 PNG，meta 属实）。
- 「复制 Base64」在 waveform/spectrum/data-matrix 三页复制的是完整 `data:image/png;base64,…` Data URL（含前缀），并非纯 Base64 字符串（`:320-323`、`:337-340`、`:303-305`）；可粘贴使用，但与按钮字面略有出入。
- 所有复制按钮（waveform/spectrum/data-matrix/tailwind/base64）均未处理 `navigator.clipboard` 失败（无 `.catch`/降级），在 http、权限拒绝或旧浏览器下会静默无反馈；与 D-N127 同族，属低危共通项。

### 留存建议（逐页）

**留存建议（tools/design/waveform-visualizer.html）**：整改保留。功能本身是有用的参数化波形演示，但必须先把 meta/简介/FAQ 从「上传音频/缩放」改为「参数化波形」，并做 `ResizeObserver + DPR` 自适应；若要保住「音频波形」SEO 定位，再接 `decodeAudioData`（纯前端，工作量中等）。

**留存建议（tools/design/spectrum-visualizer.html）**：整改保留。视觉动画质量尚可，但当前以「Web Audio/FFT/麦克风」获客属误导，且 `microphone=()` 与 FAQ 直接冲突；建议改为「模拟频谱动画生成器」文案，或接入 `AnalyserNode` 后移除麦克风禁用。另需修复圆环的 CSS 拉伸。

**留存建议（tools/design/data-matrix.html）**：必须整改后再保留（否则建议下架）。作为「Data Matrix 生成器」它不可扫码、不可纠错，工业标识场景会被误用；最小方案是改名为「矩阵纹理生成器」并删除扫码/ISO 承诺，正解是接入 ECC200 编码库并锁定版本。

**留存建议（tools/design/base64-to-image.html）**：整改保留。解码+下载主路径可用，需删「反向转换」或补上传编码（实现简单）；同时修 `lastURL` 清空与 SVG 扩展名，并把套话 formula-desc 换成真实解码流程。

**留存建议（tools/design/tailwind-colors.html）**：保留（本批价值最高的速查页之一）。色板数据与官方 v3 值一致，只需把黑白字阈值改为对比度取优、色块改按钮化、CSS 变量名改为 `--color-*`；改动集中在 `:365-366`、`:366`、`:447`。

**留存建议（tools/design/pixel-art.html）**：保留。绘制/撤销/PNG 导出链路真实可用，导出透明且倍率可控；需修模板 history 语义、清理简介 CSS 套话、补 `touchcancel`。可再补「复制像素数据/PNG Data URL」提升复用。

**留存建议（tools/design/signature-pad.html）**：整改保留（高价值）。当前笔宽滑杆失效必须优先修；透明导出改为按笔画层重绘；把 `#spPresets` 与 `#spRefTbl` 移出 `touch-action:none` 的 `.canvas-wrap`。引据表还应把「Pointer Events」改成实际使用的 mouse/touch 事件（`:280-282` 对照 `:550-557`）。

**留存建议（tools/design/colorblind-simulator.html）**：保留（本批功能最完整的页面）。建议按类型保存严重度、补真正的色相均分评分、去掉伪 AAA 列；D-N102/D-N103/D-N104 已于第317批修复，D-N105 待处理。

### 覆盖

- 实读：8/8 页整份 HTML（含内联脚本、deep-dive、FAQ、引据表），外加 `js/tools/colorblind-simulator.js` 全量（约 1100 行）。
- 新增 25 条：高 4（D-N131、D-N134、D-N137、D-N148）/ 中 14 / 低 7，编号连续 D-N131–D-N155。
- 未覆盖：`tools/design/` 其余工具页；colorblind 的 D-N102–D-N105 已存在，本批只补新角度（严重度语义、hue 策略、AAA/监听/文件名），不重复旧条；其中 D-N102/D-N103/D-N104 已于第317批修复。
- 未做：浏览器真实渲染与交互、`?lang=en-US` 运行态探针、移动端真机、`_build.py`/`run_gates.py` 门禁与线上验证；未改任何源码、未做 git 写操作。
- 复算说明：Tailwind 242 色对比度、频谱 CSS 拉伸后的圆环尺寸、Base64 扩展名正则、Data Matrix 图案与定位边方向均由 `node` 内存复算，未在页面内实测。

### 承诺 vs 实际（R 批专项）

| 页面 | 宣称（行号） | 实际 |
|---|---|---|
| stripe-pattern | 可导出图片 / 纯前端导出图片（`:10`、`:154`、`:156`） | 只有 CSS 文本与复制，无 canvas/png/SVG/download（`:177-178`、`:259-284`） |
| dot-pattern | 导出透明或纯色图片、SVG pattern / 矢量输出（`:10`、`:156`、`:229-230`、`:238-240`） | 只有 CSS；实际为 `radial-gradient`，无图片/SVG 导出（`:175-176`、`:257-273`） |
| generator-6 | 拖动控件调整 offset/blur/spread/color、支持内阴影与多层（`:10`、`:113-116`） | 仅 1 个「生成数量」输入，所有参数随机（`:120`、`:219-243`） |
| aztec-code | 移动端识读、票据物流、可扫描、扫码即得原文、超容量不生成（`:10`、`:196`、`:199`、`:203`） | 哈希+LCG 随机格，无编码/纠错/版本；尺寸与文本长度无关（`:259-292`、`:256-258`） |
| checker | 大号文字 ≥18px / ≥14px 粗体（`:230`）；WCAG 2.1（`:123`、`:229`） | WCAG 为 18pt/14pt（24px/18.66px）；引据表又写 2.2（`:210`、`:215`、`:220`） |
| analysis-64 | 优先补强取「负贡献且权重最高」（`:123`）、优势 TOP2（`:297`） | 优势不过滤正值（全落后仍列负贡献）；need 按最负排序（`:276-284`） |
| css-border-radius | 可视化调节、实时生成、支持百分比（`:10`） | >100px 被隐藏滑杆 max=100 截断，预览/代码滞后于滑杆（`:213`、`:227`、`:418-426`） |
| tester-assessor | 满意度 1–7 分（`:151`）、SUS 第4/10题子量表（`:335`） | 输入 8 可得 satScore 116.7（`:242`、`:262`）；子量表实际用第 5 题（`:335`）；标题/描述截断（`:10-11`） |

- 未发现「批量处理」「限时」「自动识别」类承诺；本批 8 页的复制按钮同样未处理 `navigator.clipboard` 失败（无 `.catch`/降级），与 D-N127 同族，属低危共通项。

**留存建议（tools/design/checker.html）**：保留。对比度公式与判定主体正确，改两处即可：预览色改用解析后的 rgb、把大字号阈值改成 pt/24px；顺带把 rgb() 输入的取色器回填统一为 #rrggbb。

**留存建议（tools/design/analysis-64.html）**：整改保留。加权计算本身可用，但「优势维度」必须过滤正值，简介块补齐 `<ul>` 与两个 h4，并统一 need 排序口径；权重敏感性文案按当前 bias 动态生成。

**留存建议（tools/design/stripe-pattern.html）**：整改保留。CSS 条纹生成准确且轻量，但「导出图片」是 meta 主卖点，最小改动是补 PNG/SVG 下载；同时修 ResText（改读 cssOutput.value）与双线型窄宽几何。

**留存建议（tools/design/dot-pattern.html）**：整改保留。图案预览可用，但需补透明 PNG/SVG 导出；引据表从 SVG 改为 CSS radial-gradient（或真的用 SVG 实现），并把「渐变大小」改名为「柔边圆点」。

**留存建议（tools/design/generator-6.html）**：必须整改后再保留（否则建议下架/改名）。当前只是随机阴影批量生成器，与「可视化调整」严重不符；正解是补 offset/blur/spread/color/inset 控件与层级预设，最低成本是改名「随机盒子阴影生成器」并重写 meta/简介。

**留存建议（tools/design/css-border-radius.html）**：保留（本批交互最完整的页面）。核心可用，需统一简单/进阶滑杆上限为 150、修未联动时的死滑杆、ResText 改读 textarea.value，并给预设条补宿主 div。

**留存建议（tools/design/tester-assessor.html）**：整改保留。SUS 与任务绩效模型有价值，修 Q4/Q10 子量表、历史 12 键截断、标题/描述残句后即可用；满意度需夹取到 1–7。

**留存建议（tools/design/aztec-code.html）**：必须整改后再保留（否则建议改名下架）。作为「Aztec 码」它不可扫描、无纠错、容量与版本均假；正解是接 Aztec 编码库，最小方案是改名「随机矩阵纹理生成器」并删除识读/容量承诺。

### 覆盖

- 实读 8/8 页整份 HTML（checker 538 / analysis-64 507 / stripe-pattern 513 / dot-pattern 507 / generator-6 459 / css-border-radius 806 / tester-assessor 603 / aztec-code 545，合计 4478 行），含内联脚本、deep-dive、FAQ、引据表与 `js/tool-kit.js` 预设宿主逻辑（`:1013-1039`）。
- 新增 24 条，编号连续 D-N156–D-N179：高 5（D-N162、D-N165、D-N168、D-N171、D-N177）/ 中 15 / 低 4（D-N158、D-N161、D-N164、D-N170）。
- 复算说明：对比度（`#767676/#FFFFFF=4.54`、`#FF0000/#FFFFFF=4.00`）、analysis-64 全落后场景（−44.4%，贡献 `-6,-6,-8,-10,-10`）、条纹双线型 w=2/w=5 停点顺序，均由 `node` 内存复算。
- 未覆盖：`tools/design/` 其余页面；未做浏览器渲染/交互、`?lang=en-US` 探针、移动端真机、`_build.py`/门禁与线上验证；未改任何源码、未做 git 写操作。

---

## S 批（2026-11-04，8 页）

### 承诺 vs 实际（S 批专项）

| 页面 | 宣称（行号） | 实际 |
|---|---|---|
| detector-28 | 按 GB 18580-2017 判 E0/E1/E2，并给出「与限值的差距」（`:10`、`:115`） | 引据表 E1≤0.124（`:187`）与代码 E1≤0.050（`:226`）冲突；结果只有限值标签、无差距 |
| detector-29 | A/AA/AAA 三级自动判定 + 14 项清单（`:10`、`:198-211`、`:508`） | 清单无任何 AAA 项，AAA 不可达、行恒「可选」（`:334`、`:396`） |
| generator-11 | 调节参数生成纹理、实时预览并导出代码（`:10`、`:116`） | 仅「生成数量」1 个输入，图案/颜色/尺寸全随机（`:120`、`:218-221`） |
| isometric-grid | 可调格子与配色、纯前端导出图片（`:10`、`:157`、`:159`） | 只有 CSS 文本 + CSV，无 canvas/PNG/SVG/下载；FAQ 称 Canvas 处理大图（`:206`） |
| generator-10 | 可视化编排、调整时长/缓动/属性并实时预览（`:10`、`:116`、`:119`） | 仅数量输入，结果只有代码文本，页面无预览元素（`:123-125`、`:234-243`） |
| music-scale-reference | 查阅调式音名与升降记号、对照和弦构成（`:10`、`:14`） | 只用升号拼写，F 大调出 A#（`:248`、`:265`）；无和弦计算（`:229-230`）；简介称「一键生成 CSS 代码」（`:367`、`:372`、`:379`） |
| generator-7 | 可视化设置宽度/样式/圆角/配色，支持单边独立设置（`:10`、`:113`、`:116`） | 仅数量输入，参数全随机，无单边控件（`:120`、`:219-222`） |

- 未发现本批页面有「批量处理」「AI 识别」「云端同步」类承诺；但 4 个模板页（generator-7/10/11、isometric-grid）共用同一套「可视化操作、所见即所得 / 一键生成 CSS 代码」简介套话（如 `generator-11.html:113`、`isometric-grid.html:157`），与本工具实际能力普遍不符，属 D-N154 同族，建议统一按能力重写而非逐页打补丁。
- 本批复制/导出按钮同样未处理 `navigator.clipboard` 失败（无 `.catch`/降级），与 D-N127 同族，仍列为低危共通项，不单列编号。

**留存建议（tools/design/checker-5.html）**：整改保留。选题（格律平仄自查）稀缺、交互闭环完整，但字库是唯一价值来源且当前示例即错；必须先做「单字→平/仄/两读」映射并移除两库交叉收录，再替换 deep-dive 串页文案，否则建议先降级为「字库演示」并去掉「格律校验」表述。

**留存建议（tools/design/detector-28.html）**：整改保留。判定流程与预设完整，但限值文案必须收敛为单一常量表（涂料 30/80、苯系物 10/50），板材改为只判 E1≤0.124 或明确引用 GB/T 39600 的 E0/ENF；`refBar` 按材料切换并禁止空值判优。

**留存建议（tools/design/detector-29.html）**：整改保留。对比度计算（WCAG 亮度公式）正确，清单+等级的产品形态可用；需删 AAA 死逻辑或补 AAA 项、修预览文案不恢复、统一顶部等级与表格判定谓词。

**留存建议（tools/design/generator-11.html）**：必须整改后再保留。当前是「随机纹理样例器」，与 meta 的「调节参数」不符；补 pattern/color/size 控件后即可成立，最低成本是改名并重写 meta/简介、同时把预设改为「N 条」。

**留存建议（tools/design/isometric-grid.html）**：整改保留。等距网格 CSS 思路正确、页面最简洁，但「导出图片」是 meta 主卖点却完全缺失，且 ResText 读错容器导致四个数据页签全空；补 canvas/SVG 导出 + 改 ResText 读 `cssOutput.value` 即可。

**留存建议（tools/design/generator-10.html）**：必须整改后再保留。`@keyframes` 生成逻辑本身可用，但没有预览与任何参数控件，「可视化编排」不成立；补一个预览 box + duration/easing 控件，或改名「随机关键帧代码生成器」。

**留存建议（tools/design/music-scale-reference.html）**：整改保留（本批价值最高）。音阶结构、十二平均律频率与 CSV 导出均正确，唯一硬伤是音名拼写与调号表；按 15 个标准调查表重写 `notes`/`keySig`、补小调调号后即可作为乐理参考长期保留。

**留存建议（tools/design/generator-7.html）**：整改保留。边框 CSS 输出可直接用，但「可视化设置/单边独立」是 meta 主承诺且完全未实现；补控件与单边模式，或删承诺并改名「随机边框样式生成器」。

### 覆盖

- 实读 8/8 页整份 HTML：checker-5 458 / detector-28 463 / detector-29 671 / generator-11 468 / isometric-grid 491 / generator-10 468 / music-scale-reference 441 / generator-7 448，合计 3908 行；含 head meta、内联脚本、formula 块、deep-dive、FAQ JSON-LD 与 TBKIT 页签注入段。
- 新增 24 条，编号连续 D-N180–D-N203：高 7（D-N180、D-N183、D-N189、D-N192、D-N195、D-N198、D-N201）/ 中 11 / 低 6（D-N182、D-N191、D-N194、D-N197、D-N202、D-N203）。
- 复算说明：平仄字库去重与重叠（172/2043，重叠 118）、示例诗 8 次误标、12 根音大调拼写（6 错）均由 `node -e` 内存复算，未落地任何脚本；isometric 的「无导出」为静态核对（全文无 `<canvas>` / `toDataURL`，仅 FAQ `:206` 提到 Canvas）。
- 未覆盖：`tools/design/` 其余页面；未做浏览器渲染/交互（含 CSS 等距网格实际视觉、`double` 1px 真机渲染、`?lang=en-US` 探针）、移动端真机、`_build.py`/门禁与线上验证；未改任何源码、未做 git 写操作。

## T 批 design 覆盖（2026-11-04）

- 本轮审计 13 页：`material-color`、`iso-noise-reference`、`generator-33`、`generator-8`、`blueprint-grid`、`generator-12`、`generator-9`、`generator-34`、`particle-effect-generator`、`farnsworth-d15-test`、`generator-38`、`bpm-tapper`、`web-audio-metronome`
- 新增 15 条（高 12 / 中 3），编号 D-N204–D-N218；假工具候选 4 页（generator-8、generator-9、generator-12、blueprint-grid）
- 未做浏览器/门禁/线上验证

## AB 批 · 设计族矩阵：图像/格式转换（2026-11-04）

> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

本轮复用 T 批末尾编号，新增 D-N219 起。6 页均实读整份 HTML，并按「输出物能否被标准工具还原」取向核查：像素尺寸用页面算式复算，blob/下载路径逐行核对，换算类用 `node -e` 内存复算（未落地脚本）。无浏览器实测，故 MIME 结论以「代码实际取哪个字段」为准。

| 页面 | 实现方式 | 可验证性 | 结论 |
|---|---|---|---|
| `tools/design/svg-to-png.html`（死键 2） | Canvas（Blob→Image→drawImage→`toDataURL`） | 中：PNG 可解码，像素=宽×倍率；但无尺寸/面积上限，超大画布 `toDataURL` 返回 `data:,` → 0 字节 | 真实现，需补上限 |
| `tools/design/px-to-rem.html`（死键 1） | 自写算术（`px/root`） | 高：算术可复算；默认 16/16=1rem，站点 CSS 未改写根字号，与浏览器 16px 一致 | 真实现；62.5% 说明写反 |
| `tools/image/image-compress.html`（死键 0） | Canvas + `toBlob` + 对比滑块 | 中：blob 可下载、长边限制正确；MIME 与极端比例不可靠 | 真实现 |
| `tools/image/image-resize.html`（死键 1） | Canvas + `toBlob` + token 防竞态 | 高：尺寸/比例/质量可复算，blob 真下载；大画布内存与 MIME 有缺口 | 本批最完备 |
| `tools/image/image-converter.html`（死键 0） | Canvas 三格式批量 `toBlob` | 中：三份 blob 均可下载；换图竞态会把旧图卡片追加到新网格 | 真实现 |
| `tools/design/photo-print-size.html`（死键 0） | 自写算术 + 相纸规格表 | 高：`cm = px/DPI×2.54` 与相纸需求像素均可复算 | 真实现；预设与表差 1px |

### 逐页结论

- **svg-to-png**：透明默认已修正——背景下拉默认 `transparent`，仅选「白色」才 `fillRect`（`svg-to-png.html:168`、`:283-286`），D-N20 的「恒定铺白底」已不成立；导出像素与 `exportMeta` 一致（`w*scale`，`:273`、`:280`）。真实缺口在尺寸校验只有 `w>0&&h>0`（`:266`），6000×6000 @3x 即 18000²=3.24 亿像素，超过 Chrome 约 2.68 亿像素画布上限，`canvas.toDataURL` 返回 `data:,`，下载得到 0 字节且无提示；`img.onload` 内异常也未捕获（`:278-291`，外层 `try` 管不到异步回调）。预设「高清 2 倍图 800×800」只写 `width/height`、不重置 `scale`，选过 3x 后实际输出 2400×2400，与标签不符（`:435-441`）。
- **px-to-rem**：默认态 `calcTool()` 加载即算，16px/16 → `1.0000rem`，合理；`num()` 支持全角数字/`px`/`rem` 后缀与千分位（`:224-232`），`root<=0` 回退 16 并在结果下提示（`:235-236`）。硬伤是参考区 `:188`：62.5% 方案下应为「上表 rem 值 **乘以** 1.6」，写成了「除以 1.6」；该句自带示例 16px→1.6rem、24px→2.4rem 恰是乘法的结果，按字面除得 0.625rem/0.9375rem，与示例自相矛盾（node 复算 1/1.6=0.625，1×1.6=1.6）。页面换算本体与 CSS 根字号口径一致。
- **image-compress**：核心链路真实：`calcDims` 按长边等比、`toBlob(mime, 0.01~1)`、扩展名跟随 `compType`（`:507-528`、`:780`）。两处可验证性缺口：① `resolve({…,type:mime})` 把**请求的** MIME 当实际类型（`:527`），全页不读 `blob.type`，浏览器不支持 WebP 编码时 `.webp` 里是 PNG 字节；② 极端纵横比会算出 0 边——1×4000 图配 1920 长边 → `Math.round(1920*0.00025)=0`（`:511`），canvas 宽 0，产出失败且无「最小 1px」提示。JPEG 先铺白底符合预期（`:521`），PNG/WebP 保留 alpha。默认态无图时结果卡隐藏，默认 1920/WebP/80 合理。
- **image-resize**：本批质量最高：`MAX_SIDE=10000` 校验、空/超限显式报错并停止渲染（不退化 1px）、换图用 `loadToken`/`blobToken` 丢弃过期回调（`:567-570`、`:716-724`、`:770-772`），下载名跟随实际生成时的 `resultFmt`。缺口是上限只限单边不限面积：10000×10000=1 亿像素（约 400MB），且预览 `canvas.cloneNode` 保留同样大的后备画布（`:751-763`），桌面双份约 800MB、Safari 约 1677 万像素上限下直接空白（只 toast「尺寸过大」）。MIME 同样只记请求格式（`:782`）。
- **image-converter**：三格式并行 `toBlob` 按 0.85 质量输出，JPEG 单独铺白、PNG/WebP 保留 alpha（`:295-321`），下载为 blob URL，真实可用。缺 token：`handleFile` 换图后 `grid.innerHTML=''`，但上一张图 3 个异步回调仍会 `appendChild`（`:294`、`:308`、`:319`），快速连选两张会得到「头部文件名 B、卡片里混着 A」的可下载结果。另 PNG/WebP 卡片无条件写「已保留透明」（`:316`），源为 JPG 时并无 alpha，属误导；整图按原始像素建 3 份 canvas，无尺寸上限（`:298-299`）。
- **photo-print-size**：公式与相纸表正确（一寸 2.5×3.5 … A3 29.7×42，`:253-263`），默认 4000×3000@300 → 33.9×25.4cm，合理；`reqW/reqH` 用 `ceil`，三档判定逻辑可复算（`:284-290`）。预设「一寸证件照 295×413」与表格自身需求 296×414 差 1px（node 复算 `ceil(2.5/2.54*300)=296`、`ceil(3.5/2.54*300)=414`），点击该预设时「一寸」行只显示「🆗 基本可用」而非「✅ 像素充足」，预设与标准表自相矛盾。CSV 恒写「是」的问题已在早前条目记录（见本文件 :44 起），本轮不重复编号。

### 新增问题

| 编号 | 级别 | 页面 | 问题与证据 |
|---|---|---|---|
| D-N219 | 高 | svg-to-png | 宽高无上限，6000×6000@3x=3.24 亿像素超画布上限，`toDataURL` 返回 `data:,`，下载为 0 字节 PNG；`img.onload` 内异常无捕获。`:261-262`、`:278-291`、`:296-302` |
| D-N220 | 高 | px-to-rem | 62.5% 根字号换算说明方向写反：「上表 rem 值除以 1.6」应为乘以 1.6；与同句示例 16px→1.6rem 矛盾。`:178-188` |
| D-N221 | 高 | image-compress | 极端纵横比取整为 0：1×4000 配 1920 长边 → 宽 `Math.round(1920*0.00025)=0`，canvas 0 宽、产出失败且无提示。`:507-512`、`:518` |
| D-N222 | 高 | image-converter | 换图无 token，旧图 `toBlob` 回调晚到会向新网格追加旧图卡片，头部显示 B 却可下载 A。`:294`、`:308`、`:319` |
| D-N223 | 中 | image-compress / image-resize / image-converter | 实际 MIME 一律按请求格式记录，不读 `blob.type`；不支持 WebP 编码时 `.webp` 落盘为 PNG 字节，卡片/CSV 仍标 WebP。compress `:527`、resize `:782`、converter `:316-317` |
| D-N224 | 中 | image-resize | `MAX_SIDE=10000` 只限单边不限面积：1 亿像素主画布 + 同尺寸预览画布约 800MB；Safari 超约 1677 万像素上限时画布空白，仅 toast。`:527`、`:751-763`、`:771-775` |
| D-N225 | 中 | photo-print-size | 内置「一寸证件照 295×413」与表格需求 296×414 差 1px，点该预设时「一寸」行仅「基本可用」，预设与标准表不一致。`:162`、`:284-290`、`:300` |
| D-N226 | 低 | image-converter | PNG/WebP 卡片无条件写「已保留透明」，源为 JPG 时无 alpha，标注误导。`:316` |
| D-N227 | 低 | svg-to-png | 「复制 Base64」复制的是含 `data:image/png;base64,` 前缀的完整 URL；`navigator.clipboard.writeText` 无 `.catch`/降级。`:303-306` |

### 统计

- 实读 6/6 页整份 HTML：svg-to-png 534 / px-to-rem 396 / image-compress 964 / image-resize 1002 / image-converter 540 / photo-print-size 484，合计 3920 行。
- 新增 9 条，编号连续 D-N219–D-N227：高 4（D-N219、D-N220、D-N221、D-N222）/ 中 3 / 低 2。
- 假工具候选 **0**：6 页均有真实 Canvas/算术输出与可下载产物（压缩/缩放/转换三页确有 blob 下载，svg 出真 PNG，打印尺寸为真换算）。
- 安全 **0**：未见 `eval`、`allow-same-origin`、明文存密或第三方外传；用户 SVG 仅经 `image/svg+xml` Blob→`<img>` 渲染，脚本不执行；文件名均过 `escHtml`（resize 的 `file.type` 直接入模板，属浏览器已归一化的 MIME 令牌，风险可忽略）。
- 复算说明：相纸需求像素/一寸预设判定、62.5% 换算、`calcDims` 极端比例均由 `node -e` 内存复算；未落地脚本、未改任何源码、未运行 `_build.py`/门禁、未做 git 与浏览器/线上验证。

## AC 批 · 颜色/色彩处理族（2026-11-04）

> 死键口径见 AB 段图例；本段不逐页重标，按 `plan/i18n-dead-keys.md` 取数。

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/design/color-palette-generator` | 自写 HSL 旋转（单色/互补/三角/四角/分裂互补/随机）+ HSL→RGB；色块字色改为黑白两案取最大对比度 | HSL 定义 + WCAG 可复算 | 默认单色 5 色可复算；随机模式仍是无约束随机 HEX |
| `tools/design/color-palette` | 自写 HSL 旋转（固定 20/35/50/65/80/95 明度） | 可复算 | 默认互补数值正确；字色仍用亮度 0.5 阈值 |
| `tools/design/color-picker` | 自写 HSB/HSL⇄RGB、和声、WCAG 对比度、历史 | 可复算 | 取色与对比度主流程正确；「推荐文字色」用 0.5 阈值 |
| `tools/design/color-shade-generator` | 自写 sRGB 线性混白/混黑（`C·(1−t)+目标·t`） | 可复算 | 默认 #6366F1 生成 11 卡；文档仍称 HSL/OKLCH 明度阶梯 |
| `tools/design/color-temperature-converter` | Tanner Helland 黑体近似（正）+ 1000–12000K/100K 曼哈顿距离反查 | 正算可验证；反查无残差判据 | 默认 5500K→(255,238,222) 正确；轨迹外反查恒返回边界温 |
| `tools/design/colorblind-simulator` | 外置共享库 `js/tools/colorblind-simulator.js`：Machado 2009 三矩阵 + 灰度 | 矩阵与官方值逐字一致 | 默认 #FF6B35 绿盲 100%→#B9A62F 正确；严重度用线性插值 |
| `tools/design/contrast-checker` | 自写 WCAG 相对亮度/对比度 + 阈值判定 | 可复算 | 默认 14.68:1，判定正确 |
| `tools/design/cvd-safe-palette` | 自写 OKLCH/Lab 候选集 + 8 型模拟 + ΔE2000 贪心 | 可验证（无默认结果） | 发散亮度曲线与注释相反、策略两分支同实现、首色恒灰 |
| `tools/design/gradient-from-color` | 自写 HSL 明度阶梯（固定 L 90→20）+ 方向/步数 | 可复算 | 基色 L 被丢弃，默认 #667eea 不出现在色标里 |
| `tools/design/gradient` | 自写 CSS 渐变拼装 + 色标解析 + WCAG 对比度 | CSS/WCAG 可验证 | 默认相邻色标 1.74:1；「正文级」标签属口径误用 |
| `tools/design/material-color` | 纯常量表（Material 2014，19 族×10 阶）+ 亮度阈值选字 | 常量表可核对 | 数据正确；主色徽标取 600 阶、图表取 500 阶 |
| `tools/design/mesh-gradient` | 自写 3 色 radial-gradient + Canvas farthest-corner 近似导出 | 视觉可验证 | 默认白字 vs #f093fb 仅 2.04:1；历史/预设/CSV 恒空 |
| `tools/design/palette-cvd-checker` | 自写 Lab/CIE76/CIEDE2000 + 复制 Machado 矩阵 + 自写 OKLCH 距离 | ΔE00 可验证；oklch 分支不可信 | 默认绿盲最小 ΔE00=4.27 正确；OKLCH 分支把 Lab 当 RGB |
| `tools/design/palette-extractor` | 自写中位切分（`maxDepth=ceil(log2 N)`）+ 降采样 200px | 频率可核对 | 默认 8 色正确；5/10/12 色丢簇、极小图产 NaN 黑块 |
| `tools/design/tailwind-colors` | 纯常量表（Tailwind v3，22 族×11 阶）+ 亮度阈值选字 | 常量表可核对 | 数据正确；43/242 色块文字 <4.5:1 |
| `tools/design/image-color-picker` | Canvas `getImageData` 单像素取色 + 复制 | 取样可验证 | 比例映射正确；忽略 alpha、无 WCAG 实现 |

### 独立实现 vs 共享实现

- **独立 6 页**：contrast-checker、color-shade-generator、color-temperature-converter、gradient、mesh-gradient、image-color-picker。
- **共享/同模板 10 页**：
  - `tailwind-colors` ↔ `material-color`：`getLuminance/textColor/render/filter/showDetail/copy` 整段同构（material 的 D-N204/N205 与 tailwind 的 D-N142 同源）。
  - Machado 矩阵在 `colorblind-simulator`、`palette-cvd-checker`、`cvd-safe-palette` 三页逐字重复（数值正确，三页都用「单位阵→满矩阵」线性插值模拟严重度）。
  - HSL 转换在 `color-palette-generator`、`color-palette`、`gradient-from-color` 三份重复（h/s/l 取整致基色回代漂移）。
  - `lum>0.4/0.5` 选黑白字在 color-palette、tailwind、material、palette-extractor、color-picker 五页重复，同错同源。
- 结论：本族修「字色阈值」一处口径即可同时消解 5 页同类缺陷；`palette-extractor` 的簇数问题是本页独有，需单独修。

### 逐页结论

- **color-palette-generator**：默认单色 #0C1A5A→#E9ECFC 五档可复算，字色取 max(CR) 正确；D-N2 已失效（旧 YIQ 已改），D-N3（随机无协调）仍成立。
- **color-palette**：默认互补五色；#788EED 上白字仅 3.05:1（D-N228）；FAQ 宣称的 WCAG 校验不存在（D-N229）；D-N33（HEX 只校验长度）已于第311批修复。
- **color-picker**：默认 #4151e1 自洽、白字 6.02:1；#788EED 时「推荐文字色」仍给 #FFF（3.05:1），与同页 WCAG 面板自相矛盾（D-N230）；D-N31/D-N32 已于第314批修复（越界回写 + HEX 3/6/8 位校验）。
- **color-shade-generator**：默认 11 卡线性混白/黑，公式一致；D-N34/D-N36 已失效，D-N35 部分仍成立（`:148`、`:383` 仍称 HSL/OKLCH 十档）。
- **color-temperature-converter**：默认 5500K→(255,238,222) 正算可用；D-N17 已失效（已加范围校验），D-N18（轨迹外反查仍返回边界温）已于第315批修复（残差超阈值提示）。
- **colorblind-simulator**：默认绿盲 #FF6B35→#B9A62F 与 Machado 1.0 手算一致；D-N102（取色器不写回 HEX）已于第317批修复。
- **contrast-checker**：默认 14.68:1、AA/AAA 判定正确；D-N1（非法 HEX 不刷新结果）仍成立。
- **cvd-safe-palette**：无默认结果；D-N106（发散亮度方向反，L 两端 0.90、中心 0.32）、D-N107（策略两分支同实现）仍成立；D-N108（首色恒定）已于第317批修复。
- **gradient-from-color**：默认 L90→20 五色标，基色 #667eea(L66) 不出现；D-N125/D-N126 仍成立，D-N124/D-N127 已于第318批修复。
- **gradient**：默认相邻色标 1.74:1；新增对比度使 D-N47/D-N48 的 gradient 部分失效（image-color-picker 部分仍成立）；D-N233/D-N234 为新增。
- **material-color**：常量表正确；主色徽标取 600 阶而图表取 500 阶；D-N204（图表取 400 阶）已于第311批修复，D-N205 仍成立。
- **mesh-gradient**：默认白字最差 2.04:1，报告正确；D-N59（动态色块无 id → 历史/预设/CSV 恒空）已于第320批修复，D-N60 已失效。
- **palette-cvd-checker**：默认绿盲最小 ΔE00=4.27、判「差」正确；D-N112（OKLCH 分支把 Lab 当 RGB，复算最小距离 0.55 vs 正确 2.14）仍成立。
- **palette-extractor**：默认 8 色正确；5/10/12 色百分比合计仅 62.5%/62.5%/75.0%（D-N231）；极小/大面积透明图产 #000000 0.0%（D-N232）；D-N56（排序后导出不刷新）已于第311批修复。
- **tailwind-colors**：数据与 Tailwind v3 一致；43/242 色块文字 <4.5:1（yellow-500 白字 1.92:1），D-N142 仍成立。
- **image-color-picker**（实际在 `tools/design/`）：取样坐标换算正确；半透明 PNG 按原始 RGB 复制（预览为白底合成）；D-N46/D-N47 仍成立。

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| D-N228 | `tools/design/color-palette.html:401-405` | 中 | 色块字色按 `lum>0.5` 选白/黑：默认 #788EED 白字 3.05:1（黑字 6.89:1）、单色 #A5B3F3 白字 2.03:1（黑字 10.34:1）。期望按 `max(CR_black,CR_white)` 选字（阈值 L≈0.179） |
| D-N229 | `tools/design/color-palette.html:248,278` | 假 | FAQ「会按 WCAG 算出对比度、未达标标红」+ 引据表 4.5:1 条目，全页无相对亮度/对比度计算、无红标，仅亮度阈值选字 |
| D-N230 | `tools/design/color-picker.html:487,494,546` | 中 | 「推荐文字色」同用 `luminance>0.5`：HSL(230,76,65)=#788EED(L=0.295) 推荐 #FFF，仅 3.05:1；期望 #000（6.89:1） |
| D-N231 | `tools/design/palette-extractor.html:840,848,859` | 中 | `maxDepth=ceil(log2 count)` 先切 2^k 簇再 `slice(0,count)`：5 色丢 3/8 簇、10 色丢 6/16、12 色丢 4/16，`percent` 合计仅 62.5%/62.5%/75.0%，JSON 导出同带错值；期望按保留簇重新归一或精确切 N 簇 |
| D-N232 | `tools/design/palette-extractor.html:752-755` | 中 | 1 像素簇 `mid=0` 仍递归，空簇 `n=0` 分支得 NaN，`rgbToHex` 位运算把 NaN 变 #000000 0.0%。复现：不透明像素 <8 的图（2×2 PNG / 大面积透明 logo）→ 多个 #000000 0.0% |
| D-N233 | `tools/design/gradient.html:270` | 假 | 引据表称「按 sRGB 或 oklab 插值，oklab 可用」，页面无 oklab 选项/代码，输出一律浏览器 sRGB 插值 |
| D-N234 | `tools/design/gradient.html:365-421` | 中 | 新补对比度为「相邻色标互比」，却套 WCAG 文字档位贴「正文级/大字或图形级」；默认 1.74:1 被标「仅装饰」，易被读成文字可读性结论。期望改名「色标间对比度、不适用 WCAG 文字等级」 |

### 统计

- 页数 **16**；独立实现 **6** / 共享或同模板 **10**。
- 新增 **7** 条（高 **0** / 中 **5** / 假 **2** / 安全 **0**）；编号 D-N228–D-N234。
- 复核既有 **27** 条：22 条仍成立或部分成立，5 条已失效（D-N2、D-N17、D-N34、D-N36、D-N60）；`plan/fake-tools.md` 中 gradient/mesh 的假工具结论已随实现补齐而失效，建议降级。
- 复算方式：按页面同款公式用 node/Python 内存复算（HSL/OKLab/WCAG/ΔE00/中位切分），未开浏览器、未跑 `_build.py`/门禁、未改源码、未做 git 写操作。

### AA 批第 1 波处置（2026-11-07 X 批 · 对比度校验器非法 HEX 校验）

- **D-N1（中，确认源码缺陷）**：`contrast-checker.html` 原 `onFgHexInput`/`onBgHexInput` 仅在 `isValidHex` 为真时刷新结果，非法值（如 `GGGGGG`）静默保留旧结果且无任何提示；且 `isValidHex` 只认 6 位、`#fff` 三位的简写被丢弃。本批：(1) `isValidHex` 扩为 `/^[0-9A-Fa-f]{3}$|^[0-9A-Fa-f]{6}$/`；(2) 输入处理函数改为始终从 DOM 读真实值（harness 经 `new Function` 注册内联 `oninput`、调用时 `this` 绑定丢失、参数可能为 `undefined`，故不再依赖入参）；非法值显式写「颜色需为有效的 3 或 6 位 HEX 值」并清空比率（`ratioNum`→`—`），合法值才同步色板并 `updateAll()`。
- **D-N2 / D-N3 不在本批范围**：ledger 第 9 行明示 D-N2「仍待处理，不能按已修关闭」（WCAG 选字色的语义/标注口径争议），D-N3 为产品定位决策（受约束随机 vs 标注），均留待各自批次，本批未改动 `color-palette-generator.html` 源码。
- **同批门禁维护**：`verify_design_calc.js` 增 2 用例——`GGGGGG→颜色需为有效的 3 或 6 位 HEX 值`、`#fff→21.00`；全量 `node scripts/verify_design_calc.js` **264/264**（原 262 + 2）。`discriminate_check.js verify_design_calc.js` **264 已检 / 262 变红 / 2 逃生**（2 项 `photo-print-size`、`spacing-scale` 为既有的其他工具遗留逃生项，非本批引入，留待各批次处理）。
- **验证**：`node scripts/_verify_design_batch_x.mjs` **1/1**，`--head` 回退 **1/1**（HEAD 版 `GGGGGG` 静默显示 `14.68 / AAA 优秀` 无报错——修复真实有效）；i18n 无需同步（提示串为页面硬编码中文，EN 态同一逻辑、不影响）。

### AA 批第 1 波处置续（2026-11-07 Y 批 · 断点生成器注释 operator-precedence）

- **D-N15（中，确认源码缺陷）**：`breakpoint-queries.html:274` 原 `let css='/* '+mode==='min'?'移动优先（Mobile First）':'桌面优先'+' */\n';` 因 `+` 先于 `?:` 求值，恒按 `('/* '+mode)==='min'` 判假，两模式都落入「桌面优先」分支，且 min 模式产出缺起始 `/*` 的孤立 `*/`，复制进项目会误导协作方或被工具链判为语法错误。本批改为 `let css='/* '+(mode==='min'?'移动优先（Mobile First）':'桌面优先')+' */\n';`（先求标签再拼接、统一闭合注释）。
- **同批门禁维护（铁律①）**：`verify_design_calc.js` 增 1 用例 `mode='max' → /* 桌面优先 */`（265/265，原 264+1）。选 `mode='max'` 而非 `min` 是因为默认 mode 即 `min`，锚 `/* 桌面优先 */` 与默认态 `/* 移动优先（Mobile First） */` 不重合并零逃生。
- **验证**：`node scripts/verify_design_calc.js` **265/265**；`discriminate_check.js verify_design_calc.js` **265 已检 / 263 变红 / 2 逃生**（2 项 `photo-print-size`、`spacing-scale` 为其他工具既有遗留逃生项，非本批引入）；`node scripts/_verify_design_batch_y.mjs` **1/1**，`--head` 回退 **1/1**（HEAD 版实测 `桌面优先 */` 孤立 `*/` 无 `/*` 开头——修复真实有效）；i18n 无需同步（注释串为页面硬编码中文）。

### AA 批第 1 波处置续（2026-11-07 Z 批 · SVG 转 PNG 清空输入后仍可下载旧图）

- **D-N21（中，确认源码缺陷，2026-11-06 复核"仍部分存在"）**：`svg-to-png.html` 的 `generate()` 在空 SVG（`:349`）与非法宽高（`:344`）分支提前 `return`，均未清空 `lastDataURL`；下载函数 `downloadPNG()` 仅判 `!lastDataURL` 即导出。故先转有效 SVG 得真实 `lastDataURL`，再清空文本框点「转换」（预览显示「请输入 SVG 代码」）后直接下载，仍导出上一张 PNG。本批在两处提前 `return` 前补 `lastDataURL = ''`，使清空/非法分支立即失效下载。
- **验证约束**：Canvas/Image 在门禁桩下无法真实渲染，故不新增 harness 用例（避免假通过）；改用运行期回归脚本 `scripts/_verify_design_batch_z.mjs`：桩 `getContext/toDataURL/Image` 让成功路径把 `lastDataURL` 置为 STALE，再清空 SVG 重新 `generate()`，断言 `downloadPNG()` 因 `lastDataURL` 空而提示「请先转换」（`alert` 桩捕获）。脚本 **1/1**，`--head` 回退 **1/1**（HEAD 版清空后仍不拦截——修复真实有效）。
- **同批门禁维护**：既有 `svg-to-png` 3 用例（`:2018/:2237/:2245`）复跑 **3/3**，全量 `verify_design_calc.js` **265/265** 不变；i18n 无需同步（提示串为页面硬编码中文）。
