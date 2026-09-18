#!/usr/bin/env node
/**
 * 第 22 道门禁：health 分类计算正确性验证（26 个计算器 / 30 个用例）
 *
 * 期望值全部由独立复算得出（脚本内 ref 字段写明完整算式），不回读页面输出。
 * 用法: node scripts/verify_health_calc.js
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---------- 血醇与血压 ----------
  {
    slug: "health/alcohol-units",
    inputs: { qty: "3", weight: "70", hours: "2" },
    expect: ["0.052"],
    ref: "酒精 = 5%×330mL×0.789×3÷100 = 39.06 g；BAC = 39.06÷(70×0.68×10) − 0.015×2 = 0.0821 − 0.030 = 0.052（避开默认 2 杯/65 kg/0 h）",
  },
  {
    slug: "health/blood-pressure-classifier",
    inputs: { sys: "138", dia: "88", age: "55" },
    expect: ["105 平均动脉压"],
    ref: "脉压 = 138 − 88 = 50；MAP = round(88 + 50÷3) = 105；138/88 属正常高值（避开默认 120/80/40）",
  },

  // ---------- 单位换算 ----------
  {
    slug: "health/blood-sugar-converter",
    inputs: { mmol: "7.2" },
    expect: ["130 mg/dL"],
    ref: "mg/dL = 7.2 mmol/L × 18.0182 = 129.7 → 130（避开默认 5.5）",
  },

  // ---------- 体成分 ----------
  {
    slug: "health/body-fat-calculator",
    inputs: { height: "175", weight: "78", waist: "88", neck: "40" },
    expect: ["17.7"],
    ref: "海军法（男）：BFP = 495÷(1.0324 − 0.19077·lg(88−40) + 0.15456·lg175) − 450 = 495÷1.05835 − 450 = 17.7%（避开默认 170/65/80/38）",
  },
  {
    slug: "health/body-surface-area",
    inputs: { height: "180", weight: "75" },
    expect: ["1.94"],
    ref: "Mosteller = √(180×75÷3600) = √3.75 = 1.9365 → 1.94 m²（避开默认 170/65）",
  },
  {
    slug: "health/waist-hip-ratio",
    inputs: { waist: "92", hip: "100" },
    expect: ["0.92"],
    ref: "WHR = 92 ÷ 100 = 0.92 → 高风险（避开默认 85/95）",
  },
  {
    slug: "health/ibw-calculator",
    inputs: { height: "180", actualWeight: "85" },
    expect: ["75.0"],
    ref: "Devine（男）：50 + 2.3×((180÷2.54) − 60) = 50 + 2.3×10.866 = 74.99 → 75.0 kg（避开默认 170/70）",
  },
  {
    slug: "health/child-bmi-calculator",
    inputs: { age: "8", height: "130", weight: "30" },
    expect: ["17.8"],
    ref: "BMI = 30 ÷ 1.30² = 17.75 → 17.8 kg/m²（避开默认 10 岁/140/35）",
  },
  {
    slug: "health/child-height-predictor",
    inputs: { father: "180", mother: "165" },
    expect: ["179.0"],
    ref: "男童靶身高 = (180 + 165 + 13) ÷ 2 = 179.0 cm，范围 174.0 − 184.0（避开默认 175/162）",
  },

  // ---------- 营养与代谢 ----------
  {
    slug: "health/calorie-needs",
    inputs: { age: "45", height: "175", weight: "80" },
    expect: ["2009"],
    ref: "Mifflin（男）= 10×80 + 6.25×175 − 5×45 + 5 = 1673.75 → 1674；TDEE = 1674×1.2 = 2008.8 → 2009 kcal（避开默认 30/170/65）",
  },
  {
    slug: "health/protein-needs",
    inputs: { weight: "65", age: "30", activity: "1.4" },
    expect: ["91"],
    ref: "蛋白质 = 体重 × 活动系数 = 65 × 1.4 = 91 g；安全区间 = 65×0.8 ~ 65×2.5 = 52 – 163 g/天",
  },
  {
    slug: "health/calc-1",
    inputs: { weight: "75", exercise: "45", baseFactor: "30" },
    expect: ["2500 ml"],
    ref: "基础 = 75 kg × 30 ml/kg = 2250 ml；运动 45 min 档位补 250 ml；合计 2500 ml（避开默认 65 kg/30 min）",
  },
  {
    slug: "health/water-intake-calculator",
    inputs: { weight: "72", age: "35" },
    expect: ["2500 ml"],
    ref: "基础 = 72 kg × 35 ml/kg = 2520 ml → 取整到 50 的倍数 = 2500 ml；杯数 = 2500÷250 = 10（避开默认 65/30）",
  },
  {
    slug: "health/caffeine-limit",
    inputs: { weight: "80" },
    expect: ["480 mg"],
    ref: "健康成人上限 = 6 mg/kg × 80 kg = 480 mg；≈ 480÷95 = 5.1 杯美式（避开默认 65 kg）",
  },

  // ---------- 评分与评估 ----------
  {
    slug: "health/calc-2",
    inputs: { duration: "7", latency: "10", wakings: "10", depth: "15", alertness: "15", breathing: "0" },
    expect: ["70"],
    ref: "总分 = 时长20(7–9h) + 潜伏期10 + 觉醒10 + 深度15 + 警觉15 + 呼吸0 = 70",
  },
  {
    slug: "health/calc-3",
    inputs: { phone: "4", computer: "7", tv: "2", tablet: "1.5" },
    expect: ["14.5h"],
    ref: "总时长 = 4 + 7 + 2 + 1.5 = 14.5 h（避开默认 3/6/1/0.5）",
  },

  // ---------- 临床检验 ----------
  {
    slug: "health/cholesterol-ratio",
    inputs: { total: "220", hdl: "45", ldl: "140", tg: "180" },
    expect: ["4.89", "3.11 LDL/HDL", "175 非HDL-C"],
    ref: "TC/HDL = 220÷45 = 4.89；LDL/HDL = 140÷45 = 3.11；TG/HDL = 180÷45 = 4.00；非HDL-C = 220−45 = 175（避开默认 200/50/130/150）",
  },
  {
    slug: "health/gfr-calculator",
    inputs: { age: "62", cr: "1.4", weight: "70", height: "175" },
    expect: ["57"],
    ref: "CKD-EPI 2021（男）：142 × min(1.4/0.9,1)^(−0.302) × max(1.4/0.9,1)^(−1.2) × 0.9938^62 = 142×0.5885×0.6800 = 56.8 → 57（避开默认 50 岁/1.0）",
  },
  {
    slug: "health/gfr-calculator",
    inputs: { age: "50", cr: "1.0", weight: "65", height: "170", formula: "mdrd" },
    expect: ["肾功能轻度下降"],
    ref: "MDRD（男）：186 × 1.0^(−1.154) × 50^(−0.203) = 186 × 0.4522 = 84.1 → 显示 84 mL/min/1.73m²，分期 G2 肾功能轻度下降。"
       + "原 expect「84」在 MDRD 列恒为 84（默认 CKD-EPI 也显示 84 MDRD，原逃生项），改锚定分期串「肾功能轻度下降」（CKD-EPI 默认输出为 G1 肾功能正常/良好 → 失配）。",
  },
  {
    slug: "health/gfr-calculator",
    inputs: { age: "50", cr: "1.0", weight: "65", height: "170", formula: "cockcroft" },
    expect: ["81"],
    ref: "Cockcroft-Gault（男）：(140−50) × 65 ÷ (72 × 1.0) = 5850 ÷ 72 = 81.25 → 显示 81 mL/min",
  },
  {
    slug: "health/insulin-dose",
    inputs: { currentBg: "11", targetBg: "6", icr: "12", isf: "3", carbs: "75" },
    expect: ["6.3U", "1.7U", "8.0"],
    ref: "碳水剂量 = 75÷12 = 6.25 → 6.3 U；校正剂量 = (11−6)÷3 = 1.67 → 1.7 U；合计 8.0 U（避开默认 8.5/5.5/10/2.5/60）",
  },

  // ---------- 孕产 ----------
  {
    slug: "health/pregnancy-weight-gain",
    inputs: { h: "170", w: "62", week: "28" },
    expect: ["7.3 ~ 9.5"],
    ref: "孕前 BMI = 62÷1.70² = 21.5（正常）；28 周累计增重 ≈ 7.3 ~ 9.5 kg（避开默认 165/55/20）",
  },
  {
    slug: "health/safe-period-calculator",
    inputs: { lmp: "2026-03-10", cycle: "30", period: "6" },
    expect: ["2026-03-26"],
    ref: "排卵日 = 末次月经 2026-03-10 + (30 − 14) = 2026-03-26（避开默认 2026-08-01/28/5）",
  },

  // ---------- 运动 ----------
  {
    slug: "health/one-rep-max",
    inputs: { weight: "100", reps: "8" },
    expect: ["126.7"],
    ref: "Epley：1RM = 100 × (1 + 8÷30) = 126.67 → 126.7 kg（避开默认 80 kg/5 次）",
  },
  {
    slug: "health/vo2-max-calculator",
    inputs: { cooperAge: "42", cooperDist: "2400" },
    expect: ["42.4"],
    ref: "Cooper 12 min：VO₂max = (2400 − 504.9) ÷ 44.73 = 42.37 → 42.4 ml/kg/min（避开默认 30 岁/2800 m）",
  },
  {
    slug: "health/dumbbell-weight-calculator",
    inputs: { targetWeight: "80", barWeight: "20" },
    expect: ["30 每侧配重"],
    ref: "每侧配重 = (80 − 20) ÷ 2 = 30 kg；实际总重 80 kg（避开默认 60/20）",
  },

  // ---------- 费用 ----------
  {
    slug: "health/smoking-cost-calculator",
    inputs: { perDay: "15", years: "8", price: "30" },
    expect: ["65,700"],
    ref: "每日 = 15÷20×30 = 22.5 元；总计 = 22.5 × 365 × 8 = 65,700 元（避开默认 20 支/10 年/25 元）",
  },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== health calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();