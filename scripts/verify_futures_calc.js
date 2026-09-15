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
  "expect": [
    "5700"
  ],
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
  "slug": "futures/option-payoff",
  "inputs": {
    "strike": "150",
    "premium": "5"
  },
  "expect": [
    "145.00"
  ],
  "ref": "auto-restore"
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
  console.log("==== futures calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
