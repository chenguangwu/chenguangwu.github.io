#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "quality/convert-qualified-defect",
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
  "slug": "quality/ppm-calculator",
  "inputs": {
    "defect": "15",
    "total": "8000",
    "pct": "0.15",
    "rate": "0.0015",
    "ppm": "1500",
    "dpmo": "1500"
  },
  "expect": [
    "0.001875"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/process-capability",
  "inputs": {
    "usl": "13.5",
    "lsl": "9.5",
    "mean": "10.0",
    "sigma": "0.1",
    "usl2": "10.5",
    "lsl2": "9.5",
    "dataInput": "10.1, 9.9, 10.0, 10.2, 9.8, 10.0, 10.05, 9.95, 10.1, 9.9"
  },
  "expect": [
    "100.0000%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/six-sigma",
  "inputs": {
    "dpmo": "6210",
    "yield": "99.379",
    "st": "7"
  },
  "expect": [
    "3.4008"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/calc-cpk",
  "inputs": {
    "usl_m": "15.5",
    "lsl_m": "9.5",
    "mean_m": "10.0",
    "sd_m": "0.1",
    "usl_d": "10.5",
    "lsl_d": "9.5",
    "rawData": "10.1\n9.9\n10.0\n10.2\n9.8\n10.0\n10.1\n9.9\n10.0\n10.1\n9.9\n10.0"
  },
  "expect": [
    "15.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/estimate-six-sigma",
  "inputs": {
    "dpmo": "9315",
    "defects": "62",
    "units": "10000",
    "opps": "1"
  },
  "expect": [
    "9315"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/table-sampling",
  "inputs": {
    "kw": "zzzz"
  },
  "clicks": ["search()"],
  "expect": [
    "未找到匹配项"
  ],
  "ref": "search() 在 kw 为空时输出 DATA 全量 ⇒ 任何具体编号（A01 等）在默认态都命中 ⇒ 只能反向锚"
     + "「未找到匹配项」。注入不存在的关键词 zzzz ⇒ results 为空 ⇒ 输出该提示；默认态 DATA 非空、永不出现。"
     + "原 expect「A01」即默认全量表的首行编号，典型逃生项。",
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
  console.log("==== quality calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
