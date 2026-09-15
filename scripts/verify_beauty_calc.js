#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "beauty/aging-calculator", inputs: {"realAge":"25"}, expect: ["下一题"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/analysis-cost-profit", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/analysis-detector-diagnosis", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/assessor-risk-12", inputs: {}, _min_inputs: 0, expect: ["机构完成"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/bmi-beauty", inputs: {"height":"165","weight":"55","age":"25","waist":"50","hip":"50"}, expect: ["风格"] },
  { slug: "beauty/calc-1", inputs: {}, _min_inputs: 0, expect: ["敏感"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/calc-2", inputs: {}, _min_inputs: 0, expect: ["避免过黄"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/checker-14", inputs: {}, _min_inputs: 0, expect: ["提升计划"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/checker-assessor-1", inputs: {}, _min_inputs: 0, expect: ["闭环"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/checker-assessor-2", inputs: {}, _min_inputs: 0, expect: ["评估"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/face-hair-match", inputs: {}, _min_inputs: 0, expect: ["五官比例和气质也很关"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/hair-color", inputs: {}, _min_inputs: 0, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/hair-dye-ratio", inputs: {"colorAmt":"60"}, expect: ["行操作"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/makeup-shade", inputs: {}, _min_inputs: 0, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/nail-color-harmony", inputs: {}, _min_inputs: 0, expect: ["艺术感十足"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/perming-rod", inputs: {}, _min_inputs: 0, expect: ["发根立体"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/rater-nail", inputs: {}, _min_inputs: 0, expect: ["点缀色不宜过多"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/recommender-cycle", inputs: {"cnt":"5"}, expect: ["避免反吸"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/recommender-face-shape", inputs: {"cnt":"5"}, expect: ["皮造型"], _selfcheck: true, _min_inputs: 1 },
  { slug: "beauty/skin-tewl", inputs: {}, _min_inputs: 0, expect: ["以上"], _selfcheck: true, _min_inputs: 0 },
  { slug: "beauty/skincare-routine", inputs: {}, _min_inputs: 0, expect: ["暂无历史记录"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== beauty calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();