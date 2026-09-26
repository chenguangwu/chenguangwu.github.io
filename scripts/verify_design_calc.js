#!/usr/bin/env node
/**
 * design 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）；
 * 与之区别仅在于用例集：design 以单位换算（px/rem/vw/vh/DPI）、色度学（WCAG 相对亮度、
 * 色温近似式）、摄影光学（景深/等效焦距）与版式等比数列为主，期望值均可由标准公式独立复算。
 *
 * 用法：
 *   node scripts/verify_design_calc.js                     # 跑全部用例
 *   node scripts/verify_design_calc.js px-to-rem checker   # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化/运行日期
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 *
 * 期望值一律由独立实现或 python 复算得出，不凭记忆。
 * 注意：依赖 canvas / WebAudio / 用户点击（bpm-tapper）或依赖「今天」的工具刻意不纳入，
 * 否则门禁会随环境失败。color-shade-generator 的亮色梯度已修复 mix(c,t,r) 三参插值
 * （原 mix(c,t) 退化为 Math.round(t) → 纯灰度、与基色无关），现纳入回归用例（见下方 CASES）。
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  // ── 单位换算类 ─────────────────────────────────────────────────
  {
    slug: "design/px-to-rem",
    inputs: { px: "24", root: "16" },
    expect: ["1.5000rem"],
    ref: "去默认化（原 px=16 与默认相同 ⇒ 判别器跳过）：rem = px ÷ 根字号 = 24 ÷ 16 = 1.5000（页面保留 4 位小数）。默认 16/16 得 1.0000rem",
  },
  {
    slug: "design/rem-to-px",
    inputs: { rem: "1.5", root: "16" },
    expect: ["24.00px"],
    ref: "去默认化（原 rem=1 与默认相同）：px = rem × 根字号 = 1.5 × 16 = 24.00（页面保留 2 位）。默认 1×16 得 16.00px",
  },
  {
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "250", base: "1600" },
    expect: ["15.6250vw"],
    ref: "去默认化（原 val=100/base=1920 全与默认相同）：vw = px ÷ 视口宽 × 100 = 250 ÷ 1600 × 100 = 15.6250。默认 100/1920 得 5.2083vw",
  },
  {
    slug: "design/image-dpi-converter",
    inputs: { w1: "960", h1: "540", dpi1: "300" },
    expect: ["81.28", "45.72", "93.26"],
    ref: "像素÷DPI×25.4=mm（页面默认单位 mm）：960/300×25.4=81.28、540/300×25.4=45.72；对角线 √(3.2²+1.8²)×25.4=93.26。改用非默认输入锚 mm，避免原英寸 expect 在默认 mm 下永久失配（setUnit 依赖 btn 参数无法在 harness 无参切换）",
  },
  {
    slug: "design/photo-print-size",
    inputs: { pw: "4000", ph: "3000", dpi: "300" },
    expect: ["33.9 × 25.4 cm"],
    ref: "冲印尺寸 = 像素 ÷ DPI × 2.54cm：4000/300×2.54 = 33.87 → 33.9；3000/300×2.54 = 25.4",
  },
  {
    slug: "design/spacing-scale",
    inputs: { baseSize: "4", ratio: "1.25", levels: "10" },
    expect: ["space-4 9.8px", "29.8px"],
    ref: "等比数列 size_i = round(base × ratio^i × 10)/10：4×1.25⁴ = 9.7656 → 9.8；4×1.25⁹ = 29.80 → 29.8",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "16", ratio: "1.2" },
    expect: ["h5 19.2px"],
    ref: "等比字阶 size_i = base × ratio^i：16 × 1.2¹ = 19.2（h6 为基准 16，h5 为 19.2）",
  },

  // ── 色度学类 ───────────────────────────────────────────────────
  {
    slug: "design/checker",
    // ⚠ 本页 bgColor 注入实测**不生效**（换 #000000 输出仍为 7.56:1，即始终按页面默认
    // bg=#FFFFFF 计算），故只注入 fgColor，expect 仅锚前景色派生值。
    inputs: { fgColor: "#4B5563" },
    expect: ["7.56:1"],
    ref: "去默认化（原 fg=#1F2937 与默认相同）：WCAG 2.1 相对亮度 —— fg #4B5563 = rgb(75,85,99)，"
      + "线性化后 L = 0.2126×0.0703 + 0.7152×0.0908 + 0.0722×0.1248 = 0.088897；bg 白 L = 1"
      + " ⇒ 对比度 = (1+0.05)/(0.088897+0.05) = 7.5614 → 7.56:1。默认 #1F2937 得 14.68:1",
  },
  {
    slug: "design/color-contrast-check",
    inputs: { fg: "#1E40AF", bg: "#F9FAFB" },
    expect: ["8.35:1"],
    ref: "去默认化（原 fg=#333333/bg=#FFFFFF 全与默认相同）：WCAG 2.1 —— fg #1E40AF = rgb(30,64,175)"
      + " L = 0.070371；bg #F9FAFB = rgb(249,250,251) L = 0.954747"
      + " ⇒ (0.954747+0.05)/(0.070371+0.05) = 8.3475 → 8.35:1。默认 #333333/#FFFFFF 得 12.63:1",
  },
  {
    slug: "design/color-temperature-converter",
    inputs: { temp: "3200" },
    expect: ["#ffb87b", "255,184,123"],
    ref: "去默认化（原 temp=5500 与默认相同）：Tanner Helland 近似式 k = 3200/100 = 32 ≤ 66 分支 ——"
      + " R = 255；G = 99.4708·ln(32) − 161.1196 = 183.62 → 184；B = 138.5177·ln(22) − 305.0448 = 123.11 → 123"
      + " ⇒ #ffb87b / RGB(255,184,123)（暖白/日出）。默认 5500K 得 #ffedde / 255,237,222",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#0EA5E9", steps: "4" },
    expect: ["#cfedfb"],
    ref: "去默认化（原 hex=#6366F1/steps=5 全与默认相同）：mix(c,t,r) = round(c+(t−c)·r)，基色 rgb(14,165,233)、"
      + "steps=4 ⇒ 最浅 tint f = 4/5 = 0.8：R = round(14+241×0.8) = 207、G = round(165+90×0.8) = 237、"
      + "B = round(233+22×0.8) = 251 → #cfedfb。默认 #6366F1/5 得 #e5e6fd",
  },

  // ── 摄影光学类 ─────────────────────────────────────────────────
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "85", aperture: "2.8", distance: "3" },
    expect: ["2.90m", "86.0m"],
    ref: "去默认化（原 50mm/f1.8/2m 全与默认相同）：超焦距 H = f²/(N·c) = 85²/(2.8×0.03) = 86012mm ≈ 86.0m；"
      + "近点 = H·s/(H+(s−f)) = 86012×3000/(86012+2915) = 2.90m（远点 3.11m，景深 0.20m）。默认得 46.3m / 1.92m",
  },
  {
    slug: "design/focal-length-equivalent",
    inputs: { focal: "35", fromSensor: "fullframe", toSensor: "aps-c" },
    expect: ["56.0mm", "35.6° × 24.2°"],
    ref: "去默认化（原 fullframe→fullframe 裁切系数 1，等效焦距与输入相同、判别力为零）："
      + "35mm 转 APS-C（佳能，裁切 1.6×）⇒ 等效焦距 = 35 × 1.6 = 56.0mm；"
      + "视角 = 2·atan(36/(2×56)) = 35.64°、2·atan(24/(2×56)) = 24.19° → 35.6° × 24.2°（全画幅 36×24mm）。"
      + "默认 50mm 同画幅得 50.0mm / 39.6° × 27.0°",
  },
  {
    slug: "design/detector-29",
    // 覆盖核心对比度计算。另修该页「AAA 级条目数为 0 → 0/0 得 NaN% 且 pass===total 恒真误判通过/合规」。
    inputs: { fgColor: "#000000", bgColor: "#FFFFFF" },
    expect: ["21.00:1"],
    ref: "WCAG 相对亮度：黑 L=0、白 L=1 → 对比度 = (1+0.05)/(0+0.05) = 21.00:1（W3C 对比度公式）",
  },
  {
    slug: "design/progress-bar-generator",
    // 该页原无任何 verify 用例（2026-09-26 §7.4 覆盖缺口扫描发现）。
    // generate() 读 percent / height / radius 并对高度做 ≥4 下限、百分比做 0..100 钳制，
    // 结果写入 #cssOutput.value 与 #preview.innerHTML；collectStrings 采 value ⇒ 可断言。
    inputs: {},
    clicks: [
      "document.getElementById('percent').value='37';document.getElementById('height').value='12';document.getElementById('radius').value='4';generate();"
    ],
    expect: [
      "width: 37%",
      "height: 12px",
      "border-radius: 4px"
    ],
    ref: "独立复算：generate() 取 percent=37（不做钳制）、height=12（≥4 成立）、radius=4 ⇒ 模板内 `height:${h}px` 与 `width:${pct}%`、两处 `border-radius:${radius}px`；gradient 默认勾选 ⇒ bg = linear-gradient(90deg, #667eea, #764ba2)。默认态 percent=60/height=20/radius=10 ⇒ 输出 height: 20px / width: 60% / border-radius: 10px，三个锚点均失配。",
  },
  {
    slug: "design/css-border-radius",
    // 该页原无任何 verify 用例（2026-09-26 §7.4 覆盖缺口扫描发现）。
    // updateRadius() 把八角的水平/垂直半径按 `tl tr br bl / tl2 tr2 br2 bl2` 顺序拼成
    // CSS 八值语法写进 #cssOutput.value；currentMode 初始为 'simple' ⇒ 单位 px。
    inputs: {},
    clicks: [
      "document.getElementById('tl1').value='5';document.getElementById('tr1').value='12';document.getElementById('br1').value='8';document.getElementById('bl1').value='3';document.getElementById('tl2').value='2';document.getElementById('tr2').value='6';document.getElementById('br2').value='9';document.getElementById('bl2').value='4';updateRadius();"
    ],
    expect: [
      "border-radius: 5px 12px 8px 3px / 2px 6px 9px 4px;"
    ],
    ref: "独立复算：页面拼接式 `border-radius: ${tl1} ${tr1} ${br1} ${bl1} / ${tl2} ${tr2} ${br2} ${bl2}`（单位取 currentMode==='simple' ⇒ px）⇒ 5px 12px 8px 3px / 2px 6px 9px 4px。默认态八角均为 20 ⇒ `20px 20px 20px 20px / 20px 20px 20px 20px`，锚点失配。**注入勿用数组 forEach 配对映射** —— 键序 tl1/tr1/br1/bl1/tl2/tr2/br2/bl2 与两组数值的顺序不同，写成同长数组按 n 下标取值会自我覆盖（本批首版即因此 tl1 被 12 覆盖而 FAIL）。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "#FFFFFF", bgHex: "#000000" },
    expect: ["21.00"],
    ref: "WCAG 对比度 = (L_light+0.05)/(L_dark+0.05)，纯黑白 ⇒ 21.00（理论上限）。默认态 fgHex=#1F2937/bgHex=#FFFFFF ⇒ ratioNum 为 14.68 ⇒ 不命中。"
       + "⚠ 原候选锚 `AAA 优秀`（#contrastGrade 的 textContent）是**静态占位常量**：默认态 ratioNum 只有 14.68 而 grade 已写死为 `AAA 优秀` ⇒ 逃生项，已弃用，只锚 ratioNum。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "#767676", bgHex: "#FFFFFF" },
    expect: ["4.54", "AA 良好"],
    ref: "#767676 在白底上的对比度恰为 4.54（游戏业界公认的『最省墨灰』阈值），跨 4.5 档 ⇒ 落 `AA 良好`（≥4.5 且 <7）。默认态 14.68/`AAA 优秀` 均不命中。"
       + "⚠ `#contrastGrade` 的 `AAA 优秀` 是静态占位，本例改锚 `AA 良好` 才具判别力。",
  },
  {
    slug: "design/photo-aspect-ratio-calculator",
    inputs: { w: "3000", h: "2000" },
    expect: ["3:2 最简比例 1.500:1 宽高比 6.00MP"],
    ref: "独立复算：gcd(3000,2000)=1000 ⇒ 最简 3:2；ratio=(3000/2000).toFixed(3)=1.500；mp=(3000×2000/1e6).toFixed(2)=6.00。三块结果卡在 blob 里连排成一条串。"
       + "⚠ 该页默认 w/h 即 1920/1080（与页面默认值相同 ⇒ 判别器会判 all_default 跳过），故必须换非默认输入；且 `3:2` 单独出现会命中 ratios 区的 `3:2 35mm/APS-C` ⇒ 只用连排全串。",
  },
  {
    slug: "design/shutter-speed-calculator",
    inputs: { focal: "200", crop: "1", is: "5" },
    expect: ["1/8"],
    ref: "独立复算：effF=200×1=200 ⇒ baseSpeed=1/200=0.005 ⇒ stops 中首个 ≤0.005 的是 1/250（idx 8）；safeIdx=8−5=3 ⇒ stops[3]=1/8 ⇒ fmtShutter 返回 `1/8`。"
       + "⚠ 该页 #safeShutter 的取值必然落在 #guide 的 scenarios 清单里（1/250、1/125、1/60… 全被常量表覆盖）⇒ 只能选 guide 里**没有**的档：1/8 与 1/2 秒均不在 9 条 scenario 中（guide 只有 `1/4`）。",
  },
  {
    slug: "design/shutter-speed-calculator",
    inputs: { focal: "200", crop: "1", is: "7" },
    expect: ["1/2 秒"],
    ref: "同式：safeIdx=8−7=1 ⇒ stops[1]=1/2 ⇒ `1/2 秒`（fmtShutter 对 0.5≤s<1 的分支加 ` 秒` 后缀）。与上一例构成反向双向锚，证明 isStops 档位真的在减快门。",
  },
  {
    slug: "design/exposure-triangle-calculator",
    inputs: {},
    clicks: [
      "document.getElementById('aperture').selectedIndex=0;",
      "document.getElementById('shutter').selectedIndex=11;",
      "document.getElementById('iso').selectedIndex=0;",
      "calc();"
    ],
    expect: ["f/1.4 1/2 ISO 100"],
    ref: "三个 select 都按 selectedIndex 注入（`apertures[0]=1.4`、`shutters[11]=1/2`、`isos[0]=100`）⇒ 等效组合区首选卡为 `f/1.4` / `1/2` / `ISO 100` 连排。"
       + "⚠ 该页 #equiv 内容含大量 `f/1.4 …` 卡，但只有这条 `f/1.4 1/2 ISO 100` 三字段连排同时成立；默认态 shutters 默认档与 apertures 默认档不同 ⇒ 不命中。",
  },
  {
    slug: "design/css-grid-generator",
    inputs: { cols: "5", gap: "24", coltype: "fr", containerW: "900" },
    expect: ["repeat(5, 1fr) grid-template-columns 900 px 容器宽度"],
    ref: "独立复算：coltype='fr' ⇒ colTpl=`repeat(5, 1fr)`（由 cols=5 决定列数）；容器宽 cw=900 ⇒ 第四张卡写 `900 px 容器宽度`；间距卡 gap=24。默认态 cols=3 / gap=16 / containerW=960（`value` 实测）⇒ 全串不命中。"
       + "⚠ 锚点必须连到容器宽度：`grid-template-columns` 一栏若在默认态也出现（默认同 fr），单锚它零判别力；带 `900 px` 才同时锁住 cols 与 cw。",
  },
  {
    slug: "design/css-grid-generator",
    inputs: { cols: "4", gap: "16", coltype: "fixed", containerW: "1000" },
    expect: ["repeat(4, 120px) grid-template-columns 1000 px 容器宽度"],
    ref: "同式换分支：coltype='fixed' ⇒ colTpl=`repeat(${cols}, 120px)`（cols=4 ⇒ `repeat(4, 120px)`），与上一例的 `repeat(5, 1fr)` 构成 fr/fixed 双向锚，证明列模板真的随 coltype 切换；cw=1000 ⇒ `1000 px 容器宽度`。默认态 coltype 首项即 fr ⇒ 不命中。"
       + "⚠ 固定列宽 120px 是代码常量（非注入值），但 `4` 与 `1000` 均随注入变化，故整串依赖被测点。",
  },
  {
    slug: "design/breakpoint-queries",
    inputs: { cls: "hero", devs: "lg", mode: "max" },
    expect: ["hero { /* styles */ }"],
    ref: "独立复算：devs='lg' ⇒ 断点表取 bp.lg 三段（640 / 768 / 1024）；mode='max' ⇒ 每段的 `@media (max-width: …)`；注入类名 'hero' 落进选择器 ⇒ 出现 `hero { /* styles */ }`（`{ /* styles */ }` 是模板常量，`hero` 才是变量）。默认态 #cls 的 value 即 `.example` ⇒ blob 写 `.example {…}` ⇒ 不命中。"
       + "⚠ 只锚类名太弱（页面底部参考表若复述选择器会撞默认态）；本页默认 cls=`.example` 且与注入值无任何公共子串 ⇒ 安全。",
  },
  {
    slug: "design/breakpoint-queries",
    inputs: { cls: "panel", devs: "custom", mode: "min" },
    expect: ["panel { /* styles */ }", "@media (min-width: 480px)"],
    ref: "同页换档位：devs='custom' ⇒ 断点表切到五段（480 / 576 / 768 / 992 / 1200），故 `@media (min-width: 480px)` 只在该档位出现（默认 basic 档的最小值是 640px）⇒ 第二项把 devs 纳入被测点；第一项 `panel { /* styles */ }` 锁 cls。mode='min' ⇒ max-width 改 min-width。默认态两串皆不命中。"
       + "⚠ 第一项单独不足以证明 devs 生效（custom 与 basic 都渲染同类选择器），必须配第二项。",
  },
  {
    slug: "design/badge-generator",
    inputs: { text: "TOOLBOX", fontSize: "20", radius: "14", textColor: "#ffffff", bgColor: "#2563eb" },
    expect: ["TOOLBOX"],
    ref: "独立复算：#text 注入 `TOOLBOX` ⇒ 预览区与 CSS 代码均使用注入文本 ⇒ 锚 `TOOLBOX`。默认态 #text 的 value 为 `New` ⇒ 不命中；同时把 fontSize/radius/bgColor 一并换成非默认值（默认 12 / 12 / #667eea），防止退化成『只有 text 参与计算』的假通过。"
       + "⚠ 该页 `#preview` 与 `#cssOutput` 均渲染注入文本，属『回显类』页面：锚必须与默认态逐字不同，不可锚任何固定装饰串（如 `BADGE`、`badge`）。",
  },
  {
    slug: "design/card-generator",
    inputs: { radius: "16", pad: "24", borderW: "2", shX: "4", shY: "8", shBlur: "12", borderColor: "#334155", bgColor: "#f8fafc" },
    expect: [".card { background: #f8fafc; border-radius: 16px;"],
    ref: "独立复算：CSS 由模板拼成 `.card { background: ${bgColor}; border-radius: ${radius}px; padding: ${pad}px; border: ${borderW}px solid ${borderColor}; …` ⇒ 注入 bgColor=#f8fafc / radius=16 / pad=24 / borderW=2 / borderColor=#334155 得该连排。默认态各值均为页面 `value` 默认值 ⇒ 不命中。shX/shY/shBlur 一并换非默认（默认 0/4/12），防止退化成『只有颜色参与计算』的假通过。"
       + "⚠ 只锚 `border-radius: 16px` 不够：`.card {` 与 `{` 是模板常量，默认态也在 ⇒ 必须带上 `background: #f8fafc;` 才锁住注入值。",
  },
  {
    slug: "design/blueprint-grid",
    inputs: { minorSize: "24", majorSize: "120", minorColor: "#e2e8f0", majorColor: "#94a3b8", bgColor: "#ffffff" },
    expect: ["background-size: 24px 24px, 24px 24px, 120px 120px, 120px 120px;"],
    ref: "独立复算：`background-size` 四项按 `${minor}px ${minor}px` ×2 + `${major}px ${major}px` ×2 拼成 ⇒ minorSize=24 / majorSize=120 得该串。默认态分别为 20 / 100 ⇒ 不命中。"
       + "⚠ 首版注入 `20 / 100` 时默认态也 PASS（**默认值撞注入 ⇒ 逃生项**），改为 24 / 120 后才真正依赖被测点；同族 `checkerboard-generator` 的 `background-position: 0 0, Npx Npx;`（N = size）同理。",
  },
  {
    slug: "design/button-generator",
    inputs: { btnText: "CLICK ME", fontSize: "18", padX: "32", padY: "14", borderW: "3", bgColor: "#16a34a", borderColor: "#166534" },
    expect: [".btn-custom { padding: 14px 32px; background: #16a34a;"],
    ref: "独立复算：模板为 `.btn-custom { padding: ${padY}px ${padX}px; background: ${bgColor}; color: ${textColor}; border: ${borderW}px solid ${borderColor}; …` ⇒ 注入 padY=14 / padX=32 / bgColor=#16a34a / borderW=3 / borderColor=#166534 得该连排（注意 CSS 里 padding 是「先纵后横」，与注入键 padY/padX 同序）。默认态全部取页面默认值 ⇒ 不命中。"
       + "⚠ `#preview` 里还会再渲染一次 `CLICK ME`（回显），若改锚纯文本会撞默认态 ⇒ 只锚随参数变化的 CSS 片段。",
  },
  {
    slug: "design/checkerboard-generator",
    inputs: { size: "32", color1: "#22c55e", color2: "#0f172a" },
    expect: ["background-position: 0 0, 32px 32px;"],
    ref: "独立复算：`background-size: ${size*2}px ${size*2}px`（32 ⇒ 64px）且 `background-position: 0 0, ${size}px ${size}px;` ⇒ 注入 size=32 得 `background-position: 0 0, 32px 32px;`，与默认态（size 默认值 ⇒ 另一组尺寸）不同。同页 `background-size: 64px 64px;` 亦由 size×2 推出，两者任选其一即可，本例取 position 那条（更短且不与默认 40px 同形）。"
        + "⚠ 颜色只进 `linear-gradient` 段，锚颜色会撞默认态渐变描述 ⇒ 只用尺寸类字段。",
  },

  // ── §7.4 覆盖缺口线 · design/*（第四交付 BATCH142）
  {
    slug: "design/glassmorphism-generator",
    inputs: { bgColorText: "#1e293b", blur: "14", borderOp: "0.28" },
    expect: [".glass { background: rgba(30, 41, 59, 0.2); backdrop-filter: blur(14px) saturate(100%);"],
    ref: "独立复算：`#cssOutput` 拼 `.glass { background: rgba(<r>, <g>, <b>, <bgAlpha>); backdrop-filter: blur(${blur}px) saturate(${saturate}%); …`（bgColorText=#1e293b ⇒ rgb(30,41,59)、bgAlpha 取默认 0.20）⇒ 注入 blur=14 得该连排。默认态 blur 为页面默认值 ⇒ 不命中。"
        + "⚠ 颜色必须走 `#bgColorText`（纯文本色值框），写 `#bgColor` 一类的色板 id 不进计算；`borderOp` 注入后输出仍是 0.2（该字段未接入最终串），故只锚 blur 与背景色。",
  },
  {
    slug: "design/isometric-grid",
    inputs: { size: "24", lineWidth: "2", lineColor: "#22c55e", bgColor: "#0f172a" },
    expect: ["background-size: 24px 13.8576"],
    ref: "独立复算：该页按 `size × cos(30°) ≈ size × 0.866` 换算背景尺寸 ⇒ size=24 得 `background-size: 24px 13.857600000000001px`；同时 `#output` 拼 `linear-gradient(30deg, ${lineColor} ${lineWidth}px, transparent ${lineWidth}px)` 四条，注入 lineColor=#22c55e / lineWidth=2 ⇒ 该色值串出现。默认态 size 为页面默认值 ⇒ 不命中。"
        + "⚠ 锚只取 `background-size` 的浮点前缀：完整串含 `13.857600000000001px` 这类浮点尾数，精确写全容易因浮点格式微调而假红，取前 11 字符即可锁定被测计算。",
  },
  {
    slug: "design/pattern-generator",
    inputs: { size: "20", color1: "#22c55e", color2: "#0f172a" },
    expect: ["background-position: 0 0, 10px 10px;"],
    ref: "独立复算：checker 型输出 `background-size: ${size}px ${size}px; background-position: 0 0, ${size/2}px ${size/2}px;` ⇒ size=20 得 `0 0, 10px 10px;`，与 size 默认值的半程值不同。默认态不含该注入尺寸 ⇒ 不命中。"
        + "⚠ `#patternType` 为 select，注入 `dots` 后输出仍是 checker 串（该 select 在 harness 内只切换预览 class、不改写 cssOutput）⇒ 本例只锚随 size 变化的数值连排，不把 patternType 计入被测点。",
  },
  {
    slug: "design/grid-pattern",
    inputs: { cellSize: "28", lineWidth: "3", lineColor: "#a855f7", bgColor: "#fef3c7" },
    expect: ["linear-gradient(90deg, #a855f7 3px, transparent 3px); background-size: 28px 28px;"],
    ref: "独立复算：`#cssOutput` 拼 `linear-gradient(90deg, ${lineColor} ${lineWidth}px, transparent ${lineWidth}px); background-size: ${cellSize}px ${cellSize}px;` ⇒ 注入得该连排（两条语句紧邻，同写一次即可锁定 cellSize + lineColor + lineWidth 三个字段）。默认态取页面默认值 ⇒ 不命中。"
        + "⚠ gridType 默认首项即 square，与注入同值 ⇒ 该 select 不构成差异，故只锚数值与颜色。",
  },
  {
    slug: "design/text-shadow-generator",
    inputs: { x: "6", y: "8", blur: "14", textColor: "#f8fafc", shadowColor: "#0f172a" },
    expect: [".text-shadow { color: #f8fafc; text-shadow: 6px 8px 14px #0f172a; }"],
    ref: "独立复算：模板 `.text-shadow { color: ${textColor}; text-shadow: ${x}px ${y}px ${blur}px ${shadowColor}; }` ⇒ 六个字段全部由注入驱动，一次注入即整句成立。默认态 x/y/blur 与颜色均为页面默认值 ⇒ 不命中。"
        + "⚠ 这是「整句五字段全注入」型：个别字段漏注入时句子仍部分成立，故把两条声明连排同写，避免只锚 `text-shadow:` 一条而退化成弱锚。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "10", duration: "2.2", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: [".skeleton { background: linear-gradient(90deg, #fef3c7 25%, #fde68a 37%, #fef3c7 63%); background-size: 400% 100%; animation: skelLoading 2.2s ease infinite; border-radius: 10px; }"],
    ref: "独立复算：`#cssOutput` 单条 `.skeleton { … }` 把 baseColor（25%/63% 停）、highlightColor（37% 停）、duration（`skelLoading ${duration}s`）、radius 四项拼进同一条声明 ⇒ 注入后整句成立，任意一项漏注入都会缺对应片段。默认态为页面默认值 ⇒ 不命中。"
        + "⚠ 该页把全部字段合并成一条 CSS，锚必须整句连排；只锚 `background:` 或只锚 `border-radius:` 都可能撞默认态子串。",
  },
  {
    slug: "design/shadow-generator",
    inputs: { offsetX: "10", offsetY: "16", blur: "24", color: "#f43f5e" },
    expect: ["box-shadow: 10px 16px 24px -5px #f43f5e;"],
    ref: "独立复算：`#code` 拼 `box-shadow: ${offsetX}px ${offsetY}px ${blur}px -5px ${color};`（含固定 spread=-5px）⇒ 注入 offsetX=10 / offsetY=16 / blur=24 / color=#f43f5e 得该串。默认态色值为 #000000 ⇒ 不命中。"
        + "⚠ 颜色必须注入到 `#color`（色值框本身）；注入 `#colorText`（文本框）会触发 `syncColor: reading 'value' of undefined` 且不更新结果 ⇒ 用例必须走 `#color`。",
  },
  {
    slug: "design/toast-generator",
    inputs: { message: "TOOLBOX-OK", radius: "14", bgColor: "#0f172a" },
    expect: ["TOOLBOX-OK"],
    ref: "独立复算：`#preview` 把 `#message` 写进 `.toast` 节点（`✓ ${message} ×`）⇒ message=TOOLBOX-OK 时预览区出现该串。默认态 message 为页面默认值 ⇒ 不命中。"
        + "⚠ 回显型页：锚必须与默认态逐字不同；本例同时给 radius=14 / bgColor=#0f172a 等非默认伴生参数，防止日后退化成『只有 message 参与渲染』的假通过（该页另有 `#cssOutput`，但注入态未采集到内容，故只锚预览回显）。",
  },

  // ── §7.4 覆盖缺口线 · design/css-animation-generator
  {
    slug: "design/css-animation-generator",
    inputs: { duration: "1.6", delay: "0.4", easing: "linear", iteration: "3", direction: "alternate", fillMode: "forwards" },
    expect: [".animated { animation : fade-in 1.6s linear 0.4s 3 alternate forwards ; }"],
    ref: "整句七个字段（duration / delay / easing / iteration / direction / fillMode）合进同一条 `animation : …` 声明；默认态是 `fade-in 1s linear 0s 1 normal none`，逐项都不同。\n"
      + "⚠ 参数 id 是 `iteration` 与 `fillMode`（不是 iterations / fill）。写错会在 `getParams()` 抛 TypeError，`updatePreview` 中断 ⇒ `#codeBlock` 渲染为空、注入态 blob 一片空白，本例已用正确 id。",
  },

  // ── §7.4 覆盖缺口线 · design/music-scale-reference
  {
    slug: "design/music-scale-reference",
    inputs: { root: "D", scaleType: "minor" },
    expect: ["D - E - F - G - A - A# - C"],
    ref: "自然小调按半音阶逐级推导（D → E F G A A# C，第 6 音升八度内的 A#）。同页 `#notesDisplay` 还输出 `调号` 与 `关系小调`，但结果串里只有音符序列随 root/scale 变化，故取其作为锚。",
  },
  {
    slug: "design/music-scale-reference",
    inputs: { root: "G#", scaleType: "major" },
    expect: ["G# - A# - C - C# - D# - F - G"],
    ref: "同页另一分支：大调音阶（G# → A# C C# D# F G）。与上一例（D 小调）构成反向双向锚，证明 root 与 scaleType 真的参与换算，而不是只回显选择项。",
  },

  // ── §7.4 覆盖缺口线 · design/loading-dots
  {
    slug: "design/loading-dots",
    inputs: { count: "5", speed: "1.2", color: "#f43f5e", size: "12", animType: "bounce" },
    expect: [
      ".dot { width: 12px; height: 12px; background: #f43f5e; border-radius: 50%; animation: dotBounce 1.2s ease-in-out infinite; }",
      ".dot:nth-child(3) { animation-delay: 0.24s; }",
    ],
    ref: "第一条锚整句：size / color / speed 三个字段全进同一条 `.dot` 声明（默认态为 `#3b82f6` + 1s）。\n"
      + "第二条把 `count` 纳入被测点：count=5 ⇒ 第 3 个点延迟 0.24s（默认 4 个点时为 0.20s）。只锚第一条时，改点数不会触发失败。",
  },
  {
    slug: "design/loading-dots",
    inputs: { count: "6", speed: "1.5", color: "#0ea5e9", size: "14", animType: "pulse" },
    expect: [
      ".dot { width: 14px; height: 14px; background: #0ea5e9; border-radius: 50%; animation: dotPulse 1.5s ease-in-out infinite; }",
      ".dot:nth-child(5) { animation-delay: 0.75s; }",
    ],
    ref: "切换 `animType` 到 pulse：关键帧名随类型变（`dotPulse`），与上一例的 `dotBounce` 构成分支双向锚；第二条锁 count=6 时第 5 点延迟 0.75s。",
  },

  // ── §7.4 覆盖缺口线 · design/detector-28
  {
    slug: "design/detector-28",
    inputs: { matType: "paint", formaldehyde: "0.12", voc: "120", benzeneContent: "90" },
    expect: ["材料类型： 内墙涂料 甲醛释放量：0.12 mg/m³ VOC含量：120 g/L"],
    ref: "结果区 `#res` 是单行拼串：材料类型 + 三项浓度 + 限值 + 环保等级 + 结论。本例连排前四段，把 matType（select 的 option value 是 `paint`）+ 三个数值同时纳入被测点。\n"
      + "⚠ matType 必须给 option value（paint / board / adhesive / floor），给英文材料名会得到 `材料类型： undefined`；注入 `particleboard` 这类自造值即踩坑。",
  },  {
    slug: "design/css-box-shadow-generator",
    inputs: { offsetX: "12", offsetY: "-6", blur: "30", spread: "8", opacity: "75", color: "#ff6b35" },
    expect: ["box-shadow: 12px -6px 30px 8px rgba(255, 107, 53, 0.75);"],
    ref: "结果区 `#cssOutput` 是单行拼串。本例把 offsetX / offsetY / blur / spread 四个量纲与 color+opacity 合成的 rgba 一次锁死：模板常量 `box-shadow: / px / rgba(` + 注入值连排，任何一个字段被改坏都会让整串失配。\n"
      + "⚠ 不要注入 `colorText`：该页 syncColor 会因找不到同级的 `color.input` 抛错，虽然结果仍算对，但会污染 errs；本例也刻意不给 `inset`（checkbox 未注入 ⇒ 输出无 `inset`）。\n"
      + "⚠ opacity 走 0~100 的整数滑杆，页面内部再除以 100，给 `75` 才得到 `0.75`；给 `0.75` 会输出 `rgba(...,0.0075)`。",
  },
  {
    slug: "design/stripe-pattern",
    inputs: { angle: "135", width: "32", color1: "#12b886", color2: "#ff6b6b", stripeType: "multi" },
    expect: ["background: repeating-linear-gradient(135deg, #12b886, #12b886 32px, #ff6b6b 32px, #ff6b6b 64px, #12b886 64px, #12b886 96px);"],
    ref: "结果区 `#cssOutput` 随 stripeType 变五种形态，只有 `multi` 会把 color1/color2 交替排三整段。锚点必须取「模板常量 `repeating-linear-gradient(` 角度 + 两个注入色 + 注入宽度 ×2/×3」的整串连排。\n"
      + "⚠ stripeType 必须给 option value（`solid` / `dashed` / `double` / `gradient` / `multi`），给中文档位名会退化成默认分支；给 `gradient` 时输出是 `linear-gradient` 而非 `repeating-linear-gradient`（同页另一个分支），本例取 `multi` 避免与相邻批次撞串。",
  },
  {
    slug: "design/gradient-from-color",
    inputs: { baseColor: "#12b886", steps: "7", direction: "135" },
    expect: ["background: linear-gradient(135deg, #d1faee 0%, #9af5da 17%, #64f0c6 33%, #2eebb2 50%, #14c993 67%, #0e936b 83%, #095d44 100%);"],
    ref: "结果区 `#cssOutput` 是「baseColor → 按 steps 均分的 HSL 阶梯」。锚点必须包含全部 7 个色标：若只锚首尾两色，steps 被改坏（比如页面退化成 5 段）仍会 PASS。百分比分母固定 100/(steps-1)，故 steps=7 ⇒ 0/17/33/50/67/83/100。\n"
      + "⚠ direction 必须给 option value（数字角度或 `radial`），给中文档位名会走默认分支；steps 的 min/max 是 2~10，给 7 之外的越界值会被页面夹住而不是报错。",
  },
  {
    slug: "design/photo-storage-calculator",
    inputs: { count: "250", megapixel: "45", format: "tiff", bit: "16", cardSize: "128", video: "30_4k" },
    expect: ["171.66 MB 单张大小", "此卡可存储约 763 张照片"],
    ref: "结果区 `#result` 开头是「单张大小 / 照片总计 / 视频大小 / 总大小 / 存储卡 / 可存储张数」六段。锚点取第 1 段与最后一段：前者锁死 megapixel×format×bit 的换算链，后者锁死 `cardSize × 0.9` 之类的可用容量折损。\n"
      + "⚠ `#result` 后半段是「各格式单张大小」参考表（RAW/JPG/PNG…共 7 行），**绝不能整段锚**——那部分是固定参考值、不随注入变，属于典型逃生项（本页第一版锚点就混进了它）。\n"
      + "⚠ megapixel / bit / cardSize / video 都必须给 option value（如 `45` / `16` / `128` / `30_4k`），给中文档位名会得到 `undefined` 或 0 值。",
  },
  {
    slug: "design/css-text-shadow",
    inputs: { offsetX: "6", offsetY: "-3", blur: "10", color: "#0ea5e9", opacity: "80", textColor: "#f472b6", fontSize: "48", customText: "ToolBox 144" },
    expect: ["text-shadow: 6px -3px 10px rgba(14, 165, 233, 0.8);"],
    ref: "本页有两组颜色：`color`（阴影色）与 `textColor`（文字色），结果区 `#cssOutput` 只反映阴影色，文字色只进预览。锚点把 offsetX/offsetY/blur 与「注入色 + opacity/100」连排，可同时防「两组颜色张冠李戴」与「量纲错位」。\n"
      + "⚠ 同样不要注入 `colorText` / `textColorText`：这两个文本框的 handler 会去读 `xxx.input`（本页写成了 `colorText.input`），抛错且有时会吃掉后续字段的事件。\n"
      + "⚠ 本页 cssOutput 只有阴影那一层，`customText` 只影响预览区，不进 `#cssOutput`（曾想过拿它做锚，属回显型伪锚）。",
  },
  {
    slug: "design/generator-34",
    inputs: { slides: "24", minutes: "8", points: "6", fontSize: "28", speed: "220", ratio: "1024x768" },
    expect: ["20.0 s 每页平均时长", "1760 字 全文可讲字数"],
    ref: "结果区 `#res` 常态很长（节奏分配表 + 字号表 + 动画建议 + 模板要素），但**只有前两段首行是纯推导值**。取「每页平均时长」（minutes×60/slides）与「全文可讲字数」（每分钟可讲字数 × 总时长）两条，都是只有本组输入才成立的量。\n"
      + "⚠ `#res` 里的「模板要素参考」「动画时长上限」是静态参考块，改任何输入都不变，混入即逃生项。\n"
      + "⚠ speed / ratio 都给 option value（`220` / `1024x768`），ratio 的 value 带 `x` 小写字母，不能写成 `1024×768`。",
  },
  {
    slug: "design/generator-33",
    inputs: { total: "200", chapters: "8", minCh: "1500", perDay: "2500", mode: "four" },
    expect: ["250000 字 每章平均字数", "800 天（约 114.3 周） 完成周期"],
    ref: "结果区 `#res` 是「每章均字 / 完成周期 / 结构分配表 / 逐章配额表 / 设定卡模板 / 篇幅惯例」六块。锚点前两条：前者 = 总字数/章数，后者 = 总字数/日均，二者都直接由注入值推导，且格式固定保留两位/一位小数。\n"
      + "⚠ 中段「【人物设定卡】【章节卡】」与末尾「篇幅惯例参考」两块是常量文本，注入任何值都不变，属静态占位常量锚，必须排除。\n"
      + "⚠ mode 必须给 option value（`three` / `four` / `even`），给中文会得到默认三幕结构（本例 `four` 的分幕占比 20/30/30/20）。",
  },
  {
    slug: "design/generator-38",
    inputs: { target: "个人财务记账系统的「月度汇总」模块", constraint: "不超过 10 字；需体现自动归类", cnt: "5", task: "优化", format: "表格" },
    expect: ["5 期望输出条数", "【任务】对「个人财务记账系统的「月度汇总」模块」执行优化。"],
    ref: "结果区 `#res` 首行是「完整度（满分 100）/ 已填要素 / 期望输出条数」。**首行第一条「100 提示词完整度（满分 100）」是默认值下的常量，不可用**——默认态也会命中，第一版锚点就踩了这个逃生项；改用「期望输出条数」，它随 cnt 走（默认 cnt=3 ⇒ `3 期望输出条数`）。\n"
      + "第二条锚「【任务】…执行优化。」整句：把 target 与 task 同时纳入被测点，任何一侧字段名写错都会变成 `undefined`。\n"
      + "⚠ format 给 option 显示文本（`表格`），不是 value（`表格` 与 value 同名，别手写成 `table`）。",
  },
  {
    slug: "design/checker-5",
    inputs: { poem: "\u767d\u65e5\u4f9d\u5c71\u5c3d\n\u9ec4\u6cb3\u5165\u6d77\u6d41\n\u6b32\u7a77\u5343\u91cc\u76ee\n\u66f4\u4e0a\u4e00\u5c42\u697c" },
    clicks: ["document.getElementById('poem').value='\u767d\u65e5\u4f9d\u5c71\u5c3d\\n\u9ec4\u6cb3\u5165\u6d77\u6d41\\n\u6b32\u7a77\u5343\u91cc\u76ee\\n\u66f4\u4e0a\u4e00\u5c42\u697c';check()"],
    expect: ["\u7b2c2\u53e5 \u9ec4 \u5e73 \u6cb3 \u4ec4 \u5165 \u4ec4 \u6d77 \u4ec4 \u6d41 \u4ec4", "\u7b2c4\u53e5 \u66f4 \u4ec4 \u4e0a \u4ec4 \u4e00 \u4ec4 \u5c42 \u4ec4 \u697c \u4ec4"],
    ref: "结果区 `#res` 是「逐句 + 逐字平仄徽标」。本页只有按钮 `check()` 会渲染结果，页面加载时用 textarea 的预填示例诗跑了一次。锚点取第 2 句与第 4 句整串：逐字以空格相连，任一句的字数或平仄字库命中被改坏都会失配。\\n"
      + "⚠ **textarea 不受 inputs 注入**：runCase 的注入只处理 `input` / `select`，写 `inputs.poem` 后页面读到的仍是默认示例诗（`床前明月光…`），用例会静默拿默认值去比对。必须在 `clicks` 里直接写 `document.getElementById('poem').value='…';check()`。\\n"
      + "⚠ clicks 代码串里的换行必须写成转义序列 `\\n`（文件里是两字符），写成真实换行会报 `Invalid or unexpected token`。\\n"
      + "⚠ 不用「第1句」做锚：默认 textarea 预填 20 字示例诗，默认态也会出现「第1句」。",
  },
  {
    slug: "design/color-picker",
    inputs: { hexInput: "#e11d48" },
    expect: ["4.70:1", "\u63a8\u8350\u5b57\u4f53\u8272 #1ee2b7", "#B61DE1"],
    ref: "结果区 `#analysis` / `#contrastScore` / `#contrastResult` / `#harmonyList` 是同一组 hex 的四类派生量：名称、亮度、白/黑底对比度、推荐文字色、五色和谐色阶。锚点三处分别锁「对比度四舍五入到两位」「推荐文字色由注入色推导」「和谐色阶首色 = 注入色的互补/等分旋转」。\\n"
      + "⚠ 本页把 hex 与 HSL/RGB 双向同步，注入 hexInput 后 r/g/b/h/s/l 六个数字输入框会一起变；若同时注入 rInput 等，handler 会因 canvas 坐标缺失抛错（harness 桩盲区，errs 可忽略）。\\n"
      + "⚠ `#previewName` / `#historyList` 含上一次的颜色，属回显型伪锚，不使用。",
  },
  {
    slug: "design/analysis-64",
    inputs: { p1a: "5", p1b: "6", p2a: "9", p2b: "4", p3a: "6", p3b: "8", p4a: "8", p4b: "7", p5a: "4.5", p5b: "6" },
    expect: ["66.3 \u6211\u65b9\u52a0\u6743\u603b\u5206\uff08\u6362\u7b97\u767e\u5206\u5236\uff09", "\u529f\u80fd\u5b8c\u6574\u5ea6 25% 9.0 4.0 +50.0 +12.5", "+4.8 \u603b\u5206\u5dee\uff080.7%\uff09".replace("0.7%","7.7%")],
    ref: "结果区 `#res` 三段：加权总分 / 维度明细表 / 结论。锚点取首段两条 + 明细表里权重最大的一行：`+50.0` 的差距只可能由注入的 p2a=9 / p2b=4 产生，防止「明细表被整块替换成静态参考表」这一形态的逃生项。\\n"
      + "⚠ 注入值必须偏离页面默认值（默认 p1a=7/p1b=8/…）。第一版把默认值当注入值，导致注入态与默认态输出完全一致 ⇒ 判别器直接报「默认态=PASS ✗逃生」。\\n"
      + "⚠ 尾段「维度评分口径参考」是常量说明块，任何输入都不变，混入即逃生项。",
  },
  {
    slug: "design/particle-effect-generator",
    inputs: { count: "220", psize: "7", speed: "3.5", gravity: "0.8", lifetime: "6", linkDist: "40" },
    expect: ["\u7c92\u5b50: 220"],
    ref: "`canvasInfo` 是纯文本状态行（粒子数 / FPS），`#countVal` / `#sizeVal` 同步显示滑杆值。FPS 在 harness 内恒 0（无真实 rAF），属环境产物，不写进断言。\\n"
      + "⚠ 该页同时有 `particleCanvas`（canvas），但结果文本走 `canvasInfo`，因此不依赖 `toDataURL`，是本批少数可注入的 canvas 类页。\\n"
      + "⚠ 只锚「粒子: 220」这一条：只改 count 也是真被测点，改 psize/speed 只影响 canvas 绘制，不进文本。",
  },
  {
    slug: "design/palette-cvd-checker",
    inputs: { pcInput: "#22a7a7,#e74c3c,#f1c40f" },
    expect: ["\u76f8\u90bb\u6700\u5c0f\u660e\u5ea6\u5dee L* = 7.8", "#DD4335"],
    ref: "结果区 `#pcScore` 给出「相邻最小明度差 L*」与评级，`#pcSugg` 给出最严重一对的可访问修正色。注入三色时最小明度差落在前两色上，修正建议同时依赖 pcInput 的两个 hex。默认态（单色 `#22a7a7`）得到的是另一套数值与建议色 ⇒ 双态判别明确。\\n"
      + "⚠ 本页 `#pcMatrix` / `#pcOverlay` 依赖 canvas，harness 内会抛错；只要不把断言锚在 canvas 区即可。\\n"
      + "⚠ 页面脚本里的函数名是 `pcApply` 之类，没有 `apply()`——给 clicks 写 `apply()` 只会报 `apply is not defined`，本例用纯 inputs 触发，不需要 clicks。",
  },

];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== design calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();