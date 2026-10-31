#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pet/analysis-cost-profit-1",
  "inputs": {
    "visits": "250",
    "aov": "360",
    "vc": "150",
    "rent": "15000",
    "staff": "25000",
    "util": "4000",
    "other": "6000"
  },
  "expect": [
    "14,500.00",
    "181.0",
    "210.00"
  ],
  "ref": "宠物门店盈亏：unit=360−150=210.00；fixed=15000+25000+4000=44,000.00；profit=(250×360−250×150)+6000−44000=14,500.00；beVisits=(44000−6000)/210=181.0（独立复算；默认组为 25,400.00/170.6/170.00，注入失败即不命中）"
},
{
  "slug": "pet/checker-16",
  "inputs": {
    "bizType": "shop"
  },
  "expect": [
    "shop"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet/checker-diagnosis",
  "inputs": {
    "age": "3",
    "temp": "38.5",
    "weight": "10",
    "duration": "2",
    "species": "cat"
  },
  "expect": [
    "cat"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet/convert-25",
  "inputs": {
    "species": "dog",
    "age": "5"
  },
  "expect": [
    "人类年龄 ≈ 36.0 岁"
  ],
  "ref": "去默认化：狗 5 岁 ⇒ 24+(5−2)×4 = 36.0 岁。默认态 species=dog/age=3 ⇒ 28.0 岁，不命中。"
},
{
  "slug": "pet/convert-25",
  "inputs": {
    "species": "dog",
    "age": "1"
  },
  "expect": [
    "人类年龄 ≈ 15.0 岁"
  ],
  "ref": "去默认化：狗 1 岁 ⇒ 15.0 岁。默认态不命中。"
},
{
  "slug": "pet/convert-25",
  "inputs": {
    "species": "cat",
    "age": "7"
  },
  "expect": [
    "人类年龄 ≈ 44.0 岁"
  ],
  "ref": "去默认化：猫 7 岁 ⇒ 24+(7−2)×4 = 44.0 岁。默认态不命中。"
},
{
  "slug": "pet/pet-age-converter",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "相当于人类年龄（🐕 中型犬 6 岁）",
    "44 岁"
  ],
  "ref": "合并自 pets/pet-age-convert（去默认化：默认犬型=中型犬；6 岁 → 人类 44 岁。默认 3 岁为另一组值）"
},
{
  "slug": "pet/pet-feeding-calc",
  "inputs": {
    "weight": "15",
    "calDensity": "3.5"
  },
  "expect": [
    "534 RER静息能量(kcal)",
    "244 g/天"
  ],
  "ref": "合并自 pets/feeding-amount（去默认化：15kg → RER=70×15^0.75=533.5→534 kcal；×1.6÷3.5=243.9→244 g/天。默认 10kg 得 394 kcal / 180 g/天）"
},
{
  "slug": "pet/grooming-guide",
  "clicks": [
    "setPet('dog');selectBreed('bichon');"
  ],
  "expect": [
    "圆球装"
  ],
  "ref": "合并自 pets/grooming-guide（弱用例去默认化：原锚默认「该品种暂无造型数据」（判别力0）。clicks 经 setPet('dog')+selectBreed('bichon') 切到比熊造型，expect 锚比熊专属「圆球装」；清 clicks 兜底遍历不产出 ⇒ 零逃生项）"
},
{
  "slug": "pet/kennel-space",
  "inputs": {
    "count": "4",
    "days": "7"
  },
  "expect": [
    "24.0 ㎡ 犬舍总面积",
    "61.5 ㎡ 总所需面积（4只中型犬 · 7天）"
  ],
  "ref": "合并自 pets/kennel-space（去默认化：默认中型犬 4只/7天 → 犬舍 6×4=24.0 ㎡，活动区 15×(1+3×0.5)=37.5，总 61.5 ㎡。不可用小型犬值 16.0/36.0：零参兜底 selectSize() 会把尺寸重置为小型犬，同样产出该串 → 逃生项）"
},
{
  "slug": "pet/pet-medicine",
  "inputs": {
    "weight": "15"
  },
  "expect": [
    "15"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet/reminder-vaccine-deworming",
  "inputs": {
    "petWeight": "0",
    "recDate_'+p.id+'": "'+fmtDate(today())+'",
    "petSpecies": "cat"
  },
  "expect": [
    "cat"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet/training-planner",
  "inputs": {
    "age": "junior"
  },
  "expect": [
    "junior"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet/fish-tank-volume",
  "inputs": {
    "length": "90",
    "width": "30",
    "diameter": "40",
    "frontLen": "60",
    "backLen": "50",
    "bowWidth": "30",
    "height": "35",
    "substrate": "5"
  },
  "expect": [
    "19.26"
  ],
  "ref": "auto-restore"
},

{
  "slug": "pet/pet-age",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "44岁"
  ],
  "ref": "auto-restore"
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

  console.log("==== pet calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
