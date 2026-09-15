#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "restaurant/delivery-time",
  "inputs": {
    "distance": "6.5",
    "speed": "20",
    "prepTime": "15",
    "pickupWait": "5",
    "deliverWait": "3"
  },
  "expect": [
    "6.5km"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/dish-cost-card",
  "inputs": {
    "dishName": "宫保鸡丁",
    "dishQty": "4",
    "dishPrice": "38",
    "yieldRate": "95"
  },
  "expect": [
    "37.11"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/menu-margin",
  "inputs": {},
  "expect": [
    "166.00"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "restaurant/menu-pricing",
  "inputs": {
    "material": "18",
    "labor": "20",
    "fixed": "3",
    "margin": "60"
  },
  "expect": [
    "24.60"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/safety-stock",
  "inputs": {
    "ingName": "鸡腿肉",
    "avgDaily": "8",
    "maxDaily": "8",
    "avgLead": "3",
    "maxLead": "7",
    "orderCost": "50",
    "holdCost": "12",
    "currentStock": "20",
    "workDays": "365"
  },
  "expect": [
    "每次订156.0kg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/seasoning-scaler",
  "inputs": {
    "origServings": "5",
    "targetServings": "6"
  },
  "expect": [
    "×1.20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/table-turnover",
  "inputs": {
    "hours": "15",
    "tables": "20",
    "avgTime": "45",
    "occupancy": "70",
    "perTable": "3",
    "avgSpend": "65"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/taste-preference",
  "inputs": {},
  "expect": [
    "点击上方按钮开始记录顾客口味偏好"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== restaurant calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
