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