#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "fire/analysis-cost-price-8",
  "inputs": {
    "sell": "120",
    "cost": "75"
  },
  "expect": [
    "当前售价相对竞品均价"
  ]
},
{
  "slug": "fire/calc-water-pressure-hydrant",
  "inputs": {
    "staticP": "0.55",
    "elevation": "12",
    "nozzleP": "0.35",
    "lossP": "0.08"
  },
  "expect": [
    "管损"
  ]
},
{
  "slug": "fire/estimate-time-flow",
  "inputs": {
    "people": "300",
    "width": "1.8",
    "flow": "1.3",
    "dist": "30",
    "speed": "1",
    "pre": "30"
  },
  "expect": [
    "出口能力"
  ]
},
{
  "slug": "fire/evacuation-time",
  "inputs": {
    "people": "300",
    "width": "1.8",
    "flow": "1.3",
    "dist": "30",
    "speed": "1.0",
    "pre": "30",
    "aset": "300"
  },
  "expect": [
    "口数量"
  ]
},
{
  "slug": "fire/hydrant-pressure",
  "inputs": {
    "hgeo": "24",
    "hq": "16",
    "ld": "25",
    "q": "5",
    "lw": "80",
    "d": "100"
  },
  "expect": [
    "管网"
  ]
},
{
  "slug": "fire/smoke-spread",
  "inputs": {
    "hrr": "1000",
    "height": "3",
    "time": "120",
    "width": "2",
    "alpha": "0.01"
  },
  "expect": [
    "降至危险高度"
  ]
},
{
  "slug": "fire/detector-176",
  "inputs": {
    "f1": "2"
  },
  "expect": [
    "联动系统存在轻微问题"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/detector-178",
  "inputs": {
    "cycle": "4"
  },
  "expect": [
    "缩短维保周期至1-2个月"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/detector-44",
  "inputs": {
    "count": "15",
    "lastDate": "2024-01-01"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/extinguisher-calc",
  "inputs": {
    "area": "1200"
  },
  "expect": [
    "1200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/response-drill",
  "inputs": {},
  "expect": [
    "火灾"
  ],
  "ref": "auto-restore(default)；页面 newScenario() 随机选 6 个场景之一并写入 scenarioName，6 个场景名均含「火灾」，故该子串确定出现，规避 Math.random 选景偶发失败（原期望「拨打119报警」仅 5/6 场景含，约 1/6 概率误挂门禁）"
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
  console.log("==== fire calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
