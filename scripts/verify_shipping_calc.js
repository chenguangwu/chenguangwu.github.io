#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "shipping/calc-76",
  "inputs": {
    "v0": "270",
    "v1": "28",
    "v2": "9.5",
    "v3": "9.7",
    "v4": "9.9",
    "v5": "0.72",
    "v6": "1.025",
    "v7": "",
    "v8": "12000"
  },
  "expect": [
    "153.36"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/convert-speed-1",
  "inputs": {
    "val": "1",
    "from": "1.852"
  },
  "expect": [
    "1.852"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": {
    "v": "15",
    "t": "8"
  },
  "expect": [
    "航程 = 120.00 海里 (≈ 222.24 km)"
  ],
  "ref": "去默认化：航程 = v×t = 15×8 = 120.00 海里，km = 120×1.852 = 222.24。默认态 v=10/t=5 ⇒ 50.00 海里/92.60 km 不命中。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": {
    "v": "20",
    "t": "3"
  },
  "expect": [
    "航程 = 60.00 海里 (≈ 111.12 km)"
  ],
  "ref": "去默认化：航程 = 20×3 = 60.00 海里，km = 60×1.852 = 111.12。默认态不命中。"
},
{
  "slug": "shipping/estimate-length",
  "inputs": {
    "v0": "23",
    "v1": "18",
    "v2": "1.5",
    "v3": "5000",
    "v5": "4"
  },
  "expect": [
    "121.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/tide",
  "inputs": {
    "hTimeOff": "45",
    "hRatio": "1.1",
    "lTimeOff": "20",
    "lRatio": "0.9",
    "rt'+i+'": "'+d.time+'",
    "rh'+i+'": "'+d.height+'"
  },
  "expect": [
    "45"
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

  console.log("==== shipping calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
