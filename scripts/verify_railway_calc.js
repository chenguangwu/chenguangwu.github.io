#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "railway/diaoche-zuoye-xiaolv-youhua",
  "inputs": {
    "v0": "240",
    "v1": "36"
  },
  "expect": [
    "180.00",
    "16.67%"
  ],
  "ref": "v0=240,v1=36 → 单钩耗时 240/36=6.67 min/钩、每小时 36/240×60=9.00 钩/h、日产 9×20=180.00 钩、相对 8 min/钩 偏差 (8-6.67)/8=16.67%（默认 300/30 → 10.00/6.00/120.00/-25.00%，交换 30/300 → 0.10/600.00/12000.00/98.75%，均不重合；单钩耗时「6.67」被「16.67%」包含，故仅锚 180.00 与 16.67%）"
},
{
  "slug": "railway/power-5",
  "inputs": {
    "v0": "300",
    "v1": "80"
  },
  "expect": [
    "6666.67",
    "22.22",
    "3.750",
    "13.5000"
  ],
  "ref": "v0=300,v1=80 → 牵引功率 300×80÷3.6=6666.67 kW、每 kN 牵引力 80/3.6=22.22 kW/kN、单位速度牵引力 300/80=3.750 kN/(km/h)、每 km/h 当量 300×3.6/80=13.5000 kN（默认 200/60 → 3333.33/16.67/3.333/12.0000；交换 80/300 → 6666.67/83.33/0.267/0.9600，与 use 首项重合故不锚 6666.67 之外的可交换量，柴油机标定功率在交换态同样重合、不作断言）"
},
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== railway calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
