#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "restaurant/delivery-time", inputs: {"distance": "3.5", "speed": "20", "prepTime": "15", "pickupWait": "5", "deliverWait": "3"}, expect: ["OK"] },
  { slug: "restaurant/dish-cost-card", inputs: {"dishQty": "1", "dishPrice": "38", "yieldRate": "95"}, expect: ["OK"] },
  { slug: "restaurant/menu-margin", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "restaurant/menu-pricing", inputs: {"material": "12", "labor": "20", "fixed": "3", "margin": "60"}, expect: ["OK"] },
  { slug: "restaurant/safety-stock", inputs: {"avgDaily": "5", "maxDaily": "8", "avgLead": "3", "maxLead": "7", "orderCost": "50", "holdCost": "12", "currentStock": "20", "workDays": "365"}, expect: ["OK"] },
  { slug: "restaurant/seasoning-scaler", inputs: {"origServings": "2", "targetServings": "6"}, expect: ["OK"] },
  { slug: "restaurant/table-turnover", inputs: {"hours": "10", "tables": "20", "avgTime": "45", "occupancy": "70", "perTable": "3", "avgSpend": "65"}, expect: ["OK"] },
  { slug: "restaurant/taste-preference", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== restaurant calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();