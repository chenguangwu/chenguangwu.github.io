#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "12",
      "area": "48"
    },
    "expect": [
      "420.0 kg"
    ],
    "ref": "12群×48亩 混合花源基准35kg（默认10群/50亩为350.0，避开）"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "20"
    },
    "expect": [
      "175.0 kg"
    ],
    "ref": "花源不足按面积折减(20/40=0.5)"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "200"
    },
    "expect": [
      "385.0 kg"
    ],
    "ref": "花源充足(>3倍需求)加成1.1"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "40"
    },
    "clicks": [
      "selectSource('rapeseed');calc();"
    ],
    "expect": [
      "450.0 kg"
    ],
    "ref": "油菜花源基准45kg/群"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "",
      "area": "40"
    },
    "expect": [
      "请输入有效参数"
    ],
    "ref": "蜂箱空值提示"
  },
  {
    "slug": "beekeeping/winter-feed-syrup",
    "inputs": { "n": "5", "vol": "4", "ratio": "2", "price": "5", "daily": "0.5", "days": "10" },
    "expect": ["20.0 L", "17.9 kg", "8.9 kg", "26.8 kg", "89 元", "8.0 天", "3.6 kg"],
    "ref": "越冬糖浆独立复算：总糖浆=5×4=20 L；2:1 糖质量分数=2/3，实测密度 1.34 kg/L ⇒ 总重 26.8 kg、糖 17.9 kg、水 8.9 kg；成本按单价 5 元=89 元；饲喂天数=4/0.5=8.0；每群糖量 3.6 kg。"
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

  console.log("==== beekeeping calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
