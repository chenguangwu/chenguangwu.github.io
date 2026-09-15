#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "startup/burn-rate",
  "inputs": {
    "cash": "4500000",
    "income": "50000",
    "salary": "200000",
    "rent": "30000",
    "marketing": "50000",
    "other": "20000"
  },
  "expect": [
    "2028/3/15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/business-plan",
  "inputs": {
    "company": "示例科技有限公司_X",
    "sec_${s.id}": ""
  },
  "expect": [
    "示例科技有限公司_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/calc-1",
  "inputs": {
    "reg": "4500",
    "office": "20000",
    "equipment": "30000",
    "inventory": "20000",
    "brand": "15000",
    "otherOne": "5000",
    "salary": "30000",
    "rent": "5000",
    "marketing": "5000",
    "ops": "3000",
    "months": "12",
    "reserve": "3"
  },
  "expect": [
    "500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/equity-calculator",
  "inputs": {
    "w_idea": "3",
    "w_money": "1",
    "w_time": "2",
    "w_res": "2",
    "pool": "15",
    "mode": "weighted"
  },
  "expect": [
    "weighted"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/pitch-deck",
  "inputs": {
    "company": "示例科技有限公司_X",
    "tagline": "用 AI 重新定义团队协作",
    "slide_${s.id}": ""
  },
  "expect": [
    "示例科技有限公司_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {
    "bk1": "450",
    "bk2": "200",
    "bk3": "150",
    "bk4": "200",
    "bk5": "100",
    "sc_avg": "2000",
    "sc1": "120",
    "sc2": "110",
    "sc3": "100",
    "sc4": "90",
    "sc5": "80",
    "sc6": "100",
    "sc7": "100",
    "vc_exit": "50000",
    "vc_roi": "10",
    "vc_years": "5",
    "vc_inv": "500",
    "dcf_n": "5",
    "dcf_cf0": "100",
    "dcf_g": "30",
    "dcf_r": "15",
    "dcf_tg": "3",
    "cmp_rev": "500",
    "cmp_mau": "10",
    "cmp_ps_lo": "5",
    "cmp_ps_hi": "10",
    "cmp_uv_lo": "200",
    "cmp_uv_hi": "500"
  },
  "expect": [
    "450.00"
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
  console.log("==== startup calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
