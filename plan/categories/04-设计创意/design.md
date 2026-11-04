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

## 2026-11-03 续查（并行批 K）

> 本轮实读 8 页：`color-picker.html`、`color-palette.html`、`color-shade-generator.html`、`vh-vw.html`、`css-grid-generator.html`、`image-cropper.html`、`image-format-converter.html`、`favicon-generator.html`。仅源码静态阅读 + node 内存复算（临时脚本 `/private/tmp/k_audit.js`，已删除），未开浏览器、未做 EN/移动端/门禁/线上验证。

### D-N26 图片裁剪器换图或改参数后仍下载上一张的旧裁剪（高，确认源码缺陷）
- 描述：`lastURL` 只在点「裁剪」时更新；换图、改 X/Y/宽/高都不会失效，而「下载 / 复制 Base64」直接取 `lastURL`。换图后预览已显示新原图，用户会以为下载的是新图。
- 证据：`tools/design/image-cropper.html:253`（`let origImg=null,lastURL=''`）、`:254-269`（换图只换预览、未清 `lastURL`）、`:270-285`（仅 `generate()` 写 `lastURL`）、`:287-294`（下载/复制直取 `lastURL`）
- 复现：上传 A.png → 点「裁剪」→ 下载得 A 的裁剪；再上传 B.png（预览已变 B）→ 不点裁剪直接「下载」→ 落盘仍是 A 的裁剪；改宽度后不点裁剪直接下载 → 尺寸仍是旧值
- 影响：静默导出错误文件，且页面无任何「结果已过期」提示；与 D-N22（换图后仍下载旧翻转）同族，但落在新页面
- 方案：换图时 `lastURL=''` 并清空结果预览；`cx/cy/cw/ch` 的 `input` 事件即失效 `lastURL`；或下载前比对参数快照并提示「请先重新裁剪」

### D-N27 CSS Grid 生成器「列宽方式」下拉框为空，固定/auto 模式不可达（中，确认源码缺陷）
- 描述：`<select id="coltype">` 标签内无任何 `<option>`，也无脚本填充；取值恒为空串，经 `||'fr'` 回落后永远走 `repeat(n, 1fr)`。`resetForm` 的 `selectedIndex=0` 在空 select 上同样无效。
- 证据：`tools/design/css-grid-generator.html:136`（空 select）、`:273`（`coltype.value||'fr'`）、`:276-278`（fixed/auto 分支永不可达）、`:305`（selectedIndex 无效）
- 复现：打开页面 → 下拉框空白不可选；任意列数生成的 CSS 恒为 `grid-template-columns: repeat(3, 1fr)`；全文件检索无 `<option>`
- 影响：页面简介与公式框（`:118`、`:122-123`）宣称可选「固定 / fr / auto」，实际只有 fr；想生成 `repeat(n, 120px)` 的用户无法完成
- 方案：补 `fr / fixed / auto` 三个 option 并绑定 `onchange=calcTool()`；`fixed` 的 120px 改为可编辑输入（当前硬编码在 `:276`）

### D-N28 CSS Grid 生成器 HTML 结构恒为 3 个子项，与列数无关（中，确认源码缺陷）
- 描述：HTML 代码段硬编码 `1、2、cols` 三个子元素，`cols=12` 时仍只给 3 个，且第三个直接写列号 `12`，复制后布局数量与列数不符。
- 证据：`tools/design/css-grid-generator.html:280`
- 复现：列数 12 → 「HTML 结构」输出 `<div>1</div><div>2</div><div>12</div>`（3 个），粘贴到 12 列网格只占 3 格；列数 2 时反而输出 1、2、2 三个
- 影响：复制即用的产物本身就是错的，需用户自行补 9 个 div
- 方案：按 `for(let i=1;i<=cols;i++)` 生成子项；或只输出 1 个示例 div + 注释「共 n 个」

### D-N29 CSS Grid 生成器 gap 负值/超范围不拦截，生成无效 CSS 与负 padding（低，确认源码缺陷）
- 描述：`min=0 max=80` 只约束数字输入的 spinner，脚本不做校验；负 gap 直接拼进 `gap` 与 `padding:0 (gap/2)px`，两条声明均非法。
- 证据：`tools/design/css-grid-generator.html:132`（min/max 属性）、`:273`（无 clamp）、`:279`（`gap: -10px` + `padding: 0 -5px`）、`:283`（预览同样使用负值）
- 复现：gap=-10 → 输出 `gap: -10px;` 与 `padding: 0 -5px;`，浏览器丢弃 padding 声明，预览与复制代码均失效；gap=500 超过 max=80 仍照用
- 方案：`gap = Math.max(0, Math.min(80, num('gap')))` 并回写输入框；非法时给错误提示

### D-N30 视口单位转换：基准空/0/负值静默按 1920 计算，输入框不回写（中，确认源码缺陷）
- 描述：`base<=0` 时直接把局部变量改成 1920，输入框仍显示 0/空，提示语却按 1920 说明，用户无法察觉基准被替换。
- 证据：`tools/design/vh-vw.html:126`（基准输入）、`:230`（`if(base<=0){base=1920}`）、`:232-235`（输出与 tip）
- 复现：基准清空 + 数值 100 + 「px → vw」→ 输出 `5.2083vw`，提示「按视口宽度 1920px 计算」，输入框仍为空（node 复算一致）
- 影响：得到看似合理但基准错误的结果，直接用于真实视口的自适应布局会偏差数倍；`val` 负值也原样透传（-100 → `-5.2083vw`）
- 方案：base<=0 时报错并中止；确要兜底则回写 1920 到输入框；`val` 增加数值/非负校验

### D-N31 取色器 H/S/L/RGB 越界或清空静默截断，且不回写输入框（中，确认源码缺陷）
- 描述：`clampInput` 对非有限值返回 `min`，越界值四舍五入到边界；`update()` 又刻意跳过正在聚焦的输入框回写，导致框内显示值与实际颜色不一致。
- 证据：`tools/design/color-picker.html:578-581`（onHslInput）、`:584-587`（`clampInput`，非法值→min）、`:504-506`（只回写非 activeElement）、`:589-596`（RGB 同路径）
- 复现：H 输入 400 → 内部 `state.h=360`（实际色相 0°，红色），输入框仍显示 400；S 输入 -20 → 0；L 清空 → 0（页面立即变纯黑）；RGB 输入 300 → 255 但框内仍 300
- 影响：所见非所得，用户按框内数值记录设计稿会完全对不上；清空中间态直接黑屏且无提示
- 方案：非法/越界时拒绝更新并标红提示；确需 clamp 则强制回写该输入框；空值保留上一次有效值

### D-N32 取色器 HEX 非法输入无提示，结果静默停留旧值（低，确认源码缺陷）
- 描述：`onHexInput` 只在解析成功时更新，失败无 else 分支；`hexToRgb` 仅接受 3/6 位，8 位 `#RRGGBBAA` 也判为非法，用户无从得知输入未被采纳。
- 证据：`tools/design/color-picker.html:567-575`（无失败分支）、`:428-437`（长度与 NaN 校验）
- 复现：输入 `#12345`/`#ggg`/`#11223344` → 预览、HEX/RGB/HSL 行、对比度、和声色全部停留在上一个颜色，输入框保留非法串
- 方案：失败时加 `aria-invalid` + 红框与「HEX 需 3 或 6 位」提示；顺带支持 8 位含透明度

### D-N33 配色生成器 HEX 只校验长度不校验字符，非法字符产出 `#NaNNaNNaN` 色板（中，确认源码缺陷）
- 描述：`hexToRgb` 用 `parseInt` 但不查 `isNaN`；NaN 数组是真值，输入处理器的 `if(rgb)` 校验形同虚设，最终经 `NaN.toString(16)="NaN"` 拼出非法色值。
- 证据：`tools/design/color-palette.html:311-316`（无 NaN 校验）、`:318-320`（`padStart(2)` 遇 "NaN" 得 3 字符）、`:513-522`（`if(rgb)` 放过 NaN 数组）
- 复现：输入 `#gggggg` → 6 个色块 hex 全为 `#NaNNaNNaN`、`background` 样式失效、RGB/HSL 行显示 `NaN`（node 复算：`hexToRgb → [NaN,NaN,NaN]`，`hsl → NaN,NaN,NaN`）
- 影响：色板整组报废且无报错，用户可能把 `#NaNNaNNaN` 复制进设计稿
- 方案：`hexToRgb` 增加 `/^[0-9a-fA-F]{3}$|^[0-9a-fA-F]{6}$/` 校验并对 NaN 返回 null；输入框失败时红框提示

### D-N34 明暗色阶：档数无上下限，清空即 1 档，超大值生成海量卡片（中，确认源码缺陷）
- 描述：`steps` 输入无 min/max，脚本用 `Math.max(1, Math.floor(...))` 兜底，0/空/负值都变 1；同时没有上限，上千档会一次性拼出 2n+1 张卡片。
- 证据：`tools/design/color-shade-generator.html:125`（无 min/max）、`:223`（`Math.max(1, Math.floor(num('steps')))`）、`:225-227`（双循环拼 innerHTML）
- 复现：steps 清空或填 0 → 输出 3 张卡（1 亮 + 基色 + 1 暗），输入框仍为空；steps=1000 → 2001 张卡片 + 2001 次字符串拼接，页面卡死（node 复算：steps=5 得 11 档）
- 方案：clamp 1–20 并回写输入框；超出范围显式提示，禁止无上限生成

### D-N35 明暗色阶文档称「OKLCH/HSL 推明度、50~900 共 10 档」，实际线性 RGB 且档数随输入（低，确认源码缺陷）
- 描述：deep-dive 与公式说明两处口径均与实现不符：实现是 `C·(1−t) + 白/黑·t` 的线性 RGB 混合，没有 HSL/OKLCH 明度阶梯，也没有 50/100/…/900 的命名与固定 10 档。
- 证据：`tools/design/color-shade-generator.html:106-107`（公式即线性混色）、`:225-227`（档数=`steps`，总卡片=`2n+1`）、`:373`（「在 OKLCH/HSL 上推明度梯度」「共 10 档」）、`:376`（「按感知均匀色彩空间推更自然」）
- 复现：steps=5 → node 复算得 11 档（`#ffe6dd → #2b1209`），并非 50–900 十档；输出里也没有 50/100 之类 token 名
- 方案：文案改为「线性 RGB 混色、每侧 n 档共 2n+1 档」；或真的实现 HSL/OKLCH 明度阶梯与 50–900 命名，使文档与产物一致

### D-N36 明暗色阶把 4 位 HEX 当 6 位解析，第三通道变 NaN（低，确认源码缺陷）
- 描述：`h2r` 只展开 `length===3`，长度 4/5/7 一律按 6 位 `substr` 取通道，缺位补 `NaN`。
- 证据：`tools/design/color-shade-generator.html:216`
- 复现：输入 `#abcd` → `[171, 205, NaN]`，首档色卡为 `#abc...NaN`，背景与文字色失效（与 D-N33 同族，但落在此页且为长度分支缺失）
- 方案：仅接受 3/6 位（含 `#` 可选），其余长度直接报错

### D-N37 图片格式转换器改尺寸/质量后不清旧结果，下载仍是旧尺寸文件（中，确认源码缺陷）
- 描述：只有「切换格式」会清空 `state.results`（源码注释自证这一意图），改质量、改尺寸模式、改自定义尺寸都不清空，下载按钮继续指向上一次转换的 blob。
- 证据：`tools/design/image-format-converter.html:917-919`（仅格式变更清结果）、`:930-934`（质量变更不清）、`:936-944`（尺寸模式不清）、`:946-955`（自定义尺寸不清）、`:981-987`（只有「开始转换」才重置）
- 复现：转换一张 4000×3000（保持原尺寸）→ 切到「按比例缩放 50%」→ 界面显示 50%，不点转换直接「下载」→ 落盘仍是 4000×3000 旧文件
- 影响：静默导出错误尺寸，且与页面「改格式即失效」的处理不成体系
- 方案：质量/尺寸/尺寸模式变更同样 `state.results=[]`、禁用下载按钮，直到重新转换

### D-N38 图片格式转换器比例与自定义尺寸非法值静默兜底（低，确认源码缺陷）
- 描述：`parseInt(...)||100` 让 0 与空值回落到 100%；负比例使宽高为负，随后被 `Math.max(1, ...)` 夹成 1×1；自定义尺寸为 0 时静默忽略。
- 证据：`tools/design/image-format-converter.html:998-1005`（`if(cw>0)`、`pct||100`）、`:1008-1010`（`Math.max(1,w/h)`）
- 复现：percentScale=-50 → canvas 1×1，无任何报错；清空比例 → 按 100% 原尺寸；customWidth=0 → 不缩放
- 方案：按 1–1000 校验并提示，负值/0 直接报错；1×1 兜底改为显式失败提示

### D-N39 Favicon 生成器 meta/OG 与公式说明宣称「一键下载 .ico」，实际只导出 PNG（中，确认源码缺陷）
- 描述：页面 meta description、OG description、公式说明与 deep-dive 四处均写 `.ico` 可下载/可打包，但同页正文与 FAQ 又承认「纯前端无法生成真 ICO」「本工具导出 PNG」，文案自相矛盾且宣称的能力不存在。
- 证据：`tools/design/favicon-generator.html:10`、`:15`（description「一键下载 .ico 适配各浏览器」）、`:265`（formula-desc「打包为 .ico」）、`:313`（deep-dive「ICO 与 PNG 套装可下载」）对照 `:263`（「纯前端无法生成真 ICO」）、`:689`（FAQ「本工具导出 PNG」）
- 影响：搜索结果与分享卡片承诺 ICO，用户下载只得到 PNG；信任损耗，且属于对外元数据错误
- 方案：四处统一改为「导出多尺寸 PNG」；如确需 ICO，前端手写 ICO 容器（PNG-in-ICO 可行）或在页内给出明确的外部转换指引

### D-N40 Favicon 生成器字号无脚本校验，负值使字体声明失效、超限直接裁切（低，确认源码缺陷）
- 描述：`fontSize` 的 `min/max` 只约束 spinner；脚本用 `parseInt(...)||140`，负值会拼成非法的 `ctx.font`（被浏览器忽略、退回默认字体），超过上限则在固定画布内溢出裁切，且无 `measureText` 自适应。
- 证据：`tools/design/favicon-generator.html:215`（min=40/max=240）、`:470`（`parseInt(...)||140`）、`:397-400`（`ctx.font` 直接拼接、`fillText` 无测量/缩放）
- 复现：fontSize=-50 → `"bold -3.125px ..."` 非法赋值被丢弃，文字退回默认 10px（@16px 画布）；fontSize=300 → @16px 每字 18.75px，两枚汉字宽 37.5px > 16px，被裁切；输入 0 → 静默变 140
- 方案：clamp 40–240 并回写；按 `measureText` 自动缩放（或对 16/32px 档单独降级字号），避免多字符被裁

### D-N41 明暗色阶输入区 `</div` 缺右尖括号，疑似吞掉工具栏容器（低，疑似）
- 描述：`</div` 未闭合，其后紧跟 `<div class="toolbar">`；按 HTML 解析规则，残缺 end tag 会把后续起始标签吞为属性，`toolbar` 容器可能整体丢失，按钮样式与布局错位。
- 证据：`tools/design/color-shade-generator.html:127`
- 复现：静态读源码可见 `:127` 为 `    </div`；预期应为其后的 `</div>` 正常闭合输入行，但实际缺失 `>`（未开浏览器确认渲染差异）
- 方案：补成 `</div>`；顺带跑一次标签配对检查（同类残缺 end tag 可全站扫一遍）

- 本轮实读 8 页：`color-picker.html`、`color-palette.html`、`color-shade-generator.html`、`vh-vw.html`、`css-grid-generator.html`、`image-cropper.html`、`image-format-converter.html`、`favicon-generator.html`；另略读 `border-radius-generator.html`、`flexbox-generator.html`（后者 gap 负值问题与 D-N29 同族，未单列）。新增 16 条（高 1 / 中 8 / 低 7）。未覆盖：`tools/design` 其余约 86 页（含 gradient / shadow / pattern / avatar / badge / image-color-picker / palette-extractor / image-to-ascii 等尚未阅读）。所有结论均为源码行号 + node 内存复算推演，未做浏览器交互、EN 运行态探针、移动端、门禁与线上验证。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页：`tools/design/font-pairing.html`、`tools/design/gradient.html`、`tools/design/shadow-generator-advanced.html`、`tools/design/badge-generator.html`、`tools/design/card-generator.html`、`tools/design/avatar-generator.html`、`tools/design/image-color-picker.html`、`tools/design/svg-viewer.html`。仅源码 + node 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

### D-N42 SVG 查看器把用户输入原样写入 innerHTML，内嵌事件处理器可执行（高，确认源码缺陷）
- 描述：`generate()` 只用 `/svg[\s\S]*<\/svg>/i` 判断“像不像 SVG”，随后把整段输入赋给 `preview.innerHTML`；未移除 `on*` 事件属性、`<script>`、`foreignObject` 或外部引用，也没有用沙箱 iframe。通过 innerHTML 插入的 SVG 事件属性会正常注册，`<svg onload="…">` 在解析完成时即执行。页面自己的引据表还写着「SVG 可内嵌脚本，外部文件须隔离渲染以防注入」，实现与声明相反。
- 证据：`tools/design/svg-viewer.html:255-256`（`preview.innerHTML=__h1`）、`:250-262`（无任何清洗）、`:231-233`（OWASP 隔离引据）
- 复现：粘贴 `<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)"></svg>` → 点「渲染」→ 脚本执行并弹窗；粘贴 `<svg><image href="https://evil.example/x.png"/></svg>` → 页面直接向外部发请求（按 innerHTML/SVG 事件语义推演，未实测）
- 影响：`tools/design/svg-viewer.html`；从不可信来源复制/下载的 SVG 可在本站源执行脚本、读取 localStorage（收藏与历史）并发起外链请求，属于渲染型注入
- 方案：改用 `<iframe sandbox>`（不授予 `allow-scripts`）渲染；或 DOMParser 解析后按白名单清洗（移除 `on*`、`script`、`foreignObject`、外部 `href`/`xlink:href`），含脚本/事件属性时明确拒绝

### D-N43 头像生成器从历史恢复时下载上一张旧图且不重绘（中，确认源码缺陷）
- 描述：历史恢复回调先把记录写回输入框，然后直接调 `downloadImg()`，既没有先 `generate()`，导出也仍取旧 `lastURL`；恢复后预览不更新，并立即触发一次浏览器下载。
- 证据：`tools/design/avatar-generator.html:439-452`（`:450` 直接 `downloadImg()`）、`:262-357`（只有 `generate()` 刷新 `lastURL` 与预览）、`:359-363`（`downloadImg` 只判断 `lastURL` 非空）
- 复现：种子 A、大小 80 生成头像 → 改成种子 B 生成（预览与 lastURL 均为 B）→ 在历史里点回 A 的记录 → 输入框显示 A、预览仍是 B，下载落盘的也是 B 的 PNG（期望：按 A 重绘并只在用户点「下载」时导出）
- 影响：`tools/design/avatar-generator.html`；历史功能静默导出与当前参数不符的文件，且每次恢复都产生一次意外下载
- 方案：恢复末尾改调 `generate()`；导出保持用户显式触发；恢复期间禁用下载直至重新生成

### D-N44 高级阴影「+ 添加层」后预览与 CSS 不更新（中，确认源码缺陷）
- 描述：`addLayer()` 只 push 新层并 `renderLayers()`，没有调用 `generate()`；新增层默认参数不会进入预览和 `cssOutput`，直到用户再改任一输入或点「生成」。`removeLayer()` 已调用 `generate()`，二者行为不一致。
- 证据：`tools/design/shadow-generator-advanced.html:169`（按钮 `onclick="addLayer()"`）、`:273-276`（addLayer 内无 generate）、`:277-282`（removeLayer 有 generate）、`:283-293`（generate 才渲染）
- 复现：初始 3 层 → 点「+ 添加层」→ 行数变 4，预览与 CSS 仍只有 3 条阴影（期望 4 条）
- 影响：`tools/design/shadow-generator-advanced.html`；用户以为新增层已生效，复制得到的 CSS 少一层
- 方案：`addLayer()` 末尾调用 `generate()`，与 `removeLayer` 对齐

### D-N45 高级阴影清空/负模糊生成 `NaNpx`，整条 box-shadow 失效（中，确认函数缺陷）
- 描述：每层 x/y/blur/spread 直接 `parseFloat(this.value)`，清空得 `NaN`；alpha 同样 parseFloat 且脚本未使用 `min/max`。`generate()` 不做有限性/范围检查就拼进 CSS。`NaNpx`、`rgba(...,NaN)` 均为非法值，浏览器会丢弃**整条** `box-shadow`（不是只丢一层）。
- 证据：`tools/design/shadow-generator-advanced.html:263-268`（oninput 直接 parseFloat，alpha 仅声明 `min=0 max=1`）、`:284-292`（模板拼接并写 `cssText`）
- 复现（node 复算原表达式）：第 1 层 X 清空 → `box-shadow: NaNpx 4px 20px -4px rgba(0,0,0,0.25), …;`；Alpha 清空 → `rgba(0,0,0,NaN)`；Blur 填 -20 → `-20px` 模糊（规范要求非负，整条声明无效）。期望：提示非法值并停止输出
- 影响：`tools/design/shadow-generator-advanced.html`；复制到项目后阴影完全消失，页面预览同步失效且无提示
- 方案：数值入口统一 `Number.isFinite` 校验（blur/spread 负数按规范提示），alpha clamp 到 0–1 并回写输入框；非法时清空输出并提示

### D-N46 图片取色器忽略 alpha，透明/半透明像素取色与画面所见不一致（中，确认源码缺陷）
- 描述：预览把图片放在白底容器上显示，但取样 canvas 是透明画布，`getImageData` 只取 `data[0..2]` 丢掉 alpha。半透明像素画面显示的是与白底混合后的颜色，报告值却是未混合的原始通道；全透明像素报告 `#000000`。
- 证据：`tools/design/image-color-picker.html:29`（`.preview-area{background:#fff}`）、`:269-272`（新建透明 canvas 直接 `drawImage`）、`:292-294`（只读 RGB 三通道）
- 复现：上传 50% 透明度的纯红 PNG（`rgba(255,0,0,0.5)`）→ 画面接近 `#FF8080`，HEX 输出 `#FF0000`；全透明区域点选 → 画面白色但输出 `#000000`（期望按显示合成结果取色，或显式输出 RGBA 并标注）
- 影响：`tools/design/image-color-picker.html`；对带透明的 PNG/WebP/图标取色时，复制出的色值与肉眼所见不符
- 方案：取样前先填白（或提供可选底色）再 drawImage，使取样与预览一致；或输出 `rgba(r,g,b,a)`，`a<255` 时标注透明度，全透明像素给出明确提示

### D-N47 徽章生成器把文字原样拼进 innerHTML，可注入 HTML/事件（中，确认源码缺陷）
- 描述：`text` 未转义就拼进 `<span style=...>${text}</span>`，再整体赋给 `preview.innerHTML`；输入含标签时会被当 HTML 解析，`<img onerror>` 等事件可执行。
- 证据：`tools/design/badge-generator.html:261`（读取 text）、`:270/273/276/279`（模板内插 text）、`:281`（`preview.innerHTML=__h0`）
- 复现：文字填 `<img src=x onerror=alert(1)>` → 预览插入图片并在加载失败时执行脚本（期望按纯文本显示）；填 `</span><svg onload=…>` 同理
- 影响：`tools/design/badge-generator.html`；与 D-N42 同属渲染型注入，徽章文字常从工单/表格粘贴，脚本可读取本站 localStorage
- 方案：预览用 `textContent` 创建文本节点，或先做 HTML 转义（`& < > " '`）；CSS 输出中的文字不进 CSS，无需处理

### D-N48 CSS 渐变生成器 FAQ 宣称「会算 WCAG 对比度并标红」，页面未实现（低，确认文案与实现不一致）
- 描述：FAQ 第二条写明「会按 WCAG 算出对比度值与等级，未达标会标红提醒」，但脚本只有色标拼接与预设，没有任何亮度/对比度计算或提示 UI。
- 证据：`tools/design/gradient.html:241`；对照 `:348-369`（`updateGradient` 只排序色标、拼 CSS 并应用背景），全文无 `luminance/contrast` 实现。同模板问题也出现在 `tools/design/image-color-picker.html:213`
- 复现：选两个几乎相同的色（`#FFFFFF` 与 `#FEFEFE`）→ 页面无任何对比度或警告（期望按 FAQ 给出 1.0:1 与未达标提示）
- 影响：`tools/design/gradient.html`、`tools/design/image-color-picker.html`；用户据 FAQ 以为有可读性校验，实际没有，属对外承诺不实
- 方案：实现 WCAG 相对亮度与对比度并对相邻色标提示；或删除该 FAQ 条目

### D-N49 图片取色器元数据与简介宣称「放大取样」，实际无放大/放大镜功能（低，确认能力缺口）
- 描述：description/OG/twitter/正文英文均写「magnified sampling / 支持放大取样」，脚本只有点击取单像素，没有缩放视图、放大镜或像素网格。
- 证据：`tools/design/image-color-picker.html:10`、`:15`、`:68`、`:164`；脚本 `:284-301` 仅 `getBoundingClientRect` + `getImageData`
- 复现：上传 16×16 图标 → 页面按原尺寸显示，点击只能取到单个像素色，无法放大定位
- 影响：`tools/design/image-color-picker.html`；小图标/细节图取色精度无法保证，宣传的卖点不存在
- 方案：增加放大镜（hover 显示 5×5/9×9 像素网格与坐标）或删除「放大取样」表述

### D-N50 卡片生成器负数/空值不校验，输出 padding/border/blur 非法声明（低，确认源码缺陷）
- 描述：各数值 `parseInt(...)||0`、`parseFloat(...)||0`，仅空值兜底；`min/max` 只约束 spinner。负内边距、负边框宽、负模糊、负圆角都会原样拼进 CSS，这些属性对负值非法，浏览器丢弃对应声明，但输出文本仍可被复制。
- 证据：`tools/design/card-generator.html:165-175`（min/max 属性）、`:266-281`（无 clamp 并原样写入输出）
- 复现（node 复算）：圆角 -5、内边距 -20、边框粗细 -1、阴影模糊 -20 → `border-radius: -5px; padding: -20px; border: -1px solid …; box-shadow: 0 4px -20px rgba(0,0,0,0.08);`；阴影不透明度 -0.2 → `rgba(0,0,0,-0.2)` 被钳到 0，阴影实际消失
- 影响：`tools/design/card-generator.html`；粘贴后卡片样式部分失效，且无任何错误提示
- 方案：统一 clamp（radius/pad 0–50、borderW 0–5、alpha 0–1、blur≥0）并回写输入框；越界时高亮字段

