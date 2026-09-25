#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gastroenterology/bilirubin-ratio",
  "inputs": {
    "tbil": "128",
    "dbil": "55"
  },
  "expect": [
    "直接胆红素比值35-60%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/calc-1",
  "inputs": {
    "biliUnit": "mgdl"
  },
  "expect": [
    "mgdl"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/capsule-endoscopy",
  "inputs": {
    "ingest": "08:00_X",
    "duodenum": "08:25",
    "cecum": "11:30",
    "excrete": "16:00"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/cdai",
  "inputs": {
    "stool": "21",
    "pain": "10",
    "wellbeing": "7",
    "complications": "1",
    "loperamide": "0",
    "mass": "0",
    "hct": "35",
    "weight": "-5"
  },
  "expect": [
    "198"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/child-pugh",
  "inputs": {
    "bilirubin": "53",
    "albumin": "30",
    "pt": "4",
    "inr": "1.7"
  },
  "expect": [
    "80%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/colonoscopy-polyp",
  "inputs": {
    "size": "12"
  },
  "expect": [
    "12"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/detector-7",
  "inputs": {
    "prior": "7"
  },
  "expect": [
    "既往治疗7次失败"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/ercp-success",
  "inputs": {
    "stoneSize": "18",
    "cbd": "12"
  },
  "expect": [
    "80-90%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/esophageal-varices",
  "inputs": {
    "size": "2"
  },
  "expect": [
    "中度(D2)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastric-emptying",
  "inputs": {
    "r2": "98",
    "r4": "30",
    "r0": "100",
    "halfTime": "90"
  },
  "expect": [
    "排空率2.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastrin-level",
  "inputs": {
    "gastrin": "225"
  },
  "expect": [
    "225"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastroscopy-atlas",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "未找到匹配的条目"
  ],
  "ref": "关键词过滤型：inputs 写 search=zzzqx ⇒ oninput=filterAtlas() ⇒ renderAtlas() 得空集 ⇒ 「未找到匹配的条目」。默认态（search 空）渲染全量条目、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "gastroenterology/glasgow-pancreatitis",
  "inputs": {
    "age": "83",
    "wbc": "15",
    "glucose": "10",
    "ldh": "350",
    "ast": "200",
    "calcium": "2.0",
    "albumin": "32",
    "urea": "8",
    "pao2": "65"
  },
  "expect": [
    "83岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hepatic-encephalopathy",
  "inputs": {
    "consciousness": "1"
  },
  "expect": [
    "限制蛋白摄入至0.8-1.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": {
    "dob": "12.5"
  },
  "expect": [
    "12.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hp-resistance",
  "inputs": {
    "clarithro": "resistant"
  },
  "expect": [
    "resistant"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "inputs": {
    "bmi": "27.5",
    "weightLoss": "8",
    "albumin": "32",
    "age": "45"
  },
  "expect": [
    "27.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/intestinal-metaplasia",
  "inputs": {
    "antrumIM": "1"
  },
  "expect": [
    "每3年随访胃镜"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/mayo-score",
  "inputs": {
    "stool": "1"
  },
  "expect": [
    "2次/日"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/nafld-fibroscan",
  "inputs": {
    "lsm": "14.5",
    "cap": "310",
    "ast": "45",
    "plt": "180"
  },
  "expect": [
    "2)每6-12个月复查FibroScan监测进展"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/saag-ascites",
  "inputs": {
    "serumAlb": "42",
    "ascitesAlb": "12"
  },
  "expect": [
    "30.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": {
    "fit": "75",
    "age": "55",
    "fc": "120"
  },
  "expect": [
    "75"
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
  console.log("==== gastroenterology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
