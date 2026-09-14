#!/usr/bin/env node
/**
 * 第 39 道门禁：insurance 分类计算正确性验证（29 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式或已知向量），不回读页面输出。
 * 输入一律避开页面默认值（空输入默认输出 0.00/NaN），且期望值经「假通过自检」复核
 * 不等于默认输出，杜绝假通过。
 * 期望串优先取「区分度足够」的数值串（避开纯 .00 结尾隐含的 "0.00" 子串命中）。
 * 排除：
 *   - calc-pv-1 / estimate-20：通用模板，计算模式依赖 h1 标题文本判断，stub 无法还原 → 无验证意义；
 *   - mortality-table：依赖内置生命表数据，难以独立复算精确 qx；
 *   - level-premium-life：页面 resetForm() 在初始化时把 nsp 重置为 85000 并调用 calcTool，
 *     stub 注入被覆盖（与标题依赖模板同类 stub 干扰），验证无意义。
 * 用法: node scripts/verify_insurance_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "insurance/annuity-certain-pv",
    inputs: { P: "1000", i: "0.05", n: "10" },
    expect: ["7,721.73", "8,107.82"],
    ref: "v=1/1.05=0.952381；aEnd=(1−v^10)/0.05=7.72173；P·aEnd=7721.73；aBeg=7.72173×1.05=8107.82（默认空→0 避开）" },

  { slug: "insurance/annuity-nsp",
    inputs: { b: "50", ax: "8.75" },
    expect: ["437.50"],
    ref: "NSP = b×ax = 50×8.75 = 437.50（默认空→0 避开）" },

  { slug: "insurance/annuity-present",
    inputs: { pmt: "1000", rate: "5", n: "10", type: "due" },
    expect: ["8,107.82"],
    ref: "ordinaryPV=1000×(1−1.05^−10)/0.05=7721.73；due×1.05=8107.82（type 默认 ordinary→改 due 避开）" },

  { slug: "insurance/average-severity",
    inputs: { tot: "1000", n: "3" },
    expect: ["333.33"],
    ref: "平均赔付额 = 1000/3 = 333.33（默认空→0 避开）" },

  { slug: "insurance/calc-1",
    inputs: { premium: "1234.56", totalYears: "20", paidYears: "7", riderCost: "0" },
    expect: ["16,049.28"],
    ref: "remaining=20−7=13；waived=1234.56×13=16049.28（默认空→0 避开）" },

  { slug: "insurance/claim-frequency",
    inputs: { claims: "50", exposure: "1000" },
    expect: ["0.0500", "5.00"],
    ref: "f=50/1000=0.05→0.0500；出险率=5.00%（默认空→NaN 避开）" },

  { slug: "insurance/claim-reserve",
    inputs: { earnedPremium: "1000", expectLossRatio: "70", paidLoss: "400", rbns: "200", closeRate: "50", period: "0.65" },
    expect: ["700", "300", "60.0"],
    ref: "终极=1000×70%=700；IBNR=700−400−200=100；未决=200+100=300；已报赔付率=(400+200)/1000×100=60.0%（默认空→0/NaN 避开）" },

  { slug: "insurance/combined-ratio",
    inputs: { claims: "400", exp: "120", premium: "1000" },
    expect: ["52.00"],
    ref: "CR=(400+120)/1000×100=52.00%（避开页面示例默认值 533/200/1000；'承保盈利'为静态文案，不纳入期望）" },

  { slug: "insurance/complete-life-expectancy",
    inputs: { tpx: "0.9,0.95,0.98" },
    expect: ["2.830"],
    ref: "完全期望寿命=e_x 求和=0.9+0.95+0.98=2.83→2.830（默认空→0 避开）" },

  { slug: "insurance/endowment-premium",
    inputs: { B: "100000", q: "0.01", i: "0.03", n: "10" },
    expect: ["8,847.49", "8,176.37", "67,294.52"],
    ref: "逐期折现：身故现值 8176.37、满期现值 67294.52、年金系数 a=8.53、两全年保费 P=(8176.37+67294.52)/8.53=8847.49（默认空→0 避开）" },

  { slug: "insurance/expected-claim-loss",
    inputs: { freq: "2", sev: "150.4" },
    expect: ["300.80"],
    ref: "ECL = 频率×严重度 = 2×150.4 = 300.80（默认空→0 避开）" },

  { slug: "insurance/expense-ratio",
    inputs: { exp: "300", premium: "2000" },
    expect: ["15.00"],
    ref: "费用率 = 300/2000×100 = 15.00%（避开页面示例默认值 250/1000）" },

  { slug: "insurance/force-of-mortality",
    inputs: { px: "0.95" },
    expect: ["0.05129"],
    ref: "μ = −ln(0.95) = 0.051293 → 0.05129（默认空→0 避开）" },

  { slug: "insurance/gross-premium-loading",
    inputs: { pp: "600", load: "0.333" },
    expect: ["799.80"],
    ref: "毛保费 = 纯保费×(1+附加费率) = 600×1.333 = 799.80（默认空→0 避开）" },

  { slug: "insurance/ibnr-estimate",
    inputs: { ult: "1234", paid: "0.7" },
    expect: ["370.20"],
    ref: "IBNR = 终极×(1−已付比例) = 1234×0.3 = 370.20（默认空→0 避开）" },

  { slug: "insurance/ibnr-reserve",
    inputs: { reported: "500", factor: "1.625" },
    expect: ["312.50", "812.50"],
    ref: "IBNR = 已报×(因子−1) = 500×0.625 = 312.50；最终赔款 = 500×1.625 = 812.50（默认空→0 避开）" },

  { slug: "insurance/life-cover-need",
    inputs: { income: "50000", years: "20", debt: "300000", asset: "100000" },
    expect: ["1,200,000.00"],
    ref: "建议保额 = 收入×年数+负债−资产 = 50000×20+300000−100000 = 1,200,000.00（默认空→0 避开）" },

  { slug: "insurance/loss-ratio",
    inputs: { claims: "333", premium: "1000" },
    expect: ["33.30"],
    ref: "赔付率 = 333/1000×100 = 33.30%（默认空→0 避开）" },

  { slug: "insurance/mortality-prob",
    inputs: { p: "0.98", n: "5" },
    expect: ["90.392", "2.000", "9.608"],
    ref: "q=1−0.98=0.02；ₙp=0.98^5=0.903920→90.392%；ₙ年内死亡=9.608%（默认空→0/NaN 避开）" },

  { slug: "insurance/net-single-premium",
    inputs: { B: "80000", q: "0.02", i: "0.04", n: "15" },
    expect: ["15,730.63", "19.66"],
    ref: "净趸缴保费 = Σ 死亡现值 = 15730.63；占保额 = 15.7266%→19.66（避开页面示例默认值 100000/0.01/0.03/10）" },

  { slug: "insurance/premium-calc",
    inputs: { sumInsured: "100000", baseRate: "5", age: "3.5", job: "5.0", term: "0.85", payMode: "0.98" },
    expect: ["7,288.75"],
    ref: "基础=100000×5/1000=500；实际=500×3.5×5.0×0.85×0.98=7288.75（默认空→0 避开）" },

  { slug: "insurance/premium-elasticity",
    inputs: { dq: "15", dp: "5" },
    expect: ["3.00"],
    ref: "弹性 = ΔQ/ΔP = 15/5 = 3.00（默认空→0 避开）" },

  { slug: "insurance/pure-premium",
    inputs: { freq: "2", sev: "150.4" },
    expect: ["300.80"],
    ref: "纯保费 = 频率×严重度 = 2×150.4 = 300.80（默认空→0 避开）" },

  { slug: "insurance/pure-premium-rate",
    inputs: { el: "5500", exp: "1000" },
    expect: ["5.50"],
    ref: "纯费率 = 期望损失/暴露单位 = 5500/1000 = 5.50（默认空→0 避开）" },

  { slug: "insurance/stats-5",
    inputs: { data: "11,23,29,41" },
    expect: ["26.00", "104.00", "10.82"],
    ref: "均值=26.00；总和=104.00；标准差=10.82（避开页面示例默认值 10,20,30,40）" },

  { slug: "insurance/surrender-value",
    inputs: { res: "1999", rate: "0.4" },
    expect: ["799.60"],
    ref: "现金价值 = 准备金×退保比例 = 1999×0.4 = 799.60（默认空→0 避开）" },

  { slug: "insurance/survival-prob-t",
    inputs: { lxt: "800", lx: "1000" },
    expect: ["0.8000"],
    ref: "ₜp_x = l_xt/l_x = 800/1000 = 0.8000（默认空→NaN 避开）" },

  { slug: "insurance/uw-margin",
    inputs: { LR: "70", ER: "22" },
    expect: ["8.0"],
    ref: "承保利润率 = 100−(70+22) = 8.0%（避开页面示例默认值 65/30）" },

  { slug: "insurance/uw-profit",
    inputs: { premium: "1000", claims: "333", exp: "200" },
    expect: ["467.00", "46.70"],
    ref: "承保利润 = 1000−333−200 = 467.00；利润率 = 467/1000×100 = 46.70%（默认空→0 避开）" },
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0;
  const errs = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`  OK ${c.slug} (${r.via})`);
    } else {
      errs.push(c);
      console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 400)}`);
    }
  }
  console.log(`\n==== insurance calc ${pass}/${cases.length} ====`);
  if (errs.length) {
    console.log("\nfailed:");
    errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`));
    process.exit(1);
  }
}

main();
