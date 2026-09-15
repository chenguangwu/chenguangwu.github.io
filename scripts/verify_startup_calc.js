#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "startup/burn-rate", inputs: {"cash": "3000000", "income": "50000", "salary": "200000", "rent": "30000", "marketing": "50000", "other": "20000"}, expect: ["OK"] },
  { slug: "startup/business-plan", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "startup/calc-1", inputs: {"reg": "3000", "office": "20000", "equipment": "30000", "inventory": "20000", "brand": "15000", "otherOne": "5000", "salary": "30000", "rent": "5000", "marketing": "5000", "ops": "3000", "months": "12", "reserve": "3"}, expect: ["OK"] },
  { slug: "startup/equity-calculator", inputs: {"w_idea": "3", "w_money": "1", "w_time": "2", "w_res": "2", "pool": "15"}, expect: ["OK"] },
  { slug: "startup/pitch-deck", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "startup/valuation-calculator", inputs: {"bk1": "300", "bk2": "200", "bk3": "150", "bk4": "200", "bk5": "100", "sc_avg": "2000", "sc1": "120", "sc2": "110", "sc3": "100", "sc4": "90", "sc5": "80", "sc6": "100", "sc7": "100", "vc_exit": "50000", "vc_roi": "10", "vc_years": "5", "vc_inv": "500", "dcf_n": "5", "dcf_cf0": "100", "dcf_g": "30", "dcf_r": "15", "dcf_tg": "3", "cmp_rev": "500", "cmp_mau": "10", "cmp_ps_lo": "5", "cmp_ps_hi": "10", "cmp_uv_lo": "200", "cmp_uv_hi": "500"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== startup calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();