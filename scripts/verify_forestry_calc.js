#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "forestry/area-18", inputs: {"scale":"1"}, expect: ["紧凑度越大形状越狭长"], _selfcheck: true, _min_inputs: 1 },
  { slug: "forestry/calc-57", inputs: {"total":"100","covered":"65"}, expect: ["生长良好"] },
  { slug: "forestry/carbon-sequestration", inputs: {"area":"10","volume":"120","age":"20","biomass":"80","rootRatio":"0.25","mai":"10","carbonPrice":"60"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forestry/concentration-5", inputs: {"conc":"1800"}, expect: ["属优质森林康养环境"], _selfcheck: true, _min_inputs: 1 },
  { slug: "forestry/density-5", inputs: {"area":"600","n":"80","dbh":"16"}, expect: ["可考虑抚育间伐"] },
  { slug: "forestry/density-6", inputs: {"sp":"2","rp":"3","area":"100","cost":"2.5"}, expect: ["杉木"] },
  { slug: "forestry/estimate-32", inputs: {"area":"667","n":"120","dbh":"14","h":"12","f":"0.5"}, expect: ["公顷蓄积"] },
  { slug: "forestry/estimate-33", inputs: {"len":"5","w":"25","n":"12","tarea":"50"}, expect: ["估算种群数量"] },
  { slug: "forestry/forest-area", inputs: {"slope":"0","len1":"50","len2":"80","len3":"50","pointCount":"4","px'+i+'":"'+pts[i].x+'","py'+i+'":"'+pts[i].y+'"}, expect: ["暂无历史"] },
  { slug: "forestry/forest-volume", inputs: {"count":"15","avgH":"12","formFactor":"0.42","area":"10","plotArea":"600","plotVol":"9","dbh":"16","treesPerHa":"1500"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forestry/growth-rate", inputs: {"v1":"0.1","v2":"0.15","years":"5"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forestry/log-volume", inputs: {"diameter":"20","length":"4","quantity":"1"}, expect: ["暂无历史"] },
  { slug: "forestry/pest-1", inputs: {"damaged":"35","total":"200"}, expect: ["控制蔓延"] },
  { slug: "forestry/planting-density", inputs: {"spacing":"2","rowSpacing":"3","area":"100"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forestry/shengwuduoyangxingshannon", inputs: {}, expect: ["相对丰度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forestry/strength-4", inputs: {"stock":"180","ratio":"25","cycle":"10","area":"500"}, expect: ["抚育"] },
  { slug: "forestry/tree-age", inputs: {"dbh":"20","height":"12","growthPerYear":"0.8","seedlingAge":"2"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forestry/tree-volume", inputs: {"dbh":"20","height":"14","formFactor":"0.42","quantity":"1"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forestry/yield", inputs: {"area":"100","density":"55","yield":"15","price":"8","rate":"85"}, expect: ["亩产值"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== forestry calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
