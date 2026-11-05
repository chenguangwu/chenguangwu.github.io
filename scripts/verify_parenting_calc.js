#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "parenting/diaper-usage",
  "inputs": {
    "month": "9",
    "price": "1.2",
    "days": "30"
  },
  "expect": [
    "198.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/feeding-amount-baby",
  "inputs": {
    "month": "7",
    "weight": "6.8",
    "feeds": "6"
  },
  "expect": [
    "1010"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/feeding-schedule",
  "inputs": {
    "month": "6",
    "weight": "6",
    "startTime": "07:00"
  },
  "expect": [
    "132"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/formula-mixing",
  "inputs": {
    "target": "270",
    "ratio": "30"
  },
  "expect": [ "9 勺奶粉" ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/growth-chart",
  "inputs": {
    "month": "18",
    "height": "76",
    "weight": "9.5"
  },
  "expect": [
    "74.9-89.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/pumping-plan",
  "inputs": {
    "hours": "14",
    "month": "6",
    "single": "120"
  },
  "expect": [
    "480"
  ],
  "ref": "auto-restore"
},
{
  "slug": "parenting/diaper-usage",
  "inputs": {
    "month": "",
    "price": "1.2",
    "days": "30"
  },
  "expect": [
    "请填写：宝宝月龄"
  ],
  "ref": "空态守卫（A 类）：月龄留空时旧实现 Math.floor(num(''))=0 落入 month<=1 分支 → 按新生儿输出每日 11 片与 NB 码；现前置判空并点名缺失字段。默认 month=6 ⇒ 不命中。"
},
{
  "slug": "parenting/diaper-usage",
  "inputs": {
    "month": "0",
    "price": "1.2",
    "days": "30"
  },
  "expect": [
    "11.0 片 每日用量",
    "NB 码 建议尺码"
  ],
  "ref": "显式 0 合法：0 月龄即出生当月，按新生儿每日 11 片、30 天 330 片、NB 码照常计算；证明判空只看空字符串、不把月龄 0 当缺失。默认 month=6 得 7.0 片/M 码 ⇒ 不命中。"
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

  console.log("==== parenting calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
