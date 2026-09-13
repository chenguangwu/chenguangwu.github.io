#!/usr/bin/env node
/**
 * realestate 分类关键计算逻辑独立验证（收口批次 D，第 20 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式「独立复算」得出（不回读页面输出），并在 ref 中写明完整算式。
 *
 * 数字格式（决定期望值长相，断言必须按真实输出写）：
 *   - calc-1 / calc-2 的 fmt(n,d) 转发 ToolBox.formatNumber → 千分位 + 固定 d 位小数；
 *   - down-payment / fund-loan / market-valuation 的 fmt(n) → 千分位、最多 2 位小数；
 *   - calc-70 / calc-return 的 fmt(n,d) → 千分位、默认 2 位小数；
 *   - assessor-38 / assessor-39 用 toFixed(2)、toFixed(4)，无千分位；
 *   - convert-area-shared 用 toFixed(6)。
 *
 * 未纳入的三类（均非 realestate 专属计算逻辑，不属于本门禁职责）：
 *   - calc-93 / pv / depreciation-2：跨行业通用 A/B 双输入模板，按 h1 标题正则分流，
 *     同一份代码在 268 个行业复用，验证它等于验证模板而非本行业；
 *   - summary-second-hand：名为「二手房税费汇总」，calc() 实为通用统计
 *     （n/总和/均值/中位数/方差/标准差），名实不符已记入 DEV-PLAN §9.3 待内容整改，
 *     不在此处锁定错误语义。
 *
 * 用法：
 *   node scripts/verify_realestate_calc.js
 *   node scripts/verify_realestate_calc.js calc-1 down-payment
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 房贷：等额本息月供 M = P·i·(1+i)^n / ((1+i)^n − 1) ──────────────
  // 注：月供 M 被写进 compare/trend 的子表格（$('compare').querySelector('tbody')），
  // stub 采集不到子表格内容；改断言 res 里可见的「总利息」——它由 M×n−P 推出，
  // 同样能锁定 M 的正确性，且是等额本息/等额本金对比的实质结论。
  {
    slug: "realestate/calc-1",
    inputs: { amount: "1000000", rate: "4.2", years: "30" },
    expect: ["760,461.83"],
    ref: "等额本息：M=1,000,000×0.0035×(1.0035^360)/((1.0035^360)−1)=4,890.17；总利息=M×360−1,000,000=760,461.83",
  },
  {
    slug: "realestate/calc-1",
    inputs: { amount: "1000000", rate: "4.2", years: "30" },
    expect: ["631,750.00"],
    ref: "等额本金：总利息=P×i×(n+1)/2=1,000,000×0.0035×361/2=631,750.00（低于等额本息，符合省利息的结论）",
  },

  // ── 租金回报率：毛回报 = 年租金/房价；净回报 =（年租金−年成本）/房价 ──
  {
    slug: "realestate/calc-2",
    inputs: { price: "2000000", rent: "5000", cost: "8000", growth: "0" },
    expect: ["60,000.00"],
    ref: "年租金 = 月租 5,000 × 12 = 60,000.00",
  },
  {
    slug: "realestate/calc-2",
    inputs: { price: "2000000", rent: "5000", cost: "8000", growth: "0" },
    expect: ["3.00%"],
    ref: "毛租金回报率 = 60,000 / 2,000,000 = 3.00%",
  },
  {
    slug: "realestate/calc-2",
    inputs: { price: "2000000", rent: "5000", cost: "8000", growth: "0" },
    expect: ["2.60%"],
    ref: "净租金回报率 =(60,000 − 8,000)/ 2,000,000 = 52,000/2,000,000 = 2.60%",
  },

  // ── 首付与月供：首付=总价×比例；贷款=总价−首付 ────────────────────────
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "3000000", downPct: "30", years: "30", rate: "4.2" },
    expect: ["900,000"],
    ref: "首付 = 3,000,000 × 30% = 900,000",
  },
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "3000000", downPct: "30", years: "30", rate: "4.2" },
    expect: ["2,100,000"],
    ref: "贷款 = 3,000,000 − 900,000 = 2,100,000",
  },
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "3000000", downPct: "30", years: "30", rate: "4.2" },
    expect: ["10,269.36"],
    ref: "等额本息月供 = 2,100,000×0.0035×(1.0035^360)/((1.0035^360)−1) = 10,269.36",
  },

  // ── 公积金额度：余额倍数 vs 月缴存测算，取小后再受当地上限封顶 ────────
  {
    slug: "realestate/fund-loan",
    inputs: { balance: "80000", multiplier: "20", monthlyFund: "2400", fundYears: "5", payMultiple: "60", cap: "600000" },
    expect: ["1,600,000"],
    ref: "按余额倍数 = 80,000 × 20 = 1,600,000",
  },
  {
    slug: "realestate/fund-loan",
    inputs: { balance: "80000", multiplier: "20", monthlyFund: "2400", fundYears: "5", payMultiple: "60", cap: "600000" },
    expect: ["144,000"],
    ref: "按月缴存 = 2,400 × (5×12) × (60/60) = 144,000；两者取小 144,000，未超上限 600,000",
  },
  {
    slug: "realestate/fund-loan",
    inputs: { balance: "80000", multiplier: "20", monthlyFund: "2400", fundYears: "5", payMultiple: "60", cap: "100000" },
    expect: ["100,000"],
    ref: "当地上限 100,000 生效：min(144,000, 100,000) = 100,000（验证封顶逻辑）",
  },

  // ── 按揭可贷额度：loan=评估价×成数；月供/总利息按等额本息 ─────────────
  {
    slug: "realestate/assessor-38",
    inputs: { val: "200", ltv: "70", rate: "4.2", years: "30", type: "0", guarantee: "0.5" },
    expect: ["140.00"],
    ref: "可贷额度 = 200 万 × 70% = 140.00 万",
  },
  {
    slug: "realestate/assessor-38",
    inputs: { val: "200", ltv: "70", rate: "4.2", years: "30", type: "0", guarantee: "0.5" },
    expect: ["0.6846"],
    ref: "等额本息月供 = 140×0.0035×(1.0035^360)/((1.0035^360)−1) = 0.6846 万（toFixed(4)）",
  },
  {
    slug: "realestate/assessor-38",
    inputs: { val: "200", ltv: "70", rate: "4.2", years: "30", type: "0", guarantee: "0.5" },
    expect: ["106.46"],
    ref: "总利息 = 月供 0.684624 × 360 − 140 = 106.46 万",
  },

  // ── 二手房税费：契税 + 增值税及附加 + 印花/房产税 + 个税 ──────────────
  {
    slug: "realestate/assessor-39",
    inputs: { val: "200", type: "0", area: "90", years: "5", tax: "4" },
    expect: ["4.20"],
    ref: "首套≤90㎡契税 200×1%=2.00；满 5 年免增值税；印花 200×0.001=0.20；个税 200×1%=2.00；合计 4.20 万",
  },
  {
    slug: "realestate/assessor-39",
    inputs: { val: "200", type: "0", area: "90", years: "0", tax: "4" },
    expect: ["14.87"],
    ref: "未满 2 年：增值税 200/1.05×5%=9.5238、附加 9.5238×12%=1.1429，加契税 2.00 + 印花 0.20 + 个税 2.00 = 14.87 万",
  },

  // ── 地价测算：单位地价=总价/土地面积；楼面地价=总价/(面积×容积率) ─────
  {
    slug: "realestate/calc-70",
    inputs: { landArea: "10000", totalPrice: "5000", plotRatio: "2.5", density: "30", benchmark: "4000" },
    expect: ["2,000"],
    ref: "楼面地价 = 5,000万×10,000 / (10,000×2.5) = 50,000,000 / 25,000 = 2,000 元/㎡",
  },
  {
    slug: "realestate/calc-70",
    inputs: { landArea: "10000", totalPrice: "5000", plotRatio: "2.5", density: "30", benchmark: "4000" },
    expect: ["25.00"],
    ref: "单位地价 5,000 相对基准 4,000 溢价率 =(5,000−4,000)/4,000×100 = 25.00%",
  },

  // ── REITs 收益：股息率=DPU/市价；资本化率=DPU/NAV ────────────────────
  {
    slug: "realestate/calc-return",
    inputs: { nav: "10", price: "9.5", dpu: "0.5", shares: "10000", leverage: "40", futurePrice: "" },
    expect: ["5.26%"],
    ref: "股息率 = 每份分红 0.5 / 市价 9.5 = 5.2632% → 5.26%",
  },
  {
    slug: "realestate/calc-return",
    inputs: { nav: "10", price: "9.5", dpu: "0.5", shares: "10000", leverage: "40", futurePrice: "" },
    expect: ["5.00%"],
    ref: "隐含资本化率 = DPU 0.5 / NAV 10 = 5.00%（与按市价算的股息率区分开）",
  },

  // ── 二手房市场比较法估价：单价=基准价×各修正系数×房龄折损 ─────────────
  {
    slug: "realestate/market-valuation",
    inputs: { area: "100", basePrice: "30000", floor: "1", facing: "1", deco: "1", age: "10", school: "1", extra: "0" },
    expect: ["28,500"],
    ref: "房龄折损 = 1 − 10×0.005 = 0.95；评估单价 = 30,000×1×1×1×1×(1+0%)×0.95 = 28,500 元/㎡",
  },
  {
    slug: "realestate/market-valuation",
    inputs: { area: "100", basePrice: "30000", floor: "1", facing: "1", deco: "1", age: "10", school: "1", extra: "0" },
    expect: ["2,850,000"],
    ref: "评估总价 = 28,500 × 100 ㎡ = 2,850,000 元",
  },
  {
    slug: "realestate/market-valuation",
    inputs: { area: "100", basePrice: "30000", floor: "1", facing: "1", deco: "1", age: "10", school: "1", extra: "0" },
    expect: ["-5%"],
    ref: "综合修正幅度 =(28,500/30,000 − 1)×100 = −5%（房龄折损 5% 的直接体现）",
  },

  // ── 面积换算：结果 = 数值 × 换算系数 × 源单位 / 目标单位 ───────────────
  {
    slug: "realestate/convert-area-shared",
    inputs: { val: "100", rate: "0.8", from: "1", to: "1" },
    expect: ["80.000000"],
    ref: "建筑面积 100 ㎡ × 套内系数 0.8 = 80 ㎡（toFixed(6)）",
  },
];

// ---------------------------------------------------------------- main
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
