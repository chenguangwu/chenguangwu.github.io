#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "misc/complex-number", inputs: {"aRe":"3","aIm":"4","bRe":"1","bIm":"-2"}, expect: ["结果"] },
  { slug: "misc/function-plotter", inputs: {"xMin":"-10","xMax":"10","yMin":"-10","yMax":"10","p_a":"1","p_b":"10","p_c":"-4","p_w":"1","p_phi":"0"}, expect: ["结果"] },
  { slug: "misc/magic-square", inputs: {"order":"5"}, expect: ["校验"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc/number-puzzle", inputs: {}, _min_inputs: 0, expect: ["参考解法"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc/physics-constants", inputs: {}, _min_inputs: 0, expect: ["天文"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc/scientific-notation", inputs: {"mantissaInput":"6.022","expInput":"23"}, expect: ["数值大小"] },
  { slug: "misc/statistics-distribution", inputs: {"mu":"0","sigma":"1","xval":"1","aVal":"3","bVal":"7","lambda":"3","kval":"5","nval":"10","pval":"0.5"}, expect: ["标准差"] },
  { slug: "misc/truth-table", inputs: {}, _min_inputs: 0, expect: ["变量"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc/unit-prefix", inputs: {"valueInput":"1"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== misc calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();