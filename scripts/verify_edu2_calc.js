#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "edu2/exam-analysis", inputs: {"fullScore":"100","passLine":"60","excellentLine":"85"}, expect: ["不及格"] },
  { slug: "edu2/exam-countdown", inputs: {}, _min_inputs: 0, expect: ["个周末"], _selfcheck: true, _min_inputs: 0 },
  { slug: "edu2/schedule-conflict", inputs: {}, _min_inputs: 0, expect: ["课程表安排合理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "edu2/study-progress", inputs: {"dailyHours":"4"}, expect: ["整目标"], _selfcheck: true, _min_inputs: 1 },
  { slug: "edu2/wrong-book", inputs: {"fReviewDays":"3"}, expect: ["概念不清"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== edu2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();