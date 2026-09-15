#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "medical/assessor-risk-3",
  "inputs": {
    "ph": "9",
    "water": "1500",
    "protein": "1.2",
    "sodium": "3000",
    "oxalate": "150"
  },
  "expect": [
    "4/20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calc-34",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30"
  },
  "expect": [
    "1898"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "weight": "30",
    "age": ""
  },
  "expect": [
    "300.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-due-date",
  "inputs": {
    "cycle": "42"
  },
  "expect": [
    "42"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "750",
    "dur": "4",
    "conc": "0.4",
    "w": "60"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "2.0",
    "meld_cr": "1.0",
    "meld_inr": "1.2",
    "meld_na": "140",
    "gcs_e": "3"
  },
  "expect": [
    "E3+V5+M6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "1",
    "from": "18"
  },
  "expect": [
    "18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/dosage-calculator",
  "inputs": {
    "weight": "90",
    "height": "170",
    "age": "30",
    "perDose": "10"
  },
  "expect": [
    "900.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/drug-info",
  "inputs": {},
  "expect": [
    "100-200mg/次"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "medical/estimate-metabolism",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30",
    "bf": ""
  },
  "expect": [
    "+149.3%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/medical-calculator",
  "inputs": {
    "dose_weight": "90",
    "dose_per_kg": "10",
    "dose_freq": "3",
    "iv_volume": "500",
    "iv_time": "120",
    "glucose_mmol": "5.6",
    "glucose_mg": "100.9",
    "temp_value": "36.5",
    "bp_sbp": "120",
    "bp_dbp": "80",
    "timer_custom_min": ""
  },
  "expect": [
    "900.0mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/reminder-2",
  "inputs": {},
  "expect": [
    "暂无药品记录"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "medical/stats-4",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
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
  console.log("==== medical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
