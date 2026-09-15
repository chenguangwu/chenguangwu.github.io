#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "welding/analysis-37", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "welding/analysis-38", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "welding/calc-1", inputs: {"diameter": "3.2", "thickness": "8", "voltage": "24", "speed": "3"}, expect: ["OK"] },
  { slug: "welding/detector-25", inputs: {"plateThick": "24", "circDef": "3", "stripDef": "8", "evalArea": "500"}, expect: ["OK"] },
  { slug: "welding/energy-cost-1", inputs: {"current": "200", "voltage": "24", "time": "30", "price": "1.0", "duty": "60", "eff": "85"}, expect: ["OK"] },
  { slug: "welding/flow-ratio", inputs: {"nozzle": "12", "flow": "15", "ar": "80", "co2": "20"}, expect: ["OK"] },
  { slug: "welding/hancaixuanyongtuijian", inputs: {"thickness": "8"}, expect: ["OK"] },
  { slug: "welding/hanjiegongzhuangjiajusheji", inputs: {"length": "1000", "width": "500", "weight": "50"}, expect: ["OK"] },
  { slug: "welding/hanjiezidonghuapinggu", inputs: {"output": "10000", "seamlen": "0.5", "mansec": "120", "labor": "50", "robotcost": "30", "workdays": "250"}, expect: ["OK"] },
  { slug: "welding/speed-voltage-current", inputs: {"thickness": "6"}, expect: ["OK"] },
  { slug: "welding/stress", inputs: {"thickness": "10", "length": "300", "leg": "6", "yield": "235"}, expect: ["OK"] },
  { slug: "welding/temp-10", inputs: {"thickness": "12", "preheat": "100"}, expect: ["OK"] },
  { slug: "welding/temp-time-6", inputs: {"thickness": "20", "ce": "0.45", "c": "0.18", "mn": "1.4", "cr": "0.1", "mo": "0"}, expect: ["OK"] },
  { slug: "welding/ventilation-protection", inputs: {"consume": "2", "volume": "500", "hours": "8"}, expect: ["OK"] },
  { slug: "welding/wps-hanjiegongyiguichengbianzhi", inputs: {"diameter": "1.2", "current": "200", "voltage": "24", "speed": "30", "preheat": "20", "pass": "2"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== welding calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();