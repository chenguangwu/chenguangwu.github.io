#!/usr/bin node
/**
 * investment 分类计算正确性验证（覆盖 tools/investment/ 全部 24 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed / 插值算法精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_investment_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 跑法:
 *   node scripts/verify_investment_calc.js              # 全部
 *   node scripts/verify_investment_calc.js npv-calc     # 单页
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---- 时间价值 / 年金 ----
  { slug: "investment/annuity-fv-inv",
    inputs: { PMT: "2000", r: "0.03", n: "20" },
    expect: ["53740.75"],
    ref: "FV=2000×[(1.03²⁰−1)/0.03]=53740.75" },

  { slug: "investment/annuity-pv-inv",
    inputs: { PMT: "2500", r: "0.04", n: "15" },
    expect: ["27795.97"],
    ref: "PV=2500×[1−(1.04)⁻¹⁵]/0.04=27795.97" },

  { slug: "investment/future-value-inv",
    inputs: { PV: "25000", r: "0.045", n: "12" },
    expect: ["42397.04"],
    ref: "FV=25000×(1.045)¹²=42397.04" },

  { slug: "investment/present-value-inv",
    inputs: { FV: "50000", r: "0.065", n: "9" },
    expect: ["28367.66"],
    ref: "PV=50000/(1.065)⁹=28367.66" },

  // ---- 债券 ----
  { slug: "investment/bond-price",
    inputs: { face: "1000", cr: "6", ytm: "4.5", n: "8", freq: "2" },
    expect: ["1099.84"],
    ref: "freq=2：每期票息 30、贴现率 2.25%、16 期，P=Σ30/(1.0225)^t+1000/(1.0225)¹⁶=1099.84（票息率>YTM 故溢价）" },

  { slug: "investment/bond-ytm-approx",
    inputs: { C: "60", F: "1000", P: "980", n: "6" },
    expect: ["6.40"],
    ref: "YTM≈[60+(1000−980)/6]/[(1000+980)/2]=63.3333/990=6.40%" },

  { slug: "investment/yield-spread",
    inputs: { yb: "0.062", ybm: "0.028" },
    expect: ["340"],
    ref: "Spread=(0.062−0.028)×10000=340 bps（3.40 个百分点）" },

  // ---- 现金流评价 ----
  { slug: "investment/npv-calc",
    inputs: { cf0: "-2000", cf1: "600", cf2: "800", cf3: "700", cf4: "400", r: "9" },
    expect: ["47.70"],
    ref: "NPV=−2000+600/1.09+800/1.1881+700/1.295+400/1.4116=47.70（5 期全额参与，r 以百分比输入）" },

  { slug: "investment/irr-calc",
    inputs: { cf0: "-1500", cf1: "400", cf2: "600", cf3: "700", cf4: "350" },
    expect: ["13.75"],
    ref: "二分法求 NPV=0：IRR≈13.75%（页面 5 期现金流，第四期 350 亦参与求解）" },

  { slug: "investment/payback-period",
    inputs: { cf0: "-1800", cf1: "500", cf2: "600", cf3: "500", cf4: "450" },
    expect: ["3.44 年"],
    ref: "累计：−1800、−1300、−700、−200、+250；第 3→4 期转正，插值=3+200/450=3.44 年" },

  { slug: "investment/discounted-payback",
    inputs: { cf0: "-2000", cf1: "900", cf2: "900", cf3: "900", r: "8" },
    expect: ["2.55 年"],
    ref: "折现累计：−2000、−1166.67、−444.44、+269.86；插值=2+444.44/714.34=2.55 年（页面为 4 期 cf0…cf3）" },

  { slug: "investment/profitability-index",
    inputs: { cf0: "-2500", cf1: "900", cf2: "1000", cf3: "1100", r: "7" },
    expect: ["1.045", "2612.49"],
    ref: "PV=900/1.07+1000/1.1449+1100/1.2250=2612.49；PI=2612.49/2500=1.045（页面为 4 期 cf0…cf3）" },

  // ---- 收益率口径 ----
  { slug: "investment/geometric-mean-return",
    inputs: { r: "0.20, -0.10, 0.15" },
    expect: ["7.49"],
    ref: "g=[1.20×0.90×1.15]^(1/3)−1=7.49%（算术平均 8.33% 会高估）" },

  { slug: "investment/holding-period-return",
    inputs: { p0: "45", p1: "58", d: "3" },
    expect: ["35.56", "16.00"],
    ref: "HPR=(58−45+3)/45=35.56%；总收益=58−45+3=16.00" },

  { slug: "investment/real-rate-return",
    inputs: { nom: "0.062", inf: "0.021" },
    expect: ["4.02"],
    ref: "r_real=(1.062/1.021)−1=4.02%（减法近似 6.2%−2.1%=4.1% 略偏高）" },

  { slug: "investment/roi-calc",
    inputs: { gain: "4400", cost: "4000" },
    expect: ["10.00", "400.00"],
    ref: "ROI=(4400−4000)/4000=10.00%；净收益 400.00" },

  // ---- 估值与财务比率 ----
  { slug: "investment/dividend-payout-ratio",
    inputs: { DPS: "1.5", EPS: "4" },
    expect: ["37.5"],
    ref: "DPR=1.5/4=37.5%" },

  { slug: "investment/dividend-yield",
    inputs: { dps: "3.6", price: "45" },
    expect: ["8.00"],
    ref: "股息率=3.6/45=8.00%（须避开默认 3/60=5.00%）" },

  { slug: "investment/eps-calc",
    inputs: { ni: "2400000", pref: "400000", shares: "800000" },
    expect: ["2.50"],
    ref: "EPS=(2400000−400000)/800000=2.50（须先扣优先股股利）" },

  { slug: "investment/pe-ratio",
    inputs: { price: "42", eps: "2.5" },
    expect: ["16.80"],
    ref: "P/E=42/2.5=16.80 倍" },

  { slug: "investment/retention-ratio",
    inputs: { DPR: "55" },
    expect: ["45.0"],
    ref: "b=100−55=45.0%" },

  { slug: "investment/sustainable-growth",
    inputs: { ROE: "18", b: "45" },
    expect: ["8.10"],
    ref: "g=ROE×b=18%×45%=8.10%" },

  // ---- 风险 ----
  { slug: "investment/portfolio-beta",
    inputs: { w1: "0.7", b1: "1.15", w2: "0.3", b2: "0.9" },
    expect: ["1.075"],
    ref: "βp=0.7×1.15+0.3×0.9=1.075" },

  { slug: "investment/sortino-ratio",
    inputs: { rp: "11", rf: "2.5", dd: "5" },
    expect: ["1.700"],
    ref: "索提诺=(11−2.5)/5=1.700（仅用下行波动作分母）" },
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
  console.log("==== investment calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();