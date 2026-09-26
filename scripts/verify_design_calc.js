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