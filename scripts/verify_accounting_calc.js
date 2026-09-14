#!/usr/bin/env node
/**
 * 第 35 道门禁：accounting 分类计算正确性验证（35 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经复核「不等于」默认值输出，杜绝假通过。
 * calc-1 为「含税/不含税」双向开关，需以 checks:["gross"] 声明 mode 单选选中项。
 * 用法: node scripts/verify_accounting_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "accounting/current-ratio", inputs: { ca: "4500000", cl: "1500000" }, expect: ["3.00"], ref: "流动比率=流动资产/流动负债=4500000/1500000=3.00（负债占比=33.3%；默认 3000000/1500000=2.00 避开）" },
  { slug: "accounting/quick-ratio", inputs: { ca: "3600000", inv: "600000", cl: "1500000" }, expect: ["2.00"], ref: "速动比率=(CA−存货)/CL=(3600000−600000)/1500000=2.00（默认 2200000/1500000=1.47 避开）" },
  { slug: "accounting/debt-to-asset", inputs: { tl: "2000000", ta: "8000000" }, expect: ["25.00"], ref: "资产负债率=负债/资产=2000000/8000000=25.00%（权益比率 75.00%；默认 3000000/8000000=37.50 避开）" },
  { slug: "accounting/gross-margin", inputs: { rev: "2000000", cost: "1300000" }, expect: ["35.00"], ref: "毛利率=(营收−成本)/营收=(2000000−1300000)/2000000=35.00%（毛利额 700000；默认 1000000/600000 亦为 40.00%，故避开 40%）" },
  { slug: "accounting/gross-profit", inputs: { rev: "1500", cogs: "900" }, expect: ["600.00"], ref: "毛利=营收−营业成本=1500−900=600.00 万元（默认 1000−600=400.00 避开）" },
  { slug: "accounting/net-profit-margin", inputs: { np: "240000", rev: "1200000" }, expect: ["20.00"], ref: "净利率=净利/营收=240000/1200000=20.00%（年化 240.00%；默认 150000/1000000 亦为 15.00%，故避开 15%）" },
  { slug: "accounting/roe-calc", inputs: { np: "300000", eq: "2000000" }, expect: ["15.00"], ref: "ROE=净利/净资产=300000/2000000=15.00%（默认 200000/2000000=10.00 避开）" },
  { slug: "accounting/roa-calc", inputs: { np: "350000", ta: "5000000" }, expect: ["7.00"], ref: "ROA=净利/总资产=350000/5000000=7.00%（默认 200000/5000000=4.00 避开）" },
  { slug: "accounting/roe-dupont", inputs: { nm: "10", at: "1.2", em: "2.5" }, expect: ["30.00"], ref: "杜邦 ROE=净利率×周转率×权益乘数=(10/100)×1.2×2.5×100=30.00%（默认 12×1.5×2.0=36.00% 避开）" },
  { slug: "accounting/ebit", inputs: { rev: "1200", cogs: "700", opex: "200" }, expect: ["300.00"], ref: "EBIT=营收−成本−费用=1200−700−200=300.00 万元（默认 1000−600−200=200.00 避开）" },
  { slug: "accounting/ebitda", inputs: { EBIT: "300", DA: "80" }, expect: ["380.00"], ref: "EBITDA=EBIT+折旧摊销=300+80=380.00 万元（默认 200+50=250.00 避开）" },
  { slug: "accounting/interest-coverage", inputs: { EBIT: "300", int: "50" }, expect: ["6.00"], ref: "利息保障倍数=EBIT/利息费用=300/50=6.00（默认 200/40=5.00 避开）" },
  { slug: "accounting/inventory-turnover", inputs: { cogs: "6000000", inv: "1000000" }, expect: ["6.00"], ref: "存货周转率=营业成本/存货=6000000/1000000=6.00 次/年（周转天数=365/6=60.8 天；默认 4000000/800000 亦为 5.00，故避开 5）" },
  { slug: "accounting/inventory-days", inputs: { inv: "200", cogs: "600" }, expect: ["121.7"], ref: "DIO=存货/营业成本×365=200/600×365=121.7 天（默认 150/600×365=91.3 天 避开）" },
  { slug: "accounting/days-sales-outstanding", inputs: { AR: "200", rev: "1000" }, expect: ["73.0"], ref: "DSO=应收/营收×365=200/1000×365=73.0 天（默认 100/1000×365=36.5 天 避开）" },
  { slug: "accounting/days-payable-outstanding", inputs: { AP: "120", cogs: "600" }, expect: ["73.0"], ref: "DPO=应付/营业成本×365=120/600×365=73.0 天（默认 80/600×365=48.7 天 避开）" },
  { slug: "accounting/cash-conversion-cycle", inputs: { DSO: "50", DIO: "100", DPO: "60" }, expect: ["90.00"], ref: "CCC=DSO+DIO−DPO=50+100−60=90.00 天（默认 36.5+91.25−48.67=79.08 天 避开）" },
  { slug: "accounting/working-capital", inputs: { CA: "800", CL: "300" }, expect: ["500.00"], ref: "营运资金=流动资产−流动负债=800−300=500.00 万元（默认 500−300=200.00 避开）" },
  { slug: "accounting/asset-turnover", inputs: { rev: "1500", assets: "500" }, expect: ["3.00"], ref: "总资产周转率=营收/平均总资产=1500/500=3.00（默认 1000/500=2.00 避开）" },
  { slug: "accounting/contribution-margin", inputs: { p: "120", vc: "70", q: "10000" }, expect: ["41.67"], ref: "边际贡献=(单价−单位变动)×销量=(120−70)×10000=500000 元；贡献率=500000/(120×10000)=41.67%（默认 100−60→40.00% 避开）" },
  { slug: "accounting/break-even-units", inputs: { fc: "300000", p: "120", vc: "70" }, expect: ["6000.0"], ref: "平衡产量=固定成本/(单价−单位变动)=300000/(120−70)=6000.0 件（平衡销售额 720000 元、单位边际贡献 50.00；默认 200000/40=5000.0 避开）" },
  { slug: "accounting/debt-service-coverage", inputs: { OCF: "200", ds: "50" }, expect: ["4.00"], ref: "DSCR=经营现金流/债务偿付=200/50=4.00（默认 150/60=2.50 避开）" },
  { slug: "accounting/free-cash-flow", inputs: { OCF: "200", capex: "120" }, expect: ["80.00"], ref: "FCF=OCF−资本支出=200−120=80.00 万元（默认 150−80=70.00 避开）" },
  { slug: "accounting/operating-cash-flow", inputs: { NI: "150", DA: "60", dWC: "30" }, expect: ["180.00"], ref: "OCF=净利+折旧摊销−营运资本变动=150+60−30=180.00 万元（默认 120+50−20=150.00 避开）" },
  { slug: "accounting/depreciation-straight", inputs: { c: "200000", s: "20000", n: "8" }, expect: ["22500.00"], ref: "直线法年折旧=(原值−残值)/年限=(200000−20000)/8=22500.00 元（折旧率 11.25%、首年末账面 177500.00；默认 100000/10000/10→9000.00 避开）" },
  { slug: "accounting/depreciation-declining", inputs: { c: "200000", s: "20000", n: "5", yr: "2" }, expect: ["48000.00"], ref: "双倍余额递减率=2/5=0.4；第1年 200000×0.4=80000，第2年 120000×0.4=48000.00 元（期末账面 72000.00、累计 128000.00；默认 yr=3 避开）" },
  { slug: "accounting/depreciation-syd", inputs: { c: "210000", s: "10000", n: "6", yr: "2" }, expect: ["47619.05"], ref: "SYD=n(n+1)/2=21；第2年折旧=(6−2+1)/21×(210000−10000)=5/21×200000=47619.05 元（占原值 22.68%；默认 yr=1 避开）" },
  { slug: "accounting/amortization-intangible", inputs: { c: "720000", s: "0", n: "6" }, expect: ["120000.00"], ref: "直线摊销年额=(成本−残值)/年限=720000/6=120000.00 元（月摊销 10000.00；默认 600000/10→60000.00 避开）" },
  { slug: "accounting/calc-1", inputs: { amount: "21800", rate: "9" }, checks: ["gross"], expect: ["20,000.00"], ref: "含税价反算（mode=gross、税率 9%）：不含税=21800/(1+0.09)=20000.00、税额=1800.00（默认 net 模式 amount=10000 税率 13%→10,000.00 避开）" },
  { slug: "accounting/calc-2", inputs: { revenue: "800000", cost: "300000", loss: "0", rate: "15" }, expect: ["75,000.00"], ref: "利润总额=800000−300000=500000；应纳所得额 500000；按 15% 预缴=75000.00 元（利润率 62.50%；默认 revenue=500000 税率 25%→50,000.00 避开）" },
  { slug: "accounting/split-bill", inputs: { total: "600", people: "5", tip: "15" }, expect: ["138.00"], ref: "小费=600×15%=90.00；含小费总额=690.00；每人=690/5=138.00（默认 480/4/10→132.00 避开）" },
  { slug: "accounting/assessor-risk-11", inputs: { x1: "0.5", x2: "0.3", x3: "0.2", x4: "1.0", x5: "0.8" }, expect: ["3.0800"], ref: "Altman Z=1.2X1+1.4X2+3.3X3+0.6X4+1.0X5=0.6+0.42+0.66+0.60+0.80=3.0800（≥2.99 安全区；默认 x=0.35/0.20/0.12/1.5/1.2→3.1960 避开）" },
  { slug: "accounting/analysis-46", inputs: { data: "5,10,15,20" }, expect: ["12.50"], ref: "财务数据描述统计：n=4、总和 50.00、均值=中位数 12.50、极差 15.00、方差 31.25、标准差 5.59（默认 10..80 八个数→均值 45.00 避开；避开子串陷阱：默认方差 525.00 含 \"25.00\"）" },
  { slug: "accounting/analysis-cost-5", inputs: { data: "5,10,15,20" }, expect: ["12.50"], ref: "成本数据描述统计：n=4、总和 50.00、均值=中位数 12.50、极差 15.00、方差 31.25（默认八个数→45.00 避开；避开子串陷阱 525.00 含 \"25.00\"）" },
  { slug: "accounting/report-2", inputs: { data: "5,10,15,20" }, expect: ["12.50"], ref: "账务数据描述统计：n=4、总和 50.00、均值=中位数 12.50、极差 15.00、方差 31.25（默认八个数→45.00 避开；避开子串陷阱 525.00 含 \"25.00\"）" },
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
  console.log(`\n==== accounting calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
