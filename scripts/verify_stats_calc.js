#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "stats/data-distribution",
  "inputs": {
    "bins": "6",
    "data": "5,8,12,15,18,21,24,27,30,33,36,39,42,45,48,51"
  },
  "clicks": ["calc()"],
  "expect": [
    "16 样本数 n",
    "454.00 总和 Σ",
    "28.375 均值 x̄"
  ],
  "ref": "n=16；Σ=5+8+12+…+51=454；均值=454/16=28.375；中位数=(27+30)/2=28.500；极差=51−5=46；"
     + "σ²=196.609、σ=14.022、CV=49.42%。bins=6 ⇒ 组距=(51−5)/6=7.67。"
     + "原 expect「0.1」是 alpha 输入回显（且默认态同样含该串）⇒ 零判别力，已换非默认数据与统计锚点。",
},
{
  "slug": "stats/regression-analysis",
  "inputs": {
    "pred-x": "17",
    "x-data": "1,2,3,4,5,6,7,8,9,10",
    "y-data": "2.1,3.9,6.2,7.8,10.2,11.9,14.1,15.8,18.3,19.7"
  },
  "expect": [
    "33.8467"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stats/sample-size",
  "inputs": {
    "e": "5",
    "p": "0.5",
    "n": "0",
    "conf": "0.95"
  },
  "expect": [
    "3.842"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stats/statistical-tests",
  "inputs": {
    "one-mu": "30",
    "one-data": "12,15,18,22,25,28,30,32,35,38"
  },
  "expect": [
    "-1.6413"
  ],
  "ref": "默认样本 12…38：n=10、均值 25.5、s=8.6700、SE=2.7417；μ₀=30 ⇒ t=(25.5−30)/2.7417=−1.6413（页面 toFixed(4)）。改动 μ₀ 后由 input 事件即时重算（此前必须点按钮，直接改输入结果区不变）。μ₀ 默认 20 ⇒ t=2.0061，不命中；原用例 one-data 带 '_X' 且 expect 为输入回显（恒绿）已替换。"
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

  console.log("==== stats calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
