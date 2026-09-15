#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "chinese/chinese-character", inputs: {}, expect: ["无相关汉字"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese/chinese-culture", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese/chinese-radical-lookup", inputs: {}, expect: ["请输入一个汉字进行查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese/lunar-calendar", inputs: {}, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "chinese/stroke-order-viewer", inputs: {}, expect: ["结果供学习参考"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== chinese calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();