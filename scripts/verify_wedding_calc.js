#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "wedding/countdown-timeline",
  "inputs": {
    "weddingTime": "10:00_X"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/detector-2",
  "inputs": {
    "c1": "#e8638f_X",
    "c2": "#7c3aed"
  },
  "expect": [
    "e8638f_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/detector-33",
  "inputs": {
    "prof": "12",
    "punctual": "9",
    "creative": "7",
    "comm": "8",
    "contract": "95"
  },
  "expect": [
    "12/10(30%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/material-checklist",
  "inputs": {},
  "expect": [
    "200"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "wedding/seating-chart",
  "inputs": {
    "perTable": "15",
    "mainTable": "8"
  },
  "expect": [
    "15人"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/wedding-budget-planner",
  "inputs": {
    "totalBudget": "150000",
    "spent": "0",
    "cat-'+i+'": "'+amount+'"
  },
  "expect": [
    "150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/wedding-car-route",
  "inputs": {
    "departTime": "07:00_X",
    "carCount": "6"
  },
  "expect": [
    "00_X"
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
  console.log("==== wedding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
