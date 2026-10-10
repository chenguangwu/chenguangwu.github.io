#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "antiques/bronze-identification",
  "inputs": {
    "era": "xia"
  },
  "expect": [
    "xia"
  ],
  "ref": "auto-restore"
},
{
  "slug": "antiques/calligraphy-style",
  "inputs": {
    "era": "shang"
  },
  "expect": [
    "shang"
  ],
  "ref": "auto-restore"
},
{
  "slug": "antiques/furniture-style",
  "inputs": {
    "era": "song"
  },
  "expect": [
    "song"
  ],
  "ref": "auto-restore"
},
{
  "slug": "antiques/porcelain-date",
  "inputs": {
    "dynasty": "tang"
  },
  "expect": [
    "tang"
  ],
  "ref": "auto-restore"
},
{
  "slug": "antiques/seal-identification",
  "inputs": {
    "era": "qin"
  },
  "expect": [
    "qin"
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

  console.log("==== antiques calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
