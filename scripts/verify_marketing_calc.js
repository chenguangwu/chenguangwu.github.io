#!/usr/bin/env node
/**
 * 第 25 道门禁：marketing 分类计算正确性验证（14 个确定性数值工具 / 24 个用例）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：estimate-sample-size-confidence（含 select :checked 查询，stub 不稳）；
 *       funnel-calculator / market-share（多行/多 competitor 动态结构，框架难注入）；
 *       ad-roi / marketing-roi（buyMode 切换全局 + 多分支）。
 * 用法: node scripts/verify_marketing_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "marketing/marketing-ctr-calculator",
    inputs: { impressions: "10000", clicks: "500", cost: "2000", conversions: "50" },
    expect: ["10.00", "4.00"],
    ref: "ctr=500/10000×100=5.00；cvr=50/500×100=10.00；cpc=2000/500=4.00；cpm=2000/10000×1000=200.00",
  },
  {
    slug: "marketing/marketing-conversion-rate-calculator",
    inputs: { visitors: "1000", conversions: "50", totalCost: "5000", avgOrder: "200" },
    expect: ["5.00", "100.00"],
    ref: "cvr=50/1000×100=5.00；cpa=5000/50=100.00；revenue=50×200=10000；roas=10000/5000=2.00",
  },
  {
    slug: "marketing/marketing-churn-rate",
    inputs: { startCustomers: "1000", endCustomers: "900", newCustomers: "100", arpu: "50" },
    expect: ["20.00", "80.00", "5.00"],
    ref: "lost=1000+100-900=200；churnRate=200/1000×100=20.00；retention=80.00；lifespan=1/(0.2)=5.00",
  },
  {
    slug: "marketing/marketing-roas-calculator",
    inputs: { adSpend: "8000", adRevenue: "50000" },
    expect: ["6.25x", "广告毛利润 ¥42,000.00"],
    ref: "roas=50000/8000=6.25；profit=42000；profitMargin=42000/50000×100=84.0（原 10000/40000 与默认 5000/20000 比值相同 → 逃生项）",
  },
  {
    slug: "marketing/marketing-cac-calculator",
    inputs: { marketingSpend: "8000", salesSpend: "2000", newCustomers: "100", ltv: "500" },
    expect: ["100.00", "80.00"],
    ref: "totalSpend=10000；cac=10000/100=100.00；marketingCAC=8000/100=80.00；ltvCacRatio=500/100=5.00",
  },
  {
    slug: "marketing/marketing-ltv-calculator",
    inputs: { mrrDetail: "100", churnDetail: "10", marginDetail: "60", cacDetail: "200" },
    expect: ["600.00", "3.00"],
    ref: "默认 detail 模式：lifespanMonths=1/(10/100)=10；ltvGross=100×10=1000；ltv=1000×0.6=600.00；LTV:CAC=600/200=3.00",
  },
  {
    slug: "marketing/marketing-markup-margin",
    inputs: { costMarkup: "180", markupRate: "35" },
    expect: ["¥243.00", "¥63.00", "25.93%"],
    ref: "price=180×1.35=243.00；profit=63.00；marginRate=63/243×100=25.93%。"
       + "原 100/50 即页面默认态，150.00/33.33 回退默认仍命中 ⇒ 逃生项，已换非默认输入。",
  },
  {
    slug: "marketing/marketing-discount-rate",
    inputs: { origPrice: "200", discountPct: "20" },
    expect: ["160.00", "40.00"],
    ref: "salePrice=200×0.8=160.00；saveAmount=40.00（percent 模式默认）",
  },
  {
    slug: "marketing/marketing-break-even-roas",
    inputs: { price: "100", margin: "40" },
    expect: ["40.00"],
    ref: "marginRatio=0.4；breakEvenRoas=1/0.4=2.50；profitPerUnit=100×0.4=40.00",
  },
  {
    slug: "marketing/calc-1",
    inputs: { spend: "25000", revenue: "90000", conversions: "250", costRate: "25" },
    expect: ["170.00%", "3.60", "42,500.00", "47.22%"],
    ref: "cogs=90000×0.25=22500；profit=90000−25000−22500=42500；roi=42500/25000=170.00%；"
       + "roas=90000/25000=3.60；利润率=42500/90000=47.22%；cpa=25000/250=100.00"
       + "（与默认态 CPA 同值 ⇒ 不入断言，否则回退默认仍命中）。",
  },
  {
    slug: "marketing/marketing-ltv-cac-ratio",
    inputs: { ltv: "600", cac: "200" },
    expect: ["3.00", "200.00"],
    ref: "ratio=600/200=3.00；profit=400；roi=(400/200)×100=200.00；paybackMonths=200/(600/36)=12.00",
  },
  {
    slug: "marketing/calc-price-elasticity",
    inputs: { p1: "100", q1: "100", p2: "90", q2: "120" },
    expect: ["-1.727"],
    ref: "midQ=110,midP=95；pctQ=20/110×100=18.18；pctP=-10/95×100=-10.53；ed=18.18/-10.53=-1.73（|Ed|>1 富有弹性）",
  },
  {
    slug: "marketing/price-elasticity",
    inputs: { p1: "100", q1: "100", p2: "110", q2: "80" },
    expect: ["-2.33"],
    ref: "avgQ=90,avgP=105；pctQ=-20/90×100=-22.22；pctP=10/105×100=9.52；ped=-22.22/9.52=-2.33（|Ed|>1 富有弹性）",
  },
  // ── 广告投放 ROI 测算（marketing/ad-roi）：CPC / CPM 双计费分支 ──
  {
    // CPC 盈利档：非默认（预算 2 万元、CPC 4 元、CTR 2%、CVR 6%、客单 300 元、毛利 40%＋固定成本 1000 元）
    slug: "marketing/ad-roi",
    inputs: { budget: "20000", cpc: "4", ctr: "2", cvr: "6", aov: "300", costRate: "40", fixedCost: "1000" },
    clicks: ["setBuy('cpc');calc();"],
    expect: ["4.50 ROAS", "57.9% 综合 ROI", "250,000 展示量"],
    ref: "CPC 分支：点击 = 20000/4 = 5000；展示 = 点击/CTR = 5000/2% = 250,000；转化 = 5000×6% = 300；"
     + "收入 = 300×300 = 90000；商品成本 = 90000×40% = 36000；总成本 = 20000+36000+1000 = 57000；"
     + "利润 = 33000；ROAS = 90000/20000 = 4.50；ROI = 33000/57000 = 57.89% ⇒ 57.9%。盈亏平衡 ROAS"
     + " = 1/(1−40%) = 1.67，4.50 ≥ 1.67 ⇒ 盈利。默认态（1 万元 / CPC 2 / CTR 3% / CVR 5% /客单 200 /"
     + "毛利 50% / 固定 0）为 −33.3% / ROAS 5.00，三条均不命中。",
  },
  {
    // CPC 亏损档：非默认（预算 5000、CPC 5、CTR 1%、CVR 2%、客单 100、毛利 60%＋固定 200）
    slug: "marketing/ad-roi",
    inputs: { budget: "5000", cpc: "5", ctr: "1", cvr: "2", aov: "100", costRate: "60", fixedCost: "200" },
    clicks: ["setBuy('cpc');calc();"],
    expect: ["0.40 ROAS", "-68.8% 综合 ROI", "5.00%"],
    ref: "点击 = 5000/5 = 1000；展示 = 1000/1% = 100,000；转化 = 20；收入 = 2000；商品成本 = 1200；"
     + "总成本 = 5000+1200+200 = 6400；利润 = −4400；ROAS = 0.40；ROI = −4400/6400 = −68.75% ⇒ −68.8%。"
     + "盈亏平衡 ROAS = 1/40% = 2.50；补亏提示「转化率需提升至 (5000/100)/1000 = 5.00% 或客单价提升至"
     + " 5000/(1000×2%) = 250 元」。默认态三条全不命中。",
  },
  {
    // CPM 计费分支（buyMode 默认 cpc，用例显式切 cpm）：非默认（预算 8000、CPM 40、CTR 2.5%、CVR 4%）
    slug: "marketing/ad-roi",
    inputs: { budget: "8000", cpm: "40", ctr: "2.5", cvr: "4", aov: "250", costRate: "45", fixedCost: "500" },
    clicks: ["setBuy('cpm');calc();"],
    expect: ["6.25 ROAS", "61.3% 综合 ROI", "200,000 展示量"],
    ref: "CPM 分支：展示 = 8000/40×1000 = 200,000；点击 = 200,000×2.5% = 5000；转化 = 200；收入 ="
     + " 200×250 = 50000；商品成本 = 22500；总成本 = 8000+22500+500 = 31000；利润 = 19000；"
     + "ROAS = 50000/8000 = 6.25；ROI = 19000/31000 = 61.29% ⇒ 61.3%；盈亏平衡 ROAS = 1/55% = 1.82。"
     + "注意 CPC 分支会读 #cpc（默认值 2），本例不参与计算（默认态走 cpc 分支，三条全不命中）。",
  },
  {
    // 零转化边界：CVR=0 ⇒ 转化/收入为 0，CPA 回落 0；客单价补亏项出现 ∞（fmt(Infinity)）
    slug: "marketing/ad-roi",
    inputs: { budget: "1000", cpc: "3", cvr: "0", fixedCost: "300" },
    clicks: ["setBuy('cpc');calc();"],
    expect: ["-100.0% 综合 ROI", "∞ 元"],
    ref: "点击 = 1000/3 = 333.33 ⇒ 展示 11,111；转化 0、收入 0、商品成本 0；总成本 = 1000+0+300 = 1300；"
     + "利润 = −1300；ROAS = 0；ROI = −1300/1300 = −100.0%。CPA 走 `conversions>0?budget/conversions:0` ⇒ 0。"
     + "亏损建议里「客单价提升至 budget/(clicks×cvr) = 1000/0 = ∞」是页面在 CVR=0 下的自然产物（非缺陷，"
     + "修复 ∞ 显示后本条须同步更新）。costRate 沿用默认 50%（默认态同值，不参与本条判定）。⚠ 本例不锚"
     + "「0 转化数」—— harness 默认态下各 input 为空串 ⇒ 整条链算出全 0，同样产出「0 转化数」，"
     + "锚它即成逃生项，故只保留 −100.0% 与 ∞ 两条。",
  },
  {
    // ⚠ 页面逻辑缺陷（已留档报老板，未擅改）：costRate=100 ⇒ 毛利率 0 ⇒ 盈亏平衡 ROAS 恒 0
    //   ⇒ roasOk 恒真，亏损（利润 −5000、ROI −35.7%）却显示「✓ 盈利」与「当前盈利」
    slug: "marketing/ad-roi",
    inputs: { budget: "5000", cpm: "50", ctr: "2", cvr: "3", aov: "150", costRate: "100", fixedCost: "0" },
    clicks: ["setBuy('cpm');calc();"],
    expect: ["0.00 盈亏平衡 ROAS", "-35.7%"],
    ref: "CPM：展示 = 5000/50×1000 = 100,000，点击 2000，转化 60，收入 9000，商品成本 = 9000×100% = 9000，"
     + "总成本 = 5000+9000 = 14000，利润 = −5000 ⇒ ROI = −35.7%、ROAS = 1.80。"
     + "毛利率 = 1−100% = 0 ⇒ breakEvenRoas = 1/0 走 else 分支取 0（`grossMargin>0?1/grossMargin:0`）"
     + " ⇒ roasOk = 1.80≥0 恒真 ⇒ 页面输出「✓ 盈利」/**「当前盈利」**，与利润为负矛盾。"
     + "本条用例锚的是页面**当前实际产物**（修复后须同步更新）。",
  },  {
    slug: "marketing/cpc-calculator",
    inputs: { budget: "20000", unitPrice: "4", ctr: "2", cvr: "2.5" },
    clicks: ["setMode('cpc');document.getElementById('budget').value='20000';document.getElementById('unitPrice').value='4';document.getElementById('ctr').value='2';document.getElementById('cvr').value='2.5';calcConvert();"],
    expect: ['250,000', '¥80.00', '¥160.00'],
    ref: 'CPC 模式（unitPrice 即点击单价）：点击 = 20000÷4 = 5000；展示 = 5000÷2% = **250,000**；转化 = 5000×2.5% = 125 ⇒ CPA = 20000÷125 = **¥160.00**、CPM = 20000÷(250000÷1000) = **¥80.00**。三条锚分属「展示反推」「转化率 → CPA」「展示量 → CPM」三个独立系数，默认态（¥50.00 / ¥66.67 / 200,000）全不命中。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { unitPrice: "40", ctr: "5", cvr: "8" },
    clicks: ["setMode('cpm');document.getElementById('unitPrice').value='40';document.getElementById('ctr').value='5';document.getElementById('cvr').value='8';calcConvert();"],
    expect: ['250,000', '¥10.00'],
    ref: 'CPM 模式（unitPrice 改为千次展示单价）：展示 = 10000÷40×1000 = **250,000**；点击 = 250000×5% = 12500；转化 = 12500×8% = 1000 ⇒ CPC = 10000÷12500 = ¥0.80、CPA = 10000÷1000 = **¥10.00**。本条与上一条同预算但走完全不同的反推方向，任一条口径写反都会被另一条抓到。两条教训均来自逃生项：① 首轮锚 CPA `¥50.00` —— harness 兜底无参调用把 `currentMode` 写成非 cpc 值后，另一分支恰好也算出 50；② 点击量 `12,500` —— **inputs 里的赋值在默认态同样生效**（只有模式不同），于是默认态用同一组 40/5 走 cpm 分支也会得到 12,500。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { budget: "15000", unitPrice: "75", ctr: "4", cvr: "5" },
    clicks: ["setMode('cpa');document.getElementById('budget').value='15000';document.getElementById('unitPrice').value='75';document.getElementById('ctr').value='4';document.getElementById('cvr').value='5';calcConvert();"],
    expect: ['100,000', '¥150.00', '¥75.00'],
    ref: 'CPA 模式（unitPrice 即行动单价）：转化 = 15000÷75 = 200；点击 = 200÷5% = 4000；展示 = 4000÷4% = **100,000** ⇒ CPM = 15000÷(100000÷1000) = **¥150.00**、CPC = 15000÷4000 = ¥3.75。三模式的差异只在「哪个量由 unitPrice 直达」，本条 CPA 列恒等于输入单价 ¥75.00。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { totalBudget: "80000" },
    clicks: ["document.getElementById('totalBudget').value='80000';calcBudget();"],
    expect: ['¥34,286', '53,333', '19,048'],
    ref: '预算分配表：总预算 80000，渠道按 ratio 分摊。微信（30%）得 80000×30/70 = 34285.71 ⇒ 千分位化后 **¥34,286**，其点击量 = 34285.71÷1.8 = **19,048**；合计点击 = 5714+19048+28571 = **53,333**。注意 harness 兜底会无参调 `addChannel()` 给渠道清单多加一条 10% 渠道（合计占比 70% 而非 100%），故本条只锚按比例缩放的量，不锚逐渠道转化量；首轮锚的合计 CPA `¥53.16` 也是逃生项——该量与总预算**无关**（转化量与预算同比例缩放），默认态同样命中。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { targetConv: "500", estCpa: "60", estCtr: "2.5", estCvr: "5", estPrice: "299", estMargin: "45" },
    clicks: ["calcEstimate();"],
    expect: ['¥37,275', '124.3%', '400.0K'],
    ref: '预估标签页：预算 = 500×60 = **¥30,000**；收入 = 500×299 = ¥149,500；利润 = 149500×45% − 30000 = 67275 − 30000 = **¥37,275**；点击 = 500÷5% = 10000、展示 = 10000÷2.5% = 400000 ⇒ **400.0K**；ROI = 37275÷30000×100 = 124.25 ⇒ **124.3%**。默认态该页根本不执行 calcEstimate（结果区停留在 HTML 静态占位 ¥39,600 / 49.5%），三条锚全不命中。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { targetConv: "1000", estCpa: "120", estCtr: "2.5", estCvr: "5", estPrice: "299", estMargin: "10" },
    clicks: ["calcEstimate();"],
    expect: ['¥-90,100', '-75.1%', '800.0K'],
    ref: '同式的亏本分支：预算 = 1000×120 = ¥120,000、收入 = 299,000；利润 = 299000×10% − 120000 = 29900 − 120000 = **¥-90,100**（负号与千分位同时出现）；ROI = −90100÷120000×100 = −75.083 ⇒ **−75.1%**；展示 = (1000÷5%)÷2.5% = 800000 ⇒ **800.0K**。与上一条构成同式异参对照：同一批系数，利润由其唯一变量（毛利率 45% vs 10%）决定正负。',
  },

  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "150", freeShipThreshold: "99", shippingFee: "10", avgMargin: "45" },
    expect: ["✅ 已满足包邮条件"],
    ref: '免费门槛：购物车 ¥150 ≥ 阈值 ¥99 ⇒ 已包邮，输出「✅ 已满足包邮条件」。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "50", freeShipThreshold: "99", shippingFee: "12", avgMargin: "40" },
    expect: ["还差 ¥49.00 包邮", "建议直接支付运费¥12更划算"],
    ref: '未包邮差额 = 99−50 = ¥49.00；凑单成本 = 49×(1−40%) = ¥29.40 ≥ 运费¥12 ⇒ 直接付运费更划算。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "80", freeShipThreshold: "99", shippingFee: "8", avgMargin: "50" },
    expect: ["还差 ¥19.00 包邮", "建议直接支付运费¥8更划算"],
    ref: '差额 = 99−80 = ¥19.00；凑单成本 = 19×50% = ¥9.50 ≥ 运费¥8 ⇒ 付运费更划算。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "85", freeShipThreshold: "99", shippingFee: "15", avgMargin: "30" },
    expect: ["还差 ¥14.00 包邮", "建议凑单¥14的商品（商家成本约¥9.80，低于运费¥15）"],
    ref: '差额 = 99−85 = ¥14.00；凑单成本 = 14×70% = ¥9.80 < 运费¥15 ⇒ 建议凑单。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "90", freeShipThreshold: "99", shippingFee: "25", avgMargin: "10" },
    expect: ["还差 ¥9.00 包邮", "建议凑单¥9的商品（商家成本约¥8.10，低于运费¥25）"],
    ref: '差额 = 99−90 = ¥9.00；凑单成本 = 9×90% = ¥8.10 < 运费¥25 ⇒ 建议凑单。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "30", freeShipThreshold: "50", shippingFee: "5", avgMargin: "60" },
    expect: ["还差 ¥20.00 包邮", "建议直接支付运费¥5更划算"],
    ref: '阈值改 ¥50：差额 = 50−30 = ¥20.00；凑单成本 = 20×40% = ¥8.00 ≥ 运费¥5 ⇒ 付运费更划算。',
  }

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
  console.log("==== marketing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();