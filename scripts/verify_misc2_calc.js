#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "misc2/car-residual",
  "inputs": {
    "price": "150000",
    "years": "3",
    "life": "10",
    "salvage": "5"
  },
  "expect": [
    "估算残值"
  ]
},
{
  "slug": "misc2/cigarette-tar",
  "inputs": {
    "tar": "10",
    "nic": "0.8",
    "cigs": "20"
  },
  "expect": [
    "中焦油"
  ]
},
{
  "slug": "misc2/screen-size",
  "inputs": {
    "width": "1080",
    "height": "2400",
    "diagonal": "6.7"
  },
  "expect": [
    "细腻"
  ]
},
{
  "slug": "misc2/tax-refund",
  "inputs": {
    "amount": "50000",
    "rate": "0.048"
  },
  "expect": [
    "日元可退税"
  ]
},
{
  "slug": "misc2/coin-grade",
  "inputs": {
    "grade": "au"
  },
  "expect": [
    "仅在币面最高点"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/instrument-tuning",
  "inputs": {
    "baseFreq": "660"
  },
  "expect": [
    "1047.685"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/insurance-fee",
  "inputs": {
    "value": "7500"
  },
  "expect": [
    "500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/luggage-size",
  "inputs": {
    "size": "20"
  },
  "expect": [
    "国际标准随身尺寸约55×40×20cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/shoe-size",
  "inputs": {
    "footLen": "383"
  },
  "expect": [
    "请输入200-320mm之间的脚长"
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
  console.log("==== misc2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
