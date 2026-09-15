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
