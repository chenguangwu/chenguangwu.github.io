#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pr/analysis-6",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/analysis-assessor",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/analysis-density-1",
  "inputs": {
    "text": "本厂推进智能制造改造，引入自动排程与在线检测。业内普遍认为智能制造的价值在于稳定良率，而不是简单替代人工。实践表明，智能制造需要先把数据采集做扎实。",
    "kw": "智能制造"
  },
  "expect": [
    "4.41",
    "出现 3 次"
  ],
  "ref": "关键词密度：正文中文字符 68 个、英文单词 0 个，总词数 68；关键词「智能制造」出现 3 次，密度=3÷68=4.41%（独立复算）"
},
{
  "slug": "pr/assessor-56",
  "inputs": {
    "a1": "4"
  },
  "expect": [
    "97%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-57",
  "inputs": {
    "a1": "4"
  },
  "expect": [
    "96%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-58",
  "inputs": {
    "k1": "15",
    "k6": "5",
    "k7": "100"
  },
  "expect": [
    "0.33元"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-59",
  "inputs": {
    "p1": "75",
    "p2": "10",
    "p3": "100"
  },
  "expect": [
    "13%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-manager-2",
  "inputs": {
    "r1": "4"
  },
  "expect": [
    "96%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-risk",
  "inputs": {},
  "expect": [
    "按常规预案执行"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pr/media-invite",
  "inputs": {
    "mediaType": "paper"
  },
  "expect": [
    "paper"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/press-conference",
  "inputs": {
    "startTime": "14:00",
    "eventType": "press"
  },
  "expect": [
    "85"
  ],
  "ref": "auto-restore → 收紧：eventType=press 时 7 环节总时长 85 分（默认 product 为 135 分）。原 expect「25」取环节单行时长，回退默认仍可命中（逃生项），改锚定总时长「85」（product 为 135 → 失配）。"
},
{
  "slug": "pr/risk-assessment",
  "inputs": {
    "riskProb": "3",
    "riskImpact": "3"
  },
  "expect": [
    "(12)"
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
  console.log("==== pr calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
