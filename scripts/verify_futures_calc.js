#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "futures/futures-pricing",
  "inputs": {
    "spot": "7500",
    "rate": "4",
    "time": "0.25",
    "yield": "1",
    "storage": "0.5",
    "actualFuture": "5075"
  },
  "expect": [
    "565.91"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/hedge-ratio",
  "inputs": {
    "sigmaS": "6",
    "sigmaF": "3.5",
    "rho": "0.85",
    "spotValue": "1000000",
    "futurePrice": "3800",
    "futureMult": "300"
  },
  "expect": [
    "1.4571"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/margin-calc",
  "inputs": {
    "price": "5700",
    "multiplier": "300",
    "marginRate": "12",
    "capital": "200000",
    "lots": "0",
    "fee": "10"
  },
  "expect": [ "205,200 每手保证金" ],
  "ref": "auto-restore"
},
{
  "slug": "futures/option-greeks",
  "inputs": {
    "spot": "150",
    "strike": "100",
    "rate": "3",
    "vol": "20",
    "time": "0.5",
    "div": "0"
  },
  "expect": [
    "51.4960"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/option-greeks",
  "inputs": {
    "spot": "100",
    "strike": "100",
    "rate": "3",
    "vol": "20",
    "time": "0.5",
    "div": "0",
    "marketPrice": "6.371"
  },
  "expect": [
    "隐含波动率 IV: 20.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/option-payoff",
  "inputs": {
    "strike": "150",
    "premium": "5"
  },
  "expect": [
    "145.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/futures-pricing",
  "inputs": { "spot": "5000", "rate": "", "time": "0.25", "yield": "1", "storage": "0.5" },
  "expect": ["请填写现货价格、无风险利率、到期时间、便利收益率和存储成本率"],
  "ref": "第1063批：清空无风险利率不得按 0 继续给出理论价，必须提示并清空结果。"
},
{
  "slug": "futures/futures-pricing",
  "inputs": { "spot": "5000", "rate": "0", "time": "0.25", "yield": "1", "storage": "0.5" },
  "expect": ["4,993.75"],
  "ref": "第1063批：合法零利率仍应正常计算；连续复利 F=5000×e^((0+0.5%-1%)×0.25)=4993.75，与空值错误路径区分。"
},
{
  "slug": "futures/hedge-ratio",
  "inputs": { "sigmaS": "6", "sigmaF": "3.5", "rho": "", "spotValue": "1000000", "futurePrice": "3800", "futureMult": "300" },
  "expect": ["请填写现货标准差、期货标准差、相关系数"],
  "ref": "第1063批：清空相关系数不得按 0 生成零对冲结果，必须提示并清空结果。"
},
{
  "slug": "futures/margin-calc",
  "inputs": { "price": "", "multiplier": "300", "marginRate": "12", "capital": "200000", "lots": "0", "fee": "10" },
  "expect": ["请填写价格、合约乘数、保证金比例和资金"],
  "ref": "第1063批：清空价格不得按 0 生成零保证金结果，必须提示并清空结果。"
},
{
  "slug": "futures/option-greeks",
  "inputs": { "spot": "100", "strike": "100", "rate": "3", "vol": "20", "time": "0.5", "div": "" },
  "expect": ["请填写标的价格、行权价、无风险利率、波动率、到期时间和股息率"],
  "ref": "第1063批：清空股息率不得按 0 继续定价，必须提示并清空 Greeks。"
},
{
  "slug": "futures/option-payoff",
  "inputs": { "strike": "150", "premium": "" },
  "expect": ["请输入有效的行权价和权利金；数值不能为空"],
  "ref": "第1063批：清空权利金不得按零成本出盈亏，必须提示并清空结果。"
},
{
  "slug": "futures/option-payoff",
  "inputs": { "strike": "150", "premium": "0" },
  "expect": ["150.00"],
  "ref": "第1063批：权利金合法零仍应计算，盈亏平衡点=150；与空值错误路径区分。"
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
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== futures calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
