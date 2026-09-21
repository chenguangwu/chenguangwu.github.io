#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "media/assessor-25",
  "inputs": {
    "sent": "10000",
    "opened": "2500",
    "finished": "1200",
    "interact": "350",
    "readTime": "45",
    "words": "1500"
  },
  "expect": [
    "复制到后续内容"
  ]
},
{
  "slug": "media/tester-14",
  "inputs": {
    "aShow": "5000",
    "aClick": "250",
    "bShow": "5000",
    "bClick": "380"
  },
  "expect": [
    "建议采用方案"
  ]
},
{
  "slug": "media/tester-18",
  "inputs": {
    "aShow": "3000",
    "aClick": "120",
    "bShow": "3000",
    "bClick": "210"
  },
  "expect": [
    "继续迭代测试"
  ]
},
{
  "slug": "media/analysis-26",
  "inputs": {
    "data": "物流太慢，包装破损，非常失望\n质量很好，客服耐心，强烈推荐\n一般般，没什么特别感觉"
  },
  "expect": [
    "情感倾向： 整体中性",
    "正面 1 / 负面 1 / 中性 1"
  ],
  "ref": "重做为舆情情感词频：3 条 → 负面1（失望）/正面1（推荐）/中性1（一般般），倾向整体中性（默认 正面2/负面1/中性0 → 偏正面，区分）。非默认输入 + 独立复算。"
},
{
  "slug": "media/analysis-funnel",
  "inputs": {
    "data": "2000,1000,400,120"
  },
  "expect": [
    "6.00%"
  ],
  "ref": "整体转化率 = 末环节/首环节 = 120/2000 = 6.00%（独立手算）"
},
{
  "slug": "media/tester-13",
  "inputs": {
    "title": "震惊！这个方法让你轻松月入过万",
    "platform": "toutiao"
  },
  "expect": [
    "适合toutiao"
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
  console.log("==== media calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
