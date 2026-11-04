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
    "45.0 债务收入比 DTI (%)"
  ],
  "ref": "独立复算：月债务 4500 / 月收入 10000 = 45.0% ⇒ DTI=45.0。⚠ 原 expect '4500' 是注入值回显（blob 含所有 el.value），零判别力，已改为计算结果串。默认态 0/0 ⇒ 0.0，不含该串 ⇒ 无逃生。"
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
    "94.2 还款期数 n (期)"
  ],
  "ref": "独立复算：n = −ln(1 − P·r/PMT)/ln(1+r) = −ln(1 − 75/200)/ln(1.005) = 0.4700/0.0049875 ≈ 94.2 期。⚠ 原 expect '15000' 为本金输入回显（零判别力），已改为期数结果串；默认态参数不同 ⇒ 不命中。"
},
{
  "slug": "banking/loan-to-value",
  "inputs": {
    "loan": "1200000",
    "val": "1000000"
  },
  "expect": [
    "120.0 贷款价值比 LTV (%)",
    "⚠ 贷款额高于抵押物价值，LTV 已超过 100%"
  ],
  "ref": "独立复算：贷款 1,200,000 / 抵押物价值 1,000,000 = 120.0% ⇒ LTV=120.0。⚠ 原 expect '1200000' 为输入值回显（零判别力），已改为计算结果串；默认态 0 ⇒ 0.0，不命中。F-N16：贷款高于价值须额外警示。"
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
    "550000 净资产 NW (元)"
  ],
  "ref": "独立复算：资产 750,000 − 负债 200,000 = 550,000。⚠ 原 expect '750000' 为输入值回显（零判别力），已改为净资产结果串；默认态 0 ⇒ ‘0 净资产 NW (元)’，不命中。"
},
{
  "slug": "banking/nominal-from-effective",
  "inputs": {
    "EAR": "3.05116",
    "n": "12"
  },
  "expect": [
    "148.382 名义年利率 r (%)"
  ],
  "ref": "独立复算：r = n[(1+EAR)^(1/n) − 1] = 12[(4.05116)^(1/12) − 1] = 12×0.12365 = 148.382%。⚠ 原 expect '3.05116' 为 EAR 输入回显（零判别力），已改为名义利率结果串；默认态不命中。"
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
},
{
  "slug": "banking/apy-calculator",
  "inputs": {
    "r": "0.05",
    "n": "0"
  },
  "expect": [
    "⚠ 年复利次数 n 必须为正整数（如 12 表示每月复利）。"
  ],
  "ref": "F-N14：n=0 时 (1+r/n)^n 产生 Infinity 伪结果，必须拒绝并提示 n 为正整数。默认 n=12 ⇒ 不命中。"
},
{
  "slug": "banking/apy-calculator",
  "inputs": {
    "r": "-12",
    "n": "12"
  },
  "expect": [
    "⚠ 名义年利率 r 必须大于 −1（即 −100%）；r 按小数口径填写（0.05 = 5%）。"
  ],
  "ref": "F-N14：r=-12 小于 -1 会使 1+r/n 为负，n 为偶数时 pow 产生伪正数，必须拒绝。默认 r=0.05 ⇒ 不命中。"
},
{
  "slug": "banking/apy-calculator",
  "inputs": {
    "r": "5",
    "n": "12"
  },
  "expect": [
    "⚠ 当前 r=5 按小数口径识别为 500.00%；若想表达 5%，请填写 0.05（即 0.05）。"
  ],
  "ref": "F-N14：r=5 是百分数口径误填（页面按小数读取即 500%），须提示改填 0.05。默认 r=0.05 ⇒ 不命中。"
},
{
  "slug": "banking/loan-to-value",
  "inputs": {
    "loan": "-100000",
    "val": "1000000"
  },
  "expect": [
    "⚠ 贷款额与抵押物价值均须大于 0，请输入正数后再计算。"
  ],
  "ref": "F-N16：负贷款旧代码被接受并算出 -10.0% LTV 与 110% 首付，必须拒绝。默认 loan=800000、val=1000000 ⇒ 不命中。"
},
{
  "slug": "banking/amortization-first-interest",
  "inputs": { "p": "", "r": "" },
  "expect": ["请填写「贷款本金 P」后再计算。"],
  "ref": "空态守卫（TOOLBOX-REQ-GUARD）：清空 p/r 后必须提示，不得渲染 0.00 结构化零值。"
},
{
  "slug": "banking/amortization-first-interest",
  "inputs": { "p": "500000", "r": "0" },
  "expect": ["0.00 首月利息 I₁ 500000.00 首月还本金"],
  "ref": "合法 0 边界：r=0（零利率）必须正常计算（I₁=500000×0=0，首月还本金=500000），不得被守卫拦掉。"
},
{
  "slug": "banking/continuous-compounding",
  "inputs": { "p": "", "r": "", "t": "" },
  "expect": ["请填写「本金 P」后再计算。"],
  "ref": "空态守卫：清空 p/r/t 后必须提示，不得渲染 0.00 结构化零值。"
},
{
  "slug": "banking/effective-annual-rate",
  "inputs": { "r": "", "n": "" },
  "expect": ["请填写「名义年利率 r」后再计算。"],
  "ref": "空态守卫：清空 r/n 后必须提示，不得渲染 0.000 结构化零值。"
},
{
  "slug": "banking/net-worth",
  "inputs": { "assets": "", "liab": "" },
  "expect": ["请填写「总资产」后再计算。"],
  "ref": "空态守卫：清空 assets/liab 后必须提示，不得渲染 0 净资产结构化零值。"
},
{
  "slug": "banking/net-worth",
  "inputs": { "assets": "500000", "liab": "0" },
  "expect": ["500000 净资产 NW (元) 0.00 负债率 (%)"],
  "ref": "合法 0 边界：liab=0（无负债）必须正常计算，不得被守卫拦掉。"
},
{
  "slug": "banking/tax-equivalent-yield",
  "inputs": { "muni": "", "tax": "" },
  "expect": ["请填写「免税收益率」后再计算。"],
  "ref": "空态守卫：清空 muni/tax 后必须提示，不得渲染 0.000 结构化零值。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== banking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
