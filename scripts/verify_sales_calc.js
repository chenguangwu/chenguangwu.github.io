#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "sales/commission-calc",
  "inputs": {
    "sales": "375000",
    "base": "0",
    "taxThreshold": "5000"
  },
  "expect": [
    "375000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/commission-calculator",
  "inputs": {
    "sales": "150000",
    "fixedRate": "5",
    "baseSalary": "5000",
    "threshold": "20000",
    "baseRate": "8",
    "teamSales": "500000",
    "teamRate": "6",
    "shareRatio": "0.3"
  },
  "expect": [
    "150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/conversion-funnel",
  "inputs": {
    "preset": "ecom"
  },
  "expect": [
    "50.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/cost-price-margin",
  "inputs": {
    "cost": "90",
    "price": "100",
    "margin": "40"
  },
  "expect": [
    "126.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/moving-average",
  "inputs": {
    "window": "6",
    "periods": "3",
    "data": "120\n135\n128\n142\n150\n165\n170"
  },
  "expect": [
    "148"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/price-calculator",
  "inputs": {
    "cost": "150",
    "fixedCost": "0",
    "markup": "40",
    "targetProfit": "20000",
    "volume": "500",
    "compPrice": "180",
    "deviation": "-5",
    "custValue": "300",
    "captureRate": "60"
  },
  "expect": [
    "210.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/sales-forecast",
  "inputs": {
    "paramN": "3",
    "forecastN": "3",
    "histData": "",
    "method": "wma"
  },
  "expect": [
    "102904"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/stacked-discount",
  "inputs": {
    "price": "899"
  },
  "expect": [
    "819.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/target-breakdown",
  "inputs": {
    "total": "1500"
  },
  "expect": [
    "1500"
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
  console.log("==== sales calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
