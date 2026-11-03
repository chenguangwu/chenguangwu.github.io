# 图片处理 · tools/image（~20 页）

## 已知问题
- image-converter/nine-grid-cutter 等已在图表池甄别（天然不需要/已注入）。

## 功能缺陷
- image-resize 缺「常用平台尺寸预设」（小红书 3:4、公众号封面 2.35:1 等）——高频刚需。
- 无「批量」（多文件本地处理）版本。

## 优化点
- S2 平台尺寸预设矩阵（社交/电商/证件照全表）。
- 隐私声明前置：所有处理本地完成的徽标（信任感）。

## 受影响范围
- tools/image/（~20 页）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 马赛克预览与导出不一致（高，确认源码缺陷）
- 问题与证据：`tools/image/image-mosaic.html:373-386,460-478,634-651` 全图模式预览将 region 置空而画原图，导出却对全图打码；区域模式预览使用缩小后画布的块大小，导出在原图使用相同数值，因而缩图时预览可能高估打码强度。实际浏览器像素尚未核验。
- 影响：`tools/image/image-mosaic.html`，隐私打码判断可能失真。
- 方案：全图预览实际打码，统一块大小的原图坐标语义并按缩放换算；加入大图与区域预览/导出像素对照，确保敏感信息不可辨识。

### 拼图裁切越界与加载乱序（中，确认源码缺陷，两个问题）
- 问题与证据：`tools/image/image-collage.html:507-520,610-617` cover 分支绘制超出单格而无裁剪；原函数内存执行将 200×100 图填入 100×100 格时绘制范围为 −50 至 150，可能覆盖其他格和间距。`:409-428` 多文件在各自 onload 时 push，解码较快的图先进入列表，不保证 FileList 顺序。
- 影响：`tools/image/image-collage.html`，拼图边界或截图次序可能错误；尚未实测浏览器画布。
- 方案：每格绘制时按格子裁剪并恢复上下文；按选择次序存储并统一处理加载失败。可进一步提供文件名排序、反转和撤销，方便长截图拼接。

### 边缘裁剪框尺寸与导出不一致（中，确认函数缺陷）
- 问题与证据：`tools/image/image-crop.html:681-697,793-804,839-844` 先限制边界再强制最小尺寸；100×100 图右下角以 (98,98) 建立 1:1 裁剪框时，内存执行得到 12×12，而导出再次裁边最多 2×2，信息显示与实际不同。真实指针交互尚未复测。
- 影响：`tools/image/image-crop.html`。
- 方案：最小尺寸服从边界，空间不足时移动起点或提示，显示与导出统一。

### 水印 WebP 导出丢失透明背景（中，确认源码缺陷）
- 问题与证据：`tools/image/image-watermark.html:948-964` 非 PNG 都先铺白底，包含支持透明的 WebP；透明 PNG 加水印后导出 WebP 会丢失透明区域。浏览器实际下载像素未测。
- 影响：`tools/image/image-watermark.html`。
- 方案：仅 JPEG 默认铺底，WebP 保留透明；补透明像素导出回归。

### 留存建议（低，建议）
- `tools/image/image-mosaic.html:616-654`：当前单选区导出流程可增加多个独立选区和导出前检查，方便一次遮挡姓名、电话和地址；先修复预览一致性。
- `tools/image/image-collage.html:431-477`：在现有上下移动基础上提供按名称排序、反转及撤销，降低长图重排成本。

### 覆盖
- 本次只读核查 4 页：`tools/image/image-mosaic.html`、`tools/image/image-collage.html`、`tools/image/image-crop.html`、`tools/image/image-watermark.html`；合计 5 个缺陷，2 条建议。未做真实浏览器、移动端、线上或其他图片页逐页验证。

## 2026-11-03 续查：缩放与批量压缩

### IM-N1 目标宽高为空或 0 时静默输出 1 像素图（中，确认源码缺陷）
- 证据：`tools/image/image-resize.html:629-630` 用 `parseInt(value,10)||1` 与 `Math.max(1, …)`，清空或输入 0 后直接按 1 像素渲染；HTML 仅写 `min=1 max=10000`（`:300,305`），JS 不校验上限，手输 20000 会创建超大画布，`toBlob` 失败时 `resultBlob` 为空，下载却提示「请上传图片」（`:700-703`），与真实失败原因不符。
- 影响：`tools/image/image-resize.html`；用户误得 1×1 图或无法判断为何下载失败。
- 方案：宽高原因为空/0/超上限时给出字段级错误并停止渲染；`toBlob` 为空时提示「尺寸过大或浏览器不支持该格式」，保留上次成功结果并标注参数。

