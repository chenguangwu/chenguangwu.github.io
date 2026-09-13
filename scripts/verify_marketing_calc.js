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
    expect: ["5.00", "10.00", "4.00"],
    ref: "ctr=500/10000×100=5.00；cvr=50/500×100=10.00；cpc=2000/500=4.00；cpm=2000/10000×1000=200.00",
  },
  {
    slug: "marketing/marketing-conversion-rate-calculator",
    inputs: { visitors: "1000", conversions: "50", totalCost: "5000", avgOrder: "200" },
    expect: ["5.00", "100.00", "10000"],
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
    inputs: { adSpend: "10000", adRevenue: "40000" },
    expect: ["4.00", "75.00", "30000"],
    ref: "roas=40000/10000=4.00；profit=30000；profitMargin=30000/40000×100=75.00",
  },
  {
    slug: "marketing/marketing-cac-calculator",
    inputs: { marketingSpend: "8000", salesSpend: "2000", newCustomers: "100", ltv: "500" },
    expect: ["100.00", "80.00", "5.00"],
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
    inputs: { costMarkup: "100", markupRate: "50" },
    expect: ["150.00", "33.33"],
    ref: "price=100×1.5=150.00；profit=50；marginRate=50/150×100=33.33（markup 模式默认）",
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
    expect: ["2.50", "40.00"],
    ref: "marginRatio=0.4；breakEvenRoas=1/0.4=2.50；profitPerUnit=100×0.4=40.00",
  },
  {
    slug: "marketing/calc-1",
    inputs: { spend: "10000", revenue: "30000", conversions: "100", costRate: "40" },
    expect: ["80.00", "3.00", "100.00"],
    ref: "cogs=30000×0.4=12000；profit=30000-10000-12000=8000；roi=8000/10000=80.00%；roas=30000/10000=3.00；cpa=10000/100=100.00",
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
    expect: ["-1.73", "富有弹性"],
    ref: "midQ=110,midP=95；pctQ=20/110×100=18.18；pctP=-10/95×100=-10.53；ed=18.18/-10.53=-1.73（|Ed|>1 富有弹性）",
  },
  {
    slug: "marketing/price-elasticity",
    inputs: { p1: "100", q1: "100", p2: "110", q2: "80" },
    expect: ["-2.33", "富有弹性"],
    ref: "avgQ=90,avgP=105；pctQ=-20/90×100=-22.22；pctP=10/105×100=9.52；ped=-22.22/9.52=-2.33（|Ed|>1 富有弹性）",
  },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const errs = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`  OK ${c.slug}`);
    } else {
      errs.push(c);
      console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      console.log(`     ref: ${c.ref}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 300)}`);
    }
  }
  console.log(`\n==== marketing calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