### D-N51 字体搭配只有拉丁字体与拉丁示例，中文场景无法预览也无 CJK 回退（低，确认能力缺口）
- 描述：FAQ 专门回答「中文怎么配」，但 36 组搭配（35 种字体）全部是 Google Fonts 拉丁字体，预览文本默认英文，CSS 产物也只输出 `font-family:'X', sans-serif`，没有中文字体或 CJK 回退；中文标题会静默落到浏览器默认中文字体，与预览观感完全不同。
- 证据：`tools/design/font-pairing.html:268`（FAQ 中文问题）、`:322-370`（FONT_PAIRS 全拉丁字体）、`:433-446`（copy CSS 只含拉丁 + sans-serif）、`:416-417`（默认英文字样）
- 复现：标题输入「中文标题测试」→ 卡片仍以拉丁字体渲染中文（实际由系统中文回退）；复制 CSS 到中文站点后标题字体与预览不一致
- 影响：`tools/design/font-pairing.html`；中文用户按 FAQ 使用会得到与预览不符的实际效果
- 方案：增加 `"Noto Sans SC"`、`"Noto Serif SC"` 等 CJK 字体并输出中英文双字体栈；FAQ 明确说明中文由系统回退或补中文字体分类

- 本轮实读 8 页：`font-pairing.html`、`gradient.html`、`shadow-generator-advanced.html`、`badge-generator.html`、`card-generator.html`、`avatar-generator.html`、`image-color-picker.html`、`svg-viewer.html`；新增 10 条（高 1 / 中 5 / 低 4）；未覆盖：`tools/design` 其余约 71 页（含 `palette-extractor.html`、`image-to-ascii.html`、`gradient-from-color.html`、`mesh-gradient.html`、`shadow-generator.html`、`pattern-generator.html`、`identicon-generator.html`、`initials-avatar.html`、`css-box-shadow-generator.html` 等）。所有结论均为源码行号 + node 内存复算/源码路径推演；SVG/HTML innerHTML 注入与 Canvas 透明取样为静态语义推演，未做浏览器交互、EN 运行态探针、移动端、门禁与线上验证。
- 补记（未单列编号，属 K 批略读页的复核）：`tools/design/border-radius-generator.html:387` 历史恢复调用无参 `setUniform()`，`:267-273` 会把四角输入写成字符串 `"undefined"`，`:284` 的 `generate()` 因 `value || 0` 判真而输出 `border-radius: undefinedpx;`；本批仅复核该路径，未计入上方 10 条。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页：`tools/design/button-generator.html`、`tools/design/text-shadow-generator.html`、`tools/design/css-animation-generator.html`、`tools/design/skeleton-loader.html`、`tools/design/palette-extractor.html`、`tools/design/image-to-ascii.html`、`tools/design/mesh-gradient.html`、`tools/design/pattern-generator.html`。仅源码 + node 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

### D-N52 按钮生成器悬停态无法预览，负值/小数被静默写入 CSS（中，确认源码缺陷，两个问题）
- 描述：预览按钮 `<button id="previewBtn">` 不带 `.btn-custom` 类，`generate()` 只把样式写成 inline `cssText`，而 `:hover` 规则只存在于输出文本里；inline 样式无法被伪类命中，页面宣称的「悬停态实时预览」实际不生效。另所有数值走 `parseInt(...)||0/14`，负值原样拼入，小数被截断且不回写输入框。
- 证据：`tools/design/button-generator.html:180`（预览按钮无 class）、`:278-282`（inline cssText + 输出 `:hover`）、`:265-274`（`parseInt(...)||0`，仅 `fontSize` 用 `||14`）、`:213`（FAQ 称悬停可直接用）
- 复现（node 复算原表达式）：圆角 `-5`、水平内边距 `-20`、边框 `-1`、阴影模糊 `-20` → 输出 `border-radius: -5px; padding: 10px -20px; border: -1px solid …; box-shadow: 0px 4px -20px …`（期望拒绝并提示）；圆角 `8.5` → 按 8 生成，输入框仍显示 8.5；鼠标移入预览按钮无任何位移/阴影变化（期望看到 `translateY(-2px)` 与阴影变化）
- 影响：`tools/design/button-generator.html`；复制出的负值声明会被浏览器整条丢弃，且用户在页面上永远看不到 hover 效果，交付前必须自行贴回项目验证
- 方案：预览按钮加 `.btn-custom` 并把规则写进 `<style>`（不要用 inline cssText），或让 `:hover` 选择器指向 `#previewBtn`；数值统一 clamp/校验后回写，非法时标红并停止输出

### D-N53 文字阴影负模糊生成整条非法声明，预设模式不会因手改参数退出（中，确认源码缺陷）
- 描述：`blur` 的 `min=0` 只约束 spinner，脚本用 `parseInt(...)||0`，负值原样进入 `text-shadow`；`text-shadow` 的 blur 必须非负，负值会让整条声明失效（不是只丢一层）。同时手动改 X/Y/模糊后 `preset` 下拉仍停在「3D 立体/霓虹」等模式，输出继续按多层生成。
- 证据：`tools/design/text-shadow-generator.html:288-289`（`parseInt(blur)||0` 直接拼接）、`:290-301`（按 `preset.value` 继续多层分支）、`:161-163`（输入 min/max 未参与脚本）、`:166`（预设 select）
- 复现（node 复算原表达式）：模糊 `-4` → `text-shadow: 2px 2px -4px #000000`（期望提示并停止）；模糊清空 → `0px` 静默；`2.5` → 按 2 计算而输入框仍 2.5。选「3D 立体」后把 X 从 3 改成 6，下拉仍显示「3D 立体」，输出仍是 5 层而非基础阴影
- 影响：`tools/design/text-shadow-generator.html`；复制到项目后文字阴影完全不出现；预设状态与产物不一致，用户无法判断当前是否为自定义模式
- 方案：blur 必须为 0–50 的有限数，非法时清空输出并提示；X/Y/模糊任一被手改时把 `preset` 重置为「自定义」

### D-N54 CSS 动画自定义 cubic-bezier 的 x 越界不校验，整条 animation 失效（中，确认源码缺陷；浏览器丢弃行为按规范推演）
- 描述：`getEasingValue()` 对四个控制点统一 `parseFloat(...)||0`，没有检查 x1/x2 必须落在 0–1；输入框 `min=0 max=1` 只约束 spinner，手输负值或 >1 可通过。CSS Easing 规范要求 x 分量在 [0,1]，越界时浏览器丢弃整条 `animation` 声明。
- 证据：`tools/design/css-animation-generator.html:855-865`（`parseFloat(...)||0` 与直接拼接）、`:476-479`（bx1/bx2 `min=0 max=1` 未参与脚本）
- 复现（node 复算原表达式）：`bx1=-0.5`、其余默认 → `cubic-bezier(-0.5, -0.55, 0.265, 1.55)`（期望拒绝/夹取并提示）；清空 `bx1` → 静默按 0；`bx1` 输入 `1e2` → 100，同样越界
- 影响：`tools/design/css-animation-generator.html`；预览不动、复制出的 CSS 动画不播放，且没有任何错误提示，用户只会以为浏览器不支持
- 方案：x1/x2 限定 0–1 并回写输入框，y 允许 -1–2；非法时标红并清空预览/代码，或把越界值 clamp 后明确提示

### D-N55 骨架屏圆角 0 被改成 4、时长 0 被改成 1.4，负时长生成非法动画（中，确认源码缺陷）
- 描述：`duration` 用 `parseFloat(...)||1.4`、`radius` 用 `parseInt(...)||4`，把合法的 0 当空值替换；负值（`-3`）则原样通过并拼进 `animation`。输入框不回写也不提示。
- 证据：`tools/design/skeleton-loader.html:268-269`（两处 `||` 兜底）、`:271`（直接拼 `animation: skelLoading ${dur}s`）、`:174-175`（min/max 未参与脚本）
- 复现（node 复算原表达式）：圆角 `0` → `border-radius: 4px`（期望直角 0）；动画速度 `0` → `1.4s`；`-3` → `animation: skelLoading -3s ease infinite`（负时长非法，动画不播放）；`2.5` → `parseInt` 得 2
- 影响：`tools/design/skeleton-loader.html`；想关闭圆角或暂停 shimmer 的用户拿不到预期结果，负值则预览与复制产物同时失效
- 方案：改用显式空值/NaN 判断（不要用 `||`），`duration>0`、`radius>=0`，越界回写输入框并给出提示

### D-N56 调色板提取器改排序后导出代码不刷新，复制/下载仍是旧顺序（中，确认源码缺陷）
- 描述：排序按钮只调用 `sortPalette()` + `renderPalette()`，没有调用 `renderExport()`；导出区文本只在提取、切换格式时重算。用户按色相排序后直接复制/下载，得到的仍是上一次（按频率）的 token 顺序。
- 证据：`tools/design/palette-extractor.html:996-1006`（排序回调无 `renderExport()`）、`:920-955`（`renderExport()` 才写 `exportCode.textContent`）、`:958-969`（复制/下载直接读 `exportCode.textContent`）
- 复现：提取后保持默认「按频率」，导出框为频率顺序 → 点「按色相」，色块网格已按色相重排，但导出框/CSS 变量仍按频率顺序 → 直接点「复制代码」得到旧顺序（期望导出与色块同序）
- 影响：`tools/design/palette-extractor.html`；`--color-1…n` 与界面所见色板对不上，贴进设计系统后命名错位
- 方案：`sortPalette()` 后同时调用 `renderExport()`；或在 `copyExport()/downloadExport()` 内按当前 `state.palette` 重新生成，避免读缓存文本

### D-N57 图片转 ASCII 点历史记录会自动下载当前结果且不重绘（中，确认源码缺陷）
- 描述：历史恢复回调设置完输入后调用的是 `downloadResult()`，而不是 `convert()`；既不会按旧参数重新生成，还会立刻触发一次浏览器下载，且下载内容仍是当前输出（不是历史记录对应的字符画）。
- 证据：`tools/design/image-to-ascii.html:484-498`（`:495` 调 `downloadResult()`）、`:415-424`（`downloadResult` 直接读 `#output`）
- 复现：上传图 → 宽度 100 转换 → 宽度改成 160 再转换 → 在历史里点回宽度 100 的记录 → 输出区仍显示 160 列结果，同时浏览器下载一份 160 列的 txt（期望按 100 列重绘，且只有用户点「下载」才导出）
- 影响：`tools/design/image-to-ascii.html`；历史功能不可用并产生意外下载，与 D-N43 同族
- 方案：历史回调改调 `convert()`；下载保持显式触发，恢复期间禁用下载直至重绘完成

### D-N58 图片转 ASCII 引据表写 BT.709，正文与实现用 BT.601，页面自相矛盾（低，确认文案与实现不一致）
- 描述：引据表明确写 `Y = 0.2126 R + 0.7152 G + 0.0722 B（BT.709 权重）`，但公式说明（`:176`）与实现（`:392`）都是 BT.601 的 `0.299/0.587/0.114`；同一页出现两套权重口径。
- 证据：`tools/design/image-to-ascii.html:280`（BT.709 引据）对照 `:176`（正文写 BT.601）、`:392`（`0.299*r+0.587*g+0.114*b`）
- 复现（node 复算，默认 `detailed` 字符集 `" .:-=+*#%@"` 共 10 档）：纯红 `#FF0000` → 按实现灰度 76.245，`floor(76.245/255*9)=2`，取索引 2 的 `:`；按引据表 BT.709 应为 54.213，`floor(1.913)=1`，取索引 1 的 `.`。同一输入两套标准差一个字符档
- 影响：`tools/design/image-to-ascii.html`；用户按引据表校核字符画明暗时对不上，红/蓝高饱和区域的档位偏差约 1 档
- 方案：保留 BT.601 实现与正文，把引据表改为 BT.601（0.299/0.587/0.114）；或实现改 BT.709 并同步正文与引据。权重常量只保留一处

### D-N59 网格渐变的历史/数据表/预设/CSV 恒为空（中，确认源码缺陷）
- 描述：动态生成的 2–5 个颜色输入框没有 `id`，而历史快照只收集 `input[id]`；同时 `#output` 里的预览块没有文本，`ResText` 判空后直接返回。结果历史从不记录、数据表为空、CSV 导出为空；预设函数本身也是空实现，预设页签无按钮。
- 证据：`tools/design/mesh-gradient.html:255-258`（`<input type="color" value=…>` 无 id）、`:331-339`（`querySelectorAll('input[id]…)`）、`:396-397`（`if(!keys.length) return`）、`:424-426`（`__mesh_gradientPresets()` 空函数）、`:170`（数据表/历史容器）
- 复现：改任一颜色或「+ 添加颜色」「随机」→ 切到「历史」页签始终为空；「数据表」与「导出明细 CSV」同样无内容；「预设」页签无按钮（期望记录颜色组合并可回放）
- 影响：`tools/design/mesh-gradient.html`；三个页签与导出按钮全部形同虚设，用户无法保存/复用调好的配色
- 方案：给动态色块分配稳定 id（如 `color0…color4`），或让 Snap 直接收集 `#colorRow input` 并把 `colors` 数组序列化进记录；补预设条；`ResText` 改用 `cssOutput` 文本

### D-N60 网格渐变宣称「拖拽色标、导出图片」与 WCAG 校验，页面均未实现（低，确认文案与实现不一致）
- 描述：公式说明与简介写「拖拽色标调整各点位置与颜色，导出为图片或 CSS」，实际只有颜色选择与 CSS 文本，没有拖拽控制点、没有图片/Canvas 导出；FAQ 还称会「按 WCAG 算出对比度并标红」，脚本无任何对比度计算（与 D-N48 同模板）。
- 证据：`tools/design/mesh-gradient.html:157`、`:159`（拖拽与图片导出承诺）、`:204`（WCAG 承诺）、`:279-287`（仅按索引计算 x/y 并写 CSS）
- 复现：页面无拖拽手柄、无「导出图片」按钮；选两个近乎相同的色（如 `#667eea` 与 `#687fea`）无任何对比度或警告
- 影响：`tools/design/mesh-gradient.html`；对外承诺的核心交互与导出能力不存在，用户按文案寻找功能会失败
- 方案：删除「拖拽/导出图片/WCAG」表述，或实现控制点拖拽 + Canvas/SVG 导出并补对比度提示

### D-N61 图案生成器「三角形」与「菱形」输出完全相同的 CSS（中，确认源码缺陷）
- 描述：`triangles` 与 `diamonds` 两个分支使用逐字符相同的两条 `linear-gradient(45deg,…)` 模板与相同的 `background-size/position`，选「菱形」得到的仍是三角形平铺图案，六个图案类型里有两个重复。
- 证据：`tools/design/pattern-generator.html:273`（triangles 模板）、`:281`（diamonds 模板，与 273 相同）
- 复现（node 复算同一组参数）：`type=triangles` 与 `type=diamonds`、size 40、同两色 → 两条 CSS 字符串 `===` 为 true，预览像素级一致（期望菱形为 45° 旋转的菱形 tile，或至少与三角形不同）
- 影响：`tools/design/pattern-generator.html`；用户选「菱形」拿不到菱形底纹，且会以为是自己参数没生效
- 方案：把 diamonds 改为真正的菱形构造（如 135°/225° 两组渐变或 `conic-gradient`），并补一条断言「六种类型输出互不相同」

### D-N62 图案生成器尺寸只夹下限，999 直接进入 background-size；类型未写入历史（低，确认源码缺陷）
- 描述：`size` 仅 `Math.max(5, parseInt(...)||40)`，无上限；`max=200` 只约束 spinner。`999` 原样生成 `background-size: 999px 999px`，负值被夹到 5、空值变 40 且不回写。另历史快照不含当前图案类型（`currentType` 不是表单元素），且 `#output` 无文本导致历史恒空（同 D-N59 模板问题）。
- 证据：`tools/design/pattern-generator.html:270`（只有下限夹取）、`:162`（`min=5 max=200` 未参与脚本）、`:392-397`（`ResText` 判空后不记录）、`:260-266`（`currentType` 为全局变量，不入快照）
- 复现（node 复算）：size `999` → 999（期望 200）；`4` → 5；清空 → 40；输入框仍显示 999/空。历史页签与「导出明细 CSV」始终无内容
- 影响：`tools/design/pattern-generator.html`；超大 tile 撑爆预览、参数显示与实际不一致；历史/CSV 功能不可用
- 方案：size clamp 5–200 并回写；历史记录把 `currentType` 与颜色/尺寸一并写入，`ResText` 改用 `cssOutput` 文本

- 本轮实读 8 页：`button-generator.html`、`text-shadow-generator.html`、`css-animation-generator.html`、`skeleton-loader.html`、`palette-extractor.html`、`image-to-ascii.html`、`mesh-gradient.html`、`pattern-generator.html`；新增 11 条（高 0 / 中 8 / 低 3）。未覆盖：`tools/design` 其余约 60 页（按本文件全部 `tools/design/*.html` 引用去重统计，108 个工具页中已引 48 个），代表页含 `glassmorphism-generator`、`neomorphism-generator`、`css-text-shadow`、`css-box-shadow-generator`、`shadow-generator`、`spinner-generator`、`progress-bar-generator`、`toast-generator`、`checkerboard-generator`、`grid-pattern`、`dot-pattern`、`stripe-pattern`、`identicon-generator`、`initials-avatar`、`gradient-from-color`、`pixel-art-generator`、`favicon-from-text`、`favicon-from-emoji` 等。所有结论均为源码行号 + node 内存复算/源码路径推演；未做浏览器交互、EN 运行态探针、移动端、门禁与线上验证。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页：`tools/design/css-box-shadow-generator.html`、`tools/design/css-text-shadow.html`、`tools/design/shadow-generator.html`、`tools/design/glassmorphism-generator.html`、`tools/design/neomorphism-generator.html`、`tools/design/spinner-generator.html`、`tools/design/progress-bar-generator.html`、`tools/design/grid-pattern.html`。仅源码 + node 内存复算（临时命令均在 `/private/tmp`，未落盘），未开浏览器/未做 EN/移动端/门禁验证。

### D-N63 CSS 盒阴影生成器：增删/重置阴影层后预览与 CSS 不刷新（中，确认源码缺陷，与 D-N44 同族）
- 描述：`addLayer / deleteLayer / resetLayers` 都只经 `setActive()`，而 `setActive()` 仅调用 `renderLayerList()`；真正重算 `#preview` 与 `#cssOutput` 的 `render()` 未被调用，层数据已变但产物停留在上一次。
- 证据：`tools/design/css-box-shadow-generator.html:452-456`（addLayer）、`:458-464`（deleteLayer）、`:466-470`（resetLayers）、`:433-450`（setActive，仅 `:449` renderLayerList）、`:410-416`（render 才写预览与 CSS）
- 复现：默认单层 → 点「+ 添加阴影层」→ 层列表出现第 2 层，但 CSS 框仍是 `box-shadow: 0px 10px 20px -5px rgba(0, 0, 0, 0.5);`（期望两层逗号叠加）；点 ✕ 删除一层后 CSS 仍包含被删层，预览不更新
- 影响：`tools/design/css-box-shadow-generator.html`；用户若只看列表后直接复制，得到的是旧层组合；与 D-N44（高级阴影同模板）属同一缺陷扩散，需一并修复
- 方案：三处入口在 `setActive()` 后补 `render()`，或让 `setActive()` 内部统一调用 `render()`；删除/重置后同步刷新收藏按钮状态

### D-N64 CSS 文字阴影生成器：增删/重置阴影层后预览与 CSS 不刷新（中，确认源码缺陷，与 D-N44 同族）
- 描述：与 D-N63 同模板：`addLayer / deleteLayer / resetLayers` 走 `setActive()`，而 `setActive()` 只重绘层列表；`render()` 才写 `textShadow` 与 CSS 文本，故层数量变化不影响预览/代码。
- 证据：`tools/design/css-text-shadow.html:470-474`（addLayer）、`:476-482`（deleteLayer）、`:484-488`（resetLayers）、`:454-468`（setActive 仅 `:467` renderLayerList）、`:432-438`（render）
- 复现：默认单层 → 「+ 添加阴影层」→ 层列表 2 项，CSS 仍是单层 `text-shadow: 2px 2px 4px rgba(0,0,0,0.5);`；删除一层后 CSS 仍保留被删层（期望立即同步）
- 影响：`tools/design/css-text-shadow.html`；复制产物与界面层列表不一致，多层光晕/3D 效果无法通过增删层得到
- 方案：`setActive()` 末尾调用 `render()`，或三个入口各自补 `render()`；补回归用例「加层后 CSS 层数 = 列表项数」

### D-N65 阴影生成器：文字阴影模式仍拼入扩散半径，整条声明非法（高，确认源码缺陷）
- 描述：`buildShadowStr()` 无论模式都输出 `x px y px blur px spread px color` 五参数；切到「文字阴影」后该串被写入 `text-shadow`，而规范中 text-shadow 只有 x/y/blur/color，无 spread，整条声明会被浏览器丢弃。默认 spread 为 -5px，切过去即全失效。
- 证据：`tools/design/shadow-generator.html:393-397`（恒含 `${l.spread}px`）、`:405-411`（text 模式赋给 `preview.style.textShadow` 与 `#code`）、`:200-202`（扩展半径滑杆默认 -5，文字模式未隐藏）、`:183`（模式入口）
- 复现（node 复算原串）：切「文字阴影」→ `text-shadow: 0px 10px 20px -5px #667eea;`（期望 `0px 10px 20px #667eea`）；预览无任何阴影，把扩展半径拖到 0 才短暂出现
- 影响：`tools/design/shadow-generator.html`；页面自述「文字阴影模式支持文本阴影效果」，实际该模式默认不可用，复制结果亦为非法 CSS
- 方案：文字模式下省略 spread（并把 `inset` 与扩展半径一起隐藏/禁用）；切回盒子模式恢复；输出前按模式做参数白名单

### D-N66 阴影生成器删除最后一层后输出空声明，继续操作触发 TypeError（中，确认源码缺陷）
- 描述：`deleteLayer()` 直接 `splice`，没有「至少保留一层」守卫；层为空后 `activeLayer=-1`，`update()` 读取 `getActiveLayer()` 的 `x/y/...` 会抛异常，页面交互中断。
- 证据：`tools/design/shadow-generator.html:454-459`（无长度守卫）、`:366-373`（update 直接解引用 activeLayer）、`:410-411`（空层输出 `box-shadow: ;`）、`:422-428`（空态仅提示文案）
- 复现：仅 1 层时点 ✕ → 列表显示「无阴影层」，CSS 变为 `box-shadow: ;`；随后拖动任一滑杆 → `update()` 抛 `Cannot read properties of undefined`，预览/CSS 不再更新（期望至少保留一层或安全禁用控件）
- 影响：`tools/design/shadow-generator.html`；用户可把自己带进无法继续编辑的状态，只能刷新页面
- 方案：`if(layers.length<=1) return;` 或删除后自动补默认层；`update()` 对无 activeLayer 时直接 return 并提示

### D-N67 玻璃拟态生成器的 12 种背景图案全部不生效（中，确认源码缺陷）
- 描述：`PATTERNS` 存的是纯渐变值（无属性名），但缩略图写成 `style="${p.css}"`、点击时写 `style.cssText = PATTERNS[i].css`，两处都缺少 `background:`；CSSOM 会丢弃无属性名的声明。含 `background-size/position/color` 的第 9–12 项只能应用后半段，仍没有 background-image。
- 证据：`tools/design/glassmorphism-generator.html:341-353`（PATTERNS 值）、`:518`（`style="${p.css}"`）、`:524`（`cssText = PATTERNS[i].css`）、`:578`（启动即 `setPattern(0)`）、`:30`（`.bg-pattern` 无默认背景）
- 复现：打开页面 → `.bg-pattern` 无任何渐变；切到「背景图案」→ 12 个缩略图空白（第 9–12 项只有底色/尺寸）；点任意图案预览背景不变（期望切换紫/日落/海洋/圆点/网格/波浪等底纹）
- 影响：`tools/design/glassmorphism-generator.html`；页面主打卖点「背景图案」完全失效，玻璃面板失去对比背景，预览效果与复制产物脱节
- 方案：缩略图写 `style="background:${p.css}"`；点击写 `'background:'+PATTERNS[i].css`（多声明项拆成 `background-image` 与 `background-size/position/color`，或统一改用 `background` 简写）

### D-N68 新拟态生成器：圆形/按钮与凹陷/浮雕预览无法导出对应 CSS（中，确认源码缺陷）
- 描述：三种形状预览分别用 `.neu-box`（radius px）、`.neu-circle`（border-radius:50%）、`.neu-btn`（50px），并同时展示 convex / pressed(inset) / punch 三种阴影；但导出 CSS 固定为 `border-radius:${radius}px` + `flatShadow`，形状与变体信息全部丢失。
- 证据：`tools/design/neomorphism-generator.html:406-424`（按 currentShape 渲染三形状与三变体）、`:426-430`（唯一导出模板用 radius px 与 flatShadow）、`:30-32`（三形状各自圆角）
- 复现：选「圆形」→ 预览 100×100 圆形，复制 CSS 得 `border-radius: 20px`（方形）；点预览里的「凹陷/浮雕」卡片无任何复制入口，代码始终是 `box-shadow: 6px 6px 12px …`（期望导出与所选形状/变体一致）
- 影响：`tools/design/neomorphism-generator.html`；设计师按圆形按钮调整后复制到项目得到方形卡片，凹/浮雕效果需手改 CSS
- 方案：按 currentShape 选圆角（圆 50%、按钮 50px）；增加「凸起/凹陷/浮雕」变体切换并输出 pressedShadow/punchShadow；或移除无处导出的预览变体

### D-N69 加载动画生成器：预览引用的 keyframes 未定义，五种动画全部静止（高，确认源码缺陷）
- 描述：`generate()` 输出 `spinGen / bounceGen / barsGen / dotsGen`，但页面 `<style>` 只定义了 `spin / scaleB / bars`；生成的 `@keyframes` 仅写入 textarea，从未注入 `<style>`。预览内联 `animation` 引用不存在的动画名，浏览器不会播放。
- 证据：`tools/design/spinner-generator.html:34-38`（页面仅定义 spin/scaleB/bars）、`:273-294`（生成 spinGen/bounceGen/barsGen/dotsGen）、`:297`（只写 `#cssOutput.value`，无样式注入）、`:296`（预览 HTML）
- 复现（node 复算输出串）：任选「边框旋转/双色/弹跳/音波柱/三点」→ 预览完全静止（不旋转、不缩放、无逐点跳动），CSS 文本框内才含对应 `@keyframes`；把文本框内容贴回页面后才动（期望预览即动）
- 影响：`tools/design/spinner-generator.html`；页面所有类型的「实时预览」均失效，用户只能盲选参数再复制
- 方案：生成时把 `css` 注入页面专用 `<style id="spinnerPreviewStyle">`（先清空再写）；或让预览 animation-name 改用页面已定义的 spin/scaleB/bars，并保持尺寸/速度同步

