#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "misc/complex-number",
  "inputs": {
    "aRe": "6",
    "aIm": "4",
    "bRe": "1",
    "bIm": "-2"
  },
  "expect": [
    "(33.690068°)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc/function-plotter",
  "inputs": {
    "xMin": "-15",
    "xMax": "10",
    "yMin": "-10",
    "yMax": "10",
    "p_a": "1",
    "p_b": "10",
    "p_c": "-4",
    "p_w": "1",
    "p_phi": "0",
    "p_expr": "sin(x)*2"
  },
  "expect": [
    "-15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc/magic-square",
  "inputs": {
    "order": "8"
  },
  "expect": [
    "369"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc/physics-constants",
  "inputs": {},
  "expect": [
    "原子物理"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "misc/scientific-notation",
  "inputs": {
    "rawInput": "602214076000000000000000",
    "mantissaInput": "6.022",
    "expInput": "35"
  },
  "expect": [
    "6.022e+35"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc/statistics-distribution",
  "inputs": {
    "mu": "0",
    "sigma": "1",
    "xval": "1",
    "aVal": "6",
    "bVal": "7",
    "lambda": "3",
    "kval": "5",
    "nval": "10",
    "pval": "0.5"
  },
  "expect": [
    "0.322266"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc/truth-table",
  "inputs": {
    "exprInput": "A and (B or not C)_X"
  },
  "expect": [
    "无法识别字符"
  ],
  "ref": "auto-restore"
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
  console.log("==== misc calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
