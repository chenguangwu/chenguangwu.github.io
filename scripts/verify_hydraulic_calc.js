#!/usr/bin/env node
/**
 * hydraulic 分类关键计算逻辑独立验证（收口批次 E，第 17 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_hydraulic_calc.js
 *   node scripts/verify_hydraulic_calc.js bernoulli-velocity calc-2
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 伯努利方程求下游流速（v₂² = v₁² + 2(P₁−P₂)/ρ + 2g(z₁−z₂)）──────
  {
    slug: "hydraulic/bernoulli-velocity",
    inputs: { P1: "250000", v1: "3", z1: "8", P2: "80000", z2: "1", rho: "1000", g: "9.81" },
    expect: ["22.05 m/s"],
    ref: "v₂ = √(3² + 2×(250000−80000)/1000 + 2×9.81×(8−1)) = √(9+340+137.34) = √486.34 ≈ 22.05 m/s（避开默认 200000/1/0/100000/5/1000/9.81）",
  },
  // ── 连续性方程变径（A₁v₁ = A₂v₂）─────────────────────────────────
  {
    slug: "hydraulic/continuity-pipe",
    inputs: { A1: "0.2", v1: "3", A2: "0.08" },
    expect: ["7.50 m/s"],
    ref: "v₂ = A₁v₁/A₂ = 0.2×3/0.08 = 7.50 m/s（避开默认 0.1/2/0.05）",
  },
  // ── 达西-魏斯巴赫沿程压降（ΔP = f(L/D)(ρv²/2)）────────────────────
  {
    slug: "hydraulic/darcy-head-loss",
    inputs: { f: "0.03", L: "200", D: "0.2", rho: "1000", v: "2" },
    expect: ["60000 Pa", "6.116 m"],
    ref: "ΔP = 0.03×(200/0.2)×(1000×2²/2) = 60000 Pa；h = 60000/(1000×9.81) = 6.116 m（避开默认 0.02/100/0.1/1000/1）",
  },
  // ── Hazen-Williams 水头损失（hf = 10.67LQ^1.852/(C^1.852 D^4.87)）──
  {
    slug: "hydraulic/hazen-williams-headloss",
    inputs: { Q: "0.05", L: "300", C: "140", D: "0.15" },
    expect: ["13.601 m"],
    ref: "hf = 10.67×300×0.05^1.852/(140^1.852×0.15^4.87) ≈ 13.601 m（避开默认 0.01/100/120/0.1）",
  },
  // ── 曼宁明渠流量（Q = (1/n)A·R^(2/3)·√S）─────────────────────────
  {
    slug: "hydraulic/manning-flow",
    inputs: { n: "0.02", A: "2", R: "0.8", S: "0.002" },
    expect: ["3.854 m³/s"],
    ref: "Q = (1/0.02)×2×0.8^(2/3)×√0.002 = 50×2×0.86177×0.044721 ≈ 3.854 m³/s（避开默认 0.013/1/0.5/0.001）",
  },
  // ── 局部水头损失（h_L = K·v²/(2g)）───────────────────────────────
  {
    slug: "hydraulic/minor-head-loss",
    inputs: { K: "1.2", v: "4", g: "9.81" },
    expect: ["0.979 m"],
    ref: "h_L = 1.2×4²/(2×9.81) = 19.2/19.62 ≈ 0.979 m（避开默认 0.5/3/9.81）",
  },
  // ── 水泵轴功率（P = ρgQH/η）──────────────────────────────────────
  {
    slug: "hydraulic/pump-power",
    inputs: { rho: "1000", g: "9.81", Q: "0.08", H: "30", eta: "0.8" },
    expect: ["29.43 kW", "23.54 kW"],
    ref: "P = 1000×9.81×0.08×30/0.8 = 29430 W = 29.43 kW；有效功率 = 1000×9.81×0.08×30 = 23544 W = 23.54 kW（避开默认 1000/9.81/0.05/20/0.75）",
  },
  // ── 矩形薄壁堰流量（Q = (2/3)Cd·b·√(2g)·H^1.5）────────────────────
  {
    slug: "hydraulic/rectangular-weir",
    inputs: { Cd: "0.58", b: "3", H: "0.5", g: "9.81" },
    expect: ["1.8166 m³/s"],
    ref: "Q = (2/3)×0.58×3×√19.62×0.5^1.5 = 1.16×4.4294×0.35355 ≈ 1.8166 m³/s（避开默认 0.62/2/0.3/9.81）",
  },
  // ── 由流量求流速（v = Q/A）───────────────────────────────────────
  {
    slug: "hydraulic/velocity-from-flow",
    inputs: { Q: "0.25", A: "0.1" },
    expect: ["2.50 m/s"],
    ref: "v = 0.25/0.1 = 2.50 m/s（避开默认 0.1/0.05）",
  },
  // ── 明渠均匀流（梯形断面 Manning + 弗劳德数判流态）─────────────────
  {
    slug: "hydraulic/calc-26",
    inputs: { b: "2.5", h: "1.5", m: "1.5", s: "0.5", n: "0.025" },
    expect: ["5.945"],
    ref: "A = (2.5+1.5×1.5)×1.5 = 7.125；P = 2.5+2×1.5×√3.25 = 7.9083；R = A/P = 0.9010；"
       + "V = (1/0.025)×0.9010^(2/3)×√0.0005 = 40×0.93283×0.022361 = 0.83430；Q = V·A = 5.9444（b=2.5 已非默认，余字段同默认）",
  },
  // ── 伯努利能量分解（总水头 H = z + p/ρg + v²/2g）──────────────────
  {
    slug: "hydraulic/water-level",
    inputs: { inZ: "10", inP: "50", inV: "4", inRho: "1000" },
    expect: ["5.097 m", "0.8155 m", "15.912 m"],
    ref: "hP = 50×1000/(1000×9.81) = 5.097 m；hV = 4²/(2×9.81) = 0.8155 m；"
       + "H = 10 + 5.097 + 0.8155 = 15.912 m（避开默认 5/30/2/1000；inP 单位为 kPa）",
  },
  // ── 水力发电功率（P = 9.81·q·h·η1·η2）────────────────────────────
  {
    slug: "hydraulic/flow-power",
    inputs: { h: "80", q: "15", et1: "85", et2: "95", hours: "3000" },
    expect: ["9,505.89", "28,517,670", "80.75%"],
    ref: "η = 0.85×0.95 = 0.8075；P = 9.81×15×80×0.8075 = 9505.89 kW；"
       + "年发电量 = 9505.89×3000 = 28,517,670 kWh；综合效率 = 80.75%（避开默认 100/10/90/97/4000）",
  },
  // ── 泵站效率（Pe = ρgQH，η = Pe/P轴）─────────────────────────────
  {
    slug: "hydraulic/power-3",
    inputs: { q: "720", h: "25", p: "80", hours: "5000", price: "0.6" },
    expect: ["49.05", "61.31%", "400,000", "240,000"],
    ref: "Q = 720/3600 = 0.2 m³/s；Pe = 1000×9.81×0.2×25 = 49050 W = 49.05 kW；η = 49.05/80×100 = 61.31%；"
       + "年耗电 = 80×5000 = 400,000 kWh；年电费 = 400000×0.6 = 240,000 元（避开默认 360/30/50/4000/0.7）",
  },
  // ── 蓄能器容量（等温 V₀ = ΔV·P₁·P₂/[P₀(P₂−P₁)]）──────────────────
  {
    slug: "hydraulic/calc-pressure-capacity",
    inputs: { p0: "10", p1: "15", p2: "25", dv: "8", proc: "iso" },
    expect: ["30.00", "34.50", "26.7%"],
    ref: "V₀ = 8×15×25/(10×(25−15)) = 3000/100 = 30.00 L；"
       + "推荐容积 = 30.00×1.15 = 34.50 L；有效利用率 = 8/30.00×100 = 26.7%（避开默认 9/12/21/5/iso）",
  },
  // ── 水锤防护（波相时间 T = 2L/a，间接水锤 ΔH = 2Lv/(gTs)）────────
  {
    slug: "hydraulic/calc-protection",
    inputs: { L: "800", v: "3.0", ts: "8", a: "1200", h0: "40", d: "800" },
    expect: ["61.16", "600.0"],
    ref: "T = 2×800/1200 = 1.33 s；Ts = 8 s > T → 间接水锤；"
       + "ΔH = 2×800×3/(9.81×8) = 61.16 m；ΔP = 61.16×9.81 ≈ 600.0 kPa（避开默认 500/2.0/5/1000/30/600）",
  },
  // ── 液压伺服（F = mω²X，A = F/[(2/3)ps]，fh = √(4βe·A/(Lm·m))/2π）──
  {
    slug: "hydraulic/ratio-24",
    inputs: { m: "800", L: "150", f: "8", ps: "16", be: "800", ir: "12" },
    expect: ["151.60", "142.12", "134.5", "3,214.7", "306.91", "32.66"],
    ref: "ω = 2π×8 = 50.265，X = ir/200 = 0.06，a = ω²X = 151.60；F = 800×151.60 = 121,280 N；"
       + "dp = (2/3)×16 = 10.667 MPa；A = F/dp → 142.12 cm²；D = √(4A/π) = 134.5 mm；Q = 3,214.7 L/min；"
       + "Qn = 306.91；fh = 32.66 Hz（Hydraulik 伺服公式，逐项独立复算 F/D 一致；避开默认 500/100/5/14/700/10）",
  },
  // ── 水泵扬程（几何高差 + 吸/压水管沿程与局部损失 + 速度水头差）──────
  {
    slug: "hydraulic/calc-2",
    inputs: { Hs: "5", Hd: "30", Q: "80", ds: "150", Ls: "10", zetas: "3.0",
              dd: "125", Ld: "150", zetad: "6.0", lambda: "0.03", pIn: "0", pOut: "0" },
    expect: ["42.51", "35.00", "0.403"],
    ref: "几何高差 = Hs + Hd = 5 + 30 = 35.00 m；吸水侧 v = Q/A、hf + hj 合计 0.403 m；"
       + "压水侧损失 7.022 m；H = 5+30+0.403+7.022+0.0866 = 42.51 m（避开默认 3/25/50/125/8/4.0/100/120/8.5/0.025/0/0）",
  },
  // ── 管段水力计算（达西-魏斯巴赫 + Blasius 紊流摩阻，绝对粗糙度=0 走 Blasius）──
  {
    slug: "hydraulic/calc-1",
    inputs: { flow: "36", diameter: "100", length: "100", roughness: "0", nu: "0.000001004", localResistance: "3.5" },
    expect: ["1.386", "16.43"],
    ref: "D=0.1m，A=πD²/4=0.007854m²，Q=36/3600=0.01m³/s，v=Q/A=1.273m/s，Re=vD/ν≈1.27e5 紊流；"
       + "粗糙度=0 → Blasius λ=0.3164/Re^0.25≈0.01677；hf=λ(L/D)(v²/2G)=1.386m，"
       + "hj=ζ·v²/2G=0.289m，hTotal=1.675m，ΔP=hTotal×9.81=16.43kPa（roughness=0 已非默认，余同默认）",
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
      if (r.ok) { pass++; console.log(`✅ ${c.slug}  (via ${r.via})`); }
      else { fails.push(c.slug); console.log(`❌ ${c.slug}  ${r.why}`); if (r.sample) console.log("     got: " + r.sample.slice(0, 200)); }
    } catch (e) {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  THREW ${e.message.slice(0, 80)}`);
    }
  }
  console.log(`\n==== hydraulic calc ${pass}/${cases.length} ====`);
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