### D-N70 加载动画生成器「音波柱」预览 HTML 重复 style 属性，延迟全部丢失（低，确认源码缺陷）
- 描述：`bars` 用两次 `replace` 拼接（第一次替换 `<div` 为带 `style="…animation-delay:` 的新标签），产生嵌套引号与重复 `style` 属性；第二个正则 `animation-delay:([0-9.]+)s;"></div>` 因中间多了 `style="` 而匹配不到，延迟值被丢弃。
- 证据：`tools/design/spinner-generator.html:283-284`（两次 replace 拼 HTML）、`:286`（CSS 延迟正确）
- 复现（node 复算 `size=40/speed=1`）：输出 `<div style="…animation-delay: style="0s;"></div>` 等 5 个重复 style 属性；浏览器只保留第一个 style，`animation-delay:` 为空值，5 根柱同时起伏（期望 0/0.1/0.2/0.3/0.4s 错开）；CSS 文本框里的 nth-child 延迟反而正确
- 影响：`tools/design/spinner-generator.html`；预览与可复制 CSS 不一致，用户以为参数没生效
- 方案：用数组一次性生成完整标签：`bars += '<div style="width:6px;background:'+color+';animation:barsGen '+speed+'s ease-in-out infinite;animation-delay:'+(i*0.1)+'s;"></div>'`，删除二次 replace

### D-N71 进度条生成器：同时勾选条纹+动画时条纹停滚，百分比被动画忽略（中，确认源码缺陷）
- 描述：预览元素同时带 `progress-striped` 与 `progress-animated` 两个类；两条规则权重相同（`.progress-bar.progress-striped` / `.progress-bar.progress-animated`），后者在后，其 `animation` 简写覆盖前者的 `stripes`，条纹滚动被替换为宽度动画。并且 animated 时预览刻意去掉 `width:${pct}%`，而 keyframes 固定 0→80→100，percent 输入完全不参与。
- 证据：`tools/design/progress-bar-generator.html:271-273`（两个类共存、animated 时 actualPct 为空）、`:280-281`（两条 animation 声明与固定 keyframes）、`:282`（输出仍写 `width:${pct}%`）、`:32-35`（页面同权重规则顺序）
- 复现：percent=35、勾选「条纹」+「动画」→ 预览宽度按 0→80→100 循环、条纹静止；把 percent 改为 80 动画轨迹不变（期望条纹持续滚动且宽度以输入值为终点，或明确动画仅作演示并禁用百分比）
- 影响：`tools/design/progress-bar-generator.html`；两个视觉参数互相覆盖，用户按「35% 下载进度」交付会得到全程 0–100 的循环动画
- 方案：合并为一条 `animation: stripes 1s linear infinite, progressAnim 3s …`（或条纹改伪元素避免 animation 冲突）；keyframes 终点改用 pct，或在 animated 时禁用 percent 并标注

### D-N72 网格图案生成器「虚线网格」与「方形网格」输出相同实线（中，确认源码缺陷）
- 描述：`dashed` 分支与 `square` 分支使用逐字符相同的两条 `linear-gradient` 与 `background-size`，仅额外加 `background-position: -lw/2 0, 0 -lw/2`，结果仍是连续实线网格，只是整体左/上移半像素，没有虚线段。
- 证据：`tools/design/grid-pattern.html:269-270`（square 模板）、`:273-274`（dashed 模板，渐变与 size 完全相同）、`:167-173`（五种类型下拉）
- 复现（node 复算同一组 30/1/#667eea）：`type=square` 与 `type=dashed` 的 `background-image` 与 `background-size` 字符串 `===`，仅 background-position 不同；预览像素级相同（期望虚线由实线段+间隔组成）
- 影响：`tools/design/grid-pattern.html`；五种类型里两个实质重复，用户选「虚线网格」拿不到虚线
- 方案：用 `repeating-linear-gradient(${line} 0 ${lw}px, transparent ${lw}px ${lw*3}px)` 构造两方向的虚线段；补「五种类型输出互不相同」断言

### D-N73 网格图案生成器尺寸/线宽只夹下限，999 直接进入 background-size（低，确认源码缺陷）
- 描述：`size = Math.max(5, parseInt(...)||30)`、`lw = Math.max(1, parseInt(...)||1)` 仅约束下限；HTML 的 `max=200`/`max=10` 只约束 spinner，脚本不读取。清空回落 30/1 且不回写输入框。
- 证据：`tools/design/grid-pattern.html:265-266`（仅 Math.max）、`:164-165`（min/max 属性）、`:270-279`（原样拼入 background-size/线宽）
- 复现（node 复算）：cellSize=999 → `background-size: 999px 999px`（期望 200）；lineWidth=999 → 线宽大于格子，预览整片填色（期望 10）；清空 → 30/1，输入框仍为空
- 影响：`tools/design/grid-pattern.html`；超大值撑爆/糊死预览，界面数值与实际参数不一致
- 方案：`Math.min(200, Math.max(5, …))`、`Math.min(10, Math.max(1, …))` 并回写；超范围给出提示

### D-N74 进度条生成器高度/圆角越界不拦截，负圆角生成非法声明（低，确认源码缺陷）
- 描述：`h = Math.max(4, parseInt(...)||20)` 无上限，`radius = parseInt(...)||0` 接受负值；HTML 的 `max=60`/`min=0` 不参与脚本。负 border-radius 非法，浏览器会丢弃该声明。
- 证据：`tools/design/progress-bar-generator.html:263`（高度仅下限）、`:266`（圆角无校验）、`:275-276`（拼入内联样式）、`:164`、`:167`（min/max 属性）、`:282`（CSS 文本同值）
- 复现（node 复算原表达式）：height=9999 → `height: 9999px`（期望 60）；radius=-10 → `border-radius: -10px`，预览退回直角且复制产物无效（期望 0）；清空 → 20/0，输入框不回写
- 影响：`tools/design/progress-bar-generator.html`；超高进度条破坏页面布局，负圆角在项目中静默失效
- 方案：clamp 高度 4–60、圆角 0–50 并回写；非法时标红并停止生成

- 本轮实读 8 页：`css-box-shadow-generator.html`、`css-text-shadow.html`、`shadow-generator.html`、`glassmorphism-generator.html`、`neomorphism-generator.html`、`spinner-generator.html`、`progress-bar-generator.html`、`grid-pattern.html`；新增 12 条（高 2 / 中 7 / 低 3）。D-N63/D-N64 与既有 D-N44 属同一「增删层不重绘」模板缺陷，D-N69/D-N70 为同页两个独立问题（keyframes 未注入 / 音波柱 HTML 拼接），其余为各页独有。未覆盖：`tools/design` 其余约 53 页（108 个工具页中本文件已引 56 个），代表页含 `favicon-from-text`、`favicon-from-emoji`、`initials-avatar`、`identicon-generator`、`loading-dots`、`ripple-effect`、`pixel-art-generator`、`checkerboard-generator`、`dot-pattern`、`stripe-pattern`、`toast-generator`、`material-color`、`tailwind-colors`、`colorblind-simulator`、`cvd-safe-palette`、`gradient-from-color`、`base64-to-image`、`signature-pad` 等。所有结论均为源码行号 + node 内存复算/源码路径推演；未做浏览器交互、EN 运行态探针、移动端、门禁与线上验证。

## 2026-11-04 续查（并行批 O）

- 范围：`tools/design` 剩余生成器/互动演示 8 页（Favicon 文字、Favicon Emoji、首字母头像、Identicon、Loading Dots、Ripple、像素画、棋盘），逐页通读整份 HTML（内联 JS/CSS 生成逻辑、deep-dive、FAQ），编号续 D-N75。

### D-N75 favicon-from-text 三档预览的圆角/字号与画布不成比例（中，确认源码缺陷）

- 问题：小预览（16px）用 `radius/64*8` 缩放，相当于按 8px 参照框计算，圆角只有正确值的一半；公式说明还把这一档写成「64px 档」。字号比例也不一致（画布 0.55，大预览 CSS 固定 0.5）。
- 证据：`tools/design/favicon-from-text.html:28`（small 为 16px）、`:285`（`radius/64*8`）、`:286`（中档 64px）、`:287`（大档 `radius*2`、字号继承 `:27` 的 64px）、`:279`（画布 `.55`）、`:152`（说明文字「64px 档用 radius ÷ 64 × 8」）。
- 复现：radius=12、size=64 → 小预览 `border-radius:1.5px`（正确应为 12×16/64=3px）；大预览字号 64px（比例 0.5），画布为 35.2px（比例 0.55）。
- 影响：三档预览并非所见即所得，小图圆角明显偏方、文字比例略小，用户按预览调参后导出结果不同。
- 方案：小档改 `radius*16/size`（或统一按 `size` 缩放 `radius/mediumSize`），大档字号改 `size*0.55*128/size`；若坚持按 128/64 参照，则说明文字同步改成「16px 档」。

### D-N76 favicon-from-text 圆角可超半边长导致路径自交，边长无上限（中，确认源码缺陷）

- 问题：`radius` 只做下限 0，未限制 ≤ size/2；HTML `max=100` 不参与脚本校验。半径大于半边长时四段贝塞尔角的起止点交叉，路径自交。`size` 只 `Math.max(16)`，输入 9999 会创建超大画布。
- 证据：`tools/design/favicon-from-text.html:256-257`；路径拼接 `:262-274`；输入约束 `:161-162`（min/max 仅提示）。
- 复现：size=64、radius=100 → 生成 `lineTo(-36,0)`、`quadraticCurveTo(64,0,64,100)` 等负坐标/交叉段（node 复算 `64-100=-36`）；size=9999 → `canvas.width=9999`。
- 影响：默认边长 64 下只要圆角 >32 就出现畸形图标；超大画布可能触发浏览器内存告警或 `toDataURL` 失败。
- 方案：`radius = Math.min(radius, size/2)`；`size = Math.min(size, 256)`，越界时钳制并提示。

### D-N77 两个 Favicon 页的历史恢复执行下载而不是重绘（中，确认源码缺陷；与 D-N43/D-N57 同族）

- 问题：历史记录点击后只把参数写回控件，最后调用 `downloadImg()`，不重新 `generate()`；`downloadImg` 直接使用上一次的 `lastURL`，因此下载的是当前旧图，预览也不更新。
- 证据：`tools/design/favicon-from-text.html:370-383`（恢复回调结尾 `:381 downloadImg()`）、`:291-295`（下载读 `lastURL`）；`tools/design/favicon-from-emoji.html:361-375`（`:372 downloadImg()`）、`:282-286`。
- 复现：生成 A（红底）→ 改蓝底但不点「生成」→ 点历史 A → 控件回红底、预览仍蓝底，浏览器下载蓝底 PNG。
- 影响：历史功能语义错误且产生预期外下载；用户以为恢复了历史，实际拿到另一张图。
- 方案：恢复回调末尾改为 `generate()`；下载按钮前如需最新值，先调用 `generate()`。

### D-N78 favicon-from-text 按钮称「下载 ICO/PNG」实际只有单张 PNG，改参数后仍导出旧图（中，确认源码缺陷）

- 问题：页面与说明宣称多尺寸 PNG/ICO，实际 `download='favicon.png'` 单张；输入控件无 `onchange`，改文字/配色后直接下载仍是上一次结果。
- 证据：`tools/design/favicon-from-text.html:167`（按钮文案）、`:153`（「多尺寸 PNG / ICO」）、`:199`（deep-dive「多尺寸 favicon 可下载」）、`:294`（`a.download='favicon.png'`）、`:158-162`（输入无事件绑定）。
- 复现：文字 T→AB、底色调绿（不点「生成」）→ 点「下载 ICO/PNG」得到旧 T 红底 `.png`；产物中不存在 `.ico` 或第二尺寸。
- 影响：SEO/文案承诺与实际产物不符；用户拿到过期图，需再点一次生成才正确。
- 方案：按钮改「下载 PNG」或真正实现 ICO 打包；输入加 `onchange=generate()`（或下载前强制重绘）。

### D-N79 favicon-from-text 预设「三字缩写 API」与「1-2 字符」/maxlength=2 矛盾（低，确认源码缺陷）

- 问题：输入框标注 1–2 字符且 `maxlength=2`，预设却写入 3 字符 `API`；程序赋值绕过 `maxlength`，于是画布绘制 3 个字，小预览溢出。
- 证据：`tools/design/favicon-from-text.html:158`（label + maxlength=2）、`:433`（预设 `text:'API'`）。
- 复现：点预设「三字缩写 API」→ 输入框显示 `API`（浏览器不截断程序赋值），画布三字、16px 预览挤压。
- 影响：预设与字段约束自相矛盾，用户手动输入 `API` 时反而只能得到 `AP`。
- 方案：预设改 `AB`，或把字段上限改为 3 并同步文案。

### D-N80 favicon-from-emoji 预览圆角固定按 128 参照，改 size 后与画布不符（中，确认源码缺陷）

- 问题：三档预览按 `radius/128*16`、`radius/2`、`radius` 缩放，隐含画布 128；实际画布圆角就是用户 `size` 上的 `radius`。`size` 改成 64/256 时预览比例失真。
- 证据：`tools/design/favicon-from-emoji.html:26-29`（16/64/128 三档）、`:276-278`、`:146`（说明明确写「radius ÷ 128 × 16…」）、`:248`（size 可任意 16–256）。
- 复现：size=64、radius=24 → 画布圆角比 0.375，128px 大预览比 0.1875（差一倍）；三档均按 128 计算。
- 影响：默认 128 时一致，改尺寸即预览失真，用户无法靠预览判断导出效果。
- 方案：预览统一用 `radius/size*档位像素`。

### D-N81 favicon-from-emoji 宣称多尺寸 ICO/PNG，实际仅单张 PNG；改参数后仍导旧图（中，确认文案与实现不一致）

- 问题：meta/OG/Twitter、公式说明、deep-dive 均写「多尺寸 ICO/PNG」，实现只有 `canvas.toDataURL` 单张 PNG；Emoji/大小/圆角无 `onchange`，改后直接下载仍旧图。
- 证据：`tools/design/favicon-from-emoji.html:10,15,60`（meta 描述）、`:147`（formula-desc）、`:192`（deep-dive）、`:270-274`（只导 PNG）、`:285`（`favicon-emoji.png`）、`:152-155`（输入无事件）。
- 复现：emoji 🚀→🔥（不点生成）→ 下载仍是 🚀 的 PNG；任何路径都不产生 ICO 或第二种尺寸。
- 影响：与 D-N39 同类文案承诺落空；用户拿到过期图。
- 方案：文案改为「PNG」，或补 ICO/16/32/48 多尺寸打包；输入加 `onchange=generate()`。

### D-N82 favicon-from-emoji 圆角上限 100 已超默认半边长，生成自交路径；边长无上限（中，确认源码缺陷）

- 问题：默认 size=128 半边长仅 64，而圆角输入允许到 100；脚本只做下限 0。半径 > 半边长时路径交叉。`size` 只 `Math.max(16)`。
- 证据：`tools/design/favicon-from-emoji.html:154-155`（HTML max 256/100）、`:248-249`（脚本只钳下限）、`:254-266`（路径拼接）。
- 复现：size=128、radius=100 → `lineTo(28,0)`、`lineTo(28,128)` 等交叉段，填充出现缺口/自交；size=9999 → 超大 canvas。
- 影响：合法输入范围内即可产生畸形图标；超大尺寸可能导致导出失败。
- 方案：`radius=Math.min(radius,size/2)`、`size=Math.min(size,256)`。

### D-N83 initials-avatar 白字在 13/15 个哈希色上对比度低于 4.5:1，与引据表矛盾（中，确认源码缺陷）

- 问题：默认字色 `#ffffff`，哈希调色板含大量浅色；页面引据表写「首字母与底色对比不低于 4.5:1」，但实现从不校验，也未按底色自动切换黑白字。
- 证据：`tools/design/initials-avatar.html:267`（palette）、`:289`（`palette[hash % palette.length]`）、`:162`（textColor 默认 `#ffffff`）、`:248`（引据 4.5:1）、`:273`/`:319`（直接使用字色）。
- 复现（node 复算）：15 色中 13 色对白字 <4.5:1；`张三` → idx 4 `#43e97b` 对比 1.59:1，`陈光武` → idx 0 `#667eea` 3.66:1，`李四` → idx 6 `#30cfd0` 1.92:1，`user@x.com` → idx 12 `#feca57` 1.52:1；仅 `#764ba2`、`#5f27cd` 达标。
- 影响：多数中文姓名生成的头像首字母几乎看不清，且与页面自述的可访问性标准直接矛盾。
- 方案：按底色相对亮度自动选 `#111827`/`#ffffff`；或把 palette 整体压到 L≈45% 以下并保留对比校验。

### D-N84 initials-avatar 按 UTF-16 码位取首字母，emoji 名称产生孤立代理字符（中，确认源码缺陷）

- 问题：`parts[0][0]` 与 `name.substring(0,count)` 都按码位切分，不看字素簇；首字符是 emoji 时会切出半个代理对，`count===1` 再 `initials[0]` 进一步截断。
- 证据：`tools/design/initials-avatar.html:278-285`（`:281` 取 `[0]`、`:283` substring、`:285` 截断）、`:238`（引据 UAX #29「按字素簇取首字符」）。
- 复现（node）：姓名 `😀 Smith`、默认 2 字 → `"\ud83dS"`（高位代理 + S）；`🚀Dev`、1 字 → `"\ud83d"` 孤立高位代理，Canvas 画豆腐块/空白。
- 影响：emoji 或部分扩展汉字姓名生成破字；与引据的标准实现不一致。
- 方案：用 `Intl.Segmenter` 或 `Array.from(str)[0]` 按字素/码点取字符，再做 `toUpperCase()`。

### D-N85 initials-avatar 宣称导出 PNG/SVG，实际只有 PNG（低，确认文案与实现不一致）

- 问题：formula-desc 与英文 intro 写「导出 PNG / SVG」，页面没有 SVG 输出、也没有第二个下载入口。
- 证据：`tools/design/initials-avatar.html:10,15,64`（meta 描述「一键下载 PNG/SVG」）、`:155`（formula-desc）、`:521`（英文 intro「downloadable as PNG or SVG」）、`:325`（`toDataURL('image/png')`）、`:331`（`initials-avatar.png`）。
- 复现：页面上只有单个「下载」按钮，任何操作都只得到 `.png`。
- 影响：文案承诺落空，设计场景常用的矢量导出缺失。
- 方案：补 SVG 导出（圆形/圆角矩形 + `<text>`），或删掉文案中的 SVG。

### D-N86 initials-avatar 历史/数据表/CSV 恒空（中，确认源码缺陷；与 D-N59/D-N62 同族）

- 问题：结果区只写入 `<img>`，无任何文本；`ResText` 取 `textContent` 为空即不记录历史，因此历史页签、数据表与 CSV 永远为空。
- 证据：`tools/design/initials-avatar.html:185`（output 仅 preview）、`:326`（只写 img）、`:383-390`（`ResText` 空则提前 return）、`:440`、`:473-475`（仅在 `downloadImg` 后触发 Extras）。
- 复现：改姓名/尺寸并多次点「下载」→ 历史页签无记录，导出 CSV 为空表头。
- 影响：历史与导出两个功能形同虚设；下载本身正常。
- 方案：`ResText` 返回可序列化的参数摘要（姓名/尺寸/色值），或记录 base64 长度 + 参数。

### D-N87 identicon 引据表称 SHA-256，实现为 Java 风格 31 乘哈希（低，确认文案与实现不一致）

- 问题：引据表声称 SHA-256 保证 256 位分布，代码实际是 `hash = hash*31 + charCode` 的 32 位字符串哈希；公式说明自己写的也是 31 乘，两处自相矛盾。
- 证据：`tools/design/identicon-generator.html:238`（引据 SHA-256）、`:257-263`（`hashString`）、`:157`（公式说明「Java 风格乘 31」）、`:269`（调用）。
- 复现：node 复算 `hashString("github") = 1245635613`（0x4a3ee41d）；`SHA-256("github")` 前 32 位为 `0xc0b0109d = 3232764061`，两者不同。
- 影响：标准引据不可信；同一页面两套算法描述，易误导二次开发者。
- 方案：改引据为「Java String.hashCode 变体（32 位乘 31 哈希）」，或改用 `crypto.subtle.digest('SHA-256')` 并调整取位。

### D-N88 identicon 画廊固定 5 块与固定底色，不随当前参数（低，确认源码缺陷）

- 问题：画廊每格硬编码 `blocks=5`、`bg='#f0f0f0'`，不读用户输入的方块数与背景色；点画廊格子只改种子，主图却按当前输入渲染，两者视觉不一致。
- 证据：`tools/design/identicon-generator.html:302-303`（`size=60`、`blocks=5`）、`:308`（`#f0f0f0`）、`:266-268`（主图读 size/bg/blocks）、`:323`（点击只写 seed）。
- 复现：方块数 9、背景 `#1e293b` → 主图 9 块深底；画廊仍 5 块浅灰底；点任一画廊格 → 主图变 9 块深底，与所点缩略图不符。
- 影响：画廊不能预览当前配色方案，选图后出现「所见非所得」。
- 方案：画廊复用当前 `blocks/bg`，并在参数变化时重绘画廊。

### D-N89 identicon 历史/数据表/CSV 恒空（中，确认源码缺陷；与 D-N59 同族）

- 问题：结果区只写 `<img>`，`ResText` 恒为空，历史与 CSV 不会产生记录。
- 证据：`tools/design/identicon-generator.html:173`（output 仅 preview）、`:291`（只写 img）、`:382-389`（`ResText` 空则 return）、`:474`（Extras 仅在下载后触发）。
- 复现：改种子/方块数并多次下载 → 历史页签空、CSV 空。
- 影响：历史/导出入口不可用。
- 方案：`ResText` 返回 `seed|size|blocks|bg` 摘要。

### D-N90 loading-dots 速度 ≤0 生成非法动画，尺寸无上限（中，确认源码缺陷，两个问题）

- 问题：`parseFloat(...) || 1.4` 把 0 静默改成 1.4，负值原样进入 `animation` 简写；负 `animation-duration` 非法，整条声明被浏览器丢弃，预览与复制出的 CSS 都无动画。`size` 只做下限 4。
- 证据：`tools/design/loading-dots.html:268`（speed）、`:267`（size）、`:276`（拼 `animation:${speed}s`）、`:291`（延迟同用负值）、`:174` 附近（HTML max 仅提示）。
- 复现（node）：speed=-1.4 → `animation: dotBounce -1.4s ease-in-out infinite;`，延迟 `-0.47s`；speed=0 → 变成 1.4s；size=9999 → 9999px 圆点撑爆预览。
- 影响：负值输入下动画完全失效且无提示；超大尺寸破坏布局。
- 方案：`speed = Math.max(0.1, parseFloat(...) || 1.4)`，`size = Math.min(size, 80)`，越界时提示。

### D-N91 loading-dots 历史/CSV 恒空，导出 CSS 无配套 HTML 标记（中，确认源码缺陷，两个问题）

- 问题：结果区圆点全是空 `div`，`textContent` 为空 → 历史与 CSV 永不记录；复制的 CSS 只含 `.loading-dots`/`.dot` 规则，页面不提供对应 HTML 结构，用户粘贴后看不到动画。
- 证据：`tools/design/loading-dots.html:181`（output 仅 preview）、`:276-278`（预览仅空 div）、`:346-352`（`ResText`）、`:427`（CSV）、`:293`（CSS 输出无 HTML）。
- 复现：改类型/颜色/速度 → 历史页签空、CSV 空；复制 CSS 后直接粘到空页面，无 `.dot` 元素即无任何效果。
- 影响：历史/导出不可用；「复制即用」体验断裂。
- 方案：`ResText` 返回参数摘要；CSS 输出同时附 `<div class="loading-dots">…</div>` 片段（或提供「复制 HTML+CSS」）。

### D-N92 ripple-effect 点击预览不产生任何涟漪（高，确认源码缺陷）

- 问题：JS 创建的元素 `className='ripple'`，页面 CSS 只定义了 `.ripple-circle`；`.ripple` 规则仅存在于文本框中。该 `span` 作为 flex 子项虽会生效 width/height，但 `position:static` 使 left/top 无效，且无背景色/圆角/动画，点击后看不到任何涟漪，只会把「点击我」文字挤开造成布局跳动。
- 证据：`tools/design/ripple-effect.html:31`（`.ripple-circle{position:absolute;…background:rgba(255,255,255,0.5);…}`）、`:280`（`className='ripple'`）、`:282-284`（设置 width/height/left/top）、`:273`（`.ripple` 仅拼进 `cssOutput`）。
- 复现：类型选「点击涟漪」，在预览框「点击我」上点击 → 实际 append 一个无背景/无定位/无动画的 flex 子项 span，画面无扩散圆且文字被挤位；期望出现扩散圆。
- 影响：演示区的核心交互失效，用户无法验证效果，只能盲信复制出的 CSS。
- 方案：`className='ripple-circle'`，或复制页内 `.ripple-circle` 规则到 `.ripple`；同时内联 `position:absolute;border-radius:50%;background:rgba(...)`。

### D-N93 ripple-effect 多重涟漪缺 keyframes，脉冲预览轨迹与导出不一致（中，确认源码缺陷）

- 问题：页面只定义 `rippleAnim` 与 `pulseAnim`，预览用的 `multiPulse` 没有定义（只在文本框 CSS 里），多重模式静止；`pulseAnim` 页面版是 `scale(.5)→scale(2)`，导出 CSS 是 `scale(1)→scale(2.5)`，预览与复制结果不同。
- 证据：`tools/design/ripple-effect.html:32,34`（页内两条 keyframes）、`:300`（预览引用 `multiPulse`）、`:303`（`multiPulse` 仅在 CSS 文本）、`:34` vs `:296`（pulse 关键帧差异）。
- 复现：选「多重涟漪」→ 三个圆叠在一起静止不动；选「脉冲」→ 预览从 0.5 倍开始，复制后粘到项目变成从 1 倍开始。
- 影响：两种模式预览与产物不一致，用户看到的动效不是最终效果。
- 方案：页内补 `@keyframes multiPulse`，并让页内 `pulseAnim` 与导出字符串共用同一份定义。

### D-N94 ripple-effect「涟漪色」在脉冲/多重模式被忽略（中，确认源码缺陷）

- 问题：`r/g/b` 只用于点击模式的 `.ripple` 背景；脉冲与多重模式的圆点/圆环全部用背景色 `bg`，`rippleColor` 输入在两个模式下完全无效且无提示。
- 证据：`tools/design/ripple-effect.html:267-269`（解析 rippleColor）、`:273`（仅 click 用 rgba(r,g,b)）、`:292-294`、`:300`（pulse/multi 全用 `${bg}`）。
- 复现：背景 `#667eea`、涟漪色 `#ff0000`、类型「脉冲/多重」→ 预览与导出 CSS 中都不出现 `#ff0000`。
- 影响：参数被静默吞掉，用户反复调色无反馈。
- 方案：脉冲/多重改用 rippleColor（或按类型禁用该输入并置灰）。

### D-N95 ripple-effect 文案称导出 CSS/JS，实际只复制 CSS（中，确认文案与实现不一致）

