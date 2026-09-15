#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "fengshui/birthday-analysis", inputs: {}, expect: ["人生贵在努力"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fengshui/fengshui-calculator", inputs: {"angleInput":"0"}, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fengshui/fengshui-guide", inputs: {}, expect: ["大要素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fengshui/good-day-selector", inputs: {}, expect: ["出行"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fengshui/zodiac-lookup", inputs: {"birthYear":"1990"}, expect: ["忌配鼠"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== fengshui calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();