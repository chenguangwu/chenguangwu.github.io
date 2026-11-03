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

## 2026-11-03 续查（并行批 G）

### D-N6 景深计算器「1英寸」与「全画幅」共用 value=1，默认状态名不符实（高，确认源码缺陷）
- 问题：传感器下拉把「1英寸」写成 `value="1"` 且带 `selected`，与「全画幅 (35mm)」重复；页面默认显示「1英寸」，实际按全画幅 CoC 计算，且用户永远选不到 1 英寸对应的 2.7x。
- 证据：`tools/design/depth-of-field-calculator.html:153`（`<option value="1">全画幅…</option>` … `<option value="1" selected>1英寸</option>`）与 `:240-247`（`coc` 表已有 `2.7:0.011` 键，但 `c=coc[crop]||0.03`）。复现：默认打开页面（显示「1英寸」）→ `crop=+value=1` → `c=0.03`；50mm、f/1.8、对焦 2m 得 `h=46.296m`、景深 `1.92m ~ 2.09m`；若按 1 英寸 CoC 0.011mm 计算应为 `h=126.26m`、`1.97m ~ 2.03m`。
- 影响：`tools/design/depth-of-field-calculator.html`；常用画幅选项形同虚设，默认结果与界面标注不符，按 1 英寸取景布光会高估景深。
- 方案：为「1英寸」分配独立值（如 2.7）并去重 option value；`coc` 缺失时显式提示而非静默回退 0.03，默认值改为与文案一致的画幅。

### D-N7 对焦距离超过超焦距时近点被判为无穷，页面输出「Infinitym ~ ∞」（中，确认函数缺陷）
- 问题：近点与远点共用一个「`s<=h`」条件，越过超焦距后近点也被置为 `Infinity`；页面只做 `Infinity` → 「—」的字符串替换，留下「—m ~ ∞」和「Infinitym」。
- 证据：`tools/design/depth-of-field-calculator.html:250-252,258-266`。复现（node 内存执行原公式）：焦距 24mm、f/8、对焦 5m、全画幅 → `h=2.4m`，`s=5000mm>h` 使 `near=far=Infinity` → `dofTotal` 显示 `—m ~ ∞`、近点卡片为 `Infinitym`、`indicator` 的 `left` 为 `0%`；按标准公式近点应为 `1.63m`、远点为 `∞`。
- 影响：`tools/design/depth-of-field-calculator.html`；风光常用的「对焦到超焦距」场景完全拿不到近点数值，结果文案夹带非法值。
- 方案：近点始终算 `h*s/(h+s-f)`，仅在 `s>=h+f` 时把远点判 `∞`；对 `∞` 用明确文案（如「近点 1.63m ~ ∞」），不要把数值直接转字符串再替换。

### D-N8 焦距换算器空/零焦距仍输出 0mm、180° 视角与「超广角」（中，确认函数缺陷）
- 问题：焦距取 `+value||0` 后不校验即参与除法，0mm 时 `atan(w/0)=90°` 使视角恒显示 180°×180°，焦段分类落到「超广角」，页面没有任何错误提示。
- 证据：`tools/design/focal-length-equivalent.html:439-453,455-472`（输入 `:178` 声明 `min="1"`，但脚本未使用约束）。复现（node 内存执行原函数）：焦距清空（`focal=""`）→ 结果卡 `0mm`、`= 0.0mm`、`全画幅等效 0mm`、`焦段类型 超广角`、`视角: 180.0° × 180.0° → 180.0° × 180.0°`；正常 50mm（全画幅→APS-C 1.6x）时为 `= 31.3mm`、视角 `39.6° × 27.0°`。
- 影响：`tools/design/focal-length-equivalent.html`；用户误清输入框后得到的是一组看似合理、实际无意义的数值，可能被直接抄进选型表。
- 方案：焦距必须为正数才计算，空/0/负数显示提示并清空结果；补充等价校验区间（如 1–2000mm），并让 `min` 与脚本校验共用同一常量。