- 问题：formula-desc 写「导出 CSS / JS」，但只有 CSS 文本框与「复制 CSS」；点击涟漪所需的 `box.onclick` 创建 `span` 的 JS 只存在于预览逻辑，从未输出。
- 证据：`tools/design/ripple-effect.html:159`（文案）、`:180`（唯一 `cssOutput`）、`:277-288`（JS 仅预览内）、`:308-311`（复制只取 CSS）。
- 复现：复制得到 `.ripple-container`/`.ripple`/keyframes，但没有任何创建涟漪元素的脚本；粘进项目后点击无反应。
- 影响：复制产物不可独立工作，与「导出 CSS / JS」承诺不符。
- 方案：增加 JS 输出片段（事件委托 + 创建 span），或把文案改为「复制 CSS」。

### D-N96 pixel-art 点击上色命中错位一格，首个格子命中画布容器（高，确认源码缺陷）

- 问题：`querySelectorAll('div[style*="32px"]')` 会把外层画布容器（style 含 `repeat(n,32px)`）也算进集合，容器排在所有格子之前，导致 `cells[0]` 是容器，按 `r*gs+c` 取到的元素整体错位一格（实际涂到左/上一格）。
- 证据：`tools/design/pixel-art-generator.html:289`（容器 `grid-template-columns:repeat(gs,32px)`）、`:293`（格子 `width:32px`）、`:319`（选择器）、`:320`（`idx=r*gs+c`）。
- 复现（8×8，node 复算匹配数 = 1+64 = 65）：点 (r=0,c=0) → `idx=0` → 改的是容器背景；点 (r=0,c=1) → `idx=1` → 实际涂到第 0 格。即每次点击都涂到「左/上一格」，首格涂到整块容器。
- 影响：绘制结果与鼠标位置错位，用户无法精确作画；容器背景被改后可能影响整块画布。
- 方案：给格子加统一 class（如 `px-cell`）后按 class 选择；或改用 `:scope > div` 过滤容器。

### D-N97 pixel-art 字符画不随点击更新，重算/历史恢复会清空绘制（中，确认源码缺陷）

- 问题：`grid` 是 `calcTool` 的局部数组，`_px` 只改 DOM 背景与 `data-c`，不写回 `grid`；字符画一次性由 `grid` 生成。任何重新 `calcTool`（点「计算」或历史恢复）都按预置笑脸重建，覆盖用户绘制。
- 证据：`tools/design/pixel-art-generator.html:286`（grid 局部初始化）、`:299-303`（art 来自 grid）、`:317-326`（只改 DOM）、`:384`（历史恢复 `calcTool`）。
- 复现：点几格涂色 → 字符画预览仍是初始笑脸（无新 ■）；点「计算」→ 所有手工涂色被预置图案覆盖。
- 影响：字符画与实际画布不一致；用户作品无法保留，历史里也没有绘制内容。
- 方案：把网格状态提到函数外（或读 DOM 的 `data-c` 重建 grid），`_px` 同步更新 grid 并刷新 `<pre>`；历史快照包含网格。

### D-N98 pixel-art 名实不符：无上传/量化/块大小/下载，6 色却称 8 色，且无复制导出（中，确认文案与实现不一致）

- 问题：标题/meta/intro 承诺「导出为字符画或 CSS 代码」；deep-dive 示例描述「上传图片 → 32 色 → 块 12px → 下载像素风图」；说明称「8 种基础色板」「字符画可复制」。实际无 file input、无 canvas、无下载、无复制按钮，调色板只有 6 色，CSS 从未生成。
- 证据：`tools/design/pixel-art-generator.html:10,13,16`（标题/描述）、`:121`（intro）、`:134`（6 个 option）、`:142-147`（仅计算/CSV/重置）、`:182-186`（deep-dive 上传图/32 色/块大小/下载）、`:227-228`（8 色/可复制）、`:304-315`（结果仅 dataGrid + 网格 + pre）。
- 复现：全页 grep `type="file"`/`<canvas`/`toDataURL`/`download`/`clipboard` 均 0 命中；选色只有红/橙/绿/蓝/紫/黑 6 项；字符画只能看不能复制。
- 影响：页面标题与示例引导用户做一件页面做不到的事，属严重名实不符；导出与复制能力缺失。
- 方案：补 PNG/SVG 导出与「复制字符画」；调色板补到 8 色；或把 deep-dive/说明改成实际支持的绘制流程。

### D-N99 checkerboard 历史/数据表/CSV 恒空（中，确认源码缺陷；与 D-N59 同族）

- 问题：结果区仅一个用 CSS 背景绘制的空 `div`，`textContent` 恒为空，历史与 CSV 永不记录。
- 证据：`tools/design/checkerboard-generator.html:168`（output 仅 preview）、`:255-256`（只写 `style.cssText` 与 textarea）、`:309-316`（`ResText`）、`:345`（历史恢复 `generate`）。
- 复现：改配色/格子大小多次 → 历史页签始终空，导出 CSV 只有表头。
- 影响：历史/导出入口不可用；生成本身正常。
- 方案：`ResText` 返回 `c1|c2|size` 摘要。

### D-N100 checkerboard 文案承诺「格数」与「导出图片」，实际无格数控件、无图片导出（中，确认文案与实现不一致）

- 问题：标题/描述/meta 反复写「可调格数」「可导出图片」；公式引据描述「SVG pattern、格数决定单元尺寸、单元边长 = 画布边长 / 格数」。实际只有颜色 1/2 + 格子大小三个输入，纯 CSS 平铺，无 canvas/SVG/下载。预设「透明底导出棋盘」也仍带 `background-color:#ffffff`，并不透明。
- 证据：`tools/design/checkerboard-generator.html:10,14,20`（title/meta）、`:154,156`（formula-desc/intro）、`:222,227`（引据 SVG pattern/画布边长）、`:159-161`（仅 3 个输入）、`:253-255`（只生成 CSS）、`:395`（预设「透明底」用 `#ffffff`）。
- 复现：页面无「格数」输入、无下载/Canvas 调用；选预设「透明底导出棋盘（16px）」→ CSS 仍为 `background-color:#ffffff`，无法作透明底使用。
- 影响：SEO 标题与 deep-dive 引导与实际能力不符；透明底预设名不副实。
- 方案：补「格数/画布尺寸」与 PNG/SVG 导出；或把文案统一改为「可调格子大小、复制 CSS」；透明预设改 `background-color: transparent`。

### D-N101 checkerboard 格子尺寸无上限，999 直接生成 1998px 背景（低，确认源码缺陷）

- 问题：`s` 只 `Math.max(5)`，HTML `max=200` 不参与脚本校验；超大值直接进入 `background-size/position`，预览区被巨大色块撑破。
- 证据：`tools/design/checkerboard-generator.html:253`（只钳下限）、`:254`（拼 CSS）、`:161`（max 仅提示）。
- 复现（node）：size=999 → `background-size: 1998px 1998px; background-position: 0 0, 999px 999px;`；预览最小高度 200px 内出现整块单色。
- 影响：输入越界时图案失去棋盘结构，页面布局被撑坏。
- 方案：`s = Math.min(200, Math.max(5, s))`，越界提示。

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
- 高优均给出可复现输入：D-N92 点击预览无涟漪（`.ripple` 无样式）；D-N96 8×8 点击命中错位（匹配 65 个元素，`idx` 整体偏移 1）。
- 同族合并：D-N77 = favicon 两页历史恢复下载；D-N83/D-N84 为 initials 独有；D-N86/D-N89/D-N91/D-N99 = 结果区无文本致历史/CSV 恒空（与 D-N59 同族）。
- 未覆盖：`tools/design` 其余约 44 页（本文件累计覆盖 64/108）。
- 未做：浏览器交互、EN 运行态探针、移动端、门禁与线上验证；D-N96 的 DOM 命中顺序按标准文档序推演，未开浏览器。

## 2026-11-04 续查（并行批 P）

- 范围：`tools/design/` 8 页（`colorblind-simulator` / `cvd-safe-palette` / `palette-cvd-checker` / `exposure-triangle-calculator` / `shutter-speed-calculator` / `flexbox-generator` / `gradient-from-color` / `toast-generator`），整份 HTML（含内联 JS、外链 `js/tools/colorblind-simulator.js`、deep-dive、FAQ、引据表）全读。
- 方法：静态源码审计 + `node` 复算；未开浏览器、未跑构建与门禁、未做 EN 运行态探针与移动端验证，行号按当前磁盘版本。

### D-N102 colorblind 取色器改色不回写 HEX 输入框（中，确认源码缺陷）

- 问题：`#c1Color` 的 `change` 处理调用 `setColorFromRgb(c, true)`，`skipInputs=true` 跳过整段输入回写，只另调 `syncRgbInputs` 同步 RGB 数字与滑杆，未更新 `#c1Hex`；HEX 文本框仍显示旧值，而预览/矩阵/色差已按新色计算。
- 证据：`js/tools/colorblind-simulator.js:321`（`setColorFromRgb(c, true)`）、`:308-313`（`if (!skipInputs)` 内才写 `c1Hex`）、`:328-331`（`syncRgbInputs` 只写 R/G/B）。
- 复现：默认色下打开取色器选 `#FF0000` → 单色预览与矩阵变红，`#c1Hex` 仍是旧 HEX；期望 HEX 框同步为 `#FF0000`。
- 影响：同屏两个「当前颜色」互相矛盾；用户照 HEX 框复制会拿到旧色。
- 方案：`skipInputs` 只跳过取色器自身，HEX/RGB 一并回写；或给 `setColorFromRgb` 增加 `hexOnly` 参数。

### D-N103 colorblind 单色调色板被误判「灰度糊成一片」且矩阵判全通过（中，确认源码缺陷，两个问题）

- 问题：灰度可分辨性用 `gaps.length ? min(gaps) : 0`，只有一个颜色时 `gaps=[]` → 0 → 直接判不合格；矩阵没有任何配对 → `warnLines` 为空 → 显示「所有颜色两两 ΔE 均 ≥ 10」。
- 证据：`js/tools/colorblind-simulator.js:406-412`（`minGap` 与阈值 10）、`:471-473`（无配对即输出通过文案）。
- 复现：调色板只填 `#FF0000` → 灰度提示 `0.0 ✗ 转灰度后会糊成一片`（单色不存在相邻混淆）；矩阵同时显示 `✓ 两两 ΔE ≥ 10`，两处结论互斥。
- 影响：极简调色板（单色/两色）得到自相矛盾的结论，用户无法判断。
- 方案：`n < 2` 时两处统一提示「至少输入 2 个颜色」，不要用 0 参与阈值比较。

### D-N104 colorblind 同一 ΔE 在卡片/矩阵/清单用三套阈值（低，确认源码缺陷）

- 问题：卡片标签按 5/15 分级，矩阵与混淆清单按 5/10 分级，页面说明又写 5–15 可察觉。
- 证据：`js/tools/colorblind-simulator.js:244-246`（`d<5` / `d<15`）、`:456-459`（`d<5` / `d<10`，清单只收 `<10`）。
- 复现：两色 ΔE=12 → 卡片标「可察觉」(warn)、矩阵格标 `good`、且不进混淆清单。
- 影响：同一对颜色在三个区域得到三种结论。
- 方案：抽一组常量（如 BAD<5 / WARN<10 / GOOD≥10）供三处共用，文案随之调整。

### D-N105 colorblind 切换视觉类型后标签回落中文（低，确认源码缺陷）

- 问题：切换「视觉类型」时把右侧标签硬写为 `TYPE_MAP[k].zh`，未走 `tn()`；初值走 `tn()`，切换后不走。
- 证据：`js/tools/colorblind-simulator.js:636`（`$('c3CmpRight').textContent = TYPE_MAP[k].zh`）。
- 复现：`?lang=en-US` 下把下拉从「绿色盲」切到「红色盲」→ 对照条标题显示中文「红色盲」；期望 `Red-blind`。
- 影响：英文态一致性；属源码直读，未做运行态探针。
- 方案：改为 `tn(TYPE_MAP[k])`。

### D-N106 cvd-safe 发散模式亮度曲线与注释/文档相反（高，确认源码缺陷）

- 问题：`L = 0.32 + 0.58 × |2t − 1|` 得到两端最亮（0.90）、中点最暗（0.32），而同一行注释写「中心最亮，两极最暗」，也与发散配色「中间浅、两端深」的常规写法相反；顺序模式（`:454`，`0.90 − 0.58t`）才是浅到深。
- 证据：`tools/design/cvd-safe-palette.html:468`（公式 + 注释）、`:454`（顺序模式对照）。
- 复现（node，n=5）：t=0 → L=0.90；t=0.5 → L=0.32；t=1 → L=0.90。即序列亮度为「亮 → 暗 → 亮」，中点最暗。
- 影响：发散模式的核心视觉（中心锚点）被做反，色带中间塌成深色，且与自身注释矛盾。
- 方案：改为 `L = 0.90 − 0.58 × |2t − 1|`（两端 0.32、中点 0.90），并同步公式说明。

### D-N107 cvd-safe「最大化最小色差」策略是空实现（中，确认源码缺陷）

- 问题：`generate()` 中 `if (strat === 'lightness' || strat === 'auto')` 与 `else` 两个分支都调用同一个 `greedyQualitative(n, seeds)`，`maxmin` 没有任何实现分支，但界面仍提供该选项。
- 证据：`tools/design/cvd-safe-palette.html:485-486`（两个分支语句完全相同）、`:175`（`#csStrategy` 下拉共 `lightness` / `maxmin` 两项）。
- 复现：定性模式、数量 5、不锁色，分别选「明暗交替优先」与「最大化最小色差」点生成 → 两组 HEX 完全相同（首色恒为 h=0°/L≈0.64/C=0.04）。
- 影响：策略下拉一半是死控件，用户以为换了算法。
- 方案：实现 maxmin 分支（去掉/放宽 targetL 过滤，按最小 ΔE 贪心），或合并为一个选项并改文案。

### D-N108 cvd-safe 未锁定色时首色恒定，与「自动选择最优起点」不符（中，确认源码缺陷）

- 问题：`greedyQualitative` 首轮 `chosen=[]`，每个候选 `minD=Infinity`，`if (minD > bestScore)` 只在第一个候选成立（此后 `bestScore=Infinity`，`Infinity > Infinity` 为假）→ 首色恒为候选表首项。
- 证据：`tools/design/cvd-safe-palette.html:437-443`（比较逻辑）、`:413-418`（候选按 `h` 外层、`L` 从 0.34 递增，首个满足 `|L-0.80|≤0.16` 的是 L=0.64、h=0）、`:381`（「生成将自动选择最优起点」）。
- 复现：连续点生成 / 改数量再生成 → 首色始终是同一固定色（h=0°/L=0.64/C=0.04 的浊红），不随约束变化。
- 影响：所有未锁色的定性配色都以同一个浊红开头，多样性差；文案承诺未兑现。
- 方案：首轮按「与目标 L 的距离 + 色相分散度」评分，或先打散候选顺序（确定性 shuffle）再取最优。

### D-N109 cvd-safe 称「8 种色觉类型」，实为 7 类 CVD + 正常且缺蓝锥单色视（中，文案与实现不一致）

- 问题：meta/正文写「红绿 / 蓝黄 / 全色盲等 8 种色觉类型」「全部 8 种色觉类型」，`VTYPES` 实为 1 个「正常」+ 7 个 CVD（红/绿/蓝各 opia+anomaly，全色盲），没有蓝锥单色视（`colorblind-simulator` 的 8 型含 blue-cone）。
- 证据：`tools/design/cvd-safe-palette.html:13,15,77`（meta/og/twitter）、`:243-251`（实际数组）、`:242`（注释「含正常」）、`:596`（「全部 8 种色觉类型」）。
- 复现：数 `VTYPES` 行 = 8（1 正常 + 7 缺陷）；页面 canvas 8 行里只有 7 行是色觉缺陷。
- 影响：SEO 与校验范围不符；蓝锥单色视用户得不到「全类型可区分」的保证。
- 方案：补 blue-cone 矩阵（与 simulator 同源）凑足 8 类缺陷，或把文案改为「7 种色觉缺陷 + 正常视」。

### D-N110 cvd-safe 恢复上次参数后不重新生成，控件与结果脱节（中，确认源码缺陷）

- 问题：`cvRestore()` 只回填控件并 `dispatchEvent(change)`，而各 change 处理仅赋值 `S.mode / S.count / S.strategy`，不调用生成；首屏 `:662` 已按默认值跑过一次，因此刷新后控件是旧参数、画面仍是默认配色。
- 证据：`tools/design/cvd-safe-palette.html:846-854`（restore 只 dispatch）、`:650-652`（change 只赋值）、`:662`（首屏按默认生成）。
- 复现：把数量改为 7 并生成（自动保存）→ 刷新 → 数量控件显示 7、色块仍是 5 色。
- 影响：保存/恢复功能看起来生效，实际结果与参数不一致。
- 方案：`cvRestore` 末尾触发 `#csGen.click()`（或直接 `generate(); renderResult();`）。

### D-N111 cvd-safe 预计算的 `c.labs` 在贪心中未被使用，生成时重复海量 Lab 转换（低，确认源码缺陷）

- 问题：`:428` 已为每个候选预计算 `c.labs`（8 种类型各做一次模拟 + Lab），但贪心评分 `:437` 仍调 `minDeltaAcross8(c.rgb, chosen[j].rgb)`，每次配对都对两边重跑 8 次 `simulate + rgbToLab`，预计算数据完全没用上。
- 证据：`tools/design/cvd-safe-palette.html:425-428`（`candLabs` / `c.labs`）、`:433-443`（每步约 1800 个候选 × 已选数 × 8 类型）。
- 复现：数量取 8～10 点生成 → `#csOut` 先塞一句「正在搜索最优安全配色…」，30ms 后同步跑完，期间不可取消；按候选规模估算约 70 万次重复 Lab 转换（量级估算，未计时）。
- 影响：大数量生成有可感知阻塞（低端移动设备更明显）；预计算内存白占。
- 方案：评分改用预计算数组（`minDeltaAcrossLabs(c.labs, chosen[j].labs)`），或把候选网格 `h` 步长由 5 放宽到 10。

### D-N112 palette-cvd「OKLCH 距离」把 Lab 当 RGB 计算（高，确认源码缺陷）

- 问题：`distFor('oklch', a, b)` 直接 `rgbToOklch(a)`，但所有调用方传入的都是 **Lab** 三元组（`renderMatrix` 的 `activeLabs()`、`analyzeWarnings` 的 `rgbToLab(simulate(...))`、图表 `list.map(rgbToLab)`）；`rgbToOklch` 却按 0–255 sRGB 解释，负的 a/b 会被 `srgbToLin` 当作负通道值处理，结果与真实 OKLCH 距离无关。
- 证据：`tools/design/palette-cvd-checker.html:399-401`（`oklchDist(rgbToOklch(a), rgbToOklch(b))`）、`:541`（`distFor(metric, labs[i], labs[j2])`，`labs` 来自 `activeLabs()`）、`:583`、`:662`、`:741`、`:769`（图表 / CSV / 叠加对照均传 `rgbToLab(...)`）。
- 复现（node，按页面同款 `rgbToOklch/oklchDist`）：`#FFFF33` vs `#FFFFFF`（真实 ΔE00=29.8，肉眼明显）页面记 `oklch=1.1`（<10 → 判为易混）；`#E41A1C` vs `#377EB8`（ΔE00=49.0）页面记 `18.7`，而用它自己的 `oklchDist` 以真实 RGB 计算仅 ≈1.0，两个方向都反了。
- 影响：一旦把指标切到「OKLCH 距离」，矩阵数值、混淆清单、修正建议全部失真。
- 方案：`distFor` 的 oklch 分支改为接收 RGB 原值（或在分支内把 Lab 转回 RGB 再转 OKLCH），调用方按指标取参。

### D-N113 palette-cvd 叠加对照写进告警区，会重复叠加且取消勾选不消失（中，确认源码缺陷）

- 问题：`renderOverlay` 把对照块 **追加** 到 `#pcWarn`（告警区）；切视觉类型只调 `renderMatrix()` 会再次追加；`analyzeWarnings()` 随后又把 `warnEl.innerHTML` 整体覆盖，取消勾选也没有移除逻辑。
- 证据：`tools/design/palette-cvd-checker.html:550`（`if (S.overlay) renderOverlay`）、`:554-569`（拼块后 `w.innerHTML = (w.innerHTML||'') + bh`）、`:610`（`warnEl.innerHTML = __h16` 覆盖）、`:719`（取消勾选只 `renderMatrix()`）。
- 复现：勾选「叠加模拟色块」→ 对照出现在告警区下方；再切换 3 次类型 → 同一组对照叠加 4 份；改任一色值（触发 `analyzeWarnings`）→ 对照消失，但勾选框仍勾选。
- 影响：控件状态与画面不一致，告警信息被叠加块挤占。
- 方案：给叠加块独立容器（如 `#pcOverlayBox`），每次渲染前清空，取消勾选时隐藏。

### D-N114 palette-cvd「9 种视觉通道」含一组完全重复，且 meta 写 8 种（中，文案与实现不一致，两个问题）

- 问题：`achromatopsia` 与 `grayscale` 都走 `mode:'gray'` 的同一实现，矩阵两行逐格相同；meta 写「共 8 种视觉通道」，页面标题写「9 种」，而实际 9 行 = 正常 + 7 类 CVD + 1 组重复灰度，仍缺蓝锥单色视。
- 证据：`tools/design/palette-cvd-checker.html:277-287`（`VISION` 九项）、`:285-286`（两项同为 `mode:'gray'`）、`:202`（「9 种视觉通道」）、`:13,15`（meta「共 8 种」）。
- 复现：看「全色盲」与「灰度/黑白」两行 → 数值完全一致；meta 数量与正文数量不一致。
- 影响：通道数量三处口径不一，且 9 行里有 1 组冗余。
- 方案：删重复行（保留灰度）并把标题改 8；或补 blue-cone 后统一为 9，同时改 meta。

### D-N115 exposure-triangle ISO 到边界后「等效组合」不再等效（高，确认源码缺陷）

- 问题：ISO 分支把 `niso` clamp 后仍用未校验的 `ns = si − da` 改快门，卡片却统一标在「等效曝光组合（相同曝光量）」下。ISO 已封顶时，快门继续加快 → 实际变暗 1–2 档。
- 证据：`tools/design/exposure-triangle-calculator.html:253`（标题「相同曝光量」）、`:260-263`（`niso` clamp、`ns = si-da` 未校验）、`:300-308`（CSV 同逻辑：`niso` 同样 clamp 后仍写 `ns`）。
- 复现（node，`EV=log₂(N²/t) − log₂(S/100)`）：ISO 6400 + 1/60（EV=3.91）时，卡片给出 f/4 1/125 ISO6400（EV=4.97，+1.06 档）与 f/4 1/250 ISO6400（EV=5.97，+2.06 档）；ISO 100 + 1/60（EV=9.91）时 da=-2 给出 f/4 1/15 ISO100（EV=7.91，−2.00 档）。
- 影响：标称等效的组合实际改变曝光，按提示拍会过暗/过亮。
- 方案：`niso !== ii+da` 时跳过该卡片（或让快门回退保持 EV），并提示「已到 ISO 边界」。

### D-N116 exposure-triangle ±1EV 按钮与「曝光量变化」文案方向相反（中，语义与实现冲突）

- 问题：`changeExp(delta)` 用 `si − delta` 且只改快门；「−1EV」实际放慢快门（更亮），「+1EV」实际加快（更暗），与左侧「修改后曝光量变化」的曝光量语义相反（若按公式的 EV 数值口径则自洽，按钮语义因此含糊）。
- 证据：`tools/design/exposure-triangle-calculator.html:151`（按钮与文案）、`:283-288`（`si=si-delta`，只动 `#shutter`）、`:245`（EV 公式）。
- 复现（node）：默认 f/4 1/60 ISO200 EV=8.91；点「−1EV」→ 1/30 → EV=7.91（亮 1 档）；点「+1EV」→ 1/125 → EV=9.97（暗 1 档）。
- 影响：按曝光补偿直觉操作必得到相反结果；且点一次 1/60↔1/125 实际是 1.06 档而非整 1 档。
- 方案：交换两个按钮的 `delta`，或把文案改成「EV 数值 ±1（越快越暗）」，并同时支持光圈/ISO。

### D-N117 exposure-triangle 公式框承诺的 EV 从不显示，图表 EV 轴光圈/ISO 符号反了（中，确认源码缺陷，两个问题）

- 问题：`evFromIdx` 的光圈/ISO 项与 EV 公式相反——`(3−ai)` 使 f 值变大（进光减少，EV 应 +1）却减 1，`(ii−1)` 使 ISO 升高（EV 应 −1）却加 1；`calc()` 里 `const ev = evFromIdx(...)` 从未使用，页面不显示任何 EV 数字。
- 证据：`tools/design/exposure-triangle-calculator.html:245`（`evFromIdx`）、`:252`（死变量 `ev`）、`:437`、`:442`（图表用同一函数作纵值）。
- 复现（node，固定 1/60 ISO200）：光圈 f/4 → f/8（ai 3→5）图表纵值整体下移 2，真值应上移 2；ISO 200 → 800（ii 1→3）图表纵值 +2，真值应 −2。
- 影响：EV-快门曲线在换光圈/ISO 后读数反向，公式框却从不给出 EV 数值。
- 方案：`evFromIdx = (ai−3)+(6−si)−(ii−1)`，并在结果区显示绝对 EV；删除死变量。

### D-N118 exposure-triangle 光圈边界生成重复卡片；「锁定曝光」是空按钮（低，确认源码缺陷，两个问题）

- 问题：光圈分支 clamp 后 `neededSi = si + (na−ai) = si`，`da=−1` 与 `da=−2`（或 `+1/+2`）生成两张完全相同的卡片；「🔒 锁定曝光」只调用 `calc()`，没有任何锁定状态。
- 证据：`tools/design/exposure-triangle-calculator.html:254-259`（clamp 后仍 push）、`:151`（按钮只绑 `calc()`）、`:290`（`calc` 包装）。
- 复现：光圈选 f/1.4 → 头两张卡片均为 `f/1.4 1/60 ISO 200`；点「锁定曝光」后继续改参数，等效表照常重算，未锁定。
- 影响：结果卡重复且无法区分；按钮名不副实。
- 方案：clamp 后若 `na===ai && da!==0` 跳过；锁定按钮改为记录当前 EV 并据此换算，或直接删除。

### D-N119 shutter-speed 图表与结果/CSV 给出三个不同快门（中，确认源码缺陷，两个问题）

- 问题：结果/CSV 先在标准档位表 `findIndex` 取「更快的第一档」（基础速度从 1/75 跳到 1/125，再按档位回退），图表却用 `round(effF / 2^stops)` 直接算；`Math.round` 还可能把值取到更慢的一档，违反公式框「向更快方向取整」。
- 证据：`tools/design/shutter-speed-calculator.html:259-262`（档位表取整）、`:292-295`（CSV 复算同逻辑）、`:442`（`d2=Math.max(1,Math.round(d1/Math.pow(2,isStops)))`）、`:139`（公式说明「向更快方向取整」）。
- 复现（node）：默认 50mm/1.5x/3 档 → effF=75，结果档位 1/15、CSV 基础速度 1/125，而图表「含防抖」标注 `round(75/8)=9 → 1/9 s`、「无防抖」为 1/75 s；effF=90、3 档时图表给 1/11（比 1/11.25 更慢）。
- 影响：同一页三处（结果 / CSV / 图表）三个快门值，用户不知该信哪个。
- 方案：图表复用同一 `stops.findIndex` 逻辑，`Math.round` 改 `Math.ceil`（更快方向）。

