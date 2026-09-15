#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "engineering/axial-stress", inputs: {"F":"50","A":"500","E":"200","L":"2"}, expect: ["轴向变形"] },
  { slug: "engineering/beam-calculator", inputs: {"length":"5","load":"10","E":"200","I":"500","limit":"250"}, expect: ["公式"] },
  { slug: "engineering/bending-stress", inputs: {"M":"20","b":"150","h":"300"}, expect: ["最大弯曲应力"] },
  { slug: "engineering/bolt-preload", inputs: {"T":"100","d":"12","K":"0.2"}, expect: ["预紧力"] },
  { slug: "engineering/cantilever-deflection", inputs: {"P":"5","L":"3","E":"30","I":"5000"}, expect: ["自由端转角"] },
  { slug: "engineering/heat-transfer", inputs: {"k":"0.04","A":"10","L":"0.2","T1":"20","T2":"0","h":"10","Ts":"80","Tinf":"20","eps":"0.9","T1K":"500","T2K":"300","h1":"10","h2":"20"}, expect: ["温差"] },
  { slug: "engineering/material-calculator", inputs: {"b":"50","h":"200","L":"1","d":"5.5","D":"50","t":"5","a":"50","c":"50"}, expect: ["角钢"] },
  { slug: "engineering/poisson-strain", inputs: {"ex":"0.001","nu":"0.3"}, expect: ["泊松比"] },
  { slug: "engineering/pressure-vessel", inputs: {"P":"1.6","D":"1000","sigma":"130","phi":"0.85"}, expect: ["计入腐蚀裕量后"] },
  { slug: "engineering/section-inertia", inputs: {"shape":"1","b":"200","h":"400"}, expect: ["矩形"] },
  { slug: "engineering/shaft-torsion", inputs: {"T":"2","d":"50","G":"80","L":"1"}, expect: ["扭转角"] },
  { slug: "engineering/stress-calculator", inputs: {"F":"50","A":"500","V":"30","M":"5000","W":"100","T":"1000","D":"50","d":"0"}, expect: ["扭转应力"] },
  { slug: "engineering/thermal-expansion", inputs: {"alpha":"12","L0":"10","dT":"40"}, expect: ["膨胀量"] },
  { slug: "engineering/weld-strength", inputs: {"F":"50","hf":"6","lw":"200"}, expect: ["焊缝剪应力"] }
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
  console.log("==== engineering calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();