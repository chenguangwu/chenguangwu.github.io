#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "bridge/deflection-calc", inputs: {"inL":"20","inE":"32.5","inI":"0.15","inQ":"30","inP":"200"}, expect: ["满足要求"] },
  { slug: "bridge/foundation-calc", inputs: {"inD":"1.2","inL":"25","inQp":"1200","inQs1":"45","inL1":"10","inQs2":"60","inL2":"10","inQs3":"80","inN":"12000"}, expect: ["单桩承担"] },
  { slug: "bridge/load-calc", inputs: {"inL":"30","inB":"12","inG":"120","inLane":"3","inQp":"3.0","inBw":"2"}, expect: ["活载"] },
  { slug: "bridge/material-qty", inputs: {"inL":"30","inNbeam":"6","inArea":"1.2","inB":"12","inT":"0.15","inSpan":"5","inRatio":"120","inPc":"600","inPs":"4500"}, expect: ["万元"] },
  { slug: "bridge/span-calc", inputs: {"inLt":"300","inN":"5","inG":"150","inQ":"60"}, expect: ["单孔总荷载"] }
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
  console.log("==== bridge calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();