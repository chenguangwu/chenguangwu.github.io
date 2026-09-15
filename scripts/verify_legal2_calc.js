#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "legal2/compensation-n1",
  "inputs": {
    "avgSalary": "15000",
    "capSalary": "30000"
  },
  "expect": [
    "15000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "legal2/contract-dates",
  "inputs": {
    "noticeDays": "45"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "legal2/ip-protection",
  "inputs": {
    "ipType": "utility"
  },
  "expect": [
    "2031-09-15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "legal2/keyword-extract",
  "inputs": {
    "docInput": ""
  },
  "expect": [
    "被告李四于本判决生效之日起十日内支付原告张三货款50万元及违约金5万元"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "legal2/statute-deadline",
  "inputs": {
    "customYears": "3",
    "limitType": "1"
  },
  "expect": [
    "2027-03-15"
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
  console.log("==== legal2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
