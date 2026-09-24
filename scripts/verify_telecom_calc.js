#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "telecom/ap-coverage",
  "inputs": {
    "ptx": "30",
    "gt": "3",
    "freq": "2412",
    "prmin": "-82",
    "gr": "2",
    "extraLoss": "10",
    "fadeMargin": "8"
  },
  "expect": [
    "0.88231"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/bandwidth-calculator",
  "inputs": {
    "bandwidth": "100",
    "fileSize": "7.7",
    "efficiency": "85"
  },
  "expect": [
    "7.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/ber-snr",
  "inputs": {
    "ber": "1e-5",
    "ebn0": "14.6"
  },
  "expect": [
    "14.6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/convert-24",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/estimate-9",
  "inputs": {
    "freq": "3600",
    "dist": "1",
    "ptx": "20",
    "gt": "2",
    "gr": "2"
  },
  "expect": [
    "3600.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/path-loss",
  "inputs": {
    "freq": "3600",
    "dist": "1",
    "ptx": "20",
    "gt": "2",
    "gr": "2"
  },
  "expect": [
    "(3600.00)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/quick-calc-time-bandwidth",
  "inputs": {
    "kw": "zzzz"
  },
  "clicks": ["search()"],
  "expect": [
    "未找到匹配项"
  ],
  "ref": "与 quality/table-sampling 同模板：kw 为空时输出 DATA 全量，具体编号在默认态必命中 ⇒ 反向锚"
     + "「未找到匹配项」。原 expect「A01」是默认全量表首行编号，零判别力。",
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {
    "baseIp": "192.168.1.0",
    "oldMask": "36",
    "newMask": "26",
    "subCount": "4"
  },
  "expect": [
    "36"
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
  console.log("==== telecom calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
