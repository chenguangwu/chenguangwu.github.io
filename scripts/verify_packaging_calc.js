#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "packaging/calc-66",
  "inputs": {
    "v0": "600",
    "v1": "300",
    "v2": "250",
    "v4": "2.5",
    "v5": "3",
    "v6": "12"
  },
  "expect": [
    "1.800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "packaging/shousuomo-shousuolv-refeng-canshu",
  "inputs": {
    "v0": "400",
    "v1": "240"
  },
  "expect": [
    "40.00%",
    "60.00%",
    "424.00"
  ],
  "ref": "v0=400,v1=240 → 热收缩率=(400-240)/400×100=40.00%、收缩后占比 240/400=60.00%、建议下料膜宽 400×1.06=424.00 mm（默认 300/150 → 50.00%/50.00%/318.00；swap -100.00%/200.00%/159.00，均不重合；收缩量为可正负差值，不作 expect）"
},
{
  "slug": "packaging/strength-11",
  "inputs": {
    "v0": "7",
    "v1": "3"
  },
  "expect": [
    "2251",
    "2.251",
    "321.5"
  ],
  "ref": "v0=7,v1=3 → BCT=5.87×7×√(3×1000)=2251 N（McKee 近似，箱周长 1000 mm）、2.251 kN、系数 5.87×√3000=321.5（默认 6/2.5 → 1761/1.761/293.5；swap 1137/1.137/454.7，均不重合）"
},
{
  "slug": "packaging/strength-12",
  "inputs": {
    "v0": "30",
    "v1": "48"
  },
  "expect": [
    "15.625",
    "625.0",
    "56.25%"
  ],
  "ref": "v0=30,v1=48 → 剥离强度=30×25/48=15.625 N/25mm、30×1000/48=625.0 N/m、相对 10 N/25mm 基准 (15.625-10)/10×100=56.25%（默认 24/45 → 13.333/533.3/33.33%；swap 46.875/1875.0/368.75%，均不重合）"
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
  console.log("==== packaging calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
