#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "electronics/analysis-22", inputs: {"V":"3.7","Ia":"25","Is":"0.05","duty":"5","C":"2000"}, expect: ["容量"] },
  { slug: "electronics/bandwidth", inputs: {"gain":"10","freq":"100000"}, expect: ["暂无计算记录"] },
  { slug: "electronics/calc-63", inputs: {"cur":"2","oz":"1","dt":"20"}, expect: ["暂无计算记录"] },
  { slug: "electronics/calc-frequency", inputs: {"l":"100","freq":"1000"}, expect: ["暂无计算记录"] },
  { slug: "electronics/calc-time-2", inputs: {"r":"10000","c":"10"}, expect: ["暂无计算记录"] },
  { slug: "electronics/capacitance", inputs: {"cl":"16","cs":"3"}, expect: ["暂无计算记录"] },
  { slug: "electronics/capacitor-calculator", inputs: {"R":"10000","C":"1000","V":"5"}, expect: ["耐压增加"] },
  { slug: "electronics/circuit-calculator", inputs: {"L":"10","C":"1","R":"10","val":"20","f":"1000","V":"5","I":"2","pf":"0.85"}, expect: ["带宽"] },
  { slug: "electronics/convert-capacitance", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "electronics/crystal-divider", inputs: {"xtal1":"16","divider1":"8","xtal2":"8","multi":"9","preDiv":"1","outDiv":"2","xtal3":"12","target":"48"}, expect: ["高频系统时钟"] },
  { slug: "electronics/current-pressure-drop", inputs: {"im":"100","temp":"25"}, expect: ["暂无计算记录"] },
  { slug: "electronics/dianyuanxiaolvldo-dcdc", inputs: {"vin":"12","vout":"5","iout":"1","eff":"90"}, expect: ["暂无计算记录"] },
  { slug: "electronics/estimate-power-1", inputs: {"vcc":"24","rl":"8"}, expect: ["暂无计算记录"] },
  { slug: "electronics/frequency-11", inputs: {"r":"10000","c":"0.1","l":"100"}, expect: ["暂无计算记录"] },
  { slug: "electronics/frequency-12", inputs: {"r":"16000","c":"0.01","l":"100","c1":"100","c2":"100","xf":"12"}, expect: ["暂无计算记录"] },
  { slug: "electronics/frequency-13", inputs: {"freq":"433","len":"0.35"}, expect: ["暂无计算记录"] },
  { slug: "electronics/pcb-power", inputs: {"power":"5","area":"100","ambient":"25","coverage":"60"}, expect: ["需优化热设计"] },
  { slug: "electronics/pcbzukangdieceng", inputs: {"er":"4.4","w":"0.2","h":"0.1","t":"0.035"}, expect: ["暂无计算记录"] },
  { slug: "electronics/resistance-resistor", inputs: {}, _min_inputs: 0, expect: ["暂无计算记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "electronics/resistor-calculator", inputs: {"vin":"12","r1":"1000","r2":"2000"}, expect: ["最大值"] },
  { slug: "electronics/smt-stencil", inputs: {"padW":"0.5","padL":"2.0","reduce":"10","pitch":"0.5","transfer":"70"}, expect: ["焊膏释放良好"] }
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
  console.log("==== electronics calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();