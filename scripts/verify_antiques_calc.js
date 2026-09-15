#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "antiques/bronze-identification", inputs: {}, _min_inputs: 0, expect: ["表门类"], _selfcheck: true, _min_inputs: 0 },
  { slug: "antiques/calligraphy-style", inputs: {}, _min_inputs: 0, expect: ["吴昌硕融石鼓文入画"], _selfcheck: true, _min_inputs: 0 },
  { slug: "antiques/furniture-style", inputs: {}, _min_inputs: 0, expect: ["工艺最高但创新少"], _selfcheck: true, _min_inputs: 0 },
  { slug: "antiques/porcelain-date", inputs: {}, _min_inputs: 0, expect: ["雍正单色釉为历代最佳"], _selfcheck: true, _min_inputs: 0 },
  { slug: "antiques/seal-identification", inputs: {}, _min_inputs: 0, expect: ["计白当朱"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== antiques calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();