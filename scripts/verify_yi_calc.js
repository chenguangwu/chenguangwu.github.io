#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "yi/64-gua",
  "inputs": {},
  "expect": [
    "第10卦"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "yi/bagua-viewer",
  "inputs": {},
  "expect": [
    "乾卦"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "yi/yi-yao",
  "inputs": {},
  "expect": [
    "(第1卦)"
  ],
  "ref": "auto-restore(default)"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== yi calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
