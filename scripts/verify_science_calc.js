#!/usr/bin/env node
/**
 * science 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）。
 * 用例以物理 / 化学 / 统计的确定公式为主，期望值一律由标准公式独立复算得出，不凭记忆。
 *
 * 用法：
 *   node scripts/verify_science_calc.js                       # 跑全部用例
 *   node scripts/verify_science_calc.js newtons-second molar-mass-calculator  # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  // ── 经典力学 ─────────────────────────────────────────────────
  {
    slug: "science/newtons-second",
    inputs: { m: "10", a: "3" },
    expect: ["30.0 N"],
    ref: "牛顿第二定律 F = m·a；10 × 3 = 30 → 30.0 N（页面 toFixed(1)）",
  },
  {
    slug: "science/kinetic-energy",
    inputs: { m: "10", v: "5" },
    expect: ["125.0 J"],
    ref: "动能 E = ½mv²；0.5 × 10 × 25 = 125 → 125.0 J（页面 toFixed(1)）",
  },
  {
    slug: "science/pendulum-period",
    inputs: { L: "1", g: "9.81" },
    expect: ["2.006 s"],
    ref: "单摆周期 T = 2π√(L/g)；2π√(1/9.81) = 2.0064… → 2.006 s（页面 toFixed(3)）",
  },

  // ── 电学（欧姆定律）─────────────────────────────────────────
  {
    slug: "science/ohms-law-calculator",
    inputs: { v: "10", r: "5" }, // calcVar 默认 'i'（求解电流）
    expect: ["2.00 C"],
    ref: "欧姆定律 I = V/R；10 ÷ 5 = 2 A → 电荷量 Q=I=2 → 2.00 C（resQ，toFixed(2)）",
  },

  // ── 化学（摩尔质量 / pH）────────────────────────────────────
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "H2O" },
    expect: ["18.016"],
    ref: "H₂O 摩尔质量 = 1.008×2 + 16.00 = 18.016 g/mol（页面 total.toFixed(3)，O 原子量取 16.00）",
  },
  {
    slug: "science/ph-calculator",
    inputs: { ph: "3" }, // 页面真实输入 id=ph，默认模式 pH→[H⁺]
    expect: ["3.00", "1.000e-3"],
    ref: "pH=3 → [H⁺]=10⁻³=1.000e-3 mol/L；resPh=3.00、resH=1.000e-3（toFixed(2)/toExponential(3)）",
  },

  {
    slug: "science/mean-calculator",
    inputs: { data: "1,2,4" },
    expect: ["2.333"],
    ref: "算术平均 = (1+2+4)/3 = 2.333（fmt：round(x·1e10)/1e10 后 toLocaleString，默认最多 3 位小数）",
  },

  {
    slug: "science/p-value-calculator",
    inputs: { alpha: "0.05", z0: "2.5", tail0: "two" },
    expect: ["p = 0.012"],
    ref: "z=2.5 → Φ(2.5)=0.99379，双侧 p = 2×(1−Φ) = 2×min(Φ,1−Φ) = 0.01242，fmt 显示 p = 0.012 并判定拒绝 H₀。原实现 2(1−|Φ−0.5|) 得 1.0124（p>1）且误判不拒绝",
  },

  {
    slug: "science/chi-square-calculator",
    inputs: { obs: "35, 25, 25, 15" },
    expect: ["p = 0.046"],
    ref: "O=[35,25,25,15]、E 留空 → 等概率 E=25：χ² = Σ(O−E)²/E = 4+0+0+4 = 8，df = k−1 = 3，右尾 p = P(χ²₃>8) = 0.0460（精确不完全 Gamma）。原 Wilson–Hilferty 近似漏括号得 p≈0.604（χ²=12.5/df=4 更极端：0.994 vs 真值 0.014）",
  },
  // ── 效应量（Cohen's d → U₃）──────────────────────────────────
  {
    slug: "science/effect-size-calculator",
    inputs: { m1: "112", mu0: "100", sd1: "8" }, // mode0（单样本，默认页签）
    expect: ["93.32%"],
    ref: "d = (M−μ₀)/SD = (112−100)/8 = 1.5 → Cohen's U₃ = Φ(1.5) = 0.9331928 → 93.32%（页面 toFixed(2)）。原实现把「r²」写成 d²，此例得 225% 远超 1，物理上不可能；Φ 经 Python math.erf 独立复算",
  },
  {
    slug: "science/effect-size-calculator",
    inputs: { m1: "95", mu0: "100", sd1: "10" },
    expect: ["30.85%"],
    ref: "d = (95−100)/10 = −0.5 → Φ(−0.5) = 0.3085375 → 30.85%；d 为负时百分位必须 <50%（不得对 d 取绝对值），Python math.erf 独立复算",
  },

  // ── 陨石撞击坑（CMM 标度律 + 千吨当量）─────────────────────
  {
    slug: "science/meteor-crater-estimator",
    inputs: { meteorDiameter: "50", meteorVelocity: "13", meteorDensity: "7800", impactAngle: "45", targetDensity: "2700", targetType: "sedimentary" }, // 巴林杰陨石坑参数
    expect: ["1.22 km", "202.9 m", "5.91 km"],
    ref: "CMM 瞬态坑 D=1.161(ρi/ρt)^(1/3)·L^0.78·v^0.44·g^-0.22·sin^(1/3)45° = 1.161×(7800/2700)^(1/3)×50^0.78×13000^0.44×9.80665^-0.22×0.8909 = 1217 m → 1.22 km（巴林杰坑实测 1.186 km）；深度 1217/6 = 202.9 m；E=4.314e16 J → 10312 kt → 20psi 半径 0.28×10312^0.33 = 5.91 km。原实现 D=0.07(E/ρ)^(1/4) 仅得 0.12 km（偏小 10 倍）、破坏半径误代入「吨」高估 10 倍",
  },

  // ── 样本量（E 按百分比输入）────────────────────────────────
  {
    slug: "science/sample-size-calculator",
    inputs: { N: "5000", conf: "0.99", e: "3", p: "0.4" },
    expect: ["推荐样本量 n = 1308"],
    ref: "E=3% → 0.03；z*=2.5758；n₀=6.6349×0.4×0.6/0.0009=1769.306 → 无限总体 1770；有限修正 1769.306/(1+1768.306/5000)=1307.052 → 1308。原实现直接以 E=3 代入（未 /100）→ 默认态算出 n=1",
  },

  // ── 星等亮度比（方向性）────────────────────────────────────
  {
    slug: "science/star-magnitude-compare",
    inputs: { mag1: "6.0", mag2: "1.0" },
    expect: ["星等2 (1) 的天体更亮，亮度是星等1的 100.02 倍"],
    ref: "Δm=m2−m1=−5，F₁/F₂=2.512^(−5)=1/100.02 ⇒ 星等2 更亮 100.02 倍（星等越小越亮）。原实现两分支方向写反，此处会答成「星等1 更亮」",
  },
  {
    slug: "science/star-magnitude-compare",
    inputs: { mag1: "-1.46", mag2: "0.03" }, // 天狼星 vs 织女星
    expect: ["星等1 (-1.46) 的天体更亮，亮度是星等2的 3.94 倍"],
    ref: "Δm=0.03−(−1.46)=1.49，F₁/F₂=2.512^1.49=3.94 ⇒ 天狼星（星等更小）更亮 3.94 倍",
  },

  // ── 密度（kg/m³ 取值精度 + lb/ft³ 换算）────────────────────
  {
    slug: "science/density-physics",
    inputs: { m: "0.003", V: "0.0012" },
    expect: ["2.500 kg/m³", "0.400000"],
    ref: "ρ=0.003/0.0012=2.5 kg/m³（原实现 rho.toFixed(0) 会显示为 3）；比容 1/ρ=0.4 m³/kg → 0.400000",
  },
  {
    slug: "science/density-physics",
    inputs: { m: "1.5", V: "0.0006" },
    expect: ["156.070", "2.500000"],
    ref: "ρ=2500 kg/m³ → lb/ft³ = 2500×0.062428 = 156.070（新增卡片，替代原无意义的 V/ρ「m⁶/kg」）；g/cm³ = 2500/1000 = 2.5 → 2.500000",
  },

  // ── 物理单位换算（默认同量纲）───────────────────────────────
  {
    slug: "science/convert-power",
    inputs: { val: "1", from: "N", to: "lbf" },
    expect: ["0.224809"],
    ref: "1 N = 0.2248089 lbf（1 lbf = 4.448222 N）。原默认 from=牛顿（力）/ to=公制马力（功率）量纲不同 ⇒ 打开即显示「请选择同量纲单位」，已把默认改为同类。注：harness 的 select 桩取首个 option，故默认态需显式注入 to 才能验证",
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
  console.log("==== science calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();