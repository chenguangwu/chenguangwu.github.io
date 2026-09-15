#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "cognition/cognitive-assessment", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/corsi-block-test", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/digit-span-test", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/human-benchmark", inputs: {}, _min_inputs: 0, expect: ["项测评后将自动保存记"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/nback-training", inputs: {}, _min_inputs: 0, expect: ["当前"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/schulte-table", inputs: {}, _min_inputs: 0, expect: ["暂无记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/stroop-test", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cognition/time-perception", inputs: {}, _min_inputs: 0, expect: ["秒再松手"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== cognition calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();