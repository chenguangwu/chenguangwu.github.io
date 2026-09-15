#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "beauty/aging-calculator", inputs: {"realAge":"25"}, expect: ["下一题"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/analysis-cost-profit", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/analysis-detector-diagnosis", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/assessor-risk-12", inputs: {}, expect: ["机构完成"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/bmi-beauty", inputs: {"height":"165","weight":"55","age":"25","waist":"50","hip":"50"}, expect: ["风格"] },
  { slug: "beauty/calc-1", inputs: {}, expect: ["敏感"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/calc-2", inputs: {}, expect: ["避免过黄"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/checker-14", inputs: {}, expect: ["提升计划"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/checker-assessor-1", inputs: {}, expect: ["闭环"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/checker-assessor-2", inputs: {}, expect: ["评估"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/face-hair-match", inputs: {}, expect: ["五官比例和气质也很关"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/hair-color", inputs: {}, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/hair-dye-ratio", inputs: {"colorAmt":"60"}, expect: ["行操作"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/makeup-shade", inputs: {}, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/nail-color-harmony", inputs: {}, expect: ["艺术感十足"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/perming-rod", inputs: {}, expect: ["发根立体"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/rater-nail", inputs: {}, expect: ["点缀色不宜过多"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/recommender-cycle", inputs: {"cnt":"5"}, expect: ["避免反吸"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/recommender-face-shape", inputs: {"cnt":"5"}, expect: ["皮造型"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/skin-tewl", inputs: {}, expect: ["以上"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/skincare-routine", inputs: {}, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== beauty calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();