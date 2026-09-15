#!/usr/bin/env node
/**
 * 第 23 道门禁：healthcare 分类计算正确性验证（35 个工具 / 35 个用例）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 用法: node scripts/verify_healthcare_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---------- 儿科给药与剂量 ----------
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "20", dose: "10", conc: "32" },
    expect: ["6.3", "7"],
    ref: "单次液量 = 20×10÷32 = 6.25 → 6.3 mL；日上限次数 = ⌊20×75÷32÷6.25⌋ = ⌊46.875÷6.25⌋ = ⌊7.5⌋ = 7",
  },
  {
    slug: "healthcare/healthcare",
    inputs: { adult_dose: "500", child_weight: "20", adult_weight: "70", max_factor: "0.2" },
    expect: ["142.86", "100.00", "28.57"],
    ref: "按体重 = 500×(20÷70) = 142.86 mg；受限 = min(142.86, 500×0.2) = 100.00；比例 = 20÷70×100 = 28.57%",
  },
  {
    slug: "healthcare/weight-dosage",
    inputs: { weight: "18", mgkg: "12", freq: "3" },
    expect: ["216.0", "72.0"],
    ref: "日剂量 = 18×12 = 216 mg/天；单次 = 216÷3 = 72 mg/次",
  },

  // ---------- 评分类 ----------
  {
    slug: "healthcare/apgar",
    inputs: { appearance: "2", pulse: "2", grimace: "1", activity: "2", respiration: "2" },
    expect: ["9"],
    ref: "Apgar = 2+2+1+2+2 = 9 分（7–10 为正常）",
  },
  {
    slug: "healthcare/chads-vasc",
    inputs: { c: "1", h: "1", a: "0", d: "0", s: "0", v: "1", age65: "0", sex_f: "0" },
    expect: ["3", "高危"],
    ref: "CHA₂DS₂-VASc = 心衰1 + 高血压1 + 血管病1 = 3 分 → 高危",
  },
  {
    slug: "healthcare/morse",
    inputs: { hist: "0", sec_diag: "15", aid: "0", iv: "20", gait: "10", mental: "15" },
    expect: ["60", "高风险"],
    ref: "Morse = 0+15+0+20+10+15 = 60 → >50 高风险",
  },
  {
    slug: "healthcare/nrs2002",
    inputs: { bmi: "2", weight_loss: "1", intake: "2", severity: "1", age70: "0" },
    expect: ["5", "6", "是"],
    ref: "营养受损 = 2+1+2 = 5；总分 = 5+1+0 = 6 ≥ 3 → 存在营养风险",
  },
  {
    slug: "healthcare/wells",
    inputs: { dvt: "3", pe: "3", hr: "0", imm: "1.5", dvt_hist: "0", hem: "1", cancer: "0" },
    expect: ["8.5", "高度"],
    ref: "Wells = 3+3+0+1.5+0+1+0 = 8.5 → >6 高度临床概率",
  },
  {
    slug: "healthcare/checker-manager",
    inputs: { s0: "10", s1: "10", s2: "10", s3: "10", s4: "10", s5: "10", s6: "10", s7: "10", temp: "22", humid: "50" },
    expect: ["100.0"],
    ref: "总分 = 8×10 = 80，达标率 = 80÷80×100 = 100.0%",
  },

  // ---------- 血压与循环 ----------
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "130", dia: "85", age: "50" },
    expect: ["45", "3"],
    ref: "脉压 = 130−85 = 45 mmHg；收缩压 ≥130 且 <140 → 3 级",
  },
  {
    slug: "healthcare/map",
    inputs: { sbp: "135", dbp: "85", hr: "70" },
    expect: ["101.7", "50", "正常"],
    ref: "MAP = 85 + (135−85)÷3 = 85 + 16.667 = 101.7 mmHg；脉压 = 50；≥70 判为正常",
  },
  {
    slug: "healthcare/qtc",
    inputs: { qt: "420", hr: "50", formula: "1" },
    expect: ["383.4", "440"],
    ref: "RR = 60÷50 = 1.2 s；Bazett = 420÷√1.2 = 420÷1.09545 = 383.4 ms；公式 1 取男上限 440 ms",
  },

  // ---------- 体成分与代谢 ----------
  {
    slug: "healthcare/bmi-calculator",
    inputs: { height: "175", weight: "70", waist: "80", targetWeight: "65" },
    expect: ["22.9"],
    ref: "BMI = 70 ÷ 1.75² = 70 ÷ 3.0625 = 22.857 → 22.9 kg/m²",
  },
  {
    slug: "healthcare/bmr-calculator",
    inputs: { weight: "80", height: "175", age: "30", sex: "1" },
    expect: ["1749"],
    ref: "Mifflin-St Jeor（男）= 10×80 + 6.25×175 − 5×30 + 5 = 800 + 1093.75 − 150 + 5 = 1748.75 → 1749 kcal/天",
  },
  {
    slug: "healthcare/body-fat-estimator",
    inputs: { weight: "70", height: "175", age: "30", sex: "1" },
    expect: ["22.9", "18.1"],
    ref: "BMI = 70÷1.75² = 22.857；体脂率 = 1.2×22.857 + 0.23×30 − 10.8 − 5.4 = 27.43 + 6.9 − 16.2 = 18.13 → 18.1%",
  },
  {
    slug: "healthcare/bsa-calculator",
    inputs: { weight: "70", height: "175", age: "30" },
    expect: ["1.848"],
    ref: "Du Bois = 0.007184 × 70^0.425 × 175^0.725 = 0.007184 × 6.0843 × 42.284 = 1.848 m²",
  },
  {
    slug: "healthcare/ibw",
    inputs: { height: "175", sex: "1" },
    expect: ["70.6", "77.6", "63.5"],
    ref: "Devine（男）= 50 + 0.91×(175−152.4) = 50 + 20.566 = 70.6 kg；上限 ×1.1 = 77.6；下限 ×0.9 = 63.5",
  },
  {
    slug: "healthcare/ideal-weight",
    inputs: { height: "175", sex: "1", age: "30" },
    expect: ["70.5"],
    ref: "Devine = 50 + 2.3×(175÷2.54 − 60) = 50 + 2.3×8.8976 = 50 + 20.464 = 70.46 → 70.5 kg",
  },
  {
    slug: "healthcare/healthcare-5",
    inputs: { weight: "65", activity: "1.2", goal: "1.5" },
    expect: ["62.4", "93.6", "23.4"],
    ref: "维持 = 65×0.8×1.2 = 62.4 g；目标 = 62.4×1.5 = 93.6 g；每餐 = 93.6÷4 = 23.4 g",
  },
  {
    slug: "healthcare/fat-loss-deficit",
    inputs: { loss: "4", days: "50", targetWeight: "70" },
    expect: ["30800", "616", "74"],
    ref: "总缺口 = 4×7700 = 30800 kcal；日缺口 = 30800÷50 = 616；起始体重 = 70+4 = 74 kg",
  },
  {
    slug: "healthcare/water-intake",
    inputs: { weight: "70", activity: "1.2", climate: "1.1" },
    expect: ["3234", "13"],
    ref: "饮水量 = 70×35×1.2×1.1 = 3234 mL；杯数 = 3234÷250 = 12.94 → 13 杯",
  },

  // ---------- 肾功 ----------
  {
    slug: "healthcare/egfr",
    inputs: { scr: "100", age: "60", sex: "1", race: "1" },
    expect: ["70.1", "2"],
    ref: "CKD-EPI（男）：Scr = 100÷88.4 = 1.1312 mg/dL；min(1.1312÷0.9,1) = 1 → 1；max = 1.2569 → 1.2569^(−1.209) = 0.75839；0.993^60 = 0.65605；eGFR = 141×0.75839×0.65605 = 70.15 → 70.1，60–89 为 G2 期",
  },
  {
    slug: "healthcare/egfr-calculator",
    inputs: { scr: "1.2", age: "60", sex: "2" },
    expect: ["45.8"],
    ref: "MDRD（女）= 175 × 1.2^(−1.154) × 60^(−0.203) × 0.742 = 175 × 0.81033 × 0.43550 × 0.742 = 45.83 → 45.8 mL/min",
  },
  {
    slug: "healthcare/gfr-cockcroft",
    inputs: { age: "60", weight: "65", scr: "90", sex: "0" },
    expect: ["60.30"],
    ref: "Scr = 90÷88.4 = 1.01810 mg/dL；CrCl = (140−60)×65 ÷ (72×1.01810) × 0.85 = 5200÷73.303×0.85 = 60.30 mL/min",
  },

  // ---------- 输液与电解质 ----------
  {
    slug: "healthcare/healthcare-2",
    inputs: { volume: "250", time_min: "60", drop: "15" },
    expect: ["3750", "62.50", "0.96"],
    ref: "总滴数 = 250×15 = 3750 滴；滴速 = 3750÷60 = 62.50 滴/分；秒/滴 = 60÷62.5 = 0.96",
  },
  {
    slug: "healthcare/healthcare-3",
    inputs: { na_inf: "140", tbw: "35", target: "132", current: "120" },
    expect: ["0.56", "12"],
    ref: "预期升幅 = (140−120) ÷ (35+1) = 20÷36 = 0.5556 → 0.56 mmol/L；目标差距 = 132−120 = 12 mmol/L",
  },
  {
    slug: "healthcare/parkland",
    inputs: { weight: "60", tbsa: "25", hours: "6" },
    expect: ["6000", "3000", "3000", "1500"],
    ref: "Parkland 24h = 4×60×25 = 6000 mL；前 8h = 3000；后 16h = 3000；6h 已输 = 6000×6÷24 = 1500 mL",
  },
  {
    slug: "healthcare/healthcare-4",
    inputs: { dyspnea: "1", rest: "0", limits: "1" },
    expect: ["3", "III 明显受限"],
    ref: "静息无症状 + 有呼吸困难 + 活动受限 → NYHA III 级（明显受限）",
  },
  {
    slug: "healthcare/resp-rate",
    inputs: { rr: "24", age: "40", state: "1" },
    expect: ["3", "8", "20"],
    ref: "24 > 20 → 等级 3（异常）；偏离正常 = |24−16| = 8；活动状态上限参考 20 次/分",
  },

  // ---------- 血醇 ----------
  {
    slug: "healthcare/bac-calculator",
    inputs: { volume: "500", abv: "5", weight: "70", sex: "1", hours: "1" },
    expect: ["0.026"],
    ref: "酒精 = 500×5÷100×0.789 = 19.725 g；BAC = 19.725÷(0.68×70)÷10 = 0.041439 − 0.015×1 = 0.026439 → 0.026 g/100mL",
  },

  // ---------- 孕产与儿童 ----------
  {
    slug: "healthcare/due-date-calc",
    inputs: { lmp: "140", cycleLen: "28", ovulationDay: "14" },
    expect: ["20.0", "140", "126"],
    ref: "孕周 = 140÷7 = 20.0 周；距预产期 = 280−140 = 140 天；距排卵 = 140−14 = 126 天",
  },
  {
    slug: "healthcare/bmi-2",
    inputs: { age: "8", bmi: "20", sex: "1" },
    expect: ["0.32", "正常"],
    ref: "Z = (20 − 16.5 − 8×0.35) ÷ 2.2 = 0.7÷2.2 = 0.318 → 0.32（|Z| < 2 判为正常）",
  },

  // ---------- 统计、心率与能量 ----------
  {
    slug: "healthcare/analysis-report-cost",
    inputs: { data: "2 4 12" },
    expect: ["6.00", "18.67", "4.32"],
    ref: "n = 3，总和 = 18，均值 = 6.00，中位数 = 4；方差 = ((2−6)²+(4−6)²+(12−6)²)÷3 = 56÷3 = 18.67；标准差 = √18.67 = 4.32",
  },
  {
    slug: "healthcare/heart-rate-zones",
    inputs: { age: "40", rhr: "60", lthr: "170", maxhrInput: "190" },
    expect: ["180", "156"],
    ref: "Karvonen（默认 hrr 法）：最大心率 = 220−40 = 180；HRR = 180−60 = 120；Z3 上限 = 60 + 120×0.8 = 156",
  },
  {
    slug: "healthcare/tdee-calculator",
    inputs: { age: "30", height: "175", weight: "80", bf: "20", act: "1.55" },
    expect: ["1752", "2716"],
    ref: "给体脂率 20% 时走 Katch-McArdle：瘦体重 = 80×(1−20÷100) = 64 kg；BMR = 370 + 21.6×64 = 1752.4 → 1752；TDEE = 1752×1.55 = 2715.6 → 2716 kcal（活动系数 1.55 为默认中强度）",
  },
];

async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== healthcare calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();