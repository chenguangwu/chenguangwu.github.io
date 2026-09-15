#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "fengshui/birthday-analysis",
  "inputs": {
    "birthDate": "1990-01-01",
    "birthHour": "1"
  },
  "expect": [
    "(0)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fengshui/fengshui-calculator",
  "inputs": {
    "angleSlider": "0",
    "angleInput": "0",
    "houseDir": "45"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fengshui/fengshui-guide",
  "inputs": {},
  "expect": [
    "是研究环境与人类居住关系的学问"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "fengshui/good-day-selector",
  "inputs": {},
  "expect": [
    "婚嫁"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "fengshui/zodiac-lookup",
  "inputs": {
    "birthYear": "2985"
  },
  "expect": [
    "2985"
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
  console.log("==== fengshui calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
