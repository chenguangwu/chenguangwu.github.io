#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "psychiatry/aq-autism", inputs: {}, _min_inputs: 0, expect: ["完全不同意"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/asrs-adhd", inputs: {}, _min_inputs: 0, expect: ["非常频繁"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/assessor-risk-5", inputs: {}, _min_inputs: 0, expect: ["保持社会支持"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/bis11-impulse", inputs: {}, _min_inputs: 0, expect: ["总是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/cage-substance", inputs: {}, _min_inputs: 0, expect: ["晨饮"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/calc-1", inputs: {}, _min_inputs: 0, expect: ["几乎每天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/cdrisc-resilience", inputs: {}, _min_inputs: 0, expect: ["几乎总是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/cssrs-suicide", inputs: {}, _min_inputs: 0, expect: ["个月内"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/eat26-eating", inputs: {}, _min_inputs: 0, expect: ["从不"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/gad7-anxiety", inputs: {}, _min_inputs: 0, expect: ["几乎每天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/isi-insomnia", inputs: {}, _min_inputs: 0, expect: ["极重度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/les-stress", inputs: {}, _min_inputs: 0, expect: ["重大疾病风险约"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/lsas-social", inputs: {}, _min_inputs: 0, expect: ["通常"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/mdq-bipolar", inputs: {}, _min_inputs: 0, expect: ["严重问题"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/mmpi2-personality", inputs: {"sc'+i+'":"50"}, expect: ["未见明显病理升高"], _selfcheck: true, _min_inputs: 1 },
  { slug: "psychiatry/panss-schizophrenia", inputs: {}, _min_inputs: 0, expect: ["一般"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/pcl5-ptsd", inputs: {}, _min_inputs: 0, expect: ["极其严重"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/pdss-panic", inputs: {}, _min_inputs: 0, expect: ["严重"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/phq15-somatization", inputs: {}, _min_inputs: 0, expect: ["很多困扰"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/phq9-depression", inputs: {}, _min_inputs: 0, expect: ["几乎每天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/rater-23", inputs: {}, _min_inputs: 0, expect: ["必要时寻求心理咨询"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/rater-24", inputs: {}, _min_inputs: 0, expect: ["系统提升心理韧性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/self-assess-4", inputs: {}, _min_inputs: 0, expect: ["力管理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/ybocs-ocd", inputs: {}, _min_inputs: 0, expect: ["极重度"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== psychiatry calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();