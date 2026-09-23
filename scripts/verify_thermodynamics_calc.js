#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "thermodynamics/adiabatic-tv",
  "inputs": {
    "T1": "450",
    "V1": "1",
    "V2": "2",
    "gamma": "1.4"
  },
  "expect": [
    "341.04"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/biot-number",
  "inputs": {
    "h": "75",
    "L": "0.05",
    "k": "400"
  },
  "expect": [
    "0.0094"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/boyles-law",
  "inputs": {
    "P1": "150",
    "V1": "2",
    "P2": "50"
  },
  "expect": [
    "6.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/charles-law",
  "inputs": {
    "V1": "4",
    "T1": "273.15",
    "T2": "373.15"
  },
  "expect": [
    "5.4644"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/compressor-isentropic-work",
  "inputs": {
    "T1": "450",
    "PR": "8",
    "g": "1.4",
    "Rgas": "287"
  },
  "expect": [
    "366794.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/convective-heat-rate",
  "inputs": {
    "h": "15",
    "A": "2",
    "dT": "20"
  },
  "expect": [
    "600.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/cp-cv-ratio",
  "inputs": {
    "cp": "1508",
    "Rgas": "287"
  },
  "expect": [
    "1221.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/diesel-efficiency",
  "inputs": {
    "r": "27",
    "rho": "2",
    "g": "1.4"
  },
  "expect": [
    "68.67"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/entropy-change",
  "inputs": {
    "Q": "6279",
    "T": "373.15"
  },
  "expect": [
    "16.827"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/entropy-generation",
  "inputs": {
    "dsSys": "15",
    "dsSurr": "-9"
  },
  "expect": [
    "6.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/first-law",
  "inputs": {
    "Q": "1500",
    "W": "400"
  },
  "expect": [
    "1100.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/fourier-number",
  "inputs": {
    "alpha": "1e-5",
    "t": "150",
    "L": "0.01"
  },
  "expect": [
    "15.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/gay-lussac-law",
  "inputs": {
    "P1": "150",
    "T1": "300",
    "T2": "400"
  },
  "expect": [
    "200.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/grashof-number",
  "inputs": {
    "g": "14.81",
    "beta": "0.003",
    "dT": "10",
    "L": "0.1",
    "nu": "1.5e-5"
  },
  "expect": [
    "1.975e+6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/heat-conduction",
  "inputs": {
    "k": "600",
    "A": "0.01",
    "dT": "100",
    "L": "0.1"
  },
  "expect": [
    "600000.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/humid-air-enthalpy",
  "inputs": {
    "t": "38",
    "w": "0.01"
  },
  "expect": [
    "63.945"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/ideal-gas-pressure",
  "inputs": {
    "n": "4",
    "T": "273.15",
    "V": "22.414"
  },
  "expect": [
    "405276.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/isothermal-work",
  "inputs": {
    "n": "4",
    "T": "300",
    "V1": "1",
    "V2": "2"
  },
  "expect": [
    "6915.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/latent-heat",
  "inputs": {
    "m": "4",
    "L": "334000"
  },
  "expect": [
    "1336000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/linear-expansion",
  "inputs": {
    "alpha": "1.2e-5",
    "L0": "1500",
    "dT": "50"
  },
  "expect": [
    "1500.900"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/lmtd-heat-exchanger",
  "inputs": {
    "dt1": "90",
    "dt2": "30"
  },
  "expect": [
    "54.61"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/newton-cooling",
  "inputs": {
    "T0": "150",
    "Tinf": "20",
    "k": "0.05",
    "t": "30"
  },
  "expect": [
    "49.01"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/otto-efficiency",
  "inputs": {
    "r": "15",
    "g": "1.4"
  },
  "expect": [
    "66.15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/polytropic-work",
  "inputs": {
    "p1": "150",
    "v1": "1",
    "p2": "50",
    "v2": "2",
    "n": "1.3"
  },
  "expect": [
    "166.67"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/specific-heat-q",
  "inputs": {
    "m": "4",
    "c": "4186",
    "T1": "20",
    "T2": "30"
  },
  "expect": [
    "167440.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/stefan-boltzmann",
  "inputs": {
    "eps": "4",
    "A": "1",
    "T": "300"
  },
  "expect": [
    "1837.08"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/thermal-resistance-series",
  "inputs": {
    "L1": "3.1",
    "k1": "0.04",
    "L2": "0.2",
    "k2": "1.0",
    "A": "1"
  },
  "expect": [
    "77.7000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "thermodynamics/boyles-law",
  "inputs": {
    "P1": "0",
    "V1": "0",
    "P2": "0"
  },
  "expect": [
    "无效值"
  ],
  "ref": "边界守卫：输入 0 → V2=0*0/0=NaN → dataGrid 含 NaN → 守卫渲染告警『⚠ 计算结果含无效值』；注入失败回退默认(P1=150,V1=2,P2=50)→V2=6 有限不命中，可判别"
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
  console.log("==== thermodynamics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
