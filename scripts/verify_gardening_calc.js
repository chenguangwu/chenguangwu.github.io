#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "gardening/balcony-sunlight", inputs: {}, _min_inputs: 0, expect: ["结果供选花参考"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/compost-calculator", inputs: {}, _min_inputs: 0, expect: ["暂无保存的配方"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/garden-calendar", inputs: {}, _min_inputs: 0, expect: ["磷钾肥作基肥"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/garden-layout", inputs: {"area":"20"}, expect: ["下载方案"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gardening/garden-tools", inputs: {}, _min_inputs: 0, expect: ["请调整筛选条件"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/pest-identifier", inputs: {}, _min_inputs: 0, expect: ["请调整筛选条件"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/plant-calendar", inputs: {}, _min_inputs: 0, expect: ["根茎"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/plant-care", inputs: {}, _min_inputs: 0, expect: ["请调整筛选条件"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening/pot-capacity", inputs: {"${f.id}":"${f.value}"}, expect: ["请输入有效的尺寸数值"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gardening/recommender", inputs: {"cnt":"5"}, expect: ["浇则浇透"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gardening/soil-ph", inputs: {"soilPh":"6.5"}, expect: ["可用雨水或晾晒水"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gardening/watering-schedule", inputs: {"potSize":"20"}, expect: ["暂无保存的浇水计划"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== gardening calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();