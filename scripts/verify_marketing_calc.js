#!/usr/bin/env node
/**
 * 第 25 道门禁：marketing 分类计算正确性验证（13 个确定性数值工具）
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
  console.log("==== marketing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();