### D-N9 照片存储超额时进度条锁死 100% 且不提示超出（中，确认函数缺陷）
- 问题：`Math.min(100, …)` 把超过卡容量的占用压成 100%，页面只显示「100.0%」和无上限的「此卡可存储约 N 张」，看不出已超出多少；可存张数只按单张照片大小计算，未扣视频占用。
- 证据：`tools/design/photo-storage-calculator.html:454-456,470,479-495`（格式倍率 `:396-404`、`getBaseSize :415-418`）。复现（node 内存执行原函数）：45MP + RAW 无压缩 + 14bit + 2000 张 + 64GB 卡 → 单张 `75.10 MB`、照片总计 `146.68 GB`，进度条 `100.0%`，仍显示「此卡可存储约 872 张」且无红色溢出提示。
- 影响：`tools/design/photo-storage-calculator.html`；备卡决策会被「刚好 100%」误导，实际需 2–3 张卡或降规格。
- 方案：按真实占用渲染进度（>100% 时封顶但叠加「超出 X GB / 需 N 张卡」提示）；可存张数扣除视频占用并分列展示。

### D-N10 图片旋转把透明像素强制填成白底（中，确认源码缺陷）
- 问题：旋转前用 `fillStyle='#fff'` 铺满整幅画布再绘制图片，透明 PNG 的所有透明区域被拍平成白色，导出后无法恢复；页面也未提供背景色/透明选项。
- 证据：`tools/design/image-rotator.html:274-290`（`:284-285` 白底、`:289` 直接 `canvas.toDataURL('image/png')`）。复现（源码路径确认）：上传带 alpha 的 PNG 并点「旋转」→ 画布先被白色 `fillRect` 覆盖，再 `drawImage` 叠加原图，透明处输出为 `#ffffff`。
- 影响：`tools/design/image-rotator.html`；设计素材（图标、贴纸、免抠图）一旦经此旋转就丢失透明通道，属于不可逆的交付缺陷。
- 方案：默认不清屏（保留透明），另提供「透明/纯色/棋盘格预览」选项；导出前提示当前背景模式。

### D-N11 换图后仍可下载上一次旋转结果（高，确认源码缺陷）
- 问题：上传回调只替换 `origImg` 与预览，未清空 `lastURL`；下载函数仅判断 `lastURL` 非空即导出，换图后不重新点「旋转」也能下载旧图。
- 证据：`tools/design/image-rotator.html:260-273`（change 处理无 `lastURL=''`）、`:289`（仅 `generate()` 写 `lastURL`）、`:292-296`（`downloadImg` 直接取 `lastURL`）。复现（源码路径确认）：上传 A 并旋转下载 → 再上传 B、不点「旋转」直接点「下载」→ 导出 A 的旋转 PNG。
- 影响：`tools/design/image-rotator.html`；与已记录的 `image-resizer` 同类跨页复现，误交付旧图风险高，且预览显示 B 会让人误以为导出的是 B。
- 方案：上传、改角度、切换预设时统一使 `lastURL` 失效并禁用下载，导出前校验「当前图 + 当前角度」与生成时一致，状态栏显示「结果已过期，请重新旋转」。

### D-N12 二维码编辑后未重新生成仍可下载旧码，生成失败也保留旧结果（中，确认源码缺陷）
- 问题：`lastURL` 只在生成成功回调里更新，输入文本/尺寸/纠错级别变化不会清空它；生成失败分支只改预览文案，`lastURL` 仍是上一次的码，下载按钮照常可用。
- 证据：`tools/design/qr-code-styled.html:264-295`（`:289` 成功才写 `lastURL`、`:285-288` 失败仅 `preview.textContent`）、`:296-300`（`downloadImg` 只判 `lastURL` 非空）。复现（源码路径确认）：生成 `https://example.com` 后把文本改成新地址，不点「生成」直接下载 → 得到旧地址二维码；输入超长文本使 `QRCode.toCanvas` 回调 `err` 后，预览显示生成失败但仍可下载上一张。
- 影响：`tools/design/qr-code-styled.html`；二维码常被用于支付/活动链接，导出旧码会直接指向废弃地址；失败态还可下载更易误导。
- 方案：文本/尺寸/纠错级别变化即令结果失效并禁用下载；生成失败时清空 `lastURL` 并保持按钮禁用，同时给出容量/纠错建议。

