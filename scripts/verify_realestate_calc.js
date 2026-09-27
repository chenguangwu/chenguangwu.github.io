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

  // ── BATCH297：商铺坪效/租售比测算 ─────────────────────────────────
  {
    slug: "realestate/analysis-45",
    inputs: { "gla": "60000", "flow": "40000", "bag": "20", "ticket": "100", "rentm": "50", "occ": "95" },
    clicks: ["calc();"],
    expect: ["8,000 人", "80.00 万元", "11.71%", "20.00 元/人次"],
    ref: "日均有效购买人次 = 客流 40,000 × 提袋率 20% = 8,000 人；日均销售额 = 8,000 × 客单价 100 = 800,000 元 = 80.00 万元；年租金 = 60,000 ㎡ × 50 元 × 12 × 95% = 34,200,000 元 = 3,420.00 万元；租售比 = 3,420 万 ÷ 年销售额 29,200 万 × 100% = 11.71%（10%~15% 健康档，故不锚该判读句、避免默认态同档）；单位客流贡献 = 800,000 ÷ 40,000 = 20.00 元/人次。默认档 32,000 客流/18%/120 元 ⇒ 5,760 人、69.12 万元、11.82%、21.60 元/人次，全部不命中。",
  },
  // ── BATCH297：商铺坪效/租售比测算 ─────────────────────────────────
  {
    slug: "realestate/analysis-45",
    inputs: { "gla": "50000", "flow": "60000", "bag": "25", "ticket": "200", "rentm": "30", "occ": "90" },
    clicks: ["calc();"],
    expect: ["15,000 人", "300.00 万元", "1.48%", "50.00 元/人次"],
    ref: "买家数 = 60,000 × 25% = 15,000 人；日均销售额 = 15,000 × 200 = 3,000,000 元 = 300.00 万元；年租金 = 50,000 × 30 × 12 × 90% = 16,200,000 元 = 1,620.00 万元；租售比 = 1,620 万 ÷ 109,500 万 = 1.48%（<10% ⇒ 「租售比偏低，商户经营压力小，可考虑适度提租」判读句，与第 1 条的健康档判读互斥）。",
  },
  // ── BATCH297：商铺坪效/租售比测算 ─────────────────────────────────
  {
    slug: "realestate/analysis-45",
    inputs: { "gla": "40000", "flow": "20000", "bag": "15", "ticket": "150", "rentm": "60", "occ": "100" },
    clicks: ["calc();"],
    expect: ["3,000 人", "2,880.00 万元", "17.53%", "22.50 元/人次"],
    ref: "买家数 = 20,000 × 15% = 3,000 人；日均销售额 = 3,000 × 150 = 450,000 元 = 45.00 万元；年销售额 = 450,000 × 365 = 164,250,000 元 = 16,425.00 万元；年租金 = 40,000 × 60 × 12 × 100% = 28,800,000 元 = 2,880.00 万元；租售比 = 2,880 ÷ 16,425 × 100% = 17.53%（落在 15%~20% 的「偏高」档，与第 1/2 条判读互斥）；单位客流贡献 = 450,000 ÷ 20,000 = 22.50 元/人次。",
  },
  // ── BATCH297：商铺坪效/租售比测算 ─────────────────────────────────
  {
    slug: "realestate/analysis-45",
    inputs: { "gla": "40000", "flow": "20000", "bag": "15", "ticket": "80", "rentm": "90", "occ": "100" },
    clicks: ["calc();"],
    expect: ["4,320.00 万元", "49.32%", "12.00 元/人次", "租售比超过 20%"],
    ref: "仅改客单价 80 元与租金 90 元：日均销售额降为 240,000 元 = 24.00 万元、年销售额 8,760.00 万元，而年租金升至 40,000 × 90 × 12 = 43,200,000 元 = 4,320.00 万元 ⇒ 租售比 = 4,320 ÷ 8,760 × 100% = 49.32%（>20% 最高档判读）。第 3 条与本条同为 3,000 买家、同为 occ=100%，只有客单价/租金不同 ⇒ 两条互为削弱，任一条输错都暴露。",
  },
  // ── BATCH297：商铺坪效/租售比测算 ─────────────────────────────────
  {
    slug: "realestate/analysis-45",
    inputs: { "flow": "0" },
    clicks: ["calc();"],
    expect: ["日均有效购买人次： 0 人", "0.00 万元", "年销售额为 0，无法计算租售比"],
    ref: "客流置 0（其余走默认 45,000 ㎡/18%/120 元/60 元/92%）：买家数与各销售额全为 0，年租金 45,000×60×12×92% = 2,980.80 万元不受客流影响仍照常输出，但 ratio 走 null 分支显示「—」并落到「年销售额为 0，无法计算租售比」判读。刻意不锚 2,980.80 万元（该值在默认档同样出现，属默认态同值 ⇒ 逃生项）；也不锚裸串「0 人」——它是默认态「5,760 人」的子串，双态会假通过（已实测逃生）。",
  },  {
    slug: "realestate/shichang-bijiaofa-anlixiuzheng",
    inputs: {},
    clicks: ["document.getElementById('priceA').value='10000';document.getElementById('tA').value='5';document.getElementById('mA').value='-3';document.getElementById('lA').value='2';document.getElementById('pA').value='-1';document.getElementById('priceB').value='12000';document.getElementById('tB').value='0';document.getElementById('mB').value='4';document.getElementById('lB').value='0';document.getElementById('pB').value='-2';document.getElementById('priceC').value='11000';document.getElementById('tC').value='1';document.getElementById('mC').value='0';document.getElementById('lC').value='-3';document.getElementById('pC').value='0';calc();"],
    expect: ['11,133', '10,285', '12,230', 'A 28.7%', 'C 37.1%'],
    ref: '三案例全量修正（auto 权重）：比准价 = 成交价×(1+t%)×(1+m%)×(1+l%)×(1+p%)，故 A = 10000×1.05×0.97×1.02×0.99 = **10284.813** ⇒ 表内 `10,285`（同时是「最低比准价」）、B = 12000×1.04×0.98 = **12230.4** ⇒ `12,230`（同时是「最高比准价」）、C = 11000×1.01×0.97 = **10776.7** ⇒ `10,777`；自动权重按修正幅度倒数归一 inv = 1÷(1+Σ|修正|×5)：A 的 Σ=0.11⇒0.645161、B Σ=0.06⇒0.769231、C Σ=0.04⇒0.833333，和 2.247725 ⇒ A **28.7%** / B **34.2%** / C **37.1%**，加权 = 10284.813×0.287067+12230.4×0.342219+10776.7×0.370715 = **11133.009** ⇒ `11,133`。刻意不锚 `B 34.2%`：默认组（8500/9200/8800）的 B 权重恰也是 34.2%，属默认态同值 ⇒ 逃生项（已实测剔除）；改用 A/C 两条权重锚。默认态输出 8,927 / 31.5% / 34.2% / 34.2%，四条锚全不命中。',
  },
  {
    slug: "realestate/shichang-bijiaofa-anlixiuzheng",
    inputs: {},
    clicks: ["document.getElementById('weightMode').value='equal';document.getElementById('priceA').value='10000';document.getElementById('tA').value='5';document.getElementById('mA').value='-3';document.getElementById('lA').value='2';document.getElementById('pA').value='-1';document.getElementById('priceB').value='12000';document.getElementById('tB').value='0';document.getElementById('mB').value='4';document.getElementById('lB').value='0';document.getElementById('pB').value='-2';document.getElementById('priceC').value='11000';document.getElementById('tC').value='1';document.getElementById('mC').value='0';document.getElementById('lC').value='-3';document.getElementById('pC').value='0';calc();"],
    expect: ['11,097', 'A 33.3%', 'C 33.3%'],
    ref: '与上一条同输入、只把 `weightMode` 切到 equal ⇒ 权重链改为 1÷3 等权，加权 = (10284.813+12230.4+10776.7)÷3 = **11097.304** ⇒ `11,097`，三权重均 `33.3%`。三条锚各覆盖一处独立式子（加权求和式 / 等权分子式 / 权重归一分母式）：任一处写错（例如漏 ÷3 的和、或仍走 auto 的 inv 归一）都会被抓。刻意不锚「权重方式：」那句文案——harness 下 `option:checked` 不随 `.value` 赋值更新，该串恒为「自动（按案例相似度）」，与被测点解耦 ⇒ 逃生项。默认态输出 8,927，三条锚全不命中。',
  },
  {
    slug: "realestate/shichang-bijiaofa-anlixiuzheng",
    inputs: {},
    clicks: ["document.getElementById('priceC').value='0';calc();"],
    expect: ['8,855', '2 有效可比案例数', 'A 47.9%', 'B 52.1%'],
    ref: '把案例 C 成交价置 0 ⇒ `cases = [A,B,C].filter(price>0)` 剔除 ⇒ 有效案例数 `2`、比准价回落到两组：A = 8500×1.02×0.98×1.01 = **8579.466** ⇒ `8,582`、B = 9200×0.99×1.01×0.99 = **9110.089** ⇒ `9,107`；权重链只在 A/B 上重算，inv A = 1÷(1+0.05×5)=0.8、B = 1÷(1+0.02×5)=0.909091，和 1.709091 ⇒ A **47.9%** / B **52.1%**，加权 = 8579.466×0.468085+9110.089×0.531915 = **8855.276** ⇒ `8,855`。顺带覆盖 `fmt(weighted,0)` 的取整与千分位。默认态是 3 组、8,927、47.9% 的那组不出现，四条锚全不命中。',
  },
  {
    slug: "realestate/shichang-bijiaofa-anlixiuzheng",
    inputs: {},
    clicks: ["document.getElementById('priceA').value='9500';document.getElementById('tA').value='10';document.getElementById('mA').value='5';document.getElementById('lA').value='-5';document.getElementById('pA').value='0';document.getElementById('priceB').value='0';document.getElementById('priceC').value='0';calc();"],
    expect: ['10,424', 'A 100.0%', '10,424 最高比准价', '10,424 最低比准价'],
    ref: '只保留案例 A（B/C 成交价置 0）：比准价 = 9500×1.10×1.05×0.95 = **10423.875** ⇒ `10,424`，且因只有一组 ⇒ `Math.max`/`Math.min` 同值，卡片同时显示 `10,424 最高比准价` 与 `10,424 最低比准价`；单组时权重取 1 ⇒ `A 100.0%`。四条锚分别覆盖「请至少输入一个案例」的空集分支不会误触发、`Math.max.apply` 与 `Math.min.apply` 的单元素退化、`weights` 的 1÷1。默认态是 3 组，全不命中。',
  },
  {
    slug: "realestate/shichang-bijiaofa-anlixiuzheng",
    inputs: {},
    clicks: ["document.getElementById('priceA').value='8000';document.getElementById('tA').value='-8';document.getElementById('mA').value='-6';document.getElementById('lA').value='-4';document.getElementById('pA').value='-2';document.getElementById('priceB').value='9000';document.getElementById('tB').value='-10';document.getElementById('priceC').value='7000';document.getElementById('mC').value='-2';calc();"],
    expect: ['6,509', '8,100', '6,860', 'A 24.1%', 'B 32.1%', 'C 43.8%'],
    ref: '三组全负修正（A 四项全负、B 仅交易情况 −10%、C 仅市场状况 −2%）：比准价 A = 8000×0.92×0.94×0.96×0.98 = **6508.83** ⇒ `6,509`（同时最低）、B = 9000×0.90 = **8100** ⇒ `8,100`（同时最高）、C = 7000×0.98 = **6860** ⇒ `6,860`；自动权重 Σ|A|：A 0.20⇒inv 0.5、B 0.10⇒0.666667、C 0.02⇒0.909091，和 2.075758 ⇒ A **24.1%** / B **32.1%** / C **43.8%**，加权 = **7173.66** ⇒ `7,174`（不锚，避免与例①的取整串混淆）。本条同时压住「四项连乘顺序无关」与「Σ|A| 对四项求和」两处；默认态的 8,582/9,107/9,066 与 31.5%/34.2%/34.2% 全不命中。',
  },
  {
    slug: "realestate/shichang-bijiaofa-anlixiuzheng",
    inputs: {},
    clicks: ["document.getElementById('weightMode').value='equal';document.getElementById('priceA').value='10500';document.getElementById('tA').value='3';document.getElementById('mA').value='-2';document.getElementById('lA').value='1';document.getElementById('pA').value='0';document.getElementById('priceB').value='0';document.getElementById('priceC').value='0';calc();"],
    expect: ['10,705', 'A 100.0%'],
    ref: 'equal 权重 + 仅一组可比案例：比准价 = 10500×1.03×0.98×1.01 = **10704.687** ⇒ `10,705`；等权分支 `w = 1/cases.length` 在 n=1 时退化为 1，加权与比准价恒等 ⇒ `A 100.0%`。本条与例④（同样只留一组、auto 权重）互为对照：同一份成交价/修正若权重链写错（把 auto 的 inv 归一塞进去）数值仍会偏，但权重串会从 100.0% 翻成别的比例 ⇒ 被抓。默认态 3 组 8,927，两条锚全不命中。',
  },
  {
    slug: "realestate/analysis-41",
    inputs: { supply: "1200", demand: "600", stock: "9000", p0: "22000", p1: "19800" },
    expect: ["2.00", "15.00 月", "-10.0%", "供过于求·价格下行（偏冷）"],
    ref: 'S=1200 D=600 I=9000 p0=22000 p1=19800；供需比=2.00、去化周期=15.00 月、价格环比=-10.0%；分支2 供过于求·价格下行（偏冷）：sr>1 且 chg<0'
  },
  {
    slug: "realestate/analysis-41",
    inputs: { supply: "3000", demand: "500", stock: "600000", p0: "25000", p1: "20000" },
    expect: ["1,200 月", "-20.0%", "控量保价、以价换量去库存，强化产品力"],
    ref: 'S=3000 D=500 I=600000 p0=25000 p1=20000；供需比=6.00、去化周期=1,200 月、价格环比=-20.0%；分支2 大值：cycle=1200 触发 fmtN 千分位（d=0 + 逗号）'
  },
  {
    slug: "realestate/analysis-41",
    inputs: { supply: "1000", demand: "800", stock: "8000", p0: "18000", p1: "19000" },
    expect: ["1.25", "10.00 月", "5.6%"],
    ref: 'S=1000 D=800 I=8000 p0=18000 p1=19000；供需比=1.25、去化周期=10.00 月、价格环比=5.6%；分支3 供过于求·价格平稳：sr>1 且 chg>0（state/strat 与默认态同串，只能锚数值）'
  },
  {
    slug: "realestate/analysis-41",
    inputs: { supply: "900", demand: "600", stock: "5400", p0: "21000", p1: "21000" },
    expect: ["1.50", "9.00 月", "0.0%"],
    ref: 'S=900 D=600 I=5400 p0=21000 p1=21000；供需比=1.50、去化周期=9.00 月、价格环比=0.0%；分支3 边界 chg=0：sr>1、chg 不<0 ⇒ 仍落分支3'
  },
  {
    slug: "realestate/analysis-41",
    inputs: { supply: "700", demand: "700", stock: "4900", p0: "20000", p1: "18600" },
    expect: ["1.00", "7.00 月", "-7.0%", "供需偏紧·价格回落（观望）"],
    ref: 'S=700 D=700 I=4900 p0=20000 p1=18600；供需比=1.00、去化周期=7.00 月、价格环比=-7.0%；分支4 供需偏紧·价格回落：sr=1（不>1）且 chg<0 ⇒ 落分支4'
  },
  {
    slug: "realestate/analysis-41",
    inputs: { supply: "800", demand: "800", stock: "9600", p0: "16000", p1: "16800" },
    expect: ["12.00 月", "5.0%", "供需基本均衡"],
    ref: 'S=800 D=800 I=9600 p0=16000 p1=16800；供需比=1.00、去化周期=12.00 月、价格环比=5.0%；else 分支供需基本均衡：sr=1、chg>0 ⇒ 四个条件全不满足'
  },
  {
    slug: "realestate/estimate-analysis-2",
    inputs: { inv: "2000", cf: "400", rv: "300", disc: "10", yrs: "8" },
    expect: ["净现值 NPV： 273.92 万元", "现值指数 PI： 1.137", "静态回收期： 5.00 年"],
    ref: 'inv=2000 cf=400 rv=300 disc=10 yrs=8；pv=400×(1-1.1^-8)/0.1=2133.97、pvRv=300/1.1^8=139.95、NPV=273.92；PI=2273.92/2000=1.137；静态回收期=2000/400=5.00 年；动态=7.28 年。正 NPV 基准，五参数全改'
  },
  {
    slug: "realestate/estimate-analysis-2",
    inputs: { inv: "3000", cf: "200", rv: "100", disc: "12", yrs: "10" },
    expect: ["净现值 NPV： -1,837.76 万元", "现值指数 PI： 0.387", "净现值为负，按该折现率该项目不创造价值，但 IRR 低于折现率，财务上不可行"],
    ref: 'inv=3000 cf=200 rv=100 disc=12 yrs=10；pv=200×5.650223=1130.04、pvRv=100/1.12^10=32.20、NPV=-1837.76；PI=0.387；IRR=-5.80% < 12% ⇒ 结论取『不创造价值…不可行』分支（默认态为正，不撞）'
  },
  {
    slug: "realestate/estimate-analysis-2",
    inputs: { inv: "100", cf: "600", rv: "10", disc: "8", yrs: "5" },
    expect: ["净现值 NPV： 2,302.43 万元", "现值指数 PI： 24.024", "内部收益率 IRR： —"],
    ref: 'inv=100 cf=600 rv=10 disc=8 yrs=5；IRR 无解分支：npvAt(5)=600×Σ(1/6^i)+10/6^5-100=600×0.199975+0.0013-100≈+19.99>0，与 npvAt(-0.9)>0 同号 ⇒ 二分前提 npvAt(lo)*npvAt(hi)<0 不成立 ⇒ IRR 恒为『—』（默认态 IRR=9.29%，不撞）'
  },
  {
    slug: "realestate/estimate-analysis-2",
    inputs: { inv: "1000", cf: "100", rv: "50", disc: "8", yrs: "5" },
    expect: ["净现值 NPV： -566.70 万元", "动态回收期： 超过项目期 5 年", "未折现现金流合计： 550.00 万元"],
    ref: 'inv=1000 cf=100 rv=50 disc=8 yrs=5；动态回收期超期分支：折现累计 5 年仅 399.27+34.03=433.30 < inv ⇒ dynPay=null ⇒ 渲染『超过项目期 5 年』；未折现=100×5+50=550.00'
  },
  {
    slug: "realestate/estimate-analysis-2",
    inputs: { inv: "800", cf: "0", rv: "600", disc: "6", yrs: "5" },
    expect: ["净现值 NPV： -351.65 万元", "静态回收期： —", "动态回收期： 超过项目期 5 年"],
    ref: 'inv=800 cf=0 rv=600 disc=6 yrs=5；零现金流分支：cf=0 ⇒ statPay/dynPay 均 null ⇒ 静态『—』、动态『超过项目期 5 年』；NPV=600/1.06^5-800=448.35-800=-351.65'
  },
  {
    slug: "realestate/estimate-analysis-2",
    inputs: { inv: "1000", cf: "200", rv: "100", disc: "0", yrs: "5" },
    expect: ["净现值 NPV： 100.00 万元", "现值指数 PI： 1.100", "静态回收期： 5.00 年"],
    ref: 'inv=1000 cf=200 rv=100 disc=0 yrs=5；折现率 0 分支：r=0 ⇒ pv=cf×yrs=1000、pvRv=rv=100 ⇒ NPV=100.00、PI=1.100、动态=5.00 年。刻意不锚 IRR（3.07%，200 次二分浮点边界）'
  },
  {
    slug: "realestate/assessor-return",
    inputs: { rent: "30", vacancy: "8", opex: "30", capRate: "6", method: "0", landVal: "0" },
    expect: ["322.00", "19.32", "10.7倍", "直接资本化法适用于稳定收益型房产。毛租金倍数偏低(<15倍)，投资回报率较高。"],
    ref: 'rent=30 vac=8 opex=30 capRate=6% method=0 land=0；有效毛收入=27.60 运营费用=8.28 NOI=19.32 V=322.00 GRM=10.7 实际收益率=6.00% 租售比=9.32%。method=0 直接资本化：grm=10.7<15 ⇒ it 追加『偏低』串（默认态无此后缀，故完整 it 串可锚）'
  },
  {
    slug: "realestate/assessor-return",
    inputs: { rent: "36", vacancy: "10", opex: "25", capRate: "6", method: "1", landVal: "80" },
    expect: ["325.00", "24.30", "剩余法适用于开发项目，从总开发价值中扣除土地价值后得出建筑物价值。毛租金倍数偏低(<15倍)，投资回报率较高。", "土地价值 -80.00"],
    ref: 'rent=36 vac=10 opex=25 capRate=6% method=1 land=80；有效毛收入=32.40 运营费用=8.10 NOI=24.30 V=325.00 GRM=9.0 实际收益率=7.48% 租售比=11.08%。method=1 剩余法：V=NOI/r-80；it 为『剩余法…偏低(<15倍)…』完整串；另锚表格行『土地价值 -80.00』'
  },
  {
    slug: "realestate/assessor-return",
    inputs: { rent: "20", vacancy: "0", opex: "0", capRate: "4", method: "0", landVal: "0" },
    expect: ["500.00", "25.0倍", "20.00"],
    ref: 'rent=20 vac=0 opex=0 capRate=4% method=0 land=0；有效毛收入=20.00 运营费用=0.00 NOI=20.00 V=500.00 GRM=25.0 实际收益率=4.00% 租售比=4.00%。grm=25.0 边界：vac=0、opex=0、capRate=4 ⇒ grm 恰为 25.0，既不>25 也不<15 ⇒ it 不追加任何说明（验证边界不误入偏低支）'
  },
  {
    slug: "realestate/assessor-return",
    inputs: { rent: "100", vacancy: "12", opex: "35", capRate: "8", method: "0", landVal: "0" },
    expect: ["715.00", "57.20", "7.2倍"],
    ref: 'rent=100 vac=12 opex=35 capRate=8% method=0 land=0；有效毛收入=88.00 运营费用=30.80 NOI=57.20 V=715.00 GRM=7.2 实际收益率=8.00% 租售比=13.99%。高租金 capRate=8：grm=7.2<15；数值与例① 全不同'
  },
  {
    slug: "realestate/assessor-return",
    inputs: { rent: "45", vacancy: "3", opex: "22", capRate: "4.5", method: "0", landVal: "0" },
    expect: ["756.60", "34.05", "16.8倍"],
    ref: 'rent=45 vac=3 opex=22 capRate=4.5% method=0 land=0；有效毛收入=43.65 运营费用=9.60 NOI=34.05 V=756.60 GRM=16.8 实际收益率=4.50% 租售比=5.95%。capRate=4.5 档，grm=16.8 落在 15~25 的『不追加说明』区间'
  },
  {
    slug: "realestate/assessor-return",
    inputs: { rent: "500", vacancy: "15", opex: "40", capRate: "7", method: "1", landVal: "1200" },
    expect: ["2442.86", "255.00", "4.9倍", "土地价值 -1200.00"],
    ref: 'rent=500 vac=15 opex=40 capRate=7% method=1 land=1200；有效毛收入=425.00 运营费用=170.00 NOI=255.00 V=2442.86 GRM=4.9 实际收益率=10.44% 租售比=20.47%。大数值 method=1：土地价值 1200 万元，V=NOI/0.07-1200'
  },
  {
    slug: "realestate/assessor-second-hand",
    inputs: { p1: "4.2", p2: "4.6", p3: "4.0", loc: "2", floor: "2", decor: "2", orient: "0", age: "0", area: "110" },
    expect: ["4.5227", "497.49", "4.2667", "总调整幅度 +6%"],
    ref: 'p1=4.2 p2=4.6 p3=4.0 loc=2 floor=2 decor=2 orient=0 age=0 area=110；案例均价=4.2667 总调整=+6% 调整后单价=4.5227 评估总价=497.49。totalAdj=+6（可达最大值：loc/floor/decor 均取 +2）⇒ 颜色 success 支（≥0）'
  },
  {
    slug: "realestate/assessor-second-hand",
    inputs: { p1: "5.0", p2: "5.4", p3: "5.2", loc: "1", floor: "1", decor: "0", orient: "0", age: "0", area: "80" },
    expect: ["5.3040", "424.32", "5.2000", "总调整幅度 +2%"],
    ref: 'p1=5.0 p2=5.4 p3=5.2 loc=1 floor=1 decor=0 orient=0 age=0 area=80；案例均价=5.2000 总调整=+2% 调整后单价=5.3040 评估总价=424.32。totalAdj=+2 ⇒ success 支（≥0）'
  },
  {
    slug: "realestate/assessor-second-hand",
    inputs: { p1: "2.0", p2: "2.6", p3: "2.9", loc: "0", floor: "0", decor: "0", orient: "0", age: "0", area: "60" },
    expect: ["2.5000", "150.00", "2.5000", "待估面积 60平米"],
    ref: 'p1=2.0 p2=2.6 p3=2.9 loc=0 floor=0 decor=0 orient=0 age=0 area=60；案例均价=2.5000 总调整=0% 调整后单价=2.5000 评估总价=150.00。totalAdj=0 支：与默认同为『0%』故不可锚，改用『待估面积 60平米』（默认 90平米）'
  },
  {
    slug: "realestate/assessor-second-hand",
    inputs: { p1: "6.0", p2: "6.3", p3: "6.6", loc: "0", floor: "-3", decor: "0", orient: "0", age: "0", area: "75" },
    expect: ["6.1110", "458.32", "6.3000", "总调整幅度 -3%"],
    ref: 'p1=6.0 p2=6.3 p3=6.6 loc=0 floor=-3 decor=0 orient=0 age=0 area=75；案例均价=6.3000 总调整=-3% 调整后单价=6.1110 评估总价=458.32。totalAdj=-3 边界 ⇒ info 支（-3 ≥ -3，不落 warning）'
  },
  {
    slug: "realestate/assessor-second-hand",
    inputs: { p1: "7.0", p2: "7.5", p3: "8.0", loc: "-2", floor: "-3", decor: "0", orient: "0", age: "0", area: "120" },
    expect: ["7.1250", "855.00", "7.5000", "总调整幅度 -5%"],
    ref: 'p1=7.0 p2=7.5 p3=8.0 loc=-2 floor=-3 decor=0 orient=0 age=0 area=120；案例均价=7.5000 总调整=-5% 调整后单价=7.1250 评估总价=855.00。totalAdj=-5 ⇒ warning 支（<-3）'
  },
  {
    slug: "realestate/assessor-second-hand",
    inputs: { p1: "9.0", p2: "9.6", p3: "9.3", loc: "-2", floor: "-3", decor: "-3", orient: "-3", age: "-3", area: "100" },
    expect: ["7.9980", "799.80", "9.3000", "总调整幅度 -14%"],
    ref: 'p1=9.0 p2=9.6 p3=9.3 loc=-2 floor=-3 decor=-3 orient=-3 age=-3 area=100；案例均价=9.3000 总调整=-14% 调整后单价=7.9980 评估总价=799.80。totalAdj=-14（可达最小值）⇒ warning 支，验证极端负调整不越界'
  },
  {
    slug: "realestate/calc-assessor",
    inputs: { area: "120", price: "25000", type: "0", method: "0", temp: "18", tempRate: "40", move: "3500", bonus: "1" },
    expect: ["3239900", "86400", "150000", "奖励政策 按期签约奖励5%"],
    ref: 'area=120 price=25000 type=0(住宅) method=0(货币补偿) temp=18 tempRate=40 move=3500 bonus=1(按期签约奖励5%)；房屋补偿=3000000 临时安置=86400 搬迁=3500 奖励金=150000 总额=3239900。method=0 + bonus=1(5%)：货币补偿行与默认同串故不锚，改锚『奖励政策 按期签约奖励5%』'
  },
  {
    slug: "realestate/calc-assessor",
    inputs: { area: "95", price: "18000", type: "0", method: "1", temp: "24", tempRate: "35", move: "2800", bonus: "0" },
    expect: ["1792600", "79800", "补偿方式 产权调换(等面积)", "产权调换面积"],
    ref: 'area=95 price=18000 type=0(住宅) method=1(产权调换(等面积)) temp=24 tempRate=35 move=2800 bonus=0(无奖励)；房屋补偿=1710000 临时安置=79800 搬迁=2800 奖励金=0 总额=1792600。method=1 产权调换：锚『补偿方式 产权调换(等面积)』（默认『货币补偿』）+ 表格行『产权调换面积』'
  },
  {
    slug: "realestate/calc-assessor",
    inputs: { area: "150", price: "22000", type: "0", method: "2", temp: "6", tempRate: "50", move: "5000", bonus: "3" },
    expect: ["3614000", "264000", "奖励政策 签约+搬迁奖励8%", "产权调换面积"],
    ref: 'area=150 price=22000 type=0(住宅) method=2(货币补偿+产权调换) temp=6 tempRate=50 move=5000 bonus=3(签约+搬迁奖励8%)；房屋补偿=3300000 临时安置=45000 搬迁=5000 奖励金=264000 总额=3614000。method=2 混合方式；bonus=3(8%) ⇒ 奖励金 264000 + 『签约+搬迁奖励8%』'
  },
  {
    slug: "realestate/calc-assessor",
    inputs: { area: "60", price: "45000", type: "1", method: "0", temp: "30", tempRate: "60", move: "8000", bonus: "2" },
    expect: ["2897000", "108000", "商铺拆迁还需考虑停产停业损失补偿。", "奖励政策 按期搬迁奖励3%"],
    ref: 'area=60 price=45000 type=1(商铺) method=0(货币补偿) temp=30 tempRate=60 move=8000 bonus=2(按期搬迁奖励3%)；房屋补偿=2700000 临时安置=108000 搬迁=8000 奖励金=81000 总额=2897000。type=1 商铺：it 切换为『商铺拆迁还需考虑停产停业损失补偿。』+ bonus=2(3%)'
  },
  {
    slug: "realestate/calc-assessor",
    inputs: { area: "200", price: "12000", type: "3", method: "1", temp: "36", tempRate: "45", move: "12000", bonus: "1" },
    expect: ["2856000", "324000", "厂房拆迁需考虑设备搬迁和停产损失补偿。", "补偿方式 产权调换(等面积)", "产权调换面积"],
    ref: 'area=200 price=12000 type=3(厂房) method=1(产权调换(等面积)) temp=36 tempRate=45 move=12000 bonus=1(按期签约奖励5%)；房屋补偿=2400000 临时安置=324000 搬迁=12000 奖励金=120000 总额=2856000。type=3 厂房：it 切换为『厂房拆迁需考虑设备搬迁和停产损失补偿。』+ method=1'
  },
  {
    slug: "realestate/calc-assessor",
    inputs: { area: "75", price: "36000", type: "2", method: "1", temp: "20", tempRate: "25", move: "1500", bonus: "0" },
    expect: ["2739000", "37500", "房屋性质 办公", "补偿方式 产权调换(等面积)", "产权调换面积"],
    ref: 'area=75 price=36000 type=2(办公) method=1(产权调换(等面积)) temp=20 tempRate=25 move=1500 bonus=0(无奖励)；房屋补偿=2700000 临时安置=37500 搬迁=1500 奖励金=0 总额=2739000。type=2 办公：锚『房屋性质 办公』（默认『住宅』）+ method=1；bonus=0 故不锚奖励金'
  },
  {
    slug: "realestate/assessor-23",
    inputs: { cv: "250", used: "5", durable: "40", salvage: "3", struct: "7", decor: "5", equip: "7", method: "0" },
    expect: ["80.8%", "202.00"],
    ref: 'cv=250 used=5 durable=40 salvage=3 struct=7 decor=5 equip=7 method=0(加权平均)；年限法87.5% 打分法74.1% 综合80.8% 评估值202.00 残值7.50'
  },
  {
    slug: "realestate/assessor-23",
    inputs: { cv: "180", used: "12", durable: "60", salvage: "4", struct: "9", decor: "9", equip: "9", method: "1" },
    expect: ["144.00", "20.0%"],
    ref: 'cv=180 used=12 durable=60 salvage=4 method=1(仅年限法)；成新率80.0% 评估值144.00 残值7.20 折旧率20.0%。method=1 判别：若为加权平均则 rate=(80+100)/2=90 → 162.00'
  },
  {
    slug: "realestate/assessor-23",
    inputs: { cv: "320", used: "10", durable: "50", salvage: "8", struct: "3", decor: "3", equip: "5", method: "2" },
    expect: ["42.8%", "136.96"],
    ref: 'cv=320 salvage=8 struct=3 decor=3 equip=5 method=2(仅打分法)；打分法=(1.8+0.6+1.0)/9*100*0.92+8=42.756 → 42.8% 评估值136.96 残值25.60'
  },
  {
    slug: "realestate/assessor-23",
    inputs: { cv: "420", used: "8", durable: "80", salvage: "20", struct: "9", decor: "9", equip: "9", method: "1" },
    expect: ["378.00", "84.00"],
    ref: 'cv=420 used=8 durable=80 salvage=20 method=1(仅年限法)；成新率90.0% 评估值378.00 残值84.00。高残值率20%下打分法=100% → 若误走加权平均则为95% → 399.00'
  },
  {
    slug: "realestate/assessor-23",
    inputs: { cv: "500", used: "10", durable: "50", salvage: "20", struct: "3", decor: "3", equip: "3", method: "2" },
    expect: ["46.7%", "233.50"],
    ref: 'cv=500 salvage=20 struct=3 decor=3 equip=3 method=2(仅打分法)；打分法=3/9*100*0.8+20=46.667 → 46.7% 评估值233.50 残值100.00（打分法下限形态）'
  },
  {
    slug: "realestate/assessor-23",
    inputs: { cv: "75", used: "45", durable: "40", salvage: "10", struct: "5", decor: "7", equip: "5", method: "0" },
    expect: ["24.00", "68.0%"],
    ref: 'cv=75 used=45 durable=40 salvage=10 struct=5 decor=7 equip=5 method=0；年限法=(40-45)/40<0 截断为0，打分法=(3+1.4+1)/9*100*0.9+10=64 → 综合32.0% 评估值24.00 折旧率68.0%（测 ageRate 负值截断分支）'
  },
  {
    slug: "realestate/assessor-40",
    inputs: { rebuild: "300", used: "6", durable: "40", loss: "25", method: "0", insured: "360" },
    expect: ["255.00", "75.00"],
    ref: 'rebuild=300 used=6 durable=40 loss=25 method=0(比例赔偿) insured=360；折旧率15.0% 实际价值255.00 损失金额75.00 投保比例1.2(足额，ratio>1 取 1) 赔偿金额75.00。判别：若 ratio 未 clamp 则赔偿=75×1.2=90.00'
  },
  {
    slug: "realestate/assessor-40",
    inputs: { rebuild: "400", used: "15", durable: "60", loss: "50", method: "1", insured: "120" },
    expect: ["300.00", "120.00", "第一危险赔偿方式下"],
    ref: 'rebuild=400 used=15 durable=60 loss=50 method=1(第一危险) insured=120；实际价值300.00 损失金额200.00 赔偿=min(200,120)=120.00。判别：若误走比例赔偿则 200×0.3=60.00'
  },
  {
    slug: "realestate/assessor-40",
    inputs: { rebuild: "260", used: "5", durable: "25", loss: "20", method: "1", insured: "180" },
    expect: ["208.00", "52.00"],
    ref: 'rebuild=260 used=5 durable=25 loss=20 method=1(第一危险) insured=180；折旧率20.0% 实际价值208.00 损失金额52.00 赔偿=min(52,180)=52.00（损失<保额，全额赔付）'
  },
  {
    slug: "realestate/assessor-40",
    inputs: { rebuild: "500", used: "20", durable: "80", loss: "40", method: "0", insured: "300" },
    expect: ["375.00", "120.00", "不足额投保(60%)"],
    ref: 'rebuild=500 used=20 durable=80 loss=40 method=0(比例赔偿) insured=300；实际价值375.00 损失金额200.00 投保比例0.6 → 赔偿=200×0.6=120.00，附加提示『赔偿金额仅为损失的60%』'
  },
  {
    slug: "realestate/assessor-40",
    inputs: { rebuild: "180", used: "30", durable: "30", loss: "35", method: "0", insured: "90" },
    expect: ["100.0%", "31.50"],
    ref: 'rebuild=180 used=30 durable=30 loss=35 method=0 insured=90；折旧率100.0% ⇒ 实际价值截断为0.00（0.00 是默认串 200.00 的子串，故不锚）损失金额63.00 赔偿=63×0.5=31.50'
  },
  {
    slug: "realestate/assessor-40",
    inputs: { rebuild: "320", used: "60", durable: "40", loss: "12.5", method: "0", insured: "320" },
    expect: ["150.0%", "40.00"],
    ref: 'rebuild=320 used=60 durable=40 loss=12.5 method=0 insured=320；折旧率150.0%>100% ⇒ 实际价值=320×(1−1.5)<0 截断为0（测 av<0 分支）投保比例1.0(足额) 损失金额40.00 赔偿40.00'
  },
  {
    slug: "realestate/assessor-42",
    inputs: { area: "8", output: "4500", landComp: "10", resettle: "6", attach: "25000", crop: "1200", popul: "6" },
    expect: ["556600", "360000", "4500元/亩×10倍×8亩"],
    ref: 'area=8 output=4500 landComp=10倍 resettle=6倍 attach=25000 crop=1200 popul=6；土地补偿费360000 安置补助费162000 青苗9600 总额556600。30倍上限：10×8+6×6=116 < 240 ⇒ 不触发警告'
  },
  {
    slug: "realestate/assessor-42",
    inputs: { area: "2", output: "5000", landComp: "20", resettle: "15", attach: "30000", crop: "900", popul: "8" },
    expect: ["831800", "600000", "超过30倍上限"],
    ref: 'area=2 output=5000 landComp=20倍(最高) resettle=15倍(最高) attach=30000 crop=900 popul=8；土地补偿费200000 安置补助费600000 青苗1800 总额831800。20×2+15×8=160 > 30×2=60 ⇒ 触发30倍上限警告（默认态不触发，故该串可锚）'
  },
  {
    slug: "realestate/assessor-42",
    inputs: { area: "5", output: "4000", landComp: "10", resettle: "15", attach: "15000", crop: "1000", popul: "6" },
    expect: ["580000", "360000", "4000元/亩×15倍×6人"],
    ref: 'area=5 output=4000 landComp=10倍 resettle=15倍(最高) attach=15000 crop=1000 popul=6；土地补偿费200000 安置补助费360000 青苗5000 总额580000。10×5+15×6=140 < 150 ⇒ 边界附近不触发警告（与例2 同 area 量级、仅倍数不同，构成警告分支对照）'
  },
  {
    slug: "realestate/assessor-42",
    inputs: { area: "3", output: "6000", landComp: "8", resettle: "10", attach: "0", crop: "500", popul: "0" },
    expect: ["145500", "144000", "6000元/亩×10倍×0人"],
    ref: 'area=3 output=6000 landComp=8倍 resettle=10倍 attach=0 crop=500 popul=0；安置补助费=0（无人需安置）青苗1500 总额145500。判别：popul=0 若被当作缺省人数则总额不同'
  },
  {
    slug: "realestate/assessor-42",
    inputs: { area: "120", output: "2000", landComp: "6", resettle: "4", attach: "80000", crop: "600", popul: "30" },
    expect: ["1832000", "1440000"],
    ref: 'area=120 output=2000 landComp=6倍(最低) resettle=4倍(最低) attach=80000 crop=600 popul=30；土地补偿费1440000 安置补助费240000 青苗72000 总额1832000。6×120+4×30=840 < 3600 ⇒ 不触发（大面积下最低倍数仍合规）'
  },
  {
    slug: "realestate/assessor-42",
    inputs: { area: "0", output: "2000", landComp: "6", resettle: "4", attach: "0", crop: "500", popul: "3" },
    expect: ["24000", "超过30倍上限"],
    ref: 'area=0 output=2000 landComp=6倍 resettle=4倍 attach=0 crop=500 popul=3；土地补偿费0 青苗0 安置补助费=2000×4×3=24000 总额24000。30倍上限分母 output×30×area=0 ⇒ 只要安置费>0 即触发警告（area=0 边界，上限判断退化为恒真）'
  },
  {
    slug: "realestate/assessor-43",
    inputs: { assets: "8000", liab: "2400", intang: "1200", equity: "67", premium: "15" },
    expect: ["6440.00", "4314.80", "67%股权价值"],
    ref: 'assets=8000 liab=2400 intang=1200 equity=67%(绝对控股) premium=15；净资产5600 整体价值=5600×1.15=6440.00 股权价值=6440×0.67=4314.80 无形资产占比15.0% 资产负债率30.0%（两提示均不触发）'
  },
  {
    slug: "realestate/assessor-43",
    inputs: { assets: "6000", liab: "1500", intang: "2400", equity: "100", premium: "-10" },
    expect: ["4050.00", "无形资产占比较高(40.0%)"],
    ref: 'assets=6000 liab=1500 intang=2400 equity=100% premium=-10(折价)；净资产4500 整体价值=4500×0.9=4050.00 无形资产占比40.0%>30 ⇒ 追加『建议结合收益法评估』提示。判别：premium 符号若反则 4950.00'
  },
  {
    slug: "realestate/assessor-43",
    inputs: { assets: "10000", liab: "7500", intang: "1000", equity: "34", premium: "5" },
    expect: ["2625.00", "892.50", "资产负债率偏高(75.0%)"],
    ref: 'assets=10000 liab=7500 intang=1000 equity=34%(否决权) premium=5；净资产2500 整体价值2625.00 股权价值=2625×0.34=892.50 资产负债率75.0%>70 ⇒ 追加『财务风险较大』提示（无形资产占比10.0% 不触发）'
  },
  {
    slug: "realestate/assessor-43",
    inputs: { assets: "5000", liab: "4000", intang: "2000", equity: "51", premium: "20" },
    expect: ["1200.00", "612.00", "无形资产占比较高(40.0%)", "资产负债率偏高(80.0%)"],
    ref: 'assets=5000 liab=4000 intang=2000 equity=51%(相对控股) premium=20；净资产1000 整体价值1200.00 股权价值612.00。两提示同时触发（占比40.0% 且 负债率80.0%）——覆盖『if+if 双命中』分支组合'
  },
  {
    slug: "realestate/assessor-43",
    inputs: { assets: "9000", liab: "1000", intang: "500", equity: "10", premium: "-50" },
    expect: ["4000.00", "400.00", "10%股权价值"],
    ref: 'assets=9000 liab=1000 intang=500 equity=10%(最小档) premium=-50(折价下限)；净资产8000 整体价值=8000×0.5=4000.00 股权价值=4000×0.1=400.00。覆盖 equity 末档 + premium 下限'
  },
  {
    slug: "realestate/assessor-43",
    inputs: { assets: "3000", liab: "3600", intang: "300", equity: "100", premium: "10" },
    expect: ["-660.00", "资产负债率偏高(120.0%)"],
    ref: 'assets=3000 liab=3600 intang=300 equity=100% premium=10；净资产=-600（资不抵债）整体价值=-600×1.1=-660.00 资产负债率120.0%>70 ⇒ 触发提示。覆盖负净资产形态（锚 -660.00 带负号，非默认子串）'
  },
  {
    slug: "realestate/assessor-44",
    inputs: { type: "1", revenue: "2500", margin: "8", years: "10", rate: "12", tax: "20" },
    expect: ["904.04", "160.00", "专利权的收益期限"],
    ref: 'type=1(专利权) revenue=2500 margin=8 years=10 rate=12 tax=20；超额利润200.00 税后160.00 年金现值系数(12%,10)=(1−1.12^−10)/0.12=5.650223 ⇒ 评估价值904.04。锚『专利权的收益期限』锁 type select（默认商标权）'
  },
  {
    slug: "realestate/assessor-44",
    inputs: { type: "4", revenue: "3000", margin: "6", years: "999", rate: "15", tax: "25" },
    expect: ["900.00", "135.00", "评估价值=税后超额收益/资本化率"],
    ref: 'type=4(商誉) revenue=3000 margin=6 years=999(无限期) rate=15 tax=25；超额利润180.00 税后135.00 value=135/0.15=900.00。锚『评估价值=税后超额收益/资本化率』（years>=999 分支独有；默认态是『×年金现值系数』版）'
  },
  {
    slug: "realestate/assessor-44",
    inputs: { type: "3", revenue: "5000", margin: "4", years: "20", rate: "8", tax: "15" },
    expect: ["1669.09", "170.00", "特许经营权的收益期限"],
    ref: 'type=3(特许经营权) revenue=5000 margin=4 years=20(长期) rate=8 tax=15；超额利润200.00 税后170.00 系数(8%,20)=(1−1.08^−20)/0.08=9.818148 ⇒ 1669.09'
  },
  {
    slug: "realestate/assessor-44",
    inputs: { type: "2", revenue: "800", margin: "12", years: "15", rate: "20", tax: "30" },
    expect: ["314.19", "67.20", "著作权的收益期限"],
    ref: 'type=2(著作权) revenue=800 margin=12 years=15 rate=20 tax=30；超额利润96.00 税后67.20 系数(20%,15)=(1−1.2^−15)/0.2=4.675473 ⇒ 314.19（高折现率 + 高税率组合）'
  },
  {
    slug: "realestate/assessor-44",
    inputs: { type: "0", revenue: "1200", margin: "10", years: "10", rate: "10", tax: "0" },
    expect: ["737.35", "120.00"],
    ref: 'type=0(商标权) revenue=1200 margin=10 years=10 rate=10 tax=0(免税边界)；超额利润120.00 税后=120.00（tax=0 ⇒ 不折税）系数(10%,10)=6.144567 ⇒ 737.35。判别：tax 若未生效则税后90 ⇒ 552.99'
  },
  {
    slug: "realestate/assessor-44",
    inputs: { type: "1", revenue: "600", margin: "15", years: "5", rate: "1", tax: "25" },
    expect: ["327.61", "67.50"],
    ref: 'type=1(专利权) revenue=600 margin=15 years=5 rate=1(折现率下限) tax=25；超额利润90.00 税后67.50 系数(1%,5)=(1−1.01^−5)/0.01=4.853431 ⇒ 327.61。覆盖 rate 下限（折现率越小系数越大）'
  },
  {
    slug: "realestate/assessor-45",
    inputs: { val: "50000", market: "42000", tax: "1", stage: "1" },
    expect: ["8000.00", "48.00", "适用税种 房产税", "2/3 当前阶段"],
    ref: 'val=50000 market=42000 tax=1(房产税 0.6%) stage=1(异议阶段)；差额8000.00 多缴税款=8000×0.006=48.00。锚『适用税种 房产税』锁 tax select、『2/3 当前阶段』锁 stage（默认 1/3）'
  },
  {
    slug: "realestate/assessor-45",
    inputs: { val: "8000", market: "9500", tax: "2", stage: "2" },
    expect: ["-1500.00", "-75.00", "评估偏低 差额方向", "3/3 当前阶段", "适用税率 5%"],
    ref: 'val=8000 market=9500 tax=2(增值税 5%) stage=2(复议阶段)；差额−1500.00（评估低于市场）多缴/少缴=−1500×0.05=−75.00。覆盖 diff<0 分支（默认 diff>0）与 stage 末档'
  },
  {
    slug: "realestate/assessor-45",
    inputs: { val: "30000", market: "28000", tax: "3", stage: "0" },
    expect: ["2000.00", "80.00", "适用税种 土地增值税"],
    ref: 'val=30000 market=28000 tax=3(土地增值税) stage=0；差额2000.00 税款=2000×0.04=80.00。注：页面 taxRates[3]=0.04 与 select 标签『30%-60%』不一致（实现取简化值 4%），按实现复算锚定，仅留档不改页面'
  },
  {
    slug: "realestate/assessor-45",
    inputs: { val: "15000", market: "15000", tax: "0", stage: "2" },
    expect: ["评估结果： 评估价值与市场价值一致", "3/3 当前阶段"],
    ref: 'val=market=15000 tax=0 stage=2；差额=0 ⇒ 走第三分支『评估价值与市场价值一致，无争议』（默认态为 diff>0 分支）。0.00 系默认串 20.00 的子串故不锚数值'
  },
  {
    slug: "realestate/assessor-45",
    inputs: { val: "120000", market: "100000", tax: "0", stage: "2" },
    expect: ["20000.00", "400.00", "评估完成后 已完成"],
    ref: 'val=120000 market=100000 tax=0(契税 2%) stage=2；差额20000.00 税款=20000×0.02=400.00。锚『评估完成后 已完成』（stage>0 时第一阶段行状态为已完成，默认态为『当前』）'
  },
  {
    slug: "realestate/assessor-45",
    inputs: { val: "60000", market: "75000", tax: "0", stage: "1" },
    expect: ["-15000.00", "-300.00", "评估价值低于市场价值"],
    ref: 'val=60000 market=75000 tax=0(契税 2%) stage=1；差额−15000.00 税款=−15000×0.02=−300.00。覆盖 diff<0 + 契税组合，锚偏低提示串（默认态为『评估价值高于市场价值』串）'
  },
  {
    slug: "realestate/assessor-46",
    inputs: { a1: "3", a2: "2", a3: "3", a4: "3", a5: "3", a6: "3", a7: "3", a8: "3" },
    expect: ["职业道德评分： 23 / 24", "2. 客观公正 2 / 3 基本合规"],
    ref: 't=23 优秀档，a2 降 2 分；基本合规状态'
  },
  {
    slug: "realestate/assessor-46",
    inputs: { a1: "3", a2: "3", a3: "3", a4: "3", a5: "3", a6: "3", a7: "0", a8: "0" },
    expect: ["职业道德评分： 18 / 24", "合规等级： 良好", "8. 收费合规 0 / 3 不合规"],
    ref: 't=18 良好档，末两项 0 分'
  },
  {
    slug: "realestate/assessor-46",
    inputs: { a1: "3", a2: "3", a3: "3", a4: "3", a5: "1", a6: "0", a7: "0", a8: "0" },
    expect: ["职业道德评分： 13 / 24", "合规评价： 职业道德存在不足，需针对性改进。", "改进建议： 请针对不合规项目"],
    ref: 't=13 需改进档且触发改进建议'
  },
  {
    slug: "realestate/assessor-46",
    inputs: { a1: "3", a2: "2", a3: "0", a4: "0", a5: "0", a6: "0", a7: "0", a8: "0" },
    expect: ["职业道德评分： 5 / 24", "合规等级： 不合格", "合规评价： 职业道德严重不合规"],
    ref: 't=5 不合格档'
  },
  {
    slug: "realestate/assessor-46",
    inputs: { a1: "0", a2: "3", a3: "3", a4: "3", a5: "3", a6: "3", a7: "3", a8: "3" },
    expect: ["职业道德评分： 21 / 24", "1. 独立性 0 / 3 不合规"],
    ref: 't=21 优秀档下边界（误写 >21 则落良好）'
  },
  {
    slug: "realestate/assessor-46",
    inputs: { a1: "3", a2: "3", a3: "3", a4: "3", a5: "3", a6: "1", a7: "0", a8: "0" },
    expect: ["职业道德评分： 16 / 24", "合规等级： 良好", "6. 利益冲突回避 1 / 3 需改进"],
    ref: 't=16 良好档下边界且不触发改进建议（t<16 严格）'
  },
  {
    slug: "realestate/assessor-47",
    inputs: { a1: "5", a2: "5", a3: "5", a4: "5", a5: "5", a6: "3" },
    expect: ["区位评分： 28 / 30", "加权评分： 96.0 / 100", "6. 规划前景 10% 3 / 5 6.0"],
    ref: 't=28 优质档（等级串与默认同为优质，故只锚评分/加权/明细行）'
  },
  {
    slug: "realestate/assessor-47",
    inputs: { a1: "4", a2: "4", a3: "4", a4: "4", a5: "3", a6: "3" },
    expect: ["区位评分： 22 / 30", "加权评分： 75.0 / 100", "区位等级： 良好区位"],
    ref: 't=22 良好档，权重表正确则加权 75.0'
  },
  {
    slug: "realestate/assessor-47",
    inputs: { a1: "3", a2: "3", a3: "3", a4: "2", a5: "2", a6: "2" },
    expect: ["区位评分： 15 / 30", "加权评分： 52.0 / 100", "区位等级： 一般区位", "薄弱项： 商业配套、环境质量、规划前景评分较低"],
    ref: 't=15 一般档下边界 + 薄弱项三连（误写 >15 落较差档）'
  },
  {
    slug: "realestate/assessor-47",
    inputs: { a1: "2", a2: "2", a3: "2", a4: "2", a5: "2", a6: "1" },
    expect: ["区位评分： 11 / 30", "加权评分： 38.0 / 100", "区位等级： 较差区位", "薄弱项： 交通便利度、教育配套"],
    ref: 't=11 较差档 + 六项全薄弱'
  },
  {
    slug: "realestate/assessor-47",
    inputs: { a1: "5", a2: "5", a3: "5", a4: "5", a5: "4", a6: "1" },
    expect: ["区位评分： 25 / 30", "加权评分： 89.0 / 100", "6. 规划前景 10% 1 / 5 2.0"],
    ref: 't=25 优质档下边界（误写 >25 落良好档）'
  },
  {
    slug: "realestate/assessor-47",
    inputs: { a1: "4", a2: "4", a3: "4", a4: "4", a5: "2", a6: "2" },
    expect: ["区位评分： 20 / 30", "加权评分： 70.0 / 100", "薄弱项： 环境质量、规划前景评分较低"],
    ref: 't=20 良好档下边界；与例 2 同为 20 分但加权 70.0≠75.0，可判权重表非等权平均'
  },
  {
    slug: "realestate/assessor-41",
    inputs: { a1: "1", a2: "1", a3: "2", a4: "2", a5: "2", a6: "2", a7: "2", a8: "2" },
    expect: ["合规评分： 14 / 16", "1. 鉴定主体资格 1 / 2 需完善"],
    ref: 't=14 合规档下边界（误写 >14 落基本合规）；等级名『合规』与默认同串故不锚'
  },
  {
    slug: "realestate/assessor-41",
    inputs: { a1: "1", a2: "1", a3: "1", a4: "1", a5: "2", a6: "2", a7: "2", a8: "2" },
    expect: ["合规评分： 12 / 16", "合规等级： 基本合规", "4. 现场勘验 1 / 2 需完善"],
    ref: 't=12 基本合规档 + 需完善状态行'
  },
  {
    slug: "realestate/assessor-41",
    inputs: { a1: "1", a2: "1", a3: "1", a4: "1", a5: "1", a6: "1", a7: "2", a8: "2" },
    expect: ["合规评分： 10 / 16", "合规等级： 基本合规", "6. 报告规范 1 / 2 需完善"],
    ref: 't=10 基本合规下边界且风险提示不触发（与例 4 配对区分 <10 / <=10）'
  },
  {
    slug: "realestate/assessor-41",
    inputs: { a1: "1", a2: "1", a3: "1", a4: "1", a5: "1", a6: "1", a7: "1", a8: "2" },
    expect: ["合规评分： 9 / 16", "合规等级： 部分违规", "风险提示： 评估程序存在违规情形"],
    ref: 't=9 部分违规档且风险提示触发'
  },
  {
    slug: "realestate/assessor-41",
    inputs: { a1: "0", a2: "0", a3: "1", a4: "1", a5: "1", a6: "1", a7: "1", a8: "1" },
    expect: ["合规评分： 6 / 16", "合规等级： 部分违规", "1. 鉴定主体资格 0 / 2 违规", "风险提示： 评估程序存在违规情形"],
    ref: 't=6 部分违规下边界 + 违规状态行'
  },
  {
    slug: "realestate/assessor-41",
    inputs: { a1: "0", a2: "0", a3: "0", a4: "0", a5: "0", a6: "1", a7: "1", a8: "1" },
    expect: ["合规评分： 3 / 16", "合规等级： 严重违规", "合规评价： 评估程序严重违规，评估结果不可采信，建议重新评估。"],
    ref: 't=3 严重违规档 + 结论串'
  },
  {
    slug: "realestate/assessor-risk-10",
    inputs: { a1: "4", a2: "4", a3: "4", a4: "4", a5: "4", invest: "3000", revenue: "600" },
    expect: ["20 风险指数/100", "20 安全评分/25", "5.0 回本年限", "20.0% 投资回报率"],
    ref: 't=20 低风险档下边界（风险指数=100−20/25×100=20）；等级串与默认同为『低风险』故不锚'
  },
  {
    slug: "realestate/assessor-risk-10",
    inputs: { a1: "4", a2: "4", a3: "3", a4: "3", a5: "3", invest: "8000", revenue: "1000" },
    expect: ["32 风险指数/100", "风险等级： 中等风险", "8.0 回本年限", "12.5% 投资回报率"],
    ref: 't=17 中等风险档；风险指数与财务两表同时锁定'
  },
  {
    slug: "realestate/assessor-risk-10",
    inputs: { a1: "4", a2: "3", a3: "3", a4: "3", a5: "2", invest: "2000", revenue: "500" },
    expect: ["40 风险指数/100", "风险等级： 中等风险", "高风险项： 环境风险风险较高", "4.0 回本年限"],
    ref: 't=15 中等风险档下边界 + 高风险项单项（仅环境风险）'
  },
  {
    slug: "realestate/assessor-risk-10",
    inputs: { a1: "3", a2: "3", a3: "2", a4: "2", a5: "2", invest: "12000", revenue: "800" },
    expect: ["52 风险指数/100", "风险等级： 较高风险", "高风险项： 政策风险、财务风险、环境风险", "15.0 回本年限"],
    ref: 't=12 较高风险档 + 高风险项三项连续'
  },
  {
    slug: "realestate/assessor-risk-10",
    inputs: { a1: "2", a2: "2", a3: "2", a4: "2", a5: "2", invest: "5000", revenue: "0" },
    expect: ["60 风险指数/100", "风险等级： 较高风险", "回本年限 -年", "投资回报率 0.0%"],
    ref: 't=10 较高风险档下边界 + revenue=0 ⇒ 回本年限退化为『-』、roi 为 0.0%'
  },
  {
    slug: "realestate/assessor-risk-10",
    inputs: { a1: "1", a2: "1", a3: "1", a4: "1", a5: "1", invest: "0", revenue: "300" },
    expect: ["80 风险指数/100", "风险等级： 高风险", "投资回报率 0%", "高风险项： 市场风险、运营风险、政策风险、财务风险、环境风险"],
    ref: 't=5 高风险档 + invest=0 ⇒ roi 走兜底字面量『0』（非 0.0）+ 高风险项全五项'
  },
  {
    slug: "realestate/analysis-risk-1",
    inputs: { inv: "5000000", rate: "8", data: "Y1,1200000\nY2,1500000\nY3,1800000\nY4,1600000\nY5,1200000" },
    expect: ["现金流期数： 5", "NPV： 818764.98", "IRR： 13.94%", "静态回收期： 3.31 年", "动态回收期： 4.00 年", "可行（NPV 为正）"],
    ref: '五年期主路径：NPV 正、IRR 走二分分支，静态/动态回收期均有解'
  },
  {
    slug: "realestate/analysis-risk-1",
    inputs: { inv: "100000", rate: "12", data: "Y1,1000000" },
    expect: ["NPV： 792857.14", "IRR： >200%", "折现率： 12.00%", "静态回收期： 0.10 年"],
    ref: 'IRR 上界分支：npvAt(2.0)>0 ⇒ 显示 >200%（不进二分）'
  },
  {
    slug: "realestate/analysis-risk-1",
    inputs: { inv: "1000000", rate: "8", data: "Y1,1000" },
    expect: ["NPV： -999074.07", "IRR： <-90%", "静态回收期： 计算期内未收回"],
    ref: 'IRR 下界分支：npvAt(-0.9)<0 ⇒ 显示 <-90%；两个回收期均未收回'
  },
  {
    slug: "realestate/analysis-risk-1",
    inputs: { inv: "3000000", rate: "15", data: "Y1,1000000\nY2,1000000\nY3,1200000" },
    expect: ["NPV： -585271.64", "静态回收期： 2.83 年", "IRR： 3.20%", "现金流合计： 3200000.00"],
    ref: '静态回收期有解而动态未收回；『动态回收期： 计算期内未收回』与默认同串已弃用，改锚 NPV/IRR/合计'
  },
  {
    slug: "realestate/analysis-risk-1",
    inputs: { inv: "1000000", rate: "0", data: "Y1,500000\nY2,600000" },
    expect: ["折现率： 0.00%", "NPV： 100000.00", "静态回收期： 1.83 年", "动态回收期： 1.83 年", "可行（NPV 为正）"],
    ref: '折现率 0 ⇒ 折现值=净现金流，静态与动态回收期必然相等（1.83 年）'
  },
  {
    slug: "realestate/analysis-risk-1",
    inputs: { inv: "2000000", rate: "10", data: "Y1,500000\nY2,-300000\nY3,800000" },
    expect: ["NPV： -1192336.59", "静态回收期： 计算期内未收回", "现金流合计： 1000000.00", "Y2 -300000.00 -247933.88", "IRR： -24.58%"],
    ref: '含负现金流期：IRR 解为负值(-24.58%)、两回收期均未收回；判定串与默认同为『不可行』故不锚'
  }
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