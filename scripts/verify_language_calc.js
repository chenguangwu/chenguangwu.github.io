#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "language/calc-1",
  "inputs": {
    "knownRatio": "90"
  },
  "expect": [
    "90"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/calc-2",
  "inputs": {
    "wordCount": "1200",
    "comprehension": "80",
    "minutes": "3",
    "seconds": "30"
  },
  "expect": [
    "342.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/french-verb-conjugator",
  "inputs": {},
  "expect": [
    "commencer"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "language/generator-19",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/hanyuyanwenchaijie-yuanyin-fuyin",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/idiom-solitaire",
  "inputs": {
    "timeLimit": "20"
  },
  "expect": [
    "20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/korean-hangul-decomposer",
  "inputs": {},
  "expect": [
    "请输入韩文内容"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "language/language-toolkit",
  "inputs": {
    "acronymInput": "",
    "charInput": ""
  },
  "expect": [
    "154"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "language/phrase-translator",
  "inputs": {},
  "expect": [
    "gentlemen."
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "language/riyuwushiyintulianxi-dianjifayin",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/stats-2",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/text-polisher",
  "inputs": {
    "input": "这是一段 测试文本，里面有  多余空格 。中英文 混排时 , 标点容易出错 。_X"
  },
  "expect": [
    "41"
  ],
  "ref": "auto-restore"
},
{
  "slug": "language/translator",
  "inputs": {
    "src-text": "",
    "tgt-text": ""
  },
  "expect": [
    "Tomorrow"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "language/vocabulary-builder",
  "inputs": {},
  "expect": [
    "50"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "language/xibanyayuzhongyinweizhipanduan-neizhiguize",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
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
  console.log("==== language calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