### D-N13 间距比例尺层级/基础值越界被静默截断，输入框不同步（低，确认函数缺陷）
- 问题：`levels` 被 `Math.max(5, Math.min(15, …))` 静默夹取，`base` 用 `parseInt` 截断小数；生成结果与输入框显示不一致，且无提示。
- 证据：`tools/design/spacing-scale.html:271-273`（表单 `:168,179` 声明 `min/max`，脚本另行夹取）。复现（node 内存执行原函数）：`levels=3`、base 4、ratio 1.25 → 实际生成 5 档 `4 / 5 / 6.3 / 7.8 / 9.8`，输入框仍显示 3；`levels=20` → 15 档；`base=2.5` → `parseInt` 得 2。
- 影响：`tools/design/spacing-scale.html`；按错档数生成 token 后复制到设计系统，间距阶梯数量与预期不符。
- 方案：越界输入即时提示并把夹取后的值回写输入框；`base` 明确整数或支持 0.5 步进；输出区标注实际档数。

### D-N14 px↔rem 转换器对空值/非正根字号静默代入（低，确认函数缺陷）
- 问题：`px` 空值按 0 参与计算、`root<=0` 直接改成 16 并继续输出，输入框保留原值，页面未提示。
- 证据：`tools/design/px-to-rem.html:227-232`（输入 `:115,119` 无 `min`）。复现（node 内存执行原函数）：px 清空 → `0px = 0.0000rem`；`root=-8` 或清空 → 结果按 `1rem = 16px` 计算（`16px = 1.0000rem`），而输入框仍为 `-8`/空。`rem-to-px.html:230-235` 为同构代码，同样以 `root<=0 → 16` 兜底。
- 影响：`tools/design/px-to-rem.html`、`tools/design/rem-to-px.html`；换算基准被悄悄换成 16px，用户照结果改样式会得到非预期尺寸。
- 方案：空值与 `root<=0` 显示明确错误并清空结果；输入加 `min="1"`；`rem`/`px` 负值同样校验，两个页面共用同一校验逻辑。

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

### D-N15 断点生成器注释拼接优先级错误，移动优先产物被标成「桌面优先」并带孤立 `*/`（中，确认源码缺陷）
- 问题：`let css='/* '+mode==='min'?'移动优先（Mobile First）':'桌面优先'+' */\n';` 中 `+` 先于三元运算，实际按 `('/* '+mode==='min') ? …` 求值，左侧恒为 `"/* min"`/`"/* max"` 而不等于 `'min'`，于是任何模式都落到「桌面优先」分支。
- 证据：`tools/design/breakpoint-queries.html:274`（模板串），`:276-280`（按 mode 生成 min/max 规则）。node 内存复算：`mode='min'` → 首行 `"桌面优先 */\n"`；`mode='max'` → 同样 `"桌面优先 */\n"`；随后才是 `@media (min-width: 640px) {` 等正确规则。移动优先时注释文案与实际规则相反，且首行是缺少起始 `/*` 的孤立 `*/`，浏览器对该 token 的容错行为未实测。
- 影响：`tools/design/breakpoint-queries.html`；用户复制到项目后，CSS 首行文案误导协作方，孤立 `*/` 可能被部分工具链判为语法错误或吞掉后续规则。
- 方案：先求标签再拼接——`let css='/* '+(mode==='min'?'移动优先（Mobile First）':'桌面优先')+' */\n';`；补一条 `mode=min` 的产物首行断言。