### IM-N2 GIF/SVG 被当位图静默输出静态帧（中，确认源码缺陷）
- 证据：`tools/image/image-resize.html:262` 接受 `image/*`，`:646-660` 直接 `drawImage` 到 canvas，导出仅 PNG/JPEG/WebP；GIF 动图只保留首帧，SVG 被栅格化，页面无任何提示。
- 影响：`tools/image/image-resize.html`；用户上传动图后以为得到动图。
- 方案：检测 `image/gif` 与 `image/svg+xml` 并明确提示「将输出静态首帧/栅格图」，或对 GIF 提供逐帧处理；下载文件名与结果区标注实际输出格式。

### IM-N3 压缩页英文态提示与复制文本仍是中文（中，确认源码缺陷；运行态待探针）
- 证据：`tools/image/image-compress.html:531,776,781,791-795` 添加成功、下载、批量下载及复制结果文本全为硬编码中文，而同页其它 toast 用 `i18nText`（如 `:530`）；`tools/image/image-resize.html:719` 下载 toast 同样硬编码。运行时词典按 `textContent` 替换，不会改写 JS 动态 toast。
- 影响：`tools/image/image-compress.html`、`tools/image/image-resize.html`；英文态操作反馈与复制结果夹中文（G05 同类，页面级）。
- 方案：所有动态文案走 `i18nText`/`__T`，第三层词典补齐；改后重跑 `_build.py` 并用 EN 探针复验下载与复制路径。

### 留存优化（按页落点，非确认缺陷）
- `tools/image/image-resize.html`：无平台尺寸预设，用户改小红书 1242×1660、公众号封面 900×383 只能手算。建议内置常用平台预设与「按长边等比」模式，并在结果区给出文件体积与格式建议。
- `tools/image/image-compress.html`：只有「质量 + 最大边」单向调节，缺「目标体积（如 ≤200KB）」反推质量。建议加目标体积模式（二分搜索质量并在结果标注实际体积），批量列表展示压缩前后总计，这是该类工具最主要的复用点。
- `tools/image/image-compress.html`：批量下载按 500ms 逐个触发，浏览器易拦截多文件下载；建议打包 ZIP 或明确提示允许自动下载。

### IM-N4 格式转换一律先铺白底，透明 PNG 被压成白底（高，确认源码缺陷）
- 证据：`tools/image/image-converter.html:286-291` 在绘制前无条件 `fillStyle='#fff'` 并 `fillRect`，随后对 JPEG/PNG/WebP 三种输出共用同一张已铺白底的 canvas（`:293-316`）。上传透明背景 PNG 转 PNG，透明区变成白色。
- 影响：`tools/image/image-converter.html`；Logo、图标、贴纸类透明素材转换后失去透明度，且页面没有任何提示。
- 方案：按目标格式决定背景——PNG/WebP 保留透明、JPEG 才铺白（或提供「透明区填充色」选项）；结果卡标注「已保留透明/已铺白底」。

### IM-N5 九宫格「全部下载」并发触发被浏览器拦截（中，确认源码缺陷）
- 证据：`tools/image/nine-grid-cutter.html:368-380` 在 `Promise.all` 后同步循环对每个 blob 依次 `a.click()`，9 张同刻触发；Chrome/Safari 默认只允许首个下载，其余被静默拦截。页面无 ZIP 打包入口。
- 影响：`tools/image/nine-grid-cutter.html`；用户点「全部下载」实际只得到 1 张，误以为工具坏了。
- 方案：改为 ZIP 打包（复用 gif-split 的 JSZip 方案）或每张间隔并提示需允许「多个文件下载」；按钮文案与结果一致。

### IM-N6 GIF 拆帧 ZIP 依赖外部 CDN，打包提示为硬编码中文（中，确认源码缺陷；离线行为待验证）
- 证据：`tools/image/gif-split.html:28` 从 `cdn.jsdelivr.net` 加载 JSZip；`:950-960` 仅判断 `typeof JSZip==='undefined'` 后弹通用提示，`'正在打包...'` 直接硬编码中文；同页其它文案走 `i18nText`。
- 影响：`tools/image/gif-split.html`；弱网/离线时无法打包且提示不可操作；英文态打包状态栏残留中文（G05/G09 同类，按页记录）。
- 方案：JSZip 本地托管并锁版本，缺失时明确提示「可逐帧下载」；打包状态与错误文案走 `i18nText`，改后重跑 `_build.py`。

