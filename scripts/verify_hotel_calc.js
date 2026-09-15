#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "hotel/assessor-62", inputs: {}, _min_inputs: 0, expect: ["推荐加盟"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hotel/checker-assessor", inputs: {}, _min_inputs: 0, expect: ["可作为标杆推广"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hotel/currency-exchange", inputs: {"rate":"0.138","fee":"0","amount":"10000"}, expect: ["手续费"] },
  { slug: "hotel/itinerary-planner", inputs: {"totalDays":"5","hoursPerDay":"8","spotCount":"6","avgHours":"3","pri${i}":"${Math.min(5, Math.max(1, 6 - i))}"}, expect: ["行程节奏合理"] },
  { slug: "hotel/luggage-weight", inputs: {"days":"7"}, expect: ["避免携带过多衣物"], _selfcheck: true, _min_inputs: 1 },
  { slug: "hotel/occupancy-revpar", inputs: {"totalRooms":"120","soldRooms":"96","revenue":"38400","days":"1"}, expect: ["出租率"] },
  { slug: "hotel/tip-calculator", inputs: {"bill":"120","tipPct":"15","people":"2","tax":"0"}, expect: ["未计算小费"] }
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
  console.log("==== hotel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();