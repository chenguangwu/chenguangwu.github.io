#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "text/analysis-density",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/calc-1",
  "inputs": {
    "textA": "",
    "textB": ""
  },
  "expect": [
    "console.log("
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "text/convert-6",
  "inputs": {
    "val": "Hello World",
    "to": "lower"
  },
  "expect": [
    "lower"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/convert-7",
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
  "slug": "text/lorem-ipsum-generator",
  "inputs": {
    "n": "3",
    "seed": "mid"
  },
  "expect": [
    "mid"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/reading-time-estimator",
  "inputs": {
    "cjkwpm": "450",
    "enwpm": "200",
    "src": "在纯前端工具站里，阅读时长估算是一个很实用的小功能，帮助用户判断一篇长文需要投入多少时间。"
  },
  "expect": [
    "450"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/sensitive-word-filter",
  "inputs": {
    "replaceWith": "*_X",
    "content": "",
    "words": "违法,垃圾,诈骗,外挂"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/stats-1",
  "inputs": {
    "text": "统计中文 English 测试 ABC 数字 99 与符号！"
  },
  "expect": [
    "24",
    "11"
  ],
  "ref": "字数统计：'统计中文 English 测试 ABC 数字 99 与符号！' → 含空白30、不含空白24、中文11、英文单词2(English/ABC)、数字组1(99)、行数1、非空行1（非默认输入，注入失败即不命中）"
},
{
  "slug": "text/text-to-1337",
  "inputs": {
    "src": "leet speak is fun",
    "level": "mid"
  },
  "expect": [
    "mid"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/text-to-ascii-art",
  "inputs": {
    "src": "HELLO_X",
    "ch": "#"
  },
  "expect": [
    "HELLO_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "text/text-to-braille",
  "inputs": {
    "src": "Hello 123!_X"
  },
  "expect": [
    "_X"
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
  console.log("==== text calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
