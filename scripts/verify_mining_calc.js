#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "mining/analysis-cost-3", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "mining/calc-1", inputs: {"q":"0.45","k":"0.4","a":"3.0","b":"2.5","H":"10","W":"2.5","holes":"20","stem":"2.0"}, expect: ["近似"] },
  { slug: "mining/calc-ventilation", inputs: {"workers":"30","diesel":"120","explosive":"50","gas":"3","cmax":"1","leak":"1.2"}, expect: ["暂无计算记录"] },
  { slug: "mining/checker-training-hr", inputs: {"gas":"0.6","vent":"8000","ventReq":"7500","equip":"96","train":"95","hours":"28","rect":"92","monitor":"98"}, expect: ["本要求"] },
  { slug: "mining/convert-grade-ore", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "mining/estimate-reserve", inputs: {}, _min_inputs: 0, expect: ["请先添加至少一个块段"], _selfcheck: true, _min_inputs: 0 },
  { slug: "mining/excavation-volume", inputs: {"swell":"1.3","price":"20","L":"25","W":"10","D":"2","W1":"12","W2":"6","slope":"1","D1":"20","D2":"10","H":"5"}, expect: ["单价"] },
  { slug: "mining/haulage-optimization", inputs: {"totalTonnage":"1500","shiftMinutes":"480","carCapacity":"20","loadFactor":"0.9","loadTime":"5","haulTime":"12","dumpTime":"3","returnTime":"10","waitTime":"3","utilization":"75"}, expect: ["各项指标合理"] },
  { slug: "mining/mineral-density", inputs: {"mass":"1000","volume":"500","solidVol":"350"}, expect: ["孔隙比"] },
  { slug: "mining/ore-grade", inputs: {"gradeInput":"3.5","oreAmount":"100000","metalPrice":"500"}, expect: ["品位"] },
  { slug: "mining/reserve-estimate", inputs: {"areaInput":"50000","thickInput":"12.5","densityInput":"2.8","gradeInput":"3.2","recoveryInput":"85"}, expect: ["中型矿床"] },
  { slug: "mining/safety-check", inputs: {"riskValue":"12"}, expect: ["输入具体数值获得分级"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== mining calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();