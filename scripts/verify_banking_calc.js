#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "banking/amortization-first-interest",
  "inputs": {
    "p": "750000",
    "r": "4.9"
  },
  "expect": [
    "746937.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/apy-calculator",
  "inputs": {
    "r": "3.05",
    "n": "12"
  },
  "expect": [
    "1414.478"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/bond-current-yield",
  "inputs": {
    "c": "75",
    "p": "980"
  },
  "expect": [
    "7.653"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/break-even-savings",
  "inputs": {
    "rd": "5",
    "rl": "5"
  },
  "expect": [
    "50.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/continuous-compounding",
  "inputs": {
    "p": "15000",
    "r": "5",
    "t": "10"
  },
  "expect": [
    "24730.82"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/credit-card-interest-monthly",
  "inputs": {
    "bal": "1500",
    "dr": "0.0005",
    "days": "30"
  },
  "expect": [
    "22.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/daily-interest",
  "inputs": {
    "p": "150000",
    "r": "3.65",
    "d": "100"
  },
  "expect": [
    "151500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/debt-to-income",
  "inputs": {
    "debt": "4500",
    "inc": "10000"
  },
  "expect": [
    "4500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/effective-annual-rate",
  "inputs": {
    "r": "9",
    "n": "12"
  },
  "expect": [
    "0.09381"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/emi-loan",
  "inputs": {
    "p": "750000",
    "r": "4.9",
    "y": "30"
  },
  "expect": [
    "1432962.15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/fd-quarterly",
  "inputs": {
    "p": "150000",
    "r": "3",
    "t": "5"
  },
  "expect": [
    "174177.62"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/fisher-real-rate",
  "inputs": {
    "nom": "9",
    "infl": "2"
  },
  "expect": [
    "6.863"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/future-value-annuity-due",
  "inputs": {
    "PMT": "150",
    "r": "0.005",
    "n": "12"
  },
  "expect": [
    "1859.59"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/growing-annuity-pv",
  "inputs": {
    "C": "150",
    "r": "0.05",
    "g": "0.02",
    "n": "10"
  },
  "expect": [
    "1258.22"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/loan-remaining-balance",
  "inputs": {
    "p": "750000",
    "r": "4.9",
    "y": "30",
    "k": "60"
  },
  "expect": [
    "687732.81"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/loan-tenure",
  "inputs": {
    "P": "15000",
    "r": "0.005",
    "PMT": "200"
  },
  "expect": [
    "15000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/loan-to-value",
  "inputs": {
    "loan": "1200000",
    "val": "1000000"
  },
  "expect": [
    "1200000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/loan-total-interest",
  "inputs": {
    "p": "750000",
    "r": "4.9",
    "y": "30"
  },
  "expect": [
    "682962.15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/net-worth",
  "inputs": {
    "assets": "750000",
    "liab": "200000"
  },
  "expect": [
    "750000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/nominal-from-effective",
  "inputs": {
    "EAR": "3.05116",
    "n": "12"
  },
  "expect": [
    "3.05116"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/perpetuity-pv",
  "inputs": {
    "C": "150",
    "r": "0.05"
  },
  "expect": [
    "3000.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/present-value-annuity-due",
  "inputs": {
    "PMT": "150",
    "r": "0.005",
    "n": "12"
  },
  "expect": [
    "1751.55"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/rd-maturity",
  "inputs": {
    "p": "1500",
    "r": "8",
    "t": "1"
  },
  "expect": [
    "18793.99"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/savings-goal-monthly",
  "inputs": {
    "fv": "300000",
    "r": "4",
    "y": "10"
  },
  "expect": [
    "244482.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "banking/tax-equivalent-yield",
  "inputs": {
    "muni": "3.03",
    "tax": "0.25"
  },
  "expect": [
    "404.000"
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
  console.log("==== banking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
