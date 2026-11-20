#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": "250"
    },
    "expect": [
      "39.5",
      "25.0"
    ],
    "ref": "250mm→EU39.5/CN25.0"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": "300",
      "gender": "w"
    },
    "expect": [
      "16.5",
      "14"
    ],
    "ref": "300mm 女码 US16.5/UK14"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": "100"
    },
    "expect": [
      "请输入200-320mm之间的脚长"
    ],
    "ref": "越界提示"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": ""
    },
    "expect": [
      "请输入200-320mm之间的脚长"
    ],
    "ref": "空值提示"
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

  console.log("==== daily-goods calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
