#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "wedding/countdown-timeline",
  "inputs": {
    "weddingTime": "10:00_X"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/detector-2",
  "inputs": {
    "c1": "#e8638f_X",
    "c2": "#7c3aed"
  },
  "expect": [
    "e8638f_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/detector-33",
  "inputs": {
    "prof": "12",
    "punctual": "9",
    "creative": "7",
    "comm": "8",
    "contract": "95"
  },
  "expect": [
    "12/10(30%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/material-checklist",
  "clicks": ["CATEGORIES=[{name:'婚宴用品',items:[{name:'喜糖礼盒',qty:30,price:18,status:'done'},{name:'定制喜帖',qty:200,price:3,status:'pending'}]},{name:'现场布置',items:[{name:'主舞台背景',qty:1,price:2800,status:'ordered'}]}];calc()"],
  "expect": [
    "¥3,940 总预算",
    "33% 完成",
    "婚宴用品 ¥1,140",
    "现场布置 ¥2,800"
  ],
  "ref": "顶层数组 CATEGORIES 注入：婚宴用品 30×18 + 200×3 = ¥1,140、现场布置 1×2800 = ¥2,800 ⇒ 总预算 ¥3,940、共 3 项物料、已到货 1 项 ⇒ 进度 1/3 = 33%。默认态 loadDefault 为 ¥50,200 / 23 项 / 30%；「3 总物料数」会被默认态「23 总物料数」作为子串命中 ⇒ 改锚两个分类合计。"
},
{
  "slug": "wedding/seating-chart",
  "inputs": {
    "perTable": "15",
    "mainTable": "8"
  },
  "expect": [
    "15人"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/wedding-budget-planner",
  "inputs": {
    "totalBudget": "150000",
    "spent": "0",
    "cat-'+i+'": "'+amount+'"
  },
  "expect": [
    "150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/wedding-car-route",
  "inputs": {
    "departTime": "07:00_X",
    "carCount": "6"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
  {
    slug: "wedding/wedding-banquet",
    inputs: { guests: "120", type: "round10", backup: "mid" },
    expect: ["14 桌"],
    ref: "主桌 ceil(120/10)=12；备桌 mid=2；合计 14 桌；到场估算 ceil(120×0.9)=108 人。"
       + "原 expect 含「12 桌」「约 108 人」为备桌无关项（回退 backup=none 仍命中，逃生项），且「2 桌」会撞「12 桌」子串；"
       + "收紧为仅「14 桌 合计预订桌数」（backup=none 时为 12 桌 → 失配）。",
  },

  {
    slug: "wedding/wedding-banquet",
    inputs: { guests: "137", type: "square8", backup: "big" },
    expect: ["18 桌 主桌数（方桌 8 人）", "21 桌 合计预订桌数", "约 124 人 按 90% 到场率估算"],
    ref: "type=square8 ⇒ perTable=8；主桌数=ceil(137/8)=18；按 90% 到场=ceil(137×0.9)=ceil(123.3)=124；"
       + "backup=big ⇒ backupN=3；合计=18+3=21。默认态为 120 人/round10/none ⇒ 12 桌、约 108 人、12 桌合计，三条锚全部失配。"
       + "（「20-40 桌」等容纳参考表为与输入无关的常量块，已回避。）",
  },

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

  console.log("==== wedding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
