#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forex/cross-rate",
  "inputs": {
    "baseUsd": "4.085",
    "quoteUsd": "0.00665",
    "amount": "1000"
  },
  "expect": [
    "614.2857"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forex/leverage-calc",
  "inputs": {
    "lots": "4",
    "baseUsdRate": "1",
    "balance": "10000",
    "stopOut": "50"
  },
  "expect": [
    "400.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forex/lot-size",
  "inputs": { "balance": "50000", "riskPct": "1", "stopPips": "30", "pair": "USDJPY" },
  "expect": ["2.50 建议手数", "$500 风险金额", "盈亏比 = 100 ÷ 30"],
  "ref": "注入非默认（默认 balance=10000 / riskPct=2 / stopPips=50 / pair=EURUSD）：风险金额 = 50000×1% = $500；USD/JPY 的 pip=0.01、报价货币 USD 汇率 150（option 的 data 值）⇒ 每手每点 = 100000×0.01÷150 = $6.6667；每手止损 = 30×6.6667 = $200 ⇒ 手数 = 500÷200 = 2.50；盈亏比 = 止盈 100 ÷ 止损 30 = 3.33。默认态 0.40 手 / $200 / 2.00，三串均不出现。⚠ 该页此前因 `selectedOptions[0].dataset.pip` 未建模而整页初始化失败，harness 补 mkOpt 后可读数。"
},
{
  "slug": "forex/pip-calc",
  "inputs": { "pair": "USDJPY", "lotSize": "1", "pips": "80", "accountCcy": "CNY" },
  "expect": ["¥48.33 每点价值", "波动80点盈亏 = +¥3,866.67"],
  "ref": "注入非默认（默认 EURUSD / 0.01 手 / 50 点 / USD）：合约单位 = 1×100000 = 100,000 USD；USD/JPY 的 1 点 = 0.01 ⇒ 点值 = 100000×0.01 = 1,000 JPY ⇒ ÷150 = $6.67 ⇒ ×7.25（CNY 账户汇率）= ¥48.33；80 点盈亏 = 48.33×80 = +¥3,866.67。默认态 $0.10 / 1,000 合约 / +$5.00，两串均不出现。"
},
{
  "slug": "forex/spread-cost",
  "inputs": { "pair": "GBPUSD", "lots": "3", "days": "2" },
  "expect": ["$60.00 点差成本", "总交易成本 = $60.00"],
  "ref": "注入非默认（默认 EURUSD / lots=1 / days=0）：⚠ 选 pair 会联动改写 ask/bid（GBP/USD 的 data 报价 1.2752/1.275）⇒ 不手工注入 ask/bid（注入也会被覆盖，真机同样）。点差 = 0.00020 ⇒ 2.0 点；每手每点 = 100000×0.0001÷1 = $10 ⇒ 点差成本 = 3×2.0×10 = $60.00；佣金 = 3×7 = $21.00；隔夜 = 3×(−3.5)×2 = −$21.00 ⇒ 总成本 = 60+21−21 = $60.00。默认态点差成本 $20.00 / 总成本 $27.00，两串均不出现。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== forex calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