### D-N16 字体比例尺只夹下限，基础字号越界/小数/空值静默改写（中，确认函数缺陷）
- 问题：页面标注基础字号范围 8–48，但脚本只做 `Math.max(8, parseInt(v)||16)`，没有上限夹取，`parseInt` 还会截断小数；空值退回 16、负数变 8，输入框均不回写也不提示。
- 证据：`tools/design/typography-scale.html:168`（`min="8" max="48"`）与 `:281`（`Math.max(8, parseInt(...)||16)`）、`:285-287`（按 `base * ratio^i` 递推）。node 内存复算：`base=100`、ratio 1.2 → 7 档 `100 / 120 / 144 / 172.8 / 207.4 / 248.8 / 298.6px`（超出页面承诺的 48px 上限）；`base=16.5` → 按 16 起算，最大 `47.8px`，而输入框仍显示 `16.5`；`base=''`、`base=-5` → 分别按 16、8 计算。
- 影响：`tools/design/typography-scale.html`；设计系统 token 的阶梯数量/字号与输入框显示不一致，越界值还会把预览撑到不可用尺寸。
- 方案：上下限共用同一常量并夹取后回写输入框；非正整数、空值显式提示并清空结果；输出区标注实际基准字号。

### D-N17 色温输入为负或空时生成 NaN 通道与非法 HEX（中，确认函数缺陷）
- 问题：`fromTemp()` 用 `+value||5500`，空值静默按 5500、负值则原样传入；`kelvinToRGB()` 对 `k/100<=66` 走对数公式，负温度取对数得 `NaN`，随后直接参与 `toString(16)` 与背景色拼接；只有 `#info` 的 NaN 守卫会报错，输入框与预览文本已被污染。
- 证据：`tools/design/color-temperature-converter.html:242-251`（对数/幂函数）、`:262-267`（`||5500`、写入 `rgb` 与 `preview`）、`:268`（回写 RGB）、`:277`（仅 info 做 NaN 守卫）；输入 `:145` 声明 `min="1000" max="40000"` 但脚本未使用。node 内存复算：`temp=-2000` → `kelvinToRGB(-2000)` 得 `[255, NaN, 0]`，HEX 为 `#ffNaN00`；RGB 输入框被写成 `255,NaN,0`；`temp=0` → `[255,0,0]`（`#ff0000`）而不报错；`temp=''` → 按 5500 计算但输入框仍为空。
- 影响：`tools/design/color-temperature-converter.html`；预览文字与 RGB 框出现 `NaN` 和非法色值，复制后落到设计稿/代码里不可用。
- 方案：色温必须是 1000–40000 的有限正数，越界或空值提示并清空预览/RGB 框；输入 `min/max` 与脚本校验共用常量；`kelvinToRGB` 入口加有限性检查。

### D-N18 反向换算对轨迹外颜色仍返回边界色温，冒充「精确 CCT」（低，确认函数缺陷）
- 问题：`rgbToKelvin()` 只在 1000–12000K 每 100K 采样取最小曼哈顿距离，不判断残差是否可接受；纯蓝、纯黑、纯红等远离黑体轨迹的颜色也会返回一个边界附近的温度。
- 证据：`tools/design/color-temperature-converter.html:252-260`（固定区间线性搜索）。node 内存复算：`rgbToKelvin(0,0,255)` → `11800K`（minDiff 406）；`rgbToKelvin(0,0,0)` → `1000K`（minDiff 323）；`rgbToKelvin(255,0,0)` → `1000K`（minDiff 68）。
- 影响：`tools/design/color-temperature-converter.html`；用户输入任意品牌色后得到一个看似精确的「色温」，实际该色已明显偏离黑体轨迹。
- 方案：设最大残差阈值，超出时提示「该颜色不在黑体轨迹附近」；如需严谨结果改用 CIE 相关色温 + Duv，并展示残差/偏移量。

