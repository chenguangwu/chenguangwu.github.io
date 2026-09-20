#!/usr/bin/env node
/**
 * life 分类关键计算逻辑独立验证（收口批次 C）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 用法：
 *   node scripts/verify_life_calc.js
 *   node scripts/verify_life_calc.js parking-fee percentage-calculator
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 停车费（先扣免费时长，再按费率，最后套封顶）────────────────
  {
    slug: "life/parking-fee",
    inputs: { hours: "5.5", rate: "10", free: "1", cap: "60" },
    expect: ["45.00"],
    ref: "计费时长 = 5.5 − 1 = 4.5 h；费用 = 4.5 × 10 = 45.00（未触及封顶 60）",
  },
  // ── 百分比（占比）────────────────────────────────────────────
  {
    slug: "life/percentage-calculator",
    inputs: { isWhatX: "30", isWhatY: "150" },
    expect: ["30 是 150 的 20%"],
    ref: "30 ÷ 150 × 100 = 20 → 显示 20%（单断言“20%”会被页面默认 ofWhatPct=20 的区块命中 → 逃生项）",
  },
  // ── 温度换算（°F = °C×9/5+32）────────────────────────────────
  {
    slug: "life/temperature-converter",
    inputs: { celsius: "25" },
    expect: ["77.00"],
    ref: "25 × 9/5 + 32 = 77 → 华氏 77.00",
  },
  // ── 每日热量（Mifflin-St Jeor 男式）──────────────────────────
  {
    slug: "life/daily-calorie-needs",
    inputs: { bmrGender: "male", bmrAge: "30", bmrHeight: "175", bmrWeight: "70" },
    expect: ["1649"],
    ref: "10×70 + 6.25×175 − 5×30 + 5 = 1648.75 → round = 1649 千卡",
  },
  // ── 饮水计划（体重×30ml + 运动 + 高温 + 特殊）─────────────────
  {
    slug: "life/drinking-water-plan",
    inputs: { w: "70", act: "mid", temp: "26", stage: "normal" },
    expect: ["2,850.00"],
    ref: "基础 70×30 = 2100；运动中档 +500；26°C（≥25）+250；特殊 0 → 2850.00 ml",
  },
  // ── 罩杯换算（上下围差 → 罩杯索引）────────────────────────────
  {
    slug: "life/bra-size-converter",
    inputs: { under: "75", upper: "90" },
    expect: ["75F"],
    ref: "差 15 cm → cupIdx = round(15/2.5)−1 = 5 → cups[6] = F；下围 75 → 国际码 75F",
  },
  // ── 日期差（含开始日 +1）─────────────────────────────────────
  {
    slug: "life/date-difference-calculator",
    inputs: { startDate: "2025-12-25", endDate: "2026-01-01" },
    expect: ["7 天"],
    ref: "getDaysDiff(12-25 → 01-01) = 7 天",
  },
  // ── 生日悖论（23 人 ≈ 50.7%）────────────────────────────────
  {
    slug: "life/birthday-paradox",
    inputs: { n: "23", d: "365" },
    expect: ["50.7297"],
    ref: "p = 1 − ∏(i=1..22)(1 − i/365) = 0.5072972 → 50.7297%",
  },
  // ── 闰年判定（格里高利历规则）────────────────────────────────
  {
    slug: "life/leap-year-checker",
    inputs: { year: "2024" },
    expect: ["闰年（366 天）"],
    ref: "2024 能被 4 整除且不能被 100 整除 → 闰年（366 天）",
  },
  // ── 单位换算（因子归一：m → cm）──────────────────────────────
  {
    slug: "life/unit-converter",
    inputs: { fromValue: "1", fromUnit: "meter", toUnit: "centimeter" },
    expect: ["100"],
    ref: "1 × factor(meter)=1 ÷ factor(cm)=0.01 = 100 → 结果 100",
  },
  // ── 选址加权模型（五项加权求和）──────────────────────────────
  {
    slug: "life/assessor-target",
    inputs: {
      traffic: "8000", competitors: "3", population: "5000",
      rent: "200", shopArea: "80", visibility: "8",
    },
    expect: ["优秀（强烈推荐）"],
    ref: "人流 80×.30 + 竞争 55×.20 + 人口 100×.20 + 租金 60×.15 + 可见 80×.15 "
       + "= 24+11+20+9+12 = 76 → ≥75 优秀（强烈推荐）",
  },
  {
    "slug": "life/analysis-cost-9",
    "inputs": {
      "data": "研发,80\n营销,50\n生产,120\n管理,30"
    },
    "expect": [
      "成本合计： 280.00",
      "最大项： 生产"
    ],
    "ref": "成本结构：合计80+50+120+30=280.00、项均70.00、最大项生产120(42.86%)（独立复算；默认 原料42/人工31/物流15/能耗9 合计97、最大项原料，注入失败即不命中）"
  },
  {
    "slug": "life/analysis-80",
    "inputs": {
      "data": "A,8,100\nB,12,240\nC,5,50"
    },
    "expect": [
      "高发环节： C",
      "平均损耗率： 6.41%"
    ],
    "ref": "损耗率：A8/100=8.00%、B12/240=5.00%、C5/50=10.00%；损耗合计25、应售合计390、平均损耗率6.41%、高发环节C（独立复算；默认 进货5/货架10/报损3 应售100/200/50 → 平均5.14%、高发报损，注入失败即不命中）"
  },
];

// ---------------------------------------------------------------- main
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
  console.log("==== life calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();