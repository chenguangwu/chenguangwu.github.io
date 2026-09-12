#!/usr/bin/env node
/**
 * sports 分类关键计算逻辑独立验证（§4.1.1 收口批次 C）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 用例以运动科学 / 体能计算的确定公式为主，期望值一律由标准公式独立复算得出。
 *
 * 用法：
 *   node scripts/verify_sports_calc.js
 *   node scripts/verify_sports_calc.js tester-1 estimate-tester
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 力量 / 1RM ──────────────────────────────────────────────
  {
    slug: "sports/tester-1",
    inputs: { bw: "70", reps: "10", move: "pullup", added: "0" }, // pullup → load = 体重 + 附加负重(0) = 70
    expect: ["93.3", "1.33"],
    ref: "Epley = 70×(1+10/30)=93.3 kg；相对力量 = 93.3/70 = 1.33（页面 toFixed(1)/toFixed(2)）",
  },

  // ── 最大摄氧量 ──────────────────────────────────────────────
  {
    slug: "sports/estimate-tester",
    inputs: { method: "0", distance: "2400" }, // method 0 = Cooper 12 分钟跑
    expect: ["42.4"],
    ref: "Cooper：VO2max = (2400−504.9)/44.73 = 42.36 → 42.4 ml/kg/min（页面 round·10/10）",
  },

  // ── 心率储备（Karvonen）────────────────────────────────────
  {
    slug: "sports/calc-heart-rate-1",
    inputs: { age: "30", restHr: "60", formula: "fox" }, // fox: 220−age
    expect: ["190"],
    ref: "最大心率 = 220−30 = 190 bpm（页面 Math.round(mx)，summary 显示）",
  },

  // ── 氧脉搏 ──────────────────────────────────────────────────
  {
    slug: "sports/yangmaiboxiaolv",
    inputs: { vo2: "3200", hr: "180" }, // phase 默认 '' → a-vO2diff 0.05
    expect: ["17.78"],
    ref: "氧脉搏 O₂pulse = VO₂/HR = 3200/180 = 17.78 ml/beat（页面 toFixed(2)）",
  },

  // ── 骑行齿比 ────────────────────────────────────────────────
  {
    slug: "sports/calculator-calc-9",
    inputs: { chainring: "50", cog: "11", circ: "2.105", cadence: "90", targetSpeed: "30" },
    expect: ["4.55"],
    ref: "齿比 = 50/11 = 4.545 → 4.55（页面 toFixed(2)，summary 齿比卡片）",
  },

  // ── 坡度百分比 ──────────────────────────────────────────────
  {
    slug: "sports/calc-angle-slope",
    inputs: { v1: "100", v2: "20" }, // m 默认 'part'（求部分值）
    expect: ["20.00"],
    ref: "20% of 100 = 100×20/100 = 20.00（页面 toFixed(2)）",
  },

  // ── 游泳 SWOLF ──────────────────────────────────────────────
  {
    slug: "sports/swimming-stroke-efficiency",
    inputs: { "pool-length": "", strokeCount: "20", swimTime: "30", strokeType: "" }, // 池长默认 25
    expect: ["26.0"],
    ref: "SWOLF = 划次 + 时间/5 = 20 + 30/5 = 26.0（页面 toFixed(1)，big-val）",
  },

  // ── 出汗率 ──────────────────────────────────────────────────
  {
    slug: "sports/estimate-35",
    inputs: { pre: "70", post: "69.2", dur: "60", intake: "500", urine: "0" },
    expect: ["1.30"],
    ref: "出汗量 = (70−69.2)+500/1000 = 1.3 kg；出汗率 = 1.3/(60/60) = 1.30 L/h（页面 toFixed(2)）",
  },
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 200));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { CASES };

if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