### D-N19 PNG 转 SVG 阈值 0 被代换为 128、负块宽生成非法 SVG，换图后仍复制旧结果（中，确认函数缺陷，三个问题）
- 问题：① `parseInt(...) || 128` 把合法的 `0` 当作空值换成 128，用户想保留全部像素却得到大量透明格被跳过；② 块大小同样用 `|| 8`，负值 `-5` 能通过，`Math.max(1, floor(w/block))` 把网格压成 1，但输出宽高仍用 `w*block`，得到负值；③ `lastSVG` 只在生成成功时覆盖，换图或改参数后不失效，直接点「复制 SVG」会拿到上一张的结果。
- 证据：`tools/design/png-to-svg.html:258-259`（`||8` / `||128`）、`:264-265`（网格下限 1）、`:280`（`width="${w*block}"`）、`:253`（`lastSVG` 初值，全文无清空）、`:288-290`（复制只判非空）、`:160-163`（`min/max` 未参与脚本）。node 内存复算：`alphaTh=0` → 实际按 128；`block=0` → 8，`block=-5` → -5；100px 原图配 `block=-5` → 网格 `w=1`、输出宽 `-5`（`<svg width="-5">`）；`block=8.7` → `parseInt` 得 8。
- 影响：`tools/design/png-to-svg.html`；阈值 0 场景输出严重缺块、非法 SVG 在部分浏览器/编辑器打不开，换图复制则把上一张的矢量交给用户。
- 方案：用 `Number.isNaN` 显式判空而非 `||`；块大小限定正整数并在越界时回写/提示；换图、改块大小或阈值时清空 `lastSVG`、清空代码框并禁用复制，直至重新生成。

### D-N20 SVG 转 PNG 恒定铺白底，与页面「导出支持透明」的 FAQ 相反（中，确认源码缺陷）
- 问题：无论 SVG 是否透明，画布都先 `fillStyle='#fff'` 整幅填充再绘制，导出 PNG 的透明区域全部变成白色；页面 FAQ 两处均声称「导出 PNG 支持透明，如需白底可自行垫底」。
- 证据：`tools/design/svg-to-png.html:268-270`（白底 + `drawImage`）、`:272`（`toDataURL('image/png')`）、FAQ `:204-205`。复现路径：输入带透明背景的 `<svg>`（仅一个居中圆形），点「转换」→ 画布先被白 `fillRect` 覆盖，圆形以外的透明区域导出为 `#ffffff`。
- 影响：`tools/design/svg-to-png.html`；透明图标/贴纸导出后无法叠加到深色底，且与页面承诺矛盾，用户按 FAQ 预期使用会拿到错误交付物。
- 方案：默认不清屏以保留 alpha，另提供「透明 / 白底 / 自定义底色」选项；同步修正 FAQ 与公式说明。

### D-N21 SVG 转 PNG 转换失败或改参数后仍可下载旧 PNG（中，确认源码缺陷）
- 问题：`lastDataURL` 只在 `img.onload` 成功分支写入；空 SVG 提前 return、`img.onerror`、修改宽高或替换 SVG 文本都不会使其失效；下载仅判断非空。
- 证据：`tools/design/svg-to-png.html:259`（空输入提前返回）、`:272`（成功才写）、`:275`（失败仅改预览文案）、`:279-285`（`downloadPNG` 只判 `lastDataURL`）。复现路径：先转换有效 SVG → 清空文本框再点「转换」（预览显示「请输入 SVG 代码」）→ 直接点「下载 PNG」仍导出上一张；把宽高从 400 改为 800 但不重新转换，下载的仍是 400×400 图。
- 影响：`tools/design/svg-to-png.html`；与 `qr-code-styled`/`image-rotator` 同类的旧结果复用，误交付尺寸或内容不符的 PNG。
- 方案：输入、宽高变化及任一失败分支统一清空 `lastDataURL` 并禁用下载；状态栏显示「结果已过期，请重新转换」。

