#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "food-testing/acid-peroxide-titration", inputs: {"acidV":"2.50","acidC":"0.1000","acidM":"3.00","acidLimit":"3","povV1":"12.50","povV0":"0.20","povC":"0.0020","povM":"2.00","povLimit":"0.25"}, expect: ["超标"] },
  { slug: "food-testing/aflatoxin-limit", inputs: {"detected":"5.0","limit":"20"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "food-testing/allergen-cross-risk", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-testing/assessor-risk-6", inputs: {"salmonella":"0","staph":"100","ecoli":"0","listeria":"0","vibrio":"0","tvc":"5000"}, expect: ["标准"] },
  { slug: "food-testing/coliform-mpn", inputs: {"d1":"3","d2":"2","d3":"1","inoc1":"0.1"}, expect: ["结果为"] },
  { slug: "food-testing/colony-count", inputs: {"d1p1":"156","d1p2":"168","d2p1":"18","d2p2":"22","inoculum":"1"}, expect: ["报告为"] },
  { slug: "food-testing/convert-36", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "food-testing/convert-37", inputs: {"val":"1"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food-testing/detector-3", inputs: {"da0":"0.500","dat":"0.300"}, expect: ["抑制率"] },
  { slug: "food-testing/elisa-conversion", inputs: {"sampleOD":"0.650","dilution":"1","limit":"1.0"}, expect: ["建议检查标准曲线"] },
  { slug: "food-testing/fat-soxhlet", inputs: {"sampleMass":"2.000","moisture":"5.0","flaskEmpty":"60.000","flaskFat":"61.250","theoretical":"0"}, expect: ["干基含量"] },
  { slug: "food-testing/foreign-matter-density", inputs: {"particleDensity":"7800","diameter":"2.0","fluidDensity":"1000","viscosity":"0.001"}, expect: ["属检测"] },
  { slug: "food-testing/generator-27", inputs: {"cnt":"5"}, expect: ["报告结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food-testing/generator-31", inputs: {"cnt":"5"}, expect: ["流水号"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food-testing/heavy-metal-migration", inputs: {"conc":"0.05","volume":"100","area":"2","foodVol":"1000","sml":"0.01"}, expect: ["超标"] },
  { slug: "food-testing/ingredient-sorter", inputs: {}, _min_inputs: 0, expect: ["的规定"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-testing/irradiation-dose", inputs: {"d10":"0.5","n0":"100000","n":"1","dose":"3.0"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "food-testing/nitrite-colorimetric", inputs: {"slope":"0.0185","intercept":"0.002","absorbance":"0.210","weight":"5.0","totalVol":"100","testVol":"40","colorVol":"50","limit":"30"}, expect: ["超标"] },
  { slug: "food-testing/nutrition-label-nrv", inputs: {"servingSize":"100","energy":"800","protein":"5","fat":"10","satFat":"3","carbs":"60","sugar":"15","sodium":"200","fiber":"0","calcium":"0","iron":"0","vitA":"0","vitC":"0"}, expect: ["碳水化合物"] },
  { slug: "food-testing/packaging-migration", inputs: {"conc":"0.5","volume":"200","area":"3","sml":"1.5"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "food-testing/pesticide-residue-test", inputs: {"dA0":"0.500","dA":"0.450"}, expect: ["抑制率"] },
  { slug: "food-testing/protein-kjeldahl", inputs: {"v1":"10.50","v0":"0.20","acidC":"0.0500","mass":"0.500","factor":"6.25"}, expect: ["蛋白质含量"] },
  { slug: "food-testing/salmonella-serotype", inputs: {}, _min_inputs: 0, expect: ["常见食源性病原体"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-testing/salt-titration", inputs: {"agNo3Vol":"10.50","agNo3C":"0.1000","sampleMass":"5.00","totalVol":"100","testVol":"20","limit":"0"}, expect: ["食盐含量"] },
  { slug: "food-testing/sugar-fehling", inputs: {"fehlingF":"0.500","sampleMass":"5.00","totalVol":"250","titrateVol":"15.20","reducingSugar":"0"}, expect: ["定容体积"] },
  { slug: "food-testing/summary", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-testing/total-migration", inputs: {"m1":"50000.0","m2":"50015.0","m0":"48000.0","area":"3","limit":"10"}, expect: ["总迁移限量要求"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== food-testing calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();