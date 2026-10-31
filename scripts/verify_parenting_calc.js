#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "parenting/diaper-usage",
  "inputs": {
    "month": "9",
    "price": "1.2",
    "days": "30"
  },
  "expect": [
    "198.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/feeding-amount-baby",
  "inputs": {
    "month": "7",
    "weight": "6.8",
    "feeds": "6"
  },
  "expect": [
    "1010"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/feeding-schedule",
  "inputs": {
    "month": "6",
    "weight": "6",
    "startTime": "07:00"
  },
  "expect": [
    "132"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/formula-mixing",
  "inputs": {
    "target": "270",
    "ratio": "30"
  },
  "expect": [ "所需奶粉勺数 270" ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/growth-chart",
  "inputs": {
    "month": "18",
    "height": "76",
    "weight": "9.5"
  },
  "expect": [
    "74.9-89.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/pumping-plan",
  "inputs": {
    "hours": "14",
    "month": "6",
    "single": "120"
  },
  "expect": [
    "480"
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

  console.log("==== parenting calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
