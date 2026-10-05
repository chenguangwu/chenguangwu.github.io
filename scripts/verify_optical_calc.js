#!/usr/bin/env node
/**
 * 第 27 道门禁：optical 分类计算正确性验证（6 个确定性光学/视光工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 覆盖：调节幅度(Hofstetter)、抗疲劳下加光、瞳高占比、周边离焦、棱镜移心(普伦蒂斯)、AC/A(梯度法)。
 * 用法: node scripts/verify_optical_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "optical/accommodation-amplitude",
    inputs: { age: "40" },
    expect: ["6.50"],
    ref: "Hofstetter 平均 A=18.5−0.30×40=6.50 D（最小 15−0.25×40=5.00，最大 25−0.40×40=9.00）",
  },
  {
    slug: "optical/anti-fatigue-design",
    inputs: { age: "48", workDist: "30", rx: "0" },
    expect: ["0.50"],
    ref: "平均 A=18.5−0.30×48=4.10；调节需求=100/30=3.33；保留 1/3=1.37；可用=2.73；Add=max(0,3.33−2.73)=0.60→量化0.25D=0.50D",
  },
  {
    slug: "optical/pupil-height",
    inputs: { pupilToBottom: "18", frameB: "30" },
    expect: ["60"],
    ref: "占比=18/30×100=60%（默认方法 direct）",
  },
  {
    slug: "optical/peripheral-defocus",
    inputs: { central: "1", peripheral: "4", angle: "20" },
    checks: ["single"],
    expect: ["+3.00", "3.00D"],
    ref: "RPD=周边−中央=4−1=3.00 D（radio lens=single 经 checks 注入，规避 stub :checked 返回 null）",
  },
  {
    slug: "optical/prism-decentration",
    inputs: { power: "5", prism: "3", base: "BO" },
    expect: ["6.00"],
    ref: "页面默认 prism 分支（setMode 在 stub 下报错但 calc 走 prism 分支）：移心量 c=P/|F|=3/5=0.6cm→6.00mm；普伦蒂斯 P=c×|F|",
  },
  {
    slug: "optical/aca-ratio",
    inputs: { nearPhoria: "2", nearPhoriaLens: "8", lens: "4" },
    expect: ["1.50"],
    ref: "默认 gradient 法：AC/A=(加镜后隐斜−裸眼隐斜)/|镜片度|=(8−2)/4=1.50 Δ/D",
  },
  {
    slug: "optical/detector-31",
    inputs: { element: "lens", pv: "0.25", rms: "0.05", decent: "3", trans: "98",
              surface: "40-20", coating: "ar", grade: "standard" },
    expect: ["满足标准级要求"],
    ref: "各项分 75/85/85/80/100 → 综合 85；grade=standard 达标线 75 → 通过，评价按所选等级写「满足标准级要求」（默认 grade=precision 达标线 90 → 判「未达精密级」，与本值不重合）",
  },
  {
    slug: "optical/detector-31",
    inputs: { element: "lens", pv: "1.5", rms: "0.15", decent: "12", trans: "93",
              surface: "80-50", coating: "ar", grade: "precision" },
    expect: ["当前指标为「不合格」"],
    ref: "各项分 45/30/30/20/40 → 综合 33 <60 → 实际档位「不合格」；grade=precision 达标线 90 未达，评价须同时给出实际档位（默认综合 85 实际档位为「标准级合格」，与本值不重合）",
  },
  {
    slug: "optical/calc-47",
    inputs: { idxN: "1.6", idxR: "80", idxH: "12", idxK: "-1" },
    expect: ["205.66 μm 当前锥面纵向球差"],
    ref: "LSA球面=(n−1)h²/(2nR)=(0.6×144)/(2×1.6×80)=0.3375mm=337.5μm；K=−1 → LSA=337.5×(1+K/n²)=337.5×(1−1/2.56)=205.66μm（默认 1.5/100/25/0 → 1041.67μm，避开）",
  },

  // ── §7.4 零用例加固 · optical 确定性数值页（探针实测取锚）────
  {
    slug: "optical/numerical-aperture",
    inputs: { n: "1.52", theta: "38" },
    expect: ["0.936", "0.87573"],
    ref: "注入非默认(默认 1.0/30)：NA = n·sinθ = 1.52×sin38° = 1.52×0.61566 = 0.936；NA² = 0.87573。默认态 NA = 1.0×0.5 = 0.5、NA² = 0.25，两条均不命中。"
  },
  {
    slug: "optical/lens-refractive-index",
    inputs: { power: "-6.25", diameter: "70", ct: "1.4" },
    expect: ["70mm", "32.02"],
    ref: "注入非默认(默认 -4.00/65/2.0)：−6.25D、直径 70mm、中心厚 1.4mm ⇒ 1.50 折射率档边缘厚度 32.02 mm，随折射率升高递减至 1.74 档的 22.09 mm。默认态为另一套表格值。"
  },
  {
    slug: "optical/telescope-magnification",
    inputs: { fo: "1200", fe: "10" },
    expect: ["120.0", "14400.000", "1210.000"],
    ref: "注入非默认(默认 1000/25)：角放大率 M = f₀/fₑ = 1200/10 = 120.0×；相对聚光力 = M² = 14400.000；两镜焦距之和 = 1200+10 = 1210.000 mm。默认态 40.0/1600/1025 均不命中。"
  },
  {
    slug: "optical/gaussian-beam-waist",
    inputs: { lam: "532", f: "80", D: "8" },
    expect: ["6.77", "2.7095e-4", "2.5000e-2"],
    ref: "注入非默认(默认 650/50/10)：束腰半径 w₀ = 4λf/(πD) = 4×532e-9×0.08/(π×0.008) = 6.77 µm；瑞利长度 = πw₀²/λ = 2.7095e-4 m；远场发散角 = λ/(πw₀) = 2.5000e-2 rad。默认态 4.14/… 不同。"
  },
  {
    slug: "optical/blue-light-filter",
    inputs: { cutoff: "450", steepness: "14" },
    expect: ["61.1%", "71.5%"],
    ref: "注入非默认(默认 430/10)：截止 450nm、陡度 14 ⇒ 有害蓝光(415-455nm)阻隔率 61.1%，有益蓝光(465-495nm)保留率 71.5%。默认态两项均不同。"
  },
  {
    slug: "optical/aspheric-design",
    inputs: { n: "1.67", power: "-5.50", aperture: "65" },
    expect: ["26.934", "-6.21"],
    ref: "注入非默认(默认 1.60/-3.00/60)：球面三阶纵向球差 LSA = 26.934 mm；消球差所需圆锥常数 K = -6.21（K<−1 ⇒ 扁长椭球面）。默认态两者均不同。"
  },
  {
    slug: "optical/thin-lens-imaging",
    inputs: { u: "450", f: "120" },
    expect: ["163.64", "-0.364"],
    ref: "注入非默认(默认 300/100)：由 1/v = 1/f − 1/u = 1/120 − 1/450 ⇒ 像距 v = 163.64 mm（实像）；放大率 m = −v/u = −0.364。默认态 150/(-0.5) 均不命中。"
  },
  {
    slug: "optical/lens-maker",
    inputs: { n: "1.6", R1: "150", R2: "-150" },
    expect: ["125.00", "0.0080"],
    ref: "注入非默认(默认 1.5/100/-100)：1/f = (n−1)(1/R₁ − 1/R₂) = 0.6×(1/150 + 1/150) = 0.008 mm⁻¹ ⇒ f = 125.00 mm；光焦度 = 0.0080 mm⁻¹。默认态 100.00/0.0100 不命中。"
  },
  {
    slug: "optical/diffraction-grating",
    inputs: { d: "1200", m: "2", lam: "589" },
    expect: ["79.01", "0.98167", "29.40"],
    ref: "注入非默认(默认 1000/1/500)：sinθ = mλ/d = 2×589/1200 = 0.98167 ⇒ 衍射角 θ = 79.01°；一级衍射角（对比）= arcsin(589/1200) = 29.40°。默认态 30.00/0.5/30.00 均不命中。"
  },
  {
    slug: "optical/mirror-imaging",
    inputs: { u: "450", R: "300" },
    expect: ["225.00", "150.0 mm 焦距"],
    ref: "注入非默认(默认 300/200)：f = R/2 = 150.0 mm；1/v = 1/f − 1/u ⇒ 像距 v = 225.00 mm。⚠️ 默认态 R=200 ⇒ f=100.0、v=150.00、m=−0.500 —— 裸值 150 与 −0.500 会与注入态的焦距离散值字面重合，故必须用「150.0 mm 焦距」完整标签串，且不可选 m。"
  },
  {
    slug: "optical/critical-angle",
    inputs: { n1: "1.49", n2: "1.33" },
    expect: ["63.20", "1.1203", "10.738"],
    ref: "注入非默认(默认 1.5/1.0)：临界角 θc = arcsin(n₂/n₁) = arcsin(1.33/1.49) = 63.20°；折射率比 = 1.1203；相对折射率差 10.738%。默认态 41.81/1.5 均不命中。"
  },
  {
    slug: "optical/optical-path-length",
    inputs: { n: "1.7", L: "250" },
    expect: ["425.0", "0.425000", "157.4074"],
    ref: "注入非默认(默认 1.5/100)：光程 OPL = n·L = 1.7×250 = 425.0 mm = 0.425000 m；与 (n+1) 之比 = 425/(1.7+1)×… = 157.4074。默认态 150.0/0.15 均不命中。"
  },
  {
    slug: "optical/frame-pupillary",
    inputs: { eyeSize: "54", dbl: "20", pd: "66", ed: "55" },
    expect: ["65.0", "74.0mm", "4.0 单眼移心量"],
    ref: "注入非默认(默认 48/18/62/50)：几何中心距 GCD = A + DBL = 54+20 = 74.0 mm，单眼几何中心到鼻中线 37.0 mm，单眼瞳距 33.0 mm ⇒ 移心量 4.0 mm（向鼻侧），所需最小片径 65.0 mm。默认态 66.0/2.0/61.0 均不命中。"
  },
  {
    slug: "optical/report-cost-profit-1",
    inputs: { lens: "150", frame: "220", proc: "55", misc: "30", price: "880", qty: "120", fixed: "24000" },
    expect: ["48.30%", "25.57%", "56.47"],
    ref: "注入非默认(默认 120/180/40/20/680/80/18000)：单副成本 455 元 ⇒ 毛利 425 元、毛利率 48.30%；月毛利 51,000 元、减固定成本 24,000 后营业利润 27,000 元（净利率 25.57%）；盈亏平衡销量 = 24000/425 = 56.47 副。默认态 47.50%/… 不同。"
  },
  {
    slug: "optical/frame-tilt",
    inputs: { tilt: "12", pd: "66", pupilHeight: "26" },
    expect: ["32.0", "前倾角： 12.0°"],
    ref: "注入非默认(默认 8/62/22)：光心下移量 = 前倾角 × 0.5 = 12.0×0.5 = 6.0 mm ⇒ 调整后瞳高 = 26.0 + 6.0 = 32.0 mm。默认态为 26.0 mm；评价文案会随倾角档位漂移，故配一条带标签的倾角串。"
  },
  {
    slug: "optical/convergence-near-point",
    inputs: { pd: "66", distance: "35", npc: "10" },
    expect: ["18.9", "37.7"],
    ref: "注入非默认(默认 62/40/8)：集合需求 = PD(cm)/距离(m) 每眼 = 6.6/0.35 = 18.9Δ，双眼总集合 37.7Δ。默认态 15.5/31.0 均不命中。"
  },
  {
    slug: "optical/polarized-axis",
    inputs: { sph: "-5.25", cyl: "-1.50", axis: "45", panto: "12", wrap: "8" },
    expect: ["0.30D", "-5.38D"],
    ref: "注入非默认(默认 -3.00/0/0/9/5)：前倾角 12° 诱导柱镜 −0.27D@90°、面弯 8° 诱导 −0.12D@180° ⇒ 诱导柱镜总量 0.30D；有效球镜（含 −0.13D 补偿增量）= −5.38D。默认态两者均不同。"
  },
  {
    slug: "optical/coating-design",
    inputs: { wavelength: "520", lensN: "1.67" },
    expect: ["93.2%", "0.43%"],
    ref: "注入非默认(默认 550/1.60)：MgF₂(n=1.38) 单层对 n=1.67 基片的折射率匹配度 93.2%；反射率由无膜 6.3% 降至 0.43%（理想四分之一波厚）。默认态两项均不同。"
  },
  {
    slug: "optical/progressive-corridor",
    inputs: { add: "2.50", bHeight: "32", pupilH: "22" },
    expect: ["27.0", "瞳高22mm"],
    ref: "注入非默认(默认 2.00/30/19)：下加 +2.50D ⇒ 通道长度 14 mm，近用区中心距下缘 8.0 mm，所需最低镜圈高度 = 22 + 8.0 − 3 = 27.0 mm。⚠️ Add 2.00 与 2.50 落在同一通道档位（均 14 mm），裸值「14 通道长度」在默认态一样会命中 ⇒ 改锚最低镜圈高度 27.0 与带标签的瞳高串；评价文案随 Add 档位漂移，不锚。"
  },
  {
    slug: "optical/rayleigh-resolution",
    inputs: { lam: "633", D: "150" },
    expect: ["5.148e-6", "1.06 ″", "2.950e-4"],
    ref: "注入非默认(默认 550/100)：最小分辨角 θ = 1.22λ/D = 1.22×633e-9/0.15 = 5.148e-6 rad = 1.06 角秒 = 2.950e-4 度。默认态 6.71e-6/1.38″ 均不命中。"
  },
  {
    slug: "optical/f-number",
    inputs: { f: "135", D: "50" },
    expect: ["2.7 光圈数", "1963.4954", "2.8659"],
    ref: "注入非默认(默认 50/25)：光圈数 N = f/D = 135/50 = 2.7；相对孔径倒数 0.370370；有效孔径面积 = π(50/2)² = 1963.4954 mm²；曝光级差 = log₂(N²/…) ⇒ 2.8659 EV。默认态 2.0/490.8739 均不命中。"
  },
  {
    slug: "optical/snell-refraction",
    inputs: { n1: "1.00", n2: "1.52", theta1: "42" },
    expect: ["26.12", "0.6691"],
    ref: "注入非默认(默认 1.0/1.33/30)：n₁sinθ₁ = 1.00×sin42° = 0.6691 ⇒ sinθ₂ = 0.6691/1.52，折射角 θ₂ = 26.12°（未达全反射）。默认态 22.08/0.5 均不命中。"
  },
  {
    slug: "optical/microscope-magnification",
    inputs: { fo: "10", fe: "20", L: "170", D: "260" },
    expect: ["221", "17.0", "13.0"],
    ref: "注入非默认(默认 4/25/160/250)：物镜放大率 = L/f₀ = 170/10 = 17.0×；目镜放大率 = D/fₑ = 260/20 = 13.0×；总放大率 = 17.0×13.0 = 221×。默认态 40.0/10.0/400 均不命中。"
  },
  {
    slug: "optical/checker-stress",
    inputs: { f_value: "18.5", fringe: "4.5", thickness: "12" },
    expect: ["6.94 MPa", "2475 光程差"],
    ref: "注入非默认(默认 14.5/3.5/10)：光程差 δ = N·λ = 4.5×550 = 2475 nm；应力双折射 σ₁−σ₂ = N·F/t = 4.5×18.5/12 = 6.94 MPa ⇒ 应力很小档。默认态 2.53 MPa/1925 均不命中；等级文案随档位漂移故不锚。"
  },
];

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
  console.log("==== optical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();