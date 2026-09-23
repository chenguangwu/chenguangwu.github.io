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