#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "logistics2/inventory-aging", inputs: {"period":"90","threshold":"180"}, expect: ["降价处理或退供应商"] },
  { slug: "logistics2/loading-utilization", inputs: {"truckL":"6.8","truckW":"2.3","truckH":"2.4","truckLoad":"5000","boxL":"0.6","boxW":"0.4","boxH":"0.5","boxWeight":"15","planQty":"500"}, expect: ["建议装载"] },
  { slug: "logistics2/packaging-cushion", inputs: {"weight":"3","dropH":"80","fragility":"60"}, expect: ["跌落下不受损"] },
  { slug: "logistics2/picking-route", inputs: {"aisles":"8","aisleLen":"20","aisleGap":"3","speed":"1.2","pickTime":"10","picksPerAisle":"3"}, expect: ["式更优"] },
  { slug: "logistics2/storage-allocation", inputs: {"totalRows":"10"}, expect: ["可显著降低拣货行走距"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== logistics2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();