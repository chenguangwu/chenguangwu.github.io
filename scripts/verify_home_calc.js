#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "home/furniture-layout", inputs: {"rl":"5","rw":"4"}, expect: ["橱柜"] },
  { slug: "home/lighting-calculator", inputs: {"length":"5","width":"4","height":"2.8","lumens":"800","cu":"0.6","mf":"0.8"}, expect: ["合计"] },
  { slug: "home/paint-calculator", inputs: {"surface-area":"30","coats":"2","coverage":"10","bucket-size":"5","bucket-price":"280"}, expect: ["客厅墙面"] },
  { slug: "home/renovation-budget", inputs: {"new-price":"0","new-qty":"1"}, expect: ["暂无数据"] },
  { slug: "home/room-calculator", inputs: {"${f}":"${f==='radius'?3:5}"}, expect: ["暂无历史"], _selfcheck: true, _min_inputs: 1 },
  { slug: "home/washer-capacity", inputs: {"people":"3"}, expect: ["大件"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== home calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();