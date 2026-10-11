#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "woodwork/analysis-cost-price",
  "inputs": {
    "data": "3200,3300,3100,3400,3500",
    "ref": "3000",
    "warn": "10"
  },
  "expect": [
    "3300.00",
    "132.29",
    "4.01%",
    "3500.00",
    "+16.67%"
  ],
  "ref": "非默认输入+独立复算：均价3300、样本标准差132.29、CV4.01%、最新价3500、相对基准3000偏离+16.67%"
},
{
  "slug": "woodwork/angle-1",
  "inputs": {
    "v0": "45",
    "v1": "18",
    "v4": "45"
  },
  "expect": [
    "18×tan(45.0°)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/calculator-calc-15",
  "inputs": {
    "v0": "27",
    "v1": "60",
    "v4": "20",
    "v5": "6"
  },
  "expect": [
    "10.13"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/convert-30",
  "inputs": { "mci": "30", "mcf": "12", "k": "0.26", "orig": "100" },
  "expect": ["线干缩率 = 4.68 %", "收缩后尺寸 ≈ 95.32 cm"],
  "ref": "初始 30%、终了 12%、收缩系数 0.26 → 线干缩率=(30−12)×0.26=4.68%，原 100cm 收缩后 ≈95.32cm（默认 30/8/0.26 → 5.72%/94.28，注入态不重合）"
},
{
  "slug": "woodwork/convert-30",
  "inputs": { "mci": "45", "mcf": "8", "k": "0.15", "orig": "100" },
  "expect": ["线干缩率 = 5.55 %", "收缩后尺寸 ≈ 94.45 cm"],
  "ref": "初始 45%、终了 8%、径向系数 0.15 → (45−8)×0.15=5.55%，原 100cm→94.45cm"
},
{
  "slug": "woodwork/desk-dimensions",
  "inputs": {
    "height": "255",
    "mon": "24"
  },
  "expect": [
    "255"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/detector-32",
  "inputs": {
    "hcho": "3.8",
    "loadForce": "1200",
    "cycles": "10000",
    "stability": "0.15"
  },
  "expect": [
    "3.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/detector-37",
  "inputs": {
    "moisture": "21",
    "knotSize": "25",
    "width": "150",
    "knotCount": "3",
    "bend": "3"
  },
  "expect": [
    "21%"
  ],
  "ref": "auto-restore"
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

  console.log("==== woodwork calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
