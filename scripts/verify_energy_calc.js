#!/usr/bin/env node
/**
 * energy 分类关键计算逻辑独立验证（收口批次 D，第 21 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式「独立复算」得出（不回读页面输出），并在 ref 中写明完整算式。
 *
 * 数字格式（决定期望值长相，断言必须按真实输出写）：
 *   - 本分类绝大多数页面直接用 toFixed(d)，无千分位（与 realestate 的
 *     ToolBox.formatNumber 千分位不同），例如 heat-energy-q 输出 "334880.00"；
 *   - carbon-footprint 用 total.toFixed(0)，输出 "5980"（不带千分位逗号）。
 *
 * 未纳入的两类（均非 energy 专属计算逻辑，不属于本门禁职责）：
 *   - power-consumption / standby-power-calculator：电器条目由用户动态增删，
 *     初始 appliances 为空，calc() 直接 toast 报错返回，无默认可断言输出；
 *   - energy-calculator：6 合 1 多标签页，各子计算器与单页工具同源码，
 *     入口依赖 tab 切换，验证它等于重复验证单页工具。
 *
 * 用法：
 *   node scripts/verify_energy_calc.js
 *   node scripts/verify_energy_calc.js carnot-efficiency lcoe
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 电功率 P = U × I ────────────────────────────────────────────
  {
    slug: "energy/electrical-power",
    inputs: { U: "12", I: "2" },
    expect: ["24.00"],
    ref: "P = U×I = 12×2 = 24.00 W",
  },

  // ── 耗电量与电费 E = P×t/1000；电费 = E×单价 ──────────────────────
  {
    slug: "energy/energy-consumption",
    inputs: { p: "1500", t: "3", price: "0.6" },
    expect: ["4.50", "2.70"],
    ref: "E = 1500×3/1000 = 4.50 kWh；电费 = 4.50×0.6 = 2.70 元",
  },

  // ── 电费 = P(kW)×h×单价 ─────────────────────────────────────────
  {
    slug: "energy/energy-cost",
    inputs: { P: "1500", h: "24", rate: "0.6" },
    expect: ["21.60"],
    ref: "费用 = 1500/1000×24×0.6 = 21.60 元",
  },

  // ── 电能 E = P×t（kWh） ─────────────────────────────────────────
  {
    slug: "energy/energy-from-power",
    inputs: { P: "1000", t: "2" },
    expect: ["2.000"],
    ref: "E = 1000/1000×2 = 2.000 kWh",
  },

  // ── 电池容量 Wh = Ah × V；续航 = Wh / 负载 ────────────────────────
  {
    slug: "energy/battery-capacity-wh",
    inputs: { ah: "50", v: "12", load: "100" },
    expect: ["600", "6.00", "360"],
    ref: "Wh = 50×12 = 600；续航 = 600/100 = 6.00 h = 360 min",
  },

  // ── 电池续航（mAh → Wh，含效率） ─────────────────────────────────
  {
    slug: "energy/battery-life",
    inputs: { capacity: "4000", voltage: "3.7", power: "2", efficiency: "85" },
    expect: ["14.80", "12.58", "6时 17分"],
    ref: "Wh = 4000×3.7/1000 = 14.80；可用 = 14.80×0.85 = 12.58；续航 = 12.58/2 = 6.29 h = 6 时 17 分（377 分钟）",
  },

  // ── 卡诺效率 η = 1 − Tc/Th ──────────────────────────────────────
  {
    slug: "energy/carnot-efficiency",
    inputs: { Tc: "300", Th: "600" },
    expect: ["50.00"],
    ref: "η = 1 − 300/600 = 0.5 → 50.00%",
  },

  // ── 导热热流率 Q̇ = k·A·ΔT/d ───────────────────────────────────
  {
    slug: "energy/conductive-heat-rate",
    inputs: { k: "0.04", A: "10", dT: "20", d: "0.2" },
    expect: ["40.00"],
    ref: "Q̇ = 0.04×10×20/0.2 = 40.00 W",
  },

  // ── 热泵 COP = Q/W；节电率 = (Q−W)/Q ────────────────────────────
  {
    slug: "energy/cop-heatpump",
    inputs: { q: "4000", w: "1000" },
    expect: ["4.00", "75.0"],
    ref: "COP = 4000/1000 = 4.00；节电率 = (4000−1000)/4000×100 = 75.0%",
  },

  // ── 日辐照量 = 峰值 × 等效日照时数 / 1000 ─────────────────────────
  {
    slug: "energy/daily-irradiation",
    inputs: { g: "1000", t: "4.5" },
    expect: ["4.50"],
    ref: "日辐照量 = 1000×4.5/1000 = 4.50 kWh/m²",
  },

  // ── 能量密度 = E/m（kJ/kg 与 kWh/kg） ──────────────────────────
  {
    slug: "energy/energy-density",
    inputs: { e: "3600000", m: "10" },
    expect: ["360.0", "0.1000"],
    ref: "E/m = 3600000/10 = 360000 J/kg = 360.0 kJ/kg = 0.1000 kWh/kg（1 kWh = 3.6 MJ）",
  },

  // ── 投资回收期 = 投资/年节约；年回报率 = 年节约/投资 ────────────────
  {
    slug: "energy/energy-payback",
    inputs: { inv: "30000", save: "6000" },
    expect: ["5.00", "20.0"],
    ref: "回收期 = 30000/6000 = 5.00 年；年回报率 = 6000/30000×100 = 20.0%",
  },

  // ── 太阳能年发电量 = 面积×日照×365×组件效率×系统效率 ────────────────
  {
    slug: "energy/estimate-area",
    inputs: { area: "30", sunHours: "4", moduleEff: "20", sysEff: "80", price: "0.40" },
    expect: ["7008", "19.2"],
    ref: "年发电量 = 30×4×365×0.20×0.80 = 7008 kWh；日均 = 7008/365 = 19.2 kWh",
  },

  // ── 燃料费用 = 用量×单价；单位里程费用 = 总费/里程 ──────────────────
  {
    slug: "energy/fuel-cost",
    inputs: { q: "50", price: "8", dist: "600" },
    expect: ["400.00", "0.67"],
    ref: "费用 = 50×8 = 400.00 元；单位里程 = 400/600 = 0.67 元/km",
  },

  // ── 燃料热值能量 Q = m × 低位热值 ───────────────────────────────
  {
    slug: "energy/fuel-heat-value",
    inputs: { m: "1000", h: "42000" },
    expect: ["42000.0", "11.667"],
    ref: "Q = 1000×42000 = 42,000,000 J = 42000.0 MJ = 11.667 kWh",
  },

  // ── 热量 Q = m·c·ΔT ───────────────────────────────────────────
  {
    slug: "energy/heat-energy-q",
    inputs: { m: "1", c: "4186", dT: "80" },
    expect: ["334880.00"],
    ref: "Q = 1×4186×80 = 334880.00 J（1 kg 水升温 80 K）",
  },

  // ── 热泵 COP（制热分支默认） = 制热量/输入功率 ────────────────────
  {
    slug: "energy/heat-pump-cop",
    inputs: { heatOutput: "12", copInput: "3.5" },
    expect: ["3.43"],
    ref: "COP = 12/3.5 = 3.43",
  },

  // ── 焦耳热 P = I²·R ───────────────────────────────────────────
  {
    slug: "energy/joule-heating",
    inputs: { I: "2", R: "5" },
    expect: ["20.00"],
    ref: "P = 2²×5 = 20.00 W",
  },

  // ── LCOE：CRF = r(1+r)^n/((1+r)^n−1)；LCOE = (C·CRF+OM)/E ──────
  {
    slug: "energy/lcoe",
    inputs: { capex: "5000000", n: "20", r: "0.06", om: "100000", e: "1200000" },
    expect: ["0.447", "0.0872"],
    ref: "CRF = 0.06×1.06^20/(1.06^20−1) = 0.0872；LCOE = (5,000,000×0.0872+100,000)/1,200,000 = 0.447 元/kWh",
  },

  // ── 功率因数 PF = P/S；相位角 φ = acos(PF) ──────────────────────
  {
    slug: "energy/power-factor-calc",
    inputs: { p: "800", s: "1000" },
    expect: ["0.800", "36.87"],
    ref: "PF = 800/1000 = 0.800；φ = acos(0.8)×180/π = 36.87°",
  },

  // ── 热阻 R = d/k ──────────────────────────────────────────────
  {
    slug: "energy/r-value-insulation",
    inputs: { d: "0.2", k: "0.04" },
    expect: ["5.000"],
    ref: "R = 0.2/0.04 = 5.000 m²·K/W",
  },

  // ── 光伏输出功率 P = A·G·η ─────────────────────────────────────
  {
    slug: "energy/solar-output-physics",
    inputs: { A: "10", G: "1000", eta: "0.2" },
    expect: ["2000.00"],
    ref: "P = 10×1000×0.2 = 2000.00 W",
  },

  // ── 光伏阵列功率（同时给出 kW 与 W） ──────────────────────────────
  {
    slug: "energy/solar-panel-power",
    inputs: { a: "20", g: "1000", eta: "0.2" },
    expect: ["4.00", "4000"],
    ref: "P = 20×1000×0.2 = 4000 W = 4.00 kW",
  },

  // ── 比能量 = E/m ──────────────────────────────────────────────
  {
    slug: "energy/specific-energy",
    inputs: { E: "3600000", m: "10" },
    expect: ["360000"],
    ref: "比能量 = 3600000/10 = 360000 J/kg",
  },

  // ── 热效率 = 输出/输入；损失率 = 1 − 效率 ────────────────────────
  {
    slug: "energy/thermal-efficiency",
    inputs: { out: "300", in: "1000" },
    expect: ["30.00", "70.00"],
    ref: "η = 300/1000×100 = 30.00%；损失率 = 70.00%",
  },

  // ── 三相功率 P = √3·U·I·cosφ ──────────────────────────────────
  {
    slug: "energy/three-phase-power",
    inputs: { u: "380", i: "100", pf: "0.9" },
    expect: ["59.24"],
    ref: "P = √3×380×100×0.9 = 59236.1 W = 59.24 kW",
  },

  // ── 风能功率 P = ½·ρ·A·v³ ────────────────────────────────────
  {
    slug: "energy/wind-power-physics",
    inputs: { rho: "1.225", A: "10", v: "10" },
    expect: ["6125.00"],
    ref: "P = 0.5×1.225×10×10³ = 6125.00 W",
  },

  // ── 风力机功率（含风能利用系数 Cp） ──────────────────────────────
  {
    slug: "energy/wind-power-estimator",
    inputs: { windSpeed: "12", bladeRadius: "40", airDensity: "1.225", cpValue: "0.40" },
    expect: ["2128039", "5026.5"],
    ref: "A = π×40² = 5026.5 m²；P = 0.5×1.225×5026.5×12³×0.40 = 2128039 W",
  },

  // ── 噪声分贝叠加 L = 10·log₁₀(Σ10^(Li/10)) ─────────────────────
  {
    slug: "energy/calculator-calc-4",
    inputs: { data: "60,60" },
    expect: ["63.01"],
    ref: "Σ10^(Li/10) = 10^6+10^6 = 2×10^6；L = 10×log₁₀(2×10^6) = 63.01 dB（两个相同声源叠加 +3.01 dB）",
  },

  // ── 热泵 COP 与能效等级 ────────────────────────────────────────
  {
    slug: "energy/calculator-calc-5",
    inputs: { capacity: "10000", power: "3000" },
    expect: ["3.33"],
    ref: "COP = 10000/3000 = 3.33（≥3.2 判二级能效）",
  },

  // ── 阶梯电费 = Σ 各档电量 × 档位电价 ────────────────────────────
  {
    slug: "energy/calculator-calc-power-usage",
    inputs: { usage: "350", tier1: "240", tier2: "400", price1: "0.50", price2: "0.55", price3: "0.80" },
    expect: ["180.50"],
    ref: "第一档 240×0.50 = 120.00；第二档 (350−240)×0.55 = 60.50；合计 180.50 元（未进入第三档）",
  },

  // ── 碳足迹 = Σ(活动量 × 排放因子) ──────────────────────────────
  {
    slug: "energy/carbon-footprint",
    inputs: {
      car_gasoline: "10000", car_electric: "0", flight: "2000", transit: "3000",
      electricity: "2400", gas: "200", water: "100", meat: "50", dairy: "30",
    },
    expect: ["5980"],
    ref: "10000×0.192 + 2000×0.255 + 3000×0.089 + 2400×0.581 + 200×2.04 + 100×0.344 + 50×27 + 30×3.2 = 5979.8 → 5980 kgCO₂e",
  },

  // ── 水质 TDS 分级（阈值分段判定，非算术） ────────────────────────
  {
    slug: "energy/assessor-water-quality",
    inputs: { tds: "150", temp: "20" },
    expect: ["良好饮用水", "273"],
    ref: "150 mg/L 落在 (100,300] → 良好饮用水；电导率估算 = TDS/0.55 = 272.7 → 273 μS/cm",
  },

  // ── 空气净化器适用面积 ≈ CADR × 系数 ───────────────────────────
  {
    slug: "energy/air-purifier-area",
    inputs: { cadrInput: "400", factorInput: "0.10" },
    expect: ["40"],
    ref: "推荐面积 = CADR×0.1 = 400×0.1 = 40 m²（最小 0.07×400 = 28，最大 0.12×400 = 48）",
  },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 300));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
