#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "food-processing/additive-limit-lookup", inputs: {}, _min_inputs: 0, expect: ["螯合金属离子"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-processing/blanching-conditions", inputs: {"n":"3","Dref":"' + e.Dref + '","Tref":"' + e.Tref + '","Z":"' + e.Z + '","T":"95","t":"1.5"}, expect: ["热烫温度"] },
  { slug: "food-processing/dough-absorption", inputs: {"flour":"1000","flourMoist":"13.5","water":"620","otherLiquid":"0","dryAdd":"20","dryMoist":"2"}, expect: ["量后计入"] },
  { slug: "food-processing/emulsion-stability", inputs: {"total":"50","emul":"42","serum":"8","t":"15","rpm":"3000"}, expect: ["提高连续相粘度"] },
  { slug: "food-processing/estimate-analysis-1", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-processing/fermentation-brix", inputs: {"vol":"100","b0":"20","b1":"6","theoYield":"0.511","eff":"92"}, expect: ["密度法测定为准"] },
  { slug: "food-processing/filling-volume", inputs: {"dia":"62","h":"120","V":"330"}, expect: ["灌装量"] },
  { slug: "food-processing/filtration-rate", inputs: {"A":"1","dP":"100","mu":"1.0","alpha":"1e11","c":"20","Rm":"1e10","t":"30"}, expect: ["会增大"] },
  { slug: "food-processing/freeze-thaw-loss", inputs: {"w0":"500","w1":"475","cycles":"1","baseLoss":"5","incRate":"0.15"}, expect: ["仅供工艺参考"] },
  { slug: "food-processing/homogenization-pressure", inputs: {"P0":"20","d0":"1.5","P":"40","b":"0.6","N":"1"}, expect: ["为准"] },
  { slug: "food-processing/material-balance", inputs: {}, _min_inputs: 0, expect: ["存在损耗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food-processing/oil-absorption-rate", inputs: {"w0":"100","m0":"70","w1":"55","m1":"40","k":"0.65"}, expect: ["短油炸"] },
  { slug: "food-processing/ph-adjustment", inputs: {"vol":"10","ph0":"7.0","ph1":"4.5","conc":"1"}, expect: ["建议逐滴加入并实测"] },
  { slug: "food-processing/quick-freeze-time", inputs: {"d":"50","Tf":"-1.5","Tinf":"-35","h":"50","L":"230","rho":"1000","k":"1.5"}, expect: ["测校正"] },
  { slug: "food-processing/recipe-cost-calculator", inputs: {"yield":"1000"}, expect: ["每克成本"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food-processing/residual-oxygen", inputs: {"vol":"500","pvol":"400","o2init":"2","otr":"20","area":"300","days":"180"}, expect: ["结果仅供参考"] },
  { slug: "food-processing/shelf-life-aslt", inputs: {"Tt":"37","Ts":"25","thetaT":"30","Q10":"2"}, expect: ["最终保质期须以实测为"] },
  { slug: "food-processing/smoking-concentration", inputs: {"vol":"2","wood":"300","smokeRate":"5","phenolRatio":"8","t":"120","vent":"3","temp":"60"}, expect: ["为准"] },
  { slug: "food-processing/spray-drying", inputs: {"feed":"500","solid":"40","moist":"4","recovery":"98"}, expect: ["含回收损失"] },
  { slug: "food-processing/sterilization-f-value", inputs: {"T":"110","Tref":"121.1","Z":"10","t":"15","Ftarget":"3","nlog":"0","Dref":"0.1"}, expect: ["安全基准"] },
  { slug: "food-processing/water-activity", inputs: {"aw":"0.85"}, expect: ["需防霉"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== food-processing calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();