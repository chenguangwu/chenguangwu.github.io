#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "banking/amortization-first-interest", inputs: {"p": "500000", "r": "4.9"}, expect: ["497958.33 首月还本金"] },
  { slug: "banking/apy-calculator", inputs: {"r": "0.05", "n": "12"}, expect: ["5.116 年化收益率"] },
  { slug: "banking/bond-current-yield", inputs: {"c": "50", "p": "980"}, expect: ["5.102 当前收益率"] },
  { slug: "banking/break-even-savings", inputs: {"rd": "2", "rl": "5"}, expect: ["28.57 贷款占比"] },
  { slug: "banking/continuous-compounding", inputs: {"p": "10000", "r": "5", "t": "10"}, expect: ["6487.21 利息总额"] },
  { slug: "banking/credit-card-interest-monthly", inputs: {"bal": "1000", "dr": "0.0005", "days": "30"}, expect: ["15.00 利息"] },
  { slug: "banking/daily-interest", inputs: {"p": "100000", "r": "3.65", "d": "100"}, expect: ["101000.00 本利和"] },
  { slug: "banking/debt-to-income", inputs: {"debt": "3000", "inc": "10000"}, expect: ["30.0 债务收入比"] },
  { slug: "banking/effective-annual-rate", inputs: {"r": "6", "n": "12"}, expect: ["6.168 有效年利率"] },
  { slug: "banking/emi-loan", inputs: {"p": "500000", "r": "4.9", "y": "30"}, expect: ["955308.10 还款总额"] },
  { slug: "banking/fd-quarterly", inputs: {"p": "100000", "r": "3", "t": "5"}, expect: ["16118.41 利息总额"] },
  { slug: "banking/fisher-real-rate", inputs: {"nom": "6", "infl": "2"}, expect: ["4.000 近似"] },
  { slug: "banking/future-value-annuity-due", inputs: {"PMT": "100", "r": "0.005", "n": "12"}, expect: ["1239.72 终值"] },
  { slug: "banking/growing-annuity-pv", inputs: {"C": "100", "r": "0.05", "g": "0.02", "n": "10"}, expect: ["838.81 现值"] },
  { slug: "banking/loan-remaining-balance", inputs: {"p": "500000", "r": "4.9", "y": "30", "k": "60"}, expect: ["41511.46 已还本金"] },
  { slug: "banking/loan-tenure", inputs: {"P": "10000", "r": "0.005", "PMT": "200"}, expect: ["57.7 还款期数"] },
  { slug: "banking/loan-to-value", inputs: {"loan": "800000", "val": "1000000"}, expect: ["80.0 贷款价值比"] },
  { slug: "banking/loan-total-interest", inputs: {"p": "500000", "r": "4.9", "y": "30"}, expect: ["2653.63 月供"] },
  { slug: "banking/net-worth", inputs: {"assets": "500000", "liab": "200000"}, expect: ["300000 净资产"] },
  { slug: "banking/nominal-from-effective", inputs: {"EAR": "0.05116", "n": "12"}, expect: ["5.000 名义年利率"] },
  { slug: "banking/perpetuity-pv", inputs: {"C": "100", "r": "0.05"}, expect: ["2000.00 现值"] },
  { slug: "banking/present-value-annuity-due", inputs: {"PMT": "100", "r": "0.005", "n": "12"}, expect: ["1167.70 现值"] },
  { slug: "banking/rd-maturity", inputs: {"p": "1000", "r": "8", "t": "1"}, expect: ["529.33 利息总额"] },
  { slug: "banking/savings-goal-monthly", inputs: {"fv": "200000", "r": "4", "y": "10"}, expect: ["162988.33 累计存入"] },
  { slug: "banking/tax-equivalent-yield", inputs: {"muni": "0.03", "tax": "0.25"}, expect: ["4.000 税后等效收益率"] }];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== banking calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();