#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "fengshui/birthday-analysis", inputs: {}, _min_inputs: 0, expect: ["人生贵在努力"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fengshui/fengshui-calculator", inputs: {"angleInput":"0"}, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fengshui/fengshui-guide", inputs: {}, _min_inputs: 0, expect: ["大要素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fengshui/good-day-selector", inputs: {}, _min_inputs: 0, expect: ["出行"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fengshui/zodiac-lookup", inputs: {"birthYear":"1990"}, expect: ["忌配鼠"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== fengshui calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();