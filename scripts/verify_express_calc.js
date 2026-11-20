#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  {
    "slug": "express/insurance-fee",
    "inputs": {
      "company": "sf",
      "value": "5000",
      "coverage": "20000"
    },
    "expect": [
      "25.00",
      "4,975.00"
    ],
    "ref": "顺丰0.5% 5000→25元"
  },
  {
    "slug": "express/insurance-fee",
    "inputs": {
      "company": "ems",
      "value": "1000",
      "coverage": "20000"
    },
    "expect": [
      "10.00",
      "990.00"
    ],
    "ref": "EMS 1% 1000→10元"
  },
  {
    "slug": "express/insurance-fee",
    "inputs": {
      "company": "sf",
      "value": "30000",
      "coverage": "20000"
    },
    "expect": [
      "20,000.00",
      "10,000.00"
    ],
    "ref": "超上限：理赔封顶2万、超出1万"
  },
  {
    "slug": "express/insurance-fee",
    "inputs": {
      "company": "sf",
      "value": "0",
      "coverage": "20000"
    },
    "expect": [
      "1.00"
    ],
    "ref": "声明价值0→按最低1元"
  },
  {
    "slug": "express/insurance-fee",
    "inputs": {
      "company": "sf",
      "value": "100",
      "coverage": "0"
    },
    "expect": [
      "请输入有效的单票保价上限"
    ],
    "ref": "上限空/0 提示"
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

  console.log("==== express calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