### D-N120 shutter-speed 焦距无上限，越界给出荒谬「安全快门」（低，确认源码缺陷）

- 问题：`focal` 只 `+value||50`，无上限、无提示；`min=1` 不阻止输入 100000。
- 证据：`tools/design/shutter-speed-calculator.html:253`（`+value||50`）、`:145`（`min=1` 无 max）。
- 复现：焦距输入 100000、裁切 2.7、5 档 → effF=270000，档位表封顶 1/1000（baseIdx=10），safeIdx=10−5=5 → 仍显示 `1/30`。
- 影响：越界输入被当成有效结果，且与任何真实镜头无关。
- 方案：设上限（如 2000mm），超出档位表时提示「低于 1/1000 s，需三脚架」。

### D-N121 flexbox-generator gap 无校验，负数/科学计数法直接进 CSS（中，确认源码缺陷）

- 问题：`g` 直接取 `#gap` 的值，无 `parseFloat`、上限与符号校验，原样拼进生成的 CSS 与预览 `style`。
- 证据：`tools/design/flexbox-generator.html:238`（`gap: '+g+'px`）、`:241`（预览同理）、`:129`（gap 输入无 min/max）。
- 复现：gap 输入 `-5` → 输出 `gap: -5px`（`gap` 不接受负值，声明被浏览器丢弃），预览无间距而代码块写着 -5px；输入 `1e3` → `gap: 1e3px` 同样非法。
- 影响：复制出的 CSS 失效，预览与代码不一致。
- 方案：`g = Math.max(0, Math.min(200, parseFloat(value) || 0))`，非法输入提示。

### D-N122 deep-dive 示例显示转义后的 `<p><strong>` 标签文本（中，文案与实现不一致；同族 5 页）

- 问题：示例正文把整段 `<p><strong>` 转义后写入 `dd-ex-body`，页面上直接显示 `<p><strong>输入：</strong>…` 的标签文字，而不是「输入：」加粗。
- 证据：`tools/design/flexbox-generator.html:389`。
- 复现：滚动到「深度解析」→ 示例卡片显示 `<p><strong>输入：</strong>row、justify-center。` 原文。
- 影响：可读性与可信度；同族：`toast-generator.html:209`、`exposure-triangle-calculator.html:189`、`shutter-speed-calculator.html:185`、`gradient-from-color.html:212`。
- 方案：去掉 `&lt;p&gt;`/`&lt;strong&gt;`，直接写纯文本或真实标签。

### D-N123 flexbox-generator「实时预览」名不符实（低，文案与实现不一致）

- 问题：结果标题写「实时预览（3 个项目）」，但所有控件都没有 `onchange/oninput`，只有点「生成」才调用 `calcTool()`。
- 证据：`tools/design/flexbox-generator.html:240`（标题）、`:111-129`（控件无事件）、`:233-243`（唯一渲染路径）。
- 复现：改 flex-direction 下拉 → 预览不动，必须点「生成」。
- 影响：用户以为调参即预览。
- 方案：给控件绑 `change` 调 `calcTool()`，或把标题改为「预览」。

### D-N124 gradient-from-color 历史/数据表/趋势/CSV 恒空（中，确认源码缺陷）

- 问题：`#output` 只含一个纯背景的 `div#preview`，`__gradient_from_colorResText` 读 `#output.textContent` 恒为空 → `Extras` 直接 return，三个页签与「导出明细 CSV」永远为空。
- 证据：`tools/design/gradient-from-color.html:180`（output 仅 preview）、`:393-399`（ResText）、`:450-451`（`if(!res) return`）。
- 复现：改方向/步数点生成 3 次 → 历史页签空、CSV 只有表头。
- 影响：附加页签与导出入口不可用（与 D-N59/D-N89/D-N91/D-N99 同族）。
- 方案：ResText 返回 `base|dir|steps|首色标` 摘要。

### D-N125 gradient-from-color FAQ 宣称 WCAG 对比度检测，实际无任何实现（中，文案与实现不一致）

- 问题：FAQ 写「会按 WCAG 算出对比度值与等级，未达标会标红提醒」，引据表也登记 WCAG 2.2 (1.4.3)，但全页没有对比度计算（无 relative luminance、无 4.5:1 判断）。
- 证据：`tools/design/gradient-from-color.html:216`（FAQ）、`:246`（引据表对比度条目）、`:306-345`（仅生成渐变，无对比度逻辑）。
- 复现：任意两色（如 `#FFFFFF` 与 `#EEEEEE`）→ 页面不输出任何对比度数值或红标。
- 影响：承诺的功能不存在，用户会误以为已校验可读性。
- 方案：补 WCAG 对比度计算（逐色标对白/黑文字），或删掉该问答与引据行。

### D-N126 gradient-from-color 基色亮度被丢弃，深/浅基色不出现在渐变里（中，确认源码缺陷）

- 问题：主渐变只取基色 H、S，亮度固定从 90 到 20；基色自身的 L 从不参与，深色/浅色基色根本不出现在结果中。
- 证据：`tools/design/gradient-from-color.html:312-314`（`hslToHex(hsl.h, hsl.s, l)`，`l` 由 90 递减到 20，与 `hsl.l` 无关）。
- 复现（node）：基色 `#000000`（HSL 0,0,0）→ 色标 `hsl(0,0%,90%)`→`hsl(0,0%,20%)`，即 `#E6E6E6 → #333333`，纯黑不出现；`#FFFFFF` 同样得到灰阶 90→20。
- 影响：「从颜色生成渐变」却不含该颜色，黑白基色结果不符合预期。
- 方案：端点锚定基色（i=0 用 `hsl.l`），或整体在 `[max(10, l−45), min(95, l+30)]` 内插值。

### D-N127 gradient-from-color 复制无 `navigator.clipboard` 兜底（低，确认源码缺陷）

- 问题：`copyGradient`/`copyResult` 直接 `navigator.clipboard.writeText(...).then(...)`，无存在性判断、无 catch/兜底；非安全上下文或旧浏览器下抛 TypeError，点击无反馈。
- 证据：`tools/design/gradient-from-color.html:340`、`:345`（两处均直接 `navigator.clipboard.writeText(...)`）。
- 复现：在 `http://`（非 localhost）或禁用剪贴板权限的浏览器点渐变卡 → 控制台 TypeError，无「已复制」提示。
- 影响：核心「点击卡片复制」静默失败。
- 方案：加 `if (!navigator.clipboard)` 的 textarea + `execCommand` 兜底与 catch 提示。

### D-N128 toast-generator 任何「生成」触发都会把自定义背景色改回预设（中，确认源码缺陷）

- 问题：`generate()` 中只要当前焦点不在 `#bgColor` 上就强制把背景改回类型预设并回写取色器；除切类型外，改文案、改圆角、点「生成」、点预设都会触发，用户自定义背景色被静默丢弃，而公式框只声明「选中类型时」才这样做。
- 证据：`tools/design/toast-generator.html:273-276`（`document.activeElement.id !== 'bgColor'` 即覆盖）、`:170-172`（消息/圆角/取色器都绑 `generate()`）、`:175`（生成按钮）、`:156`（文案只写「选中类型时」）。
- 复现：背景色设为 `#000000` → 把圆角改成 16（或点「生成」）→ 背景立刻回 `#4caf50`，取色器也变绿。
- 影响：自定义背景色无法稳定使用；与文档描述不符。
- 方案：只在 `#toastType` 的 change 里套预设色，其余触发不覆盖（或仅在用户未手动改色时跟随类型）。

### D-N129 toast-generator 描述承诺「位置/动画」配置，实际无控件也无输出（中，文案与实现不一致）

- 问题：描述写「配置 Toast 的文案、位置、图标与动画」，页面只有类型/消息/圆角/背景色 4 个输入；生成 CSS 只有 padding/radius/background/color/flex/shadow/icon，没有 `position`、没有 `transform/opacity` 或 keyframes。
- 证据：`tools/design/toast-generator.html:159`（描述）、`:168-172`（4 个输入）、`:285`（写入 `#cssOutput` 的 CSS）、`:157`（公式框也只列这些）、`:213`（FAQ 承认位置/自动关闭要自己写）。
- 复现：任选类型点生成 → `#cssOutput` 中 grep `position|animation|@keyframes|transform` 均 0 命中；页面无位置/动画控件。
- 影响：核心卖点缺失，复制出的代码只能塞进已摆好位置的容器。
- 方案：补位置（四角/顶/底）与动画（slide/fade/scale + 时长）并写进 `position:fixed` 的完整片段；或把描述改为「样式生成」。

### D-N130 toast-generator 消息内容未转义直插 innerHTML（低，确认源码缺陷）

- 问题：`msg` 未转义直接拼进 `#preview.innerHTML` 的模板字符串。
- 证据：`tools/design/toast-generator.html:281`（模板串 `<span>${msg}</span>`）、`:284`（`innerHTML=__h0`）。
- 复现：消息内容输入 `<img src=x onerror=alert(1)>` 并触发生成 → 预览区执行脚本（自 XSS，仅影响本页）。
- 影响：本地工具的自伤型注入；导出的 CSS 不含 msg，不向他人扩散。
- 方案：`msg` 走 `esc()` 后再插入，或改用 `textContent` 赋值。

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
- 同族合并：转义标签文本只记 D-N122（另 4 页同行号已在条目列出）；结果区无文本致历史/CSV 恒空记 D-N124（与 D-N59/N89/N91/N99 同族）。
- 未覆盖：`tools/design` 其余约 36 页（本文件累计覆盖 72/108）。
- 未做：浏览器交互、EN 运行态探针、移动端、`run_gates.py` 与线上验证；D-N112/D-N115/D-N106 的数值均为 `node` 按页面同款公式复算，未在页面内实测。

## 2026-11-04 续查（并行批 Q：8 个设计页功能 / 渲染 / 文案）

- 范围：`tools/design/` 8 页（`waveform-visualizer` / `tailwind-colors` / `base64-to-image` / `data-matrix` / `spectrum-visualizer` / `pixel-art` / `colorblind-simulator` / `signature-pad`），整份 HTML（含内联 JS/CSS、外链 `js/tools/colorblind-simulator.js`、deep-dive、FAQ、引据表）全读。
- 方法：只读源码 + `node` 内存复算（Tailwind 242 色 WCAG、CSS 拉伸后的圆环比例、Base64 扩展名正则、Data Matrix 图案）；未改代码、未跑 `_build.py`/门禁/浏览器、未做英文态与移动端实测，行号按当前磁盘版本。

### D-N131 waveform 简介与 FAQ 承诺「上传音频 / 实时渲染 / 缩放」，实际是参数化数学波形（高，确认文案与实现不一致）

- 问题：meta、公式说明、SEO 简介、deep-dive 示例/FAQ 均称可上传音频文件、取峰值、缩放查看；页面只有类型/频率/振幅/相位/颜色五个参数，波形由解析式逐像素计算，无任何文件或音频输入。
- 证据：`tools/design/waveform-visualizer.html:10`（meta「上传文件与实时渲染、缩放查看」）、`:155`（formula-desc「把音频采样…支持上传文件与缩放查看」）、`:509`（简介英文「file upload, live rendering and zoom」）、`:207`（示例「上传音频→取峰值绘制」）、`:514`（「一键复制 CSS 代码」）。
- 复现：全页 grep `type="file"|FileReader|AudioContext|AnalyserNode` 0 命中；输入区只有 `:157-170` 五项；`drawWave` 在 `:282-295` 用 `sin/asin` 计算，并非采样数据。
- 影响：`tools/design/waveform-visualizer.html` 的 SEO/教学定位整体失真，用户无法完成「上传音频看波形」。
- 方案：把文案统一改为「参数化波形（正弦/方波/三角/锯齿/混合）演示」；若要保留音频卖点，接 `decodeAudioData` 并按像素列取 min/max 峰值桶（纯前端可行）。

### D-N132 waveform 画布固定 800×200 + CSS 非等比拉伸、无 DPR，移动端变形且高分屏模糊（中，确认源码缺陷）

- 问题：`<canvas width="800" height="200">` 的内部像素固定，CSS 却设 `width:100%; height:200px`，横向随容器缩放、纵向恒 1:1，且未按 `devicePixelRatio` 重设画布。
- 证据：`tools/design/waveform-visualizer.html:178`（canvas 800×200）、`:30`（`canvas{display:block;width:100%;height:200px}`）。
- 复现（node 复算）：容器 350/860/1080 px 时横向缩放分别为 0.438/1.075/1.350，纵向恒 1.0；860 px 下网格被横向放大 1.075 倍、1080 px 下 1.35 倍，高 DPR 屏再叠加一次位图放大。期望等比或按真实像素重绘。
- 影响：`tools/design/waveform-visualizer.html` 波形周期疏密随窗口变化，放大后笔画发虚。
- 方案：用 `ResizeObserver` 设 `canvas.width=clientWidth*dpr`、`canvas.height=200*dpr` 并按 CSS 坐标缩放绘制；或固定内部比例并加 `aspect-ratio:4/1`。

### D-N133 waveform 振幅/频率越界不拦截，超大振幅整条波形画出画布（低，确认源码缺陷）

- 问题：`amp = parseFloat(...) || 0.8`、`freq = parseInt(...) || 3`，脚本不夹 HTML 的 `min/max`；振幅 >1、频率 0 等直接进入公式。
- 证据：`tools/design/waveform-visualizer.html:265-266`（解析）、`:295`（`py = h/2 − y*amp*(h/2−10)`）、`:167-169`（HTML 仅提示 1–20 / 0.1–1 / 0–360）。
- 复现（node 复算）：amp=5 → `py = 100 − 5×90 = −350`，整条线在 200 px 画布之外；freq=0 输入被 `||3` 改成 3。期望夹到 [0.1,1]/[1,20] 并回写输入框。
- 影响：`tools/design/waveform-visualizer.html` 用户输入越界后「生成」看似无反应。
- 方案：统一 `clamp()` 后再计算，并把夹取后的值写回输入框。

### D-N134 spectrum 简介/FAQ 承诺 Web Audio + FFT + 峰值 + 麦克风，实际是正弦动画且麦克风被 Permissions-Policy 禁止（高，确认文案与实现不一致）

- 问题：meta、formula-desc、deep-dive 示例与 FAQ 称「AnalyserNode 做 FFT」「频谱条动画」「可用麦克风或音频输入」；实现只有 `sin(animT…)` 伪随机柱状动画，且页面 `Permissions-Policy` 明确 `microphone=()`。
- 证据：`tools/design/spectrum-visualizer.html:10`（meta「Web Audio API…FFT 分析与峰值查看」）、`:155`（formula-desc「基于 Web Audio 的 AnalyserNode 做 FFT…峰值查看」）、`:205`（示例「播放/麦克风音频→FFT 分析」）、`:208`（FAQ「可用麦克风或音频输入」）、`:71`（`microphone=()`）、`:258-305`（`draw()` 纯 sin 计算）、`:175`（界面自标「预览 (模拟数据)」）。
- 复现：全页 grep `AudioContext|AnalyserNode|getUserMedia` 0 命中；`val` 由 `Math.sin(animT*0.05+i*0.3)` 生成，与 FFT 无关。
- 影响：`tools/design/spectrum-visualizer.html` 核心卖点全部未实现，FAQ 还引导用户授权一个被 policy 禁用的能力。
- 方案：文案改为「模拟频谱动画生成器」并去掉 FFT/麦克风；或接 `AudioContext.createAnalyser()`、移除 `microphone=()`，并提供音频文件/麦克风入口。

### D-N135 spectrum 圆环模式被 CSS 非等比拉伸成椭圆（移动端 2.28:1）且无 DPR（中，确认源码缺陷）

- 问题：内部 800×200，CSS `width:100%;height:200px`；圆环用 `r = min(w,h)/4` 按内部坐标画正圆，显示时横向被压缩/放大，正圆变椭圆。
- 证据：`tools/design/spectrum-visualizer.html:176`（canvas 800×200）、`:30`（CSS 100%/200px）、`:267-284`（圆环几何，`:269` 半径）。
- 复现（node 复算）：容器 350 px → 半径 50 显示为 21.9×50 CSS px（纵横比 0.44，竖椭圆）；860 px → 53.8×50（1.07）；1080 px → 67.5×50（1.35）。期望 1:1。
- 影响：`tools/design/spectrum-visualizer.html` 移动端圆环严重变形，视觉不可信。
- 方案：按 CSS 尺寸重设画布并按同一坐标系绘制；或固定 `aspect-ratio:4/1` 并让圆环按短边取半径。

### D-N136 spectrum 条数负数/0/超上限不夹取，负值直接空白画布（低，确认源码缺陷）

- 问题：`barCount = parseInt(...) || 48` 只处理 0 与 NaN，不夹 `min=8/max=120`；负值参与 `barW` 计算。
- 证据：`tools/design/spectrum-visualizer.html:262`（解析）、`:158`（HTML 8–120）、`:286-287`（`barW=w/barCount` 与循环）。
- 复现：输入 -8 → `barW = 800/-8 = -100`，`for(i<-8)` 执行 0 次 → 画布空白；输入 1000 → 每柱 0.8 px 近似不可见；期望夹到 [8,120]。
- 影响：`tools/design/spectrum-visualizer.html` 越界输入后「生成」无任何图形。
- 方案：`Math.max(8, Math.min(120, n||48))` 并回写。

### D-N137 data-matrix 输出不是 Data Matrix：无编码/无纠错，定位边方向与 ISO 16022 相反，扫码器读不出（高，确认源码缺陷）

- 问题：除定位边外的模块由「文本哈希 → LCG 伪随机」填充（`rnd() > 0.5`），没有任何数据编码与 Reed-Solomon；定位图案把**上边与右边**画成实心、**左边与下边**画成交替时钟轨，而 ECC200 规范是**左列+底行实心 L 边、顶行+右列交替时钟轨**；因此不是可解码符号。
- 证据：`tools/design/data-matrix.html:154`（formula-eq 哈希/LCG）、`:155`（formula-desc 却称 Reed-Solomon）、`:258-281`（填充与定位边；`:276-281` 四条边赋值）、`:282-294`（仅绘制色块）、`:230`（引据表称 RS 纠错）、`:225`（引据表称 L 形实心边）、`:201`（示例「扫码得原文」）。
- 复现（node 复算 size=14，text=`Data Matrix`）：顶行 14 个全实心；右列前 13 个实心、右下角被 `grid[13][13]=false` 覆盖；左列 `10101010101010`、底行 `00101010101010`，不存在 L 形实心边。任意长度文本只参与 32 位哈希，数据格恒为 12×12=144 个随机格。
- 影响：`tools/design/data-matrix.html` 声称用于工业零件标识，实际任何 Data Matrix 读码器都读不出原文；属高危误导。
- 方案：接入成熟的 ECC200 Data Matrix 编码库并锁定版本（纯前端）；若只想做纹理，改名为「矩阵纹理生成器」并删除扫码/纠错/工业标识文案。

### D-N138 data-matrix 公式框自相矛盾，尺寸语义与引据表冲突（中，确认文案与实现不一致）

- 问题：同一公式框里 formula-eq 写哈希+LCG，formula-desc 却写「数据经 Reed-Solomon 纠错后排布」；输入「尺寸」实际是模块数（画布=阶数×18 px），但示例写「模块 4px」；输入 `min=8` 与引据表「模块数自 10×10 起」矛盾，且允许 8/9 等真实 DM 不存在的奇数规格。
- 证据：`tools/design/data-matrix.html:154-155`（两段互斥描述）、`:164`（`min=8 max=24`）、`:235`（引据表 10×10 起、四档）、`:201`（示例「SN2026X、模块 4px」）、`:282-284`（`cellSize=18`，画布=size×18）。
- 复现：把「尺寸」填 9 → 生成 9×9=162 px 的 9 模块方阵，真实 ECC200 无 9×9 符号；填 8 → 8×8。期望要么用规范尺寸表（10–144 偶数档），要么明确「演示模块数」并删掉规范口吻。
- 影响：`tools/design/data-matrix.html` 参数与「Data Matrix 规范」互相对不上，用户无法对齐工业标准。
- 方案：统一术语为「模块数（演示 8–24）」，删除 4px/RS/规范尺寸表述；或换成规范尺寸下拉。

### D-N139 base64 描述承诺「反向转换」，页面只有解码、无编码入口（中，确认文案与实现不一致）

- 问题：meta×3 与正文均称「也支持反向转换」，英文简介更写「encode an image to Base64」；实际无 `type="file"`、无 `FileReader`、无 `btoa/encode`，只能解码。
- 证据：`tools/design/base64-to-image.html:10`、`:15`、`:64`（meta/OG/Twitter「也支持反向转换」）、`:160`（正文/`data-zh` 同句）、`:158`（formula-desc 纯套话，无公式）。
- 复现：全页 grep `type="file"|FileReader|readAsDataURL|btoa` 0 命中；工具区只有 textarea + 转换/复制/下载（`:162-167`）。
- 影响：`tools/design/base64-to-image.html` 用户找不到「图片→Base64」入口，核心承诺缺失。
- 方案：补上传控件并 `FileReader.readAsDataURL()` 输出 Data URL（纯前端、无依赖）；或删除所有反向文案，并把 formula-desc 改为真实解码流程。

### D-N140 base64 清空输入后仍下载上一张；SVG 被保存成 .png（中，确认源码缺陷，两个问题）

- 问题：① `generate()` 在空输入时 `return`，未清 `lastURL`，下载按钮继续指向旧结果；② 扩展名正则 `/data:image\/(\w+);/` 匹配不了 `image/svg+xml`（`+` 中断），回退 `png`。
- 证据：`tools/design/base64-to-image.html:255`（空输入提前返回）、`:261`/`:264`（成功/失败才改 `lastURL`）、`:267-273`（下载）、`:271`（扩展名正则）。
- 复现（node 复算）：`data:image/svg+xml;base64,…` → 正则无匹配 → ext=`png`；操作「成功转换→清空 textarea→点转换（提示请粘贴）→点下载图片」仍下载上一张图。期望清空即失效、SVG 存为 `.svg`。
- 影响：`tools/design/base64-to-image.html` 误存旧文件与错误扩展名。
- 方案：`generate()` 入口先 `lastURL=''`；扩展名用 `mime.split('+')[0]` 或 `svg+xml → svg` 映射。

### D-N141 base64 纯 Base64 一律按 PNG，FAQ 的「按 MIME 识别」未实现（低，文案与实现不一致，类型嗅探待真机验证）

- 问题：无 `data:` 前缀时硬补 `data:image/png;base64,`；不做魔数/MIME 识别，格式完全交给 `<img>` 解码；FAQ 与示例却称「按 data URI 中的 MIME 识别」「解码为二进制并识别格式」。
- 证据：`tools/design/base64-to-image.html:256-258`（补 PNG 前缀）、`:202`（FAQ 按 MIME 识别）、`:199`（示例「识别格式」）、`:157`（formula-eq 只写「交由 Image 加载校验」）。
- 复现：粘贴纯 JPEG/WebP Base64（无前缀）→ 被标成 `image/png` 再下载；不同浏览器对 MIME 与真实字节不一致的嗅探策略不同（待验证）。损坏/非图片数据由 `img.onerror` 拒绝（`:264`），这部分成立。
- 影响：`tools/design/base64-to-image.html` 类型信息与下载命名不可靠，FAQ 过度承诺。
- 方案：解码前读 4 字节魔数（PNG/JPEG/GIF/WEBP/BMP）或解析 SVG 头，按识别结果补 MIME；识别失败再回退 PNG 并提示。

### D-N142 tailwind 用亮度 0.5 阈值代替 WCAG 选黑白字，43/242 个色块文字对比度低于 4.5:1（中，确认源码缺陷）

- 问题：`const textColor = lum > 0.5 ? '#000' : '#fff'`；黑白字的等优点在 L≈0.179，而非 0.5。L 在 0.179–0.5 的色块被强制用白字，对比度不足；详情面板与导出表/CSV 的「建议文字色」复用同一错误。
- 证据：`tools/design/tailwind-colors.html:365-366`（渲染选字）、`:400`（数据表「建议文字色」）、`:433`（详情预览）、`:427`（导出 CSV）。
- 复现（node 按 WCAG 相对亮度+对比度全量复算 22×11=242 块）：选字后 <4.5:1 共 **43 块（17.8%）**；例：`yellow-500 #eab308` 选白字仅 **1.92:1**（黑字 10.95:1）、`slate-400 #94a3b8` 选白字 **2.56:1**（黑字 8.19:1）、`red-400 #f87171` 2.77:1（黑字 7.59:1）。期望按 `max(CR_black, CR_white)` 选字。
- 影响：`tools/design/tailwind-colors.html` 页面自称可查 WCAG，却给出不可读组合，并被 CSV 带出。
- 方案：分别计算黑/白对比度取高者；把 0.5 阈值改为 0.179 仅作快速近似并注明「精确值以对比度为准」。

### D-N143 tailwind 242 个色块是纯 div + onclick，键盘/读屏不可达（低，确认源码缺陷）

- 问题：色块 `<div class="shade" onclick="showDetail(...)">` 无 `tabindex`、无 `role`、无键盘事件；CSS 仅给 `cursor:pointer`。
- 证据：`tools/design/tailwind-colors.html:366`（色块标记）、`:34-35`（样式，仅 hover）。
- 复现：Tab 键遍历不会停在任何色块，Enter/Space 无响应；读屏不会将其识别为按钮。期望可用键盘打开详情。
- 影响：`tools/design/tailwind-colors.html` 可访问性不达标（同页却做 WCAG 对比度展示）。
- 方案：改为 `<button type="button">` 或补 `role="button" tabindex="0"` + `keydown` 处理 Enter/Space。

### D-N144 tailwind 详情里的「CSS 变量」名 `--tw-<color>-<level>` 不是 Tailwind 实际变量（低，确认文案错误）

- 问题：详情面板展示 `--tw-${name}-${level}`；Tailwind v3 无该变量，v4 官方命名是 `--color-${name}-${level}`。该值会被用户当真实 token 复制。
- 证据：`tools/design/tailwind-colors.html:447`（CSS 变量行）、`:435`（`bg-${name}-${level}` 类名本身正确）、`:448`（任意值类）。
- 复现：查 Tailwind v4 主题变量 → `--color-blue-500`；页面给出 `--tw-blue-500`，复制到 CSS 中变量不存在。
- 影响：`tools/design/tailwind-colors.html` 输出错误参考值。
- 方案：改为 `--color-${name}-${level}` 并标注适用 v4；或删掉该行只保留 `bg-/text-/border-` 类。

### D-N145 pixel-art 应用画布模板不写入历史，撤销后无法重做回模板（中，确认源码缺陷）

