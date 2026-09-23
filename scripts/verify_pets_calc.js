#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pets/feeding-amount",
  "inputs": {
    "weight": "15",
    "calDensity": "3.5"
  },
  "expect": [
    "534 RER静息能量(kcal)",
    "244 g/天"
  ],
  "ref": "auto-restore（去默认化：15kg → RER=70×15^0.75=533.5→534 kcal；×1.6÷3.5=243.9→244 g/天。默认 10kg 得 394 kcal / 180 g/天）"
},
{
  "slug": "pets/grooming-guide",
  "inputs": {},
  "expect": [
    "该品种暂无造型数据"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pets/kennel-space",
  "inputs": {
    "count": "4",
    "days": "7"
  },
  "expect": [
    "24.0 ㎡ 犬舍总面积",
    "61.5 ㎡ 总所需面积（4只中型犬 · 7天）"
  ],
  "ref": "auto-restore（去默认化：默认中型犬 4只/7天 → 犬舍 6×4=24.0 ㎡，活动区 15×(1+3×0.5)=37.5，总 61.5 ㎡。**不可用小型犬值 16.0/36.0**：零参兜底 selectSize() 会把尺寸重置为小型犬，同样产出该串 → 逃生项）"
},
{
  "slug": "pets/pet-age-convert",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "相当于人类年龄（🐕 中型犬 6 岁）",
    "44 岁"
  ],
  "ref": "auto-restore（去默认化：默认犬型=中型犬（currentSize='medium'）；6 岁 → 人类 44 岁。默认 3 岁为另一组值）"
},
{
  "slug": "pets/vaccine-reminder",
  "inputs": {
    "newType": "cat"
  },
  "expect": [
    "cat"
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
  console.log("==== pets calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
