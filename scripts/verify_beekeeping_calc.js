#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "40"
    },
    "expect": [
      "350.0 kg"
    ],
    "ref": "10群×40亩 混合花源基准35kg"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "20"
    },
    "expect": [
      "175.0 kg"
    ],
    "ref": "花源不足按面积折减(20/40=0.5)"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "200"
    },
    "expect": [
      "385.0 kg"
    ],
    "ref": "花源充足(>3倍需求)加成1.1"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "40"
    },
    "clicks": [
      "selectSource('rapeseed');calc();"
    ],
    "expect": [
      "450.0 kg"
    ],
    "ref": "油菜花源基准45kg/群"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "",
      "area": "40"
    },
    "expect": [
      "请输入有效参数"
    ],
    "ref": "蜂箱空值提示"
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

  console.log("==== beekeeping calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
