#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "psychiatry/aq-autism",
  "inputs": {},
  "expect": [
    "0/50"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/asrs-adhd",
  "inputs": {},
  "expect": [
    "0/6"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/assessor-risk-5",
  "inputs": {},
  "expect": [
    "近3月"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/bis11-impulse",
  "inputs": {},
  "expect": [
    "0/30"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/cage-substance",
  "inputs": {},
  "expect": [
    "0/4"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/calc-1",
  "inputs": {},
  "expect": [
    "0-27"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/cdrisc-resilience",
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/cssrs-suicide",
  "inputs": {},
  "expect": [
    "最近一次实际尝试是否在过去3个月内"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/eat26-eating",
  "inputs": {},
  "expect": [
    "0/26"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/gad7-anxiety",
  "inputs": {},
  "expect": [
    "0/7"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/isi-insomnia",
  "inputs": {},
  "expect": [
    "0/7"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/les-stress",
  "inputs": {},
  "expect": [
    "重大疾病风险约30%"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/lsas-social",
  "inputs": {},
  "expect": [
    "0/48"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/mdq-bipolar",
  "inputs": {},
  "expect": [
    "第一部分0/13"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/mmpi2-personality",
  "inputs": {
    "sc'+i+'": "75"
  },
  "expect": [
    "75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychiatry/panss-schizophrenia",
  "inputs": {},
  "expect": [
    "0/30"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/pcl5-ptsd",
  "inputs": {},
  "expect": [
    "0/20"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/pdss-panic",
  "inputs": {},
  "expect": [
    "2-3次"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/phq15-somatization",
  "inputs": {},
  "expect": [
    "0/15"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/phq9-depression",
  "inputs": {},
  "expect": [
    "0/9"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/rater-23",
  "inputs": {},
  "expect": [
    "0-144"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/rater-24",
  "inputs": {},
  "expect": [
    "0.00/4.0"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychiatry/self-assess-4",
  "inputs": {
    "q'+i+'": "'+opt.v+'"
  },
  "expect": [
    "+opt.v+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychiatry/ybocs-ocd",
  "inputs": {},
  "expect": [
    "0/10"
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
  console.log("==== psychiatry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