- 问题：`__paApplyTemplate` 先 `saveHistory()`（保存「应用前」快照）再改写 `pixels`；模板结果本身从未入栈。撤销可回到应用前，但 redo 只能回到同一张应用前图，模板丢失。
- 证据：`tools/design/pixel-art.html:863-880`（`:870` 先 saveHistory、`:871-877` 后写像素）、`:582-587`（saveHistory 推入当前快照）、`:598-604`（redo 读取 history）。
- 复现：空白画布 → 点「❤️ 爱心」→ 撤销（回到空白，符合预期）→ 重做 → 仍是空白（期望恢复爱心）；先画几笔再套模板同样无法 redo 回模板。
- 影响：`tools/design/pixel-art.html` 模板操作历史语义错位，用户误以为模板不可撤销/不可恢复。
- 方案：先写 `pixels` 再 `saveHistory()`（使模板成为新快照）；或在 saveHistory 后额外 push 模板状态。

### D-N146 pixel-art SEO 简介承诺「一键生成/复制 CSS 代码」，页面无 CSS 输出（中，确认文案与实现不一致）

- 问题：简介写「设计创意工具，可视化操作，一键生成 CSS 代码」，功能特点列「一键复制 CSS 代码」「支持实时预览与调试」；页面只有 Canvas 绘制与 PNG 导出，无 clipboard、无 CSS 文本输出。
- 证据：`tools/design/pixel-art.html:719`（简介）、`:723-724`（功能特点）、`:729-731`（使用场景还写「快速生成 CSS 效果代码」）；全页无 `clipboard`/CSS 输出，实际导出为 `toDataURL` PNG（`:628`）、按钮「导出原始/放大版」（`:203-204`）。
- 复现：页面无「复制 CSS」按钮，Ctrl+F「CSS 代码」只命中 `:719`、`:724`、`:731` 三处简介文本。
- 影响：`tools/design/pixel-art.html` 简介与真实能力不符（与另一页 `pixel-art-generator` 的 D-N98 不同页）。
- 方案：把简介改为「网格像素绘制、画笔/橡皮/填充/吸管、撤销重做、PNG 导出」，删除 CSS 卖点。

### D-N147 pixel-art 触摸未被 `touchcancel` 收尾，系统手势打断后仍处于绘制态（低，确认源码缺陷）

- 问题：只绑 `touchstart/touchmove/touchend`，未绑 `touchcancel`；触摸被系统手势/来电中断时 `isDrawing` 保持 true。
- 证据：`tools/design/pixel-art.html:647-649`（触摸绑定）；对照 `tools/design/signature-pad.html:557`（同项目另一页已处理 touchcancel）。
- 复现：移动端画到一半被系统手势打断（无 touchend）→ 之后若混合设备再收到 `mousemove`，`draw()` 仍会追加点并落笔，产生「鬼画」。
- 影响：`tools/design/pixel-art.html` 偶发误绘，需重新加载恢复。
- 方案：补 `canvas.addEventListener('touchcancel', endDraw, {passive:false})`。

### D-N148 signature-pad 笔宽滑杆与笔迹预设不更新 `strokeWidth` 变量，画笔恒定 3px（高，确认源码缺陷）

- 问题：`#strokeWidth` 的 `oninput` 只改 `#widthVal` 文本，从不写 JS 变量；`__spStrokePreset`（页面按钮）直接写变量所以有效，但工具栏预设 `__spApply` 只改滑杆 value 并 `dispatchEvent('input')`（同样只改文本）。新笔画在 `startDraw` 读取变量，故滑杆与工具栏预设都不影响实际粗细。
- 证据：`tools/design/signature-pad.html:169`（`oninput` 仅写 widthVal）、`:316`（变量初值 3）、`:412`（`width: strokeWidth`）、`:348`（按钮预设写变量）、`:674-678`（工具栏预设只 dispatch input）、`:375`（信息条显示变量值）。
- 复现：把滑杆拖到 8 → 标签显示 8，信息条仍「当前 3px」，画出的笔画仍 3px；点「🖍️ 马克笔粗（8px）」→ 同样 3px（且 1.5 对 `step=1` 还会被取整）。
- 影响：`tools/design/signature-pad.html` 核心笔宽控制失效，合同/批注等预设名不副实。
- 方案：滑杆 `input` 处理器中 `strokeWidth = +this.value; __spRenderInfo()`；`__spApply` 同时直接赋 `strokeWidth`（或让滑杆处理器成为唯一写入口）。

### D-N149 signature-pad 白色/网格背景下「导出 PNG」仍带背景，不是透明导出（中，确认源码缺陷）

- 问题：`drawBackground()` 把白底/网格直接画进主画布；`exportPNG()`（无参）只新建透明 tmp 后 `drawImage(canvas)`，因此背景选白色/网格时导出图仍带白底/网格。只有背景选「透明」时才真透明。
- 证据：`tools/design/signature-pad.html:465-480`（背景烘焙）、`:520-537`（导出，`:532-537` 仅在传入 `bgColor` 时铺色，否则直接复制主画布）、`:10`（meta「导出 PNG 透明背景」）。
- 复现：背景选「网格」→ 写几笔 → 点「⬇ 导出 PNG」→ 下载图含白底与 20px 网格线；期望按钮名对应的透明底。
- 影响：`tools/design/signature-pad.html` 的透明导出承诺只在一种背景模式下成立。
- 方案：导出时按笔画层重绘（只画 `strokes`、不画背景），或把按钮拆成「导出所见画布 / 导出透明 PNG」。

### D-N150 signature-pad 预设条与建议表放在 `touch-action:none` 的 canvas-wrap 内，移动端该区域无法滚动（中，确认源码缺陷）

- 问题：`.canvas-wrap` 设 `touch-action:none; overflow:hidden`，而 `#spPresets` 与 `#spRefTbl` 被放在该 wrap 内；手指在这两块区域上下滑动时，浏览器不接管页面滚动。
- 证据：`tools/design/signature-pad.html:29`（wrap 样式）、`:212-216`（canvas 与 presets/refTbl 同处 wrap）。
- 复现：手机打开页面 → 在签名板下方的预设条或「签署笔迹建议」表上上下滑动 → 页面不动；期望正常滚动（表格本身 `overflow-x:auto` 只解决横向）。
- 影响：`tools/design/signature-pad.html` 移动端近半屏区域成为「滚动死区」，长表格尤甚。
- 方案：把 presets/表格移出 `.canvas-wrap`，或只对 `#canvas` 设 `touch-action:none`。

### D-N151 colorblind 严重度滑杆对所有 8 型统一生效，与「完全型默认 100%」提示冲突（中，确认源码缺陷）

- 问题：滑杆写入全局 `S1.sev`，8 型卡片全部使用该值；提示却写「严重度仅在色弱型按默认 60% 起算，完全型默认 100%」。拖动滑杆后完全型也被降到低严重度；只有点击某类型卡片才重置为该类型的默认值。
- 证据：`tools/design/colorblind-simulator.html:223`（滑杆）、`:227`（提示）、`js/tools/colorblind-simulator.js:343`（写 `S1.sev`）、`:284-285`（所有类型用 `S1.sev`）、`:355`（点类型才重置默认）。
- 复现：初始选「红色盲（100%）」→ 拖滑杆到 20% → 8 张卡片（含红色盲）全部按 20% 渲染；期望完全型保持 100%，或提示改为「统一严重度」。
- 影响：`tools/design/colorblind-simulator.html` 严重度语义混乱，多类型对比失真。
- 方案：按类型维护 `sevByType`；滑杆只改当前选中类型、卡片各用自己的值；或明确改为「统一严重度」并删掉 60/100 的默认描述。

### D-N152 colorblind 安全配色「色相均分」策略没有任何色相项，与默认策略实质相同（中，确认源码缺陷）

- 问题：`hue` 分支评分 `score = minD − |cand.L − avgL| * 0.35`，只惩罚亮度偏离平均值，不含色相距离/色相分布项；与默认 `score = minD` 相比仅多了亮度惩罚，不会「均分色相」。
- 证据：`tools/design/colorblind-simulator.html:361`（选项文案「色相均分（保留色相感）」）、`js/tools/colorblind-simulator.js:971-974`（hue 评分）、`:975-976`（默认 minD）。
- 复现：同基准色、同数量分别选「色相均分」与默认「最大最小色差」→ 结果相同或仅亮度略变；色相不会沿色环均匀分布。
- 影响：`tools/design/colorblind-simulator.html` 策略名不副实，用户以为能控色相。
- 方案：加入与已选色的最小色相角差惩罚（或显式按 H 均分候选带），再与 minD 加权；否则删除该选项。

### D-N153 colorblind UI 模式标注「AAA 3:1」不符合 WCAG，对照拖动监听累积，导出名双扩展（低，确认源码缺陷，三个小问题）

- 问题：① `size==='ui'` 返回 `aa=3.0`、`aaa=3.0`，但 WCAG 2.2 的非文本对比度（1.4.11）只有 AA 3:1，不存在 AAA 档；② `buildCompare` 每次调用都在 `window` 上新增 `mouseup/touchend` 监听；③ 导出名直接拼 `S3.name`（含原扩展名）。
- 证据：`js/tools/colorblind-simulator.js:839-841`（阈值）、`:861-868`（表格 AAA 列）、`:687-690`（window 监听）、`:820` 与 `:709`（文件名）。
- 复现：选「UI 元素」→ AAA 列与 AA 列阈值同为 3.0（伪 AAA）；连续切换类型/标签 10 次 → window 上累积 10+ 个 `onUp`；上传 `photo.jpg` → 导出 `cvd-8types-photo.jpg.png`。
- 影响：`tools/design/colorblind-simulator.html` 引据不严谨、轻微监听泄漏、文件名脏。
- 方案：UI 模式只保留 AA 列或改标「非文本 AA」；把 `onUp` 提到初始化注册一次；文件名用 `S3.name.replace(/\.[^.]+$/,'')`。

### D-N154 7 个页面的 SEO 简介块共用「一键生成/复制 CSS 代码」套话，均无该能力（中，确认文案与实现不一致）

- 问题：除 colorblind 外，其余 7 页的「工具简介/功能特点」都写「设计创意工具，可视化操作，一键生成 CSS 代码」「支持实时预览与调试」「一键复制 CSS 代码」，但页面均无 CSS 生成或复制按钮。
- 证据：`tools/design/waveform-visualizer.html:509,513-514`；`tools/design/spectrum-visualizer.html:526,530-531`；`tools/design/base64-to-image.html:458,462-463`；`tools/design/data-matrix.html:490,494-495`；`tools/design/tailwind-colors.html:530,534-535`；`tools/design/pixel-art.html:719,723-724`；`tools/design/signature-pad.html:619,623-624`。
- 复现：任选一页 Ctrl+F「CSS 代码」→ 只命中简介；页面按钮与 JS 中无 `clipboard`/CSS 字符串输出（tailwind 只复制颜色值，不是 CSS 代码）。
- 影响：7 页同时出现与功能无关的卖点，降低工具可信度；colorblind 的简介（`:504-509`）是唯一按真实能力撰写的。
- 方案：按工具真实能力重写简介/功能特点（构建期按工具注入），删除「CSS 代码/实时预览与调试」通用套话。

### D-N155 waveform/spectrum/data-matrix/base64 的历史、数据表、CSV 恒为空（中，确认源码缺陷，同族 D-N59/D-N89/D-N91/D-N99）

- 问题：四页结果区 `#output` 只有 canvas/img 或纯预览 div，没有可读文本；`ResText()` 取 `#output.textContent` 后为空 → 历史永不记录、数据表无行、CSV 只有表头。base64 的历史恢复回调还会调用 `downloadImg()`，一旦有记录会“恢复即下载”。
- 证据：`tools/design/waveform-visualizer.html:178`（output 仅 canvas）、`:371-377`（ResText）、`:450`（导出 CSV）；`tools/design/spectrum-visualizer.html:176`、`:388-394`；`tools/design/data-matrix.html:172`、`:352-358`；`tools/design/base64-to-image.html:170`、`:324-330`、`:360`（恢复调 downloadImg）。
- 复现：连续生成/转换 5 次 → 历史页签为空，点「导出明细 CSV」只得到表头；`ResText` 的过滤还只排除「无效/错误/NaN」，无法补救空串。
- 影响：四页的历史/CSV/数据表入口全部失效，属结果区结构的系统性问题。
- 方案：`ResText` 返回参数+结果摘要（波形 `type|freq|amp|phase`、频谱 `bars|style`、矩阵 `text|size`、Base64 `mime|尺寸`）；把历史恢复回调改为纯重绘（base64 不要调 `downloadImg`）。

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

**留存建议（tools/design/colorblind-simulator.html）**：保留（本批功能最完整的页面）。建议按类型保存严重度、补真正的色相均分评分、去掉伪 AAA 列；已有 D-N102~D-N105 的四项旧问题仍应一并修复。

### 覆盖

- 实读：8/8 页整份 HTML（含内联脚本、deep-dive、FAQ、引据表），外加 `js/tools/colorblind-simulator.js` 全量（约 1100 行）。
- 新增 25 条：高 4（D-N131、D-N134、D-N137、D-N148）/ 中 14 / 低 7，编号连续 D-N131–D-N155。
- 未覆盖：`tools/design/` 其余工具页；colorblind 的 D-N102–D-N105 已存在，本批只补新角度（严重度语义、hue 策略、AAA/监听/文件名），不重复旧条。
- 未做：浏览器真实渲染与交互、`?lang=en-US` 运行态探针、移动端真机、`_build.py`/`run_gates.py` 门禁与线上验证；未改任何源码、未做 git 写操作。
- 复算说明：Tailwind 242 色对比度、频谱 CSS 拉伸后的圆环尺寸、Base64 扩展名正则、Data Matrix 图案与定位边方向均由 `node` 内存复算，未在页面内实测。

### D-N156 checker 输入 rgb() 时预览文字色回退旧值，与算出的比率不同步（中，确认源码缺陷）

- 问题：`calc()` 用 `'#' + fgStr.replace('#','')` 拼预览色，只对 3/6 位十六进制成立；`parseColor()` 明确支持 `rgb(r,g,b)`，此时拼成 `#rgb(255,0,0)` 非法，`style.color` 被浏览器丢弃，预览保留上一次颜色。
- 证据：`tools/design/checker.html:245-251`（接受 rgb）、`:301`（拼预览色）、`:302`（背景直接用 bgStr，反衬该处可正常工作）。
- 复现：前景输入 `rgb(255,0,0)`、背景 `#ffffff` → 结果 `4.00:1`、AA 未通过，但预览文字仍是默认深灰；期望变红。node 复算 `#FF0000/#FFFFFF = 4.00`。
- 影响：对比度判定与预览不同步，rgb() 输入下用户会按错误颜色目测。
- 方案：用解析后的 `fg` 生成 `rgb(r,g,b)` 赋给预览，背景同理。

### D-N157 checker 大号文字阈值写成 18px / 14px 粗体，与 WCAG 的 18pt / 14pt 差一档（中，确认标准错误）

- 问题：说明页把大号文字定义为「≥18px 或 ≥14px 粗体」。WCAG 2.1/2.2 的定义是 18 point（24 CSS px）或 14 point bold（≈18.66px）；页面同时混用 2.1（`:123`、`:229`）与引据表的 2.2（`:210`、`:215`、`:220`）。
- 证据：`:230`（阈值文案）、`:123`/`:229`（WCAG 2.1）、`:210`/`:215`/`:220`（WCAG 2.2）。
- 复现：19px 常规字重、对比度 4.0:1 → 页面按「大号文字」判 AA 通过；按 WCAG 应算正文（<24px）需 4.5:1，判不通过。
- 影响：常见字号下给出过于乐观的合规结论，设计评审/无障碍审计有实质风险。
- 方案：改为「≥18pt（≈24px）或 ≥14pt 粗体（≈18.66px）」，并把标准标注统一到 WCAG 2.2。

### D-N158 checker 支持 rgb() 输入但交换/取色回填经 `<input type=color>`，rgb() 下取色器被置黑并覆盖文本（低，确认源码缺陷）

- 问题：`swapColors()` 把文本值直接赋给 `#fgPicker/#bgPicker`。color input 只接受 `#rrggbb`，`rgb(...)` 或 3 位 hex 会被清成 `#000000`；随后用户动一下取色器，`syncColor()` 即把文本覆盖为 `#000000`。
- 证据：`:248-249`（接受 rgb）、`:274-281`（交换与回填）、`:264-272`（syncColor 覆盖文本）。
- 复现：前景 `rgb(255,0,0)`、背景 `rgb(0,0,255)` → 点「交换」→ 取色器显示黑色；再点任一取色器 → 文本被改成 `#000000`，原颜色丢失。
- 影响：rgb() 模式下的快捷操作会破坏已输入色值。
- 方案：赋给 color input 前统一 `toHex6(parseColor(v))`；或 rgb() 输入时禁用取色器回填。

### D-N159 analysis-64 「优势维度」未过滤负贡献，全线落后时仍把劣势当优势展示（中，确认源码缺陷）

- 问题：`adv` 只按贡献降序排序，`top=adv.slice(0,2)` 没有 `con>0` 过滤；只有 `need` 过滤了 `con<0`。当五个维度全部落后时，「优势维度」会显示两条负贡献。且 `formula-desc` 说优先补强取「贡献为负且权重最高」，代码实际按「最负」排序，两者口径不一致。
- 证据：`tools/design/analysis-64.html:276-284`（排序与 top）、`:118`（负贡献最大）、`:123`（权重最高）、`:297`（输出「优势维度」）。
- 复现（node 复算）：我方 5/5/5/5/5、竞品 9/9/9/9/9、均衡权重 → 总分差 −44.4%（我方落后），各维贡献 `-6,-6,-8,-10,-10`，页面「优势维度：价格竞争力（贡献 -6.0）、功能完整度（贡献 -6.0）」。
- 影响：结论区把拖累项标成优势，直接误导竞品决策。
- 方案：`adv = gaps.filter(g=>g.con>0)` 后再排序；为空时输出「无明显优势维度」；并把 `need` 的排序口径（按权重或按最负）写死并同步文案。

### D-N160 analysis-64 简介块缺 `<ul>` 开标签与两个小标题，6 条 `<li>` 裸挂在 div 下（中，确认源码缺陷）

- 问题：`工具简介` 段落之后直接出现 `<li>`，随后两个 `</ul>` 无对应开标签；「功能特点」「使用场景」两个 `<h4>` 也缺失。浏览器把 6 条 li 当无列表文本渲染，折叠区层级消失。
- 证据：`:341-353`（`:342` 段落、`:343-347` 与 `:349-352` 均为裸 li、`:348`/`:353` 为孤立 `</ul>`）。
- 复现：查看 DOM → `.tool-intro-body` 下没有 `ul`；展开「工具简介」只见无项目符号文本，且无「功能特点/使用场景」标题。
- 影响：介绍区结构语义与可读性受损，构建/英文替换也难以按列表定位。
- 方案：在 `:343` 前补 `<h4>…功能特点</h4><ul class="intro-features">`，在 `:349` 前补 `<h4>…使用场景</h4><ul>`，并补齐对应闭合。

### D-N161 analysis-64 权重敏感性提示无条件建议「切换重体验」，当前已是重体验时自相矛盾（低，确认文案缺陷）

- 问题：`:299` 固定句式「当前「X」权重下 价格竞争力 占 Y%，若企业实际更看重体验，可切换「重体验」」。当 X=重体验 时，等于建议切到当前已选方案；同时固定拿 `DIMS[0]`（价格）举例，忽略当前权重里价格可能不是最低。
- 证据：`:299`（固定文案与 `DIMS[0]`）。
- 复现：选「重体验」→ 提示仍写「若企业实际更看重体验，可切换『重体验』」。
- 影响：文案自指，削弱建议可信度。
- 方案：按当前 bias 选择一句「可切换的对比方案」，并从当前权重最低的维度取示例。

### D-N162 stripe-pattern 宣称「导出图片」，实际只有 CSS 文本与复制，没有任何图片下载（高，确认承诺与实现不符）

- 问题：meta/简介/formula-desc 三处写「纯前端导出图片」「可导出图片」；页面与脚本中没有 canvas、toDataURL、Blob、download、SVG 生成，结果区只有 `#preview` 与只读 `#cssOutput`。
- 证据：`:10`（meta）、`:154`（formula-desc）、`:156`（简介）、`:177-178`（结果区）、`:259-284`（生成逻辑）、`:171-172`（仅有「导出明细 CSV / 复制 CSS」）。
- 复现：Ctrl+F `png|download|toDataURL|canvas|Blob` → 0 命中；点遍按钮只能得到 CSS 文本，无法产出可用于包装/印刷的图片。
- 影响：以「图片导出」获客的页面无法交付承诺物；包装/印刷场景不可用。
- 方案：补「导出 PNG」（离屏 canvas 绘制 repeating 条纹，尺寸/倍率可选）与「导出 SVG」；同步改文案。

### D-N163 stripe-pattern 结果区只有空预览 div，历史/数据表/CSV 永久为空（中，确认源码缺陷，同族 D-N155）

- 问题：`#output` 只包一个空 `#preview`，`ResText()` 读 `#output.textContent` 得到空串并直接返回 ''；CSS 写在 `<textarea>` 的 `value` 里，textContent 读不到。`__stripe_patternExtras` 因此从不 record，表格/CSV 永远只有表头。
- 证据：`:175`（结构）、`:331-337`（ResText）、`:410`（导出）、`:278`（写 textarea.value）。
- 复现：连续生成 5 次 → 历史 tab 空；点「导出明细 CSV」→ 仅表头。
- 影响：历史回看与 CSV 导出入口全失效。
- 方案：`ResText` 返回 `角度|宽度|类型|色1|色2` 摘要，或直接读 `#cssOutput.value` 并截断。

### D-N164 stripe-pattern 双线型在宽度 <6px 时停点越界，实际周期为 w+6 而非 2×w（低，确认源码/复算缺陷）

- 问题：双线型停点 `w+6` 与末点 `w*2` 在 w<6 时逆序；CSS 会把小于前值的停点抬到前值，末段 c2 变成零宽，重复周期变成 `w+6`，与 formula-eq 写的「色二 宽度+6→2×宽度」自相矛盾。
- 证据：`:153`（公式）、`:271`（停点串）。
- 复现（node）：w=2 停点 `0,2,2,5,5,8,8,4` → 末点被抬到 8，周期 8；w=5 停点 `0,5,5,8,8,11,11,10` → 周期 11。期望周期 4/10。
- 影响：窄条纹下预览与说明不一致，按公式推算会错。
- 方案：四个停点按宽度比例分配（间隙取 `min(3, w/2)`），或在 w<6 时禁用双线型；同步改公式。

### D-N165 dot-pattern 宣称「导出透明或纯色图片」，实际无任何图片导出（高，确认承诺与实现不符）

- 问题：meta 与简介/formula-desc 都写导出图片；脚本只有 CSS 文本，没有 canvas/download/Blob/SVG；按钮只有「导出明细 CSV / 复制 CSS」。
- 证据：`:10`（meta）、`:154`（formula-desc）、`:156`（简介）、`:175-176`（结果区）、`:257-273`（生成逻辑）、`:171-172`（按钮）。
- 复现：Ctrl+F `png|download|toDataURL|canvas|SVG` → 0；无下载按钮，预览只是 DOM 背景。
- 影响：透明底 PNG / SVG 底纹无法产出，「印刷稿」用途落空。
- 方案：canvas 平铺绘制并支持透明/背景色两种导出；或用 `<svg><pattern>` 生成矢量下载。

### D-N166 dot-pattern 结果区只有空预览 div，历史/数据表/CSV 永久为空（中，确认源码缺陷，同族 D-N155）

- 问题：`#output` 内只有空 `#preview`；`ResText()` 读其 `textContent` 为空即返回 ''，`__dot_patternExtras` 从不写入历史。
- 证据：`:175`（结构）、`:325-331`（ResText）、`:404`（导出）、`:272`（写 textarea.value）。
- 复现：切换排列方式生成 5 次 → 历史空、CSV 仅表头。
- 影响：历史与明细导出入口失效。
- 方案：ResText 返回 `排列|点径|间距|背景|点色` 摘要。

### D-N167 dot-pattern 引据称 SVG pattern/矢量输出，实际是 CSS radial-gradient；选项「渐变大小」也不改变点径（中，确认引据与实现不符）

- 问题：引据表两行都写 `SVG pattern` / `vector output stays crisp`，但实现是 `radial-gradient` CSS 背景（无 SVG、无矢量文件）；排列选项「渐变大小」实际只把边缘从硬边改成柔边，点半径仍为 `size/2`，点的大小不变。
- 证据：`:229-230`、`:238-240`（SVG/矢量）、`:168`（选项名）、`:153`（公式称「柔边排列」）、`:268-269`（实现）。
- 复现：选「渐变大小」→ 点径与方格模式相同，只有边缘变虚；输出仍是 CSS 字符串。
- 影响：技术引据失实，选项名与行为不符。
- 方案：改为 SVG pattern 实现，或把引据换成「CSS radial-gradient 平铺」；选项改名「柔边圆点」。

### D-N168 generator-6 标题/描述承诺「拖动控件调整偏移、模糊、扩散、颜色」，实际只有 1 个「生成数量」输入（高，确认承诺与实现不符）

- 问题：页面 `input` 总数只有 `#cnt`，所有阴影参数（x/y/blur/spread/color/inset/层数）都由 `Math.random` 决定；没有滑杆、颜色选择器或 inset 开关，也没有「多层叠加」编辑能力。
- 证据：`:10`（meta）、`:113`（简介）、`:115-116`（公式/desc）、`:120-121`（唯一输入与工具栏）、`:219-243`（全随机生成）。
- 复现：`document.querySelectorAll('input[type=range]').length === 0`；改 cnt 只能改变条数，无法调任何阴影参数。
- 影响：工具名「可视化调整」名不副实，用户无法得到目标阴影，只能反复随机。
- 方案：补 offsetX/Y、blur、spread、color、inset、层数滑杆与实时预览；或改名为「随机阴影生成器」并删掉「拖动控件」承诺。

### D-N169 generator-6 「层级体系」预设只是随机条数，不构成有序 elevation，且每次点击重掷（中，确认语义缺陷）

- 问题：预设仅设置 `cnt`，`gen()` 每条独立随机 1–3 层、偏移/模糊/扩散/透明度全随机，因此「8 组阴影（层级体系）」「15 组（完整规范）」产出的是互不相关的随机样式，不能作为设计系统的 elevation scale；连续点击还会整批重掷。
- 证据：`:419-422`（预设只给 cnt）、`:223-232`（逐条随机）。
- 复现：点「8 组阴影（层级体系）」两次 → 两组结果完全不同，且第 1 组可能比第 8 组更重；期望按层级递增（如 blur/offset 随层级增大）。
- 影响：预设名误导，无法沉淀为可复用规范。
- 方案：预设按层级生成参数（blur=4/8/12…、y=1/2/4…、透明度递减），随机仅作可选模式。

### D-N170 generator-6 生成数量输入非法/清空时静默回落 5，无提示且键入即重掷（低，确认行为缺陷）

