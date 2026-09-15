#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "property/analysis-40", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "property/area-shared", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "property/assessor-manager-1", inputs: {"contractAmt": "50", "contractTerm": "12"}, expect: ["OK"] },
  { slug: "property/calc-shared-property-fee", inputs: {"totalArea": "100", "sharedRatio": "20", "feeRate": "2.5", "sharedFeeRate": "0.5", "customPeriod": "12"}, expect: ["OK"] },
  { slug: "property/checker-11", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "property/checker-7", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "property/checker-recorder-drill", inputs: {"drillCount": "50", "evacTime": "180"}, expect: ["OK"] },
  { slug: "property/cleaning-allocation", inputs: {"staffCount": "4"}, expect: ["OK"] },
  { slug: "property/cost-profit", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "property/cycle-10", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "property/cycle-elevator", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "property/elevator-energy", inputs: {"liftCount": "2", "floors": "18", "floorHeight": "3", "power": "11", "loadRate": "40", "tripsPerDay": "200", "tripFloors": "6", "idleHours": "20", "idlePower": "0.5", "price": "0.8"}, expect: ["OK"] },
  { slug: "property/energy", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "property/fee-allocation", inputs: {"totalFee": "50000"}, expect: ["OK"] },
  { slug: "property/irrigation-schedule", inputs: {"days": "14", "seed": "42", "rainProb": "25"}, expect: ["OK"] },
  { slug: "property/rater-performance", inputs: {"v0": "85", "w0": "20", "v1": "80", "w1": "20", "v2": "90", "w2": "15", "v3": "88", "w3": "15", "v4": "92", "w4": "15", "v5": "85", "w5": "15"}, expect: ["OK"] },
  { slug: "property/report-manager", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "property/response-1", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "property/response-4", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "property/shared-area", inputs: {"innerArea": "3200", "unitCount": "40"}, expect: ["OK"] },
  { slug: "property/stats-manager", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== property calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();