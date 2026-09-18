#!/usr/bin/env node
/**
 * legal 分类关键计算逻辑独立验证（收口批次 D，第 19 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * traffic-accident-compensation 的伤残赔偿系数缺陷已修复：原 disabilityRate = parseInt(injuryLevel)/10
 *      导致一级=10%、十级=100% 倒置（法定应为一级100%、十级10%）；现公式改为 (11 - level)/10，
 *      并已纳入下方 traffic-accident-compensation 用例做防回归断言。
 *
 * 用法：
 *   node scripts/verify_legal_calc.js
 *   node scripts/verify_legal_calc.js overtime-pay severance-pay
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 加班费（工作日150% / 休息日200% / 法定300%）────────────────────
  {
    slug: "legal/overtime-pay",
    inputs: { monthlySalary: "10000", workDays: "21.75", hoursPerDay: "8", calcType: "days", weekendDays: "2", holidayDays: "1" },
    expect: ["3218.39", "459.77", "1839.08", "1379.31"],
    ref: "日工资=10000/21.75=459.77；休息日2天×459.77×2=1839.08；法定1天×459.77×3=1379.31；合计=3218.39",
  },
  // ── 违法解除赔偿金（2N）────────────────────────────────────────────
  {
    slug: "legal/severance-pay",
    inputs: { workYears: "5", monthlySalary: "10000", salaryCap: "0", terminationType: "illegal" },
    expect: ["100,000", "50,000"],
    ref: "N=5（满5年），经济补偿=5×10000=50000；违法解除2N=100000",
  },
  // ── 经济补偿金（N）────────────────────────────────────────────────
  {
    slug: "legal/labor-compensation",
    inputs: { workYears: "3", monthlySalary: "8000", salaryCap: "0", noticeGiven: "1" },
    expect: ["24,000"],
    ref: "N=3，经济补偿=3×8000=24000（currentType 默认 N，已提前通知无代通知金）",
  },
  // ── N+1 经济补偿金（代通知金按上月工资）────────────────────────────
  {
    slug: "legal/labor-compensation-n1",
    inputs: { workYears: "4", monthlySalary: "9000", salaryCap: "0", noticeGiven: "0" },
    expect: ["45,000", "36,000"],
    ref: "N=4，经济补偿=4×9000=36000；未提前通知代通知金=9000；合计=45000",
  },
  // ── 逾期付款利息（LPR×4 上限 / 按日计息）──────────────────────────
  {
    slug: "legal/late-payment-interest",
    inputs: { principal: "100000", interestType: "lpr4x", lprRate: "3.45", dueDate: "2024-01-01", endDate: "2024-04-10", customRate: "6" },
    expect: ["LPR×4倍", "民间借贷上限"],
    ref: "天数=2024-01-01→2024-04-10=100天；年利率=3.45×4=13.8%；利息=100000×0.138×100/365=3780.82；本息=103780.82。"
       + "原 expect「3780.82」等数值在 lpr1x(默认) 下巧合也出现（原逃生项），改锚定随利率类型变化的「LPR×4倍」「民间借贷上限」（lpr1x 为「LPR 1倍」→ 失配）。",
  },
  // ── 抚养费（月收入20%-30%）────────────────────────────────────────
  {
    slug: "legal/child-support",
    inputs: { monthlyIncome: "20000", childCount: "1", childAge: "5", livingCost: "0", paymentRatio: "0.2" },
    expect: ["624,000", "4,000"],
    ref: "比例20%→月抚养费=20000×0.2=4000；至18岁=13年×12=156月×4000=624000",
  },
  // ── 离婚财产分割（净值×比例）──────────────────────────────────────
  {
    slug: "legal/divorce-property",
    inputs: { houseValue: "3000000", houseLoan: "800000", savings: "500000", carValue: "200000", otherAssets: "100000", jointDebt: "300000", splitRatio: "0.5" },
    expect: ["2,700,000", "1,350,000"],
    ref: "房产净值=220万；总资产=300万；净=270万；我方50%=135万（原用例 houseValue 取默认值，注入失败结果恰好相同 → 逃生项）",
  },
  // ── 诉讼费（财产案件阶梯费率）──────────────────────────────────────
  {
    slug: "legal/court-fee",
    inputs: { amount: "100000", caseType: "property", hasPropertySplit: "false", simplified: "false" },
    expect: ["2,300"],
    ref: "财产案件10万：100000×2.5%−200=2300（分段：≤1万50；1-10万2.5%−200）",
  },
  // ── 知识产权保护期（著作权自然人：死亡后50年）─────────────────────
  {
    slug: "legal/calc-17",
    inputs: { ipType: "copyright_natural", startDate: "2010" },
    expect: ["2060年12月31日"],
    ref: "自然人作品保护至死亡后第50年12月31日：2010+50=2060年12月31日",
  },
  // ── 年终奖个税（单独 vs 并入）─────────────────────────────────────
  {
    slug: "legal/calc-8",
    inputs: { bonus: "36000", salary: "10000", social: "0", extra: "0" },
    expect: ["¥1,080", "¥4,560", "¥7,080", "¥2,520"],
    ref: "单独：月均奖3000→3%档，税=36000×3%=1080；工资税=(120000−60000)×10%−2520=3480；合计4560。"
      + "并入：应税96000×10%−2520=7080；单独省税2520",
  },
  // ── 民间借贷利息（LPR×4 上限，到期还本付息）───────────────────────
  {
    slug: "legal/calc-interest",
    inputs: { principal: "150000", rate: "10", months: "12", method: "lump", lpr: "3.45" },
    expect: ["¥165,000", "¥15,000"],
    ref: "约定10%（≤3.45×4=13.8%受保护）；利息=150000×10%×1=15000；本息=165000（原 expect 写成默认 rate=12 的 112000/12000，与 ref 自相矛盾）",
  },
  // ── 法律援助资格（低保户免核查）────────────────────────────────────
  {
    slug: "legal/legal-aid-eligibility",
    inputs: { applicantType: "lowincome" },
    checks: ["labor"],
    expect: ["初步判断符合法律援助申请条件"],
    ref: "低保户/特困人员免予经济困难核查，且已选申请事项→符合",
  },
  // ── 工伤赔偿（一级27个月 + 90%津贴）───────────────────────────────
  {
    slug: "legal/work-injury-compensation",
    inputs: { disabilityLevel: "1", monthlySalary: "10000", avgSalary: "8000", terminateRelation: "0" },
    expect: ["270,000", "9,000"],
    ref: "一级一次性伤残补助金=27×10000=270000；1-4级津贴=10000×90%=9000/月",
  },
  // ── 交通事故残疾赔偿金（伤残系数：一级100%/十级10%，修复倒置缺陷）──
  {
    slug: "legal/traffic-accident-compensation",
    inputs: { liability: "1", injuryLevel: "1", age: "30", disposableIncome: "60000" },
    expect: ["1,200,000"],
    ref: "一级系数=1.0：残疾赔偿金=60000×20年×1.0=1,200,000（" + "100%" + "只依赖伤残等级不依赖收入，属逃生项，已剔除）",
  },
  {
    slug: "legal/traffic-accident-compensation",
    inputs: { liability: "1", injuryLevel: "10", age: "30", disposableIncome: "60000" },
    expect: ["120,000"],
    ref: "十级系数=0.1：残疾赔偿金=60000×20年×0.1=120,000（" + "10%" + "不依赖收入，属逃生项，已剔除）",
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
  console.log("==== legal calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();