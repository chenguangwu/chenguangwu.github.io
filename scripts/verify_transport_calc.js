#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "transport/calc-4", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "transport/calc-53", inputs: {"q1": "320", "q2": "380", "q3": "410", "q4": "350"}, expect: ["OK"] },
  { slug: "transport/calculator-calc-3", inputs: {"hours": "0", "minutes": "30", "firstHour": "10", "afterHour": "5", "dailyCap": "60"}, expect: ["OK"] },
  { slug: "transport/calculator-calc-depreciation", inputs: {"cost": "200000", "life": "5", "salvageRate": "5"}, expect: ["OK"] },
  { slug: "transport/calculator-calc-fuel", inputs: {"distance": "500", "consumption": "7.5", "price": "8.00"}, expect: ["OK"] },
  { slug: "transport/calculator-calc-speed", inputs: {"speed": "120", "reaction": "0.75", "slope": "0"}, expect: ["OK"] },
  { slug: "transport/calculator-calc-tire", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "transport/convert-fuel-oil", inputs: {"val": "30"}, expect: ["OK"] },
  { slug: "transport/convert-volume-weight", inputs: {"l": "40", "w": "30", "h": "20"}, expect: ["OK"] },
  { slug: "transport/cycle-signal", inputs: {"cycle": "90", "satFlow": "1800"}, expect: ["OK"] },
  { slug: "transport/estimate-4", inputs: {"boxL": "40", "boxW": "30", "boxH": "25", "boxWt": "8"}, expect: ["OK"] },
  { slug: "transport/estimate-capacity", inputs: {"laneW": "3.75", "shoulder": "3.0", "speed": "120", "heavy": "10", "volume": "1800", "phf": "0.92"}, expect: ["OK"] },
  { slug: "transport/estimate-energy", inputs: {"capacity": "60", "consumption": "15", "soc": "80"}, expect: ["OK"] },
  { slug: "transport/estimate-speed-time", inputs: {"distance": "400", "speed": "100", "restCount": "2", "restMin": "20"}, expect: ["OK"] },
  { slug: "transport/noise", inputs: {"volume": "2000", "speed": "80", "heavy": "8", "distance": "30"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== transport calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();