### IM-N7 九宫格行列数越界被静默截断（低，确认源码缺陷）
- 证据：`tools/image/nine-grid-cutter.html:250` `__ngcClamp` 用 `parseInt(v)||1` 后 `Math.min(6, …)`；输入 7 或 10 直接按 6 切割，页面不回显错误。
- 影响：`tools/image/nine-grid-cutter.html`；用户以为得到 7 列，实际 6 列。
- 方案：越界时提示并恢复上次合法值，输入框同步显示实际生效值。

### 留存优化（按页落点，非确认缺陷）
- `tools/image/image-converter.html`：输出质量固定 0.85、无尺寸限制，且不能只转单个格式。建议加质量滑杆、最长边限制、透明区填充选择，并支持「只转选中格式」。
- `tools/image/nine-grid-cutter.html`：直接按原图分辨率切，4000px 原图得到 1333px 切片，超出社交平台需要。建议加输出边长预设（1080/1440）与顺序说明（微信九宫格需按 1→9 发布）。
- `tools/image/gif-split.html`：只导出 PNG 帧，丢失每帧延迟/循环信息。建议在 ZIP 内附 `frames.json`（帧序号、延迟、尺寸）或导出 WebP 动图。

### 续查覆盖
- 新抽查 `tools/image/gif-split.html`、`tools/image/nine-grid-cutter.html`、`tools/image/image-converter.html` 共 3 页，新增 4 条（1 条高优）与 3 条留存建议；累计 image 小类抽查 5 页，其余 9 页仍未逐页覆盖；未做浏览器、EN 探针、移动端或门禁验证。

## 2026-11-03 续查（并行批）：上传/导出承诺核实（剩余 5 页）

### IM-N8 圆角图片页没有上传、圆角参数和下载，随机色块冒充（高，确认）
- 证据：`tools/image/generator-15.html:121-125,203-226` 无 `<input type="file">`、无圆角输入、无下载按钮；`gen()` 只按 `cnt` 画随机颜色 `120×120` 画布并 `roundRect(10,10,100,100,随机10–39px)`。而 description（`:10`）、FAQ 与深度解析（`:153-154,409`）承诺「上传图片、指定圆角、批量、导出 PNG 约 90KB」。`:398` 预设把 `cnt` 设为 2.5/7.5，`parseInt` 实取 2/7。
- 影响：`tools/image/generator-15.html`；文案与产物完全不符，用户拿不到可用的圆角图。
- 方案：落地真实上传+半径/比例+PNG 下载；否则改文案为「圆角色块样例」并移出图片分类；预设改整数。

### IM-N9 证件照下载先落一个 0 字节同名 PNG（高，确认）
- 证据：`tools/image/id-photo-crop.html:334-355` 在真实 PNG 前调用 `ToolBox.downloadText(name,'')`；`js/common.js:2004-2014` 该函数以 `text/plain` 空串建 Blob 且 `a.download=name`，默认文件名 `id-photo.png` 被触发两次（浏览器第二个改名为 `(1)`）；`:354` 的 `revokeObjectURL` 紧随 `click()`。
- 影响：`tools/image/id-photo-crop.html`；用户得到空文件+重名文件，易误判导出损坏。
- 方案：删除 `downloadText`，统一走 Blob 下载并 `setTimeout` 后再 revoke。

### IM-N10 证件照底色不生效、规格像素与标注不符（高，确认）
- 证据：`:292-294` 先 `fillRect(bg)` 再 `drawImage` 铺满整个输出，不透明照片把底色完全覆盖，与「背景色替换」（`:49,119,489`）不符。`:126-129` 规格与 `:491-496` 标注矛盾：25mm@300DPI=25÷25.4×300≈295px，页面用 258（实为≈22×28mm）；二寸 35×49mm 应为 413×579，页面 531（=35×45mm）；护照 33×48mm 应为 390×567，页面 354×472（恰为 30×40mm）。
- 影响：`tools/image/id-photo-crop.html`；标称「合规证件照」但尺寸与底色均存疑。
- 方案：先做背景分割，或文案改为「仅填充留白」；按 mm@DPI 重算四规格并写明实际毫米。

