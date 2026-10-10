#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "food-testing/acid-peroxide-titration",
  "inputs": {
    "acidV": "5.5",
    "acidC": "0.1000",
    "acidM": "3.00",
    "acidLimit": "3",
    "povV1": "12.50",
    "povV0": "0.20",
    "povC": "0.0020",
    "povM": "2.00",
    "povLimit": "0.25"
  },
  "expect": [
    "10.285"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/assessor-risk-6",
  "inputs": {
    "salmonella": "7",
    "staph": "100",
    "ecoli": "0",
    "listeria": "0",
    "vibrio": "0",
    "tvc": "5000"
  },
  "expect": [
    "检出(不得检出)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/coliform-mpn",
  "inputs": {
    "d1": "6",
    "d2": "2",
    "d3": "1",
    "inoc1": "0.1"
  },
  "expect": [
    "5-2-1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/colony-count",
  "inputs": {
    "d1p1": "234",
    "d1p2": "168",
    "d2p1": "18",
    "d2p2": "22",
    "inoculum": "1"
  },
  "expect": [
    "2.0×10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/convert-36",
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
  "slug": "food-testing/convert-37",
  "inputs": {
    "val": "1",
    "from": "6.25"
  },
  "expect": [
    "6.25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/detector-3",
  "inputs": {
    "da0": "3.5",
    "dat": "0.300"
  },
  "expect": [
    "3.500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/elisa-conversion",
  "inputs": {
    "sampleOD": "3.65",
    "dilution": "1",
    "limit": "1.0"
  },
  "expect": [
    "202.78%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/fat-soxhlet",
  "inputs": {
    "sampleMass": "5",
    "moisture": "5.0",
    "flaskEmpty": "60.000",
    "flaskFat": "61.250",
    "theoretical": "0"
  },
  "expect": [
    "2631.5789%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/foreign-matter-density",
  "inputs": {
    "particleDensity": "11700",
    "diameter": "2.0",
    "fluidDensity": "1000",
    "viscosity": "0.001"
  },
  "expect": [
    "(23326.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/generator-27",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "#8"
  ],
  "ref": "auto-restore-structural（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "food-testing/heavy-metal-migration",
  "inputs": {
    "conc": "3.05",
    "volume": "100",
    "area": "2",
    "foodVol": "1000",
    "sml": "0.01"
  },
  "expect": [
    "152.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/ingredient-sorter",
  "inputs": {
    "foodName": "",
    "ingredients": "小麦粉, 55\n水, 20\n白砂糖, 10\n植物油, 8\n酵母, 2\n食盐, 1\n食用香精, 0.5",
    "sortMode": "asc"
  },
  "expect": [
    "asc"
  ],
  "ref": "配料排序 sortMode=asc（默认 desc）；排序结果内容相同、仅排序模式串随输入变化。「96.5%」为恒定合计占比（原逃生项），改锚定 asc。"
},
{
  "slug": "food-testing/nitrite-colorimetric",
  "inputs": {
    "slope": "3.0185",
    "intercept": "0.002",
    "absorbance": "0.210",
    "weight": "5.0",
    "totalVol": "100",
    "testVol": "40",
    "colorVol": "50",
    "limit": "30"
  },
  "expect": [
    "3.0185"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/nutrition-label-nrv",
  "inputs": {
    "foodName": "示例食品",
    "servingSize": "150",
    "energy": "800",
    "protein": "5",
    "fat": "10",
    "satFat": "3",
    "carbs": "60",
    "sugar": "15",
    "sodium": "200",
    "fiber": "0",
    "calcium": "0",
    "iron": "0",
    "vitA": "0",
    "vitC": "0"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/pesticide-residue-test",
  "inputs": {
    "dA0": "3.5",
    "dA": "0.450"
  },
  "expect": [
    "87.14%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/protein-kjeldahl",
  "inputs": {
    "v1": "15.5",
    "v0": "0.20",
    "acidC": "0.0500",
    "mass": "0.500",
    "factor": "6.25"
  },
  "expect": [
    "13.3875%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/salmonella-serotype",
  "inputs": {
    "oAntigen": "4",
    "h1Antigen": "i",
    "h2Antigen": "1,2",
    "seroName": "Typhimurium",
    "queryMode": "name"
  },
  "expect": [
    "name"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/salt-titration",
  "inputs": {
    "agNo3Vol": "15.5",
    "agNo3C": "0.1000",
    "sampleMass": "5.00",
    "totalVol": "100",
    "testVol": "20",
    "limit": "0"
  },
  "expect": [
    "(90.675"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/sugar-fehling",
  "inputs": {
    "fehlingF": "3.5",
    "sampleMass": "5.00",
    "totalVol": "250",
    "titrateVol": "15.20",
    "reducingSugar": "0"
  },
  "expect": [
    "1151.3158"
  ],
  "ref": "auto-restore"
},
  // 注：food-testing/summary 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "food-testing/total-migration",
  "inputs": {
    "m1": "75000",
    "m2": "50015.0",
    "m0": "48000.0",
    "area": "3",
    "limit": "10"
  },
  "expect": [
    "75000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food-testing/aflatoxin-limit",
  "inputs": { "detected": "15", "limit": "20", "foodCategory": "corn" },
  "expect": ["食品类别「玉米及其制品」", "75 占限量比 %", "合格（接近限值）"],
  "ref": "注入非默认（默认 detected=5.0 / foodCategory=peanut_oil）：15/20 = 75% ⇒ 未超限量但 ≥50% ⇒ 判定「合格（接近限值）」、风险等级中风险；类别切换联动更新限量与类别名。默认态 5.0/20 = 25% ⇒ 合格（远低于限值）、低风险，三串均不出现。"
},
{
  "slug": "food-testing/allergen-cross-risk",
  "inputs": {
    "allergenType": "nut", "sharedEquip": "simultaneous", "cleaning": "none",
    "changeover": "none", "form": "powder", "amount": "high",
    "airborne": "high", "packaging": "open"
  },
  "expect": ["综合得分 39/40（98%）", "综合风险评分 39 /40", "包装隔离 4/5"],
  "ref": "8 个 select 全部注入非默认（默认全取首项：peanut/dedicated/validated/long/liquid/trace/none/separate ⇒ 低风险低分）。因子分值取自各 option 的 data-score：过敏原类型 5、设备共用 5、清洁验证 5、切换间隔 5、物理形态 5、添加量 5、空气传播 5、包装隔离 4 ⇒ 合计 39/40（98%）⇒ 极高风险。⚠ harness 需建模 option 的 data-*（本轮已补 mkOpt 的 dataset/getAttribute），否则各因子读不到分而输出「—」，该页恒不可验证。"
},
{
  "slug": "food-testing/irradiation-dose",
  "inputs": { "organism": "listeria", "n": "100" },
  "expect": ["所需辐照剂量 1.2 kGy", "灭活3个对数级需 1.2 kGy"],
  "ref": "注入非默认（默认 organism=salmonella / n0=100000 / n=1）。选 organism 会联动改写 d10（单增李斯特菌 data-d10 = 0.4 kGy，沙门氏菌 0.5）⇒ 不手工注入 d10（注入也会被 onchange 覆盖，这正是真机行为）。灭活对数 = log₁₀(n0/n) = log₁₀(100000/100) = 3；所需剂量 = 0.4 × 3 = 1.2 kGy。默认态：n=1 ⇒ 对数 5、剂量 0.5×5 = 2.5 kGy，两串均不出现。"
},
{
  "slug": "food-testing/packaging-migration",
  "inputs": { "conc": "2.0", "volume": "500", "area": "6", "substance": "BPA", "simulant": "95%乙醇" },
  "expect": ["0.16667 迁移量 mg/dm²", "判定为 超标"],
  "ref": "注入非默认（默认 conc=0.5/volume=200/area=3/substance=DEHP/simulant=10%乙醇）。选 substance 会联动改写 sml（BPA 的 SML = 0.6 mg/kg，DEHP 为 1.5）⇒ 不手工注入 sml。迁移量 = conc×volume/area/1000 = 2.0×500/6/1000 = 0.16667 mg/dm²；食品中含量 = 0.16667×6 = 1 mg/kg > SML 0.6 ⇒ 判定超标。默认态 0.5×200/3/1000 = 0.03333、含量 0.2 < 1.5 ⇒ 判定合格，两串均不出现。"
},
  {
    "slug": "food-testing/generator-31",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "0240425-L1772 16. 69025272047-B806059-20231201-L1682 17. 69038782100-B270359-20231217-L9085 18. 69054902830-B187499-2024"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「0240425-L1772 16. 69025272047-B806059-20…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== food-testing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
