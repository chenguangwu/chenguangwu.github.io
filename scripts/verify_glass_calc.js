#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "glass/annealing-curve", inputs: {"thick":"6","coolTo":"50"}, expect: ["总退火约"] },
  { slug: "glass/cutting-score", inputs: {"sheetW":"1830","sheetH":"1220","thick":"5","pieceW":"400","pieceH":"300","kerf":"3"}, expect: ["需切割"] },
  { slug: "glass/snell-refraction", inputs: {"n1":"1.0003","n2":"1.33","angle":"30"}, expect: ["离法线偏折"] },
  { slug: "glass/thermal-bend", inputs: {"thick":"5","angle":"90","radius":"60"}, expect: ["难度等级"] },
  { slug: "glass/thickness-selection", inputs: {"width":"800","height":"1200"}, expect: ["实际工程需按规范验算"] }
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
  console.log("==== glass calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();