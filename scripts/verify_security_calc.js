#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "security/anti-fraud-cards",
  "inputs": {
    "catFilter": "telecom"
  },
  "expect": [
    "telecom"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/data-erase-simulator",
  "inputs": {
    "blockSize": "24"
  },
  "expect": [
    "24"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/detector-45",
  "inputs": {
    "resistTime": "23",
    "steelThick": "1.2",
    "lockTime": "5",
    "envScore": "8"
  },
  "expect": [
    "23分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/earthquake-escape",
  "inputs": {
    "floorSelect": "mid"
  },
  "expect": [
    "mid"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/emergency-contacts",
  "inputs": {},
  "expect": [
    "400-161-9995"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "security/first-aid-kit",
  "inputs": {},
  "expect": [
    "20片"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "security/flood-level",
  "inputs": {
    "depthSlider": "7"
  },
  "expect": [
    "7cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/smoke-alarm-test",
  "inputs": {
    "alarmLocation": "卧室"
  },
  "expect": [
    "卧室"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/typhoon-scale",
  "inputs": {
    "windInput": "45"
  },
  "expect": [
    "162.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/virtual-safe",
  "inputs": {
    "itemContent": ""
  },
  "expect": [
    "请设置一个主密码来创建新的保险箱"
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
  console.log("==== security calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
