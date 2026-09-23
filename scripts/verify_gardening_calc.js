#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gardening/balcony-sunlight",
  "inputs": {},
  "expect": [
    "6.0"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening/compost-calculator",
  "inputs": {},
  "expect": [
    "0.0333"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening/garden-calendar",
  "inputs": {},
  "expect": [
    "10月"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening/garden-layout",
  "inputs": {
    "area": "30"
  },
  "expect": [
    "3265"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/garden-tools",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的工具，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部工具，不产此串）"
},
{
  "slug": "gardening/pest-identifier",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的病虫害，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部病虫害，不产此串）"
},
{
  "slug": "gardening/plant-calendar",
  "inputs": {},
  "expect": [
    "11-12月"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening/plant-care",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的植物，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部植物，不产此串）"
},
{
  "slug": "gardening/pot-capacity",
  "inputs": {
    "${f.id}": "${f.value}_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/recommender",
  "inputs": {
    "cnt": "5"
  },
  "expect": [
    "建议每10-14天1次"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening/soil-ph",
  "inputs": {
    "soilPh": "9.5"
  },
  "expect": [
    "+3.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/watering-schedule",
  "inputs": {
    "potSize": "30"
  },
  "expect": [
    "1.08L"
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
  console.log("==== gardening calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
