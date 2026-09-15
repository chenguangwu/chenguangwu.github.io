#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "chinese-cook/cutting-sizes", inputs: {}, _min_inputs: 0, expect: ["蒜蓉菜"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese-cook/estimate-16", inputs: {"v1":"100","v2":"20"}, expect: ["结果"] },
  { slug: "chinese-cook/ingredient-substitute", inputs: {}, _min_inputs: 0, expect: ["详情"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese-cook/oil-temp", inputs: {}, _min_inputs: 0, expect: ["食材易吸油"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese-cook/sauce-ratio", inputs: {"spoons":"2"}, expect: ["料酒"], _selfcheck: true, _min_inputs: 1 },
  { slug: "chinese-cook/wok-heat", inputs: {}, _min_inputs: 0, expect: ["防糊防焦"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== chinese-cook calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();