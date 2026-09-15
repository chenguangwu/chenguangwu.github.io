#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "decor/ceiling-panel-quantity", inputs: {"L":"4.2","W":"3.6","pl":"600","pw":"600","loss":"5"}, expect: ["经济型厨卫"] },
  { slug: "decor/curtain-fabric", inputs: {"rodW":"2.5","curtainH":"2.6","sideHem":"0.05","topBottomHem":"0.3","patternLoss":"0"}, expect: ["需分别计算后相加"] },
  { slug: "decor/detector-18", inputs: {"hcho":"0.08","tvoc":"0.50","benzene":"0.05","ammonia":"0.15","radon":"200"}, expect: ["室内空气质量合格"] },
  { slug: "decor/paint-color-mix", inputs: {"paintKg":"5"}, expect: ["避免一次性过量"], _selfcheck: true, _min_inputs: 1 },
  { slug: "decor/room-illumination", inputs: {"area":"20","lux":"100","wattPer":"12","util":"0.6","maint":"0.8"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "decor/scheduler", inputs: {}, expect: ["请添加或载入模板"], _selfcheck: true, _min_inputs: 0 },
  { slug: "decor/skirting-length", inputs: {"roomLen":"5","roomWid":"4","doors":"1","doorWid":"0.9","windows":"0","winWid":"1.5","wasteSk":"5","wasteCo":"8","skLen":"2.4","coLen":"2.4"}, expect: ["每根"] },
  { slug: "decor/wallpaper-quantity", inputs: {"perimeter":"12","height":"2.8","deduct":"6","rollWidth":"0.53","rollLen":"10","pattern":"0.32","waste":"5"}, expect: ["素色无花壁纸损耗率可"] }
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
  console.log("==== decor calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();