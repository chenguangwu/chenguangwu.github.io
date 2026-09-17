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
    inputs: { U: "24", I: "3" },
    expect: ["72.00"],
    ref: "P = U×I = 24×3 = 72.00 W",
  },

  // ── 耗电量与电费 E = P×t/1000；电费 = E×单价 ──────────────────────
  {
    slug: "energy/energy-consumption",
    inputs: { p: "2000", t: "5", price: "0.8" },
    expect: ["10.00", "8.00"],
    ref: "E = 2000×5/1000 = 10.00 kWh；电费 = 10.00×0.8 = 8.00 元",
  },

  // ── 电费 = P(kW)×h×单价 ─────────────────────────────────────────
  {
    slug: "energy/energy-cost",
    inputs: { P: "2500", h: "10", rate: "0.75" },
    expect: ["18.75"],
    ref: "费用 = 2500/1000×10×0.75 = 18.75 元",
  },

  // ── 电能 E = P×t（kWh） ─────────────────────────────────────────
  {
    slug: "energy/energy-from-power",
    inputs: { P: "1500", t: "3" },
    expect: ["4.500"],
    ref: "E = 1500/1000×3 = 4.500 kWh",
  },

  // ── 电池容量 Wh = Ah × V；续航 = Wh / 负载 ────────────────────────
  {
    slug: "energy/battery-capacity-wh",
    inputs: { ah: "60", v: "24", load: "120" },
    expect: ["1440", "12.00", "720"],
    ref: "Wh = 60×24 = 1440；续航 = 1440/120 = 12.00 h = 720 min",
  },

  // ── 电池续航（mAh → Wh，含效率） ─────────────────────────────────
  {
    slug: "energy/battery-life",
    inputs: { capacity: "5000", voltage: "3.6", power: "2", efficiency: "90" },
    expect: ["18.00", "16.20", "486"],
    ref: "Wh = 5000×3.6/1000 = 18.00；可用 = 18.00×90% = 16.20；续航 = 16.20/2 = 8.1000 h = 486 分钟",
  },

  // ── 卡诺效率 η = 1 − Tc/Th ──────────────────────────────────────
  {
    slug: "energy/carnot-efficiency",
    inputs: { Tc: "300", Th: "900" },
    expect: ["66.67"],
    ref: "η = 1 − 300/900 = 0.666667 → 66.67%",
  },

  // ── 导热热流率 Q̇ = k·A·ΔT/d ───────────────────────────────────
  {
    slug: "energy/conductive-heat-rate",
    inputs: { k: "0.05", A: "12", dT: "25", d: "0.15" },
    expect: ["100.00"],
    ref: "Q̇ = 0.05×12×25/0.15 = 100.00 W",
  },


  // ── 日辐照量 = 峰值 × 等效日照时数 / 1000 ─────────────────────────
  {
    slug: "energy/daily-irradiation",
    inputs: { g: "850", t: "6" },
    expect: ["5.10"],
    ref: "日辐照量 = 850×6/1000 = 5.10 kWh/m²",
  },

  // ── 能量密度 = E/m（kJ/kg 与 kWh/kg） ──────────────────────────
  {
    slug: "energy/energy-density",
    inputs: { e: "5000000", m: "20" },
    expect: ["250.0", "0.0694"],
    ref: "E/m = 5000000/20 = 250000 J/kg = 250.0 kJ/kg = 0.0694 kWh/kg（1 kWh = 3.6 MJ）",
  },

  // ── 投资回收期 = 投资/年节约；年回报率 = 年节约/投资 ────────────────
  {
    slug: "energy/energy-payback",
    inputs: { inv: "45000", save: "7500" },
    expect: ["6.00", "16.7"],
    ref: "回收期 = 45000/7500 = 6.00 年；年回报率 = 7500/45000×100 = 16.7%",
  },

  // ── 太阳能年发电量 = 面积×日照×365×组件效率×系统效率 ────────────────
  {
    slug: "energy/estimate-area",
    inputs: { area: "25", sunHours: "5", moduleEff: "21", sysEff: "75", price: "0.5" },
    expect: ["7186", "19.7"],
    ref: "年发电量 = 25×5×365×0.21×0.75 = 7186 kWh；日均 = 7186/365 = 19.7 kWh",
  },

  // ── 燃料费用 = 用量×单价；单位里程费用 = 总费/里程 ──────────────────
  {
    slug: "energy/fuel-cost",
    inputs: { q: "60", price: "7.5", dist: "500" },
    expect: ["450.00", "0.90"],
    ref: "费用 = 60×7.5 = 450.00 元；单位里程 = 450.00/500 = 0.90 元/km",
  },

  // ── 燃料热值能量 Q = m × 低位热值 ───────────────────────────────
  {
    slug: "energy/fuel-heat-value",
    inputs: { m: "2000", h: "45000" },
    expect: ["90000.0", "25.000"],
    ref: "Q = 2000×45000 = 90,000,000 J = 90000.0 MJ = 25.000 kWh",
  },

  // ── 热量 Q = m·c·ΔT ───────────────────────────────────────────
  {
    slug: "energy/heat-energy-q",
    inputs: { m: "2", c: "4200", dT: "50" },
    expect: ["420000.00"],
    ref: "Q = 2×4200×50 = 420000.00 J",
  },

  // ── 热泵 COP（制热分支默认） = 制热量/输入功率 ────────────────────
  {
    slug: "energy/heat-pump-cop",
    inputs: { heatOutput: "15", copInput: "4" },
    expect: ["3.75"],
    ref: "COP = 15/4 = 3.75",
  },

  // ── 焦耳热 P = I²·R ───────────────────────────────────────────
  {
    slug: "energy/joule-heating",
    inputs: { I: "3", R: "8" },
    expect: ["72.00"],
    ref: "P = 3²×8 = 72.00 W",
  },

  // ── LCOE：CRF = r(1+r)^n/((1+r)^n−1)；LCOE = (C·CRF+OM)/E ──────
  {
    slug: "energy/lcoe",
    inputs: { capex: "8000000", n: "25", r: "0.05", om: "150000", e: "2000000" },
    expect: ["0.359", "0.0710"],
    ref: "CRF = 0.05×1.05^25/(1.05^25−1) = 0.0710；LCOE = (8,000,000×0.0710+150,000)/2,000,000 = 0.359",
  },

  // ── 功率因数 PF = P/S；相位角 φ = acos(PF) ──────────────────────
  {
    slug: "energy/power-factor-calc",
    inputs: { p: "600", s: "800" },
    expect: ["0.750", "41.41"],
    ref: "PF = 600/800 = 0.750；φ = acos(0.750)×180/π = 41.41°",
  },

  // ── 热阻 R = d/k ──────────────────────────────────────────────
  {
    slug: "energy/r-value-insulation",
    inputs: { d: "0.3", k: "0.05" },
    expect: ["6.000"],
    ref: "R = 0.3/0.05 = 6.000 m²·K/W",
  },


  // ── 光伏阵列功率（同时给出 kW 与 W） ──────────────────────────────
  {
    slug: "energy/solar-panel-power",
    inputs: { a: "15", g: "900", eta: "0.18" },
    expect: ["2.43", "2430"],
    ref: "P = 15×900×0.18 = 2430 W = 2.43 kW",
  },


  // ── 热效率 = 输出/输入；损失率 = 1 − 效率 ────────────────────────
  {
    slug: "energy/thermal-efficiency",
    inputs: { out: "450", in: "1200" },
    expect: ["37.50", "62.50"],
    ref: "η = 450/1200×100 = 37.50%；损失率 = 62.50%",
  },

  // ── 三相功率 P = √3·U·I·cosφ ──────────────────────────────────
  {
    slug: "energy/three-phase-power",
    inputs: { u: "400", i: "50", pf: "0.85" },
    expect: ["29.44"],
    ref: "P = √3×400×50×0.85 = 29444.86 W = 29.44 kW",
  },

  // ── 风能功率 P = ½·ρ·A·v³ ────────────────────────────────────
  {
    slug: "energy/wind-power-physics",
    inputs: { rho: "1.225", A: "20", v: "8" },
    expect: ["6272.00"],
    ref: "P = 0.5×1.225×20×8³ = 6272.00 W",
  },

  // ── 风力机功率（含风能利用系数 Cp） ──────────────────────────────
  {
    slug: "energy/wind-power-estimator",
    inputs: { windSpeed: "10", bladeRadius: "30", airDensity: "1.225", cpValue: "0.35" },
    expect: ["2827.4", "606.1 kW"],
    ref: "A = π×30² = 2827.4 m²；P = 0.5×1.225×2827.4334×10³×0.35 = 606131.0 W = 606.1 kW",
  },

  // ── 噪声分贝叠加 L = 10·log₁₀(Σ10^(Li/10)) ─────────────────────
  {
    slug: "energy/calculator-calc-4",
    inputs: { data: "60,60" },
    expect: ["63.01"],
    ref: "Σ10^(Li/10) = 10^6+10^6 = 2×10^6；L = 10×log₁₀(2×10^6) = 63.01 dB（两个相同声源叠加 +3.01 dB）",
  },


  // ── 阶梯电费 = Σ 各档电量 × 档位电价 ────────────────────────────
  {
    slug: "energy/calculator-calc-power-usage",
    inputs: { usage: "500", tier1: "200", tier2: "450", price1: "0.55", price2: "0.6", price3: "0.85" },
    expect: ["302.50"],
    ref: "第一档 200×0.55 = 110.00；第二档 250×0.6 = 150.00；第三档 50×0.85 = 42.50；合计 302.50 元",
  },

  // ── 碳足迹 = Σ(活动量 × 排放因子) ──────────────────────────────
  {
    slug: "energy/carbon-footprint",
    inputs: { car_gasoline: "8000", car_electric: "2000", flight: "1500", transit: "2000", electricity: "3000", gas: "150", water: "80", meat: "40", dairy: "25" },
    expect: ["5439"],
    ref: "Σ(用量×因子) = 8000×0.192 + 2000×0.053 + 1500×0.255 + 2000×0.089 + 3000×0.581 + 150×2.04 + 80×0.344 + 40×27 + 25×3.2 = 5439 kg CO₂e",
  },

  // ── 水质 TDS 分级（阈值分段判定，非算术） ────────────────────────
  {
    slug: "energy/assessor-water-quality",
    inputs: { tds: "400", temp: "25" },
    expect: ["合格饮用水", "727"],
    ref: "400 mg/L 落在 (300,500] → 合格饮用水；电导率估算 = TDS/0.55 = 727 μS/cm",
  },

  // ── 空气净化器适用面积 ≈ CADR × 系数 ───────────────────────────
  {
    slug: "energy/air-purifier-area",
    // 系数 factorInput 已修复为真正参与计算，故用例刻意取非默认系数 0.12：
    // 若系数再次被硬编码为 0.10，本例必失败（判别力来源）
    inputs: { cadrInput: "550", factorInput: "0.12" },
    // 注意：expect 的每一项都必须依赖 recArea（被测点）。不得混入 minArea/maxArea 等
    // 只依赖 factor 本身的项 ——「任一命中即通过」下，那类项会成为逃生通道（已实测）。
    expect: ["66.0", "3.5 次"],
    ref: "推荐面积 = CADR×factor = 550×0.12 = 66.0 m²；最小 = (0.12−0.03)×550 = 49.5 m²；最大 = (0.12+0.02)×550 = 77.0 m²；换气次数 = 550/(66.0×2.4) = 3.5 次/h",
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
  console.log("==== energy calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();