- 问题：`parseInt(value)||5` 把空串、`0`、负数（负数经 max 夹到 1，但 0 直接变 5）都当 5；输入框 min/max 只约束步进器，手输 `0` 仍触发生成 5 条，无任何校验提示。
- 证据：`:220`（回落逻辑）、`:120`（`oninput="gen()"`）。
- 复现：清空「生成数量」→ 立刻变成 5 条；输入 `0` → 生成 5 条；期望提示范围 1–50 或保留上次值。
- 影响：用户以为输入生效，实际条数被静默替换，且每次按键都重掷整批。
- 方案：用 `Number.isFinite` 校验并提示；非法时不清空/不重掷，改用 `change` 触发。

### D-N171 css-border-radius 简单模式滑杆上限 150px，隐藏的进阶滑杆 max=100，>100px 时预览与代码被夹到 100px（高，确认源码缺陷）

- 问题：`#allRadius` 是 0–150，联动时把值写给 8 个 `max=100` 的 range；HTML range 的值会被清洗到 max，于是 `tl1=100`，`updateRadius()` 生成 `100px` 并把 `#allVal` 改回「100px」，但滑杆拇指仍在 120–150 处。
- 证据：`:213`（max=150）、`:227`/`:232`/`:242`/`:247`/`:257`/`:262`/`:272`/`:277`（max=100）、`:414-426`（回写）、`:451-457`（生成 CSS 并回写标签）。
- 复现：拖动到 150 → 标签闪成「100px」，`#cssOutput` 为 `border-radius: 100px …`，滑杆停在 150；期望 150px 且标签与拇指一致。
- 影响：核心「实时预览/代码生成」在最常用的大圆角区间失真，150px 整段无效。
- 方案：把 8 个进阶滑杆 max 统一为 150（或简单模式单独维护 150 上限，不写进阶滑杆）。

### D-N172 css-border-radius 关闭「四角联动」后，简单模式唯一滑杆完全失效（中，确认源码缺陷）

- 问题：`updateAll()` 仅在 `linkCorners` 勾选时把 `allRadius` 写入 8 个角；取消勾选后仍调用 `updateRadius()`，后者只读旧的角值。简单模式没有其它可编辑控件，于是滑杆拖动无任何视觉/代码变化。
- 证据：`:216`（checkbox）、`:413-429`（分支与回写）、`:431-451`（只读角值）、`:409-410`（进阶模式隐藏）。
- 复现：切到简单模式 → 取消「四角联动」→ 拖动圆角滑杆 20→80 → 预览与 CSS 不变；期望至少作用于四角或提示需切到进阶模式。
- 影响：用户可见的死控件，误以为工具卡死。
- 方案：未勾选时禁用滑杆并提示「请切换到进阶模式分角调整」，或仍按统一值更新四角。

### D-N173 css-border-radius 结果在 `<textarea>` 的 value 里，ResText 读 textContent 恒为空，历史/CSV 全空（中，确认源码缺陷，同族 D-N155）

- 问题：`#cssOutput` 是 `<textarea readonly>`，代码写 `value`；`__css_border_radiusResText()` 对 `#cssOutput` 读 `textContent`（textarea 的文本节点为空），因此永远返回 ''，`__css_border_radiusExtras` 从不记录。
- 证据：`:286`（textarea）、`:454`（写 value）、`:649-655`（读 textContent）、`:741`（历史钩子）。
- 复现：拖滑杆 5 次或应用 4 个预设 → 历史 tab 空、数据表无行、「导出明细 CSV」只有表头。
- 影响：历史与导出入口失效。附带：本页无 `#css_border_radiusPresets` 占位 div，`ensureHost` 会回退到 `body` 并把预设条插到页面最顶部（`js/tool-kit.js:1028-1029`）。
- 方案：ResText 改读 `#cssOutput.value`；同时在正文放 `#css_border_radiusPresets` 占位 div。

### D-N174 tester-assessor 「可学习性」子量表用了第 5 题（sus4），不是第 4 题（sus3）（中，确认源码缺陷）

- 问题：Brooke 的可学习性 = Q4 + Q10；代码取 `sus4`（第 5 题，正向「功能整合得好」）与 `sus9`（第 10 题），标签却写「第4、10题」。改 Q4 不影响子量表，改 Q5 反而影响。
- 证据：`:210-221`（题目顺序，Q4=索引3、Q5=索引4）、`:269-276`（SUS 计分）、`:335`（learnability 用 sus4）、`:336`（可用性=总分−可学习性）。
- 复现：默认全 3 分 → 可学习性 10；把 Q4 改成 1 → 页面不变（应 15）；把 Q5 改成 1 → 页面降到 5（不应受影响）。
- 影响：子量表口径错误，SUS 明细误导可用性诊断。
- 方案：改用 `sus3`；同步核对「可用性 = 其余 8 题」的推导。

### D-N175 tester-assessor 历史快照被截到前 12 个输入，SUS 只存 4 题，恢复后结果与记录不符（中，确认源码缺陷）

- 问题：快照按 DOM 顺序收集 18 个键（8 个数值 + 10 个 SUS select），`keys.slice(0,12)` 只保留前 4 个 SUS 题；恢复回调只回填这 12 个，剩余 6 题保留当前值，随后 `calc()` 重算，得到与记录不同的分数。
- 证据：`:466-476`（收集顺序）、`:531-535`（截断 12）、`:503-517`（恢复并 calc）、`:269-270`（10 个 select）。
- 复现：默认全 3 分（SUS 50）→ 评估 → 把第 10 题改为 1（SUS 45）→ 在历史点「恢复」→ 分数仍 45，而该记录结果文本是 50。
- 影响：历史恢复不可信，跨记录对比失真。
- 方案：按字段白名单/分组保存全部 18 键（或把 SUS 存成数组），去掉 12 键截断。

### D-N176 tester-assessor `<title>` 含残句「助 / 满意度）」，description 在「、」处截断（中，确认文案缺陷）

- 问题：标题为「可用性（测试/评估/改进）流程 - 助 / 满意度）」，末尾残留「助 / 满意度）」；description 恰好在 120 字处停在「输出 SUS 等级、」，句子未完成（疑为按 120 字截取）。
- 证据：`:10-11`；同类 120 字截断也出现在 `tools/design/analysis-64.html:10`（末尾「…优先补强维」）。
- 复现：查看 `<head>` 或搜索结果标题 → 「可用性（测试/评估/改进）流程 - 助 / 满意度）」；描述无结尾。
- 影响：搜索结果与分享卡片出现残句，降低点击与可信度。
- 方案：重写为「可用性测试与评估（SUS 量表 + 任务绩效）— 在线计算」，描述补全为完整句并控制在 150 字内。

### D-N177 aztec-code 生成的是哈希 + LCG 随机格，不是 Aztec 编码，无纠错/版本/定位，任何扫码器都读不出（高，确认源码缺陷）

- 问题：实现只对文本做 32 位 hash 作为 LCG 种子填格，再画 3×3 靶心、两侧数据环与 4 个角点；没有模式消息、Reed-Solomon 纠错码字、层/版本选择、参考网格，不符合 ISO/IEC 24778。meta 却写「用于票据与物流信息的移动端识读」，deep-dive 写「可扫描」「扫码即得原文」。
- 证据：`tools/design/aztec-code.html:259-292`（hash+LCG+固定靶心）、`:293-304`（逐格绘制）；`:10`、`:196`、`:199`、`:233`（按数据量选 compact/full）。
- 复现：生成任意文本（如 `TB-2026-009`）→ 用手机扫码器/Aztec 解码库读取 → 无输出（随机格不构成合法码字）；期望解出原文。
- 影响：票据/物流等识读场景会直接失败，属核心功能虚假。
- 方案：接入成熟的 Aztec 编码库（锁定版本，纯前端），按字符集/ECI 选择 compact/full 与纠错级别；否则改名「随机矩阵纹理」并删除所有识读承诺。

### D-N178 aztec-code 矩阵尺寸只由滑杆决定，与文本长度/容量无关；预设 8/10 还低于 min=11（中，确认源码缺陷）

- 问题：`size` 仅取输入值并夹到 11–25（偶数 +1），文本只影响 hash；因此 10 字符与 200 字符生成同尺寸矩阵。FAQ 写「过长会超出容量无法生成」，引据写「compact/full by payload size」均不成立。预设 `size:10`/`8` 写进 number input 后显示 10/8，但生成时被夹成 11，UI 与实际不符。
- 证据：`:162`（min=11）、`:256-258`（尺寸处理）、`:259-262`（只做 hash）、`:203`（容量承诺）、`:448-451`（预设 10/8）。
- 复现：输入 `"A"` 与 200 字符文本 → 同一 15×15；点「紧凑型大容量码」→ 输入框显示 8，实际 canvas 11×11。
- 影响：容量/版本承诺失实，尺寸参数语义混乱。
- 方案：按编码后码字长度选择版本并拒绝超容量输入；至少让输入显示值等于实际矩阵尺寸（预设改 ≥11 或回写夹取后的值）。

### D-N179 aztec-code 历史钩子包在 `downloadImg` 上且 `#output` 无可读文本，历史/CSV 永远为空；改文本后下载仍是旧图（中，确认源码缺陷）

- 问题：`__aztec_codeExtras` 由 `downloadImg` 包裹（不是 `generate`），而 `ResText` 读 `#output`（只有 canvas）得到空串 → 从不 record。`lastURL`/预览仅在 generate 时更新，文本或颜色改了但没点生成时，点「下载」仍下载上一张 PNG。
- 证据：`:453-455`（包裹 downloadImg）、`:363-369`（读 output）、`:305-307`（空文本 + canvas）、`:309-312`（下载用 lastURL）。
- 复现：生成 3 次 → 历史空、CSV 仅表头；改文本为 `NEW` 不点生成直接点下载 → 得到旧文本的 PNG。
- 影响：历史/导出失效，下载结果与当前输入不一致，易误交付。
- 方案：把 Extras 钩到 `generate`；ResText 返回 `文本摘要|尺寸|前景|背景`；输入变更时清空 `lastURL` 并禁用下载。

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

### D-N180 平仄字库错收：示例《静夜思》20 字误标 8 次（高，确认缺陷）

- 问题：`PING` / `ZE` 两库数据本身错误且大量交叉收录——「明、疑、头、低、思」只在仄库，「望」同时在两库；判定又是先查 PING（`:218-219`），于是常用平声字被判「仄」、「望」被判「平」。内置示例诗直接演示错误结果；且两库去重后仅 172 / 2043 字，与文案「198 / 2086 字」不符。
- 证据：`tools/design/checker-5.html:197`（PING 字串）、`:200`（ZE 字串）、`:218-219`（先 PING 后 ZE）；字数文案 `:130`、`:308`；示例诗 `:135-138`。
- 复现：node 读取两处 `new Set(...)` 字串复算：PING 原始 198 字符 / 唯一 172，ZE 原始 2086 / 唯一 2043，PING 的 172 字中有 118 字同时出现在 ZE。按 `:218-219` 逻辑跑《静夜思》20 字，误标 8 次：`明→仄(应平)`×2、`头→仄(应平)`×2、`疑→仄(应平)`、`低→仄(应平)`、`思→仄(应平)`、`望→平(应仄)`，即 40% 字位错标。
- 影响：工具唯一输出就是平仄串；示例即出错会让用户对整库失去信任，格律自查结论被反向。
- 方案：改为「单字→平/仄/两读」映射（`Map`）并删交叉收录：把 明/疑/头/低/思 移入 PING，望/长/广/忘 从 PING 移出；多音字标「两读」而非强行归一；文案字数改为去重后的实际值。

### D-N181 deep-dive 使用场景/FAQ 与本工具无关（中，确认缺陷）

- 问题：「使用场景」「常见问题」写的是公众号/博客稿件批量审校（标题层级、img alt、外链有效性、重复段落），与平仄标注毫无关系；FAQ「能替代人工审校吗」直接答「层级/链接/重复」，属模板串页。
- 证据：`tools/design/checker-5.html:262`、`:264`、`:267`、`:271-272`。
- 复现：滚动到「使用场景」→ 例 1 为「公众号/博客发布前，批量扫标题层级、图片 alt、外链有效性」；全文无标题/链接/alt 检查能力（平仄逻辑仅 `:206-231`）。期望场景是近体诗自查、填词选调、对联平仄核对。
- 影响：SEO 正文与工具语义冲突，按场景进来的用户找不到入口；亦属套话质量门禁风险。
- 方案：整段替换为格律诗场景；FAQ 改为「多音字/入声字怎么处理」「为什么出现 ?」「能替代韵书吗」。

### D-N182 「预设」页签为空 + 句切分口径不符（低，确认缺陷）

- 问题：页签有「预设」，但 `__checker_5Presets()` 在 `TBKit` 判空后没有任何 `TBKit.preset.bar(...)`，点开永远空白；公式写「按空行切分为句」，实现却是 `split(/\n+/)`，任何换行都切句，标点（，。！）也被当单字计入「未收录」。
- 证据：`:141`（`#checker_5Presets` 宿主）、`:422-424`（空实现）；`:129`（公式「按空行切分」）、`:207`（`split(/\n+/)`）、`:216`（逐字符未排除标点）。
- 复现：点「预设」→ 无按钮；把「床前明月光，疑是地上霜。」粘成一行 → 输出 11 个徽章，「，」「。」标「?」。期望按标点断句且标点不计入字数。
- 影响：预设空白像页面故障；标点污染「未收录」计数，五言/七言行校验失真。
- 方案：补 3 个预设（五绝/七律/自定义）；切句改 `split(/[，。！？；、\n]+/)`，或在逐字循环中跳过 `\u3000-\u303f` 与 ASCII 标点。

### D-N183 涂料「限值要求」与判定阈值四套口径（高，确认缺陷）

- 问题：内墙涂料实际按 `voc<=30 && bz<=10` 判优等、`voc<=80 && bz<=50` 判合格，但结果里的「限值要求」写 `VOC≤80g/L`（优等）、`VOC≤120g/L`（合格）、`VOC>120g/L`（不合格）；简介块写 30/80，注意事项又写 80/120，公式块再写「VOC≤80 为优等」。同一页四套数。
- 证据：`tools/design/detector-28.html:230-232`（判定条件 vs `limit` 文案）、`:118`、`:208`、`:115`。
- 复现：材料选「内墙涂料」，VOC=60、苯系物=30（页面自带预设 `:426`）→ 等级「合格品」，但「限值要求」显示 `VOC≤120g/L`，而判定实际 80 即截止。期望显示 `VOC≤80g/L 且 苯系物≤50mg/kg`。
- 影响：验收/采购会把 80–120 g/L 的涂料误认为「符合限值」，属结论级误导。
- 方案：`limit` 由阈值常量统一生成（优等 30/10、合格 80/50），删除 `:208` 的 80/120，并让简介、公式、结果、注意事项共用同一常量。

### D-N184 板材三级阈值与引据表冲突，「E1 临界」预设被判 E2（中，确认缺陷）

- 问题：代码把 0.025/0.050/0.124 依次当 E0/E1/E2，引据表却写「E1 级甲醛释放量不超过 0.124」；GB 18580-2017 实际只有 E1≤0.124（气候箱法），E0(≤0.050)/ENF(≤0.025) 出自 GB/T 39600-2021，E2 在 2017 版已取消。页面把两套标准拼成三级，并把「干燥器法」与 mg/m³ 混用（干燥器法单位是 mg/L）。
- 证据：`:115`、`:117`、`:225-228`（三级阈值）、`:187`（引据表 E1≤0.124）、`:207`（「干燥器法」+ mg/m³）。
- 复现：选预设「人造板超标排查（E1 临界）」（`:425`，formaldehyde=0.12）→ 结果「E2级（限室内）」，而同一页引据表说 E1 上限是 0.124。期望同为 E1，或明确标注「按 GB/T 39600 分级」。
- 影响：板材验收结论与引据自相矛盾，0.05–0.124 区间到底算 E1 还是 E2 无法判断。
- 方案：统一一套标准：GB 18580-2017 只判 E1≤0.124 / 不合格；要 E0/ENF 则改引 GB/T 39600-2021 并写明 E0≤0.050、ENF≤0.025，删除 E2；单位改为气候箱法 mg/m³ 或干燥器法 mg/L。

### D-N185 空值/负值被当 0 判「优等」，甲醛标尺不分材料（中，确认缺陷）

- 问题：`+value||0` 让空串、0、负数都变 0，直接落进最优档；且 `refBar` 无论材料类型都画甲醛 E0/E1/E2 标尺，涂料/胶粘剂按 VOC/苯系物分级时标尺与结论口径无关。
- 证据：`:219-221`（`||0`）、`:225`（hcho<=0.025→E0）、`:230`（voc<=30→优等）、`:245`（refBar 固定 hcho bands）。
- 复现：清空「甲醛释放量」→「E0级（优等）」；清空 VOC 与苯系物且选涂料 →「优等品」。选「内墙涂料合规验收」（hcho=0.05、voc=60、bz=30）→ 结论「合格品」，右侧标尺却落在甲醛「E1级（合格）」区间。期望空值提示「请输入」并禁用判定，标尺按材料切换。
- 影响：空表单=最优等级，可被截图当作「检测合格」；标尺与结论冲突降低可信度。
- 方案：先校验 `Number.isFinite` 且 >0，空/负值返回错误提示；`refBar` 按 `matType` 选 bands，涂料/胶粘剂不显示甲醛标尺。

### D-N186 14 项清单无 AAA 项，AAA 等级/通过行是死逻辑（中，确认缺陷）

- 问题：`a11yItems` 14 项全部 A/AA，没有 `level:'AAA'`；`levelAAA_total` 恒 0，`:334` 的 AAA 分支永不进入，`:396` 的 AAA 行恒「○ 可选」，`:393` 百分比恒「—」，`:417` 的 AAA 建议恒不出现。简介却宣称「A/AA/AAA 三级合规等级自动判定」。
- 证据：`tools/design/detector-29.html:198-211`（清单数据）、`:303`、`:314-319`、`:334`、`:393`、`:396`、`:417`；宣称见 `:10`、`:461`、`:508`。
- 复现：14 项全勾、对比度 7:1 → 最高仍「AA级合规」；「合规清单」表 AAA 行永远「0/0 — ○ 可选」。期望出现 AAA 项并可判 AAA，或删掉 AAA 行。
- 影响：整块 AAA UI 不可达，无论怎么操作都拿不到 AAA，功能承诺落空。
- 方案：补 3–4 个 AAA 项（1.4.6 对比度≥7:1、2.4.9 链接目的、1.4.8 视觉呈现），或在 `:396`/`:417` 删 AAA 并改简介为「A/AA 两级」。

### D-N187 颜色预览一旦报错就永久显示错误文案（中，确认缺陷）

- 问题：非法色值时把 `#colorPreview` 的 `textContent` 改成「颜色格式错误…」；之后颜色合法只回填 `style.color/background`，从不恢复示例文字，预览块永远是错误提示。另输入无 `#` 的 `1F2937` 能算出对比度，但 `style.color='1F2937'` 是非法 CSS，预览前景不生效。
- 证据：`tools/design/detector-29.html:271-278`（合法分支只设样式、非法分支改 textContent）。
- 复现：前景输入 `#GGGGGG` → 预览变错误文案；再改回 `#1F2937` → 对比度恢复 14.68、结果表正常，预览块仍显示错误文案。期望恢复示例文本并用解析后的 `rgb()` 回填。
- 影响：修正输入后仍像「坏了」，用户反复改色；无 `#` 合法输入预览不更新。
- 方案：示例文案存变量，合法分支 `preview.textContent=原文` 并赋 `rgb(r,g,b)`；非法分支只加错误 class，不改文本。

### D-N188 AA/AAA 表格「通过」与顶部等级口径不一致（中，确认缺陷）

- 问题：等级判定 `:333` 要求 `contrastLevelAA` 才给 AA 级，但 AA 行 `:395` 的「✓ 通过」只看清单勾选、不看对比度；AAA 行 `:396` 只看 AAA 勾选与 `contrastLevelAAA`，不要求 A/AA 全过。于是「14 项全勾但对比度 3.0:1」会同时出现等级「A级合规」与 AA 行「✓ 通过」。
- 证据：`:333-344`（conformanceLevel）、`:395`（AA 行缺 `contrastLevelAA`）、`:396`（AAA 行缺 A/AA）。
- 复现：14 项全勾，前景 `#949494` / 背景 `#FFFFFF`（正常文字约 3.0:1）→ 顶部「A级合规」，AA 行「✓ 通过」。期望 AA 行「○ 未达标」且与顶部一致。
- 影响：同页给出两个相反结论，清单工具的核心价值（合规判定）失效。
- 方案：抽出 `isAAPass()` / `isAAAPass()`，顶部等级与三行表格全部复用；AA 行加 `contrastLevelAA`，AAA 行加 A/AA 全过。

### D-N189 背景纹理生成器只有「数量」一个输入，图案/颜色/尺寸全随机（高，确认缺陷）

- 问题：meta 与简介承诺「调节参数生成…实时预览并导出代码」「参数可调」，实际只有 `#cnt` 一个数字输入；图案按 `i % 6` 固定轮换、尺寸 `randInt(8,64)`、颜色随机。用户无法选点阵/网格/波浪、无法调色与密度，也无法复现上次结果。
- 证据：`tools/design/generator-11.html:10`、`:116`（参数可调）、`:120`（唯一输入）、`:218`（图案按索引轮换）、`:216`、`:221`（随机尺寸/颜色）。
- 复现：输入 5 → 固定得到「圆点/条纹/网格/棋盘/斜纹」前 5 种；再点「生成」→ 类型顺序不变、颜色尺寸全变。期望可选图案、设主/底色与 tile 尺寸并得到可复现输出。
- 影响：核心 generator 退化为随机样例展示，与 generator-6/7/10 同质；无法产出符合品牌色的纹理。
- 方案：补「图案类型」select、「主色/底色」color、「尺寸/线宽」range；`randInt` 改读输入；`i % patterns.length` 仅用于「随机混合」模式。

### D-N190 预设「N 种纹理」只改数量，15 条实为 6 种循环（中，确认缺陷）

- 问题：三个预设的 values 都只有 `cnt`，点击只改生成条数；纹理种类仍由 `i % 6` 决定，15 条里只有 6 种图案循环重复，并非 15 种不同纹理。
- 证据：`tools/design/generator-11.html:409-411`（预设仅 cnt）、`:218`（类型轮换）。
- 复现：点「15 种纹理（丰富）」→ 实际 6 种图案各重复 2–3 次。期望 15 种不同类型，或预设名改为「15 条纹理」。
- 影响：预设文案夸大能力，用户点完发现「丰富」等于同样 6 种。
- 方案：预设改名「3/8/15 条」，或让预设同时设置图案集合；若要「丰富」，扩到 ≥15 种 pattern。

### D-N191 历史趋势图恒空（低，确认缺陷）

- 问题：`__generator_11ResText()` 返回以「生成结果：」开头的文本，趋势图却用 `parseFloat(rec['结果'])`，恒 NaN，`nums.length>=2` 永不成立，图表页签一直空白。
- 证据：`tools/design/generator-11.html:216`（结果前缀）、`:343-349`（原样返回）、`:385`（parseFloat）、`:389`（nums>=2 才画）。
- 复现：连续生成 3 次切「图表」→ 无折线；`parseFloat('生成结果： 1. 圆点纹理…')` = NaN。期望横轴有 3 个时间点。
- 影响：历史/趋势页签形同虚设。
- 方案：历史记录另存结构化数值列（`count`/`size`），图表用该列；或 ResText 返回 `cnt|size|color` 供解析。

### D-N192 承诺「导出图片 / Canvas 处理」，实际只有 CSS 文本（高，确认缺陷）

- 问题：meta/og/简介/FAQ 反复承诺「纯前端导出图片」「可调格子大小与配色并导出图片」「处理大图用 Canvas 完成」，但页面只有 `#preview` 背景与 `#cssOutput` 文本域 + 复制/CSV，全文无 canvas、无 `toDataURL`、无 SVG/PNG 下载。
- 证据：`tools/design/isometric-grid.html:10`、`:15`、`:157`、`:159`（导出图片）、`:206`（Canvas 大图）；实际 `:172-173`、`:259`（仅 CSS）。
- 复现：找遍按钮 → 只有「生成/复制/导出明细 CSV」；全文无 `<canvas>` / `toDataURL` / `.png` 链接，唯一「Canvas」字样就是 FAQ `:206` 的虚构说明。期望点「导出图片」得到 PNG，meta 主卖点无法兑现。
- 影响：SEO 描述与实际功能不符，按「导出图片」进来的用户找不到入口；FAQ 的 Canvas 说法纯属虚构。
- 方案：用 `canvas` 画 512×512 平铺图 + `toDataURL('image/png')` 下载，或至少导出 SVG `<pattern>`；删掉 `:206` 的 Canvas 大图说法。

### D-N193 历史/数据表恒空：ResText 读的是只有预览的 `#output`（中，确认缺陷）

- 问题：`__isometric_gridResText()` 读 `#output`，而 `#output` 内只有 `#preview` 背景 div（无文本），CSS 代码在 `#output` 之外的 `#cssOutput`；`res` 恒空 → extras 提前 return → 历史、数据表、趋势图、CSV 全无数据。
- 证据：`:172`（`<div id="output"><div id="preview"></div></div>`）、`:173`（`cssOutput` 在外部）、`:314-320`（ResText 读 `#output`，空则返回 ''）、`:395`（导出读 `#isometric_gridTable`）。
- 复现：生成 2 次切「历史/数据表」→ 空白；导出 CSV → 只有表头。期望记录尺寸/线宽/主色/底色。
- 影响：四个数据页签全部失效，CSV 导出无内容。
- 方案：ResText 改读 `cssOutput.value`（或返回 `size|lw|line|bg`）；表头改为「尺寸/线宽/主色/底色」。

### D-N194 四层渐变实为 3 方向（30° 重复）+ 公式与规格不符（低，确认缺陷）

- 问题：`background-image` 写了 4 层，第 1、4 层都是 `linear-gradient(30deg …)`，完全重复，实际只有 30°/150°/270° 三个方向；公式却把「四层 30°、150°、270°、30°」当特性，`background-size = 边长 × (边长 × 0.5774)` 写成面积式（实际是 `s` 宽 × `0.5774s` 高）；引据表又推荐 2:1 菱形（0.5），与实现的 0.5774 不一致。
- 证据：`:259`（第 1/4 层相同）、`:156`（公式写法）、`:231`（2:1 菱形）、`:257-258`（只夹下限）。
- 复现：线宽设 5 → 一组斜线因重复层明显更粗；输入 size=999 → JS 接受 999（`max` 未在 JS 夹取）。期望 4 层各不相同或明确只画 3 层。
- 影响：网格疏密不均，公式/参数说明误导；上限失控会生成超大 tile。
- 方案：删重复第 4 层（或补第 4 方向）；公式改「宽 = s，高 = s·tan30° ≈ 0.5774s」；JS 用 `Math.min(200, Math.max(10, …))`。

### D-N195 动画生成器无参数控件、无预览，只有代码文本（高，确认缺陷）

