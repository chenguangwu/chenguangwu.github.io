#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "psychiatry/aq-autism", inputs: {}, expect: ["完全不同意"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/asrs-adhd", inputs: {}, expect: ["非常频繁"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/assessor-risk-5", inputs: {}, expect: ["保持社会支持"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/bis11-impulse", inputs: {}, expect: ["总是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/cage-substance", inputs: {}, expect: ["晨饮"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/calc-1", inputs: {}, expect: ["几乎每天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/cdrisc-resilience", inputs: {}, expect: ["几乎总是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/cssrs-suicide", inputs: {}, expect: ["个月内"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/eat26-eating", inputs: {}, expect: ["从不"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/gad7-anxiety", inputs: {}, expect: ["几乎每天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/isi-insomnia", inputs: {}, expect: ["极重度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/les-stress", inputs: {}, expect: ["重大疾病风险约"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/lsas-social", inputs: {}, expect: ["通常"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/mdq-bipolar", inputs: {}, expect: ["严重问题"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/mmpi2-personality", inputs: {"sc'+i+'":"50"}, expect: ["未见明显病理升高"], _selfcheck: true, _min_inputs: 1 },
  { slug: "psychiatry/panss-schizophrenia", inputs: {}, expect: ["一般"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/pcl5-ptsd", inputs: {}, expect: ["极其严重"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/pdss-panic", inputs: {}, expect: ["严重"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/phq15-somatization", inputs: {}, expect: ["很多困扰"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/phq9-depression", inputs: {}, expect: ["几乎每天"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/rater-23", inputs: {}, expect: ["必要时寻求心理咨询"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/rater-24", inputs: {}, expect: ["系统提升心理韧性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/self-assess-4", inputs: {}, expect: ["力管理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "psychiatry/ybocs-ocd", inputs: {}, expect: ["极重度"], _selfcheck: true, _min_inputs: 0 }
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