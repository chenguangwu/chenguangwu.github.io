#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "service/complaint-analysis",
  "inputs": {
    "keywords": "物流:配送,快递,发货,慢,延迟,到货;质量:质量,坏了,破损,缺陷,次品;服务:态度,客服,不理, rude,敷衍;价格:贵,涨价,价格,收费,乱收费;售后:退款,退货,售后,维修,保修_X",
    "complaintText": ""
  },
  "expect": [
    "保修_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "service/csat-score",
  "inputs": {
    "s5": "45",
    "s4": "30",
    "s3": "12",
    "s2": "8",
    "s1": "5"
  },
  "expect": [
    "81.5%"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "service/response-time",
  "inputs": {
    "slaTarget": "45"
  },
  "expect": [
    "100.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "service/script-template",
  "inputs": {},
  "expect": [
    "实在不好意思让您久等了"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "service/ticket-priority",
  "inputs": {},
  "expect": [
    "5/5"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== service calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
