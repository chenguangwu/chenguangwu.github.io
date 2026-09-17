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
    "96.5%"
  ],
  "ref": "auto-restore(default-hit)"
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
{
  "slug": "food-testing/summary",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
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
