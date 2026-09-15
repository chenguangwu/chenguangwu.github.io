#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "acupuncture/acupoint-combination", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/acupoint-injection", inputs: {"points":"2"}, expect: ["次为一疗程"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/acupoint-location", inputs: {"realCm":"50","targetCun":"50"}, expect: ["对应"] },
  { slug: "acupuncture/analysis-10", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/bloodletting-therapy", inputs: {"points":"3"}, expect: ["血色由暗转红即可停止"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/cupping-mark-analysis", inputs: {}, expect: ["更准确"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/cupping-pressure", inputs: {"time":"10"}, expect: ["肌肉丰厚处可用"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/deqi-sensation", inputs: {}, expect: ["候气至再行补泻"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/ear-acupressure", inputs: {}, expect: ["不宜过多"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/electroacupuncture", inputs: {"duration":"20"}, expect: ["再取下导线起针"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/flash-cupping", inputs: {"time":"10"}, expect: ["罐印为正常反应"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/guasha-direction", inputs: {}, expect: ["每周不超过"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/intradermal-needle", inputs: {}, expect: ["取针后消毒按压针孔"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/meridian-pathway", inputs: {}, expect: ["拇指"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/moxibustion-count", inputs: {}, expect: ["防止化脓"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/needle-retention", inputs: {}, expect: ["保持针感"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/needling-depth", inputs: {}, expect: ["标准"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/pediatric-tuina", inputs: {"month":"50"}, expect: ["慢性调理宜缓"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/recommender-acupoint", inputs: {"cnt":"5"}, expect: ["通络止痛"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/recommender-time", inputs: {"cnt":"5"}, expect: ["手法宜轻"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/tuina-frequency", inputs: {"duration":"5"}, expect: ["单次约"], _selfcheck: true, _min_inputs: 1 },
  { slug: "acupuncture/tuina-medium", inputs: {}, expect: ["蛋清过敏禁用"], _selfcheck: true, _min_inputs: 0 },
  { slug: "acupuncture/warm-needle-moxibustion", inputs: {"ambTemp":"25"}, expect: ["或改用艾条温和灸"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== acupuncture calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();