#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chemical/calc-pipeline-pressure-drop",
  "inputs": {
    "v0": "300",
    "v1": "150",
    "v2": "2.0",
    "v3": "850",
    "v4": "0.0005",
    "v5": "0.1"
  },
  "expect": [
    "3.29 kPa",
    "1020000",
    "0.0039",
    "0.394 m"
  ]
},
{
  "slug": "chemical/convert-capacity-tank",
  "inputs": {
    "val": "1",
    "rate": "1"
  },
  "expect": [
    "系数"
  ]
},
{
  "slug": "chemical/convert-density-crude",
  "inputs": {
    "val": "1",
    "rate": "1"
  },
  "expect": [
    "系数"
  ]
},
{
  "slug": "chemical/detector-39",
  "inputs": {
    "conc": "0.1000",
    "vol": "25.00",
    "mass": "0.2000",
    "molar": "204.22",
    "ratio": "1",
    "threshold": "99.0",
    "g_mass": "0.5000",
    "g_dry": "0.4850",
    "g_factor": "1.000",
    "g_threshold": "98.0"
  },
  "expect": [
    "纯度"
  ]
},
{
  "slug": "chemical/miaomu-guige-zhiliang-yanshou-biaozhun",
  "inputs": {
    "v0": "200",
    "v1": "180",
    "v2": "165"
  },
  "expect": [
    "90.0%",
    "82.5%",
    "86.3"
  ]
},
{
  "slug": "chemical/mixture-ratio",
  "inputs": {
    "ca": "60",
    "ma": "200",
    "cb": "30",
    "mb": "100",
    "c1": "95",
    "v1": "500",
    "c2": "70",
    "value": "25",
    "al1": "95",
    "al2": "40"
  },
  "expect": [
    "混合浓度 50.00%",
    "混合比 (A:B) 200 : 100"
  ],
  "ref": "去默认化（原 expect「混合比」是静态标签词，默认态同样命中 = 逃生项）：A 60%×200 + B 30%×100，总质量 300 ⇒ 混合浓度 (12000+3000)/300 = 50.00%；混合比 200 : 100。默认 80/100/20/300 得 35.00% 与 100 : 300（v1 只影响「稀释」页签，不影响本结果，故须改 ca/ma/cb/mb）"
},
{
  "slug": "chemical/reaction-yield",
  "inputs": {
    "theo": "10",
    "actual": "7.5",
    "na": "0.5",
    "nb": "0.3",
    "ratio": "1",
    "m": "10",
    "m1": "100",
    "m2": "80",
    "coef": "1",
    "small": "5",
    "times": "10",
    "yield": "80",
    "big": "75"
  },
  "expect": [
    "损失量"
  ]
},
{
  "slug": "chemical/solution-concentration",
  "inputs": {
    "mass": "58.5",
    "molar": "58.5",
    "vol": "1",
    "solute": "10",
    "total": "100",
    "mg": "5",
    "kg": "1",
    "c1": "2",
    "v1": "100",
    "c2": "0.5"
  },
  "expect": [
    "质量浓度"
  ]
},
{
  "slug": "chemical/analysis-cost-7",
  "inputs": {
    "data": "11,22,33,44,55",
    "budget": "100",
    "topn": "2"
  },
  "expect": [
    "55.00",
    "60.00%",
    "超支 65.00"
  ],
  "ref": "非默认输入+独立复算：合计165、最大分项55、前2大项累计占比60.00%、对比预算100超支65（默认数据 800,200,1200,300,500,150 均不含 55.00/60.00%/超支65.00，注入失败即不命中）"
},
{
  "slug": "chemical/checker-15",
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chemical/molar-mass",
  "inputs": {
    "formula": "H2O",
    "mass": "27"
  },
  "expect": [
    "9.025e+23"
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
  console.log("==== chemical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