- 问题：meta/简介承诺「以可视化方式编排关键帧，调整时长、缓动与属性并实时预览」，实际只有 `#cnt` 一个输入；时长/缓动/延迟/方向全部随机，页面没有任何预览元素或动画实例，`#res` 只输出 `<pre>` 代码。
- 证据：`tools/design/generator-10.html:10`、`:116`、`:119`、`:123`（唯一输入）、`:125`（结果容器，无预览）、`:234-243`（随机参数与 `animation` 简写）。
- 复现：打开页面 → 看不到任何会动的元素；改「生成数量」只增减代码条目。期望有预览方块循环播放并可用滑杆调 duration/easing。
- 影响：「可视化」「实时预览」两个主卖点均未实现，用户只能盲拷代码、无法判断动效观感。
- 方案：加预览 box，把选中条 `animation` 应用到它；补 duration/easing/iteration/direction 控件；`cnt` 保留为「生成候选条数」。

### D-N196 预设「N 个关键帧」实为 N 段独立动画（中，确认缺陷）

- 问题：「3 个关键帧（简化演示）」「8 个关键帧（常规动效）」只设 `cnt`，而 `cnt` 是循环生成 N 个**完整动画**（每个仅 2–3 个百分比停点），不是一条动画里的 N 个关键帧。
- 证据：`tools/design/generator-10.html:428-430`（预设仅 `cnt`）、`:231`（`for i < cnt` 生成 N 个动画）、`:232`（类型按 `i % …` 轮换）。
- 复现：点「15 个关键帧（复杂序列）」→ 得到 15 个独立 `@keyframes` + 15 条 `animation`，每个仅 2–3 帧。期望一条动画 15 个关键帧。
- 影响：按「关键帧数量」预期会拿到 15 段互不相关的动画，无法用于同一条动效。
- 方案：预设改名「3/8/15 段动画」；若要真关键帧数，在单条 `@keyframes` 内生成 N 个百分比停点。

### D-N197 趋势图恒空 + `randColor` 死代码（低，确认缺陷）

- 问题：结果文本以「生成结果：」开头，`parseFloat` 得 NaN，图表永不渲染；`randColor()` 定义后从未调用，属死代码。
- 证据：`:230`（前缀）、`:384`（parseFloat）、`:212-215`（`randColor`）、`:235`/`:241`（实际取色方式）。
- 复现：生成 3 次 →「图表」空白；`parseFloat('生成结果： 1. fadeIn-…')` = NaN。
- 影响：图表页签无效；死代码增加维护噪音（非功能缺陷）。
- 方案：历史存 `duration` 数值列供图表；删除 `randColor` 或改用它生成颜色。

### D-N198 只用升号拼写，6/12 个根音音阶错误（高，确认缺陷）

- 问题：`notes` 数组只有升号（C…A#），`scaleNotes` 直接 `notes[(rootIdx+i)%12]`，凡需降号或重升/重降的调都会拼错。F 大调同屏出现「1个降号（Bb）」与「F - G - A - A# - C - D - E」；D 小调也把 B♭ 写成 A#。
- 证据：`tools/design/music-scale-reference.html:248`（升号音名表）、`:249`（音阶结构）、`:265`（映射）、`:278`（输出）；调号文案 `:282-283`。
- 复现：node 按同逻辑复算 12 个根音大调：C/D/E/G/A/B 正确；F→`F G A A# C D E`（应 B♭）、C#→`C# D# F F# G# A# C`（应 E♯/B♯）、F#→`F# G# A# B C# D# F`（应 E♯），G#/A#/D# 同错，共 6/12 根音错误；小调同理（D 小调 → `D E F G A A# C`）。
- 影响：这是「音阶调号参考」的唯一核心输出；F 大调这种最常用调直接给出错误音名，乐理教学场景不可用。
- 方案：按调查表「音级→音名（含升降）」（大调/小调各 15 调一张 7 音表），至少先把 F/F#/C#/D#/G#/A# 与 D/G/C/F 小调补成正确拼写。

### D-N199 G#/A#/D# 大调显示「无升降号（C大调/A小调）」（中，确认缺陷）

- 问题：`keySig` 只覆盖 7 个自然音 + F#/C#，选 G#/A#/D# 时 `keySig[root]` 为 `undefined`，`||0` 后落入「0 个升降号」分支，直接显示「调号：无升降号（C大调/A小调）」，与音阶列表明显矛盾。
- 证据：`:250`（`keySig` 缺 G#/A#/D#，也缺全部降号调）、`:279`（`||0`）、`:281-284`（0 分支文案）。
- 复现：根音 G#、大调 → `sigInfo` 显示「无升降号（C大调/A小调）」，而音阶含 A#/C/D#/F/G。期望「6 个升号」或「非标准调，等音 A♭ 大调」。
- 影响：3/12 根音调号完全错误，且与同页音阶自相矛盾。
- 方案：补全 `keySig`（含 G#/A#/D# 与 Bb/Eb/Ab/Db/Gb）；缺失时不要 `||0`，显式提示「非标准调」；或下拉只保留 15 个标准调。

### D-N200 小调不显示调号；和声/旋律小调承诺落空；和弦构成仅静态示例（中，确认缺陷）

- 问题：`sigInfo` 只在 `type==='major'` 时拼调号，选自然小调/五声/布鲁斯只剩一句图例，作为「调号参考」页却查不到小调调号；deep-dive 宣称「可切换自然/和声小调」、FAQ 讲和声/旋律小调规则，但下拉只有「自然小调」；表格「和弦构成」是固定示例文案，未按当前调计算。
- 证据：`:153`（仅 5 个类型）、`:281-287`（仅 major 分支）、`:196`（宣称可切和声小调）、`:200`（旋律小调规则）、`:229-230`（和弦构成静态示例）；meta `:10`「快速对照调号与和弦构成」。
- 复现：选 A 自然小调 → 无任何「调号」文字；想查 A 和声小调 → 下拉中没有。期望显示「A 小调：0 个升降号」并可选和声/旋律。
- 影响：小调是工具一半使用场景，调号缺失 + 类型缺失使「调号参考」不完整；「和弦构成」承诺无对应计算。
- 方案：补 minor/harmonicMinor/melodicMinor 结构与调号表；`sigInfo` 对小调输出「X 小调：n 个升/降号」；和弦行按当前调算 I 级三和弦（1/3/5 级音）。

### D-N201 边框生成器宣称「可视化设置 + 单边独立」，实际只有数量输入（高，确认缺陷）

- 问题：meta 写「可视化设置边框宽度、样式、圆角与配色并生成 CSS，支持单边独立设置」，简介块也写「支持单边独立设置」；实际只有 `#cnt` 一个输入，宽度 `randInt(1,8)`、圆角 `randInt(0,32)`、颜色随机、样式 8 种轮换，无任何单边（`border-top` 等）输出。
- 证据：`tools/design/generator-7.html:10`、`:113`（per-side control）、`:116`（单边独立设置）、`:120`（唯一输入）、`:215`（8 样式轮换）、`:219-222`（随机宽度/圆角/颜色，只输出 `border` 与 `border-radius`）。
- 复现：打开页面 → 无宽度/圆角/颜色/单边控件；连点生成 → 参数全变。期望可设 `border-top-width` 等，meta 的「per-side control」同样未实现。
- 影响：主关键词「单边设置」无法兑现，按描述进来的用户找不到功能，属结论级不符。
- 方案：补 width/style/radius/color 控件 +「四边联动/单边」切换，单边模式输出 `border-top` 等；最低成本是删掉「可视化设置」「单边独立设置」并改名「随机边框样式生成器」。

### D-N202 `double` 在 1–2px 宽时退化为实线（低，确认缺陷）

- 问题：宽度随机 1–8px，样式含 `double`；CSS 规定 `double` 在 1–2px 时按 `solid` 渲染，所以该条目在 1/2px 时预览与 solid 无法区分，代码却仍写 `double`。
- 证据：`:215`（含 double）、`:219`（width 1–8）、`:222-223`（原样写入 `border:${width}px double`）。
- 复现：连点生成直到出现 width=1 的 `double` 卡片 → 预览为实线；同一行 CSS 在浏览器也是实线。期望 double 最小 3px。
- 影响：8 种样式里有一种在约 1/4 概率下名不符实，用户以为样式没生效。
- 方案：`style==='double' && width<3` 时把 width 提升到 3，或从样式池排除 double。

### D-N203 预设只改数量 + 预览写死白底 + 趋势图恒空（低，确认缺陷）

- 问题：三个预设（「3 组边框（基础样式）」等）values 只有 `cnt`，「基础样式/组件库/设计规范」实际是同一随机池；预览块 `background:#fff` 写死，深色主题出现刺眼白块；趋势图用 `parseFloat` 解析「生成结果：…」恒 NaN，永不渲染。
- 证据：`:408-411`（预设仅 cnt）、`:229`（`background:#fff`）、`:383`（rk='结果'）、`:365`（parseFloat）。
- 复现：切深色主题 → 每个预览都是白块；生成 2 次切「图表」→ 空白；`parseFloat('生成结果： 1. …')` = NaN。
- 影响：预设与图表两个页签基本无信息量，深色模式预览观感突兀。
- 方案：预设补 `style/width/radius` 组合；预览底色改用 `var(--card-bg)`（边框对比用内层小色块）；历史加 `width/radius` 数值列供图表。

### 承诺 vs 实际（S 批专项）

| 页面 | 宣称（行号） | 实际 |
|---|---|---|
| checker-5 | 内置平声 198 字 / 仄声 2086 字（`:130`、`:308`） | Set 去重后实为 172 / 2043；示例《静夜思》误标 8 次（`:197-201`、`:218-219`） |
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

### D-N204 Material 主色明度图表取 400 阶，却标为 500 阶（高，确认源码缺陷）

- 问题：`mc_groups()` 用 `MATERIAL_COLORS[k][4]`（索引 4 = 400 阶）取色，但图表标题、表头和「主色(500)」列都按 500 阶展示；色块区主色用的是 `shades[5]`（500 阶）。同一「主色」在两处给出不同色值与明度。
- 证据：`tools/design/material-color.html:540`、`:356`、`:549`、`:552-553`
- 复现：打开「图表/明细表」→ Gray 实际显示 #BDBDBD、明度 51（400 阶）；期望 #9E9E9E、明度 34（500 阶，node 复算 L=0.342）。Red 实际 #EF5350(25)，期望 #F44336(24)。
- 影响：整张「500 主色明度」表与图表系统性浅一档，按表选主色会偏离规范值；`json`/CSV 派生数据同样错。
- 方案：`MATERIAL_COLORS[k][4]` 改为 `[5]`（或把列名/标题改成 400）；`:176` 承诺「A100–A700」但页面未收录，二者一并收敛。

### D-N205 推荐文字色按亮度 0.5 阈值判定，多数主色白字对比度不足 4.5:1（高，确认源码缺陷）

- 问题：`textColor = lum > 0.5 ? '#000' : '#fff'` 用亮度阈值选字色，而不是比较黑/白两方案的实际对比度；明细表 `:551` 又把 `lum>0.5` 写成「白字」，与色块预览正好相反。
- 证据：`tools/design/material-color.html:367`、`:393`、`:551`、`:235`、`:265`
- 复现：Orange 500 #FF9800（L=0.437）→ 实际白字 2.16:1，期望黑字 9.74:1；Blue 500 #2196F3 → 白字 3.12:1 vs 黑字 6.72:1；Green 500 #4CAF50 → 2.78:1 vs 7.56:1（node WCAG 复算）。全部低于页面 `:265` 自引的 4.5:1。FAQ `:235` 声称「会按 WCAG 算出对比度并标红」在源码中不存在。
- 影响：色块上的 HEX 文字低对比度难读；「建议文字色」列与预览自相矛盾，等于给错建议。
- 方案：逐色算 `contrast(black,bg)` 与 `contrast(white,bg)` 取高者；明细表复用同一结果；实现 `:235` 的对比度检测/标红或删除该承诺。

### D-N206 ISO 噪点分级用等效 ISO 判阈，但纯净/可用上限按原始 ISO 展示（高，确认源码缺陷）

- 问题：`effectiveISO = iso / s.mult` 后才与 `s.cleanMax` / `s.usableMax` 比较；而统计卡把 `cleanMax/usableMax` 直接当作「ISO 纯净上限 / 可用上限」展示，两套口径相差 `1/mult` 倍。
- 证据：`tools/design/iso-noise-reference.html:501-505`、`:530-531`、`:549`
- 复现：APS-C（mult=0.7）ISO 5000 → 实际判「较重」，页面却标可用上限 6400；期望「可用」（真实可用截止 = 6400×0.7 = 4480，若以上限为准则应判可用）。APS-C ISO 1600（页面标「纯净上限」）→ 实际「良好」，期望「优秀」（真实优秀截止 1120）。
- 影响：用户照页面标称的上限选 ISO（APS-C 5000/6400）会拿到更低一档的评级，噪点预期偏乐观；进度条 `:549` 按 6400 满格，与「较重」判定矛盾。
- 方案：统一口径——要么用原始 ISO 与 cleanMax/usableMax 比较，要么把上限展示为 `cleanMax*mult` / `usableMax*mult`（APS-C 1120 / 4480），进度条阈值同步。

### D-N207 目标章数小于幕数时逐幕章数出现 0 或负数（高，确认源码缺陷）

- 问题：章数分配先 `Math.round` 再 `if(c<1)c=1`，最后只做总和尾差修正，未处理「钳 1 后已超额」的情况，末幕被减成负数。
- 证据：`tools/design/generator-33.html:242-246`（输入下限见 `:128`）
- 复现：章数=1、三幕 → 实际 [1,1,-1]，表格显示「-1 章」，逐章配额只有 2 行（应为 1 行）；章数=2、四段 → [1,1,1,-1]；章数=3、三幕 → [1,2,0]（node 复算）。
- 影响：合法的 `min=1` 输入直接产出负章数，幕章数与目标章数、配额条数自相矛盾，复制/CSV 结果不可用。
- 方案：分配前校验 `ch >= 幕数`，不足时提示「章数少于幕数」或改按每幕 1 章；尾差只允许从最大幕扣除，扣除后若 <1 则回退到「无法分配」。

### D-N208 二维码生成器不生成任何二维码，只输出随机配置文本（高，确认源码缺陷）

- 假工具候选：是（类型 A+C：唯一输入是数量，输出与内容无关的随机参数；宣称的 qrcode.js 生成与图片导出均无实现）
- 问题：`gen()` 只拼接 `<pre>` 文本（渲染模式/画布尺寸/边距/纠错级/前景色/示例 URL + 一段 `.qr-N` 容器 CSS），全页没有 `canvas`、二维码矩阵或图片下载；也没有「输入网址或文本」的输入控件。
- 证据：`tools/design/generator-8.html:123`、`:219-255`、`:119`、`:10`、`:158-159`
- 复现：数量填 5 → 实际得到 5 段随机配置文本，复制后无法扫码；期望生成 5 个可扫二维码并提供 PNG/SVG 下载。
- 影响：`<title>`、meta、formula-desc 均写「输入网址或文本…生成二维码…支持导出」，搜索意图与页面能力完全不符。
- 方案：本地实现 QR 编码（矩阵→canvas/SVG），补文本输入与尺寸/纠错/颜色控件、PNG/SVG 导出；若不做则删除「生成/导出」表述并下架该页。

### D-N209 蓝图网格宣称「导出图片」，实际只有 CSS 文本与明细 CSV（高，确认源码缺陷）

- 假工具候选：是（类型 C：网格本身可生成，但 meta 主卖点「导出图片」完全未实现）
- 问题：页面只有「复制 CSS」与「导出明细 CSV」；源码无 `canvas`、无 `toDataURL/toBlob/download`，`generate()` 仅把 CSS 写进 `<textarea>`。
- 证据：`tools/design/blueprint-grid.html:154`、`:156`、`:203`、`:166-167`、`:258-260`
- 复现：点击任何按钮 → 只得到 `background-image` CSS 或 CSV，得不到 PNG；期望按当前尺寸导出可平铺 PNG（或至少 SVG）。
- 影响：meta description/og/twitter 三处都主推「纯前端导出图片」，实际无法导出，属名不副实。
- 方案：加离屏 canvas 按主/次间距绘制并 `toBlob` 下载 PNG；或删掉全部「导出图片」表述，改为「复制 CSS」。

### D-N210 粒子特效生成的 CSS 无元素与动画绑定，多数参数不生效（高，确认源码缺陷）

- 假工具候选：是（类型 A+C：仅数量输入，输出随机参数且不可运行）
- 问题：输出只声明 `--count/--color/--size/--shape/--speed/--spread/--opacity` 与 `@keyframes float-N`，既没有粒子 DOM/伪元素，也没有任何选择器写 `animation`；`--count`、`--shape`、`--speed` 全文未被引用。
- 证据：`tools/design/generator-12.html:231-248`
- 复现：复制任一方案 CSS 到空白页 → 无粒子、无动画；期望出现 count 个粒子并按 speed/shape 运动。
- 影响：所有「粒子方案」均为不可运行代码，参数只影响注释里的文本。
- 方案：输出可直接运行的 HTML+多粒子节点（或 box-shadow 方案）并绑定 `animation: float-N var(--speed) linear infinite`；否则降级为「随机参数清单」并改名。

### D-N211 条形码生成器只输出 13 位数字，没有条空图形或下载（高，确认源码缺陷）

- 假工具候选：是（类型 A+C：仅数量输入，输出随机数字；宣称生成/下载条形码图片未实现）
- 问题：`gen()` 只用 `genEAN13()` 生成随机 12 位 + 校验位，拼成一行等宽数字文本；没有 EAN-13 的 95 位条空编码、没有 canvas/SVG 绘制、没有图片下载，也没有数字输入框。
- 证据：`tools/design/generator-9.html:219-231`、`:207-218`、`:117`、`:10`、`:121`
- 复现：数量 5 → 实际 5 行「7 642153 842607」文本；期望 5 个可扫描的 EAN-13 条码图形 + PNG/SVG 下载。
- 影响：校验位算法本身正确，但输出物不是条形码，用户无法用于商品标签；meta「可下载条码」落空。
- 方案：补 EAN-13 左侧 A/B 编码与右侧 C 编码的条空表 → canvas/SVG，并加数字输入（校验位自动算）与导出。

### D-N212 幻灯片比例下拉是死输入，切换不改变任何输出（高，确认源码缺陷）

- 问题：`ratio` 被解析成 `W/H` 后全文再未引用；「比例像素对照」表把 16:9/16:10/4:3/A4 四行硬编码全部列出，px 列四行都是同一个 `fs*96/72`，与所选比例无关。
- 证据：`tools/design/generator-34.html:232-233`、`:257-260`、`:135-140`
- 复现：16:9 切到 4:3 → 输出逐字不变；期望画布尺寸/安全区与实际 px 换算随比例变化（如 1920 宽下 24pt ≈ 48px，1024 宽下 ≈ 25.6px）。
- 影响：主参数之一完全无效，用户误以为已按 4:3 或 A4 规划字号/像素。
- 方案：在标题或新增一行输出 `W×H`；px 按 `fs/72 * W/13.333` 计算并只显示当前比例（或高亮当前行）。

### D-N213 完整度评分实际下限 60，与文档「全空 20 分」不符（中，确认源码缺陷）

- 问题：任务与输出格式都是 `<select>`，永远有值且 `ok:true`，因此最低分为 3/5=60；目标对象与约束同时清空也只到 60，文档却写「全空 20 分」「目标对象留空降为 60」。
- 证据：`tools/design/generator-38.html:123-139`、`:241`、`:172`、`:176`
- 复现：清空目标对象与约束 → 实际 60 分（文档期望 20）；仅清空目标对象、保留默认约束 → 实际 80 分，文档写 60 且缺失项只列「上下文」。
- 影响：分数虚高，用户会误判提示词要素已基本齐备；文档算例与实际输出对不上。
- 方案：任务/格式改为可空或默认项不计入已填；统一评分口径并同步 FAQ/算例中的 20/60/80 数值与缺失项列表。

### D-N214 主显示 BPM 未按声明的「5 拍取整」，与历史记录值不一致（中，确认源码缺陷）

- 问题：`bpm=Math.round(60000/avg)` 直接取整；公式框 `:144` 声明 `round(实测BPM/5)*5`；扩展历史 `:272` 又按 5 取整，同一次测量出现两个值。
- 证据：`tools/design/bpm-tapper.html:144`、`:247`、`:259`、`:272`
- 复现：以 487ms 间隔点 3 次 → 实测 123.2，主显示 123、历史 125；期望两处均为 125（或删除取整声明）。
- 影响：主结果与自身说明矛盾，练习历史曲线和屏幕数值对不上。
- 方案：主显示/历史/导出共用一个 `round(raw/5)*5` 函数，或保留原始值并删去「5 拍取整」文案。

### D-N215 节拍器用 setTimeout 链式重排，未用音频时钟预排，节拍持续漂移（高，确认源码缺陷）

- 问题：`scheduler()` 每次 `setTimeout(scheduler, 60000/bpm)` 重新计时，下一拍基准是上一次回调的实际执行时刻，延迟逐拍累加；`playClick()` 也在 `currentTime` 即时发声，没有任何 lookahead，与页面 `:143`/`:235` 的「预排音频事件、避免定时器漂移」相反。
- 证据：`tools/design/web-audio-metronome.html:272-277`、`:267-270`、`:143`、`:235`
- 复现：120 BPM 连播 10 分钟（600 拍），每拍回调平均晚 1ms → 累计慢约 0.6s（node 复算 600×0.001）；期望 600 拍累计误差在数毫秒内。
- 影响：长时间练习/录音时节拍逐渐落后，切后台被节流后误差成倍放大。
- 方案：维护 `nextTime`，每拍 `nextTime += 60/bpm`，用 25ms lookahead 把 `osc.start(nextTime)` 排进音频时钟；UI 更新与调度解耦。

### D-N216 粒子运动按「每帧」积分，速度与寿命随刷新率变化（高，确认源码缺陷）

- 问题：`p.vy += gravity*0.1`、`p.x += p.vx`、`p.life--` 均无 dt；`opts.lifetime = Math.round(lifeVal*60)` 又把「秒」硬换算成 60fps 帧数，动画循环也未做时间归一。
- 证据：`tools/design/particle-effect-generator.html:636-638`、`:712`、`:737-743`、`:617`、`:546`
- 复现：同一「速度 2、寿命 1.5s」在 120Hz 屏幕上位移速度约为 60Hz 的 2 倍、寿命约 0.75s；期望两种刷新率下速度（px/s）与寿命（真实秒）一致。
- 影响：高刷设备动效明显偏快/短命，与 constRefBox「按真实时间差 dt 归一」及 UI 的「1.5s」不符。
- 方案：用 `dt=(ts-last)/1000` 归一（`v += g*dt*6`、`x += vx*dt*60`），寿命改用毫秒时间戳；或按实测 fps 动态换算帧数。

### D-N217 「星空/星云」预设的连线距离因粒子数 ≥300 被静默禁用（中，确认源码缺陷）

- 问题：绘制连线前有 `particles.length < 300` 硬门槛，而预设明确给出 300/400 粒子 + 60/100 的连线距离，参数被静默丢弃。
- 证据：`tools/design/particle-effect-generator.html:775`、`:1039`、`:931`
- 复现：点「星空」预设（count=300、linkDist=60）→ 实际一条连线都没有；「星云」（400/100）同样恒无连线。期望按 60/100px 连线（或提示已自动降低粒子数）。
- 影响：预设的核心视觉效果缺失，用户调 linkDist 也看不到任何变化。
- 方案：门槛改为 `<=300`；超限预设自动降到 299 并在 UI 提示「连线仅 ≤300 粒子生效」，不要静默忽略参数。

### D-N218 色帽文字色阈值 0.32 高于黑白对比交叉点 0.179，15 个色帽全部白字仅 4.23:1（高，确认源码缺陷）

- 问题：15 个色帽等亮度 `CAP_Y=0.198`，`textOn` 用 `L>0.32` 判黑字，导致全部返回 `#FFFFFF`；按 WCAG 黑白交叉点在 L≈0.179（node 复算 `√0.0525−0.05=0.1791`），0.198 下白字 4.23:1、纯黑 4.96:1。
- 证据：`tools/design/farnsworth-d15-test.html:318`、`:356-359`、`:621`、`:893`
- 复现：任一色帽（灰度预览 #7B7B7B 亦然）→ 实际白字 4.23:1，期望黑字 #000 4.96:1 达 AA；若仍用 `#111827` 则只有 4.19:1，不能作为深色文字。
- 影响：色帽编号（canvas 11px 粗体、色块内序号）对比度不达 AA，低视力用户难以辨认。
- 方案：改为比较黑白两方案的实际对比度取高者，深色用 `#000`；或把编号字号/字重提升到「大文本」3:1 口径并在页面注明。

## T 批 design 覆盖（2026-11-04）

- 本轮审计 13 页：`material-color`、`iso-noise-reference`、`generator-33`、`generator-8`、`blueprint-grid`、`generator-12`、`generator-9`、`generator-34`、`particle-effect-generator`、`farnsworth-d15-test`、`generator-38`、`bpm-tapper`、`web-audio-metronome`
- 新增 15 条（高 12 / 中 3），编号 D-N204–D-N218；假工具候选 4 页（generator-8、generator-9、generator-12、blueprint-grid）
- 未做浏览器/门禁/线上验证

## AB 批 · 设计族矩阵：图像/格式转换（2026-11-04）

本轮复用 T 批末尾编号，新增 D-N219 起。6 页均实读整份 HTML，并按「输出物能否被标准工具还原」取向核查：像素尺寸用页面算式复算，blob/下载路径逐行核对，换算类用 `node -e` 内存复算（未落地脚本）。无浏览器实测，故 MIME 结论以「代码实际取哪个字段」为准。

| 页面 | 实现方式 | 可验证性 | 结论 |
|---|---|---|---|
| `tools/design/svg-to-png.html` | Canvas（Blob→Image→drawImage→`toDataURL`） | 中：PNG 可解码，像素=宽×倍率；但无尺寸/面积上限，超大画布 `toDataURL` 返回 `data:,` → 0 字节 | 真实现，需补上限 |
| `tools/design/px-to-rem.html` | 自写算术（`px/root`） | 高：算术可复算；默认 16/16=1rem，站点 CSS 未改写根字号，与浏览器 16px 一致 | 真实现；62.5% 说明写反 |
| `tools/image/image-compress.html` | Canvas + `toBlob` + 对比滑块 | 中：blob 可下载、长边限制正确；MIME 与极端比例不可靠 | 真实现 |
| `tools/image/image-resize.html` | Canvas + `toBlob` + token 防竞态 | 高：尺寸/比例/质量可复算，blob 真下载；大画布内存与 MIME 有缺口 | 本批最完备 |
| `tools/image/image-converter.html` | Canvas 三格式批量 `toBlob` | 中：三份 blob 均可下载；换图竞态会把旧图卡片追加到新网格 | 真实现 |
| `tools/design/photo-print-size.html` | 自写算术 + 相纸规格表 | 高：`cm = px/DPI×2.54` 与相纸需求像素均可复算 | 真实现；预设与表差 1px |

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

