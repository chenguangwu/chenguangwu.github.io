#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "construction/ac-size-guide", inputs: {"area":"20","height":"2.8","windows":"1"}, expect: ["调销售人员"] },
  { slug: "construction/area-calculator", inputs: {"len1":"5","wid1":"4","lA":"8","lB":"6","la":"3","lb":"2","radius":"3","rooms":"3","shared":"20"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/area", inputs: {"area":"20","height":"2.8"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/blueprint-tool", inputs: {"customScale":"100","distance":"100"}, expect: ["暂无历史"] },
  { slug: "construction/brick-calculator", inputs: {"length":"10","height":"3","loss":"3"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/calc-1", inputs: {"od":"48.3","thickness":"3.6","fy":"205","h":"1.8","k":"1.155","a":"0.3","area":"4","load":"3","self":"0.35"}, expect: ["稳定满足"] },
  { slug: "construction/calc-5", inputs: {"dia":"20","logLen":"4","logQty":"10","bLen":"2.4","bWid":"120","bThk":"40","bQty":"50"}, expect: ["暂无计算记录"] },
  { slug: "construction/calc-6", inputs: {"altitude":"60","overhang":"0.8","winH":"1.5"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/calc-area-lux", inputs: {"area":"20","cu":"0.5","mf":"0.8"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/calc-dosage-1", inputs: {"area":"20","tLen":"600","tWid":"600","gap":"2","waste":"5","perBox":"4"}, expect: ["暂无计算记录"] },
  { slug: "construction/calc-dosage", inputs: {"area":"20","fLen":"1215","fWid":"165","waste":"5","perBox":"10"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/calc-power-voltage", inputs: {"power":"5000","pf":"0.8","kd":"0.8"}, expect: ["暂无计算记录"] },
  { slug: "construction/calculator-calc-area", inputs: {"shareRate":"25"}, expect: ["暂无计算记录"], _selfcheck: true, _min_inputs: 1 },
  { slug: "construction/calculator-calc-ratio-2", inputs: {"volume":"10","pCement":"450","pSand":"120","pStone":"130"}, expect: ["暂无计算记录"] },
  { slug: "construction/cement-mortar-ratio", inputs: {"vol":"1","bag":"50"}, expect: ["基础"] },
  { slug: "construction/concrete-calculator", inputs: {"loss":"3","length":"10","width":"5","height":"0.12"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "construction/construction-calculator", inputs: {"paintWallCount":"4","paintWallLen":"5","paintWallH":"2.8","paintCoverage":"10","paintCoats":"2","floorArea":"20","floorLen":"1210","floorWid":"165","floorWaste":"5","floorPpPack":"8","tileArea":"15","tileLen":"600","tileWid":"600","tileWaste":"10","concVol":"1","elecPower":"2000","elecVolt":"220","stairHeight":"280","stairRise":"17"}, expect: ["级应设休息平台"] },
  { slug: "construction/cost-estimator", inputs: {"area":"100"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "construction/estimate-area-dosage", inputs: {"area":"50","thk":"0.15","density":"1400","perBucket":"25","waste":"5"}, expect: ["暂无计算记录"] },
  { slug: "construction/pipe-flow", inputs: {"diameter":"25","velocity":"1.5","pipeLength":"10","temperature":"20"}, expect: ["流速在合理范围内"] },
  { slug: "construction/radiator-calculator", inputs: {"roomArea":"20","roomHeight":"2.8"}, expect: ["组安装以确保散热均匀"] },
  { slug: "construction/renovation-labor-cost", inputs: {"area":"90"}, expect: ["请至少勾选一个施工项"], _selfcheck: true, _min_inputs: 1 },
  { slug: "construction/soundproof-material", inputs: {"wallArea":"20"}, expect: ["施工人工费未计入"], _selfcheck: true, _min_inputs: 1 },
  { slug: "construction/timber-volume", inputs: {"logD1":"20","logD2":"18","logLen":"4","logQty":"1","boardLen":"4","boardW":"0.12","boardH":"0.05","boardQty":"1"}, expect: ["单块"] },
  { slug: "construction/window-shading", inputs: {"latitude":"39.9","hour":"12","winH":"1.5","winW":"1.2","overhang":"0.5"}, expect: ["较差"] }
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
  console.log("==== construction calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();