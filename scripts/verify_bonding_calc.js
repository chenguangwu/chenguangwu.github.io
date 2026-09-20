#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "bonding/assessor-cycle-lifespan",
  "inputs": {
    "sigmaB": "600",
    "deltaSigma": "200",
    "sigmaM": "100",
    "kt": "2.0",
    "designN": "100"
  },
  "expect": [
    "建议结合实验验证"
  ]
},
{
  "slug": "bonding/detector-26",
  "inputs": {
    "designT": "0.2",
    "tolerance": "20"
  },
  "expect": [
    "建议返修补胶后复检"
  ]
},
{
  "slug": "bonding/detector-27",
  "inputs": {
    "echo": "-6",
    "attenuation": "3",
    "area": "100",
    "signals": "2"
  },
  "expect": [
    "可疑信号面积比"
  ]
},
{
  "slug": "bonding/analysis-cost-4",
  "inputs": {
    "data": "环氧AB胶,4.0,5,0.6,96\n热熔胶,1.8,1.5,0.6,92\n结构胶带,6.0,2,0.6,99"
  },
  "expect": [
    "最优方案： 热熔胶",
    "节省： 59.75%",
    "单件成本 2.93"
  ],
  "ref": "单件成本=(材料+工时×费率)÷良品率：环氧AB胶(4.0+5×0.6)/0.96=7.29、热熔胶(1.8+1.5×0.6)/0.92=2.93、结构胶带(6.0+2×0.6)/0.99=7.27；最优=热熔胶，较基准节省=(7.29-2.93)/7.29=59.75%，有效工时5.21→1.63（提升68.70%）（独立复算；默认 环氧胶3.5/4/0.5/98、瞬干胶2.0/2/0.5/95 → 最优瞬干胶3.16，注入失败即不命中）"
},
{
  "slug": "bonding/analysis-resolution",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
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
  console.log("==== bonding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
