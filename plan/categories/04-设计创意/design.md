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
