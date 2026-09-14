#!/usr/bin/env node
/**
 * 第 45 道门禁：tax 分类计算正确性验证（29 个确定性数值工具，全覆盖）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值（resetForm 预设），且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * tax 目录 29 页全部为纯数值计算（calcTool + num()），无外部状态依赖，故全覆盖。
 * 用法: node scripts/verify_tax_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "tax/ad-valorem-duty",
    inputs: { p: "2500", r: "0.06" },
    expect: ["150.00"],
    ref: "T=计税价格×税率=2500×0.06=150.00（默认 1000/0.1→100.00，避开）" },

  { slug: "tax/average-tax-rate",
    inputs: { T: "45000", Y: "120000" },
    expect: ["37.50"],
    ref: "ATR=T/Y=45000/120000=37.50%（默认 30000/100000→30.00%，避开）" },

  { slug: "tax/break-even-taxable",
    inputs: { target: "800000", deduct: "10000", r: "20" },
    expect: ["1012500.00", "202500.00"],
    ref: "应税所得=(800000+10000)/(1−0.2)=1012500.00；税额=1012500×0.2=202500.00（默认 750000/0/25→1000000.00，避开）" },

  { slug: "tax/capital-gains-effective",
    inputs: { g: "250000", r: "0.15" },
    expect: ["37500.00"],
    ref: "T=收益×优惠税率=250000×0.15=37500.00（默认 100000/0.1→10000.00，避开）" },

  { slug: "tax/capital-gains-tax",
    inputs: { sell: "200000", cost: "140000", r: "25" },
    expect: ["60000.00", "15000.00", "185000.00"],
    ref: "收益=200000−140000=60000.00；税=60000×0.25=15000.00；税后=200000−15000=185000.00（默认 150000/100000/20→50000/10000/140000，避开）" },

  { slug: "tax/corporate-income-tax",
    inputs: { profit: "4000000", r: "15" },
    expect: ["600000.00"],
    ref: "税额=利润×税率=4000000×0.15=600000.00（默认 1000000/25→250000.00，避开）" },

  { slug: "tax/customs-duty",
    inputs: { value: "30000", r: "8" },
    expect: ["2400.00", "32400.00"],
    ref: "关税=30000×0.08=2400.00；含税成本=30000×1.08=32400.00（默认 50000/10→5000.00，避开）" },

  { slug: "tax/effective-tax-rate",
    inputs: { tax: "360000", pretax: "900000" },
    expect: ["40.00", "540000.00"],
    ref: "实际税率=360000/900000=40.00%；税后=900000−360000=540000.00（默认 250000/1000000→25.00%，避开）" },

  { slug: "tax/excise-tax",
    inputs: { p: "25", q: "200", r: "0.15" },
    expect: ["750.00"],
    ref: "T=出厂价×数量×税率=25×200×0.15=750.00（默认 10/100/0.2→200.00，避开）" },

  { slug: "tax/foreign-tax-credit",
    inputs: { ft: "1800", lim: "2500" },
    expect: ["1800.00"],
    ref: "抵扣额=min(1800,2500)=1800.00（默认 2000/1500→1500.00，避开）" },

  { slug: "tax/gift-tax",
    inputs: { a: "1500000", e: "500000", r: "0.15" },
    expect: ["150000.00"],
    ref: "T=max(1500000−500000,0)×0.15=1000000×0.15=150000.00（默认 1000000/200000/0.2→160000.00，避开）" },

  { slug: "tax/gst-calculator",
    inputs: { amt: "440", rate: "10" },
    expect: ["400.00", "40.00"],
    ref: "含税 440、税率 10%（默认 mode=incl）→ 税前价=440/1.1=400.00；税额=440−400=40.00（默认 110/10→100.00，避开）" },

  { slug: "tax/interest-income-tax",
    inputs: { interest: "8000", r: "25" },
    expect: ["2000.00", "6000.00"],
    ref: "税=8000×0.25=2000.00；税后=8000×0.75=6000.00（默认 5000/20→1000.00，避开）" },

  { slug: "tax/marginal-tax-rate",
    inputs: { Y1: "80000", T1: "12000", Y2: "140000", T2: "33000" },
    expect: ["35.00"],
    ref: "MTR=(33000−12000)/(140000−80000)=21000/60000=35.00%（默认 20000/100000/35000/150000→30.00%，避开）" },

  { slug: "tax/payroll-tax",
    inputs: { w: "20000", er: "0.15", ee: "0.05" },
    expect: ["4000.00"],
    ref: "T=工资×(雇主率+雇员率)=20000×(0.15+0.05)=4000.00（默认 10000/0.2/0.08→2800.00，避开）" },

  { slug: "tax/progressive-income-tax",
    inputs: { income: "50000", l1: "10000", r1: "10", l2: "30000", r2: "20", r3: "30" },
    expect: ["11000.00", "22.00"],
    ref: "税=10000×0.1+min(40000,20000)×0.2+(50000−30000)×0.3=1000+4000+6000=11000.00；实际税率=11000/50000=22.00%（默认 30000→5000/16.67%，避开）" },

  { slug: "tax/property-tax",
    inputs: { base: "1500000", r: "0.6" },
    expect: ["9000.00"],
    ref: "税额=1500000×0.006=9000.00（默认 800000/1.2→9600.00，避开）" },

  { slug: "tax/reverse-charge",
    inputs: { a: "8000", r: "0.05" },
    expect: ["400.00"],
    ref: "T=金额×征收率=8000×0.05=400.00（默认 5000/0.03→150.00，避开）" },

  { slug: "tax/sales-tax-addon",
    inputs: { price: "250", r: "8" },
    expect: ["20.00", "270.00"],
    ref: "税=250×0.08=20.00；含税=250×1.08=270.00（默认 100/5→5.00，避开）" },

  { slug: "tax/social-security-tax",
    inputs: { b: "20000", r: "0.11" },
    expect: ["2200.00"],
    ref: "T=缴费基数×费率=20000×0.11=2200.00（默认 10000/0.18→1800.00，避开）" },

  { slug: "tax/specific-duty",
    inputs: { q: "250", u: "8" },
    expect: ["2000.00"],
    ref: "T=数量×单位税额=250×8=2000.00（默认 100/5→500.00，避开）" },

  { slug: "tax/stamp-duty",
    inputs: { amount: "2500000", r: "0.03" },
    expect: ["750.00"],
    ref: "税额=2500000×0.0003=750.00（默认 1000000/0.05→500.00，避开）" },

  { slug: "tax/tax-credit",
    inputs: { t: "8000", c: "2500" },
    expect: ["5500.00"],
    ref: "T'=max(8000−2500,0)=5500.00（默认 5000/1000→4000.00，避开）" },

  { slug: "tax/tax-on-discount",
    inputs: { price: "500", disc: "15", r: "13" },
    expect: ["425.00", "55.25"],
    ref: "净价=500×(1−0.15)=425.00；税=425×0.13=55.25（默认 200/20/13→160.00，避开）" },

  { slug: "tax/tax-to-gdp",
    inputs: { tax: "25", gdp: "120" },
    expect: ["20.83"],
    ref: "宏观税负=25/120×100=20.83%（默认 18/100→18.00%，避开）" },

  { slug: "tax/vat-from-exclusive",
    inputs: { ex: "250", r: "6" },
    expect: ["15.00", "265.00"],
    ref: "税=250×0.06=15.00；含税=250+15=265.00（默认 100/13→13.00，避开）" },

  { slug: "tax/vat-inclusive-to-exclusive",
    inputs: { inc: "159", r: "6" },
    expect: ["150.00", "9.00"],
    ref: "不含税=159/1.06=150.00；税=159−150=9.00（默认 113/13→100.00，避开）" },

  { slug: "tax/vat-output",
    inputs: { s: "25000", r: "0.09" },
    expect: ["2250.00"],
    ref: "T=销售额×税率=25000×0.09=2250.00（默认 10000/0.13→1300.00，避开）" },

  { slug: "tax/withholding-tax",
    inputs: { payment: "80000", r: "12" },
    expect: ["9600.00", "70400.00"],
    ref: "税=80000×0.12=9600.00；净额=80000×0.88=70400.00（默认 100000/10→10000.00，避开）" },
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
      console.log(`  OK ${c.slug} (${r.via})`);
    } else {
      errs.push(c);
      console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 300)}`);
    }
  }
  console.log(`\n==== tax calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
