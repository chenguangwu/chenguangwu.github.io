#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "maritime/anchorage-capacity", inputs: {"shipLength":"200","waterDepth":"20","scopeFactor":"5","safetyMargin":"50","anchorageArea":"5"}, expect: ["出链长度合理"] },
  { slug: "maritime/compass-correction", inputs: {"variation":"-5","deviation":"3","headingInput":"045"}, expect: ["罗航向"] },
  { slug: "maritime/speed-distance", inputs: {"speedValue":"15","timeValue":"12","distValue":"333"}, expect: ["小时"] },
  { slug: "maritime/stowage-factor", inputs: {"volume":"100","weight":"60","sfInput":"1.5","totalWeight":"5000","holdCapacity":"9000","dwt":"7000"}, expect: ["舱容受限"] },
  { slug: "maritime/tide-window", inputs: {"highTideHeight":"4.5","lowTideHeight":"0.8","nextLowTideHeight":"1.0","chartDepth":"3.0","draft":"5.0","ukc":"0.5","transitTime":"60"}, expect: ["分钟"] }
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
  console.log("==== maritime calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();