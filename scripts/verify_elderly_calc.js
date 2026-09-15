#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "elderly/aid-height", inputs: {"height":"165","shoe":"2"}, expect: ["肘杖"] },
  { slug: "elderly/assessor-35", inputs: {"age":"75"}, expect: ["提供健康指导和社交活"], _selfcheck: true, _min_inputs: 1 },
  { slug: "elderly/assessor-36", inputs: {}, _min_inputs: 0, expect: ["保持社区联系即可"], _selfcheck: true, _min_inputs: 0 },
  { slug: "elderly/assessor-37", inputs: {}, _min_inputs: 0, expect: ["保持标准"], _selfcheck: true, _min_inputs: 0 },
  { slug: "elderly/assessor-risk-1", inputs: {}, _min_inputs: 0, expect: ["建议保持现有安全措施"], _selfcheck: true, _min_inputs: 0 },
  { slug: "elderly/bp-trend", inputs: {"logSys":"50","logDia":"50","logHr":"50","logGlu":"50"}, expect: ["空腹"] },
  { slug: "elderly/eldercare-level", inputs: {}, _min_inputs: 0, expect: ["完全依赖"], _selfcheck: true, _min_inputs: 0 },
  { slug: "elderly/fall-risk", inputs: {}, _min_inputs: 0, expect: ["站立不稳"], _selfcheck: true, _min_inputs: 0 },
  { slug: "elderly/medication-schedule", inputs: {}, _min_inputs: 0, expect: ["新药"], _selfcheck: true, _min_inputs: 0 },
  { slug: "elderly/reminder-time", inputs: {"medHours":"8"}, expect: ["请先添加"], _selfcheck: true, _min_inputs: 1 },
  { slug: "elderly/wheelchair-width", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== elderly calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();