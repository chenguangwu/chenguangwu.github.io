#!/usr/bin/env node
/**
 * 第 30 道门禁：securities 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：beta-calc（收益率序列 + 双文本域）；bond-convexity / bond-duration（多参数循环折现）；
 *       calc-1（沪深费率多分项）；calc-29 / technical-indicator（价格序列）；
 *       position-sizing（tab 切换）；black-scholes（多分支）。
 * 用法: node scripts/verify_securities_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "securities/market-cap",
    inputs: { price: "80", shares: "3000000000" },
    expect: ["2400.00"],
    ref: "总市值=80×30亿=2400.00 亿元（默认 50/20亿 避开）",
  },
  {
    slug: "securities/enterprise-value",
    inputs: { MCap: "1500", Debt: "300", Cash: "200" },
    expect: ["1600.00"],
    ref: "EV=市值+债务−现金=1500+300−200=1600.00（默认 1000/200/100 避开）",
  },
  {
    slug: "securities/price-to-book",
    inputs: { price: "40", bv: "10" },
    expect: ["4.00", "0.250"],
    ref: "P/B=40/10=4.00；账面市值比=10/40=0.250（默认 30/10 结果亦 3.00，改输入确保注入路径）",
  },
  {
    slug: "securities/book-to-market",
    inputs: { BVPS: "40", P: "100" },
    expect: ["0.400"],
    ref: "B/M=每股净资产/股价=40/100=0.400（默认 30/100 避开）",
  },
  {
    slug: "securities/earnings-yield",
    inputs: { EPS: "8", P: "100" },
    expect: ["8.00"],
    ref: "盈利收益率=EPS/股价×100=8/100×100=8.00%（默认 5/100 避开）",
  },
  {
    slug: "securities/dividend-payout",
    inputs: { dps: "3", eps: "8" },
    expect: ["37.50", "62.50"],
    ref: "股利支付率=3/8×100=37.50%；留存收益率=(1−3/8)×100=62.50%（默认 2/5 避开）",
  },
  {
    slug: "securities/current-yield",
    inputs: { c: "60", p: "1200" },
    expect: ["5.00"],
    ref: "当前收益率=年息/现价×100=60/1200×100=5.00%（默认 50/950 避开）",
  },
  {
    slug: "securities/peg-ratio",
    inputs: { PE: "30", g: "12" },
    expect: ["2.50"],
    ref: "PEG=PE/增长率=30/12=2.50（默认 20/10 避开）",
  },
  {
    slug: "securities/option-breakeven-call",
    inputs: { k: "120", prem: "10" },
    expect: ["130.00"],
    ref: "看涨期权盈亏平衡价=行权价+权利金=120+10=130.00（默认 100/8 避开）",
  },
  {
    slug: "securities/option-breakeven-put",
    inputs: { K: "80", P: "5" },
    expect: ["75.00"],
    ref: "看跌期权盈亏平衡价=行权价−权利金=80−5=75.00（默认 50/3 避开）",
  },
  {
    slug: "securities/market-risk-premium",
    inputs: { rm: "0.10", rf: "0.03" },
    expect: ["7.00"],
    ref: "市场风险溢价=(市场收益−无风险利率)×100=(0.10−0.03)×100=7.00%（默认 0.08/0.025 避开）",
  },
  {
    slug: "securities/margin-requirement",
    inputs: { eq: "36000", pos: "120000" },
    expect: ["30.0"],
    ref: "保证金比例=账户权益/持仓市值×100=36000/120000×100=30.0%（默认 25000/100000 结果亦 25.0，改输入确保注入路径）",
  },
  {
    slug: "securities/holding-return-stock",
    inputs: { P0: "200", P1: "230", D: "4" },
    expect: ["17.00"],
    ref: "持有期收益率=(卖出−买入+股息)/买入×100=(230−200+4)/200×100=17.00%（默认 100/110/2 避开）",
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
  console.log("==== securities calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();