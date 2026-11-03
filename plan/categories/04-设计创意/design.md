# 设计创意 · tools/design（111 页）

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

### D-N1 手输非法色值时输入框与对比度结果脱节（中，确认源码缺陷）
- 证据：`tools/design/contrast-checker.html:823-837` 仅在 `isValidHex(val)` 为真时更新结果；用户把 HEX 框改成 `GGGGGG` 或 `#12` 后输入框显示新串，右侧对比度仍是上一颜色的结果，且无任何错误提示。`updateAll`（`:744-751`）本身不校验，`hexToRgb`（`:712-719`）把非法值返回 `[0,0,0]`。
- 影响：`tools/design/contrast-checker.html`；用户以为看到的是当前输入色对的对比度，可能据此判定「不达标」而实际测的是黑底。
- 方案：输入即时校验，非法格式标红并不刷新结果或明确提示；同步支持 3 位简写与 `rgb()` 语法（`hexToRgb` 已能处理 3 位，但 `isValidHex :722-724` 只认 6 位，手输 `#fff` 被静默丢弃）。

### D-N2 色块文字用亮度阈值而非 WCAG 决定黑白字（中，确认源码缺陷）
- 证据：`tools/design/color-palette-generator.html:556-557` 用 YIQ 亮度 `>128` 选 `#333`、否则 `#fff`，未计算对比度；中亮度色（如 `#767676`）两种文字都可能达不到 AA 4.5:1，但页面仍自信地渲染色值标签。
- 影响：`tools/design/color-palette-generator.html`；用户把色板当成品交付时，色块上的文字标注本身可能不可读，且页面没有对比度信息。
- 方案：色块文字按 WCAG 选可读色，并在每个色块标出与白/黑文字的对比度与是否达 AA/AAA；导出时保留该标注。

### D-N3 「随机配色」产出无序色且与其它模式同样呈现（低，确认源码缺陷）
- 证据：`tools/design/color-palette-generator.html:502-508` 随机模式直接生成 5 个独立随机 hex，与单色/互补/三角等协调规则并列展示，页面未提示该模式不具备协调性。
- 影响：`tools/design/color-palette-generator.html`；设计师点击随机得到不可用配色后直接离开。
- 方案：随机模式改为在 HSL 空间内受约束随机（固定色相区间/饱和度亮度阶梯），或明确标注「实验性随机」；提供「锁定当前色再生成」避免整组被替换。

### D-N4 字体预览英文态残留中文操作提示（中，确认源码缺陷；运行态待探针）
- 证据：`tools/design/font-preview.html:553,568` 卡片内的「点击复制」与计数「N / M 种字体」为硬编码中文，`render()` 未见 `__T` 分支（`:531-570`）；`isEn` 仅用于图表 `:634`。`i18n/tools/en/design/font-preview.json` 与全站短语表均未收录该串。
- 影响：`tools/design/font-preview.html`；英文态每张字体卡片夹中文按钮提示，属 G05 同类的页面级 i18n 泄漏。
- 方案：这两个串走 `__T` 双语或补进第三层词典，改后必须重跑 `_build.py` 使版本戳生效；用 EN 探针复验。

### D-N5 字体预览只反映本机字体，无法判断跨平台效果（低，确认能力缺口）
- 证据：`tools/design/font-preview.html:550-557` 用本机系统字体栈渲染、点击复制整条 `font-family`；页面没有平台标注、回退链展示或「缺少该字体时」的对比。
- 影响：`tools/design/font-preview.html`；macOS 上效果好的字体栈在 Windows/Android 用户端会退化，用户复制后线上效果不符。
- 方案：标明当前预览平台，展示回退链并把「缺失时使用」的字体一并预览；提供常见平台（Win/macOS/Android/iOS）字体可用性表。

### 留存优化（按页落点，非确认缺陷）
- `tools/design/contrast-checker.html`：缺「一键调到 AA/AAA 达标」——用户测出 3.9:1 后只能自己反复微调。建议给出最接近的达标前景/背景色候选（保持色相，只调亮度）、可对比并保存的历史色对，这是此类工具的主要留存点。
- `tools/design/color-palette-generator.html`：色板只有 CSS 变量文本，无常驻「锁定色 + 再生成」与多格式导出（JSON/SVG/PNG）。建议加锁色、色板命名与导出，避免每次重新生成整组。
- `tools/design/font-preview.html`：输入框只支持单行固定字号，缺少字号阶梯与真实段落排版预览；建议加 12/16/24/32 阶梯同时预览与行高对比，贴近实际选字场景。

### 续查覆盖
- 新抽查 `tools/design/contrast-checker.html`、`tools/design/color-palette-generator.html`、`tools/design/font-preview.html` 共 3 页，新增 5 条（0 条高优）与 3 条留存建议；为源码静态核查，未做浏览器、EN 运行态探针、移动端或门禁验证。