### IM-N11 封面只导出固定 900×383，无缩略图；英文态把中文烤进图（中，确认）
- 证据：`tools/image/wechat-cover-maker.html:141` 画布固定 900×383，`:286-297` 仅导出 `wechat-cover.png`；`:337-364` 的 WC_SIZES（次条 200×200、分享 1080×1080、缩略 360×200）只是表格，无选择器，与「尺寸模板…导出封面与缩略图」「图片排版」（`:43`）不符。`:116-118` 默认标题/副标题是中文 input value，`:283` 页脚硬编码 `ToolBox · 在线工具集`，`:235` 按字符断行会截断英文单词。
- 影响：`tools/image/wechat-cover-maker.html`；英文态导出图仍含中文。
- 方案：复用 WC_SIZES 做尺寸/缩略图切换，页脚走 i18n，英文按词断行并限行；`:295` 即时 revoke 改延迟（英文/Safari 实际影响疑似待验证）。

### IM-N12 滤镜预设与滑杆失同步，预览模糊与导出不一致（中，确认）
- 证据：`tools/image/image-filter.html:312-316` `applyPreset` 只改预览 CSS 与 `currentFilter`，不回写滑杆；`:318-338` 任一滑杆 `applyFilter` 用滑杆值重建 filter，预设立即丢失。预览 `img` 被 CSS 缩到 `max-height:400px`（`:32`），导出在 `naturalWidth` 原图执行 `ctx.filter blur(Npx)`（`:351-366`），同一 Npx 相对强度差数倍。`toBlob` 无 null 判断，`:360-362` 直接 `createObjectURL` 抛错且无提示。
- 影响：`tools/image/image-filter.html`；调参后效果回退、导出与所见不符。
- 方案：预设回写滑杆；模糊按缩放比换算；导出失败给字段级提示。

### IM-N13 旋转页按全分辨率建画布，无面积上限（中；iOS 失败疑似待验证）
- 证据：`tools/image/image-rotate.html:552-567` 以 `ceil(w·|cos|+h·|sin|)` 直接写入 canvas 背存，且预览与导出共用同一画布；4000×3000 转 45° 得 4949×4949≈24.5MP，超 iOS Safari 约 16.7MP 画布上限。
- 影响：`tools/image/image-rotate.html`；移动端大图可能整屏空白或下载失败。
- 方案：预览用缩略画布，导出前判面积并提示/降级，或分块渲染。

### IM-N14 换图失败仍可按新文件名下载旧图；英文信息区留中文（中，确认）
- 证据：`tools/image/id-photo-crop.html:257-270` 无 `img.onerror`，解码失败时 `srcImg` 仍是上一张且预览不刷新；`image-rotate.html:443-477` 先写 `fileName` 再解码，`onerror`（`:468`）不清空 `originalImg`，导出得到「新文件名+旧像素」。英文态 `updateInfo` 注入「原图尺寸/输出尺寸/旋转角度/水平翻转/是/否」（`image-rotate.html:588-596`）不在 `i18n/tools/en/image/image-rotate.json` 的 map 内；id-photo `alert('请先上传并生成。')`（`:336`）同样硬编码。
- 影响：`tools/image/id-photo-crop.html`、`tools/image/image-rotate.html`；错误换图无提示且旧结果可下载。
- 方案：失败时清空状态并显式报错；补齐词典或改 `data-i18n`，动态文案走 `i18nText`。

### 留存优化（按页落点）
- `tools/image/generator-15.html`：若做成真工具，落点「上传→半径/比例→批量 PNG/JPEG」，并记忆上次半径。
- `tools/image/id-photo-crop.html`：中心裁剪易切头，建议加可拖动/缩放的取景框、DPI 写入与多规格 ZIP 导出。
- `tools/image/image-rotate.html`：该页无 `localStorage` 持久化块，建议记忆角度/底色/格式并支持多图批量。
- `tools/image/wechat-cover-maker.html`：用 WC_SIZES 做尺寸切换（次条/分享/缩略），导出前提示安全区与标题溢出；`image-filter.html` 可做预设↔滑杆双向同步并沿用原文件名导出。

### 续查覆盖
- 实际剩余非 index 页仅 5 个（目录内无 heic/格式转换/svg 转 png/upscale 独立页）：`generator-15.html`、`id-photo-crop.html`、`image-filter.html`、`image-rotate.html`、`wechat-cover-maker.html`。新增 7 条（3 条高优）与 4 条留存建议；数值均为源码与算术推导，未做浏览器、EN 探针、移动端或门禁验证。
