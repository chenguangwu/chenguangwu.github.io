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
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "100", base: "" },
    expect: ["⚠ 请输入大于 0 的基准视口尺寸（px）。"],
    ref: "基准视口清空：修复前 `num()` 把空串转成 0 后静默回落 1920，输出 5.2083vw；修复后应直接提示并拒绝按默认视口换算。默认态（100/1920）不含该提示串 ⇒ 判别明确。",
  },
  {
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "-100", base: "1920" },
    expect: ["⚠ 请输入不小于 0 的数值。"],
    ref: "负值输入：修复前 -100 → -5.2083vw 原样透传；修复后应提示数值须 ≥0 且不输出负换算结果。默认 100 不含该提示 ⇒ 判别明确。",
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
    inputs: { baseSize: "20", ratio: "1.125" },
    expect: ["h5 22.5px"],
    ref: "等比字阶 size_i = base × ratio^i：20 × 1.125¹ = 22.5（h6 为基准 20，h5 为 22.5）。"
       + "默认 baseSize=16 / ratio=1.200 ⇒ h5=19.2px；旧用例注入的正是这两个默认值，判别器回退后仍 PASS ⇒ 已改注入非默认值。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "16.5", ratio: "1.2" },
    expect: ["⚠ 基准字号需为 8–48 之间的整数。"],
    ref: "非整数基准：修复前 parseInt 静默截成 16 后照常生成；修复后应显式提示并清空结果。默认基数 16 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "100", ratio: "1.25" },
    expect: ["--h6-size: 48px"],
    ref: "上界夹取：修复前 base=100 原样生成 h6=100px；修复后按 BASE_MAX=48 夹取并回写输入框 ⇒ 首档 CSS 变量为 48px。默认 16/1.25 得 16px ⇒ 判别明确。",
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
    slug: "design/color-temperature-converter",
    inputs: { temp: "3200" },
    expect: ["#ffb87b", "255,184,123"],
    ref: "去默认化（原 temp=5500 与默认相同）：Tanner Helland 近似式 k = 3200/100 = 32 ≤ 66 分支 ——"
      + " R = 255；G = 99.4708·ln(32) − 161.1196 = 183.62 → 184；B = 138.5177·ln(22) − 305.0448 = 123.11 → 123"
      + " ⇒ #ffb87b / RGB(255,184,123)（暖白/日出）。默认 5500K 得 #ffedde / 255,237,222",
  },
  {
    slug: "design/color-temperature-converter",
    inputs: { temp: "-2000" },
    expect: ["⚠ 请输入 1000–40000K 之间的有效色温。"],
    ref: "负色温：修复前 k=-20 走对数分支得到 NaN 通道并生成 `#NaNNaNNaN` 非法 HEX；修复后应提示范围并清空预览/RGB。默认 5500K 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#0EA5E9", steps: "4" },
    expect: ["#cfedfb"],
    ref: "去默认化（原 hex=#6366F1/steps=5 全与默认相同）：mix(c,t,r) = round(c+(t−c)·r)，基色 rgb(14,165,233)、"
      + "steps=4 ⇒ 最浅 tint f = 4/5 = 0.8：R = round(14+241×0.8) = 207、G = round(165+90×0.8) = 237、"
      + "B = round(233+22×0.8) = 251 → #cfedfb。默认 #6366F1/5 得 #e5e6fd",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#6366F1", steps: "" },
    expect: ["⚠️ 请输入 1–20 之间的整数档数。"],
    ref: "清空档数：修复前空串经 `parseFloat||0` → 1 档静默生成；修复后应显式提示并拒绝生成。默认 5 档不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#6366F1", steps: "1000" },
    expect: ["⚠️ 档数超过上限 20，已按 20 档生成。"],
    ref: "超大档数：修复前 1000 档会渲染 2001 张卡片；修复后按上限 20 夹取并回写输入框，同时给出上限提示。默认 5 档不含该提示 ⇒ 判别明确。",
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
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "24", aperture: "8", distance: "5" },
    expect: ["1.63m ~ ∞"],
    ref: "对焦距离 5000mm 超过超焦距 H = 24²/(8×0.03) = 2400mm：修复前把近点也误判为无穷，输出 `Infinitym ~ ∞`；"
      + "修复后近点 = H·s/(H+(s−f)) = 2400×5000/(2400+5000−24) = 1626.9mm → 1.63m，仅远点为 ∞。默认 50mm/f1.8/2m 得 1.92m ~ 2.08m ⇒ 判别明确。",
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
    slug: "design/focal-length-equivalent",
    inputs: { focal: "0", fromSensor: "fullframe", toSensor: "aps-c" },
    expect: ["⚠ 请输入 1–2000mm 之间的有效焦距。"],
    ref: "零焦距：修复前 `+value||0` 得到 0，输出 `0.0mm` 等效与 `180.0° × 180.0°` 视角（FOV 退化、条宽 NaN）；"
      + "修复后应显式提示并清空结果条。默认 50mm 不含该提示 ⇒ 判别明确。",
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
    inputs: { aperture: "1.4", shutter: "1/2", iso: "100" },
    clicks: ["calc();"],
    expect: ["f/2 1s ISO 100"],
    ref: "三个 select 按 option 文本注入（`apertures[0]=1.4`、`1/2`、`ISO 100`）⇒ 等效组合区首张卡为放大一档光圈 `f/2` + 放慢一档快门 `1s` + `ISO 100` 连排。"
       + "⚠ 默认态（f/4、1/60、ISO 200）首张卡是 `f/2.8 1/125 ISO 200` ⇒ 不命中，判别成立。",
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
    expect: ["font-size:20px;font-weight:600;border-radius:14px"],
    ref: "独立复算：字号 20px、圆角 14px 被写进生成的 CSS（默认 12px/12px）。⚠ 原 expect TOOLBOX 为徽标文字输入回显（零判别力）；本页可见产物都由输入拼出，故锚「随参数变化的 CSS 片段」而非文字。默认态 font-size:12px;font-weight:600;border-radius:12px，不命中 ⇒ 无逃生（已双态实测）。"
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
    slug: "design/pattern-generator",
    inputs: { size: "20", color1: "#22c55e", color2: "#0f172a" },
    clicks: ["currentType='diamonds';generate();"],
    expect: ["conic-gradient(from 45deg, #0f172a 0deg 90deg, transparent 90deg 180deg, #0f172a 180deg 270deg, transparent 270deg 360deg)"],
    ref: "菱形图案：修复前 `diamonds` 与 `triangles` 共用同一条 45° 双层 linear-gradient 串（输出完全相同）；"
      + "修复后 `diamonds` 走 conic-gradient 四象限交替（from 45deg 形成菱形平铺）。默认 triangles 不含 `conic-gradient` ⇒ 判别明确。",
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
    slug: "design/skeleton-loader",
    inputs: { radius: "0", duration: "2.2", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: ["border-radius: 0px;"],
    ref: "圆角 0：修复前 `parseInt(value)||4` 把合法的 0 改成 4；修复后应保留 0 ⇒ CSS 输出 `border-radius: 0px;`。默认圆角 4px ⇒ 判别明确。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "10", duration: "0", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: ["skelLoading 0s ease infinite"],
    ref: "时长 0：修复前 `parseFloat(value)||1.4` 把合法的 0 静默改成 1.4s；修复后应保留 0 ⇒ CSS 输出 `animation: skelLoading 0s ease infinite`（可作静态骨架）。默认 1.4s ⇒ 判别明确。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "10", duration: "-3", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: ["⚠ 动画时长需为不小于 0 的数字（秒）。"],
    ref: "负时长：修复前 -3 原样拼成非法的 `animation: skelLoading -3s ease infinite`；修复后应显式提示并拒绝生成。默认 1.4s 不含该提示 ⇒ 判别明确。",
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
    expect: ["border-radius: 14px"],
    ref: "独立复算：圆角 14px 写进生成的 .toast CSS（默认 8px）。⚠ 原 expect TOOLBOX-OK 为提示文字输入回显（零判别力）。默认态 border-radius: 8px，不命中 ⇒ 无逃生（已双态实测）。"
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
    expect: ["D - E - F - G - A - Bb - C"],
    ref: "自然小调按半音阶逐级推导（D → E F G A Bb C，第 6 音按降号记谱写 Bb）。同页 `#notesDisplay` 还输出 `调号` 与 `关系小调`，但结果串里只有音符序列随 root/scale 变化，故取其作为锚。",
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
    expect: ["180.00 MB 单张大小", "此卡可存储约 661 张照片"],
    ref: "十进制容量口径：45MP×16bit×TIFF(×2) = 180,000,000 B = 180.00 MB；"
      + "128 GB 卡 = 128×10^9 B，30 分钟 4K 视频按 300 MB/分钟 = 9×10^9 B，"
      + "(128−9)×10^9 ÷ 180×10^6 = 661.1 ⇒ 661 张（旧实现用 1024^3 且不扣视频 ⇒ 763 张）。\n"
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
    // 遮蔽回归：本页复制函数已改名 copySwatch(btn, text)，避免被 js/common.js 的全局 copyText(text) 覆盖。
    // 断言锚在「传给剪贴板的文本」本身：旧实现会把按钮元素当 text 传下去，得到 [object HTMLButtonElement]。
    slug: "design/color-picker",
    inputs: { hexInput: "#123456" },
    clicks: ["var __c=ToolBox.copyText;ToolBox.copyText=function(t){document.getElementById('hexInput').value='COPIED:'+t;};copySwatch({textContent:'复制'},'#123456');ToolBox.copyText=__c;"],
    expect: ["COPIED:#123456"],
    ref: "copySwatch(btn, text) 调用 ToolBox.copyText(text, …)：点击复制按钮时应把该色值原样交给剪贴板。用例把 ToolBox.copyText 换成采集器（两种桩模式下都成立），旧实现被全局 copyText 覆盖后第一个实参是按钮对象 ⇒ 采集到 [object HTMLButtonElement]，不命中。",
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
  {
    slug: "design/svg-minifier",
    checkIds: ["optComment", "optWhitespace"],
    clicks: ["var e=document.getElementById('svgInput');e.value='<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\"><!-- hello --><rect   width=\"100\"   height=\"100\" /></svg>';generate();"],
    expect: ["原始: 122 字节 → 压缩后: 104 字节 (节省 14.8% )"],
    ref: "结果走 `#stat` 文本行「原始 N 字节 → 压缩后 M 字节 (节省 R%)」，注入带注释与多余空白的 SVG 后四项「移除注释/移除空白」生效 ⇒ 字节数真实下降。\\n"
      + "⚠ harness 里 checkbox 恒未勾选，必须显式写 `checkIds` 声明 optComment/optWhitespace，否则四个开关全关、压缩量恒 0.0%（等于默认态）。\\n"
      + "⚠ 本页没有 `setSVGOpts` / `generateMinified`，只有 `generate()`；写错函数名会整条 clicks 抛错、回落到默认态。",
  },
  {
    slug: "design/pixel-art-generator",
    inputs: { gs: "12" },
    expect: ["12×12 网格尺寸"],
    ref: "状态行 `#gridInfo` 是纯文本（网格尺寸 / 当前颜色），只依赖 gs 滑杆；画布与字符画预览属 canvas 产物，不进断言。默认态是另一档网格尺寸 ⇒ 双态判别明确。",
  },
  {
    slug: "design/color-palette",
    inputs: { hexInput: "#e11d48" },
    expect: ["主色 #E21D48 rgb(226, 29, 72) hsl(347, 77%, 50%)"],
    ref: "结果区 `#palette` 在注入 hex 后先给出主色的 hex/rgb/hsl 三连，随后才是「配色1」等派生色 ⇒ 锚点落在推导值上，不受派生段常量干扰。默认态主色为 #61D172 ⇒ 判别明确。",
  },
  {
    slug: "design/neomorphism-generator",
    inputs: { distance: "18", blur: "30", intensity: "35", radius: "44", bgColor: "#1f2937" },
    expect: [".neomorphism { background-color: #1f2937; border-radius: 44px; box-shadow: 18px 18px 30px rgba(10, 20, 34, 0.35), -18px -18px 30px rgba(52, 62, 76, 0.35); }"],
    ref: "输出整行由 bgColor/radius/distance/blur/intensity 共同决定，必须整行锚；只锚 `.neomorphism` 会让默认态（#e0e5ec / 20px）也命中 ⇒ 报「默认态=PASS ✗逃生」。注入瞬间 `adjustColor` 会抛错（依赖未注入的取色字段），但 `#cssOutput` 已先写入。",
  },
  {
    slug: "design/border-radius-generator",
    clicks: ["setUniform('28');generate();"],
    expect: ["border-radius: 28px;"],
    ref: "纯 CSS 拼串生成器：注入角度后 `#cssOutput` 输出对应的 border-radius 单行。默认态为 `border-radius: 16px;`（uniform=16）⇒ 判别明确。\\n"
      + "⚠ `copyResult` 在 harness 内报 `Cannot read properties of undefined (reading 'then')`（无 navigator.clipboard），属环境产物，不影响 `#cssOutput` 已写入。",
  },
  {
    slug: "design/border-radius-generator",
    clicks: ["document.getElementById('tl').value='40';document.getElementById('tr').value='8';generate();"],
    expect: ["border-radius: 40px 8px 16px 16px;"],
    ref: "同一页的第二条路径：分别改 tl/tr 两个角 ⇒ 输出四值简写，br/bl 沿用默认 16。与 uniform 分支互补，覆盖「分别调角」函数。默认态同样不命中该串。",
  },
  {
    slug: "design/dot-pattern",
    inputs: { bgColor: "#0f172a", dotColor: "#22d3ee", dotSize: "14", spacing: "48", arrangement: "square" },
    expect: ["background-image: radial-gradient(#22d3ee 7px, transparent 8px); background-size: 48px 48px;"],
    ref: "按 dotSize/2 与 spacing 拼出渐变与背景尺寸，三处都吃注入值。默认态是另一组 dotColor/spacing ⇒ 判别明确。\\n"
      + "⚠ arrangement 只接受 square/offset/gradient，传 `hex` 之类的非法档位会静默只输出 `background-color` 一条 ⇒ 注入等于默认。",
  },
  {
    slug: "design/dot-pattern",
    inputs: { bgColor: "#0f172a", dotColor: "#22d3ee", dotSize: "14", spacing: "48", arrangement: "offset" },
    expect: ["background-position: 0 0, 24px 24px;"],
    ref: "offset 档位独有的第二条渐变与背景位移（spacing/2），锚点在该页只有 offset 分支才会出现 ⇒ 强判别。默认态为 square 分支，不命中。",
  },
  {
    slug: "design/css-grid-generator",
    inputs: { cols: "4", coltype: "repeat", containerW: "1200", gap: "24" },
    expect: ["grid-template-columns: repeat(4, 1fr); gap: 24px; max-width: 1200px;"],
    ref: "结果区 `#result` 同时给出统计行与完整 CSS，锚点落在 CSS 代码段的三项注入值上（列数 / 间距 / 容器宽度）。默认态是 3 列 / 16px / 960px ⇒ 判别明确。\\n"
      + "⚠ 该页 `fmtMoney` / `dataGrid` 在 harness 内会抛错（`rows is not iterable`），但 `#result` 已先写入，不影响断言。",
  },
  {
    slug: "design/progress-bar-generator",
    inputs: { percent: "72", color1: "#f43f5e", color2: "#facc15", height: "28", radius: "14" },
    expect: [".progress-bar { width: 72%; height: 100%; background: #f43f5e; border-radius: 14px; }"],
    ref: "进度条 CSS 由百分比 / 主色 / 圆角共同决定，锚点覆盖三项注入值。默认态为 60% / #667eea / 10px ⇒ 判别明确。\\n"
      + "⚠ 渐变与条纹开关（`gradient` / `striped` / `animated`）虽在页面内，但注入后本条 CSS 未变化；本例只锚确定生效的量，不写开关相关断言。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "18", ratio: "1.618" },
    expect: ["--h1-size: 199.6px; --h2-size: 123.4px;"],
    ref: "字号阶梯是 baseSize × ratio^n 的连续推导，锚点取 h1/h2 两档（18×1.618≈29.1 → h1≈47.1 之外的中间档），能同时兜住 baseSize 与 ratio 两个输入。默认态 baseSize=16/ratio=1.25 得到的是 22.1px / 20.7px ⇒ 判别明确。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { baseSize: "12", ratio: "1.5", levels: "7" },
    expect: ["--space-3: 40.5px; --space-4: 60.8px;"],
    ref: "间距阶梯同为 baseSize × ratio^n，levels 决定条数。本例注入 7 档 ⇒ 末档 space-6=136.7px，注入值与默认态（10 档、4px 起）完全错开 ⇒ 判别明确。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { baseSize: "12", ratio: "1.5", levels: "4" },
    expect: ["--space-0: 12px; --space-1: 18px; --space-2: 27px; --space-3: 40.5px;"],
    ref: "同一页的第二条路径：levels 降到 4 ⇒ 只输出 space-0 ~ space-3 四档，锚点整串覆盖四档推导值。默认态 10 档且首档为 4px ⇒ 强判别，专门覆盖 levels 输入。",
  },
  {
    slug: "design/glassmorphism-generator",
    inputs: { bgColor: "#0f172a", blur: "18", saturate: "160", radius: "24", borderOp: "0.4", shadow: "30" },
    expect: [".glass { background: rgba(15, 23, 42, 0.2); backdrop-filter: blur(18px) saturate(160%);"],
    ref: "毛玻璃样式串由背景色 / 模糊 / 饱和度 / 圆角共同决定，锚点整段覆盖四项。默认态为 #ffffff / blur(10px) / saturate(100%) / 16px ⇒ 判别明确。\\n"
      + "⚠ `opacity` 项注入被页面忽略（回落到常量 0.2），本例不注入该项；锚点以 dump 实测值为准，改注入前先重跑 dump。",
  },
  {
    slug: "design/shadow-generator",
    inputs: { offsetX: "6", offsetY: "10", blur: "24", spread: "-4", color: "#f43f5e" },
    expect: ["box-shadow: 6px 10px 24px -4px #f43f5e;"],
    ref: "输出区 `#code` 首行是四值 + 颜色的 box-shadow 简写，五项注入值全部落在这一个串里。默认态为 `0px 10px 20px -5px #667eea;` ⇒ 判别明确。\\n"
      + "⚠ `inset` 勾选后首行串不变（inset 走另一渲染路径），本例不写 inset 断言，避免写成假用例。",
  },
  {
    slug: "design/button-generator",
    inputs: { bgColor: "#f43f5e", textColor: "#fff", borderColor: "#9f1239", borderW: "2", radius: "12", padX: "28", padY: "16", fontSize: "18", shX: "3", shY: "5", shBlur: "10" },
    expect: [".btn-custom { padding: 16px 28px; background: #f43f5e; color: #fff; border: 2px solid #9f1239; border-radius: 12px; font-size: 18px;"],
    ref: "按钮 CSS 的 padding/背景/文字色/边框/圆角/字号六项全部吃注入值，锚点整段覆盖；默认态是 10px 20px / #667eea / 14px ⇒ 判别明确。\\n"
      + "⚠ 页面另有 `#btnText`（按钮文案）与阴影三件套，本例不注入文案（文案只进预览区、不进 `#cssOutput`），阴影三项已注入但落在 `:hover` 段，故只锚基础段。",
  },
  {
    slug: "design/toast-generator",
    inputs: { radius: "16" },
    expect: [".toast { padding: 14px 20px; border-radius: 16px;"],
    ref: "提示条圆角直接进 `#cssOutput` 首行，锚点与默认值（8px）错开 ⇒ 判别明确。背景色与文案在 success 档位下被档位样式固定（注入不生效），本例只锚确实受控的圆角。",
  },
  {
    slug: "design/color-palette-generator",
    inputs: { baseColor: "#0ea5e9" },
    expect: ["--color-1: #064460; --color-2: #0A76A9; --color-3: #0EA9F1;"],
    ref: " monochromatic 派生算法的确定性输出：注入基色后前三条色阶是推导值，与默认基色（#1E3A8A 系）推导出的 `--color-1: #0C1A5A` 完全不同 ⇒ 强判别。\n"
      + "⚠ 页面另有 `generateMonochromatic/Complementary/Analogous` 三个函数在 harness 内报 `Cannot read properties of null (reading 'r')`（读不到基础色的 rgb 分量），属 Harness 桩盲区；但 `#cssOutput` 已由主路径写入且不含 NaN，不影响本例。\n"
      + "⚠ 不锚 `--color-4/5`：它们依赖同样受污染的派生链，锚前三档已足够锁定被测点。",
  },
  {
    slug: "design/color-palette-generator",
    inputs: { baseColor: "#808080" },
    expect: ["黑底 5.32:1 AA", "白底 3.95:1 ✗"],
    ref: "色块文字对比度：WCAG 相对亮度 —— #808080 线性化后 L = 0.2159，黑字对比度 = (0.2159+0.05)/0.05 = 5.32:1、"
      + "白字 = 1.05/0.2659 = 3.95:1 ⇒ 应按 WCAG 选黑字并标注 5.32:1 AA。修复前用亮度阈值 YIQ=128 判 `>128` 为假而选白字（3.95:1 未达 AA）。"
      + "默认基色 #667eea 的派生色不含该串 ⇒ 判别明确。",
  },
  {
    slug: "design/generator-6",
    inputs: { cnt: "6" },
    expect: [".shadow-6 { box-shadow:"],
    ref: "随机阴影生成器。`#res` 每条的 `box-shadow` 数值是随机的，本例只锚第 6 条的**结构前缀** `.shadow-6 { box-shadow:`，该串只在 cnt≥6 时出现 ⇒ 条数型判别。\n"
      + "默认态 cnt=5 ⇒ 只有 `.shadow-1`~`.shadow-5`，必然不命中。\n"
      + "⚠ 严禁把随机数值写进 expect，否则每次跑都不同（flaky）。",
  },
  {
    slug: "design/generator-7",
    inputs: { cnt: "7" },
    expect: [".border-7 { border:"],
    ref: "随机边框生成器，锚第 7 条的结构前缀 `.border-7 { border:`。边框样式枚举（solid/dashed/dotted/...）与颜色是随机的，只取结构前缀规避 flaky。默认态 5 条 ⇒ 不命中。",
  },
  {
    slug: "design/generator-8",
    inputs: { cnt: "6" },
    expect: ["配置参数 #6"],
    ref: "二维码定制方案生成器。每条方案内部含随机示例链接与随机色值，只锚第 6 条的序号标签 `配置参数 #6`（默认态 5 条 ⇒ 不命中）。\n"
      + "⚠ `errs` 里的 `randItem: ... 'length'` 是 harness 内随机数组取值的桩盲区，不阻断 `#res` 写入。",
  },
  {
    slug: "design/generator-9",
    inputs: { cnt: "6" },
    expect: ["6. EAN-13 条形码"],
    ref: "EAN-13 生成器。12 位随机码 + 确定校验位 ⇒ 数值部分不可锚，只锚第 6 条的序号与标题 `6. EAN-13 条形码`（默认态 5 条 ⇒ 不命中）。校验位算法本身的正确性由页面其它验证路径覆盖，本例只锁「条数随 cnt 增长」。\n"
      + "本页是本批唯一 `errs` 为空的 generator 页（gen 不依赖 `randItem`）。",
  },
  {
    slug: "design/generator-11",
    inputs: { cnt: "6" },
    expect: ["6. 波浪纹理"],
    ref: "纹理生成器。纹理类型序列固定（圆点/条纹/网格/棋盘/斜线/波浪），注入 cnt=6 时第 6 条为波浪纹理；随机色值不进 expect。默认态 5 条 ⇒ 不命中。",
  },
  {
    slug: "design/generator-12",
    inputs: { cnt: "6" },
    expect: ["6. square 粒子方案"],
    ref: "粒子特效生成器。形状枚举按序取（circle/square/...），第 6 条落到 square；粒子数量/速度/色值随机，不进 expect。默认态 5 条 ⇒ 不命中。",
  },
  {
    slug: "design/favicon-generator",
    inputs: { textInput: "AB", fgColor: "#f43f5e", bgColor: "#0f172a", fontSize: "22", fontWeight: "700" },
    expect: [ "#0f172a" ],
    ref: "浏览器地址栏 favicon 预览 `#browserFavicon` 直接渲染 `textInput` 的首字母组合：默认文本是 `F`（默认文字 'Favicon'），注入 `AB` 后变 `AB` ⇒ 默认态必然不命中。\n ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。"
      + "⚠ 这是「输入 → 结果区文本渲染」型锚，不是纯输入框回显：被测点是**渲染管线**而非回显本身，页面默认值与注入值明确错开。\n"
      + "⚠ `errs` 里的 `canvas.toBlob is not a function` / `draw: ... 'getC...` 是 harness 无 canvas 2d 上下文的产物，不阻断 `#browserFavicon` 写入；`#sizesPreview` 是常量（16×16px…256×256px），不锚。",
  },
  {
    slug: "design/favicon-generator",
    inputs: { textInput: "72" },
    expect: ["72"],
    ref: "覆盖「注入值为纯数字」的分支（首例测字母）。默认态文本 `F` 不命中，注入 `72` 后 `#browserFavicon` 渲染为 `72`。\n"
      + "⚠ 本页只有一个文本结果通道（`#browserFavicon`），因此只拆两例（字母 / 数字），刻意不重复同一形态。",
  },

  // ── BATCH157：CSS 生成类（走 clicks 改层参数）＋ 色板搜索类（空态反用）────
  {
    slug: "design/shadow-generator-advanced",
    clicks: ["layers[0].x=20;layers[0].blur=40;layers[0].alpha=0.5;generate();"],
    expect: ["20px 4px 40px -4px rgba(0,0,0,0.5)"],
    ref: "顶层 var `layers` 每项有 x/y/blur/spread/color/alpha，层内输入框无 id ⇒ 只能走 clicks 直接改字段再 generate()。注入后首层为 x=20/blur=40/alpha=0.5（默认 0/20/0.25），锚首层完整串而非单个数字，避免只改一个字段的弱断言。",
  },
  {
    slug: "design/material-color",
    inputs: { searchInput: "zzzz" },
    expect: ["未找到匹配颜色"],
    ref: "顺序保持型筛选 ⇒ 注入命中词（如 `red`）只会渲染默认态的子集、任何锚都成默认态子串（逃生项），故改走反用：注入无匹配词 `zzzz` ⇒ 落空态。⚠ 该空态安全的前提是零参 `render()` 的 filter 默认为空串、渲染全量、不复现空态；若页面兜底改成带 filter 调用需重评。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "design/tailwind-colors",
    inputs: { searchInput: "zzzz" },
    expect: ["未找到匹配颜色"],
    ref: "与 material-color 同模板同渲染函数，空态成因与安全性一致；两例同锚但落在不同页，可互相兜住模板改动。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },

  // ── §7.4 零用例加固：design 确定性页（注入非默认 + harness 实测锚）──
  {
    slug: "design/tester-assessor",
    inputs: {
      totalTasks: "6", successTasks: "5", avgTime: "150", expectedTime: "100",
      helpCount: "1", satisfaction: "4",
      sus0: "4", sus1: "4", sus2: "4", sus3: "4", sus4: "4",
      sus5: "4", sus6: "4", sus7: "4", sus8: "4", sus9: "4"
    },
    expect: ["83% (5/6)", "1.50x (150s/100s)", "4/7"],
    ref: "注入非默认(默认 5/4/120/90/2/5)：任务完成率 5/6 = 83%、完成时间比 150/100 = 1.50x、用户满意度 4/7；SUS 十题全选 4 ⇒ 偶数索引(正表述) val−1=3×5=15、奇数索引(反表述) 5−val=1×5=5 ⇒ susSum=20 ⇒ SUS=50.0。⚠ 两条排雷：① harness 判定是『expect 任一子串命中即通过』，而判别器是**一次性把 inputs 全部换回页面默认**；sus0..sus9 由 JS 动态渲染、不在静态 HTML ⇒ 无法回退 ⇒ 失败态 = 默认绩效 + 注入 SUS，实测其任务绩效综合也恰为 73、综合评分也恰为 59 ⇒ **SUS 类锚与综合评分锚在两态相同，一律不可用**，只能锚依赖绩效输入的明细串；② errors 键改 2/1 时错误率评分四舍五入后综合不变 ⇒ 对输出无判别力，不予注入。",
  },
  {
    slug: "design/ripple-effect",
    inputs: { duration: "1.5", size: "320" },
    expect: ["animation: rippleAnim 1.5s ease-out"],
    ref: "注入非默认(默认 duration=0.8)：生成的 CSS 关键帧动画时长取注入值 ⇒ 'animation: rippleAnim 1.5s ease-out'。默认态为 0.8s，本锚不命中。size 不参与 CSS 输出，仅作陪注入。",
  },
  {
    slug: "design/spinner-generator",
    inputs: { size: "64", speed: "2" },
    expect: ["width: 64px", "animation: spinGen 2s linear infinite"],
    ref: "注入非默认(默认 size=40/speed=1)： spinner 边长取注入的 64px、旋转周期取注入的 2s ⇒ 生成 CSS 含 'width: 64px' 与 'animation: spinGen 2s linear infinite'。默认态为 40px/1s，两条均不命中。",
  },
  {
    slug: "design/flexbox-generator",
    inputs: { gap: "20" },
    expect: ["gap: 20px;"],
    ref: "注入 gap=20（默认 12）⇒ 生成的 CSS 与预览内联 style 里都出现 `gap: 20px;`。expect 带 `gap: ` 前缀与 px 单位，而输入框 value 只是裸值 `20` ⇒ 不与输入回显冲突。默认态输出 `gap: 12px`。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20'><text x='0' y='15'>probeTB2026</text></svg>" },
    clicks: ["generate()"],
    expect: ["probeTB2026"],
    ref: "注入带唯一文本标记 probeTB2026 的 SVG。generate() 对输入做安全清洗后写入 preview.innerHTML，文本节点 probeTB2026 进入输出。注意：采集器会去标签，故标记必须置于 <text> 内容而非 id 属性（属性会被整块吞掉）。默认态 svgInput 为空 ⇒ 输出『请输入 SVG 代码』，不出现 probeTB2026。纯前端无随机。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg xmlns='http://www.w3.org/2000/svg' onload='alert(1)'><script>alert(2)</script><text x='0' y='15'>SVGXSS2026</text></svg>" },
    clicks: ["generate()"],
    expect: ["已移除 SVG 中的不安全脚本或事件属性", "SVGXSS2026"],
    ref: "安全修复判别：注入含 onload 与 <script> 的 SVG。清洗后仍预览 SVGXSS2026，并额外输出『已移除 SVG 中的不安全脚本或事件属性』提示；旧实现直接 innerHTML 原文、无该提示 ⇒ 不命中。默认态无该提示。",
  },
  {
    slug: "design/font-preview",
    inputs: { fpText: "ZZPREVZZ" },
    expect: ["ZZPREVZZ"],
    ref: "注入唯一预览文字 ZZPREVZZ。fpText 的 input 监听器更新 state.text 后 render()，将 ZZPREVZZ 渲染进每个可见字体的预览区（escHtml 转义后仍为文本，去标签后保留）。默认态 fpText=『永和九年岁在癸丑』，不出现 ZZPREVZZ。render 纯本地 fonts 对象、不触网，确定性强。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  // ── 零用例收敛（2026-10-09）：design 29 页中仅本页可收敛 ──
  {
    slug: "design/iso-noise-reference",
    inputs: { sensor: "medium", light: "low", camera: "canon_r5", isoRange: "51200" },
    expect: ["中画幅", "佳能 R5 全画幅 · 45MP", "8K视频", "几乎不可见，画质纯净"],
    ref: "注入 sensor=medium（默认 phone）/ light=low（默认 bright）/ camera=canon_r5（默认 sony_a7iv）。三条均经页面 change 监听器 → onISOChange → renderISO 生效，独立复算依据页面内置噪声基准表：medium 画幅纯净上限 6400、可用上限 25600；弱光档等效 ISO = 6400×1.3 = 8320。判别锚（均与默认态零撞车）：①『中画幅』（默认渲染『手机 (1/1.3 吋)』）②『佳能 R5 全画幅 · 45MP』（默认 sony_a7iv ⇒『索尼 A7 IV 全画幅 · 33MP』）③『8K视频』（佳能 R5 独有优点，默认 A7 IV 为『对焦优秀、视频强、实时眼部对焦』）④『几乎不可见，画质纯净』（ISO 6400 在 medium+low 下评『优秀』，默认 phone+bright 评『较重』并输出『噪点明显，需要后期降噪』）。⚠️ 不用『原生ISO 100-51200』——默认 A7 IV 同为 100-51200，属逃生串（判别器已实测报出）。纯本地查表，无随机、无时间依赖。",
  },
  {
    slug: "design/cvd-safe-palette",
    inputs: { csMode: "sequential", csStrategy: "lightness" },
    expect: ["sequential"],
    ref: "⚠ 下拉值回显（结构性不可修）：csMode=sequential / csStrategy=lightness 注入后，模式与策略标签确实变化，但实测色板（#A2828B → #1B179C → …）、ΔE、对比度表在默认 qualitative/auto 下**逐字节相同** —— 该页色板由固定种子搜索生成、不受模式/策略影响 ⇒ 任何色板数值锚都会在默认态命中（已双态实测 A/B 一致）。能区分的只有 `sequential`/`lightness` 两个下拉回显本身，故维持原断言。",
  },
  {
    "slug": "design/avatar-generator",
    "inputs": {
      "seed": "abc123测试",
      "size": "42",
      "radius": "42",
      "c1": "abc123测试",
      "c2": "abc123测试",
      "avatarStyle": "block"
    },
    "expect": [
      "abc123测试\n42\n42\nabc123测试\nabc123测试\nblock\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"seed\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\",\"c1\":\"abc123测试\",\"c2\":\"abc123测试\",\"avatarStyle\":\"block\"}，输出区含「abc123测试\n42\n42\nabc123测试\nabc123测试\nblock\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/analysis-64",
    "inputs": {
      "p1a": "42",
      "p1b": "42",
      "p2a": "42",
      "p2b": "42",
      "p3a": "42",
      "p3b": "42",
      "p4a": "42",
      "p4b": "42",
      "p5a": "42",
      "p5b": "42",
      "scale": "5",
      "bias": "price"
    },
    "expect": [
      "0 功能完整度 20% 5.0 5.0 +0.0 +0.0 使用体验 20% 5.0 5.0 +0.0 +0.0 品牌信任 10% 5.0 5.0 +0.0 +0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"p1a\":\"42\",\"p1b\":\"42\",\"p2a\":\"42\",\"p2b\":\"42\",\"p3a\":\"42\",\"p3b\":\"42\",\"p4a\":\"42\",\"p4b\":\"42\",\"p5a\":\"42\",\"p5b\":\"42\",\"scale\":\"5\",\"bias\":\"price\"}，输出区含「0 功能完整度 20% 5.0 5.0 +0.0 +0.0 使用体验 20% 5…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/aztec-code",
    "inputs": {
      "text": "abc123测试",
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/badge-generator",
    "inputs": {
      "text": "abc123测试",
      "bgColor": "abc123测试",
      "textColor": "abc123测试",
      "radius": "42",
      "fontSize": "42",
      "cssOutput": "1\n2\n3",
      "badgeStyle": "outline"
    },
    "expect": [
      "ckground:transparent;color:abc123测试;border:1px solid abc123测试; }"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"radius\":\"42\",\"fontSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"badgeStyle\":\"outline\"}，输出区含「ckground:transparent;color:abc123测试;bord…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/base64-to-image",
    "inputs": {
      "b64Input": "1\n2\n3"
    },
    "expect": [
      "1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"b64Input\":\"1\\n2\\n3\"}，输出区含「1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/blueprint-grid",
    "inputs": {
      "bgColor": "abc123测试",
      "majorColor": "abc123测试",
      "minorColor": "abc123测试",
      "majorSize": "42",
      "minorSize": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "nd-size: 42px 42px, 42px 42px, 42px 42px, 42px 42px;"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"majorColor\":\"abc123测试\",\"minorColor\":\"abc123测试\",\"majorSize\":\"42\",\"minorSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「nd-size: 42px 42px, 42px 42px, 42px 42px…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/border-radius-generator",
    "inputs": {
      "uniform": "42",
      "tl": "42",
      "tr": "42",
      "br": "42",
      "bl": "42",
      "cssOutput": "1\n2\n3",
      "unit": "%"
    },
    "expect": [
      "-radius: 42%;\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"uniform\":\"42\",\"tl\":\"42\",\"tr\":\"42\",\"br\":\"42\",\"bl\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"unit\":\"%\"}，输出区含「-radius: 42%;\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/button-generator",
    "inputs": {
      "bgColor": "abc123测试",
      "textColor": "abc123测试",
      "radius": "42",
      "padX": "42",
      "padY": "42",
      "borderColor": "abc123测试",
      "borderW": "42",
      "btnText": "abc123测试",
      "fontSize": "42",
      "shX": "42",
      "shY": "42",
      "shBlur": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\n42\nabc123测试\n42\nabc123测试\n42\n42\n42\n42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"radius\":\"42\",\"padX\":\"42\",\"padY\":\"42\",\"borderColor\":\"abc123测试\",\"borderW\":\"42\",\"btnText\":\"abc123测试\",\"fontSize\":\"42\",\"shX\":\"42\",\"shY\":\"42\",\"shBlur\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「abc123测试\nabc123测试\n42\n42\n42\nabc123测试\n42\na…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/breakpoint-queries",
    "inputs": {
      "cls": "abc123测试"
    },
    "expect": [
      "40px） */ abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cls\":\"abc123测试\"}，输出区含「40px） */ abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/card-generator",
    "inputs": {
      "bgColor": "abc123测试",
      "radius": "42",
      "shX": "42",
      "shY": "42",
      "shBlur": "42",
      "pad": "42",
      "borderColor": "abc123测试",
      "borderW": "42",
      "shadowColor": "abc123测试",
      "shadowOp": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "abc123测试\n42\n42\n42\n42\n42\nabc123测试\n42\nabc123测试\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"radius\":\"42\",\"shX\":\"42\",\"shY\":\"42\",\"shBlur\":\"42\",\"pad\":\"42\",\"borderColor\":\"abc123测试\",\"borderW\":\"42\",\"shadowColor\":\"abc123测试\",\"shadowOp\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「abc123测试\n42\n42\n42\n42\n42\nabc123测试\n42\nabc1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/checker",
    "inputs": {
      "fgColor": "abc123测试",
      "fgPicker": "abc123测试",
      "bgColor": "abc123测试",
      "bgPicker": "abc123测试"
    },
    "expect": [
      "ABC123测试\nABC123测试\n色值格式无效，请输入 #RRGGBB 或 rgb(r,g,b) 格式\nABC123测试\nABC123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fgColor\":\"abc123测试\",\"fgPicker\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgPicker\":\"abc123测试\"}，输出区含「ABC123测试\nABC123测试\n色值格式无效，请输入 #RRGGBB 或 r…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/checkerboard-generator",
    "inputs": {
      "color1": "abc123测试",
      "color2": "abc123测试",
      "size": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "ent 75%, abc123测试 75%, abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"size\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「ent 75%, abc123测试 75%, abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/color-shade-generator",
    "inputs": {
      "hex": "abc123测试",
      "steps": "42"
    },
    "expect": [
      "abc123测试\n明暗梯度 ⚠️ 请输入有效的 HEX 颜色（如 #6366F1）。\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"hex\":\"abc123测试\",\"steps\":\"42\"}，输出区含「abc123测试\n明暗梯度 ⚠️ 请输入有效的 HEX 颜色（如 #6366F1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/colorblind-simulator",
    "inputs": {
      "c1Color": "abc123测试",
      "c1Hex": "abc123测试",
      "c1R": "42",
      "c1G": "42",
      "c1B": "42",
      "c1Sev": "42",
      "c4Fg": "abc123测试",
      "c4FgHex": "abc123测试",
      "c4Bg": "abc123测试",
      "c4BgHex": "abc123测试",
      "c5Base": "abc123测试",
      "c5BaseHex": "abc123测试",
      "c5Count": "42",
      "c2Input": "1\n2\n3",
      "c4Size": "large",
      "c5Mode": "lightness"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\n42\n42\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\n42\n1 2 3\nlarge\nlightness"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c1Color\":\"abc123测试\",\"c1Hex\":\"abc123测试\",\"c1R\":\"42\",\"c1G\":\"42\",\"c1B\":\"42\",\"c1Sev\":\"42\",\"c4Fg\":\"abc123测试\",\"c4FgHex\":\"abc123测试\",\"c4Bg\":\"abc123测试\",\"c4BgHex\":\"abc123测试\",\"c5Base\":\"abc123测试\",\"c5BaseHex\":\"abc123测试\",\"c5Count\":\"42\",\"c2Input\":\"1\\n2\\n3\",\"c4Size\":\"large\",\"c5Mode\":\"lightness\"}，输出区含「abc123测试\nabc123测试\n42\n42\n42\n42\nabc123测试\na…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/contrast-checker",
    "inputs": {
      "fgColor": "abc123测试",
      "fgHex": "abc123测试",
      "bgColor": "abc123测试",
      "bgHex": "abc123测试"
    },
    "expect": [
      "灰背景 暖色背景\nabc123测试\nabc123测试\n1.00\n不达标"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fgColor\":\"abc123测试\",\"fgHex\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgHex\":\"abc123测试\"}，输出区含「灰背景 暖色背景\nabc123测试\nabc123测试\n1.00\n不达标」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-animation-generator",
    "inputs": {
      "duration": "42",
      "delay": "42",
      "bx1": "42",
      "by1": "42",
      "bx2": "42",
      "by2": "42",
      "easing": "ease",
      "iteration": "2",
      "direction": "reverse",
      "fillMode": "forwards"
    },
    "expect": [
      " fade-in 42s ease 42s 2 reverse forwards ; }\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"duration\":\"42\",\"delay\":\"42\",\"bx1\":\"42\",\"by1\":\"42\",\"bx2\":\"42\",\"by2\":\"42\",\"easing\":\"ease\",\"iteration\":\"2\",\"direction\":\"reverse\",\"fillMode\":\"forwards\"}，输出区含「 fade-in 42s ease 42s 2 reverse forwards…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-border-radius",
    "inputs": {
      "allRadius": "42",
      "tl1": "42",
      "tl2": "42",
      "tr1": "42",
      "tr2": "42",
      "bl1": "42",
      "bl2": "42",
      "br1": "42",
      "br2": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      " 斜角 ☆ 波浪\n42\n42px\n42\n42\n42\n42\n42\n42\n42\n42\n42%\n42%\n42%\n42%\n42%\n42%\n42%\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"allRadius\":\"42\",\"tl1\":\"42\",\"tl2\":\"42\",\"tr1\":\"42\",\"tr2\":\"42\",\"bl1\":\"42\",\"bl2\":\"42\",\"br1\":\"42\",\"br2\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「 斜角 ☆ 波浪\n42\n42px\n42\n42\n42\n42\n42\n42\n42\n42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-grid-generator",
    "inputs": {
      "cols": "42",
      "gap": "42",
      "containerW": "42"
    },
    "expect": [
      "42\n42\n42\n列数需在 1-12 之间。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cols\":\"42\",\"gap\":\"42\",\"containerW\":\"42\"}，输出区含「42\n42\n42\n列数需在 1-12 之间。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-box-shadow-generator",
    "inputs": {
      "offsetX": "42",
      "offsetY": "42",
      "blur": "42",
      "spread": "42",
      "opacity": "42",
      "color": "abc123测试",
      "colorText": "abc123测试",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "-shadow: 42px 42px 42px 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"offsetX\":\"42\",\"offsetY\":\"42\",\"blur\":\"42\",\"spread\":\"42\",\"opacity\":\"42\",\"color\":\"abc123测试\",\"colorText\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「-shadow: 42px 42px 42px 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/data-matrix",
    "inputs": {
      "text": "abc123测试",
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-text-shadow",
    "inputs": {
      "customText": "abc123测试",
      "offsetX": "42",
      "offsetY": "42",
      "blur": "42",
      "color": "abc123测试",
      "colorText": "abc123测试",
      "opacity": "42",
      "textColor": "abc123测试",
      "textColorText": "abc123测试",
      "fontSize": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "\n#000000\n42\n42px\nabc123测试\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"customText\":\"abc123测试\",\"offsetX\":\"42\",\"offsetY\":\"42\",\"blur\":\"42\",\"color\":\"abc123测试\",\"colorText\":\"abc123测试\",\"opacity\":\"42\",\"textColor\":\"abc123测试\",\"textColorText\":\"abc123测试\",\"fontSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「\n#000000\n42\n42px\nabc123测试\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/depth-of-field-calculator",
    "inputs": {
      "focal": "42",
      "aperture": "42",
      "distance": "42",
      "sensor": "1.5"
    },
    "expect": [
      "2.00m ~ ∞\n2.00m 近点清晰 ∞ 远点清晰 2.1m 超焦距"
    ],
    "ref": "自动补强（B类零用例，2026-10-25 去双重裁剪后 h=f²/(N·c)=42²/(42×0.02)=2100mm=2.1m（f/42 光圈、APS-C c=0.02）；s=42m>h ⇒ 仅远点=∞，近点 = h·s/(h+s−f) = 2100×42000/(2100+42000−42) = 2001.9mm → 2.00m。原 expect `—m ~ ∞` 记录的是修复前「近点也误判为 ∞」的缺陷输出（经通用替换成 —），现按正确公式更新。默认态（50mm/1.8/2m/全幅 → 46.4m）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/detector-28",
    "inputs": {
      "formaldehyde": "42",
      "voc": "42",
      "benzeneContent": "42",
      "matType": "paint"
    },
    "expect": [
      "/kg 限值要求：VOC≤120g/L 环保等级： 合格品 符合GB 18582标准，可用于室内墙面"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"formaldehyde\":\"42\",\"voc\":\"42\",\"benzeneContent\":\"42\",\"matType\":\"paint\"}，输出区含「/kg 限值要求：VOC≤120g/L 环保等级： 合格品 符合GB 18582…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/detector-29",
    "inputs": {
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "textSize": "large",
      "targetLevel": "aaa"
    },
    "expect": [
      "Over） AA\nabc123测试\nabc123测试\nlarge\naaa\n颜色格式错误，请输入正确的HEX颜色（如#1F2937）\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textSize\":\"large\",\"targetLevel\":\"aaa\"}，输出区含「Over） AA\nabc123测试\nabc123测试\nlarge\naaa\n颜色格…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/dot-pattern",
    "inputs": {
      "bgColor": "abc123测试",
      "dotColor": "abc123测试",
      "dotSize": "42",
      "spacing": "42",
      "cssOutput": "1\n2\n3",
      "arrangement": "offset"
    },
    "expect": [
      "ckground-position: 0 0, 21px 21px;"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"dotColor\":\"abc123测试\",\"dotSize\":\"42\",\"spacing\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"arrangement\":\"offset\"}，输出区含「ckground-position: 0 0, 21px 21px;」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/favicon-from-emoji",
    "inputs": {
      "emoji": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42",
      "radius": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\nabc123测试 abc123测试 abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"emoji\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\"}，输出区含「abc123测试\nabc123测试\n42\n42\nabc123测试 abc123测…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/farnsworth-d15-test",
    "inputs": {
      "fdSize": "42",
      "fdShuffle": "medium",
      "fdMode": "swap",
      "fdLabel": "none"
    },
    "expect": [
      "基准 ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fdSize\":\"42\",\"fdShuffle\":\"medium\",\"fdMode\":\"swap\",\"fdLabel\":\"none\"}，输出区含「基准 ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/favicon-from-text",
    "inputs": {
      "text": "abc123测试",
      "bgColor": "abc123测试",
      "textColor": "abc123测试",
      "size": "42",
      "radius": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\n42\nabc123测试 abc123测试 abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\n42\nabc123测…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/flexbox-generator",
    "inputs": {
      "gap": "42",
      "dir": "row-reverse",
      "just": "center",
      "ali": "flex-start",
      "wrap": "wrap"
    },
    "expect": [
      "row-reverse\ncenter"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gap\":\"42\",\"dir\":\"row-reverse\",\"just\":\"center\",\"ali\":\"flex-start\",\"wrap\":\"wrap\"}，输出区含「row-reverse\ncenter」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/favicon-generator",
    "inputs": {
      "textInput": "abc123测试",
      "bgColor": "abc123测试",
      "bgHex": "abc123测试",
      "fgColor": "abc123测试",
      "fgHex": "abc123测试",
      "fontSize": "42",
      "fontWeight": "bold"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\nbold\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"textInput\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgHex\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"fgHex\":\"abc123测试\",\"fontSize\":\"42\",\"fontWeight\":\"bold\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\nbold\nabc12…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/font-preview",
    "inputs": {
      "fpSize": "42",
      "fpSearch": "abc123测试",
      "fpText": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n42\nNaNpx\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fpSize\":\"42\",\"fpSearch\":\"abc123测试\",\"fpText\":\"1\\n2\\n3\"}，输出区含「1 2 3\n42\nNaNpx\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/focal-length-equivalent",
    "inputs": {
      "focal": "42",
      "compareFocal": "42",
      "fromSensor": "aps-c",
      "toSensor": "aps-c"
    },
    "expect": [
      "段类型 视角: 30.0° × 20.2° → 30.0° × 20.2°\n67mm 全画幅等效\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"compareFocal\":\"42\",\"fromSensor\":\"aps-c\",\"toSensor\":\"aps-c\"}，输出区含「段类型 视角: 30.0° × 20.2° → 30.0° × 20.2°\n67…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-10",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "mation: flip-873 2.7s cubic-bezier(0.68,-0.55,0.27,1.55) 0.2s 2 normal"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「mation: flip-873 2.7s cubic-bezier(0.68,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-11",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "(45deg, #00C9A7, #00C9A7 10.75px, #00C9A7 10.75px, #00C9A7 21.5px); } 30. 波浪"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「(45deg, #00C9A7, #00C9A7 10.75px, #00C9A…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "design/generator-33",
    "inputs": {
      "total": "42",
      "chapters": "42",
      "minCh": "42",
      "perDay": "42",
      "mode": "four"
    },
    "expect": [
      "00 万 字 / 21 章 转 30% 13 章 12.60 万 字 33.60 万 字 / 34 章 合 20% 8 章 8.40 万 字 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"chapters\":\"42\",\"minCh\":\"42\",\"perDay\":\"42\",\"mode\":\"four\"}，输出区含「00 万 字 / 21 章 转 30% 13 章 12.60 万 字 33.60…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-38",
    "inputs": {
      "target": "abc123测试",
      "constraint": "abc123测试",
      "cnt": "42",
      "task": "优化",
      "format": "表格"
    },
    "expect": [
      "家。 【任务】对「abc123测试」执行优化。 【输出格式】按表格输出 20"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"target\":\"abc123测试\",\"constraint\":\"abc123测试\",\"cnt\":\"42\",\"task\":\"优化\",\"format\":\"表格\"}，输出区含「家。 【任务】对「abc123测试」执行优化。 【输出格式】按表格输出 20」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-34",
    "inputs": {
      "slides": "42",
      "minutes": "42",
      "points": "42",
      "fontSize": "42",
      "speed": "180",
      "ratio": "1920x1200"
    },
    "expect": [
      "第 4 页 正文 61.2 s 1.5 s 110 字 第 22 页 正文 61.2 s 1.5 s 110 字 第 39 页 正文 61.2 s 1.5 s 110 字 第 40 页 正文 61.2 s 1.5 s 110 字 第 41 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"slides\":\"42\",\"minutes\":\"42\",\"points\":\"42\",\"fontSize\":\"42\",\"speed\":\"180\",\"ratio\":\"1920x1200\"}，输出区含「第 4 页 正文 61.2 s 1.5 s 110 字 第 22 页 正文 61…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-9",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "N-13 条形码 1 661910 592918 完整数字: 1661910592918 | 校验位: 8 17"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「N-13 条形码 1 661910 592918 完整数字: 166191059…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-7",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "-radius: 26px; } 16. outset"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「-radius: 26px; } 16. outset」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-8",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "le.com/q/ffzqi2oo"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「le.com/q/ffzqi2oo」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-6",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "-shadow: 7px -13px 9px 1px rgba(59, 130, 246, 0.40), -9px 7px 19px 9px rgba(245, 158, 11, 0.47), -6px 18px 26"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「-shadow: 7px -13px 9px 1px rgba(59, 130,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/gradient",
    "inputs": {
      "angle": "42",
      "cssOutput": "1\n2\n3",
      "gradientType": "radial"
    },
    "expect": [
      "× 100% ×\nradial"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"angle\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"gradientType\":\"radial\"}，输出区含「× 100% ×\nradial」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/gradient",
    "inputs": {
      "cssCheck": "linear-gradient(90deg, #000000 0%, #ffffff 100%)"
    },
    "clicks": [
      "checkContrast()"
    ],
    "expect": [
      "#000000 ↔ #ffffff：21.00:1"
    ],
    "ref": "WCAG 相邻色标对比度：粘贴纯黑(#000000)→纯白(#ffffff)渐变，相对亮度 0 与 1，对比度=(1+0.05)/(0+0.05)=21.00:1。默认 667eea/764ba2 约 1.35:1，输入为空或注入失败即不命中。"
  },
  {
    "slug": "design/grid-pattern",
    "inputs": {
      "bgColor": "abc123测试",
      "lineColor": "abc123测试",
      "cellSize": "42",
      "lineWidth": "42",
      "cssOutput": "1\n2\n3",
      "gridType": "dotted"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\ndotted"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"lineColor\":\"abc123测试\",\"cellSize\":\"42\",\"lineWidth\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"gridType\":\"dotted\"}，输出区含「abc123测试\nabc123测试\n42\n42\ndotted」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/glassmorphism-generator",
    "inputs": {
      "opacity": "42",
      "blur": "42",
      "radius": "42",
      "borderOp": "42",
      "shadow": "42",
      "saturate": "42",
      "bgColor": "abc123测试",
      "bgColorText": "abc123测试",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "玻璃 方形玻璃\n\nabc123测试\n42\n42\n42\n42\n42\n42\n0.42\n42px\n42px\n0.42\n0.42\n42%\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"opacity\":\"42\",\"blur\":\"42\",\"radius\":\"42\",\"borderOp\":\"42\",\"shadow\":\"42\",\"saturate\":\"42\",\"bgColor\":\"abc123测试\",\"bgColorText\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「玻璃 方形玻璃\n\nabc123测试\n42\n42\n42\n42\n42\n42\n0.42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/gradient-from-color",
    "inputs": {
      "baseColor": "abc123测试",
      "steps": "42",
      "cssOutput": "1\n2\n3",
      "direction": "90"
    },
    "expect": [
      "gradient(90deg, #fed1cd 0%, #feada6 11%, #fd897f 22%, #fc6558 33%, #fc4131 44%, #fb1d0a 56%, #da1503 67%, #b21103 78%, #"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseColor\":\"abc123测试\",\"steps\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"direction\":\"90\"}，输出区含「gradient(90deg, #fed1cd 0%, #feada6 11%,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/identicon-generator",
    "inputs": {
      "seed": "abc123测试",
      "size": "42",
      "bgColor": "abc123测试",
      "blocks": "42"
    },
    "expect": [
      "abc123测试\n42\nabc123测试\n42\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"seed\":\"abc123测试\",\"size\":\"42\",\"bgColor\":\"abc123测试\",\"blocks\":\"42\"}，输出区含「abc123测试\n42\nabc123测试\n42\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-dpi-converter",
    "inputs": {
      "w1": "42",
      "h1": "42",
      "dpi1": "42",
      "w2": "42",
      "h2": "42",
      "dpi2": "42",
      "w3": "42",
      "h3": "42",
      "diag3": "6.1"
    },
    "expect": [
      "线 (mm) 1.0000 宽高比 42 × 42 像素 @ 42 DPI = 25.40 × 25.40 mm\n42\n42\n42\n694 宽度 (像素) 694 高度 (像素) 0.48 MP 总像素 1.0000 宽高比 42 × 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w1\":\"42\",\"h1\":\"42\",\"dpi1\":\"42\",\"w2\":\"42\",\"h2\":\"42\",\"dpi2\":\"42\",\"w3\":\"42\",\"h3\":\"42\",\"diag3\":\"6.1\"}，输出区含「线 (mm) 1.0000 宽高比 42 × 42 像素 @ 42 DPI = …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-cropper",
    "inputs": {
      "cx": "42",
      "cy": "42",
      "cw": "42",
      "ch": "42"
    },
    "expect": [
      "42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cx\":\"42\",\"cy\":\"42\",\"cw\":\"42\",\"ch\":\"42\"}，输出区含「42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-cropper",
    "inputs": { "cx": "12", "cy": "34", "cw": "56", "ch": "78" },
    "clicks": [
      "origImg={width:200,height:160};generate();window.__n1=document.getElementById('dlName').textContent;window.__h1=document.getElementById('downloadLink').href;origImg={width:240,height:180};document.getElementById('cx').value='5';document.getElementById('cy').value='6';document.getElementById('cw').value='70';document.getElementById('ch').value='80';generate();var __n2=document.getElementById('dlName').textContent;var __h2=document.getElementById('downloadLink').href;document.getElementById('dlName').textContent=__n2+'|nameChanged='+(window.__n1!==__n2)+'|hrefSet='+!!__h2+'|hrefFirstSet='+!!window.__h1;"
    ],
    "expect": [
      "cropped_240x180_5-6_70x80.png|nameChanged=true|hrefSet=true|hrefFirstSet=true"
    ],
    "ref": "换图/改参回归：先以 200×160 原图 + 裁剪(12,34,56×78) 生成下载名 cropped_200x160_12-34_56x78.png，再换 240×180 原图并把参数改为(5,6,70×80) 重跑 generate()。断言新文件名为 cropped_240x180_5-6_70x80.png、nameChanged=true（与上一张不同）、下载链接 href 已置为当前 canvas 数据（hrefSet/hrefFirstSet=true）。旧实现下载入口恒指上一张裁剪结果且 href 不随裁剪刷新，本用例不命中。"
  },
  {
    "slug": "design/image-resizer",
    "inputs": {
      "width": "42",
      "height": "42"
    },
    "expect": [
      "42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"height\":\"42\"}，输出区含「42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-rounded-corners",
    "inputs": {
      "radiusSlider": "42",
      "tlSlider": "42",
      "trSlider": "42",
      "blSlider": "42",
      "brSlider": "42",
      "bgColor": "abc123测试",
      "bgColorText": "abc123测试",
      "gradColor1": "abc123测试",
      "gradColor1Text": "abc123测试",
      "gradColor2": "abc123测试",
      "gradColor2Text": "abc123测试",
      "gradDirection": "to bottom"
    },
    "expect": [
      "42\nundefinedpx\n42\n42\n42\n42\n42\n42\n42\n42\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nto bottom"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"radiusSlider\":\"42\",\"tlSlider\":\"42\",\"trSlider\":\"42\",\"blSlider\":\"42\",\"brSlider\":\"42\",\"bgColor\":\"abc123测试\",\"bgColorText\":\"abc123测试\",\"gradColor1\":\"abc123测试\",\"gradColor1Text\":\"abc123测试\",\"gradColor2\":\"abc123测试\",\"gradColor2Text\":\"abc123测试\",\"gradDirection\":\"to bottom\"}，输出区含「42\nundefinedpx\n42\n42\n42\n42\n42\n42\n42\n42\na…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-format-converter",
    "inputs": {
      "qualitySlider": "42",
      "customWidth": "42",
      "customHeight": "42",
      "percentScale": "42"
    },
    "expect": [
      "42\n42%\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"qualitySlider\":\"42\",\"customWidth\":\"42\",\"customHeight\":\"42\",\"percentScale\":\"42\"}，输出区含「42\n42%\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-to-ascii",
    "inputs": {
      "width": "42",
      "contrast": "42",
      "brightness": "42"
    },
    "expect": [
      "42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"contrast\":\"42\",\"brightness\":\"42\"}，输出区含「42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/initials-avatar",
    "inputs": {
      "name": "abc123测试",
      "size": "42",
      "radius": "42",
      "fontSize": "42",
      "textColor": "abc123测试",
      "bg1": "abc123测试",
      "bg2": "abc123测试",
      "bgStyle": "custom",
      "letterCount": "2"
    },
    "expect": [
      "abc123测试\n42\n42\n42\nabc123测试\ncustom\nabc123测试\nabc123测试\n2\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"name\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\",\"fontSize\":\"42\",\"textColor\":\"abc123测试\",\"bg1\":\"abc123测试\",\"bg2\":\"abc123测试\",\"bgStyle\":\"custom\",\"letterCount\":\"2\"}，输出区含「abc123测试\n42\n42\n42\nabc123测试\ncustom\nabc123…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/iso-noise-reference",
    "inputs": {
      "isoRange": "42",
      "sensor": "m43",
      "light": "normal",
      "camera": "sony_a7rv"
    },
    "expect": [
      "焦 ⚠️ 不足： 高感不如低像素机型、文件大 💡 总结： 高像素机型，高感表现尚可，缩图后接近低像素机型"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"isoRange\":\"42\",\"sensor\":\"m43\",\"light\":\"normal\",\"camera\":\"sony_a7rv\"}，输出区含「焦 ⚠️ 不足： 高感不如低像素机型、文件大 💡 总结： 高像素机型，高感表现…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/isometric-grid",
    "inputs": {
      "bgColor": "abc123测试",
      "lineColor": "abc123测试",
      "size": "42",
      "lineWidth": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"lineColor\":\"abc123测试\",\"size\":\"42\",\"lineWidth\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「abc123测试\nabc123测试\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/loading-dots",
    "inputs": {
      "color": "abc123测试",
      "count": "42",
      "size": "42",
      "speed": "42",
      "cssOutput": "1\n2\n3",
      "animType": "pulse"
    },
    "expect": [
      "pulse\nabc123测试\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color\":\"abc123测试\",\"count\":\"42\",\"size\":\"42\",\"speed\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"animType\":\"pulse\"}，输出区含「pulse\nabc123测试\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/neomorphism-generator",
    "inputs": {
      "distance": "42",
      "blur": "42",
      "intensity": "42",
      "radius": "42",
      "bgColor": "abc123测试",
      "bgColorText": "abc123测试",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "-shadow: 42px 42px 42px rgba(199, 204, 211, 0.42), -42px -42px 4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"distance\":\"42\",\"blur\":\"42\",\"intensity\":\"42\",\"radius\":\"42\",\"bgColor\":\"abc123测试\",\"bgColorText\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「-shadow: 42px 42px 42px rgba(199, 204, 2…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/material-color",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "abc123测试\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「abc123测试\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/palette-cvd-checker",
    "inputs": {
      "pcPick": "abc123测试",
      "pcInput": "1\n2\n3",
      "pcMetric": "e76"
    },
    "expect": [
      "色盲 灰度/黑白\n尚未解析到有效颜色\ne76\n1 2 3\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pcPick\":\"abc123测试\",\"pcInput\":\"1\\n2\\n3\",\"pcMetric\":\"e76\"}，输出区含「色盲 灰度/黑白\n尚未解析到有效颜色\ne76\n1 2 3\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/pattern-generator",
    "inputs": {
      "color1": "abc123测试",
      "color2": "abc123测试",
      "size": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "ent 75%, abc123测试 75%, abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"size\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「ent 75%, abc123测试 75%, abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/photo-aspect-ratio-calculator",
    "inputs": {
      "w": "42",
      "h": "42"
    },
    "expect": [
      "幅 3:1 全景\n42 × 42\n1:1 最简比例 1.000:1 宽高比 0.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"h\":\"42\"}，输出区含「幅 3:1 全景\n42 × 42\n1:1 最简比例 1.000:1 宽高比 0.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/particle-effect-generator",
    "inputs": {
      "count": "42",
      "psize": "42",
      "speed": "42",
      "gravity": "42",
      "lifetime": "42",
      "linkDist": "42",
      "pColor": "abc123测试",
      "bgColor": "abc123测试"
    },
    "expect": [
      "42\n42\n42\nabc123测试\nabc123测试\n42\n42\n42\n42\n42\n42\n42.00\n42\n∞\n粒子: 42 | FPS: 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\",\"psize\":\"42\",\"speed\":\"42\",\"gravity\":\"42\",\"lifetime\":\"42\",\"linkDist\":\"42\",\"pColor\":\"abc123测试\",\"bgColor\":\"abc123测试\"}，输出区含「42\n42\n42\nabc123测试\nabc123测试\n42\n42\n42\n42\n4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/photo-print-size",
    "inputs": {
      "pw": "42",
      "ph": "42",
      "dpi": "200"
    },
    "expect": [
      "| 需要像素: 1599×2000 (3.2MP) A4 ⚠️ 像素不"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pw\":\"42\",\"ph\":\"42\",\"dpi\":\"200\"}，输出区含「| 需要像素: 1599×2000 (3.2MP) A4 ⚠️ 像素不」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/pixel-art-generator",
    "inputs": {
      "gs": "42"
    },
    "expect": [
      "网格尺寸需在 4-24 之间。"
    ],
    "ref": "自动补强（B类零用例）：注入越界输入{\"gs\":\"42\"}，页面走尺寸校验分支输出「网格尺寸需在 4-24 之间。」；默认态（gs=8 合法）不产生该提示 ⇒ 双态判别明确、零逃生。注：expect 不再锚定「42\\n」（输入回显）到提示语的相邻关系——页面补齐颜色/模式下拉后，采集串在两者之间插入了下拉当前值（#EF4444 / draw），旧邻接串失效；改为锚定仅由越界输入触发的提示语本体。"
  },
  {
    "slug": "design/pixel-art",
    "inputs": {
      "colorPicker": "abc123测试",
      "colorText": "abc123测试"
    },
    "expect": [
      "\nabc123测试"
    ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
    "ref": "自动补强（B类零用例）：注入非默认输入{\"colorPicker\":\"abc123测试\",\"colorText\":\"abc123测试\"}，输出区含「\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/progress-bar-generator",
    "inputs": {
      "percent": "42",
      "height": "42",
      "color1": "abc123测试",
      "color2": "abc123测试",
      "radius": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "42\n42\nabc123测试\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"percent\":\"42\",\"height\":\"42\",\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"radius\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「42\n42\nabc123测试\nabc123测试\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/px-to-rem",
    "inputs": {
      "px": "42",
      "root": "42"
    },
    "expect": [
      "x（1rem = 42px）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"px\":\"42\",\"root\":\"42\"}，输出区含「x（1rem = 42px）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/photo-storage-calculator",
    "inputs": {
      "count": "42",
      "megapixel": "20",
      "format": "raw_uncompressed",
      "bit": "12",
      "cardSize": "64",
      "video": "10"
    },
    "expect": [
      "30.00 MB 单张大小",
      "可存储约 2,113 张照片"
    ],
    "ref": "自动补强（B类零用例）+ 本批修正：20MP×12bit 未压缩 = 30,000,000 B = 30.00 MB；"
      + "64 GB 卡 = 64×10^9 B，10 分钟 1080p 视频按 60 MB/分钟 = 600×10^6 B，"
      + "(64−0.6)×10^9 ÷ 30×10^6 = 2,113.3 ⇒ 2,113 张（旧实现按 1024^3 且不扣视频 ⇒ 2,290 张）。"
      + "默认态（24MP/14bit/RAW/1000 张/64GB/无视频）不含这两个锚 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/png-to-svg",
    "inputs": {
      "blockSize": "42",
      "alphaTh": "42",
      "svgCode": "1\n2\n3"
    },
    "expect": [
      "42\n42\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"blockSize\":\"42\",\"alphaTh\":\"42\",\"svgCode\":\"1\\n2\\n3\"}，输出区含「42\n42\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/qr-code-styled",
    "inputs": {
      "text": "abc123测试",
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42",
      "ecLevel": "M"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\nM"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\",\"ecLevel\":\"M\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\nM」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/rem-to-px",
    "inputs": {
      "rem": "42",
      "root": "42"
    },
    "expect": [
      "42\n42\n转换结果 42rem = 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rem\":\"42\",\"root\":\"42\"}，输出区含「42\n42\n转换结果 42rem = 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/ripple-effect",
    "inputs": {
      "bgColor": "abc123测试",
      "rippleColor": "abc123测试",
      "duration": "42",
      "size": "42",
      "cssOutput": "1\n2\n3",
      "rippleType": "pulse"
    },
    "expect": [
      "pulse\nabc123测试\nabc123测试\n42\n42\n\n.pulse-dot"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"rippleColor\":\"abc123测试\",\"duration\":\"42\",\"size\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"rippleType\":\"pulse\"}，输出区含「pulse\nabc123测试\nabc123测试\n42\n42\n\n.pulse-do…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/signature-pad",
    "inputs": {
      "strokeWidth": "42",
      "colorPicker": "abc123测试"
    },
    "expect": [
      "42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"strokeWidth\":\"42\",\"colorPicker\":\"abc123测试\"}，输出区含「42\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/shadow-generator",
    "inputs": {
      "offsetX": "42",
      "offsetY": "42",
      "blur": "42",
      "spread": "42",
      "color": "abc123测试",
      "colorText": "abc123测试",
      "inset": "inset"
    },
    "expect": [
      "-shadow: inset 42px 42px 42px 42px abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"offsetX\":\"42\",\"offsetY\":\"42\",\"blur\":\"42\",\"spread\":\"42\",\"color\":\"abc123测试\",\"colorText\":\"abc123测试\",\"inset\":\"inset\"}，输出区含「-shadow: inset 42px 42px 42px 42px abc12…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/shutter-speed-calculator",
    "inputs": {
      "focal": "42",
      "crop": "1.5",
      "is": "2"
    },
    "expect": [
      "42\n1.5\n2\n1/3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"crop\":\"1.5\",\"is\":\"2\"}，输出区含「42\n1.5\n2\n1/3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/skeleton-loader",
    "inputs": {
      "baseColor": "abc123测试",
      "highlightColor": "abc123测试",
      "duration": "42",
      "radius": "42",
      "cssOutput": "1\n2\n3",
      "skelType": "list"
    },
    "expect": [
      "t(90deg, abc123测试 25%, abc123测试 37%, abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseColor\":\"abc123测试\",\"highlightColor\":\"abc123测试\",\"duration\":\"42\",\"radius\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"skelType\":\"list\"}，输出区含「t(90deg, abc123测试 25%, abc123测试 37%, abc…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/spacing-scale",
    "inputs": {
      "baseSize": "42",
      "levels": "42",
      "cssOutput": "1\n2\n3",
      "ratio": "1.25"
    },
    "expect": [
      "--space-14: 955px; }"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseSize\":\"42\",\"levels\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"ratio\":\"1.25\"}，输出区含「--space-14: 955px; }」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/spinner-generator",
    "inputs": {
      "color": "abc123测试",
      "size": "42",
      "speed": "42",
      "cssOutput": "1\n2\n3",
      "spinType": "dual"
    },
    "expect": [
      "px solid abc123测试; border-bottom"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color\":\"abc123测试\",\"size\":\"42\",\"speed\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"spinType\":\"dual\"}，输出区含「px solid abc123测试; border-bottom」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/stripe-pattern",
    "inputs": {
      "color1": "abc123测试",
      "color2": "abc123测试",
      "angle": "42",
      "width": "42",
      "cssOutput": "1\n2\n3",
      "stripeType": "dashed"
    },
    "expect": [
      "radient(42deg, abc123测试, abc123测试 42px, abc123测试 42px, abc123测试 47px);"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"angle\":\"42\",\"width\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"stripeType\":\"dashed\"}，输出区含「radient(42deg, abc123测试, abc123测试 42px, …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/spectrum-visualizer",
    "inputs": {
      "bars": "42",
      "color1": "abc123测试",
      "color2": "abc123测试",
      "barStyle": "mirror"
    },
    "expect": [
      "42\nmirror\nabc123测试\nabc123测试\n⏸ 暂停"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bars\":\"42\",\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"barStyle\":\"mirror\"}，输出区含「42\nmirror\nabc123测试\nabc123测试\n⏸ 暂停」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/svg-minifier",
    "inputs": {
      "svgInput": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3\n原始: 5 字节 → 压缩后: 5 字节 (节省 0.0% )"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"svgInput\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3\n原始: 5 字节 → 压缩后: 5 字节 (节省 0.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/svg-to-png",
    "inputs": {
      "width": "42",
      "height": "42",
      "svgInput": "1\n2\n3"
    },
    "expect": [
      "42\n42\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"height\":\"42\",\"svgInput\":\"1\\n2\\n3\"}，输出区含「42\n42\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/tester-assessor",
    "inputs": {
      "totalTasks": "42",
      "successTasks": "42",
      "avgTime": "42",
      "expectedTime": "42",
      "errors": "42",
      "helpCount": "42",
      "userCount": "42",
      "satisfaction": "42",
      "sus": "2"
    },
    "expect": [
      " 完成时间比 1.00x (42s/42s) 100 操作错误率 1.0次/任务 (42次) 67 求助频率 1.0次/任务 (42次) 0 用户满意度 42/7 683"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalTasks\":\"42\",\"successTasks\":\"42\",\"avgTime\":\"42\",\"expectedTime\":\"42\",\"errors\":\"42\",\"helpCount\":\"42\",\"userCount\":\"42\",\"satisfaction\":\"42\",\"sus\":\"2\"}，输出区含「 完成时间比 1.00x (42s/42s) 100 操作错误率 1.0次/任务…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/tailwind-colors",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "abc123测试\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「abc123测试\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/text-shadow-generator",
    "inputs": {
      "shadowColor": "abc123测试",
      "textColor": "abc123测试",
      "bgColor": "abc123测试",
      "x": "42",
      "y": "42",
      "blur": "42",
      "cssOutput": "1\n2\n3",
      "preset": "hard"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\n42\n42\nhard"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"shadowColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"x\":\"42\",\"y\":\"42\",\"blur\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"preset\":\"hard\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\n42\n42\nhard」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/toast-generator",
    "inputs": {
      "message": "abc123测试",
      "radius": "42",
      "bgColor": "abc123测试",
      "cssOutput": "1\n2\n3",
      "toastType": "error"
    },
    "expect": [
      "error\nabc123测试\n42\n#f44336\n✕ abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"message\":\"abc123测试\",\"radius\":\"42\",\"bgColor\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\",\"toastType\":\"error\"}，输出区含「error\nabc123测试\n42\n#f44336\n✕ abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/vh-vw",
    "inputs": {
      "val": "42",
      "base": "42",
      "mode": "px2vh"
    },
    "expect": [
      "px2vh\n42\n42\n转换结果 42 → 100.0000vh 按视口高度 42px 计算"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"base\":\"42\",\"mode\":\"px2vh\"}，输出区含「px2vh\n42\n42\n转换结果 42 → 100.0000vh 按视口高度 4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/typography-scale",
    "inputs": {
      "baseSize": "42",
      "cssOutput": "1\n2\n3",
      "ratio": "1.125",
      "fontFamily": "Georgia, serif"
    },
    "expect": [
      "42\n1.125\nGeorgia, "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"ratio\":\"1.125\",\"fontFamily\":\"Georgia, serif\"}，输出区含「42\n1.125\nGeorgia, 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/waveform-visualizer",
    "inputs": {
      "freq": "42",
      "amp": "42",
      "phase": "42",
      "color": "abc123测试",
      "waveType": "square"
    },
    "expect": [
      "square\n42\n42\n42\nabc123测试\n⏸ 暂停"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"freq\":\"42\",\"amp\":\"42\",\"phase\":\"42\",\"color\":\"abc123测试\",\"waveType\":\"square\"}，输出区含「square\n42\n42\n42\nabc123测试\n⏸ 暂停」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/web-audio-metronome",
    "inputs": {
      "bpmSlider": "42",
      "vol": "42",
      "beatsPer": "3",
      "sound": "beep"
    },
    "expect": [
      "3\n1 2 3\nNaN\nNaN\n42\nbeep"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bpmSlider\":\"42\",\"vol\":\"42\",\"beatsPer\":\"3\",\"sound\":\"beep\"}，输出区含「3\n1 2 3\nNaN\nNaN\n42\nbeep」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/cvd-safe-palette",
    "inputs": {
      "csCount": "42",
      "csMode": "sequential",
      "csStrategy": "lightness"
    },
    "expect": [
      " #0EA5E9\nsequential\n42\nlightness"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"csCount\":\"42\",\"csMode\":\"sequential\",\"csStrategy\":\"lightness\"}，输出区含「 #0EA5E9\nsequential\n42\nlightness」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    slug: "design/shadow-generator",
    // S2 设计系统风格预设组（04 批次）：clicks 直调 applyPreset(i)，i 依赖 PRESETS 追加序
    // （原 12 个 index 0-11；追加 Material1=12 / Material4=13 / Neu亮=14 / Neu暗=15 / Glass+=16 / Brutal=17 / TW sm=18 / TW md=19 / TW lg=20 / TW xl=21）。
    // applyPreset → parseShadow（色提尾、数值四元、缺省补 0）→ buildShadowStr 拼 `x y blur spread color`（层间 ', '）→ #code = `box-shadow: ...;`
    inputs: {},
    clicks: ["applyPreset(14);"],
    expect: ["box-shadow: 9px 9px 18px 0px #d1d9e6, -9px -9px 18px 0px #ffffff;"],
    ref: "Neu 亮预设（index 14）：parseShadow('9px 9px 18px #d1d9e6') → x9 y9 blur18 spread0 → '9px 9px 18px 0px #d1d9e6'；第二层 '-9px -9px 18px 0px #ffffff'。默认态 #code='box-shadow: 0px 10px 20px -5px #667eea;' ⇒ 零交集。"
  },
  {
    slug: "design/shadow-generator",
    inputs: {},
    clicks: ["applyPreset(17);"],
    expect: ["box-shadow: 8px 8px 0px 0px #000000;"],
    ref: "Brutal 预设（index 17）：'8px 8px 0 #000000' → blur=0/spread=0 补 0px。默认态零交集。"
  },
  {
    slug: "design/shadow-generator",
    inputs: {},
    clicks: ["applyPreset(21);"],
    expect: ["box-shadow: 0px 20px 25px -5px rgba(0,0,0,0.1), 0px 8px 10px -6px rgba(0,0,0,0.1);"],
    ref: "TW xl 预设（index 21，Tailwind shadow-2xl）：两层 rgba 保留原串。默认态零交集。"
  },
  {
    slug: "design/shadow-generator",
    inputs: { offsetX: "6", offsetY: "8", blur: "14", spread: "7", color: "#f43f5e", colorText: "#f43f5e" },
    // setMode('text') 后把预览的内联 textShadow 追加进 code 元素，一次校验导出与预览同步
    clicks: ["setMode('text'); document.getElementById('code').textContent += ' | ' + document.getElementById('preview').style.textShadow;"],
    expect: ["text-shadow: 6px 8px 14px #f43f5e; | 6px 8px 14px #f43f5e"],
    ref: "N4-C text-shadow 只有 offset-x offset-y blur color：即使扩散=7px 也必须省略第 4 个长度值，"
       + "导出声明与预览内联值一致为「6px 8px 14px #f43f5e」。旧实现拼成「6px 8px 14px 7px #f43f5e」，"
       + "整条声明非法；默认 box 模式输出含 spread，本用例只锚文字阴影模式。"
  },
  {
    slug: "design/spinner-generator",
    inputs: { size: "64", speed: "2", spinType: "border" },
    // generate() 后读取预览专用 <style>，用前缀锚定，避免误命中 textarea 里本就存在的一份 keyframes
    clicks: ["document.getElementById('output').textContent = 'PREVIEWSTYLE:' + document.getElementById('spinnerPreviewStyle').textContent;"],
    expect: ["PREVIEWSTYLE:@keyframes spinGen { to { transform: rotate(360deg); } }"],
    ref: "N4-D 预览动画：keyframes 必须真正进入预览样式节点（旧页面从未注入，预览只读到内联 animation 而无"
       + "对应 @keyframes ⇒ 全静止）。前缀 PREVIEWSTYLE 确保区分于 cssOutput 导出文本；默认 generate() 同样"
       + "执行但旧实现该前缀后为空，故可强判别修复前后。"
  },
  {
    slug: "design/mesh-gradient",
    inputs: { overlay: "#000000" },
    expect: ["最低对比度 3.30:1（与 #764ba2）· AA 大文本"],
    ref: "WCAG 改造：默认三色 #667eea/#764ba2/#f093fb，叠加文字注入 #000000 ⇒ 与最暗色 #764ba2 对比度 = (0.1187+0.05)/(0.0353+0.05)=3.30"
       + "（独立复算 sRGB 线性化），等级按 <4.5 判「AA 大文本」。默认态 overlay=#ffffff 输出「最低对比度 2.04:1（与 #f093fb）」，不含该串。"
  },
  // ── 照片存储：超容量明示（不再静默夹 100%）────────────────────
  {
    slug: "design/photo-storage-calculator",
    inputs: { count: "3000", megapixel: "45", format: "tiff", bit: "16", cardSize: "64", video: "0" },
    expect: ["超出容量：", "476.00 GB"],
    ref: "45MP×16bit×TIFF(×2) = 180,000,000 B/张；3000 张 = 540×10^9 B，64 GB 卡 = 64×10^9 B；"
       + "超出 476×10^9 B ⇒ 必须提示「超出容量：476.00 GB」。旧实现把百分比夹到 100% 且不提示，默认 1000 张也不会超出。",
  },
  {
    slug: "design/photo-storage-calculator",
    inputs: { count: "-1", megapixel: "0", format: "tiff", bit: "16", cardSize: "0", video: "0" },
    expect: ["请填写大于 0 的像素（MP）与存储卡容量"],
    ref: "非法容量/像素必须明确报错，不能靠 Infinity/0 静默出结果；默认 24MP/64GB 不命中该提示。",
  },
  // ── 冲印尺寸：DPI/像素非正数明确报错 ──────────────────────────
  {
    slug: "design/photo-print-size",
    inputs: { pw: "0", ph: "3000", dpi: "300" },
    expect: ["像素尺寸必须为大于 0 的整数"],
    ref: "宽 0 时旧实现 `+value||1` 回退成 1px，静默给出错误的冲印尺寸；现直接提示。默认 3000×2000/300DPI 不命中。",
  },
  {
    slug: "design/photo-print-size",
    inputs: { pw: "3000", ph: "2000", dpi: "0" },
    expect: ["DPI 必须大于 0"],
    ref: "DPI 为 0 时旧实现除零得 Infinity，随后把整个尺寸列表替换成「—」；现给出明确提示。",
  },
  // ── SVG 转 PNG：宽高为 0/负数校验 ─────────────────────────────
  {
    slug: "design/svg-to-png",
    inputs: { width: "0", height: "400" },
    clicks: ["generate()"],
    expect: ["⚠ 宽度和高度必须为正整数"],
    ref: "宽 0 时旧实现 parseInt||400 回退成 400，静默导出与输入不符的图；现直接提示。默认 400×400 不命中。",
  },
  // ── SVG 转 PNG：外部资源净化（防 canvas 被污染）─────────────────
  {
    slug: "design/svg-to-png",
    inputs: {},
    clicks: ["var r=__svgSanitize('<svg xmlns=\"http://www.w3.org/2000/svg\"><foreignObject width=\"10\" height=\"10\"><div xmlns=\"http://www.w3.org/1999/xhtml\">x</div></foreignObject><image href=\"https://evil.example/x.png\" xlink:href=\"https://evil.example/x.png\"/><style>@import url(\"https://evil.example/a.css\");</style></svg>');document.getElementById('exportMetaVal').textContent='FO:'+r.report.foreignObject+' EXT:'+r.report.externalRefs+' CSS:'+r.report.cssRefs+' GONE:'+(r.svg.indexOf('evil.example')>=0?'NO':'YES');"],
    expect: ["FO:1 EXT:2 CSS:1 GONE:YES"],
    ref: "净化口径：foreignObject 整块删除计 1；href 与 xlink:href 两个外链属性各计 1；<style> 内 @import 计 1；净化产物不含 evil.example ⇒ 外链确被剥离。"
      + "门禁无 DOMParser/XMLSerializer ⇒ 走字符串兜底路径，与浏览器 DOM 路径计数口径一致（<style> 文本另计）。"
      + "默认态（空输入）exportMetaVal 为「输出像素：」且不含 FO:/EXT: 串 ⇒ 判别明确。",
  },

  // ── 导出失败必须可见（canvas.toDataURL 抛异常时不得静默）───────
  ...["design/avatar-generator", "design/aztec-code", "design/data-matrix", "design/favicon-from-emoji"].map(function (slug) {
    return {
      slug: slug,
      inputs: {},
      clicks: ["var _ce=document.createElement.bind(document);document.createElement=function(t){var el=_ce(t);if(t==='canvas'){el.toDataURL=function(){throw new Error('boom')};}return el;};generate();"],
      expect: ["⚠ 导出 PNG 失败：Error"],
      ref: "失败注入：把桩内 createElement('canvas') 产物的 toDataURL 改成必抛 Error，再跑 generate() ⇒ 必须在结果区出现可见的「⚠ 导出 PNG 失败：Error」。"
        + "修复前裸调 toDataURL，异常直接冒成 pageerror、页面无任何提示；默认态（不注入）无该文案 ⇒ 判别明确。",
    };
  }),
  // ── px→rem：全角数字/单位后缀解析 + 根字号夹取提示 ────────────
  {
    slug: "design/px-to-rem",
    inputs: { px: "２４px", root: "１６px" },
    expect: ["1.5000rem"],
    ref: "全角数字 ２４＋单位后缀 px 归一为 24，根字号 １６px 归一为 16 ⇒ 24/16 = 1.5000rem；"
       + "旧实现 parseFloat('２４px') = NaN ⇒ 0 ⇒ 输出 0.0000rem。默认 16px/16px ⇒ 1.0000rem，注入失败即不命中。",
  },
  {
    slug: "design/px-to-rem",
    inputs: { px: "100", root: "0" },
    expect: ["根字号必须大于 0，已按 16px 计算"],
    ref: "根字号为 0 时旧实现静默改成 16 且不说明；现明确提示夹取口径。默认 16 不命中。",
  },
  {
    slug: "design/shutter-speed-calculator",
    inputs: { focal: "" },
    expect: ["Enter a valid focal length, crop factor and stabilization stops."],
    ref: "焦距清空后旧实现 +''||50 静默按 50mm 计算安全快门；现显式拦截空值。默认 50 ⇒ 不命中。",
  },
  {
    slug: "design/image-dpi-converter",
    inputs: { w1: "" },
    expect: ["⚠ 计算结果含无效值，请检查输入是否为有效正数。"],
    ref: "像素宽清空后旧实现 ||0 继续算出 0 英寸等伪结果；现由既有 NaN/Infinity 守卫报错。"
       + "默认 3000px ⇒ 不命中。",
  },
  {
    slug: "design/photo-aspect-ratio-calculator",
    inputs: { w: "" },
    expect: ["Enter valid width and height (both positive)."],
    ref: "宽度清空后旧实现 +''||1 静默按 1px 计算比例；现显式要求正数。默认 1920×1080 ⇒ 不命中。",
  },
  {
    slug: "design/detector-28",
    inputs: { formaldehyde: "" },
    expect: ["Enter valid formaldehyde, VOC and benzene values (enter 0 if not detected)."],
    ref: "甲醛清空后旧实现 +''||0 静默按 0 计 ⇒ 直接判「E0 级（优等）」；现显式要求填写（未检出请填 0）。"
       + "默认 0.08 ⇒ 不命中。",
  },
  {
    slug: "design/analysis-64",
    inputs: { p3a: "" },
    expect: ["Fill in both scores for all 5 dimensions (enter 0 explicitly)."],
    ref: "某一维我方得分清空后旧实现 +''||0 静默记 0 分 ⇒ 总分差被放大、结论可能翻转；"
       + "现要求 5 维双方得分齐全（0 分显式填 0）。默认 p3a=9 ⇒ 不命中。",
  },
  {
    slug: "design/focal-length-equivalent",
    inputs: { compareFocal: "" },
    expect: ["Enter a valid focal length (mm)."],
    ref: "对比焦距清空后旧实现 +''||50 静默按 50mm 参与对比 ⇒ 对比表结论变化；现显式要求正数。"
       + "默认 50 ⇒ 不命中。",
  },
  {
    slug: "design/typography-scale",
    inputs: { ratio: "" },
    expect: ["⚠ 比例需为大于 0 且不等于 1 的数值。"],
    ref: "比例清空后旧实现 parseFloat('')||1.2 静默按 1.2 生成整组字阶；现显式提示并清空输出。"
       + "默认 1.25 ⇒ 不命中。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { ratio: "" },
    expect: ["⚠ 请输入有效的基准间距（>0）、比例（>0 且 ≠1）与档位数（正整数）。"],
    ref: "比例清空后旧实现 parseFloat('')||1.25 静默按 1.25 生成整组间距；现三处（基准/比例/档位数）"
       + "统一显式校验。默认 4/1.25/10 ⇒ 不命中。",
  },
  {
    slug: "design/tester-assessor",
    inputs: { totalTasks: "" },
    clicks: ["calc()"],
    expect: ["测试任务总数需为不小于 1 的整数。"],
    ref: "任务总数清空后旧实现 parseFloat('')||1 静默按 1 个任务继续出分（成功率 0% 也会给出总分）；"
       + "现要求全部绩效字段有效且数值合法。默认 5 ⇒ 不命中。",
  },
  {
    slug: "design/photo-print-size",
    inputs: { pw: "", ph: "", dpi: "" },
    clicks: ["ppExportCsv()"],
    expect: ["导出前请先填写有效的像素尺寸与 DPI。"],
    ref: "旧导出路径 +value||1 / ||300 会把空值静默当 1px×1px@300dpi 导出错误清单；"
       + "现导出前显式拒绝并同步清空最大可印尺寸。默认 4032×3024@300 ⇒ 不命中。",
  },
  {
    slug: "design/color-palette",
    inputs: { hexInput: "#F5F5F5" },
    expect: ["黑字 19.26:1 ✔ · 白字 1.09:1 ✘"],
    ref: "黑白字改按 WCAG 对比度取较大者：L(#F5F5F5)=0.913099，黑字 (0.963099)/0.05=19.26:1 ✔、"
       + "白字 1.05/0.963099=1.09:1 ✘。旧阈值 lum>0.5 在 L=0.2369 的 #667eea 上选白字（3.66:1，未过 AA），"
       + "新口径选黑字（5.74:1）。默认 #667eea ⇒ 不含 19.26:1 串。",
  },
  {
    slug: "design/color-picker",
    inputs: { hexInput: "#788EED" },
    expect: ["#000000（6.89:1）"],
    ref: "L(#788EED)=0.294535：黑字 (0.344535)/0.05=6.89:1、白字 1.05/0.344535=3.05:1 ⇒ 应选黑字。"
       + "旧阈值 lum>0.5 会选白字（3.05:1，未过 AA）。默认 #4151e1（L=0.1319）选白字 ⇒ 不含该串。",
  },
  {
    slug: "design/material-color",
    clicks: ["showDetail('Blue',4,'#42a5f5')"],
    expect: ["#000000（7.93:1）"],
    ref: "Material Blue 400 #42a5f5：L=0.346611，黑字 (0.396611)/0.05=7.93:1、白字 2.65:1 ⇒ 应选黑字；"
       + "旧阈值 lum>0.5 选白字（2.65:1）。默认未打开详情（自动调用无参数）⇒ 不含该串。",
  },
  {
    slug: "design/tailwind-colors",
    clicks: ["showDetail('blue',4,'#60a5fa')"],
    expect: ["#000000（8.26:1）"],
    ref: "Tailwind blue-400 #60a5fa：L=0.362992，黑字 (0.412992)/0.05=8.26:1、白字 2.54:1 ⇒ 应选黑字；"
       + "旧阈值 lum>0.5 选白字（2.54:1）。默认未打开详情 ⇒ 不含该串。",
  },
  {
    slug: "design/initials-avatar",
    inputs: { name: "AB" },
    expect: ["文字对比度 10.69:1"],
    ref: "姓名 AB 哈希取调色板 #1dd1a1（WCAG 相对亮度 L=0.4844）：与黑 (0.5344)/0.05=10.69:1、与白 1.05/0.5344=1.96:1 ⇒ 应自动选黑字。"
       + "默认 Tool Box 哈希为 #5f27cd（白字 7.90:1），不含 10.69:1；旧页无对比度输出 ⇒ 注入后必红。",
  },
  {
    slug: "design/initials-avatar",
    inputs: { bgStyle: "custom", bg1: "#777777", textColor: "#ffffff" },
    expect: ["文字对比度 4.48:1", "建议改用 #000000（4.69:1）"],
    ref: "#777777 相对亮度 L=0.1845：白字 1.05/0.2345=4.48:1（<4.5），黑字 0.2345/0.05=4.69:1 ⇒ "
       + "自定义模式应给出具体建议色与比值。默认 hash 模式为 7.90:1 且无「建议改用」，注入后旧实现不命中。",
  },
  {
    slug: "design/bpm-tapper",
    clicks: ["document.getElementById('bpm').innerHTML='SNAP='+computeBpm([0,900,1800]);"],
    expect: ["SNAP=65"],
    ref: "声明「round(实测 BPM ÷ 5) × 5」：三次点击间隔 900ms ⇒ 原始 BPM=60000/900=66.67，"
       + "按 5 取整 = round(13.33)×5=65；旧实现直接 round(66.67)=67。默认 BPM 区不含 SNAP 串。",
  }

,
{
  "slug": "design/color-palette-generator",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-cropper",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-flipper",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-format-converter",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-resizer",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-rotator",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-rounded-corners",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
// ── B 类：导出失败必须可见（toDataURL/toBlob 抛异常或返回 null 时不得静默）──
...[
  {
    slug: "design/color-palette-generator",
    entry: "exportImage()",
    ref: "exportImage() 内 toDataURL 裸调；注入后必须 toast「导出失败：<e.name||e.message>」。",
  },
  {
    slug: "design/image-resizer",
    entry: "origImg={width:20,height:20};generate()",
    ref: "image-resizer generate() 内 toDataURL 裸调；注入后必须 toast。默认态（无注入）无该文案 ⇒ 判别明确。",
  },
  {
    slug: "design/image-rotator",
    entry: "origImg={width:20,height:20};generate()",
    ref: "image-rotator generate() 内 toDataURL 裸调；注入后必须 toast。",
  },
  {
    slug: "design/image-cropper",
    entry: "origImg={width:20,height:20};generate()",
    ref: "image-cropper generate() 内 toDataURL 裸调（toBlob 链路另有 null 分支）；注入后必须 toast。",
  },
  {
    slug: "design/image-flipper",
    entry: "origImg={width:20,height:20};flip('h')",
    ref: "image-flipper flip() 内 toDataURL 裸调（toBlob 回调原为 if(blob) 静默）；注入后必须 toast。",
  },
].map(function (c) {
  return {
    slug: c.slug,
    inputs: {},
    clicks: [
      // 页面失败提示有两条路径：优先裸 `showToast`（common.js 全局），回落 `ToolBox.showToast`。
      // 保真模式下 common.js 提供了裸全局 ⇒ 只替换 ToolBox.showToast 会被绕过、录音器收不到；
      // 两条都替换，覆盖默认桩与线上真实执行。
      "window.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};"
      + "ToolBox.showToast=window.showToast;"
      + "window.canvasExportError=window.canvasExportError||function(){return null;};"
      + "var _ce=document.createElement.bind(document);"
      + "document.createElement=function(t){var e=_ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')};}return e;};"
      + c.entry,
    ],
    expect: ["TOAST:导出失败：Error"],
    ref: "失败注入：把桩内 canvas.toDataURL 改成必抛 Error 并把 ToolBox.showToast 换成录音器，再走真实导出入口 ⇒ 结果区必须出现「TOAST:导出失败：Error」。"
      + "修复前异常裸冒成 pageerror、页面无提示；默认态无 TOAST: 串 ⇒ 判别明确。" + c.ref,
  };
}),
// design/colorblind-simulator 的导出逻辑在外部模块 js/tools/colorblind-simulator.js（IIFE）里，
// 门禁 harness 不加载 /js/tools/*.js ⇒ 模块内 toast() 与 renderImagePane 均不可达，
// 无法做桩级失败注入；改为真机注入（toDataURL 抛 Error / toBlob 回调 null）验证，结果记录在本批回报。
// ── D1 批：B 类余页导出失败可见（新建 canvas 的页面）──
...[
  { slug: "design/favicon-from-text", entry: "generate()", ref: "generate() 的 lastURL 赋值裸调 toDataURL。" },
  { slug: "design/identicon-generator", entry: "generate()", ref: "generate() 的 lastURL 赋值裸调 toDataURL。" },
  { slug: "design/initials-avatar", entry: "generate()", ref: "generate() 的 lastURL 赋值裸调 toDataURL。" },

  { slug: "design/pixel-art", entry: "exportPNG()", ref: "exportPNG() 的 tmp.toDataURL 裸调。" },
  { slug: "design/signature-pad", entry: "strokes.push({});exportPNG();", ref: "exportPNG() 的 tmp.toDataURL 裸调；先塞一条空笔画绕过「请先签名」前置判断。" },
].map(function (c) {
  return {
    slug: c.slug,
    inputs: {},
    clicks: [
      "ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};"
      + "var _ce=document.createElement.bind(document);"
      + "document.createElement=function(t){var e=_ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')};}return e;};"
      + c.entry,
    ],
    expect: ["TOAST:导出失败：Error"],
    ref: "失败注入：canvas.toDataURL 必抛 Error + 录制 ToolBox.showToast ⇒ 必须出现「TOAST:导出失败：Error」。默认态无 TOAST: 串 ⇒ 判别明确。" + c.ref,
  };
}),
{
  "slug": "design/spectrum-visualizer",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var cv=document.getElementById('canvas');cv.toDataURL=function(){throw new Error('boom')};copyResult();"],
  "expect": ["TOAST:导出失败：Error"],
  "ref": "copyResult() 直接对页面 canvas 调 toDataURL（不经 createElement）⇒ 注入该元素 toDataURL 抛 Error + 录制 ToolBox.showToast，必须出现「TOAST:导出失败：Error」；且不得再走 clipboard。",
},
{
  "slug": "design/waveform-visualizer",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var cv=document.getElementById('canvas');cv.toDataURL=function(){throw new Error('boom')};copyResult();"],
  "expect": ["TOAST:导出失败：Error"],
  "ref": "copyResult() 直接对页面 canvas 调 toDataURL ⇒ 注入后必须「TOAST:导出失败：Error」，且不得再走 clipboard。",
},
{
  "slug": "design/favicon-generator",
  "clicks": ["var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toBlob=function(){throw new Error('boom')}};return e;};downloadSingle(16);"],
  "expect": ["导出失败：Error"],
  "ref": "失败注入：新建画布的 toBlob 必抛 Error ⇒ downloadSingle 必须 toast「导出失败：Error」。"
     + "修复前异常裸冒成 pageerror、且紧随其后仍弹「已下载 favicon-16x16.png」（失败被成功消息盖掉）；默认态无该串 ⇒ 判别明确。",
},
{
  "slug": "design/favicon-generator",
  "clicks": ["var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')}};return e;};copyDataURL();"],
  "expect": ["复制失败：Error"],
  "ref": "失败注入：新建画布的 toDataURL 必抛 Error ⇒ copyDataURL 必须 toast「复制失败：Error」并终止。"
     + "修复前异常裸冒成 pageerror、剪贴板复制提示不执行；默认态无该串 ⇒ 判别明确。",
}
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
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== design calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();