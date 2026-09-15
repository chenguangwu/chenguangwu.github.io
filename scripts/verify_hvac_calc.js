#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hvac/cooling-tower",
  "inputs": {
    "flow": "600",
    "twIn": "37",
    "twOut": "32",
    "twb": "27",
    "cycles": "3",
    "driftRate": "0.001"
  },
  "expect": [
    "当前"
  ]
},
{
  "slug": "hvac/duct-calculator",
  "inputs": {
    "Q": "3600",
    "v": "5",
    "rho": "1.2",
    "rectA": "500",
    "rectB": "400",
    "diaD": "500",
    "L": "20",
    "xi": "1.5"
  },
  "expect": [
    "总阻力"
  ]
},
{
  "slug": "hvac/pump-calculator",
  "inputs": {
    "q": "50",
    "L": "120",
    "d": "100",
    "lambda": "0.025",
    "kexi": "12",
    "dz": "10",
    "eta": "0.70",
    "margin": "10"
  },
  "expect": [
    "计算过程"
  ]
},
{
  "slug": "hvac/supply-air",
  "inputs": {
    "coolLoad": "2500",
    "deltaT": "8",
    "roomVol": "120"
  },
  "expect": [
    "送风口数量"
  ]
},
{
  "slug": "hvac/air-filter",
  "inputs": {
    "airflow": "2003",
    "filtW": "592",
    "filtH": "592",
    "filtArea": ""
  },
  "expect": [
    "2003"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/chiller-efficiency",
  "inputs": {
    "capacityKw": "503",
    "capacityRt": "142.17",
    "powerKw": "90",
    "tIn": "12",
    "tOut": "7",
    "cop100": "5.6",
    "cop75": "6.3",
    "cop50": "6.8",
    "cop25": "6.0"
  },
  "expect": [
    "143.02"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/dehumidifier",
  "inputs": {
    "volume": "123",
    "temp": "26",
    "ach": "0.5",
    "rh1": "80",
    "rh2": "55"
  },
  "expect": [
    "61.5×1.168×5.39/1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/fan-selector",
  "inputs": {
    "Q": "10003",
    "dP": "800",
    "eta": "75",
    "etaMotor": "90",
    "n": "1450",
    "K": "1.15"
  },
  "expect": [
    "2222.89"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hvac/fresh-air-load",
  "inputs": {
    "people": "23",
    "stdAir": "30",
    "indoorT": "26",
    "indoorRH": "55",
    "outdoorT": "34",
    "outdoorRH": "65"
  },
  "expect": [
    "690×1.2×1.01×8.00/3600"
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
  console.log("==== hvac calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
