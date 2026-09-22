#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "paper/basis-weight",
  "inputs": {
    "gsmInput": "120",
    "reamGsm": "70"
  },
  "expect": [
    "120.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/detector-17",
  "inputs": {
    "defSize": "5.5",
    "defPerSqm": "8",
    "area": "10"
  },
  "expect": [
    "5.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/moisture-calc",
  "inputs": {
    "wetWeight": "150",
    "dryWeight": "92"
  },
  "expect": [
    "38.67%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/pulp-yield",
  "inputs": {
    "rawInput": "1500",
    "pulpInput": "480"
  },
  "expect": [
    "0.3200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/roll-length",
  "inputs": {
    "outerDia": "1500",
    "coreDia": "76",
    "paperThk": "0.1",
    "targetLen": "500",
    "coreDia2": "76",
    "paperThk2": "0.1"
  },
  "expect": [
    "17626094"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/calc-concentration-1",
  "inputs": {
    "wet": "750",
    "dry": "20",
    "vol": "480",
    "target": "3"
  },
  "expect": [
    "4250.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/carbon-5",
  "inputs": {
    "v0": "1000",
    "v1": "20"
  },
  "expect": [
    "12.28%",
    "0.1400",
    "16.67%"
  ],
  "ref": "v0=1000,v1=20 → 成纸灰分=0.7×20/(100+0.7×20)×100=12.28%、填料纤维比 0.7×20/100=0.1400、加入量占比 200/1200=16.67%（默认 800/15 → 9.50%/0.1050/13.04%；swap 84.85%/5.6000/90.91%，均不重合；第 1/2 行 200.00/140.00 为对称量，不作 expect）"
},
{
  "slug": "paper/naipo-dingpo-zhishu",
  "inputs": {
    "v0": "350",
    "v1": "80"
  },
  "expect": [
    "4.375",
    "3.57",
    "45.83%"
  ],
  "ref": "v0=350,v1=80 → 耐破指数=350/80=4.375 kPa·m²/g、换算 350×0.0102=3.57 kgf/cm²、相对 3.0 基准 (4.375-3)/3×100=45.83%（默认 250/60 → 4.167/2.55/38.89%；swap 0.240/0.61/-92.00%，均不重合）"
},
{
  "slug": "paper/strength-1",
  "inputs": {
    "rctFace": "6000",
    "rctLiner": "4000",
    "rctMed": "2500",
    "d": "3.6",
    "eff": "0.5",
    "ectDirect": "",
    "L": "400",
    "W": "300",
    "H": "300",
    "sf": "3",
    "boxWt": "15"
  },
  "expect": [
    "(6000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/strength-10",
  "inputs": {
    "v0": "180",
    "v1": "75"
  },
  "expect": [
    "2400.0",
    "2.4000",
    "140.00%"
  ],
  "ref": "v0=180,v1=75 → 剥离强度=180×1000/75=2400.0 N/m、2.4000 kN/m、相对 1.0 kN/m 富余 (2.4-1)×100=140.00%（默认 100/50 → 2000.0/2.0000/100.00%；swap 500.0/0.5000/-50.00%，均不重合）"
},
{
  "slug": "paper/strength-9",
  "inputs": {
    "v0": "750",
    "v1": "80"
  },
  "expect": [
    "9.375",
    "937.5",
    "17.19%"
  ],
  "ref": "v0=750,v1=80 → 撕裂指数=750/80=9.375 mN·m²/g、每 100 g/m² 归一化 937.5 mN、相对 8.0 基准 (9.375-8)/8×100=17.19%（默认 500/60 → 8.333/833.3/4.17%；swap 0.120/12.0/-98.50%，均不重合）"
},
{
  "slug": "paper/paper-grade",
  "inputs": {},
  "expect": [
    "12.0"
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
  console.log("==== paper calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
