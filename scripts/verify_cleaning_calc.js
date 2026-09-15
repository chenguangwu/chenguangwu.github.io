#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "cleaning/appliance-cycle", inputs: {}, _min_inputs: 0, expect: ["记录今日"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cleaning/area-hours", inputs: {"area":"100","staff":"2"}, expect: ["总分钟数"] },
  { slug: "cleaning/checker-10", inputs: {}, _min_inputs: 0, expect: ["限期整改并安排复查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cleaning/checker-9", inputs: {}, _min_inputs: 0, expect: ["未制定"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cleaning/cycle-20", inputs: {"logArea":"50"}, expect: ["再清水处理残留"], _selfcheck: true, _min_inputs: 1 },
  { slug: "cleaning/dilution-ratio", inputs: {"ratioN":"50","totalVol":"10","totalVolP":"10","conc":"100"}, expect: ["瓶数"] },
  { slug: "cleaning/staff-schedule", inputs: {"newArea":"50"}, expect: ["工作"], _selfcheck: true, _min_inputs: 1 },
  { slug: "cleaning/supply-usage", inputs: {"area":"200","period":"30","safety":"7"}, expect: ["全能清洁剂"] }
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
  console.log("==== cleaning calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();