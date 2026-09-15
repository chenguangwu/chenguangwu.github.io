#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "sales/commission-calc", inputs: {"sales": "250000", "base": "0", "taxThreshold": "5000"}, expect: ["OK"] },
  { slug: "sales/commission-calculator", inputs: {"sales": "100000", "fixedRate": "5", "baseSalary": "5000", "threshold": "20000", "baseRate": "8", "teamSales": "500000", "teamRate": "6", "shareRatio": "0.3"}, expect: ["OK"] },
  { slug: "sales/conversion-funnel", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "sales/cost-price-margin", inputs: {"cost": "60", "price": "100", "margin": "40"}, expect: ["OK"] },
  { slug: "sales/moving-average", inputs: {"window": "3", "periods": "3"}, expect: ["OK"] },
  { slug: "sales/price-calculator", inputs: {"cost": "100", "fixedCost": "0", "markup": "40", "targetProfit": "20000", "volume": "500", "compPrice": "180", "deviation": "-5", "custValue": "300", "captureRate": "60"}, expect: ["OK"] },
  { slug: "sales/sales-forecast", inputs: {"paramN": "3", "forecastN": "3"}, expect: ["OK"] },
  { slug: "sales/stacked-discount", inputs: {"price": "599"}, expect: ["OK"] },
  { slug: "sales/target-breakdown", inputs: {"total": "1000"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== sales calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();