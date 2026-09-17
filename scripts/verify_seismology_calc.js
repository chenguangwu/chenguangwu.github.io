#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "seismology/analysis-stress",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
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
  console.log("==== seismology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