### D-N22 图片翻转换图后仍可下载上一次翻转结果（高，确认源码缺陷）
- 问题：上传回调只替换 `origImg`/`currentImg` 与预览，未清空 `lastURL`；下载与复制只判断 `lastURL` 非空。
- 证据：`tools/design/image-flipper.html:250-263`（change 处理无 `lastURL=''`）、`:279`（仅 `flip()` 写 `lastURL`）、`:285-289`（`downloadImg` 直接取 `lastURL`）、`:290-293`（`copyResult` 同理）。复现路径：上传 A 并翻转后下载 → 再上传 B、不点「翻转」直接点「下载」→ 导出 A 的翻转 PNG，而预览显示 B。
- 影响：`tools/design/image-flipper.html`；本分类第三个同类页面（另有 `image-resizer`、`image-rotator`），换图后误交付旧图风险高。
- 方案：上传、切模式时统一使 `lastURL` 失效并禁用下载；导出前校验「当前原图 + 当前模式」与生成时一致，状态栏提示「结果已过期，请重新翻转」。

### D-N23 翻转依赖异步 `currentImg`，快速连点两次不能还原（中，待验证）
- 问题：`flip()` 在点击时读取 `currentImg`，但 `currentImg` 只在下一次生成图片的 `newImg.onload` 回调里更新；若第二次点击早于回调，两次都基于 `origImg` 生成同一张单次翻转图，页面「重复翻转两次应完全还原」的说明不成立。
- 证据：`tools/design/image-flipper.html:265-266`（读取 `currentImg || origImg`）、`:280-282`（`newImg.onload` 才赋值 `currentImg`）、说明表 `:230-234`。源码路径推演：连点「水平翻转」两次 → 第一次 `lastURL` 生成水平镜像，第二次仍在 `onload` 前读到 `origImg` → 覆盖为同一张水平镜像，而非原图。Canvas 与回调时序未在浏览器实测，故列待验证。
- 影响：`tools/design/image-flipper.html`；用户快速连点或想「翻过去再翻回来」时得到错误结果。
- 方案：以同步的累计变换状态（`flips` 计数/矩阵）驱动绘制，或生成期间禁用按钮，待 `currentImg` 就绪并提示后再允许下一次；补一条双击还原的回归用例。

### D-N24 圆角图片先铺背景再裁剪，纯色/渐变模式导出仍是方角（中，确认源码缺陷）
- 问题：`render()` 先整幅填充背景，再建立圆角/圆形裁剪路径并绘制图片；裁剪只作用于图片，不作用于已铺满的背景，因此圆角外区域保留背景色，导出 PNG 四角是实心方块，而非「圆角 + 透明」或「圆角纯色底」。
- 证据：`tools/design/image-rounded-corners.html:1106`（清屏）、`:1109-1113`（按背景类型整幅 `fillRect`）、`:1115-1125`（建立裁剪并 `clip`）、`:1127-1128`（仅裁剪图片）、`:1152-1168`（直接导出 `previewCanvas` PNG）。复现路径：上传任意图 → 选「纯色」背景 → 导出 → 四角为背景色矩形，透明模式之外的所有背景模式都受影响。
- 影响：`tools/design/image-rounded-corners.html`；用户以为得到圆角成品，实际交付仍带方角，且默认透明模式掩盖了该问题。
- 方案：先构造圆角路径并在填充背景前 `clip`，或在导出前按同一路径清除角外像素；纯色/渐变模式下导出仍保持角外透明（或明确提供「填满角外」开关）。

### D-N25 SVG 转 PNG 声明「保持长宽比」但实现为强制拉伸（低，确认源码缺陷）
- 问题：公式引据表写「输出像素宽 = viewBox 宽 x 缩放倍率，保持长宽比」，实际直接 `drawImage(img, 0, 0, w, h)`，宽高独立生效；目标尺寸与原图比例不同即变形。
- 证据：`tools/design/svg-to-png.html:225`（引据表文案）、`:256-257`（宽高各自读取）、`:270`（四参数拉伸绘制）。复现输入：64×64 的正方形 SVG 配 400×200 输出 → 图形被横向拉伸为 2:1。
- 影响：`tools/design/svg-to-png.html`；按页面说明按比例放大时会得到变形图，尤其影响图标/Logo 出图。
- 方案：默认按 `viewBox`/SVG 固有比例做 contain 适配并留白，另提供「拉伸铺满」选项；公式表与预览尺寸说明同步修正。

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
