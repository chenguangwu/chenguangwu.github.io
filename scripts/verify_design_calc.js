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
    inputs: { px: "16", root: "16" },
    expect: ["1.0000rem"],
    ref: "rem = px ÷ 根字号；16 ÷ 16 = 1，页面保留 4 位小数 → 1.0000rem",
  },
  {
    slug: "design/rem-to-px",
    inputs: { rem: "1", root: "16" },
    expect: ["16.00px"],
    ref: "px = rem × 根字号；1 × 16 = 16，页面保留 2 位小数 → 16.00px",
  },
  {
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "100", base: "1920" },
    expect: ["5.2083vw"],
    ref: "vw = px ÷ 视口宽 × 100；100 ÷ 1920 × 100 = 5.20833…，保留 4 位 → 5.2083vw",
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
    inputs: { fgColor: "#1F2937", bgColor: "#FFFFFF" },
    expect: ["14.68:1"],
    ref: "WCAG 2.1 对比度 = (L_亮+0.05)/(L_暗+0.05)，L 按 sRGB gamma 线性化后加权(0.2126/0.7152/0.0722)。"
      + "#1F2937 的 L = 0.021525，白 L = 1 → 1.05 ÷ 0.071525 = 14.68",
  },
  {
    slug: "design/color-contrast-check",
    inputs: { fg: "#333333", bg: "#FFFFFF" },
    expect: ["12.63:1"],
    ref: "同上 WCAG 公式：#333333 三通道 = 51/255 = 0.2 → chan = ((0.2+0.055)/1.055)^2.4 = 0.033105，"
      + "L = 0.033105（R=G=B）→ 1.05 ÷ 0.083105 = 12.635 → 12.63:1",
  },
  {
    slug: "design/color-temperature-converter",
    inputs: { temp: "5500" },
    expect: ["#ffedde", "255,237,222"],
    ref: "Tanner Helland 近似式（k = K/100 = 55 ≤ 66 分支）：R = 255；"
      + "G = 99.47·ln55 − 161.12 = 237.49 → 237；B = 138.5·ln(55−10) − 305 = 222.22 → 222 → #FFEDDE",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#6366F1", steps: "5" },
    expect: ["#e5e6fd"],
    ref: "mix(c,t,r)=round(c+(t−c)·r)。基色 rgb(99,102,241)、steps=5："
      + "最浅 tint i=5 f=5/6 → round(99+(255−99)·0.833)=229 等 → #e5e6fd（靛蓝 tint，非灰度）。"
      + "修复前 mix 仅 2 参 → Math.round(t)：tint 退化为纯灰度 (#d5d5d5 档) 或 3 参缺 r 致 NaN，均不含此串。",
  },

  // ── 摄影光学类 ─────────────────────────────────────────────────
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "50", aperture: "1.8", distance: "2" },
    expect: ["46.3m", "1.92m"],
    ref: "超焦距 H = f²/(N·c)（f=50mm、N=1.8、全画幅 c=0.03mm）= 2500/0.054 = 46296mm ≈ 46.3m；"
      + "近点 = H·s/(H+(s−f)) = 46296×2000/48246 = 1.92m（远点 2.09m，景深 0.17m）",
  },
  {
    slug: "design/focal-length-equivalent",
    inputs: { focal: "50", fromSensor: "fullframe", toSensor: "fullframe" },
    expect: ["50.0mm", "39.6° × 27.0°"],
    ref: "同画幅（裁切系数 1）等效焦距 = 50 × 1 = 50.0mm；视角 = 2·atan(36/(2×50)) = 39.60°、"
      + "2·atan(24/(2×50)) = 26.99° → 39.6° × 27.0°（全画幅 36×24mm）",
  },
  {
    slug: "design/detector-29",
    // 覆盖核心对比度计算。另修该页「AAA 级条目数为 0 → 0/0 得 NaN% 且 pass===total 恒真误判通过/合规」。
    inputs: { fgColor: "#000000", bgColor: "#FFFFFF" },
    expect: ["21.00:1"],
    ref: "WCAG 相对亮度：黑 L=0、白 L=1 → 对比度 = (1+0.05)/(0+0.05) = 21.00:1（W3C 对比度公式）",
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