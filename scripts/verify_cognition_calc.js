#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cognition/cognitive-assessment",
  "inputs": {
    "scaLen": "quick"
  },
  "expect": [
    "quick"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cognition/corsi-block-test",
  "inputs": {
    "cbMode": "bwd"
  },
  "expect": [
    "bwd"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cognition/digit-span-test",
  "inputs": {
    "dsSpeed": "1000"
  },
  "expect": [
    "1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cognition/human-benchmark",
  "inputs": {
    "tArea": ""
  },
  "expect": [
    "9×9"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：8 个子测验全部由点击 / 倒计时 / 随机序列驱动，"
     + "成绩存 localStorage 历史；无表单输入路径可注入，注入 tArea 不触发任何渲染（2026-09-25 实测）。"
},
{
  "slug": "cognition/nback-training",
  "inputs": {
    "nbDur": "1350",
    "nbIsi": "500"
  },
  "expect": [
    "1350"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cognition/schulte-table",
  "inputs": {
    "scMode": "letter"
  },
  "expect": [
    "letter"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cognition/stroop-test",
  "inputs": {
    "stTimeout": "3750"
  },
  "expect": [
    "3750"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cognition/time-perception",
  "inputs": {
    "bSel": "90"
  },
  "expect": [
    "90"
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
  console.log("==== cognition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
