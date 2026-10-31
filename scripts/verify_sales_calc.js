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
  "expect": [ "22,500 元" ],
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
  "expect": [ "7,500.00 计算：销售额" ],
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
  "expect": ["36.00 利润额（元）"],
  "ref": "独立复算：mode 默认 price（成本加成口径）：售价=90×1.4=126.00，利润额=36.00；售价口径利润率=36/126=28.571%→28.6%，加价率=36/90=40.0%。"
     + "Z2 修复前「利润率」行误输出加成率 40.0%（与加价率同值），全页无 28.6% ⇒ 强判别、零逃生。"
     + "对照表值（25%/42.9%/66.7%/100%）与默认态均不含 28.6%。",
},
{
  "slug": "sales/cost-price-margin",
  "inputs": {
    "mode": "cost",
    "cost": "100",
    "price": "125",
    "margin": "20"
  },
  "expect": [
    "16.7%"
  ],
  "ref": "独立复算：mode=cost：成本=125÷1.2=104.17，利润额=20.83；售价口径利润率=20.83/125=16.667%→16.7%，加价率=20.0%。"
     + "Z2 修复前该分支「利润率」行输出 20.0%（加价率同值），全页无 16.7% ⇒ 强判别。",
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
  "expect": [ "1,500 万元" ],
  "ref": "auto-restore"
},

{
    "slug": "sales/commission-calculator",
    "inputs": {
      "sales": "250000",
      "fixedRate": "8"
    },
    "expect": [
      "应得提成 ¥20,000.00"
    ],
    "ref": "提成 = 250000 × 8% = ¥20,000.00。页面输出 '应得提成 ¥20,000.00'。默认态其他输入不产生 ¥20,000.00。"
  },
  {
    "slug": "sales/price-calculator",
    "inputs": {
      "cost": "100",
      "fixedCost": "0",
      "markup": "30",
      "targetProfit": "0",
      "volume": "1",
      "compPrice": "0",
      "deviation": "0",
      "custValue": "0",
      "captureRate": "0"
    },
    "expect": [
      "建议售价 ¥130.00"
    ],
    "ref": "售价 = 100 × (1 + 30%) = ¥130.00。页面输出 '建议售价 ¥130.00'。默认态其他输入不产生 ¥130.00。"
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

  console.log("==== sales calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
