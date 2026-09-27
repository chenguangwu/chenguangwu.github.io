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
    inputs: { amount: "800000", rate: "5.0", years: "20" },
    expect: ["467,115.02"],
    ref: "de-default(80万/5.0%/20年)：等额本息 M=800,000×(0.05/12)×(1+0.05/12)^240/((1+0.05/12)^240−1)=5,279.65；总利息=M×240−800,000=467,115.02",
  },
  {
    slug: "realestate/calc-1",
    inputs: { amount: "800000", rate: "5.0", years: "20" },
    expect: ["401,666.67"],
    ref: "de-default：等额本金总利息=P×i×(n+1)/2=800,000×(0.05/12)×241/2=401,666.67（低于等额本息，符合省利息的结论）",
  },

  // ── 租金回报率：毛回报 = 年租金/房价；净回报 =（年租金−年成本）/房价 ──
  {
    slug: "realestate/calc-2",
    inputs: { price: "1800000", rent: "6500", cost: "9000", growth: "0" },
    expect: ["78,000.00"],
    ref: "de-default(180万/6500/9000)：年租金 = 月租 6,500 × 12 = 78,000.00",
  },
  {
    slug: "realestate/calc-2",
    inputs: { price: "1800000", rent: "6500", cost: "9000", growth: "0" },
    expect: ["4.33%"],
    ref: "de-default：毛租金回报率 = 78,000 / 1,800,000 = 4.33%",
  },
  {
    slug: "realestate/calc-2",
    inputs: { price: "1800000", rent: "6500", cost: "9000", growth: "0" },
    expect: ["3.83%"],
    ref: "de-default：净租金回报率 =(78,000 − 9,000)/ 1,800,000 = 69,000/1,800,000 = 3.83%",
  },

  // ── 首付与月供：首付=总价×比例；贷款=总价−首付 ────────────────────────
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "2500000", downPct: "35", years: "25", rate: "4.8" },
    expect: ["875,000"],
    ref: "de-default(250万/35%/25年/4.8%)：首付 = 2,500,000 × 35% = 875,000",
  },
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "2500000", downPct: "35", years: "25", rate: "4.8" },
    expect: ["1,625,000"],
    ref: "de-default：贷款 = 2,500,000 − 875,000 = 1,625,000",
  },
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "2500000", downPct: "35", years: "25", rate: "4.8" },
    expect: ["9,311.2"],
    ref: "de-default：等额本息月供 = 1,625,000×0.004×(1.004^300)/((1.004^300)−1) = 9,311.2（fmt 最多 2 位小数、去尾零）",
  },

  // ── 公积金额度：余额倍数 vs 月缴存测算，取小后再受当地上限封顶 ────────
  {
    slug: "realestate/fund-loan",
    inputs: { balance: "60000", multiplier: "25", monthlyFund: "2000", fundYears: "8", payMultiple: "60", cap: "500000" },
    expect: ["¥1,500,000"],
    ref: "de-default(6万/25倍/2000/8年)：按余额倍数 = 60,000 × 25 = 1,500,000",
  },
  {
    slug: "realestate/fund-loan",
    inputs: { balance: "60000", multiplier: "25", monthlyFund: "2000", fundYears: "8", payMultiple: "60", cap: "500000" },
    expect: ["¥192,000"],
    ref: "de-default：按月缴存 = 2,000 × (8×12) × (60/60) = 192,000；两者取小 192,000，未超上限 500,000 → 建议可贷 192,000",
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
    expect: ["利息占本金比例76.0%"],
    ref: "可贷额度 = 200 万 × 70% = 140.00 万（与利率无关，原 expect「140.00」逃生项）；本例改锚定随利率变化的「利息占本金比例76.0%」（rate=3.10 时为 53.7% → 失配）。",
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
    expect: ["增值税及附加"],
    ref: "未满 2 年：增值税 200/1.05×5%=9.5238、附加 9.5238×12%=1.1429，加契税 2.00 + 印花 0.20 + 个税 2.00 = 14.87 万。"
       + "原 expect「14.87」在 years=0 时不论 tax=4/0 均为 14.87（未满 2 年增值税必征，原逃生项），"
       + "改锚定随 tax 出现的「增值税及附加」税目行（tax=0 默认时不出现 → 失配）。",
  },

  // ── 地价测算：单位地价=总价/土地面积；楼面地价=总价/(面积×容积率) ─────
  {
    slug: "realestate/calc-70",
    inputs: { landArea: "8000", totalPrice: "6000", plotRatio: "3.0", density: "25", benchmark: "5000" },
    expect: ["2,500"],
    ref: "de-default(8000/6000万/3.0/25%/5000)：楼面地价 = 6,000万×10,000 / (8,000×3.0) = 60,000,000 / 24,000 = 2,500 元/㎡",
  },
  {
    slug: "realestate/calc-70",
    inputs: { landArea: "8000", totalPrice: "6000", plotRatio: "3.0", density: "25", benchmark: "5000" },
    expect: ["50.00%"],
    ref: "de-default：单位地价 = 6,000万×10,000/8,000 = 7,500；溢价率 =(7,500−5,000)/5,000×100 = 50.00%",
  },

  // ── REITs 收益：股息率=DPU/市价；资本化率=DPU/NAV ────────────────────
  {
    slug: "realestate/calc-return",
    inputs: { nav: "12", price: "9.8", dpu: "0.55", shares: "8000", leverage: "50", futurePrice: "" },
    expect: ["5.61%"],
    ref: "de-default(NAV12/9.8/DPU0.55/8000/50%)：股息率 = 每份分红 0.55 / 市价 9.8 = 5.6122% → 5.61%",
  },
  {
    slug: "realestate/calc-return",
    inputs: { nav: "12", price: "9.8", dpu: "0.55", shares: "8000", leverage: "50", futurePrice: "" },
    expect: ["4.58%"],
    ref: "de-default：隐含资本化率 = DPU 0.55 / NAV 12 = 4.5833% → 4.58%（与按市价算的股息率区分开）",
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
{
  "slug": "realestate/analysis-risk-1",
  "inputs": { "inv": "5000000", "rate": "8", "data": "Y1,1200000\nY2,1500000\nY3,1800000\nY4,1600000\nY5,1200000" },
  "expect": [
    "NPV： 818764.98",
    "静态回收期： 3.31",
    "动态回收期： 4.00"
  ],
  "ref": "折现 1111111.11+1286008.23+1428894.53+1176080.86+816699.55=5818794.28，NPV=818764.98；累计现金流第 4 年覆盖 → 静态 3.31 年；累计折现第 4 年覆盖 → 动态 4.00 年（默认 2000000/8%/三年 60/80/90 万 NPV −44124.37、静态 2.67、动态计算期内未收回，避开）"
},

  // ── BATCH266：realestate 第二批「折扣 / 机会成本 / 折旧 / 首付 / 租售比 / 公积金额度」族 ──
  // 全部为「默认参数之外的第二组注入值」：默认态只跑到原默认值 ⇒ 注入值产物必变 ⇒
  // 双态天然成立；锚均为一步可手算的派生量，不碰输入回显。
  {
    slug: "realestate/price-discount-1",
    inputs: { v0: "12000", v1: "15" },
    expect: ["10200.00"],
    ref: "实售价 = 标价 12,000 ×（1 − 15%）= 12,000 × 0.85 = **10,200.00** 元（页面 sp=A*(1-B/100) 后 toFixed(2)）。第二组注入值（默认 8800/12），刻意与默认不同以逼出非零优惠额。",
  },
  {
    slug: "realestate/price-discount-1",
    inputs: { v0: "12000", v1: "15" },
    expect: ["85.00%"],
    ref: "实售占标价比 = 10,200 ÷ 12,000 × 100% = **85.00%**，与同页「等效折数 8.5 折」同源（(1−15%)×10）⇒ 两条锚互为交叉校验；不锚「标价 12,000 / 15%」（那是输入回显）。",
  },
  {
    slug: "realestate/calc-cost",
    inputs: { v0: "1200000", v1: "5" },
    expect: ["60000.00"],
    ref: "年机会成本 = 占用资金 1,200,000 × 收益率 5% = 1,200,000 × 0.05 = **60,000.00** 元（默认 800000/4.2，换一组以避开默认分支）。",
  },
  {
    slug: "realestate/calc-cost",
    inputs: { v0: "1200000", v1: "5" },
    expect: ["300000.00"],
    ref: "5 年累计机会成本 = 60,000.00 × 5 = **300,000.00** 元；月机会成本 5,000.00 由年额 ÷12 得、与两条锚同源 ⇒ 不单独锚。",
  },
  {
    slug: "realestate/cost-depreciation",
    inputs: { v0: "1500000", v1: "25" },
    expect: ["57000.00"],
    ref: "年折旧额 = 重建成本 1,500,000 ×（1 − 残值率 5%）÷ 使用年限 25 = 1,425,000 ÷ 25 = **57,000.00** 元（默认 900000/30）。",
  },
  {
    slug: "realestate/cost-depreciation",
    inputs: { v0: "1500000", v1: "25" },
    expect: ["570000.00"],
    ref: "10 年累计折旧 = 57,000.00 × 10 = **570,000.00** 元；月折旧 4,750.00 亦由年额 ÷12 得 ⇒ 不单独锚。",
  },
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "5000000", downPct: "40", years: "20", rate: "5" },
    expect: ["¥2,000,000"],
    ref: "首付金额 = 总价 5,000,000 × 40% = **2,000,000** → fmt 千分位输出 ¥2,000,000（默认 2500000/35% ⇒ ¥875,000）。",
  },
  {
    slug: "realestate/down-payment",
    inputs: { totalPrice: "5000000", downPct: "40", years: "20", rate: "5" },
    expect: ["¥3,000,000"],
    ref: "贷款金额 = 5,000,000 − 2,000,000 = **3,000,000** → ¥3,000,000；与首付两条互斥、相加恰为总价 ⇒ 互为交叉校验，任一条错都会破坏和的关系。",
  },
  {
    slug: "realestate/calc-2",
    inputs: { price: "3500000", rent: "12000", cost: "20000", growth: "0" },
    expect: ["4.11%"],
    ref: "毛租金回报率 = 年租金 12,000 × 12 = 144,000 ÷ 房款 3,500,000 × 100% = **4.11%**（默认 2000000/5000/9000 ⇒ 3.00%/3.65%）。",
  },
  {
    slug: "realestate/calc-2",
    inputs: { price: "3500000", rent: "12000", cost: "20000", growth: "0" },
    expect: ["3.54%"],
    ref: "净租金回报率 =（144,000 − 运营成本 20,000）÷ 3,500,000 × 100% = 124,000 ÷ 3,500,000 = **3.54%**；毛利口径 4.11% 未减成本 ⇒ 两条锚互相削弱，2 位小数足以分辨。",
  },
  {
    slug: "realestate/fund-loan",
    inputs: { balance: "150000", multiplier: "25", monthlyFund: "3600", fundYears: "5", payMultiple: "60", cap: "400000" },
    expect: ["¥216,000"],
    ref: "建议可贷额度 = min(余额倍数 150,000×25 = 3,750,000；月缴存 3,600×(5×12)×(60/60) = 216,000) = 216,000，再受当地上限 400,000 封顶不改变 ⇒ **¥216,000**。本组刻意让「余额倍数」远大于「月缴存测算」，使最终额度由后者决定，可同时锁定 amt2 公式与 min/封顶链路。",
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
  console.log("==== realestate calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();