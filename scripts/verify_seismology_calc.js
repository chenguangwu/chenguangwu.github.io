#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "seismology/analysis-stress",
  "inputs": { "data": "节面A,30,60,-90\n节面B,45,80,10" },
  "expect": [
    "节面数： 2",
    "P 300.0°/75.0°",
    "T 120.0°/15.0°"
  ],
  "ref": "按 Aki&Richards 节面解除算：节面A(30/60/−90) 正断型，P 轴 300.0°/75.0°、B 轴 30.0°/0.0°、T 轴 120.0°/15.0°；节面B(45/80/10) 走滑型（默认 1 个节面 45/60/0，P 4.1°/20.7°，避开）"
},
{
  "slug": "seismology/assessor-30",
  "inputs": {
    "pga": "300",
    "pgv": "20",
    "damageIndex": "0.3"
  },
  "expect": [
    "0.306g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "seismology/assessor-31",
  "inputs": {
    "totalBldg": "150",
    "minorDmg": "30",
    "moderateDmg": "15",
    "severeDmg": "8",
    "partialCol": "3",
    "totalCol": "1",
    "water": "2.5",
    "power": "30",
    "gas": "1.0",
    "road": "15",
    "comm": "20",
    "landslide": "5",
    "rockfall": "10",
    "cracks": "3",
    "liquefaction": "2"
  },
  "expect": [
    "0.097"
  ],
  "ref": "auto-restore"
},
{
  "slug": "seismology/generator-drill",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "seismology/stats-attenuation",
  "inputs": {
    "mags": "3.0,3.5,4.0,4.5,5.0,3.2,4.1,4.8"
  },
  "expect": [
    "0.41",
    "2.13"
  ],
  "ref": "非默认输入+独立复算：G-R b=lg e/(均值4.0125−Mmin3.0+0.05)=0.41、a=lg8+0.41×3.0=2.13（默认序列2.5…4.2 输出 b=0.38/a=1.86，注入失败即不命中）"
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
  console.log("==== seismology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
