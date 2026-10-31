#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tunnel/advance-rate",
  "inputs": {
    "inL": "6",
    "inEta": "0.9",
    "inDrill": "3",
    "inBlast": "1",
    "inVent": "0.5",
    "inMuck": "3",
    "inSupport": "2",
    "inCycles": "3"
  },
  "expect": [
    "10.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/gas-monitor",
  "inputs": {
    "inGas": "3.5"
  },
  "expect": [
    "3.50%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/lining-thickness",
  "inputs": {
    "inB": "15"
  },
  "expect": [ "102 cm" ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/support-design",
  "inputs": {
    "inB": "18",
    "inH": "8"
  },
  "expect": [ "199.8 m" ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/ventilation-calc",
  "inputs": {
    "inA": "90",
    "inV": "2.5",
    "inL": "1000",
    "inN": "800",
    "inQco": "0.02",
    "inDelta": "100",
    "inAco": "60"
  },
  "expect": [
    "810000"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== tunnel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
