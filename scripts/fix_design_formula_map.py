#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design 分类 formula-box 数据源（配合 scripts/fix_formula.py 使用）。

覆盖 89 处缺口：
  A) 无 formula-box 49 个     → 插入完整框
  B) 有框但无 formula-desc 24 → 补 desc（缺 eq 时一并补）
  C) formula-desc 为生成器套话 16 → 换真实原理说明

分类原则（§4.1.2「真实内容」，不编造公式）：
  - 计算 / 算法类（WCAG 对比度、色温、景深、曝光、DPI、单位换算、比例尺…）给真实公式 + 依据
  - 生成器 / 预览类（CSS 生成器、图案、二维码、头像、图像处理…）给核心原理与参数说明，不虚构公式
"""

MAP = {
    # ================= 计算 / 算法类（eq + desc）=================
    'analysis': {
        'eq': '按颜色量化统计频次：占比 = 该色像素数 / 总像素数，取占比最高的若干色为主色',
        'desc': '用 Canvas 读取图片像素并按颜色量化统计出现频次，取占比最高的若干色作为主色并生成完整调色板，同时给出各色占比，用于从参考图快速提取配色方案。',
    },
    'bpm-tapper': {
        'eq': 'BPM = 60 / 平均点击间隔(秒)',
        'desc': '按多次点击的时间间隔取平均求得每分钟拍数；点击次数越多结果越稳定，用于测量歌曲速度、辅助乐器与舞蹈练习。',
    },
    'checker': {
        'eq': 'CR = (L₁ + 0.05) / (L₂ + 0.05)，L = 0.2126R + 0.7152G + 0.0722B（sRGB 归一化并线性化后）',
        'desc': '依据 WCAG 2.1：先将 sRGB 各通道归一化并按 gamma 线性化，再加权求相对亮度 L，两色亮度各加 0.05 后取比值。CR ≥ 4.5 为 AA（正文）、≥ 7 为 AAA；大字号阈值分别为 3 与 4.5。',
    },
    'color-contrast-check': {
        'eq': 'CR = (L1 + 0.05) / (L2 + 0.05)，L 为 WCAG 相对亮度（按 sRGB gamma 校正）',
        'desc': '基于 WCAG 2.1 无障碍标准：对比度比值为两色相对亮度（含 0.05 常数项）之比，范围 1:1 至 21:1；据此判定文字是否达到 AA / AAA 可读性要求。',
    },
    'contrast-checker': {
        'eq': 'CR = (Llight + 0.05) / (Ldark + 0.05)，L = Σ(wᵢ·Cᵢ)，w = [0.2126, 0.7152, 0.0722]',
        'desc': '依据 WCAG 2.1 计算前景色与背景色的对比度比值：相对亮度按 sRGB gamma 校正后加权求得；用于保证正文、按钮与图标在网页上的可读性。',
    },
    'color-picker': {
        'eq': 'V = max(R,G,B)；S = (max−min)/max；H 由最大通道分段求得；CMYK = 1 − RGB/255（减色法近似）',
        'desc': '基于标准色彩空间转换：HEX 与 RGB 为 8 位三通道，HSL/HSV 将色相、饱和度、明度分离，CMYK 由 RGB 按减色法近似换算；用于跨格式取色与印刷输出参考。',
    },
    'color-shade-generator': {
        'eq': 'tint = C·(1−t) + 255·t；shade = C·(1−t) + 0·t（t 为混合比例，0 ≤ t ≤ 1）',
        'desc': '按线性混色：tint 是在基色上按比例混入白色得到更亮的色，shade 是混入黑色得到更暗的色；按固定步长生成整组明暗色卡，用于按钮、背景与边框的层次设计。',
    },
    'color-palette': {
        'eq': '互补 +180°；类似 ±30°；三角 +120° / +240°；分裂互补 +150° / +210°（HSV 色相环）',
        'desc': '基于 HSV 色相环的调和关系：在固定饱和度与明度下按色相角度偏移取色，得到互补、类似、三角等协调配色，实时预览并可导出色值，用于网页与品牌视觉的快速定调。',
    },
    'color-palette-generator': {
        'eq': '邻近色相 = H ± Δ（Δ 常取 15°/30°）；明度阶梯 = L ± k·ΔL；饱和度按规则微调',
        'desc': '按色彩调和规则在主色基础上做色相偏移与明度、饱和度阶梯，生成可复用的调色板，支持导出色值、渐变与 CSS 变量，用于为网站与海报建立统一色彩体系。',
    },
    'color-temperature-converter': {
        'eq': 'Tanner Helland 近似：按温度分段幂函数求 R/G/B，如 R = 329.7·(T/100 − 60)^(−0.1332)（T 为开尔文）',
        'desc': '基于黑体辐射的屏幕近似算法：把色温 K 映射为可显示的 RGB（非线性、仅近似，非精确光谱），反向亦可由 RGB 估计色温；用于摄影白平衡与灯光色彩参考。',
    },
    'depth-of-field-calculator': {
        'eq': '超焦距 H = f²/(N·c) + f；前景深 = s(H−f)/(H+s−2f)；后景深 = s(H−f)/(H−s)',
        'desc': '依据景深公式：f 为焦距、N 为光圈 F 值、c 为允许弥散圆直径（随画幅变化）、s 为对焦距离；光圈越小、焦距越短、对焦越远，景深越大，用于构图与虚化控制。',
    },
    'exposure-triangle-calculator': {
        'eq': 'EV = log₂(N² / t) − log₂(S / 100)（N 为光圈 F 值、t 为快门秒数、S 为 ISO）',
        'desc': '依据曝光三角：光圈、快门与 ISO 共同决定曝光量；保持 EV 不变即可等效互换（如开大一级光圈同时加快一级快门）。ISO 越高画面越亮但噪点越多，用于等效曝光组合换算。',
    },
    'focal-length-equivalent': {
        'eq': '等效焦距 f_eq = f × 裁切系数 k（全画幅 1.0、APS-C 1.5/1.6、M43 2.0）',
        'desc': '按画幅裁切系数换算：以 35mm 全画幅为基准，不同画幅因传感器尺寸不同产生视角差异；等效焦距 = 实际焦距 × 裁切系数，用于跨画幅对比视角与镜头选型。',
    },
    'image-dpi-converter': {
        'eq': '像素 = 英寸 × DPI；英寸 = 像素 / DPI（数字图像中 PPI 与 DPI 同义）',
        'desc': '基于分辨率定义：DPI/PPI 表示每英寸包含的像素数，像素尺寸与物理尺寸按 DPI 线性互换；用于印刷排版与屏幕输出的尺寸核对。',
    },
    'image-to-ascii': {
        'eq': '亮度 L = 0.299R + 0.587G + 0.114B；字符索引 i = round(L / 255 × (n − 1))',
        'desc': '基于 BT.601 亮度加权：把每个采样块的平均亮度映射到字符集（如 "@%#*+=-:. "）的对应档位；输出宽度、对比度、亮度与字符集均可调，用于生成字符画。',
    },
    'photo-aspect-ratio-calculator': {
        'eq': '比例 = W / H；已知一边求另一边：目标边 = 已知边 × (目标比例的另一边 / 已知边)',
        'desc': '按宽高比定义换算：输入像素或目标尺寸即可求出最简比例（如 16:9、4:3）与另一边的对应长度，用于裁剪与多平台发布尺寸统一。',
    },
    'photo-print-size': {
        'eq': '打印尺寸(英寸) = 像素 / DPI；再对照常见相纸规格（3R/4R/5R/A4 等）取最接近者',
        'desc': '基于打印分辨率：给定 DPI 时由像素尺寸求最佳打印物理尺寸并对照标准相纸规格；DPI 越高越精细但可印尺寸越小，用于避免冲印模糊或浪费相纸。',
    },
    'photo-storage-calculator': {
        'eq': '单张体积 ≈ 分辨率(MP) × 每像素字节数；总容量 = 单张体积 × 张数 × 冗余系数',
        'desc': '按相机分辨率、文件格式（JPEG/RAW）与拍摄张数估算存储需求：不同格式与压缩率对应不同每像素字节数，用于存储卡容量规划与备卡。',
    },
    'px-to-rem': {
        'eq': 'rem = px / root（root 为根元素 font-size，默认 16px）',
        'desc': 'rem 相对根元素字体大小：以根字号为基准换算，便于做响应式与可访问性友好的布局（用户调整根字号时整体等比缩放），用于设计稿落地。',
    },
    'rem-to-px': {
        'eq': 'px = rem × root（root 为当前根元素 font-size）',
        'desc': '把以 rem 为单位的标注或设计稿按当前根字号反算为像素，用于需要固定尺寸的场景或与设计师核对标注。',
    },
    'shutter-speed-calculator': {
        'eq': '安全快门 t ≤ 1 / (f × k)（k 为裁切系数；经验法则为焦距倒数）',
        'desc': '依据“安全快门 ≈ 焦距倒数”的经验法则：焦距越长越易手抖，需要更快快门；有防抖可放宽若干档，用于手持拍摄的曝光参数参考。',
    },
    'spacing-scale': {
        'eq': '间距 s(n) = base × rⁿ（等比）或 base × n（线性，如 4/8/12/16）',
        'desc': '基于模数化间距体系：以一个基数按固定比例或倍数派生整组间距，保证页面留白节奏一致；输出为 CSS 变量，用于设计规范与组件间距。',
    },
    'typography-scale': {
        'eq': '字号 size(n) = base × rⁿ（r 为模数比，如 1.25 为大三度、1.618 为黄金比）',
        'desc': '基于模数化排版比例：以基准字号按比例派生标题到正文的字号阶梯，输出字号表与 CSS，用于建立一致的排版层级。',
    },
    'music-scale-reference': {
        'eq': '十二平均律 f = f₀ × 2^(n/12)（n 为半音数）；大调音阶半音结构 2-2-1-2-2-2-1',
        'desc': '依据十二平均律与大调/小调音阶结构，列出各调式的音名与升降记号分布，可对照调号与和弦构成，用于乐理学习与音乐创作。',
    },
    'identicon-generator': {
        'eq': '哈希 = FNV-1a / MD5(输入串) → 取位生成左右对称网格与色相',
        'desc': '按哈希算法把任意字符串确定性映射为对称几何图案：同一输入始终得到同一头像，无需服务端存储；用于无头像用户的默认标识。',
    },
    'iso-noise-reference': {
        'eq': '（参考表）动态范围 ≈ 14 − log₂(ISO / 100) EV；ISO 每翻倍约损失 1 EV',
        'desc': '按不同相机在各 ISO 下的噪点与动态范围表现提供对照参考：ISO 越高画面越亮但噪点越多、动态范围越窄，用于暗光拍摄时权衡亮度与画质。',
    },
    'web-audio-metronome': {
        'eq': '拍间隔(ms) = 60000 / BPM；每小节拍数由拍号（如 4/4、3/4）决定',
        'desc': '基于 Web Audio 的精确时钟调度：按 BPM 计算拍间隔并预排音频事件以降低定时抖动；支持多种拍号与重音，用于乐器练习与节奏训练。',
    },

    # ================= CSS 生成器 / 图案类（核心原理与参数）=================
    'audio-recorder': {
        'desc': '基于 MediaRecorder 采集麦克风音频并本地保存为文件，支持音量与播放速度（playbackRate）调节及实时波形绘制；全程在浏览器内完成，数据不上传。',
    },
    'avatar-generator': {
        'desc': '按种子确定性生成几何 / 像素 / 渐变头像：种子决定形状与配色，同一种子结果一致；可调大小与圆角，支持导出 PNG 或 SVG，用于社交占位图与测试数据。',
    },
    'aztec-code': {
        'desc': '按 Aztec 码编码规则生成：文本经高等级纠错编码与位填充后排布为方阵，并带中央定位图案（简化版采用固定模式）；纯前端生成，用于票据与物流信息的移动端识读。',
    },
    'badge-generator': {
        'desc': '以 SVG 绘制圆角或盾形徽章：文字、配色与图标参数化后实时渲染并导出图片；基于矢量绘制，放大不失真，用于活动标识、成就奖章与社交头像。',
    },
    'blueprint-grid': {
        'desc': '由两套不同疏密的网格线按固定比例（如细格与粗格 5:1）叠加构成蓝图风格底纹，方格尺寸与颜色可调并导出图片；用于工程草图、手绘底图与演示背景。',
    },
    'border-radius-generator': {
        'desc': '四角半径分别映射为 CSS border-radius 的左上 / 右上 / 右下 / 左下值，实时预览并生成声明；支持独立设置各角，用于前端圆角样式落地。',
    },
    'breakpoint-queries': {
        'eq': '@media (min-width: <断点>) { /* 移动优先样式 */ }',
        'desc': '按移动优先思路生成媒体查询：以设备档位（如 640 / 768 / 1024 / 1280px）为 min-width 断点拼装 @media 规则，用于响应式布局的骨架代码。',
    },
    'button-generator': {
        'desc': '把背景、圆角、内边距、阴影与悬停态参数拼装为完整 CSS 规则（含 :hover 伪类），实时预览并可复制；用于快速产出风格统一的按钮样式。',
    },
    'card-generator': {
        'desc': '把圆角、阴影、内边距与配色参数组合为卡片 CSS（分层 box-shadow + border-radius），实时预览并可复制；用于落地页与列表卡片。',
    },
    'checkerboard-generator': {
        'desc': '按行列交替填充两种颜色生成棋盘图案：格子尺寸与配色可调并导出图片；用于棋类演示、背景底纹与游戏素材。',
    },
    'css-animation-generator': {
        'desc': '选择动画类型（平移 / 旋转 / 缩放 / 透明度等）后拼接 @keyframes 与 animation 声明，实时预览并复制；用于前端动效原型开发。',
    },
    'css-box-shadow-generator': {
        'desc': '按 offset-x / offset-y / blur / spread / color 拼装 box-shadow 声明，支持多层叠加与 inset 内阴影，实时预览并复制；用于元素立体感与层次设计。',
    },
    'css-border-radius': {
        'desc': '将各角半径（支持 px 与百分比）拼装为 CSS border-radius 声明，实时预览并复制；用于圆角容器、胶囊按钮与卡片。',
    },
    'css-grid-generator': {
        'eq': 'grid-template-columns: repeat(n, 1fr | <固定宽度> | auto)；gap: <行间距> <列间距>',
        'desc': '把列数、列宽方式（固定 / fr / auto）、gap 与断点拼装为 CSS Grid 声明及对应 HTML，实时预览并复制；用于二维布局搭建。',
    },
    'css-text-shadow': {
        'desc': '按 offset-x / offset-y / blur / color 拼装 text-shadow 声明，支持多层叠加，实时预览并复制；用于标题与标语的质感效果。',
    },
    'data-matrix': {
        'desc': '按 Data Matrix 编码规则生成：数据经 Reed-Solomon 纠错后排布为方阵，并带 L 形实线与虚线定位图案（简化版）；纯前端生成，用于工业零件与物料的小面积标识。',
    },
    'dot-pattern': {
        'desc': '按固定间距在背景上重复绘制圆点（可用错位排列形成六角感），点径、间距与配色可调并导出图片；用于包装、网页底纹与印刷稿。',
    },
    'favicon-from-emoji': {
        'desc': '将所选 Emoji 以指定字号渲染到 Canvas 并导出为多尺寸 ICO / PNG；用于快速更换站点图标，纯前端生成不上传。',
    },
    'favicon-from-text': {
        'desc': '把文字或字母渲染为方形图标（可调字体、字号与配色）并导出多尺寸 PNG / ICO；适合无 Logo 的小站快速获得品牌标识。',
    },
    'favicon-generator': {
        'desc': '上传图片或将文字 / Emoji 渲染到 Canvas，按 16 / 32 / 48 / 64 等尺寸导出并打包为 .ico；用于适配各浏览器与设备的站点图标。',
    },
    'flexbox-generator': {
        'eq': 'display: flex；flex-direction / flex-wrap / justify-content / align-items / gap 组合',
        'desc': '把 flex-direction、wrap、justify-content、align-items、gap 等属性拼装为 display:flex 声明，并以 1 / 2 / 3 个项目实时演示排列效果；用于一维布局。',
    },
    'font-pairing': {
        'desc': '从编排好的字体组合库中选取标题 / 正文字体对，生成对应的 font-family 与引用声明；组合按风格与可读性筛选，用于网页与海报的字体搭配。',
    },
    'font-preview': {
        'desc': '用系统字体栈分别渲染同一段文字并并排对比，点击卡片即可复制对应 font-family 声明；用于快速挑选与核对字体。',
    },
    'generator-6': {
        'desc': '拖动控件调节 offset / blur / spread / color 并拼装 box-shadow（支持 inset 与多层阴影），实时预览并复制；用于快速获得阴影样式。',
    },
    'generator-7': {
        'desc': '按边框宽度、样式、圆角与配色拼装 border 系列声明，支持单边独立设置；用于分隔线、卡片边框等样式产出。',
    },
    'generator-8': {
        'desc': '调用内置 qrcode.js 按文本生成二维码，支持尺寸、纠错级别与颜色定制并导出；用于名片、海报与物料上的信息扫码。',
    },
    'generator-9': {
        'eq': 'EAN-13 校验位 = (10 − (Σ 前 12 位奇偶权重 1/3 交替之和 mod 10)) mod 10',
        'desc': '按 EAN-13 等码制编码：数据位按奇偶位权重 1 / 3 交替加权求得校验位后绘制条空并导出；用于商品标签、仓储与演示。',
    },
    'generator-10': {
        'desc': '可视化编排关键帧：把时间点、动画属性与缓动函数拼装为 @keyframes 与 animation 声明，实时预览并复制；用于 CSS 动画开发。',
    },
    'generator-11': {
        'desc': '以 CSS 渐变（repeating-linear-gradient 等）或 SVG 平铺生成可重复背景纹理（点阵 / 网格 / 波浪），参数可调并导出代码；用于 UI 背景装饰。',
    },
    'generator-12': {
        'desc': '基于 Canvas 的粒子系统：按数量、速度、颜色与引力等参数逐帧更新粒子位置并渲染，可导出代码或图片；用于网页背景与活动页特效。',
    },
    'glassmorphism-generator': {
        'desc': '玻璃拟态 = 半透明背景 + backdrop-filter: blur() + 细边框 + 圆角 + 内高光；参数化拼装 CSS 并实时预览，用于现代 UI 卡片质感设计。',
    },
    'gradient-from-color': {
        'desc': '由单色推导渐变色标：在同色系（调整明度 / 饱和度）或互补色相基础上生成停靠点，拼装为 linear-gradient 并可调角度；用于快速生成协调渐变。',
    },
    'gradient': {
        'desc': '把起止颜色、角度与颜色停靠点拼装为 linear-gradient / radial-gradient 声明，实时预览并复制；用于网页背景与按钮配色。',
    },
    'grid-pattern': {
        'desc': '按固定间距重复绘制方格或网格线（线宽与颜色可调）生成背景图案并导出图片；用于工程图底图、网页纹理与印刷稿。',
    },
    'initials-avatar': {
        'desc': '取姓名首字母或缩写，按哈希映射到固定调色板生成带底色头像，可调字体与圆角并导出 PNG / SVG；用于团队与用户占位标识。',
    },
    'isometric-grid': {
        'desc': '等距网格由 30° / 150° 斜线按固定步距平铺构成菱形格，网格尺寸与配色可调并导出图片；用于 2.5D 游戏地图、插画底图与示意图。',
    },
    'loading-dots': {
        'desc': '三点加载动画：为每个点设置错开的 animation-delay 触发缩放或位移，参数化拼装 CSS 并可复制；用于网页加载占位。',
    },
    'material-color': {
        'desc': 'Material Design 色板共 19 色系 × 10 阶（50–900 及 A100–A700），点击色块可复制对应 HEX；用于遵循 Material 设计规范的配色。',
    },
    'mesh-gradient': {
        'desc': '网格渐变由多个径向渐变叠加构成：拖拽色标调整各色团的位置与颜色，导出为图片或 CSS；用于海报、封面与网页英雄区背景。',
    },
    'neomorphism-generator': {
        'desc': '新拟态 = 同色系浅色双阴影（左上高光 + 右下暗影）营造凸起或凹陷感；按距离、强度、模糊与底色拼装 box-shadow 与圆角并预览，用于柔和立体 UI。',
    },
    'particle-effect-generator': {
        'desc': '基于 Canvas 的实时粒子系统：支持多种发射模式与鼠标交互，参数实时调整即时生效；用于动态背景与视觉特效。',
    },
    'pattern-generator': {
        'desc': '基于 SVG <pattern> 生成无缝纹理（点阵 / 条纹 / 网格 / 波浪），调节间距、颜色与透明度后导出 CSS 背景声明；用于网页装饰。',
    },
    'pixel-art': {
        'desc': '网格化像素绘制：以二维数组存储每个像素的颜色，支持画笔、橡皮、填充与吸管，可撤销重做并导出原始或放大版 PNG；用于像素画创作。',
    },
    'pixel-art-generator': {
        'desc': '在网格上点击上色，数据按二维数组存储并渲染为字符画或 CSS 像素块；网格大小与调色板可调，用于像素风图形制作。',
    },
    'progress-bar-generator': {
        'desc': '按长度、厚度、圆角、渐变色与动画拼装进度条 HTML / CSS（含 @keyframes 流光），实时预览并可复制；用于下载、投票与任务进度展示。',
    },
    'ripple-effect': {
        'desc': '涟漪动效 = 点击处生成圆形伪元素并放大 + 淡出（transform / opacity 过渡）；参数化颜色、扩散半径与时长并导出 CSS / JS，用于 Material 风格按钮。',
    },
    'shadow-generator': {
        'desc': '按 offset / blur / spread / color 拼装 box-shadow（支持外阴影与 inset 内阴影），提供常用预设并实时预览；用于 UI 质感设计。',
    },
    'shadow-generator-advanced': {
        'desc': '高级阴影 = 多条 box-shadow 叠加（多层外阴影营造景深，inset 内阴影营造凹陷）或 drop-shadow 滤镜；逐层调节模糊与扩散并预览，用于卡片与按钮层次。',
    },
    'signature-pad': {
        'desc': '用 Canvas 记录指针轨迹，以 quadraticCurveTo 平滑相邻点，支持撤销与清空，导出透明背景 PNG；用于电子签名与手写批注。',
    },
    'skeleton-loader': {
        'desc': '骨架屏 = 占位色块（列表 / 卡片 / 图文）叠加 shimmer 流光动画（背景位移动画）；配置圆角、间距与闪烁后导出 CSS，用于加载占位。',
    },
    'spinner-generator': {
        'desc': '加载动画模板（旋转圆环、点阵等）基于 CSS @keyframes 的 rotate / scale 实现，可调尺寸、颜色与速度并复制；用于网页加载占位。',
    },
    'stripe-pattern': {
        'desc': '条纹纹理 = repeating-linear-gradient 按固定角度与周期重复双色条纹；条纹宽度、角度与配色可调并导出图片，用于包装、网页与印刷底纹。',
    },
    'spectrum-visualizer': {
        'desc': '基于 Web Audio 的 AnalyserNode 做 FFT，把音频各频段能量绘制为频域柱状谱并支持峰值查看；用于音频调试与教学演示。',
    },
    'tailwind-colors': {
        'desc': 'Tailwind CSS 色板共 22 色系 × 11 阶（50–950），点击色块可复制各种格式色值；用于遵循 Tailwind 设计体系的配色。',
    },
    'text-shadow-generator': {
        'desc': '按 offset / blur / color 拼装 text-shadow（支持多层叠加）并实时预览，用于标题装饰与网页视觉增强。',
    },
    'toast-generator': {
        'desc': 'Toast 提示 = 定位容器 + 图标 + 文案 + 进出场动画（translate / opacity）；按位置、图标与动画拼装 HTML / CSS / JS 片段，用于消息提示。',
    },
    'waveform-visualizer': {
        'desc': '把音频采样按时间绘制为振幅波形（Canvas 逐点连线），支持上传文件与缩放查看；用于信号分析与教学演示。',
    },

    # ================= 图像处理类（算法原理）=================
    'image-compress': {
        'desc': '用 Canvas 重绘并按 quality 参数导出（JPEG / WebP 为有损、PNG 为无损），并对比压缩前后体积；基于浏览器内置编解码器，原图不上传。',
    },
    'image-format-converter': {
        'desc': '经 Canvas 重编码实现 PNG / JPEG / WebP / BMP 互转，可调质量与尺寸；转换全程在浏览器本地完成，不上传图片。',
    },
    'image-mosaic': {
        'desc': '马赛克 = 把图像划分为 n×n 区块并对每块取平均色填充；块大小与作用区域（全图或框选）可调，用于本地打码脱敏。',
    },
    'image-rounded-corners': {
        'desc': '圆角图片 = 用 Canvas 路径（arcTo 圆角矩形）裁剪并保留透明通道后导出 PNG；圆角参数可调，用于头像与卡片图。',
    },
    'image-watermark': {
        'desc': '在 Canvas 上叠加文字或图片水印，支持位置、透明度、旋转、平铺与字号调节；纯本地处理，用于版权保护与批量加注。',
    },
    'palette-extractor': {
        'eq': '中位切分：在 RGB 空间沿像素分布最长的颜色轴递归取中位分割，直至达到目标色数 k',
        'desc': '基于中位切分（median-cut）色彩量化：反复沿最长颜色轴中位切分，得到 k 个代表色，相比平均法更能保留画面主色调；可编辑并导出 CSS 或 JSON。',
    },
    'vh-vw': {
        'eq': 'px → vw：vw = px ÷ 视口宽度 × 100；vw → px：px = vw × 视口宽度 ÷ 100（vh 同理按高度计算）',
        'desc': 'vw 与 vh 分别是视口宽、高的 1%，因此换算需给定基准视口尺寸。按宽度换算时以视口宽为基准、按高度换算时以视口高为基准，反向（vw/vh → px）则为乘算，用于替代写死的 px 实现自适应间距与全屏布局。',
    },
}
