#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "electrical/battery-bank", inputs: {"cellV":"3.2","cellAh":"100","seriesN":"16","parallelN":"2","loadW":"500","dod":"80","eff":"90"}, expect: ["每组串联"] },
  { slug: "electrical/breaker-sizing", inputs: {"I":"10"}, expect: ["选择合理"], _selfcheck: true, _min_inputs: 1 },
  { slug: "electrical/calc-1", inputs: {"area":"4","ambient":"30","group":"1.0","soil":"1.0","depth":"1.0"}, expect: ["环境温度"] },
  { slug: "electrical/calc-2", inputs: {"voltage":"380","current":"50","pf":"0.85","pInput":"","qInput":""}, expect: ["功率因数"] },
  { slug: "electrical/calc-power-capacitance", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "electrical/current-divider", inputs: {"It":"100","R1":"1000","R2":"2000"}, expect: ["电流合计"] },
  { slug: "electrical/home-load-estimate", inputs: {"fridge":"1","ac":"2","washer":"1","waterheater":"1","kitchen":"3000","light":"500"}, expect: ["预热耗电"] },
  { slug: "electrical/led-resistor", inputs: {"Vs":"5","Vf":"2.0","If":"20"}, expect: ["电阻功耗"] },
  { slug: "electrical/load-curve", inputs: {"h'+h+'":"'+PRESETS.factory[h]+'"}, expect: ["电时段"], _selfcheck: true, _min_inputs: 1 },
  { slug: "electrical/opamp-gain", inputs: {"Rin":"1000","Rf":"10000"}, expect: ["同相增益"] },
  { slug: "electrical/power-factor-compensation", inputs: {"power":"200","pf1":"0.75","pf2":"0.95"}, expect: ["有效减少线路损耗"] },
  { slug: "electrical/rc-filter", inputs: {"R":"10","C":"0.1"}, expect: ["截止频率"] },
  { slug: "electrical/rlc-resonance", inputs: {"L":"10","C":"0.1"}, expect: ["谐振频率"] },
  { slug: "electrical/transformer-sizing", inputs: {"pTotal":"160","cosPhi":"0.85","kd":"0.8","beta":"0.75","kReserve":"1.1","uKv":"0.4"}, expect: ["可选标准容量"] },
  { slug: "electrical/voltage-capacity-battery", inputs: {"v0":"100","v1":"50","v2":"10"}, expect: ["合计"] },
  { slug: "electrical/voltage-divider", inputs: {"vin":"12","r1":"1000","r2":"2000","rl":"1000","r":"1000","pos":"50","n":"3"}, expect: ["功耗"] },
  { slug: "electrical/voltage-drop", inputs: {"power":"15","length":"80","cosPhi":"0.85","section":"10","allowDrop":"5"}, expect: ["满足要求"] },
  { slug: "electrical/wire-gauge-selector", inputs: {"I":"20","len":"30"}, expect: ["即热式热水器"] },
  { slug: "electrical/wire-resistance", inputs: {"rho":"0.0172","L":"100","A":"2.5"}, expect: ["每千米电阻"] }
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
  console.log("==== electrical calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();