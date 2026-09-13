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
    inputs: { qty: "2", weight: "65", hours: "0" },
    expect: ["0.059"],
    ref: "酒精 = 5(%ABV)×330(mL)×0.789×2÷100 = 26.04 g；BAC = 26.04÷(65×0.68×10)×1.0 − 0 = 0.0589 → 0.059",
  },
  {
    slug: "health/blood-pressure-classifier",
    inputs: { sys: "120", dia: "80", age: "40" },
    expect: ["40"],
    ref: "脉压 = 收缩压 − 舒张压 = 120 − 80 = 40；MAP = 80 + 40/3 ≈ 93（120/80 属正常血压）",
  },

  // ---------- 单位换算 ----------
  {
    slug: "health/blood-sugar-converter",
    inputs: { mmol: "5.5" },
    expect: ["99"],
    ref: "mg/dL = 5.5 mmol/L × 18.0182 = 99.1（空腹 70–99 mg/dL 为正常范围上限）",
  },

  // ---------- 体成分 ----------
  {
    slug: "health/body-fat-calculator",
    inputs: { height: "170", weight: "65", waist: "80", neck: "38" },
    expect: ["13.7"],
    ref: "美国海军法（男）：BFP = 495÷(1.0324 − 0.19077·lg(80−38) + 0.15456·lg170) − 450 = 495÷1.0675 − 450 = 13.7%",
  },
  {
    slug: "health/body-surface-area",
    inputs: { height: "170", weight: "65" },
    expect: ["1.75"],
    ref: "Mosteller：BSA = √(170×65÷3600) = √3.0694 = 1.7520 → 1.75 m²",
  },
  {
    slug: "health/waist-hip-ratio",
    inputs: { waist: "85", hip: "95" },
    expect: ["0.89"],
    ref: "WHR = 腰围 ÷ 臀围 = 85 ÷ 95 = 0.895 → 0.89（男性 <0.90 为正常）",
  },
  {
    slug: "health/ibw-calculator",
    inputs: { height: "170", actualWeight: "70" },
    expect: ["65.9"],
    ref: "Devine（男）：IBW = 50 + 2.3×(170÷2.54 − 60) = 50 + 2.3×6.93 = 65.9 kg；ABW = 65.9 + 0.4×(70−65.9) = 67.6",
  },
  {
    slug: "health/child-bmi-calculator",
    inputs: { age: "10", height: "140", weight: "35" },
    expect: ["17.9"],
    ref: "BMI = 体重 ÷ 身高² = 35 ÷ 1.40² = 17.857 → 17.9 kg/m²（10 岁 P35，属健康体重）",
  },
  {
    slug: "health/child-height-predictor",
    inputs: { father: "175", mother: "162" },
    expect: ["175.0"],
    ref: "男孩靶身高 = (父身高 + 母身高 + 13) ÷ 2 = (175 + 162 + 13) ÷ 2 = 175.0 cm（范围 170–180）",
  },

  // ---------- 营养与代谢 ----------
  {
    slug: "health/calorie-needs",
    inputs: { age: "30", height: "170", weight: "65" },
    expect: ["1568", "2430"],
    ref: "Mifflin-St Jeor（男）：BMR = 10×65 + 6.25×170 − 5×30 + 5 = 1567.5 → 1568；TDEE = 1567.5×1.55 = 2429.6 → 2430",
  },
  {
    slug: "health/protein-needs",
    inputs: { weight: "65", age: "30", activity: "1.4" },
    expect: ["91"],
    ref: "蛋白质 = 体重 × 活动系数 = 65 × 1.4 = 91 g；安全区间 = 65×0.8 ~ 65×2.5 = 52 – 163 g/天",
  },
  {
    slug: "health/calc-1",
    inputs: { weight: "65", exercise: "30", baseFactor: "30" },
    expect: ["2200", "8.8"],
    ref: "基础 = 65 × 30 = 1950 ml；运动补充 = ⌊30÷30⌋×250 = 250 ml；总量 = 2200 ml；杯数 = 2200÷250 = 8.8 杯",
  },
  {
    slug: "health/water-intake-calculator",
    inputs: { weight: "65", age: "30", gender: "male", activity: "1.0", weather: "1.0", special: "1.0" },
    expect: ["2300"],
    ref: "成年男性基础 = 65 kg × 35 ml/kg = 2275 ml；× 活动 1.0 × 天气 1.0 × 特殊 1.0 = 2275 → 取整到 50 ml 显示 2300 ml",
  },
  {
    slug: "health/caffeine-limit",
    inputs: { weight: "65" },
    expect: ["390", "4.1"],
    ref: "安全上限 = 65 × 6 = 390 mg；咖啡杯数 = 390 ÷ 95 = 4.1 杯；中等 = 65×3 = 195 mg",
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
    inputs: { phone: "3", computer: "6", tv: "1", tablet: "0.5" },
    expect: ["10.5"],
    ref: "总屏幕时长 = 3 + 6 + 1 + 0.5 = 10.5 小时/天（成人娱乐建议 ≤2h，明显超标）",
  },

  // ---------- 临床检验 ----------
  {
    slug: "health/cholesterol-ratio",
    inputs: { total: "200", hdl: "50", ldl: "130", tg: "150" },
    expect: ["4.00", "2.60", "3.00", "150"],
    ref: "TC/HDL = 200÷50 = 4.00；LDL/HDL = 130÷50 = 2.60；TG/HDL = 150÷50 = 3.00；非 HDL = 200−50 = 150",
  },
  {
    slug: "health/gfr-calculator",
    inputs: { age: "50", cr: "1.0", weight: "65", height: "170" },
    expect: ["92"],
    ref: "CKD-EPI（男，Scr 1.0）：142 × min(1/0.9,1)^(−0.302) × max(1/0.9,1)^(−1.2) × 0.9938^50 = 142×1×0.8783×0.7305 = 91.7 → 显示 92",
  },
  {
    slug: "health/gfr-calculator",
    inputs: { age: "50", cr: "1.0", weight: "65", height: "170", formula: "mdrd" },
    expect: ["84"],
    ref: "MDRD（男）：186 × 1.0^(−1.154) × 50^(−0.203) = 186 × 0.4522 = 84.1 → 显示 84 mL/min/1.73m²",
  },
  {
    slug: "health/gfr-calculator",
    inputs: { age: "50", cr: "1.0", weight: "65", height: "170", formula: "cockcroft" },
    expect: ["81"],
    ref: "Cockcroft-Gault（男）：(140−50) × 65 ÷ (72 × 1.0) = 5850 ÷ 72 = 81.25 → 显示 81 mL/min",
  },
  {
    slug: "health/insulin-dose",
    inputs: { currentBg: "8.5", targetBg: "5.5", icr: "10", isf: "2.5", carbs: "60" },
    expect: ["7"],
    ref: "碳水剂量 = 60÷10 = 6 U；校正剂量 = (8.5−5.5)÷2.5 = 1.2 U；合计 = 7.2 → 7 U",
  },

  // ---------- 孕产 ----------
  {
    slug: "health/pregnancy-weight-gain",
    inputs: { h: "165", w: "55", week: "20" },
    expect: ["20.2"],
    ref: "孕前 BMI = 55 ÷ 1.65² = 20.2 → 正常组，总增重建议 11.5–16 kg（IOM 2009）",
  },
  {
    slug: "health/safe-period-calculator",
    inputs: { lmp: "2026-08-01", cycle: "28", period: "5" },
    expect: ["2026-08-15"],
    ref: "排卵日 = 末次月经 + 周期 − 14 天 = 2026-08-01 + 14 天 = 2026-08-15；易孕期 08-10 ~ 08-19",
  },

  // ---------- 运动 ----------
  {
    slug: "health/one-rep-max",
    inputs: { weight: "80", reps: "5" },
    expect: ["93.3"],
    ref: "Epley：1RM = 80 × (1 + 5/30) = 93.3 kg；Brzycki = 80×36/32 = 90.0；O'Conner = 80×1.125 = 90.0",
  },
  {
    slug: "health/vo2-max-calculator",
    inputs: { cooperAge: "30", cooperDist: "2800" },
    expect: ["51.3"],
    ref: "Cooper 12 分钟跑：VO₂max = (2800 − 504.9) ÷ 44.73 = 51.3 mL/kg/min",
  },
  {
    slug: "health/dumbbell-weight-calculator",
    inputs: { targetWeight: "60", barWeight: "20" },
    expect: ["20"],
    ref: "每侧配重 = (60 − 20) ÷ 2 = 20 kg，由 1 片 20 kg 组成（每侧 20 kg × 2 侧 = 40 kg + 杆 20 kg = 60 kg）",
  },

  // ---------- 费用 ----------
  {
    slug: "health/smoking-cost-calculator",
    inputs: { perDay: "20", years: "10", price: "25", perPack: "20" },
    expect: ["91,250"],
    ref: "日花费 = 20÷20×25 = ¥25.0；年 = 25×365 = ¥9125；10 年 = ¥91,250（共 73,000 支）",
  },
];

async function main() {
  let pass = 0;
  const errs = [];
  for (const c of CASES) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`  ✅ ${c.slug}`);
    } else {
      errs.push(c);
      console.log(`  ❌ ${c.slug} — 期望 ${JSON.stringify(c.expect)} 未全部命中`);
      console.log(`     ref: ${c.ref}`);
      if (r.why) console.log(`     why: ${r.why}`);
    }
  }
  console.log(`\n==== health 计算验证通过 ${pass}/${CASES.length} ====`);
  if (errs.length) {
    console.log("\n未通过用例：");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
